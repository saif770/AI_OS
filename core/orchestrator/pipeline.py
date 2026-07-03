"""
Orchestrator pipeline definition.

Defines the execution order of AI-OS engines.
The Pipeline contains no execution logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from .models import PipelineContext


@dataclass(slots=True)
class PipelineStep:
    """
    Represents one pipeline stage.
    """

    name: str

    executor: Callable[[PipelineContext], object]


@dataclass(slots=True)
class Pipeline:
    """
    Ordered AI-OS execution pipeline.
    """

    steps: list[PipelineStep] = field(
        default_factory=list
    )

    def add_step(
        self,
        name: str,
        executor: Callable[[PipelineContext], object],
    ) -> None:
        """
        Register a pipeline step.
        """

        self.steps.append(
            PipelineStep(
                name=name,
                executor=executor,
            )
        )

    def names(self) -> list[str]:
        """
        Return the ordered step names.
        """

        return [
            step.name
            for step in self.steps
        ]

    def __len__(self) -> int:
        return len(self.steps)

    def __iter__(self):
        return iter(self.steps)

    @classmethod
    def default(cls) -> "Pipeline":
        """
        Create an empty default pipeline.

        The Orchestrator engine is responsible
        for registering the actual engine
        implementations.
        """

        return cls()