"""
Pytest verification step.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import time

from .models import VerificationCheck


@dataclass(slots=True)
class TestRunner:
    """Runs the project's pytest suite."""

    pytest_args: tuple[str, ...] = ("-q",)

    def run(self, project_root: Path) -> VerificationCheck:
        start = time.perf_counter()

        cmd = ["pytest", *self.pytest_args]

        result = subprocess.run(
            cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
        )

        duration = time.perf_counter() - start

        success = result.returncode == 0

        message = "All tests passed." if success else "Tests failed."

        return VerificationCheck(
            name="test_runner",
            success=success,
            duration=duration,
            message=message,
            details={
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
        )
