# SIH26101: ten-user synthetic integration demo

**Version 2.0.0 | Seed reference: 6 September 2026 | Local synthetic demonstration**

A linked dataset, review workbook and runnable reference backend for the supplied competency-gap pipeline. This package does not connect to a government database, run a live LLM, or reproduce official iGOT completion and certification.

## Quick start

1. Open `SIH26101_Review_Workbook.xlsx`, starting with START_HERE and user_gap_matrix.
2. Read `docs/USER_JOURNEYS.md` for the ten individual scenarios.
3. Run `python backend/validate.py` to validate the immutable seed.
4. Run `python backend/api.py --port 8010` with Python 3.10+. Runtime uses only the Python standard library.
5. Fetch `http://127.0.0.1:8010/api/v1/users/USR-001/journey` from your frontend or browser. This local address is an API, not a course destination.
6. Follow `docs/DEMO_SCRIPT.md` for the judge-facing walkthrough and evidence POST.

Stop the server before running `python backend/reset_demo.py`. This restores only this package's local `data/demo.sqlite` from the immutable seed. Do not run reset if you want to preserve local demo changes. No external database is modified.

## Final inventory

| Item | Quantity / meaning |
|---|---|
| Fictional users | Exactly 10, USR-001 through USR-010 |
| Official-reference organization | 1 MDO and 6 divisions |
| Fictional position records | 14 |
| Derived roles | 8: six technical plus two supervisory/leadership roles |
| Derived activities | 13: original ten plus three explicitly marked extensions |
| Competencies | 18: fifteen backbone competencies plus three genuinely used leadership competencies |
| Competency level rows | 90, five per competency |
| Physical tables / seed rows | 26 / 745, including joins and derived snapshots |
| Official-source course metadata | 10 courses |
| Fictional training blueprints | 10, retained only where a known positive user gap exists |
| Real populated course URLs | 4 documented iGOT destinations; no live-access verification |
| Demo-approved mappings | 2, with explicitly simulated review |
| Stored recommendations | 4 scope-specific rows for two users, not four distinct courses |
| Unknown competency states | 3 across two users |
| Original teaching fixture | Three-page PDF, five traceable hand-authored MCQs |
| Automated checks | 53 structural/functional and 33 local HTTP checks passed |

The 745 rows are not independent random records or extra users. They include level definitions, requirements, evidence, current/target gaps and path steps. Unneeded fictional course blueprints were removed without renumbering retained IDs.

## Architecture and baseline reconciliation

Master Prompt v2 labels its schema “19 tables” but lists 20 names and also says not to split outcomes. Here, `course_learning_outcomes` is the physical outcome table with `course_id`; `learning_outcomes` is a compatibility view. There is no duplicate writable outcome dictionary or separate course-outcome join.

The original 19 baseline entities remain present. Seven supporting additions are `sources`, `divisions`, `course_prerequisites`, `competency_gaps`, `course_recommendations`, `learning_paths`, and `learning_path_items`. This is why there are 26 physical tables. In particular, activity-to-competency requirements, five-level definitions, training history, resources and course-resource links were not discarded merely because the later list omitted them.

Canonical names follow the plural v2 convention; read-only singular baseline aliases are supplied. `activities.role_id` remains the relationship, without a role_activity many-to-many table. `position_role` remains many-to-many with one primary role per position. Current and target roles are resolved through positions, not maintained as competing direct user-role assignments.

`COMP-SAMPLING` preserves the supplied hero competency ID. Other competency IDs are newly assigned COMP-002 through COMP-018. No second sampling record or fictitious formerly frozen COMP-001 is introduced. Current and target positions are different contexts and must not be silently conflated.

The five level names remain Awareness, Basic Application, Independent Application, Advanced, and Expert / Strategic. The latest explicit hyphenated activity IDs and Master Prompt v2 gap-status policy are used. The v2 HIGH/MEDIUM policy supersedes the older plan's severity labels explicitly, not silently.

## Provenance and fictional identity

Every canonical row carries provenance, a matching source_type alias, source_id and timestamps. Timestamps on reference facts indicate package creation, not government publication or live verification. Sources describe the exact supported claim; an official institution name does not validate its fictional employee assignments.

PUBLIC_OFFICIAL covers published MDO/division names and sourced course/source metadata. DERIVED covers normalized activities, competency definitions, levels, mappings, objectives and calculations. SYNTHETIC covers fictional people, positions, initial competency states, training blueprints and original teaching material. MOCK_BEHAVIOUR covers fabricated manager validation, training history, reviews and assessment events.

User names end with “Demo” and emails use `example.invalid`, a reserved non-deliverable domain. Career paths are plausible test hypotheses, not sanctioned posts, recruitment rules, years-of-service eligibility criteria or official promotion decisions. Readiness refers only to the selected project competency requirements.

The six divisions are FOD, HSD, EnSD, PSD, NAD and DIID. Enterprise Survey Division is not Economic Statistics Division; historical SDRD/DPDD names are not reintroduced.

## Courses: documentary links are not validated syllabuses

`destination_verified=true` means an exact course title-to-link association appears in the cited official publication. `verification_basis=OFFICIAL_PUBLISHED_LINK` specifies the method. All rows retain `live_access_verified=false` and `last_verified_at=null`. No claim is made about current enrollment, authentication, price, entitlement, certificate access or permission to copy course content.

Populated destinations belong only to Microsoft Excel Advanced, Responsible Data Management and the two IIT Madras Cybersecurity courses. Basics of Communication remains null as explicitly requested by the latest prompt, even though its documentary source can support a future reviewed update. The five MoSPI statistical/ministry courses retain unresolved URLs. Their authoring provider remains null because a MoSPI/NSSTA circular does not establish course authorship.

Unknown language, license and official syllabus fields remain null or empty. ASI/ASUSE durations retain fractional minutes. The 24 stored learning outcomes are DERIVED project objectives, not published iGOT syllabus text.

Only two mappings have APPROVED status: Excel to Digital Tools L2->L3, and Responsible Data Management to Statistical Data Management L2->L3. Both explicitly use SIMULATED_TRAINER_REVIEW, MOCK-TRAINER-001 and production_approved=0. They exercise a demo workflow; they are not actual human approvals or verified claims about course outcomes. Production eligibility rejects every current mapping.

Excel never maps to sampling or national accounts. Cybersecurity mappings are limited, pending proposals and never establish advanced statistical disclosure-control competence. An L2->L3 bridge never claims to satisfy an L4 requirement. Course completion never awards a level automatically.

Synthetic courses are BLUEPRINT_ONLY, with fictional providers, pending mappings and null URLs. They support training design only. They are not recommended as existing courses or presented with a Learn on iGOT button.

## Gap, ranking and readiness rules

Role requirement = MAX across its activity requirements. All contributing activity IDs and maximum-level contributors are stored. Position requirement = MAX across all assigned roles. Both CURRENT and TARGET gaps are calculated.

Unknown levels are SQL/JSON null with level_status=UNKNOWN; CSV uses blank cells. User-journey display may render UNKNOWN. Do not insert that string into an integer SQL column or substitute 0/1. Unknown gaps retain null signed_gap/unmet_gap and get INSUFFICIENT_EVIDENCE plus DIAGNOSTIC_REQUIRED.

For known values: signed_gap = required - current; unmet_gap = max(0, signed_gap). Unmet 2+ is HIGH, 1 MEDIUM, 0 NO_GAP. Confidence is stored separately and never multiplied into gap priority.

Readiness: any required unknown -> INSUFFICIENT_EVIDENCE; otherwise any HIGH -> CRITICAL_GAPS; two or more MEDIUM -> DEVELOPMENT_REQUIRED; one MEDIUM -> NEAR_READY; none -> READY. All five states occur.

Recommendation eligibility requires a known positive gap, an approved same-competency mapping, a documented real destination, a valid entry level and useful progression. Completed courses are excluded and in-progress courses are resumable. Ranking components are exposed: match 40, normalized gap 20, role 15, activity 10, level progression 10, prerequisites 5. These are project heuristics, not efficacy estimates. A suggested prerequisite is not represented as a published mandatory prerequisite.

Paths distinguish available supporting learning, missing catalogue coverage, planned practical work and planned assessment. Missing coverage remains NO_VERIFIED_COURSE, not an invented destination. Planned path items are not published assignments.

## Backend and AI boundary

`data/csv/` and `data/json/` contain identical canonical records. `data/dataset.json` is the immutable combined seed. `data/demo.sqlite` is ready to query. `data/table_order.json` gives import order. DDL was executed and tested in SQLite; PostgreSQL-oriented DDL is supplied but was not executed against PostgreSQL in this build.

Import into a NEW database/schema, not an existing application without a reviewed migration. JSON preserves nulls and numeric types and is the safest interchange format. JSON-in-TEXT trace fields in SQL are decoded into arrays/objects by the API. CSV imports must interpret blank cells correctly.

Person 1 consumes Person 2 APIs, not Person 2 database tables. The preferred API entry point is backend/api.py, with camelCase JSON fields; relational exports use snake_case. backend/server.py contains shared transport helpers. The reference server is loopback-only and uses a dummy bearer token for writes. It does not implement production RBAC, government SSO, TLS, tenancy, malware-safe uploads or real authorization.

The supplied sampling practice is hand-authored, not generated live. Trainer questions include answer keys; serve learner_questions.json before submission instead. Source chunks reference exact pages in an original project PDF, not official iGOT material. Quality scores and review states are simulated.

The five-question practice gives 4/5 = 80% and stores evidence without estimating a level. A separate practical fixture stipulates five assessed work products scoring 43/50 = 86%, with an independently anchored L3 estimate. The engine accepts only configured demo rubrics, rejects conflicting retries, preserves older evidence without overwriting newer state, and limits a qualifying practical promotion to one level. The ratio 86% does not determine L3.

## Further documentation

Architecture/PK/FK: docs/DATA_DICTIONARY.md. Ten journeys: docs/USER_JOURNEYS.md. API: docs/API_CONTRACT.md. Judge walkthrough: docs/DEMO_SCRIPT.md. AI boundary: docs/AI_HANDOFF.md. Sources: docs/SOURCES.md. Per-table provenance: docs/PROVENANCE_LEDGER.md and provenance_ledger.csv. Coverage limitations: docs/COURSE_COVERAGE.md and course_coverage.csv. Executed checks: validation_report.json and api_smoke_report.json.

Not supplied or claimed: finished learner/trainer UI, live LLM/RAG generation, multi-agent validation, official course content, live iGOT integration, official certification, expert-calibrated competency measurement, production security, PostgreSQL execution or load-tested scalability.
