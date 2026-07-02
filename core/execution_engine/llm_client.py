"""
LLM client abstraction for the AI_OS Execution Engine.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class LLMResponse:
    """Normalized LLM response."""

    success: bool
    content: str
    raw: Any = None
    error: str | None = None


class LLMClient:
    """
    Base LLM client interface.

    Concrete providers should subclass this class and implement
    the generate() method.
    """

    def __init__(self, model: str = "default") -> None:
        self.model = model

    def generate(self, prompt: str, **kwargs: Any) -> LLMResponse:
        """
        Generate code or text from a prompt.

        Override in provider-specific implementations.
        """
        raise NotImplementedError(
            "LLMClient.generate() must be implemented by subclasses."
        )


