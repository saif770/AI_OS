"""
Execution Engine.

Coordinates the complete execution workflow.

Planning
    â†“
Prompt Builder
    â†“
LLM Client
    â†“
Code Generator
    â†“
Patch Generator
    â†“
Patch Applier
    â†“
Validator
    â†“
Report
"""

from __future__ import annotations

from pathlib import Path

from .code_generator import CodeGenerator
from .llm_client import LLMClient
from .models import ExecutionReport, ExecutionTask
from .patch_applier import PatchApplier
from .patch_generator import PatchGenerator
from .prompt_builder import PromptBuilder
from .report import ReportWriter
from .validator import Validator


class ExecutionEngine:
    """
    High-level orchestration of the execution pipeline.
    """

    def __init__(
        self,
        project_root: Path,
        llm_client: LLMClient,
    ) -> None:
        self.project_root = Path(project_root)
        self.llm = llm_client

        self.prompt_builder = PromptBuilder()
        self.generator = CodeGenerator()
        self.patch_generator = PatchGenerator()
        self.patch_applier = PatchApplier(
            project_root=self.project_root
        )
        self.validator = Validator()
        self.report_writer = ReportWriter(
            self.project_root / "output"
        )

    def execute(
        self,
        tasks: list[ExecutionTask],
    ) -> ExecutionReport:

        report = ExecutionReport(
            project_name=self.project_root.name,
            total_tasks=len(tasks),
        )

        for task in tasks:

            prompt = self.prompt_builder.build(task)

            response = self.llm.generate(prompt)

            generated = self.generator.generate(
                response,
                filename="generated.py",
            )

            bundle = self.patch_generator.generate(generated)

            validations = self.validator.validate_all(
                bundle.patches
            )

            if not all(v.passed for v in validations):
                report.failed += 1
                continue

            self.patch_applier.apply_many(bundle.patches)

            report.completed += 1

        self.report_writer.write_json(report)

        return report


