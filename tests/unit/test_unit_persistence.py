import os
import sqlite3
import json
import pytest

from safehome.database.db_manager import DatabaseManager
from safehome.configuration.storage_manager import StorageManager
from safehome.configuration.system_settings import SystemSettings
from safehome.configuration.log_manager import LogManager
from safehome.configuration.log import Log


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def db(tmp_path):
    db_path = tmp_path / "safehome.db"
    mgr = DatabaseManager(db_path=str(db_path))
    mgr.connect()
    mgr.initialize_schema()
    yield mgr
    mgr.disconnect()


def test_db_manager_basic_queries(db):
    """UT-DB-Basic (SDS state p33): schema setup and insert/select paths."""
    db.update_system_settings(master_password="9999")
    row = db.get_system_settings()
    assert row["master_password"] == "9999"
    # add event log and fetch
    log_id = db.add_event_log("INFO", "db test", source="UT")
    rows = db.get_event_logs(event_type="INFO", limit=5)
    assert any(r["log_id"] == log_id for r in rows)
    db.clear_event_logs()
    assert db.get_event_logs(limit=1) == []


def test_storage_manager_settings_json_and_db(tmp_path, db, monkeypatch):
    """UT-Storage-Settings (SDS state p33/p34): JSON + DB read/write."""
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    storage = StorageManager(db)
    settings = SystemSettings(master_password="abcd", entry_delay=10)
    storage.save_settings(settings)
    assert os.path.exists(StorageManager.CONFIG_FILE)
    loaded = storage.load_settings()
    assert loaded["master_password"] == "abcd"
    # DB roundtrip only
    settings.master_password = "efgh"
    storage.save_settings_to_db(settings)
    loaded_db = storage.load_settings_from_db()
    assert loaded_db["master_password"] == "efgh"


def test_storage_manager_logs_and_seen(db):
    """UT-Storage-Logs (SDS seq p64): save/get/seen/clear."""
    storage = StorageManager(db)
    lm = LogManager(storage)
    lm.add_log("event1", level="ALARM", source="UT")
    logs = storage.get_logs(event_type="ALARM", limit=5)
    assert any(l["event_message"] == "event1" for l in logs)
    unseen = storage.get_unseen_logs(limit=5)
    assert unseen
    storage.mark_logs_seen([unseen[0]["log_id"]])
    storage.clear_logs()
    assert storage.get_logs(limit=1) == []


def test_storage_manager_zone_and_sensor_crud(db):
    """UT-Storage-ZoneSensor (SDS seq p59~63): CRUD for zones/sensors/cameras."""
    storage = StorageManager(db)
    # Zone CRUD
    from safehome.configuration.safety_zone import SafetyZone

    zone = SafetyZone(None, "Lab")
    zid = storage.save_safety_zone(zone)
    assert zid is not None
    assert storage.load_safety_zone_by_id(zid).name == "Lab"
    storage.delete_all_safety_zones()
    assert storage.load_all_safety_zones() == []

    # Sensor CRUD
    storage.save_sensor(1, "WINDOOR", "Door", None)
    sensors = storage.load_all_sensors()
    assert sensors and sensors[0]["sensor_type"] == "WINDOOR"
    storage.delete_sensor(1)
    assert storage.load_all_sensors() == []

    # Camera CRUD
    storage.save_camera(1, "Cam", "Hall", "pw")
    cams = storage.load_all_cameras()
    assert cams and cams[0]["camera_password"] == "pw"
    storage.update_camera_password(1, None)
    cams2 = storage.load_all_cameras()
    assert cams2[0]["camera_password"] is None
    storage.clear_camera_passwords()
    storage.delete_camera(1)
    assert storage.load_all_cameras() == []


def test_storage_manager_mode_sensor_mapping(db):
    """UT-Storage-ModeMap (SDS seq p59~63): mode-sensor map roundtrip."""
    storage = StorageManager(db)
    storage.save_sensor(1, "WINDOOR", "Door", None)
    storage.save_mode_sensor_mapping("HOME", [1])
    assert storage.get_sensors_for_mode("HOME") == [1]


def test_storage_manager_invalid_mode_mapping(db):
    """UT-Storage-ModeMap-Invalid: unknown mode name no-op."""
    storage = StorageManager(db)
    storage.save_mode_sensor_mapping("NOTAMODE", [1, 2])  # should not throw


def test_storage_manager_check_db_and_json_errors(tmp_path):
    """UT-Storage-CheckDb/JSON: _check_db raises; bad JSON raises decode error."""
    storage = StorageManager(db_manager=None)
    with pytest.raises(ValueError):
        storage._check_db()
    bad_json = tmp_path / "bad.json"
    bad_json.write_text("{invalid", encoding="utf-8")
    StorageManager.CONFIG_FILE = str(bad_json)
    with pytest.raises(json.JSONDecodeError):
        storage.load_settings_from_json()
