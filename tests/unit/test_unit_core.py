import time
import pytest
import types

from safehome.configuration.storage_manager import StorageManager
from safehome.core.system import System
from safehome.device.alarm.alarm import Alarm
from safehome.device.sensor.windoor_sensor import WindowDoorSensor


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    """Avoid GUI popups in device layers."""
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def system(tmp_path, monkeypatch):
    """Isolated System with temporary DB."""
    db_path = tmp_path / "safehome.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    sys = System(db_path=str(db_path))
    yield sys
    sys.shutdown()


def test_system_turn_on_off(system):
    """UT-System-OnOff (SDS seq p50/p52): toggles running state and polling thread."""
    system.turn_on()
    assert system.is_running
    system.turn_off()
    assert not system.is_running


def test_system_status_snapshot(system):
    """UT-System-Status (SDS class/state p41): get_system_status reflects state."""
    status = system.get_system_status()
    assert status["is_running"] is False
    assert status["num_sensors"] == len(system.sensor_controller.sensors)


def test_alarm_ring_and_stop():
    """UT-Alarm-Ring (SDS state p35): alarm toggles ringing flag."""
    alarm = Alarm(duration=0.1)
    alarm.ring()
    assert alarm.is_active()
    time.sleep(0.2)
    assert not alarm.is_active()
    alarm.stop()


def test_system_polling_start_stop(system, monkeypatch):
    """UT-System-Polling: start/stop polling threads safely."""
    started = {}

    def fake_loop():
        started["ran"] = True

    monkeypatch.setattr(system, "_sensor_polling_loop", fake_loop)
    system._start_sensor_polling()
    time.sleep(0.05)
    system._stop_sensor_polling()
    assert started.get("ran")


def test_system_trigger_alarm_and_stop(system):
    """UT-System-Trigger: trigger alarm and stop polling."""
    system.turn_on()
    fake_sensor = types.SimpleNamespace(location="Test")
    system._trigger_alarm(fake_sensor)
    assert system.alarm.is_active()
    system.alarm.stop()
    system._stop_sensor_polling()
    system.turn_off()


def test_system_shutdown_calls_components(system):
    """UT-System-Shutdown: shutdown does not raise."""
    system.shutdown()


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
