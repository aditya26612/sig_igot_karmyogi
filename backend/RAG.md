# RAG Stack — Operator Guide

Retrieval-augmented generation for SkillBridge: overlapping chunking → FTS5 + embedding
hybrid retrieval → RRF fusion → cross-encoder reranking → grounded generation with
semantic validation. Every stage degrades gracefully; the platform is fully usable
with nothing installed beyond `requirements.txt`.

## Quickstart

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000
```

First use of semantic search / reranking downloads the HuggingFace models once:

- Embedding model (`paraphrase-multilingual-MiniLM-L12-v2`): ~470 MB download.
- Reranker (`BAAI/bge-reranker-v2-m3`, 568M params): ~2.2 GB on disk after download
  (fp32 weights). The first retrieval request pays this one-time cost; until then the
  system runs FTS5-only and logs `[rag] reranker unavailable ... Using RRF order.`
- Until models are cached, run with network available; afterwards everything works
  offline (FTS5 legs need nothing).

Optional local LLM fallback chain (no Groq keys → Ollama):

```bash
ollama pull qwen2.5:1.5b
```

## Ingestion

```bash
cd backend
python -m scripts.ingest_transcripts                 # all lessons
python -m scripts.ingest_transcripts --lesson <id>   # one lesson
python -m scripts.ingest_transcripts --refetch       # ignore raw cache, re-fetch
python -m scripts.ingest_transcripts --no-embed      # skip embedding writes
```

Semantics:

- **Resumable / idempotent:** a lesson with a FETCHED raw transcript row is never
  re-fetched; its cached text is re-chunked (status CACHED). `--refetch` overrides.
- **Rate-limit posture:** YouTube is fetched once per lesson, never on the request
  path, with 3–5 s jittered delays between lessons; the raw transcript is cached in
  `raw_transcripts` forever.
- **Failure isolation:** a failed fetch marks the lesson FAILED and moves on; the
  lesson keeps its seed chunks (ingestion replaces only `AUTO_CHUNK` rows).
- Embeddings are written per chunk into `chunk_embeddings` when the embedding model
  is available (`--no-embed` or model unavailable → SKIPPED/UNAVAILABLE, FTS5 still
  indexes the chunks).

## Configuration

| Env var | Default | Meaning |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://127.0.0.1:11434` | Ollama endpoint for the local LLM fallback leg |
| `OLLAMA_MODEL` | `qwen2.5:1.5b` | Model asked from Ollama when Groq is unavailable |
| `RAG_RERANKER_ENABLED` | `1` | Cross-encoder reranking on/off (`0` disables; pass-through RRF order is used) |
| `RAG_EMBEDDING_MODEL` | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | Embedding model for the semantic retrieval leg (multilingual: en + hi) |
| `RAG_RERANKER_MODEL` | `BAAI/bge-reranker-v2-m3` | Cross-encoder used to reorder fused candidates |
| `RAG_CHUNK_TARGET_CHARS` | `900` | Target chunk length in characters for the sliding-window chunker |
| `RAG_CHUNK_OVERLAP_CHARS` | `225` | Overlap between consecutive chunks (25% of target) |
| `GROQ_ASSISTANT_TIMEOUT_S` | `8` | Timeout per Groq call on the assistant path |
| `GROQ_QUIZ_TIMEOUT_S` | `20` | Timeout per Groq call on the quiz-generation path |
| `AI_PRESENTATION_DELAY_SECONDS` | `3` | Presentation delay gate before AI work starts (perceived-latency budget) |
| `PREWARM_ENABLED` | `1` | Background quiz pre-generation on lesson open (`0` = kill-switch; disabled automatically during tests) |

## Degradation Matrix

The platform is fully working at every rung (spec §12):

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

## Evaluation

```bash
cd backend
python -m tests.eval_retrieval
```

Runs a 24-item golden set (EN + HI queries, 2 per seeded chunk) through four
configs — `like` (legacy substring), `fts5` (BM25), `hybrid` (FTS5 + vector + RRF),
`hybrid+rerank` — and prints a judge-ready table:

- **hit@k** — fraction of queries whose expected chunk appears in the top-k results.
- **MRR** — mean reciprocal rank (1.0 = expected chunk always ranked first).

**Regression guard:** exit code 1 if `hybrid` hit@5 drops below the `like` baseline.
Reference run on the seeded curriculum: LIKE 0.96 hit@5 → FTS5 1.00 → hybrid 1.00 →
hybrid+rerank 1.00 hit@1 / 1.00 MRR.

## Hardware Guidance

- Embeddings and FTS5 run comfortably on CPU; no GPU required for retrieval.
- The reranker tries CUDA first, then falls back to CPU automatically.
- 4 GB-VRAM laptops are fine: models are small (MiniLM ~120M params; reranker 568M).
- With no GPU, the first reranker-scoring request is CPU-slow (~seconds for a
  handful of candidates) — subsequent requests reuse the loaded model.
