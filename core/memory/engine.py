"""
Memory System engine.

Coordinates persistence, history management,
and report generation for AI_OS memory.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .history import HistoryManager
from .models import (
    MemoryEntry,
    MemoryReport,
)
from .report import MemoryReportWriter
from .store import MemoryStore


class MemoryEngine:
    """
    Memory System orchestration.
    """

    def __init__(
        self,
        output_root: Path,
    ) -> None:

        self.store = MemoryStore(output_root)

        self.history = HistoryManager()

        self.writer = MemoryReportWriter(output_root)

    def run(
        self,
        reflection_report,
        improvement_report,
    ) -> MemoryReport:
        """
        Store the latest iteration and generate
        memory reports.
        """

        history = self.store.load()

        latest = self.history.latest(history)

        iteration = (
            1
            if latest is None
            else latest.iteration + 1
        )

        entry = MemoryEntry(
            iteration=iteration,
            timestamp=datetime.now(
                timezone.utc
            ),
            reflection_summary=reflection_report.summary,
            improvement_summary=improvement_report.summary,
            overall_score=(
                reflection_report.score.overall_score
            ),
        )

        history = self.history.append(
            history,
            entry,
        )

        self.store.save(history)

        report = MemoryReport(
            history=history,
            saved=True,
            location=str(
                self.store.file_path
            ),
        )

        self.writer.write(report)

        return report