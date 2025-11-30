# Unit Test Mapping (Template IDs ↔ Pytest Cases)
This document maps currently written pytest unit tests to template IDs (e.g., UT-Conf-..., UT-Storage-..., UT-Cam-..., UT-LogMgr-...) without modifying the existing `UNITTEST_DOCUMENTATION.md`. The SDS reference pages are listed by test purpose.

## Legend
- File → `tests/unit/...`
- ID → UT ID to be entered in the template/report (suggested)
- SDS Ref → Main sequence/state diagram page

## Configuration / Persistence
- File: `tests/unit/test_unit_persistence.py`
  - UT-Storage-Settings: save/load settings JSON+DB (`test_storage_manager_settings_json_and_db`) — SDS state p33/p34
  - UT-DB-Basic: DB initialize & event log insert/select/clear (`test_db_manager_basic_queries`) — SDS state p33
  - UT-Storage-Logs: save/get/seen/clear event logs (`test_storage_manager_logs_and_seen`) — SDS seq p64
  - UT-Storage-ZoneSensor: zone/sensor/camera CRUD, password clear (`test_storage_manager_zone_and_sensor_crud`) — SDS seq p59~63/p66~73
  - UT-Storage-ModeMap: mode-sensor mapping (`test_storage_manager_mode_sensor_mapping`) — SDS seq p59~63

## Camera / Surveillance
- File: `tests/unit/test_unit_camera_guard.py`
  - UT-CamGuard-Require: CameraAccessGuard deny/lockout (`test_camera_access_guard_denies_when_locked`) — SDS seq p66~69
  - UT-CamCtrl-AccessHelper: internal access helper password check (`test_camera_controller_get_camera_with_access`) — SDS seq p66~69
  - UT-Cam-LockStatus: SafeHomeCamera lockout reset/status (`test_safehome_camera_lock_and_status`) — SDS state p38
  - UT-CamCtrl-Status: remove_camera + get_all_camera_statuses (`test_camera_controller_remove_and_statuses`) — SDS seq p72~73
  - UT-CamCtrl-RemoveAll: CameraController remove/view PTZ/zoom/password persistence (`test_camera_controller_access_and_password` in `test_unit_surveillance.py`) — SDS seq p66~73
- File: `tests/unit/test_unit_interfaces_and_devices.py`
  - UT-DeviceCam-Tick: DeviceCamera _tick/time increment + missing asset handling (`test_device_camera_tick_and_id`) — SDS device state p36
  - UT-DeviceSensorTester-Headless: showSensorTester skips in headless (`test_device_sensor_tester_headless_skip`) — hardware shim
  - UT-Hardware-Motion/WinDoor: DeviceMotionDetector/DeviceWinDoorSensor arm/intrude/release/test_armed_state (`test_device_motion_detector_and_windoor_hardware`) — SDS state p37/p42
  - UT-Sensor-Accessors: WindowDoorSensor/MotionSensor getters/setters/test_armed_state (`test_motion_and_windoor_test_armed_state_and_accessors`) — SDS state p37/p42/p39
  - UT-CP-LoginArm: SafeHomeControlPanel login + arm/disarm command logic (headless) (`test_safehome_control_panel_login_and_arm_disarm` in `test_unit_ui_logic.py`) — SDS seq p47/p55
  - UT-CP-ChangePwd: SafeHomeControlPanel change password flow (headless) (`test_safehome_control_panel_change_password_flow` in `test_unit_ui_logic.py`) — SDS seq p54
  - UT-Dashboard-Permissions: MainDashboard permission matrix (admin vs guest) (`test_main_dashboard_build_permissions` in `test_unit_ui_logic.py`) — design rule

## Core / System
- File: `tests/unit/test_unit_core.py`
  - UT-System-OnOff: turn_on/turn_off (`test_system_turn_on_off`) — SDS seq p50/p52
  - UT-System-Status: get_system_status snapshot (`test_system_status_snapshot`) — SDS state p41
  - UT-Alarm-Ring: alarm ring/auto-stop (`test_alarm_ring_and_stop`) — SDS state p35
  - UT-System-Polling: start/stop sensor polling threads (`test_system_polling_start_stop`) — SDS state p41
- File: `tests/unit/test_unit_edges.py`
  - UT-System-Monitoring: call_monitoring_service logs monitoring call (`test_call_monitoring_service_logs`) — SDS seq p65
  - UT-System-EntryDelay-Cancel: entry delay canceled when disarmed (`test_start_entry_delay_countdown_no_alarm_when_disarmed`) — SDS seq p58
  - UT-System-EntryDelay-Alarm: alarm triggers after delay (`test_start_entry_delay_countdown_triggers_after_delay`) — SDS seq p58
  - UT-Conf-Email: `send_email_alert` success/failure branches (`test_send_email_alert_success_and_failure`) — SDS p65
  - UT-Storage-CheckDb: `_check_db` raises without DB (`test_storage_manager_check_db_and_json_errors`) — SDS state p33
  - UT-Storage-JSON-Invalid: invalid JSON raises decode error (same test) — SDS state p33
  - UT-Storage-ModeMap-Invalid: unknown mode name no-op (`test_storage_manager_invalid_mode_mapping`) — SDS seq p59~63
  - UT-Mode-FromDb: `SafeHomeMode.from_db_mode_name` unknown → DISARMED (`test_safehome_mode_from_db_defaults`) — SDS state p32
  - UT-Settings-FromDb: `SystemSettings.from_db_row` happy/None cases (`test_system_settings_from_db_row_and_defaults`) — SDS state p34
  - UT-DeviceCamera-SetId: missing asset handled (`test_device_camera_missing_file`) — SDS device state p36

## Security / Sensors / Login
- File: `tests/unit/test_unit_security.py`
  - UT-Sensor-Add-Poll: add/arm/poll/remove (`test_sensor_controller_add_poll_remove`) — SDS state p40
  - UT-Sensor-ClosedCheck: open window blocks arm (`test_sensor_controller_check_all_windoor_closed`) — SDS seq p55
  - UT-Sensor-Behaviors: armed gating for window/motion (`test_window_and_motion_sensor_behaviors`) — SDS state p37/p42
  - UT-Login-Lock: lockout + unlock (`test_login_manager_lock_and_unlock`) — SDS state p29~30
  - UT-System-ArmDisarm: arm/disarm + alarm on intrusion (`test_system_arm_disarm_and_alarm`) — SDS seq p55/p58
  - UT-System-Login: login + password change (`test_system_login_and_password_change`) — SDS seq p47/p54

## Log Manager
- File: `tests/unit/test_unit_log_manager.py`
  - UT-LogMgr-WriteClear: add_log writes file/DB; clear_logs empties (`test_log_manager_write_and_clear`) — SDS state p27~28

## Camera / Surveillance (additional)
- File: `tests/unit/test_unit_surveillance.py`
  - UT-Cam-Pwd: SafeHomeCamera password/lockout (`test_safehome_camera_password_and_lockout`) — SDS seq p68~69
  - UT-Cam-Controls: PTZ/zoom bounds + status (`test_safehome_camera_controls_and_status`) — SDS state p38/p67
  - UT-CamCtrl-Access: CameraController view/password + set/delete password (`test_camera_controller_access_and_password`) — SDS seq p66~69/p72~73
- File: `tests/unit/test_unit_models.py`
  - UT-Model-SystemSettings/Zone: `SystemSettings.from_db_row`, `SafetyZone.from_db_row` (`test_model_from_db_row_system_settings_and_zone`) — SDS state p34/p31
  - UT-Model-Others: SafeHomeMode/Sensor/Camera/EventLog/LoginSession `from_db_row` (`test_model_from_db_row_mode_sensor_camera_event_login`) — SDS class diagrams p13~16

## Sensors / Security (additional)
- File: `tests/unit/test_unit_surveillance.py` (covers sensor simulators via camera? N/A) — already mapped above
- File: `tests/unit/test_unit_security.py` (covers sensors/system/login) — already mapped above

## Notes / Remaining Gaps
- GUI-heavy TK classes (ControlPanel, Dashboard, dialogs) remain untested in unit scope due to headless constraints; consider widget-level tests with `SAFEHOME_HEADLESS` off + xvfb if needed.
- Device hardware shims (DeviceCamera tick thread, DeviceSensorTester GUI launcher) partially covered; deeper coverage requires allowing threads/GUI in test env.
- For any UT IDs missing in `UNITTEST_DOCUMENTATION.md`, use the proposed UT-* IDs above when filling the template tables (Class/Method/Test Case Description/Input/Expected/Actual/Reference).
- Manual/GUI-required (not covered in pytest): CameraMonitor (Tk feed), DeviceControlPanelAbstract/SafeHomeControlPanel UI wiring, LoginWindow/MainDashboard/ZoneManager/Add/Edit/Assign dialogs, Sensor simulator GUI. These need interactive or xvfb-based UI tests.
