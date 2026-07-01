"""
bootstrap/ai_readiness.py

AI readiness analysis stage.
"""

from __future__ import annotations

from pathlib import Path

from .base import BootstrapStage
from .result import BootstrapResult


class AIReadinessStage(BootstrapStage):
    """
    Analyze whether the project is ready for AI agents.
    """

    name = "AI Readiness"

    order = 80

    REQUIRED_ITEMS = [
        "README.md",
        "requirements.txt",
        "bootstrap.py",
        "bootstrap",
        "config",
        "docs",
    ]

    def execute(self) -> BootstrapResult:

        result = BootstrapResult(self.name)

        project_root = self.context.project_root

        existing = []
        missing = []

        score = 0

        # ---------------------------------------------------------
        # Check required project items
        # ---------------------------------------------------------

        for item in self.REQUIRED_ITEMS:

            path = project_root / item

            if path.exists():

                existing.append(item)

                score += 1

            else:

                missing.append(item)

        # ---------------------------------------------------------
        # Python source analysis
        # ---------------------------------------------------------

        python_files = self.context.get(
            "python_files",
            [],
        )

        total_python_files = len(python_files)

        # ---------------------------------------------------------
        # MCP availability
        # ---------------------------------------------------------

        mcp_available = (
            self.context.get(
                "codebase_memory_mcp"
            )
            is not None
        )

        if mcp_available:

            score += 2

        # ---------------------------------------------------------
        # Git availability
        # ---------------------------------------------------------

        git_available = self.context.get(
            "git_installed",
            False,
        )

        if git_available:

            score += 1

        # ---------------------------------------------------------
        # Calculate readiness
        # ---------------------------------------------------------

        maximum_score = len(self.REQUIRED_ITEMS) + 3

        readiness = round(
            (score / maximum_score) * 100,
            2,
        )

        if readiness >= 90:

            status = "Excellent"

        elif readiness >= 75:

            status = "Good"

        elif readiness >= 50:

            status = "Fair"

        else:

            status = "Poor"

        # ---------------------------------------------------------

        result.update(

            readiness_score=readiness,

            readiness_status=status,

            maximum_score=maximum_score,

            achieved_score=score,

            existing_items=existing,

            missing_items=missing,

            python_files=total_python_files,

            git_available=git_available,

            mcp_available=mcp_available,

        )

        self.context.set(
            "ai_readiness",
            readiness,
        )

        self.context.set(
            "ai_status",
            status,
        )

        return result