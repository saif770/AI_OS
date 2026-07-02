"""
bootstrap/mcp_setup.py

MCP discovery and configuration stage.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from .base import BootstrapStage
from .result import BootstrapResult


class MCPSetupStage(BootstrapStage):
    """
    Discover MCP configuration and installed servers.
    """

    name = "MCP Setup"

    order = 60

    MCP_CONFIGS = [
        Path.home() / ".claude" / ".mcp.json",
        Path.home() / ".cursor" / ".mcp.json",
        Path.home() / ".vscode" / ".mcp.json",
        Path.home() / ".zcode" / "mcp.json",
        Path.home() / ".hermes" / "mcp.json",
    ]

    def execute(self) -> BootstrapResult:

        result = BootstrapResult(self.name)

        node = shutil.which("node")
        npm = shutil.which("npm")
        npx = shutil.which("npx")

        codebase_memory = shutil.which("codebase-memory-mcp")

        found_configs = []

        for config in self.MCP_CONFIGS:

            if config.exists():

                found_configs.append(str(config))

        result.update(
            node=node,
            npm=npm,
            npx=npx,
            codebase_memory_mcp=codebase_memory,
            configuration_files=found_configs,
            configuration_count=len(found_configs),
            node_installed=node is not None,
            npm_installed=npm is not None,
            npx_installed=npx is not None,
            codebase_memory_installed=codebase_memory is not None,
        )

        self.context.set(
            "node",
            node,
        )

        self.context.set(
            "npm",
            npm,
        )

        self.context.set(
            "npx",
            npx,
        )

        self.context.set(
            "codebase_memory_mcp",
            codebase_memory,
        )

        self.context.set(
            "mcp_configs",
            found_configs,
        )

        return result

