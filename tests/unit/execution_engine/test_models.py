"""
Unit tests for execution_engine.models.
"""

from datetime import datetime, UTC, UTC

from core.execution_engine.models import (
    CodePatch,
    ExecutionReport,
    ExecutionResult,
    ExecutionTask,
    ValidationResult,
)


def test_execution_task_defaults():
    task = ExecutionTask(
        id="1",
        title="Demo",
        description="Demo task",
    )

    assert task.priority == 0
    assert task.metadata == {}


def test_validation_result():
    result = ValidationResult(
        passed=True,
        message="OK",
    )

    assert result.passed
    assert result.message == "OK"
    assert result.diagnostics == []


def test_execution_report_success_rate():
    report = ExecutionReport(
        project_name="AI-OS",
        total_tasks=4,
        completed=3,
        failed=1,
    )

    assert report.success_rate == 75.0


def test_execution_result_creation():
    task = ExecutionTask(
        id="2",
        title="Generate",
        description="Create code",
    )

    patch = CodePatch(
        target_file="demo.py",
        description="Demo patch",
        updated="print('demo')",
    )

    validation = ValidationResult(
        passed=True,
        message="Valid",
    )

    result = ExecutionResult(
        task=task,
        success=True,
        validation=validation,
        patches=[patch],
        finished_at=datetime.now(UTC),
    )

    assert result.success
    assert len(result.patches) == 1
    assert result.validation.passed


