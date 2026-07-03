"""
Reflection Engine data models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List


@dataclass(slots=True)
class Recommendation:
    """
    Reflection recommendation.
    """

    title: str
    description: str
    priority: str = "Medium"


@dataclass(slots=True)
class AnalysisResult:
    """
    Deterministic analysis produced from execution
    and verification reports.
    """

    tasks_total: int
    tasks_completed: int
    tasks_failed: int

    verification_success_rate: float
    verification_failed_checks: int

    overall_success: bool

    def completion_rate(self) -> float:
        if self.tasks_total == 0:
            return 100.0

        return (
            self.tasks_completed
            / self.tasks_total
        ) * 100.0


@dataclass(slots=True)
class ReflectionScore:
    """
    Quality score for a completed iteration.
    """

    execution_score: float
    verification_score: float
    reliability_score: float
    overall_score: float


@dataclass(slots=True)
class ReflectionReport:
    """
    Final Reflection Engine output.
    """

    summary: str

    analysis: AnalysisResult

    score: ReflectionScore

    recommendations: List[Recommendation] = field(
        default_factory=list
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )

    @property
    def recommendation_count(self) -> int:
        return len(self.recommendations)