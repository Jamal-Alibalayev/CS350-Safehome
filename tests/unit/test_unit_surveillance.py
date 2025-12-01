import time
import pytest
from PIL import Image

from safehome.configuration.configuration_manager import ConfigurationManager
from safehome.configuration.storage_manager import StorageManager
from safehome.device.camera.camera_controller import CameraController
from safehome.device.camera.safehome_camera import SafeHomeCamera
from safehome.device.camera.interface_camera import InterfaceCamera
from safehome.device.camera.device_camera import DeviceCamera


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    """Avoid GUI popups."""
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def camera_controller(tmp_path, monkeypatch):
    """CameraController with isolated DB."""
    db_path = tmp_path / "safehome.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    cm = ConfigurationManager(db_path=str(db_path))
    controller = CameraController(
        storage_manager=cm.storage,
        logger=cm.logger,
        login_manager=cm.login_manager,
        settings=cm.settings,
    )
    yield controller
    controller.shutdown()
    cm.shutdown()


def test_safehome_camera_password_and_lockout():
    """UT-Cam-Pwd (SDS seq p68/p69): password verify + lockout behavior."""
    cam = SafeHomeCamera(
        camera_id=1, name="Lab", location="Lab", password="pw", max_attempts=2, lockout_seconds=1
    )
    assert not cam.verify_password("bad")
    assert not cam.verify_password("bad")
    assert cam.is_locked()
    time.sleep(1.1)
    # After lockout expires, correct password works
    assert cam.verify_password("pw")
    cam.stop()


def test_safehome_camera_controls_and_status():
    """UT-Cam-Controls (SDS state p38/p67): PTZ/zoom boundaries reflected in status."""
    cam = SafeHomeCamera(camera_id=2, name="Kitchen", location="Kitchen")
    assert cam.pan_left()
    assert cam.pan_right()
    assert cam.tilt_up()
    assert cam.tilt_down()
    # Zoom bounds
    for _ in range(10):
        cam.zoom_out()
    assert cam.zoom_out() is False  # hit lower bound
    for _ in range(10):
        cam.zoom_in()
    assert cam.zoom_in() is False  # hit upper bound
    status = cam.get_status()
    assert status["name"] == "Kitchen"
    cam.stop()


def test_camera_controller_access_and_password(camera_controller):
    """UT-CamCtrl-Access (SDS seq p66~69/p72~73): view requires password when set."""
    cam = camera_controller.add_camera("Front", "Door", password="1234")
    # Wrong password denies view
    assert camera_controller.get_camera_view(cam.camera_id, password="0000") is None
    # Correct password allows view
    view = camera_controller.get_camera_view(cam.camera_id, password="1234")
    assert isinstance(view, Image.Image)
    # Change password
    assert camera_controller.set_camera_password(
        cam.camera_id, new_password="5678", old_password="1234", confirm_password="5678"
    )
    assert camera_controller.delete_camera_password(cam.camera_id, old_password="5678")
    camera_controller.shutdown()


def test_camera_controller_access_denied_branches(tmp_path, monkeypatch):
    """UT-CamCtrl-Branches: bad directions, role denied, password mismatch, missing cam."""
    db_path = tmp_path / "safehome.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    cm = ConfigurationManager(db_path=str(db_path))
    cc = CameraController(
        storage_manager=cm.storage,
        logger=cm.logger,
        login_manager=cm.login_manager,
        settings=cm.settings,
    )
    cam = cc.add_camera("Hall", "Hall", password="1234")
    assert cc.pan_camera(cam.camera_id, "noop", password="1234") is False
    assert cc.tilt_camera(cam.camera_id, "noop", password="1234") is False
    assert cc.zoom_camera(cam.camera_id, "noop", password="1234") is False
    assert cc.enable_camera(cam.camera_id, role="guest") is False
    assert cc.set_camera_password(cam.camera_id, new_password="5678", old_password="wrong") is False
    assert cc.delete_camera_password(cam.camera_id, old_password="bad") is False
    guard = cc.access_guard
    assert guard.require_access(None, 99, None, "view") is None
    cc.load_cameras_from_storage()
    assert cc.get_camera_status(cam.camera_id)["id"] == cam.camera_id
    cc.shutdown()
    cm.shutdown()


def test_camera_controller_lockout_and_require_access(monkeypatch, tmp_path):
    """UT-CamCtrl-Lockout: lockout prevents access in guard."""
    db_path = tmp_path / "safehome.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    cm = ConfigurationManager(db_path=str(db_path))
    cc = CameraController(
        storage_manager=cm.storage,
        logger=cm.logger,
        login_manager=cm.login_manager,
        settings=cm.settings,
    )
    cam = cc.add_camera("Front", "Door", password="pw")
    cam.max_attempts = 1
    cc.get_camera_view(cam.camera_id, password="bad")
    guard = cc.access_guard
    assert guard.require_access(cam, cam.camera_id, password="pw", action="view") is None
    cc.shutdown()
    cm.shutdown()


def test_camera_controller_boundaries_and_status(monkeypatch, tmp_path):
    """UT-CamCtrl-Bounds: PTZ/zoom boundaries and status retrieval."""
    db_path = tmp_path / "safehome.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    cm = ConfigurationManager(db_path=str(db_path))
    cc = CameraController(
        storage_manager=cm.storage,
        logger=cm.logger,
        login_manager=cm.login_manager,
        settings=cm.settings,
    )
    cam = cc.add_camera("Test", "Loc")
    for _ in range(10):
        cc.pan_camera(cam.camera_id, "left")
        cc.pan_camera(cam.camera_id, "right")
        cc.tilt_camera(cam.camera_id, "up")
        cc.tilt_camera(cam.camera_id, "down")
        cc.zoom_camera(cam.camera_id, "in")
        cc.zoom_camera(cam.camera_id, "out")
    assert cc.get_all_camera_statuses()
    cc.shutdown()
    cm.shutdown()


def test_interface_camera_concrete():
    """UT-InterfaceCam: minimal subclass covers abstract methods."""
    class DummyCam(InterfaceCamera):
        def __init__(self):
            self._id = 0
        def set_id(self, id_): self._id = id_
        def get_id(self): return self._id
        def get_view(self): return None
        def pan_right(self): return True
        def pan_left(self): return True
        def zoom_in(self): return True
        def zoom_out(self): return True
    cam = DummyCam()
    cam.set_id(5)
    assert cam.get_id() == 5 and cam.pan_right() and cam.zoom_out()


def test_safehome_camera_getters_and_lock_state():
    """UT-Cam-Getters: SafeHomeCamera getters and lock handling."""
    cam = SafeHomeCamera(1, "Name", "Loc")
    assert cam.get_id() == 1
    assert cam.get_name() == "Name"
    assert cam.get_location() == "Loc"
    assert cam.has_password() is False
    assert cam.verify_password(None)
    cam.set_password("pw")
    cam.verify_password("bad")
    cam.verify_password("bad")
    _ = cam.is_locked()
    cam.stop()


def test_device_camera_view_with_real_image():
    """UT-DeviceCam-View: ensure get_view returns image when asset available."""
    cam = DeviceCamera()
    cam.set_id(1)
    assert cam.get_view() is not None
    cam.stop()


def test_device_camera_missing_file(monkeypatch):
    """UT-DeviceCam-Missing: missing asset logs error but stays usable."""
    shown = {}
    def fake_showerror(title, msg):
        shown["msg"] = msg
    monkeypatch.setattr("tkinter.messagebox.showerror", fake_showerror)
    cam = DeviceCamera()
    cam.set_id(999)
    assert "file open error" in shown.get("msg", "")
    cam.stop()


def test_device_camera_crop_failure(monkeypatch):
    """Force crop failure path inside get_view."""
    cam = DeviceCamera()
    # Provide an imgSource too small and extreme pan/zoom to trigger crop exception
    from PIL import Image
    cam.imgSource = Image.new("RGB", (10, 10), "black")
    cam.centerWidth = 5
    cam.centerHeight = 5
    cam.zoom = 9
    cam.pan = 10
    view = cam.get_view()
    assert view is not None
    cam.stop()
