"""
planner.py

Planning engine that converts project intelligence into tasks.
"""

from __future__ import annotations

from typing import Any

from .models import PlanningResult, Priority, Roadmap, Milestone
from .task import TaskFactory


class Planner:
    """
    Generate an initial implementation plan from project intelligence.
    """

    def create_plan(
        self,
        project_name: str,
        intelligence: dict[str, Any],
    ) -> PlanningResult:

        roadmap = Roadmap()

        milestone = Milestone(name="Initial Roadmap")

        metrics = intelligence.get("metrics", {})
        git = intelligence.get("git", {})
        mcp = intelligence.get("mcp", {})

        milestone.tasks.append(
            TaskFactory.create(
                "Review project architecture",
                "Understand the detected architecture and entry points.",
                Priority.HIGH,
                2,
            )
        )

        if not git.get("repository", False):
            milestone.tasks.append(
                TaskFactory.create(
                    "Initialize Git repository",
                    "Project is not under Git version control.",
                    Priority.HIGH,
                    1,
                )
            )

        if not mcp.get("available", False):
            milestone.tasks.append(
                TaskFactory.create(
                    "Configure MCP",
                    "Install and configure codebase-memory-mcp.",
                    Priority.HIGH,
                    1,
                )
            )

        if metrics.get("test_files", 0) == 0:
            milestone.tasks.append(
                TaskFactory.create(
                    "Create test suite",
                    "No tests were detected.",
                    Priority.CRITICAL,
                    8,
                )
            )

        roadmap.milestones.append(milestone)

        return PlanningResult(
            project_name=project_name,
            roadmap=roadmap,
            metadata={
                "generated_tasks": len(milestone.tasks),
            },
        )
