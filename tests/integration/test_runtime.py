"""
Integration tests for the AI-OS Runtime Engine.
"""

from core.runtime.engine import RuntimeEngine
from core.runtime.scheduler import RuntimeScheduler


def test_runtime_runs_single_iteration(tmp_path):
    scheduler = RuntimeScheduler(
        max_iterations=1,
    )

    engine = RuntimeEngine(
        project_root=tmp_path,
        scheduler=scheduler,
    )

    result = engine.run()

    assert result.success
    assert result.iterations_completed == 1
    assert result.context is not None


def test_runtime_runs_multiple_iterations(tmp_path):
    scheduler = RuntimeScheduler(
        max_iterations=3,
    )

    engine = RuntimeEngine(
        project_root=tmp_path,
        scheduler=scheduler,
    )

    result = engine.run()

    assert result.success
    assert result.iterations_completed == 3


def test_runtime_creates_reports(tmp_path):
    scheduler = RuntimeScheduler(
        max_iterations=1,
    )

    engine = RuntimeEngine(
        project_root=tmp_path,
        scheduler=scheduler,
    )

    engine.run()

    report_dir = (
        tmp_path
        / "output"
        / "runtime"
    )

    assert (
        report_dir
        / "runtime.json"
    ).exists()

    assert (
        report_dir
        / "runtime.md"
    ).exists()


def test_runtime_preserves_project_root(tmp_path):
    engine = RuntimeEngine(tmp_path)

    result = engine.run()

    assert result.context.project_root == str(tmp_path)


def test_runtime_duration_recorded(tmp_path):
    engine = RuntimeEngine(tmp_path)

    result = engine.run()

    assert result.duration_seconds >= 0.0


def test_runtime_stop_reason_exists(tmp_path):
    engine = RuntimeEngine(tmp_path)

    result = engine.run()

    assert result.stopped_reason != ""