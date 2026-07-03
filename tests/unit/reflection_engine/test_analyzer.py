from types import SimpleNamespace
from core.reflection_engine.analyzer import ReflectionAnalyzer


def test_analyze():
    e=SimpleNamespace(tasks_total=5,tasks_completed=5,tasks_failed=0)
    v=SimpleNamespace(success_rate=100.0,failed_checks=[])
    result=ReflectionAnalyzer().analyze(e,v)
    assert result.overall_success is True
