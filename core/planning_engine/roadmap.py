"""
roadmap.py

Roadmap builder for the Planning Engine.
"""

from __future__ import annotations

from .models import Milestone, Roadmap, Task


class RoadmapBuilder:
    """
    Organize tasks into project milestones.
    """

    DEFAULT_PHASES = (
        "Foundation",
        "Core Development",
        "Testing",
        "Deployment",
    )

    def build(self, tasks: list[Task]) -> Roadmap:
        """
        Build a roadmap from a list of tasks.
        """

        roadmap = Roadmap()

        milestones = {
            phase: Milestone(name=phase)
            for phase in self.DEFAULT_PHASES
        }

        for task in tasks:

            title = task.title.lower()

            if "test" in title:
                milestones["Testing"].tasks.append(task)

            elif (
                "deploy" in title
                or "release" in title
            ):
                milestones["Deployment"].tasks.append(task)

            elif (
                "setup" in title
                or "initialize" in title
                or "configure" in title
            ):
                milestones["Foundation"].tasks.append(task)

            else:
                milestones["Core Development"].tasks.append(task)

        for milestone in milestones.values():

            if milestone.tasks:
                roadmap.milestones.append(milestone)

        return roadmap


