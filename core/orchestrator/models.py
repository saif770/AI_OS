"""
Orchestrator data models.

These models describe the execution state of an AI-OS
pipeline run. They intentionally contain no orchestration
logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class PipelineContext:
    """
    Shared context passed between pipeline stages.
    """

    project_root: str

    started_at: datetime = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )

    project_intelligence: Any | None = None

    planning_report: Any | None = None

    execution_report: Any | None = None

    verification_report: Any | None = None

    reflection_report: Any | None = None

    improvement_report: Any | None = None

    memory_report: Any | None = None


@dataclass(slots=True)
class PipelineResult:
    """
    Final result returned by the Orchestrator.
    """

    success: bool

    completed_steps: list[str] = field(
        default_factory=list
    )

    failed_step: str | None = None

    message: str = ""

    duration_seconds: float = 0.0

    context: PipelineContext | None = None

    finished_at: datetime = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )