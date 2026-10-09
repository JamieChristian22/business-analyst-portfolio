"""Local BA workbench. Standard-library Python; bind to loopback only."""
from pathlib import Path
import argparse,csv,datetime,hashlib,hmac,io,json,os,secrets,sqlite3,sys,threading,time
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlsplit,parse_qs
BASE=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(BASE/'scripts'))
from run_analysis import load_project
CONFIG=json.loads((BASE/'scripts/project_config.json').read_text())
PROJECTS={p['code']:p for p in CONFIG}
LOCK=threading.RLock()
SESSIONS={}

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def connect(path):
 c=sqlite3.connect(path,timeout=15);c.row_factory=sqlite3.Row;c.execute('PRAGMA foreign_keys=ON');return c
def password_hash(password,salt):return hashlib.pbkdf2_hmac('sha256',password.encode(),bytes.fromhex(salt),180000).hex()
def audit(c,user,action,entity,before,after):
 c.execute('INSERT INTO audit(actor,action,entity,before_json,after_json,at) VALUES(?,?,?,?,?,?)',(user,action,entity,json.dumps(before),json.dumps(after),now()))
def refresh(c,actor):
 staging=sqlite3.connect(':memory:');profiles=[]
 for p in CONFIG:
  profile=load_project(staging,p,BASE)
  profile['input_hashes']={src.name:hashlib.sha256(src.read_bytes()).hexdigest() for src in (BASE/p['folder']/'Data').glob('*.csv')}
  if profile['source_validation_exceptions']:raise ValueError(p['code']+' source validation failed; prior data retained')
  profiles.append(profile)
 # All input files validate before changing any persistent table.
 previous=c.execute('SELECT profiles_json FROM refresh_runs ORDER BY id DESC LIMIT 1').fetchone()
 old_profiles={p['project']:p for p in json.loads(previous[0])} if previous else {}
 changed=[p['project'] for p in profiles if p['project'] in old_profiles and old_profiles[p['project']].get('input_hashes')!=p['input_hashes']]
 with c:
  for p in CONFIG:
   tbl=p['tbl'];schema=staging.execute("SELECT sql FROM sqlite_master WHERE name=?",(tbl,)).fetchone()[0]
   if not c.execute("SELECT 1 FROM sqlite_master WHERE name=?",(tbl,)).fetchone():c.execute(schema)
   c.execute('DELETE FROM '+tbl)
   data=staging.execute('SELECT * FROM '+tbl).fetchall()
   c.executemany('INSERT INTO '+tbl+' VALUES('+','.join('?' for _ in data[0])+')',data)
  if not c.execute("SELECT 1 FROM sqlite_master WHERE name='finance_summary'").fetchone():c.execute('CREATE TABLE finance_summary(month TEXT,department TEXT,revenue_actual REAL)')
  c.execute('DELETE FROM finance_summary');c.executemany('INSERT INTO finance_summary VALUES(?,?,?)',staging.execute('SELECT * FROM finance_summary').fetchall())
  c.execute('INSERT INTO refresh_runs(at,actor,profiles_json) VALUES(?,?,?)',(now(),actor,json.dumps(profiles)))
  for project in changed:
   for row in c.execute("SELECT * FROM requirements WHERE project=? AND status IN ('Approved','Submitted')",(project,)).fetchall():
    c.execute("UPDATE requirements SET status='Needs review',reviewer=NULL,review_evidence=NULL,version=version+1 WHERE id=?",(row['id'],));audit(c,actor,'invalidate approval after source change',row['id'],dict(row),{'status':'Needs review'})
   for row in c.execute("SELECT uat.* FROM uat JOIN requirements ON uat.requirement_id=requirements.id WHERE requirements.project=? AND uat.status='Passed'",(project,)).fetchall():
    c.execute("UPDATE uat SET status='Blocked',actual=actual||?,version=version+1 WHERE id=?",('\nSource changed: re-execute against the new source version.',row['id']));audit(c,actor,'invalidate UAT after source change',row['id'],dict(row),{'status':'Blocked'})
   for row in c.execute("SELECT * FROM gaps WHERE project=? AND status='Closed'",(project,)).fetchall():
    c.execute("UPDATE gaps SET status='Open',reviewer=NULL,version=version+1 WHERE id=?",(row['id'],));audit(c,actor,'reopen gap after source change',row['id'],dict(row),{'status':'Open'})
  audit(c,actor,'refresh','source data',None,{'projects':6,'records':sum(p['records'] for p in profiles),'hashes':{p['project']:p['sha256'] for p in profiles}})
 staging.close()
 return profiles

def initialize(path):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 c=connect(path);accounts={}
 c.executescript('''
 CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY,role TEXT NOT NULL,salt TEXT NOT NULL,password_hash TEXT NOT NULL);
 CREATE TABLE IF NOT EXISTS requirements(id TEXT PRIMARY KEY,project TEXT NOT NULL,title TEXT NOT NULL,priority TEXT NOT NULL,owner TEXT NOT NULL,acceptance TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'Draft',submitted_by TEXT,reviewer TEXT,review_evidence TEXT,version INTEGER NOT NULL DEFAULT 1);
 CREATE TABLE IF NOT EXISTS uat(id TEXT PRIMARY KEY,requirement_id TEXT NOT NULL REFERENCES requirements(id),scenario TEXT NOT NULL,steps TEXT NOT NULL,expected TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'Not executed',actual TEXT NOT NULL DEFAULT '',evidence TEXT NOT NULL DEFAULT '',tester TEXT,executed_at TEXT,version INTEGER NOT NULL DEFAULT 1);
 CREATE TABLE IF NOT EXISTS gaps(id TEXT PRIMARY KEY,project TEXT NOT NULL,requirement_id TEXT NOT NULL REFERENCES requirements(id),title TEXT NOT NULL,current_state TEXT NOT NULL,target_state TEXT NOT NULL,priority TEXT NOT NULL,owner TEXT NOT NULL,closure TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'Open',evidence TEXT NOT NULL DEFAULT '',proposed_by TEXT,reviewer TEXT,version INTEGER NOT NULL DEFAULT 1);
 CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT,actor TEXT NOT NULL,action TEXT NOT NULL,entity TEXT NOT NULL,before_json TEXT,after_json TEXT,at TEXT NOT NULL);
 CREATE TABLE IF NOT EXISTS refresh_runs(id INTEGER PRIMARY KEY AUTOINCREMENT,at TEXT NOT NULL,actor TEXT NOT NULL,profiles_json TEXT NOT NULL);
 ''')
 if not c.execute('SELECT COUNT(*) FROM users').fetchone()[0]:
  for role in ['admin','analyst','reviewer','viewer']:
   pw=secrets.token_urlsafe(16);salt=secrets.token_hex(16)
   c.execute('INSERT INTO users VALUES(?,?,?,?)',(role,role,salt,password_hash(pw,salt)));accounts[role]=pw
 if not c.execute('SELECT COUNT(*) FROM requirements').fetchone()[0]:
  for p in CONFIG:
   for r in csv.DictReader((BASE/p['folder']/'Delivery/requirements_traceability.csv').open()):
    c.execute('INSERT INTO requirements(id,project,title,priority,owner,acceptance) VALUES(?,?,?,?,?,?)',(r['Requirement ID'],p['code'],r['Requirement'],r['Priority'],r['Owner'],r['Acceptance Criteria']))
   for r in csv.DictReader((BASE/p['folder']/'Delivery/uat_cases.csv').open()):
    c.execute('INSERT INTO uat(id,requirement_id,scenario,steps,expected) VALUES(?,?,?,?,?)',(r['Test ID'],r['Requirement ID'],r['Scenario'],r['Steps'],r['Expected Result']))
   for r in csv.DictReader((BASE/p['folder']/'Delivery/gap_register.csv').open()):
    c.execute('INSERT INTO gaps(id,project,requirement_id,title,current_state,target_state,priority,owner,closure) VALUES(?,?,?,?,?,?,?,?,?)',(r['Gap ID'],p['code'],r['Requirement ID'],r['Gap'],r['Current State'],r['Target State'],r['Priority'],r['Owner'],r['Closure Criteria']))
 c.commit()
 if not c.execute('SELECT COUNT(*) FROM refresh_runs').fetchone()[0]:refresh(c,'system initialization')
 c.close();return accounts

class APIError(Exception):
 def __init__(self,status,message):self.status=status;self.message=message

class Handler(BaseHTTPRequestHandler):
 server_version='BAWorkbench/2.0'
 def log_message(self,*args):pass
 def output(self,status,payload,headers=None):
  data=json.dumps(payload,allow_nan=False).encode();self.send_response(status)
  self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)))
  self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
  for k,v in (headers or {}).items():self.send_header(k,v)
  self.end_headers();self.wfile.write(data)
 def session(self):
  cookies={s.strip().split('=',1)[0]:s.strip().split('=',1)[1] for s in self.headers.get('Cookie','').split(';') if '=' in s}
  session=SESSIONS.get(cookies.get('ba_session',''))
  if not session or session['expires']<time.time():raise APIError(401,'Sign in required')
  return session
 def permit(self,s,*roles):
  if s['role'] not in roles:raise APIError(403,'Your role cannot perform this action')
 def do_GET(self):
  try:
   parts=urlsplit(self.path)
   if parts.path=='/':
    data=(Path(__file__).parent/'index.html').read_bytes();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; object-src 'none'; frame-ancestors 'none'");self.end_headers();self.wfile.write(data);return
   s=self.session();params={k:v[0] for k,v in parse_qs(parts.query).items()};c=connect(self.server.db_path)
   try:
    if parts.path=='/api/session':result={k:s[k] for k in ['username','role','csrf']}
    elif parts.path=='/api/projects':result=[{k:p[k] for k in ['code','title','decision','limitations','dims']} for p in CONFIG]
    elif parts.path=='/api/records':
     project=params.get('project','');where=' WHERE project=?' if project else '';args=(project,) if project else ()
     result={'requirements':[dict(r) for r in c.execute('SELECT * FROM requirements'+where+' ORDER BY id',args)],'gaps':[dict(r) for r in c.execute('SELECT * FROM gaps'+where+' ORDER BY id',args)],'uat':[dict(r) for r in c.execute('SELECT uat.*,requirements.project FROM uat JOIN requirements ON requirements.id=uat.requirement_id'+(' WHERE requirements.project=?' if project else '')+' ORDER BY uat.id',args)]}
    elif parts.path=='/api/audit':
     self.permit(s,'admin','reviewer');result=[dict(r) for r in c.execute('SELECT * FROM audit ORDER BY id DESC LIMIT 200')]
    elif parts.path=='/api/refresh':result=dict(c.execute('SELECT id,at,actor,profiles_json FROM refresh_runs ORDER BY id DESC LIMIT 1').fetchone())
    elif parts.path in ['/api/dashboard','/api/export']:
     p=PROJECTS.get(params.get('project'))
     if not p:raise APIError(400,'Select a valid project')
     dim=params.get('dim','');value=params.get('value','');month=params.get('month','')
     allowed_dims=['department'] if p['code']=='FIN' else p['dims']
     if dim and dim not in allowed_dims:raise APIError(400,'Invalid dimension')
     if month and not p['period']:raise APIError(400,'This snapshot has no reporting month')
     opts={d:[r[0] for r in c.execute(f'SELECT DISTINCT "{d}" FROM {p["tbl"]} ORDER BY "{d}"')] for d in allowed_dims}
     if dim and value and value not in opts[dim]:raise APIError(400,'Invalid dimension value')
     months=[r[0] for r in c.execute('SELECT DISTINCT month FROM '+p['tbl']+' ORDER BY month')] if p['period'] else []
     if month and month not in months:raise APIError(400,'Invalid reporting month')
     mem=sqlite3.connect(':memory:');mem.row_factory=sqlite3.Row;c.backup(mem)
     clauses=[];values=[]
     if month:clauses.append('month=?');values.append(month)
     if dim and value:clauses.append('"'+dim+'"=?');values.append(value)
     tbl=p['tbl'];mem.execute('ALTER TABLE '+tbl+' RENAME TO original_source')
     mem.execute('CREATE TABLE '+tbl+' AS SELECT * FROM original_source'+(' WHERE '+' AND '.join(clauses) if clauses else ''),values)
     if p['code']=='FIN':
      if month:mem.execute('DELETE FROM finance_summary WHERE month<>?',(month,))
      if dim=='department' and value:mem.execute('DELETE FROM finance_summary WHERE department<>?',(value,))
     tables=[]
     for query in p['queries']:
      sql=(BASE/p['folder']/'SQL'/(query['id']+'.sql')).read_text();cursor=mem.execute(sql);allrows=[dict(r) for r in cursor.fetchall()]
      tables.append({'id':query['id'],'title':query['title'],'rows':allrows,'columns':[x[0] for x in cursor.description]})
     count=mem.execute('SELECT COUNT(*) FROM '+tbl).fetchone()[0]
     offset=max(0,int(params.get('offset','0')))
     detail=[] if s['role']=='viewer' else [dict(r) for r in mem.execute('SELECT * FROM '+tbl+' ORDER BY source_row LIMIT 100 OFFSET ?',(offset,))]
     result={'project':p['code'],'record_count':count,'months':months,'options':opts,'tables':tables,'detail':detail,'offset':offset,'detail_allowed':s['role']!='viewer'}
     if parts.path=='/api/export':
      qid=params.get('query','Q01');chosen=next((t for t in tables if t['id']==qid),None)
      if qid=='detail':
       self.permit(s,'admin','analyst','reviewer');cur=mem.execute('SELECT * FROM '+tbl+' ORDER BY source_row');chosen={'columns':[x[0] for x in cur.description],'rows':[dict(r) for r in cur.fetchall()]}
      if not chosen:raise APIError(400,'Invalid export query')
      stream=io.StringIO();w=csv.DictWriter(stream,fieldnames=chosen['columns']);w.writeheader();w.writerows(chosen['rows']);data=stream.getvalue().encode()
      with c:audit(c,s['username'],'export',p['code']+'/'+qid,None,{'rows':len(chosen['rows']),'filters':params})
      self.send_response(200);self.send_header('Content-Type','text/csv; charset=utf-8');self.send_header('Content-Disposition',f'attachment; filename="{p["code"]}_{qid}.csv"');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data);mem.close();return
     mem.close()
    else:raise APIError(404,'Unknown endpoint')
    self.output(200,result)
   finally:c.close()
  except APIError as e:self.output(e.status,{'error':e.message})
  except (ValueError,KeyError) as e:self.output(400,{'error':str(e)})
  except Exception:self.output(500,{'error':'Request failed; inspect the local source contract or server configuration'})
 def do_POST(self):
  try:
   # Reject cross-site requests to the loopback demo.
   origin=self.headers.get('Origin')
   if origin and origin!=f'http://{self.headers.get("Host")}':raise APIError(403,'Cross-origin write rejected')
   length=int(self.headers.get('Content-Length','0'))
   if length>100000:raise APIError(413,'Request too large')
   body=json.loads(self.rfile.read(length) or '{}');path=urlsplit(self.path).path
   with LOCK:
    c=connect(self.server.db_path)
    try:
     if path=='/api/login':
      user=c.execute('SELECT * FROM users WHERE username=?',(body.get('username',''),)).fetchone()
      if not user or not hmac.compare_digest(password_hash(str(body.get('password','')),user['salt']),user['password_hash']):raise APIError(401,'Invalid credentials')
      token=secrets.token_urlsafe(32);s={'username':user['username'],'role':user['role'],'csrf':secrets.token_urlsafe(24),'expires':time.time()+3600};SESSIONS[token]=s
      with c:audit(c,s['username'],'login','session',None,{'role':s['role']})
      self.output(200,{k:s[k] for k in ['username','role','csrf']},{'Set-Cookie':'ba_session='+token+'; HttpOnly; SameSite=Strict; Path=/; Max-Age=3600'});return
     s=self.session()
     if not hmac.compare_digest(self.headers.get('X-CSRF-Token',''),s['csrf']):raise APIError(403,'CSRF token required')
     if path=='/api/logout':
      for token,v in list(SESSIONS.items()):
       if v is s:del SESSIONS[token]
      self.output(200,{'ok':True},{'Set-Cookie':'ba_session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0'});return
     if path=='/api/refresh':
      self.permit(s,'admin');profiles=refresh(c,s['username']);self.output(200,{'ok':True,'records':sum(p['records'] for p in profiles)});return
     table={'/api/uat':'uat','/api/requirement':'requirements','/api/gap':'gaps'}.get(path)
     if not table:raise APIError(404,'Unknown endpoint')
     row=c.execute('SELECT * FROM '+table+' WHERE id=?',(body.get('id'),)).fetchone()
     if not row:raise APIError(404,'Record not found')
     before=dict(row)
     if body.get('version')!=row['version']:raise APIError(409,'Record changed; reload before saving')
     status=body.get('status','');evidence=str(body.get('evidence','')).strip()
     with c:
      if table=='uat':
       self.permit(s,'analyst','reviewer');actual=str(body.get('actual','')).strip()
       if status not in ['Not executed','Passed','Failed','Blocked']:raise APIError(400,'Invalid UAT status')
       if status!='Not executed' and (not actual or not evidence):raise APIError(400,'Actual result and evidence are required')
       c.execute('UPDATE uat SET status=?,actual=?,evidence=?,tester=?,executed_at=?,version=version+1 WHERE id=?',(status,actual,evidence,s['username'] if status!='Not executed' else None,now() if status!='Not executed' else None,row['id']))
       r=c.execute('SELECT * FROM requirements WHERE id=?',(row['requirement_id'],)).fetchone()
       if r['status'] in ['Approved','Submitted']:
        c.execute("UPDATE requirements SET status='Needs review',reviewer=NULL,review_evidence=NULL,version=version+1 WHERE id=?",(r['id'],));audit(c,s['username'],'invalidate approval',r['id'],dict(r),{'status':'Needs review','reason':'UAT changed'})
      elif table=='requirements':
       if status=='Submitted':
        self.permit(s,'analyst');c.execute("UPDATE requirements SET status='Submitted',submitted_by=?,reviewer=NULL,review_evidence=NULL,version=version+1 WHERE id=?",(s['username'],row['id']))
       elif status in ['Approved','Rejected']:
        self.permit(s,'reviewer')
        if row['status']!='Submitted':raise APIError(409,'Submit before review')
        if row['submitted_by']==s['username']:raise APIError(403,'Submitter cannot approve their own record')
        if not evidence:raise APIError(400,'Review evidence is required')
        if status=='Approved':
         tests=c.execute('SELECT * FROM uat WHERE requirement_id=?',(row['id'],)).fetchall()
         if len(tests)!=3 or any(t['status']!='Passed' or not t['evidence'] or not t['actual'] for t in tests):raise APIError(409,'All three UAT cases must pass with evidence')
        c.execute('UPDATE requirements SET status=?,reviewer=?,review_evidence=?,version=version+1 WHERE id=?',(status,s['username'],evidence,row['id']))
       else:raise APIError(400,'Invalid requirement transition')
      else:
       if status=='Proposed closure':
        self.permit(s,'analyst')
        if not evidence:raise APIError(400,'Closure evidence is required')
        c.execute('UPDATE gaps SET status=?,evidence=?,proposed_by=?,reviewer=NULL,version=version+1 WHERE id=?',(status,evidence,s['username'],row['id']))
       elif status in ['Closed','Open']:
        self.permit(s,'reviewer')
        if row['status']!='Proposed closure':raise APIError(409,'Propose closure before review')
        if not evidence:raise APIError(400,'Reviewer rationale is required')
        c.execute('UPDATE gaps SET status=?,evidence=?,reviewer=?,version=version+1 WHERE id=?',(status,row['evidence']+'\nReviewer: '+evidence,s['username'],row['id']))
       else:raise APIError(400,'Invalid gap transition')
      after=dict(c.execute('SELECT * FROM '+table+' WHERE id=?',(row['id'],)).fetchone());audit(c,s['username'],'update '+table,row['id'],before,after)
     self.output(200,after)
    finally:c.close()
  except APIError as e:self.output(e.status,{'error':e.message})
  except (ValueError,TypeError) as e:self.output(400,{'error':str(e)})
  except Exception:self.output(500,{'error':'Update failed; no workflow changes committed'})

def make_server(db,port=0):
 server=ThreadingHTTPServer(('127.0.0.1',port),Handler);server.db_path=str(db);return server
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8765);parser.add_argument('--db',default=str(BASE/'Runtime/workbench.sqlite'));args=parser.parse_args()
 accounts=initialize(args.db)
 if accounts:
  text='LOCAL DEMO ACCOUNTS - generated on this computer\n'+''.join(u+': '+pw+'\n' for u,pw in accounts.items())
  credentials=Path(args.db).parent/'LOCAL_ACCOUNTS.txt';credentials.write_text(text);os.chmod(credentials,0o600);print(text+'Saved to '+str(credentials),flush=True)
 print(f'Open http://127.0.0.1:{args.port} (loopback-only local demo)',flush=True)
 make_server(args.db,args.port).serve_forever()
