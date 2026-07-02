"""
Unit tests for the PatchApplier.
"""

from pathlib import Path

from core.execution_engine.models import CodePatch
from core.execution_engine.patch_applier import (
    ApplyResult,
    PatchApplier,
)


def test_apply_single_patch(tmp_path: Path):
    applier = PatchApplier()

    patch = CodePatch(
        target_file=tmp_path / "hello.py",
        description="Create hello.py",
        updated="print('hello')\n",
    )

    result = applier.apply(patch)

    assert isinstance(result, ApplyResult)
    assert result.success

    created = tmp_path / "hello.py"

    assert created.exists()
    assert "hello" in created.read_text(encoding="utf-8")


def test_apply_multiple_patches(tmp_path: Path):
    applier = PatchApplier()

    patches = [
        CodePatch(
            target_file=tmp_path / "a.py",
            description="A",
            updated="print('A')\n",
        ),
        CodePatch(
            target_file=tmp_path / "b.py",
            description="B",
            updated="print('B')\n",
        ),
    ]

    results = applier.apply_many(patches)

    assert len(results) == 2
    assert all(r.success for r in results)

    assert (tmp_path / "a.py").exists()
    assert (tmp_path / "b.py").exists()


