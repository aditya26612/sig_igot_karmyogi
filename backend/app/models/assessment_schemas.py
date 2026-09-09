from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class PracticalTaskItem(BaseModel):
    task_id: str
    title: str
    scenario: str
    instructions: str
    expected_output_type: str

class AssessmentDetailDTO(BaseModel):
    assessment_id: str
    title: str
    competency_id: str
    competency_label: str
    assessment_type: str # 'PRACTICAL'
    rubric_version: str
    estimated_time_minutes: int
    prerequisites_met: bool
    current_level: int
    target_level: int
    rules: List[str]
    tasks: List[PracticalTaskItem]
    notice: str = "This formal assessment generates official evidence. Requires supervisor evaluation before proficiency level updates."

class AssessmentSubmissionRequest(BaseModel):
    assessment_id: str
    competency_id: str
    practical_answers: Dict[str, Any]
    self_reported_score: Optional[float] = 86.0

class AssessmentSubmissionResponse(BaseModel):
    submission_id: str
    assessment_id: str
    user_id: str
    status: str # 'PENDING_REVIEW'
    submitted_at: str
    notice: str = "Your assessment has been submitted successfully. A supervisor must verify the evidence against the rubric before your proficiency level changes."

class ReviewQueueItemDTO(BaseModel):
    submission_id: str
    user_id: str
    learner_name: str
    assessment_id: str
    assessment_title: str
    competency_id: str
    competency_label: str
    current_level: int
    proposed_level: int
    overall_score: float
    confidence: float
    coverage: float
    rubric_version: str
    submitted_at: str
    status: str

class ReviewDecisionRequest(BaseModel):
    approved: bool
    reviewer_comments: str
    adjusted_score: Optional[float] = None

class ReviewDecisionResponse(BaseModel):
    submission_id: str
    status: str # 'APPROVED' or 'REJECTED'
    level_promoted: bool
    before_level: Optional[int]
    after_level: Optional[int]
    learning_path_recalculated: bool
    message: str
