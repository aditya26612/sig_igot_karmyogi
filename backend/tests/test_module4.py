"""
Verification script for Module 4: Practice Quiz Engine (AI-Powered with Groq)
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
from app.engine import find
from reset_demo import reset_database

def test_practice_quiz():
    # Isolate from other module tests (e.g. module 5 promotes USR-001 to L3): start from the clean seed.
    reset_database()
    print("\n--- Testing Module 4: Practice Quiz Engine (Question Bank / Offline Fallback Path) ---")
    # Simulate Groq being unavailable so this module deterministically verifies the
    # curated question bank path. The live AI path is covered by test_quiz_ai_generation.py.
    from app.services import groq_service as _gs
    _gs.groq_service.generate_quiz_questions = lambda *a, **k: None
    with TestClient(app) as client:
        # 1. Authenticate as USR-001 (Aarav)
        switch_res = client.post("/api/auth/demo-switch", json={"user_id": "USR-001"})
        assert switch_res.status_code == 200
        token = switch_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Check initial level for COMP-SAMPLING
        con = get_db_connection()
        try:
            D = load_db(con)
            initial_comp = next((x for x in D["user_competencies"] if x["user_id"] == "USR-001" and x["competency_id"] == "COMP-SAMPLING"), None)
            initial_level = initial_comp["current_level"] if initial_comp else None
            assert initial_level == 2, f"Expected initial level 2, found {initial_level}"
            print(f"✓ Initial USR-001 level for COMP-SAMPLING is Level {initial_level}")
        finally:
            con.close()
            
        # 2. Test GET /api/practice/sampling-lesson-3
        #    (Question-bank path: remove any AI-cached quiz so the curated bank serves this request.
        #     The AI generation path is covered separately in test_quiz_ai_generation.py)
        con = get_db_connection()
        try:
            with con:
                ai_quiz_ids = [r["quiz_id"] for r in con.execute(
                    "SELECT quiz_id FROM practice_quizzes WHERE lesson_id = 'sampling-lesson-3' AND quiz_id LIKE 'QUIZ-AI-%'"
                ).fetchall()]
                for aid in ai_quiz_ids:
                    con.execute("DELETE FROM practice_questions WHERE quiz_id = ?", (aid,))
                    con.execute("DELETE FROM practice_quizzes WHERE quiz_id = ?", (aid,))
        finally:
            con.close()

        res = client.get("/api/practice/sampling-lesson-3", headers=headers)
        assert res.status_code == 200, f"GET practice quiz failed: {res.text}"
        quiz = res.json()
        assert quiz["quiz_id"] == "QUIZ-SAMPLING-03"
        assert quiz["total_questions"] == 5
        print(f"✓ GET /api/practice/sampling-lesson-3 returned bank quiz: '{quiz['title']}' ({quiz['total_questions']} questions)")

        # Verify answer keys are NOT exposed in question payload
        q1 = quiz["questions"][0]
        assert "correct_option" not in q1
        assert "explanation" not in q1
        assert len(q1["options"]) == 4
        print(f"✓ Answer keys properly hidden: Q1 has {len(q1['options'])} options with difficulty {q1['difficulty']}")

        # 3. Test POST /api/practice/QUIZ-SAMPLING-03/submit
        #    Answer 4 correctly and 1 wrong, using the ACTUAL bank keys from the DB
        con = get_db_connection()
        try:
            bank_rows = con.execute(
                "SELECT question_id, correct_option FROM practice_questions WHERE quiz_id = 'QUIZ-SAMPLING-03' ORDER BY question_id"
            ).fetchall()
        finally:
            con.close()
        assert len(bank_rows) == 5, f"Expected 5 bank questions, found {len(bank_rows)}"
        bank_keys = {r["question_id"]: r["correct_option"] for r in bank_rows}
        answers = []
        for qid, correct in bank_keys.items():
            # answer the first four correctly, miss the last one on purpose
            sel = correct if qid != list(bank_keys.keys())[-1] else "D"
            answers.append({"question_id": qid, "selected_option": sel})
        missed_qid = list(bank_keys.keys())[-1]
        
        sub_res = client.post(f"/api/practice/{quiz['quiz_id']}/submit", json={"answers": answers}, headers=headers)
        assert sub_res.status_code == 200, f"Submit failed: {sub_res.text}"
        result = sub_res.json()
        
        assert result["score"] == len(bank_keys) - 1
        assert result["total_questions"] == len(bank_keys)
        assert result["percentage"] == round((len(bank_keys) - 1) / len(bank_keys) * 100, 1)
        print(f"✓ Quiz evaluated: Score {result['score']}/{result['total_questions']} ({result['percentage']}%)")
        
        # Check explanations and citations returned
        assert len(result["results"]) == len(bank_keys)
        q5_res = next(r for r in result["results"] if r["question_id"] == missed_qid)
        assert q5_res["is_correct"] is False
        assert q5_res["correct_option"] == bank_keys[missed_qid]
        assert len(q5_res["explanation"]) > 20
        print(f"✓ Question-level feedback verified for incorrect item: correct option {q5_res['correct_option']}, explanation: '{q5_res['explanation'][:60]}...'")

        # Check weak topics
        assert len(result["weak_topics"]) > 0
        print(f"✓ Weak topics identified for revision: {result['weak_topics']}")
        
        # 4. CRITICAL INVARIANT: Verify practice CANNOT update competency level
        con = get_db_connection()
        try:
            D = load_db(con)
            post_comp = next((x for x in D["user_competencies"] if x["user_id"] == "USR-001" and x["competency_id"] == "COMP-SAMPLING"), None)
            post_level = post_comp["current_level"] if post_comp else None
            assert post_level == 2, f"INVARIANT VIOLATION! Practice quiz altered level to {post_level}"
            assert result["competency_level_changed"] is False
            assert "NOT change" in result["notice"]
            print(f"✓ CORE INVARIANT VERIFIED: Level remains at {post_level} (Practice quizzes NEVER upgrade proficiency)")
        finally:
            con.close()
            
        # 5. Test GET /api/practice/history/USR-001
        hist_res = client.get("/api/practice/history/USR-001", headers=headers)
        assert hist_res.status_code == 200
        history = hist_res.json()
        assert len(history) >= 1
        print(f"✓ GET /api/practice/history returned {len(history)} recorded attempt(s)")

if __name__ == "__main__":
    test_practice_quiz()
    print("\n==================================================")
    print("MODULE 4 COMPLETED AND FULLY VERIFIED!")
    print("==================================================")
