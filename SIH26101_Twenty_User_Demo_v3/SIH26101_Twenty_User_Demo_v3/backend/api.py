"""Preferred API entry point: camelCase boundary, snake_case relational storage.
Run python backend/api.py --port 8010. Demo-only service; bind to loopback.
"""
import argparse,json,sqlite3
from http.server import HTTPServer
from server import Handler,ROOT

def camel(key):
    parts=key.split('_');return parts[0]+''.join(s[:1].upper()+s[1:] for s in parts[1:])
def serialize(value):
    if isinstance(value,list):return [serialize(x) for x in value]
    if isinstance(value,dict):
        result={}
        for k,v in value.items():
            # JSON-in-TEXT is normalized into actual arrays/objects at the API boundary.
            if k in ('contributing_role_ids','contributing_activity_ids','max_level_activity_ids','learning_outcome_ids','score_components') and isinstance(v,str):v=json.loads(v)
            result[camel(k)]=serialize(v)
        return result
    return value
class APIHandler(Handler):
    def reply(self,status,data):super().reply(status,serialize(data))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--port',type=int,default=8010);args=ap.parse_args()
    con=sqlite3.connect(ROOT/'data/demo.sqlite');con.execute('PRAGMA foreign_keys=ON')
    s=HTTPServer(('127.0.0.1',args.port),APIHandler);s.db=con
    print(f'SIH26101 camelCase local demo API on http://127.0.0.1:{args.port}',flush=True);s.serve_forever()
