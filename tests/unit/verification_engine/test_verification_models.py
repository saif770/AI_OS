"""
Unit tests for verification_engine.models.
"""

from pathlib import Path

from core.verification_engine.models import (
    VerificationCheck,
    VerificationReport,
    VerificationResult,
)


def test_verification_check():
    check = VerificationCheck(
        name="compiler",
        success=True,
        duration=1.23,
        message="OK",
    )

    assert check.name == "compiler"
    assert check.success
    assert check.duration == 1.23


def test_verification_result():
    result = VerificationResult(
        project_root=Path("."),
    )

    result.checks.append(
        VerificationCheck(
            name="tests",
            success=True,
        )
    )

    assert result.passed
    assert len(result.failed_checks) == 0


def test_verification_report():
    report = VerificationReport(
        project_name="AI-OS",
        total_checks=5,
        passed=4,
        failed=1,
    )

    assert report.success_rate == 80.0
