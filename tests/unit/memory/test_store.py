"""
Unit tests for MemoryStore.
"""

from datetime import datetime, timezone

from core.memory.models import (
    MemoryEntry,
    MemoryHistory,
)
from core.memory.store import MemoryStore


def test_store_initially_empty(tmp_path):
    store = MemoryStore(tmp_path)

    assert store.exists() is False

    history = store.load()

    assert history.count == 0


def test_save_creates_file(tmp_path):
    store = MemoryStore(tmp_path)

    history = MemoryHistory(
        entries=[
            MemoryEntry(
                iteration=1,
                timestamp=datetime.now(timezone.utc),
                reflection_summary="Reflection",
                improvement_summary="Improvement",
                overall_score=95.0,
            )
        ]
    )

    store.save(history)

    assert store.exists()


def test_save_and_load_round_trip(tmp_path):
    store = MemoryStore(tmp_path)

    original = MemoryHistory(
        entries=[
            MemoryEntry(
                iteration=1,
                timestamp=datetime.now(timezone.utc),
                reflection_summary="Reflection",
                improvement_summary="Improvement",
                overall_score=91.5,
            )
        ]
    )

    store.save(original)

    loaded = store.load()

    assert loaded.count == 1

    entry = loaded.latest

    assert entry is not None
    assert entry.iteration == 1
    assert entry.reflection_summary == "Reflection"
    assert entry.improvement_summary == "Improvement"
    assert entry.overall_score == 91.5


def test_clear_removes_history(tmp_path):
    store = MemoryStore(tmp_path)

    history = MemoryHistory(
        entries=[
            MemoryEntry(
                iteration=1,
                timestamp=datetime.now(timezone.utc),
                reflection_summary="A",
                improvement_summary="B",
                overall_score=100.0,
            )
        ]
    )

    store.save(history)

    assert store.exists()

    store.clear()

    assert not store.exists()


def test_load_missing_history_returns_empty(tmp_path):
    store = MemoryStore(tmp_path)

    history = store.load()

    assert history.count == 0
    assert history.entries == []