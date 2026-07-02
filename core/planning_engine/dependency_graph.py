"""
dependency_graph.py

Task dependency graph for the Planning Engine.
"""

from __future__ import annotations

from collections import defaultdict, deque

from .models import Task


class DependencyGraph:
    """
    Build and analyze task dependency relationships.
    """

    def build(self, tasks: list[Task]) -> dict:
        """
        Build an adjacency list for task dependencies.
        """

        graph = defaultdict(list)

        for task in tasks:
            for dependency in task.dependencies:
                graph[dependency].append(task.id)

            graph.setdefault(task.id, [])

        return dict(graph)

    def execution_order(self, tasks: list[Task]) -> list[str]:
        """
        Return a topological execution order.
        Raises ValueError if a cycle is detected.
        """

        graph = self.build(tasks)
        indegree = {task.id: 0 for task in tasks}

        for deps in graph.values():
            for node in deps:
                indegree[node] += 1

        queue = deque(
            node for node, degree in indegree.items()
            if degree == 0
        )

        order = []

        while queue:
            node = queue.popleft()
            order.append(node)

            for neighbor in graph.get(node, []):
                indegree[neighbor] -= 1

                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        if len(order) != len(tasks):
            raise ValueError(
                "Circular dependency detected."
            )

        return order

    def has_cycles(self, tasks: list[Task]) -> bool:
        """
        Check whether dependency cycles exist.
        """

        try:
            self.execution_order(tasks)
            return False
        except ValueError:
            return True
