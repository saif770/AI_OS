from types import SimpleNamespace
from core.reflection_engine.engine import ReflectionEngine


def test_engine_run(tmp_path):
    engine=ReflectionEngine(tmp_path)
    e=SimpleNamespace(tasks_total=1,tasks_completed=1,tasks_failed=0)
    v=SimpleNamespace(success_rate=100.0,failed_checks=[])
    report=engine.run(e,v)
    assert report.analysis.overall_success is True
    assert (tmp_path/"reflection"/"reflection.md").exists()
