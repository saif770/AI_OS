"""
work_breakdown.py

Break large planning tasks into smaller subtasks.
"""

from __future__ import annotations

from .models import Priority, Task
from .task import TaskFactory, add_dependency


class WorkBreakdown:
    """
    Split large tasks into manageable subtasks.
    """

    DEFAULT_SUBTASK_HOURS = 4.0

    def breakdown(self, tasks: list[Task]) -> list[Task]:
        """
        Expand oversized tasks into subtasks.
        """

        expanded: list[Task] = []

        for task in tasks:

            if task.estimated_hours <= self.DEFAULT_SUBTASK_HOURS:
                expanded.append(task)
                continue

            subtasks = self._split(task)

            expanded.extend(subtasks)

        return expanded

    # ---------------------------------------------------------

    def _split(self, task: Task) -> list[Task]:

        count = max(
            2,
            int(task.estimated_hours // self.DEFAULT_SUBTASK_HOURS),
        )

        hours = round(
            task.estimated_hours / count,
            2,
        )

        subtasks: list[Task] = []

        previous = None

        for index in range(1, count + 1):

            subtask = TaskFactory.create(
                title=f"{task.title} (Part {index}/{count})",
                description=task.description,
                priority=task.priority,
                estimated_hours=hours,
            )

            subtask.tags.extend(task.tags)

            if previous:
                add_dependency(subtask, previous.id)

            previous = subtask
            subtasks.append(subtask)

        return subtasks

    # ---------------------------------------------------------

    def estimate_total_hours(
        self,
        tasks: list[Task],
    ) -> float:

        return round(
            sum(task.estimated_hours for task in tasks),
            2,
        )
