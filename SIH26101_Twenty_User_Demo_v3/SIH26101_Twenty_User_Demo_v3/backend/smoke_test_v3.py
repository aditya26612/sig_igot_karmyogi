"""Local expanded API contract checks; resets this package DB before/after testing."""
from pathlib import Path
import subprocess,sys,socket,time,json,urllib.request,urllib.error,os
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'data/dataset.json').read_text())
subprocess.run([sys.executable,str(R/'backend/reset_demo.py')],check=True,stdout=subprocess.DEVNULL)
s=socket.socket();s.bind(('127.0.0.1',0));port=s.getsockname()[1];s.close()
p=subprocess.Popen([sys.executable,str(R/'backend/api.py'),'--port',str(port)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
results=[]
def req(path,payload=None):
 r=urllib.request.Request(f'http://127.0.0.1:{port}'+path,data=None if payload is None else json.dumps(payload).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+os.environ.get('SIH_DEMO_TOKEN','local-demo-only')})
 try:
  with urllib.request.urlopen(r,timeout=10) as f:return f.status,json.loads(f.read())
 except urllib.error.HTTPError as e:return e.code,json.loads(e.read())
def check(name,fn):
 try:
  assert fn(),name;results.append(dict(test=name,status='PASS'))
 except Exception as e:results.append(dict(test=name,status='FAIL',detail=str(e)))
try:
 for _ in range(100):
  try:
   if req('/health')[0]==200:break
  except Exception:time.sleep(.1)
 for table,count in [('users',20),('positions',28),('roles',15),('competencies',32),('courses',30)]:
  check('Catalogue count '+table,lambda table=table,count=count:len(req('/api/v1/mock/igot/'+table)[1])==count)
 for u in D['users']:
  uid=u['user_id'];base='/api/v1/mock/igot/users/'+uid;learn='/api/v1/users/'+uid
  check(uid+' profile IDs preserved',lambda: (lambda x:x['userId']==uid and x['positionId']==u['position_id'] and x['targetPositionId']==u['target_position_id'])(req(base)[1]))
  check(uid+' competencies count and camelCase',lambda:(lambda x:len(x)==sum(c['user_id']==uid for c in D['user_competencies']) and all('competencyId' in c and 'currentLevel' in c for c in x))(req(base+'/competencies')[1]))
  check(uid+' training history',lambda:(lambda x:len(x)==sum(h['user_id']==uid for h in D['training_records']) and all(h['userId']==uid for h in x))(req(base+'/training-history')[1]))
  for scope in ['current','target']:
   check(uid+' '+scope+' gaps and decoded trace arrays',lambda scope=scope:(lambda x:len(x)==sum(g['user_id']==uid and g['scope']==scope.upper() for g in D['competency_gaps']) and all(isinstance(g['contributingActivityIds'],list) for g in x))(req(learn+'/competency-gaps?scope='+scope)[1]))
   check(uid+' '+scope+' recommendations',lambda scope=scope:(lambda x:len(x)==sum(r['user_id']==uid and next(g for g in D['competency_gaps'] if g['gap_id']==r['gap_id'])['scope']==scope.upper() for r in D['course_recommendations']))(req(learn+'/recommendations?scope='+scope)[1]))
  check(uid+' target learning path',lambda:(lambda x:x['path']['userId']==uid and x['path']['scope']=='TARGET' and len(x['items'])==sum(i['learning_path_id']=='PATH-'+uid for i in D['learning_path_items']))(req(learn+'/learning-path')[1]))
  check(uid+' full journey',lambda:(lambda x:x['user']['userId']==uid and x['learningPath']['userId']==uid)(req(learn+'/journey')[1]))
 for c in D['competencies']:
  check(c['competency_id']+' five levels',lambda c=c:len(req('/api/v1/mock/igot/competencies/'+c['competency_id'])[1]['levels'])==5)
 for c in D['courses']:
  check(c['course_id']+' course context and objectives',lambda c=c:(lambda x:x['courseId']==c['course_id'] and bool(x['learningOutcomes']) and x['courseUrl']==c['course_url'])(req('/api/v1/mock/igot/courses/'+c['course_id'])[1]))
 check('CRS-010 remains explicitly unmapped',lambda:req('/api/v1/mock/igot/courses/CRS-010/competencies')==(200,[]))
 check('Invalid scope is rejected',lambda:req('/api/v1/users/USR-011/competency-gaps?scope=oops')[0]==400)
 payload=json.loads((R/'fixtures/evidence_practical.json').read_text());payload['userId']='USR-020';payload['competencies'][0]['competencyId']='COMP-032'
 check('Sampling rubric cannot promote cybersecurity',lambda:req('/api/v1/users/USR-020/competency-evidence',payload)[0]==400)
 check('Rejected assessment leaves evidence count intact',lambda:(lambda x:x['currentLevel']==1)(next(x for x in req('/api/v1/mock/igot/users/USR-020/competencies')[1] if x['competencyId']=='COMP-032')))
finally:
 p.terminate();p.wait(timeout=10)
 subprocess.run([sys.executable,str(R/'backend/reset_demo.py')],check=True,stdout=subprocess.DEVNULL)
report=dict(scope='Local HTTP checks for every persona, course and competency. No external integration or production security claims. DB restored after tests.',tests_run=len(results),passed=sum(x['status']=='PASS' for x in results),failed=sum(x['status']=='FAIL' for x in results),results=results)
(R/'docs/api_expansion_smoke_report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
for x in results:
 if x['status']=='FAIL':print(x)
sys.exit(1 if report['failed'] else 0)
