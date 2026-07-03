"""
Unit tests for the Orchestrator Pipeline.
"""

from core.orchestrator.models import PipelineContext
from core.orchestrator.pipeline import (
    Pipeline,
    PipelineStep,
)


def dummy_executor(context: PipelineContext):
    return "ok"


def test_pipeline_initially_empty():
    pipeline = Pipeline()

    assert len(pipeline) == 0
    assert pipeline.names() == []


def test_add_single_step():
    pipeline = Pipeline()

    pipeline.add_step(
        "planning_report",
        dummy_executor,
    )

    assert len(pipeline) == 1
    assert pipeline.names() == [
        "planning_report"
    ]


def test_add_multiple_steps():
    pipeline = Pipeline()

    pipeline.add_step(
        "planning_report",
        dummy_executor,
    )

    pipeline.add_step(
        "execution_report",
        dummy_executor,
    )

    pipeline.add_step(
        "verification_report",
        dummy_executor,
    )

    assert len(pipeline) == 3

    assert pipeline.names() == [
        "planning_report",
        "execution_report",
        "verification_report",
    ]


def test_pipeline_iteration():
    pipeline = Pipeline()

    pipeline.add_step(
        "planning_report",
        dummy_executor,
    )

    pipeline.add_step(
        "execution_report",
        dummy_executor,
    )

    names = []

    for step in pipeline:
        names.append(step.name)

    assert names == [
        "planning_report",
        "execution_report",
    ]


def test_pipeline_step_creation():
    step = PipelineStep(
        name="planning_report",
        executor=dummy_executor,
    )

    assert step.name == "planning_report"
    assert callable(step.executor)


def test_default_pipeline():
    pipeline = Pipeline.default()

    assert isinstance(
        pipeline,
        Pipeline,
    )

    assert len(pipeline) == 0