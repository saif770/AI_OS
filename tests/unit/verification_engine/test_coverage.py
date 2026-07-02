"""
Unit tests for the Verification Engine coverage runner.
"""

from pathlib import Path

from core.verification_engine.coverage import CoverageRunner


def test_coverage_success(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()

    (project / "main.py").write_text(
        "def add(a, b):\n    return a + b\n",
        encoding="utf-8",
    )

    (project / "test_main.py").write_text(
        """
from main import add

def test_add():
    assert add(2, 3) == 5
""",
        encoding="utf-8",
    )

    result = CoverageRunner().run(project)

    assert result.name == "coverage"
    assert result.duration >= 0
    assert "returncode" in result.details


def test_coverage_failure(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()

    (project / "test_failure.py").write_text(
        """
def test_failure():
    assert False
""",
        encoding="utf-8",
    )

    result = CoverageRunner().run(project)

    assert result.name == "coverage"
    assert not result.success
