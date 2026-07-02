"""
Unit tests for the PromptBuilder.
"""

from core.execution_engine.models import ExecutionTask
from core.execution_engine.prompt_builder import PromptBuilder


def test_build_single_prompt():
    builder = PromptBuilder()

    task = ExecutionTask(
        id="1",
        title="Create API",
        description="Implement a REST endpoint.",
        priority=2,
    )

    prompt = builder.build(task)

    assert "Create API" in prompt
    assert "Implement a REST endpoint." in prompt
    assert "Priority: 2" in prompt


def test_build_batch():
    builder = PromptBuilder()

    tasks = [
        ExecutionTask(
            id="1",
            title="Task A",
            description="First",
        ),
        ExecutionTask(
            id="2",
            title="Task B",
            description="Second",
        ),
    ]

    prompts = builder.build_batch(tasks)

    assert len(prompts) == 2
    assert "Task A" in prompts[0]
    assert "Task B" in prompts[1]


