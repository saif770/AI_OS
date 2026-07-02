"""
bootstrap/project_scan.py

Project scanning and inventory stage.
"""

from __future__ import annotations

from pathlib import Path

from .base import BootstrapStage
from .result import BootstrapResult


class ProjectScanStage(BootstrapStage):
    """
    Scan the project and collect metadata.
    """

    name = "Project Scan"

    order = 70

    EXCLUDED_DIRECTORIES = {
        ".git",
        ".venv",
        "__pycache__",
        ".pytest_cache",
        ".idea",
        ".vscode",
        "node_modules",
        ".mypy_cache",
        ".bootstrap",
    }

    def execute(self) -> BootstrapResult:

        result = BootstrapResult(self.name)

        project_root = self.context.project_root

        directories = []

        files = []

        python_files = []

        total_size = 0

        # ---------------------------------------------------------

        for path in project_root.rglob("*"):

            relative = path.relative_to(project_root)

            if any(
                part in self.EXCLUDED_DIRECTORIES
                for part in relative.parts
            ):
                continue

            if path.is_dir():

                directories.append(str(relative))

                continue

            files.append(str(relative))

            try:
                total_size += path.stat().st_size
            except OSError:
                pass

            if path.suffix == ".py":

                python_files.append(str(relative))

        # ---------------------------------------------------------

        result.update(

            project_root=str(project_root),

            directory_count=len(directories),

            file_count=len(files),

            python_file_count=len(python_files),

            total_size_bytes=total_size,

            directories=sorted(directories),

            files=sorted(files),

            python_files=sorted(python_files),

        )

        self.context.set(
            "project_directories",
            directories,
        )

        self.context.set(
            "project_files",
            files,
        )

        self.context.set(
            "python_files",
            python_files,
        )

        return result

