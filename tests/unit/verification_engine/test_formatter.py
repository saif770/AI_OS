"""
Unit tests for the Verification Engine formatter.
"""

from pathlib import Path

from core.verification_engine.formatter import Formatter


def test_formatter_valid_project(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()

    (project / "main.py").write_text(
        "def hello() -> None:\n    print('hello')\n",
        encoding="utf-8",
    )

    result = Formatter().run(project)

    assert result.name == "formatter"
    assert result.duration >= 0
    assert "returncode" in result.details


def test_formatter_detects_unformatted_code(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()

    (project / "main.py").write_text(
        "def hello():print('hello')\n",
        encoding="utf-8",
    )

    result = Formatter().run(project)

    assert result.name == "formatter"
    assert not result.success
