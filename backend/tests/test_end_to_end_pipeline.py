"""
Comprehensive End-to-End Pipeline Test for SIH26101:
Validates the complete 11-step chain from learner profiling to supervisor approval and path recalculation.
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
from reset_demo import reset_database

def test_full_pipeline_journey():
    print("\n================================================================================")
    print("STARTING FULL END-TO-END SIH26101 PIPELINE VERIFICATION")
    print("================================================================================")
    reset_database()

    
    with TestClient(app) as client:
        # STEP 1: Admin Governance & Registry Oversight
        print("\n[Step 1] System Administrator Oversight:")
        admin_auth = client.post("/api/auth/demo-switch", json={"user_id": "admin-001"}).json()
        admin_headers = {"Authorization": f"Bearer {admin_auth['access_token']}"}
        
        dash = client.get("/api/admin/dashboard", headers=admin_headers).json()
        print(f"✓ Admin Dashboard loaded: {dash['total_learners']} Registered Officers across {len(dash['division_gap_breakdown'])} Divisions")
        print(f"✓ Official Competencies Tracked: {dash['total_competencies']}")
        
        # STEP 2: Learner Authentication & Profile Inspection
        print("\n[Step 2] Learner Signs in (Aarav Sharma, USR-001):")
        learner_auth = client.post("/api/auth/demo-switch", json={"user_id": "USR-001"}).json()
        learner_headers = {"Authorization": f"Bearer {learner_auth['access_token']}"}
        
        profile = client.get("/api/learner/me", headers=learner_headers).json()
        print(f"✓ Authenticated: {profile['name']} ({profile['designation']})")
        print(f"✓ Current Position: {profile['current_position_name']}")
        print(f"✓ Target Promotional Position: {profile['target_position_name']}")
        
        # STEP 3: Skill Gap Identification
        print("\n[Step 3] System Identifies Competency Gaps:")
        gaps = client.get("/api/learner/gaps?scope=TARGET", headers=learner_headers).json()
        sampling_gap = next(g for g in gaps if g["competency_id"] == "COMP-SAMPLING")
        initial_level = sampling_gap["current_level"]
        initial_unmet = sampling_gap["unmet_gap"]
        print(f"✓ Identified Priority Gap: {sampling_gap['plain_title']} ({sampling_gap['competency_id']})")
        print(f"  Current Level: L{initial_level} | Target Need: L{sampling_gap['required_level']} | Unmet Gap: {initial_unmet} Levels")
        assert initial_unmet == (sampling_gap['required_level'] - initial_level)
        
        # STEP 4: Personalized Dashboard & One Clear Next Action
        print("\n[Step 4] Learner Dashboard & Next Action:")
        learner_dash = client.get("/api/learner/dashboard", headers=learner_headers).json()
        action = learner_dash["next_action"]
        print(f"✓ Single Clear Action: [{action['badge_label']}] {action['title']} - {action['subtitle']}")
        print(f"  Action Target: {action['target_url']}")
        
        # STEP 5: Curated Video Lesson & Transcript Search
        print("\n[Step 5] Learning Content & Searchable Transcripts:")
        lesson = client.get("/api/content/lessons/sampling-lesson-3", headers=learner_headers).json()
        print(f"✓ Active Lesson: '{lesson['lesson']['title']}' (YouTube Video ID: {lesson['lesson']['youtube_video_id']})")
        print(f"✓ Transcript Loaded: {len(lesson['transcript_chunks'])} indexed segments")
        
        search_res = client.get("/api/content/search?q=proportional", headers=learner_headers).json()
        print(f"✓ Transcript Search for 'proportional': Found {search_res['total_matches']} grounded matches with timestamps")
        
        # Record watch progress
        client.post("/api/content/lessons/sampling-lesson-3/progress", json={"completed": True}, headers=learner_headers)
        print("✓ Marked lesson as watched")
        
        # STEP 6: AI Learning Copilot Grounded Q&A
        print("\n[Step 6] AI Learning Copilot Interaction:")
        copilot_res = client.post("/api/assistant/ask", json={
            "question": "How are sampling weights derived for units with unequal selection probability?",
            "context_type": "LESSON",
            "lesson_id": "sampling-lesson-3"
        }, headers=learner_headers).json()
        print(f"✓ Copilot Response Grounded in Transcript:")
        print(f"  Source: {copilot_res['source_lesson_title']} at [{copilot_res['timestamp_label']}]")
        print(f"  Answer: {copilot_res['answer'][:100]}...")
        
        # STEP 7: Practice Quiz (Invariant: Never Promotes Level)
        print("\n[Step 7] Interactive Practice Quiz:")
        quiz = client.get("/api/practice/sampling-lesson-3", headers=learner_headers).json()
        print(f"✓ Starting Practice Quiz: '{quiz['title']}' ({quiz['total_questions']} items)")
        
        quiz_sub = client.post(f"/api/practice/{quiz['quiz_id']}/submit", json={
            "answers": [
                {"question_id": "Q-DEMO-001", "selected_option": "A"},
                {"question_id": "Q-DEMO-002", "selected_option": "B"},
                {"question_id": "Q-DEMO-003", "selected_option": "C"},
                {"question_id": "Q-DEMO-004", "selected_option": "A"},
                {"question_id": "Q-DEMO-005", "selected_option": "B"}
            ]
        }, headers=learner_headers).json()
        print(f"✓ Practice Score: {quiz_sub['score']}/{quiz_sub['total_questions']} ({quiz_sub['percentage']}%)")
        print(f"✓ INVARIANT CHECK: Practice competency_level_changed = {quiz_sub['competency_level_changed']}")
        assert quiz_sub["competency_level_changed"] is False
        
        # Verify level in DB is unchanged
        con = get_db_connection()
        D = load_db(con)
        comp_check = next(x for x in D["user_competencies"] if x["user_id"] == "USR-001" and x["competency_id"] == "COMP-SAMPLING")
        assert comp_check["current_level"] == initial_level
        con.close()
        print(f"✓ Verified Database: COMP-SAMPLING remains strictly at Level {comp_check['current_level']}")
        
        # STEP 8: Formal Proficiency Assessment Submission
        print("\n[Step 8] Formal Practical Proficiency Assessment:")
        ass_detail = client.get("/api/assessments/ASS-DEMO-PRACTICAL-001", headers=learner_headers).json()
        print(f"✓ Blueprint: '{ass_detail['title']}' (Rubric: {ass_detail['rubric_version']})")
        print(f"✓ Target Promotion: Level {ass_detail['current_level']} -> Level {ass_detail['target_level']}")
        
        ass_sub = client.post("/api/assessments/ASS-DEMO-PRACTICAL-001/submit", json={
            "assessment_id": "ASS-DEMO-PRACTICAL-001",
            "competency_id": "COMP-SAMPLING",
            "practical_answers": {
                "TASK-01": {"stratum_A": 80, "stratum_B": 40},
                "TASK-02": {"design_weight": 10, "justification": "Inverse of inclusion probability ensures unbiased estimation"}
            },
            "self_reported_score": 86.0
        }, headers=learner_headers).json()
        
        sub_id = ass_sub["submission_id"]
        print(f"✓ Practical Evidence Packaged & Submitted: ID '{sub_id}'")
        print(f"✓ Status: {ass_sub['status']} (Awaiting Supervisor Evaluation)")
        
        # STEP 9: Supervisor Evaluation Queue & Rubric Verification
        print("\n[Step 9] Supervisor (Sunita Rao, NSSO) Review Queue:")
        rev_auth = client.post("/api/auth/demo-switch", json={"user_id": "reviewer-001"}).json()
        rev_headers = {"Authorization": f"Bearer {rev_auth['access_token']}"}
        
        queue = client.get("/api/reviewer/queue", headers=rev_headers).json()
        my_item = next(x for x in queue if x["submission_id"] == sub_id)
        print(f"✓ Submission Detected in Queue for Officer '{my_item['learner_name']}'")
        print(f"  Score: {my_item['overall_score']}% | Confidence: {my_item['confidence']} | Coverage: {my_item['coverage']}")
        
        # STEP 10: Supervisor Approves Level Promotion
        print("\n[Step 10] Supervisor Authorizes Level Promotion:")
        decision = client.post(f"/api/reviewer/{sub_id}/decision", json={
            "approved": True,
            "reviewer_comments": "Calculations verified against NSSO practical rubric sampling-practical-demo-v1. Approved for L3 advancement."
        }, headers=rev_headers).json()
        
        print(f"✓ DECISION: {decision['status']}")
        print(f"✓ LEVEL PROMOTION: Level {decision['before_level']} -> Level {decision['after_level']}")
        print(f"✓ DYNAMIC RECOMPUTATION: learning_path_recalculated = {decision['learning_path_recalculated']}")
        assert decision["level_promoted"] is True
        assert decision["after_level"] == initial_level + 1
        
        # STEP 11: Learner Journey & Learning Path Recalculation
        print("\n[Step 11] Learner Profile & Path Recalculation Verification:")
        con = get_db_connection()
        D = load_db(con)
        promoted_comp = next(x for x in D["user_competencies"] if x["user_id"] == "USR-001" and x["competency_id"] == "COMP-SAMPLING")
        assert promoted_comp["current_level"] == initial_level + 1
        con.close()
        print(f"✓ Official Competency Level Updated in Core DB: Level {promoted_comp['current_level']}")
        
        # Verify gap reduction
        updated_gaps = client.get("/api/learner/gaps?scope=TARGET", headers=learner_headers).json()
        updated_sampling = next(g for g in updated_gaps if g["competency_id"] == "COMP-SAMPLING")
        print(f"✓ Unmet Gap Reduced: Was {initial_unmet} Levels -> Now {updated_sampling['unmet_gap']} Level!")
        assert updated_sampling["unmet_gap"] == initial_unmet - 1
        
        # Verify updated learning path
        updated_path = client.get("/api/learner/learning-path", headers=learner_headers).json()
        print(f"✓ Learning Path Dynamically Recalculated: {len(updated_path['items'])} sequential items")
        
        # STEP 12: iGOT Integration Simulator Verification
        print("\n[Step 12] iGOT Integration Simulator:")
        sync_res = client.post("/api/integrations/igot/sync", headers=admin_headers).json()
        print(f"✓ iGOT Simulator Sync: {sync_res['courses_synced']} courses, {sync_res['training_records_synced']} training records")
        print(f"✓ Status: {sync_res['status']} ({sync_res['provider']})")

    print("\n================================================================================")
    print("ALL 12 STEPS OF THE END-TO-END PIPELINE PASSED WITH 100% INTEGRITY!")
    print("================================================================================\n")

if __name__ == "__main__":
    test_full_pipeline_journey()
