"""Basic unit tests for SQLBot utilities."""

import importlib
import os

import pytest

from sql_guard import is_safe_sql, guard_query
from llm_client import call_llm


def test_is_safe_sql() -> None:
    assert is_safe_sql("select * from users")
    assert is_safe_sql("SELECT name FROM employees where id = 1")
    assert not is_safe_sql("DROP TABLE users")
    assert not is_safe_sql("delete from accounts")
    assert not is_safe_sql("TrUnCaTe logs")


def test_guard_query() -> None:
    # Safe query should not raise
    guard_query("select * from items")
    # Dangerous query should raise
    with pytest.raises(ValueError):
        guard_query("update users set password='123'")


def test_call_llm_echo(monkeypatch: pytest.MonkeyPatch) -> None:
    """If no API key is set the LLM client should echo input."""
    # Remove API key if present
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    # Reload module to pick up env change
    mod = importlib.reload(importlib.import_module("llm_client"))
    response = mod.call_llm("hello")
    assert response.startswith("(echo)")