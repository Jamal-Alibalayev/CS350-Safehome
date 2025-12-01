import time

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


def test_it_cam_lockout_recover(system):
    """IT-Cam-Lockout-Recover: lockout then recover after timeout."""
    cc = system.camera_controller
    cam = cc.add_camera("LockCam", "Lab", password="pw")
    cam.max_attempts = 1
    cam.lockout_seconds = 0.2
    assert cc.get_camera_view(cam.camera_id, password="bad") is None
    # Should be locked now
    assert cc.get_camera_view(cam.camera_id, password="pw") is None
    time.sleep(0.25)
    view = cc.get_camera_view(cam.camera_id, password="pw")
    assert isinstance(view, Image.Image)


def test_it_cam_bad_direction(system):
    """IT-Cam-BadDirection: invalid directions return False safely."""
    cc = system.camera_controller
    cam = cc.add_camera("DirCam", "Hall")
    assert cc.pan_camera(cam.camera_id, "noop") is False
    assert cc.tilt_camera(cam.camera_id, "noop") is False
    assert cc.zoom_camera(cam.camera_id, "noop") is False
