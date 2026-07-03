"""
Unit tests for Orchestrator models.
"""

from core.orchestrator.models import (
    PipelineContext,
    PipelineResult,
)


def test_pipeline_context_defaults():
    context = PipelineContext(
        project_root="C:/AI-OS"
    )

    assert context.project_root == "C:/AI-OS"

    assert context.project_intelligence is None
    assert context.planning_report is None
    assert context.execution_report is None
    assert context.verification_report is None
    assert context.reflection_report is None
    assert context.improvement_report is None
    assert context.memory_report is None


def test_pipeline_result_success():
    result = PipelineResult(
        success=True,
        completed_steps=[
            "planning",
            "execution",
        ],
        duration_seconds=3.5,
    )

    assert result.success
    assert result.failed_step is None
    assert len(result.completed_steps) == 2


def test_pipeline_result_failure():
    result = PipelineResult(
        success=False,
        completed_steps=["planning"],
        failed_step="execution",
        message="Execution failed",
    )

    assert not result.success
    assert result.failed_step == "execution"
    assert result.message == "Execution failed"