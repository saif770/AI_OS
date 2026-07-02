"""
bootstrap/verification.py

Final project verification stage.
"""

from __future__ import annotations

from pathlib import Path

from .base import BootstrapStage
from .result import BootstrapResult


class VerificationStage(BootstrapStage):
    """
    Verify that the AI-OS project is ready.
    """

    name = "Verification"

    order = 50

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

        missing_directories = []

        missing_files = []

        # ---------------------------------------------------------
        # Verify directories
        # ---------------------------------------------------------

        for directory in self.REQUIRED_DIRECTORIES:

            path = project_root / directory

            if not path.exists():

                missing_directories.append(directory)

        # ---------------------------------------------------------
        # Verify files
        # ---------------------------------------------------------

        for file in self.REQUIRED_FILES:

            path = project_root / file

            if not path.exists():

                missing_files.append(file)

        # ---------------------------------------------------------
        # Verify Context
        # ---------------------------------------------------------

        python_version = self.context.get("python_version")

        git_installed = self.context.get("git_installed")

        repository_exists = self.context.get("repository_exists")

        # ---------------------------------------------------------
        # Final Status
        # ---------------------------------------------------------

        if missing_directories:

            result.add_error(
                f"Missing directories: {', '.join(missing_directories)}"
            )

        if missing_files:

            result.add_error(
                f"Missing files: {', '.join(missing_files)}"
            )

        result.update(
            project_root=str(project_root),
            python_version=python_version,
            git_installed=git_installed,
            repository_exists=repository_exists,
            missing_directories=missing_directories,
            missing_files=missing_files,
            directories_verified=len(self.REQUIRED_DIRECTORIES),
            files_verified=len(self.REQUIRED_FILES),
            verification_passed=(
                not missing_directories
                and not missing_files
            ),
        )

        return result

