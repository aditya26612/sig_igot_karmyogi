from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class PracticeOption(BaseModel):
    option_id: str # 'A', 'B', 'C', 'D'
    text: str

class PracticeQuestionDTO(BaseModel):
    question_id: str
    question_text: str
    options: List[PracticeOption]
    difficulty: str
    topic: str
    timestamp_label: Optional[str] = None
    chunk_id: Optional[str] = None

class PracticeQuizDTO(BaseModel):
    quiz_id: str
    lesson_id: str
    title: str
    topic: str
    total_questions: int
    questions: List[PracticeQuestionDTO]
    notice: str = "This practice quiz reinforces key concepts. Results do NOT change your official competency level."

class PracticeAnswerItem(BaseModel):
    question_id: str
    selected_option: str # 'A', 'B', 'C', or 'D'

class PracticeSubmissionRequest(BaseModel):
    answers: List[PracticeAnswerItem]

class QuestionResultItem(BaseModel):
    question_id: str
    question_text: str
    selected_option: str
    correct_option: str
    is_correct: bool
    explanation: str
    timestamp_label: Optional[str] = None
    chunk_id: Optional[str] = None

class PracticeSubmissionResponse(BaseModel):
    attempt_id: str
    quiz_id: str
    lesson_id: str
    score: int
    total_questions: int
    percentage: float
    weak_topics: List[str]
    results: List[QuestionResultItem]
    notice: str = "This practice result helps personalize your learning. It does NOT change your official proficiency level."
    competency_level_changed: bool = False # Always False - Core Invariant

class PracticeAttemptHistoryItem(BaseModel):
    attempt_id: str
    quiz_id: str
    lesson_id: str
    score: int
    total_questions: int
    percentage: float
    weak_topics: List[str]
    attempted_at: str
