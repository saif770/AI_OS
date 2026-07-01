"""
architecture.py

Detect the project's architectural style.
"""

from __future__ import annotations

from pathlib import Path


class ArchitectureDetector:
    """
    Detect high-level project architecture.
    """

    def __init__(self, project_root: Path):

        self.project_root = Path(project_root)

    # -------------------------------------------------------------

    def detect(self) -> dict:

        architecture = "Unknown"

        confidence = "Low"

        reasons = []

        if self._is_django():

            architecture = "MVC"

            confidence = "High"

            reasons.append("manage.py found")

        elif self._is_fastapi():

            architecture = "Layered"

            confidence = "Medium"

            reasons.append("FastAPI detected")

        elif self._is_plugin():

            architecture = "Plugin Architecture"

            confidence = "High"

            reasons.append("bootstrap/ and core/ packages found")

        elif self._is_monolith():

            architecture = "Monolith"

            confidence = "Medium"

            reasons.append("Single application entrypoint")

        return {
            "architecture": architecture,
            "confidence": confidence,
            "reasons": reasons,
        }

    # -------------------------------------------------------------

    def _exists(self, name: str) -> bool:

        return (self.project_root / name).exists()

    # -------------------------------------------------------------

    def _is_plugin(self) -> bool:

        return (
            self._exists("bootstrap")
            and self._exists("core")
        )

    # -------------------------------------------------------------

    def _is_fastapi(self) -> bool:

        requirements = self.project_root / "requirements.txt"

        if requirements.exists():

            content = requirements.read_text(
                encoding="utf-8",
                errors="ignore",
            ).lower()

            return "fastapi" in content

        return False

    # -------------------------------------------------------------

    def _is_django(self) -> bool:

        return self._exists("manage.py")

    # -------------------------------------------------------------

    def _is_monolith(self) -> bool:

        candidates = [
            "main.py",
            "app.py",
            "bootstrap.py",
        ]

        count = 0

        for file in candidates:

            if self._exists(file):

                count += 1

        return count == 1