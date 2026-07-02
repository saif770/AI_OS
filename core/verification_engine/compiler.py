"""
Compiler verification step.

Compiles all Python files in a project and reports syntax errors.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import compileall
import time

from .models import VerificationCheck


@dataclass(slots=True)
class Compiler:
    """Runs Python compilation checks."""

    quiet: int = 1

    def run(self, project_root: Path) -> VerificationCheck:
        start = time.perf_counter()

        success = compileall.compile_dir(
            str(project_root),
            force=False,
            quiet=self.quiet,
        )

        duration = time.perf_counter() - start

        return VerificationCheck(
            name="compiler",
            success=success,
            duration=duration,
            message=(
                "Compilation successful."
                if success
                else "Compilation failed."
            ),
        )
