"""
dependency_analyzer.py

Analyze project dependencies from supported package managers.
"""

from __future__ import annotations

import json
from pathlib import Path


class DependencyAnalyzer:
    """
    Analyze project dependencies.
    """

    def __init__(self, project_root: Path):

        self.project_root = Path(project_root)

    # -------------------------------------------------------------

    def analyze(self) -> dict:

        return {
            "python": self._requirements(),
            "pyproject": self._pyproject(),
            "node": self._package_json(),
            "go": self._gomod(),
            "rust": self._cargo(),
        }

    # -------------------------------------------------------------

    def _requirements(self):

        file = self.project_root / "requirements.txt"

        if not file.exists():

            return []

        packages = []

        for line in file.read_text(
            encoding="utf-8",
            errors="ignore",
        ).splitlines():

            line = line.strip()

            if (
                not line
                or line.startswith("#")
            ):
                continue

            packages.append(line)

        return packages

    # -------------------------------------------------------------

    def _pyproject(self):

        file = self.project_root / "pyproject.toml"

        if not file.exists():

            return []

        content = file.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        packages = []

        for line in content.splitlines():

            line = line.strip()

            if "=" not in line:

                continue

            if line.startswith("["):

                continue

            packages.append(line)

        return packages

    # -------------------------------------------------------------

    def _package_json(self):

        file = self.project_root / "package.json"

        if not file.exists():

            return []

        try:

            package = json.loads(
                file.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:

            return []

        packages = []

        dependencies = {}

        dependencies.update(
            package.get(
                "dependencies",
                {}
            )
        )

        dependencies.update(
            package.get(
                "devDependencies",
                {}
            )
        )

        for name, version in dependencies.items():

            packages.append(
                f"{name} {version}"
            )

        return sorted(packages)

    # -------------------------------------------------------------

    def _gomod(self):

        file = self.project_root / "go.mod"

        if not file.exists():

            return []

        packages = []

        for line in file.read_text(
            encoding="utf-8",
            errors="ignore",
        ).splitlines():

            line = line.strip()

            if line.startswith("require"):

                packages.append(line)

        return packages

    # -------------------------------------------------------------

    def _cargo(self):

        file = self.project_root / "Cargo.toml"

        if not file.exists():

            return []

        packages = []

        in_dependencies = False

        for line in file.read_text(
            encoding="utf-8",
            errors="ignore",
        ).splitlines():

            line = line.strip()

            if line == "[dependencies]":

                in_dependencies = True

                continue

            if (
                in_dependencies
                and line.startswith("[")
            ):

                break

            if (
                in_dependencies
                and "=" in line
            ):

                packages.append(line)

        return packages

