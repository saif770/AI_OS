"""
Shared pytest fixtures for AI_OS integration tests.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------
# Ensure the project root is importable
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------
# Project imports
# ---------------------------------------------------------------------

from bootstrap import BootstrapEngine

from core.project_intelligence.analyzer import ProjectAnalyzer
from core.planning_engine.engine import PlanningEngine


# ---------------------------------------------------------------------
# Common Fixtures
# ---------------------------------------------------------------------

@pytest.fixture(scope="session")
def project_root() -> Path:
    """
    Return the AI_OS project root.
    """
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def bootstrap_engine() -> BootstrapEngine:
    """
    Create and execute the Bootstrap Engine once.
    """
    engine = BootstrapEngine()
    engine.run()
    return engine


@pytest.fixture(scope="session")
def bootstrap_context(bootstrap_engine):
    """
    Return the populated BootstrapContext.
    """
    return bootstrap_engine.context


@pytest.fixture(scope="session")
def project_intelligence(project_root: Path):
    """
    Execute Project Intelligence once.
    """
    analyzer = ProjectAnalyzer(project_root)
    return analyzer.analyze()


@pytest.fixture(scope="session")
def planning_engine(project_root: Path):
    """
    Return a PlanningEngine instance.
    """
    return PlanningEngine(project_root)


@pytest.fixture(scope="session")
def planning_result(
    planning_engine: PlanningEngine,
    project_root: Path,
    project_intelligence: dict,
):
    """
    Execute the Planning Engine once.
    """
    return planning_engine.run(
        project_name=project_root.name,
        intelligence=project_intelligence,
    )

