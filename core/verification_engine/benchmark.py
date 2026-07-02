"""
Benchmark verification step.

Executes a user-supplied benchmark command and records timing.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import time

from .models import VerificationCheck


@dataclass(slots=True)
class BenchmarkRunner:
    """Runs project performance benchmarks."""

    command: tuple[str, ...] = ("pytest", "-m", "benchmark")

    def run(self, project_root: Path) -> VerificationCheck:
        start = time.perf_counter()

        result = subprocess.run(
            list(self.command),
            cwd=project_root,
            capture_output=True,
            text=True,
        )

        duration = time.perf_counter() - start

        return VerificationCheck(
            name="benchmark",
            success=result.returncode == 0,
            duration=duration,
            message=(
                "Benchmark completed successfully."
                if result.returncode == 0
                else "Benchmark failed."
            ),
            details={
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
        )
