from __future__ import annotations

import json
from pathlib import Path

from core.reflection_engine.models import (
    AnalysisResult,
    ReflectionReport,
    ReflectionScore,
)
from core.reflection_engine.report import ReflectionReportWriter


def test_report_writer(tmp_path: Path):
    analysis = AnalysisResult(
        tasks_total=1,
        tasks_completed=1,
        tasks_failed=0,
        verification_success_rate=100.0,
        verification_failed_checks=0,
        overall_success=True,
    )

    score = ReflectionScore(
        execution_score=100.0,
        verification_score=100.0,
        reliability_score=100.0,
        overall_score=100.0,
    )

    report = ReflectionReport(
        summary="Reflection completed successfully.",
        analysis=analysis,
        score=score,
        recommendations=[],
    )

    writer = ReflectionReportWriter(tmp_path)
    writer.write(report)

    json_file = tmp_path / "reflection" / "reflection.json"
    md_file = tmp_path / "reflection" / "reflection.md"

    assert json_file.exists()
    assert md_file.exists()

    data = json.loads(json_file.read_text(encoding="utf-8"))

    assert data["summary"] == "Reflection completed successfully."
    assert "analysis" in data
    assert "score" in data
    assert "recommendations" in data