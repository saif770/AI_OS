"""
entrypoint_detector.py

Detect project entry points.
"""

from __future__ import annotations

from pathlib import Path


class EntrypointDetector:
    """
    Detect executable entry points within a project.
    """

    PRIORITY = [
        "bootstrap.py",
        "main.py",
        "app.py",
        "manage.py",
        "run.py",
        "__main__.py",
        "cli.py",
        "server.py",
        "index.py",
        "index.js",
        "main.js",
    ]

    def __init__(self, project_root: Path):

        self.project_root = Path(project_root)

    # -------------------------------------------------------------

    def detect(self) -> dict:

        entrypoints = []

        # Priority search

        for filename in self.PRIORITY:

            matches = list(
                self.project_root.rglob(filename)
            )

            for match in matches:

                entrypoints.append(
                    str(match.relative_to(self.project_root))
                )

        # Executable Python files

        for file in self.project_root.rglob("*.py"):

            try:

                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )

            except Exception:

                continue

            if (
                "__name__ == '__main__'" in content
                or '__name__ == "__main__"' in content
            ):

                relative = str(
                    file.relative_to(self.project_root)
                )

                if relative not in entrypoints:

                    entrypoints.append(relative)

        # pyproject console scripts

        pyproject = self.project_root / "pyproject.toml"

        if pyproject.exists():

            entrypoints.append("pyproject.toml")

        # package.json scripts

        package_json = self.project_root / "package.json"

        if package_json.exists():

            entrypoints.append("package.json")

        primary = (
            entrypoints[0]
            if entrypoints
            else None
        )

        return {
            "primary_entrypoint": primary,
            "entrypoints": sorted(entrypoints),
            "count": len(entrypoints),
        }

