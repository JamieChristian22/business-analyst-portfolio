"""Independent source reconciliation and adversarial query fixtures."""
from pathlib import Path
import csv,json,sqlite3,math,datetime,sys,re
sys.path.insert(0,str(Path(__file__).resolve().parent))
from run_analysis import load_project,BASE

checks=[]
def check(name,condition,detail=''):
    checks.append({'check':name,'status':'PASS' if condition else 'FAIL','detail':str(detail)})
def eq(a,b,tol=.01):return math.isclose(a,b,rel_tol=0,abs_tol=tol)
def rows(path):return list(csv.DictReader(path.open()))
def q(db,p,n):return db.execute((BASE/p['folder']/'SQL'/f'Q{n:02}.sql').read_text()).fetchall()

config=json.loads((BASE/'scripts'/'project_config.json').read_text())
for p in config:
    db=sqlite3.connect(':memory:');db.row_factory=sqlite3.Row
    profile=load_project(db,p)
    raw=rows(BASE/p['folder']/'Data'/p['source'])
    check(p['code']+' ingestion count',db.execute(f'SELECT COUNT(*) FROM {p["tbl"]}').fetchone()[0]==len(raw),len(raw))
    check(p['code']+' source validity',profile['source_validation_exceptions']==0,profile['source_validation_exceptions'])
    data=q(db,p,1)
    if p['code']=='FIN':
        for r in data:
            independent=sum(float(x['Amount']) for x in raw if x['Scenario']==r['scenario'] and x['AccountCategory']==r['account_category'])
            check('FIN '+r['scenario']+' '+r['account_category']+' source control',eq(r['amount'],independent),r['amount'])
        rec=q(db,p,4);different=sum(r['disposition']!='MATCH' for r in rec)
        check('FIN discrepancy report retains every comparison',len(rec)==30,len(rec))
        # Detection, not business approval: differences are expected to stay unresolved.
        check('FIN reconciliation dispositions match arithmetic',all((r['disposition']=='MATCH')==(r['difference'] is not None and abs(r['difference'])<=.01) for r in rec),f'{different} unresolved revenue comparisons; matching does not imply business approval')
        check('FIN department variance reconciles',eq(sum(r['revenue_variance'] for r in q(db,p,3)),sum(r['revenue_variance'] for r in q(db,p,2))))
    else:
        target={'MKT':'gmv','ECOM':'revenue','ADS':'revenue','REG':'sales','CRM':'all_record_amount'}[p['code']]
        control=sum(float(x[p['money']]) for x in raw)
        check(p['code']+' monetary source control',eq(data[0][target],control),control)
    if p['code']=='MKT':
        check('MKT seller GMV shares sum to one',eq(sum(r['gmv_share'] for r in q(db,p,3)),1,1e-9))
        pareto=q(db,p,4);check('MKT Pareto ends at one',eq(pareto[-1]['cumulative_gmv_share'],1,1e-9))
    if p['code']=='ECOM':
        check('ECOM anonymous repetitions retained',profile['complete_repeated_rows']==138,profile['complete_repeated_rows'])
        check('ECOM device purchases reconcile',sum(r['purchases'] for r in q(db,p,2))==sum(float(x['Purchased Customers']) for x in raw))
    if p['code']=='ADS':check('ADS P&L reconciles at row tolerance',len(q(db,p,5))==0,len(q(db,p,5)))
    if p['code']=='REG':
        check('REG first monthly change is undefined',q(db,p,3)[0]['mom_sales_change'] is None)
        check('REG all restaurants have complete coverage',all(r['months_reported']==6 for r in q(db,p,4)))
    if p['code']=='CRM':
        bridge=q(db,p,2)[0];check('CRM open closed bridge',eq(bridge['open_pipeline']+bridge['closed_won']+bridge['closed_lost'],sum(float(x['Amount']) for x in raw)))
        check('CRM open review excludes closed stages',all(r['stage'] not in ('Closed Won','Closed Lost') for r in q(db,p,4)))
    # Query fixtures exercise actual delivered SQL against deliberately small data.
    db.execute(f'DELETE FROM {p["tbl"]}')
    if p['code']=='MKT':
        db.executemany('INSERT INTO marketplace VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',[(1,'2025-07-01','2025','2025-07','A','S1','P1',1,1,100,10,.1,100),(2,'2025-07-02','2025','2025-07','A','S2','P2',1,1,900,180,.2,900)])
        check('MKT weighted unequal GMV fixture',eq(q(db,p,2)[0]['weighted_take_rate'],.19,1e-10))
        db.execute('UPDATE marketplace SET gmv=0');check('MKT zero GMV fixture',q(db,p,2)[0]['weighted_take_rate'] is None)
    if p['code']=='ECOM':
        vals=[1,'2025-07','mobile','organic','US','A','P1',10,3,2,1,100,40,1,.4,.3,.66,.5,.7,.33,.5,'Purchase Conversion','Purchased',100]
        db.execute('INSERT INTO ecommerce VALUES('+','.join('?' for _ in vals)+')',vals)
        check('ECOM funnel fixture',eq(q(db,p,2)[0]['view_purchase_rate'],.1,1e-10))
        db.execute('UPDATE ecommerce SET views=0,carts=0,checkouts=0,purchases=0');check('ECOM zero checkout fixture',q(db,p,2)[0]['checkout_purchase_rate'] is None)
        db.execute('UPDATE ecommerce SET purchases=2');check('ECOM invalid funnel detected',len(q(db,p,5))==1)
    if p['code']=='FIN':
        db.executemany('INSERT INTO finance VALUES(?,?,?,?,?,?,?,?,?)',[(1,'2025-07','2025','D','NA','Sales','Revenue','Actual',100),(2,'2025-07','2025','D','NA','Sales','Revenue','Budget',80),(3,'2025-07','2025','D','NA','Costs','COGS','Actual',30),(4,'2025-07','2025','D','NA','Salary','OpEx','Actual',20)])
        r=q(db,p,2)[0];check('FIN signed variance fixture',eq(r['revenue_variance'],20) and eq(r['operating_income'],50) and eq(r['gross_margin'],.7,1e-10))
        db.execute("UPDATE finance SET amount=0 WHERE scenario='Budget'");check('FIN zero budget fixture',q(db,p,2)[0]['revenue_variance_rate'] is None)
        db.execute('DELETE FROM finance_summary');check('FIN missing summary surfaced',q(db,p,4)[0]['disposition']=='MISSING SOURCE')
        db.execute("INSERT INTO finance_summary VALUES('2025-07','D',999)");check('FIN mismatched summary surfaced',q(db,p,4)[0]['disposition']=='UNRESOLVED DIFFERENCE')
    if p['code']=='ADS':
        db.executemany('INSERT INTO advertising VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[(1,'2025-07','A','Mobile',100,10,.1,1,.1,1,10,20,20,10),(2,'2025-07','A','Desktop',1000,100,.1,1,.1,10,100,500,50,400)])
        check('ADS weighted ROAS fixture',eq(q(db,p,2)[0]['roas'],520/110,1e-10))
        db.execute('UPDATE advertising SET cost=0,clicks=0,impressions=0,conversions=0');r=q(db,p,2)[0];check('ADS zero denominators fixture',all(r[k] is None for k in ['roas','ctr','cpc','conversion_rate']))
    if p['code']=='REG':
        db.executemany('INSERT INTO restaurant_sales VALUES(?,?,?,?,?,?)',[(1,'A','Raleigh','1','2025-07',100),(2,'A','Raleigh','1','2025-09',150)])
        check('REG missing adjacent month fixture',q(db,p,3)[1]['mom_sales_change'] is None)
        db.execute("INSERT INTO restaurant_sales VALUES(3,'A','Raleigh','1','2025-09',50)");check('REG duplicate key fixture',len(q(db,p,5))==1)
    if p['code']=='CRM':
        db.executemany('INSERT INTO pipeline VALUES(?,?,?,?,?)',[(1,'A','Proposal',100,.5),(2,'B','Negotiate',900,.75),(3,'C','Closed Won',200,1),(4,'D','Closed Lost',300,0)])
        r=q(db,p,2)[0];check('CRM weighted open fixture',eq(r['weighted_open_pipeline'],725) and eq(r['open_pipeline'],1000))
        db.execute("UPDATE pipeline SET probability=.5 WHERE stage='Closed Won'");check('CRM closed probability fixture',len(q(db,p,5))==1)
    db.close()

# Check internal relative Markdown links, ignoring historical preserved content.
bad=[]
for path in BASE.rglob('*.md'):
    if 'Legacy' in path.parts:continue
    for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
        if target.startswith(('https:','http:','#','mailto:')):continue
        target=target.split('#')[0]
        if not (path.parent/target).exists():bad.append(str(path.relative_to(BASE))+': '+target)
check('Current Markdown links resolve',not bad,bad)
for p in config:
    req=rows(BASE/p['folder']/'Delivery'/'requirements_traceability.csv')
    tests=rows(BASE/p['folder']/'Delivery'/'uat_cases.csv')
    ids={r['Requirement ID'] for r in req};covered={r['Requirement ID'] for r in tests}
    check(p['code']+' complete UAT requirement coverage',ids<=covered)
    check(p['code']+' requirements have acceptance criteria',all(r['Acceptance Criteria'] for r in req))
    check(p['code']+' approval status remains truthful',all(r['Business Approval']=='Pending simulated stakeholder review' for r in req))

result={'executed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'passed':sum(r['status']=='PASS' for r in checks),'failed':sum(r['status']=='FAIL' for r in checks),'scope':'Source calculations and SQL fixtures executed locally. Business approval, CRM controls, dashboard interaction, RLS, accessibility, and production deployment are not executed.'}
(BASE/'Quality'/'validation_report.json').write_text(json.dumps(result,indent=2))
lines=['# Validation report','',f"Executed: {result['executed_at_utc']}",f"Passed: {result['passed']} | Failed: {result['failed']}",'',result['scope'],'','| Check | Result | Evidence |','| --- | --- | --- |']
lines+=['| '+r['check']+' | '+r['status']+' | '+r['detail'].replace('|','/')+' |' for r in checks]
(BASE/'Quality'/'VALIDATION_REPORT.md').write_text('\n'.join(lines)+'\n')
print(f"Validation: {result['passed']} passed, {result['failed']} failed")
if result['failed']:sys.exit(1)
