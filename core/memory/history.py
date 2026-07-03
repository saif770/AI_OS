"""
Memory System history management.

Provides high-level operations for manipulating
memory history independently of persistence.
"""

from __future__ import annotations

from .models import (
    MemoryEntry,
    MemoryHistory,
)


class HistoryManager:
    """
    Performs operations on MemoryHistory.
    """

    def append(
        self,
        history: MemoryHistory,
        entry: MemoryEntry,
    ) -> MemoryHistory:
        """
        Append a new memory entry.
        """

        history.entries.append(entry)

        return history

    def latest(
        self,
        history: MemoryHistory,
    ) -> MemoryEntry | None:
        """
        Return the newest entry.
        """

        if not history.entries:
            return None

        return history.entries[-1]

    def last(
        self,
        history: MemoryHistory,
        count: int,
    ) -> list[MemoryEntry]:
        """
        Return the most recent N entries.
        """

        if count <= 0:
            return []

        return history.entries[-count:]

    def count(
        self,
        history: MemoryHistory,
    ) -> int:
        """
        Total stored iterations.
        """

        return len(history.entries)

    def average_score(
        self,
        history: MemoryHistory,
    ) -> float:
        """
        Average overall score across all
        stored iterations.
        """

        if not history.entries:
            return 0.0

        total = sum(
            entry.overall_score
            for entry in history.entries
        )

        return round(
            total / len(history.entries),
            2,
        )