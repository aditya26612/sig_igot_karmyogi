"""
Verification script for Module 5: Proficiency Assessment & Supervisor Review Workflow
"""

import sys
from pathlib import Path

# Fix Windows console encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db_connection, load_db

def test_assessment_and_review_workflow():
    print("\n--- Testing Module 5: Proficiency Assessment & Supervisor Review Workflow ---")
    with TestClient(app) as client:
        # 1. Authenticate as Learner (USR-001)
        learner_switch = client.post("/api/auth/demo-switch", json={"user_id": "USR-001"})
        assert learner_switch.status_code == 200
        learner_token = learner_switch.json()["access_token"]
        learner_headers = {"Authorization": f"Bearer {learner_token}"}
        
        # Verify initial level is 2
        con = get_db_connection()
        try:
            D = load_db(con)
            c_entry = next((x for x in D["user_competencies"] if x["user_id"] == "USR-001" and x["competency_id"] == "COMP-SAMPLING"), None)
            assert c_entry["current_level"] == 2
            print(f"✓ Initial USR-001 COMP-SAMPLING level: Level {c_entry['current_level']}")
        finally:
            con.close()
            
        # 2. Learner views assessment detail
        res = client.get("/api/assessments/ASS-DEMO-PRACTICAL-001", headers=learner_headers)
        assert res.status_code == 200
        ass_detail = res.json()
        assert ass_detail["assessment_type"] == "PRACTICAL"
        assert len(ass_detail["tasks"]) == 2
        print(f"✓ GET /api/assessments/ASS-DEMO-PRACTICAL-001: '{ass_detail['title']}' ({len(ass_detail['tasks'])} practical tasks)")
        
        # 3. Learner submits practical task
        sub_payload = {
            "assessment_id": "ASS-DEMO-PRACTICAL-001",
            "competency_id": "COMP-SAMPLING",
            "practical_answers": {
                "TASK-01": {"allocation_stratum_A": 80, "allocation_stratum_B": 40},
                "TASK-02": {"basic_weight": 10, "justification": "Inverse of inclusion probability 0.10 guarantees unbiased estimation."}
            },
            "self_reported_score": 86.0
        }
        sub_res = client.post("/api/assessments/ASS-DEMO-PRACTICAL-001/submit", json=sub_payload, headers=learner_headers)
        assert sub_res.status_code == 200, f"Submission failed: {sub_res.text}"
        sub_data = sub_res.json()
        assert sub_data["status"] == "PENDING_REVIEW"
        submission_id = sub_data["submission_id"]
        print(f"✓ Assessment submitted: Submission ID '{submission_id}', Status: {sub_data['status']}")
        
        # INVARIANT: Level must NOT be promoted yet
        con = get_db_connection()
        try:
            D = load_db(con)
            c_entry = next((x for x in D["user_competencies"] if x["user_id"] == "USR-001" and x["competency_id"] == "COMP-SAMPLING"), None)
            assert c_entry["current_level"] == 2
            print("✓ Invariant confirmed: Level remains Level 2 while pending supervisor review")
        finally:
            con.close()
            
        # 4. Role Guard: Learner cannot access reviewer queue
        forbidden_res = client.get("/api/reviewer/queue", headers=learner_headers)
        assert forbidden_res.status_code == 403
        print("✓ Role guard verified: Learner rejected from reviewer queue with 403 Forbidden")
        
        # 5. Authenticate as Supervisor / Reviewer (reviewer-001)
        reviewer_switch = client.post("/api/auth/demo-switch", json={"user_id": "reviewer-001"})
        assert reviewer_switch.status_code == 200
        reviewer_token = reviewer_switch.json()["access_token"]
        reviewer_headers = {"Authorization": f"Bearer {reviewer_token}"}
        
        # Reviewer checks queue
        q_res = client.get("/api/reviewer/queue", headers=reviewer_headers)
        assert q_res.status_code == 200
        queue = q_res.json()
        assert len(queue) >= 1
        target_item = next((item for item in queue if item["submission_id"] == submission_id), None)
        assert target_item is not None
        print(f"✓ Supervisor queue verified: Found submission from '{target_item['learner_name']}' for {target_item['competency_label']}")
        print(f"   Current Level: L{target_item['current_level']} -> Proposed Level: L{target_item['proposed_level']} (Score: {target_item['overall_score']}%)")
        
        # 6. Supervisor Evaluates and Approves evidence
        decision_payload = {
            "approved": True,
            "reviewer_comments": "Verified practical sampling calculations against standard NSSO rubric. Frame allocation and design weights are completely accurate."
        }
        dec_res = client.post(f"/api/reviewer/{submission_id}/decision", json=decision_payload, headers=reviewer_headers)
        assert dec_res.status_code == 200, f"Decision failed: {dec_res.text}"
        dec_data = dec_res.json()
        assert dec_data["status"] == "APPROVED"
        assert dec_data["level_promoted"] is True
        assert dec_data["before_level"] == 2
        assert dec_data["after_level"] == 3
        assert dec_data["learning_path_recalculated"] is True
        print(f"✓ SUPERVISOR APPROVED PROMOTION: Level {dec_data['before_level']} -> Level {dec_data['after_level']}")
        print(f"   Message: {dec_data['message']}")
        
        # 7. Check that Learner's live state in engine reflects the promotion
        con = get_db_connection()
        try:
            D = load_db(con)
            promoted_comp = next((x for x in D["user_competencies"] if x["user_id"] == "USR-001" and x["competency_id"] == "COMP-SAMPLING"), None)
            assert promoted_comp["current_level"] == 3, f"Expected promoted level 3, found {promoted_comp['current_level']}"
            print(f"✓ DATABASE VERIFIED: User COMP-SAMPLING current_level is officially Level {promoted_comp['current_level']}")
        finally:
            con.close()
            
        # Check gap API: Unmet gap reduced from 2 to 1!
        gaps_res = client.get("/api/learner/gaps?scope=TARGET", headers=learner_headers)
        assert gaps_res.status_code == 200
        gaps = gaps_res.json()
        sampling_gap = next((g for g in gaps if g["competency_id"] == "COMP-SAMPLING"), None)
        assert sampling_gap is not None
        assert sampling_gap["current_level"] == 3
        assert sampling_gap["unmet_gap"] == 1 # (Required 4 - Current 3 = 1)
        print(f"✓ ENGINE RECOMPUTATION VERIFIED: Sampling unmet gap reduced to {sampling_gap['unmet_gap']} (Required: 4, Current: 3)")

if __name__ == "__main__":
    test_assessment_and_review_workflow()
    print("\n==================================================")
    print("MODULE 5 COMPLETED AND FULLY VERIFIED!")
    print("==================================================")
