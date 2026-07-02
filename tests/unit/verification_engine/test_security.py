"""
Unit tests for the Verification Engine security scanner.
"""

from pathlib import Path

from core.verification_engine.security import SecurityScanner


def test_security_scan_clean_project(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()

    (project / "main.py").write_text(
        "def hello(name: str) -> str:\n    return f'Hello {name}'\n",
        encoding="utf-8",
    )

    result = SecurityScanner().run(project)

    assert result.name == "security"
    assert result.duration >= 0
    assert "returncode" in result.details


def test_security_scan_detects_issue(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()

    (project / "main.py").write_text(
        "import subprocess\nsubprocess.Popen('ls', shell=True)\n",
        encoding="utf-8",
    )

    result = SecurityScanner().run(project)

    assert result.name == "security"
    assert not result.success
