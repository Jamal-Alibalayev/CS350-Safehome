import pytest
from unittest.mock import Mock

from safehome.device.sensor.device_sensor_tester import DeviceSensorTester
from safehome.device.sensor.device_motion_detector import DeviceMotionDetector
from safehome.device.sensor.device_windoor_sensor import DeviceWinDoorSensor
from safehome.device.sensor.motion_sensor import MotionSensor
from safehome.device.sensor.windoor_sensor import WindowDoorSensor
from safehome.device.camera.device_camera import DeviceCamera


@pytest.fixture
def mock_system():
    """Provides a mock System object that can be passed to showSensorTester."""
    return Mock()


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


def test_device_sensor_tester_headless_skip(mock_system):
    """UT-DeviceSensorTester-Headless: showSensorTester no-ops in headless."""
    DeviceSensorTester.safeHomeSensorTest = None
    DeviceSensorTester.showSensorTester(mock_system)
    assert DeviceSensorTester.safeHomeSensorTest is None


def test_motion_and_windoor_test_armed_state_and_accessors():
    """UT-Sensor-Accessors: getters/setters and test_armed_state on concrete sensors."""
    win = WindowDoorSensor(10, "Door", zone_id=1)
    mot = MotionSensor(11, "Hall", zone_id=2)
    assert win.get_id() == 10
    assert win.get_type() == "WINDOOR"
    assert win.get_location() == "Door"
    assert win.get_zone_id() == 1
    win.set_zone_id(3)
    assert win.get_zone_id() == 3
    assert isinstance(win.get_status(), dict)

    mot.arm()
    assert mot.test_armed_state()
    mot.simulate_motion()
    assert mot.is_motion_detected()
    mot.simulate_clear()
    assert not mot.is_motion_detected()


def test_device_motion_detector_and_windoor_hardware():
    """UT-DeviceHardware: basic intrude/release/arm state on hardware layer."""
    md = DeviceMotionDetector()
    md.arm()
    assert md.test_armed_state()
    md.intrude()
    assert md.read()
    md.release()
    md.disarm()
    assert not md.read()

    wd = DeviceWinDoorSensor()
    wd.arm()
    assert wd.test_armed_state()
    wd.intrude()
    assert wd.read()
    wd.release()
    wd.disarm()
    assert not wd.read()


def test_device_camera_tick_and_id(monkeypatch):
    """UT-DeviceCamera-Tick: _tick increments time safely."""
    shown = {}

    def fake_showerror(title, msg):
        shown["msg"] = msg

    monkeypatch.setattr("tkinter.messagebox.showerror", fake_showerror)
    cam = DeviceCamera()
    cam._tick()
    assert cam.time == 1
    cam.stop()
