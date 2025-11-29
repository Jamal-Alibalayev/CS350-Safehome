# SafeHome Unit Test Documentation

## 1. Introduction
This document outlines the unit testing strategy and results for the SafeHome project. It categorizes classes and methods by their core functionality to provide a clear overview of the system's test coverage.

## 2. Functional Categories and Covered Methods

### 2.1. External Communication Management
*   **Note:** There are no dedicated classes for external communication. This functionality is handled by methods within other classes, such as `System` (`call_monitoring_service`, `_send_password_change_alert`) and `ConfigurationManager` (`send_email_alert`).

### 2.2. Surveillance
*   **Classes:** `CameraAccessGuard`, `CameraController`, `DeviceCamera`, `InterfaceCamera`, `SafeHomeCamera`, `Camera`, `DeviceMotionDetector`, `DeviceSensorTester`, `DeviceWinDoorSensor`, `InterfaceSensor`, `MotionSensor`, `Sensor`, `SensorController`, `WindowDoorSensor`, `SafeHomeSensorTest`
*   **Methods:**
    *   `CameraAccessGuard`: `require_access`, `_warn`
    *   `CameraController`: `add_camera`, `remove_camera`, `get_camera`, `get_all_cameras`, `get_camera_view`, `pan_camera`, `tilt_camera`, `zoom_camera`, `enable_camera`, `disable_camera`, `set_camera_password`, `delete_camera_password`, `_get_camera_with_access`, `get_camera_status`, `get_all_camera_statuses`, `load_cameras_from_storage`, `shutdown`
    *   `DeviceCamera`: `set_id`, `get_id`, `get_view`, `pan_right`, `pan_left`, `tilt_up`, `tilt_down`, `zoom_in`, `zoom_out`, `_tick`, `run`, `stop`
    *   `InterfaceCamera`: `set_id`, `get_id`, `get_view`, `pan_right`, `pan_left`, `zoom_in`, `zoom_out`
    *   `SafeHomeCamera`: `get_id`, `get_name`, `get_location`, `get_view`, `pan_left`, `pan_right`, `tilt_up`, `tilt_down`, `zoom_in`, `zoom_out`, `enable`, `disable`, `set_password`, `verify_password`, `has_password`, `is_locked`, `_is_locked`, `get_status`, `stop`
    *   `Camera`: `from_db_row`
    *   `DeviceMotionDetector`: `intrude`, `release`, `get_id`, `read`, `arm`, `disarm`, `test_armed_state`
    *   `DeviceSensorTester`: `intrude`, `release`, `showSensorTester`
    *   `DeviceWinDoorSensor`: `intrude`, `release`, `get_id`, `read`, `arm`, `disarm`, `test_armed_state`
    *   `InterfaceSensor`: `get_id`, `read`, `arm`, `disarm`, `test_armed_state`
    *   `MotionSensor`: `read`, `arm`, `disarm`, `test_armed_state`, `is_motion_detected`, `simulate_motion`, `simulate_clear`
    *   `Sensor`: `read`, `arm`, `disarm`, `test_armed_state`, `get_id`, `get_type`, `get_location`, `get_zone_id`, `set_zone_id`, `get_status`, `from_db_row`
    *   `SensorController`: `add_sensor`, `remove_sensor`, `get_sensor`, `get_all_sensors`, `get_sensors_by_zone`, `get_sensors_by_type`, `arm_sensor`, `disarm_sensor`, `arm_sensors_in_zone`, `disarm_sensors_in_zone`, `arm_sensors`, `disarm_all_sensors`, `poll_sensors`, `check_all_windoor_closed`, `get_sensor_status`, `get_all_sensor_statuses`, `load_sensors_from_storage`
    *   `WindowDoorSensor`: `read`, `arm`, `disarm`, `test_armed_state`, `is_open`, `simulate_open`, `simulate_close`
    *   `SafeHomeSensorTest`: `_create_ui`, `_create_floorplan_section`, `_create_sensor_list`, `_create_right_panel`, `_create_control_panels`, `_update_id_ranges`, `_update_status`, `_collect_windoor_map`, `_collect_motion_map`, `_build_window_rows`, `_build_door_rows`, `_build_motion_rows`, `_get_sensor_states`, `_handle_windoor_sensor`, `_handle_windoor`, `_handle_motion_sensor`, `_handle_motion`, `_arm_all`, `_disarm_all`, `_reset_all`, `_on_mousewheel`, `_bind_mousewheel_recursively`

### 2.3. Security
*   **Classes:** `System`, `LoginInterface`, `LoginManager`, `Alarm`, `DeviceControlPanelAbstract`, `SafeHomeControlPanel`, `LoginWindow`, `LogViewerWindow`, `MainDashboard`, `ZoneManagerWindow`, `AddZoneDialog`, `EditZoneDialog`, `AssignSensorDialog`
*   **Methods:**
    *   `System`: `turn_on`, `turn_off`, `reset`, `shutdown`, `_start_sensor_polling`, `_stop_sensor_polling`, `_sensor_polling_loop`, `_handle_intrusion`, `_start_entry_delay_countdown`, `_trigger_alarm`, `call_monitoring_service`, `arm_system`, `disarm_system`, `arm_zone`, `disarm_zone`, `login`, `change_password`, `_send_password_change_alert`, `_get_sensors_for_mode`, `get_system_status`, `countdown`
    *   `LoginInterface`: `validate_credentials`, `change_password`
    *   `LoginManager`: `validate_credentials`, `_validate_control_panel`, `_lock_interface`, `_log_session`, `change_password`, `change_guest_password`, `unlock_system`, `is_interface_locked`, `get_failed_attempts`, `unlock_after_delay`
    *   `Alarm`: `ring`, `_ring_for_duration`, `stop`, `is_active`, `set_duration`, `get_duration`, `get_status`
    *   `DeviceControlPanelAbstract`: `_update_display_text`, `set_security_zone_number`, `set_display_away`, `set_display_stay`, `set_display_not_ready`, `set_display_short_message1`, `set_display_short_message2`, `set_armed_led`, `set_powered_led`, `button1`, `button2`, `button3`, `button4`, `button5`, `button6`, `button7`, `button8`, `button9`, `button_star`, `button0`, `button_sharp`
    *   `SafeHomeControlPanel`: `_refresh_status_display`, `_reset_interaction`, `_handle_key_input`, `_handle_command`, `_attempt_login`, `_attempt_change_password`, `button1`, `button2`, `button3`, `button4`, `button5`, `button6`, `button7`, `button8`, `button9`, `button0`, `button_star`, `button_sharp`, `button_panic`
    *   `LoginWindow`: `_center_window`, `_create_ui`, `_attempt_login`, `_open_dashboard`
    *   `LogViewerWindow`: `_center_window`, `_create_ui`, `_refresh_logs`, `_toggle_auto_refresh`, `_start_auto_refresh`, `_clear_logs`, `_ts`
    *   `MainDashboard`: `_build_permissions`, `_create_ui`, `_create_header`, `_create_camera_section`, `_create_control_buttons`, `_create_sensor_section`, `_create_zone_section`, `_create_quick_actions`, `_update_loop`, `_update_cameras`, `_update_sensors`, `_update_zones`, `_update_header`, `_prompt_camera_password`, `_set_mode`, `_pan_camera`, `_tilt_camera`, `_zoom_camera`, `_toggle_camera`, `_set_camera_password`, `_delete_camera_password`, `_open_zone_manager`, `_open_log_viewer`, `_trigger_panic`, `_silence_alarm`, `_open_settings`, `_reset_system`, `_save_settings`, `_open_sensor_simulator`, `_logout`, `_on_close`, `add_row`
    *   `ZoneManagerWindow`: `_on_close`, `_center_window`, `_create_ui`, `_refresh_zones`, `_on_zone_select`, `_refresh_zone_sensors`, `_add_zone`, `_edit_zone`, `_delete_zone`, `_assign_sensors`
    *   `AddZoneDialog`: `_create_ui`, `_create_zone`
    *   `EditZoneDialog`: `_create_ui`, `_save_zone`
    *   `AssignSensorDialog`: `_create_ui`, `_assign`

### 2.4. Configuration and Data Management
*   **Classes:** `ConfigurationManager`, `SystemSettings`, `SafeHomeMode`, `SafetyZone`, `StorageManager`, `Log`, `LogManager`, `DatabaseManager`, `EventLog`, `LoginSession`
*   **Methods:**
    *   `ConfigurationManager`: `register_zone_update_callback`, `_notify_zone_update`, `send_email_alert`, `_load_safehome_modes`, `save_configuration`, `reset_configuration`, `set_mode`, `get_mode`, `get_safehome_modes`, `get_sensors_for_mode`, `configure_mode_sensors`, `get_safety_zone`, `get_all_safety_zones`, `add_safety_zone`, `update_safety_zone`, `delete_safety_zone`, `get_all_zones`, `shutdown`
    *   `SystemSettings`: `update_settings`, `to_dict`, `from_db_row`
    *   `SafeHomeMode`: `get_db_mode_name`, `from_db_mode_name`, `from_db_row`
    *   `SafetyZone`: `add_sensor`, `remove_sensor`, `get_sensors`, `arm`, `disarm`, `to_dict`, `from_db_row`
    *   `StorageManager`: `_check_db`, `save_settings_to_json`, `load_settings_from_json`, `save_settings`, `load_settings`, `save_settings_to_db`, `load_settings_from_db`, `save_safety_zone`, `load_all_safety_zones`, `load_safety_zone_by_id`, `delete_safety_zone`, `delete_all_safety_zones`, `save_sensor`, `load_all_sensors`, `delete_sensor`, `save_camera`, `load_all_cameras`, `delete_camera`, `update_camera_password`, `clear_camera_passwords`, `save_log`, `get_logs`, `get_unseen_logs`, `mark_logs_seen`, `clear_logs`, `get_sensors_for_mode`, `save_mode_sensor_mapping`
    *   `Log`: `event_type`
    *   `LogManager`: `add_log`, `_write_to_file`, `get_recent_logs`, `get_all_logs`, `clear_logs`
    *   `DatabaseManager`: `_ensure_db_directory`, `connect`, `disconnect`, `initialize_schema`, `execute_query`, `execute_insert_query`, `execute_many`, `commit`, `rollback`, `get_last_insert_id`, `get_system_settings`, `update_system_settings`, `get_safety_zones`, `get_safehome_modes`, `get_sensors`, `get_cameras`, `add_event_log`, `get_event_logs`, `clear_event_logs`
    *   `EventLog`: `from_db_row`
    *   `LoginSession`: `from_db_row`


## 3. Unit Test Results

### 3.1. External Communication Management

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `System` |
| **Method**                   | `call_monitoring_service` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `System` |
| **Method**                   | `_send_password_change_alert` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `ConfigurationManager` |
| **Method**                   | `send_email_alert` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

### 3.2. Surveillance

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `CameraAccessGuard` |
| **Method**                   | `require_access` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `CameraAccessGuard` |
| **Method**                   | `_warn` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `CameraController` |
| **Method**                   | `add_camera` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `CameraController` |
| **Method**                   | `remove_camera` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `CameraController` |
| **Method**                   | `get_camera` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `CameraController` |
| **Method**                   | `get_all_cameras` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `CameraController` |
| **Method**                   | `get_camera_view` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `CameraController` |
| **Method**                   | `pan_camera` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `CameraController` |
| **Method**                   | `tilt_camera` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `CameraController` |
| **Method**                   | `zoom_camera` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `CameraController` |
| **Method**                   | `enable_camera` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `CameraController` |
| **Method**                   | `disable_camera` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `CameraController` |
| **Method**                   | `set_camera_password` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `CameraController` |
| **Method**                   | `delete_camera_password` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `CameraController` |
| **Method**                   | `_get_camera_with_access` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `CameraController` |
| **Method**                   | `get_camera_status` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `CameraController` |
| **Method**                   | `get_all_camera_statuses` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `CameraController` |
| **Method**                   | `load_cameras_from_storage` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `CameraController` |
| **Method**                   | `shutdown` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceCamera` |
| **Method**                   | `set_id` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceCamera` |
| **Method**                   | `get_id` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceCamera` |
| **Method**                   | `get_view` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceCamera` |
| **Method**                   | `pan_right` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceCamera` |
| **Method**                   | `pan_left` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceCamera` |
| **Method**                   | `tilt_up` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceCamera` |
| **Method**                   | `tilt_down` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceCamera` |
| **Method**                   | `zoom_in` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceCamera` |
| **Method**                   | `zoom_out` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceCamera` |
| **Method**                   | `_tick` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceCamera` |
| **Method**                   | `run` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceCamera` |
| **Method**                   | `stop` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `InterfaceCamera` |
| **Method**                   | `set_id` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `InterfaceCamera` |
| **Method**                   | `get_id` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `InterfaceCamera` |
| **Method**                   | `get_view` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `InterfaceCamera` |
| **Method**                   | `pan_right` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `InterfaceCamera` |
| **Method**                   | `pan_left` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `InterfaceCamera` |
| **Method**                   | `zoom_in` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `InterfaceCamera` |
| **Method**                   | `zoom_out` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeCamera` |
| **Method**                   | `get_id` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeCamera` |
| **Method**                   | `get_name` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeCamera` |
| **Method**                   | `get_location` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeCamera` |
| **Method**                   | `get_view` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeCamera` |
| **Method**                   | `pan_left` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeCamera` |
| **Method**                   | `pan_right` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeCamera` |
| **Method**                   | `tilt_up` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeCamera` |
| **Method**                   | `tilt_down` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeCamera` |
| **Method**                   | `zoom_in` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeCamera` |
| **Method**                   | `zoom_out` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeCamera` |
| **Method**                   | `enable` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeCamera` |
| **Method**                   | `disable` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeCamera` |
| **Method**                   | `set_password` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeCamera` |
| **Method**                   | `verify_password` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeCamera` |
| **Method**                   | `has_password` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeCamera` |
| **Method**                   | `is_locked` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeCamera` |
| **Method**                   | `_is_locked` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeCamera` |
| **Method**                   | `get_status` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeCamera` |
| **Method**                   | `stop` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `Camera` |
| **Method**                   | `from_db_row` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceMotionDetector` |
| **Method**                   | `intrude` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceMotionDetector` |
| **Method**                   | `release` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceMotionDetector` |
| **Method**                   | `get_id` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceMotionDetector` |
| **Method**                   | `read` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceMotionDetector` |
| **Method**                   | `arm` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceMotionDetector` |
| **Method**                   | `disarm` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceMotionDetector` |
| **Method**                   | `test_armed_state` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceSensorTester` |
| **Method**                   | `intrude` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceSensorTester` |
| **Method**                   | `release` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceSensorTester` |
| **Method**                   | `showSensorTester` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceWinDoorSensor` |
| **Method**                   | `intrude` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceWinDoorSensor` |
| **Method**                   | `release` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceWinDoorSensor` |
| **Method**                   | `get_id` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceWinDoorSensor` |
| **Method**                   | `read` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceWinDoorSensor` |
| **Method**                   | `arm` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceWinDoorSensor` |
| **Method**                   | `disarm` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceWinDoorSensor` |
| **Method**                   | `test_armed_state` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `InterfaceSensor` |
| **Method**                   | `get_id` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `InterfaceSensor` |
| **Method**                   | `read` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `InterfaceSensor` |
| **Method**                   | `arm` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `InterfaceSensor` |
| **Method**                   | `disarm` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `InterfaceSensor` |
| **Method**                   | `test_armed_state` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `MotionSensor` |
| **Method**                   | `read` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `MotionSensor` |
| **Method**                   | `arm` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `MotionSensor` |
| **Method**                   | `disarm` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `MotionSensor` |
| **Method**                   | `test_armed_state` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `MotionSensor` |
| **Method**                   | `is_motion_detected` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `MotionSensor` |
| **Method**                   | `simulate_motion` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `MotionSensor` |
| **Method**                   | `simulate_clear` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `Sensor` |
| **Method**                   | `read` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `Sensor` |
| **Method**                   | `arm` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `Sensor` |
| **Method**                   | `disarm` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `Sensor` |
| **Method**                   | `test_armed_state` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `Sensor` |
| **Method**                   | `get_id` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `Sensor` |
| **Method**                   | `get_type` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `Sensor` |
| **Method**                   | `get_location` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `Sensor` |
| **Method**                   | `get_zone_id` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `Sensor` |
| **Method**                   | `set_zone_id` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `Sensor` |
| **Method**                   | `get_status` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `Sensor` |
| **Method**                   | `from_db_row` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SensorController` |
| **Method**                   | `add_sensor` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SensorController` |
| **Method**                   | `remove_sensor` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SensorController` |
| **Method**                   | `get_sensor` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SensorController` |
| **Method**                   | `get_all_sensors` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SensorController` |
| **Method**                   | `get_sensors_by_zone` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SensorController` |
| **Method**                   | `get_sensors_by_type` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SensorController` |
| **Method**                   | `arm_sensor` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SensorController` |
| **Method**                   | `disarm_sensor` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SensorController` |
| **Method**                   | `arm_sensors_in_zone` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SensorController` |
| **Method**                   | `disarm_sensors_in_zone` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SensorController` |
| **Method**                   | `arm_sensors` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SensorController` |
| **Method**                   | `disarm_all_sensors` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SensorController` |
| **Method**                   | `poll_sensors` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SensorController` |
| **Method**                   | `check_all_windoor_closed` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SensorController` |
| **Method**                   | `get_sensor_status` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SensorController` |
| **Method**                   | `get_all_sensor_statuses` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SensorController` |
| **Method**                   | `load_sensors_from_storage` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `WindowDoorSensor` |
| **Method**                   | `read` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `WindowDoorSensor` |
| **Method**                   | `arm` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `WindowDoorSensor` |
| **Method**                   | `disarm` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `WindowDoorSensor` |
| **Method**                   | `test_armed_state` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `WindowDoorSensor` |
| **Method**                   | `is_open` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `WindowDoorSensor` |
| **Method**                   | `simulate_open` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `WindowDoorSensor` |
| **Method**                   | `simulate_close` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_create_ui` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_create_floorplan_section` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_create_sensor_list` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_create_right_panel` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_create_control_panels` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_update_id_ranges` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_update_status` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_collect_windoor_map` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_collect_motion_map` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_build_window_rows` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_build_door_rows` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_build_motion_rows` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_get_sensor_states` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_handle_windoor_sensor` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_handle_windoor` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_handle_motion_sensor` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_handle_motion` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_arm_all` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_disarm_all` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_reset_all` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_on_mousewheel` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeSensorTest` |
| **Method**                   | `_bind_mousewheel_recursively` |
| **Author**                   |             |
| **Date**                     |             |
| **Version**                  |             |
| **Test Case Description**    |             |
| **Input Specifications**     |             |
| **Expected Result**          |             |
| **Actual Result** (Pass/Fail/Exception) |             |
| **Comment (including references)** |             |

### 3.3. Security

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `_update_display_text` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Verify display text updates correctly. |
| **Input Specifications**     | `text="Test Message"` |
| **Expected Result**          | Display shows "Test Message" |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `set_security_zone_number` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Verify security zone number is set. |
| **Input Specifications**     | `number=1` |
| **Expected Result**          | Internal zone number variable set to 1 |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `set_display_away` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Verify away mode display is activated. |
| **Input Specifications**     | N/A |
| **Expected Result**          | Display shows "Away" or similar indicator |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `set_display_stay` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Verify stay mode display is activated. |
| **Input Specifications**     | N/A |
| **Expected Result**          | Display shows "Stay" or similar indicator |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `set_display_not_ready` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Verify not ready display is activated. |
| **Input Specifications**     | N/A |
| **Expected Result**          | Display shows "Not Ready" or similar indicator |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `set_display_short_message1` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Verify short message 1 is displayed. |
| **Input Specifications**     | `message="Msg1"` |
| **Expected Result**          | Display shows "Msg1" |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `set_display_short_message2` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Verify short message 2 is displayed. |
| **Input Specifications**     | `message="Msg2"` |
| **Expected Result**          | Display shows "Msg2" |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `set_armed_led` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Verify armed LED state can be controlled. |
| **Input Specifications**     | `state=True` |
| **Expected Result**          | Armed LED is on |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `set_powered_led` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Verify powered LED state can be controlled. |
| **Input Specifications**     | `state=False` |
| **Expected Result**          | Powered LED is off |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `button1` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate button press 1. |
| **Input Specifications**     | N/A |
| **Expected Result**          | Internal handler for button 1 is called |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | This method is abstract and triggers a callback, expected to be implemented by concrete classes. |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `button2` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate button press 2. |
| **Input Specifications**     | N/A |
| **Expected Result**          | Internal handler for button 2 is called |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `button3` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate button press 3. |
| **Input Specifications**     | N/A |
| **Expected Result**          | Internal handler for button 3 is called |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `button4` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate button press 4. |
| **Input Specifications**     | N/A |
| **Expected Result**          | Internal handler for button 4 is called |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `button5` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate button press 5. |
| **Input Specifications**     | N/A |
| **Expected Result**          | Internal handler for button 5 is called |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `button6` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate button press 6. |
| **Input Specifications**     | N/A |
| **Expected Result**          | Internal handler for button 6 is called |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `button7` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate button press 7. |
| **Input Specifications**     | N/A |
| **Expected Result**          | Internal handler for button 7 is called |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `button8` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate button press 8. |
| **Input Specifications**     | N/A |
| **Expected Result**          | Internal handler for button 8 is called |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `button9` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate button press 9. |
| **Input Specifications**     | N/A |
| **Expected Result**          | Internal handler for button 9 is called |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `button_star` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate star button press. |
| **Input Specifications**     | N/A |
| **Expected Result**          | Internal handler for star button is called |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `button0` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate button press 0. |
| **Input Specifications**     | N/A |
| **Expected Result**          | Internal handler for button 0 is called |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `DeviceControlPanelAbstract` |
| **Method**                   | `button_sharp` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate sharp button press. |
| **Input Specifications**     | N/A |
| **Expected Result**          | Internal handler for sharp button is called |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeControlPanel` |
| **Method**                   | `_refresh_status_display` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Verify display is updated with current system status. |
| **Input Specifications**     | N/A |
| **Expected Result**          | Display reflects current system armed state and mode. |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeControlPanel` |
| **Method**                   | `_reset_interaction` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Verify input buffer and state are reset. |
| **Input Specifications**     | N/A |
| **Expected Result**          | Input buffer cleared, state returned to default. |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeControlPanel` |
| **Method**                   | `_handle_key_input` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Verify key input is processed correctly. |
| **Input Specifications**     | `key='1'` |
| **Expected Result**          | Key added to input buffer. |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeControlPanel` |
| **Method**                   | `_handle_command` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Verify commands are executed based on input. |
| **Input Specifications**     | `input_code="1234"` |
| **Expected Result**          | Appropriate system command is triggered. |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | Depends on the command mapping. |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeControlPanel` |
| **Method**                   | `_attempt_login` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Verify login attempt with valid credentials. |
| **Input Specifications**     | `username="admin", password="password"` |
| **Expected Result**          | Login successful, system unlocked. |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | Relies on `LoginManager`. |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeControlPanel` |
| **Method**                   | `_attempt_change_password` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Verify password change with old and new passwords. |
| **Input Specifications**     | `old_pass="old", new_pass="new"` |
| **Expected Result**          | Password changed successfully. |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | Relies on `LoginManager`. |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeControlPanel` |
| **Method**                   | `button1` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate button press 1, extending abstract method. |
| **Input Specifications**     | N/A |
| **Expected Result**          | `_handle_key_input('1')` called. |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | Calls internal handler. |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeControlPanel` |
| **Method**                   | `button2` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate button press 2, extending abstract method. |
| **Input Specifications**     | N/A |
| **Expected Result**          | `_handle_key_input('2')` called. |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeControlPanel` |
| **Method**                   | `button3` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate button press 3, extending abstract method. |
| **Input Specifications**     | N/A |
| **Expected Result**          | `_handle_key_input('3')` called. |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeControlPanel` |
| **Method**                   | `button4` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate button press 4, extending abstract method. |
| **Input Specifications**     | N/A |
| **Expected Result**          | `_handle_key_input('4')` called. |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeControlPanel` |
| **Method**                   | `button5` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate button press 5, extending abstract method. |
| **Input Specifications**     | N/A | 
| **Expected Result**          | `_handle_key_input('5')` called. |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeControlPanel` |
| **Method**                   | `button6` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate button press 6, extending abstract method. |
| **Input Specifications**     | N/A |
| **Expected Result**          | `_handle_key_input('6')` called. |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeControlPanel` |
| **Method**                   | `button7` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate button press 7, extending abstract method. |
| **Input Specifications**     | N/A |
| **Expected Result**          | `_handle_key_input('7')` called. |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeControlPanel` |
| **Method**                   | `button8` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate button press 8, extending abstract method. |
| **Input Specifications**     | N/A |
| **Expected Result**          | `_handle_key_input('8')` called. |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeControlPanel` |
| **Method**                   | `button9` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate button press 9, extending abstract method. |
| **Input Specifications**     | N/A |
| **Expected Result**          | `_handle_key_input('9')` called. |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeControlPanel` |
| **Method**                   | `button0` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate button press 0, extending abstract method. |
| **Input Specifications**     | N/A |
| **Expected Result**          | `_handle_key_input('0')` called. |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeControlPanel` |
| **Method**                   | `button_star` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate star button press, extending abstract method. |
| **Input Specifications**     | N/A |
| **Expected Result**          | `_handle_key_input('*')` called. |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeControlPanel` |
| **Method**                   | `button_sharp` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Simulate sharp button press, extending abstract method. |
| **Input Specifications**     | N/A |
| **Expected Result**          | `_handle_key_input('#')` called. |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | N/A |

| Field                         | Description |
|------------------------------|-------------|
| **Class**                    | `SafeHomeControlPanel` |
| **Method**                   | `button_panic` |
| **Author**                   | Gemini |
| **Date**                     | 2025-11-29 |
| **Version**                  | 1.0 |
| **Test Case Description**    | Trigger panic alarm. |
| **Input Specifications**     | N/A |
| **Expected Result**          | System alarm triggered. |
| **Actual Result** (Pass/Fail/Exception) | Pass |
| **Comment (including references)** | Relies on `System` to trigger the alarm. |

### 3.4. Configuration and Data Management
*No unit tests in this category.*
