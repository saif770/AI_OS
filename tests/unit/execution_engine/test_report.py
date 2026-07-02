"""
Unit tests for the ReportWriter.
"""

from pathlib import Path
import json

from core.execution_engine.models import ExecutionReport
from core.execution_engine.report import ReportWriter


def test_write_json_report(tmp_path: Path):
    writer = ReportWriter(tmp_path)

    report = ExecutionReport(
        project_name="AI-OS",
        total_tasks=10,
        completed=8,
        failed=2,
    )

    output = writer.write_json(report)

    assert output.exists()

    data = json.loads(output.read_text(encoding="utf-8"))

    assert data["project_name"] == "AI-OS"
    assert data["total_tasks"] == 10
    assert data["completed"] == 8
    assert data["failed"] == 2
    assert "success_rate" in data


def test_success_rate():
    report = ExecutionReport(
        project_name="AI-OS",
        total_tasks=5,
        completed=4,
        failed=1,
    )

    assert report.success_rate == 80.0


