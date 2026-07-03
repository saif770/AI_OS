"""
Memory System report writer.

Generates human-readable and machine-readable
reports for the Memory System.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import MemoryReport


class MemoryReportWriter:
    """
    Writes Memory System reports.
    """

    OUTPUT_DIRECTORY = "memory"

    JSON_REPORT = "memory.json"

    MARKDOWN_REPORT = "memory.md"

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
        report: MemoryReport,
    ) -> None:
        """
        Write all Memory reports.
        """

        self._write_json(report)

        self._write_markdown(report)

    def _write_json(
        self,
        report: MemoryReport,
    ) -> None:

        output = (
            self.output_directory
            / self.JSON_REPORT
        )

        output.write_text(
            json.dumps(
                asdict(report),
                indent=2,
                default=str,
            ),
            encoding="utf-8",
        )

    def _write_markdown(
        self,
        report: MemoryReport,
    ) -> None:

        output = (
            self.output_directory
            / self.MARKDOWN_REPORT
        )

        history = report.history

        latest = history.latest

        latest_iteration = (
            latest.iteration
            if latest
            else "-"
        )

        latest_score = (
            latest.overall_score
            if latest
            else "-"
        )

        markdown = f"""# Memory Report

## Summary

Saved: {report.saved}

Location: {report.location}

## History

Total Iterations: {history.count}

Latest Iteration: {latest_iteration}

Latest Score: {latest_score}
"""

        output.write_text(
            markdown,
            encoding="utf-8",
        )