"""
Integration test for Project Intelligence.
"""

from pathlib import Path

from core.project_intelligence.analyzer import ProjectAnalyzer


def test_project_intelligence_runs():
    project_root = Path.cwd()

    analyzer = ProjectAnalyzer(project_root)

    report = analyzer.analyze()

    assert isinstance(report, dict)

    assert "project" in report
    assert "language" in report
    assert "framework" in report
    assert "metrics" in report
    assert "architecture" in report
    assert "mcp" in report

    assert report["project"]["name"] == project_root.name

    assert report["metrics"]["python_files"] >= 0
