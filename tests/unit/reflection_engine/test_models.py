from core.reflection_engine.models import (
    AnalysisResult,
    Recommendation,
    ReflectionReport,
    ReflectionScore,
)


def test_analysis_completion_rate():
    analysis = AnalysisResult(
        tasks_total=10,
        tasks_completed=8,
        tasks_failed=2,
        verification_success_rate=100.0,
        verification_failed_checks=0,
        overall_success=False,
    )

    assert analysis.completion_rate() == 80.0


def test_report_defaults():
    analysis = AnalysisResult(
        tasks_total=0,
        tasks_completed=0,
        tasks_failed=0,
        verification_success_rate=100.0,
        verification_failed_checks=0,
        overall_success=True,
    )

    score = ReflectionScore(
        execution_score=100.0,
        verification_score=100.0,
        reliability_score=100.0,
        overall_score=100.0,
    )

    report = ReflectionReport(
        summary="ok",
        analysis=analysis,
        score=score,
        recommendations=[
            Recommendation("A", "B")
        ],
    )

    assert report.recommendation_count == 1