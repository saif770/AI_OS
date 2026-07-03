"""
Memory System data models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List


@dataclass(slots=True)
class MemoryEntry:
    """
    Represents one completed AI_OS iteration.
    """

    iteration: int

    timestamp: datetime

    reflection_summary: str

    improvement_summary: str

    overall_score: float


@dataclass(slots=True)
class MemoryHistory:
    """
    Complete stored memory history.
    """

    entries: List[MemoryEntry] = field(default_factory=list)

    @property
    def latest(self) -> MemoryEntry | None:
        if not self.entries:
            return None
        return self.entries[-1]

    @property
    def count(self) -> int:
        return len(self.entries)


@dataclass(slots=True)
class MemoryReport:
    """
    Output produced by the Memory Engine.
    """

    history: MemoryHistory

    saved: bool

    location: str

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )