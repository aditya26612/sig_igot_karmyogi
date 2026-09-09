# SIH26101: expanded dataset and integration overview

**Version 3.0.0 | 7 September 2026 | Synthetic integration demonstration**

## 1. What you receive

The same 26-table structure and original folder layout, expanded to **20 users, 32 competencies, 160 level definitions, 30 courses, 46 course mappings and 50 training records**. There are **1,937 canonical seed rows**. JSON, CSV, the ready-to-use SQLite database, review workbook and journey fixtures have been rebuilt together.

This is a tested data expansion, not a claim that the full SIH problem statement or a production learning platform is implemented. The original ZIP is untouched. Import this version into a **new database**, not over an existing application without a reviewed migration.

## 2. Preservation and structure

Both SQL schema files are byte-identical to the original package. No tables, columns, field types, relationships, primary keys, foreign keys or existing IDs were renamed. Original user profiles, position/role/activity assignments, required levels, current competencies, evidence and course records remain unchanged. All four existing training records remain. Every original user now has two history rows; each new user has three.

Only the description of the existing Statistical Computing competency (COMP-011) was clarified to mention Python, R and SQL. This does not award tool-specific proficiency: three distinct new competencies hold those skills. Existing broad Metadata and Dissemination (COMP-015) remains separate from Metadata Standards (COMP-024). Survey Design is separate from data collection, sampling and frame maintenance.

Seven complementary roles and 21 activities were added. Each role has a current/target position pair; target positions add the existing capability-leadership role. Existing official division names are reused as reference contexts; new fictional assignments are not claims about sanctioned posts or official division ownership.

The advisory SRS ranges are not hard schema limits: retaining the original 14 positions plus 14 new positions gives 28, and role-competency mappings total 85. Those deviations avoid repurposing existing personas. The recommendation/rubric rule version stays v2 because the engine's behavior is unchanged; expanded seed version is v3. Derived snapshot timestamps retain the original deterministic engine reference time, not the wall-clock build time.

## 3. Twenty meaningful personas

| User | Learning profile | Preservation | History rows |
|---|---|---|---|
| USR-001 | Field to supervisory field | Original, preserved | 2 |
| USR-002 | Entry technical to senior quality analyst | Original, preserved | 2 |
| USR-003 | Price-data analyst to senior index analyst | Original, preserved | 2 |
| USR-004 | Senior national-accounts specialist to technical supervisor | Original, preserved | 2 |
| USR-005 | Data steward to governance supervisor | Original, preserved | 2 |
| USR-006 | Survey-methods analyst to senior technical role | Original, preserved | 2 |
| USR-007 | Field supervisor to operations manager | Original, preserved | 2 |
| USR-008 | Technical supervisor to unit leadership | Original, preserved | 2 |
| USR-009 | Experienced field official to supervisory field | Original, preserved | 2 |
| USR-010 | Experienced supervisor ready for capability leadership | Original, preserved | 2 |
| USR-011 | Labour statistics analyst to labour-statistics capability lead | New | 3 |
| USR-012 | Agricultural statistics analyst to crop-statistics capability lead | New | 3 |
| USR-013 | SDG indicator analyst to indicator-quality capability lead | New | 3 |
| USR-014 | Data quality reviewer to cross-programme assurance lead | New | 3 |
| USR-015 | Python analyst to reproducible data-science lead | New | 3 |
| USR-016 | R analyst to statistical programming lead | New | 3 |
| USR-017 | SQL analyst to analytical data-products lead | New | 3 |
| USR-018 | Questionnaire and metadata analyst to survey-design lead | New | 3 |
| USR-019 | Cloud and API engineer to statistical platform lead | New | 3 |
| USR-020 | Cybersecurity reviewer to statistical-service security lead | New | 3 |

New personas are distinct learning profiles, not necessarily ten separate job functions. For example, the Python, R and SQL personas share the programming role but have different current evidence and gaps. The SDG analyst and quality reviewer share an assurance role with different weaknesses.

## 4. Added competencies and connected rows

| New competency | ID |
|---|---|
| Labour Statistics | COMP-019 |
| Agricultural Statistics | COMP-020 |
| SDG Indicators | COMP-021 |
| Data Quality Frameworks | COMP-022 |
| Survey Design | COMP-023 |
| Metadata Standards | COMP-024 |
| Python | COMP-025 |
| R | COMP-026 |
| SQL | COMP-027 |
| Data Visualization | COMP-028 |
| AI/ML | COMP-029 |
| Cloud Computing | COMP-030 |
| APIs | COMP-031 |
| Cybersecurity | COMP-032 |

Each added competency has five observable prototype level anchors, activity requirements, MAX-aggregated role requirements, assigned positions, explicit user states, separate simulated evidence, at least one positive target gap, course/blueprint mappings, mapped learning objectives and target-path items. Missing course availability is shown as a blocked catalogue step rather than hidden.

The original three unknown states across two users remain null. Unknown is not zero or level one: it produces a diagnostic requirement. Confidence remains separate from gap severity. Known gaps use required minus current; unmet gaps never go below zero. Current and target contexts are both present for all 20 users.

## 5. Honest problem-statement coverage

The statement names **33 items** across its four domain lists. This 32-competency package explicitly models **22 of those named items**, alongside 10 retained supporting/broader competencies. A count of 32 competencies therefore does **not** mean 32 of the named items are covered.

All ten statistical items are modeled. The eleven deliberately deferred items are **Stata, SPSS, SAS, Open Data, Digital Signatures, Government Cloud, Digital Public Infrastructure, Project Management, Ethics, Decision Making and Change Management**. They are not implicitly counted as covered through broad computing, cloud, leadership or critical-thinking labels. `docs/problem_statement_coverage.csv` lists each item and its status.

No official competency framework has been authenticated by this expansion. Definitions, levels and mappings are DERIVED project constructs. The supplied problem statement defines the requested scope, not authoritative evidence for fictional course outcomes.

## 6. Courses, objectives and recommendation boundaries

The package now contains **17 public-source metadata records and 13 explicitly fictional training blueprints**. Seven added metadata records use exact topic titles found in the historical/tentative NSSTA FY2025-26 calendar:

- CRS-011: Labour Force Statistics & Price Statistics (1w)
- CRS-012: Agriculture & Allied Statistics (1w)
- CRS-013: Theory & Practices in Official Statistics for Monitoring SDGs
- CRS-014: Data Analysis its Interpretation and visualization using R
- CRS-015: Foundation Course on Machine Learning using Python
- CRS-016: National Accounts Statistics
- CRS-017: Application of GIS, Forest Statistics & Data tools

These are documentary course/topic candidates, not current enrollment offers, verified syllabuses, confirmed individual TPAC approvals or new iGOT learner URLs. Provider authorship and instructional minutes are left null where the calendar does not support them. A venue is not automatically the authoring provider; five calendar days are not automatically a known number of learning minutes.

The three added blueprints are SQL query/reconciliation, cloud/API statistical services, and quality/metadata standards. Every new blueprint mapping connects to an actual positive gap. Public-source metadata can legitimately support training history or future catalogue work even when nobody currently has a gap in that topic.

All 32 competencies now have at least one course/topic/blueprint mapping. **All 46 mappings have an outcome at the proposed target level, and all 30 courses have at least one objective.** None of these newly added objectives is claimed to be a published provider learning outcome.

**CRS-010 remains deliberately unmapped.** “Know Your Ministry” now has an explicitly proposed orientation objective, but a ministry introduction is not evidence for a particular skill-level bridge. Inventing a mapping merely to remove an orphan would misrepresent the data. It is an intentional catalogue-only record and cannot enter a competency recommendation.

The existing four documentary-linked iGOT URLs are unchanged. Only the original Excel and Responsible Data Management mappings have **simulated demo approval**. All new mappings, including dedicated cybersecurity mappings, remain pending. No production approval or live-course verification was fabricated.

There are 10 stored scope-specific recommendation rows, but still only two distinct recommended course IDs. The new data-management support recommendations exercise the same safe rules with more personas. Other added skill gaps can correctly return `NO_VERIFIED_COURSE`. A real topic title alone is not enough for a recommendation. A completed course is excluded, an in-progress eligible course is resumable, and an L2-to-L3 bridge never claims to satisfy L4.

The original suggested prerequisite is retained. No additional mandatory prerequisites were invented without evidence. Original noncontiguous blueprint IDs remain intentionally stable; gaps in numbering are not missing rows.

## 7. Training, evidence and assessment fixtures

All 50 histories are `MOCK_BEHAVIOUR`, with `completion_verified=0`. Status, progress and dates are coherent. No fictional blueprint is marked completed. Historical topic dates are simulated attendance dates, not authenticated calendar-cohort schedules. Names end in Demo and emails use the reserved example.invalid domain.

All 125 new current-competency states have separately stored simulated manager-review evidence. Course completion never directly awards a competency level. The original sampling practice/practical feedback loop, idempotent retries, stale-evidence handling and conflicting-retry rejection are preserved and tested.

A second ingestible source is provided at `assessment/sql_practice.txt`: original teaching material on SQL join grain, NULL and validation. It is connected to the SQL blueprint and may be consumed by Person 1's document pipeline. It is not copied iGOT content, live AI generation, an approved scored assessment or a practical competency rubric.

**The evidence API still accepts only the configured sampling rubrics.** All 20 personas have a complete profile-to-gap-to-path read flow, but this is not a working assessed promotion loop for all 32 competencies. Cybersecurity evidence submitted using a sampling rubric is correctly rejected. New competency-specific rubrics and the Person 1 assessment pipeline require separate implementation and review.

## 8. How to integrate without schema changes

1. Extract into a new directory. Keep the original ZIP as your rollback reference.
2. Prefer `data/dataset.json` for typed imports. Use `data/table_order.json` for foreign-key-safe import order. `docs/baseline_v2.json` is comparison-only, never the current seed.
3. Use the supplied `data/demo.sqlite` directly for the local demo, or run the reset command below before starting the server.
4. Run the validation and local API checks while the server is stopped. The smoke tests reset this separate package's database before and after testing.
5. Start `backend/api.py`, then integrate through its API rather than sharing database tables between Person 1 and Person 2.

```sh
python backend/reset_demo.py
python backend/validate_v3.py
python backend/smoke_test.py
python backend/smoke_test_v3.py
python backend/api.py --port 8010
```

The inherited `backend/validate.py` is a v2-baseline test suite with v2 inventory expectations. `validate_v3.py` is the correct v3 entry point; it executes those same functional tests with four documented expanded-inventory/mapping expectations, then performs the expanded checks. Do not interpret raw v2 count failures as v3 data failures.

Key endpoints:

```text
GET /api/v1/mock/igot/users
GET /api/v1/mock/igot/users/USR-011/training-history
GET /api/v1/users/USR-011/competency-gaps?scope=current
GET /api/v1/users/USR-011/competency-gaps?scope=target
GET /api/v1/users/USR-011/recommendations?scope=target
GET /api/v1/users/USR-011/learning-path
GET /api/v1/users/USR-011/journey
GET /api/v1/mock/igot/courses/CRS-117
```

The API entry point returns **camelCase**. JSON/CSV/SQLite columns remain **snake_case**. Trace fields stored as JSON-in-TEXT become arrays or objects at the API boundary. Course modules/tags remain empty when unprovided. The `learning-path` endpoint is explicitly target-career scope.

CSV blanks represent nulls and must not become zero. The workbook is for review: Excel has limited floating-point precision, so JSON/SQLite are authoritative for fractional durations. All workbook values matched the seed within a 1e-10 numeric tolerance. Boolean-looking database flags remain 0/1 in canonical records.

Use a same-origin development proxy for browser integration; the loopback API has no cross-origin CORS implementation. The default local bearer token is a demo convenience, not authentication. Stop the server before reset/rebuild. Always render unavailable learning as an explicit catalogue gap, never as a clickable nonexistent course.

## 9. Executed verification

**212 structural, functional, preservation and export checks passed; 33 inherited HTTP checks passed; 251 expanded HTTP checks passed. Total: 496 executed checks, zero failures.** The 53 inherited structural/functional checks are included in the 212, not an additional count.

The checks cover unchanged SQL hashes and columns, original-row preservation, valid primary/foreign keys, SQLite integrity, all known states backed by evidence, complete new competency chains, correct gaps, every mapping's outcomes, coherent histories, no completed recommendations, recommendation eligibility, deterministic recomputation, all journey fixtures, JSON/CSV/SQLite/workbook parity, and HTTP reads for every user, competency and course. The database is restored to the expanded seed after HTTP tests.

Reports are in `docs/expansion_validation_report.json`, `docs/validation_report.json`, `docs/api_smoke_report.json` and `docs/api_expansion_smoke_report.json`.

This is **not a guarantee of zero integration issues**. PostgreSQL DDL was not executed; production security, concurrency, load capacity, live iGOT connectivity, curriculum validity and official course access were not verified. Runtime API dependencies remain Python standard library, Python 3.10+. Workbook validation additionally requires optional openpyxl; it was available during this review.

## 10. Remaining application requirements

Inserting data cannot implement educational-qualification fields, a current-assignment entity, actual learning-hours logs, live enrollment/completion adapters, SSO/RBAC, secure file ingestion, deployed cloud infrastructure, multilingual assistants, virtual laboratories, live LLM/ML assessment generation, dashboards or predictive analytics. These are still application or schema work. Do not count nominal course duration as recorded learning hours.

The new metadata covers NSSTA training topics but does not implement a separate TPAC recommendation adapter. No source URL has been used as a substitute learner URL. Production eligibility intentionally returns no courses until real validation and approval exist.

## 11. Table inventory

| Table | v3 rows |
|---|---:|
| sources | 13 |
| mdos | 1 |
| divisions | 6 |
| competencies | 32 |
| competency_levels | 160 |
| roles | 15 |
| activities | 34 |
| activity_competencies | 94 |
| role_competencies | 85 |
| positions | 28 |
| position_role | 41 |
| users | 20 |
| user_competencies | 202 |
| competency_evidence | 199 |
| courses | 30 |
| course_competencies | 46 |
| course_learning_outcomes | 59 |
| learning_outcome_competency | 58 |
| course_prerequisites | 1 |
| training_records | 50 |
| knowledge_resources | 2 |
| course_resources | 2 |
| competency_gaps | 338 |
| course_recommendations | 10 |
| learning_paths | 20 |
| learning_path_items | 391 |

## 12. Provenance source

[NSSTA tentative Advance Training Calendar FY2025-26](https://www.mospi.gov.in/sites/default/files/announcements/Circular_NSSTA_Advance_Training_Calander_FY%2825-26%29.pdf). Its inspected text supports the seven added historical topic titles only. Row-level sources distinguish that evidence from project-derived mappings and simulated attendance.

Earlier v2 documentation is retained under `docs/historical_v2/` for traceability, not as current inventory.
