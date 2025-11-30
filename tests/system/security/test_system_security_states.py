import time
import pytest

from safehome.core.system import System
from safehome.configuration.safehome_mode import SafeHomeMode
from safehome.configuration.storage_manager import StorageManager


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    """Avoid GUI popups during system-level flows."""
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def system(tmp_path, monkeypatch):
    """System instance with isolated storage for security state tests."""
    db_path = tmp_path / "safehome.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    sys = System(db_path=str(db_path))
    yield sys
    sys.shutdown()


def test_st_prearm_ready_not_ready(system):
    """
    ST-PreArm-Ready: arming is blocked while entry sensor open, succeeds after close.
    """
    sc = system.sensor_controller
    sensor = sc.add_sensor("WINDOOR", "Front Door")
    system.config.storage.save_mode_sensor_mapping("AWAY", [sensor.sensor_id])

    sensor.simulate_open()
    system.turn_on()
    assert not system.arm_system(SafeHomeMode.AWAY)

    sensor.simulate_close()
    assert system.arm_system(SafeHomeMode.AWAY)
    assert sensor.is_active


def test_st_alarm_duration_expiry(system):
    """
    ST-Alarm-Duration-Expiry: alarm auto-stops after configured duration.
    """
    system.alarm.set_duration(0.05)
    system.alarm.ring()
    assert system.alarm.is_active()
    time.sleep(0.12)  # duration + buffer
    assert not system.alarm.is_active()


def test_st_mixed_zone_intrusion(system):
    """
    ST-Mixed-Zone-Intrusion: only armed zone triggers detection; disarmed zone ignored.
    """
    cm = system.config
    sc = system.sensor_controller
    zone_a = cm.add_safety_zone("Zone A")
    zone_b = cm.add_safety_zone("Zone B")
    sensor_a = sc.add_sensor("WINDOOR", "A Door", zone_a.zone_id)
    sensor_b = sc.add_sensor("WINDOOR", "B Door", zone_b.zone_id)

    system.arm_zone(zone_a.zone_id)  # only zone A armed
    sensor_b.simulate_open()
    sensor_a.simulate_open()

    detections = sc.poll_sensors()
    triggered_ids = {sid for sid, _ in detections}
    assert sensor_a.sensor_id in triggered_ids
    assert sensor_b.sensor_id not in triggered_ids

    system.alarm.stop()


def test_st_alarm_silence(system):
    """
    ST-Alarm-Silence: alarm can be silenced and system recovers.
    """
    system.alarm.set_duration(1)
    system.alarm.ring()
    assert system.alarm.is_active()
    system.alarm.stop()
    assert not system.alarm.is_active()
