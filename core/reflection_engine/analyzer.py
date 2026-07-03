from __future__ import annotations

from .models import AnalysisResult

class ReflectionAnalyzer:
    """Deterministic analyzer for execution and verification reports."""

    def analyze(self, execution_report, verification_report) -> AnalysisResult:
        tasks_total = getattr(execution_report, "tasks_total", 0)
        tasks_completed = getattr(execution_report, "tasks_completed", 0)
        tasks_failed = getattr(execution_report, "tasks_failed", 0)
        success_rate = getattr(verification_report, "success_rate", 0.0)
        failed_checks = len(getattr(verification_report, "failed_checks", []))
        overall_success = (
            tasks_failed == 0 and failed_checks == 0 and success_rate >= 100.0
        )
        return AnalysisResult(
            tasks_total=tasks_total,
            tasks_completed=tasks_completed,
            tasks_failed=tasks_failed,
            verification_success_rate=success_rate,
            verification_failed_checks=failed_checks,
            overall_success=overall_success,
        )
