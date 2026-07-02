"""
report.py

Generate planning reports.
"""

from __future__ import annotations

import json
from pathlib import Path

from .models import PlanningResult


class PlanningReport:
    """
    Generate planning artifacts.
    """

    def __init__(self, project_root: Path):

        self.project_root = Path(project_root)

        self.output_dir = (
            self.project_root / ".bootstrap"
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ---------------------------------------------------------

    def generate(
        self,
        result: PlanningResult,
    ) -> dict:

        self._write_tasks(result)
        self._write_plan(result)
        self._write_roadmap(result)
        self._write_risks(result)

        return {
            "tasks": str(self.output_dir / "TASKS.json"),
            "plan": str(self.output_dir / "PLAN.md"),
            "roadmap": str(self.output_dir / "ROADMAP.md"),
            "risks": str(self.output_dir / "RISKS.md"),
        }

    # ---------------------------------------------------------

    def _write_tasks(self, result: PlanningResult):

        tasks = []

        for milestone in result.roadmap.milestones:
            for task in milestone.tasks:
                tasks.append({
                    "id": task.id,
                    "title": task.title,
                    "priority": task.priority.value,
                    "status": task.status.value,
                    "estimated_hours": task.estimated_hours,
                    "dependencies": task.dependencies,
                    "tags": task.tags,
                })

        path = self.output_dir / "TASKS.json"

        path.write_text(
            json.dumps(tasks, indent=4),
            encoding="utf-8",
        )

    # ---------------------------------------------------------

    def _write_plan(self, result: PlanningResult):

        path = self.output_dir / "PLAN.md"

        lines = [
            "# Project Plan",
            "",
            f"Project: {result.project_name}",
            "",
        ]

        for milestone in result.roadmap.milestones:

            lines.append(f"## {milestone.name}")
            lines.append("")

            for task in milestone.tasks:
                lines.append(
                    f"- [{task.priority.value}] {task.title}"
                )

            lines.append("")

        path.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

    # ---------------------------------------------------------

    def _write_roadmap(self, result: PlanningResult):

        path = self.output_dir / "ROADMAP.md"

        lines = [
            "# Roadmap",
            "",
        ]

        for index, milestone in enumerate(
            result.roadmap.milestones,
            start=1,
        ):

            lines.append(
                f"## Phase {index}: {milestone.name}"
            )

            lines.append("")

            for task in milestone.tasks:
                lines.append(f"- {task.title}")

            lines.append("")

        path.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

    # ---------------------------------------------------------

    def _write_risks(self, result: PlanningResult):

        path = self.output_dir / "RISKS.md"

        lines = [
            "# Risks",
            "",
        ]

        if not result.roadmap.risks:
            lines.append("No risks detected.")
        else:
            for risk in result.roadmap.risks:
                lines.append(
                    f"- [{risk.severity.value}] {risk.title}"
                )
                if risk.mitigation:
                    lines.append(
                        f"  - Mitigation: {risk.mitigation}"
                    )

        path.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )


