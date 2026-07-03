from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List

@dataclass(slots=True)
class ImprovementCandidate:
    title:str
    description:str
    category:str
    priority:str="Medium"

@dataclass(slots=True)
class ImprovementPlan:
    items:List[ImprovementCandidate]=field(default_factory=list)
    highest_priority:str="Low"
    created_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc))

@dataclass(slots=True)
class ImprovementReport:
    summary:str
    plan:ImprovementPlan
    overall_priority:str
    recommendations:List[ImprovementCandidate]=field(default_factory=list)
