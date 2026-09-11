import json
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db_connection, load_db, save_feedback
from app.auth import require_role
from app.engine import find, recompute, row

router = APIRouter(prefix="/api/admin", tags=["Admin Portal & Governance"])


def _index_uploaded_chunk(con, chunk_id: str) -> None:
    """Indexes an admin-uploaded chunk into transcript_fts inside the caller's
    transaction, so uploads are searchable immediately (not only after a full
    rebuild)."""
    con.execute(
        "INSERT INTO transcript_fts (chunk_id, text_content, topic) "
        "SELECT chunk_id, text_content, COALESCE(topic, '') "
        "FROM transcript_chunks WHERE chunk_id = ?",
        (chunk_id,),
    )


class AdminDashboardMetrics(BaseModel):
    total_learners: int
    learners_with_critical_gaps: int
    total_competencies: int
    assessment_backlog: int
    content_curated_playlists: int
    total_lessons: int
    division_gap_breakdown: Dict[str, int]

class LearnerAdminListItem(BaseModel):
    user_id: str
    name: str
    email: str
    designation: str
    division_name: str
    current_position_name: str
    target_position_name: str
    readiness_status: str
    target_gaps_count: int
    priority_gaps_count: int

class RegisterLearnerRequest(BaseModel):
    name: str
    email: str
    designation: str
    division_id: str = "DIV-001"
    position_id: str = "POS-001"
    target_position_id: str = "POS-002"
    experience_years: int = 1

class RegisterLearnerResponse(BaseModel):
    user_id: str
    name: str
    email: str
    status: str
    message: str

class TranscriptUploadRequest(BaseModel):
    lesson_id: str
    topic: str
    text_content: str
    timestamp_label: str = "00:00"
    start_seconds: int = 0
    end_seconds: int = 300

class QuestionReviewDecision(BaseModel):
    is_approved: bool
    review_status: str # 'APPROVED', 'REJECTED', 'NEEDS_EDIT'

@router.get("/dashboard", response_model=AdminDashboardMetrics)
def get_admin_dashboard(current_user: Dict[str, Any] = Depends(require_role(["ADMIN"]))):
    """Returns official governance metrics for MoSPI competency oversight."""
    con = get_db_connection()
    try:
        D = load_db(con)
        users = D.get("users", [])
        competencies = D.get("competencies", [])
        paths = D.get("learning_paths", [])
        
        critical_learners = sum(1 for p in paths if p.get("readiness_status") in ("CRITICAL_GAPS", "DEVELOPMENT_REQUIRED"))
        
        # Count backlog
        cur = con.execute("SELECT COUNT(*) as cnt FROM assessment_attempts WHERE status = 'PENDING_REVIEW'")
        backlog_count = cur.fetchone()["cnt"]
        
        # Count playlists & lessons
        p_cur = con.execute("SELECT COUNT(*) as cnt FROM curated_playlists")
        playlist_count = p_cur.fetchone()["cnt"]
        l_cur = con.execute("SELECT COUNT(*) as cnt FROM curated_lessons")
        lesson_count = l_cur.fetchone()["cnt"]
        
        # Division gaps breakdown
        div_gaps: Dict[str, int] = {}
        for g in D.get("competency_gaps", []):
            if g.get("gap_status") in ("HIGH", "MEDIUM") and g.get("scope") == "TARGET":
                u = find(D, "users", "user_id", g["user_id"])
                if u:
                    d = find(D, "divisions", "division_id", u["division_id"])
                    dname = d["name"] if d else u["division_id"]
                    div_gaps[dname] = div_gaps.get(dname, 0) + 1
                    
        return AdminDashboardMetrics(
            total_learners=len(users),
            learners_with_critical_gaps=critical_learners,
            total_competencies=len(competencies),
            assessment_backlog=backlog_count,
            content_curated_playlists=playlist_count,
            total_lessons=lesson_count,
            division_gap_breakdown=div_gaps
        )
    finally:
        con.close()

@router.get("/learners", response_model=List[LearnerAdminListItem])
def list_learners_admin(current_user: Dict[str, Any] = Depends(require_role(["ADMIN"]))):
    """Returns comprehensive list of registered learners with competency readiness metrics."""
    con = get_db_connection()
    try:
        D = load_db(con)
        users = D.get("users", [])
        results = []
        
        for u in users:
            div = find(D, "divisions", "division_id", u["division_id"])
            cur_p = find(D, "positions", "position_id", u["position_id"])
            tar_p = find(D, "positions", "position_id", u["target_position_id"])
            path = find(D, "learning_paths", "user_id", u["user_id"])
            
            target_gaps = [x for x in D.get("competency_gaps", []) if x["user_id"] == u["user_id"] and x["scope"] == "TARGET"]
            priority_gaps = [x for x in target_gaps if x.get("priority") in ("HIGH", "DIAGNOSTIC_REQUIRED")]
            
            results.append(LearnerAdminListItem(
                user_id=u["user_id"],
                name=u["name"],
                email=u["email"],
                designation=u["designation"],
                division_name=div["name"] if div else u["division_id"],
                current_position_name=cur_p["name"] if cur_p else u["position_id"],
                target_position_name=tar_p["name"] if tar_p else u["target_position_id"],
                readiness_status=path["readiness_status"] if path else "UNKNOWN",
                target_gaps_count=len(target_gaps),
                priority_gaps_count=len(priority_gaps)
            ))
        return results
    finally:
        con.close()

@router.post("/learners", response_model=RegisterLearnerResponse)
def register_learner(
    learner: RegisterLearnerRequest,
    current_user: Dict[str, Any] = Depends(require_role(["ADMIN"]))
):
    """
    Registers a new learner into the official statistical system registry.
    Automatically assigns role competencies and recomputes the learning baseline.
    """
    con = get_db_connection()
    try:
        D = load_db(con)
        new_uid = f"USR-{len(D['users']) + 1:03d}"
        now = datetime.now(timezone.utc).isoformat()
        
        # New User Record
        u = row(
            user_id=new_uid,
            mdo_id="MDO-001",
            division_id=learner.division_id,
            position_id=learner.position_id,
            target_position_id=learner.target_position_id,
            name=learner.name,
            email=learner.email,
            designation=learner.designation,
            experience_years=learner.experience_years,
            status="ACTIVE",
            scenario="Admin Registered Officer",
            career_note="Registered via MoSPI Competency Platform Admin console."
        )
        D["users"].append(u)
        
        # Initialize default user competencies for position
        pos_roles = [p["role_id"] for p in D.get("position_role", []) if p["position_id"] == learner.position_id]
        assigned_comp = set()
        for rc in D.get("role_competencies", []):
            if rc["role_id"] in pos_roles and rc["competency_id"] not in assigned_comp:
                assigned_comp.add(rc["competency_id"])
                D["user_competencies"].append(row(
                    user_id=new_uid,
                    competency_id=rc["competency_id"],
                    current_level=1,
                    level_status="KNOWN",
                    confidence=0.75,
                    assessed_at=now,
                    source="INITIAL_ADMIN_BASELINE"
                ))
                
        # Recompute derived tables
        recompute(D)
        
        # Persist new user and competencies
        with con:
            con.execute("""
            INSERT INTO users (
                user_id, mdo_id, division_id, position_id, target_position_id, name,
                email, designation, experience_years, status, scenario, career_note,
                source_id, provenance, source_type, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'SRC-PROJECT', 'DERIVED', 'DERIVED', ?, ?)
            """, (
                u["user_id"], u["mdo_id"], u["division_id"], u["position_id"],
                u["target_position_id"], u["name"], u["email"], u["designation"],
                u["experience_years"], u["status"], u["scenario"], u["career_note"],
                now, now
            ))
            
            for uc in [x for x in D["user_competencies"] if x["user_id"] == new_uid]:
                con.execute("""
                INSERT INTO user_competencies (
                    user_id, competency_id, current_level, level_status, confidence,
                    assessed_at, source, source_id, provenance, source_type, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, 'SRC-PROJECT', 'DERIVED', 'DERIVED', ?, ?)
                """, (
                    uc["user_id"], uc["competency_id"], uc["current_level"], uc["level_status"],
                    uc["confidence"], uc["assessed_at"], uc["source"], now, now
                ))
                
        save_feedback(con, D)
        
        return RegisterLearnerResponse(
            user_id=new_uid,
            name=learner.name,
            email=learner.email,
            status="REGISTERED",
            message=f"Learner '{learner.name}' successfully registered as {new_uid}. Baseline competencies and target learning path established."
        )
    finally:
        con.close()

@router.post("/content/upload-transcript")
def upload_transcript(
    req: TranscriptUploadRequest,
    current_user: Dict[str, Any] = Depends(require_role(["ADMIN"]))
):
    """Uploads and indexes an administrative transcript chunk for a lesson."""
    con = get_db_connection()
    try:
        # Derive course/competency from the lesson itself (previously hardcoded CRS-101/COMP-SAMPLING)
        l_cur = con.execute(
            "SELECT course_id, competency_id FROM transcript_chunks WHERE lesson_id = ? LIMIT 1",
            (req.lesson_id,)
        )
        existing = l_cur.fetchone()
        if existing:
            course_id, competency_id = existing["course_id"], existing["competency_id"]
        else:
            les_cur = con.execute(
                "SELECT competency_id FROM curated_lessons WHERE lesson_id = ?", (req.lesson_id,)
            )
            lesson = les_cur.fetchone()
            if not lesson:
                raise HTTPException(status_code=404, detail=f"Lesson '{req.lesson_id}' not found in curriculum catalogue.")
            course_id, competency_id = "CRS-ADM", lesson["competency_id"]

        chunk_id = f"CHK-ADM-{uuid.uuid4().hex[:8]}"
        with con:
            con.execute("""
            INSERT INTO transcript_chunks (
                chunk_id, lesson_id, course_id, competency_id, topic,
                start_seconds, end_seconds, timestamp_label, text_content, summary, provenance
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'ADMIN_UPLOAD')
            """, (
                chunk_id, req.lesson_id, course_id, competency_id, req.topic, req.start_seconds,
                req.end_seconds, req.timestamp_label, req.text_content,
                req.text_content[:80] + "..."
            ))
            _index_uploaded_chunk(con, chunk_id)
            con.execute("""
            INSERT INTO audit_logs (log_id, actor_id, action, entity_type, entity_id, details, timestamp)
            VALUES (?, ?, 'TRANSCRIPT_INDEXED', 'TRANSCRIPT_CHUNK', ?, ?, ?)
            """, (
                f"LOG-{uuid.uuid4().hex[:12]}", current_user["user_id"], chunk_id,
                f"Admin indexed transcript chunk for lesson {req.lesson_id} (topic: {req.topic}).",
                datetime.now(timezone.utc).isoformat()
            ))
        return {
            "status": "INDEXED",
            "chunk_id": chunk_id,
            "lesson_id": req.lesson_id,
            "competency_id": competency_id,
            "topic": req.topic
        }
    finally:
        con.close()

@router.get("/audit-logs")
def list_audit_logs(
    limit: int = 50,
    current_user: Dict[str, Any] = Depends(require_role(["ADMIN"]))
):
    """Returns the most recent governance audit events (approvals, syncs, uploads)."""
    con = get_db_connection()
    try:
        limit = max(1, min(limit, 200))
        cur = con.execute(
            "SELECT log_id, actor_id, action, entity_type, entity_id, details, timestamp "
            "FROM audit_logs ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        return [dict(r) for r in cur.fetchall()]
    finally:
        con.close()

@router.get("/questions/review")
def list_questions_for_review(current_user: Dict[str, Any] = Depends(require_role(["ADMIN"]))):
    """Returns practice questions for administrator quality review."""
    con = get_db_connection()
    try:
        cur = con.execute("SELECT * FROM practice_questions ORDER BY question_id ASC")
        return [dict(r) for r in cur.fetchall()]
    finally:
        con.close()

@router.post("/questions/{question_id}/review")
def review_question(
    question_id: str,
    decision: QuestionReviewDecision,
    current_user: Dict[str, Any] = Depends(require_role(["ADMIN"]))
):
    """Approves or rejects a practice question."""
    con = get_db_connection()
    try:
        with con:
            con.execute("""
            UPDATE practice_questions
            SET is_approved = ?, review_status = ?
            WHERE question_id = ?
            """, (int(decision.is_approved), decision.review_status, question_id))
        return {
            "status": "UPDATED",
            "question_id": question_id,
            "review_status": decision.review_status
        }
    finally:
        con.close()
