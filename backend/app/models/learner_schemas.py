from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class OfficialCompetencyItem(BaseModel):
    competency_id: str
    label: str
    current_level: Optional[int] = None
    level_label: str  # e.g. "Level 3" or "Not Assessed"
    required_level: Optional[int] = None  # level required by the target position
    gap_status: Optional[str] = None

class LearnerProfileDetail(BaseModel):
    user_id: str
    name: str
    email: str
    designation: str
    department: Optional[str] = None
    division: Optional[str] = None
    mdo: Optional[str] = None
    current_position_id: str
    current_position_name: str
    target_position_id: str
    target_position_name: str
    experience_years: int
    status: str
    official_competencies: List[OfficialCompetencyItem] = []
    recent_promotions: List[OfficialCompetencyItem] = []  # approved evidence upgrades visible on the profile

class NextActionItem(BaseModel):
    action_type: str # 'CONTINUE_LESSON', 'TAKE_PRACTICE', 'START_ASSESSMENT', 'WAIT_REVIEW'
    title: str
    subtitle: str
    competency_id: str
    competency_label: str
    target_url: str
    button_label: str
    badge_label: str

class CompetencyGapItem(BaseModel):
    gap_id: str
    competency_id: str
    competency_label: str
    plain_title: str # e.g. "Survey Sampling & Design"
    plain_explanation: str # Why this matters in plain terms
    current_level: Optional[int]
    required_level: int
    unmet_gap: Optional[int]
    gap_status: str # 'HIGH', 'MEDIUM', 'NO_GAP', 'INSUFFICIENT_EVIDENCE'
    priority: str
    target_role_name: str
    contributing_activities: List[str]
    recommendation_status: str
    has_recommended_course: bool

class LearningPathItemDTO(BaseModel):
    path_item_id: str
    sequence_no: int
    stage: str # 'DIAGNOSTIC', 'FOUNDATION', 'INTERMEDIATE', 'ADVANCED', 'PRACTICAL', 'ASSESSMENT'
    item_type: str
    competency_id: str
    competency_label: str
    course_id: Optional[str]
    course_title: Optional[str]
    status: str # 'AVAILABLE', 'IN_PROGRESS', 'REQUIRED', 'BLOCKED', 'PLANNED_NOT_PUBLISHED'
    action_label: str

class LearningPathDTO(BaseModel):
    learning_path_id: str
    user_id: str
    readiness_status: str
    status: str
    items: List[LearningPathItemDTO]

class LearnerDashboardResponse(BaseModel):
    greeting: str
    learner_name: str
    current_role: str
    target_role: str
    next_action: NextActionItem
    priority_gaps: List[CompetencyGapItem]
    learning_path_preview: List[LearningPathItemDTO]
    readiness_status: str
    total_gaps_count: int
    completed_competencies_count: int

class CareerReadinessResponse(BaseModel):
    user_id: str
    learner_name: str
    current_position: str
    target_position: str
    readiness_status: str
    plain_readiness_label: str # "Learning Readiness: Needs Development" (not promotion eligibility)
    notice: str
    total_required_competencies: int
    met_competencies_count: int
    high_priority_gaps_count: int
    target_gaps: List[CompetencyGapItem]
