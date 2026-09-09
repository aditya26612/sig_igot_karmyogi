# A credible seven-minute judge walkthrough

## 1. Set the boundary, 30 seconds

Say: “This is a competency-intelligence layer around iGOT, not an iGOT clone. Employee profiles, career requirements and assessment events are synthetic. Course links are taken from official publications; no live government integration is claimed.” Show the provenance columns in the workbook.

## 2. Show work-to-gap reasoning, 90 seconds

Open USR-001. Current position POS-001 maps to Survey Field Operations. Target POS-002 includes Survey Field Supervision as well as field work. Drill into COMP-SAMPLING: ACT-001 needs L3, supervisory ACT-011 needs L4, current evidence is L2. Show current gap 1 and target gap 2 separately. This distinction is more useful than a generic “skill score.”

Show Digital Tools as a separate L2-to-L3 gap: ACT-003 contributes the L3 requirement. Microsoft Excel Advanced has a documented real destination and a simulated-review supporting mapping. Click the actual course link if accessible, but do not pretend you can complete it or inspect its private content without authorized access. Do not describe Excel as sampling training.

## 3. Demonstrate an honest missing-course branch, 45 seconds

Return to Sampling Methodology. The gap is real in the synthetic scenario, but there is no verified sampling-course destination. Show NO_VERIFIED_COURSE. Open the fictional sampling-training blueprint and explain that it is an internal training design, not an iGOT course. This refusal to invent a course is intentional product behavior.

## 4. Show exact assessment traceability, 90 seconds

Open `assessment/learner_questions.json` in your learner UI, or inspect the provided sample. For trainer source review, show question Q-DEMO-001 with `assessment/sampling_practice.pdf`, page 1, “Stratified sampling,” and the exact supporting passage. Show the chunk ID and file hash in `assessment/chunks.json`.

Say: “These are hand-authored, simulated-review fixtures. Our AI layer must produce and validate the same schema from authorized material.” Do not claim that the supplied fixture was generated live by an LLM.

Run `python assessment/score_demo.py`: four of five correct gives 80%. Submit the practice fixture if desired; it stores evidence but must not automatically change the competency level.

## 5. Close the evidence loop, 60 seconds

Show the separate practical rubric, not the MCQ score. It stipulates five assessed work products and a mock 43/50 result with an independently anchored L3 estimate. POST `fixtures/evidence_practical.json`. Reload the user journey: sampling moves L2 -> L3, target requirement remains L4, and the target gap falls 2 -> 1. The missing-course branch remains honest. Submit again to demonstrate idempotency.

## 6. Show missing evidence and course bridges, 60 seconds

Open USR-006: Statistical Computing is UNKNOWN. There is no invented zero/one or numeric gap; readiness is INSUFFICIENT_EVIDENCE and the first step is diagnostic evidence collection.

Open USR-005: Responsible Data Management is already in progress in the mock history. It supports proposed L2 -> L3 learning but the target requirement is L4. Show the remaining advanced learning gap. Course completion alone does not close it.

## 7. Show readiness without overtraining, 45 seconds

Open USR-010: READY on project competency requirements, with no unnecessary remedial recommendations. Explain that this is not an official promotion decision.

Show the 53 structural/functional checks and 33 local HTTP checks. Mention what was not tested: government integration, course enrollment, real LLM generation, expert calibration and production-scale performance.

## Reset for the next demo

Stop the API server, run `python backend/reset_demo.py`, and restart `python backend/api.py --port 8010`. Never replace a failed live course click with a fake course page or fake certificate. Keep screenshots or a source publication available as documentary evidence, labeled with their actual context.
