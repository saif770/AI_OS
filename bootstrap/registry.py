"""
bootstrap/registry.py

Stage registry and execution engine.
"""

from __future__ import annotations

from typing import Type

from .base import BootstrapStage
from .context import BootstrapContext
from .result import BootstrapResult


class StageRegistry:
    """
    Registers and executes bootstrap stages.
    """

    def __init__(self) -> None:

        self._stages: list[Type[BootstrapStage]] = []

    # -------------------------------------------------------------

    def register(self, stage: Type[BootstrapStage]) -> None:
        """
        Register a stage class.
        """

        if stage not in self._stages:
            self._stages.append(stage)

    # -------------------------------------------------------------

    def unregister(self, stage: Type[BootstrapStage]) -> None:
        """
        Remove a registered stage.
        """

        if stage in self._stages:
            self._stages.remove(stage)

    # -------------------------------------------------------------

    def clear(self) -> None:
        """
        Remove all registered stages.
        """

        self._stages.clear()

    # -------------------------------------------------------------

    @property
    def stages(self) -> list[Type[BootstrapStage]]:
        """
        Return registered stages sorted by execution order.
        """

        return sorted(
            self._stages,
            key=lambda stage: stage.order,
        )

    # -------------------------------------------------------------

    def run(
        self,
        context: BootstrapContext,
    ) -> list[BootstrapResult]:
        """
        Execute every registered stage.
        """

        results: list[BootstrapResult] = []

        for stage_class in self.stages:

            stage = stage_class(context)

            result = stage.run()

            context.add_result(result)

            results.append(result)

        return results

    # -------------------------------------------------------------

    def __len__(self) -> int:

        return len(self._stages)

    # -------------------------------------------------------------

    def __iter__(self):

        return iter(self.stages)

    # -------------------------------------------------------------

    def __contains__(self, stage: Type[BootstrapStage]) -> bool:

        return stage in self._stages

    # -------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"<StageRegistry stages={len(self._stages)}>"
        )

