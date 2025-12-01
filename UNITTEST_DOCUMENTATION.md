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
*   **Classes:** `System`, `LoginInterface`, `LoginManager`, `Alarm`, `DeviceControlPanelAbstract`, `SafeHomeControlPanel`, `CameraMonitor`, `LoginWindow`, `LogViewerWindow`, `MainDashboard`, `ZoneManagerWindow`, `AddZoneDialog`, `EditZoneDialog`, `AssignSensorDialog`
*   **Methods:**
    *   `System`: `turn_on`, `turn_off`, `reset`, `shutdown`, `_start_sensor_polling`, `_stop_sensor_polling`, `_sensor_polling_loop`, `_handle_intrusion`, `_start_entry_delay_countdown`, `_trigger_alarm`, `call_monitoring_service`, `arm_system`, `disarm_system`, `arm_zone`, `disarm_zone`, `login`, `change_password`, `_send_password_change_alert`, `_get_sensors_for_mode`, `get_system_status`, `countdown`
    *   `LoginInterface`: `validate_credentials`, `change_password`
    *   `LoginManager`: `validate_credentials`, `_validate_control_panel`, `_lock_interface`, `_log_session`, `change_password`, `change_guest_password`, `unlock_system`, `is_interface_locked`, `get_failed_attempts`, `unlock_after_delay`
    *   `Alarm`: `ring`, `_ring_for_duration`, `stop`, `is_active`, `set_duration`, `get_duration`, `get_status`
    *   `DeviceControlPanelAbstract`: `_update_display_text`, `set_security_zone_number`, `set_display_away`, `set_display_stay`, `set_display_not_ready`, `set_display_short_message1`, `set_display_short_message2`, `set_armed_led`, `set_powered_led`, `button1`, `button2`, `button3`, `button4`, `button5`, `button6`, `button7`, `button8`, `button9`, `button_star`, `button0`, `button_sharp`
    *   `SafeHomeControlPanel`: `_refresh_status_display`, `_reset_interaction`, `_handle_key_input`, `_handle_command`, `_attempt_login`, `_attempt_change_password`, `button1`, `button2`, `button3`, `button4`, `button5`, `button6`, `button7`, `button8`, `button9`, `button0`, `button_star`, `button_sharp`, `button_panic`
    *   `CameraMonitor`: `__init__`, `_update_feed`, `_pan_left`, `_pan_right`, `_zoom_in`, `_zoom_out`, `_on_close`
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
|-------------------------------|-------------|
| **Class**                     | `System` |
| **Method**                    | `call_monitoring_service` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that when `call_monitoring_service` is executed, it creates an appropriate log entry. |
| **Input Specifications**      | `call_monitoring_service` is called with a mock sensor object. |
| **Expected Result**           | A log message containing "Calling monitoring service" should be present in the recent logs. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_core.py::test_call_monitoring_service_logs` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `ConfigurationManager` |
| **Method**                    | `send_email_alert` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies the `send_email_alert` functionality, covering both success (an email address is configured) and failure (the email address is blank) scenarios. It uses a mock SMTP server. |
| **Input Specifications**      | `send_email_alert` is called once with `settings.alert_email` set, and once with it empty. |
| **Expected Result**           | The first call should succeed and a message should be "sent" by the dummy SMTP server. The second call should fail and return `False`. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_configuration.py::test_configuration_manager_send_email_alert` |

### 3.2. Surveillance

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `CameraAccessGuard` |
| **Method**                    | `require_access` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that the `CameraAccessGuard` denies access to a camera when the camera is locked due to too many failed password attempts. It also checks that a log message is generated. |
| **Input Specifications**      | An instance of `CameraAccessGuard`, a `SafeHomeCamera` with a password, `max_attempts=1`, and `lockout_seconds=1`. A wrong password ("bad") is provided. |
| **Expected Result**           | `require_access` should return `None` (access denied), a log message should be appended, the camera should become locked, and even with the correct password, access should be denied while locked. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_camera_guard.py::test_camera_access_guard_denies_when_locked` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `CameraController` |
| **Method**                    | `_get_camera_with_access` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that the internal helper method `_get_camera_with_access` in `CameraController` correctly grants or denies access based on the provided password. |
| **Input Specifications**      | A `CameraController` with a camera that has a password ("1234"). The helper is called once with an incorrect password ("0000") and once with the correct password. |
| **Expected Result**           | The call with the incorrect password should return `None`. The call with the correct password should return the camera object. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_camera_guard.py::test_camera_controller_get_camera_with_access` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `SafeHomeCamera` |
| **Method**                    | `is_locked`, `verify_password`, `get_status` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that a `SafeHomeCamera` enters a locked state after a failed password attempt and that the lockout is released after the specified `lockout_seconds`. It also confirms that `get_status()` reflects the correct camera name. |
| **Input Specifications**      | A `SafeHomeCamera` with `max_attempts=1` and `lockout_seconds=0.1`. `verify_password` is called with a wrong password, then `time.sleep` is called for longer than the lockout, then it's called with the correct password. |
| **Expected Result**           | The camera should be locked after the first bad attempt. After the timeout, `verify_password` with the correct password should succeed. The dictionary from `get_status()` should contain the camera's name. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_camera_guard.py::test_safehome_camera_lock_and_status` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `CameraController` |
| **Method**                    | `remove_camera`, `get_all_camera_statuses` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests the `remove_camera` functionality and verifies that `get_all_camera_statuses` returns the correct number of cameras before and after removal. |
| **Input Specifications**      | A `CameraController` with two cameras added. One camera is then removed. |
| **Expected Result**           | `get_all_camera_statuses` should initially return 2 statuses. After removing one camera, `get_camera` for the removed ID should return `None`, and `get_all_cameras` should return a list with 1 camera. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_camera_guard.py::test_camera_controller_remove_and_statuses` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `SafeHomeCamera` |
| **Method**                    | `verify_password`, `is_locked` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies the password protection and lockout mechanism on a `SafeHomeCamera`. It checks that failed attempts lead to a lockout and that access is restored after the lockout period expires. |
| **Input Specifications**      | A camera with `max_attempts=2` and `lockout_seconds=1` is created. `verify_password` is called twice with a wrong password, then the test waits for the lockout to expire. |
| **Expected Result**           | The camera should be locked after the second failed attempt. After the timeout, a call to `verify_password` with the correct password should succeed. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_surveillance.py::test_safehome_camera_password_and_lockout` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `SafeHomeCamera` |
| **Method**                    | `pan_left`, `pan_right`, `tilt_up`, `tilt_down`, `zoom_in`, `zoom_out`, `get_status` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests the Pan/Tilt/Zoom (PTZ) controls of the `SafeHomeCamera`, ensuring they respect their movement boundaries. Also verifies the `get_status` method. |
| **Input Specifications**      | PTZ and zoom methods are called repeatedly to hit their upper and lower limits. |
| **Expected Result**           | The PTZ methods should return `True` within bounds. The zoom methods should eventually return `False` when they hit their limits. `get_status` should return a dictionary with correct camera info. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_surveillance.py::test_safehome_camera_controls_and_status` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `CameraController` |
| **Method**                    | `get_camera_view`, `set_camera_password`, `delete_camera_password` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that the `CameraController` correctly enforces password checks for viewing a camera feed. It also tests the password lifecycle: setting, changing (via `set_camera_password`), and deleting a password. |
| **Input Specifications**      | A camera with a password is created. `get_camera_view` is called with wrong and correct passwords. The password is then set and deleted. |
| **Expected Result**           | `get_camera_view` should fail with a wrong password and succeed with the correct one, returning an image. Setting and deleting the password should also succeed. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_surveillance.py::test_camera_controller_access_and_password` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `CameraController`, `CameraAccessGuard` |
| **Method**                    | `pan_camera`, `tilt_camera`, `zoom_camera`, `enable_camera`, `set_camera_password`, `delete_camera_password` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | A comprehensive test for various access-denied scenarios, such as using invalid PTZ directions, insufficient role permissions (guest trying to enable), password mismatches, and attempting to access a non-existent camera. |
| **Input Specifications**      | Various methods of `CameraController` are called with invalid parameters (bad directions, wrong passwords, 'guest' role). |
| **Expected Result**           | All the tested calls should fail, returning `False` or `None` as appropriate, without raising exceptions. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_surveillance.py::test_camera_controller_access_denied_branches` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `CameraController`, `CameraAccessGuard` |
| **Method**                    | `get_camera_view`, `require_access` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that a camera lockout (triggered by a failed `get_camera_view` attempt) is correctly enforced by the `CameraAccessGuard`, preventing further access even with the correct password. |
| **Input Specifications**      | `get_camera_view` is called with a wrong password to lock the camera. Then, the internal `require_access` method is called with the correct password while the camera is locked. |
| **Expected Result**           | The `require_access` call should return `None` (access denied) because the camera is locked. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_surveillance.py::test_camera_controller_lockout_and_require_access` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `CameraController` |
| **Method**                    | `pan_camera`, `tilt_camera`, `zoom_camera`, `get_all_camera_statuses` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | This test ensures that the PTZ boundary logic works correctly when called from the controller level and that `get_all_camera_statuses` functions correctly. |
| **Input Specifications**      | PTZ methods are called repeatedly on a camera via the controller. |
| **Expected Result**           | The calls should not raise errors, and `get_all_camera_statuses` should successfully return a list of statuses. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_surveillance.py::test_camera_controller_boundaries_and_status` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `InterfaceCamera` |
| **Method**                    | All abstract methods |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Demonstrates that the `InterfaceCamera` abstract base class can be successfully subclassed and that all its abstract methods can be implemented. |
| **Input Specifications**      | A minimal concrete implementation of `InterfaceCamera` is created and its methods are called. |
| **Expected Result**           | The object can be instantiated and all its methods can be called without error. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_surveillance.py::test_interface_camera_concrete` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `SafeHomeCamera` |
| **Method**                    | `get_id`, `get_name`, `get_location`, `has_password`, `verify_password`, `is_locked` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | A general test for various getter methods on `SafeHomeCamera` and its lock state handling. |
| **Input Specifications**      | A camera is created, its getters are called, a password is set, and failed verifications are performed. |
| **Expected Result**           | Getters should return correct values. `has_password` should be `True` after setting a password. `is_locked` should be `True` after failed attempts. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_surveillance.py::test_safehome_camera_getters_and_lock_state` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `DeviceCamera` |
| **Method**                    | `get_view` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that the hardware-level `DeviceCamera` simulation returns an actual image object when the required image asset is available. |
| **Input Specifications**      | `get_view` is called on a `DeviceCamera`. |
| **Expected Result**           | The method should return a non-`None` value (an image object). |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_surveillance.py::test_device_camera_view_with_real_image` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `DeviceCamera` |
| **Method**                    | Constructor (`__init__`) |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests the error handling of `DeviceCamera` when its underlying image asset is missing. It should show an error message (mocked) but not crash. |
| **Input Specifications**      | A `DeviceCamera` is initialized with an ID (999) that doesn't correspond to an available image file. A `tkinter.messagebox` function is monkeypatched to capture the error. |
| **Expected Result**           | The mocked `showerror` function should be called with a "file open error" message. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_surveillance.py::test_device_camera_missing_file` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `DeviceCamera` |
| **Method**                    | `get_view` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests a specific edge case within the `get_view` method, where extreme pan/zoom values on a small source image could cause the image cropping logic to fail. The test ensures this is handled gracefully. |
| **Input Specifications**      | A `DeviceCamera`'s source image is replaced with a very small one, and pan/zoom values are set to extreme numbers to force an error in the cropping calculation. |
| **Expected Result**           | The `get_view` method should still return a valid (though maybe blank) image object and not raise an unhandled exception. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_surveillance.py::test_device_camera_crop_failure` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `DeviceSensorTester` |
| **Method**                    | `showSensorTester` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Confirms the `showSensorTester` function does nothing when in a headless environment. |
| **Input Specifications**      | `SAFEHOME_HEADLESS` is set. `showSensorTester` is called. |
| **Expected Result**           | `DeviceSensorTester.safeHomeSensorTest` should remain `None`. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_interfaces_and_devices.py::test_device_sensor_tester_headless_skip` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `WindowDoorSensor`, `MotionSensor` |
| **Method**                    | Various accessors (`get_id`, `get_type`, etc.), `test_armed_state`, `simulate_motion`, `simulate_clear`. |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | This test verifies the correct functioning of accessor methods (getters/setters) and state simulation methods for the concrete `WindowDoorSensor` and `MotionSensor` classes. |
| **Input Specifications**      | `WindowDoorSensor` and `MotionSensor` objects are created. Accessor methods are called. The motion sensor is armed and its state is changed via simulation methods. |
| **Expected Result**           | All accessors should return the correct initial or updated values. The `is_motion_detected` flag should correctly reflect the state after simulation calls. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_interfaces_and_devices.py::test_motion_and_windoor_test_armed_state_and_accessors` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `DeviceMotionDetector`, `DeviceWinDoorSensor` |
| **Method**                    | `arm`, `disarm`, `intrude`, `release`, `read`, `test_armed_state`. |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | This test checks the basic functionality of the simulated hardware-level device classes (`DeviceMotionDetector`, `DeviceWinDoorSensor`). It ensures they correctly manage their armed/disarmed state and their triggered (`intrude`)/cleared (`release`) status. |
| **Input Specifications**      | `DeviceMotionDetector` and `DeviceWinDoorSensor` objects are armed, intruded, released, and disarmed. |
| **Expected Result**           | The `read()` method should return `True` only when the device is armed and in an intruded state. `test_armed_state()` should reflect the calls to `arm()` and `disarm()`. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_interfaces_and_devices.py::test_device_motion_detector_and_windoor_hardware` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `DeviceCamera` |
| **Method**                    | `_tick` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that the internal `_tick` method of the `DeviceCamera` correctly increments its internal time counter. It also ensures that any GUI-related errors that might occur are handled. |
| **Input Specifications**      | A `DeviceCamera` is instantiated and `_tick()` is called. `tkinter.messagebox.showerror` is monkeypatched to prevent a GUI popup. |
| **Expected Result**           | The camera's internal `time` attribute should be incremented to 1. No unhandled exceptions should occur. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_interfaces_and_devices.py::test_device_camera_tick_and_id` |

### 3.3. Security

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `System` |
| **Method**                    | `turn_on`, `turn_off` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that the `turn_on` and `turn_off` methods correctly toggle the system's running state (`is_running` flag). |
| **Input Specifications**      | A `System` instance is turned on and then off. |
| **Expected Result**           | The `is_running` attribute should be `True` after `turn_on` and `False` after `turn_off`. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_core.py::test_system_turn_on_off` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `System` |
| **Method**                    | `get_system_status` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Checks if the `get_system_status` method returns a dictionary that accurately reflects the current state of the system, such as its running status and the number of sensors. |
| **Input Specifications**      | `get_system_status` is called on an idle `System` instance. |
| **Expected Result**           | The returned dictionary should show `is_running` as `False` and contain the correct number of sensors. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_core.py::test_system_status_snapshot` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `Alarm` |
| **Method**                    | `ring`, `stop` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that the `Alarm` object correctly becomes active when `ring()` is called and inactive again after its specified duration has passed. |
| **Input Specifications**      | An `Alarm` with a duration of 0.1 seconds is created. `ring()` is called. The test waits for 0.2 seconds. |
| **Expected Result**           | The alarm should be active immediately after `ring()` and inactive after the duration has elapsed. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_core.py::test_alarm_ring_and_stop` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `System` |
| **Method**                    | `_start_sensor_polling`, `_stop_sensor_polling` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Ensures that the sensor polling thread can be started and stopped safely. It monkeypatches the polling loop to verify that the thread was actually executed. |
| **Input Specifications**      | The `_sensor_polling_loop` is replaced with a simple function that sets a flag. The polling is started and then stopped. |
| **Expected Result**           | The flag set by the fake polling loop should be `True`, indicating the thread ran. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_core.py::test_system_polling_start_stop` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `System` |
| **Method**                    | `_trigger_alarm` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that calling the internal `_trigger_alarm` method activates the system's alarm. |
| **Input Specifications**      | The system is turned on, and `_trigger_alarm` is called with a mock sensor object. |
| **Expected Result**           | The `system.alarm` should become active. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_core.py::test_system_trigger_alarm_and_stop` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `System` |
| **Method**                    | `shutdown` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | A simple test to ensure that calling the `shutdown` method on the `System` object does not raise any exceptions. |
| **Input Specifications**      | `shutdown()` is called on a `System` instance. |
| **Expected Result**           | The method completes without raising any errors. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_core.py::test_system_shutdown_calls_components` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `System` |
| **Method**                    | `_start_entry_delay_countdown` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests the entry delay logic. It verifies that if the system is disarmed (or the sensor is disarmed) during the entry delay countdown, the alarm is *not* triggered. |
| **Input Specifications**      | The entry delay is set to a short interval. A sensor is armed and then triggered, starting the countdown. The sensor is then disarmed before the delay expires. |
| **Expected Result**           | The system alarm should not be active after the delay period has passed. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_core.py::test_start_entry_delay_countdown_no_alarm_when_disarmed` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `System` |
| **Method**                    | `_start_entry_delay_countdown` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests the other path of the entry delay logic. It verifies that if an intrusion is detected and the system remains armed, the alarm is triggered after the entry delay countdown finishes. |
| **Input Specifications**      | The entry delay is set to a short interval. A sensor is armed and triggered, starting the countdown. The system remains armed. |
| **Expected Result**           | The system alarm should be active after the delay period has passed. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_core.py::test_start_entry_delay_countdown_triggers_after_delay` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `SensorController` |
| **Method**                    | `add_sensor`, `poll_sensors`, `remove_sensor` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests the lifecycle of sensors within the `SensorController`: adding them, polling them to detect intrusions, and removing them. |
| **Input Specifications**      | A window and motion sensor are added. They are armed and an intrusion is simulated. `poll_sensors` is called. One sensor is removed. |
| **Expected Result**           | `poll_sensors` should detect both intrusions. `remove_sensor` should succeed, and `get_sensor` for the removed ID should then return `None`. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_security.py::test_sensor_controller_add_poll_remove` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `SensorController` |
| **Method**                    | `check_all_windoor_closed` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies the prerequisite check for arming the system. If a window/door sensor is open, this check should fail and identify the open sensor. |
| **Input Specifications**      | A window sensor is added, armed, and simulated to be open. `check_all_windoor_closed` is called. |
| **Expected Result**           | The method should return `False` and a list containing the open sensor. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_security.py::test_sensor_controller_check_all_windoor_closed` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `WindowDoorSensor`, `MotionSensor` |
| **Method**                    | `read` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Confirms that the `read()` method (which reports an intrusion) on sensors is gated by their armed state. An intrusion should only be reported if the sensor is armed. |
| **Input Specifications**      | Sensors are simulated as open/triggered while disarmed, then armed, then disarmed again. |
| **Expected Result**           | `read()` should only return `True` when the sensor is both armed and in a triggered state. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_security.py::test_window_and_motion_sensor_behaviors` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `LoginManager` |
| **Method**                    | `validate_credentials`, `is_interface_locked`, `unlock_system` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests the user authentication lockout mechanism. It verifies that exceeding the max login attempts locks the interface, and that the interface is unlocked after the configured timeout. |
| **Input Specifications**      | With `max_login_attempts=2`, `validate_credentials` is called twice with a wrong password. The test waits for the lockout duration, then checks the lock status. |
| **Expected Result**           | The interface should be locked after two failed attempts. After the timeout, it should be unlocked, and a correct login should then succeed. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_security.py::test_login_manager_lock_and_unlock` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `LoginManager` |
| **Method**                    | `validate_credentials`, `change_guest_password`, `unlock_system`, `get_failed_attempts` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Covers several other branches in `LoginManager`: successful web login, changing the guest password (both failed and successful attempts), and ensuring failed attempts are reset after an unlock. |
| **Input Specifications**      | Various calls are made to test web login format, guest password changes, and the state of `failed_attempts` after a lockout/unlock cycle. |
| **Expected Result**           | All branches should behave as expected: web login with correct format succeeds, guest password change requires correct master password, and `failed_attempts` resets to 0 after unlock. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_security.py::test_login_manager_more_branches` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `LoginManager` |
| **Method**                    | `validate_credentials` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests two specific failure conditions: attempting to log in on an already locked interface, and attempting to log in on an unrecognized interface type. |
| **Input Specifications**      | The `is_locked` flag is manually set to `True` for one test. An "UNKNOWN" interface type is used for the other. |
| **Expected Result**           | Both calls to `validate_credentials` should return `False`. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_security.py::test_login_manager_locked_and_unknown_interface` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `LoginManager` |
| **Method**                    | `_log_session` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that the private `_log_session` method correctly executes a database query to record the login attempt. |
| **Input Specifications**      | `_log_session` is called. The test uses a mock storage/DB object to capture the executed queries. |
| **Expected Result**           | The mock database object should have at least one query recorded in its list of executed queries. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_security.py::test_login_manager_log_session` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `System` |
| **Method**                    | `arm_system`, `disarm_system`, `_handle_intrusion` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests the main system arming/disarming flow and the intrusion detection logic. It verifies that arming activates sensors and that an intrusion (when the entry delay is zero) triggers the alarm. |
| **Input Specifications**      | The system is armed in "AWAY" mode, activating a sensor. It's then disarmed. Then, with `entry_delay=0`, it's turned on, a sensor is armed and triggered, and `_handle_intrusion` is called. |
| **Expected Result**           | The sensor should be active when the system is armed and inactive when disarmed. The intrusion should cause the system alarm to become active. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_security.py::test_system_arm_disarm_and_alarm` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `System` |
| **Method**                    | `login`, `change_password` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests the high-level login and password change functionality exposed by the main `System` class. |
| **Input Specifications**      | A successful login is performed. The password is then changed. |
| **Expected Result**           | The initial login should succeed. The password change should succeed. A subsequent login with the *new* password should also succeed. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_security.py::test_system_login_and_password_change` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `LoginManager` |
| **Method**                    | `validate_credentials` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests edge cases for authentication: verifies the default guest password ("0000") works if none is set, and that web logins fail if the `user:pass` format is incorrect. |
| **Input Specifications**      | Login is attempted with user "guest" and password "0000". Web login is attempted with a string missing the colon separator. |
| **Expected Result**           | The guest login should succeed. The web logins with bad formats should fail. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_security.py::test_login_manager_guest_and_web_parsing` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `SensorController` |
| **Method**                    | `remove_sensor`, `disarm_sensor`, etc. |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | This is a catch-all test for various edge cases and no-op branches in `SensorController`, such as trying to operate on a non-existent sensor ID or loading a sensor of an "UNKNOWN" type from storage. It ensures these actions don't cause crashes and are logged. |
| **Input Specifications**      | Various methods are called with invalid IDs (e.g., 999). A sensor with type "UNKNOWN" is saved to storage and loaded. |
| **Expected Result**           | The methods should handle invalid inputs gracefully (e.g., returning `False` or doing nothing) without raising exceptions. A log message should be generated when the unknown sensor type is loaded. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_security.py::test_sensor_controller_edge_branches` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `DeviceSensorTester` |
| **Method**                    | `showSensorTester` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that if an instance of the sensor tester window already exists, `showSensorTester` will not create a new one, but will instead just bring the existing one to the front. This prevents duplicate windows. |
| **Input Specifications**      | A dummy window object is placed in `DeviceSensorTester.safeHomeSensorTest`. `showSensorTester` is then called. |
| **Expected Result**           | The `DeviceSensorTester.safeHomeSensorTest` should remain the same dummy window object, indicating no new window was created. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_device_shims.py::test_device_sensor_tester_existing_window` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `DeviceSensorTester` |
| **Method**                    | `showSensorTester` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | This test covers two scenarios for the sensor tester GUI: 1) In a headless environment (no GUI), the function should do nothing and exit early. 2) If creating the GUI fails (e.g., `tkinter` raises an error), the exception should be caught gracefully and the application should not crash. |
| **Input Specifications**      | 1. The `SAFEHOME_HEADLESS` environment variable is set to "1". `showSensorTester` is called.<br>2. The environment variable is removed, but `tkinter.Tk` is monkeypatched to raise a `RuntimeError`. `showSensorTester` is called. |
| **Expected Result**           | In both cases, `DeviceSensorTester.safeHomeSensorTest` should be `None`, and no exceptions should be raised. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_device_shims.py::test_device_sensor_tester_headless_and_exception` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `SafeHomeControlPanel` |
| **Method**                    | `_handle_key_input`, `button_sharp`, `_handle_command` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Simulates a user logging into the physical control panel, which authenticates them, and then issuing a disarm command. This tests the state machine logic for login and command handling. |
| **Input Specifications**      | UI methods of the base class are patched to do nothing. The test simulates key presses for "1234" followed by the "#" button. Then it calls the handler for command "0". |
| **Expected Result**           | After entering the password and pressing '#', the panel's `is_authenticated` flag should be `True`. After handling the disarm command, the flag should become `False`. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_ui_logic.py::test_safehome_control_panel_login_and_arm_disarm` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `SafeHomeControlPanel` |
| **Method**                    | `_handle_key_input`, `button_sharp`, `_handle_command` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests the entire flow for changing the master password via the physical control panel: login, enter password change mode, enter new password, and confirm. |
| **Input Specifications**      | The test simulates a successful login, then entering command "3" (change password), then entering the new password "9999", followed by "#" to confirm. |
| **Expected Result**           | After the sequence, the panel should no longer be authenticated. A subsequent login attempt on the main `System` object with the new password ("9999") should succeed. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_ui_logic.py::test_safehome_control_panel_change_password_flow` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `MainDashboard` |
| **Method**                    | `_logout` |
| **Author**                    | Gemini |
| **Date**                      | 2025-12-01 |
| **Version**                   | 1.0 |
| **Test Case Description**     | `UT-Dashboard-LogoutForce`: Verifies that a forced logout immediately destroys the dashboard window and shows the login window, without a confirmation prompt. |
| **Input Specifications**      | `_logout` is called with `force_logout=True`. |
| **Expected Result**           | The `destroy` and `login_window.deiconify` methods are called once. `messagebox.askyesno` is not called. |
| **Actual Result**             | Pass |
| **Comment (including refs)**  | `test_unit_main_dashboard.py::test_dashboard_logout_force` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `MainDashboard` |
| **Method**                    | `_logout` |
| **Author**                    | Gemini |
| **Date**                      | 2025-12-01 |
| **Version**                   | 1.0 |
| **Test Case Description**     | `UT-Dashboard-LogoutConfirm`: Verifies the user-confirmed logout path. It checks that a confirmation dialog is shown and that the logout proceeds only if the user confirms. |
| **Input Specifications**      | `_logout` is called with `force_logout=False`, and the mocked `messagebox.askyesno` returns `True`. |
| **Expected Result**           | `messagebox.askyesno` is called once. The `destroy` and `login_window.deiconify` methods are also called once. |
| **Actual Result**             | Pass |
| **Comment (including refs)**  | `test_unit_main_dashboard.py::test_dashboard_logout_confirm` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `MainDashboard` |
| **Method**                    | `_logout` |
| **Author**                    | Gemini |
| **Date**                      | 2025-12-01 |
| **Version**                   | 1.0 |
| **Test Case Description**     | `UT-Dashboard-LogoutCancel`: Verifies that the logout process is aborted if the user cancels the confirmation dialog. |
| **Input Specifications**      | `_logout` is called with `force_logout=False`, and the mocked `messagebox.askyesno` returns `False`. |
| **Expected Result**           | `messagebox.askyesno` is called once, but the `destroy` and `login_window.deiconify` methods are not called. |
| **Actual Result**             | Pass |
| **Comment (including refs)**  | `test_unit_main_dashboard.py::test_dashboard_logout_cancel` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `MainDashboard` |
| **Method**                    | `_on_close` |
| **Author**                    | Gemini |
| **Date**                      | 2025-12-01 |
| **Version**                   | 1.0 |
| **Test Case Description**     | `UT-Dashboard-OnClose`: Tests the handler for the window's close button, covering both cases where the user confirms and cancels quitting the application. |
| **Input Specifications**      | `_on_close` is called twice. The first time, `messagebox.askokcancel` returns `True`. The second time, it returns `False`. |
| **Expected Result**           | When confirmed, `system.shutdown` and `login_window.destroy` are called. When canceled, they are not called. |
| **Actual Result**             | Pass |
| **Comment (including refs)**  | `test_unit_main_dashboard.py::test_dashboard_on_close` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `MainDashboard` |
| **Method**                    | Multiple (`_set_mode`, `_trigger_panic`, etc.) |
| **Author**                    | Gemini |
| **Date**                      | 2025-12-01 |
| **Version**                   | 1.0 |
| **Test Case Description**     | `UT-Dashboard-Permissions`: Verifies that a user with the 'guest' role is blocked from performing privileged actions, and that an appropriate warning message is shown. |
| **Input Specifications**      | A `MainDashboard` is created for a 'guest' user. Various administrative methods are then called. |
| **Expected Result**           | Each action should be blocked, and `messagebox.showwarning` should be called with a specific permission-denied message for each action. |
| **Actual Result**             | Pass |
| **Comment (including refs)**  | `test_unit_main_dashboard.py::test_dashboard_permission_denied_actions` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `MainDashboard` |
| **Method**                    | `_set_mode` |
| **Author**                    | Gemini |
| **Date**                      | 2025-12-01 |
| **Version**                   | 1.0 |
| **Test Case Description**     | `UT-Dashboard-SetMode`: Verifies the system mode setting logic for an admin user, covering disarming, successful arming, and failed arming scenarios. |
| **Input Specifications**      | `_set_mode` is called for `DISARMED`, `AWAY`, and `HOME` modes. The underlying `system.arm_system` is mocked to return `True` and then `False`. |
| **Expected Result**           | The correct system methods (`disarm_system`, `arm_system`) are called, and the correct `showinfo` or `showwarning` message is displayed based on the outcome. |
| **Actual Result**             | Pass |
| **Comment (including refs)**  | `test_unit_main_dashboard.py::test_set_mode_admin` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `MainDashboard` |
| **Method**                    | `_trigger_panic` |
| **Author**                    | Gemini |
| **Date**                      | 2025-12-01 |
| **Version**                   | 1.0 |
| **Test Case Description**     | `UT-Dashboard-Panic`: Verifies the logic for the panic button for an admin user, covering both user confirmation and cancellation. |
| **Input Specifications**      | `_trigger_panic` is called once with the confirmation dialog returning `False`, and once with it returning `True`. |
| **Expected Result**           | If canceled, no action is taken. If confirmed, the system mode is set to `PANIC`, the alarm rings, and a warning is shown. |
| **Actual Result**             | Pass |
| **Comment (including refs)**  | `test_unit_main_dashboard.py::test_trigger_panic_admin` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `MainDashboard` |
| **Method**                    | `_silence_alarm` |
| **Author**                    | Gemini |
| **Date**                      | 2025-12-01 |
| **Version**                   | 1.0 |
| **Test Case Description**     | `UT-Dashboard-Silence`: Verifies the alarm silencing logic for an admin user. |
| **Input Specifications**      | `_silence_alarm` is called. |
| **Expected Result**           | The `system.alarm.stop` method is called, and an `showinfo` message is displayed. |
| **Actual Result**             | Pass |
| **Comment (including refs)**  | `test_unit_main_dashboard.py::test_silence_alarm_admin` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `CameraMonitor` |
| **Method**                    | `__init__` |
| **Author**                    | Gemini |
| **Date**                      | 2025-12-01 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies successful initialization of the `CameraMonitor` window when provided with a valid system and camera ID. |
| **Input Specifications**      | `CameraMonitor` is instantiated with a mock system and a valid camera ID. The camera does not require a password. |
| **Expected Result**           | The camera is fetched from the controller, the GUI setup method is called, and the feed update process is initiated. No errors are shown. |
| **Actual Result**             | Pass |
| **Comment (including refs)**  | `test_unit_camera_monitor.py::test_init_success` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `CameraMonitor` |
| **Method**                    | `__init__` |
| **Author**                    | Gemini |
| **Date**                      | 2025-12-01 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests that `CameraMonitor` initialization fails gracefully with an error message if no system object is provided. |
| **Input Specifications**      | `CameraMonitor` is instantiated with `system=None`. |
| **Expected Result**           | `messagebox.showerror` is called with the message "System not initialized". |
| **Actual Result**             | Pass |
| **Comment (including refs)**  | `test_unit_camera_monitor.py::test_init_no_system` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `CameraMonitor` |
| **Method**                    | `__init__` |
| **Author**                    | Gemini |
| **Date**                      | 2025-12-01 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests that `CameraMonitor` initialization fails gracefully if the requested camera ID is not found in the system. |
| **Input Specifications**      | `CameraMonitor` is instantiated with a camera ID that the mock `camera_controller` will not find. |
| **Expected Result**           | `messagebox.showerror` is called with the message "Camera 1 not found". |
| **Actual Result**             | Pass |
| **Comment (including refs)**  | `test_unit_camera_monitor.py::test_init_camera_not_found` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `CameraMonitor` |
| **Method**                    | `__init__` |
| **Author**                    | Gemini |
| **Date**                      | 2025-12-01 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests that `CameraMonitor` denies access if an incorrect password is provided for a password-protected camera. |
| **Input Specifications**      | A password-protected camera is used, and `CameraMonitor` is instantiated with an incorrect password. |
| **Expected Result**           | `messagebox.showerror` is called with the message "Invalid camera password". |
| **Actual Result**             | Pass |
| **Comment (including refs)**  | `test_unit_camera_monitor.py::test_init_invalid_password` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `CameraMonitor` |
| **Method**                    | `_update_feed` |
| **Author**                    | Gemini |
| **Date**                      | 2025-12-01 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that the camera feed successfully updates by displaying a new image received from the controller. |
| **Input Specifications**      | `_update_feed` is called after mocking `camera_controller.get_camera_view` to return a valid image object. |
| **Expected Result**           | `ImageTk.PhotoImage` is called with the new image, and the image label in the UI is updated. The method schedules itself to run again. |
| **Actual Result**             | Pass |
| **Comment (including refs)**  | `test_unit_camera_monitor.py::test_update_feed_success` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `CameraMonitor` |
| **Method**                    | `_update_feed` |
| **Author**                    | Gemini |
| **Date**                      | 2025-12-01 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that the UI displays a "Camera Unavailable" message if the controller does not return an image for the feed. |
| **Input Specifications**      | `_update_feed` is called after mocking `camera_controller.get_camera_view` to return `None`. |
| **Expected Result**           | The image label in the UI is updated with the text "Camera Unavailable". The method schedules itself to run again. |
| **Actual Result**             | Pass |
| **Comment (including refs)**  | `test_unit_camera_monitor.py::test_update_feed_unavailable` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `CameraMonitor` |
| **Method**                    | `_pan_left`, `_pan_right`, `_zoom_in`, `_zoom_out` |
| **Author**                    | Gemini |
| **Date**                      | 2025-12-01 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests the Pan/Tilt/Zoom (PTZ) control methods, verifying both successful commands and failures (e.g., when a movement limit is reached). |
| **Input Specifications**      | The PTZ methods are called when the underlying mock controller method is set to return `True` (success) and then `False` (failure). |
| **Expected Result**           | The corresponding `camera_controller` methods are called with the correct parameters. On failure, `messagebox.showwarning` is called with an appropriate message. |
| **Actual Result**             | Pass |
| **Comment (including refs)**  | `test_unit_camera_monitor.py::test_ptz_controls` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `CameraMonitor` |
| **Method**                    | `_on_close` |
| **Author**                    | Gemini |
| **Date**                      | 2025-12-01 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that the `_on_close` handler correctly triggers the destruction of the window. |
| **Input Specifications**      | The `destroy` method of the monitor object is replaced with a spy mock, and `_on_close` is called. |
| **Expected Result**           | The spy mock for the `destroy` method is called exactly once. |
| **Actual Result**             | Pass |
| **Comment (including refs)**  | `test_unit_camera_monitor.py::test_on_close` |

### 3.4. Configuration and Data Management

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `ConfigurationManager` |
| **Method**                    | `_notify_zone_update` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that the `ConfigurationManager` can handle exceptions that occur within a registered zone update callback function without crashing. It ensures that an error message is printed to standard output. |
| **Input Specifications**      | A `ConfigurationManager` where a callback function that unconditionally raises a `RuntimeError` is registered. The private method `_notify_zone_update` is then called. |
| **Expected Result**           | The program should not crash, and an error message "Error in zone update callback" should be captured in `stdout`. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_config_errors.py::test_notify_zone_update_handles_exception` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `ConfigurationManager` |
| **Method**                    | `reset_configuration` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that if the `StorageManager` fails to clear camera passwords during a configuration reset, the error is caught and a log entry is created. |
| **Input Specifications**      | The `clear_camera_passwords` method of the `StorageManager` is monkeypatched to always raise a `RuntimeError`. The `reset_configuration` method is then called on the `ConfigurationManager`. |
| **Expected Result**           | A log message containing "Failed to clear camera passwords" should be recorded by the logger. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_config_errors.py::test_reset_configuration_clear_camera_passwords_error` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `SystemSettings` |
| **Method**                    | `update_settings`, `to_dict` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that the `update_settings` method correctly updates the settings object and that `to_dict` returns a dictionary with the updated values. |
| **Input Specifications**      | A `SystemSettings` object is updated with `entry_delay=30` and `monitoring_phone="112"`. |
| **Expected Result**           | The dictionary returned by `to_dict` should contain the correct, updated values. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_configuration.py::test_system_settings_update_and_dict` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `SafeHomeMode` |
| **Method**                    | `get_db_mode_name`, `from_db_mode_name` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies the conversion between the `SafeHomeMode` enum and its corresponding database string representation. |
| **Input Specifications**      | Various `SafeHomeMode` enum members and string names, including an unknown one. |
| **Expected Result**           | The conversion methods should return the correct string/enum values. An unknown string should default to `DISARMED`. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_configuration.py::test_safehome_mode_mapping` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `ConfigurationManager` |
| **Method**                    | `add_safety_zone`, `update_safety_zone`, `delete_safety_zone`, `get_safety_zone` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests the full Create, Read, Update, Delete (CRUD) lifecycle for safety zones managed by the `ConfigurationManager`. |
| **Input Specifications**      | A zone is added, its name is updated, and then it is deleted. |
| **Expected Result**           | `add_safety_zone` should return a new zone. `update_safety_zone` should succeed and the change should be retrievable via `get_safety_zone`. `delete_safety_zone` should succeed and `get_safety_zone` should then return `None`. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_configuration.py::test_configuration_manager_zone_crud` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `ConfigurationManager` |
| **Method**                    | `register_zone_update_callback`, `reset_configuration`, `set_mode`, `get_mode`, `configure_mode_sensors` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests various `ConfigurationManager` features, including callback notification on reset, setting/getting the system mode, and configuring which sensors are active for a given mode. |
| **Input Specifications**      | A callback is registered, `reset_configuration` is called. The mode is set and retrieved. Sensor mapping for "HOME" mode is cleared. |
| **Expected Result**           | The registered callback should be called during reset. `get_mode` should return the value set by `set_mode`. `get_sensors_for_mode` should return an empty list after configuration. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_configuration.py::test_configuration_manager_callbacks_and_modes` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `ConfigurationManager` |
| **Method**                    | `save_configuration` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Ensures that calling `save_configuration` executes without error and creates a log entry. |
| **Input Specifications**      | `save_configuration` is called. |
| **Expected Result**           | The method completes successfully and at least one recent log message is present. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_configuration.py::test_configuration_manager_save_configuration` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `ConfigurationManager` |
| **Method**                    | `load_settings` (via constructor) |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests that when the `ConfigurationManager` is initialized, it correctly loads settings from the `StorageManager` and applies them to its internal `SystemSettings` object. |
| **Input Specifications**      | The `StorageManager.load_settings` method is monkeypatched to return a dictionary with specific settings. A new `ConfigurationManager` is then created. |
| **Expected Result**           | The new `ConfigurationManager` instance should have its `settings` object updated with the values from the mocked `load_settings` return. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_configuration.py::test_configuration_manager_load_settings_branch` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `ConfigurationManager` |
| **Method**                    | `load_all_safety_zones` (via constructor) |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that if no safety zones are found in storage upon initialization, the `ConfigurationManager` creates a default set of zones. |
| **Input Specifications**      | `StorageManager.load_all_safety_zones` is monkeypatched to return an empty list on its first call. A new `ConfigurationManager` is created. |
| **Expected Result**           | The `ConfigurationManager` instance should contain at least two safety zones after initialization. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_configuration.py::test_configuration_manager_no_zones` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `ConfigurationManager` |
| **Method**                    | `reset_configuration` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests the system reset functionality, ensuring it recreates default zones and clears sensitive data like camera passwords from storage. |
| **Input Specifications**      | A camera password is saved to storage, then `reset_configuration` is called. |
| **Expected Result**           | After the reset, the default zones should exist, and all camera passwords in storage should be `None`. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_configuration.py::test_configuration_manager_reset` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `StorageManager` |
| **Method**                    | `save_sensor`, `load_all_sensors`, `save_camera`, `load_all_cameras` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that the `StorageManager` can correctly save and load sensor and camera data to/from the persistent storage. |
| **Input Specifications**      | Two sensors and two cameras (one with a password) are saved. Then all sensors and cameras are loaded. |
| **Expected Result**           | The loaded data should correctly reflect the saved items, including their IDs and the camera password. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_configuration.py::test_storage_manager_sensor_camera_persistence` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `StorageManager` |
| **Method**                    | `save_mode_sensor_mapping`, `get_sensors_for_mode` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that the `StorageManager` can save and retrieve the mapping of which sensors are active for specific system modes. |
| **Input Specifications**      | Sensors are saved, then mappings for "HOME" and "AWAY" modes are saved. |
| **Expected Result**           | `get_sensors_for_mode` should return the correct list of sensor IDs for each mode. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_configuration.py::test_storage_manager_mode_sensor_mapping` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `SafetyZone` |
| **Method**                    | `add_sensor`, `remove_sensor`, `get_sensors`, `arm`, `disarm` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests the behavior of the `SafetyZone` data object itself, ensuring it correctly manages its list of associated sensors and its armed/disarmed state. |
| **Input Specifications**      | A `SafetyZone` is created. Sensors are added and removed. The zone is armed and disarmed. |
| **Expected Result**           | `get_sensors` should reflect the current membership. The `is_armed` property should correctly reflect the state after `arm()` and `disarm()` are called. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_configuration.py::test_safety_zone_object_behaviors` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `LogManager` |
| **Method**                    | `add_log`, `clear_logs`, `get_recent_logs`, `get_all_logs` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies the basic logging functionality. It checks that `add_log` writes to both the log file and the database, and that `clear_logs` successfully empties both. |
| **Input Specifications**      | A log message is added. Then logs are cleared. |
| **Expected Result**           | After adding a log, the log file should exist and contain the message, and `get_recent_logs` should return the log object. After clearing, `get_all_logs` should return an empty list and the log file should be empty. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_log_manager.py::test_log_manager_write_and_clear` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `Log` |
| **Method**                    | `event_type` (property) |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Checks that the `event_type` property of a `Log` object correctly returns its `level`. |
| **Input Specifications**      | A `Log` object is created with `level="INFO"`. |
| **Expected Result**           | The `event_type` property should return "INFO". |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_log_manager.py::test_log_event_type_property` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `LogManager` |
| **Method**                    | Constructor (`__init__`), `add_log` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | This test covers multiple error and edge-case scenarios for `LogManager`, including handling I/O errors, a `None` `StorageManager`, and exceptions during log preloading from storage. |
| **Input Specifications**      | `builtins.open` is monkeypatched to raise an `IOError`. `LogManager` is initialized with various mock `StorageManager` objects that simulate failures or specific data conditions. |
| **Expected Result**           | No unhandled exceptions should occur in any of the scenarios. The `LogManager` should handle the errors gracefully. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_log_manager.py::test_log_manager_error_and_preload` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `LogManager` |
| **Method**                    | `add_log` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that `add_log` can handle a failure in the underlying `StorageManager`'s `save_log` method without crashing. |
| **Input Specifications**      | A mock `StorageManager` is created whose `save_log` method always raises an exception. `add_log` is called on a `LogManager` using this mock storage. |
| **Expected Result**           | The call to `add_log` should complete without raising an unhandled exception. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_log_manager.py::test_log_manager_storage_save_error` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `LogManager` |
| **Method**                    | `clear_logs` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that `clear_logs` can gracefully handle an exception raised by the `StorageManager`'s `clear_logs` method (e.g., a database error) and still proceed to clear the flat log file. |
| **Input Specifications**      | A log file is created. A mock `StorageManager` is used whose `clear_logs` method always raises an exception. `clear_logs` is called. |
| **Expected Result**           | The `clear_logs` method should complete without an unhandled exception. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_log_manager.py::test_log_manager_clear_logs_db_error` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `LoginManager` |
| **Method**                    | `_lock_interface`, `unlock_system`, `is_interface_locked`, `validate_credentials` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies the complete interface lockout and unlock cycle. It checks that after exceeding the maximum number of login attempts, the interface becomes locked, and that it is automatically unlocked after the configured `system_lock_time` has passed. |
| **Input Specifications**      | A `LoginManager` is configured with `max_login_attempts=1` and `system_lock_time=0.05`. `validate_credentials` is called with a wrong password to trigger the lock. The test then waits for a period longer than the lock time. |
| **Expected Result**           | The interface should be locked immediately after the failed login. After the timeout, calling `unlock_system` (which the internal timer would do) should successfully unlock the interface. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_login_branches.py::test_lock_interface_sets_timer_and_unlocks` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `models.SystemSettings`, `models.SafetyZone` |
| **Method**                    | `from_db_row` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies that the `from_db_row` factory method on the `SystemSettings` and `SafetyZone` models correctly creates objects from a dictionary (simulating a database row). It also checks that it returns `None` when the input is `None`. |
| **Input Specifications**      | A dictionary simulating a database row for settings and one for a zone. Also `None` is passed to the method. |
| **Expected Result**           | The methods should return a correctly populated object when given a dictionary, and `None` when given `None`. The boolean `is_armed` should be correctly converted from `1`. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_models.py::test_model_from_db_row_system_settings_and_zone` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `models.SafeHomeMode`, `models.Sensor`, `models.Camera`, `models.EventLog`, `models.LoginSession` |
| **Method**                    | `from_db_row` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | This is a comprehensive test that verifies the `from_db_row` factory method for the remaining data models in the application, ensuring they are all correctly instantiated from dictionary data. |
| **Input Specifications**      | A dictionary simulating a database row for each of the following models: `SafeHomeMode`, `Sensor`, `Camera`, `EventLog`, `LoginSession`. |
| **Expected Result**           | Each call to `from_db_row` should return a new object with its attributes correctly populated from the input dictionary. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_models.py::test_model_from_db_row_mode_sensor_camera_event_login` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `DatabaseManager` |
| **Method**                    | `initialize_schema`, `update_system_settings`, `get_system_settings`, `add_event_log`, `get_event_logs`, `clear_event_logs` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies the fundamental database operations: initializing the schema, inserting and retrieving settings, and adding, fetching, and clearing log events. |
| **Input Specifications**      | Update settings with a password. Add a log event. Clear the logs. |
| **Expected Result**           | The retrieved settings should match the updated ones. The added log should be fetchable. After clearing, the event logs should be empty. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_persistence.py::test_db_manager_basic_queries` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `StorageManager` |
| **Method**                    | `save_settings`, `load_settings`, `save_settings_to_db`, `load_settings_from_db` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests the `StorageManager`'s ability to save and load system settings to/from both the JSON backup file and the main database, ensuring both persistence layers work as expected. |
| **Input Specifications**      | A `SystemSettings` object is saved (to both JSON and DB), then loaded. It is then modified and saved only to the DB, and loaded again from the DB. |
| **Expected Result**           | The JSON file should be created. The loaded settings should match the saved settings in both cases (JSON and DB-only). |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_persistence.py::test_storage_manager_settings_json_and_db` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `StorageManager`, `LogManager` |
| **Method**                    | `add_log`, `get_logs`, `get_unseen_logs`, `mark_logs_seen`, `clear_logs` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies the full lifecycle of log management through the `StorageManager`, including adding a log, retrieving it, marking it as "seen", and clearing the log table. |
| **Input Specifications**      | A log is added via `LogManager`. It's retrieved via `get_logs` and `get_unseen_logs`. It is then marked as seen. Finally, logs are cleared. |
| **Expected Result**           | The log should be retrievable and initially be "unseen". After being marked as seen, it should no longer appear in the `get_unseen_logs` result. `clear_logs` should empty the log table. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_persistence.py::test_storage_manager_logs_and_seen` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `StorageManager` |
| **Method**                    | `save_safety_zone`, `load_safety_zone_by_id`, `delete_all_safety_zones`, `save_sensor`, `load_all_sensors`, `delete_sensor`, `save_camera`, `load_all_cameras`, `update_camera_password`, `clear_camera_passwords`, `delete_camera` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | A comprehensive CRUD test for all major data objects managed by `StorageManager`: zones, sensors, and cameras. It verifies creation, retrieval, update (for camera password), and deletion. |
| **Input Specifications**      | A zone, a sensor, and a camera are created, retrieved, updated (where applicable), and deleted. |
| **Expected Result**           | All create, read, update, and delete operations should succeed and be reflected in subsequent load calls. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_persistence.py::test_storage_manager_zone_and_sensor_crud` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `StorageManager` |
| **Method**                    | `save_mode_sensor_mapping`, `get_sensors_for_mode` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Tests the roundtrip persistence of the mode-to-sensor mapping. |
| **Input Specifications**      | A sensor is saved, and a mapping for the "HOME" mode is saved to include this sensor. |
| **Expected Result**           | `get_sensors_for_mode("HOME")` should return a list containing the ID of the saved sensor. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_persistence.py::test_storage_manager_mode_sensor_mapping` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `StorageManager` |
| **Method**                    | `save_mode_sensor_mapping` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Ensures that attempting to save a sensor mapping for a non-existent mode name does not cause an error. |
| **Input Specifications**      | `save_mode_sensor_mapping` is called with an invalid mode name "NOTAMODE". |
| **Expected Result**           | The method should complete without raising an exception. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_persistence.py::test_storage_manager_invalid_mode_mapping` |

| Field                         | Description |
|-------------------------------|-------------|
| **Class**                     | `StorageManager` |
| **Method**                    | `_check_db`, `load_settings_from_json` |
| **Author**                    | Gemini |
| **Date**                      | 2025-11-30 |
| **Version**                   | 1.0 |
| **Test Case Description**     | Verifies the error handling of the `StorageManager`. It checks that a `ValueError` is raised if the DB is not available when required, and that a `json.JSONDecodeError` is raised when trying to load a malformed JSON file. |
| **Input Specifications**      | 1. `_check_db` is called on a `StorageManager` initialized with no database.<br>2. `load_settings_from_json` is called when the `CONFIG_FILE` contains invalid JSON. |
| **Expected Result**           | The first case should raise a `ValueError`. The second case should raise a `json.JSONDecodeError`. |
Actual Result             | Pass
| **Comment (including refs)**  | `test_unit_persistence.py::test_storage_manager_check_db_and_json_errors` |