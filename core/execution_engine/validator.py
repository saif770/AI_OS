"""
Validator for the AI_OS Execution Engine.

Performs lightweight validation of generated patches and files.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .models import CodePatch, ValidationResult


@dataclass(slots=True)
class Validator:
    """
    Validates generated code and applied patches.
    """

    def validate_patch(self, patch: CodePatch) -> ValidationResult:
        if not patch.updated.strip():
            return ValidationResult(
                passed=False,
                message="Generated patch is empty.",
            )

        return ValidationResult(
            passed=True,
            message="Patch validation passed.",
        )

    def validate_file(self, file_path: Path) -> ValidationResult:
        path = Path(file_path)

        if not path.exists():
            return ValidationResult(
                passed=False,
                message=f"Missing file: {path}",
            )

        if path.stat().st_size == 0:
            return ValidationResult(
                passed=False,
                message=f"Empty file: {path}",
            )

        return ValidationResult(
            passed=True,
            message="File validation passed.",
        )

    def validate_all(
        self,
        patches: list[CodePatch],
    ) -> list[ValidationResult]:
        return [self.validate_patch(patch) for patch in patches]


