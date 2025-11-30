import os
import pytest

from safehome.device.sensor.device_sensor_tester import DeviceSensorTester


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


def test_device_sensor_tester_existing_window(monkeypatch):
    """UT-SensorTester-Existing: existing window with winfo_exists returns early."""
    class DummyWin:
        def winfo_exists(self): return True
        def deiconify(self): pass
        def lift(self): pass
    DeviceSensorTester.safeHomeSensorTest = DummyWin()
    DeviceSensorTester.showSensorTester()
    assert isinstance(DeviceSensorTester.safeHomeSensorTest, DummyWin)


def test_device_sensor_tester_headless_and_exception(monkeypatch):
    """UT-SensorTester-Headless/Exception: headless returns; exception handled."""
    # Headless path: should return without creating window
    DeviceSensorTester.safeHomeSensorTest = None
    os.environ["SAFEHOME_HEADLESS"] = "1"
    DeviceSensorTester.showSensorTester()
    # Non-headless with Tk error
    os.environ.pop("SAFEHOME_HEADLESS", None)
    monkeypatch.setattr("tkinter.Tk", lambda: (_ for _ in ()).throw(RuntimeError("fail")))
    DeviceSensorTester.showSensorTester()
    assert DeviceSensorTester.safeHomeSensorTest is None
