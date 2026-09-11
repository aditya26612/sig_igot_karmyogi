# backend/tests/conftest.py
"""Shared test configuration: disables background quiz pre-warm for the suite.

Task 11 fix: prewarm daemon threads spawned by lesson-detail requests during
tests (test_module3, test_end_to_end_pipeline) hold a data/demo.sqlite
connection open for the whole job (up to ~25s with real model loads), which
(a) collides with test_module4's reset_database() unlink()/os.replace() on
Windows (PermissionError on an open target file), (b) adds one-time real
embedding (458MB) + reranker (2.2GB) model loads to suite runtime, and
(c) can persist QUIZ-AI-* rows into the shared demo DB.

The kill-switch is bound at Settings import time from PREWARM_ENABLED, so the
fixture flips the live singleton attribute instead of the environment. Any
test that needs prewarm active (test_practice_pregen.py) re-enables it at
function scope via monkeypatch, which restores this value afterwards.
"""
import pytest

from app.config import settings


@pytest.fixture(scope="session", autouse=True)
def _disable_prewarm():
    settings.PREWARM_ENABLED = False
    yield
    settings.PREWARM_ENABLED = True
