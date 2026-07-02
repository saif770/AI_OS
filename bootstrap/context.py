"""
bootstrap/context.py

Shared runtime context for the Bootstrap Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .result import BootstrapResult


@dataclass
class BootstrapContext:
    """
    Shared context available to every bootstrap stage.
    """

    # ------------------------------------------------------------------
    # Project Information
    # ------------------------------------------------------------------

    project_root: Path

    project_name: str = ""

    version: str = "1.0.0"

    # ------------------------------------------------------------------
    # Runtime Information
    # ------------------------------------------------------------------

    dry_run: bool = False

    verbose: bool = False

    force: bool = False

    # ------------------------------------------------------------------
    # Stage Results
    # ------------------------------------------------------------------

    results: list[BootstrapResult] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Shared Data Store
    # ------------------------------------------------------------------

    data: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Result Management
    # ------------------------------------------------------------------

    def add_result(self, result: BootstrapResult) -> None:
        """
        Store the result of a completed stage.
        """
        self.results.append(result)

    # ------------------------------------------------------------------

    def get_result(self, stage: str) -> BootstrapResult | None:
        """
        Retrieve a stage result by name.
        """
        for result in self.results:
            if result.stage == stage:
                return result
        return None

    # ------------------------------------------------------------------

    def set(self, key: str, value: Any) -> None:
        """
        Store shared data.
        """
        self.data[key] = value

    # ------------------------------------------------------------------

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve shared data.
        """
        return self.data.get(key, default)

    # ------------------------------------------------------------------

    def has(self, key: str) -> bool:
        """
        Check if shared data exists.
        """
        return key in self.data

    # ------------------------------------------------------------------

    def clear(self) -> None:
        """
        Reset shared runtime state.
        """
        self.results.clear()
        self.data.clear()

    # ------------------------------------------------------------------

    @property
    def success(self) -> bool:
        """
        True if every stage completed successfully.
        """
        return all(result.success for result in self.results)

    # ------------------------------------------------------------------

    @property
    def failed(self) -> bool:
        """
        True if any stage failed.
        """
        return any(result.failed for result in self.results)

    # ------------------------------------------------------------------

    def summary(self) -> dict[str, Any]:
        """
        Return a summary of execution.
        """
        return {
            "project": self.project_name,
            "version": self.version,
            "total_stages": len(self.results),
            "successful": sum(r.success for r in self.results),
            "failed": sum(r.failed for r in self.results),
            "shared_data": len(self.data),
        }

