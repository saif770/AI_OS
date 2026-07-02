"""
Unit tests for the ExecutionEngine.
"""

from pathlib import Path

from core.execution_engine.engine import ExecutionEngine
from core.execution_engine.llm_client import LLMClient, LLMResponse
from core.execution_engine.models import ExecutionTask


class FakeLLMClient(LLMClient):
    """Mock LLM client for unit tests."""

    def generate(self, prompt: str, **kwargs):
        return LLMResponse(
            success=True,
            content="print('generated')\n",
        )


def test_execute_single_task(tmp_path: Path):
    engine = ExecutionEngine(
        project_root=tmp_path,
        llm_client=FakeLLMClient(),
    )

    report = engine.execute([
        ExecutionTask(
            id="1",
            title="Generate",
            description="Create file",
            priority=1,
        )
    ])

    assert report.total_tasks == 1
    assert report.completed == 1
    assert report.failed == 0


def test_execute_empty_task_list(tmp_path: Path):
    engine = ExecutionEngine(
        project_root=tmp_path,
        llm_client=FakeLLMClient(),
    )

    report = engine.execute([])

    assert report.total_tasks == 0
    assert report.completed == 0
    assert report.failed == 0


