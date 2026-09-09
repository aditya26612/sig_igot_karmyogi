import json
import logging
from typing import List, Dict, Any, Optional
from app.config import settings
from app.database import get_db_connection
from app.services.transcript_service import search_transcripts_keywords

logger = logging.getLogger(__name__)

class GroqService:
    def __init__(self):
        self.key_index = 0
        
    def _get_next_client(self):
        keys = settings.groq_keys
        if not keys:
            return None, None
        key = keys[self.key_index % len(keys)]
        self.key_index += 1
        try:
            from groq import Groq
            return Groq(api_key=key), key
        except Exception as e:
            logger.warning(f"Failed to initialize Groq client: {e}")
            return None, None

    def ask_grounded_assistant(
        self,
        question: str,
        lesson_id: Optional[str] = None,
        competency_id: Optional[str] = None,
        lang: str = "en"
    ) -> Dict[str, Any]:
        """
        Answers learner queries grounded in lesson transcripts and official competencies.
        Cites lesson titles, timestamps, and quotes. Responds in EN or HI when requested.
        """
        con = get_db_connection()
        relevant_chunks = []
        try:
            if lesson_id:
                cur = con.execute("""
                SELECT c.*, l.title as lesson_title, p.title as playlist_title
                FROM transcript_chunks c
                JOIN curated_lessons l ON c.lesson_id = l.lesson_id
                JOIN curated_playlists p ON l.playlist_id = p.playlist_id
                WHERE c.lesson_id = ?
                ORDER BY c.start_seconds ASC
                """, (lesson_id,))
                relevant_chunks = [dict(r) for r in cur.fetchall()]
            elif competency_id:
                cur = con.execute("""
                SELECT c.*, l.title as lesson_title, p.title as playlist_title
                FROM transcript_chunks c
                JOIN curated_lessons l ON c.lesson_id = l.lesson_id
                JOIN curated_playlists p ON l.playlist_id = p.playlist_id
                WHERE c.competency_id = ?
                LIMIT 5
                """, (competency_id,))
                relevant_chunks = [dict(r) for r in cur.fetchall()]
            else:
                # Honest fallback: keyword search over all transcripts (tokenized, OR-matched)
                relevant_chunks = search_transcripts_keywords(con, question)
        finally:
            con.close()
            
        # If we have relevant chunks, build context
        context_text = ""
        best_chunk = relevant_chunks[0] if relevant_chunks else None
        
        for chk in relevant_chunks[:4]:
            context_text += f"\n[Lesson: {chk.get('lesson_title', 'Lesson')} | Timestamp: {chk.get('timestamp_label', '00:00')} | Topic: {chk.get('topic', '')}]\n{chk.get('text_content', '')}\n"
            
        # Check if Groq client can be initialized
        client, key_used = self._get_next_client()
        
        if client and context_text:
            try:
                system_prompt = """
You are the AI Learning Copilot for India's Official Statistical System (MoSPI) and iGOT Karmayogi.
Your purpose is to help government statistical officers master survey methodology, data analysis, and official statistics.

CRITICAL RULES:
1. Ground your answer strictly in the provided transcript context.
2. Clearly cite the lesson title, timestamp (e.g. [02:15]), and topic in your response.
3. Keep answers clear, professional, and accessible (plain language first).
4. If the information is not present in the context, say: "I could not find this in the approved learning material for this module."
5. NEVER reveal quiz answer keys before submission.
6. NEVER promise or alter competency levels.
"""
                if lang == "hi":
                    system_prompt += """
7. Respond entirely in Hindi (Devanagari script), using standard Indian government statistical terminology.
   Keep technical identifiers, competency codes, and timestamps in their original form.
"""
                user_content = f"Context from approved curriculum:\n{context_text}\n\nLearner Question: {question}"

                completion = client.chat.completions.create(
                    model=settings.GROQ_PRIMARY_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content}
                    ],
                    temperature=0.3,
                    max_tokens=600
                )
                answer_text = completion.choices[0].message.content.strip()

                if best_chunk:
                    suggested = [
                        "Explain this with a village survey example",
                        "How do I calculate sampling weights?",
                        "Take practice quiz on this topic",
                        "What should I learn next?"
                    ] if lang != "hi" else [
                        "इसे ग्रामीण सर्वेक्षण उदाहरण से समझाइए",
                        "प्रतिदर्श भार की गणना कैसे करें?",
                        "इस विषय पर अभ्यास क्विज़ दें",
                        "मुझे आगे क्या सीखना चाहिए?"
                    ]
                    return {
                        "answer": answer_text,
                        "source_lesson_id": best_chunk.get("lesson_id"),
                        "source_lesson_title": best_chunk.get("lesson_title"),
                        "timestamp_label": best_chunk.get("timestamp_label"),
                        "chunk_id": best_chunk.get("chunk_id"),
                        "citation_snippet": best_chunk.get("text_content", "")[:120] + "...",
                        "suggested_actions": suggested
                    }
                # No grounding chunk found: do NOT fabricate a citation
                return {
                    "answer": answer_text,
                    "source_lesson_id": None,
                    "source_lesson_title": None,
                    "timestamp_label": None,
                    "chunk_id": None,
                    "citation_snippet": None,
                    "suggested_actions": []
                }
            except Exception as e:
                logger.warning(f"Groq API call failed: {e}. Falling back to deterministic grounded response.")

        # Deterministic Grounded Fallback (Ensures the platform operates with 100% reliability offline)
        if best_chunk:
            ts = best_chunk.get("timestamp_label")
            citation = f" at [{ts}]" if ts else ""
            fallback_answer = (
                f"Based on the approved training material for '{best_chunk.get('lesson_title', 'Curated Module')}'"
                f"{citation}:\n\n"
                f"{best_chunk.get('text_content', '')}\n\n"
                f"Key Takeaway: {best_chunk.get('summary', 'Reinforce this concept with the practice quiz.')}"
            )
            if lang == "hi":
                fallback_answer = (
                    f"अनुमोदित प्रशिक्षण सामग्री '{best_chunk.get('lesson_title', 'Curated Module')}'"
                    f"{citation} के आधार पर:\n\n"
                    f"{best_chunk.get('text_content', '')}\n\n"
                    f"मुख्य बात: {best_chunk.get('summary', 'इस अवधारणा को अभ्यास क्विज़ से सुदृढ़ करें।')}"
                )
            return {
                "answer": fallback_answer,
                "source_lesson_id": best_chunk.get("lesson_id"),
                "source_lesson_title": best_chunk.get("lesson_title"),
                "timestamp_label": ts,
                "chunk_id": best_chunk.get("chunk_id"),
                "citation_snippet": best_chunk.get("text_content", "")[:120] + "..." if best_chunk.get("text_content") else None,
                "suggested_actions": [
                    "Explain this simply",
                    "Show relevant transcript section",
                    "Take practice quiz",
                    "Review next role requirements"
                ] if lang != "hi" else [
                    "इसे सरल भाषा में समझाइए",
                    "संबंधित ट्रांसक्रिप्ट अंश दिखाएँ",
                    "अभ्यास क्विज़ दें",
                    "अगली भूमिका आवश्यकताएँ देखें"
                ]
            }
        else:
            no_match_en = "I could not find this in the approved learning material for this module. Please consult the curated playlist lessons or ask your supervisor."
            no_match_hi = "यह सूचना इस मॉड्यूल की अनुमोदित शिक्षण सामग्री में नहीं मिली। कृपया अनुशंसित पाठ्यक्रम देखें या अपने पर्यवेक्षक से परामर्श करें।"
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
                    "Return to home dashboard"
                ]
            }



    # ------------------------------------------------------------------
    # AI Quiz Generation (Groq-powered, question bank as guaranteed fallback)
    # ------------------------------------------------------------------

    def generate_quiz_questions(
        self,
        lesson: Dict[str, Any],
        transcript_chunks: List[Dict[str, Any]],
        num_questions: int = 5,
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Asks Groq to generate formative practice questions grounded in the
        lesson transcript. Returns a validated list of question dicts, or
        None if the API fails / output fails validation (caller falls back
        to the curated question bank).
        """
        client, _ = self._get_next_client()
        if not client:
            return None

        context_text = ""
        for chk in transcript_chunks[:4]:
            context_text += (
                "\n[" + str(chk.get('topic', 'Topic')) + " | " + str(chk.get('timestamp_label', '00:00')) + "] "
                + str(chk.get('text_content', '')) + "\n"
            )
        if not context_text.strip():
            return None

        prompt = (
            "Create a practice quiz for government statistical officers.\n"
            "Lesson: " + str(lesson['title']) + "\n"
            "Competency: " + str(lesson['competency_id']) + "\n"
            "Approved transcript context:\n" + context_text + "\n"
            "Generate exactly " + str(num_questions) + " multiple-choice questions grounded ONLY in the transcript. "
            "Return STRICT JSON only (no markdown, no commentary): a JSON array where each item has keys: "
            '"question_text" (string), "options" (array of exactly 4 objects with keys "text" (string)), '
            '"correct_index" (integer 0-3 pointing to the correct option), '
            '"explanation" (string citing why, referencing the transcript), '
            '"difficulty" (one of EASY/MEDIUM/HARD), '
            '"timestamp_label" (string MM:SS from the transcript context).'
        )

        try:
            completion = client.chat.completions.create(
                model=settings.GROQ_PRIMARY_MODEL,
                messages=[
                    {"role": "system", "content": (
                        "You are an assessment designer for India's Official Statistical System (MoSPI). "
                        "You output ONLY valid JSON. Questions must be answerable from the given transcript "
                        "alone, in plain professional language, with one unambiguously correct option."
                    )},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
                max_tokens=1600,
            )
            raw = (completion.choices[0].message.content or "").strip()
            # Strip any accidental markdown fencing
            if raw.startswith("```"):
                raw = raw.strip("`")
                if raw.lower().startswith("json"):
                    raw = raw[4:]
            # Extract the JSON array even if the model added stray text
            start, end = raw.find("["), raw.rfind("]")
            if start == -1 or end == -1:
                logger.warning("Groq quiz generation: no JSON array found in response")
                return None
            items = json.loads(raw[start:end + 1])
        except Exception as e:
            logger.warning(f"Groq quiz generation failed: {e}. Falling back to question bank.")
            return None

        # ---- Validation: never trust LLM output blindly ----
        validated: List[Dict[str, Any]] = []
        option_ids = ["A", "B", "C", "D"]
        for i, item in enumerate(items[:num_questions], 1):
            try:
                q_text = str(item["question_text"]).strip()
                opts_raw = item["options"]
                correct_idx = int(item["correct_index"])
                explanation = str(item["explanation"]).strip()
                difficulty = str(item.get("difficulty", "MEDIUM")).upper()
                ts_label = str(item.get("timestamp_label", "02:15")).strip() or "02:15"

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

                validated.append({
                    "question_id": f"Q-{lesson['lesson_id'].upper()}-AI-{i:02d}",
                    "question_text": q_text,
                    "options_json": json.dumps(
                        [{"option_id": option_ids[j], "text": texts[j]} for j in range(4)]
                    ),
                    "correct_option": option_ids[correct_idx],
                    "explanation": explanation,
                    "difficulty": difficulty,
                    "timestamp_label": ts_label,
                    "chunk_id": transcript_chunks[0]["chunk_id"] if transcript_chunks else None,
                })
            except (KeyError, ValueError, TypeError):
                continue

        if len(validated) < 3:
            logger.warning(f"Groq quiz generation: only {len(validated)} valid questions, discarding batch.")
            return None
        return validated


groq_service = GroqService()
