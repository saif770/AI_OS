"""
Formatter verification step.

Runs Black in check mode to verify formatting.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .models import VerificationCheck
from .tool_runner import ToolRunner


@dataclass(slots=True)
class Formatter:
    """Runs Black formatting checks."""

    command: tuple[str, ...] = ("black", "--check", ".")
    tool_runner: ToolRunner = field(default_factory=ToolRunner)

    def run(self, project_root: Path) -> VerificationCheck:
        return self.tool_runner.run(
            name="formatter",
            project_root=project_root,
            command=list(self.command),
            module_fallback="black",
        )
