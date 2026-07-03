"""
Unit tests for Memory System models.
"""

from datetime import datetime, timezone

from core.memory.models import (
    MemoryEntry,
    MemoryHistory,
    MemoryReport,
)

from core.memory.history import HistoryManager


def test_memory_entry_creation():
    entry = MemoryEntry(
        iteration=1,
        timestamp=datetime.now(timezone.utc),
        reflection_summary="Reflection OK",
        improvement_summary="Improve tests",
        overall_score=92.5,
    )

    assert entry.iteration == 1
    assert entry.reflection_summary == "Reflection OK"
    assert entry.improvement_summary == "Improve tests"
    assert entry.overall_score == 92.5


def test_empty_history():
    history = MemoryHistory()

    manager = HistoryManager()

    assert history.entries == []
    assert history.latest is None
    assert history.count == 0
    assert manager.average_score(history) == 0.0


def test_history_latest():
    first = MemoryEntry(
        iteration=1,
        timestamp=datetime.now(timezone.utc),
        reflection_summary="A",
        improvement_summary="B",
        overall_score=80,
    )

    second = MemoryEntry(
        iteration=2,
        timestamp=datetime.now(timezone.utc),
        reflection_summary="C",
        improvement_summary="D",
        overall_score=95,
    )

    history = MemoryHistory(
        entries=[first, second]
    )

    assert history.count == 2
    assert history.latest == second


def test_average_score():
    history = MemoryHistory(
        entries=[
            MemoryEntry(
                1,
                datetime.now(timezone.utc),
                "A",
                "B",
                80,
            ),
            MemoryEntry(
                2,
                datetime.now(timezone.utc),
                "C",
                "D",
                100,
            ),
        ]
    )

    manager = HistoryManager()

    assert manager.average_score(history) == 90.0


def test_memory_report_creation():
    report = MemoryReport(
        history=MemoryHistory(),
        saved=True,
        location="output/memory/history.json",
    )

    assert report.saved is True
    assert report.location.endswith("history.json")
    assert report.history.count == 0