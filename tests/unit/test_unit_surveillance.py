import time
import pytest
from PIL import Image

from safehome.configuration.configuration_manager import ConfigurationManager
from safehome.configuration.storage_manager import StorageManager
from safehome.device.camera.safehome_camera import SafeHomeCamera
from safehome.device.camera.camera_controller import CameraController


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
