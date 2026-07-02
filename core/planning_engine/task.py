"""
task.py

Task utilities for the Planning Engine.
"""

from __future__ import annotations

from dataclasses import asdict

from .models import Priority, Task, TaskStatus


class TaskFactory:
    """Factory methods for creating planning tasks."""

    _counter = 1

    @classmethod
    def create(
        cls,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        estimated_hours: float = 0.0,
    ) -> Task:
        task = Task(
            id=f"TASK-{cls._counter:04d}",
            title=title,
            description=description,
            priority=priority,
            estimated_hours=estimated_hours,
        )
        cls._counter += 1
        return task


def mark_done(task: Task) -> None:
    task.status = TaskStatus.DONE


def mark_blocked(task: Task) -> None:
    task.status = TaskStatus.BLOCKED


def add_dependency(task: Task, dependency_id: str) -> None:
    if dependency_id not in task.dependencies:
        task.dependencies.append(dependency_id)


def add_tag(task: Task, tag: str) -> None:
    if tag not in task.tags:
        task.tags.append(tag)


def to_dict(task: Task) -> dict:
    return asdict(task)


