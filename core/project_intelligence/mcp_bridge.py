"""
mcp_bridge.py

Bridge between the AI Operating System and MCP servers.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


class MCPBridge:
    """
    Discover and communicate with local MCP servers.
    """

    MCP_CONFIGS = [
        Path.home() / ".claude" / ".mcp.json",
        Path.home() / ".zcode" / "mcp.json",
        Path.home() / ".cursor" / ".mcp.json",
        Path.home() / ".vscode" / ".mcp.json",
    ]

    def __init__(self, project_root: Path):

        self.project_root = Path(project_root)

    # -------------------------------------------------------------

    def analyze(self) -> dict:

        info = {
            "node": shutil.which("node"),
            "npm": shutil.which("npm"),
            "npx": shutil.which("npx"),
            "codebase_memory_mcp": shutil.which(
                "codebase-memory-mcp"
            ),
            "configs": [],
            "servers": [],
            "available": False,
        }

        info["available"] = (
            info["codebase_memory_mcp"] is not None
        )

        for config in self.MCP_CONFIGS:

            if not config.exists():

                continue

            info["configs"].append(str(config))

            try:

                data = json.loads(
                    config.read_text(
                        encoding="utf-8"
                    )
                )

            except Exception:

                continue

            servers = data.get("servers", {})

            if isinstance(servers, dict):

                info["servers"].extend(
                    servers.keys()
                )

        info["servers"] = sorted(
            set(info["servers"])
        )

        return info

    # -------------------------------------------------------------

    def index_project(self) -> bool:
        """
        Index the current project using codebase-memory-mcp.
        """

        executable = shutil.which(
            "codebase-memory-mcp"
        )

        if executable is None:

            return False

        try:

            process = subprocess.run(
                [
                    executable,
                    "index",
                    str(self.project_root),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            return process.returncode == 0

        except Exception:

            return False

    # -------------------------------------------------------------

    def search_graph(
        self,
        query: str,
    ) -> str | None:
        """
        Search the indexed project graph.
        """

        executable = shutil.which(
            "codebase-memory-mcp"
        )

        if executable is None:

            return None

        try:

            process = subprocess.run(
                [
                    executable,
                    "search_graph",
                    query,
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            if process.returncode != 0:

                return None

            return process.stdout

        except Exception:

            return None

