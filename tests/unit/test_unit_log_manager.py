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


def test_log_event_type_property():
    """UT-Log-EventType: property returns level."""
    log = Log("msg", level="INFO")
    assert log.event_type == "INFO"


def test_log_manager_error_and_preload(monkeypatch):
    """UT-LogMgr-Errors: file write error and preload error/no db."""
    lm = LogManager(storage_manager=None)
    monkeypatch.setattr(
        "builtins.open", lambda *a, **k: (_ for _ in ()).throw(IOError("disk full"))
    )
    lm.add_log("msg", level="INFO", source="UT")

    class BadStorage:
        def get_logs(self, limit=500):
            raise Exception("fail")

        db = None

    lm2 = LogManager(BadStorage())
    lm2.add_log("hello", level="INFO", source="UT")

    class GoodStorage:
        def __init__(self):
            self.db = None

        def get_logs(self, limit=500):
            return [
                {
                    "event_message": "hi",
                    "event_type": "INFO",
                    "source": "Sys",
                    "event_timestamp": None,
                }
            ]

    lm3 = LogManager(GoodStorage())
    assert lm3.logs and lm3.logs[0].message == "hi"


def test_log_manager_storage_save_error(monkeypatch):
    """UT-LogMgr-SaveError: storage.save_log raises but handled."""

    class BadStorage:
        def __init__(self):
            self.db = True

        def save_log(self, log, **kwargs):
            raise Exception("fail")

    lm = LogManager(BadStorage())
    lm.add_log("msg", level="INFO", source="UT")


def test_log_manager_clear_logs_db_error(monkeypatch, tmp_path):
    """UT-LogMgr-ClearError: clear_logs catches DB error."""

    class BadStorage:
        def __init__(self):
            self.db = True

        def clear_logs(self):
            raise Exception("fail")

    lm = LogManager(BadStorage())
    lm.log_file = str(tmp_path / "log.txt")
    # create file
    lm.add_log("x", level="INFO", source="UT")
    lm.clear_logs()
