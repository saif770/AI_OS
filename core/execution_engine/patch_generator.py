"""
Patch Generator for the AI_OS Execution Engine.

Converts generated code into one or more executable patches.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .code_generator import GeneratedCode
from .models import CodePatch


@dataclass(slots=True)
class PatchBundle:
    """Collection of patches produced for a task."""

    patches: list[CodePatch] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.patches)


class PatchGenerator:
    """
    Generates patch bundles from generated code.
    """

    def generate(
        self,
        generated: GeneratedCode,
    ) -> PatchBundle:

        patch = CodePatch(
            target_file=generated.filename,
            description=generated.explanation or "Generated code patch",
            original="",
            updated=generated.source,
        )

        return PatchBundle(patches=[patch])


