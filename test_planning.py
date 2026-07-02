from pathlib import Path

from core.project_intelligence.analyzer import ProjectAnalyzer
from core.planning_engine.engine import PlanningEngine

project_root = Path.cwd()

print("=" * 60)
print("Running Project Intelligence")
print("=" * 60)

intelligence = ProjectAnalyzer(project_root).analyze()

print("=" * 60)
print("Running Planning Engine")
print("=" * 60)

engine = PlanningEngine(project_root)

planning = engine.run(
    project_name=project_root.name,
    intelligence=intelligence,
)

engine.summary(planning)

print("\nPASS")