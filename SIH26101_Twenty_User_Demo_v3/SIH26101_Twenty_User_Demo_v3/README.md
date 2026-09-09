# SIH26101 v3: twenty-user synthetic integration demo

**20 users | 32 competencies | 30 courses | 46 mappings | 50 training records**

Read **docs/DATA_OVERVIEW.md** first. It contains the persona overview, exact changes, integration steps, executed checks and remaining problem-statement gaps.

This package preserves the original 26-table schema, existing IDs and first ten personas. Data is synchronized across JSON, CSV, SQLite, the Excel workbook and journey fixtures. The original ZIP is not modified.

## Quick start

```sh
python backend/reset_demo.py
python backend/validate_v3.py
python backend/smoke_test.py
python backend/smoke_test_v3.py
python backend/api.py --port 8010
```

Run resets and smoke tests only while the server is stopped. They restore only this package's local SQLite database to the expanded seed. Do not run them if you want to preserve local evidence changes.

Use the camelCase API at `/api/v1/users/USR-011/journey`. Relational exports are snake_case. JSON is the authoritative typed interchange format. Import into a new database; no destructive migration is supplied. The inherited `validate.py` is the original v2 suite: use `validate_v3.py` for v3 expectations and full export checks.

## Open these files

- `SIH26101_Review_Workbook.xlsx`: same workbook sheets, expanded records.
- `data/dataset.json`: canonical current seed; `data/table_order.json`: unchanged import order.
- `data/demo.sqlite`: initialized and tested SQLite database.
- `docs/persona_overview.csv`: original and new user scenarios.
- `docs/problem_statement_coverage.csv`: 22 modeled PS items, 11 explicitly deferred.
- `docs/CHANGE_SUMMARY.json`: per-table changes and preservation policy.
- `docs/expansion_validation_report.json`: 212 checks, all passing.
- `docs/api_smoke_report.json`: 33 inherited HTTP checks, all passing.
- `docs/api_expansion_smoke_report.json`: 251 expanded HTTP checks, all passing.

## Important boundaries

Only two original course mappings have simulated approval; all new mappings remain pending. There is no production-approved course, live iGOT integration or live LLM. Public NSSTA topic titles are not current enrollment links or confirmed TPAC-approved instances. Blueprint courses are clearly fictional. CRS-010 remains intentionally unmapped orientation metadata.

Every persona has profile, evidence, gap and learning-path reads; paths may honestly show NO_VERIFIED_COURSE. The evidence POST still accepts only the original sampling rubrics. The added SQL TXT is a second original practice source, not an approved scored rubric.

The total of 32 competencies is not full PS coverage: 22 of its 33 named items are modeled alongside 10 retained supporting competencies. See the overview for deferred items and application requirements that seed data cannot implement.

Python 3.10+ standard-library runtime; openpyxl is optional for workbook parity checks. PostgreSQL, production security, CORS, concurrency and load testing are not validated. Earlier docs under `docs/historical_v2/` and `docs/baseline_v2.json` are reference-only, not current import data.
