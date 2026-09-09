"""Validation against immutable seed, not the mutable live demo DB.
Run: python backend/validate.py. Reports are written to docs/validation_report.json.
"""
from pathlib import Path
import json,copy,re,sqlite3,sys,collections
from engine import recompute,required,find,eligible,readiness,ingest
ROOT=Path(__file__).resolve().parents[1];D=json.loads((ROOT/'data/dataset.json').read_text());results=[]
def test(name,fn):
    try:
        assert fn(),name
        results.append({'test':name,'status':'PASS','provenance':'MOCK_BEHAVIOUR'})
    except Exception as e:results.append({'test':name,'status':'FAIL','detail':str(e),'provenance':'MOCK_BEHAVIOUR'})
def raises(fn):
    try:fn();return False
    except (ValueError,KeyError,AssertionError):return True

def sql_check():
    c=sqlite3.connect(':memory:');c.execute('PRAGMA foreign_keys=ON');c.executescript((ROOT/'sql/schema.sql').read_text())
    for t,rows in D.items():
        for x in rows:c.execute('INSERT INTO '+t+' ('+','.join(x)+') VALUES ('+','.join('?' for _ in x)+')',list(x.values()))
    ok=not c.execute('PRAGMA foreign_key_check').fetchall() and c.execute('PRAGMA integrity_check').fetchone()[0]=='ok';c.close();return ok

test('Exactly ten users, USR-001 through USR-010',lambda:[x['user_id'] for x in D['users']]==[f'USR-{i:03}' for i in range(1,11)])
test('All users explicitly synthetic with reserved invalid-domain emails',lambda:all(x['provenance']=='SYNTHETIC' and x['email'].endswith('@example.invalid') and x['name'].endswith('Demo') for x in D['users']))
test('No orphan foreign keys, duplicate primary keys or violated SQL constraints',sql_check)
test('Every stored record has one allowed provenance and matching source_type',lambda:all(x['provenance'] in ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR') and x['source_type']==x['provenance'] for rows in D.values() for x in rows))
test('Every nonsource record links a provenance source',lambda:all(find(D,'sources','source_id',x['source_id']) for t,rows in D.items() if t!='sources' for x in rows))
test('Original ten activities preserved with three explicit extensions',lambda:len(D['activities'])==13 and [x['activity_id'] for x in D['activities'] if not x['is_extension']]==[f'ACT-{i:03}' for i in range(1,11)])
test('Every role requirement equals activity MAX and preserves complete trace',lambda:all((lambda aa: r['required_level']==max(x['required_level'] for x in aa) and set(json.loads(r['contributing_activity_ids']))=={x['activity_id'] for x in aa} and set(json.loads(r['max_level_activity_ids']))=={x['activity_id'] for x in aa if x['required_level']==r['required_level']})([x for x in D['activity_competencies'] if x['competency_id']==r['competency_id'] and find(D,'activities','activity_id',x['activity_id'])['role_id']==r['role_id']]) for r in D['role_competencies']))
test('All activities have requirements and all roles have activities',lambda:all(any(y['activity_id']==x['activity_id'] for y in D['activity_competencies']) for x in D['activities']) and all(any(y['role_id']==x['role_id'] for y in D['activities']) for x in D['roles']))
test('Fixed five-level names and exactly five rows per competency',lambda:all([x['level_name'] for x in D['competency_levels'] if x['competency_id']==c['competency_id']]==['Awareness','Basic Application','Independent Application','Advanced','Expert / Strategic'] for c in D['competencies']))
test('Competency types are B/D/F only',lambda:all(x['type'] in ('BEHAVIOURAL','DOMAIN','FUNCTIONAL') for x in D['competencies']))
test('Every position has exactly one primary role',lambda:all(sum(x['is_primary'] for x in D['position_role'] if x['position_id']==p['position_id'])==1 for p in D['positions']))
test('All user MDO/division assignments agree with current position',lambda:all((lambda p:p['mdo_id']==u['mdo_id'] and p['division_id']==u['division_id'])(find(D,'positions','position_id',u['position_id'])) for u in D['users']))
test('Each target advances one project career band only',lambda:all(find(D,'positions','position_id',u['target_position_id'])['career_band']-find(D,'positions','position_id',u['position_id'])['career_band']==1 for u in D['users']))
test('Three explicit unknown competencies across two users',lambda:sum(x['current_level'] is None for x in D['user_competencies'])==3 and len({x['user_id'] for x in D['user_competencies'] if x['current_level'] is None})==2)
test('No fabricated evidence for withheld competency states',lambda:all(not any(e['user_id']==x['user_id'] and e['competency_id']==x['competency_id'] for e in D['competency_evidence']) for x in D['user_competencies'] if x['current_level'] is None))
test('Known states supported by separately stored mock evidence',lambda:all(any(e['user_id']==x['user_id'] and e['competency_id']==x['competency_id'] and e['estimated_level']==x['current_level'] for e in D['competency_evidence']) for x in D['user_competencies'] if x['current_level'] is not None))
test('Both current-role and target-role scopes exist for each user',lambda:all({g['scope'] for g in D['competency_gaps'] if g['user_id']==u['user_id']}=={'CURRENT','TARGET'} for u in D['users']))
test('All numeric gaps and HIGH/MEDIUM/NO_GAP labels correct',lambda:all(g['signed_gap']==g['required_level']-g['current_level'] and g['unmet_gap']==max(0,g['signed_gap']) and g['gap_status']==('HIGH' if g['unmet_gap']>=2 else 'MEDIUM' if g['unmet_gap']==1 else 'NO_GAP') for g in D['competency_gaps'] if g['current_level'] is not None))
test('Unknown gaps preserve null arithmetic and require evidence',lambda:all(g['signed_gap'] is None and g['unmet_gap'] is None and g['gap_status']=='INSUFFICIENT_EVIDENCE' and g['recommendation_status']=='ASSESSMENT_REQUIRED' for g in D['competency_gaps'] if g['current_level'] is None))
test('Negative signed gaps do not create negative unmet gaps',lambda:any(g['signed_gap'] is not None and g['signed_gap']<0 and g['unmet_gap']==0 for g in D['competency_gaps']))
test('All five readiness statuses exercised',lambda:{x['readiness_status'] for x in D['learning_paths']}=={'READY','NEAR_READY','DEVELOPMENT_REQUIRED','CRITICAL_GAPS','INSUFFICIENT_EVIDENCE'})
test('All ten real course rows have official documentary sources and unknown syllabus fields',lambda:sum(c['tier']==1 for c in D['courses'])==10 and all(c['provenance']=='PUBLIC_OFFICIAL' and c['description'] is None and c['license'] is None and c['language'] is None for c in D['courses'] if c['tier']==1))
URLS={
'https://portal.igotkarmayogi.gov.in/app/toc/do_11363681497528729611020/overview',
'https://portal.igotkarmayogi.gov.in/app/toc/do_1140994741049999361127/overview',
'https://portal.igotkarmayogi.gov.in/app/toc/do_1142432002191196161252/overview',
'https://portal.igotkarmayogi.gov.in/app/toc/do_1142432175613706241256/overview'}
test('Only the four source-documented, permitted deep links populate course_url',lambda:{c['course_url'] for c in D['courses'] if c['course_url']}==URLS)
test('No synthetic course has a URL or verified destination',lambda:all(c['course_url'] is None and c['destination_verified']==0 and c['status']=='BLUEPRINT_ONLY' for c in D['courses'] if c['tier']==2))
test('No claim of live course verification',lambda:all(c['live_access_verified']==0 and c['last_verified_at'] is None for c in D['courses']))
test('All recommendations have a positive gap and eligible mapping',lambda:all(any(c['course_id']==r['course_id'] for c,m,s in eligible(D,find(D,'competency_gaps','gap_id',r['gap_id']))) for r in D['course_recommendations']))
test('No completed courses recommended',lambda:all(not any(h['user_id']==r['user_id'] and h['course_id']==r['course_id'] and h['status']=='COMPLETED' for h in D['training_records']) for r in D['course_recommendations']))
test('Excel has no statistical/domain competency mappings',lambda:all(m['competency_id']=='COMP-002' for m in D['course_competencies'] if m['course_id']=='CRS-001'))
test('Cybersecurity mappings never certify advanced privacy and stay pending',lambda:all(m['competency_id']=='COMP-014' and m['to_level']<=3 and m['approval_status']=='PENDING_REVIEW' for m in D['course_competencies'] if m['course_id'] in ('CRS-004','CRS-005')))
test('Every recommended outcome maps to the recommended competency',lambda:all(all(any(l['learning_outcome_id']==oid and l['competency_id']==r['competency_id'] for l in D['learning_outcome_competency']) for oid in json.loads(r['learning_outcome_ids'])) for r in D['course_recommendations']))
test('No generated learning outcome presented as published iGOT text',lambda:all(o['provenance']=='DERIVED' and not o['is_published_outcome'] for o in D['course_learning_outcomes']))
test('Approvals explicitly simulated; no production approval',lambda:all(m['approval_basis']=='SIMULATED_TRAINER_REVIEW' and m['reviewer_id']=='MOCK-TRAINER-001' and m['production_approved']==0 for m in D['course_competencies'] if m['approval_status']=='APPROVED'))
test('Fallback NO_VERIFIED_COURSE is exercised',lambda:any(g['recommendation_status']=='NO_VERIFIED_COURSE' for g in D['competency_gaps']))
test('Production mode refuses all unvalidated course mappings',lambda:all(not eligible(D,g,'PRODUCTION') for g in D['competency_gaps']))
test('All real recommendations have planned bridge-gap accounting',lambda:all(r['remaining_gap_after_planned_learning']==max(0,find(D,'competency_gaps','gap_id',r['gap_id'])['required_level']-next(m['to_level'] for m in D['course_competencies'] if m['course_id']==r['course_id'] and m['competency_id']==r['competency_id'])) for r in D['course_recommendations']))
test('Learning paths do not disguise synthetic courses as iGOT learning',lambda:all(p['course_id'] is None or find(D,'courses','course_id',p['course_id'])['destination_verified']==1 for p in D['learning_path_items']))
test('Ready user gets no unnecessary course or remedial path',lambda:not any(r['user_id']=='USR-010' for r in D['course_recommendations']) and not any(p['learning_path_id']=='PATH-USR-010' for p in D['learning_path_items']))
def deterministic():
    r=copy.deepcopy(D);recompute(r);return all(r[t]==D[t] for t in ('competency_gaps','course_recommendations','learning_paths','learning_path_items'))
test('Recomputation produces byte-equivalent derived row structures',deterministic)
def confidence_not_priority():
    r=copy.deepcopy(D)
    for x in r['user_competencies']:
        if x['confidence'] is not None:x['confidence']=0.1
    recompute(r);return r['competency_gaps']==D['competency_gaps']
test('Changing confidence does not change gap priority',confidence_not_priority)
event=json.loads((ROOT/'fixtures/evidence_practical.json').read_text());practice=json.loads((ROOT/'fixtures/evidence_practice.json').read_text())
def feedback():
    r=copy.deepcopy(D);answer=ingest(r,'USR-001',event)
    g=next(g for g in r['competency_gaps'] if g['user_id']=='USR-001' and g['scope']=='TARGET' and g['competency_id']=='COMP-SAMPLING')
    return answer['updates']==[{'competencyId':'COMP-SAMPLING','before':2,'after':3}] and g['required_level']==4 and g['unmet_gap']==1
test('Practical rubric updates sampling L2 to L3, target gap 2 to 1',feedback)
def replay():
    r=copy.deepcopy(D);ingest(r,'USR-001',event);before=copy.deepcopy(r);a=ingest(r,'USR-001',event);return a['status']=='IDEMPOTENT_REPLAY' and r==before
test('Evidence retries are idempotent',replay)
def conflict():
    r=copy.deepcopy(D);ingest(r,'USR-001',event);p=copy.deepcopy(event);p['overallScore']=85;return raises(lambda:ingest(r,'USR-001',p))
test('Same assessment ID with changed payload is rejected',conflict)
def practice_only():
    r=copy.deepcopy(D);a=ingest(r,'USR-001',practice);return not a['updates'] and r['user_competencies']==D['user_competencies'] and len(r['competency_evidence'])==len(D['competency_evidence'])+1
test('Five-question 80% practice stores evidence without promoting level',practice_only)
def low_conf():
    r=copy.deepcopy(D);p=copy.deepcopy(event);p['competencies'][0]['confidence']=0.2;return not ingest(r,'USR-001',p)['updates']
test('Low-confidence practical evidence does not promote competency',low_conf)
def invalid(field,value):
    p=copy.deepcopy(event);p['competencies'][0][field]=value;r=copy.deepcopy(D);return raises(lambda:ingest(r,'USR-001',p)) and r==D
for f,v in [('competencyId','COMP-NONEXISTENT'),('estimatedLevel',6),('confidence',True),('coverage',1.5),('score',101)]:test('Reject invalid '+f,lambda f=f,v=v:invalid(f,v))
test('Reject path/payload user mismatch',lambda:raises(lambda:ingest(copy.deepcopy(D),'USR-002',event)))
def old_evidence():
    r=copy.deepcopy(D);p=copy.deepcopy(event);p['assessedAt']='2026-08-01T09:00:00Z';return not ingest(r,'USR-001',p)['updates']
test('Stale evidence is stored without overwriting newer state',old_evidence)
Q=json.loads((ROOT/'assessment/questions.json').read_text());CH=json.loads((ROOT/'assessment/chunks.json').read_text())
test('Five hand-authored fixture MCQs each have exactly one correct answer',lambda:len(Q)==5 and all(len(q['options'])==4 and sum(o['is_correct'] for o in q['options'])==1 and q['correct_option_id']==next(o['option_id'] for o in q['options'] if o['is_correct']) for q in Q))
test('Every fixture question has a valid competency, outcome and exact stored source chunk',lambda:all(find(D,'competencies','competency_id',q['competency_id']) and find(D,'course_learning_outcomes','learning_outcome_id',q['learning_outcome_id']) and q['source'] in CH for q in Q))
summary={'provenance':'MOCK_BEHAVIOUR','validation_scope':'Deterministic structural and functional demo tests. NOT human subject-matter validation, course syllabus/live enrollment verification, PostgreSQL execution, security certification, or performance testing.','tests_run':len(results),'passed':sum(r['status']=='PASS' for r in results),'failed':sum(r['status']=='FAIL' for r in results),'results':results}
(ROOT/'docs/validation_report.json').write_text(json.dumps(summary,indent=2))
print(json.dumps({k:v for k,v in summary.items() if k!='results'},indent=2))
for r in results:
    if r['status']=='FAIL':print(r)
sys.exit(1 if summary['failed'] else 0)
