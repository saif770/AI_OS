"""
AI Operating System Bootstrap Framework

Core bootstrap package.
"""

from .base import BootstrapStage
from .config import BootstrapConfig
from .context import BootstrapContext
from .registry import StageRegistry
from .result import BootstrapResult

__version__ = "1.0.0"

__all__ = [
    "BootstrapStage",
    "BootstrapConfig",
    "BootstrapContext",
    "StageRegistry",
    "BootstrapResult",
]