"""
Unit tests for the RollbackManager.
"""

from pathlib import Path

from core.execution_engine.rollback import (
    RollbackManager,
    RollbackRecord,
)


def test_backup_existing_file(tmp_path: Path):
    manager = RollbackManager()

    source = tmp_path / "sample.py"
    source.write_text("print('hello')\n", encoding="utf-8")

    backup_dir = tmp_path / "backup"

    record = manager.backup(source, backup_dir)

    assert isinstance(record, RollbackRecord)
    assert record.backup.exists()
    assert record.original == source


def test_restore_backup(tmp_path: Path):
    manager = RollbackManager()

    source = tmp_path / "restore.py"
    source.write_text("original\n", encoding="utf-8")

    backup_dir = tmp_path / "backup"

    record = manager.backup(source, backup_dir)

    source.write_text("modified\n", encoding="utf-8")

    restored = manager.restore(record)

    assert restored
    assert source.read_text(encoding="utf-8") == "original\n"


