from types import SimpleNamespace
from core.improvement_loop.engine import ImprovementEngine

def test_engine(tmp_path):
    rec=[SimpleNamespace(title="A",description="B",category="Quality",priority="High")]
    reflection=SimpleNamespace(recommendations=rec)
    report=ImprovementEngine(tmp_path).run(reflection)
    assert report.overall_priority=="High"
    assert (tmp_path/"improvement"/"improvement.md").exists()
