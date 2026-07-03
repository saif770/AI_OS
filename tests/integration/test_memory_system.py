"""
Integration tests for the Memory System.
"""

from core.execution_engine.models import ExecutionReport
from core.improvement_loop.engine import ImprovementEngine
from core.memory.engine import MemoryEngine
from core.reflection_engine.engine import ReflectionEngine
from core.verification_engine.models import (
    VerificationCheck,
    VerificationReport,
)


def create_execution_report() -> ExecutionReport:
    return ExecutionReport(
        project_name="AI-OS",
        total_tasks=1,
        completed=1,
        failed=0,
        results=[],
    )


def create_verification_report() -> VerificationReport:
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


def create_improvement_report(tmp_path):
    improvement = ImprovementEngine(tmp_path)

    return improvement.run(
        create_reflection_report(tmp_path),
    )


def test_memory_engine_runs(tmp_path):
    engine = MemoryEngine(tmp_path)

    report = engine.run(
        create_reflection_report(tmp_path),
        create_improvement_report(tmp_path),
    )

    assert report.saved
    assert report.history.count == 1
    assert report.history.latest is not None


def test_memory_creates_reports(tmp_path):
    engine = MemoryEngine(tmp_path)

    engine.run(
        create_reflection_report(tmp_path),
        create_improvement_report(tmp_path),
    )

    report_dir = (
        tmp_path
        / "memory"
    )

    assert (
        report_dir
        / "memory.json"
    ).exists()

    assert (
        report_dir
        / "memory.md"
    ).exists()


def test_memory_history_grows(tmp_path):
    engine = MemoryEngine(tmp_path)

    reflection = create_reflection_report(tmp_path)
    improvement = create_improvement_report(tmp_path)

    engine.run(
        reflection,
        improvement,
    )

    report = engine.run(
        reflection,
        improvement,
    )

    assert report.history.count == 2

    latest = report.history.latest

    assert latest is not None
    assert latest.iteration == 2


def test_memory_score_persisted(tmp_path):
    engine = MemoryEngine(tmp_path)

    reflection = create_reflection_report(tmp_path)
    improvement = create_improvement_report(tmp_path)

    report = engine.run(
        reflection,
        improvement,
    )

    latest = report.history.latest

    assert latest is not None
    assert (
        latest.overall_score
        == reflection.score.overall_score
    )


def test_memory_location_exists(tmp_path):
    engine = MemoryEngine(tmp_path)

    report = engine.run(
        create_reflection_report(tmp_path),
        create_improvement_report(tmp_path),
    )

    assert report.location != ""


def test_memory_iteration_numbers(tmp_path):
    engine = MemoryEngine(tmp_path)

    reflection = create_reflection_report(tmp_path)
    improvement = create_improvement_report(tmp_path)

    engine.run(
        reflection,
        improvement,
    )

    second = engine.run(
        reflection,
        improvement,
    )

    assert second.history.latest.iteration == 2


def test_memory_latest_entry_contains_summaries(tmp_path):
    engine = MemoryEngine(tmp_path)

    reflection = create_reflection_report(tmp_path)
    improvement = create_improvement_report(tmp_path)

    report = engine.run(
        reflection,
        improvement,
    )

    latest = report.history.latest

    assert latest is not None
    assert latest.reflection_summary == reflection.summary
    assert latest.improvement_summary == improvement.summary


def test_memory_saved_flag(tmp_path):
    engine = MemoryEngine(tmp_path)

    report = engine.run(
        create_reflection_report(tmp_path),
        create_improvement_report(tmp_path),
    )

    assert report.saved is True