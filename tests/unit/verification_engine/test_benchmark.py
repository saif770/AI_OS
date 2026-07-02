"""
Unit tests for the Verification Engine benchmark runner.
"""

from pathlib import Path

from core.verification_engine.benchmark import BenchmarkRunner


def test_benchmark_runner_executes(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()

    (project / "test_sample.py").write_text(
        """
def test_example():
    assert True
""",
        encoding="utf-8",
    )

    result = BenchmarkRunner().run(project)

    assert result.name == "benchmark"
    assert result.duration >= 0
    assert "returncode" in result.details


def test_benchmark_runner_failure(tmp_path: Path):
    project = tmp_path / "project"
    project.mkdir()

    (project / "test_failure.py").write_text(
        """
def test_failure():
    assert False
""",
        encoding="utf-8",
    )

    result = BenchmarkRunner().run(project)

    assert result.name == "benchmark"
    assert not result.success
