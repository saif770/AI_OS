"""
Shared pytest fixtures for the Verification Engine unit tests.
"""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def project_dir(tmp_path: Path) -> Path:
    """Create an empty project directory."""
    project = tmp_path / "project"
    project.mkdir()
    return project


@pytest.fixture
def valid_python_file(project_dir: Path) -> Path:
    """Create a valid Python source file."""
    path = project_dir / "main.py"
    path.write_text(
        "def hello() -> str:\n"
        "    return 'hello'\n",
        encoding="utf-8",
    )
    return path


@pytest.fixture
def invalid_python_file(project_dir: Path) -> Path:
    """Create an invalid Python source file."""
    path = project_dir / "broken.py"
    path.write_text(
        "def broken(:\n"
        "    pass\n",
        encoding="utf-8",
    )
    return path


@pytest.fixture
def passing_test(project_dir: Path) -> Path:
    """Create a passing pytest test."""
    path = project_dir / "test_sample.py"
    path.write_text(
        "def test_ok():\n"
        "    assert True\n",
        encoding="utf-8",
    )
    return path


@pytest.fixture
def failing_test(project_dir: Path) -> Path:
    """Create a failing pytest test."""
    path = project_dir / "test_failure.py"
    path.write_text(
        "def test_fail():\n"
        "    assert False\n",
        encoding="utf-8",
    )
    return path
