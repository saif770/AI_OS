from .models import ImprovementPlan
class ImprovementPlanner:
    ORDER={"Critical":0,"High":1,"Medium":2,"Low":3}
    def build(self,candidates):
        items=sorted(candidates,key=lambda c:self.ORDER.get(c.priority,99))
        highest=items[0].priority if items else "Low"
        return ImprovementPlan(items=items,highest_priority=highest)
