"""
bootstrap.py

Main entry point for the AI Operating System Bootstrap Engine.
"""

from __future__ import annotations

from pathlib import Path

from bootstrap.config import BootstrapConfig
from bootstrap.context import BootstrapContext
from bootstrap.registry import StageRegistry

# Bootstrap Stages
from bootstrap.environment import EnvironmentStage
from bootstrap.structure import StructureStage
from bootstrap.dependencies import DependencyStage
from bootstrap.git_setup import GitSetupStage
from bootstrap.verification import VerificationStage
from bootstrap.mcp_setup import MCPSetupStage
from bootstrap.project_scan import ProjectScanStage
from bootstrap.ai_readiness import AIReadinessStage
from bootstrap.report import ReportStage


VERSION = "1.0.0"


def create_context() -> BootstrapContext:
    """
    Create the shared bootstrap context.
    """

    project_root = Path(__file__).resolve().parent

    return BootstrapContext(
        project_root=project_root,
        project_name=project_root.name,
        version=VERSION,
    )


def create_registry() -> StageRegistry:
    """
    Register all bootstrap stages.
    """

    registry = StageRegistry()

    registry.register(EnvironmentStage)
    registry.register(StructureStage)
    registry.register(DependencyStage)
    registry.register(GitSetupStage)
    registry.register(VerificationStage)
    registry.register(MCPSetupStage)
    registry.register(ProjectScanStage)
    registry.register(AIReadinessStage)
    registry.register(ReportStage)

    return registry


def print_header() -> None:

    print("=" * 70)
    print("AI Operating System")
    print(f"Bootstrap Engine v{VERSION}")
    print("=" * 70)


def print_summary(context: BootstrapContext) -> None:

    summary = context.summary()

    print("\n" + "=" * 70)
    print("Execution Summary")
    print("=" * 70)

    print(f"Project        : {summary['project']}")
    print(f"Version        : {summary['version']}")
    print(f"Stages         : {summary['total_stages']}")
    print(f"Successful     : {summary['successful']}")
    print(f"Failed         : {summary['failed']}")
    print("=" * 70)


def main() -> int:

    print_header()

    config = BootstrapConfig()

    context = create_context()

    context.set("config", config)

    registry = create_registry()

    registry.run(context)

    print_summary(context)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())