"""
Unit tests for MemoryEngine.
"""

from types import SimpleNamespace

from core.memory.engine import MemoryEngine
from core.memory.history import HistoryManager


def create_reflection_report(score: float = 95.0):
    """
    Create a lightweight ReflectionReport stub.
    """
    return SimpleNamespace(
        summary="Reflection completed successfully.",
        score=SimpleNamespace(
            overall_score=score,
        ),
    )


def create_improvement_report():
    """
    Create a lightweight ImprovementReport stub.
    """
    return SimpleNamespace(
        summary="Improvement analysis completed.",
    )


def test_memory_engine_first_run(tmp_path):
    engine = MemoryEngine(tmp_path)

    report = engine.run(
        create_reflection_report(),
        create_improvement_report(),
    )

    assert report.saved is True
    assert report.history.count == 1

    latest = report.history.latest

    assert latest is not None
    assert latest.iteration == 1
    assert latest.overall_score == 95.0


def test_memory_engine_multiple_runs(tmp_path):
    engine = MemoryEngine(tmp_path)

    engine.run(
        create_reflection_report(90.0),
        create_improvement_report(),
    )

    report = engine.run(
        create_reflection_report(100.0),
        create_improvement_report(),
    )

    assert report.history.count == 2

    latest = report.history.latest

    assert latest is not None
    assert latest.iteration == 2
    assert latest.overall_score == 100.0


def test_memory_engine_creates_history_file(tmp_path):
    engine = MemoryEngine(tmp_path)

    engine.run(
        create_reflection_report(),
        create_improvement_report(),
    )

    history_file = (
        tmp_path
        / "memory"
        / "history.json"
    )

    assert history_file.exists()


def test_memory_engine_creates_reports(tmp_path):
    engine = MemoryEngine(tmp_path)

    engine.run(
        create_reflection_report(),
        create_improvement_report(),
    )

    assert (
        tmp_path
        / "memory"
        / "memory.json"
    ).exists()

    assert (
        tmp_path
        / "memory"
        / "memory.md"
    ).exists()


def test_memory_engine_average_score(tmp_path):
    engine = MemoryEngine(tmp_path)

    engine.run(
        create_reflection_report(80.0),
        create_improvement_report(),
    )

    report = engine.run(
        create_reflection_report(100.0),
        create_improvement_report(),
    )

    manager = HistoryManager()

    assert manager.average_score(report.history) == 90.0