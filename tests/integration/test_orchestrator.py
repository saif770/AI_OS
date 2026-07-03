"""
Integration tests for the AI-OS Orchestrator.
"""

from core.orchestrator.engine import Orchestrator


def planning_step(context):
    return {
        "stage": "planning",
        "success": True,
    }


def execution_step(context):
    return {
        "stage": "execution",
        "success": True,
    }


def verification_step(context):
    return {
        "stage": "verification",
        "success": True,
    }


def failing_step(context):
    raise RuntimeError(
        "Pipeline failed."
    )


def test_orchestrator_runs_pipeline(tmp_path):
    orchestrator = Orchestrator(tmp_path)

    orchestrator.register_step(
        "planning_report",
        planning_step,
    )

    orchestrator.register_step(
        "execution_report",
        execution_step,
    )

    orchestrator.register_step(
        "verification_report",
        verification_step,
    )

    result = orchestrator.run()

    assert result.success

    assert result.completed_steps == [
        "planning_report",
        "execution_report",
        "verification_report",
    ]


def test_context_is_populated(tmp_path):
    orchestrator = Orchestrator(tmp_path)

    orchestrator.register_step(
        "planning_report",
        planning_step,
    )

    orchestrator.register_step(
        "execution_report",
        execution_step,
    )

    result = orchestrator.run()

    context = result.context

    assert context is not None

    assert context.planning_report["success"]

    assert context.execution_report["success"]


def test_pipeline_failure(tmp_path):
    orchestrator = Orchestrator(tmp_path)

    orchestrator.register_step(
        "planning_report",
        planning_step,
    )

    orchestrator.register_step(
        "execution_report",
        failing_step,
    )

    result = orchestrator.run()

    assert not result.success

    assert result.failed_step == (
        "execution_report"
    )

    assert result.completed_steps == [
        "planning_report"
    ]

    assert "Pipeline failed." in result.message


def test_orchestrator_creates_reports(tmp_path):
    orchestrator = Orchestrator(tmp_path)

    orchestrator.register_step(
        "planning_report",
        planning_step,
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


def test_duration_recorded(tmp_path):
    orchestrator = Orchestrator(tmp_path)

    orchestrator.register_step(
        "planning_report",
        planning_step,
    )

    result = orchestrator.run()

    assert result.duration_seconds >= 0.0


def test_project_root_preserved(tmp_path):
    orchestrator = Orchestrator(tmp_path)

    orchestrator.register_step(
        "planning_report",
        planning_step,
    )

    result = orchestrator.run()

    assert (
        result.context.project_root
        == str(tmp_path)
    )