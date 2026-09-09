from typing import Optional, List, Dict, Any
import time
from pydantic import BaseModel
from fastapi import APIRouter, Depends
from app.config import settings
from app.auth import get_current_user
from app.services.groq_service import groq_service

router = APIRouter(prefix="/api/assistant", tags=["Learning Assistant (AI Copilot)"])

class AssistantAskRequest(BaseModel):
    question: str
    context_type: str = "LESSON" # 'LESSON', 'GAP', 'GENERAL'
    lesson_id: Optional[str] = None
    competency_id: Optional[str] = None
    lang: str = "en"  # 'en' | 'hi' — response language for the copilot

class AssistantAskResponse(BaseModel):
    answer: str
    source_lesson_id: Optional[str] = None
    source_lesson_title: Optional[str] = None
    timestamp_label: Optional[str] = None
    chunk_id: Optional[str] = None
    citation_snippet: Optional[str] = None
    suggested_actions: List[str]

class QuickPromptItem(BaseModel):
    label: str
    prompt: str
    category: str

@router.get("/prompts", response_model=List[QuickPromptItem])
def get_quick_prompts():
    """Returns contextual quick-action prompts for learners."""
    return [
        QuickPromptItem(
            label="Explain Simply",
            prompt="Can you explain the main concept of this lesson in plain language for a junior officer?",
            category="CONCEPT"
        ),
        QuickPromptItem(
            label="Practical Example",
            prompt="Can you provide a realistic field survey or census scenario illustrating this concept?",
            category="PRACTICAL"
        ),
        QuickPromptItem(
            label="Show Citation",
            prompt="Where in the lesson transcript is this topic discussed? Show the exact quote and timestamp.",
            category="CITATION"
        ),
        QuickPromptItem(
            label="Practice Questions",
            prompt="What key question should I be able to answer after studying this material?",
            category="PRACTICE"
        ),
        QuickPromptItem(
            label="Career Relevance",
            prompt="Why is this specific competency essential for my target position responsibilities?",
            category="CAREER"
        )
    ]

@router.post("/ask", response_model=AssistantAskResponse)
def ask_assistant(
    request: AssistantAskRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Submits a query to the AI learning copilot.
    Grounded in curriculum transcripts with mandatory timestamp citations.
    A short presentation delay keeps the response feeling like live synthesis.
    """
    t0 = time.perf_counter()
    result = groq_service.ask_grounded_assistant(
        question=request.question,
        lesson_id=request.lesson_id,
        competency_id=request.competency_id,
        lang=getattr(request, "lang", "en")
    )
    # Guarantee a MINIMUM total response time (not additive): sleep only the remainder
    remaining = settings.AI_PRESENTATION_DELAY_SECONDS - (time.perf_counter() - t0)
    if remaining > 0:
        time.sleep(remaining)
    return AssistantAskResponse(**result)
