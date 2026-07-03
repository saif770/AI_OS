"""
Runtime report writer.

Writes machine-readable and human-readable reports
for Runtime Engine executions.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import RuntimeResult


class RuntimeReportWriter:
    """
    Writes Runtime reports.
    """

    OUTPUT_DIRECTORY = "runtime"

    JSON_REPORT = "runtime.json"

    MARKDOWN_REPORT = "runtime.md"

    def __init__(
        self,
        output_root: Path,
    ) -> None:

        self.output_directory = (
            Path(output_root)
            / self.OUTPUT_DIRECTORY
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def write(
        self,
        result: RuntimeResult,
    ) -> None:
        """
        Write all Runtime reports.
        """

        self._write_json(result)

        self._write_markdown(result)

    def _write_json(
        self,
        result: RuntimeResult,
    ) -> None:

        output = (
            self.output_directory
            / self.JSON_REPORT
        )

        output.write_text(
            json.dumps(
                asdict(result),
                indent=2,
                default=str,
            ),
            encoding="utf-8",
        )

    def _write_markdown(
        self,
        result: RuntimeResult,
    ) -> None:

        output = (
            self.output_directory
            / self.MARKDOWN_REPORT
        )

        markdown = f"""# AI-OS Runtime Report

## Status

Success: {result.success}

Iterations Completed: {result.iterations_completed}

Stopped Reason: {result.stopped_reason}

Duration: {result.duration_seconds:.2f} seconds
"""

        output.write_text(
            markdown,
            encoding="utf-8",
        )