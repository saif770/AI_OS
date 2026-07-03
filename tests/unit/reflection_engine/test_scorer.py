from core.reflection_engine.models import AnalysisResult
from core.reflection_engine.scorer import ReflectionScorer


def test_score_success():

    analysis = AnalysisResult(
        tasks_total=10,
        tasks_completed=10,
        tasks_failed=0,
        verification_success_rate=100.0,
        verification_failed_checks=0,
        overall_success=True,
    )

    score = ReflectionScorer().score(analysis)

    assert score.overall_score == 100.0


def test_score_with_failures():

    analysis = AnalysisResult(
        tasks_total=10,
        tasks_completed=8,
        tasks_failed=2,
        verification_success_rate=90.0,
        verification_failed_checks=2,
        overall_success=False,
    )

    score = ReflectionScorer().score(analysis)

    assert score.overall_score < 100
    assert score.reliability_score < 100