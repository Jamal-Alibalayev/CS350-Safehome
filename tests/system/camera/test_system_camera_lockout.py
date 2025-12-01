import time
import pytest

from safehome.core.system import System
from safehome.configuration.storage_manager import StorageManager


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def system(tmp_path, monkeypatch):
    db_path = tmp_path / "cam.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "cam.json"))
    sys = System(db_path=str(db_path))
    # shorten lockout for test
    sys.camera_controller.lockout_seconds = 0.1
    sys.camera_controller.max_attempts = 2
    yield sys
    sys.shutdown()


def test_st_camera_lockout_recover(system):
    """
    ST-Camera-Lockout-Recover: wrong password causes lockout, then unlocks after timeout.
    """
    cam = system.camera_controller.add_camera("Porch", "Front Porch", password="9999")
    assert system.camera_controller.get_camera_view(cam.camera_id, password="0000") is None
    assert system.camera_controller.get_camera_view(cam.camera_id, password="0000") is None
    assert cam.is_locked()

    time.sleep(0.15)
    view = system.camera_controller.get_camera_view(cam.camera_id, password="9999")
    assert view is not None
    assert not cam.is_locked()


def test_st_camera_enable_persist_behavior(system):
    """
    ST-Camera-Enable-Persist: disable blocks access; after restart (state not persisted) camera is enabled again.
    """
    cam = system.camera_controller.add_camera("Porch", "Front Porch", password=None)
    assert system.camera_controller.get_camera_view(cam.camera_id) is not None

    system.camera_controller.disable_camera(cam.camera_id, role="admin")
    assert system.camera_controller.get_camera_view(cam.camera_id) is None

    # Restart system and load cameras from storage; enabled by default after reload
    db_path = system.config.db_manager.db_path
    system.shutdown()
    sys2 = System(db_path=db_path)
    try:
        sys2.camera_controller.load_cameras_from_storage()
        view = sys2.camera_controller.get_camera_view(cam.camera_id)
        assert view is not None  # enabled on restart
    finally:
        sys2.shutdown()
