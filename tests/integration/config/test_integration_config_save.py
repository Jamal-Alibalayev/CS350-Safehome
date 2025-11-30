import pytest

from safehome.core.system import System
from safehome.configuration.storage_manager import StorageManager
from safehome.database.db_manager import DatabaseManager


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def system(tmp_path, monkeypatch):
    db_path = tmp_path / "safehome.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    sys = System(db_path=str(db_path))
    yield sys
    sys.shutdown()


def test_it_config_save_restore(tmp_path, monkeypatch):
    """IT-Config-Save-Restore: save settings then reload via new System."""
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    sys1 = System(db_path=str(tmp_path / "safehome.db"))
    sys1.config.settings.entry_delay = 42
    sys1.config.save_configuration()
    sys1.shutdown()

    # New instance should pick up saved entry_delay
    sys2 = System(db_path=str(tmp_path / "safehome.db"))
    assert sys2.config.settings.entry_delay == 42
    sys2.shutdown()


def test_it_reset_and_reinit(tmp_path, monkeypatch):
    """IT-Reset-And-Reinit: reset, then new System has default zones and cleared passwords."""
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    sys1 = System(db_path=str(tmp_path / "safehome.db"))
    # seed camera password and custom zone
    sys1.config.storage.save_camera(1, "Cam", "Loc", password="pw")
    sys1.config.add_safety_zone("Custom")
    sys1.config.reset_configuration()
    sys1.shutdown()

    sys2 = System(db_path=str(tmp_path / "safehome.db"))
    zones = sys2.config.get_all_safety_zones()
    assert len(zones) >= 2
    cams = sys2.config.storage.load_all_cameras()
    for c in cams:
        assert c.get("camera_password") is None
    sys2.shutdown()


def test_it_db_disconnect_reconnect(tmp_path):
    """IT-DB-Disconnect-Reconnect: disconnect and reconnect then query succeeds."""
    db_path = tmp_path / "safehome.db"
    dbm = DatabaseManager(db_path=str(db_path))
    dbm.connect()
    dbm.initialize_schema()
    dbm.disconnect()
    # reconnect and run a simple query
    dbm.connect()
    rows = dbm.get_safehome_modes()
    assert rows  # default modes
    dbm.disconnect()


def test_it_storage_clear_logs_empty(tmp_path, monkeypatch):
    """IT-Storage-ClearLogs-Empty: clear_logs and mark_logs_seen on empty DB."""
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    db_path = tmp_path / "safehome.db"
    sys = System(db_path=str(db_path))
    storage = sys.config.storage
    # No logs yet
    storage.mark_logs_seen([])
    storage.clear_logs()
    assert storage.get_logs(limit=1) == []
    sys.shutdown()
