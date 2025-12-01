import pytest

from safehome.core.system import System
from safehome.configuration.safehome_mode import SafeHomeMode
from safehome.configuration.storage_manager import StorageManager


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


def test_st_power_cycle(tmp_path, monkeypatch):
    """
    ST-Power-Cycle: turn on/off/reset preserves config and disarms safely on off.
    """
    db_path = tmp_path / "power.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "power.json"))

    sys = System(db_path=str(db_path))
    try:
        sc = sys.sensor_controller
        sensor = sc.add_sensor("WINDOOR", "Entry Door")
        sys.config.storage.save_mode_sensor_mapping("AWAY", [sensor.sensor_id])

        sys.turn_on()
        assert sys.arm_system(SafeHomeMode.AWAY)
        assert sys.is_running
        assert sensor.is_active

        sys.turn_off()
        assert not sys.is_running
        # turn_off should save; sensor remains configured
        sys.turn_on()
        assert sys.is_running
        # sensors are reloaded and can be re-armed
        assert sys.arm_system(SafeHomeMode.AWAY)
        sys.disarm_system()
    finally:
        sys.shutdown()
