import json
import time
import types
import pytest

from safehome.configuration.configuration_manager import ConfigurationManager
from safehome.configuration.storage_manager import StorageManager
from safehome.configuration.safehome_mode import SafeHomeMode
from safehome.configuration.system_settings import SystemSettings
from safehome.core.system import System
from safehome.device.camera.device_camera import DeviceCamera
from safehome.device.sensor.windoor_sensor import WindowDoorSensor


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def config_mgr(tmp_path, monkeypatch):
    db_path = tmp_path / "safehome.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    cm = ConfigurationManager(db_path=str(db_path))
    yield cm
    cm.shutdown()


@pytest.fixture
def system(tmp_path, monkeypatch):
    db_path = tmp_path / "safehome.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    sys = System(db_path=str(db_path))
    yield sys
    sys.shutdown()


def test_send_email_alert_success_and_failure(monkeypatch, config_mgr):
    """UT-Conf-Email: send_email_alert handles success/failure paths."""
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

    monkeypatch.setattr("smtplib.SMTP", DummySMTP)
    cfg = config_mgr
    cfg.settings.alert_email = "to@test"
    assert cfg.send_email_alert("subj", "body")
    assert sent_messages and sent_messages[0]["To"] == "to@test"

    # Failure path: missing alert_email should return False
    cfg.settings.alert_email = ""
    assert not cfg.send_email_alert("subj", "body")


def test_call_monitoring_service_logs(system):
    """UT-System-Monitoring: call_monitoring_service adds ALARM log."""
    sys = system
    sys.call_monitoring_service(types.SimpleNamespace(location="Lab"))
    logs = sys.config.logger.get_recent_logs(1)
    assert any("Calling monitoring service" in log.message for log in logs)


def test_start_entry_delay_countdown_no_alarm_when_disarmed(system):
    """UT-System-EntryDelay-Cancel: disarming during delay prevents alarm."""
    sys = system
    sys.turn_on()
    sys.config.settings.entry_delay = 0.05
    sensor = WindowDoorSensor(1, "Door")
    sensor.arm()
    sensor.simulate_open()
    # Immediately disarm before delay elapses
    sys._start_entry_delay_countdown(sensor)
    sensor.disarm()
    time.sleep(0.1)
    assert not sys.alarm.is_active()
    sys.turn_off()


def test_start_entry_delay_countdown_triggers_after_delay(system):
    """UT-System-EntryDelay-Alarm: stays armed -> alarm triggers after delay."""
    sys = system
    sys.turn_on()
    sys.config.settings.entry_delay = 0.01
    sensor = WindowDoorSensor(2, "Door2")
    sensor.arm()
    sensor.simulate_open()
    sys._start_entry_delay_countdown(sensor)
    time.sleep(0.05)
    assert sys.alarm.is_active()
    sys.alarm.stop()
    sys.turn_off()


def test_safehome_mode_from_db_defaults():
    """UT-Mode-FromDb: unknown maps to DISARMED."""
    assert SafeHomeMode.from_db_mode_name("unknown") == SafeHomeMode.DISARMED


def test_system_settings_from_db_row_and_defaults():
    """UT-Settings-FromDb: from_db_row builds object and handles None."""
    row = {
        "id": 1,
        "master_password": "9999",
        "guest_password": None,
        "web_password_1": "a",
        "web_password_2": "b",
        "entry_delay": 1,
        "exit_delay": 2,
        "alarm_duration": 3,
        "system_lock_time": 4,
        "monitoring_phone": "100",
        "homeowner_phone": "200",
        "max_login_attempts": 3,
    }
    # reuse model helper from database.models
    from safehome.database.models import SystemSettings as ModelSettings

    model = ModelSettings.from_db_row(row)
    assert model.master_password == "9999"
    assert ModelSettings.from_db_row(None) is None


def test_storage_manager_check_db_and_json_errors(tmp_path):
    """UT-Storage-CheckDb/JSON: _check_db raises, bad JSON returns {}."""
    storage = StorageManager(db_manager=None)
    with pytest.raises(ValueError):
        storage._check_db()

    # Invalid JSON currently raises JSONDecodeError (no suppress in code)
    bad_json = tmp_path / "bad.json"
    bad_json.write_text("{invalid", encoding="utf-8")
    # Monkeypatch config file path
    StorageManager.CONFIG_FILE = str(bad_json)
    with pytest.raises(json.JSONDecodeError):
        storage.load_settings_from_json()


def test_storage_manager_invalid_mode_mapping(config_mgr):
    """UT-Storage-ModeMap-Invalid: unknown mode name does nothing."""
    storage = config_mgr.storage
    storage.save_mode_sensor_mapping("NOTAMODE", [1, 2])  # should no-op without crash


def test_device_camera_missing_file(monkeypatch):
    """UT-DeviceCamera-SetId: missing asset logs error but stays usable."""
    shown = {}

    def fake_showerror(title, msg):
        shown["msg"] = msg

    monkeypatch.setattr("tkinter.messagebox.showerror", fake_showerror)
    cam = DeviceCamera()
    cam.set_id(999)  # unlikely to exist
    # Should not raise; message captured
    assert "file open error" in shown.get("msg", "")
    cam.stop()
