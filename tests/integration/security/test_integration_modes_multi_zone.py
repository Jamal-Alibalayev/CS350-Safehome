import pytest
import time

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


def test_it_mode_interaction_multi_zone(system):
    """IT-Mode-Interaction-MultiZone: Zone A armed, Zone B disarmed; intrusion only from armed zone."""
    cm = system.config
    sc = system.sensor_controller
    zone_a = cm.add_safety_zone("A")
    zone_b = cm.add_safety_zone("B")
    sa = sc.add_sensor("WINDOOR", "A Door", zone_a.zone_id)
    sb = sc.add_sensor("WINDOOR", "B Door", zone_b.zone_id)

    # Arm only zone A
    system.arm_zone(zone_a.zone_id)
    assert sa.is_active and not sb.is_active

    # Intrusion on zone B should not trigger when disarmed
    sb.simulate_open()
    detections = sc.poll_sensors()
    assert all(d[0] != sb.sensor_id for d in detections)

    # Intrusion on zone A should trigger alarm
    sa.simulate_open()
    detections = sc.poll_sensors()
    ids = {sid for sid, _ in detections}
    assert sa.sensor_id in ids
    system._handle_intrusion(sa)
    time.sleep(0.05)
    system.alarm.stop()
