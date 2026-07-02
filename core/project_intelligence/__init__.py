"""
Project Intelligence package.
"""

__version__ = "1.0.0"

__all__ = [
    "ProjectAnalyzer",
]


def __getattr__(name):
    if name == "ProjectAnalyzer":
        from .analyzer import ProjectAnalyzer
        return ProjectAnalyzer
    raise AttributeError(name)

