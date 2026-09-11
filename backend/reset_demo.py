"""
Restore the local demo DB to deterministic seed state.
Usage: python backend/reset_demo.py
"""

from pathlib import Path
import json
import sqlite3
import os
import sys

# Fix Windows console encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from app.database import init_db, get_db_connection
from app.auth import seed_demo_users
from app.services.transcript_service import seed_content_catalogue
from app.services.quiz_gen_service import seed_practice_data
from app.services import retrieval_service

def reset_database():
    root = backend_dir
    data = json.loads((root / 'data/dataset.json').read_text(encoding='utf-8'))
    tmp = root / 'data/demo-reset.sqlite'
    if tmp.exists():
        tmp.unlink()
        
    con = sqlite3.connect(tmp)
    con.execute('PRAGMA foreign_keys=ON')
    con.executescript((root / 'sql/schema.sql').read_text(encoding='utf-8'))
    
    table_names = json.loads((root / 'data/table_order.json').read_text(encoding='utf-8'))
    for t in table_names:
        for x in data[t]:
            con.execute(f"INSERT INTO {t} ({','.join(x)}) VALUES ({','.join('?' for _ in x)})", list(x.values()))
            
    con.commit()
    assert not con.execute('PRAGMA foreign_key_check').fetchall()
    con.close()
    
    target_db = root / 'data/demo.sqlite'
    if target_db.exists():
        try:
            target_db.unlink()
        except PermissionError:
            pass
            
    os.replace(tmp, target_db)
    
    # Initialize extensions & seed demo personas
    init_db()
    c = get_db_connection()
    try:
        seed_demo_users(c)
        seed_content_catalogue(c)
        seed_practice_data(c)
        # Fresh DB from schema.sql has an empty FTS index; seeded chunks must be
        # retrievable (rebuild_fts is idempotent).
        retrieval_service.rebuild_fts(c)
    finally:
        c.close()
        
    print('✓ Local demo database restored to clean deterministic seed state.')

if __name__ == '__main__':
    reset_database()
