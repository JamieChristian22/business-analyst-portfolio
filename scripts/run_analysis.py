"""Dependency-free portfolio analysis. Run from any working directory."""
from pathlib import Path
import argparse,csv,json,sqlite3,hashlib,datetime,collections,re

BASE=Path(__file__).resolve().parent.parent

def readcsv(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);return reader.fieldnames,list(reader)

def load_project(db,p,base=BASE):
    path=base/p['folder']/'Data'/p['source']
    headers,raw=readcsv(path)
    if headers!=list(p['fields']):
        raise ValueError(f"{p['code']}: source schema changed; review mappings")
    cols=['source_row INTEGER PRIMARY KEY']+[f'"{v}" '+('REAL NOT NULL' if v in p['nums'] else 'TEXT NOT NULL') for v in p['fields'].values()]
    db.execute(f'CREATE TABLE {p["tbl"]} ({",".join(cols)})')
    records=[]
    for i,row in enumerate(raw,1):
        vals=[]
        for source,target in p['fields'].items():
            value=row[source]
            if value is None or value.strip()=='':raise ValueError(f'{p["code"]} row {i}: missing {source}')
            if target in p['nums']:
                value=float(value)
                if not (-1e300<value<1e300):raise ValueError('nonfinite numeric input')
            vals.append(value)
        records.append([i,*vals])
    db.executemany(f'INSERT INTO {p["tbl"]} VALUES ({",".join("?" for _ in cols)})',records)
    if p['code']=='FIN':
        _,summary=readcsv(base/p['folder']/'Data'/'fpna_dashboard_aligned.csv')
        db.execute('CREATE TABLE finance_summary(month TEXT,department TEXT,revenue_actual REAL)')
        db.executemany('INSERT INTO finance_summary VALUES(?,?,?)',[(r['MonthYear'],r['Department'],float(r['Revenue Actual'])) for r in summary])
    violations=[]
    if p['code']=='ECOM':
        violations=db.execute('SELECT source_row FROM ecommerce WHERE views<carts OR carts<checkouts OR checkouts<purchases OR purchases<0').fetchall()
    elif p['code']=='CRM':
        violations=db.execute("SELECT source_row FROM pipeline WHERE probability<0 OR probability>1 OR amount<0 OR stage NOT IN ('Qualify','Meet','Proposal','Negotiate','Closed Won','Closed Lost') OR (stage='Closed Won' AND probability<>1) OR (stage='Closed Lost' AND probability<>0)").fetchall()
    elif p['code']=='REG':
        violations=db.execute('SELECT restaurant_id,month,COUNT(*) FROM restaurant_sales GROUP BY restaurant_id,month HAVING COUNT(*)>1').fetchall()
        violations+=db.execute('SELECT restaurant_id FROM restaurant_sales GROUP BY restaurant_id HAVING COUNT(DISTINCT city)>1 OR COUNT(DISTINCT zone)>1').fetchall()
    elif p['code']=='FIN':
        violations=db.execute("SELECT source_row FROM finance WHERE scenario NOT IN ('Actual','Budget') OR account_category NOT IN ('Revenue','COGS','OpEx') OR amount<0").fetchall()
    elif p['code']=='MKT':
        violations=db.execute('SELECT source_row FROM marketplace WHERE gmv<0 OR platform_revenue<0 OR orders<0 OR units<0').fetchall()
    elif p['code']=='ADS':
        violations=db.execute('SELECT source_row FROM advertising WHERE cost<0 OR revenue<0 OR impressions<clicks OR clicks<conversions OR conversions<0').fetchall()
    if p['period']:
        period_values=sorted({r[p['period']] for r in raw})
        for month in period_values:
            if not re.fullmatch(r'\d{4}-(0[1-9]|1[0-2])',month):raise ValueError('invalid month')
    else:period_values=[]
    profile={
      'project':p['code'],'source_file':p['source'],'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
      'records':len(raw),'fields':headers,'periods':period_values,
      'complete_repeated_rows':len(raw)-len({tuple(r.values()) for r in raw}),
      'source_validation_exceptions':len(violations),'exception_examples':violations[:10],
      'deduplication':'None. Source rows are retained. Business-key exceptions must be investigated.',
      'lineage':'source_row is the one-based data record number after the CSV header.',
      'dimensions':{source:sorted({r[source] for r in raw}) for source,target in p['fields'].items() if target in p['dims'] and len({r[source] for r in raw})<=25},
    }
    return profile

def run(base=BASE):
    config=json.loads((base/'scripts'/'project_config.json').read_text())
    logs=[]
    for p in config:
        db=sqlite3.connect(':memory:');db.row_factory=sqlite3.Row
        profile=load_project(db,p,base)
        results=base/p['folder']/'Analysis';results.mkdir(exist_ok=True)
        (results/'data_profile.json').write_text(json.dumps(profile,indent=2))
        for q in p['queries']:
            sql=(base/p['folder']/'SQL'/f"{q['id']}.sql").read_text()
            cursor=db.execute(sql);rows=cursor.fetchall();headers=[d[0] for d in cursor.description]
            with (results/f"{q['id']}.csv").open('w',newline='') as f:
                writer=csv.writer(f);writer.writerow(headers);writer.writerows(rows)
            logs.append({'project':p['code'],'query':q['id'],'rows':len(rows),'result':str((results/f"{q['id']}.csv").relative_to(base))})
        # Control queries are executed even when a production data exception exists.
        # Exceptions remain visible; a production release requires disposition.
        db.close()
    log={'executed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sqlite_version':sqlite3.sqlite_version,'queries':logs}
    (base/'Quality'/'analysis_run.json').write_text(json.dumps(log,indent=2))
    print(f'Executed {len(logs)} queries across {len(config)} projects.')

if __name__=='__main__':run()
