"""
report.py

Generate Project Intelligence reports.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


class ProjectReport:
    """
    Generate project intelligence reports.
    """

    OUTPUT_DIRECTORY = ".bootstrap"

    def __init__(self, project_root: Path):

        self.project_root = Path(project_root)

        self.output_directory = (
            self.project_root / self.OUTPUT_DIRECTORY
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # -------------------------------------------------------------

    def generate(
        self,
        data: dict,
    ) -> dict:

        report = {
            "generated_at": datetime.now().isoformat(),
            "project": self.project_root.name,
            "root": str(self.project_root),
            "intelligence": data,
        }

        self._write_json(
            "PROJECT_OVERVIEW.json",
            report,
        )

        self._write_markdown(
            "PROJECT_CONTEXT.md",
            report,
        )

        return report

    # -------------------------------------------------------------

    def _write_json(
        self,
        filename: str,
        data: dict,
    ) -> None:

        path = self.output_directory / filename

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
            )

    # -------------------------------------------------------------

    def _write_markdown(
        self,
        filename: str,
        report: dict,
    ) -> None:

        path = self.output_directory / filename

        intelligence = report["intelligence"]

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:

            file.write("# Project Intelligence Report\n\n")

            file.write(
                f"Generated: {report['generated_at']}\n\n"
            )

            for section, value in intelligence.items():

                file.write(
                    f"## {section.replace('_', ' ').title()}\n\n"
                )

                if isinstance(value, dict):

                    for key, item in value.items():

                        file.write(
                            f"- **{key}**: {item}\n"
                        )

                elif isinstance(value, list):

                    for item in value:

                        file.write(f"- {item}\n")

                else:

                    file.write(f"{value}\n")

                file.write("\n")

    # -------------------------------------------------------------

    def output_files(self) -> dict:

        return {
            "json": str(
                self.output_directory
                / "PROJECT_OVERVIEW.json"
            ),
            "markdown": str(
                self.output_directory
                / "PROJECT_CONTEXT.md"
            ),
        }