# backend/app/services/groq_service.py
import json
import logging
import sqlite3
from typing import Any, Dict, List, Optional

from app.config import settings
from app.database import get_db_connection
from app.services import embedding_service as _embedding_probe
from app.services import llm_router, retrieval_service

logger = logging.getLogger(__name__)

_GROUNDING_COSINE_THRESHOLD = 0.45


def _llm_generate(system: str, user: str, max_tokens: int, **kw) -> Optional[str]:
    return llm_router.generate(system, user, max_tokens, **kw)


class GroqService:

    # ---------------- Assistant (copilot) ----------------
    def ask_grounded_assistant(
        self,
        question: str,
        lesson_id: Optional[str] = None,
        competency_id: Optional[str] = None,
        lang: str = "en",
        con: sqlite3.Connection = None,
    ) -> Dict[str, Any]:
        should_close = con is None
        if should_close:
            con = get_db_connection()
        try:
            relevant_chunks = retrieval_service.retrieve(
                question, lesson_id=lesson_id, competency_id=competency_id,
                top_k=4, con=con,
            )
        finally:
            if should_close:
                con.close()

        best_chunk = relevant_chunks[0] if relevant_chunks else None
        context_text = ""
        for chk in relevant_chunks[:4]:
            context_text += (
                f"\n[CHUNK {chk.get('chunk_id')} | Lesson: {chk.get('lesson_title', 'Lesson')} | "
                f"Timestamp: {chk.get('timestamp_label', '00:00')} | Topic: {chk.get('topic', '')}]\n"
                f"{chk.get('text_content', '')}\n"
            )

        system_prompt = (
            "You are the AI Learning Copilot for India's Official Statistical System (MoSPI) "
            "and iGOT Karmayogi. Your purpose is to help government statistical officers master "
            "survey methodology, data analysis, and official statistics.\n\n"
            "ANSWER STYLE: be concise (120-180 words), lead with the direct answer, short "
            "paragraphs or 3-5 bullets, plain language with one concrete field example.\n"
            "GROUNDING: answer strictly from the provided transcript context; cite inline "
            "exactly once as [MM:SS] at the sentence it supports; never reveal quiz answer "
            "keys; if the context genuinely has nothing related, say you could not find this "
            "in the approved learning material for this module."
        )
        if lang == "hi":
            system_prompt += (
                "\nRespond entirely in Hindi (Devanagari script), using standard Indian "
                "government statistical terminology. Keep timestamps in original form."
            )
        user_content = (
            f"Context from approved curriculum:\n{context_text}\n\nLearner Question: {question}"
        )

        answer_text = None
        if context_text.strip():
            answer_text = _llm_generate(
                system_prompt, user_content, max_tokens=450, temperature=0.3,
                timeout=settings.GROQ_ASSISTANT_TIMEOUT_S,
            )

        if answer_text:
            if best_chunk:
                return {
                    "answer": answer_text,
                    "source_lesson_id": best_chunk.get("lesson_id"),
                    "source_lesson_title": best_chunk.get("lesson_title"),
                    "timestamp_label": best_chunk.get("timestamp_label"),
                    "chunk_id": best_chunk.get("chunk_id"),
                    "citation_snippet": (best_chunk.get("text_content") or "")[:120] + "...",
                    "suggested_actions": self._contextual_follow_ups(
                        question, relevant_chunks, lang),
                }
            return {
                "answer": answer_text,
                "source_lesson_id": None,
                "source_lesson_title": None,
                "timestamp_label": None,
                "chunk_id": None,
                "citation_snippet": None,
                "suggested_actions": [],
            }

        # Deterministic grounded fallback (100% offline reliability)
        if best_chunk:
            ts = best_chunk.get("timestamp_label")
            citation = f" at [{ts}]" if ts else ""
            if lang == "hi":
                fallback_answer = (
                    f"अनुमोदित प्रशिक्षण सामग्री '{best_chunk.get('lesson_title', 'Curated Module')}'"
                    f"{citation} के आधार पर:\n\n{best_chunk.get('text_content', '')}\n\n"
                    f"मुख्य बात: {best_chunk.get('summary', 'इस अवधारणा को अभ्यास क्विज़ से सुदृढ़ करें।')}"
                )
            else:
                fallback_answer = (
                    f"Based on the approved training material for "
                    f"'{best_chunk.get('lesson_title', 'Curated Module')}'{citation}:\n\n"
                    f"{best_chunk.get('text_content', '')}\n\n"
                    f"Key Takeaway: {best_chunk.get('summary', 'Reinforce this concept with the practice quiz.')}"
                )
            return {
                "answer": fallback_answer,
                "source_lesson_id": best_chunk.get("lesson_id"),
                "source_lesson_title": best_chunk.get("lesson_title"),
                "timestamp_label": ts,
                "chunk_id": best_chunk.get("chunk_id"),
                "citation_snippet": (best_chunk.get("text_content") or "")[:120] + "..."
                if best_chunk.get("text_content") else None,
                "suggested_actions": self._contextual_follow_ups(
                    question, relevant_chunks, lang),
            }

        no_match_en = ("I could not find this in the approved learning material for this "
                       "module. Please consult the curated playlist lessons or ask your "
                       "supervisor.")
        no_match_hi = ("यह सूचना इस मॉड्यूल की अनुमोदित शिक्षण सामग्री में नहीं मिली। "
                       "कृपया अनुशंसित पाठ्यक्रम देखें या अपने पर्यवेक्षक से परामर्श करें।")
        return {
            "answer": no_match_hi if lang == "hi" else no_match_en,
            "source_lesson_id": None,
            "source_lesson_title": None,
            "timestamp_label": None,
            "chunk_id": None,
            "citation_snippet": None,
            "suggested_actions": [
                "View all available courses",
                "Check my skill gaps",
                "Return to home dashboard",
            ],
        }

    def _contextual_follow_ups(
        self,
        question: str,
        chunks: List[Dict[str, Any]],
        lang: str
    ) -> List[str]:
        """
        Builds follow-up suggestions tied to what was actually discussed:
        - Reference the topic keyword of a *different* chunk in the same lesson.
        - Offer the quiz on the lesson the answer came from.
        - Offer a plain-language re-explanation of the current topic.
        Falls back to generic (but lesson-anchored) prompts when no metadata exists.
        """
        hi = lang == "hi"
        follow_ups: List[str] = []
        topics = [str(c.get("topic", "")).strip() for c in chunks if c.get("topic")]
        lesson_title = str(chunks[0].get("lesson_title", "")).strip() if chunks else ""
        primary_topic = topics[0] if topics else ""
        other_topics = [t for t in topics[1:] if t and t.lower() != primary_topic.lower()][:1]

        # 1. A concrete next topic from the same lesson the answer came from
        if other_topics:
            follow_ups.append(
                f"अगला: {other_topics[0]} क्या है?" if hi else f"What is {other_topics[0]}?"
            )
        elif lesson_title:
            follow_ups.append(
                f"'{lesson_title}' का सारांश दें" if hi else f"Summarize '{lesson_title}'"
            )

        # 2. Deepen the concept that was just answered
        if primary_topic:
            follow_ups.append(
                f"{primary_topic} का एक क्षेत्रीय उदाहरण दें" if hi else f"Give a field example of {primary_topic}"
            )
        else:
            follow_ups.append("Explain this in simpler words" if not hi else "इसे और सरल भाषा में बताएँ")

        # 3. Practice — anchored to the same lesson
        if lesson_title:
            follow_ups.append(
                f"'{lesson_title}' का अभ्यास क्विज़ दें" if hi else f"Quiz me on '{lesson_title}'"
            )

        return follow_ups[:3]



    # ------------------------------------------------------------------
    # AI Quiz Generation (Groq-powered, question bank as guaranteed fallback)
    # ------------------------------------------------------------------

    def generate_quiz_questions(
        self,
        lesson: Dict[str, Any],
        transcript_chunks: List[Dict[str, Any]],
        num_questions: int = 5,
    ) -> Optional[List[Dict[str, Any]]]:
        context_text = ""
        for chk in transcript_chunks[:4]:
            context_text += (
                "\n[CHUNK " + str(chk.get("chunk_id", "CHUNK")) + " | " +
                str(chk.get("topic", "Topic")) + " | " +
                str(chk.get("timestamp_label", "00:00")) + "] " +
                str(chk.get("text_content", "")) + "\n"
            )
        if not context_text.strip():
            return None

        prompt = (
            "Create a practice quiz for government statistical officers.\n"
            "Lesson: " + str(lesson["title"]) + "\n"
            "Competency: " + str(lesson["competency_id"]) + "\n"
            "Approved transcript context:\n" + context_text + "\n"
            "Generate exactly " + str(num_questions) + " multiple-choice questions grounded "
            "ONLY in the transcript. Return STRICT JSON only, no markdown: "
            '{"questions": [{"question_text": str, "options": [exactly 4 objects with key '
            '"text"], "correct_index": int 0-3, "explanation": str citing the transcript, '
            '"difficulty": "EASY"|"MEDIUM"|"HARD", "timestamp_label": "MM:SS from context", '
            '"chunk_id": "the CHUNK id this question is drawn from"}]}'
        )

        # max_tokens=2400 (not the brief's 1100): with json_mode the provider validates
        # the streamed JSON; at 1100 the completion is cut before a valid document
        # closes and Groq rejects with json_validate_failed ~75% of live runs
        # (empirically probed: 1100 -> 0-2 questions, 2400 -> 5/5 questions).
        raw = _llm_generate(
            "You are an assessment designer for India's Official Statistical System (MoSPI). "
            "You output ONLY valid JSON. Questions must be answerable from the given transcript "
            "alone, in plain professional language, with one unambiguously correct option.",
            prompt,
            max_tokens=2400,
            temperature=0.4,
            json_mode=True,
            timeout=settings.GROQ_QUIZ_TIMEOUT_S,
        )
        payload = llm_router.parse_json_payload(raw) if raw else None
        if not payload or not isinstance(payload.get("questions"), list):
            logger.warning("Quiz generation: no valid JSON payload")
            return None
        items = payload["questions"]

        option_ids = ["A", "B", "C", "D"]
        chunk_texts = {
            str(c.get("chunk_id")): str(c.get("text_content", ""))
            for c in transcript_chunks if c.get("chunk_id")
        }
        chunk_ids_present = list(chunk_texts.keys())
        grounding_rejects = 0

        # Pre-embed cited chunk texts once when embeddings are available
        emb_chunks = None
        if chunk_ids_present:
            try:
                emb_chunks = _embedding_probe.embed_texts(
                    [chunk_texts[cid] for cid in chunk_ids_present])
            except Exception:
                emb_chunks = None

        validated: List[Dict[str, Any]] = []
        for i, item in enumerate(items[:num_questions], 1):
            try:
                q_text = str(item["question_text"]).strip()
                opts_raw = item["options"]
                correct_idx = int(item["correct_index"])
                explanation = str(item["explanation"]).strip()
                difficulty = str(item.get("difficulty", "MEDIUM")).upper()
                ts_label = str(item.get("timestamp_label", "")).strip() or "02:15"
                cited_chunk = str(item.get("chunk_id", "")).strip()

                if not q_text or len(q_text) < 15:
                    continue
                if not isinstance(opts_raw, list) or len(opts_raw) != 4:
                    continue
                texts = [str(o["text"]).strip() for o in opts_raw]
                if any(not t or len(t) < 3 for t in texts) or len(set(texts)) != 4:
                    continue
                if not (0 <= correct_idx <= 3):
                    continue
                if not explanation:
                    continue
                if difficulty not in ("EASY", "MEDIUM", "HARD"):
                    difficulty = "MEDIUM"

                # Semantic grounding (spec section 8): question+explanation must be
                # cosine >= 0.45 with the cited chunk, when embeddings are available.
                if emb_chunks is not None:
                    if cited_chunk not in chunk_texts:
                        grounding_rejects += 1
                        continue
                    idx = chunk_ids_present.index(cited_chunk)
                    qvec = _embedding_probe.embed_texts([q_text + " " + explanation])
                    if qvec is not None:
                        score = float(_embedding_probe.cosine_sim(
                            emb_chunks[idx:idx + 1], qvec[0])[0])
                        if score < _GROUNDING_COSINE_THRESHOLD:
                            grounding_rejects += 1
                            logger.info(
                                f"GROUNDING_REJECT q{i} score={score:.3f}")
                            continue

                validated.append({
                    "question_id": f"Q-{lesson['lesson_id'].upper()}-AI-{i:02d}",
                    "question_text": q_text,
                    "options_json": json.dumps(
                        [{"option_id": option_ids[j], "text": texts[j]}
                         for j in range(4)]),
                    "correct_option": option_ids[correct_idx],
                    "explanation": explanation,
                    "difficulty": difficulty,
                    "timestamp_label": ts_label,
                    "chunk_id": cited_chunk or None,
                })
            except (KeyError, ValueError, TypeError):
                continue

        if len(validated) < 3:
            logger.warning(
                f"Quiz generation: {len(validated)} valid "
                f"({grounding_rejects} grounding rejects); discarding batch.")
            return None
        return validated


groq_service = GroqService()

# Module-level aliases bound to the singleton: lets tests (and any future
# callers) invoke the public API directly off the module. The routers keep
# using the `groq_service` singleton; both forms share one instance.
ask_grounded_assistant = groq_service.ask_grounded_assistant
generate_quiz_questions = groq_service.generate_quiz_questions
