# Integration Test Plan (Implemented Cases)
Each entry mirrors the course template fields (ID, Class/Function, Author/Date TBD, Description, Input, Steps, Expected, Actual, References). All cases below are implemented in `tests/integration/**` and executed headlessly via pytest.

---

### IT-Login-Sys-Su — System master login success  
| Class/Modules | Function | Author | Date |  
| --- | --- | --- | --- |  
| System, LoginManager, StorageManager | System.login | TBD | TBD |  
**Test Case Description** Validate master login succeeds and session is recorded.  
**Input Specifications** User `admin`, password `1234`, interface `CONTROL_PANEL`.  
**Detailed Step** 1) Init System. 2) Call `login("admin","1234","CONTROL_PANEL")`. 3) Query `login_sessions`.  
**Expected Result** login returns True; session row with username=admin, success=1.  
**Actual Result** Pass (automated pytest).  
**Comment** SDS login sequence p47.

---

### IT-Login-Guest-Su — Guest login session recorded  
| Class/Modules | Function | Author | Date |  
| System, LoginManager, StorageManager | System.login | TBD | TBD |  
**Test Case Description** Guest login succeeds and session row stored.  
**Input Specifications** Set guest password `0000`; interface `CONTROL_PANEL`.  
**Detailed Step** 1) Seed guest password. 2) Call login guest. 3) Read latest `login_sessions`.  
**Expected Result** login True; session username=guest, success=1.  
**Actual Result** Pass.  
**Comment** SDS login sequence p47.

---

### IT-Login-Web — Web two-level password success  
| Class/Modules | Function | Author | Date |  
| System, LoginManager | System.login | TBD | TBD |  
**Test Case Description** Validate web credentials `pass1:pass2` succeed.  
**Input Specifications** `web_password_1:web_password_2`, interface `WEB`.  
**Detailed Step** 1) Init System. 2) Call login with two-level password. 3) Inspect `login_sessions`.  
**Expected Result** login True; interface_type=WEB, success=1.  
**Actual Result** Pass.  
**Comment** SDS login seq p48.

---

### IT-Login-Lock — Lockout after failed attempts  
| Class/Modules | Function | Author | Date |  
| System, LoginManager | validate_credentials, _lock_interface | TBD | TBD |  
**Test Case Description** Repeated wrong PIN locks control panel.  
**Input Specifications** max_login_attempts=2; wrong password twice.  
**Detailed Step** 1) Set attempts=2. 2) Two failed logins. 3) Check `is_locked`. 4) Inspect last session row.  
**Expected Result** is_locked[CONTROL_PANEL]=True; failed_attempts ≥2; last login_successful=0.  
**Actual Result** Pass.  
**Comment** SDS login state p29–30.

---

### IT-Password-Change-CP — Control panel password change persists  
| Class/Modules | Function | Author | Date |  
| System, LoginManager, StorageManager | change_password | TBD | TBD |  
**Test Case Description** Change master PIN and persist to DB.  
**Input Specifications** Old PIN `1234`, new `8888` (or `9999`).  
**Detailed Step** 1) Call `change_password`. 2) Query system_settings.master_password. 3) Re-login with new PIN.  
**Expected Result** DB shows new password; login with new succeeds, old fails.  
**Actual Result** Pass.  
**Comment** SDS password change flow p54.

---

### IT-Config-Save-Restore — Save settings and reload in new System  
| Class/Modules | Function | Author | Date |  
| ConfigurationManager, StorageManager | save_configuration/load | TBD | TBD |  
**Test Case Description** Persist settings then reload in fresh System.  
**Input Specifications** entry_delay set to 42.  
**Detailed Step** 1) Set entry_delay. 2) save_configuration. 3) Shutdown. 4) New System reads settings.  
**Expected Result** New System settings.entry_delay == 42.  
**Actual Result** Pass.  
**Comment** SDS config persistence p49.

---

### IT-Reset-Config — Factory reset recreates defaults  
| Class/Modules | Function | Author | Date |  
| ConfigurationManager, StorageManager | reset_configuration | TBD | TBD |  
**Test Case Description** Reset clears camera passwords and recreates default zones.  
**Input Specifications** Seed camera password, add custom zone, then reset.  
**Detailed Step** 1) Save camera with password; add zone. 2) Call reset_configuration. 3) Inspect zones and cameras.  
**Expected Result** Default zones present; camera_passwords cleared; custom zone removed.  
**Actual Result** Pass.  
**Comment** SDS reset p53.

---

### IT-DB-Disconnect-Reconnect — DB reconnect works after disconnect  
| Class/Modules | Function | Author | Date |  
| DatabaseManager | connect/disconnect/get_safehome_modes | TBD | TBD |  
**Test Case Description** Ensure reconnect after disconnect can query modes.  
**Input Specifications** Fresh DB path.  
**Detailed Step** 1) connect + initialize_schema. 2) disconnect. 3) reconnect. 4) call get_safehome_modes.  
**Expected Result** Query returns default modes without error.  
**Actual Result** Pass.  
**Comment** SDS DB design.

---

### IT-Storage-ClearLogs-Empty — Safe on empty log operations  
| Class/Modules | Function | Author | Date |  
| StorageManager | mark_logs_seen/clear_logs | TBD | TBD |  
**Test Case Description** Mark seen and clear logs when none exist.  
**Input Specifications** Empty DB.  
**Detailed Step** 1) mark_logs_seen([]). 2) clear_logs(). 3) get_logs(limit=1).  
**Expected Result** No errors; get_logs returns [].  
**Actual Result** Pass.  
**Comment** SDS logging p64.

---

### IT-Email-Alert-Failure — SMTP failure handled  
| Class/Modules | Function | Author | Date |  
| ConfigurationManager | send_email_alert | TBD | TBD |  
**Test Case Description** SMTP error returns False and logs error.  
**Input Specifications** alert_email set; SMTP mocked to raise.  
**Detailed Step** 1) Patch smtplib.SMTP to raise. 2) call send_email_alert. 3) check recent logs.  
**Expected Result** send_email_alert returns False; log contains failure message.  
**Actual Result** Pass.  
**Comment** SDS ext comms p65.

---

### IT-Email-Alert-Success — SMTP success path  
| Class/Modules | Function | Author | Date |  
| ConfigurationManager | send_email_alert | TBD | TBD |  
**Test Case Description** Mock SMTP success sends message.  
**Input Specifications** alert_email set; DummySMTP records send.  
**Detailed Step** 1) Patch SMTP with dummy. 2) call send_email_alert. 3) verify sent list. 4) blank alert_email returns False.  
**Expected Result** First call True and recipient matches; second call False when email missing.  
**Actual Result** Pass.  
**Comment** SDS ext comms p65.

---

### IT-Arm-OpenBlock — Open window prevents arming  
| Class/Modules | Function | Author | Date |  
| System, SensorController | arm_system, check_all_windoor_closed | TBD | TBD |  
**Test Case Description** Arming blocked when window open, warning logged.  
**Input Specifications** One WINDOOR sensor armed+open; mode AWAY.  
**Detailed Step** 1) Add/arm windoor; simulate_open. 2) call arm_system(AWAY). 3) inspect recent logs.  
**Expected Result** arm_system returns False; warning message logged.  
**Actual Result** Pass.  
**Comment** SDS security seq p55.

---

### IT-Alarm-Delay — Intrusion triggers alarm after entry delay  
| Class/Modules | Function | Author | Date |  
| System, Alarm | _handle_intrusion, _start_entry_delay_countdown | TBD | TBD |  
**Test Case Description** Armed system with entry_delay 0 triggers alarm and monitoring log.  
**Input Specifications** Mode AWAY; entry_delay=0; windoor intrusion.  
**Detailed Step** 1) Map sensor to AWAY. 2) arm_system. 3) simulate_open + _handle_intrusion. 4) wait; check alarm active.  
**Expected Result** Alarm active; monitoring log recorded.  
**Actual Result** Pass.  
**Comment** SDS p58/p65.

---

### IT-Arm-Zone-Alarm — Arm zone and log intrusion  
| Class/Modules | Function | Author | Date |  
| System, SensorController, LogManager | arm_system/_handle_intrusion | TBD | TBD |  
**Test Case Description** Arm AWAY, trigger sensor, ALARM log persists.  
**Input Specifications** Windoor sensor mapped to AWAY.  
**Detailed Step** 1) Add sensor map. 2) arm_system. 3) simulate_open + _handle_intrusion. 4) query event_logs ALARM.  
**Expected Result** ALARM log contains INTRUSION.  
**Actual Result** Pass.  
**Comment** SDS p58.

---

### IT-Mode-Sensor — Mode mapping retrieval  
| Class/Modules | Function | Author | Date |  
| StorageManager, System | save_mode_sensor_mapping/_get_sensors_for_mode | TBD | TBD |  
**Test Case Description** Save sensor mapping for mode and retrieve via System.  
**Input Specifications** HOME mode mapped to sensor ID.  
**Detailed Step** 1) add sensor. 2) save_mode_sensor_mapping("HOME",[id]). 3) call _get_sensors_for_mode(HOME).  
**Expected Result** Returned list contains sensor id.  
**Actual Result** Pass.  
**Comment** SDS mode config p59–63.

---

### IT-Mode-Interaction-MultiZone — Only armed zone triggers  
| Class/Modules | Function | Author | Date |  
| System, SensorController | arm_zone, poll_sensors | TBD | TBD |  
**Test Case Description** Zone A armed, Zone B disarmed; only A intrusion detected.  
**Input Specifications** Two zones with windoor sensors.  
**Detailed Step** 1) Arm zone A only. 2) Trigger B → poll_sensors. 3) Trigger A → poll_sensors + _handle_intrusion.  
**Expected Result** B not returned; A returned; alarm handled.  
**Actual Result** Pass.  
**Comment** SDS p55/p59–63.

---

### IT-Zone-Mode-Arm — Arm/disarm specific zone  
| Class/Modules | Function | Author | Date |  
| System, SensorController | arm_zone/disarm_zone | TBD | TBD |  
**Test Case Description** Only zone sensors are activated when zone armed.  
**Input Specifications** Zone with windoor; separate sensor outside zone.  
**Detailed Step** 1) Create zone+sensor. 2) arm_zone. 3) Verify sensor active, others not. 4) disarm_zone.  
**Expected Result** Zone sensors active when armed; inactive when disarmed.  
**Actual Result** Pass.  
**Comment** SDS zone handling p59–63.

---

### IT-Mode-Configure — configure_mode_sensors persists mapping  
| Class/Modules | Function | Author | Date |  
| ConfigurationManager | configure_mode_sensors/get_sensors_for_mode | TBD | TBD |  
**Test Case Description** Mode mapping created via API and retrievable.  
**Input Specifications** HOME mode with one windoor sensor.  
**Detailed Step** 1) Add sensor. 2) call configure_mode_sensors("HOME",[id]). 3) get_sensors_for_mode("HOME").  
**Expected Result** List equals assigned sensors.  
**Actual Result** Pass.  
**Comment** SDS mode config p59–63.

---

### IT-Poll-Intrusion — poll_sensors detects armed/open  
| Class/Modules | Function | Author | Date |  
| SensorController, System | poll_sensors/_handle_intrusion | TBD | TBD |  
**Test Case Description** Armed/open windoor returned by poll and intrusion handled.  
**Input Specifications** Windoor armed, simulate_open.  
**Detailed Step** 1) Add/arm windoor. 2) simulate_open. 3) poll_sensors. 4) optionally _handle_intrusion.  
**Expected Result** poll returns sensor id; alarm can be triggered.  
**Actual Result** Pass.  
**Comment** SDS p58.

---

### IT-Poll-MixedSensors — Only triggered armed sensors returned  
| Class/Modules | Function | Author | Date |  
| SensorController | poll_sensors | TBD | TBD |  
**Test Case Description** Armed windoor open, motion idle → only windoor returned.  
**Input Specifications** One windoor (open), one motion (not triggered).  
**Detailed Step** 1) Add/arm both. 2) simulate_open windoor. 3) poll_sensors.  
**Expected Result** Result ids include windoor, not motion.  
**Actual Result** Pass.  
**Comment** SDS p58.

---

### IT-Camera-Pwd — Password-protected camera access  
| Class/Modules | Function | Author | Date |  
| CameraController, SafeHomeCamera | add_camera/get_camera_view | TBD | TBD |  
**Test Case Description** Camera password stored; wrong denied, correct returns image.  
**Input Specifications** password="1234"; wrong="0000".  
**Detailed Step** 1) add_camera with password. 2) get_camera_view wrong→None. 3) get_camera_view correct→Image. 4) check DB camera_password.  
**Expected Result** Access only with correct password; DB row persists password.  
**Actual Result** Pass.  
**Comment** SDS camera seq p66–69/p72–73.

---

### IT-Camera-PTZ — PTZ operations persist status  
| Class/Modules | Function | Author | Date |  
| CameraController | pan_camera/tilt_camera/zoom_camera/get_camera_status | TBD | TBD |  
**Test Case Description** PTZ updates status and DB row exists.  
**Input Specifications** Camera without password.  
**Detailed Step** 1) add_camera. 2) pan/tilt/zoom. 3) get_camera_status. 4) query cameras table.  
**Expected Result** Status id matches camera; DB row present.  
**Actual Result** Pass.  
**Comment** SDS p67/p72–73.

---

### IT-Camera-EnableDisable — Admin toggles camera  
| Class/Modules | Function | Author | Date |  
| CameraController | enable_camera/disable_camera | TBD | TBD |  
**Test Case Description** Admin can disable/enable and status reflects.  
**Input Specifications** role="admin".  
**Detailed Step** 1) add_camera. 2) disable_camera(admin). 3) check status is_enabled False. 4) enable_camera(admin) → True.  
**Expected Result** Status toggles accordingly.  
**Actual Result** Pass.  
**Comment** SDS p72–73.

---

### IT-Camera-DeletePwd — Remove password allows view  
| Class/Modules | Function | Author | Date |  
| CameraController | delete_camera_password/get_camera_view | TBD | TBD |  
**Test Case Description** After deleting password, view accessible without password.  
**Input Specifications** Initial password="pw".  
**Detailed Step** 1) add_camera with password. 2) delete_camera_password(...,"pw"). 3) get_camera_view with None.  
**Expected Result** View returns Image without password.  
**Actual Result** Pass.  
**Comment** SDS p69.

---

### IT-Camera-Lockout — Wrong password triggers lockout  
| Class/Modules | Function | Author | Date |  
| CameraController, SafeHomeCamera | get_camera_view | TBD | TBD |  
**Test Case Description** After exceeding attempts, camera denies access even with correct password.  
**Input Specifications** max_attempts=1; wrong then correct.  
**Detailed Step** 1) add_camera with password. 2) get_camera_view wrong → None. 3) Immediately retry correct → None (locked).  
**Expected Result** Lockout enforced.  
**Actual Result** Pass.  
**Comment** SDS p66–69.

---

### IT-Camera-Lockout-Recover — Lockout timeout restores access  
| Class/Modules | Function | Author | Date |  
| CameraController, SafeHomeCamera | get_camera_view | TBD | TBD |  
**Test Case Description** After lockout period, correct password succeeds.  
**Input Specifications** max_attempts=1; lockout_seconds=0.2.  
**Detailed Step** 1) wrong attempt triggers lock. 2) correct attempt during lock → None. 3) wait > lockout. 4) correct attempt succeeds.  
**Expected Result** Image returned after timeout.  
**Actual Result** Pass.  
**Comment** SDS p66–69.

---

### IT-Camera-BadDirection — Invalid PTZ directions safe-fail  
| Class/Modules | Function | Author | Date |  
| CameraController | pan/tilt/zoom | TBD | TBD |  
**Test Case Description** Invalid direction returns False without error.  
**Input Specifications** direction="noop".  
**Detailed Step** 1) add_camera. 2) call pan/tilt/zoom with invalid.  
**Expected Result** Each returns False.  
**Actual Result** Pass.  
**Comment** SDS p67.

---

### IT-CP-Login-Arm — Control panel headless login + logout  
| Class/Modules | Function | Author | Date |  
| SafeHomeControlPanel, System | _handle_key_input/button_sharp/_handle_command | TBD | TBD |  
**Test Case Description** Simulate CP input to login and logout.  
**Input Specifications** PIN "1234"; commands via _handle_command.  
**Detailed Step** 1) Patch CP UI methods to no-op. 2) Enter "1234#", login. 3) Command "0" to logout.  
**Expected Result** is_authenticated toggles True then False; System login succeeds.  
**Actual Result** Pass.  
**Comment** SDS CP/login flow p47.

---

### IT-CP-Invalid-Cmd — Invalid command handled  
| Class/Modules | Function | Author | Date |  
| SafeHomeControlPanel | _handle_command | TBD | TBD |  
**Test Case Description** Invalid command produces message without crash.  
**Input Specifications** Command "7".  
**Detailed Step** 1) Patch display recorders. 2) Login. 3) _handle_command("7").  
**Expected Result** Display message contains "Invalid"; panel remains functional.  
**Actual Result** Pass.  
**Comment** SDS CP command handling.

---

### IT-Dashboard-ModeSwitch — Dashboard handler sets mode  
| Class/Modules | Function | Author | Date |  
| MainDashboard | _set_mode handler | TBD | TBD |  
**Test Case Description** Headless stub invokes mode set handler.  
**Input Specifications** Desired mode AWAY.  
**Detailed Step** 1) Stub MainDashboard Tk deps. 2) Invoke handler to set mode. 3) Verify current_mode set.  
**Expected Result** Mode updated without error.  
**Actual Result** Pass.  
**Comment** SDS dashboard mode control.

---

### IT-LogViewer-Refresh — Log viewer handler loads logs  
| Class/Modules | Function | Author | Date |  
| LogViewerWindow, LogManager | _refresh_logs | TBD | TBD |  
**Test Case Description** Refresh handler retrieves recent logs headlessly.  
**Input Specifications** Pre-seeded log "UI log".  
**Detailed Step** 1) Stub LogViewerWindow init/UI. 2) Add log. 3) Call _refresh_logs.  
**Expected Result** Returns recent log with message "UI log".  
**Actual Result** Pass.  
**Comment** SDS logging UI.

---

### IT-ZoneManager-Handlers — Zone manager CRUD handlers  
| Class/Modules | Function | Author | Date |  
| ZoneManagerWindow, ConfigurationManager | add/update/delete zone | TBD | TBD |  
**Test Case Description** Simulate zone manager add/edit/delete in headless stubs.  
**Input Specifications** Zone name "UI-Zone".  
**Detailed Step** 1) Stub ZoneManagerWindow init. 2) Add zone. 3) Update name. 4) Delete zone.  
**Expected Result** Zone exists after add/update; removed after delete.  
**Actual Result** Pass.  
**Comment** SDS zone manager UI p59–63.

---

### IT-Monitoring-Call-Log — Monitoring call logged  
| Class/Modules | Function | Author | Date |  
| System, LogManager | call_monitoring_service | TBD | TBD |  
**Test Case Description** Monitoring call produces log entry.  
**Input Specifications** Armed/triggered sensor.  
**Detailed Step** 1) Add/arm sensor. 2) simulate_open. 3) call_monitoring_service. 4) Inspect recent logs.  
**Expected Result** Log message contains "Calling monitoring service".  
**Actual Result** Pass.  
**Comment** SDS monitoring call p65.

