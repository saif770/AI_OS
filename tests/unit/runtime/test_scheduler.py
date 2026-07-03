"""
Unit tests for RuntimeScheduler.
"""

from types import SimpleNamespace

from core.runtime.models import RuntimeContext
from core.runtime.scheduler import RuntimeScheduler


def test_scheduler_default_values():
    scheduler = RuntimeScheduler()

    assert scheduler.max_iterations == 1
    assert scheduler.stop_on_failure is True


def test_should_continue_first_iteration():
    scheduler = RuntimeScheduler(
        max_iterations=2,
    )

    context = RuntimeContext(
        project_root="C:/AI-OS",
    )

    assert scheduler.should_continue(context)


def test_should_stop_at_max_iterations():
    scheduler = RuntimeScheduler(
        max_iterations=2,
    )

    context = RuntimeContext(
        project_root="C:/AI-OS",
        iteration=2,
    )

    assert not scheduler.should_continue(context)


def test_should_stop_on_failure():
    scheduler = RuntimeScheduler(
        max_iterations=5,
        stop_on_failure=True,
    )

    context = RuntimeContext(
        project_root="C:/AI-OS",
    )

    context.orchestrator_result = SimpleNamespace(
        success=False,
    )

    assert not scheduler.should_continue(context)


def test_should_continue_when_failure_check_disabled():
    scheduler = RuntimeScheduler(
        max_iterations=5,
        stop_on_failure=False,
    )

    context = RuntimeContext(
        project_root="C:/AI-OS",
    )

    context.orchestrator_result = SimpleNamespace(
        success=False,
    )

    assert scheduler.should_continue(context)


def test_next_iteration():
    scheduler = RuntimeScheduler()

    context = RuntimeContext(
        project_root="C:/AI-OS",
    )

    scheduler.next_iteration(context)

    assert context.iteration == 2


def test_reset():
    scheduler = RuntimeScheduler()

    context = RuntimeContext(
        project_root="C:/AI-OS",
        iteration=5,
    )

    context.metadata["key"] = "value"

    context.orchestrator_result = object()

    scheduler.reset(context)

    assert context.iteration == 1
    assert context.orchestrator_result is None
    assert context.metadata == {}