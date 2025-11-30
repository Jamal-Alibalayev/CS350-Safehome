# SafeHome Integration Test Plan (Template Mapping)
Use this as a companion to `UNITTEST_DOCUMENTATION.md`. Each test entry mirrors the template fields (ID, Class/Function, Test Case Description, Input, Expected/Actual, SDS reference). IDs align with the implemented pytest integration tests.

## Legend
- ID examples: IT-Login-Sys-Su, IT-Arm-OpenBlock, IT-Cam-Pwd, IT-Zone-Mode, IT-Alarm-Delay, IT-Log-Persist, IT-Cam-EnableDisable, IT-DB-Disconnect.
- SDS Ref: Key sequence/state/class diagram pages (SDS) to cite in the template.

## 1) External Communication / Login
- **IT-Login-Sys-Su** — Class/Function: System.login, LoginManager, StorageManager  
  Test Case Description: Master login succeeds and session recorded.  
  Input: (“admin”, “1234”), interface CONTROL_PANEL.  
  Expected: login True; login_sessions row added; failed_attempts reset.  
  SDS Ref: Common seq p47.

- **IT-Login-Guest-Su** — System.login, LoginManager  
  Scenario: Guest login records session. Input (“guest”, “0000”), CONTROL_PANEL.  
  Expected: login True; session username=guest. SDS: Common seq p47.

- **IT-Login-Web** — System.login, LoginManager._validate_web  
  Scenario: WEB two-level password “webpass1:webpass2”.  
  Expected: login True; session interface=WEB. SDS: Common seq p48.

- **IT-Login-Lock** — System.login, LoginManager._lock_interface  
  Scenario: Repeated failures lock interface.  
  Expected: is_locked[CONTROL_PANEL]=True; login_sessions failed_attempts ≥ max. SDS: p47, Login state p29~30.

- **IT-Password-Change** — System.change_password, StorageManager.save_settings  
  Scenario: Change control-panel password persists to DB.  
  Expected: login with new password succeeds; DB master_password updated. SDS: p54.

- **IT-Password-Change-CP (headless)** — SafeHomeControlPanel/System.change_password  
  Scenario: CP input changes password then re-login succeeds.  
  Expected: System login with new password succeeds; settings saved. SDS: p54.

## 2) Security / Alarm / Zone / Mode
- **IT-Arm-OpenBlock** — System.arm_system, SensorController.check_all_windoor_closed  
  Scenario: Open window blocks arming; warning log. SDS: Security seq p55.

- **IT-Alarm-Delay** — System._handle_intrusion, Alarm, call_monitoring_service  
  Scenario: Armed + entry_delay, intrusion triggers alarm/log. SDS: p58/p65.

- **IT-Arm-Zone-Alarm** — System.arm_system, SensorController, Logger  
  Scenario: Arm mode/zone, intrusion logs ALARM. SDS: p55/p58.

- **IT-Mode-Configure** — ConfigurationManager.configure_mode_sensors/get_sensors_for_mode  
  Scenario: Map sensors to mode and retrieve same list. SDS: p59~63.

- **IT-Mode-Sensor** — System._get_sensors_for_mode, StorageManager.save_mode_sensor_mapping  
  Scenario: Mode mapping reflected in system. SDS: p59~63.

- **IT-Zone-Mode** — ConfigurationManager.add_safety_zone, StorageManager.save_mode_sensor_mapping  
  Scenario: Create zone, add sensor, save/retrieve mapping. SDS: p59~63.

- **IT-Zone-Mode-Arm** — System.arm_zone/disarm_zone, SensorController  
  Scenario: Arm/disarm specific zone; only that zone’s sensors active. SDS: p55/p59~63.

- **IT-Mode-Interaction-MultiZone** — System.arm_system, SensorController  
  Scenario: Zone A armed, Zone B disarmed; intrusion only from armed zone triggers. SDS: p55/p59~63.

- **IT-Poll-Intrusion** — SensorController.poll_sensors, System._handle_intrusion  
  Scenario: Poll detects armed+open sensor, triggers intrusion handling. SDS: p58.

- **IT-Poll-MixedSensors** — SensorController.poll_sensors  
  Scenario: Mixed WINDOOR/MOTION; only armed+triggered returned. SDS: p58.

- **IT-Reset-Config** — ConfigurationManager.reset_configuration  
  Scenario: Reset recreates default zones, clears camera passwords, saves defaults. SDS: p53.

## 3) Surveillance / Camera
- **IT-Cam-Pwd** — CameraController.add_camera/get_camera_view  
  Scenario: Password-protected camera; correct password returns view; DB stores password. SDS: p66~69/p72~73.

- **IT-Cam-PTZ** — CameraController.pan/tilt/zoom, get_camera_status  
  Scenario: PTZ operations reflected in status/DB. SDS: p67/p72~73.

- **IT-Cam-Lockout** — CameraController.get_camera_view/CameraAccessGuard  
  Scenario: Repeated wrong password → lockout; access denied. SDS: p66~69.

- **IT-Cam-Lockout-Recover** — CameraAccessGuard, SafeHomeCamera.lockout timeout  
  Scenario: Lockout expires, subsequent correct password succeeds. SDS: p66~69.

- **IT-Cam-BadDirection** — CameraController pan/tilt/zoom invalid direction  
  Scenario: Invalid direction returns False safely. SDS: p67.

- **IT-Cam-EnableDisable** — CameraController.enable_camera/disable_camera  
  Scenario: Admin toggles camera enable; status/DB updated. SDS: p72~73.

- **IT-Cam-DeletePwd** — CameraController.delete_camera_password  
  Scenario: Remove password, view accessible without password. SDS: p69.

## 4) Configuration / Logging
- **IT-Log-Persist** — LogManager.add_log, StorageManager.get_logs  
  Scenario: Log written, retrievable from DB. SDS: p64.

- **IT-Log-Seen/Clear** — StorageManager.mark_logs_seen/clear_logs  
  Scenario: Mark seen, clear logs → empty result. SDS: p64.

- **IT-Email-Alert** — ConfigurationManager.send_email_alert (mock SMTP)  
  Scenario: Success/failure branches produce logs. SDS: p65.

- **IT-Email-Alert-Failure** — send_email_alert with SMTP error  
  Scenario: Failure logs error, returns False. SDS: p65.

- **IT-Config-Save-Restore** — ConfigurationManager.save_configuration + new System  
  Scenario: Save settings, new System picks up saved values. SDS: p49.

- **IT-Reset-And-Reinit** — Reset then new System defaults restored. SDS: p53.

- **IT-DB-Disconnect-Reconnect** — DatabaseManager.disconnect/connect  
  Scenario: Reconnect and execute queries after disconnect. SDS: DB design.

- **IT-Storage-ClearLogs-Empty** — StorageManager clear/mark seen on empty DB  
  Scenario: No errors on empty log operations. SDS: p64.

- **IT-DB-Rollback/Error Handling** *(pending if needed)* — DatabaseManager.rollback/execute bad SQL  
  Scenario: Error handled, connection stays usable. SDS: DB design.

- **IT-Storage-Log-Filter** *(pending)* — get_logs with start/end date/event_type filters. SDS: p64.

## 5) Control Panel / UI Logic (Headless)
- **IT-CP-Login-Arm (headless)** — SafeHomeControlPanel + System  
  Scenario: CP input “1234#” then arm/disarm commands. SDS: p47/p55.

- **IT-CP-ChangePwd (headless)** — CP password change then re-login. SDS: p54.

- **IT-CP-Invalid-Cmd (headless)** — Invalid command shows message, state handled. SDS: p55.

## 6) Dashboard / UI Handlers (Headless-friendly stubs)
- **IT-Dashboard-ModeSwitch** — MainDashboard mode handler → System set_mode/arm/disarm. SDS: p55.
- **IT-LogViewer-Refresh** — LogViewer handler loads latest DB logs. SDS: p64.
- **IT-Dashboard-LogViewer-OpenClose** — Open/close log viewer without leaks. SDS: p64.
- **IT-Dashboard-Settings-Save** — Settings save handler persists via ConfigurationManager.save_configuration. SDS: p49.
- **IT-Dashboard-ZoneManager** — Zone add/edit/delete/assign handlers reflect in DB. SDS: p59~63.
- **IT-Dashboard-CamPTZ-UI** — PTZ/enable/disable handlers call CameraController; status/logs updated. SDS: p67/p72~73.

## 7) Summary of Implemented vs Pending
- Implemented in pytest:  
  IT-Login-Sys-Su, IT-Login-Guest, IT-Login-Lock, IT-Password-Change, IT-Login-Web, IT-Password-Change-CP, IT-Arm-OpenBlock, IT-Alarm-Delay, IT-Arm-Zone-Alarm, IT-Cam-Pwd, IT-Cam-PTZ, IT-Cam-Lockout, IT-Cam-Lockout-Recover, IT-Cam-BadDirection, IT-Zone-Mode, IT-Mode-Sensor, IT-Mode-Configure, IT-Zone-Mode-Arm, IT-Mode-Interaction-MultiZone, IT-Poll-Intrusion, IT-Poll-MixedSensors, IT-Log-Persist, IT-Log-Seen/Clear, IT-Email-Alert, IT-Email-Alert-Failure, IT-Reset-Config, IT-Config-Save-Restore, IT-Reset-And-Reinit, IT-DB-Disconnect-Reconnect, IT-Storage-ClearLogs-Empty, IT-Cam-EnableDisable, IT-Cam-DeletePwd, IT-Monitoring-Call-Log, IT-CP-Login-Arm (headless), IT-CP-ChangePwd (headless), IT-CP-Invalid-Cmd (headless), IT-Dashboard-ModeSwitch/LogViewer-Refresh/ZoneManager (headless stubs).
- Pending/optional (require deeper UI or DB error sims): IT-Dashboard-LogViewer-OpenClose, IT-Dashboard-Settings-Save, IT-Dashboard-CamPTZ-UI (full Tk/xvfb), IT-DB-Rollback/Error-Handling, IT-Storage-Log-Filter, IT-Email-Alert-External (real SMTP).

## Template Entry Example (for each IT)
```
ID: IT-Login-Sys-Su
Class/Function: System.login / LoginManager / StorageManager
Test Case Description: Validate master login and DB session record.
Input Specifications: username “admin”, password “1234”, interface “CONTROL_PANEL”; DB seeded defaults.
Detailed Steps:
 1) Initialize SafeHomeSystem (creates LoginManager, StorageManager).
 2) Call System.login("admin","1234","CONTROL_PANEL").
 3) Check login_sessions row recorded; failed_attempts reset.
Expected Result: login returns True; session row added; failed_attempts == 0.
Actual Result: Pass/Fail/Exception (fill after execution).
Comment/Reference: SDS Common seq p47.
```
