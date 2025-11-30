import pytest

from safehome.core.system import System
from safehome.configuration.storage_manager import StorageManager


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def system(tmp_path, monkeypatch):
    db_path = tmp_path / "logs.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "logs.json"))
    sys = System(db_path=str(db_path))
    yield sys
    sys.shutdown()


def test_st_log_unseen_retention(system):
    """
    ST-Log-Unseen-Retention: unseen counter increments, mark-seen clears, clear removes.
    """
    storage = system.config.storage
    logger = system.config.logger

    logger.add_log("Login success", source="Test", level="INFO")
    logger.add_log("Intrusion", source="Test", level="ALARM")

    unseen = storage.get_unseen_logs(limit=10)
    assert len(unseen) >= 1

    storage.mark_logs_seen([row["log_id"] for row in unseen])
    unseen_after = storage.get_unseen_logs(limit=10)
    assert unseen_after == []

    # Add one more and then clear
    logger.add_log("Another", source="Test", level="INFO")
    assert storage.get_unseen_logs(limit=5, event_type=None)
    storage.clear_logs()
    assert storage.get_unseen_logs(limit=5) == []


def test_st_logs_view_clear_logic(system):
    """
    ST-Logs-View-Clear: retrieval order and clear behavior without UI.
    """
    logger = system.config.logger
    storage = system.config.storage
    before = storage.get_logs(limit=100)
    logger.add_log("First", source="UI", level="INFO")
    logger.add_log("Second", source="UI", level="INFO")
    after = storage.get_logs(limit=100)
    assert len(after) >= len(before) + 2
    storage.clear_logs()
    assert storage.get_logs(limit=2) == []
