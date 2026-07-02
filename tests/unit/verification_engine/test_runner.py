"""
Unit tests for the Verification Engine pytest runner.
"""

from pathlib import Path

from core.verification_engine import pytest_runner
from core.verification_engine.models import VerificationCheck
from core.verification_engine.tool_runner import ToolRunner


def test_test_runner_delegates_to_tool_runner(
    tmp_path: Path,
    monkeypatch,
):
    project = tmp_path / "project"
    project.mkdir()

    captured: dict[str, object] = {}

    def fake_run(
        self,
        *,
        name: str,
        project_root: Path,
        command: list[str],
        module_fallback: str | None = None,
    ) -> VerificationCheck:
        captured["name"] = name
        captured["project_root"] = project_root
        captured["command"] = command
        captured["module_fallback"] = module_fallback

        return VerificationCheck(
            name=name,
            success=True,
            duration=0.01,
            message="Passed.",
            details={"command": command},
        )

    monkeypatch.setattr(ToolRunner, "run", fake_run)

    result = pytest_runner.TestRunner().run(project)

    assert captured == {
        "name": "test_runner",
        "project_root": project,
        "command": ["pytest", "-q"],
        "module_fallback": "pytest",
    }
    assert result.success
