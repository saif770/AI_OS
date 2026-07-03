from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

class ReflectionReportWriter:
    """Writes reflection reports to disk."""

    def __init__(self, output_root: Path):
        self.output_dir = Path(output_root) / "reflection"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write(self, report) -> None:
        data = asdict(report)
        (self.output_dir / "reflection.json").write_text(
            json.dumps(data, indent=2, default=str),
            encoding="utf-8",
        )
        (self.output_dir / "reflection.md").write_text(
            f"# Reflection Report\n\n{report.summary}\n",
            encoding="utf-8",
        )
