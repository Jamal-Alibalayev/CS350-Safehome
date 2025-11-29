import time
import os
import pytest

from safehome.configuration.configuration_manager import ConfigurationManager
from safehome.configuration.system_settings import SystemSettings
from safehome.configuration.safehome_mode import SafeHomeMode
from safehome.configuration.safety_zone import SafetyZone
from safehome.configuration.storage_manager import StorageManager


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    """Avoid GUI popups in device layers."""
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def config_mgr(tmp_path, monkeypatch):
    """Create a temporary ConfigurationManager with an isolated DB and JSON path."""
    db_path = tmp_path / "safehome.db"
    # Redirect JSON backup to temp to avoid polluting repo
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    cm = ConfigurationManager(db_path=str(db_path))
    yield cm
    cm.shutdown()


def test_system_settings_update_and_dict():
    """UT-Settings-Update (SDS state p34): verify update_settings/to_dict."""
    settings = SystemSettings()
    settings.update_settings(entry_delay=30, monitoring_phone="112")
    data = settings.to_dict()
    assert data["entry_delay"] == 30
    assert data["monitoring_phone"] == "112"


def test_safehome_mode_mapping():
    """UT-Mode-Mapping (SDS state p32): enum ↔ db name conversion."""
    assert SafeHomeMode.get_db_mode_name(SafeHomeMode.HOME) == "HOME"
    assert SafeHomeMode.get_db_mode_name(SafeHomeMode.DISARMED) == "DISARMED"
    assert SafeHomeMode.from_db_mode_name("away") == SafeHomeMode.AWAY
    assert SafeHomeMode.from_db_mode_name("unknown") == SafeHomeMode.DISARMED


def test_configuration_manager_zone_crud(config_mgr):
    """UT-Conf-Zone-CRUD (SDS seq p59~63): add/update/delete safety zones."""
    zone = config_mgr.add_safety_zone("Test Zone")
    assert zone is not None
    assert zone.zone_id is not None

    updated = config_mgr.update_safety_zone(zone.zone_id, zone_name="Renamed Zone")
    assert updated
    fetched = config_mgr.get_safety_zone(zone.zone_id)
    assert fetched and fetched.name == "Renamed Zone"

    deleted = config_mgr.delete_safety_zone(zone.zone_id)
    assert deleted
    assert config_mgr.get_safety_zone(zone.zone_id) is None


def test_configuration_manager_reset(monkeypatch, tmp_path):
    """UT-Conf-Reset (SDS seq p53): reset defaults recreates zones and clears camera passwords."""
    db_path = tmp_path / "safehome.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    cm = ConfigurationManager(db_path=str(db_path))
    # Seed a camera password to ensure reset clears it
    cm.storage.save_camera(1, "Cam", "Lab", "pw")
    cm.reset_configuration()
    zones = cm.get_all_zones()
    assert len(zones) >= 2  # default Living Room/Bedroom recreated
    cameras = cm.storage.load_all_cameras()
    for cam in cameras:
        assert cam.get("camera_password") is None
    cm.shutdown()


def test_storage_manager_sensor_camera_persistence(config_mgr):
    """UT-Storage-Persist (SDS state p33 / seq p66~73): save/load sensors & cameras."""
    storage = config_mgr.storage
    storage.save_sensor(1, "WINDOOR", "Door", zone_id=None)
    storage.save_sensor(2, "MOTION", "Hall", zone_id=None)
    sensors = storage.load_all_sensors()
    assert {s["sensor_id"] for s in sensors} == {1, 2}

    storage.save_camera(1, "Cam1", "Lab", password=None)
    storage.save_camera(2, "Cam2", "Kitchen", password="1234")
    cams = storage.load_all_cameras()
    assert {c["camera_id"] for c in cams} == {1, 2}
    assert any(c["camera_password"] == "1234" for c in cams)


def test_storage_manager_mode_sensor_mapping(config_mgr):
    """UT-Storage-ModeMap (SDS seq p59~63): mode↔sensor association stored."""
    storage = config_mgr.storage
    storage.save_sensor(1, "WINDOOR", "Door", zone_id=None)
    storage.save_sensor(2, "MOTION", "Hall", zone_id=None)
    storage.save_mode_sensor_mapping("HOME", [1])
    storage.save_mode_sensor_mapping("AWAY", [1, 2])
    assert storage.get_sensors_for_mode("HOME") == [1]
    assert set(storage.get_sensors_for_mode("AWAY")) == {1, 2}


def test_safety_zone_object_behaviors():
    """UT-Conf-Zone-Obj (SDS state p31): sensor membership and arm/disarm."""
    zone = SafetyZone(zone_id=10, name="Office")
    zone.add_sensor(1)
    zone.add_sensor(2)
    zone.remove_sensor(1)
    assert zone.get_sensors() == [2]
    zone.arm()
    assert zone.is_armed
    zone.disarm()
    assert not zone.is_armed
