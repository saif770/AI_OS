"""
Prompt Builder for the AI_OS Execution Engine.

Converts planning tasks into structured prompts suitable for LLMs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .models import ExecutionTask


@dataclass(slots=True)
class PromptBuilder:
    """Build prompts for execution tasks."""

    system_prompt: str = (
        "You are an expert software engineer. "
        "Produce safe, minimal, tested code changes."
    )

    def build(self, task: ExecutionTask) -> str:
        return (
            f"{self.system_prompt}\n\n"
            f"Task: {task.title}\n"
            f"Description: {task.description}\n"
            f"Priority: {task.priority}\n"
        )

    def build_batch(self, tasks: Iterable[ExecutionTask]) -> list[str]:
        return [self.build(task) for task in tasks]


