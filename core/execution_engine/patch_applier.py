"""
Patch Applier for the AI_OS Execution Engine.

Safely applies generated patches to the project filesystem.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .models import CodePatch


@dataclass(slots=True)
class ApplyResult:
    """Result of applying a patch."""

    success: bool
    target: Path
    message: str = ""


class PatchApplier:
    """
    Applies CodePatch objects to disk.
    """

    def apply(self, patch: CodePatch) -> ApplyResult:
        target = Path(patch.target_file)

        target.parent.mkdir(parents=True, exist_ok=True)

        target.write_text(
            patch.updated,
            encoding="utf-8",
        )

        return ApplyResult(
            success=True,
            target=target,
            message="Patch applied successfully.",
        )

    def apply_many(
        self,
        patches: list[CodePatch],
    ) -> list[ApplyResult]:
        return [self.apply(patch) for patch in patches]


