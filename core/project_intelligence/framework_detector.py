"""
framework_detector.py

Detect frameworks used by the project.
"""

from __future__ import annotations

import json
from pathlib import Path


class FrameworkDetector:
    """
    Detect project frameworks from dependency files.
    """

    PYTHON_FRAMEWORKS = {
        "fastapi": "FastAPI",
        "flask": "Flask",
        "django": "Django",
        "streamlit": "Streamlit",
        "gradio": "Gradio",
        "dash": "Dash",
        "langchain": "LangChain",
        "langgraph": "LangGraph",
        "crewai": "CrewAI",
        "autogen": "AutoGen",
        "pydantic": "Pydantic",
        "sqlalchemy": "SQLAlchemy",
        "pytest": "PyTest",
        "numpy": "NumPy",
        "pandas": "Pandas",
        "torch": "PyTorch",
        "tensorflow": "TensorFlow",
        "transformers": "HuggingFace Transformers",
    }

    NODE_FRAMEWORKS = {
        "react": "React",
        "next": "Next.js",
        "vue": "Vue",
        "nuxt": "Nuxt",
        "angular": "Angular",
        "express": "Express",
        "nestjs": "NestJS",
        "electron": "Electron",
        "vite": "Vite",
    }

    def __init__(self, project_root: Path):

        self.project_root = Path(project_root)

    # -------------------------------------------------------------

    def detect(self) -> dict:

        frameworks = set()

        frameworks.update(
            self._scan_requirements()
        )

        frameworks.update(
            self._scan_pyproject()
        )

        frameworks.update(
            self._scan_package_json()
        )

        return {
            "frameworks": sorted(frameworks),
            "primary_framework": (
                sorted(frameworks)[0]
                if frameworks
                else "Unknown"
            ),
            "count": len(frameworks),
        }

    # -------------------------------------------------------------

    def _scan_requirements(self):

        detected = set()

        file = self.project_root / "requirements.txt"

        if not file.exists():

            return detected

        for line in file.read_text(
            encoding="utf-8",
            errors="ignore",
        ).splitlines():

            package = (
                line.split("==")[0]
                .split(">=")[0]
                .split("<=")[0]
                .strip()
                .lower()
            )

            if package in self.PYTHON_FRAMEWORKS:

                detected.add(
                    self.PYTHON_FRAMEWORKS[package]
                )

        return detected

    # -------------------------------------------------------------

    def _scan_pyproject(self):

        detected = set()

        file = self.project_root / "pyproject.toml"

        if not file.exists():

            return detected

        content = file.read_text(
            encoding="utf-8",
            errors="ignore",
        ).lower()

        for package, framework in self.PYTHON_FRAMEWORKS.items():

            if package in content:

                detected.add(framework)

        return detected

    # -------------------------------------------------------------

    def _scan_package_json(self):

        detected = set()

        file = self.project_root / "package.json"

        if not file.exists():

            return detected

        try:

            package = json.loads(
                file.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:

            return detected

        dependencies = {}

        dependencies.update(
            package.get("dependencies", {})
        )

        dependencies.update(
            package.get(
                "devDependencies",
                {},
            )
        )

        for dep in dependencies:

            dep = dep.lower()

            if dep in self.NODE_FRAMEWORKS:

                detected.add(
                    self.NODE_FRAMEWORKS[dep]
                )

        return detected

