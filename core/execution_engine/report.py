"""
Reporting utilities for the AI_OS Execution Engine.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, UTC, UTC
from pathlib import Path
import json

from .models import ExecutionReport


@dataclass(slots=True)
class ReportWriter:
    """
    Writes execution reports to disk.
    """

    output_dir: Path

    def write_json(self, report: ExecutionReport) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        output = self.output_dir / "execution_report.json"

        payload = {
            "project_name": report.project_name,
            "total_tasks": report.total_tasks,
            "completed": report.completed,
            "failed": report.failed,
            "success_rate": report.success_rate,
            "generated_at": datetime.now(UTC).isoformat(),
        }

        output.write_text(
            json.dumps(payload, indent=4),
            encoding="utf-8",
        )

        return output


