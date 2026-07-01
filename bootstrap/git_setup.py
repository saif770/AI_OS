"""
bootstrap/git_setup.py

Git initialization and verification stage.
"""

from __future__ import annotations

import shutil
import subprocess

from .base import BootstrapStage
from .result import BootstrapResult


class GitSetupStage(BootstrapStage):
    """
    Verify Git installation and repository status.
    """

    name = "Git Setup"

    order = 40

    def execute(self) -> BootstrapResult:

        result = BootstrapResult(self.name)

        project_root = self.context.project_root

        git_executable = shutil.which("git")

        git_installed = git_executable is not None

        git_version = None

        repository_exists = False

        current_branch = None

        remote_origin = None

        if git_installed:

            try:

                process = subprocess.run(
                    [git_executable, "--version"],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                git_version = process.stdout.strip()

            except Exception as exc:

                result.add_warning(str(exc))

            repository_exists = (project_root / ".git").exists()

            if repository_exists:

                try:

                    process = subprocess.run(
                        [
                            git_executable,
                            "-C",
                            str(project_root),
                            "branch",
                            "--show-current",
                        ],
                        capture_output=True,
                        text=True,
                        check=False,
                    )

                    current_branch = process.stdout.strip()

                except Exception as exc:

                    result.add_warning(str(exc))

                try:

                    process = subprocess.run(
                        [
                            git_executable,
                            "-C",
                            str(project_root),
                            "remote",
                            "get-url",
                            "origin",
                        ],
                        capture_output=True,
                        text=True,
                        check=False,
                    )

                    if process.returncode == 0:
                        remote_origin = process.stdout.strip()

                except Exception as exc:

                    result.add_warning(str(exc))

        result.update(
            git_installed=git_installed,
            git_executable=git_executable,
            git_version=git_version,
            repository_exists=repository_exists,
            current_branch=current_branch,
            remote_origin=remote_origin,
        )

        self.context.set(
            "git_installed",
            git_installed,
        )

        self.context.set(
            "repository_exists",
            repository_exists,
        )

        self.context.set(
            "current_branch",
            current_branch,
        )

        return result