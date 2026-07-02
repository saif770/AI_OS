"""
Integration tests for the Verification Engine.
"""

from pathlib import Path

from bootstrap import BootstrapEngine

from core.verification_engine.engine import VerificationEngine


def test_verification_engine(tmp_path: Path):
    BootstrapEngine().run()

    project = tmp_path / "demo_project"
    project.mkdir()

    (project / "hello.py").write_text(
        "print('hello')\n",
        encoding="utf-8",
    )

    engine = VerificationEngine(project)

    report = engine.run()

    assert report.total_checks >= 1
    assert len(report.results) == report.total_checks

    assert (
        project
        / "output"
        / "verification_report.json"
    ).exists()
