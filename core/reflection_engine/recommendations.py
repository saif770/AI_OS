"""
Reflection Engine recommendations.

Produces deterministic recommendations based on analysis results.
"""

from __future__ import annotations

from .models import AnalysisResult, Recommendation


class RecommendationGenerator:
    """
    Rule-based recommendation engine.
    """

    def generate(
        self,
        analysis: AnalysisResult,
    ) -> list[Recommendation]:

        recommendations: list[Recommendation] = []

        if analysis.tasks_failed:
            recommendations.append(
                Recommendation(
                    title="Reduce Execution Failures",
                    description=(
                        "Investigate failed execution tasks "
                        "before adding new work."
                    ),
                    priority="High",
                )
            )

        if analysis.verification_failed_checks:
            recommendations.append(
                Recommendation(
                    title="Improve Verification",
                    description=(
                        "Resolve verification failures before "
                        "starting another iteration."
                    ),
                    priority="High",
                )
            )

        if analysis.completion_rate() < 80:
            recommendations.append(
                Recommendation(
                    title="Reduce Iteration Scope",
                    description=(
                        "Smaller execution batches usually "
                        "improve completion rate."
                    ),
                    priority="Medium",
                )
            )

        if (
            analysis.tasks_failed == 0
            and analysis.verification_failed_checks == 0
        ):
            recommendations.append(
                Recommendation(
                    title="Maintain Current Quality",
                    description=(
                        "Execution and verification completed "
                        "successfully."
                    ),
                    priority="Low",
                )
            )

        return recommendations