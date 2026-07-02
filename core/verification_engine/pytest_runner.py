"""
Pytest verification step.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .models import VerificationCheck
from .tool_runner import ToolRunner


@dataclass(slots=True)
class TestRunner:
    """Runs the project's pytest suite."""

    pytest_args: tuple[str, ...] = ("-q",)
    tool_runner: ToolRunner = field(default_factory=ToolRunner)

    def run(self, project_root: Path) -> VerificationCheck:
        return self.tool_runner.run(
            name="test_runner",
            project_root=project_root,
            command=["pytest", *self.pytest_args],
            module_fallback="pytest",
        )
