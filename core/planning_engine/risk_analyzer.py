"""
risk_analyzer.py

Analyze planning risks before execution.
"""

from __future__ import annotations

from .models import Priority, Risk, Roadmap, Task


class RiskAnalyzer:
    """
    Analyze a roadmap and identify execution risks.
    """

    LARGE_TASK_THRESHOLD = 16.0

    def analyze(self, roadmap: Roadmap) -> list[Risk]:
        """
        Return a list of detected risks.
        """

        risks: list[Risk] = []

        all_tasks = [
            task
            for milestone in roadmap.milestones
            for task in milestone.tasks
        ]

        risks.extend(self._large_tasks(all_tasks))
        risks.extend(self._blocked_dependencies(all_tasks))
        risks.extend(self._missing_tests(all_tasks))

        roadmap.risks.extend(risks)

        return risks

    # ---------------------------------------------------------

    def _large_tasks(self, tasks: list[Task]) -> list[Risk]:

        results: list[Risk] = []

        for task in tasks:

            if task.estimated_hours > self.LARGE_TASK_THRESHOLD:

                results.append(
                    Risk(
                        title=f"Large task: {task.title}",
                        severity=Priority.HIGH,
                        mitigation=(
                            "Split into smaller tasks."
                        ),
                    )
                )

        return results

    # ---------------------------------------------------------

    def _blocked_dependencies(
        self,
        tasks: list[Task],
    ) -> list[Risk]:

        results: list[Risk] = []

        ids = {
            task.id
            for task in tasks
        }

        for task in tasks:

            for dependency in task.dependencies:

                if dependency not in ids:

                    results.append(
                        Risk(
                            title=(
                                f"{task.id} depends on "
                                f"missing task {dependency}"
                            ),
                            severity=Priority.CRITICAL,
                            mitigation=(
                                "Create the dependency "
                                "or remove the reference."
                            ),
                        )
                    )

        return results

    # ---------------------------------------------------------

    def _missing_tests(
        self,
        tasks: list[Task],
    ) -> list[Risk]:

        has_tests = any(
            "test" in task.title.lower()
            for task in tasks
        )

        if has_tests:

            return []

        return [
            Risk(
                title="No testing task found",
                severity=Priority.MEDIUM,
                mitigation=(
                    "Add testing tasks before execution."
                ),
            )
        ]


