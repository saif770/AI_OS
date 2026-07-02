"""
Rollback manager for the AI_OS Execution Engine.

Creates backups and restores files if execution fails.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from datetime import datetime, UTC, UTC
from pathlib import Path


@dataclass(slots=True)
class RollbackRecord:
    """Represents a single backup record."""

    original: Path
    backup: Path
    created_at: datetime


class RollbackManager:
    """
    Creates backups and restores files.
    """

    def backup(self, target: Path, backup_dir: Path) -> RollbackRecord:
        target = Path(target)
        backup_dir.mkdir(parents=True, exist_ok=True)

        backup_path = backup_dir / target.name

        if target.exists():
            shutil.copy2(target, backup_path)

        return RollbackRecord(
            original=target,
            backup=backup_path,
            created_at=datetime.now(UTC),
        )

    def restore(self, record: RollbackRecord) -> bool:
        if not record.backup.exists():
            return False

        shutil.copy2(record.backup, record.original)
        return True


