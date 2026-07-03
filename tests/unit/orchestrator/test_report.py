"""
Unit tests for the Orchestrator report writer.
"""

from pathlib import Path
import json

from core.orchestrator.models import (
    PipelineContext,
    PipelineResult,
)
from core.orchestrator.report import (
    OrchestratorReportWriter,
)


def build_result() -> PipelineResult:
    context = PipelineContext(
        project_root="C:/AI-OS"
    )

    return PipelineResult(
        success=True,
        completed_steps=[
            "planning_report",
            "execution_report",
            "verification_report",
        ],
        message="Pipeline completed successfully.",
        duration_seconds=12.34,
        context=context,
    )


def test_report_writer_creates_json(tmp_path):
    writer = OrchestratorReportWriter(tmp_path)

    writer.write(build_result())

    report = (
        tmp_path
        / "orchestrator"
        / "orchestrator.json"
    )

    assert report.exists()


def test_report_writer_creates_markdown(tmp_path):
    writer = OrchestratorReportWriter(tmp_path)

    writer.write(build_result())

    report = (
        tmp_path
        / "orchestrator"
        / "orchestrator.md"
    )

    assert report.exists()


def test_json_contents(tmp_path):
    writer = OrchestratorReportWriter(tmp_path)

    writer.write(build_result())

    report = (
        tmp_path
        / "orchestrator"
        / "orchestrator.json"
    )

    data = json.loads(
        report.read_text(
            encoding="utf-8"
        )
    )

    assert data["success"] is True
    assert data["message"] == "Pipeline completed successfully."
    assert len(data["completed_steps"]) == 3


def test_markdown_contents(tmp_path):
    writer = OrchestratorReportWriter(tmp_path)

    writer.write(build_result())

    report = (
        tmp_path
        / "orchestrator"
        / "orchestrator.md"
    )

    text = report.read_text(
        encoding="utf-8"
    )

    assert "# AI-OS Orchestrator Report" in text
    assert "Pipeline completed successfully." in text
    assert "planning_report" in text
    assert "execution_report" in text
    assert "verification_report" in text


def test_failed_pipeline_report(tmp_path):
    context = PipelineContext(
        project_root="C:/AI-OS"
    )

    result = PipelineResult(
        success=False,
        completed_steps=[
            "planning_report",
        ],
        failed_step="execution_report",
        message="Execution failed.",
        context=context,
    )

    writer = OrchestratorReportWriter(tmp_path)

    writer.write(result)

    report = (
        tmp_path
        / "orchestrator"
        / "orchestrator.md"
    )

    text = report.read_text(
        encoding="utf-8"
    )

    assert "Execution failed." in text
    assert "execution_report" in text