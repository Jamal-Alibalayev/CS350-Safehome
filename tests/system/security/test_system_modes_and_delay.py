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
    db_path = tmp_path / "modes.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "modes.json"))
    sys = System(db_path=str(db_path))
    yield sys
    sys.shutdown()


def test_st_mode_stay_vs_away(system):
    """
    ST-Mode-Stay-Away: Stay arms perimeter only; Away arms all.
    """
    sc = system.sensor_controller
    door = sc.add_sensor("WINDOOR", "Front Door")
    motion = sc.add_sensor("MOTION", "Hall Motion")
    system.config.storage.save_mode_sensor_mapping("HOME", [door.sensor_id])  # Stay
    system.config.storage.save_mode_sensor_mapping(
        "AWAY", [door.sensor_id, motion.sensor_id]
    )

    system.turn_on()
    assert system.arm_system(SafeHomeMode.HOME)
    assert door.is_active
    assert not motion.is_active

    system.disarm_system()
    assert system.arm_system(SafeHomeMode.AWAY)
    assert door.is_active
    assert motion.is_active
    system.disarm_system()
    system.turn_off()


def test_st_intrusion_delay_alarm(system):
    """
    ST-Intrusion-Delay-Alarm: entry delay honored then alarm triggers.
    """
    sc = system.sensor_controller
    sensor = sc.add_sensor("WINDOOR", "Back Door")
    system.config.storage.save_mode_sensor_mapping("AWAY", [sensor.sensor_id])
    system.config.settings.entry_delay = 0.05

    system.turn_on()
    assert system.arm_system(SafeHomeMode.AWAY)

    sensor.simulate_open()
    system._handle_intrusion(sensor)
    time.sleep(0.08)  # wait past delay
    assert system.alarm.is_active()
    system.alarm.stop()
    system.turn_off()
