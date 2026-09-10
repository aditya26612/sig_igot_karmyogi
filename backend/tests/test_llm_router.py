# backend/tests/test_llm_router.py
import pytest
from app.config import Settings
from app.services import llm_router
from app.services.llm_router import generate, parse_json_payload


def _fake_groq_keys(monkeypatch, keys):
    """Patch the read-only `groq_keys` property on the Settings class.

    `groq_keys` is a @property without a setter, so instance-level
    monkeypatch.setattr raises AttributeError. Replacing the class
    property keeps `settings.groq_keys` reads working everywhere.
    """
    monkeypatch.setattr(
        Settings, "groq_keys", property(lambda self: list(keys))
    )


class FakeCompletions:
    def __init__(self, script):
        self.script = script  # list of ("ok", content) or (status_code, message)
        self.calls = 0

    def create(self, **kwargs):
        status, payload = self.script[min(self.calls, len(self.script) - 1)]
        self.calls += 1
        if status == "ok":
            message = type("M", (), {"content": payload})()
            choice = type("Ch", (), {"message": message})()
            return type("C", (), {"choices": [choice]})()
        err = Exception(payload)
        err.status_code = status
        raise err


class FakeClient:
    def __init__(self, script):
        self.chat = type("Chat", (), {"completions": FakeCompletions(script)})()


def test_parse_json_payload_variants():
    assert parse_json_payload('{"questions": [1, 2]}') == {"questions": [1, 2]}
    assert parse_json_payload('[1, 2]') == {"questions": [1, 2]}
    assert parse_json_payload('```json\n{"questions": [1]}\n```') == {"questions": [1]}
    assert parse_json_payload('noise before {"questions": [3]} noise after') == {"questions": [3]}
    assert parse_json_payload("no json here") is None


def test_generate_rotates_to_next_key_on_429(monkeypatch):
    ok_client = FakeClient([("ok", '{"questions": [{"a": 1}]}')])
    bad_client = FakeClient([(429, "rate limited")])
    clients = [bad_client, ok_client]
    monkeypatch.setattr(llm_router, "_build_groq_client", lambda key: clients.pop(0))
    monkeypatch.setattr(llm_router, "_sleep_ms", lambda ms: None)
    _fake_groq_keys(monkeypatch, ["k1", "k2"])
    out = generate("sys", "usr", max_tokens=100, json_mode=True)
    assert out == '{"questions": [{"a": 1}]}'


def test_generate_returns_none_when_everything_fails(monkeypatch):
    bad_client = FakeClient([(429, "rl")])
    monkeypatch.setattr(llm_router, "_build_groq_client", lambda key: bad_client)
    monkeypatch.setattr(llm_router, "_sleep_ms", lambda ms: None)
    _fake_groq_keys(monkeypatch, ["k1", "k2"])
    monkeypatch.setattr(llm_router, "_ollama_generate", lambda **kw: None)
    assert generate("sys", "usr", max_tokens=100) is None


def test_generate_falls_back_to_ollama(monkeypatch):
    bad_client = FakeClient([(429, "rl")])
    monkeypatch.setattr(llm_router, "_build_groq_client", lambda key: bad_client)
    monkeypatch.setattr(llm_router, "_sleep_ms", lambda ms: None)
    _fake_groq_keys(monkeypatch, ["k1"])
    monkeypatch.setattr(llm_router, "_ollama_generate",
                        lambda **kw: "ollama answer")
    assert generate("sys", "usr", max_tokens=100) == "ollama answer"
