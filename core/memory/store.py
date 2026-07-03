"""
Memory System storage.

Handles persistent storage of memory history using JSON.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from .models import MemoryEntry, MemoryHistory


class MemoryStore:
    """
    JSON-backed storage for AI_OS memory history.
    """

    FILE_NAME = "history.json"

    def __init__(self, output_root: Path):
        self.output_dir = Path(output_root) / "memory"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.file_path = self.output_dir / self.FILE_NAME

    def exists(self) -> bool:
        """
        Return True if the history file exists.
        """
        return self.file_path.exists()

    def clear(self) -> None:
        """
        Delete the history file.
        """
        if self.file_path.exists():
            self.file_path.unlink()

    def save(self, history: MemoryHistory) -> None:
        """
        Persist history to disk.
        """

        data = {
            "entries": [
                {
                    **asdict(entry),
                    "timestamp": entry.timestamp.isoformat(),
                }
                for entry in history.entries
            ]
        }

        self.file_path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    def load(self) -> MemoryHistory:
        """
        Load history from disk.
        """

        if not self.exists():
            return MemoryHistory()

        raw = json.loads(
            self.file_path.read_text(
                encoding="utf-8"
            )
        )

        entries = []

        for item in raw.get("entries", []):

            entries.append(
                MemoryEntry(
                    iteration=item["iteration"],
                    timestamp=datetime.fromisoformat(
                        item["timestamp"]
                    ),
                    reflection_summary=item[
                        "reflection_summary"
                    ],
                    improvement_summary=item[
                        "improvement_summary"
                    ],
                    overall_score=item[
                        "overall_score"
                    ],
                )
            )

        return MemoryHistory(entries)