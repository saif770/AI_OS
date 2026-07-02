"""
Unit tests for the Verification Engine linter.
"""

from pathlib import Path

from core.verification_engine.linter import Linter


def test_linter_valid_file(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()

    (project / "main.py").write_text(
        "def hello() -> None:\n    return\n",
        encoding="utf-8",
    )

    result = Linter().run(project)

    assert result.name == "linter"
    assert result.duration >= 0
    assert "returncode" in result.details


def test_linter_invalid_file(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()

    (project / "main.py").write_text(
        "import os\nimport os\n",
        encoding="utf-8",
    )

    result = Linter().run(project)

    assert result.name == "linter"
    assert not result.success
