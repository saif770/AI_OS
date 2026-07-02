"""
prioritizer.py

Task prioritization for the Planning Engine.
"""

from __future__ import annotations

from .models import Priority, Task


class Prioritizer:
    """
    Score and sort tasks for execution.
    """

    PRIORITY_SCORE = {
        Priority.CRITICAL: 100,
        Priority.HIGH: 75,
        Priority.MEDIUM: 50,
        Priority.LOW: 25,
    }

    def prioritize(self, tasks: list[Task]) -> list[Task]:
        """
        Return tasks sorted by execution priority.
        """

        return sorted(
            tasks,
            key=self._score,
            reverse=True,
        )

    def _score(self, task: Task) -> int:
        """
        Calculate task score.
        """

        score = self.PRIORITY_SCORE.get(
            task.priority,
            0,
        )

        score += len(task.dependencies) * 10

        if task.estimated_hours <= 2:
            score += 5

        return score


