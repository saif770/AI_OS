"""
bootstrap/environment.py

Environment preparation stage.
"""

from __future__ import annotations

import platform
import sys
from pathlib import Path

from .base import BootstrapStage
from .result import BootstrapResult


class EnvironmentStage(BootstrapStage):
    """
    Verify the local Python environment.
    """

    name = "Environment"

    order = 10

    def execute(self) -> BootstrapResult:

        result = BootstrapResult(self.name)

        project_root = self.context.project_root

        python_executable = Path(sys.executable)

        result.update(
            project_root=str(project_root),
            python_executable=str(python_executable),
            python_version=platform.python_version(),
            implementation=platform.python_implementation(),
            operating_system=platform.system(),
            os_version=platform.release(),
            machine=platform.machine(),
            processor=platform.processor(),
            platform=platform.platform(),
            architecture=platform.architecture()[0],
            current_working_directory=str(Path.cwd()),
        )

        # Store commonly used values in the shared context

        self.context.set(
            "python_executable",
            str(python_executable),
        )

        self.context.set(
            "python_version",
            platform.python_version(),
        )

        self.context.set(
            "operating_system",
            platform.system(),
        )

        self.context.set(
            "project_root",
            str(project_root),
        )

        return result