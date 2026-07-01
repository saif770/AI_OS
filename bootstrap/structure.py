"""
bootstrap/structure.py

Project structure verification stage.
"""

from __future__ import annotations

from pathlib import Path

from .base import BootstrapStage
from .result import BootstrapResult


class StructureStage(BootstrapStage):
    """
    Verify the AI-OS project structure.
    """

    name = "Structure"

    order = 20

    REQUIRED_DIRECTORIES = [
        "bootstrap",
        "config",
        "core",
        "docs",
        "logs",
        "output",
        "templates",
        "tests",
        "utils",
        ".bootstrap",
    ]

    REQUIRED_FILES = [
        "bootstrap.py",
        "README.md",
        "requirements.txt",
        "setup.bat",
    ]

    def execute(self) -> BootstrapResult:

        result = BootstrapResult(self.name)

        project_root = self.context.project_root

        created_directories = []
        existing_directories = []

        created_files = []
        existing_files = []

        # ---------------------------------------------------------
        # Verify directories
        # ---------------------------------------------------------

        for directory in self.REQUIRED_DIRECTORIES:

            path = project_root / directory

            if path.exists():

                existing_directories.append(directory)

            else:

                path.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                created_directories.append(directory)

        # ---------------------------------------------------------
        # Verify files
        # ---------------------------------------------------------

        for file in self.REQUIRED_FILES:

            path = project_root / file

            if path.exists():

                existing_files.append(file)

            else:

                path.touch()

                created_files.append(file)

        # ---------------------------------------------------------

        result.update(

            created_directories=created_directories,

            existing_directories=existing_directories,

            created_files=created_files,

            existing_files=existing_files,

            total_directories=len(self.REQUIRED_DIRECTORIES),

            total_files=len(self.REQUIRED_FILES),

        )

        return result