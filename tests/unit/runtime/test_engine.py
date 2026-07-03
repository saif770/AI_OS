"""
Unit tests for RuntimeEngine.
"""

from types import SimpleNamespace

from core.runtime.engine import RuntimeEngine
from core.runtime.scheduler import RuntimeScheduler


def test_runtime_single_iteration(tmp_path, monkeypatch):
    engine = RuntimeEngine(tmp_path)

    def fake_run():
        return SimpleNamespace(success=True)

    monkeypatch.setattr(
        engine.orchestrator,
        "run",
        fake_run,
    )

    result = engine.run()

    assert result.success
    assert result.iterations_completed == 1
    assert result.context is not None
    assert result.context.orchestrator_result.success is True


def test_runtime_multiple_iterations(tmp_path, monkeypatch):
    scheduler = RuntimeScheduler(
        max_iterations=3,
    )

    engine = RuntimeEngine(
        tmp_path,
        scheduler=scheduler,
    )

    calls = []

    def fake_run():
        calls.append(1)
        return SimpleNamespace(success=True)

    monkeypatch.setattr(
        engine.orchestrator,
        "run",
        fake_run,
    )

    result = engine.run()

    assert result.success
    assert len(calls) == 3
    assert result.iterations_completed == 3


def test_runtime_stops_on_failure(tmp_path, monkeypatch):
    scheduler = RuntimeScheduler(
        max_iterations=5,
        stop_on_failure=True,
    )

    engine = RuntimeEngine(
        tmp_path,
        scheduler=scheduler,
    )

    calls = []

    def fake_run():
        calls.append(1)

        if len(calls) == 2:
            return SimpleNamespace(success=False)

        return SimpleNamespace(success=True)

    monkeypatch.setattr(
        engine.orchestrator,
        "run",
        fake_run,
    )

    result = engine.run()

    assert not result.success
    assert result.iterations_completed == 2
    assert result.stopped_reason == "Pipeline execution failed."


def test_runtime_reports_created(tmp_path, monkeypatch):
    engine = RuntimeEngine(tmp_path)

    monkeypatch.setattr(
        engine.orchestrator,
        "run",
        lambda: SimpleNamespace(success=True),
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


def test_runtime_context(tmp_path, monkeypatch):
    engine = RuntimeEngine(tmp_path)

    monkeypatch.setattr(
        engine.orchestrator,
        "run",
        lambda: SimpleNamespace(success=True),
    )

    result = engine.run()

    assert result.context.project_root == str(tmp_path)


def test_runtime_duration(tmp_path, monkeypatch):
    engine = RuntimeEngine(tmp_path)

    monkeypatch.setattr(
        engine.orchestrator,
        "run",
        lambda: SimpleNamespace(success=True),
    )

    result = engine.run()

    assert result.duration_seconds >= 0.0


def test_runtime_default_scheduler(tmp_path):
    engine = RuntimeEngine(tmp_path)

    assert isinstance(
        engine.scheduler,
        RuntimeScheduler,
    )