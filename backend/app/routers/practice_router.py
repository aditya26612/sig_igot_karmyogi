import json
import threading
import time
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from app.config import settings
from app.database import get_db_connection
from app.auth import get_current_user
from app.services.groq_service import groq_service
from app.services.i18n_service import normalize_lang, notice
from app.models.practice_schemas import (
    PracticeQuizDTO,
    PracticeQuestionDTO,
    PracticeOption,
    PracticeSubmissionRequest,
    PracticeSubmissionResponse,
    QuestionResultItem,
    PracticeAttemptHistoryItem
)

router = APIRouter(prefix="/api/practice", tags=["Practice Quizzes"])

_prewarm_inflight: set = set()
_prewarm_lock = threading.Lock()


def prewarm_quiz_for_lesson(lesson_id: str) -> None:
    """Fire-and-forget background quiz generation (spec section 9).

    Called when a learner opens a lesson/video so the Practice click is a
    cache hit. Idempotent and single-flight per lesson.
    """
    with _prewarm_lock:
        if lesson_id in _prewarm_inflight:
            return
        _prewarm_inflight.add(lesson_id)

    def _job():
        con = None
        try:
            con = get_db_connection()
            existing = con.execute(
                "SELECT 1 FROM practice_quizzes WHERE lesson_id = ? AND quiz_id LIKE 'QUIZ-AI-%'",
                (lesson_id,),
            ).fetchone()
            if existing:
                return
            lesson_row = con.execute(
                "SELECT * FROM curated_lessons WHERE lesson_id = ?", (lesson_id,)
            ).fetchone()
            if not lesson_row:
                return
            lesson = dict(lesson_row)
            chunks = [dict(r) for r in con.execute(
                "SELECT * FROM transcript_chunks WHERE lesson_id = ? ORDER BY start_seconds ASC",
                (lesson_id,),
            ).fetchall()]
            from app.services import retrieval_service
            ranked = retrieval_service.retrieve(
                lesson["title"], lesson_id=lesson_id, top_k=4, con=con)
            context = ranked if ranked else chunks
            questions = groq_service.generate_quiz_questions(lesson, context, num_questions=5)
            if questions:
                _persist_ai_quiz(con, lesson, questions)
        except Exception:
            pass  # prewarm is best-effort; the quiz endpoint regenerates on demand
        finally:
            if con is not None:
                con.close()
            with _prewarm_lock:
                _prewarm_inflight.discard(lesson_id)

    threading.Thread(target=_job, daemon=True).start()


def _quiz_notice(lang: str, ai_generated: bool) -> str:
    return notice("practice_quiz_ai" if ai_generated else "practice_quiz", lang)


def _persist_ai_quiz(con, lesson: Dict[str, Any], questions: List[Dict[str, Any]]) -> str:
    """Saves an AI-generated quiz + questions as an approved, reusable cache entry."""
    generated_quiz_id = f"QUIZ-AI-{lesson['lesson_id'].upper()}"
    now = datetime.now(timezone.utc).isoformat()
    with con:
        con.execute("""
        INSERT OR REPLACE INTO practice_quizzes (quiz_id, lesson_id, course_id, competency_id, title, topic, created_at)
        VALUES (?, ?, 'CRS-GEN', ?, ?, ?, ?)
        """, (
            generated_quiz_id, lesson["lesson_id"], lesson["competency_id"],
            f"AI-Generated Practice Quiz: {lesson['title']}", lesson["title"], now
        ))
        for q in questions:
            con.execute("""
            INSERT OR REPLACE INTO practice_questions (
                question_id, quiz_id, lesson_id, competency_id, question_text, options_json,
                correct_option, explanation, chunk_id, timestamp_label, difficulty, is_approved, review_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 'AI_GENERATED')
            """, (
                q["question_id"], generated_quiz_id, lesson["lesson_id"], lesson["competency_id"],
                q["question_text"], q["options_json"], q["correct_option"], q["explanation"],
                q.get("chunk_id"), q["timestamp_label"], q["difficulty"]
            ))
    return generated_quiz_id


@router.get("/{lesson_id}", response_model=PracticeQuizDTO)
def get_practice_quiz_for_lesson(
    lesson_id: str,
    lang: str = "en",
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Returns the practice quiz for a lesson.
    Prefers a cached AI-generated quiz, otherwise generates one live via Groq
    (with a short presentation delay so generation feels like real synthesis),
    and always falls back to the curated question bank on any AI failure.
    Omits answer keys and explanations to ensure honest practice.
    """
    con = get_db_connection()
    try:
        l_cur = con.execute("SELECT * FROM curated_lessons WHERE lesson_id = ?", (lesson_id,))
        lesson = l_cur.fetchone()
        if not lesson:
            raise HTTPException(status_code=404, detail=f"Lesson '{lesson_id}' not found in curriculum catalogue.")

        lang = normalize_lang(lang)
        notice = _quiz_notice(lang, ai_generated=False)

        # 1. Cached AI quiz from a previous generation?
        q_cur = con.execute(
            "SELECT * FROM practice_quizzes WHERE lesson_id = ? AND quiz_id LIKE 'QUIZ-AI-%'",
            (lesson_id,)
        )
        quiz = q_cur.fetchone()

        # 2. No cache -> generate live via Groq (never leaves the learner without a quiz)
        if not quiz:
            from app.services import retrieval_service
            ranked = retrieval_service.retrieve(
                lesson["title"], lesson_id=lesson_id, top_k=4, con=con)
            chunks = [dict(r) for r in con.execute(
                "SELECT * FROM transcript_chunks WHERE lesson_id = ? ORDER BY start_seconds ASC",
                (lesson_id,)
            ).fetchall()]
            ai_questions = groq_service.generate_quiz_questions(
                dict(lesson), ranked if ranked else chunks, num_questions=5)
            if ai_questions:
                if settings.AI_PRESENTATION_DELAY_SECONDS > 0:
                    time.sleep(settings.AI_PRESENTATION_DELAY_SECONDS)
                generated_quiz_id = _persist_ai_quiz(con, dict(lesson), ai_questions)
                quiz = con.execute(
                    "SELECT * FROM practice_quizzes WHERE quiz_id = ?", (generated_quiz_id,)
                ).fetchone()
                notice = _quiz_notice(lang, ai_generated=True)

        # 3. Curated question bank fallback (and template generator as last resort)
        if not quiz:
            q_cur = con.execute("SELECT * FROM practice_quizzes WHERE lesson_id = ?", (lesson_id,))
            quiz = q_cur.fetchone()
        if not quiz:
            # Legacy template path for lessons with no bank questions
            generated_quiz_id = f"QUIZ-{lesson_id.upper()}"
            title = f"Practice Quiz: {lesson['title']}"
            topic = lesson['title']
            now = datetime.now(timezone.utc).isoformat()

            with con:
                con.execute("""
                INSERT OR REPLACE INTO practice_quizzes (quiz_id, lesson_id, course_id, competency_id, title, topic, created_at)
                VALUES (?, ?, 'CRS-GEN', ?, ?, ?, ?)
                """, (generated_quiz_id, lesson_id, lesson["competency_id"], title, topic, now))

                c_cur = con.execute("SELECT * FROM transcript_chunks WHERE lesson_id = ? LIMIT 1", (lesson_id,))
                chunk = c_cur.fetchone()
                ts_label = chunk["timestamp_label"] if chunk else "02:00"
                chunk_id = chunk["chunk_id"] if chunk else None

                q1_id = f"Q-{lesson_id.upper()}-GEN-01"
                q1_text = f"What is the foundational requirement covered in '{lesson['title']}' for competency {lesson['competency_id']}?"
                q1_opts = [
                    {"option_id": "A", "text": "Adherence to standardized official statistical methodology and validation protocols"},
                    {"option_id": "B", "text": "Subjective estimation without documented verification frames"},
                    {"option_id": "C", "text": "Complete omission of quality controls to reduce survey turnaround time"},
                    {"option_id": "D", "text": "Replacing official registers with ad-hoc convenience samples"}
                ]
                con.execute("""
                INSERT OR REPLACE INTO practice_questions (
                    question_id, quiz_id, lesson_id, competency_id, question_text, options_json,
                    correct_option, explanation, chunk_id, timestamp_label, difficulty, is_approved, review_status
                )
                VALUES (?, ?, ?, ?, ?, ?, 'A', ?, ?, ?, 'MEDIUM', 1, 'APPROVED')
                """, (
                    q1_id, generated_quiz_id, lesson_id, lesson["competency_id"],
                    q1_text, json.dumps(q1_opts),
                    f"Official statistical operations require strict adherence to standard protocols and verified validation frameworks.",
                    chunk_id, ts_label
                ))

            quiz = con.execute("SELECT * FROM practice_quizzes WHERE lesson_id = ?", (lesson_id,)).fetchone()

        qn_cur = con.execute(
            "SELECT question_id, question_text, options_json, difficulty, chunk_id, timestamp_label FROM practice_questions WHERE quiz_id = ? AND is_approved = 1",
            (quiz["quiz_id"],)
        )
        rows = qn_cur.fetchall()

        questions = []
        for r in rows:
            raw_options = json.loads(r["options_json"])
            options = [PracticeOption(option_id=o["option_id"], text=o["text"]) for o in raw_options]
            questions.append(PracticeQuestionDTO(
                question_id=r["question_id"],
                question_text=r["question_text"],
                options=options,
                difficulty=r["difficulty"],
                topic=quiz["topic"],
                timestamp_label=r["timestamp_label"],
                chunk_id=r["chunk_id"]
            ))

        return PracticeQuizDTO(
            quiz_id=quiz["quiz_id"],
            lesson_id=quiz["lesson_id"],
            title=quiz["title"],
            topic=quiz["topic"],
            total_questions=len(questions),
            questions=questions,
            notice=notice
        )
    finally:
        con.close()

@router.post("/{quiz_id}/submit", response_model=PracticeSubmissionResponse)
def submit_practice_quiz(
    quiz_id: str,
    submission: PracticeSubmissionRequest,
    lang: str = "en",
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Evaluates learner practice quiz submission.
    Provides immediate feedback with citations and transcript timestamps.
    Invariant: NEVER alters competency level.
    """
    con = get_db_connection()
    try:
        q_cur = con.execute("SELECT * FROM practice_quizzes WHERE quiz_id = ?", (quiz_id,))
        quiz = q_cur.fetchone()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
            
        qn_cur = con.execute("SELECT * FROM practice_questions WHERE quiz_id = ?", (quiz_id,))
        question_rows = {r["question_id"]: r for r in qn_cur.fetchall()}
        
        user_answers = {a.question_id: a.selected_option.upper().strip() for a in submission.answers}
        
        score = 0
        total = len(question_rows)
        results = []
        weak_topics = set()
        
        for qid, q_data in question_rows.items():
            selected = user_answers.get(qid, "")
            correct = q_data["correct_option"].upper().strip()
            is_correct = (selected == correct)
            
            if is_correct:
                score += 1
            else:
                # Add to weak topics for personalized review
                weak_topics.add(quiz["topic"])
                
            results.append(QuestionResultItem(
                question_id=qid,
                question_text=q_data["question_text"],
                selected_option=selected,
                correct_option=correct,
                is_correct=is_correct,
                explanation=q_data["explanation"],
                timestamp_label=q_data["timestamp_label"],
                chunk_id=q_data["chunk_id"]
            ))
            
        pct = round((score / total) * 100, 1) if total > 0 else 0.0
        attempt_id = f"ATT-{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc).isoformat()
        
        # Save attempt record
        with con:
            con.execute("""
            INSERT INTO practice_attempts (
                attempt_id, user_id, quiz_id, lesson_id, competency_id, score,
                total_questions, percentage, answers_json, topic_breakdown_json, attempted_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                attempt_id, current_user["user_id"], quiz_id, quiz["lesson_id"],
                quiz["competency_id"], score, total, pct,
                json.dumps(user_answers), json.dumps(list(weak_topics)), now
            ))
            
        return PracticeSubmissionResponse(
            attempt_id=attempt_id,
            quiz_id=quiz_id,
            lesson_id=quiz["lesson_id"],
            score=score,
            total_questions=total,
            percentage=pct,
            weak_topics=list(weak_topics),
            results=results,
            notice=notice("practice_submit", lang),
            competency_level_changed=False
        )
    finally:
        con.close()

@router.get("/history/{user_id}", response_model=List[PracticeAttemptHistoryItem])
def get_practice_history(user_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Returns past practice attempts and scores for a learner."""
    con = get_db_connection()
    try:
        cur = con.execute(
            "SELECT attempt_id, quiz_id, lesson_id, score, total_questions, percentage, topic_breakdown_json, attempted_at FROM practice_attempts WHERE user_id = ? ORDER BY attempted_at DESC",
            (user_id,)
        )
        rows = cur.fetchall()
        return [
            PracticeAttemptHistoryItem(
                attempt_id=r["attempt_id"],
                quiz_id=r["quiz_id"],
                lesson_id=r["lesson_id"],
                score=r["score"],
                total_questions=r["total_questions"],
                percentage=r["percentage"],
                weak_topics=json.loads(r["topic_breakdown_json"] or "[]"),
                attempted_at=r["attempted_at"]
            ) for r in rows
        ]
    finally:
        con.close()
