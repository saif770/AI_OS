"""
Shared subprocess runner for Verification Engine tools.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
import sys
import time

from .models import VerificationCheck


@dataclass(slots=True)
class ToolRunner:
    """Executes external verification tools consistently."""

    timeout: int = 300

    def run(
        self,
        *,
        name: str,
        project_root: Path,
        command: list[str],
        module_fallback: str | None = None,
    ) -> VerificationCheck:
        start = time.perf_counter()

        executable = command[0]

        if shutil.which(executable):
            cmd = command
        elif module_fallback:
            cmd = [sys.executable, "-m", module_fallback, *command[1:]]
        else:
            return VerificationCheck(
                name=name,
                success=False,
                duration=0.0,
                message=f"{executable} is not installed.",
                details={"missing_tool": executable},
            )

        try:
            result = subprocess.run(
                cmd,
                cwd=project_root,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )

            success = result.returncode == 0
            message = "Passed." if success else "Failed."

            return VerificationCheck(
                name=name,
                success=success,
                duration=time.perf_counter() - start,
                message=message,
                details={
                    "command": cmd,
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                },
            )

        except subprocess.TimeoutExpired:
            return VerificationCheck(
                name=name,
                success=False,
                duration=time.perf_counter() - start,
                message="Timed out.",
                details={"timeout": self.timeout},
            )
