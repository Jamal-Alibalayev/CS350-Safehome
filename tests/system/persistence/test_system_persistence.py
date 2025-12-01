import pytest

from safehome.configuration.safehome_mode import SafeHomeMode
from safehome.configuration.storage_manager import StorageManager
from safehome.core.system import System


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    """Avoid GUI popups during system-level flows."""
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


def _new_system(tmp_path, monkeypatch, db_name="safehome.db"):
    db_path = tmp_path / db_name
    monkeypatch.setattr(
        StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"), raising=False
    )
    return System(db_path=str(db_path))


def test_st_power_loss_recover(tmp_path, monkeypatch):
    """
    ST-Power-Loss-Recover: config persists across restart after abrupt stop.
    """
    sys1 = _new_system(tmp_path, monkeypatch, "safehome.db")
    try:
        cm1 = sys1.config

        zone = cm1.add_safety_zone("Garage")
        sensor = sys1.sensor_controller.add_sensor(
            "WINDOOR", "Garage Door", zone.zone_id
        )
        cm1.storage.save_mode_sensor_mapping("AWAY", [sensor.sensor_id])
        cm1.settings.entry_delay = 0

        cm1.save_configuration()
    finally:
        sys1.shutdown()

    sys2 = _new_system(tmp_path, monkeypatch, "safehome.db")
    try:
        cm2 = sys2.config
        loaded_zone = cm2.get_safety_zone(zone.zone_id)
        assert loaded_zone is not None
        assert loaded_zone.name == "Garage"

        sensors_for_mode = cm2.get_sensors_for_mode("AWAY")
        assert sensor.sensor_id in sensors_for_mode
        assert cm2.settings.entry_delay == 0
    finally:
        sys2.shutdown()


def test_st_config_save_load_roundtrip(tmp_path, monkeypatch):
    """
    ST-Config-Save-Load: modes/zones/sensors saved and reloaded on restart.
    """
    sys1 = _new_system(tmp_path, monkeypatch, "config_rt.db")
    try:
        cm1 = sys1.config

        zone = cm1.add_safety_zone("Office")
        sensor = sys1.sensor_controller.add_sensor(
            "MOTION", "Office Motion", zone.zone_id
        )
        cm1.storage.save_mode_sensor_mapping("HOME", [sensor.sensor_id])
        cm1.settings.alarm_duration = 7
        cm1.save_configuration()
    finally:
        sys1.shutdown()

    sys2 = _new_system(tmp_path, monkeypatch, "config_rt.db")
    try:
        cm2 = sys2.config
        assert cm2.settings.alarm_duration == 7
        assert cm2.get_safety_zone(zone.zone_id).name == "Office"

        # Reload sensors into controller for arming behavior
        sys2.sensor_controller.load_sensors_from_storage()
        sensors_for_home = cm2.get_sensors_for_mode("HOME")
        assert sensor.sensor_id in sensors_for_home

        sys2.turn_on()
        assert sys2.arm_system(SafeHomeMode.HOME)
        sys2.disarm_system()
    finally:
        sys2.shutdown()
