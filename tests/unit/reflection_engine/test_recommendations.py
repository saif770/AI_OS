from core.reflection_engine.models import AnalysisResult
from core.reflection_engine.recommendations import (
    RecommendationGenerator,
)


def test_success_recommendation():

    analysis = AnalysisResult(
        tasks_total=5,
        tasks_completed=5,
        tasks_failed=0,
        verification_success_rate=100,
        verification_failed_checks=0,
        overall_success=True,
    )

    recommendations = RecommendationGenerator().generate(
        analysis,
    )

    assert len(recommendations) == 1
    assert recommendations[0].priority == "Low"


def test_failure_recommendations():

    analysis = AnalysisResult(
        tasks_total=5,
        tasks_completed=3,
        tasks_failed=2,
        verification_success_rate=80,
        verification_failed_checks=2,
        overall_success=False,
    )

    recommendations = RecommendationGenerator().generate(
        analysis,
    )

    assert len(recommendations) >= 2