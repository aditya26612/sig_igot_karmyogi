import json
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db_connection, load_db, save_feedback
from app.auth import get_current_user, require_role
from app.engine import ingest, find
from app.models.assessment_schemas import (
    ReviewQueueItemDTO,
    ReviewDecisionRequest,
    ReviewDecisionResponse
)

from app.routers.assessment_router import DEMO_ASSESSMENTS

router = APIRouter(prefix="/api/reviewer", tags=["Supervisor Review & Governance"])

@router.get("/queue", response_model=List[ReviewQueueItemDTO])
def get_review_queue(
    current_user: Dict[str, Any] = Depends(require_role(["ADMIN", "REVIEWER"]))
):
    """
    Returns pending practical assessment submissions awaiting supervisor evaluation.
    Only accessible by authorized Supervisors (Reviewers) and Admins.
    """
    con = get_db_connection()
    try:
        D = load_db(con)
        cur = con.execute("""
        SELECT 
            submission_id, assessment_id, user_id, competency_id,
            rubric_version, overall_score, confidence, coverage,
            estimated_level, status, submitted_at
        FROM assessment_attempts
        WHERE status = 'PENDING_REVIEW'
        ORDER BY submitted_at ASC
        """)
        rows = cur.fetchall()
        
        results = []
        for r in rows:
            u = find(D, "users", "user_id", r["user_id"])
            c = find(D, "competencies", "competency_id", r["competency_id"])
            comp_entry = next((x for x in D["user_competencies"] if x["user_id"] == r["user_id"] and x["competency_id"] == r["competency_id"]), None)
            cur_lvl = comp_entry["current_level"] if comp_entry else 2
            ass_def = next((a for a in DEMO_ASSESSMENTS if a["assessment_id"] == r["assessment_id"]), None)
            ass_title = ass_def["title"] if ass_def else "Practical Cadre Assessment"
            
            results.append(ReviewQueueItemDTO(
                submission_id=r["submission_id"],
                user_id=r["user_id"],
                learner_name=u["name"] if u else r["user_id"],
                assessment_id=r["assessment_id"],
                assessment_title=ass_title,
                competency_id=r["competency_id"],
                competency_label=c["label"] if c else r["competency_id"],
                current_level=cur_lvl,
                proposed_level=r["estimated_level"],
                overall_score=r["overall_score"],
                confidence=r["confidence"],
                coverage=r["coverage"],
                rubric_version=r["rubric_version"],
                submitted_at=r["submitted_at"],
                status=r["status"]
            ))
        return results
    finally:
        con.close()

@router.post("/{submission_id}/decision", response_model=ReviewDecisionResponse)
def review_submission(
    submission_id: str,
    decision: ReviewDecisionRequest,
    current_user: Dict[str, Any] = Depends(require_role(["ADMIN", "REVIEWER"]))
):
    """
    Evaluates evidence against official rubric and authorizes competency level promotion.
    Upon approval:
      1. Calls engine.ingest() enforcing maximum +1 level promotion rule
      2. Persists updated competency state & evidence
      3. Automatically triggers engine.recompute() recalculating learning path
    """
    con = get_db_connection()
    try:
        cur = con.execute("SELECT * FROM assessment_attempts WHERE submission_id = ?", (submission_id,))
        sub = cur.fetchone()
        if not sub:
            raise HTTPException(status_code=404, detail="Submission not found")
        if sub["status"] != "PENDING_REVIEW":
            raise HTTPException(status_code=400, detail=f"Submission is already {sub['status']}")
            
        uid = sub["user_id"]
        cid = sub["competency_id"]
        now = datetime.now(timezone.utc).isoformat()
        
        D = load_db(con)
        comp_entry = next((x for x in D["user_competencies"] if x["user_id"] == uid and x["competency_id"] == cid), None)
        before_level = comp_entry["current_level"] if comp_entry else None
        
        if decision.approved:
            # Prepare payload for engine.ingest
            payload = json.loads(sub["payload_json"])
            payload["assessmentId"] = sub["submission_id"]
            payload["reviewed"] = True
            payload["assessedAt"] = now
            if decision.adjusted_score is not None:
                payload["overallScore"] = decision.adjusted_score
                payload["competencies"][0]["score"] = decision.adjusted_score
                
            # Ingest evidence & recompute engine derived tables
            ingest_result = ingest(D, uid, payload)
            save_feedback(con, D)
            
            # Find updated level
            updated_entry = next((x for x in D["user_competencies"] if x["user_id"] == uid and x["competency_id"] == cid), None)
            after_level = updated_entry["current_level"] if updated_entry else before_level
            
            with con:
                con.execute("""
                UPDATE assessment_attempts
                SET status = 'APPROVED', reviewer_id = ?, reviewer_comments = ?, reviewed_at = ?
                WHERE submission_id = ?
                """, (current_user["user_id"], decision.reviewer_comments, now, submission_id))
                
                # Record audit log
                con.execute("""
                INSERT INTO audit_logs (log_id, actor_id, action, entity_type, entity_id, details, timestamp)
                VALUES (?, ?, 'APPROVE_ASSESSMENT_EVIDENCE', 'COMPETENCY_EVIDENCE', ?, ?, ?)
                """, (
                    f"LOG-{uuid.uuid4().hex[:12]}", current_user["user_id"], submission_id,
                    f"Competency {cid} promoted from L{before_level} to L{after_level}. Reviewer: {current_user['full_name']}",
                    now
                ))
                
            return ReviewDecisionResponse(
                submission_id=submission_id,
                status="APPROVED",
                level_promoted=(after_level != before_level),
                before_level=before_level,
                after_level=after_level,
                learning_path_recalculated=True,
                message=f"Assessment verified against rubric {sub['rubric_version']}. Competency '{cid}' updated from Level {before_level} to Level {after_level}. Target learning path successfully recalculated."
            )
        else:
            with con:
                con.execute("""
                UPDATE assessment_attempts
                SET status = 'REJECTED', reviewer_id = ?, reviewer_comments = ?, reviewed_at = ?
                WHERE submission_id = ?
                """, (current_user["user_id"], decision.reviewer_comments, now, submission_id))
                
                con.execute("""
                INSERT INTO audit_logs (log_id, actor_id, action, entity_type, entity_id, details, timestamp)
                VALUES (?, ?, 'REJECT_ASSESSMENT_EVIDENCE', 'COMPETENCY_EVIDENCE', ?, ?, ?)
                """, (
                    f"LOG-{uuid.uuid4().hex[:12]}", current_user["user_id"], submission_id,
                    f"Assessment rejected. Reviewer feedback: {decision.reviewer_comments}",
                    now
                ))
                
            return ReviewDecisionResponse(
                submission_id=submission_id,
                status="REJECTED",
                level_promoted=False,
                before_level=before_level,
                after_level=before_level,
                learning_path_recalculated=False,
                message="Submission marked as Needs Improvement. Learner notified to complete further practice."
            )
    finally:
        con.close()
