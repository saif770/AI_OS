from core.improvement_loop.models import ImprovementCandidate
from core.improvement_loop.planner import ImprovementPlanner

def test_priority_order():
    items=[
        ImprovementCandidate("L","","","Low"),
        ImprovementCandidate("H","","","High"),
        ImprovementCandidate("M","","","Medium"),
    ]
    plan=ImprovementPlanner().build(items)
    assert plan.items[0].priority=="High"
    assert plan.highest_priority=="High"
