"""Launches a local demo server, exercises endpoints, then restores seed DB.
Do not run while a separate demo server is using this package DB.
"""
from pathlib import Path
import subprocess,sys,socket,time,json,urllib.request,urllib.error,os
R=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(R/'backend/reset_demo.py')],check=True,stdout=subprocess.DEVNULL)
s=socket.socket();s.bind(('127.0.0.1',0));port=s.getsockname()[1];s.close()
p=subprocess.Popen([sys.executable,str(R/'backend/api.py'),'--port',str(port)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
results=[]
def request(path,data=None,auth=True):
    headers={'Content-Type':'application/json'}
    if auth:headers['Authorization']='Bearer '+os.environ.get('SIH_DEMO_TOKEN','local-demo-only')
    r=urllib.request.Request(f'http://127.0.0.1:{port}'+path,data=None if data is None else json.dumps(data).encode(),headers=headers)
    try:
        with urllib.request.urlopen(r,timeout=5) as x:return x.status,json.loads(x.read())
    except urllib.error.HTTPError as x:return x.code,json.loads(x.read())
def check(name,condition):
    results.append({'test':name,'status':'PASS' if condition else 'FAIL','provenance':'MOCK_BEHAVIOUR'})
    assert condition,name
try:
    for _ in range(50):
        try:
            if request('/health')[0]==200:break
        except Exception:time.sleep(.1)
    endpoints=['/health','/api/v1/mock/igot/users','/api/v1/mock/igot/users/USR-001','/api/v1/mock/igot/users/USR-001/position','/api/v1/mock/igot/users/USR-001/competencies','/api/v1/mock/igot/users/USR-001/training-history','/api/v1/mock/igot/users/USR-001/learning-context','/api/v1/mock/igot/positions','/api/v1/mock/igot/positions/POS-002','/api/v1/mock/igot/positions/POS-002/roles','/api/v1/mock/igot/positions/POS-002/competencies','/api/v1/mock/igot/roles','/api/v1/mock/igot/roles/ROLE-001','/api/v1/mock/igot/roles/ROLE-001/activities','/api/v1/mock/igot/roles/ROLE-001/competencies','/api/v1/mock/igot/competencies','/api/v1/mock/igot/competencies/COMP-SAMPLING','/api/v1/mock/igot/courses','/api/v1/mock/igot/courses/CRS-001','/api/v1/mock/igot/courses/CRS-001/competencies','/api/v1/users/USR-001/competency-gaps','/api/v1/users/USR-001/competency-gaps?scope=target','/api/v1/users/USR-001/recommendations?scope=target','/api/v1/users/USR-001/learning-path','/api/v1/users/USR-001/journey']
    for e in endpoints:check('GET '+e,request(e)[0]==200)
    profile=request('/api/v1/mock/igot/users/USR-001')[1];check('camelCase shared profile IDs',profile['userId']=='USR-001' and profile['mdoId']=='MDO-001' and profile['positionId']=='POS-001')
    g=request('/api/v1/users/USR-001/competency-gaps?scope=target')[1];check('Trace arrays deserialize at API boundary',all(isinstance(x['contributingActivityIds'],list) for x in g))
    path='/api/v1/users/USR-001/competency-evidence';payload=json.loads((R/'fixtures/evidence_practical.json').read_text())
    check('POST needs service token',request(path,payload,False)[0]==401)
    check('Practical evidence POST applies one-level promotion',request(path,payload)[1]['updates']==[{'competencyId':'COMP-SAMPLING','before':2,'after':3}])
    check('POST retry is idempotent',request(path,payload)[1]['status']=='IDEMPOTENT_REPLAY')
    state=request('/api/v1/users/USR-001/competency-gaps?scope=target')[1]
    check('GET sees recalculated gap after POST',next(x for x in state if x['competencyId']=='COMP-SAMPLING')['unmetGap']==1)
    bad={**payload,'overallScore':85};check('Conflicting repeated assessment rejected',request(path,bad)[0]==400)
    check('Unknown route returns 404',request('/not-a-route')[0]==404)
finally:
    p.terminate();p.wait(timeout=10)
    subprocess.run([sys.executable,str(R/'backend/reset_demo.py')],check=True,stdout=subprocess.DEVNULL)
    report={'provenance':'MOCK_BEHAVIOUR','scope':'Local HTTP smoke test; no external network, iGOT API, or LLM requests. DB reset to seed afterward.','tests_run':len(results),'passed':sum(x['status']=='PASS' for x in results),'failed':sum(x['status']=='FAIL' for x in results),'results':results}
    (R/'docs/api_smoke_report.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
