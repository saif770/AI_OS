"""
code_metrics.py

Collect source code metrics for a project.
"""

from __future__ import annotations

from pathlib import Path


class CodeMetrics:
    """
    Collect repository metrics.
    """

    EXCLUDED_DIRECTORIES = {
        ".git",
        ".venv",
        "__pycache__",
        ".pytest_cache",
        ".idea",
        ".vscode",
        "node_modules",
        ".bootstrap",
    }

    def __init__(self, project_root: Path):

        self.project_root = Path(project_root)

    # -------------------------------------------------------------

    def analyze(self) -> dict:

        metrics = {
            "directories": 0,
            "files": 0,
            "python_files": 0,
            "lines_of_code": 0,
            "blank_lines": 0,
            "comment_lines": 0,
            "classes": 0,
            "functions": 0,
            "imports": 0,
            "test_files": 0,
            "documentation_files": 0,
            "largest_file": None,
            "largest_file_lines": 0,
            "total_size_bytes": 0,
        }

        for path in self.project_root.rglob("*"):

            if any(
                part in self.EXCLUDED_DIRECTORIES
                for part in path.parts
            ):
                continue

            if path.is_dir():

                metrics["directories"] += 1

                continue

            metrics["files"] += 1

            try:

                metrics["total_size_bytes"] += path.stat().st_size

            except OSError:

                pass

            if path.suffix.lower() == ".md":

                metrics["documentation_files"] += 1

            if (
                "test" in path.name.lower()
                and path.suffix == ".py"
            ):

                metrics["test_files"] += 1

            if path.suffix != ".py":

                continue

            metrics["python_files"] += 1

            try:

                lines = path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                ).splitlines()

            except Exception:

                continue

            line_count = len(lines)

            metrics["lines_of_code"] += line_count

            if line_count > metrics["largest_file_lines"]:

                metrics["largest_file_lines"] = line_count

                metrics["largest_file"] = str(
                    path.relative_to(self.project_root)
                )

            for line in lines:

                stripped = line.strip()

                if not stripped:

                    metrics["blank_lines"] += 1

                    continue

                if stripped.startswith("#"):

                    metrics["comment_lines"] += 1

                if stripped.startswith("class "):

                    metrics["classes"] += 1

                if stripped.startswith("def "):

                    metrics["functions"] += 1

                if (
                    stripped.startswith("import ")
                    or stripped.startswith("from ")
                ):

                    metrics["imports"] += 1

        metrics["code_lines"] = (
            metrics["lines_of_code"]
            - metrics["blank_lines"]
            - metrics["comment_lines"]
        )

        return metrics

