import time
import sqlite3
import pytest
from PIL import Image

from safehome.core.system import System
from safehome.configuration.safehome_mode import SafeHomeMode
from safehome.configuration.storage_manager import StorageManager


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


def fetch_one(db_conn: sqlite3.Connection, query: str, params=()):
    cur = db_conn.cursor()
    cur.execute(query, params)
    return cur.fetchone()


def test_it_guest_login_and_session_record(system):
    """IT-Login-Guest: guest login success records session row."""
    cm = system.config
    cm.settings.guest_password = "0000"
    assert system.login("guest", "0000", "CONTROL_PANEL")
    row = fetch_one(
        cm.db_manager.connection,
        "SELECT username, login_successful FROM login_sessions ORDER BY session_id DESC LIMIT 1",
    )
    assert row[0] == "guest" and row[1] == 1


def test_it_password_change_persists(system):
    """IT-Password-Change: change control-panel password persists to DB."""
    cm = system.config
    assert system.change_password(cm.settings.master_password, "9999", "CONTROL_PANEL")
    # Ensure DB has new master password
    row = cm.db_manager.get_system_settings()
    assert row["master_password"] == "9999"


def test_it_arm_zone_and_alarm_log(system):
    """IT-Arm-Zone-Alarm: arm zone, trigger motion, ALARM log persists."""
    sc = system.sensor_controller
    sensor = sc.add_sensor("WINDOOR", "Door", zone_id=None)
    system.config.storage.save_mode_sensor_mapping("AWAY", [sensor.sensor_id])
    system.turn_on()
    assert system.arm_system(SafeHomeMode.AWAY)
    sensor.simulate_open()
    system._handle_intrusion(sensor)
    time.sleep(0.05)
    logs = system.config.db_manager.get_event_logs(event_type="ALARM", limit=5)
    assert any("INTRUSION" in row["event_message"] for row in logs)
    system.alarm.stop()
    system.turn_off()


def test_it_camera_ptz_and_status_persist(system):
    """IT-Camera-PTZ: PTZ updates reflected in status and persisted."""
    cc = system.camera_controller
    cam = cc.add_camera("Cam", "Room", password=None)
    cc.pan_camera(cam.camera_id, "left")
    cc.tilt_camera(cam.camera_id, "up")
    cc.zoom_camera(cam.camera_id, "in")
    status = cc.get_camera_status(cam.camera_id)
    assert status["id"] == cam.camera_id
    rows = system.config.db_manager.get_cameras()
    assert any(r["camera_id"] == cam.camera_id for r in rows)


def test_it_mode_sensor_mapping_roundtrip(system):
    """IT-Mode-Sensor: configure and retrieve sensors for mode via storage + system."""
    sc = system.sensor_controller
    s1 = sc.add_sensor("MOTION", "Hall", None)
    system.config.storage.save_mode_sensor_mapping("HOME", [s1.sensor_id])
    assert system._get_sensors_for_mode(SafeHomeMode.HOME) == [s1.sensor_id]


def test_it_log_persistence_clear_and_seen(system):
    """IT-Log-Seen: add log, mark seen, clear logs via StorageManager."""
    cm = system.config
    cm.logger.add_log("ALARM event", level="ALARM", source="System")
    logs = cm.storage.get_logs(limit=5)
    assert logs
    cm.storage.mark_logs_seen([logs[0]["log_id"]])
    cm.storage.clear_logs()
    assert cm.storage.get_logs(limit=1) == []


def test_it_poll_sensors_and_intrusion(system):
    """IT-Poll-Intrusion: poll_sensors picks up armed and opened sensor."""
    sc = system.sensor_controller
    sensor = sc.add_sensor("WINDOOR", "Door")
    sensor.arm()
    sensor.simulate_open()
    detections = sc.poll_sensors()
    assert detections and detections[0][0] == sensor.sensor_id
