"""
Integration test for the Planning Engine.
"""

from pathlib import Path

from core.planning_engine.engine import PlanningEngine
from core.project_intelligence.analyzer import ProjectAnalyzer


def test_planning_engine_runs():
    project_root = Path.cwd()

    intelligence = ProjectAnalyzer(
        project_root
    ).analyze()

    engine = PlanningEngine(project_root)

    planning = engine.run(
        project_name=project_root.name,
        intelligence=intelligence,
    )

    assert planning is not None

    assert planning.project_name == project_root.name

    assert len(planning.roadmap.milestones) > 0

    total_tasks = sum(
        len(milestone.tasks)
        for milestone in planning.roadmap.milestones
    )

    assert total_tasks > 0

    reports = planning.metadata.get(
        "reports",
        {},
    )

    assert "tasks" in reports
    assert "plan" in reports
    assert "roadmap" in reports
    assert "risks" in reports


