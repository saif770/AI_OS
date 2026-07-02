"""
Unit tests for the Verification Engine report writer.
"""

from pathlib import Path
import json

from core.verification_engine.models import (
    VerificationCheck,
    VerificationReport,
)
from core.verification_engine.report import ReportWriter


def test_write_verification_report(tmp_path: Path):
    writer = ReportWriter(tmp_path)

    report = VerificationReport(
        project_name="AI-OS",
        total_checks=2,
        passed=2,
        failed=0,
        results=[
            VerificationCheck(
                name="compiler",
                success=True,
            ),
            VerificationCheck(
                name="tests",
                success=True,
            ),
        ],
    )

    output = writer.write_json(report)

    assert output.exists()

    data = json.loads(output.read_text(encoding="utf-8"))

    assert data["project_name"] == "AI-OS"
    assert data["total_checks"] == 2
    assert data["passed"] == 2
    assert data["failed"] == 0
    assert "generated_at" in data
    assert "success_rate" in data


def test_success_rate():
    report = VerificationReport(
        project_name="AI-OS",
        total_checks=4,
        passed=3,
        failed=1,
    )

    assert report.success_rate == 75.0
