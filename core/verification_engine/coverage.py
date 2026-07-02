"""
Coverage verification step.

Runs pytest with coverage reporting enabled.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .models import VerificationCheck
from .tool_runner import ToolRunner


@dataclass(slots=True)
class CoverageRunner:
    """Runs pytest coverage."""

    command: tuple[str, ...] = (
        "pytest",
        "--cov=.",
        "--cov-report=term-missing",
    )
    tool_runner: ToolRunner = field(default_factory=ToolRunner)

    def run(self, project_root: Path) -> VerificationCheck:
        return self.tool_runner.run(
            name="coverage",
            project_root=project_root,
            command=list(self.command),
            module_fallback="pytest",
        )
