"""
Execution Engine data models.

Shared models used throughout the execution engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC, UTC
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class CodePatch:
    """Represents a single code patch."""

    target_file: Path
    description: str
    original: str = ""
    updated: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class ValidationResult:
    """Validation outcome for a generated patch."""

    passed: bool
    message: str = ""
    diagnostics: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ExecutionTask:
    """Single execution task."""

    id: str
    title: str
    description: str
    priority: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ExecutionResult:
    """Result of executing a task."""

    task: ExecutionTask
    success: bool
    validation: ValidationResult | None = None
    patches: list[CodePatch] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.utcnow)
    finished_at: datetime | None = None


@dataclass(slots=True)
class ExecutionReport:
    """Execution summary."""

    project_name: str
    total_tasks: int = 0
    completed: int = 0
    failed: int = 0
    results: list[ExecutionResult] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return (self.completed / self.total_tasks) * 100.0


