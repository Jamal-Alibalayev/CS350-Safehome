import pytest

from safehome.configuration.safehome_mode import SafeHomeMode
from safehome.configuration.storage_manager import StorageManager
from safehome.core.system import System


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def system(tmp_path, monkeypatch):
    db_path = tmp_path / "monitor.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "monitor.json"))
    sys = System(db_path=str(db_path))
    yield sys
    sys.shutdown()


def test_st_monitoring_call_logged(system):
    """
    ST-Monitoring-Call: triggering alarm logs monitoring service call.
    """
    sc = system.sensor_controller
    sensor = sc.add_sensor("WINDOOR", "Lab Door")
    system.config.storage.save_mode_sensor_mapping("AWAY", [sensor.sensor_id])
    system.config.settings.entry_delay = 0
    system.turn_on()
    assert system.arm_system(SafeHomeMode.AWAY)

    sensor.simulate_open()
    system._handle_intrusion(sensor)
    logs = system.config.db_manager.get_event_logs(event_type="ALARM", limit=5)
    assert logs, "Alarm events should be recorded"
    system.alarm.stop()
    system.turn_off()


def test_st_monitoring_call_direct(system, capsys):
    """
    ST-Monitoring-Call external stub: call_monitoring_service runs without error.
    """
    sensor = system.sensor_controller.add_sensor("WINDOOR", "Front Door")
    system.call_monitoring_service(sensor)
    captured = capsys.readouterr()
    assert "Calling" in captured.out
