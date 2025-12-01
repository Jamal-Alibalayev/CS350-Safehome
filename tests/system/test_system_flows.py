import time

import pytest
from PIL import Image

from safehome.configuration.safehome_mode import SafeHomeMode
from safehome.configuration.storage_manager import StorageManager
from safehome.core.system import System


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    """Avoid GUI popups during system-level flows."""
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def system(tmp_path, monkeypatch):
    """Full System with isolated DB/JSON for system-level scenarios."""
    db_path = tmp_path / "safehome.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    sys = System(db_path=str(db_path))
    yield sys
    sys.shutdown()


def test_st_login_arm_disarm_flow(system):
    """
    ST-Login-Arm-Disarm (SDS seq p47/p55):
    Simulate user login then arm AWAY and disarm, verifying mode and sensor state.
    """
    sys = system
    sc = sys.sensor_controller
    sensor = sc.add_sensor("WINDOOR", "Front Door")
    sys.config.storage.save_mode_sensor_mapping("AWAY", [sensor.sensor_id])

    sys.turn_on()
    assert sys.login("admin", sys.config.settings.master_password, "CONTROL_PANEL")

    assert sys.arm_system(SafeHomeMode.AWAY)
    assert sys.config.current_mode == SafeHomeMode.AWAY
    assert sensor.is_active

    sys.disarm_system()
    assert sys.config.current_mode == SafeHomeMode.DISARMED
    assert not sensor.is_active
    sys.turn_off()


def test_st_intrusion_alarm_log_flow(system):
    """
    ST-Intrusion-Alarm (SDS seq p58/p65):
    Arm system, trigger intrusion, verify alarm rings and ALARM log is recorded.
    """
    sys = system
    sc = sys.sensor_controller
    sensor = sc.add_sensor("WINDOOR", "Back Door")
    sys.config.storage.save_mode_sensor_mapping("AWAY", [sensor.sensor_id])

    sys.config.settings.entry_delay = 0
    sys.turn_on()
    assert sys.arm_system(SafeHomeMode.AWAY)

    sensor.simulate_open()
    sys._handle_intrusion(sensor)
    time.sleep(0.1)
    assert sys.alarm.is_active()

    logs = sys.config.db_manager.get_event_logs(event_type="ALARM", limit=5)
    assert any("INTRUSION" in row["event_message"] for row in logs)

    sys.alarm.stop()
    sys.turn_off()


def test_st_camera_user_flow(system):
    """
    ST-Camera-UserFlow (SDS seq p66~69/p72~73):
    User sets password, views feed, performs PTZ/zoom, and verifies persistence.
    """
    cc = system.camera_controller
    cam = cc.add_camera("Hall", "Hallway", password="1234")

    # Wrong password denied, correct allowed
    assert cc.get_camera_view(cam.camera_id, password="0000") is None
    view = cc.get_camera_view(cam.camera_id, password="1234")
    assert isinstance(view, Image.Image)

    # PTZ/zoom actions
    assert cc.pan_camera(cam.camera_id, "left", password="1234")
    assert cc.tilt_camera(cam.camera_id, "up", password="1234")
    assert cc.zoom_camera(cam.camera_id, "in", password="1234")

    # Persisted password in DB
    rows = system.config.db_manager.get_cameras()
    assert any(row["camera_password"] == "1234" for row in rows)


def test_st_zone_management_flow(system):
    """
    ST-Zone-Manage (SDS seq p59~63):
    Create zone, add sensor to zone, arm/disarm zone and verify status.
    """
    sys = system
    cm = sys.config
    zone = cm.add_safety_zone("Garage")
    sensor = sys.sensor_controller.add_sensor("WINDOOR", "Garage Door", zone.zone_id)

    sys.arm_zone(zone.zone_id)
    assert sensor.is_active
    logs = cm.logger.get_recent_logs(1)
    assert any("Zone Garage ARMED" in log.message for log in logs)

    sys.disarm_zone(zone.zone_id)
    assert not sensor.is_active


def test_st_panic_flow(system):
    """
    ST-Panic (SDS seq p65):
    Trigger panic mode and verify alarm activation and mode state.
    """
    sys = system
    sys.turn_on()
    sys.config.set_mode(SafeHomeMode.PANIC)
    sys.alarm.ring()
    time.sleep(0.05)
    assert sys.config.current_mode == SafeHomeMode.PANIC
    assert sys.alarm.is_active()
    sys.alarm.stop()
    sys.turn_off()
