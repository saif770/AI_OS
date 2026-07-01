"""
git_analyzer.py

Analyze Git repository information.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


class GitAnalyzer:
    """
    Collect Git repository information.
    """

    def __init__(self, project_root: Path):

        self.project_root = Path(project_root)

        self.git = shutil.which("git")

    # -------------------------------------------------------------

    def analyze(self) -> dict:

        info = {
            "git_installed": self.git is not None,
            "repository": False,
            "branch": None,
            "remote": None,
            "latest_commit": None,
            "latest_commit_hash": None,
            "commit_count": 0,
            "tags": [],
            "status": [],
        }

        if self.git is None:

            return info

        if not (self.project_root / ".git").exists():

            return info

        info["repository"] = True

        info["branch"] = self._run(
            "branch",
            "--show-current",
        )

        info["remote"] = self._run(
            "remote",
            "get-url",
            "origin",
        )

        info["latest_commit_hash"] = self._run(
            "rev-parse",
            "HEAD",
        )

        info["latest_commit"] = self._run(
            "log",
            "-1",
            "--pretty=%s",
        )

        commits = self._run(
            "rev-list",
            "--count",
            "HEAD",
        )

        try:

            info["commit_count"] = int(commits)

        except Exception:

            pass

        tags = self._run(
            "tag",
        )

        if tags:

            info["tags"] = tags.splitlines()

        status = self._run(
            "status",
            "--short",
        )

        if status:

            info["status"] = status.splitlines()

        return info

    # -------------------------------------------------------------

    def _run(self, *args) -> str | None:

        try:

            process = subprocess.run(
                [
                    self.git,
                    "-C",
                    str(self.project_root),
                    *args,
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            if process.returncode != 0:

                return None

            return process.stdout.strip()

        except Exception:

            return None