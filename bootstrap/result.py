"""
bootstrap/result.py

Standard result object returned by every bootstrap stage.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class BootstrapResult:
    """
    Standard result returned by every bootstrap stage.
    """

    stage: str

    status: str = "SUCCESS"

    started_at: datetime = field(default_factory=datetime.now)

    finished_at: datetime | None = None

    duration: float = 0.0

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    data: dict[str, Any] = field(default_factory=dict)

    def finish(self) -> "BootstrapResult":
        """
        Mark stage as completed.
        """
        self.finished_at = datetime.now()

        self.duration = round(
            (self.finished_at - self.started_at).total_seconds(),
            3,
        )

        return self

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)

    def add_error(self, message: str) -> None:
        self.status = "FAILED"
        self.errors.append(message)

    def set_status(self, status: str) -> None:
        self.status = status

    def update(self, **kwargs) -> None:
        """
        Store arbitrary stage data.
        """
        self.data.update(kwargs)

    @property
    def success(self) -> bool:
        return self.status == "SUCCESS"

    @property
    def failed(self) -> bool:
        return self.status == "FAILED"

    @property
    def skipped(self) -> bool:
        return self.status == "SKIPPED"

    def to_dict(self) -> dict:
        return {
            "stage": self.stage,
            "status": self.status,
            "started_at": self.started_at.isoformat(),
            "finished_at": (
                self.finished_at.isoformat()
                if self.finished_at
                else None
            ),
            "duration": self.duration,
            "warnings": self.warnings,
            "errors": self.errors,
            "data": self.data,
        }

    def __str__(self) -> str:
        return (
            f"{self.stage} | "
            f"{self.status} | "
            f"{self.duration:.3f}s"
        )