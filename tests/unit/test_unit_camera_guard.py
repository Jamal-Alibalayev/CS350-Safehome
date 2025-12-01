import time
import pytest
from PIL import Image

from safehome.device.camera.camera_controller import CameraController, CameraAccessGuard
from safehome.device.camera.safehome_camera import SafeHomeCamera
from safehome.configuration.configuration_manager import ConfigurationManager
from safehome.configuration.storage_manager import StorageManager


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def controller(tmp_path, monkeypatch):
    db_path = tmp_path / "safehome.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    cm = ConfigurationManager(db_path=str(db_path))
    cc = CameraController(
        storage_manager=cm.storage,
        logger=cm.logger,
        login_manager=cm.login_manager,
        settings=cm.settings,
    )
    yield cc
    cc.shutdown()
    cm.shutdown()


def test_camera_access_guard_denies_when_locked(monkeypatch):
    """UT-CamGuard-Require (SDS p66~69): guard denies on password mismatch."""
    log_msgs = []

    class DummyLogger:
        def add_log(self, msg, **kwargs):
            log_msgs.append(msg)

    guard = CameraAccessGuard(logger=DummyLogger())
    cam = SafeHomeCamera(1, "Lab", "Lab", password="pw", max_attempts=1, lockout_seconds=1)
    assert guard.require_access(cam, 1, "bad", "view") is None
    assert log_msgs
    cam.verify_password("bad")
    assert cam.is_locked()
    assert guard.require_access(cam, 1, "pw", "view") is None
    cam.stop()


def test_camera_controller_get_camera_with_access(controller):
    """UT-CamCtrl-AccessHelper: internal access helper honors passwords."""
    cam = controller.add_camera("Front", "Door", password="1234")
    helper = controller._get_camera_with_access(cam.camera_id, password="0000", action="view")
    assert helper is None
    helper_ok = controller._get_camera_with_access(cam.camera_id, password="1234", action="view")
    assert helper_ok is not None
    controller.shutdown()


def test_safehome_camera_lock_and_status():
    """UT-Cam-LockStatus: lockout resets after timeout and status reflects fields."""
    cam = SafeHomeCamera(2, "Kitchen", "Kitchen", password="pw", max_attempts=1, lockout_seconds=0.1)
    assert not cam.verify_password("bad")
    assert cam.is_locked()
    time.sleep(0.11)
    assert cam.verify_password("pw")
    status = cam.get_status()
    assert status["name"] == "Kitchen"
    cam.stop()


def test_camera_controller_remove_and_statuses(controller):
    """UT-CamCtrl-Status: remove_camera and get_all_camera_statuses."""
    cam1 = controller.add_camera("A", "L1")
    cam2 = controller.add_camera("B", "L2")
    statuses = controller.get_all_camera_statuses()
    assert len(statuses) == 2
    assert controller.remove_camera(cam1.camera_id)
    assert controller.get_camera(cam1.camera_id) is None
    assert len(controller.get_all_cameras()) == 1
