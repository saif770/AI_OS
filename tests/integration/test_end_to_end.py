"""
End-to-end integration test for AI_OS.
"""

from pathlib import Path

from bootstrap import BootstrapEngine

from core.project_intelligence.analyzer import ProjectAnalyzer
from core.planning_engine.engine import PlanningEngine


def test_ai_os_end_to_end():

    project_root = Path.cwd()

    # Bootstrap

    engine = BootstrapEngine()

    context = engine.run()

    assert context.summary()["failed"] == 0

    # Project Intelligence

    intelligence = ProjectAnalyzer(
        project_root
    ).analyze()

    assert intelligence["project"]["name"] == project_root.name

    # Planning

    planner = PlanningEngine(project_root)

    planning = planner.run(
        project_name=project_root.name,
        intelligence=intelligence,
    )

    assert planning.project_name == project_root.name

    reports = planning.metadata["reports"]

    for report in reports.values():
        assert Path(report).exists()

