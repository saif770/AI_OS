"""
Integration tests for the Execution Engine.
"""

from pathlib import Path

from bootstrap import BootstrapEngine

from core.execution_engine.engine import ExecutionEngine
from core.execution_engine.llm_client import LLMClient, LLMResponse
from core.execution_engine.models import ExecutionTask


class MockLLMClient(LLMClient):
    """Simple mock LLM used for integration testing."""

    def generate(self, prompt: str, **kwargs):
        return LLMResponse(
            success=True,
            content='print("AI_OS Execution Engine")\n',
        )


def test_execution_engine(tmp_path: Path):
    BootstrapEngine().run()

    engine = ExecutionEngine(
        project_root=tmp_path,
        llm_client=MockLLMClient(),
    )

    tasks = [
        ExecutionTask(
            id="1",
            title="Generate File",
            description="Create a Python file.",
            priority=1,
        )
    ]

    report = engine.execute(tasks)

    assert report.total_tasks == 1
    assert report.completed == 1
    assert report.failed == 0

    assert (
        tmp_path / "generated.py"
    ).exists()

    assert (
        tmp_path
        / "output"
        / "execution_report.json"
    ).exists()


