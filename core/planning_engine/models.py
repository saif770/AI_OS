"""
models.py

Shared planning models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class TaskStatus(str, Enum):
    TODO = "Todo"
    IN_PROGRESS = "In Progress"
    BLOCKED = "Blocked"
    DONE = "Done"


@dataclass
class Task:
    id: str
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = TaskStatus.TODO
    estimated_hours: float = 0.0
    dependencies: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)


@dataclass
class Milestone:
    name: str
    tasks: list[Task] = field(default_factory=list)


@dataclass
class Risk:
    title: str
    severity: Priority
    mitigation: str = ""


@dataclass
class Roadmap:
    milestones: list[Milestone] = field(default_factory=list)
    risks: list[Risk] = field(default_factory=list)


@dataclass
class PlanningResult:
    project_name: str
    roadmap: Roadmap
    metadata: dict[str, Any] = field(default_factory=dict)
