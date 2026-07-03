"""
Unit tests for the AI-OS Orchestrator.
"""

from core.orchestrator.engine import Orchestrator


def successful_step(context):
    return {"status": "ok"}


def failing_step(context):
    raise RuntimeError("Pipeline failed")


def test_empty_pipeline(tmp_path):
    orchestrator = Orchestrator(tmp_path)

    result = orchestrator.run()

    assert result.success
    assert result.completed_steps == []
    assert result.failed_step is None
    assert result.context is not None


def test_single_step(tmp_path):
    orchestrator = Orchestrator(tmp_path)

    orchestrator.register_step(
        "planning_report",
        successful_step,
    )

    result = orchestrator.run()

    assert result.success
    assert result.completed_steps == [
        "planning_report"
    ]

    assert result.context.planning_report == {
        "status": "ok"
    }


def test_multiple_steps(tmp_path):
    orchestrator = Orchestrator(tmp_path)

    orchestrator.register_step(
        "planning_report",
        successful_step,
    )

    orchestrator.register_step(
        "execution_report",
        successful_step,
    )

    orchestrator.register_step(
        "verification_report",
        successful_step,
    )

    result = orchestrator.run()

    assert result.success

    assert result.completed_steps == [
        "planning_report",
        "execution_report",
        "verification_report",
    ]

    assert result.context.planning_report is not None
    assert result.context.execution_report is not None
    assert result.context.verification_report is not None


def test_pipeline_failure(tmp_path):
    orchestrator = Orchestrator(tmp_path)

    orchestrator.register_step(
        "planning_report",
        successful_step,
    )

    orchestrator.register_step(
        "execution_report",
        failing_step,
    )

    orchestrator.register_step(
        "verification_report",
        successful_step,
    )

    result = orchestrator.run()

    assert not result.success

    assert result.failed_step == "execution_report"

    assert result.completed_steps == [
        "planning_report"
    ]

    assert "Pipeline failed" in result.message


def test_reports_created(tmp_path):
    orchestrator = Orchestrator(tmp_path)

    orchestrator.register_step(
        "planning_report",
        successful_step,
    )

    orchestrator.run()

    report_dir = (
        tmp_path
        / "output"
        / "orchestrator"
    )

    assert (
        report_dir
        / "orchestrator.json"
    ).exists()

    assert (
        report_dir
        / "orchestrator.md"
    ).exists()


def test_execution_duration(tmp_path):
    orchestrator = Orchestrator(tmp_path)

    orchestrator.register_step(
        "planning_report",
        successful_step,
    )

    result = orchestrator.run()

    assert result.duration_seconds >= 0.0


def test_context_preserved(tmp_path):
    orchestrator = Orchestrator(tmp_path)

    orchestrator.register_step(
        "planning_report",
        successful_step,
    )

    result = orchestrator.run()

    assert result.context is not None
    assert result.context.project_root == str(tmp_path)


def test_pipeline_names_match(tmp_path):
    orchestrator = Orchestrator(tmp_path)

    orchestrator.register_step(
        "planning_report",
        successful_step,
    )

    orchestrator.register_step(
        "execution_report",
        successful_step,
    )

    assert orchestrator.pipeline.names() == [
        "planning_report",
        "execution_report",
    ]