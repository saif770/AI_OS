"""
Unit tests for the Verification Engine compiler.
"""

from pathlib import Path

from core.verification_engine.compiler import Compiler


def test_compile_valid_project(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()

    (project / "main.py").write_text(
        "print('hello')\n",
        encoding="utf-8",
    )

    result = Compiler().run(project)

    assert result.success
    assert result.name == "compiler"
    assert result.duration >= 0


def test_compile_invalid_project(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()

    (project / "broken.py").write_text(
        "def broken(:\n    pass\n",
        encoding="utf-8",
    )

    result = Compiler().run(project)

    assert not result.success
    assert result.name == "compiler"
