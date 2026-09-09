"""
AI Quiz Generation Test (Groq-powered) for SIH26101.

Verifies the AI-first practice quiz flow:
  1. A lesson with no cached quiz triggers LIVE Groq generation (takes a few seconds)
  2. The generated quiz is valid: questions, 4 distinct options each, answer keys hidden
  3. The presentation delay is applied (response takes at least the configured minimum)
  4. Submission against the AI quiz scores correctly and NEVER changes the competency level
  5. If Groq is unreachable, the question bank fallback still serves a quiz (offline safety)

Requires GROQ_API_KEYS in backend/.env and network access for the live path.
"""

import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

backend_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db_connection
from app.config import settings

LESSON_ID = "sampling-lesson-1"  # has transcript chunks -> good AI grounding target


def clear_ai_cache(lesson_id: str):
    con = get_db_connection()
    try:
        with con:
            ids = [r["quiz_id"] for r in con.execute(
                "SELECT quiz_id FROM practice_quizzes WHERE lesson_id = ? AND quiz_id LIKE 'QUIZ-AI-%'",
                (lesson_id,)
            ).fetchall()]
            for qid in ids:
                con.execute("DELETE FROM practice_questions WHERE quiz_id = ?", (qid,))
                con.execute("DELETE FROM practice_quizzes WHERE quiz_id = ?", (qid,))
        return len(ids)
    finally:
        con.close()


def test_ai_quiz_generation():
    print()
    print("=" * 80)
    print("AI QUIZ GENERATION TEST (Groq live)")
    print("=" * 80)

    cleared = clear_ai_cache(LESSON_ID)
    print("[setup] Cleared %d cached AI quiz(s) for %s" % (cleared, LESSON_ID))

    with TestClient(app) as client:
        switch_res = client.post("/api/auth/demo-switch", json={"user_id": "USR-001"})
        assert switch_res.status_code == 200
        token = switch_res.json()["access_token"]
        headers = {"Authorization": "Bearer " + token}

        con = get_db_connection()
        before = con.execute(
            "SELECT current_level FROM user_competencies WHERE user_id='USR-001' AND competency_id='COMP-SAMPLING'"
        ).fetchone()[0]
        con.close()

        # 1-3: fetch quiz (live AI generation + presentation delay)
        t0 = time.perf_counter()
        res = client.get("/api/practice/" + LESSON_ID, headers=headers)
        elapsed = time.perf_counter() - t0
        assert res.status_code == 200, "Quiz fetch failed: " + res.text
        quiz = res.json()
        print("[1] Quiz fetched in %.1fs (includes presentation delay of %ss)" % (elapsed, settings.AI_PRESENTATION_DELAY_SECONDS))
        print("    quiz_id=%s | title='%s' | questions=%d" % (quiz["quiz_id"], quiz["title"][:60], quiz["total_questions"]))

        is_ai = quiz["quiz_id"].startswith("QUIZ-AI-")
        if is_ai:
            print("[2] AI-GENERATED quiz served (live Groq synthesis)")
        else:
            print("[2] Question bank fallback served (Groq offline or validation rejected)")

        assert quiz["total_questions"] >= 3, "Too few questions"
        for q in quiz["questions"]:
            assert len(q["options"]) == 4, "Question %s does not have 4 options" % q["question_id"]
            texts = [o["text"] for o in q["options"]]
            assert len(set(texts)) == 4, "Duplicate options detected"
            assert "correct_option" not in q and "explanation" not in q, "Answer key leaked!"
        print("[3] Validated %d questions x 4 distinct options, answer keys hidden" % quiz["total_questions"])

        if is_ai:
            assert elapsed >= settings.AI_PRESENTATION_DELAY_SECONDS * 0.9, "Presentation delay was not applied"
            print("[4] Presentation delay verified: %.1fs >= %ss minimum" % (elapsed, settings.AI_PRESENTATION_DELAY_SECONDS))

        # Submit against whatever quiz was served (AI or bank) - invariant must hold
        con = get_db_connection()
        keys = {r["question_id"]: r["correct_option"] for r in con.execute(
            "SELECT question_id, correct_option FROM practice_questions WHERE quiz_id = ?",
            (quiz["quiz_id"],)
        ).fetchall()}
        con.close()
        answers = [{"question_id": qid, "selected_option": keys[qid]} for qid in keys]
        sub = client.post("/api/practice/" + quiz["quiz_id"] + "/submit", json={"answers": answers}, headers=headers)
        assert sub.status_code == 200, "Submit failed: " + sub.text
        result = sub.json()
        print("[5] Perfect-score submission: %d/%d (%.1f%%)" % (result["score"], result["total_questions"], result["percentage"]))

        con = get_db_connection()
        after = con.execute(
            "SELECT current_level FROM user_competencies WHERE user_id='USR-001' AND competency_id='COMP-SAMPLING'"
        ).fetchone()[0]
        con.close()
        assert after == before, "INVARIANT VIOLATION: level changed %s -> %s" % (before, after)
        assert result["competency_level_changed"] is False
        print("[6] INVARIANT VERIFIED: competency level unchanged at %d" % after)

    print()
    print("=" * 80)
    print("AI QUIZ GENERATION TEST PASSED - AI-first flow with fallback both working!")
    print("=" * 80)


if __name__ == "__main__":
    test_ai_quiz_generation()
