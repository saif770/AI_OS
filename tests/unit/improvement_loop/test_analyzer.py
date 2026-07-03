from types import SimpleNamespace
from core.improvement_loop.analyzer import ImprovementAnalyzer

def test_analyzer_returns_recommendations():
    rec=[SimpleNamespace(title="A",priority="High")]
    rr=SimpleNamespace(recommendations=rec)
    out=ImprovementAnalyzer().analyze(rr)
    assert out==rec
