from typing import Optional, List, Dict, Any
import time
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Query
from app.config import settings
from app.auth import get_current_user
from app.database import get_db_connection
from app.services.i18n_service import normalize_lang
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
def get_quick_prompts(
    lesson_id: Optional[str] = Query(None, description="When set, prompts reference this specific lesson"),
    lang: str = Query("en", description="Prompt language ('en' | 'hi')")
):
    """Returns contextual quick-action prompts; tailored to the pinned lesson when given."""
    hi = normalize_lang(lang) == "hi"

    def prompt(label_en: str, label_hi: str, prompt_en: str, prompt_hi: str, category: str) -> QuickPromptItem:
        return QuickPromptItem(
            label=label_hi if hi else label_en,
            prompt=prompt_hi if hi else prompt_en,
            category=category
        )

    if lesson_id:
        con = get_db_connection()
        try:
            row = con.execute(
                "SELECT title FROM curated_lessons WHERE lesson_id = ?", (lesson_id,)
            ).fetchone()
        finally:
            con.close()
        lesson_title = row["title"] if row else None
        if lesson_title:
            return [
                prompt(
                    "Explain Simply", "सरल व्याख्या",
                    f"Explain the main idea of '{lesson_title}' in simple words.", f"'{lesson_title}' का मुख्य विचार सरल शब्दों में समझाइए।",
                    "CONCEPT"
                ),
                prompt(
                    "Field Example", "क्षेत्रीय उदाहरण",
                    f"Give a realistic field-survey example from '{lesson_title}'.", f"'{lesson_title}' से एक वास्तविक क्षेत्रीय सर्वेक्षण उदाहरण दें।",
                    "PRACTICAL"
                ),
                prompt(
                    "Key Takeaways", "मुख्य बातें",
                    f"What are the 3 most important points in '{lesson_title}'?", f"'{lesson_title}' के तीन सबसे महत्वपूर्ण बिंदु क्या हैं?",
                    "SUMMARY"
                ),
                prompt(
                    "Practice Quiz", "अभ्यास क्विज़",
                    f"Quiz me on '{lesson_title}'.", f"'{lesson_title}' पर मेरा अभ्यास क्विज़ करें।",
                    "PRACTICE"
                )
            ]

    # No lesson pinned: generic but concrete starter prompts
    return [
        prompt(
            "Explain Simply", "सरल व्याख्या",
            "Explain stratified sampling in simple words.", "स्तरित प्रतिदर्शन को सरल शब्दों में समझाइए।",
            "CONCEPT"
        ),
        prompt(
            "Field Example", "क्षेत्रीय उदाहरण",
            "Give a village-survey example of cluster sampling.", "गुच्छा प्रतिदर्शन का एक ग्रामीण सर्वेक्षण उदाहरण दें।",
            "PRACTICAL"
        ),
        prompt(
            "Sampling vs Cluster", "स्तर vs गुच्छा",
            "What is the difference between a stratum and a cluster?", "स्तर (stratum) और गुच्छा (cluster) में क्या अंतर है?",
            "COMPARISON"
        ),
        prompt(
            "Practice Quiz", "अभ्यास क्विज़",
            "Quiz me on survey sampling.", "सर्वेक्षण प्रतिदर्शन पर मेरा अभ्यास क्विज़ करें।",
            "PRACTICE"
        )
    ]

@router.post("/ask", response_model=AssistantAskResponse)
def ask_assistant(
    request: AssistantAskRequest,
    lang: str = Query("en", description="Response language ('en' | 'hi'); overrides the body field"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Submits a query to the AI learning copilot.
    Grounded in curriculum transcripts with mandatory timestamp citations.
    A short presentation delay keeps the response feeling like live synthesis.
    """
    effective_lang = normalize_lang(lang if lang != "en" else getattr(request, "lang", "en"))
    t0 = time.perf_counter()
    result = groq_service.ask_grounded_assistant(
        question=request.question,
        lesson_id=request.lesson_id,
        competency_id=request.competency_id,
        lang=effective_lang
    )
    # Guarantee a MINIMUM total response time (not additive): sleep only the remainder
    remaining = settings.AI_PRESENTATION_DELAY_SECONDS - (time.perf_counter() - t0)
    if remaining > 0:
        time.sleep(remaining)
    return AssistantAskResponse(**result)
