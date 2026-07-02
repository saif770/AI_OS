"""
Linter verification step.

Runs Ruff against the project and reports the result.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import time

from .models import VerificationCheck


@dataclass(slots=True)
class Linter:
    """Runs Ruff lint checks."""

    command: tuple[str, ...] = ("ruff", "check", ".")

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
            name="linter",
            success=result.returncode == 0,
            duration=duration,
            message="Lint passed." if result.returncode == 0 else "Lint failed.",
            details={
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
        )
