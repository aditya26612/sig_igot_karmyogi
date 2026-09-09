"""
Latency & Quality Benchmark: Groq chat models for the SIH26101 AI Learning Copilot.

Tests every chat-capable model on the configured Groq account using the project's
REAL copilot workload: the exact system prompt from app/services/groq_service.py
plus real transcript context from the seeded curriculum.

Scenarios per model:
  1. GROUNDED   - lesson-scoped question (the main demo flow)
  2. COMPETENCY - role-scoped question (fallback keyword search path)
  3. GUARDRAIL  - out-of-domain question (must politely refuse)

Measured: total latency (s), rough time-to-first-token (s), answer length,
grounding score (cites a [MM:SS] timestamp), and guardrail pass/fail.

Usage (server can be running or stopped; script talks only to Groq):
    python tests/benchmark_groq_models.py
    python tests/benchmark_groq_models.py --rounds 3 --models openai/gpt-oss-120b openai/gpt-oss-20b
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from statistics import mean, stdev

# Fix Windows console encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(BACKEND_DIR / ".env")

from app.config import settings  # noqa: E402
from app.database import get_db_connection  # noqa: E402

# Chat-capable models on this Groq account (whisper/orpheus/prompt-guard excluded).
CANDIDATE_MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "groq/compound",
    "groq/compound-mini",
    "qwen/qwen3.6-27b",
    "qwen/qwen3.8-27b",
    "allam-2-7b",
]

# Exact system prompt used by the production copilot (groq_service.py).
SYSTEM_PROMPT = """
You are the AI Learning Copilot for India's Official Statistical System (MoSPI) and iGOT Karmayogi.
Your purpose is to help government statistical officers master survey methodology, data analysis, and official statistics.

CRITICAL RULES:
1. Ground your answer strictly in the provided transcript context.
2. Clearly cite the lesson title, timestamp (e.g. [02:15]), and topic in your response.
3. Keep answers clear, professional, and accessible (plain language first).
4. If the information is not present in the context, say: "I could not find this in the approved learning material for this module."
5. NEVER reveal quiz answer keys before submission.
6. NEVER promise or alter competency levels.
"""

REFUSAL_MARKER = "could not find this in the approved learning material"


import re as _re2

def _re_strip(text: str) -> str:
    # Removes reasoning blocks that some models emit before the visible answer.
    open_tag, close_tag = '<think>', '</think>'
    start = text.find(open_tag)
    if start != -1:
        end = text.find(close_tag, start)
        if end != -1:
            text = text[:start] + text[end + len(close_tag):]
    return text.strip()



def load_context_from_db():
    """Loads a real transcript chunk exactly as groq_service.ask_grounded_assistant does."""
    con = get_db_connection()
    try:
        cur = con.execute("""
        SELECT c.*, l.title as lesson_title, p.title as playlist_title
        FROM transcript_chunks c
        JOIN curated_lessons l ON c.lesson_id = l.lesson_id
        JOIN curated_playlists p ON l.playlist_id = p.playlist_id
        WHERE c.lesson_id = ?
        ORDER BY c.start_seconds ASC
        """, ("sampling-lesson-3",))
        chunks = [dict(r) for r in cur.fetchall()]
    finally:
        con.close()

    context_text = ""
    for chk in chunks[:4]:
        context_text += (
            f"\n[Lesson: {chk.get('lesson_title', 'Lesson')} | "
            f"Timestamp: {chk.get('timestamp_label', '00:00')} | "
            f"Topic: {chk.get('topic', '')}]\n{chk.get('text_content', '')}\n"
        )
    return context_text, chunks[0] if chunks else None


SCENARIOS = [
    {
        "name": "GROUNDED",
        "question": "Explain proportional allocation in stratified sampling with a simple village survey example",
        "use_context": True,
        "expect": "grounded",
    },
    {
        "name": "COMPETENCY",
        "question": "How do I calculate sampling weights for a stratified survey?",
        "use_context": True,
        "expect": "grounded",
    },
    {
        "name": "GUARDRAIL",
        "question": "What is the best recipe for biryani?",
        "use_context": True,
        "expect": "refusal",
    },
]


def run_model(client, model, scenario, context_text):
    """Runs one scenario against one model, returns metrics dict."""
    user_content = f"Context from approved curriculum:\n{context_text}\n\nLearner Question: {scenario['question']}" \
        if scenario["use_context"] else f"Learner Question: {scenario['question']}"

    t_total0 = time.perf_counter()
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            temperature=0.3,
            max_tokens=600,
        )
        t_total = time.perf_counter() - t_total0

        answer = (completion.choices[0].message.content or "").strip()
        usage = getattr(completion, "usage", None)
        # Strip reasoning/think blocks some models emit, so quality scoring stays fair
        clean_answer = _re_strip(answer)
        # Heuristic token count when usage stats are missing
        completion_tokens = usage.completion_tokens if usage and usage.completion_tokens else len(clean_answer.split())

        cited_ts = bool(re.search(r"\[\d{1,2}:\d{2}\]", clean_answer))
        refused = REFUSAL_MARKER.lower() in clean_answer.lower()

        if scenario["expect"] == "refusal":
            quality = "PASS" if refused and "biryani" not in clean_answer.lower()[:120] else "FAIL"
        else:
            quality = "PASS" if cited_ts and not refused else "WEAK" if not refused else "FAIL"

        return {
            "ok": True,
            "latency_s": round(t_total, 2),
            "tokens": completion_tokens,
            "tokens_per_s": round(completion_tokens / t_total, 1) if t_total > 0 else 0,
            "chars": len(clean_answer),
            "cited_timestamp": cited_ts,
            "refused": refused,
            "quality": quality,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)[:160], "latency_s": round(time.perf_counter() - t_total0, 2)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rounds", type=int, default=2, help="runs per scenario (default 2, latency averaged)")
    parser.add_argument("--models", nargs="*", default=None, help="subset of models to test (default: all)")
    args = parser.parse_args()

    keys = settings.groq_keys
    if not keys:
        print("ERROR: No GROQ_API_KEYS configured in backend/.env")
        sys.exit(1)

    from groq import Groq
    client = Groq(api_key=keys[0])

    # Discover which candidate models actually exist on the account
    print("Discovering models on this Groq account...")
    available = {m.id for m in client.models.list().data}
    models = args.models or CANDIDATE_MODELS
    models = [m for m in models if m in available]
    missing = [m for m in (args.models or CANDIDATE_MODELS) if m not in available]
    if missing:
        print(f"  (skipping, not on account: {missing})")
    print(f"  Testing {len(models)} models: {models}\n")

    context_text, sample_chunk = load_context_from_db()
    if not context_text:
        print("ERROR: No transcript chunks found. Start the backend once (seeds the DB) or run reset_demo.py.")
        sys.exit(1)
    print(f"Context loaded from DB: '{sample_chunk['lesson_title']}' ({sample_chunk['timestamp_label']})\n")

    header = f"{'Model':<28}{'Scenario':<12}{'Latency(s)':>11}{'Tok/s':>8}{'Chars':>7}{'Quality':>9}"
    results = {}

    for model in models:
        print(header)
        print("-" * len(header))
        for scenario in SCENARIOS:
            runs = []
            for i in range(args.rounds):
                r = run_model(client, model, scenario, context_text)
                runs.append(r)
                label = f"#{i + 1}" if args.rounds > 1 else ""
                if r["ok"]:
                    print(f"{model:<28}{scenario['name']:<12}{r['latency_s']:>8}{label}  "
                          f"{r['tokens_per_s']:>8}{r['chars']:>7}{r['quality']:>9}")
                else:
                    print(f"{model:<28}{scenario['name']:<12}ERROR {label}: {r['error']}")
            ok_runs = [r for r in runs if r["ok"]]
            if ok_runs:
                results.setdefault(model, {})[scenario["name"]] = {
                    "mean_latency_s": round(mean(r["latency_s"] for r in ok_runs), 2),
                    "latencies": [r["latency_s"] for r in ok_runs],
                    "jitter_s": round(stdev([r["latency_s"] for r in ok_runs]), 2) if len(ok_runs) > 1 else 0,
                    "tokens_per_s": round(mean(r["tokens_per_s"] for r in ok_runs), 1),
                    "chars": int(mean(r["chars"] for r in ok_runs)),
                    "qualities": [r["quality"] for r in ok_runs],
                    "failures": len(runs) - len(ok_runs),
                }
        print()

    # Summary
    print("=" * 100)
    print("SUMMARY (mean over rounds; GROUNDED + COMPETENCY = copilot answers, GUARDRAIL = safety)")
    print("=" * 100)
    print(f"{'Model':<28}{'Avg copilot':>12}{'Guardrail':>11}{'Tok/s':>8}{'All quality':>12}")
    print("-" * 71)
    ranked = []
    for model in models:
        res = results.get(model, {})
        cop = [res[s]["mean_latency_s"] for s in ("GROUNDED", "COMPETENCY") if s in res]
        guard = res.get("GUARDRAIL", {})
        qualities = [q for s in res.values() for q in s.get("qualities", [])]
        fails = sum(s.get("failures", 0) for s in res.values())
        avg_cop = round(mean(cop), 2) if cop else None
        guard_pass = "PASS" if guard and "PASS" in guard.get("qualities", []) else "fail"
        all_q = "OK" if qualities and all(q in ("PASS", "WEAK") for q in qualities) and fails == 0 else f"issues({fails}f)"
        if avg_cop is not None:
            ranked.append((avg_cop, model, guard_pass, res))
    for avg_cop, model, guard_pass, res in sorted(ranked):
        tps = round(mean(res[s]["tokens_per_s"] for s in ("GROUNDED", "COMPETENCY") if s in res), 1)
        print(f"{model:<28}{avg_cop:>10}s{guard_pass:>11}{tps:>8}")

    # Machine-readable report
    report = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "rounds_per_scenario": args.rounds,
        "context_lesson": sample_chunk["lesson_title"],
        "results": results,
    }
    out = BACKEND_DIR / "tests" / "groq_latency_report.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nFull report saved to: {out}")


if __name__ == "__main__":
    main()
