"""
Verification Engine orchestrator.

Coordinates all verification stages and produces a single report.
"""

from __future__ import annotations

from pathlib import Path

from .benchmark import BenchmarkRunner
from .compiler import Compiler
from .coverage import CoverageRunner
from .formatter import Formatter
from .linter import Linter
from .models import VerificationCheck, VerificationReport
from .report import ReportWriter
from .security import SecurityScanner
from .test_runner import TestRunner


class VerificationEngine:
    """Runs the complete verification pipeline."""

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)

        self.steps = [
            Compiler(),
            TestRunner(),
            Linter(),
            Formatter(),
            CoverageRunner(),
            SecurityScanner(),
            BenchmarkRunner(),
        ]

        self.report_writer = ReportWriter(
            self.project_root / "output"
        )

    def run(self) -> VerificationReport:
        checks: list[VerificationCheck] = []

        for step in self.steps:
            checks.append(step.run(self.project_root))

        report = VerificationReport(
            project_name=self.project_root.name,
            total_checks=len(checks),
            passed=sum(c.success for c in checks),
            failed=sum(not c.success for c in checks),
            results=checks,
        )

        self.report_writer.write_json(report)

        return report
