from pathlib import Path
import csv,http.cookiejar,json,shutil,sqlite3,tempfile,threading,unittest,urllib.request,urllib.error,datetime
import server

class Client:
 def __init__(self,base,user,password):
  self.base=base;self.cookies=http.cookiejar.CookieJar();self.opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies));self.csrf=''
  status,data=self.request('/api/login',{'username':user,'password':password});assert status==200;self.csrf=data['csrf']
 def request(self,path,body=None,csrf=True,origin=None):
  headers={}
  if body is not None:headers={'Content-Type':'application/json','X-CSRF-Token':self.csrf if csrf else ''}
  if origin:headers['Origin']=origin
  req=urllib.request.Request(self.base+path,data=None if body is None else json.dumps(body).encode(),headers=headers)
  try:r=self.opener.open(req)
  except urllib.error.HTTPError as e:r=e
  raw=r.read();return r.status,json.loads(raw) if r.headers.get_content_type()=='application/json' else raw

class SystemTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory();cls.seed=Path(cls.temp.name)/'seed.sqlite';cls.accounts=server.initialize(cls.seed)
 @classmethod
 def tearDownClass(cls):cls.temp.cleanup()
 def setUp(self):
  self.db=Path(self.temp.name)/'active.sqlite';shutil.copyfile(self.seed,self.db);self.http=server.make_server(self.db);self.thread=threading.Thread(target=self.http.serve_forever,daemon=True);self.thread.start();base='http://127.0.0.1:'+str(self.http.server_port)
  self.clients={r:Client(base,r,pw) for r,pw in self.accounts.items()}
 def tearDown(self):self.http.shutdown();self.http.server_close();self.thread.join()
 def records(self,role='analyst'):return self.clients[role].request('/api/records?project=MKT')[1]
 def req(self):return self.records()['requirements'][0]
 def post_req(self,role,status):
  r=self.req();return self.clients[role].request('/api/requirement',{'id':r['id'],'version':r['version'],'status':status,'evidence':'Temporary automated test evidence; not business UAT'})
 def pass_tests(self):
  for t in self.records()['uat'][:3]:
   code,_=self.clients['analyst'].request('/api/uat',{'id':t['id'],'version':t['version'],'status':'Passed','actual':'Executed fixture in temporary automated test','evidence':'test_system.py fixture only'})
   self.assertEqual(code,200)
 def test_unauthenticated_denied(self):
  try:urllib.request.urlopen('http://127.0.0.1:'+str(self.http.server_port)+'/api/projects')
  except urllib.error.HTTPError as e:self.assertEqual(e.code,401)
  else:self.fail('Anonymous access permitted')
 def test_all_six_dashboards_execute(self):
  for p in server.CONFIG:
   code,result=self.clients['viewer'].request('/api/dashboard?project='+p['code']);self.assertEqual(code,200);self.assertEqual(len(result['tables']),5);self.assertGreater(result['record_count'],0)
 def test_filtered_sales_matches_independent_source(self):
  code,result=self.clients['analyst'].request('/api/dashboard?project=REG&month=2025-07&dim=zone&value=1')
  data=list(csv.DictReader((server.BASE/'Regional_Sales_Performance_Project/Data/regional_sales_tableau_aligned.csv').open()))
  expected=sum(float(r['Sales']) for r in data if r['Month']=='2025-07' and r['Zone']=='1')
  self.assertEqual(code,200);self.assertAlmostEqual(result['tables'][0]['rows'][0]['sales'],expected,places=2)
 def test_viewer_detail_denied(self):
  code,data=self.clients['viewer'].request('/api/dashboard?project=CRM');self.assertEqual(data['detail'],[])
  self.assertEqual(self.clients['viewer'].request('/api/export?project=CRM&query=detail')[0],403)
 def test_filter_injection_and_unknown_values_rejected(self):
  self.assertEqual(self.clients['viewer'].request('/api/dashboard?project=REG&dim=zone%3BDROP%20TABLE%20users&value=1')[0],400)
  self.assertEqual(self.clients['viewer'].request('/api/dashboard?project=REG&month=2027-01')[0],400)
 def test_csv_export_matches_selection(self):
  code,raw=self.clients['analyst'].request('/api/export?project=CRM&query=Q02');self.assertEqual(code,200);self.assertIn(b'weighted_open_pipeline',raw)
  self.assertIn(b'53550',raw)
 def test_readonly_and_csrf_enforced(self):
  t=self.records()['uat'][0];payload={'id':t['id'],'version':t['version'],'status':'Passed','actual':'x','evidence':'x'}
  self.assertEqual(self.clients['viewer'].request('/api/uat',payload)[0],403)
  self.assertEqual(self.clients['analyst'].request('/api/uat',payload,csrf=False)[0],403)
  self.assertEqual(self.clients['analyst'].request('/api/uat',payload,origin='https://example.invalid')[0],403)
 def test_uat_requires_actual_and_evidence(self):
  t=self.records()['uat'][0];self.assertEqual(self.clients['analyst'].request('/api/uat',{'id':t['id'],'version':t['version'],'status':'Passed','actual':'','evidence':''})[0],400)
 def test_stale_update_conflict(self):
  t=self.records()['uat'][0];payload={'id':t['id'],'version':t['version'],'status':'Blocked','actual':'Fixture missing','evidence':'Temporary test'}
  self.assertEqual(self.clients['analyst'].request('/api/uat',payload)[0],200);self.assertEqual(self.clients['analyst'].request('/api/uat',payload)[0],409)
 def test_independent_approval_gate(self):
  self.assertEqual(self.post_req('analyst','Submitted')[0],200)
  self.assertEqual(self.post_req('reviewer','Approved')[0],409)
  self.assertEqual(self.post_req('analyst','Approved')[0],403)
  self.assertEqual(self.post_req('admin','Approved')[0],403)
  self.pass_tests();self.assertEqual(self.post_req('analyst','Submitted')[0],200);self.assertEqual(self.post_req('reviewer','Approved')[0],200)
 def test_uat_change_invalidates_approval(self):
  self.pass_tests();self.post_req('analyst','Submitted');self.post_req('reviewer','Approved');t=self.records()['uat'][0]
  self.clients['analyst'].request('/api/uat',{'id':t['id'],'version':t['version'],'status':'Failed','actual':'Regression found','evidence':'Temporary fixture'})
  self.assertEqual(self.req()['status'],'Needs review');self.assertEqual(self.post_req('reviewer','Approved')[0],409)
 def test_gap_closure_requires_proposal_and_review(self):
  g=self.records()['gaps'][0];payload={'id':g['id'],'version':g['version'],'status':'Closed','evidence':'Temporary test'}
  self.assertEqual(self.clients['reviewer'].request('/api/gap',payload)[0],409)
  payload['status']='Proposed closure';self.assertEqual(self.clients['analyst'].request('/api/gap',payload)[0],200)
  g=self.records()['gaps'][0];payload.update(version=g['version'],status='Closed');self.assertEqual(self.clients['analyst'].request('/api/gap',payload)[0],403);self.assertEqual(self.clients['reviewer'].request('/api/gap',payload)[0],200)
 def test_audit_and_persistence(self):
  t=self.records()['uat'][0];self.clients['analyst'].request('/api/uat',{'id':t['id'],'version':t['version'],'status':'Blocked','actual':'Missing fixture','evidence':'Test evidence'})
  code,log=self.clients['reviewer'].request('/api/audit');self.assertEqual(code,200);self.assertTrue(any(r['entity']==t['id'] and r['actor']=='analyst' for r in log));self.assertEqual(self.clients['viewer'].request('/api/audit')[0],403)
  c=server.connect(self.db);self.assertEqual(c.execute('SELECT status FROM uat WHERE id=?',(t['id'],)).fetchone()[0],'Blocked');c.close()
 def test_refresh_role_and_workflow_preservation(self):
  self.assertEqual(self.clients['analyst'].request('/api/refresh',{})[0],403)
  t=self.records()['uat'][0];self.clients['analyst'].request('/api/uat',{'id':t['id'],'version':t['version'],'status':'Blocked','actual':'Missing fixture','evidence':'Temporary test'})
  self.assertEqual(self.clients['admin'].request('/api/refresh',{})[0],200);self.assertEqual(self.records()['uat'][0]['status'],'Blocked')
 def test_bad_refresh_leaves_previous_data(self):
  testbase=Path(self.temp.name)/'invalid_sources'
  for p in server.CONFIG:
   dst=testbase/p['folder']/'Data';dst.mkdir(parents=True,exist_ok=True)
   for src in (server.BASE/p['folder']/'Data').glob('*.csv'):shutil.copyfile(src,dst/src.name)
  (testbase/server.CONFIG[0]['folder']/'Data'/server.CONFIG[0]['source']).write_text('bad_header\n1\n')
  old=server.BASE;server.BASE=testbase;c=server.connect(self.db)
  try:
   previous=c.execute('SELECT COUNT(*),SUM(gmv) FROM marketplace').fetchone();runs=c.execute('SELECT COUNT(*) FROM refresh_runs').fetchone()[0]
   with self.assertRaises(ValueError):server.refresh(c,'temporary test')
   self.assertEqual(tuple(c.execute('SELECT COUNT(*),SUM(gmv) FROM marketplace').fetchone()),tuple(previous));self.assertEqual(c.execute('SELECT COUNT(*) FROM refresh_runs').fetchone()[0],runs)
  finally:server.BASE=old;c.close()
 def test_changed_source_invalidates_prior_acceptance(self):
  self.pass_tests();self.post_req('analyst','Submitted');self.post_req('reviewer','Approved')
  testbase=Path(self.temp.name)/'changed_sources'
  for p in server.CONFIG:
   dst=testbase/p['folder']/'Data';dst.mkdir(parents=True,exist_ok=True)
   for src in (server.BASE/p['folder']/'Data').glob('*.csv'):shutil.copyfile(src,dst/src.name)
  path=testbase/'Amazon_Marketplace_Analytics_Project/Data/amazon_marketplace_aligned.csv'
  rows=list(csv.DictReader(path.open()));fields=list(rows[0]);rows[0]['GMV']=str(float(rows[0]['GMV'])+10)
  with path.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
  old=server.BASE;server.BASE=testbase;c=server.connect(self.db)
  try:
   server.refresh(c,'temporary source-change test')
   self.assertEqual(c.execute("SELECT status FROM requirements WHERE id='MKT-REQ-01'").fetchone()[0],'Needs review')
   self.assertEqual(c.execute("SELECT status FROM uat WHERE id='MKT-UAT-01-A'").fetchone()[0],'Blocked')
  finally:server.BASE=old;c.close()

if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(SystemTests)
 result=unittest.TextTestRunner(verbosity=2).run(suite)
 report={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'test_names':unittest.defaultTestLoader.getTestCaseNames(SystemTests),'scope':'HTTP integration tests against temporary seeded SQLite databases; generated credentials and test approvals are discarded. Not external business UAT.'}
 (server.BASE/'Quality/local_system_tests.json').write_text(json.dumps(report,indent=2))
 raise SystemExit(not result.wasSuccessful())
