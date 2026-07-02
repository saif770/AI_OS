"""
Unit tests for the PatchGenerator.
"""

from core.execution_engine.code_generator import GeneratedCode
from core.execution_engine.patch_generator import (
    PatchBundle,
    PatchGenerator,
)


def test_generate_patch_bundle():
    generator = PatchGenerator()

    generated = GeneratedCode(
        filename="sample.py",
        source="print('sample')\n",
        explanation="Generated sample",
    )

    bundle = generator.generate(generated)

    assert isinstance(bundle, PatchBundle)
    assert bundle.count == 1

    patch = bundle.patches[0]

    assert patch.target_file == "sample.py"
    assert "sample" in patch.updated


def test_patch_bundle_count():
    generator = PatchGenerator()

    generated = GeneratedCode(
        filename="example.py",
        source="pass\n",
    )

    bundle = generator.generate(generated)

    assert len(bundle.patches) == bundle.count


