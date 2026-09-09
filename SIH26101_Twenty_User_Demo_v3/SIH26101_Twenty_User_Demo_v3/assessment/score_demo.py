"""Scores fictional answers locally; no AI call. Never send trainer questions.json to learners."""
from pathlib import Path
import json
p=Path(__file__).parent
qs=json.loads((p/'questions.json').read_text())
answers=['A','B','C','A','A']
correct=sum(q['correct_option_id']==a for q,a in zip(qs,answers))
print(json.dumps({'provenance':'MOCK_BEHAVIOUR','correct':correct,'total':len(qs),'overallScore':100*correct/len(qs),'competencies':[{'competencyId':'COMP-SAMPLING','score':100*correct/len(qs),'estimatedLevel':None}],'notice':'Practice score only. Use fixtures/evidence_practice.json; it must not update competency level.'},indent=2))
