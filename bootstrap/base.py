"""
bootstrap/base.py

Base class for every Bootstrap stage.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .result import BootstrapResult


class BootstrapStage(ABC):
    """
    Base class for all bootstrap stages.
    """

    # ------------------------------------------------------------------
    # Stage Metadata
    # ------------------------------------------------------------------

    name: str = "Unnamed Stage"

    description: str = ""

    order: int = 0

    enabled: bool = True

    skippable: bool = False

    retry_count: int = 0

    # ------------------------------------------------------------------

    def __init__(self, context):

        self.context = context

    # ------------------------------------------------------------------

    @abstractmethod
    def execute(self) -> BootstrapResult:
        """
        Stage implementation.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------

    def before_execute(self):

        print(f"\n[{self.name}] Starting...")

    # ------------------------------------------------------------------

    def after_execute(self, result: BootstrapResult):

        print(f"[{self.name}] Finished ({result.status})")

        return result

    # ------------------------------------------------------------------

    def should_skip(self) -> bool:

        return False

    # ------------------------------------------------------------------

    def run(self) -> BootstrapResult:

        result = BootstrapResult(self.name)

        if not self.enabled:

            result.set_status("DISABLED")

            return result.finish()

        if self.should_skip():

            result.set_status("SKIPPED")

            result.add_warning("Stage skipped.")

            return result.finish()

        try:

            self.before_execute()

            result = self.execute()

            result = self.after_execute(result)

        except Exception as e:

            result.add_error(str(e))

        return result.finish()

    # ------------------------------------------------------------------

    def __repr__(self):

        return (
            f"<{self.__class__.__name__}"
            f" name='{self.name}'"
            f" order={self.order}"
            f">"
        )