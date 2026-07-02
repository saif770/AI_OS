"""
models.py

Shared data models for the Project Intelligence Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ProjectInfo:
    """
    Basic project information.
    """

    root: Path

    name: str

    language: str = "Unknown"

    framework: str = "Unknown"

    architecture: str = "Unknown"

    entrypoint: str | None = None

    git_enabled: bool = False

    mcp_enabled: bool = False


@dataclass
class ProjectMetrics:
    """
    Repository metrics.
    """

    total_files: int = 0

    python_files: int = 0

    directories: int = 0

    total_lines: int = 0

    total_size_bytes: int = 0

    test_files: int = 0

    documentation_files: int = 0


@dataclass
class DependencyInfo:
    """
    Dependency information.
    """

    package_manager: str = "Unknown"

    dependency_file: str | None = None

    packages: list[str] = field(default_factory=list)


@dataclass
class GitInfo:
    """
    Git repository information.
    """

    enabled: bool = False

    branch: str | None = None

    remote: str | None = None

    latest_commit: str | None = None


@dataclass
class MCPInfo:
    """
    MCP information.
    """

    enabled: bool = False

    indexed: bool = False

    project: str | None = None

    servers: list[str] = field(default_factory=list)


@dataclass
class ProjectReport:
    """
    Final Project Intelligence output.
    """

    project: ProjectInfo

    metrics: ProjectMetrics

    dependencies: DependencyInfo

    git: GitInfo

    mcp: MCPInfo

    metadata: dict[str, Any] = field(default_factory=dict)

