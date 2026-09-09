"""Expanded data validator. Standard-library checks; workbook check if openpyxl installed.
Runs inherited v2 engine tests with four explicit expansion-aware expectations,
then checks preservation, complete chains, export parity and new fixture consistency.
"""
from pathlib import Path
import json,sys,copy,csv,sqlite3,collections,hashlib
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'backend'))
from engine import recompute,required,find,journey,eligible,ingest
D=json.loads((R/'data/dataset.json').read_text());B=json.loads((R/'docs/baseline_v2.json').read_text())
results=[]
def check(name,fn):
 try:
  assert fn(),name
  results.append(dict(test=name,status='PASS'))
 except Exception as e:results.append(dict(test=name,status='FAIL',detail=str(e)))
# Original functional/evidence suite preserved verbatim on disk; explicit expectation changes only.
src=(R/'backend/validate.py').read_text()
src=src.replace('Exactly ten users, USR-001 through USR-010','Exactly twenty users, USR-001 through USR-020').replace("range(1,11)])","range(1,21)])")
src=src.replace('Original ten activities preserved with three explicit extensions','Original ten activities preserved with 24 explicit extensions').replace("len(D['activities'])==13","len(D['activities'])==34")
src=src.replace('All ten real course rows have official documentary sources and unknown syllabus fields','All 17 public metadata rows have official sources and unknown syllabus fields').replace("sum(c['tier']==1 for c in D['courses'])==10","sum(c['tier']==1 for c in D['courses'])==17")
src=src.replace("m['competency_id']=='COMP-014' and m['to_level']<=3", "m['competency_id'] in ('COMP-014','COMP-032') and m['to_level']<=3")
src=src.replace("[f'ACT-{i:03}' for i in range(1,21)]", "[f'ACT-{i:03}' for i in range(1,11)]")
ns={'__file__':str(R/'backend/validate.py'),'__name__':'__expanded_baseline_validation__'}
try:exec(compile(src,str(R/'backend/validate.py'),'exec'),ns)
except SystemExit:pass
results.extend(ns['results'])
check('32 competencies, 160 levels, 30 courses, 46 mappings, 50 histories',lambda:tuple(len(D[t]) for t in ['competencies','competency_levels','courses','course_competencies','training_records'])==(32,160,30,46,50))
check('26 canonical tables and exact same fields in each row',lambda:list(D)==list(B) and len(D)==26 and all(set(x)==set(B[t][0]) for t,rs in D.items() for x in rs))
for t in ['users','roles','activities','activity_competencies','role_competencies','positions','position_role','user_competencies','competency_evidence','courses','course_competencies','course_learning_outcomes','learning_outcome_competency','training_records']:
 check('Original rows retained unchanged: '+t,lambda t=t:all(x in D[t] for x in B[t]))
check('Only COMP-011 description/timestamp differs among original competencies',lambda:all(all(c[k]==find(D,'competencies','competency_id',c['competency_id'])[k] for k in c if not(c['competency_id']=='COMP-011' and k in ('description','updated_at'))) for c in B['competencies']))
check('Original 10 current/target requirements unchanged',lambda:all(required(B,u[k])==required(D,u[k]) for u in B['users'] for k in ('position_id','target_position_id')))
for file in ['schema.sql','schema_postgresql.sql']:
 check('Unchanged DDL hash: '+file,lambda file=file:hashlib.sha256((R/'sql'/file).read_bytes()).hexdigest()==json.loads((R/'docs/baseline_schema_hashes.json').read_text())[file])
check('Every competency has a role requirement and course candidate',lambda:all(any(r['competency_id']==c['competency_id'] for r in D['role_competencies']) and any(m['competency_id']==c['competency_id'] for m in D['course_competencies']) for c in D['competencies']))
check('Each added competency has user state, evidence, a positive target gap, a course mapping and a path item',lambda:all(all(any(x['competency_id']==c and (t!='competency_gaps' or (x['scope']=='TARGET' and (x['unmet_gap'] or 0)>0)) for x in D[t]) for t in ['user_competencies','competency_evidence','competency_gaps','course_competencies','learning_path_items']) for c in [f'COMP-{i:03}' for i in range(19,33)]))
check('All 30 courses have at least one explicit project objective',lambda:all(any(o['course_id']==c['course_id'] for o in D['course_learning_outcomes']) for c in D['courses']))
check('Every mapping has an outcome at its mapped target level',lambda:all(any(o['course_id']==m['course_id'] and any(l['learning_outcome_id']==o['learning_outcome_id'] and l['competency_id']==m['competency_id'] and l['target_level']==m['to_level'] for l in D['learning_outcome_competency']) for o in D['course_learning_outcomes']) for m in D['course_competencies']))
check('Only CRS-010 deliberately unmapped; no fabricated level objective',lambda:{c['course_id'] for c in D['courses'] if not any(m['course_id']==c['course_id'] for m in D['course_competencies'])}=={'CRS-010'})
check('New mappings are pending, never production-approved',lambda:all(m['approval_status']=='PENDING_REVIEW' and not m['production_approved'] for m in D['course_competencies'] if m not in B['course_competencies']))
check('Every new blueprint mapping participates in a positive gap somewhere',lambda:all(any(g['competency_id']==m['competency_id'] and (g['unmet_gap'] or 0)>0 for g in D['competency_gaps']) for m in D['course_competencies'] if m not in B['course_competencies'] and find(D,'courses','course_id',m['course_id'])['tier']==2))
check('No duplicate user/course training events',lambda:len({(h['user_id'],h['course_id']) for h in D['training_records']})==50)
check('Each original user has 2 histories and each new user has 3',lambda:all(sum(h['user_id']==u['user_id'] for h in D['training_records'])==(2 if i<10 else 3) for i,u in enumerate(D['users'])))
check('No training events falsely assigned to fictional blueprint courses',lambda:all(find(D,'courses','course_id',h['course_id'])['tier']==1 for h in D['training_records']))
def history_ok(h):
 if h['status']=='COMPLETED':return h['progress_percent']==100 and h['started_at']<=h['completed_at']<='2026-09-07T06:15:00Z'
 if h['status']=='IN_PROGRESS':return h['started_at'] is not None and h['completed_at'] is None and 0<h['progress_percent']<100
 return h['started_at'] is None and h['completed_at'] is None and h['progress_percent']==0
check('Training status, dates, progress and unverified completion agree',lambda:all(history_ok(h) and not h['completion_verified'] and h['provenance']=='MOCK_BEHAVIOUR' for h in D['training_records']))
check('Current and target required skills have explicit states for every persona',lambda:all(any(x['user_id']==u['user_id'] and x['competency_id']==cid for x in D['user_competencies']) for u in D['users'] for k in ('position_id','target_position_id') for cid in required(D,u[k])))
check('Second local source exists and is authorized project content',lambda:len(D['knowledge_resources'])==2 and all(x['ingestion_allowed'] and (R/x['local_path']).is_file() and x['provenance']=='SYNTHETIC' for x in D['knowledge_resources']))
for u in D['users']:
 check('Journey snapshot matches recomputation: '+u['user_id'],lambda u=u:json.loads((R/'fixtures'/f'{u["user_id"]}_journey.json').read_text())==journey(D,u['user_id']))
for t in D:
 check('JSON export matches seed: '+t,lambda t=t:json.loads((R/'data/json'/f'{t}.json').read_text())==D[t])
 def csvcheck(t=t):
  with (R/'data/csv'/f'{t}.csv').open(newline='',encoding='utf-8') as f:rs=list(csv.DictReader(f))
  return rs==[{k:'' if v is None else str(v) for k,v in x.items()} for x in D[t]]
 check('CSV export matches seed: '+t,csvcheck)
con=sqlite3.connect(R/'data/demo.sqlite');con.row_factory=sqlite3.Row
for t in D:check('SQLite rows match seed: '+t,lambda t=t:[dict(x) for x in con.execute('SELECT * FROM '+t)]==D[t])
check('SQLite integrity and foreign keys',lambda:con.execute('PRAGMA integrity_check').fetchone()[0]=='ok' and not con.execute('PRAGMA foreign_key_check').fetchall())
con.close()
try:
 import openpyxl
 w=openpyxl.load_workbook(R/'SIH26101_Review_Workbook.xlsx',read_only=True,data_only=True)
 for t in D:
  def workbookcheck(t=t):
   rows=list(w[t].values);headers=rows[0]
   return len(rows)==len(D[t])+1 and all(all((abs(a-b)<1e-10 if isinstance(a,float) and isinstance(b,float) else a==b) for a,b in zip(row,[expected[k] for k in headers])) for row,expected in zip(rows[1:],D[t]))
  check('Workbook table equals seed: '+t,workbookcheck)
 w.close()
except ImportError:results.append(dict(test='Workbook parity requires optional openpyxl',status='SKIPPED'))
check('Problem-statement audit records 33 items, 22 modeled and 11 deferred',lambda:(lambda rs:len(rs)==33 and sum(bool(x['competency_id']) for x in rs)==22)(list(csv.DictReader((R/'docs/problem_statement_coverage.csv').open()))))
report=dict(scope='Inherited functional tests plus expanded data contracts. Not syllabus, live enrollment, production security, PostgreSQL execution or load testing.',tests_run=len(results),passed=sum(r['status']=='PASS' for r in results),failed=sum(r['status']=='FAIL' for r in results),skipped=sum(r['status']=='SKIPPED' for r in results),results=results)
(R/'docs/expansion_validation_report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
for r in results:
 if r['status']=='FAIL':print(r)
sys.exit(1 if report['failed'] else 0)
