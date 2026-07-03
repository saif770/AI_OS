"""
Unit tests for the Runtime report writer.
"""

import json

from core.runtime.models import (
    RuntimeContext,
    RuntimeResult,
)
from core.runtime.report import RuntimeReportWriter


def build_result() -> RuntimeResult:
    context = RuntimeContext(
        project_root="C:/AI-OS",
    )

    return RuntimeResult(
        success=True,
        iterations_completed=2,
        stopped_reason="Maximum iterations reached.",
        duration_seconds=5.25,
        context=context,
    )


def test_report_writer_creates_json(tmp_path):
    writer = RuntimeReportWriter(tmp_path)

    writer.write(build_result())

    report = (
        tmp_path
        / "runtime"
        / "runtime.json"
    )

    assert report.exists()


def test_report_writer_creates_markdown(tmp_path):
    writer = RuntimeReportWriter(tmp_path)

    writer.write(build_result())

    report = (
        tmp_path
        / "runtime"
        / "runtime.md"
    )

    assert report.exists()


def test_json_contents(tmp_path):
    writer = RuntimeReportWriter(tmp_path)

    writer.write(build_result())

    report = (
        tmp_path
        / "runtime"
        / "runtime.json"
    )

    data = json.loads(
        report.read_text(
            encoding="utf-8"
        )
    )

    assert data["success"] is True
    assert data["iterations_completed"] == 2
    assert data["stopped_reason"] == "Maximum iterations reached."


def test_markdown_contents(tmp_path):
    writer = RuntimeReportWriter(tmp_path)

    writer.write(build_result())

    report = (
        tmp_path
        / "runtime"
        / "runtime.md"
    )

    text = report.read_text(
        encoding="utf-8"
    )

    assert "# AI-OS Runtime Report" in text
    assert "Success: True" in text
    assert "Iterations Completed: 2" in text
    assert "Maximum iterations reached." in text


def test_failed_runtime_report(tmp_path):
    context = RuntimeContext(
        project_root="C:/AI-OS",
    )

    result = RuntimeResult(
        success=False,
        iterations_completed=1,
        stopped_reason="Pipeline execution failed.",
        context=context,
    )

    writer = RuntimeReportWriter(tmp_path)

    writer.write(result)

    report = (
        tmp_path
        / "runtime"
        / "runtime.md"
    )

    text = report.read_text(
        encoding="utf-8"
    )

    assert "Success: False" in text
    assert "Pipeline execution failed." in text