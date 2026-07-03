"""
Runtime scheduler.

Determines whether the Runtime Engine should continue
executing another AI-OS iteration.
"""

from __future__ import annotations

from dataclasses import dataclass

from .models import RuntimeContext


@dataclass(slots=True)
class RuntimeScheduler:
    """
    Controls Runtime iteration flow.
    """

    max_iterations: int = 1

    stop_on_failure: bool = True

    def should_continue(
        self,
        context: RuntimeContext,
    ) -> bool:
        """
        Decide whether another iteration should run.
        """

        if context.iteration >= self.max_iterations:
            return False

        if (
            self.stop_on_failure
            and context.orchestrator_result is not None
            and not context.orchestrator_result.success
        ):
            return False

        return True

    def next_iteration(
        self,
        context: RuntimeContext,
    ) -> RuntimeContext:
        """
        Advance to the next iteration.
        """

        context.iteration += 1

        return context

    def reset(
        self,
        context: RuntimeContext,
    ) -> RuntimeContext:
        """
        Reset runtime state.
        """

        context.iteration = 1
        context.orchestrator_result = None
        context.metadata.clear()

        return context