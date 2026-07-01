"""
bootstrap/report.py

Generate the final bootstrap report.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .base import BootstrapStage
from .result import BootstrapResult


class ReportStage(BootstrapStage):
    """
    Generate bootstrap execution reports.
    """

    name = "Report"

    order = 90

    REPORT_DIR = ".bootstrap"

    REPORT_FILE = "report.json"

    def execute(self) -> BootstrapResult:

        result = BootstrapResult(self.name)

        report_directory = (
            self.context.project_root / self.REPORT_DIR
        )

        report_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        report_path = (
            report_directory / self.REPORT_FILE
        )

        execution = []

        successful = 0
        failed = 0
        warnings = 0
        errors = 0

        for stage in self.context.results:

            execution.append(stage.to_dict())

            if stage.success:
                successful += 1

            if stage.failed:
                failed += 1

            warnings += len(stage.warnings)

            errors += len(stage.errors)

        report = {
            "generated_at": datetime.now().isoformat(),
            "project": self.context.project_name,
            "version": self.context.version,
            "summary": {
                "total_stages": len(self.context.results),
                "successful": successful,
                "failed": failed,
                "warnings": warnings,
                "errors": errors,
                "ai_readiness": self.context.get(
                    "ai_readiness"
                ),
                "ai_status": self.context.get(
                    "ai_status"
                ),
            },
            "stages": execution,
        }

        with report_path.open(
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                report,
                f,
                indent=4,
            )

        result.update(
            report_file=str(report_path),
            stages=len(execution),
            successful=successful,
            failed=failed,
            warnings=warnings,
            errors=errors,
        )

        return result