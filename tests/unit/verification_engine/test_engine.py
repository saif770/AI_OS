"""
Unit tests for the Verification Engine.
"""

from pathlib import Path

from core.verification_engine.engine import VerificationEngine


def test_engine_run(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()

    (project / "main.py").write_text(
        "print('hello')\n",
        encoding="utf-8",
    )

    engine = VerificationEngine(project)

    report = engine.run()

    assert report.project_name == "project"
    assert report.total_checks == len(report.results)
    assert report.passed + report.failed == report.total_checks

    assert (
        project
        / "output"
        / "verification_report.json"
    ).exists()


def test_engine_returns_report(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()

    engine = VerificationEngine(project)

    report = engine.run()

    assert hasattr(report, "success_rate")
    assert isinstance(report.success_rate, float)
