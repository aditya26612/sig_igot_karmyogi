"""Restore the local demo DB from immutable seed JSON. Usage: python backend/reset_demo.py
Only affects data/demo.sqlite in this downloaded package. No external connections.
"""
from pathlib import Path
import json,sqlite3,os
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'data/dataset.json').read_text())
tmp=root/'data/demo-reset.sqlite'
if tmp.exists():tmp.unlink()
con=sqlite3.connect(tmp);con.execute('PRAGMA foreign_keys=ON');con.executescript((root/'sql/schema.sql').read_text())
for t in json.loads((root/'data/table_order.json').read_text()):
    for x in data[t]:con.execute('INSERT INTO '+t+' ('+','.join(x)+') VALUES ('+','.join('?' for _ in x)+')',list(x.values()))
con.commit();assert not con.execute('PRAGMA foreign_key_check').fetchall();con.close();os.replace(tmp,root/'data/demo.sqlite')
print('Local demo database restored to deterministic seed.')
