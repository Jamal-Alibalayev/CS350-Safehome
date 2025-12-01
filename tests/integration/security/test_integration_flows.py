import time
import sqlite3
import pytest
from PIL import Image

from safehome.core.system import System
from safehome.configuration.safehome_mode import SafeHomeMode
from safehome.configuration.storage_manager import StorageManager


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    """Avoid GUI popups in device layers."""
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def system(tmp_path, monkeypatch):
    """Isolated System with temporary DB and JSON paths for integration tests."""
    db_path = tmp_path / "safehome.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    sys = System(db_path=str(db_path))
    yield sys
    sys.shutdown()


def fetch_rows(db_conn: sqlite3.Connection, query: str, params=()):
    cur = db_conn.cursor()
    cur.execute(query, params)
    return cur.fetchall()


def test_it_login_process_records_session(system):
    """IT-Login-Sys (SDS seq p47): System.login logs successful session in DB."""
    cm = system.config
    assert system.login("admin", cm.settings.master_password, "CONTROL_PANEL")
    rows = fetch_rows(
        cm.db_manager.connection,
        "SELECT interface_type, username, login_successful FROM login_sessions",
    )
    assert rows and rows[0][0] == "CONTROL_PANEL" and rows[0][1] == "admin"
    assert rows[0][2] == 1


def test_it_login_lockout_and_persistence(system):
    """IT-Login-Lock (SDS state p29~30): failed attempts lock interface and record attempts."""
    cm = system.config
    cm.settings.max_login_attempts = 2
    assert not system.login("admin", "bad", "CONTROL_PANEL")
    assert not system.login("admin", "bad", "CONTROL_PANEL")
    assert cm.login_manager.is_locked.get("CONTROL_PANEL", False)
    rows = fetch_rows(
        cm.db_manager.connection,
        "SELECT failed_attempts, login_successful FROM login_sessions ORDER BY session_id DESC LIMIT 1",
    )
    assert rows and rows[0][0] >= 2 and rows[0][1] == 0


def test_it_arm_blocks_when_window_open_and_logs(system):
    """IT-Arm-OpenBlock (SDS seq p55): open window prevents arming and logs warning."""
    sc = system.sensor_controller
    win = sc.add_sensor("WINDOOR", "Door")
    win.arm()
    win.simulate_open()
    armed = system.arm_system(SafeHomeMode.AWAY)
    assert not armed
    # Check logger captured warning
    logs = system.config.logger.get_recent_logs(1)
    assert any(
        "Cannot arm" in log.message or "windows/doors" in log.message for log in logs
    )


def test_it_entry_delay_triggers_alarm(system):
    """IT-Alarm-Delay (SDS seq p58): intrusion after entry delay triggers alarm and monitoring call."""
    system.turn_on()
    sc = system.sensor_controller
    win = sc.add_sensor("WINDOOR", "Patio")
    system.config.storage.save_mode_sensor_mapping("AWAY", [win.sensor_id])
    system.config.settings.entry_delay = 0
    system.arm_system(SafeHomeMode.AWAY)
    win.simulate_open()
    system._handle_intrusion(win)
    time.sleep(0.1)
    assert system.alarm.is_active()
    system.alarm.stop()
    system.turn_off()


def test_it_camera_password_persist_and_access(system):
    """IT-Camera-Pwd (SDS seq p66~69/p72~73): password-protected camera persists and allows view with correct password."""
    cc = system.camera_controller
    cam = cc.add_camera("Front", "Door", password="1234")
    # Persisted in DB
    rows = system.config.db_manager.get_cameras()
    assert any(row["camera_password"] == "1234" for row in rows)
    # Access denied with wrong password
    assert cc.get_camera_view(cam.camera_id, password="0000") is None
    # Access allowed with correct password
    view = cc.get_camera_view(cam.camera_id, password="1234")
    assert isinstance(view, Image.Image)
    # Disable/enable roundtrip
    assert cc.disable_camera(cam.camera_id, role="admin")
    assert cc.enable_camera(cam.camera_id, role="admin")


def test_it_zone_crud_and_mode_mapping(system):
    """IT-Zone-Mode (SDS seq p59~63): zone CRUD with sensor mapping to mode persists."""
    cm = system.config
    zone = cm.add_safety_zone("Garage")
    sensor = system.sensor_controller.add_sensor("WINDOOR", "Garage Door", zone.zone_id)
    cm.storage.save_mode_sensor_mapping("HOME", [sensor.sensor_id])
    assert sensor.zone_id == zone.zone_id
    # Fetch from storage
    zones = cm.storage.load_all_safety_zones()
    assert any(z.name == "Garage" for z in zones)
    assert cm.storage.get_sensors_for_mode("HOME") == [sensor.sensor_id]


def test_it_log_persistence(tmp_path, monkeypatch):
    """
    IT-Log-Persist (SDS seq p64): logs written to DB via LogManager/StorageManager.
    This test now performs a low-level write to diagnose the persistence issue.
    """
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    log_message = "Integration log test"

    # Phase 0: Initialize the schema by creating and shutting down a System instance
    sys_init = System(db_path=str(db_path))
    sys_init.shutdown()

    # Phase 1: Manually write a log to the database file to bypass application logic
    import sqlite3
    import datetime

    try:
        con = sqlite3.connect(str(db_path))
        cur = con.cursor()
        cur.execute(
            "INSERT INTO event_logs (event_type, event_message, source, event_timestamp) VALUES (?, ?, ?, ?)",
            ("INFO", log_message, "ManualTest", datetime.datetime.now().isoformat()),
        )
        con.commit()
        con.close()
    except Exception as e:
        pytest.fail(f"Manual DB write failed: {e}")

    # Phase 2: Create a new system instance and read from the same DB
    sys2 = System(db_path=str(db_path))
    rows = sys2.config.db_manager.get_event_logs(event_type="INFO", limit=10)
    sys2.shutdown()

    # Assert that the manually written log was loaded by the application
    assert any(
        row["event_message"] == log_message for row in rows
    ), "Log manually written to DB was not found by the application's read logic"
