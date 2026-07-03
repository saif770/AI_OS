"""
AI-OS Runtime Engine.

Coordinates autonomous execution of the AI-OS
Orchestrator.
"""

from __future__ import annotations

import time
from pathlib import Path

from core.orchestrator.engine import Orchestrator

from .models import (
    RuntimeContext,
    RuntimeResult,
)
from .report import RuntimeReportWriter
from .scheduler import RuntimeScheduler


class RuntimeEngine:
    """
    Coordinates Runtime execution.
    """

    def __init__(
        self,
        project_root: Path,
        scheduler: RuntimeScheduler | None = None,
    ) -> None:

        self.project_root = Path(project_root)

        self.scheduler = (
            scheduler
            if scheduler is not None
            else RuntimeScheduler()
        )

        self.orchestrator = Orchestrator(
            self.project_root
        )

        self.report_writer = RuntimeReportWriter(
            self.project_root / "output"
        )

    def run(self) -> RuntimeResult:
        """
        Execute the Runtime loop.
        """

        context = RuntimeContext(
            project_root=str(
                self.project_root
            )
        )

        start = time.perf_counter()

        success = True
        stop_reason = "Maximum iterations reached."

        while True:

            result = self.orchestrator.run()

            context.orchestrator_result = result

            if (
                self.scheduler.stop_on_failure
                and not result.success
            ):
                success = False
                stop_reason = (
                    "Pipeline execution failed."
                )
                break

            if not self.scheduler.should_continue(
                context
            ):
                break

            self.scheduler.next_iteration(
                context
            )

        duration = (
            time.perf_counter()
            - start
        )

        runtime_result = RuntimeResult(
            success=success,
            iterations_completed=context.iteration,
            stopped_reason=stop_reason,
            duration_seconds=duration,
            context=context,
        )

        self.report_writer.write(
            runtime_result
        )

        return runtime_result