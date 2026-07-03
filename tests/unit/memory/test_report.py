"""
Unit tests for MemoryReportWriter.
"""

from datetime import datetime, timezone
import json

from core.memory.models import (
    MemoryEntry,
    MemoryHistory,
    MemoryReport,
)
from core.memory.report import MemoryReportWriter


def build_report() -> MemoryReport:
    history = MemoryHistory(
        entries=[
            MemoryEntry(
                iteration=1,
                timestamp=datetime.now(timezone.utc),
                reflection_summary="Reflection OK",
                improvement_summary="Improve tests",
                overall_score=95.5,
            )
        ]
    )

    return MemoryReport(
        history=history,
        saved=True,
        location="output/memory/history.json",
    )


def test_report_writer_creates_json(tmp_path):
    report = build_report()

    writer = MemoryReportWriter(tmp_path)

    writer.write(report)

    json_file = (
        tmp_path
        / "memory"
        / "memory.json"
    )

    assert json_file.exists()


def test_report_writer_creates_markdown(tmp_path):
    report = build_report()

    writer = MemoryReportWriter(tmp_path)

    writer.write(report)

    md_file = (
        tmp_path
        / "memory"
        / "memory.md"
    )

    assert md_file.exists()


def test_json_contents(tmp_path):
    report = build_report()

    writer = MemoryReportWriter(tmp_path)

    writer.write(report)

    json_file = (
        tmp_path
        / "memory"
        / "memory.json"
    )

    data = json.loads(
        json_file.read_text(
            encoding="utf-8"
        )
    )

    assert data["saved"] is True
    assert data["location"] == "output/memory/history.json"
    assert "history" in data


def test_markdown_contents(tmp_path):
    report = build_report()

    writer = MemoryReportWriter(tmp_path)

    writer.write(report)

    md_file = (
        tmp_path
        / "memory"
        / "memory.md"
    )

    content = md_file.read_text(
        encoding="utf-8"
    )

    assert "# Memory Report" in content
    assert "Saved: True" in content
    assert "Total Iterations: 1" in content
    assert "Latest Iteration: 1" in content