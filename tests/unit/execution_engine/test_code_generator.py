"""
Unit tests for the CodeGenerator.
"""

from core.execution_engine.code_generator import (
    CodeGenerator,
    GeneratedCode,
)
from core.execution_engine.llm_client import LLMResponse


def test_generate_code_success():
    generator = CodeGenerator()

    response = LLMResponse(
        success=True,
        content="print('hello')\n",
    )

    generated = generator.generate(
        response=response,
        filename="hello.py",
    )

    assert isinstance(generated, GeneratedCode)
    assert generated.filename == "hello.py"
    assert "print" in generated.source


def test_generate_code_failure():
    generator = CodeGenerator()

    response = LLMResponse(
        success=False,
        content="",
        error="Generation failed",
    )

    try:
        generator.generate(
            response=response,
            filename="bad.py",
        )
        assert False, "Expected RuntimeError"
    except RuntimeError as exc:
        assert "Generation failed" in str(exc)


def test_generate_patch():
    generator = CodeGenerator()

    generated = GeneratedCode(
        filename="demo.py",
        source="print('demo')\n",
        explanation="Demo file",
    )

    patch = generator.to_patch(generated)

    assert patch.target_file == "demo.py"
    assert "demo" in patch.updated


