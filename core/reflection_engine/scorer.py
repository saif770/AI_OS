"""
Reflection Engine scoring.

Converts analysis results into deterministic quality scores.
"""

from __future__ import annotations

from dataclasses import dataclass

from .models import AnalysisResult


@dataclass(slots=True)
class ReflectionScore:
    """
    Overall reflection quality score.
    """

    execution_score: float
    verification_score: float
    reliability_score: float
    overall_score: float


class ReflectionScorer:
    """
    Deterministic scoring engine.

    Weighting:

    Execution      40%
    Verification   40%
    Reliability    20%
    """

    EXECUTION_WEIGHT = 0.40
    VERIFICATION_WEIGHT = 0.40
    RELIABILITY_WEIGHT = 0.20

    def score(self, analysis: AnalysisResult) -> ReflectionScore:
        execution = analysis.completion_rate()

        verification = analysis.verification_success_rate

        reliability = 100.0

        if analysis.tasks_failed:
            reliability -= min(analysis.tasks_failed * 10, 50)

        if analysis.verification_failed_checks:
            reliability -= min(
                analysis.verification_failed_checks * 5,
                50,
            )

        reliability = max(0.0, reliability)

        overall = (
            execution * self.EXECUTION_WEIGHT
            + verification * self.VERIFICATION_WEIGHT
            + reliability * self.RELIABILITY_WEIGHT
        )

        return ReflectionScore(
            execution_score=round(execution, 2),
            verification_score=round(verification, 2),
            reliability_score=round(reliability, 2),
            overall_score=round(overall, 2),
        )