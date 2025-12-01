import pytest
from PIL import Image

from safehome.configuration.storage_manager import StorageManager
from safehome.core.system import System


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def system(tmp_path, monkeypatch):
    db_path = tmp_path / "safehome.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    sys = System(db_path=str(db_path))
    yield sys
    sys.shutdown()


def test_it_cam_enabledisable(system):
    """IT-Cam-EnableDisable: admin role enables/disables camera and persists."""
    cc = system.camera_controller
    cam = cc.add_camera("Front", "Door")
    assert cc.disable_camera(cam.camera_id, role="admin")
    status = cc.get_camera_status(cam.camera_id)
    assert status and status["is_enabled"] is False
    assert cc.enable_camera(cam.camera_id, role="admin")
    status2 = cc.get_camera_status(cam.camera_id)
    assert status2["is_enabled"] is True


def test_it_cam_delete_password_and_view(system):
    """IT-Cam-DeletePwd: remove password then view without password."""
    cc = system.camera_controller
    cam = cc.add_camera("Cam", "Room", password="pw")
    assert cc.delete_camera_password(cam.camera_id, old_password="pw")
    view = cc.get_camera_view(cam.camera_id, password=None)
    assert isinstance(view, Image.Image)


def test_it_cam_lockout(monkeypatch, system):
    """IT-Cam-Lockout: repeated wrong password triggers lockout."""
    cc = system.camera_controller
    cam = cc.add_camera("LockCam", "Lab", password="pw")
    cam.max_attempts = 1
    assert cc.get_camera_view(cam.camera_id, password="bad") is None
    assert cc.get_camera_view(cam.camera_id, password="pw") is None  # locked
