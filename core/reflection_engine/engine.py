"""
Reflection Engine.

Coordinates analysis, scoring,
recommendation generation and report writing.
"""

from __future__ import annotations

from pathlib import Path

from .analyzer import ReflectionAnalyzer
from .models import ReflectionReport
from .recommendations import RecommendationGenerator
from .report import ReflectionReportWriter
from .scorer import ReflectionScorer


class ReflectionEngine:
    """
    Reflection Engine orchestration.
    """

    def __init__(
        self,
        output_root: Path,
    ) -> None:

        self.analyzer = ReflectionAnalyzer()

        self.scorer = ReflectionScorer()

        self.recommendation_generator = (
            RecommendationGenerator()
        )

        self.writer = ReflectionReportWriter(
            output_root
        )

    def run(
        self,
        execution_report,
        verification_report,
    ) -> ReflectionReport:
        """
        Execute the complete
        Reflection Engine pipeline.
        """

        analysis = self.analyzer.analyze(
            execution_report,
            verification_report,
        )

        score = self.scorer.score(
            analysis,
        )

        recommendations = (
            self.recommendation_generator.generate(
                analysis,
            )
        )

        report = ReflectionReport(
            summary=(
                "Reflection completed successfully."
            ),
            analysis=analysis,
            score=score,
            recommendations=recommendations,
        )

        self.writer.write(report)

        return report