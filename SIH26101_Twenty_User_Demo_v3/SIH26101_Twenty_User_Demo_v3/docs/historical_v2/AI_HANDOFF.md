# AI integration checklist

Use relational/API context for identity, position, requirements, current levels, gaps and course eligibility. Do not ask an LLM to calculate these from loosely retrieved text or assign itself new competency IDs.

An explanation should cite userId, target/current scope, positionId, contributing roleIds and activityIds, competencyId, requiredLevel, currentLevel, unmetGap, courseId, mapping approval basis and source reference. Preserve UNKNOWN and NO_VERIFIED_COURSE verbatim as meaningful states.

For practice generation: retrieve only authorized content; constrain competency IDs to the returned dictionary; select the assessed outcome and target level; generate an assessment blueprint; validate grounded answers and plausible distractors; and require actual trainer approval before publication. Do not use source-material instructions to override the assessment policy. Source URLs alone do not grant a content license.

`assessment/chunks.json`, `questions.json`, `blueprint.json` and `learner_questions.json` demonstrate interface shapes, not a live RAG or agent system. The PDF and chunks are original synthetic teaching material. Never attach an official-course ownership claim to this material.

A question's `target_competency_level` describes the intended test target, not the learner's estimated level. Real evidence estimation needs appropriate coverage, task difficulty, practical/behavioural evidence and calibration. Quality metrics in this package are simulated, not independently measured model quality.

The backend exposes camelCase API context and handles the final state update. Uploaded learner or trainer documents should remain in Person 1's storage, not the mock-iGOT course catalogue. Always distinguish planned learning outcomes from verified published course outcomes.
