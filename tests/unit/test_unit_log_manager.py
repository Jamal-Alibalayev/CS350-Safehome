import os
import pytest

from safehome.configuration.log_manager import LogManager
from safehome.configuration.log import Log
from safehome.configuration.storage_manager import StorageManager
from safehome.database.db_manager import DatabaseManager


@pytest.fixture
def temp_logger(tmp_path):
    db = DatabaseManager(db_path=str(tmp_path / "safehome.db"))
    db.connect()
    db.initialize_schema()
    storage = StorageManager(db)
    lm = LogManager(storage)
    lm.log_file = str(tmp_path / "events.log")
    yield lm
    db.disconnect()


def test_log_manager_write_and_clear(temp_logger):
    """UT-LogMgr-WriteClear: add_log writes file/DB and clear_logs empties."""
    temp_logger.add_log("hello", level="INFO", source="UT")
    assert os.path.exists(temp_logger.log_file)
    with open(temp_logger.log_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "hello" in content

    logs = temp_logger.get_recent_logs(1)
    assert logs and isinstance(logs[0], Log)

    temp_logger.clear_logs()
    assert temp_logger.get_all_logs() == []
    with open(temp_logger.log_file, "r", encoding="utf-8") as f:
        assert f.read() == ""
