"""
Unit tests for the Execution Engine validator.
"""

from pathlib import Path

from core.execution_engine.models import CodePatch
from core.execution_engine.validator import Validator


def test_validate_patch_success():
    validator = Validator()

    patch = CodePatch(
        target_file=Path("example.py"),
        description="Example",
        updated="print('ok')\n",
    )

    result = validator.validate_patch(patch)

    assert result.passed


def test_validate_patch_failure():
    validator = Validator()

    patch = CodePatch(
        target_file=Path("example.py"),
        description="Empty",
        updated="",
    )

    result = validator.validate_patch(patch)

    assert not result.passed


