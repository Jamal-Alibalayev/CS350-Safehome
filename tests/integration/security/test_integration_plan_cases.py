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


def test_it_login_web(system):
    """IT-Login-Web: web interface two-level password accepted and session recorded."""
    cm = system.config
    assert system.login(
        "user", f"{cm.settings.web_password_1}:{cm.settings.web_password_2}", "WEB"
    )
    row = fetch_one(
        cm.db_manager.connection,
        "SELECT interface_type, login_successful FROM login_sessions ORDER BY session_id DESC LIMIT 1",
    )
    assert row[0] == "WEB" and row[1] == 1


def test_it_password_change_cp(system):
    """IT-Password-Change-CP: change password persists."""
    cm = system.config
    assert system.change_password(cm.settings.master_password, "8888", "CONTROL_PANEL")
    row = cm.db_manager.get_system_settings()
    assert row["master_password"] == "8888"


def test_it_reset_config(system):
    """IT-Reset-Config: reset clears camera passwords and recreates default zones."""
    cm = system.config
    cm.storage.save_camera(1, "Cam", "Loc", password="pw")
    cm.reset_configuration()
    zones = cm.get_all_safety_zones()
    assert len(zones) >= 2
    cams = cm.storage.load_all_cameras()
    for c in cams:
        assert c.get("camera_password") is None


def test_it_mode_configure(system):
    """IT-Mode-Configure: configure_mode_sensors maps sensors to mode."""
    sc = system.sensor_controller
    s = sc.add_sensor("WINDOOR", "Door")
    system.config.configure_mode_sensors("HOME", [s.sensor_id])
    assert system.config.get_sensors_for_mode("HOME") == [s.sensor_id]


def test_it_cam_lockout(system):
    """IT-Cam-Lockout: wrong password triggers lockout and denies access."""
    cc = system.camera_controller
    cam = cc.add_camera("Front", "Door", password="pw")
    cam.max_attempts = 1
    assert cc.get_camera_view(cam.camera_id, password="bad") is None
    assert cc.get_camera_view(cam.camera_id, password="pw") is None  # locked


def test_it_email_alert(monkeypatch, system):
    """IT-Email-Alert: send_email_alert success/failure via mock SMTP."""
    sent = []

    class DummySMTP:
        def __init__(self, host, port, timeout):
            self.host, self.port, self.timeout = host, port, timeout

        def starttls(self):
            pass

        def login(self, u, p):
            pass

        def send_message(self, msg):
            sent.append(msg)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False

    monkeypatch.setattr("smtplib.SMTP", DummySMTP)
    cfg = system.config
    cfg.settings.alert_email = "to@test"
    assert cfg.send_email_alert("subj", "body")
    assert sent and sent[0]["To"] == "to@test"
    cfg.settings.alert_email = ""
    assert not cfg.send_email_alert("subj", "body")


def test_it_cp_login_arm_headless(monkeypatch, system):
    """IT-CP-Login-Arm (headless): simulate CP input for login then arm/disarm."""
    from safehome.interface.control_panel.safehome_control_panel import (
        SafeHomeControlPanel,
    )
    from safehome.interface.control_panel.device_control_panel_abstract import (
        DeviceControlPanelAbstract,
    )

    # Patch UI methods to no-op for headless
    monkeypatch.setattr(
        DeviceControlPanelAbstract, "__init__", lambda self, master=None: None
    )
    for name in [
        "set_display_short_message1",
        "set_display_short_message2",
        "set_display_away",
        "set_display_stay",
        "set_display_not_ready",
        "set_armed_led",
        "set_powered_led",
        "set_security_zone_number",
        "_update_display_text",
    ]:
        monkeypatch.setattr(DeviceControlPanelAbstract, name, lambda *a, **k: None)

    panel = SafeHomeControlPanel(system=system)
    for ch in "1234":
        panel._handle_key_input(ch)
    panel.button_sharp()  # login
    assert panel.is_authenticated
    panel._handle_command("0")
    assert not panel.is_authenticated


def test_it_poll_intrusion(system):
    """IT-Poll-Intrusion: poll_sensors detects armed/open sensor and handles intrusion."""
    sc = system.sensor_controller
    sensor = sc.add_sensor("WINDOOR", "Door")
    sensor.arm()
    sensor.simulate_open()
    detections = sc.poll_sensors()
    assert detections
    # manual handle to log alarm
    system._handle_intrusion(sensor)
    time.sleep(0.05)
    system.alarm.stop()
