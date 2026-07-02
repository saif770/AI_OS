"""
Linter verification step.

Runs Ruff against the project and reports the result.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .models import VerificationCheck
from .tool_runner import ToolRunner


@dataclass(slots=True)
class Linter:
    """Runs Ruff lint checks."""

    command: tuple[str, ...] = ("ruff", "check", ".")
    tool_runner: ToolRunner = field(default_factory=ToolRunner)

    def run(self, project_root: Path) -> VerificationCheck:
        return self.tool_runner.run(
            name="linter",
            project_root=project_root,
            command=list(self.command),
            module_fallback="ruff",
        )
