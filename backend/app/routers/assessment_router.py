import json
import uuid
import hashlib
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db_connection, load_db
from app.auth import get_current_user
from app.services.i18n_service import normalize_lang, notice
from app.engine import find
from app.models.assessment_schemas import (
    AssessmentDetailDTO,
    PracticalTaskItem,
    AssessmentSubmissionRequest,
    AssessmentSubmissionResponse
)

router = APIRouter(prefix="/api/assessments", tags=["Proficiency Assessments"])

DEMO_ASSESSMENTS = [
    {
        "assessment_id": "ASS-DEMO-PRACTICAL-001",
        "title": "Practical Cadre Assessment: Sampling Design & Frame Verification",
        "competency_id": "COMP-SAMPLING",
        "competency_label": "Survey Sampling & Design",
        "assessment_type": "PRACTICAL",
        "rubric_version": "sampling-practical-demo-v1",
        "estimated_time_minutes": 45,
        "current_level": 2,
        "target_level": 3,
        "rules": [
            "This is a formal proficiency evaluation, visibly distinct from self-paced practice.",
            "Must calculate proportional sample allocation and design weights for the supplied population frame.",
            "Submissions require independent evaluation by an NSSO Supervisor / Assessor before competency levels update.",
            "Maximum 1 level promotion per approved practical assessment attempt."
        ],
        "tasks": [
            {
                "task_id": "TASK-01",
                "title": "Sampling Frame Audit & Stratum Allocation",
                "scenario": "A district survey covers two agrarian strata: Stratum A (800 enterprise units) and Stratum B (400 enterprise units). Total authorized sample size is 120 units.",
                "instructions": "Calculate the proportional sample allocation (n_A and n_B) and verify that sampling shares match population shares.",
                "expected_output_type": "NUMERICAL_ALLOCATION"
            },
            {
                "task_id": "TASK-02",
                "title": "Design Weight Derivation & Coverage Defense",
                "scenario": "A high-turnover sub-stratum of 50 units was sampled with selection probability 0.10.",
                "instructions": "Determine the basic design weight and explain why unweighted estimation would introduce bias in total output estimates.",
                "expected_output_type": "WRITTEN_JUSTIFICATION"
            }
        ],
        "notice": "Formal assessment generates reviewed official evidence. Practice scores cannot substitute for this assessment."
    },
    {
        "assessment_id": "ASS-DEMO-PRACTICAL-002",
        "title": "Practical Cadre Assessment: SQL Multi-Table Reconciliation & Registry Audits",
        "competency_id": "COMP-027",
        "competency_label": "SQL & Relational Databases",
        "assessment_type": "PRACTICAL",
        "rubric_version": "sql-practical-demo-v1",
        "estimated_time_minutes": 45,
        "current_level": 2,
        "target_level": 3,
        "rules": [
            "Formal proficiency assessment evaluated against SQL & Relational Databases rubric.",
            "Must demonstrate correct multi-table join semantics (reconciling survey vs tax registers).",
            "Must formulate window deduplication queries and justify NULL treatment in official statistics.",
            "Requires supervisor sign-off for Level 3 cadre promotion."
        ],
        "tasks": [
            {
                "task_id": "TASK-01",
                "title": "Survey-to-Tax Registry Discrepancy Outer Join",
                "scenario": "Establishment survey table `survey_est` (1,200 records) must be audited against GST tax register `gst_reg` (1,500 records). Discrepancies exist where firms operate without GST registration, or GST units are missing from the survey frame.",
                "instructions": "Formulate the SQL query using FULL OUTER JOIN to identify all mismatched enterprise IDs, and calculate the count of unregistered surveyed enterprises.",
                "expected_output_type": "SQL_QUERY"
            },
            {
                "task_id": "TASK-02",
                "title": "Window Deduplication & Three-Valued Logic Defense",
                "scenario": "Multiple enumerator visits resulted in duplicate household schedules with identical composite primary keys (`state_code`, `district_code`, `hh_id`).",
                "instructions": "Write a ROW_NUMBER() PARTITION query to isolate strictly the latest verified interview record, and explain why failing to handle NULL values in `COALESCE(electricity_expenditure, 0)` distorts stratum aggregate averages.",
                "expected_output_type": "WRITTEN_JUSTIFICATION"
            }
        ],
        "notice": "Formal assessment generates reviewed official evidence. Practice scores cannot substitute for this assessment."
    },
    {
        "assessment_id": "ASS-DEMO-PRACTICAL-003",
        "title": "Practical Cadre Assessment: Data Quality Auditing, Outlier Detection & Anonymization",
        "competency_id": "COMP-018",
        "competency_label": "Data Quality & Statistical Disclosure",
        "assessment_type": "PRACTICAL",
        "rubric_version": "quality-practical-demo-v1",
        "estimated_time_minutes": 45,
        "current_level": 2,
        "target_level": 3,
        "rules": [
            "Evaluated by NSSO Lead Assessor against Data Quality & SDC rubric.",
            "Must compute Tukey's outlier thresholds and specify hot-deck donor matching classes.",
            "Must formulate anonymization defense (k-anonymity, l-diversity, top-coding).",
            "Requires supervisor verification for Level 3 cadre promotion."
        ],
        "tasks": [
            {
                "task_id": "TASK-01",
                "title": "Tukey's IQR Outlier Calibration & Anomaly Screening",
                "scenario": "Monthly enterprise turnover in an industrial cluster exhibits Q1 = ₹12,000 and Q3 = ₹48,000. Three candidate outlier firms report turnover of ₹95,000, ₹165,000, and ₹310,000.",
                "instructions": "Calculate the Interquartile Range (IQR), the mild outlier boundary (Q3 + 1.5*IQR), and the extreme outlier boundary (Q3 + 3.0*IQR). Identify which of the three firms represent extreme anomalies requiring supervisor audit.",
                "expected_output_type": "NUMERICAL_ALLOCATION"
            },
            {
                "task_id": "TASK-02",
                "title": "Hot-Deck Donor Matching & k-Anonymity Defense",
                "scenario": "An official public microdata release includes demographic quasi-identifiers (district, age group, gender, primary occupation).",
                "instructions": "Specify the donor matching cell rules for item non-response in agricultural revenue, and defend why enforcing k-anonymity (k >= 5) with top-coding of top 1% wealth prevents re-identification attacks.",
                "expected_output_type": "WRITTEN_JUSTIFICATION"
            }
        ],
        "notice": "Formal assessment generates reviewed official evidence. Practice scores cannot substitute for this assessment."
    },
    {
        "assessment_id": "ASS-DEMO-PRACTICAL-004",
        "title": "Practical Cadre Assessment: Python Microdata Cleaning & Automated QA Pipelines",
        "competency_id": "COMP-025",
        "competency_label": "Python & Automated Survey Pipelines",
        "assessment_type": "PRACTICAL",
        "rubric_version": "python-practical-demo-v1",
        "estimated_time_minutes": 45,
        "current_level": 2,
        "target_level": 3,
        "rules": [
            "Evaluated against Python & Automated Survey Pipelines rubric.",
            "Must demonstrate vectorized Pandas survey weighting and validation assertions.",
            "Must specify automated data quality audit routines for multi-round surveys.",
            "Requires supervisor verification for Level 3 cadre promotion."
        ],
        "tasks": [
            {
                "task_id": "TASK-01",
                "title": "Vectorized Survey Weighting & Kish Effective Sample Size",
                "scenario": "A survey microdata file has 500 records with design weights ranging from 2.5 to 45.0, with weight mean = 10.0 and weight standard deviation = 8.0.",
                "instructions": "Write the vectorized Pandas expression to compute weighted average household expenditure `(df['exp'] * df['wt']).sum() / df['wt'].sum()`, and calculate Kish's design effect variance inflation factor: 1 + (std(w)/mean(w))^2.",
                "expected_output_type": "NUMERICAL_ALLOCATION"
            },
            {
                "task_id": "TASK-02",
                "title": "Automated Validation Gate Pipeline Defense",
                "scenario": "Daily CAPI returns are ingested through an automated Python ETL script before warehouse insertion.",
                "instructions": "Formulate the defensive assertion pipeline checking for zero-tolerance duplicate keys, non-negative expenditures, and Benford's first-digit distribution check for enumerator fabrication detection.",
                "expected_output_type": "WRITTEN_JUSTIFICATION"
            }
        ],
        "notice": "Formal assessment generates reviewed official evidence. Practice scores cannot substitute for this assessment."
    }
]

@router.get("", response_model=List[AssessmentDetailDTO])
def list_assessments(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Lists available formal proficiency assessments."""
    con = get_db_connection()
    try:
        D = load_db(con)
        uid = current_user["user_id"]
        
        results = []
        for a in DEMO_ASSESSMENTS:
            comp_entry = next((x for x in D["user_competencies"] if x["user_id"] == uid and x["competency_id"] == a["competency_id"]), None)
            cur_lvl = comp_entry["current_level"] if comp_entry else 2
            tasks = [PracticalTaskItem(**t) for t in a["tasks"]]
            results.append(AssessmentDetailDTO(
                assessment_id=a["assessment_id"],
                title=a["title"],
                competency_id=a["competency_id"],
                competency_label=a["competency_label"],
                assessment_type=a["assessment_type"],
                rubric_version=a["rubric_version"],
                estimated_time_minutes=a["estimated_time_minutes"],
                prerequisites_met=True,
                current_level=cur_lvl,
                target_level=min(cur_lvl + 1, 5),
                rules=a["rules"],
                tasks=tasks,
                notice=a["notice"]
            ))
        return results
    finally:
        con.close()

@router.get("/{assessment_id}", response_model=AssessmentDetailDTO)
def get_assessment_detail(assessment_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Returns assessment blueprint and task instructions."""
    item = next((a for a in DEMO_ASSESSMENTS if a["assessment_id"] == assessment_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Assessment not found")
        
    con = get_db_connection()
    try:
        D = load_db(con)
        uid = current_user["user_id"]
        comp_entry = next((x for x in D["user_competencies"] if x["user_id"] == uid and x["competency_id"] == item["competency_id"]), None)
        cur_lvl = comp_entry["current_level"] if comp_entry else 2
        
        tasks = [PracticalTaskItem(**t) for t in item["tasks"]]
        return AssessmentDetailDTO(
            assessment_id=item["assessment_id"],
            title=item["title"],
            competency_id=item["competency_id"],
            competency_label=item["competency_label"],
            assessment_type=item["assessment_type"],
            rubric_version=item["rubric_version"],
            estimated_time_minutes=item["estimated_time_minutes"],
            prerequisites_met=True,
            current_level=cur_lvl,
            target_level=min(cur_lvl + 1, 5),
            rules=item["rules"],
            tasks=tasks,
            notice=item["notice"]
        )
    finally:
        con.close()

@router.post("/{assessment_id}/submit", response_model=AssessmentSubmissionResponse)
def submit_assessment(
    assessment_id: str,
    submission: AssessmentSubmissionRequest,
    lang: str = "en",
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Submits practical assessment work.
    Packages evidence and places attempt into PENDING_REVIEW queue for supervisor verification.
    Invariant: Does NOT promote competency level at submission time.
    """
    item = next((a for a in DEMO_ASSESSMENTS if a["assessment_id"] == assessment_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Assessment not found")
        
    uid = current_user["user_id"]
    con = get_db_connection()
    try:
        # Check if already submitted and pending
        cur = con.execute(
            "SELECT submission_id, status FROM assessment_attempts WHERE assessment_id = ? AND user_id = ? AND status = 'PENDING_REVIEW'",
            (assessment_id, uid)
        )
        existing = cur.fetchone()
        if existing:
            return AssessmentSubmissionResponse(
                submission_id=existing["submission_id"],
                assessment_id=assessment_id,
                user_id=uid,
                status="PENDING_REVIEW",
                submitted_at=datetime.now(timezone.utc).isoformat(),
                notice=notice("assessment_pending", normalize_lang(lang))
            )
            
        submission_id = f"SUB-{assessment_id}-{uid}-{uuid.uuid4().hex[:6]}"
        now = datetime.now(timezone.utc).isoformat()
        
        # Package standard evidence payload matching engine.ingest specifications
        payload = {
            "userId": uid,
            "assessmentId": assessment_id,
            "assessmentType": "PRACTICAL",
            "overallScore": submission.self_reported_score or 86.0,
            "assessedAt": now,
            "rubricVersion": item["rubric_version"],
            "reviewed": False, # Will be set to True only upon supervisor approval
            "sourceType": "MOCK_BEHAVIOUR",
            "competencies": [
                {
                    "competencyId": item["competency_id"],
                    "score": submission.self_reported_score or 86.0,
                    "estimatedLevel": 3,
                    "confidence": 0.87,
                    "coverage": 0.90,
                    "itemCount": 5
                }
            ]
        }
        ph = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        
        with con:
            con.execute("""
            INSERT INTO assessment_attempts (
                submission_id, assessment_id, user_id, competency_id, assessment_type,
                rubric_version, overall_score, confidence, coverage, estimated_level,
                status, submitted_at, payload_json, payload_hash
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING_REVIEW', ?, ?, ?)
            """, (
                submission_id, assessment_id, uid, item["competency_id"], "PRACTICAL",
                item["rubric_version"], 86.0, 0.87, 0.90, 3,
                now, json.dumps(payload), ph
            ))
            
        return AssessmentSubmissionResponse(
            submission_id=submission_id,
            assessment_id=assessment_id,
            user_id=uid,
            status="PENDING_REVIEW",
            submitted_at=now,
            notice=notice("assessment_submit", normalize_lang(lang))
        )
    finally:
        con.close()

@router.get("/{assessment_id}/status")
def get_assessment_submission_status(assessment_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Returns the latest attempt status for the current learner."""
    con = get_db_connection()
    try:
        cur = con.execute(
            "SELECT submission_id, status, submitted_at, reviewed_at, reviewer_comments FROM assessment_attempts WHERE assessment_id = ? AND user_id = ? ORDER BY submitted_at DESC LIMIT 1",
            (assessment_id, current_user["user_id"])
        )
        row = cur.fetchone()
        if not row:
            return {"status": "NOT_STARTED", "assessment_id": assessment_id}
        return dict(row)
    finally:
        con.close()
