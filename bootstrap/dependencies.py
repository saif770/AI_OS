"""
bootstrap/dependencies.py

Dependency installation and verification stage.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from .base import BootstrapStage
from .result import BootstrapResult


class DependencyStage(BootstrapStage):
    """
    Verify Python dependencies.
    """

    name = "Dependencies"

    order = 30

    def execute(self) -> BootstrapResult:

        result = BootstrapResult(self.name)

        project_root = self.context.project_root

        requirements = project_root / "requirements.txt"

        venv = project_root / ".venv"

        pip_executable = shutil.which("pip")

        python_executable = sys.executable

        pip_version = None

        if pip_executable:

            try:

                process = subprocess.run(
                    [pip_executable, "--version"],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                pip_version = process.stdout.strip()

            except Exception as exc:

                result.add_warning(str(exc))

        requirements_exists = requirements.exists()

        venv_exists = venv.exists()

        result.update(
            python_executable=python_executable,
            pip_executable=pip_executable,
            pip_version=pip_version,
            requirements_file=str(requirements),
            requirements_exists=requirements_exists,
            virtual_environment=str(venv),
            virtual_environment_exists=venv_exists,
        )

        self.context.set(
            "requirements_file",
            str(requirements),
        )

        self.context.set(
            "venv_path",
            str(venv),
        )

        self.context.set(
            "pip_executable",
            pip_executable,
        )

        return result

