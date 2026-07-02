"""
language_detector.py

Detect programming languages used in a project.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path


class LanguageDetector:
    """
    Detect programming languages from file extensions.
    """

    EXTENSIONS = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".jsx": "JavaScript",
        ".java": "Java",
        ".cs": "C#",
        ".cpp": "C++",
        ".c": "C",
        ".h": "C/C++ Header",
        ".hpp": "C++ Header",
        ".go": "Go",
        ".rs": "Rust",
        ".php": "PHP",
        ".rb": "Ruby",
        ".swift": "Swift",
        ".kt": "Kotlin",
        ".scala": "Scala",
        ".r": "R",
        ".m": "MATLAB",
        ".sh": "Shell",
        ".ps1": "PowerShell",
        ".sql": "SQL",
        ".html": "HTML",
        ".css": "CSS",
        ".scss": "SCSS",
        ".json": "JSON",
        ".yaml": "YAML",
        ".yml": "YAML",
        ".xml": "XML",
        ".toml": "TOML",
        ".md": "Markdown",
    }

    EXCLUDED_DIRECTORIES = {
        ".git",
        ".venv",
        "__pycache__",
        ".pytest_cache",
        "node_modules",
        ".idea",
        ".vscode",
        ".bootstrap",
    }

    def __init__(self, project_root: Path):

        self.project_root = Path(project_root)

    # -------------------------------------------------------------

    def detect(self) -> dict:

        counts = Counter()

        total_files = 0

        for path in self.project_root.rglob("*"):

            if not path.is_file():
                continue

            if any(
                part in self.EXCLUDED_DIRECTORIES
                for part in path.parts
            ):
                continue

            language = self.EXTENSIONS.get(path.suffix.lower())

            if language:

                counts[language] += 1

                total_files += 1

        if total_files == 0:

            primary = "Unknown"

        else:

            primary = counts.most_common(1)[0][0]

        percentages = {}

        for language, count in counts.items():

            percentages[language] = round(
                (count / total_files) * 100,
                2,
            )

        return {
            "primary_language": primary,
            "total_source_files": total_files,
            "languages": dict(counts),
            "percentages": percentages,
        }

