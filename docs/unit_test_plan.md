# Unit Test Plan (Implemented Cases)
Format follows the course template: each test lists ID, Class/Method, description, inputs, expected, actual, and SDS/SRS references when applicable. Author/Date left TBD; Version set to 1.0 unless noted. All tests correspond to implemented pytest cases in `tests/unit/**`.

---

## 1. External Communication / Login / UI Logic

### UT-Login-Lock-CP — Control panel lock/unlock
| Class | Method | Author | Date | Version |
| --- | --- | --- | --- | --- |
| LoginManager | validate_credentials/_lock_interface | TBD | TBD | 1.0 |
**Test Case Description** Repeated wrong PIN locks interface, unlock clears flag.  
**Input Specifications** max_login_attempts=2; two wrong PINs; unlock_system().  
**Expected Result** is_locked[CONTROL_PANEL]=True then False after unlock.  
**Actual Result** Pass.  
**Comment** SDS login state p29–30.  

### UT-Login-Branches — Validate branches and reset attempts
| Class | Method | Author | Date | Version |
| LoginManager | validate_credentials | TBD | TBD | 1.0 |
**Test Case Description** Mixed correct/incorrect for admin/guest/web; attempts reset on success.  
**Input Specifications** admin/1234 success, wrong PIN failure, guest default “0000”, invalid interface.  
**Expected Result** Success resets attempts; invalid interface returns False without crash.  
**Actual Result** Pass.  
**Comment** SDS login seq p47–48.  

### UT-System-Login-PwdChange — System login and password change integration
| Class | Method | Author | Date | Version |
| System | login/change_password | TBD | TBD | 1.0 |
**Test Case Description** System login succeeds; password change persists and old password rejected.  
**Input Specifications** Login with default PIN; change to new PIN; re-login with old/new.  
**Expected Result** Initial login True; old PIN fails after change; new PIN succeeds.  
**Actual Result** Pass.  
**Comment** SDS login + password change p47/p54.  

### UT-Login-LogSession — Sessions recorded
| Class | Method | Author | Date | Version |
| LoginManager | _log_session | TBD | TBD | 1.0 |
**Test Case Description** Session rows written for success/failure.  
**Input Specifications** Call validate_credentials twice (success/fail).  
**Expected Result** DB rows reflect username, interface, success flag.  
**Actual Result** Pass.  
**Comment** SDS login logging p47.  

### UT-Login-Guest-Web — Guest + web parsing
| Class | Method | Author | Date | Version |
| LoginManager | _validate_control_panel/_validate_web | TBD | TBD | 1.0 |
**Test Case Description** Guest PIN acceptance and two-level web password parsing.  
**Input Specifications** guest/“0000”; web “pass1:pass2”; malformed password.  
**Expected Result** Valid combos return True; malformed returns False.  
**Actual Result** Pass.  

### UT-CP-Login-Arm — Headless control panel login/arm/disarm
| Class | Method | Author | Date | Version |
| SafeHomeControlPanel | _handle_key_input/_handle_command | TBD | TBD | 1.0 |
**Test Case Description** Simulate CP login then arm/disarm in headless mode.  
**Input Specifications** Key sequence “1234#”, arm/disarm commands.  
**Expected Result** is_authenticated True after login; arm/disarm succeeds.  
**Actual Result** Pass.  
**Comment** SDS CP seq p47.  

### UT-CP-ChangePwd — Control panel password change
| Class | Method | Author | Date | Version |
| SafeHomeControlPanel | _handle_command/change password path | TBD | TBD | 1.0 |
**Test Case Description** Change password via CP and verify login with new PIN.  
**Input Specifications** Command “3”, new PIN “8888”.  
**Expected Result** New PIN accepted; old rejected.  
**Actual Result** Pass.  
**Comment** SDS password change p54.  

### UT-CP-Invalid-Cmd — Invalid command handled
| Class | Method | Author | Date | Version |
| SafeHomeControlPanel | _handle_command | TBD | TBD | 1.0 |
**Test Case Description** Invalid command shows message without crashing.  
**Input Specifications** After login, command “7”.  
**Expected Result** Display includes “Invalid”; panel remains functional.  
**Actual Result** Pass.  

### UT-Dashboard-Permissions — Permission matrix build
| Class | Method | Author | Date | Version |
| MainDashboard | _build_permissions | TBD | TBD | 1.0 |
**Test Case Description** Permissions map contains expected roles/actions.  
**Input Specifications** Instantiate dashboard; inspect permissions dict.  
**Expected Result** Admin/guest scopes populated per SDS.  
**Actual Result** Pass.  

---

## 2. Security / Sensors / System / Alarm

### UT-Sensor-CRUD-Poll — Add/poll/remove sensors
| Class | Method | Author | Date | Version |
| SensorController | add_sensor/poll_sensors/remove_sensor | TBD | TBD | 1.0 |
**Test Case Description** Add sensors, poll armed/open, remove success.  
**Input Specifications** WINDOOR/MOTION added, armed, simulated open.  
**Expected Result** poll returns triggered sensor; remove returns True.  
**Actual Result** Pass.  

### UT-Sensor-Ready-Check — Windoor closed gating
| Class | Method | Author | Date | Version |
| SensorController | check_all_windoor_closed | TBD | TBD | 1.0 |
**Test Case Description** Open sensor detected; closed passes.  
**Input Specifications** One windoor open vs closed.  
**Expected Result** all_closed False/True accordingly; list of open sensors.  
**Actual Result** Pass.  

### UT-Windoor-Motion-Behaviors — Device behaviors
| Class | Method | Author | Date | Version |
| WindowDoorSensor / MotionSensor | simulate_open/close/motion | TBD | TBD | 1.0 |
**Test Case Description** Arm/disarm/read/status for windoor and motion sensors.  
**Input Specifications** Arm sensors, simulate intrude/release, read().  
**Expected Result** Reads only when armed; status reflects open/motion.  
**Actual Result** Pass.  

### UT-Sensor-Edge-Branches — Edge cases
| Class | Method | Author | Date | Version |
| SensorController | arm/disarm/arm_sensors_in_zone/get_sensor_status | TBD | TBD | 1.0 |
**Test Case Description** Handles missing IDs, empty lists, unknown types.  
**Input Specifications** Invalid sensor type, nonexistent IDs.  
**Expected Result** Safe False/None returns; no crashes.  
**Actual Result** Pass.  

### UT-System-Arm-Disarm-Alarm — Core arming and alarm
| Class | Method | Author | Date | Version |
| System | arm_system/disarm_system/_trigger_alarm | TBD | TBD | 1.0 |
**Test Case Description** Arm/disarm sets mode, activates sensors, stops alarm.  
**Input Specifications** Map sensor to AWAY; simulate alarm then stop.  
**Expected Result** Mode updates; alarm active then cleared; sensors disarmed.  
**Actual Result** Pass.  

### UT-System-TurnOn-Off — Power cycle core
| Class | Method | Author | Date | Version |
| System | turn_on/turn_off | TBD | TBD | 1.0 |
**Test Case Description** is_running toggles; polling threads managed.  
**Input Specifications** Call turn_on, turn_off.  
**Expected Result** Running True/False; polling started/stopped.  
**Actual Result** Pass.  

### UT-System-Status-Snapshot — Status report
| Class | Method | Author | Date | Version |
| System | get_system_status | TBD | TBD | 1.0 |
**Test Case Description** Status dict reflects counts and mode.  
**Input Specifications** Add sensors/cameras; call get_system_status.  
**Expected Result** Keys include is_running, current_mode, counts.  
**Actual Result** Pass.  

### UT-System-Polling-StartStop — Polling thread control
| Class | Method | Author | Date | Version |
| System | _start_sensor_polling/_stop_sensor_polling | TBD | TBD | 1.0 |
**Test Case Description** Starts background polling and stops cleanly.  
**Input Specifications** call start, then stop with event set.  
**Expected Result** Thread alive then joined without hang.  
**Actual Result** Pass.  

### UT-System-Entry-Delay — Countdown branches
| Class | Method | Author | Date | Version |
| System | _start_entry_delay_countdown | TBD | TBD | 1.0 |
**Test Case Description** No alarm when disarmed; alarm when armed after delay.  
**Input Specifications** entry_delay set small; disarmed vs armed sensor read.  
**Expected Result** Disarmed: no alarm; Armed: alarm after delay.  
**Actual Result** Pass.  

### UT-Alarm-Ring-Stop — Alarm duration
| Class | Method | Author | Date | Version |
| Alarm | ring/stop | TBD | TBD | 1.0 |
**Test Case Description** Alarm sets is_ringing True; stop clears.  
**Input Specifications** Call ring then stop.  
**Expected Result** is_ringing toggles True→False.  
**Actual Result** Pass.  

### UT-System-Trigger-Alarm — Trigger alarm helper
| Class | Method | Author | Date | Version |
| System | _trigger_alarm | TBD | TBD | 1.0 |
**Test Case Description** Trigger alarm invokes alarm.ring then call_monitoring_service.  
**Input Specifications** Armed system with sensor; call _trigger_alarm.  
**Expected Result** Alarm active; monitoring log emitted.  
**Actual Result** Pass.  

### UT-Monitoring-Log — Monitoring call logging
| Class | Method | Author | Date | Version |
| System | call_monitoring_service | TBD | TBD | 1.0 |
**Test Case Description** Monitoring call logs ALARM message.  
**Input Specifications** Sensor with location; call monitoring.  
**Expected Result** Log contains “Calling monitoring service”.  
**Actual Result** Pass.  

### UT-System-Shutdown — Graceful shutdown
| Class | Method | Author | Date | Version |
| System | shutdown | TBD | TBD | 1.0 |
**Test Case Description** Shutdown stops polling, saves config, shuts controllers.  
**Input Specifications** System with sensor/camera controllers.  
**Expected Result** turn_off invoked; controllers shutdown without exceptions.  
**Actual Result** Pass.  

---

## 3. Surveillance / Cameras

### UT-Cam-Password-Lockout — Password verify and lockout
| Class | Method | Author | Date | Version |
| SafeHomeCamera | verify_password/is_locked | TBD | TBD | 1.0 |
**Test Case Description** Wrong attempts increment, lockout enforced then clears.  
**Input Specifications** max_attempts=1; wrong then correct.  
**Expected Result** Locked after wrong; unlock after timeout; correct succeeds.  
**Actual Result** Pass.  

### UT-Cam-Controls-Status — PTZ/enable/status
| Class | Method | Author | Date | Version |
| SafeHomeCamera | pan_left/right/tilt/zoom/get_status | TBD | TBD | 1.0 |
**Test Case Description** PTZ changes state; status reports angles/zoom.  
**Input Specifications** Call PTZ methods; get_status.  
**Expected Result** Status reflects enabled, angles, zoom.  
**Actual Result** Pass.  

### UT-Cam-Getters-LockState — Accessors and lock state
| Class | Method | Author | Date | Version |
| SafeHomeCamera | getters/_is_locked | TBD | TBD | 1.0 |
**Test Case Description** Get id/name/location/status and lock state toggling.  
**Input Specifications** Create camera with password; call accessors.  
**Expected Result** Values match init; lock resets on correct password.  
**Actual Result** Pass.  

### UT-CamController-Access — Access with passwords
| Class | Method | Author | Date | Version |
| CameraController | add_camera/get_camera_view/require_access | TBD | TBD | 1.0 |
**Test Case Description** Correct password returns image; wrong denied; require_access enforces.  
**Input Specifications** Camera with password; get_camera_view with wrong/correct.  
**Expected Result** Image on correct; None on wrong; guard warns.  
**Actual Result** Pass.  

### UT-CamController-Denied-Branches — Access denied and delete password
| Class | Method | Author | Date | Version |
| CameraController | get_camera_view/delete_camera_password | TBD | TBD | 1.0 |
**Test Case Description** Missing file/incorrect access returns None; delete password succeeds.  
**Input Specifications** Wrong password; missing image path; delete old password.  
**Expected Result** None on denied; delete returns True.  
**Actual Result** Pass.  

### UT-CamController-Lockout-RequireAccess — Lockout enforced
| Class | Method | Author | Date | Version |
| CameraController/SafeHomeCamera | get_camera_view | TBD | TBD | 1.0 |
**Test Case Description** Wrong password causes lockout; require_access rejects.  
**Input Specifications** max_attempts=1; wrong password.  
**Expected Result** Subsequent access denied until timeout.  
**Actual Result** Pass.  

### UT-CamController-Boundaries-Status — Invalid directions/status
| Class | Method | Author | Date | Version |
| CameraController | pan/tilt/zoom/get_all_camera_statuses | TBD | TBD | 1.0 |
**Test Case Description** Bad directions return False; statuses list built.  
**Input Specifications** direction “noop”; multiple cameras.  
**Expected Result** False on invalid; statuses length matches cameras.  
**Actual Result** Pass.  

### UT-InterfaceCamera-Concrete — Interface camera methods
| Class | Method | Author | Date | Version |
| InterfaceCamera | set_id/get_id/get_view/pan/tilt/zoom | TBD | TBD | 1.0 |
**Test Case Description** Concrete stub returns basic values.  
**Input Specifications** Call methods on InterfaceCamera.  
**Expected Result** IDs set/get; view not None; PTZ return True.  
**Actual Result** Pass.  

### UT-DeviceCamera-View-And-Errors — Image loading/cropping
| Class | Method | Author | Date | Version |
| DeviceCamera | get_view/_tick | TBD | TBD | 1.0 |
**Test Case Description** Returns PIL image; handles missing file and crop errors gracefully.  
**Input Specifications** Valid image path; missing path; mocked crop failure.  
**Expected Result** Image instance or None on failure; no crash.  
**Actual Result** Pass.  

### UT-CameraGuard-Denies-Locked — Guard behavior
| Class | Method | Author | Date | Version |
| CameraAccessGuard | require_access/_warn | TBD | TBD | 1.0 |
**Test Case Description** Locked camera denied; warn called.  
**Input Specifications** Mock camera with is_locked True.  
**Expected Result** Returns None; warn invoked.  
**Actual Result** Pass.  

### UT-CamController-Status-Remove — Remove and status listing
| Class | Method | Author | Date | Version |
| CameraController | remove_camera/get_all_camera_statuses | TBD | TBD | 1.0 |
**Test Case Description** Remove returns True; statuses reflect removals.  
**Input Specifications** Add/remove cameras; call statuses.  
**Expected Result** Status list length matches remaining cameras.  
**Actual Result** Pass.  

---

## 4. Configuration / Settings / Zones / Modes / Email

### UT-Settings-Update-ToDict — Settings mutation
| Class | Method | Author | Date | Version |
| SystemSettings | update_settings/to_dict | TBD | TBD | 1.0 |
**Test Case Description** Update settings fields and round-trip dict.  
**Input Specifications** entry_delay, alarm_duration changes.  
**Expected Result** Dict reflects new values.  
**Actual Result** Pass.  

### UT-SafeHomeMode-DB-Mapping — Enum mapping
| Class | Method | Author | Date | Version |
| SafeHomeMode | get_db_mode_name/from_db_mode_name | TBD | TBD | 1.0 |
**Test Case Description** Enum ↔ DB names including aliases.  
**Input Specifications** HOME/AWAY/alias values.  
**Expected Result** Correct string mapping and reverse mapping.  
**Actual Result** Pass.  

### UT-Config-Zone-CRUD — Zone operations
| Class | Method | Author | Date | Version |
| ConfigurationManager | add/get/update/delete_safety_zone | TBD | TBD | 1.0 |
**Test Case Description** Create/update/delete zones, callbacks invoked.  
**Input Specifications** Zone name changes; callback raising exception.  
**Expected Result** IDs assigned; updates persisted; callbacks handled.  
**Actual Result** Pass.  

### UT-Config-Modes-Load — Mode loading and current mode
| Class | Method | Author | Date | Version |
| ConfigurationManager | _load_safehome_modes/set_mode/get_mode | TBD | TBD | 1.0 |
**Test Case Description** Modes loaded from DB; set/get current mode.  
**Input Specifications** Use default DB schema modes.  
**Expected Result** Mode dict populated; set_mode changes current_mode.  
**Actual Result** Pass.  

### UT-Config-Save — Save configuration (JSON+DB)
| Class | Method | Author | Date | Version |
| ConfigurationManager | save_configuration | TBD | TBD | 1.0 |
**Test Case Description** Saves settings; handles JSON path.  
**Input Specifications** Update settings; call save_configuration.  
**Expected Result** No exception; settings persisted.  
**Actual Result** Pass.  

### UT-Config-Email-Alert — send_email_alert branches
| Class | Method | Author | Date | Version |
| ConfigurationManager | send_email_alert | TBD | TBD | 1.0 |
**Test Case Description** Success with dummy SMTP and failure logged.  
**Input Specifications** Mock SMTP success/failure.  
**Expected Result** Returns True on success; False with error log.  
**Actual Result** Pass.  

### UT-Config-Load-Settings-Branch — Load settings from JSON/DB
| Class | Method | Author | Date | Version |
| ConfigurationManager/StorageManager | load_settings/load_settings_from_json | TBD | TBD | 1.0 |
**Test Case Description** Handles missing/empty JSON gracefully.  
**Input Specifications** temp config file path; empty file.  
**Expected Result** Returns defaults without crash.  
**Actual Result** Pass.  

### UT-Config-No-Zones-Default — Auto-create default zones
| Class | Method | Author | Date | Version |
| ConfigurationManager | __init__/reset_configuration | TBD | TBD | 1.0 |
**Test Case Description** When no zones, defaults created.  
**Input Specifications** Empty DB.  
**Expected Result** Default zones (Living Room/Bedroom) saved.  
**Actual Result** Pass.  

### UT-Config-Reset — Reset clears data and camera passwords
| Class | Method | Author | Date | Version |
| ConfigurationManager | reset_configuration | TBD | TBD | 1.0 |
**Test Case Description** Resets settings, zones, and clears camera passwords.  
**Input Specifications** Custom zones/camera passwords pre-seeded.  
**Expected Result** Defaults restored; passwords cleared.  
**Actual Result** Pass.  

### UT-Storage-Sensor-Camera-Persist — Persist sensors/cameras
| Class | Method | Author | Date | Version |
| StorageManager | save_sensor/save_camera/load_all_* | TBD | TBD | 1.0 |
**Test Case Description** Save/load sensors and cameras round-trip.  
**Input Specifications** Add sensor/camera, reload from storage.  
**Expected Result** Records returned with matching fields.  
**Actual Result** Pass.  

### UT-Storage-Mode-Mapping — Save/get mode sensor mapping
| Class | Method | Author | Date | Version |
| StorageManager | save_mode_sensor_mapping/get_sensors_for_mode | TBD | TBD | 1.0 |
**Test Case Description** Mapping persisted and retrieved.  
**Input Specifications** Map sensor IDs to HOME/AWAY; invalid mode.  
**Expected Result** Valid mode returns list; invalid safely ignored.  
**Actual Result** Pass.  

### UT-SafetyZone-Object — Zone DTO behaviors
| Class | Method | Author | Date | Version |
| SafetyZone | arm/disarm/add_sensor/remove_sensor/to_dict | TBD | TBD | 1.0 |
**Test Case Description** Zone arming and sensor list management.  
**Input Specifications** Add/remove sensor IDs; arm/disarm.  
**Expected Result** is_armed toggles; sensors updated; dict contains fields.  
**Actual Result** Pass.  

### UT-Config-Error-Paths — Error handling
| Class | Method | Author | Date | Version |
| ConfigurationManager | _notify_zone_update/reset_configuration | TBD | TBD | 1.0 |
**Test Case Description** Callback exceptions handled; reset clears camera passwords failures logged.  
**Input Specifications** Callback raising; mock clear_camera_passwords raising.  
**Expected Result** Exceptions caught/logged; no crash.  
**Actual Result** Pass.  

### UT-Mode-Configure-Manager — configure_mode_sensors
| Class | Method | Author | Date | Version |
| ConfigurationManager | configure_mode_sensors | TBD | TBD | 1.0 |
**Test Case Description** Manager call saves mapping via storage.  
**Input Specifications** Mode HOME with sensor list.  
**Expected Result** Storage save invoked; mapping retrievable.  
**Actual Result** Pass.  

---

## 5. Logging

### UT-Log-EventType — Property behavior
| Class | Method | Author | Date | Version |
| Log | event_type property | TBD | TBD | 1.0 |
**Test Case Description** Getter/setter normalizes level.  
**Input Specifications** Set level string.  
**Expected Result** event_type matches input.  
**Actual Result** Pass.  

### UT-LogManager-Write-Clear — File/DB logging
| Class | Method | Author | Date | Version |
| LogManager | add_log/clear_logs | TBD | TBD | 1.0 |
**Test Case Description** Adds logs to memory/file, clears all targets.  
**Input Specifications** Add multiple logs; call clear_logs.  
**Expected Result** File truncated; storage cleared; memory emptied.  
**Actual Result** Pass.  

### UT-LogManager-Error-Preload — Preload and error paths
| Class | Method | Author | Date | Version |
| LogManager | __init__/_write_to_file/add_log | TBD | TBD | 1.0 |
**Test Case Description** Handles preload exceptions; file write errors handled.  
**Input Specifications** Mock storage/get_logs failure; IO errors.  
**Expected Result** No crash; errors logged/printed.  
**Actual Result** Pass.  

### UT-LogManager-Storage-Error — DB save/clear failures
| Class | Method | Author | Date | Version |
| LogManager | add_log/clear_logs | TBD | TBD | 1.0 |
**Test Case Description** Storage save/clear exceptions handled.  
**Input Specifications** Mock storage save_log/clear_logs raising.  
**Expected Result** Errors caught; execution continues.  
**Actual Result** Pass.  

---

## 6. Persistence / Database / Models

### UT-DB-Basic-Queries — CRUD sanity
| Class | Method | Author | Date | Version |
| DatabaseManager | execute_query/execute_insert_query | TBD | TBD | 1.0 |
**Test Case Description** Insert and fetch sample rows.  
**Input Specifications** Simple create/select statements.  
**Expected Result** Rows returned; lastrowid set.  
**Actual Result** Pass.  

### UT-Storage-Settings-JSON-DB — Settings save/load
| Class | Method | Author | Date | Version |
| StorageManager | save_settings/load_settings | TBD | TBD | 1.0 |
**Test Case Description** Save to JSON and DB; reload matches.  
**Input Specifications** Custom entry_delay, alarm_duration.  
**Expected Result** Loaded settings equal saved values.  
**Actual Result** Pass.  

### UT-Storage-Logs-Seen — Logs and mark_seen
| Class | Method | Author | Date | Version |
| StorageManager | save_log/get_logs/get_unseen_logs/mark_logs_seen | TBD | TBD | 1.0 |
**Test Case Description** Save log, fetch unseen, mark seen.  
**Input Specifications** Insert sample log; mark seen.  
**Expected Result** Unseen count drops; logs retrievable.  
**Actual Result** Pass.  

### UT-Storage-Zone-Sensor-CRUD — Zone/sensor persistence
| Class | Method | Author | Date | Version |
| StorageManager | save/load/delete zones/sensors | TBD | TBD | 1.0 |
**Test Case Description** Create/read/update/delete zones/sensors in DB.  
**Input Specifications** Sample zone/sensor inserts and deletes.  
**Expected Result** Data present then removed; no integrity errors.  
**Actual Result** Pass.  

### UT-Storage-Mode-Mapping-Invalid — Invalid mode handling
| Class | Method | Author | Date | Version |
| StorageManager | save_mode_sensor_mapping | TBD | TBD | 1.0 |
**Test Case Description** Graceful no-op when mode not found.  
**Input Specifications** Nonexistent mode name.  
**Expected Result** No exception; commit safe.  
**Actual Result** Pass.  

### UT-Storage-CheckDB-JSON-Errors — Error paths
| Class | Method | Author | Date | Version |
| StorageManager | _check_db/save_settings_to_json | TBD | TBD | 1.0 |
**Test Case Description** Handles missing DB and JSON IO errors.  
**Input Specifications** tmp paths with restricted perms; mock IO error.  
**Expected Result** Exceptions handled; no crash.  
**Actual Result** Pass.  

### UT-Models-From-DB-Row — DTO parsing
| Class | Method | Author | Date | Version |
| SystemSettings/SafetyZone/SafeHomeMode/Sensor/Camera/EventLog/LoginSession | from_db_row | TBD | TBD | 1.0 |
**Test Case Description** Convert DB rows to model instances.  
**Input Specifications** Sample row dicts for each model.  
**Expected Result** Fields populated correctly.  
**Actual Result** Pass.  

---

## 7. Devices / Interfaces / Shims

### UT-DeviceSensorTester-Headless — GUI skip in headless
| Class | Method | Author | Date | Version |
| DeviceSensorTester | showSensorTester | TBD | TBD | 1.0 |
**Test Case Description** Returns None in headless; handles existing window/exception.  
**Input Specifications** SAFEHOME_HEADLESS=1; mock existing window; raise exception.  
**Expected Result** No GUI spawn; safe fallback.  
**Actual Result** Pass.  

### UT-Motion-Windoor-Hardware — Hardware adapter methods
| Class | Method | Author | Date | Version |
| DeviceMotionDetector/DeviceWinDoorSensor | intrude/release/read/arm/disarm | TBD | TBD | 1.0 |
**Test Case Description** Arming/disarming and reading simulated hardware.  
**Input Specifications** Call intrude/release, arm/disarm.  
**Expected Result** States toggle; read reflects intrusion only when armed.  
**Actual Result** Pass.  

### UT-DeviceCamera-Tick-ID — ID and tick updates
| Class | Method | Author | Date | Version |
| DeviceCamera | set_id/get_id/_tick | TBD | TBD | 1.0 |
**Test Case Description** ID setter/getter; tick adjusts angles/zoom clamped.  
**Input Specifications** set_id; call _tick multiple times.  
**Expected Result** ID stored; pan/tilt/zoom bounded.  
**Actual Result** Pass.  

### UT-DeviceSensorTester-Headless-Skip — No GUI when headless
| Class | Method | Author | Date | Version |
| DeviceSensorTester | showSensorTester | TBD | TBD | 1.0 |
**Test Case Description** Ensures headless flag skips Tk creation.  
**Input Specifications** SAFEHOME_HEADLESS=1.  
**Expected Result** Returns None.  
**Actual Result** Pass.  

---

## 8. UI Logic (Headless stubs)

### UT-CP-Login-Flow — Covered above (UT-CP-Login-Arm)  
### UT-CP-ChangePwd — Covered above  
### UT-CP-Invalid-Cmd — Covered above  
### UT-Dashboard-Permissions — Covered above  

*(UI logic tests are listed in section 1; no additional UI-only cases beyond those.)*

---

## 9. Misc / Camera Guard Aggregates

### UT-CameraGuard-Controller-Accessors — Combined checks
| Class | Method | Author | Date | Version |
| CameraAccessGuard/CameraController | require_access/_get_camera_with_access | TBD | TBD | 1.0 |
**Test Case Description** Guard enforces lock; controller resolves camera with access and returns statuses.  
**Input Specifications** Locked camera, unlocked camera, status fetch.  
**Expected Result** Locked returns None; unlocked returns camera; statuses include expected fields.  
**Actual Result** Pass.  

---

All entries above map directly to implemented pytest cases in `tests/unit/`. Use this plan as a template-ready catalog for reporting actual results and SDS/SRS references as needed.
