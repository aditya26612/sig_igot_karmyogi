# Zero-Budget Hybrid RAG Implementation — Design Spec

**Date:** 2026-09-10
**Status:** Approved by user (approach A: Local Hybrid RAG)
**Scope:** Quiz/assessment generation + AI Learning Copilot retrieval grounding

## 1. Problem Statement

The platform (SIH Karmayogi learning platform for MoSPI statistical officers) generates
AI quizzes from lesson transcripts and answers copilot questions. Today:

- Transcripts are ~13 hand-seeded chunks; there is no chunking pipeline.
- Retrieval is lexical `LIKE`-based keyword matching with hand-scored hit counts
  (`transcript_service.search_transcripts_keywords`).
- Quiz generation takes the first 4 chunks of a lesson in timestamp order — no
  relevance ranking at all (`groq_service.generate_quiz_questions`).
- There is no re-ranking stage, no semantic search, and no semantic grounding
  validation of LLM-generated questions.
- Groq calls have no 429-aware key rotation, no explicit timeouts, and quiz JSON
  is parsed by string slicing instead of JSON mode.

This makes the system "partially RAG": grounded generation exists, but retrieval
quality and chunk coverage cannot support real lesson-length transcripts.

## 2. Goals & Constraints

### Goals
1. Build a true RAG pipeline: overlapping chunking → hybrid retrieval (BM25 +
   embeddings) → cross-encoder re-ranking → grounded generation with validated
   citations.
2. Process real YouTube captions for the 25 catalogued lessons into ~400–1,000
   overlapping chunks (replacing hand-seeded data as the primary corpus).
3. Improve quiz generation to select context chunks by relevance (not timestamp
   order), with a semantic grounding check that rejects ungrounded questions.
4. Improve copilot answers with hybrid retrieval and an optional reranker stage.
5. Provide an evaluation harness measuring retrieval quality (hit@k, MRR) so
   improvements are provable to judges.
6. Reduce perceived and real latency: background quiz pre-generation, 429-aware
   Groq key rotation, JSON mode, trimmed token budgets, optional SSE streaming.

### Hard Constraints (user-confirmed)
- **$0 budget.** No paid APIs. Free tiers + local models only.
- **Hardware ceiling:** two laptops — RTX 2050 4GB VRAM and RTX 4050 4GB VRAM.
  Every model must fit or spill gracefully; CPU fallback everywhere.
- **Hugging Face role:** download-only (model files pulled once, run locally).
  The HF Inference API (hosted calls) is explicitly NOT used — it is
  rate-limited, internet-dependent, and demo-fragile.
- **LLM generation chain:** Groq free tier (primary) → Ollama qwen2.5:1.5b
  (local backup, detected via OLLAMA_BASE_URL) → existing deterministic
  question-bank / transcript-quote fallback (final).
- **No new servers:** SQLite only (FTS5 + vector BLOBs). No vector DB, no
  Redis, no Celery.
- **Learner-facing requests never call YouTube.** Caption fetching is a
  one-time, resumable, CLI/admin ingestion process (per-IP rate-limit safety).
- **Graceful degradation:** every new stage must disable itself and fall back
  to the previous behavior when models/keys are missing. The platform must
  never become less reliable than today.

## 3. Non-Goals

- No multilingual *generation* changes beyond what exists (EN/HI prompt rules
  stay as-is).
- No changes to formal assessment flow (PRACTICAL assessments, reviewer queue,
  competency levels) except where retrieval feeds them.
- No frontend redesign; only minimal additions (e.g., SSE consumption if
  streaming is built).
- No vector database migration (Chroma/Qdrant/FAISS service) — SQLite at this
  corpus scale (~1,000 chunks, ~1.5MB of vectors) is sufficient.
- No re-chunking of the hand-seeded CHK-DEMO chunks — they remain as stable
  demo fixtures.

## 4. Architecture Overview

```
INGESTION (one-time CLI: scripts/ingest_transcripts.py, never on request path)
  youtube-transcript-api fetch (jittered, resumable)
    → raw_transcripts cache (permanent; re-chunking never re-fetches)
    → clean (join caption fragments, de-noise)
    → overlapping chunker (~900 chars, ~225 char overlap, timestamp-gap aware)
    → transcript_chunks (provenance='AUTO_CHUNK')
    → FTS5 index rebuild (transcript_fts)
    → embedding backfill (chunk_embeddings)

QUERY TIME (learner path)
  question (EN or HI)
    ├─ lexical: HI→EN dictionary expansion → FTS5 BM25 top-20
    ├─ semantic: multilingual embedding → cosine top-20
    ├─ RRF fusion (k=60) → top-20 → [optional] bge-reranker-v2-m3 → top-4
    └─ scope filters respected (lesson_id / competency_id)
  → context assembly (chunk_id-labeled)
  → generation chain: Groq → Ollama qwen2.5:1.5b → deterministic fallback
  → validation: structural + semantic grounding (embed Q vs cited chunk)

QUIZ PRE-GENERATION (background thread, triggered on lesson/video open)
  same retrieval + generation, persisted to practice_quizzes/practice_questions
  so the quiz endpoint is a cache hit when the learner clicks "Practice".
```

### Component boundaries (new services)
| Unit | Purpose | Interface | Depends on |
|---|---|---|---|
| `chunking_service` | transcript text → overlapping chunks | `chunk_transcript(text, segments) -> List[Chunk]` | none |
| `embedding_service` | text ↔ float vectors; model singleton | `embed_texts(list[str]) -> ndarray`, `embed_query(str)` | sentence-transformers, numpy |
| `retrieval_service` | hybrid search entry point | `retrieve(query, lesson_id?, competency_id?, top_k) -> List[Chunk]` | FTS5, embedding_service |
| `reranker_service` | optional cross-encoder stage | `rerank(query, candidates) -> List[Chunk]` (or pass-through) | sentence-transformers, embedding-free |
| `llm_router` | generation chain + retries | `generate(system, user, json_mode, max_tokens) -> str` | groq, ollama |

All singletons lazy-load and cache models; each exposes an `is_available()`
probe used by the degradation logic and the eval harness.

## 5. Data Model

New tables only; existing tables are not migrated.

```sql
-- permanent raw caption cache
CREATE TABLE IF NOT EXISTS raw_transcripts (
    lesson_id TEXT PRIMARY KEY,
    transcript_text TEXT,
    language TEXT DEFAULT 'en',
    source TEXT DEFAULT 'YOUTUBE_AUTO',        -- YOUTUBE_AUTO | YOUTUBE_MANUAL | SEED
    fetched_at TEXT,
    status TEXT DEFAULT 'FETCHED'             -- FETCHED | FAILED | SKIPPED
);

-- vector store (384-dim float32 = 1536 bytes per chunk)
CREATE TABLE IF NOT EXISTS chunk_embeddings (
    chunk_id TEXT PRIMARY KEY,
    embedding BLOB,
    model_name TEXT,
    created_at TEXT
);

-- FTS5 lexical index (rebuilt on ingest)
CREATE VIRTUAL TABLE IF NOT EXISTS transcript_fts USING fts5(
    chunk_id UNINDEXED,
    text_content,
    topic,
    tokenize='unicode61'
);
```

`transcript_chunks` gains no new columns; `provenance='AUTO_CHUNK'` marks
generated chunks. Chunk IDs for auto chunks: `CHK-{lesson_id-upper}-{seq:03d}`.

## 6. Ingestion & Overlapping Chunking Design

### Fetch stage (`scripts/ingest_transcripts.py`)
- Iterate `curated_lessons` (25 lessons) where `raw_transcripts` row is not
  FETCHED.
- Fetch captions via `youtube-transcript-api` with 3–5s jittered delay between
  requests; retry once on failure; mark FAILED and continue (seed chunks still
  serve that lesson).
- Persist raw caption text + language into `raw_transcripts` immediately.
- Resumable: re-running skips FETCHED lessons. Idempotent: re-running after a
  code change re-chunks from the raw cache without any YouTube traffic.
- `--refetch` flag forces re-fetch for one lesson or all.

### Chunker (`app/services/chunking_service.py`)
Input: raw transcript text + timestamped caption segments.
1. Join fragments into continuous text; strip repeated filler tokens.
2. Segment at timestamp gaps > 2 seconds (natural topic boundaries for
   auto-captions, which lack punctuation).
3. Sliding window over the segment-merged text: **~900 characters target,
   ~225 character overlap (25%)**. Windows advance by ~675 chars.
4. Each chunk stores the time range of its span (start_seconds of first char,
   end_seconds of last char) → timestamp citations keep working.
5. Emit `Chunk` dicts matching `transcript_chunks` columns.

Properties to guarantee (unit-tested):
- **Coverage:** every original character position appears in ≥1 chunk.
- **Overlap:** consecutive chunks from the same lesson share ~25% prefix/suffix
  text.
- **Bounds:** each chunk's time range covers its text span; ranges are
  monotonic within a lesson.
- **Determinism:** same input → identical chunk sequence (stable IDs).

### Near-duplicate control
Overlapping windows produce near-duplicate neighbors. Retrieval merges
adjacent same-lesson hits whose time ranges overlap by >50% of the smaller
chunk's duration before final ranking (keeps top-4 context diverse).

## 7. Hybrid Retrieval Design

### Lexical: SQLite FTS5
- `transcript_fts` over `text_content` + `topic`, `unicode61` tokenizer
  (handles Devanagari script runs).
- Query prep: lowercase, strip existing stopwords, then **expand Hindi domain
  terms to English via the existing `_HI_TO_EN_TERMS` dictionary** (dictionary
  stays; it now serves lexical expansion while embeddings handle semantics).
- BM25 ranking (`bm25()`), limit 20 per leg.

### Semantic: local multilingual embeddings
- Model: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
  (470MB, 384-dim, 50+ languages including Hindi).
- Embed all chunks at ingest (backfill script / automatic post-chunking);
  store float32 bytes as BLOB.
- Query time: embed the question, load all (or scope-filtered) vectors into a
  numpy matrix (cached, invalidated on embedding table change), cosine top-20.
- GPU used if available; CPU works fine at this scale (single-query embed
  ~20–50ms CPU).

### Fusion: Reciprocal Rank Fusion
`score(d) = Σ_legs 1 / (60 + rank_leg(d))`, k=60. Documents appearing in both
legs outrank single-leg hits. Scope filters (lesson_id, competency_id) are
applied before fusion in both legs.

### Re-ranking (optional stage)
- Model: `BAAI/bge-reranker-v2-m3` via
  `sentence_transformers.CrossEncoder`, lazy singleton.
- Reranks fused top-20 → selects top-4. GPU preferred (~100ms/20 pairs);
  CPU acceptable (~200–400ms); env flag `RAG_RERANKER_ENABLED` (default on,
  auto-off if model load fails → RRF order used).

## 8. Generation Chain & Grounding Validation

### `llm_router.py`
- Providers in order: Groq (all configured keys, round-robin) → Ollama
  (`qwen2.5:1.5b` at `OLLAMA_BASE_URL`, default `http://127.0.0.1:11434`) →
  None (caller uses deterministic fallback).
- **429-aware rotation:** on 429/5xx from key A, immediately retry with key B
  (up to all keys, once each), then exponential backoff across the set
  (max ~2 rounds), then degrade to Ollama.
- **Timeouts:** assistant 8s, quiz generation 20s (per attempt).
- **JSON mode:** quiz generation uses `response_format={"type":"json_object"}`
  with the prompt asking for `{"questions": [...]}` — eliminates the
  string-slicing parser. A defensive string-fallback parser remains for
  Ollama output (no JSON mode there).
- **Token budget:** quiz `max_tokens` 1600 → 1100; assistant stays 450.
- Dead code: `quiz_gen_service.generate_ai_quiz_questions` (unused duplicate
  with a broken response_format expression) is deleted; seeding logic remains.

### Semantic grounding validation (quiz path)
1. Context passed to the LLM labels each chunk: `[CHUNK <chunk_id> | ...]`.
2. Prompt requires `chunk_id` per generated question.
3. Post-validation (after existing structural checks):
   embed(question + explanation) vs embed(cited chunk text); cosine < 0.45
   → question dropped (counted in logs as GROUNDING_REJECT).
4. If <3 questions survive, the whole batch falls back to the question bank
   (existing behavior preserved).

### Copilot path
- `ask_grounded_assistant` retrieval branch (`else: search_transcripts_keywords`)
  is replaced by `retrieval_service.retrieve(question)`.
- Lesson/competency scoped branches use the same service with scope filters —
  replaces "first 4 by timestamp" with "top-4 by relevance".
- Citation format, answer style, follow-ups, and deterministic fallback remain
  unchanged.

### Streaming (optional final phase)
- SSE variant of the assistant endpoint (`/api/assistant/ask/stream`):
  token streaming from Groq (and Ollama), assembled metadata (citations)
  attached at the end as a final SSE event. The non-streaming endpoint stays.

## 9. Latency Strategy

| Change | Effect |
|---|---|
| Background quiz pre-generation (thread on lesson open; persisted) | Quiz endpoint becomes cache hit; learner never waits for Groq |
| 429-aware key rotation + backoff | No dead time on rate-limit bursts |
| JSON mode for quizzes | Removes parse failures + retries |
| max_tokens 1600→1100 | ~30% faster generation |
| Explicit timeouts (8s/20s) | Fast failure into fallback chain |
| Reranker on GPU / off on CPU-slow | Optional 100–300ms for large precision gain |
| SSE streaming (optional) | ~70% lower perceived latency for copilot |
| AI_PRESENTATION_DELAY env-gated | The 3s artificial demo delay can be disabled |

Non-LLM retrieval overhead target: <400ms end-to-end (FTS5 <10ms, query embed
20–50ms, rerank 100–300ms).

## 10. File Change Map

### New backend files
- `app/services/chunking_service.py` — chunker + near-dup merge helper
- `app/services/embedding_service.py` — model singleton, embed/bytes utils
- `app/services/retrieval_service.py` — FTS5 + vector + RRF + scope filters
- `app/services/reranker_service.py` — CrossEncoder singleton, pass-through
- `app/services/llm_router.py` — generation chain, rotation, timeouts
- `scripts/ingest_transcripts.py` — fetch + chunk + index + embed pipeline
- `tests/eval_retrieval.py` — golden-set evaluation harness
- `backend/data/golden_set.json` — 25–30 labeled query→chunk pairs (EN+HI)

### Modified backend files
- `app/config.py` — new settings: OLLAMA_BASE_URL, OLLAMA_MODEL,
  RAG_RERANKER_ENABLED, RAG_EMBEDDING_MODEL, RAG_CHUNK_* params,
  GROQ_TIMEOUT_*, delay flag semantics
- `app/database.py` — create new tables + FTS5 virtual table on init
- `app/services/groq_service.py` — use llm_router; retrieval via
  retrieval_service; JSON mode; grounding validation; chunk-labeled context
- `app/services/quiz_gen_service.py` — delete dead `generate_ai_quiz_questions`
- `app/services/transcript_service.py` — keyword search remains as legacy
  fallback; content_router search endpoint optionally upgraded to FTS5
- `app/routers/assistant_router.py` — route via retrieval_service; optional SSE
  endpoint
- `app/routers/practice_router.py` — background pre-generation trigger on
  lesson fetch; env-gated presentation delay
- `app/routers/content_router.py` — transcript search endpoint uses FTS5 path

### Frontend (minimal, only if streaming phase is built)
- `src/views/copilot/*` — EventSource consumption for the SSE endpoint

### requirements
- Add: `sentence-transformers`, `numpy`, `youtube-transcript-api`, `httpx`
  (Ollama probes). Torch already required by sentence-transformers (CPU wheel
  acceptable; CUDA wheel if laptops have it).

## 11. Evaluation Harness

`tests/eval_retrieval.py`:
- Loads `golden_set.json`: items `{query, lang, expected_chunk_id,
  optional expected_lesson_id}` across EN + HI, covering sampling, SQL,
  Python, R, probability, quality, ML topics.
- Runs four configurations and prints a table:
  1. `like` (today's `search_transcripts_keywords`)
  2. `fts5` (lexical only)
  3. `hybrid` (FTS5 + embeddings + RRF)
  4. `hybrid+rerank`
- Metrics: hit@1, hit@3, hit@5, MRR.
- Exits non-zero if `hybrid` regresses vs `like` on hit@5 (regression guard).

## 12. Degradation Matrix (must always hold)

| Condition | Behavior |
|---|---|
| No models downloaded (first run, offline) | FTS5-only retrieval; Groq → deterministic generation fallback; platform fully usable |
| Embedding model fails to load | Retrieval falls back to FTS5-only (logged, not fatal) |
| Reranker fails to load / disabled | RRF order used directly |
| No Groq keys | Ollama if present, else deterministic fallback |
| Ollama absent | Skipped silently in chain |
| YouTube fetch fails for a lesson | Lesson keeps seed chunks; ingestion marks FAILED and continues |
| SQLite lacks FTS5 (exotic build) | Legacy keyword search used (probe at startup) |
| 429 burst from Groq | Key rotation + backoff, then chain degrade |

## 13. Testing Strategy

- **Unit:** chunker (coverage/overlap/bounds/determinism), RRF math, embedding
  bytes round-trip, grounding threshold logic, 429 rotation logic (mocked),
  JSON-mode parse + defensive parse.
- **Integration:** ingest script against fixture transcripts (no network);
  retrieval end-to-end on a seeded test DB; quiz generation with mocked
  llm_router; practice_router cache-hit path.
- **Eval:** golden-set harness as regression gate.
- **Manual smoke:** run backend, ask copilot EN+HI questions, open lesson →
  quiz pre-generated, kill Groq keys → Ollama/deterministic still serves.

## 14. Implementation Phases (summary; detailed plan follows separately)

1. **Phase 0 — cleanup & FTS5.** Dead code removal; FTS5 table + search;
   config additions; delay flag.
2. **Phase 1 — ingestion & chunking.** Fetch script, chunker, ingest
   pipeline, seed-preservation.
3. **Phase 2 — embeddings & hybrid retrieval.** Embedding service, vector
   backfill, retrieval_service with RRF, wire into assistant + quiz paths.
4. **Phase 3 — reranker + grounding validation.** Reranker stage, chunk-labeled
   context, semantic grounding check.
5. **Phase 4 — latency & polish.** llm_router (rotation/timeouts/JSON mode),
   background pre-generation, eval harness, optional SSE.

Each phase leaves the platform in a working, demo-able state.
