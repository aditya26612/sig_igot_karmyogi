"""Run: python backend/server.py --port 8010
Local demo only. No real authentication/SSO, no iGOT completion callback, no live AI.
"""
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
from urllib.parse import urlparse,parse_qs
import sqlite3,json,argparse,os
from engine import recompute,journey,find,required,ingest,DERIVED
ROOT=Path(__file__).resolve().parents[1]
def load_db(con):
    con.row_factory=sqlite3.Row
    names=json.loads((ROOT/'data/table_order.json').read_text())
    return {t:[dict(x) for x in con.execute('SELECT * FROM '+t)] for t in names}
def save_feedback(con,D):
    with con:
        for t in reversed(DERIVED):con.execute('DELETE FROM '+t)
        for x in D['user_competencies']:
            cols=[k for k in x if k not in ('user_id','competency_id')]
            con.execute('UPDATE user_competencies SET '+','.join(k+'=?' for k in cols)+' WHERE user_id=? AND competency_id=?',[x[k] for k in cols]+[x['user_id'],x['competency_id']])
        for x in D['competency_evidence']:
            con.execute('INSERT OR IGNORE INTO competency_evidence ('+','.join(x)+') VALUES ('+','.join('?' for _ in x)+')',list(x.values()))
        for t in DERIVED:
            for x in D[t]:con.execute('INSERT INTO '+t+' ('+','.join(x)+') VALUES ('+','.join('?' for _ in x)+')',list(x.values()))
class Handler(BaseHTTPRequestHandler):
    def reply(self,status,data):
        b=json.dumps(data,ensure_ascii=False,allow_nan=False).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(b)
    def do_GET(self):
        try:
            D=load_db(self.server.db);url=urlparse(self.path);parts=url.path.strip('/').split('/');q=parse_qs(url.query)
            if url.path=='/health':return self.reply(200,{'status':'ok','mode':'LOCAL_SYNTHETIC_DEMO','provenance':'MOCK_BEHAVIOUR'})
            if parts[:4]==['api','v1','mock','igot']:
                r=parts[4:];resource=r[0] if r else '';key=r[1] if len(r)>1 else None;sub=r[2] if len(r)>2 else None
                if resource=='users':
                    if key is None:return self.reply(200,D['users'])
                    j=journey(D,key)
                    values={None:j['user'],'position':j['current_position'],'competencies':j['current_competencies'],'training-history':[x for x in D['training_records'] if x['user_id']==key],'learning-context':j}
                    if sub not in values:return self.reply(404,{'error':'Unknown user resource'})
                    return self.reply(200,values[sub])
                if resource in ('positions','roles','competencies','courses'):
                    idfield={'positions':'position_id','roles':'role_id','competencies':'competency_id','courses':'course_id'}[resource]
                    if key is None:
                        rows=D[resource];term=q.get('q',[''])[0].casefold()
                        if term:rows=[x for x in rows if term in str(x).casefold()]
                        return self.reply(200,rows)
                    item=find(D,resource,idfield,key)
                    if item is None:return self.reply(404,{'error':'Not found'})
                    if resource=='positions' and sub=='roles':return self.reply(200,[find(D,'roles','role_id',x['role_id']) for x in D['position_role'] if x['position_id']==key])
                    if resource=='positions' and sub=='competencies':return self.reply(200,required(D,key))
                    if resource=='roles' and sub=='activities':return self.reply(200,[x for x in D['activities'] if x['role_id']==key])
                    if resource=='roles' and sub=='competencies':return self.reply(200,[x for x in D['role_competencies'] if x['role_id']==key])
                    if resource=='courses' and sub=='competencies':return self.reply(200,[x for x in D['course_competencies'] if x['course_id']==key])
                    if sub is not None:return self.reply(404,{'error':'Unknown resource'})
                    if resource=='competencies':item={**item,'levels':[x for x in D['competency_levels'] if x['competency_id']==key]}
                    if resource=='courses':item={**item,'learningOutcomes':[x for x in D['course_learning_outcomes'] if x['course_id']==key],'competencies':[x for x in D['course_competencies'] if x['course_id']==key],'resources':[find(D,'knowledge_resources','resource_id',x['resource_id']) for x in D['course_resources'] if x['course_id']==key],'modules':[],'tags':[],'contextCompleteness':'PARTIAL_NOT_VERIFIED_SYLLABUS'}
                    return self.reply(200,item)
            if parts[:3]==['api','v1','users'] and len(parts)==5:
                uid,action=parts[3:];j=journey(D,uid);scope=q.get('scope',['current'])[0].upper()
                if scope not in ('CURRENT','TARGET'):return self.reply(400,{'error':'scope must be current or target'})
                if action=='competency-gaps':return self.reply(200,[x for x in D['competency_gaps'] if x['user_id']==uid and x['scope']==scope])
                if action=='recommendations':return self.reply(200,[{**x,'course':find(D,'courses','course_id',x['course_id'])} for x in D['course_recommendations'] if x['user_id']==uid and find(D,'competency_gaps','gap_id',x['gap_id'])['scope']==scope])
                if action=='learning-path':return self.reply(200,{'notice':'This career-demo path uses TARGET scope explicitly.','path':j['learning_path'],'items':j['learning_path_items']})
                if action=='journey':return self.reply(200,j)
            return self.reply(404,{'error':'Not found'})
        except (KeyError,ValueError) as e:self.reply(400,{'error':str(e)})
        except Exception:self.reply(500,{'error':'Demo server failed; inspect local logs'})
    def do_POST(self):
        parts=urlparse(self.path).path.strip('/').split('/')
        if parts[:3]!=['api','v1','users'] or len(parts)!=5 or parts[4]!='competency-evidence':return self.reply(404,{'error':'Not found'})
        token=os.environ.get('SIH_DEMO_TOKEN','local-demo-only')
        if self.headers.get('Authorization')!='Bearer '+token:return self.reply(401,{'error':'Demo service token required'})
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size<1 or size>32768:return self.reply(413,{'error':'Payload must be 1-32768 bytes'})
            p=json.loads(self.rfile.read(size));D=load_db(self.server.db);result=ingest(D,parts[3],p);save_feedback(self.server.db,D);self.reply(200,result)
        except (ValueError,TypeError,AttributeError) as e:self.reply(400,{'error':str(e)})
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--port',type=int,default=8010);args=ap.parse_args()
    con=sqlite3.connect(ROOT/'data/demo.sqlite');con.execute('PRAGMA foreign_keys=ON')
    s=HTTPServer(('127.0.0.1',args.port),Handler);s.db=con
    print(f'Local synthetic demo: http://127.0.0.1:{args.port} (no live AI/iGOT)');s.serve_forever()
