# SkillBridge QA Guideline Book (SIH26101)
Team: Expeditioners | Theme: Smart Education | Category: Software

Read this once before judging. Everything is in simple words.

---

## 1. Our Idea in One Line
Government officers have to learn many skills for their job. Our platform checks which skills they are weak in, suggests the right iGOT courses, makes quizzes from the course videos, and only promotes their skill level after a senior checks their work. It's a closed loop: find gap → learn → practice → prove → level up.

## 2. The Problem (why we built this)
- iGOT Karmayogi has thousands of courses. Officers can't find the right one.
- Nobody measures which skill an officer is actually missing.
- Training is the same for everyone — not personal.
- Nobody checks if learning really happened.
- Heads of departments can't see if their staff is ready for future work.

## 3. The Full Pipeline (the heart of every answer)
1. **Admin adds an officer** → the system creates their skill profile (role, education, past training).
2. **Gap check** → the system compares the officer's current skills with the skills their job role demands. It makes a gap list (missing skills).
3. **Course suggestions** → the system matches each gap with the right iGOT course and gives a score + a reason for why that course.
4. **Learning path** → the system builds a step-by-step plan: Diagnostic → Foundation → Intermediate → Advanced → Practical → Assessment.
5. **Learn** → officer watches curated videos with searchable transcripts. Can jump to any timestamp. Can search any word in the transcript.
6. **Practice quiz** → AI makes MCQs from that same video transcript. Every question shows which part of the video it came from. Practice is only for learning — it NEVER changes the skill level.
7. **Formal assessment** → officer submits a practical task (like a real sampling design).
8. **Senior reviews** → a supervisor checks the work against a fixed marking sheet (rubric) and approves or rejects.
9. **Level up (max +1)** → if approved, the skill level goes up by at most 1 level. The engine recalculates everything — the gap shrinks and the path updates. Loop closes.

## 4. What is REAL in the demo vs FUTURE feature
Judges will ask "is this working?" Answer honestly:
- **REAL & working:** profiles, gap analysis, course matching with scores and reasons, learning path, YouTube video lessons with searchable transcripts, AI quizzes from transcripts, AI chatbot grounded in course content with timestamps, practice history, practical assessments, supervisor review with rubric, +1 level promotion rule, automatic path recalculation, admin dashboard with division-wise gaps, reviewer dashboard, 20 demo officers, full login system with roles.
- **Simulated (say "simulated, ready to plug in"):** live iGOT Karmayogi API connection. We built a 26-table copy of their data model and a connector stub. The moment we get API access, we swap it in — the code structure is already ready (provider pattern).
- **Future feature (say this confidently):** multilingual UI (the AI models already understand Hindi; the full UI language switch is on our roadmap). Predictive analytics (today the dashboard shows current gaps and target-role readiness; ML-based forecasting of future skill needs is phase 2).

## 5. Tech Stack (simple words)
- **Frontend:** React + TypeScript. Looks exactly like the iGOT Karmayogi portal (same navy/saffron/green theme, accessibility buttons A- A A+, high contrast).
- **Backend:** Python FastAPI. All logic lives in one clean "engine" file — the same math every time, no randomness.
- **Database:** SQLite for the demo (26 connected tables — users, skills, roles, courses, evidence, gaps). In production: PostgreSQL — same code, just a connection change.
- **AI:** Groq API running Llama models. We rotate multiple API keys. If the internet or the AI fails, the platform falls back to a built-in question bank and stored answers — the demo can never crash.
- **Login:** JWT tokens, 3 roles — Learner, Supervisor/Reviewer, Admin.

## 6. How Course Matching Works (the "algorithm" question)
Every recommended course gets a score out of 100:
- 40 points: how well the course matches the skill (relevance weight)
- 20 points: how big the gap is (bigger gap = more urgent)
- 15 points: how relevant to the officer's role
- 10 points: how relevant to the office's activities
- 10 points: how well the course level fits the officer's current level
- 5 points: prerequisites are respected
The system also skips courses the officer already finished and checks prerequisites. Every suggestion shows this breakdown — that's our **explainable AI**: no black box, you can see why.

## 7. Gap Levels & Readiness (simple rules)
- Gap = required level − current level.
- Gap of 2+ = HIGH (red). Gap of 1 = MEDIUM. Gap 0 = no gap. No data = "insufficient evidence" → system first asks for a diagnostic assessment.
- Officer readiness: READY / NEAR READY / DEVELOPMENT REQUIRED / CRITICAL GAPS / INSUFFICIENT EVIDENCE.

## 8. The 4 Safety Rules (our best QA answers)
These rules make us different from a normal LMS:
1. **Practice quiz can never raise your skill level.** It's only for learning. (Prevents gaming.)
2. **Level rises ONLY when a supervisor approves real practical work** — not by watching videos or clicking buttons.
3. **Max +1 level per approval.** No one jumps from L2 to L5 in a day.
4. **Only promotions apply.** If new evidence suggests a lower level, it's stored, not applied — an officer's level never drops from a bad day.
Bonus: submitting the same assessment twice is safely ignored (no double counting).

## 9. AI Safety (they WILL ask about hallucination)
- The chatbot and quiz-maker are **grounded**: they only use the official course transcripts as source material.
- Every answer cites the lesson, the timestamp, and a quote from the transcript. Every quiz question shows the exact video part it came from.
- If the answer isn't in the material, the bot says "I could not find this in the approved learning material" — it never makes things up.
- The bot refuses to reveal quiz answers before submission and never promises level promotion.
- **Traceability:** every AI question goes to the admin review queue before final approval.

## 10. Demo Walkthrough (who shows what)
- **Aarav Sharma (USR-001, Junior Statistical Officer):** big gap in Sampling → see the gap card → open the recommended course → watch video, search transcript → take practice quiz → see instant result with citations → submit practical assessment.
- **Isha Patel (USR-002) / Rohan Verma (USR-011):** different roles → different gaps → different courses. Shows personalization.
- **Sunita Rao (reviewer-001, Supervisor):** sees pending submissions → opens the officer's work → scores against the rubric → approves → officer's level +1, gap shrinks, path updates live.
- **Dr. Rajesh Kumar (admin-001, Admin):** all 20 officers, division-wise gap breakdown, can add new officers, upload transcripts, review AI-generated questions.
- Header has a **persona switcher** — switch users in one click during the demo.

## 11. Quick QA — Likely Questions & Short Answers
**Q: Is this just another LMS?**
A: No. An LMS gives courses. We build a verified skill profile, prove gaps with evidence, and update the profile only after supervised review. iGOT stays the learning source; we are the brain on top.

**Q: Why not directly integrate iGOT APIs now?**
A: Government APIs need official access approval. So we built a 26-table replica of the iGOT data model and a connector stub following the provider pattern — swapping in the live API is a config change, not a rewrite.

**Q: What if the AI gives a wrong question?**
A: Three guards: questions must come from the transcript (grounded), every question shows its source timestamp (traceable), and admin reviews AI questions before approval (human in the loop).

**Q: How do you know learning actually happened?**
A: Completion of a course is not proof. Proof = a practical task, scored by a supervisor against a rubric, stored as evidence. That's the closed loop.

**Q: Can officers cheat / game the level?**
A: No. Practice doesn't affect level. Only supervisor-approved practical work does, max +1 at a time, each evidence stored with a hash — resubmitting the same thing is ignored.

**Q: Where does the skill framework come from?**
A: MoSPI/NSSTA published job roles, competencies (TPAC) and training curricula. We mapped 32 competencies across 4 domains: Statistical, Technical, Digital Governance, Behavioural — each with 5 levels.

**Q: Is it scalable to all ministries?**
A: Yes. The engine is data-driven — roles and competencies live in tables, not code. Another ministry just loads their competency data; the same engine runs.

**Q: Why is your level system trustworthy?**
A: Deterministic engine — same input, same output, no randomness. Every level change has an evidence trail: who assessed, when, which rubric, what score.

**Q: What about officers with poor internet / low digital skills?**
A: Interface follows iGOT design (familiar), has font-size and high-contrast accessibility controls, and the offline fallback keeps the platform working even if the AI API is down.

**Q: Cost?**
A: Open-source stack (FastAPI, React, SQLite→PostgreSQL). Only real cost is AI API calls, which fall back to a built-in free question bank.

**Q: Data privacy?**
A: All data is inside the ministry's own database. JWT auth, role-based access (learner can't see admin data), no third-party data sharing. Ready for MeghRaj/cloud deployment.

**Q: What did you actually test?**
A: 8 module test suites + an end-to-end 12-step pipeline test + multi-assessment + AI generation tests. A reset script restores the demo state instantly.

## 12. Numbers to Remember
- 26 database tables | 32 competencies × 5 levels | 15 roles | 28 positions | 20 demo officers
- 30 courses mapped to competencies | ~784 iGOT courses studied during research
- 5 curated video playlists (Sampling, SQL, Python, R, Probability)
- Course score: out of 100 | Level promotion: max +1
- Backend: http://127.0.0.1:8000 (Swagger docs at /docs) | Frontend: http://localhost:5173

## 13. References (last slide backup)
- MoSPI — https://mospi.gov.in (problem source, official ministry)
- iGOT Karmayogi — https://igotkarmayogi.gov.in (784 live courses studied & mapped to MoSPI competencies)
- NSSTA — https://nssta.gov.in (official training & competency source)

## 14. Impact (if asked "so what?")
- **Social:** multilingual reach for officers across India.
- **Economic:** money goes only to training that's actually needed.
- **Operational:** assessment and learning paths run automatically.
- **Governance:** heads see real, evidence-based skill data of their workforce — today and for future roles.
- **One line:** training moves from "one-time, generic" to "continuous, role-specific, proven".
