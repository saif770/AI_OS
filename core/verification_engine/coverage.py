"""
Coverage verification step.

Runs pytest with coverage reporting enabled.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import time

from .models import VerificationCheck


@dataclass(slots=True)
class CoverageRunner:
    """Runs pytest coverage."""

    command: tuple[str, ...] = (
        "pytest",
        "--cov=.",
        "--cov-report=term-missing",
    )

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
            name="coverage",
            success=result.returncode == 0,
            duration=duration,
            message=(
                "Coverage completed successfully."
                if result.returncode == 0
                else "Coverage failed."
            ),
            details={
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
        )
