import time
import pytest

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


def test_it_zone_mode_arm(system):
    """IT-Zone-Mode-Arm: arm a specific zone and verify sensors active."""
    cm = system.config
    sc = system.sensor_controller
    zone = cm.add_safety_zone("Garage")
    s1 = sc.add_sensor("WINDOOR", "Garage Door", zone.zone_id)
    s2 = sc.add_sensor("MOTION", "Hall", None)

    system.arm_zone(zone.zone_id)
    assert s1.is_active
    assert not s2.is_active
    system.disarm_zone(zone.zone_id)
    assert not s1.is_active


def test_it_poll_mixed_sensors(system):
    """IT-Poll-MixedSensors: poll returns only armed+triggered sensors."""
    sc = system.sensor_controller
    w = sc.add_sensor("WINDOOR", "Door")
    m = sc.add_sensor("MOTION", "Hall")
    w.arm()
    m.arm()
    w.simulate_open()
    # leave motion not triggered
    detections = sc.poll_sensors()
    ids = {sid for sid, _ in detections}
    assert w.sensor_id in ids
    assert m.sensor_id not in ids


def test_it_monitoring_call_log(system):
    """IT-Monitoring-Call-Log: monitoring call message logged on intrusion handling."""
    sc = system.sensor_controller
    sensor = sc.add_sensor("WINDOOR", "Door")
    sensor.arm()
    sensor.simulate_open()
    system.call_monitoring_service(sensor)
    logs = system.config.logger.get_recent_logs(5)
    assert any("Calling monitoring service" in log.message for log in logs)
