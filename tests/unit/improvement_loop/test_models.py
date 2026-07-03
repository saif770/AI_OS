from core.improvement_loop.models import ImprovementCandidate, ImprovementPlan, ImprovementReport

def test_candidate():
    c=ImprovementCandidate("T","D","Quality","High")
    assert c.priority=="High"

def test_plan_defaults():
    p=ImprovementPlan()
    assert p.highest_priority=="Low"

def test_report():
    p=ImprovementPlan()
    r=ImprovementReport("ok",p,"Low")
    assert r.summary=="ok"
