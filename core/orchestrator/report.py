"""
Orchestrator report writer.

Writes machine-readable and human-readable reports
for completed pipeline executions.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import PipelineResult


class OrchestratorReportWriter:
    """
    Writes Orchestrator reports.
    """

    OUTPUT_DIRECTORY = "orchestrator"

    JSON_REPORT = "orchestrator.json"

    MARKDOWN_REPORT = "orchestrator.md"

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
        result: PipelineResult,
    ) -> None:
        """
        Write all orchestrator reports.
        """

        self._write_json(result)

        self._write_markdown(result)

    def _write_json(
        self,
        result: PipelineResult,
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
        result: PipelineResult,
    ) -> None:

        output = (
            self.output_directory
            / self.MARKDOWN_REPORT
        )

        completed = "\n".join(
            f"- {step}"
            for step in result.completed_steps
        )

        if not completed:
            completed = "- None"

        markdown = f"""# AI-OS Orchestrator Report

## Status

Success: {result.success}

Message: {result.message}

Duration: {result.duration_seconds:.2f} seconds

## Completed Steps

{completed}

## Failed Step

{result.failed_step or "None"}
"""

        output.write_text(
            markdown,
            encoding="utf-8",
        )