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
                system_prompt = """You are the AI Learning Copilot for India's Official Statistical System (MoSPI) and iGOT Karmayogi.
Your purpose is to help government statistical officers master survey methodology, data analysis, and official statistics.

ANSWER STYLE — you are a friendly senior trainer, not a documentation dump:
1. Be CONCISE: 120-180 words maximum. Lead with the direct answer in the first sentence; details after.
2. FORMAT simply: short paragraphs, 3-5 bullet points max, or a 2-4 step numbered list. NO markdown tables.
   NO horizontal rules, NO title headings, NO emoji. Bold sparingly for one or two key terms only.
3. PLAIN LANGUAGE first: explain in simple words, then give the technical term. Use one concrete field
   example (a district survey, a census round) when it clarifies — keep it inside the word budget.
4. END with a single short follow-up line inviting the learner to go deeper (one sentence, no list).

GROUNDING RULES:
5. Ground your answer strictly in the provided transcript context.
6. Cite inline exactly once, in the form [MM:SS] of the lesson, at the sentence it supports. Do not attach
   a separate citation section or a "Source:" block.
7. The learner may use broader or narrower terms than the transcript. If the context contains material on
   the asked topic or a closely related concept, answer from that material and cite it. Only say
   "I could not find this in the approved learning material for this module." when the context genuinely
   has nothing related to the question.
8. NEVER reveal quiz answer keys before submission.
9. NEVER promise or alter competency levels.
"""
                if lang == "hi":
                    system_prompt += """
10. Respond entirely in Hindi (Devanagari script), using standard Indian government statistical terminology.
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
                    max_tokens=450
                )
                answer_text = completion.choices[0].message.content.strip()

                if best_chunk:
                    return {
                        "answer": answer_text,
                        "source_lesson_id": best_chunk.get("lesson_id"),
                        "source_lesson_title": best_chunk.get("lesson_title"),
                        "timestamp_label": best_chunk.get("timestamp_label"),
                        "chunk_id": best_chunk.get("chunk_id"),
                        "citation_snippet": best_chunk.get("text_content", "")[:120] + "...",
                        "suggested_actions": self._contextual_follow_ups(question, relevant_chunks, lang)
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
                "suggested_actions": self._contextual_follow_ups(question, relevant_chunks, lang)
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
