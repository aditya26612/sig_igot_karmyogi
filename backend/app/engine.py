"""
Deterministic SIH26101 Competency Engine.
Executes gap calculation, readiness evaluation, learning path recomputation, and evidence ingestion.
Zero synthetic hallucinations - follows verified MoSPI competency models.
"""

import copy
import hashlib
import json
import math
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

NOW = '2026-09-06T14:52:00Z'
DERIVED = ['competency_gaps', 'course_recommendations', 'learning_paths', 'learning_path_items']

def row(**kw) -> Dict[str, Any]:
    return {
        **kw,
        'provenance': 'DERIVED',
        'source_type': 'DERIVED',
        'source_id': 'SRC-PROJECT',
        'created_at': NOW,
        'updated_at': NOW
    }

def find(D: Dict[str, List[Dict[str, Any]]], table: str, key: str, value: Any) -> Optional[Dict[str, Any]]:
    return next((x for x in D.get(table, []) if x.get(key) == value), None)

def required(D: Dict[str, List[Dict[str, Any]]], pid: str) -> Dict[str, Dict[str, Any]]:
    """Calculates all competencies required by a position via its associated roles."""
    rr = [p['role_id'] for p in D.get('position_role', []) if p['position_id'] == pid]
    result: Dict[str, Dict[str, Any]] = {}
    for x in D.get('role_competencies', []):
        if x['role_id'] not in rr:
            continue
        c = x['competency_id']
        y = result.setdefault(c, {'required_level': 0, 'role_ids': [], 'activity_ids': []})
        y['required_level'] = max(y['required_level'], x['required_level'])
        y['role_ids'].append(x['role_id'])
        y['activity_ids'] += json.loads(x['contributing_activity_ids'])
        
    for y in result.values():
        y['role_ids'] = sorted(set(y['role_ids']))
        y['activity_ids'] = sorted(set(y['activity_ids']))
    return result

def readiness(gaps: List[Dict[str, Any]]) -> str:
    """Evaluates learning readiness based on competency gap distribution."""
    if any(g['gap_status'] == 'INSUFFICIENT_EVIDENCE' for g in gaps):
        return 'INSUFFICIENT_EVIDENCE'
    if any(g['gap_status'] == 'HIGH' for g in gaps):
        return 'CRITICAL_GAPS'
    n = sum(g['gap_status'] == 'MEDIUM' for g in gaps)
    return 'READY' if n == 0 else 'NEAR_READY' if n == 1 else 'DEVELOPMENT_REQUIRED'

def eligible(D: Dict[str, List[Dict[str, Any]]], g: Dict[str, Any], mode: str = 'DEMO') -> List[tuple]:
    """Finds courses verified to address an unmet competency gap."""
    if g['unmet_gap'] is None or g['unmet_gap'] <= 0:
        return []
    out = []
    for m in D.get('course_competencies', []):
        if m['competency_id'] != g['competency_id']:
            continue
        if m['provenance'] not in ('DERIVED', 'PUBLIC_OFFICIAL') or m['approval_status'] != 'APPROVED':
            continue
        c = find(D, 'courses', 'course_id', m['course_id'])
        if not c or c.get('tier') != 1 or not c.get('destination_verified') or not c.get('course_url'):
            continue
        if mode == 'PRODUCTION' and (not m.get('production_approved') or not c.get('live_access_verified')):
            continue
        if not (m['from_level'] <= g['current_level'] < m['to_level']):
            continue
        hist = [x for x in D.get('training_records', []) if x['user_id'] == g['user_id'] and x['course_id'] == c['course_id']]
        if any(x.get('status') == 'COMPLETED' for x in hist):
            continue
        prereq = [p for p in D.get('course_prerequisites', []) if p['course_id'] == c['course_id'] and p.get('is_mandatory')]
        if any(not any(h['user_id'] == g['user_id'] and h['course_id'] == p['prerequisite_course_id'] and h['status'] == 'COMPLETED' for h in D.get('training_records', [])) for p in prereq):
            continue
        out.append((c, m, any(x.get('status') == 'IN_PROGRESS' for x in hist)))
    return out

def recompute(D: Dict[str, List[Dict[str, Any]]], mode: str = 'DEMO') -> Dict[str, List[Dict[str, Any]]]:
    """Recomputes all derived tables: competency_gaps, course_recommendations, learning_paths, learning_path_items."""
    for t in DERIVED:
        D[t] = []
        
    for u in D.get('users', []):
        uid = u['user_id']
        current = {x['competency_id']: x['current_level'] for x in D.get('user_competencies', []) if x['user_id'] == uid}
        
        for scope, pid in [('CURRENT', u['position_id']), ('TARGET', u['target_position_id'])]:
            gaps = []
            for c, r in sorted(required(D, pid).items()):
                level = current.get(c)
                signed = None if level is None else r['required_level'] - level
                unmet = None if signed is None else max(0, signed)
                status = 'INSUFFICIENT_EVIDENCE' if unmet is None else 'HIGH' if unmet >= 2 else 'MEDIUM' if unmet == 1 else 'NO_GAP'
                gid = f"GAP-{uid}-{scope}-{c}"
                
                g = row(
                    gap_id=gid,
                    user_id=uid,
                    scope=scope,
                    position_id=pid,
                    competency_id=c,
                    required_level=r['required_level'],
                    current_level=level,
                    signed_gap=signed,
                    unmet_gap=unmet,
                    gap_status=status,
                    priority='DIAGNOSTIC_REQUIRED' if unmet is None else status,
                    recommendation_status='ASSESSMENT_REQUIRED' if unmet is None else 'NOT_NEEDED' if unmet == 0 else 'NO_VERIFIED_COURSE',
                    contributing_role_ids=json.dumps(r['role_ids']),
                    contributing_activity_ids=json.dumps(r['activity_ids'])
                )
                choices = eligible(D, g, mode)
                if choices:
                    g['recommendation_status'] = 'VERIFIED_DESTINATION_DEMO_MAPPING' if mode == 'DEMO' else 'RECOMMENDABLE'
                D['competency_gaps'].append(g)
                gaps.append(g)
                
                for course, m, resume in choices:
                    delta = min(unmet, m['to_level'] - level)
                    parts = {
                        'competency_match': 40 * m['relevance_weight'],
                        'gap_severity': 20 * unmet / 4,
                        'role_relevance': 15,
                        'activity_relevance': 10,
                        'level_match': 10 * delta / unmet,
                        'prerequisites': 5,
                        'duplicate_penalty': 0
                    }
                    outcomes = [
                        o['learning_outcome_id'] for o in D.get('course_learning_outcomes', [])
                        if o['course_id'] == course['course_id'] and any(
                            l['learning_outcome_id'] == o['learning_outcome_id'] and l['competency_id'] == c
                            for l in D.get('learning_outcome_competency', [])
                        )
                    ]
                    comp_entry = find(D, 'competencies', 'competency_id', c)
                    label = comp_entry['label'] if comp_entry else c
                    
                    D['course_recommendations'].append(row(
                        recommendation_id=f"REC-{gid}-{course['course_id']}",
                        gap_id=gid,
                        user_id=uid,
                        course_id=course['course_id'],
                        competency_id=c,
                        rank=0,
                        score=round(sum(parts.values()), 3),
                        score_components=json.dumps(parts, sort_keys=True),
                        reason=f"{label}: current L{level}, required L{r['required_level']}; activities {', '.join(r['activity_ids'])}. {'Resume' if resume else 'Consider'} this documented iGOT course for supporting learning. Level/outcome alignment has SIMULATED trainer approval only. Course completion never awards a competency level.",
                        learning_outcome_ids=json.dumps(outcomes),
                        remaining_gap_after_planned_learning=max(0, r['required_level'] - m['to_level']),
                        is_bridge=int(m['to_level'] < r['required_level']),
                        eligibility_mode=mode,
                        production_eligible=int(mode == 'PRODUCTION')
                    ))
                    
            recs = [x for x in D['course_recommendations'] if x['user_id'] == uid and find(D, 'competency_gaps', 'gap_id', x['gap_id'])['scope'] == scope]
            recs.sort(key=lambda x: (-x['score'], x['course_id'], x['competency_id']))
            for i, x in enumerate(recs, 1):
                x['rank'] = i
                
            if scope != 'TARGET':
                continue
                
            pathid = f"PATH-{uid}"
            rs = readiness(gaps)
            blocked = any(g['recommendation_status'] == 'NO_VERIFIED_COURSE' for g in gaps)
            D['learning_paths'].append(row(
                learning_path_id=pathid,
                user_id=uid,
                scope='TARGET',
                target_position_id=pid,
                readiness_status=rs,
                status='ASSESSMENT_NEEDED' if rs == 'INSUFFICIENT_EVIDENCE' else 'CATALOGUE_LIMITED' if blocked else 'COMPETENCIES_MET' if rs == 'READY' else 'DEMO_LEARNING_AVAILABLE',
                rule_version='sih-demo-v2.0'
            ))
            
            items = []
            # Diagnostics precede training
            for g in gaps:
                if g['unmet_gap'] is None:
                    items.append(('DIAGNOSTIC', 'ASSESSMENT', g, None, 'REQUIRED', 'Collect evidence before calculating a gap'))
            for rec in recs:
                g = find(D, 'competency_gaps', 'gap_id', rec['gap_id'])
                resume = any(h['user_id'] == uid and h['course_id'] == rec['course_id'] and h['status'] == 'IN_PROGRESS' for h in D.get('training_records', []))
                items.append(('INTERMEDIATE', 'IGOT_COURSE', g, rec['course_id'], 'IN_PROGRESS' if resume else 'AVAILABLE_WITH_CAVEAT', 'Resume on iGOT' if resume else 'Learn on iGOT'))
            for g in gaps:
                if g['unmet_gap'] is None or g['unmet_gap'] == 0:
                    continue
                comp_item = find(D, 'competencies', 'competency_id', g['competency_id'])
                c = comp_item['label'] if comp_item else g['competency_id']
                if g['recommendation_status'] == 'NO_VERIFIED_COURSE':
                    items.append(('FOUNDATION' if (g['current_level'] or 0) <= 2 else 'ADVANCED', 'CATALOGUE_GAP', g, None, 'BLOCKED', f"No verified course for {c}; obtain approved material"))
                elif any(x['gap_id'] == g['gap_id'] and x['is_bridge'] for x in recs):
                    items.append(('ADVANCED', 'CATALOGUE_GAP', g, None, 'BLOCKED', f"Bridge course does not cover final target in {c}; source advanced material"))
                items.append(('PRACTICAL', 'PLANNED_PRACTICE', g, None, 'PLANNED_NOT_PUBLISHED', 'Trainer-reviewed practical task required; do not infer mastery from course completion'))
                items.append(('ASSESSMENT', 'PLANNED_ASSESSMENT', g, None, 'PLANNED_NOT_PUBLISHED', 'Collect competency-wise evidence and recalculate'))
                
            order = {'DIAGNOSTIC': 0, 'FOUNDATION': 1, 'INTERMEDIATE': 2, 'ADVANCED': 3, 'PRACTICAL': 4, 'ASSESSMENT': 5}
            items.sort(key=lambda x: order[x[0]])
            for i, (stage, typ, g, course, st, label) in enumerate(items, 1):
                D['learning_path_items'].append(row(
                    path_item_id=f"{pathid}-{i:02}",
                    learning_path_id=pathid,
                    sequence_no=i,
                    stage=stage,
                    item_type=typ,
                    competency_id=g['competency_id'],
                    course_id=course,
                    gap_id=g['gap_id'],
                    status=st,
                    action_label=label
                ))
    return D

def journey(D: Dict[str, List[Dict[str, Any]]], uid: str) -> Dict[str, Any]:
    """Retrieves full competency journey, positions, roles, gaps, and recommendations for a learner."""
    u = find(D, 'users', 'user_id', uid)
    if not u:
        raise KeyError(f"User {uid} not found")
        
    cur = find(D, 'positions', 'position_id', u['position_id'])
    tar = find(D, 'positions', 'position_id', u['target_position_id'])
    
    def roles(pid):
        return [find(D, 'roles', 'role_id', r['role_id']) for r in D.get('position_role', []) if r['position_id'] == pid]
        
    path = find(D, 'learning_paths', 'user_id', uid)
    
    return {
        'provenance': 'SYNTHETIC',
        'notice': 'Fictional employee. Nested records retain their own provenance. Readiness is competency-only, not promotion eligibility.',
        'user': u,
        'mdo': find(D, 'mdos', 'mdo_id', u['mdo_id']),
        'division': find(D, 'divisions', 'division_id', u['division_id']),
        'current_position': cur,
        'target_position': tar,
        'current_roles': roles(cur['position_id']) if cur else [],
        'target_roles': roles(tar['position_id']) if tar else [],
        'current_competencies': [
            {
                **x,
                'current_level': x['current_level'] if x['current_level'] is not None else 'UNKNOWN',
                'label': find(D, 'competencies', 'competency_id', x['competency_id'])['label']
            } for x in D.get('user_competencies', []) if x['user_id'] == uid
        ],
        'current_gaps': [x for x in D.get('competency_gaps', []) if x['user_id'] == uid and x['scope'] == 'CURRENT'],
        'target_gaps': [x for x in D.get('competency_gaps', []) if x['user_id'] == uid and x['scope'] == 'TARGET'],
        'priority_gaps': [x for x in D.get('competency_gaps', []) if x['user_id'] == uid and x['scope'] == 'TARGET' and x['priority'] in ('HIGH', 'DIAGNOSTIC_REQUIRED')],
        'recommendations': [
            {
                **r,
                'course': find(D, 'courses', 'course_id', r['course_id']),
                'learning_outcomes': [
                    o for o in D.get('course_learning_outcomes', [])
                    if o['learning_outcome_id'] in json.loads(r['learning_outcome_ids'])
                ]
            } for r in D.get('course_recommendations', []) if r['user_id'] == uid and find(D, 'competency_gaps', 'gap_id', r['gap_id'])['scope'] == 'TARGET'
        ],
        'learning_path': path,
        'learning_path_items': [x for x in D.get('learning_path_items', []) if path and x['learning_path_id'] == path['learning_path_id']],
        'readiness_status': path['readiness_status'] if path else 'UNKNOWN'
    }

def ingest(D: Dict[str, List[Dict[str, Any]]], uid: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ingests evaluated assessment evidence and updates competency levels if approved.
    Enforces maximum 1 level promotion, rubric compliance, and idempotent submission.
    """
    if not find(D, 'users', 'user_id', uid):
        raise ValueError('Unknown user')
    if payload.get('userId') != uid:
        raise ValueError('Path and payload userId differ')
    if payload.get('sourceType') != 'MOCK_BEHAVIOUR':
        raise ValueError('Demo endpoint accepts MOCK_BEHAVIOUR only')
        
    aid = payload.get('assessmentId')
    typ = payload.get('assessmentType')
    rubric = payload.get('rubricVersion')
    
    if not isinstance(aid, str) or not aid or len(aid) > 100:
        raise ValueError('Invalid assessmentId')
    if typ not in ('PRACTICAL', 'DIAGNOSTIC', 'PRACTICE'):
        raise ValueError('Invalid assessmentType')
        
    VALID_PRACTICAL_RUBRICS = {
        'sampling-practical-demo-v1': 'COMP-SAMPLING',
        'sql-practical-demo-v1': 'COMP-027',
        'quality-practical-demo-v1': 'COMP-018',
        'python-practical-demo-v1': 'COMP-025',
    }
    
    if rubric not in VALID_PRACTICAL_RUBRICS and rubric != 'sampling-practice-demo-v1':
        raise ValueError('Unknown demo rubric')
    if typ == 'PRACTICAL' and rubric not in VALID_PRACTICAL_RUBRICS:
        raise ValueError('Practical requires practical rubric')
        
    def num(v, lo, hi):
        return type(v) in (int, float) and math.isfinite(v) and lo <= v <= hi
        
    if not num(payload.get('overallScore'), 0, 100):
        raise ValueError('Invalid overallScore')
        
    when = payload.get('assessedAt')
    try:
        parsed = datetime.fromisoformat(when.replace('Z', '+00:00'))
        if parsed.tzinfo is None:
            raise ValueError()
    except Exception:
        raise ValueError('assessedAt must be a timezone-aware ISO timestamp')
        
    comp = payload.get('competencies')
    if not isinstance(comp, list) or not comp:
        raise ValueError('Missing competencies')
        
    seen = set()
    for c in comp:
        cid = c.get('competencyId')
        if cid in seen or not find(D, 'competencies', 'competency_id', cid):
            raise ValueError('Duplicate or unknown competency')
        seen.add(cid)
        expected_cid = VALID_PRACTICAL_RUBRICS.get(rubric, 'COMP-SAMPLING')
        if cid != expected_cid:
            raise ValueError(f'This demo rubric assesses {expected_cid} only')
        if not num(c.get('score'), 0, 100) or not num(c.get('confidence'), 0, 1) or not num(c.get('coverage'), 0, 1):
            raise ValueError('Invalid score/confidence/coverage')
        if type(c.get('itemCount')) is not int or c['itemCount'] < 1:
            raise ValueError('Invalid itemCount')
        level = c.get('estimatedLevel')
        if level is not None and (type(level) is not int or not 1 <= level <= 5):
            raise ValueError('Invalid estimatedLevel')
        if typ == 'PRACTICAL' and level != 3:
            raise ValueError('Fixed practical rubric supports L3 only')
        if typ != 'PRACTICAL' and level is not None:
            raise ValueError('This practice rubric does not estimate competency level')
            
    ph = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()
    old = [x for x in D.get('competency_evidence', []) if x['user_id'] == uid and x['assessment_id'] == aid]
    if old:
        if all(x.get('payload_hash') == ph for x in old) and {x['competency_id'] for x in old} == seen:
            return {'status': 'IDEMPOTENT_REPLAY', 'assessmentId': aid, 'provenance': 'MOCK_BEHAVIOUR', 'updates': []}
        raise ValueError('Assessment ID reused with different content')
        
    staged = copy.deepcopy(D)
    updates = []
    for c in comp:
        cid = c['competencyId']
        state = next((x for x in staged.get('user_competencies', []) if x['user_id'] == uid and x['competency_id'] == cid), None)
        if state is None:
            state = {
                'user_id': uid,
                'competency_id': cid,
                'current_level': 2,
                'level_status': 'KNOWN',
                'confidence': 0.70,
                'assessed_at': None,
                'source': 'DEFAULT_PROFILE',
                'provenance': 'MOCK_BEHAVIOUR',
                'source_type': 'MOCK_BEHAVIOUR',
                'created_at': when,
                'updated_at': when
            }
            staged.setdefault('user_competencies', []).append(state)
        level = state['current_level']
        est = c.get('estimatedLevel')
        applied = False
        
        # Promotions only, max +1. Older evidence is stored, not applied.
        fresh = state.get('assessed_at') is None or parsed >= datetime.fromisoformat(state['assessed_at'].replace('Z', '+00:00'))
        reviewed = payload.get('reviewed') is True
        if typ == 'PRACTICAL' and reviewed and c['confidence'] >= 0.8 and c['coverage'] >= 0.8 and c['itemCount'] >= 5 and level is not None and est > level and fresh:
            new = min(level + 1, est)
            state.update(
                current_level=new,
                level_status='KNOWN',
                confidence=c['confidence'],
                assessed_at=when,
                source='SIMULATED_PRACTICAL_ASSESSMENT',
                provenance='MOCK_BEHAVIOUR',
                source_type='MOCK_BEHAVIOUR',
                updated_at=when
            )
            applied = True
            updates.append({'competencyId': cid, 'before': level, 'after': new})
            
        ev = row(
            evidence_id='EVD-' + hashlib.sha256((uid + '|' + aid + '|' + cid).encode()).hexdigest()[:24],
            user_id=uid,
            competency_id=cid,
            assessment_id=aid,
            assessment_type=typ,
            evidence_type='ASSESSMENT_SCORE',
            score=c['score'],
            estimated_level=est,
            confidence=c['confidence'],
            date=when,
            coverage=c['coverage'],
            item_count=c['itemCount'],
            rubric_version=rubric,
            reviewed=int(reviewed),
            state_update_applied=int(applied),
            payload_hash=ph
        )
        ev.update(provenance='MOCK_BEHAVIOUR', source_type='MOCK_BEHAVIOUR', source_id='SRC-MOCK', created_at=when, updated_at=when)
        staged['competency_evidence'].append(ev)
        
    recompute(staged)
    D.clear()
    D.update(staged)
    return {
        'status': 'ACCEPTED',
        'assessmentId': aid,
        'provenance': 'MOCK_BEHAVIOUR',
        'updates': updates,
        'notice': 'Simulated practical-rubric evidence, not percentage-to-level conversion or official certification.'
    }
