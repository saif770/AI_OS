"""
Security verification step.

Runs Bandit recursively against the project.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .models import VerificationCheck
from .tool_runner import ToolRunner


@dataclass(slots=True)
class SecurityScanner:
    """Runs Bandit security analysis."""

    command: tuple[str, ...] = (
        "bandit",
        "-r",
        ".",
        "-q",
    )
    tool_runner: ToolRunner = field(default_factory=ToolRunner)

    def run(self, project_root: Path) -> VerificationCheck:
        return self.tool_runner.run(
            name="security",
            project_root=project_root,
            command=list(self.command),
            module_fallback="bandit",
        )
