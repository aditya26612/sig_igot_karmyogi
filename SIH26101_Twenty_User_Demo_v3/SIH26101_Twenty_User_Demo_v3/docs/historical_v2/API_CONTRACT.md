# Local integration API

Start `python backend/api.py --port 8010`. Base URL: `http://127.0.0.1:8010`. JSON response fields are camelCase; exported table fields are snake_case. This local address is for development, never a learner course destination.

## Reads

- GET `/api/v1/mock/igot/users` and `/users/{userId}`
- GET `/api/v1/mock/igot/users/{userId}/position`
- GET `/api/v1/mock/igot/users/{userId}/competencies`
- GET `/api/v1/mock/igot/users/{userId}/training-history`
- GET `/api/v1/mock/igot/users/{userId}/learning-context`
- GET `/api/v1/mock/igot/positions` and `/positions/{positionId}`
- GET `/api/v1/mock/igot/positions/{positionId}/roles`
- GET `/api/v1/mock/igot/positions/{positionId}/competencies`
- GET `/api/v1/mock/igot/roles` and `/roles/{roleId}`
- GET `/api/v1/mock/igot/roles/{roleId}/activities`
- GET `/api/v1/mock/igot/roles/{roleId}/competencies`
- GET `/api/v1/mock/igot/competencies` and `/competencies/{competencyId}`
- GET `/api/v1/mock/igot/courses` and `/courses/{courseId}`
- GET `/api/v1/mock/igot/courses/{courseId}/competencies`
- GET `/api/v1/users/{userId}/competency-gaps?scope=current|target`
- GET `/api/v1/users/{userId}/recommendations?scope=current|target`
- GET `/api/v1/users/{userId}/learning-path`
- GET `/api/v1/users/{userId}/journey`

The abbreviated paths on the same line inherit the preceding `/api/v1/mock/igot` prefix. Gap/recommendation scope defaults to CURRENT. The learning path is explicitly a TARGET career-development path and says so in its response. Course details include learningOutcomes, competencies, resources, empty modules/tags and `contextCompleteness=PARTIAL_NOT_VERIFIED_SYLLABUS`. Do not interpret empty modules as confirmation that an official course has no modules. `?q=Excel` supports simple catalogue filtering. This compact demo returns full small arrays, not production pagination.

Position competency requirements return an object keyed by competency ID with requiredLevel, roleIds and activityIds. User competency display returns currentLevel as an integer or `UNKNOWN`; gap rows keep currentLevel/signedGap/unmetGap null when unknown.

## Evidence write

POST `/api/v1/users/USR-001/competency-evidence`

Headers: `Content-Type: application/json`; `Authorization: Bearer local-demo-only`. Set environment variable `SIH_DEMO_TOKEN` to override the shared local token. It is not a real government credential.

Send `fixtures/evidence_practical.json` unchanged for the deterministic walkthrough. This fixture extends the baseline with assessedAt, rubricVersion, reviewed, coverage and itemCount so the estimation guard is explicit.

```sh
curl -X POST http://127.0.0.1:8010/api/v1/users/USR-001/competency-evidence \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer local-demo-only' \
  --data-binary @fixtures/evidence_practical.json
```

Expected update: COMP-SAMPLING L2 -> L3. Current-role sampling requirement is L3, so that current gap becomes zero; target supervisory requirement is L4, so the target gap becomes one. This is not evidence of iGOT completion and does not remove unrelated gaps.

A repeated identical payload returns IDEMPOTENT_REPLAY without a second evidence row. Reusing an assessment ID with changed content returns 400. Path/payload user mismatch, invalid levels, unknown competency IDs, invalid scores/confidence/coverage and unsupported rubric IDs return 400. Missing demo write token returns 401. Unknown routes return 404; malformed/unknown user values may return 400 in this minimal implementation.

The package only implements fixed sampling practice/practical rubrics as executable examples. Extend the trusted assessment registry and evidence policy for other competencies; do not accept arbitrary client-claimed levels in a real application. The submitted reviewed flag is trusted only within this synthetic demo service boundary and is not real trainer authorization.

All evidence in this endpoint must be MOCK_BEHAVIOUR. Real assessment ingestion, per-learner authorization, signed assessment provenance and robust multi-writer concurrency remain implementation work.

## Person 1 and Person 2 handoff

Person 2 serves context, requirements, computed gaps, courses, mappings and readiness. Person 1 uses the returned competency IDs and approved material to create/review an assessment, presents learner-safe questions, scores attempts and submits evidence. Only Person 2 applies estimation rules and updates current state.

`assessment/questions.json` contains answers, explanations and trainer metadata: never send this whole file to the learner before submission. Use `assessment/learner_questions.json` for learner presentation. The package fixtures are hand-authored and do not establish that the application's LLM generation or validation pipeline is implemented.
