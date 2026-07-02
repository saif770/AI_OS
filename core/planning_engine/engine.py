"""
engine.py

Main orchestrator for the Planning Engine.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .dependency_graph import DependencyGraph
from .planner import Planner
from .prioritizer import Prioritizer
from .report import PlanningReport
from .risk_analyzer import RiskAnalyzer
from .roadmap import RoadmapBuilder
from .work_breakdown import WorkBreakdown


class PlanningEngine:
    """
    Execute the complete planning workflow.
    """

    def __init__(self, project_root: str | Path):

        self.project_root = Path(project_root)

        self.planner = Planner()
        self.prioritizer = Prioritizer()
        self.breakdown = WorkBreakdown()
        self.graph = DependencyGraph()
        self.risks = RiskAnalyzer()
        self.roadmap_builder = RoadmapBuilder()
        self.reporter = PlanningReport(self.project_root)

    # ---------------------------------------------------------

    def run(
        self,
        project_name: str,
        intelligence: dict[str, Any],
    ):

        planning = self.planner.create_plan(
            project_name,
            intelligence,
        )

        tasks = []

        for milestone in planning.roadmap.milestones:
            tasks.extend(milestone.tasks)

        tasks = self.breakdown.breakdown(tasks)
        tasks = self.prioritizer.prioritize(tasks)

        planning.roadmap = self.roadmap_builder.build(tasks)

        execution_order = self.graph.execution_order(tasks)
        planning.metadata["execution_order"] = execution_order

        self.risks.analyze(planning.roadmap)

        outputs = self.reporter.generate(planning)
        planning.metadata["reports"] = outputs

        return planning

    # ---------------------------------------------------------

    def summary(self, planning):

        print("=" * 60)
        print("Planning Engine")
        print("=" * 60)

        total_tasks = sum(
            len(m.tasks)
            for m in planning.roadmap.milestones
        )

        print(f"Project      : {planning.project_name}")
        print(f"Milestones   : {len(planning.roadmap.milestones)}")
        print(f"Tasks        : {total_tasks}")
        print(f"Risks        : {len(planning.roadmap.risks)}")

        reports = planning.metadata.get("reports", {})

        if reports:
            print("\nGenerated Reports:")
            for name, path in reports.items():
                print(f"  {name:<10} {path}")

        print("=" * 60)


