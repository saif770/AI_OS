"""
Unit tests for HistoryManager.
"""

from datetime import datetime, timezone

from core.memory.history import HistoryManager
from core.memory.models import (
    MemoryEntry,
    MemoryHistory,
)


def create_entry(
    iteration: int,
    score: float,
) -> MemoryEntry:
    return MemoryEntry(
        iteration=iteration,
        timestamp=datetime.now(timezone.utc),
        reflection_summary=f"Reflection {iteration}",
        improvement_summary=f"Improvement {iteration}",
        overall_score=score,
    )


def test_append_entry():
    manager = HistoryManager()

    history = MemoryHistory()

    entry = create_entry(1, 90.0)

    result = manager.append(history, entry)

    assert result.count == 1
    assert result.latest == entry


def test_latest_entry():
    manager = HistoryManager()

    history = MemoryHistory(
        entries=[
            create_entry(1, 80),
            create_entry(2, 90),
            create_entry(3, 95),
        ]
    )

    latest = manager.latest(history)

    assert latest is not None
    assert latest.iteration == 3


def test_last_entries():
    manager = HistoryManager()

    history = MemoryHistory(
        entries=[
            create_entry(1, 70),
            create_entry(2, 75),
            create_entry(3, 80),
            create_entry(4, 85),
            create_entry(5, 90),
        ]
    )

    last_two = manager.last(history, 2)

    assert len(last_two) == 2
    assert last_two[0].iteration == 4
    assert last_two[1].iteration == 5


def test_last_zero():
    manager = HistoryManager()

    history = MemoryHistory(
        entries=[
            create_entry(1, 90),
        ]
    )

    assert manager.last(history, 0) == []


def test_count():
    manager = HistoryManager()

    history = MemoryHistory(
        entries=[
            create_entry(1, 80),
            create_entry(2, 90),
            create_entry(3, 95),
        ]
    )

    assert manager.count(history) == 3


def test_average_score():
    manager = HistoryManager()

    history = MemoryHistory(
        entries=[
            create_entry(1, 80),
            create_entry(2, 90),
            create_entry(3, 100),
        ]
    )

    assert manager.average_score(history) == 90.0


def test_average_score_empty():
    manager = HistoryManager()

    history = MemoryHistory()

    assert manager.average_score(history) == 0.0