"""
Verification report writer.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import UTC, datetime
import json
from pathlib import Path

from .models import VerificationReport


class ReportWriter:
    """Writes verification reports."""

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)

    def write_json(self, report: VerificationReport) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        output = self.output_dir / "verification_report.json"

        payload = {
            "generated_at": datetime.now(UTC).isoformat(),
            **asdict(report),
            "success_rate": report.success_rate,
        }

        output.write_text(
            json.dumps(payload, indent=4, default=str),
            encoding="utf-8",
        )

        return output
