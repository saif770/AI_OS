"""
Integration tests for the Improvement Loop.
"""

from core.execution_engine.models import ExecutionReport
from core.improvement_loop.engine import ImprovementEngine
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
        duration=1.20,
        message="All tests passed.",
    )

    return VerificationReport(
        project_name="AI-OS",
        total_checks=1,
        passed=1,
        failed=0,
        results=[check],
    )


def create_reflection_report(tmp_path):
    reflection = ReflectionEngine(tmp_path)

    return reflection.run(
        create_execution_report(),
        create_verification_report(),
    )


def test_improvement_engine_runs(tmp_path):
    engine = ImprovementEngine(tmp_path)

    report = engine.run(
        create_reflection_report(tmp_path),
    )

    assert report.summary == "Improvement analysis completed."


def test_improvement_creates_reports(tmp_path):
    engine = ImprovementEngine(tmp_path)

    engine.run(
        create_reflection_report(tmp_path),
    )

    report_dir = (
        tmp_path
        / "improvement"
    )

    assert (
        report_dir
        / "improvement.json"
    ).exists()

    assert (
        report_dir
        / "improvement.md"
    ).exists()


def test_improvement_plan_created(tmp_path):
    engine = ImprovementEngine(tmp_path)

    report = engine.run(
        create_reflection_report(tmp_path),
    )

    assert report.plan is not None


def test_improvement_recommendations_created(tmp_path):
    engine = ImprovementEngine(tmp_path)

    report = engine.run(
        create_reflection_report(tmp_path),
    )

    assert isinstance(
        report.recommendations,
        list,
    )


def test_improvement_priority_exists(tmp_path):
    engine = ImprovementEngine(tmp_path)

    report = engine.run(
        create_reflection_report(tmp_path),
    )

    assert report.overall_priority != ""