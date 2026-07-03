"""
Unit tests for Runtime models.
"""

from core.runtime.models import (
    RuntimeContext,
    RuntimeResult,
)


def test_runtime_context_defaults():
    context = RuntimeContext(
        project_root="C:/AI-OS"
    )

    assert context.project_root == "C:/AI-OS"
    assert context.iteration == 1
    assert context.orchestrator_result is None
    assert context.metadata == {}


def test_runtime_result_success():
    result = RuntimeResult(
        success=True,
        iterations_completed=1,
        stopped_reason="Completed",
        duration_seconds=2.5,
    )

    assert result.success
    assert result.iterations_completed == 1
    assert result.stopped_reason == "Completed"


def test_runtime_result_failure():
    result = RuntimeResult(
        success=False,
        iterations_completed=3,
        stopped_reason="Pipeline failed",
    )

    assert not result.success
    assert result.iterations_completed == 3
    assert result.stopped_reason == "Pipeline failed"