import pytest

from safehome.core.system import System
from safehome.configuration.storage_manager import StorageManager


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def system(tmp_path, monkeypatch):
    db_path = tmp_path / "ui.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "ui.json"))
    sys = System(db_path=str(db_path))
    yield sys
    sys.shutdown()


def test_st_login_cp_success(system):
    """
    ST-Login-CP-Su: control panel login scenario (logic-level).
    """
    assert system.login("admin", system.config.settings.master_password, "CONTROL_PANEL")
    assert system.config.login_manager.failed_attempts["CONTROL_PANEL"] == 0


def test_st_zone_crud_ui_flow(system):
    """
    ST-Zone-CRUD-UI: create/edit/delete zones via configuration layer.
    """
    cm = system.config
    zone = cm.add_safety_zone("UI Zone")
    assert zone and zone.zone_id
    assert cm.update_safety_zone(zone.zone_id, zone_name="Renamed")
    assert cm.get_safety_zone(zone.zone_id).name == "Renamed"
    assert cm.delete_safety_zone(zone.zone_id)
    assert cm.get_safety_zone(zone.zone_id) is None


def test_st_sensor_sim_flow(system):
    """
    ST-Sensor-Sim-Flow: simulate sensors and verify state reflects.
    """
    sc = system.sensor_controller
    door = sc.add_sensor("WINDOOR", "Sim Door")
    motion = sc.add_sensor("MOTION", "Sim Motion")
    door.simulate_open()
    assert door.is_open()
    motion.simulate_motion()
    assert motion.is_motion_detected()
    door.simulate_close()
    motion.simulate_clear()
    assert not door.is_open()
    assert not motion.is_motion_detected()


def test_st_camera_ptz_view(system):
    """
    ST-Camera-PTZ-View: PTZ actions and view retrieval headless.
    """
    cam = system.camera_controller.add_camera("Hall", "Hallway")
    view = system.camera_controller.get_camera_view(cam.camera_id)
    assert view is not None
    assert system.camera_controller.pan_camera(cam.camera_id, "left")
    assert system.camera_controller.tilt_camera(cam.camera_id, "up")
    assert system.camera_controller.zoom_camera(cam.camera_id, "in")


def test_st_log_viewer_logic(system):
    """
    ST-Logs-View-Clear: log retrieval and clear without UI.
    """
    logger = system.config.logger
    storage = system.config.storage
    logger.add_log("Log A", source="UI", level="INFO")
    logger.add_log("Log B", source="UI", level="INFO")
    logs = storage.get_logs(limit=5)
    assert any("Log A" in row["event_message"] for row in logs)
    storage.clear_logs()
    assert storage.get_logs(limit=5) == []


def test_st_logout_session_logic(system):
    """
    ST-Logout-Session: simulate session end by clearing lock and ensuring re-login works.
    """
    lm = system.config.login_manager
    system.login("admin", system.config.settings.master_password, "CONTROL_PANEL")
    lm._lock_interface("CONTROL_PANEL")
    assert lm.is_interface_locked("CONTROL_PANEL")
    lm.unlock_system("CONTROL_PANEL")
    assert not lm.is_interface_locked("CONTROL_PANEL")
    assert system.login("admin", system.config.settings.master_password, "CONTROL_PANEL")
