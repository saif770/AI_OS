"""
Runtime data models.

These models describe the state of a complete AI-OS
runtime execution.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class RuntimeContext:
    """
    Shared runtime context.
    """

    project_root: str

    started_at: datetime = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )

    iteration: int = 1

    orchestrator_result: Any | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class RuntimeResult:
    """
    Final Runtime execution result.
    """

    success: bool

    iterations_completed: int = 0

    stopped_reason: str = ""

    duration_seconds: float = 0.0

    context: RuntimeContext | None = None

    finished_at: datetime = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )