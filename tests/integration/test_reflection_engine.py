"""
Integration tests for Reflection Engine.
"""

from core.execution_engine.models import ExecutionReport
from core.reflection_engine.engine import ReflectionEngine
from core.verification_engine.models import (
    VerificationCheck,
    VerificationReport,
)


def create_execution_report():
    return ExecutionReport(
        project_name="AI-OS",
        total_tasks=1,
        completed=1,
        failed=0,
        results=[],
    )


def create_verification_report():
    check = VerificationCheck(
        name="pytest",
        success=True,
        duration=1.25,
        message="All tests passed.",
    )

    return VerificationReport(
        project_name="AI-OS",
        total_checks=1,
        passed=1,
        failed=0,
        results=[check],
    )


def test_reflection_engine_runs(tmp_path):
    engine = ReflectionEngine(tmp_path)

    report = engine.run(
        create_execution_report(),
        create_verification_report(),
    )

    assert report.summary == "Reflection completed successfully."


def test_reflection_creates_reports(tmp_path):
    engine = ReflectionEngine(tmp_path)

    engine.run(
        create_execution_report(),
        create_verification_report(),
    )

    report_dir = (
        tmp_path
        / "reflection"
    )

    assert (
        report_dir
        / "reflection.json"
    ).exists()

    assert (
        report_dir
        / "reflection.md"
    ).exists()


def test_reflection_score_created(tmp_path):
    engine = ReflectionEngine(tmp_path)

    report = engine.run(
        create_execution_report(),
        create_verification_report(),
    )

    assert report.score is not None
    assert report.score.overall_score >= 0


def test_reflection_recommendations_created(tmp_path):
    engine = ReflectionEngine(tmp_path)

    report = engine.run(
        create_execution_report(),
        create_verification_report(),
    )

    assert isinstance(
        report.recommendations,
        list,
    )