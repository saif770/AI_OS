"""
Unit tests for the LLMClient abstraction.
"""

from core.execution_engine.llm_client import LLMClient, LLMResponse


class DummyClient(LLMClient):
    def generate(self, prompt: str, **kwargs):
        return LLMResponse(
            success=True,
            content="dummy response",
            raw={"prompt": prompt},
        )


def test_dummy_client_generate():
    client = DummyClient(model="test-model")

    response = client.generate("Hello")

    assert response.success
    assert response.content == "dummy response"
    assert response.raw["prompt"] == "Hello"
    assert client.model == "test-model"


def test_base_client_not_implemented():
    client = LLMClient()

    try:
        client.generate("Hello")
        assert False, "Expected NotImplementedError"
    except NotImplementedError:
        pass


