import json
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from app.database import get_db_connection, load_db
from app.auth import get_current_user
from app.engine import journey, find, required
from app.services.i18n_service import (normalize_lang, greeting, notice,
    readiness_label as i18n_readiness_label, gap_status_label)
from app.models.learner_schemas import (
    LearnerProfileDetail,
    OfficialCompetencyItem,
    NextActionItem,
    CompetencyGapItem,
    LearningPathItemDTO,
    LearningPathDTO,
    LearnerDashboardResponse,
    CareerReadinessResponse
)

router = APIRouter(prefix="/api/learner", tags=["Learner Journey"])

PLAIN_COMPETENCY_DESCRIPTIONS = {
    "COMP-SAMPLING": {
        "title": "Survey Sampling & Design",
        "description": "Designing representative sample frames, calculating sampling weights, and auditing coverage for national surveys."
    },
    "COMP-027": {
        "title": "SQL & Relational Database Querying",
        "description": "Writing complex multi-table joins, deduplicating survey registries, and reconciling large administrative datasets."
    },
    "COMP-025": {
        "title": "Python for Official Statistics",
        "description": "Automating statistical data transformation, cleaning survey microdata, and running repeatable analysis pipelines."
    },
    "COMP-026": {
        "title": "R Programming & Statistical Computing",
        "description": "Computing survey estimates, running regression models, and generating statistical charts."
    },
    "COMP-018": {
        "title": "Data Quality & Anomaly Detection",
        "description": "Detecting survey outliers, handling missing values, and auditing statistical indicators."
    },
    "COMP-009": {
        "title": "Applied Statistical Theory & Estimation",
        "description": "Understanding probability distributions, variance estimation, and standard error calculation."
    }
}

def resolve_target_user_id(current_user: Dict[str, Any], user_id_param: Optional[str]) -> str:
    """If user is Admin/Reviewer and specifies user_id, use that. Otherwise use current user's id."""
    if current_user["role"] in ("ADMIN", "REVIEWER") and user_id_param:
        return user_id_param
    # If user_id starts with USR-, use it, else default to USR-001 for admin testing
    if current_user["user_id"].startswith("USR-"):
        return current_user["user_id"]
    return user_id_param or "USR-001"

def build_gap_item(g: Dict[str, Any], D: Dict[str, Any], target_pos_name: str) -> CompetencyGapItem:
    cid = g["competency_id"]
    comp = find(D, "competencies", "competency_id", cid)
    label = comp["label"] if comp else cid
    plain = PLAIN_COMPETENCY_DESCRIPTIONS.get(cid, {
        "title": label,
        "description": f"Target role requires verified application of {label} in official statistics."
    })
    
    act_ids = json.loads(g.get("contributing_activity_ids", "[]"))
    return CompetencyGapItem(
        gap_id=g["gap_id"],
        competency_id=cid,
        competency_label=label,
        plain_title=plain["title"],
        plain_explanation=plain["description"],
        current_level=g["current_level"],
        required_level=g["required_level"],
        unmet_gap=g["unmet_gap"],
        gap_status=g["gap_status"],
        priority=g["priority"],
        target_role_name=target_pos_name,
        contributing_activities=act_ids,
        recommendation_status=g["recommendation_status"],
        has_recommended_course=g["recommendation_status"] in ("VERIFIED_DESTINATION_DEMO_MAPPING", "RECOMMENDABLE")
    )

@router.get("/me", response_model=LearnerProfileDetail)
def get_learner_profile(
    user_id: Optional[str] = Query(None, description="Optional user_id for Admin/Reviewer inspection"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    uid = resolve_target_user_id(current_user, user_id)
    con = get_db_connection()
    try:
        D = load_db(con)
        u = find(D, "users", "user_id", uid)
        if not u:
            raise HTTPException(status_code=404, detail=f"Learner {uid} not found in official registry")
            
        cur_pos = find(D, "positions", "position_id", u["position_id"])
        tar_pos = find(D, "positions", "position_id", u["target_position_id"])
        div = find(D, "divisions", "division_id", u["division_id"])
        mdo = find(D, "mdos", "mdo_id", u["mdo_id"])

        # Official competency levels (source of truth: user_competencies, updated on supervisor approval)
        target_reqs = required(D, u["target_position_id"])
        target_gap_by_cid = {g["competency_id"]: g for g in D.get("competency_gaps", []) if g["user_id"] == uid and g["scope"] == "TARGET"}
        official_competencies = []
        for x in D.get("user_competencies", []):
            if x["user_id"] != uid:
                continue
            comp = find(D, "competencies", "competency_id", x["competency_id"])
            req = target_reqs.get(x["competency_id"], {}).get("required_level")
            gap = target_gap_by_cid.get(x["competency_id"])
            official_competencies.append(OfficialCompetencyItem(
                competency_id=x["competency_id"],
                label=comp["label"] if comp else x["competency_id"],
                current_level=x["current_level"],
                level_label=f"Level {x['current_level']}" if x["current_level"] is not None else "Not Assessed",
                required_level=req,
                gap_status=gap["gap_status"] if gap else None
            ))
        official_competencies.sort(key=lambda c: (c.required_level is None, -(c.required_level or 0), c.label))

        # Recently approved evidence promotions (what the supervisor upgraded)
        recent_promotions = []
        for a in con.execute(
            "SELECT competency_id, estimated_level, reviewed_at FROM assessment_attempts WHERE user_id = ? AND status = 'APPROVED' ORDER BY reviewed_at DESC LIMIT 5",
            (uid,)
        ).fetchall():
            comp = find(D, "competencies", "competency_id", a["competency_id"])
            entry = next((x for x in D.get("user_competencies", []) if x["user_id"] == uid and x["competency_id"] == a["competency_id"]), None)
            lvl = entry["current_level"] if entry and entry["current_level"] is not None else a["estimated_level"]
            recent_promotions.append(OfficialCompetencyItem(
                competency_id=a["competency_id"],
                label=comp["label"] if comp else a["competency_id"],
                current_level=lvl,
                level_label=f"Level {lvl}",
                required_level=None,
                gap_status=None
            ))

        return LearnerProfileDetail(
            user_id=u["user_id"],
            name=u["name"],
            email=u["email"],
            designation=u["designation"],
            department=mdo["name"] if mdo else "Ministry of Statistics and Programme Implementation",
            division=div["name"] if div else "Field Operations Division",
            mdo=mdo["name"] if mdo else "MoSPI",
            current_position_id=u["position_id"],
            current_position_name=cur_pos["name"] if cur_pos else u["position_id"],
            target_position_id=u["target_position_id"],
            target_position_name=tar_pos["name"] if tar_pos else u["target_position_id"],
            experience_years=u["experience_years"],
            status=u["status"],
            official_competencies=official_competencies,
            recent_promotions=recent_promotions
        )
    finally:
        con.close()

@router.get("/dashboard", response_model=LearnerDashboardResponse)
def get_learner_dashboard(
    user_id: Optional[str] = Query(None, description="Optional user_id for Admin/Reviewer inspection"),
    lang: str = "en",
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    uid = resolve_target_user_id(current_user, user_id)
    con = get_db_connection()
    try:
        D = load_db(con)
        j = journey(D, uid)
        u = j["user"]
        tar_pos = j["target_position"]["name"] if j["target_position"] else "Target Role"
        
        # Build priority gaps (top 2-3)
        priority_gaps = [
            build_gap_item(g, D, tar_pos)
            for g in j["priority_gaps"][:3]
        ]
        
        # Path items preview
        path_items = []
        for item in j["learning_path_items"][:5]:
            comp = find(D, "competencies", "competency_id", item["competency_id"])
            course = find(D, "courses", "course_id", item["course_id"]) if item["course_id"] else None
            path_items.append(LearningPathItemDTO(
                path_item_id=item["path_item_id"],
                sequence_no=item["sequence_no"],
                stage=item["stage"],
                item_type=item["item_type"],
                competency_id=item["competency_id"],
                competency_label=comp["label"] if comp else item["competency_id"],
                course_id=item["course_id"],
                course_title=course["title"] if course else None,
                status=item["status"],
                action_label=item["action_label"]
            ))
            
        # Determine ONE CLEAR NEXT ACTION
        # If user has a high-priority gap in COMP-SAMPLING:
        hi = normalize_lang(lang) == "hi"
        first_item = j["learning_path_items"][0] if j["learning_path_items"] else None
        if first_item and first_item["item_type"] == "IGOT_COURSE":
            next_action = NextActionItem(
                action_type="CONTINUE_LESSON",
                title="सर्वेक्षण प्रतिदर्शन अभिकल्पना जारी रखें" if hi else "Continue Survey Sampling Design",
                subtitle="पाठ 3: स्तरित प्रतिदर्शन एवं जनसंख्या भार" if hi else "Lesson 3: Stratified Sampling & Population Weights",
                competency_id="COMP-SAMPLING",
                competency_label="सर्वेक्षण प्रतिदर्शन" if hi else "Survey Sampling",
                target_url="/learning/lesson/sampling-lesson-3",
                button_label="पाठ देखें एवं अभ्यास करें" if hi else "Watch Lesson & Practice",
                badge_label="अगला चरण" if hi else "Next Step"
            )
        elif first_item and first_item["stage"] == "PRACTICAL":
            next_action = NextActionItem(
                action_type="START_ASSESSMENT",
                title="व्यावहारिक दक्षता मूल्यांकन" if hi else "Practical Proficiency Assessment",
                subtitle="व्यावहारिक फ्रेम अंकेक्षण एवं प्रतिदर्श आवंटन कार्य" if hi else "Practical Frame Audit & Sample Allocation Task",
                competency_id=first_item["competency_id"],
                competency_label="व्यावहारिक मूल्यांकन" if hi else "Practical Evaluation",
                target_url="/assessments/ASS-DEMO-PRACTICAL-001",
                button_label="व्यावहारिक कार्य प्रारंभ करें" if hi else "Begin Practical Task",
                badge_label="मूल्यांकन आवश्यक" if hi else "Assessment Required"
            )
        else:
            next_action = NextActionItem(
                action_type="CONTINUE_LESSON",
                title="मूल दक्षताएँ सुदृढ़ करें" if hi else "Strengthen Core Competencies",
                subtitle="अपने अनुशंसित शिक्षण मॉड्यूल देखें" if hi else "Review your recommended learning modules",
                competency_id="COMP-SAMPLING",
                competency_label="सर्वेक्षण पद्धति" if hi else "Survey Methodology",
                target_url="/learning",
                button_label="शिक्षण पथ खोलें" if hi else "Open Learning Path",
                badge_label="अनुशंसित" if hi else "Recommended"
            )
            
        # Total gaps & completed count
        total_gaps = len(j["target_gaps"])
        completed_comp = sum(1 for c in j["current_competencies"] if c.get("current_level") and c["current_level"] >= 3)
        
        return LearnerDashboardResponse(
            greeting=greeting(u["name"], lang),
            learner_name=u["name"],
            current_role=j["current_position"]["name"] if j["current_position"] else "Current Role",
            target_role=tar_pos,
            next_action=next_action,
            priority_gaps=priority_gaps,
            learning_path_preview=path_items,
            readiness_status=j["readiness_status"],
            total_gaps_count=total_gaps,
            completed_competencies_count=completed_comp
        )
    finally:
        con.close()

@router.get("/gaps", response_model=List[CompetencyGapItem])
def get_learner_gaps(
    scope: str = Query("TARGET", pattern="^(TARGET|CURRENT)$", description="Scope of competency evaluation"),
    user_id: Optional[str] = Query(None, description="Optional user_id for Admin/Reviewer inspection"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    uid = resolve_target_user_id(current_user, user_id)
    con = get_db_connection()
    try:
        D = load_db(con)
        j = journey(D, uid)
        gaps = j["target_gaps"] if scope == "TARGET" else j["current_gaps"]
        tar_pos = j["target_position"]["name"] if j["target_position"] else "Target Role"
        
        return [build_gap_item(g, D, tar_pos) for g in gaps]
    finally:
        con.close()

@router.get("/learning-path", response_model=LearningPathDTO)
def get_learner_learning_path(
    user_id: Optional[str] = Query(None, description="Optional user_id for Admin/Reviewer inspection"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    uid = resolve_target_user_id(current_user, user_id)
    con = get_db_connection()
    try:
        D = load_db(con)
        j = journey(D, uid)
        path = j["learning_path"]
        if not path:
            raise HTTPException(status_code=404, detail="Learning path not yet computed for user")
            
        items = []
        for x in j["learning_path_items"]:
            comp = find(D, "competencies", "competency_id", x["competency_id"])
            course = find(D, "courses", "course_id", x["course_id"]) if x["course_id"] else None
            items.append(LearningPathItemDTO(
                path_item_id=x["path_item_id"],
                sequence_no=x["sequence_no"],
                stage=x["stage"],
                item_type=x["item_type"],
                competency_id=x["competency_id"],
                competency_label=comp["label"] if comp else x["competency_id"],
                course_id=x["course_id"],
                course_title=course["title"] if course else None,
                status=x["status"],
                action_label=x["action_label"]
            ))
            
        return LearningPathDTO(
            learning_path_id=path["learning_path_id"],
            user_id=uid,
            readiness_status=path["readiness_status"],
            status=path["status"],
            items=items
        )
    finally:
        con.close()

@router.get("/career-readiness", response_model=CareerReadinessResponse)
def get_career_readiness(
    user_id: Optional[str] = Query(None, description="Optional user_id for Admin/Reviewer inspection"),
    lang: str = "en",
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    uid = resolve_target_user_id(current_user, user_id)
    con = get_db_connection()
    try:
        D = load_db(con)
        j = journey(D, uid)
        u = j["user"]
        tar_pos = j["target_position"]["name"] if j["target_position"] else "Target Role"
        
        lang = normalize_lang(lang)
        readiness_labels = {k: i18n_readiness_label(k, lang) for k in
                            ("READY", "NEAR_READY", "DEVELOPMENT_REQUIRED", "CRITICAL_GAPS", "INSUFFICIENT_EVIDENCE")}
        
        target_gaps = [build_gap_item(g, D, tar_pos) for g in j["target_gaps"]]
        met_count = sum(1 for g in target_gaps if g.gap_status == "NO_GAP")
        high_gaps = sum(1 for g in target_gaps if g.gap_status == "HIGH")
        
        return CareerReadinessResponse(
            user_id=uid,
            learner_name=u["name"],
            current_position=j["current_position"]["name"] if j["current_position"] else "Current Role",
            target_position=tar_pos,
            readiness_status=j["readiness_status"],
            plain_readiness_label=readiness_labels.get(j["readiness_status"], "Under Evaluation"),
            notice=notice("readiness", lang),
            total_required_competencies=len(target_gaps),
            met_competencies_count=met_count,
            high_priority_gaps_count=high_gaps,
            target_gaps=target_gaps
        )
    finally:
        con.close()
