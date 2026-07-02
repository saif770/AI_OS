"""
analyzer.py

Main Project Intelligence Engine.
"""

from __future__ import annotations

from pathlib import Path

from .architecture import ArchitectureDetector
from .code_metrics import CodeMetrics
from .dependency_analyzer import DependencyAnalyzer
from .entrypoint_detector import EntrypointDetector
from .framework_detector import FrameworkDetector
from .git_analyzer import GitAnalyzer
from .language_detector import LanguageDetector
from .mcp_bridge import MCPBridge
from .report import ProjectReport


class ProjectAnalyzer:
    """
    Main Project Intelligence Engine.
    """

    def __init__(self, project_root: str | Path):

        self.project_root = Path(project_root)

    # -------------------------------------------------------------

    def analyze(self) -> dict:
        """
        Execute the complete project analysis.
        """

        language = LanguageDetector(
            self.project_root
        ).detect()

        framework = FrameworkDetector(
            self.project_root
        ).detect()

        dependencies = DependencyAnalyzer(
            self.project_root
        ).analyze()

        entrypoints = EntrypointDetector(
            self.project_root
        ).detect()

        metrics = CodeMetrics(
            self.project_root
        ).analyze()

        git = GitAnalyzer(
            self.project_root
        ).analyze()

        architecture = ArchitectureDetector(
            self.project_root
        ).detect()

        mcp = MCPBridge(
            self.project_root
        ).analyze()

        report = {
            "project": {
                "name": self.project_root.name,
                "root": str(self.project_root),
            },
            "language": language,
            "framework": framework,
            "dependencies": dependencies,
            "entrypoints": entrypoints,
            "metrics": metrics,
            "git": git,
            "architecture": architecture,
            "mcp": mcp,
        }

        ProjectReport(
            self.project_root
        ).generate(report)

        return report

    # -------------------------------------------------------------

    def summary(self) -> None:

        report = self.analyze()

        print("=" * 70)
        print("Project Intelligence")
        print("=" * 70)

        print(
            f"Project      : {report['project']['name']}"
        )

        print(
            f"Language     : "
            f"{report['language']['primary_language']}"
        )

        print(
            f"Framework    : "
            f"{report['framework']['primary_framework']}"
        )

        print(
            f"Architecture : "
            f"{report['architecture']['architecture']}"
        )

        print(
            f"Python Files : "
            f"{report['metrics']['python_files']}"
        )

        print(
            f"Entry Point  : "
            f"{report['entrypoints']['primary_entrypoint']}"
        )

        print(
            f"Git Repo     : "
            f"{report['git']['repository']}"
        )

        print(
            f"MCP Ready    : "
            f"{report['mcp']['available']}"
        )

        print("=" * 70)


if __name__ == "__main__":

    ProjectAnalyzer(
        Path.cwd()
    ).summary()

