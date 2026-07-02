"""
engine.py

Reusable Bootstrap Engine.
"""

from __future__ import annotations

from bootstrap.config import BootstrapConfig
from bootstrap.context import BootstrapContext
from bootstrap.registry import StageRegistry

from bootstrap.environment import EnvironmentStage
from bootstrap.structure import StructureStage
from bootstrap.dependencies import DependencyStage
from bootstrap.git_setup import GitSetupStage
from bootstrap.verification import VerificationStage
from bootstrap.mcp_setup import MCPSetupStage
from bootstrap.project_scan import ProjectScanStage
from bootstrap.ai_readiness import AIReadinessStage
from bootstrap.report import ReportStage


class BootstrapEngine:
    """
    Reusable bootstrap engine.

    Executes all bootstrap stages and returns
    the populated BootstrapContext.
    """

    VERSION = "1.0.0"

    def __init__(self):

        self.config = BootstrapConfig()

        self.context = BootstrapContext(
            project_root=self._project_root(),
            project_name=self._project_root().name,
            version=self.VERSION,
        )

        self.context.set(
            "config",
            self.config,
        )

        self.registry = StageRegistry()

        self._register_stages()

    def run(self) -> BootstrapContext:

        self.registry.run(self.context)

        return self.context

    @property
    def summary(self) -> dict:

        return self.context.summary()

    def _register_stages(self):

        self.registry.register(EnvironmentStage)
        self.registry.register(StructureStage)
        self.registry.register(DependencyStage)
        self.registry.register(GitSetupStage)
        self.registry.register(VerificationStage)
        self.registry.register(MCPSetupStage)
        self.registry.register(ProjectScanStage)
        self.registry.register(AIReadinessStage)
        self.registry.register(ReportStage)

    @staticmethod
    def _project_root():

        from pathlib import Path

        return Path(__file__).resolve().parent.parent

