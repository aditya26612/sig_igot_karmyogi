import urllib.request
import json
from app.auth import create_access_token

tok = create_access_token({'sub': 'USR-001', 'role': 'LEARNER'})
lessons = [
    'sampling-lesson-1', 'sql-lesson-1', 'python-lesson-1',
    'r-lesson-1', 'prob-lesson-1', 'quality-lesson-1',
    'ml-lesson-1', 'dl-lesson-1'
]
for lid in lessons:
    req = urllib.request.Request(f'http://127.0.0.1:8000/api/practice/{lid}', headers={'Authorization': f'Bearer {tok}'})
    res = urllib.request.urlopen(req)
    data = json.loads(res.read())
    print(f"{lid}: {len(data['questions'])} questions -> {data['title']}")
