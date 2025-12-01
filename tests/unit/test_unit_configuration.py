import smtplib

import pytest

from safehome.configuration.configuration_manager import ConfigurationManager
from safehome.configuration.safehome_mode import SafeHomeMode
from safehome.configuration.safety_zone import SafetyZone
from safehome.configuration.storage_manager import StorageManager
from safehome.configuration.system_settings import SystemSettings


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


def test_configuration_manager_callbacks_and_modes(config_mgr):
    """UT-Conf-Callbacks: notify callbacks, set/get modes, configure mode sensors."""
    called = []
    config_mgr.register_zone_update_callback(lambda: called.append(1))
    config_mgr.reset_configuration()
    assert called
    config_mgr.set_mode(config_mgr.current_mode)
    assert config_mgr.get_mode() == config_mgr.current_mode
    assert "HOME" in config_mgr.get_safehome_modes()
    config_mgr.configure_mode_sensors("HOME", [])
    assert config_mgr.get_sensors_for_mode("HOME") == []


def test_configuration_manager_save_configuration(config_mgr):
    """UT-Conf-Save: save_configuration logs without error."""
    config_mgr.save_configuration()
    assert config_mgr.logger.get_recent_logs(1)


def test_configuration_manager_send_email_alert(monkeypatch, config_mgr):
    """UT-Conf-Email: send_email_alert handles success/failure branches."""
    sent_messages = []

    class DummySMTP:
        def __init__(self, host, port, timeout):
            self.host, self.port, self.timeout = host, port, timeout

        def starttls(self):
            pass

        def login(self, user, pw):
            pass

        def send_message(self, msg):
            sent_messages.append(msg)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False

    monkeypatch.setattr(smtplib, "SMTP", DummySMTP)
    cfg = config_mgr
    cfg.settings.alert_email = "to@test"
    assert cfg.send_email_alert("subj", "body")
    assert sent_messages and sent_messages[0]["To"] == "to@test"
    cfg.settings.alert_email = ""
    assert not cfg.send_email_alert("subj", "body")


def test_configuration_manager_load_settings_branch(monkeypatch, tmp_path):
    """UT-Conf-LoadSettings: load_settings with data updates SystemSettings."""
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))

    def fake_load(self):
        return {"entry_delay": 5, "monitoring_phone": "123"}

    monkeypatch.setattr(StorageManager, "load_settings", fake_load)
    cm = ConfigurationManager(db_path=str(tmp_path / "safehome.db"))
    assert cm.settings.entry_delay == 5
    cm.shutdown()


def test_configuration_manager_no_zones(monkeypatch, tmp_path):
    """UT-Conf-DefaultZones: empty zones triggers default creation."""
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    original_load = StorageManager.load_all_safety_zones
    calls = {"n": 0}

    def fake_load(self):
        calls["n"] += 1
        if calls["n"] == 1:
            return []
        return original_load(self)

    monkeypatch.setattr(StorageManager, "load_all_safety_zones", fake_load)
    cm = ConfigurationManager(db_path=str(tmp_path / "safehome.db"))
    assert len(cm.get_all_safety_zones()) >= 2
    cm.shutdown()


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
