"""
Shared data models for the Verification Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class VerificationCheck:
    """Represents a single verification step."""

    name: str
    success: bool
    duration: float = 0.0
    message: str = ""
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class VerificationResult:
    """Overall verification result."""

    project_root: Path
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    finished_at: datetime | None = None

    checks: list[VerificationCheck] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(check.success for check in self.checks)

    @property
    def failed_checks(self) -> list[VerificationCheck]:
        return [c for c in self.checks if not c.success]


@dataclass(slots=True)
class VerificationReport:
    """Summary report."""

    project_name: str
    total_checks: int = 0
    passed: int = 0
    failed: int = 0
    results: list[VerificationCheck] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        if self.total_checks == 0:
            return 0.0
        return (self.passed / self.total_checks) * 100.0
