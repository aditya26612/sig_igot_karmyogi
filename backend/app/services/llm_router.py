# backend/app/services/llm_router.py
"""Generation chain (spec section 8): Groq (429-aware key rotation) -> Ollama -> None."""
import json
import logging
import time
from typing import Any, Dict, Optional

import httpx

from app.config import settings

logger = logging.getLogger(__name__)


def _sleep_ms(ms: float) -> None:
    time.sleep(ms / 1000.0)


def _build_groq_client(key: str):
    try:
        from groq import Groq
        return Groq(api_key=key, timeout=settings.GROQ_ASSISTANT_TIMEOUT_S)
    except Exception:
        return None


def _ollama_generate(system: str, user: str, max_tokens: int, temperature: float) -> Optional[str]:
    payload = {
        "model": settings.OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "stream": False,
        "options": {"temperature": temperature, "num_predict": max_tokens},
    }
    try:
        r = httpx.post(
            f"{settings.OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=settings.GROQ_QUIZ_TIMEOUT_S,
        )
        if r.status_code == 200:
            return r.json().get("message", {}).get("content")
    except Exception as e:
        logger.info(f"[rag] Ollama unavailable: {e}")
    return None


def generate(
    system: str,
    user: str,
    max_tokens: int,
    temperature: float = 0.3,
    json_mode: bool = False,
    timeout: Optional[float] = None,
) -> Optional[str]:
    keys = settings.groq_keys
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    for round_no in range(2):  # up to 2 sweeps over the key set
        for key in keys:
            client = _build_groq_client(key)
            if client is None:
                continue
            try:
                kwargs: Dict[str, Any] = {
                    "model": settings.GROQ_PRIMARY_MODEL,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }
                if timeout is not None:
                    kwargs["timeout"] = timeout
                if json_mode:
                    kwargs["response_format"] = {"type": "json_object"}
                completion = client.chat.completions.create(**kwargs)
                return completion.choices[0].message.content
            except Exception as e:
                status = getattr(e, "status_code", None)
                if status in (429, 500, 502, 503, 504):
                    _sleep_ms(500 * (2 ** round_no))
                    continue  # rotate to next key immediately
                logger.warning(f"[rag] Groq call failed: {e}")
                continue
    out = _ollama_generate(
        system=system,
        user=user,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    if out:
        return out
    return None


def parse_json_payload(raw: str) -> Optional[dict]:
    """Parses LLM JSON output; always returns {"questions": [...]} dict or None."""
    if not raw:
        return None
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:]
    brace, bracket = raw.find("{"), raw.find("[")
    candidates = [p for p in (brace, bracket) if p != -1]
    if not candidates:
        return None
    start = min(candidates)
    if raw[start] == "{":
        end = raw.rfind("}")
    else:
        end = raw.rfind("]")
    if end == -1 or end <= start:
        return None
    try:
        data = json.loads(raw[start:end + 1])
    except Exception:
        return None
    if isinstance(data, dict):
        if isinstance(data.get("questions"), list):
            return data
        return data  # caller treats non-questions dicts as invalid for quizzes
    if isinstance(data, list):
        return {"questions": data}
    return None
