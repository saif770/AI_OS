"""
AI-OS Orchestrator Engine.

Coordinates the execution of all AI-OS engines.
"""

from __future__ import annotations

import time
from pathlib import Path

from .models import (
    PipelineContext,
    PipelineResult,
)
from .pipeline import Pipeline
from .report import OrchestratorReportWriter


class Orchestrator:
    """
    Coordinates execution of the AI-OS pipeline.
    """

    def __init__(
        self,
        project_root: Path,
    ) -> None:

        self.project_root = Path(project_root)

        self.pipeline = Pipeline.default()

        self.report_writer = (
            OrchestratorReportWriter(
                self.project_root / "output"
            )
        )

    def register_step(
        self,
        name: str,
        executor,
    ) -> None:
        """
        Register a pipeline stage.
        """

        self.pipeline.add_step(
            name,
            executor,
        )

    def run(self) -> PipelineResult:
        """
        Execute the complete pipeline.
        """

        context = PipelineContext(
            project_root=str(
                self.project_root
            )
        )

        completed_steps: list[str] = []

        start = time.perf_counter()

        try:

            for step in self.pipeline:

                result = step.executor(
                    context
                )

                setattr(
                    context,
                    step.name,
                    result,
                )

                completed_steps.append(
                    step.name
                )

            duration = (
                time.perf_counter()
                - start
            )

            pipeline_result = PipelineResult(
                success=True,
                completed_steps=completed_steps,
                message="Pipeline completed successfully.",
                duration_seconds=duration,
                context=context,
            )

        except Exception as exc:

            duration = (
                time.perf_counter()
                - start
            )

            pipeline_result = PipelineResult(
                success=False,
                completed_steps=completed_steps,
                failed_step=(
                    step.name
                    if "step" in locals()
                    else None
                ),
                message=str(exc),
                duration_seconds=duration,
                context=context,
            )

        self.report_writer.write(
            pipeline_result
        )

        return pipeline_result