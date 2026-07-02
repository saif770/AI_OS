"""
Benchmark verification step.

Executes a user-supplied benchmark command and records timing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .models import VerificationCheck
from .tool_runner import ToolRunner


@dataclass(slots=True)
class BenchmarkRunner:
    """Runs project performance benchmarks."""

    command: tuple[str, ...] = ("pytest", "-m", "benchmark")
    tool_runner: ToolRunner = field(default_factory=ToolRunner)

    def run(self, project_root: Path) -> VerificationCheck:
        return self.tool_runner.run(
            name="benchmark",
            project_root=project_root,
            command=list(self.command),
            module_fallback="pytest",
        )
