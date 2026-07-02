"""
Formatter verification step.

Runs Black in check mode to verify formatting.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import time

from .models import VerificationCheck


@dataclass(slots=True)
class Formatter:
    """Runs Black formatting checks."""

    command: tuple[str, ...] = ("black", "--check", ".")

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
            name="formatter",
            success=result.returncode == 0,
            duration=duration,
            message=(
                "Formatting check passed."
                if result.returncode == 0
                else "Formatting issues detected."
            ),
            details={
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
        )
