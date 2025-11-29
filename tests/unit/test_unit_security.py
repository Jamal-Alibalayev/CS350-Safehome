import time
import pytest

from safehome.configuration.configuration_manager import ConfigurationManager
from safehome.configuration.system_settings import SystemSettings
from safehome.configuration.storage_manager import StorageManager
from safehome.core.system import System
from safehome.device.sensor.sensor_controller import SensorController
from safehome.device.sensor.windoor_sensor import WindowDoorSensor
from safehome.device.sensor.motion_sensor import MotionSensor
from safehome.configuration.safehome_mode import SafeHomeMode
from safehome.configuration.login_manager import LoginManager


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    """Avoid GUI popups in device layers."""
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def system(tmp_path, monkeypatch):
    """Isolated System instance with temporary DB."""
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    sys = System(db_path=str(tmp_path / "safehome.db"))
    yield sys
    sys.shutdown()


def test_sensor_controller_add_poll_remove(system):
    """UT-Sensor-Add-Poll (SDS state p40): add, arm, poll, remove."""
    sc = system.sensor_controller
    # Add sensors
    win = sc.add_sensor("WINDOOR", "Front Door")
    mot = sc.add_sensor("MOTION", "Hall")
    # Arm and simulate intrusion
    win.arm()
    win.simulate_open()
    mot.arm()
    mot.simulate_motion()
    detections = sc.poll_sensors()
    assert {sid for sid, _ in detections} == {win.sensor_id, mot.sensor_id}
    # Remove
    assert sc.remove_sensor(win.sensor_id)
    assert sc.get_sensor(win.sensor_id) is None


def test_sensor_controller_check_all_windoor_closed(system):
    """UT-Sensor-ClosedCheck (SDS seq p55): open sensor prevents arming."""
    sc = system.sensor_controller
    win = sc.add_sensor("WINDOOR", "Back Door")
    win.arm()
    win.simulate_open()
    all_closed, open_sensors = sc.check_all_windoor_closed()
    assert not all_closed
    assert open_sensors == [win]


def test_window_and_motion_sensor_behaviors():
    """UT-Sensor-Behaviors (SDS state p37/p42): armed state gating read()."""
    win = WindowDoorSensor(1, "Door")
    mot = MotionSensor(2, "Hall")
    # Disarmed reads should be False
    assert not win.read()
    assert not mot.read()
    # Armed + intrude -> True
    win.arm()
    win.simulate_open()
    assert win.read()
    win.disarm()
    assert not win.read()

    mot.arm()
    mot.simulate_motion()
    assert mot.read()
    mot.disarm()
    assert not mot.read()


def test_login_manager_lock_and_unlock():
    """UT-Login-Lock (SDS state p29~30): lockout after max attempts and unlock later."""
    settings = SystemSettings(max_login_attempts=2, system_lock_time=1)
    lm = LoginManager(settings)
    assert not lm.validate_credentials("admin", "wrong", "CONTROL_PANEL")
    assert not lm.validate_credentials("admin", "wrong", "CONTROL_PANEL")
    assert lm.is_interface_locked("CONTROL_PANEL")
    # Wait for auto-unlock
    time.sleep(1.1)
    lm.unlock_system("CONTROL_PANEL")
    assert not lm.is_interface_locked("CONTROL_PANEL")
    # Correct password works
    assert lm.validate_credentials("admin", settings.master_password, "CONTROL_PANEL")


def test_system_arm_disarm_and_alarm(system):
    """UT-System-ArmDisarm (SDS seq p55/p58): arming requires closed doors; alarm triggers on intrusion."""
    sys = system
    sc = sys.sensor_controller
    # Add a window sensor and keep it closed
    win = sc.add_sensor("WINDOOR", "Patio")
    # Map sensor to AWAY mode so arming activates it
    sys.config.storage.save_mode_sensor_mapping("AWAY", [win.sensor_id])
    assert sys.arm_system(SafeHomeMode.AWAY)
    assert win.is_active
    # Disarm clears
    sys.disarm_system()
    assert not win.is_active

    # Intrusion path with zero delay
    sys.config.settings.entry_delay = 0
    sys.turn_on()
    sys.config.set_mode(SafeHomeMode.AWAY)
    win.arm()
    win.simulate_open()
    sys._handle_intrusion(win)
    time.sleep(0.1)
    assert sys.alarm.is_active()
    sys.alarm.stop()
    sys.turn_off()


def test_system_login_and_password_change(system):
    """UT-System-Login (SDS seq p47/p54): login succeeds and password change persists."""
    sys = system
    assert sys.login("admin", sys.config.settings.master_password, "CONTROL_PANEL")
    # Change password and verify
    changed = sys.change_password(
        sys.config.settings.master_password, "9999", "CONTROL_PANEL"
    )
    assert changed
    assert sys.login("admin", "9999", "CONTROL_PANEL")
