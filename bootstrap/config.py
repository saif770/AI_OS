"""
bootstrap/config.py

Bootstrap configuration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import json


@dataclass
class BootstrapConfig:
    """
    Bootstrap configuration.
    """

    project_name: str = "AI_OS"

    version: str = "1.0.0"

    python_version: str = "3.13"

    create_git: bool = True

    create_venv: bool = True

    install_dependencies: bool = True

    setup_mcp: bool = True

    scan_project: bool = True

    ai_ready: bool = True

    verbose: bool = False

    dry_run: bool = False

    data: dict[str, Any] = field(default_factory=dict)

    # -------------------------------------------------------------

    @classmethod
    def load(cls, file_path: str | Path):

        path = Path(file_path)

        if not path.exists():
            return cls()

        with path.open(
            "r",
            encoding="utf-8",
        ) as f:

            config = json.load(f)

        return cls(**config)

    # -------------------------------------------------------------

    def save(self, file_path: str | Path):

        path = Path(file_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with path.open(
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                self.to_dict(),
                f,
                indent=4,
            )

    # -------------------------------------------------------------

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.data.get(
            key,
            default,
        )

    # -------------------------------------------------------------

    def set(
        self,
        key: str,
        value: Any,
    ):

        self.data[key] = value

    # -------------------------------------------------------------

    def update(
        self,
        values: dict[str, Any],
    ):

        self.data.update(values)

    # -------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:

        return {
            "project_name": self.project_name,
            "version": self.version,
            "python_version": self.python_version,
            "create_git": self.create_git,
            "create_venv": self.create_venv,
            "install_dependencies": self.install_dependencies,
            "setup_mcp": self.setup_mcp,
            "scan_project": self.scan_project,
            "ai_ready": self.ai_ready,
            "verbose": self.verbose,
            "dry_run": self.dry_run,
            "data": self.data,
        }

    # -------------------------------------------------------------

    def __repr__(self):

        return (
            f"<BootstrapConfig "
            f"project='{self.project_name}' "
            f"version='{self.version}'>"
        )

