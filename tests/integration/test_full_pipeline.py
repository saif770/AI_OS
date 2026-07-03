"""
Full AI-OS integration test.

This test verifies the complete AI-OS execution
pipeline from Runtime through the Orchestrator.
"""

from core.orchestrator.engine import Orchestrator
from core.runtime.engine import RuntimeEngine
from core.runtime.scheduler import RuntimeScheduler


def planning_step(context):
    return {
        "stage": "planning",
        "success": True,
    }


def execution_step(context):
    return {
        "stage": "execution",
        "success": True,
    }


def verification_step(context):
    return {
        "stage": "verification",
        "success": True,
    }


def reflection_step(context):
    return {
        "stage": "reflection",
        "success": True,
    }


def improvement_step(context):
    return {
        "stage": "improvement",
        "success": True,
    }


def memory_step(context):
    return {
        "stage": "memory",
        "success": True,
    }


def test_full_pipeline_execution(tmp_path):
    orchestrator = Orchestrator(tmp_path)

    orchestrator.register_step(
        "planning_report",
        planning_step,
    )

    orchestrator.register_step(
        "execution_report",
        execution_step,
    )

    orchestrator.register_step(
        "verification_report",
        verification_step,
    )

    orchestrator.register_step(
        "reflection_report",
        reflection_step,
    )

    orchestrator.register_step(
        "improvement_report",
        improvement_step,
    )

    orchestrator.register_step(
        "memory_report",
        memory_step,
    )

    result = orchestrator.run()

    assert result.success

    assert len(result.completed_steps) == 6

    assert result.context.planning_report["success"]
    assert result.context.execution_report["success"]
    assert result.context.verification_report["success"]
    assert result.context.reflection_report["success"]
    assert result.context.improvement_report["success"]
    assert result.context.memory_report["success"]


def test_runtime_executes_pipeline(tmp_path):
    scheduler = RuntimeScheduler(
        max_iterations=1,
    )

    runtime = RuntimeEngine(
        project_root=tmp_path,
        scheduler=scheduler,
    )

    runtime.orchestrator.register_step(
        "planning_report",
        planning_step,
    )

    runtime.orchestrator.register_step(
        "execution_report",
        execution_step,
    )

    runtime.orchestrator.register_step(
        "verification_report",
        verification_step,
    )

    runtime.orchestrator.register_step(
        "reflection_report",
        reflection_step,
    )

    runtime.orchestrator.register_step(
        "improvement_report",
        improvement_step,
    )

    runtime.orchestrator.register_step(
        "memory_report",
        memory_step,
    )

    result = runtime.run()

    assert result.success
    assert result.iterations_completed == 1


def test_runtime_generates_reports(tmp_path):
    scheduler = RuntimeScheduler(
        max_iterations=1,
    )

    runtime = RuntimeEngine(
        project_root=tmp_path,
        scheduler=scheduler,
    )

    runtime.orchestrator.register_step(
        "planning_report",
        planning_step,
    )

    runtime.run()

    runtime_report_dir = (
        tmp_path
        / "output"
        / "runtime"
    )

    orchestrator_report_dir = (
        tmp_path
        / "output"
        / "orchestrator"
    )

    assert (
        runtime_report_dir
        / "runtime.json"
    ).exists()

    assert (
        runtime_report_dir
        / "runtime.md"
    ).exists()

    assert (
        orchestrator_report_dir
        / "orchestrator.json"
    ).exists()

    assert (
        orchestrator_report_dir
        / "orchestrator.md"
    ).exists()


def test_pipeline_execution_order(tmp_path):
    order = []

    def step(name):
        def execute(context):
            order.append(name)
            return name
        return execute

    orchestrator = Orchestrator(tmp_path)

    orchestrator.register_step(
        "planning_report",
        step("planning"),
    )

    orchestrator.register_step(
        "execution_report",
        step("execution"),
    )

    orchestrator.register_step(
        "verification_report",
        step("verification"),
    )

    orchestrator.register_step(
        "reflection_report",
        step("reflection"),
    )

    orchestrator.register_step(
        "improvement_report",
        step("improvement"),
    )

    orchestrator.register_step(
        "memory_report",
        step("memory"),
    )

    orchestrator.run()

    assert order == [
        "planning",
        "execution",
        "verification",
        "reflection",
        "improvement",
        "memory",
    ]


def test_pipeline_context_complete(tmp_path):
    orchestrator = Orchestrator(tmp_path)

    orchestrator.register_step(
        "planning_report",
        planning_step,
    )

    orchestrator.register_step(
        "execution_report",
        execution_step,
    )

    orchestrator.register_step(
        "verification_report",
        verification_step,
    )

    orchestrator.register_step(
        "reflection_report",
        reflection_step,
    )

    orchestrator.register_step(
        "improvement_report",
        improvement_step,
    )

    orchestrator.register_step(
        "memory_report",
        memory_step,
    )

    result = orchestrator.run()

    context = result.context

    assert context is not None
    assert context.planning_report is not None
    assert context.execution_report is not None
    assert context.verification_report is not None
    assert context.reflection_report is not None
    assert context.improvement_report is not None
    assert context.memory_report is not None