import time
import pytest

from safehome.configuration.storage_manager import StorageManager
from safehome.core.system import System
from safehome.device.alarm.alarm import Alarm


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
