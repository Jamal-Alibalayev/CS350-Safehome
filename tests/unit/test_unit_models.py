import pytest

from safehome.database import models


def test_model_from_db_row_system_settings_and_zone():
    """UT-Model-SystemSettings/Zone: from_db_row happy and None cases."""
    settings_row = {
        "id": 1,
        "master_password": "9999",
        "guest_password": None,
        "web_password_1": "a",
        "web_password_2": "b",
        "entry_delay": 1,
        "exit_delay": 2,
        "alarm_duration": 3,
        "system_lock_time": 4,
        "monitoring_phone": "100",
        "homeowner_phone": "200",
        "max_login_attempts": 3,
    }
    settings = models.SystemSettings.from_db_row(settings_row)
    assert settings.master_password == "9999"
    assert models.SystemSettings.from_db_row(None) is None

    zone_row = {"zone_id": 5, "zone_name": "Garage", "is_armed": 1}
    zone = models.SafetyZone.from_db_row(zone_row)
    assert zone.zone_name == "Garage" and zone.is_armed is True
    assert models.SafetyZone.from_db_row(None) is None


def test_model_from_db_row_mode_sensor_camera_event_login():
    """UT-Model-Others: SafeHomeMode, Sensor, Camera, EventLog, LoginSession."""
    mode_row = {"mode_id": 1, "mode_name": "HOME", "description": "desc"}
    mode = models.SafeHomeMode.from_db_row(mode_row)
    assert mode.mode_name == "HOME"

    sensor_row = {
        "sensor_id": 2,
        "sensor_type": "WINDOOR",
        "sensor_location": "Door",
        "zone_id": 1,
        "is_active": 1,
    }
    sensor = models.Sensor.from_db_row(sensor_row)
    assert sensor.sensor_location == "Door"

    cam_row = {
        "camera_id": 3,
        "camera_name": "Cam",
        "camera_location": "Hall",
        "camera_password": None,
        "pan_angle": 0,
        "zoom_level": 2,
        "is_enabled": 1,
    }
    cam = models.Camera.from_db_row(cam_row)
    assert cam.camera_name == "Cam" and cam.is_enabled

    log_row = {
        "log_id": 4,
        "event_type": "INFO",
        "event_message": "msg",
        "sensor_id": None,
        "camera_id": None,
        "zone_id": None,
        "source": "System",
    }
    log = models.EventLog.from_db_row(log_row)
    assert log.event_message == "msg"

    sess_row = {
        "session_id": 5,
        "interface_type": "CONTROL_PANEL",
        "username": "admin",
        "login_successful": 1,
        "failed_attempts": 0,
    }
    sess = models.LoginSession.from_db_row(sess_row)
    assert sess.interface_type == "CONTROL_PANEL"
