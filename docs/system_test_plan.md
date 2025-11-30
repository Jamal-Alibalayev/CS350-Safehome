# V. System-Level Test Plan

This document follows the course template format and lists planned system-level tests across the SafeHome system. Each case is tagged with an ID (ST-XXX), aligned to SDS/SRS sequence and state diagrams, and notes whether execution is automated (pytest/headless) or manual/GUI.

## Planned System Test Catalog
| ID | Title | Primary Modules | Automation | Notes |
| --- | --- | --- | --- | --- |
| ST-Login-CP-Su | Control Panel login success | ControlPanel, System, LoginManager, StorageManager | Manual/GUI (panel input) | Template example; confirm display text |
| ST-Login-CP-Lock | Control Panel lockout after failed attempts | ControlPanel, System, LoginManager | Manual/GUI | Verify lock timer and messaging |
| ST-Login-Web-Su | Web/Dashboard login success | LoginWindow, MainDashboard, LoginManager | Manual/GUI | Headless-friendly with Tk stubs if available |
| ST-Power-Cycle | Power on/off/reset flow | System, Alarm, SensorController, StorageManager | Automated | Persist/restore settings on reboot |
| ST-Mode-Stay-Away | Arm/disarm Stay vs Away across zones | System, ConfigurationManager, SensorController | Automated | Entry delay respected; zones armed correctly |
| ST-Intrusion-Delay-Alarm | Intrusion with entry delay leading to alarm | System, Alarm, SensorController | Automated | Countdown, alarm ring, monitoring call |
| ST-Panic | Panic button triggers immediate alarm | ControlPanel, System, Alarm | Automated/Manual | No delay; monitoring call made |
| ST-Zone-CRUD-UI | Create/edit/delete zones via UI | ZoneManagerWindow, ConfigurationManager | Manual/GUI | Sensor assignment updates stored config |
| ST-Sensor-Sim-Flow | Sensor simulator end-to-end state reflection | SafeHomeSensorTest, System, SensorController | Manual/GUI | UI reflects armed/open/motion states |
| ST-Camera-PTZ-View | Camera view and PTZ control | CameraMonitor, CameraController, SafeHomeCamera | Manual/GUI | Password prompt, PTZ actions, feed updates |
| ST-Camera-Lockout-Recover | Camera password lockout then timeout recovery | CameraController, SafeHomeCamera | Automated | Lock, wait, retry succeeds |
| ST-Config-Save-Load | Save configuration and reload on restart | ConfigurationManager, StorageManager | Automated | Modes/zones/sensors persist |
| ST-Logs-View-Clear | Log viewer shows and clears event logs | LogViewerWindow, LogManager, StorageManager | Manual/GUI | Auto-refresh toggle behavior |
| ST-Email-Alert-Failover | Email alert failure handling | ConfigurationManager | Automated | Failure logged, user notified |
| ST-Monitoring-Call | Monitoring service call on alarm | System | Automated/Manual | Stub external call; record parameters |
| ST-Logout-Session | Logout flow and session timeout | MainDashboard, LoginManager | Manual/GUI | Session cleared; controls disabled |
| ST-PreArm-Ready | Ready check blocks arming when entry points open | System, SensorController, ControlPanel | Automated | “Not Ready” gating before arming |
| ST-Guest-Login-Perm | Guest login limited permissions | LoginWindow, MainDashboard, LoginManager | Manual/GUI | Only allowed actions visible |
| ST-Pwd-Change-Alert | Password change triggers alert/email/log | System, LoginManager, ConfigurationManager | Automated | Alert logged; email attempt |
| ST-Alarm-Silence | Silence alarm then resume monitoring | System, Alarm, ControlPanel | Automated/Manual | Alarm stops sound; state consistent |
| ST-Power-Loss-Recover | Abrupt power loss and restart recovery | System, StorageManager | Automated | Restores last saved config |
| ST-Settings-UI-Persist | Update settings via UI and persist | MainDashboard, ConfigurationManager, StorageManager | Manual/GUI | Delays/durations saved and reloaded |
| ST-DB-Rollback-Recover | DB error triggers rollback without corruption | DatabaseManager, StorageManager | Automated | Rollback leaves data consistent |
| ST-Camera-Enable-Persist | Enable/disable camera persists and enforces access | CameraController, SafeHomeCamera | Automated/Manual | State and password gate persist |
| ST-Mode-Mapping-UI | Edit mode sensor mapping via UI and apply | MainDashboard, ConfigurationManager | Manual/GUI | Mapping persists and affects arming |
| ST-Log-Unseen-Retention | Unseen log counter, mark-seen, and clear | LogViewerWindow, LogManager, StorageManager | Manual/GUI | Unseen count updates correctly |
| ST-Backup-Fallback | Config save/load DB vs JSON fallback | ConfigurationManager, StorageManager, DatabaseManager | Automated | Uses JSON when DB unavailable |
| ST-Mixed-Zone-Intrusion | Intrusion in armed vs disarmed zones behaves correctly | System, SensorController, ConfigurationManager | Automated | Only armed zones trigger alarm |
| ST-Init-Schema-Defaults | First launch initializes DB schema and defaults | DatabaseManager, StorageManager, ConfigurationManager | Automated | Seeds default modes/zones/settings |
| ST-Alarm-Duration-Expiry | Alarm auto-stops after configured duration | System, Alarm | Automated | Duration honored without manual silence |
| ST-Session-Logging | Login sessions recorded and accessible | System, LoginManager, StorageManager | Automated/Manual | Session log entries viewable |
| ST-Factory-Reset | Factory reset clears config to defaults | System, ConfigurationManager, StorageManager | Automated | All zones/modes/users reset to baseline |

---

### ST-Login-CP-Su — Log onto the system through Control Panel (Success)
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| ControlPanel, SafeHomeControlPanel, System, LoginManager, StorageManager | Log onto the system through control panel | TBD | TBD |

**Test Case Description**  
Validate the successful login path and the ControlPanel display of available functions after authentication.

**Input Specifications**  
- ControlPanel receives button-press sequence "1234".  
- StorageManager contains master credentials ("1234").

**Detailed Step**
1. Seed StorageManager with the master user and password "1234" (if not already present). Reset login attempt counter.  
2. Initialize ControlPanel and simulate powering on the panel.  
3. Simulate button presses sequence of "1234".  
4. Verify that the system indicates successful login and the accessible function list is displayed.

**Expected Result**  
- SafeHomeSystem.login() returns success code for master.  
- ControlPanel transitions to LOGGED_IN state.  
- ControlPanel displays "Log In Success" followed by accessible functions message such as "2: Turn Off 3: Reset".

**Actual Result (Pass/Fail/Exception)**  
Pending (not executed yet).

**Comment (including references)**  
Sequence Diagram on ControlPanel, SafeHomeControlPanel, System, LoginManager, and StorageManager, page 47 of SDS.

---

### ST-Login-CP-Lock — Control Panel lockout after failed attempts
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| ControlPanel, SafeHomeControlPanel, System, LoginManager | Lockout on repeated failed PIN entry | TBD | TBD |

**Test Case Description**  
Validate that repeated wrong PIN entries trigger lockout, enforce timeout, and recover after cooldown.

**Input Specifications**  
- ControlPanel receives three consecutive wrong PINs (e.g., "9999").  
- Lockout duration configured to default (per SDS).

**Detailed Step**
1. Initialize system with master PIN "1234"; reset counters.  
2. Power on ControlPanel; enter wrong PIN three times.  
3. Observe lockout message/state; attempts beyond limit are blocked.  
4. Wait for lockout timeout; enter correct PIN "1234".  
5. Confirm login succeeds and counters reset.

**Expected Result**  
- After threshold, ControlPanel shows lockout message; LoginManager rejects inputs.  
- During lockout, further attempts are ignored/blocked.  
- After timeout, correct PIN logs in successfully and clears failed attempts.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS state/sequence for login lockout; LoginManager lock timer behavior.

---

### ST-Login-Web-Su — Dashboard login via desktop UI
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| LoginWindow, MainDashboard, LoginManager, StorageManager | Desktop login and dashboard launch | TBD | TBD |

**Test Case Description**  
Validate successful login from the desktop login window and transition to MainDashboard with correct permissions displayed.

**Input Specifications**  
- Stored user: master/"1234".  
- LoginWindow receives username "master" and password "1234".

**Detailed Step**
1. Seed credentials; start LoginWindow.  
2. Enter username/password; submit.  
3. Verify dashboard opens and header shows master user.  
4. Confirm control buttons reflect master permissions (arm/disarm/reset visible).

**Expected Result**  
- Login succeeds; dashboard main window created.  
- Permissions panel lists master actions.  
- No lockout or error dialogs shown.

**Actual Result (Pass/Fail/Exception)**  
Pending (GUI/manual or Tk stub).

**Comment (including references)**  
SDS: LoginWindow/MainDashboard sequence; permissions UI in SDS UI spec.

---

### ST-Power-Cycle — System power on/off/reset persistence
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| System, Alarm, SensorController, StorageManager | Power on/off/reset | TBD | TBD |

**Test Case Description**  
Validate that turning the system on/off and performing reset preserves or restores persisted configuration and leaves sensors in a safe default state.

**Input Specifications**  
- Existing configuration with zones, sensors, and Away mode.  
- Alarm initially inactive.

**Detailed Step**
1. Arm system in Away mode; ensure zones A/B armed.  
2. Call System.turn_off(); verify sensors disarmed and alarm stopped.  
3. Call System.turn_on(); configuration reloads.  
4. Call System.reset(); verify defaults restored (per SDS).  
5. Re-arm and confirm sensors resume polling.

**Expected Result**  
- turn_off disarms sensors, stops polling/alarm.  
- turn_on reloads stored settings (zones/modes).  
- reset restores factory defaults; subsequent arm works.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS System state diagram (power/reset), StorageManager persistence.

---

### ST-Mode-Stay-Away — Arm/disarm Stay vs Away across zones
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| System, ConfigurationManager, SensorController | Mode transitions and zone arming | TBD | TBD |

**Test Case Description**  
Validate that switching between Stay and Away arms the correct sensors per mode mapping and updates status displays.

**Input Specifications**  
- Mode mapping: Stay (perimeter only), Away (all sensors).  
- Two zones with mixed sensor types.

**Detailed Step**
1. Set mode to Stay; verify interior motion sensors remain disarmed, perimeter armed.  
2. Switch to Away; all sensors armed and polling started.  
3. Disarm; ensure all sensors disarmed.  
4. Repeat to confirm idempotence.

**Expected Result**  
- Mode change calls configure_mode_sensors correctly.  
- Sensor status reflects mode mapping; polling state matches.  
- No residual armed sensors after disarm.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS mode/state diagrams; ConfigurationManager mode mapping tables.

---

### ST-Intrusion-Delay-Alarm — Entry delay then alarm
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| System, Alarm, SensorController | Entry delay countdown and alarm trigger | TBD | TBD |

**Test Case Description**  
Validate intrusion handling with entry delay: countdown, optional disarm, otherwise alarm and monitoring call.

**Input Specifications**  
- Armed Away mode.  
- Entry delay configured (per SDS default).  
- Motion sensor detects intrusion.

**Detailed Step**
1. Arm system Away.  
2. Simulate motion sensor intrusion.  
3. Observe entry delay countdown; optionally disarm within window.  
4. If not disarmed, verify alarm rings and monitoring service called.  
5. Silence alarm; confirm status transitions to ALARMED then READY.

**Expected Result**  
- Countdown starts; display shows remaining time.  
- Disarm within window prevents alarm.  
- Otherwise Alarm.ring invoked; call_monitoring_service called once.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS sequence: sensor intrusion → entry delay → alarm → monitoring; Alarm state diagram.

---

### ST-Panic — Immediate panic alarm
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| ControlPanel, System, Alarm | Panic button handling | TBD | TBD |

**Test Case Description**  
Validate that pressing panic triggers immediate alarm without entry delay and invokes monitoring service.

**Input Specifications**  
- System powered on, any mode.  
- Panic button press event.

**Detailed Step**
1. Power on system; ensure disarmed.  
2. Trigger panic button (control panel or dashboard panic).  
3. Verify alarm rings immediately and monitoring service is called.  
4. Silence alarm; confirm status resets when acknowledged.

**Expected Result**  
- No delay; alarm active instantly.  
- Monitoring call includes panic reason.  
- System remains in panic state until cleared.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS panic flow; Alarm handling specs.

---

### ST-Zone-CRUD-UI — Manage zones via Zone Manager UI
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| ZoneManagerWindow, ConfigurationManager, SensorController | Create/edit/delete zones and assign sensors | TBD | TBD |

**Test Case Description**  
Validate zone lifecycle through the UI and persistence to storage, including sensor assignments and display refresh.

**Input Specifications**  
- Existing sensors inventory.  
- New zone name/desc input via dialog.

**Detailed Step**
1. Open ZoneManagerWindow from dashboard.  
2. Create zone with name/description; assign sensors.  
3. Edit zone name; reassign sensor.  
4. Delete zone; confirm removal and sensor unassignment.  
5. Restart app; verify persisted changes.

**Expected Result**  
- Zones appear in list; sensors mapped appropriately.  
- Edits persist; deletions remove mappings.  
- UI refresh reflects storage state.

**Actual Result (Pass/Fail/Exception)**  
Pending (GUI/manual).

**Comment (including references)**  
SDS UI flow for Zone Manager; ConfigurationManager zone CRUD; StorageManager persistence.

---

### ST-Sensor-Sim-Flow — Sensor simulator end-to-end reflection
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| SafeHomeSensorTest, System, SensorController | Simulated sensor states reflected in system/UI | TBD | TBD |

**Test Case Description**  
Validate that the sensor simulator updates sensor states and that these changes are reflected in system status and UI panels.

**Input Specifications**  
- Simulator inputs for window/door open/close and motion on/off.  
- System armed in Stay or Away.

**Detailed Step**
1. Open sensor simulator; arm system.  
2. Simulate window open; verify status indicates open and not ready/entry delay as appropriate.  
3. Simulate motion; verify alarm behavior per mode.  
4. Close sensors; confirm status returns to ready.  
5. Repeat for multiple zones.

**Expected Result**  
- UI shows live sensor status changes.  
- System readiness/alarm follows SDS rules per mode.  
- No stale states after closing sensors.

**Actual Result (Pass/Fail/Exception)**  
Pending (GUI/manual).

**Comment (including references)**  
SDS simulator UI; SensorController polling integration.

---

### ST-Camera-PTZ-View — Camera view and PTZ control via UI
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| CameraMonitor, CameraController, SafeHomeCamera | Live view, pan/tilt/zoom, enable/disable | TBD | TBD |

**Test Case Description**  
Validate that camera feeds display and PTZ commands from UI update camera state, respecting password protection.

**Input Specifications**  
- At least one camera configured with/without password.  
- PTZ button presses (left/right/up/down/zoom in/out).

**Detailed Step**
1. Launch camera monitor UI; select camera.  
2. If password set, enter correct password to unlock.  
3. Issue PTZ commands; observe state changes/feedback.  
4. Toggle enable/disable; verify feed availability.  
5. Attempt PTZ with wrong password to confirm denial.

**Expected Result**  
- Feed displays; PTZ commands acknowledged.  
- Password gate enforced; wrong password denied.  
- Disable hides/stops feed; enable restores.

**Actual Result (Pass/Fail/Exception)**  
Pending (GUI/manual; headless with stubs possible).

**Comment (including references)**  
SDS camera monitor UI; CameraController PTZ/password flows.

---

### ST-Camera-Lockout-Recover — Camera password lockout then recovery
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| CameraController, SafeHomeCamera | Password attempts, lockout, timeout recovery | TBD | TBD |

**Test Case Description**  
Validate that repeated wrong camera passwords trigger lockout and that access is restored after timeout.

**Input Specifications**  
- Camera password set.  
- Lockout threshold and timeout default from SDS.

**Detailed Step**
1. Attempt to view camera with wrong password until lockout.  
2. Verify further attempts blocked; lockout status shown.  
3. Wait timeout duration.  
4. Enter correct password; confirm access restored and status cleared.

**Expected Result**  
- Lockout enforced after threshold.  
- During lockout, access denied.  
- After timeout, correct password works; lockout counter resets.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
CameraController lockout logic; SDS camera access sequence.

---

### ST-Config-Save-Load — Save configuration and reload on restart
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| ConfigurationManager, StorageManager | Save/load settings (DB/JSON) | TBD | TBD |

**Test Case Description**  
Validate that configuration changes (modes, zones, sensors) are saved and restored after application restart.

**Input Specifications**  
- Configuration changes (new zone, mode sensor mapping).  
- Storage targets (DB or JSON per settings).

**Detailed Step**
1. Modify mode sensor mapping and add a zone.  
2. Save configuration.  
3. Shutdown system/application.  
4. Restart; load configuration.  
5. Verify changes persist and sensors map correctly.

**Expected Result**  
- save_configuration persists modes/zones/sensors.  
- restart/load restores the same structures.  
- No data loss or mismatch.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS configuration persistence; StorageManager save/load flows.

---

### ST-Logs-View-Clear — View and clear event logs via UI
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| LogViewerWindow, LogManager, StorageManager | Display and clear logs | TBD | TBD |

**Test Case Description**  
Validate that logs are displayed in the UI with auto-refresh and that clearing logs removes them from storage and UI.

**Input Specifications**  
- Pre-seeded event logs (intrusion, login).  
- Auto-refresh toggle input.

**Detailed Step**
1. Open LogViewerWindow; enable auto-refresh.  
2. Trigger an event (e.g., login success).  
3. Confirm new log appears without manual refresh.  
4. Click clear logs; confirm UI empties and storage cleared.  
5. Reopen viewer to ensure logs remain cleared.

**Expected Result**  
- Logs list matches storage; auto-refresh updates live.  
- Clear action deletes logs and UI reflects empty state.  
- No stale entries after reopen.

**Actual Result (Pass/Fail/Exception)**  
Pending (GUI/manual).

**Comment (including references)**  
SDS log viewer UI; LogManager clear/get flows.

---

### ST-Email-Alert-Failover — Email alert failure handling
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| ConfigurationManager | send_email_alert failover | TBD | TBD |

**Test Case Description**  
Validate that when email sending fails, the system logs the failure and surfaces a user-facing notice without crashing.

**Input Specifications**  
- Invalid SMTP configuration or simulated exception.  
- Trigger condition (alarm or password change).

**Detailed Step**
1. Configure invalid SMTP or mock send_email_alert to raise.  
2. Trigger an alert condition (e.g., password change).  
3. Observe behavior and logs.  
4. Ensure system continues operating; user notification recorded.

**Expected Result**  
- Failure logged via LogManager/storage.  
- User-facing warning shown (UI or log).  
- No crash; subsequent alerts still attempt send.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS external comms; email alert sequence.

---

### ST-Monitoring-Call — Monitoring service call on alarm
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| System | call_monitoring_service invocation | TBD | TBD |

**Test Case Description**  
Validate that alarm conditions invoke call_monitoring_service with correct parameters and that failures are handled gracefully.

**Input Specifications**  
- Alarm triggered (intrusion or panic).  
- Monitoring endpoint stubbed/mocked.

**Detailed Step**
1. Arm system; trigger intrusion to raise alarm.  
2. Capture monitoring call parameters.  
3. Simulate monitoring call failure; ensure retry or log per SDS.  
4. Silence alarm; ensure no duplicate extraneous calls.

**Expected Result**  
- call_monitoring_service invoked once per alarm event.  
- Failures logged; system remains stable.  
- No spurious calls after alarm cleared.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS external monitoring sequence.

---

### ST-Logout-Session — Logout flow and session timeout
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| MainDashboard, LoginManager, System | Logout/session clearance | TBD | TBD |

**Test Case Description**  
Validate that logout (manual or timeout) closes privileged UI, clears session, and requires re-authentication.

**Input Specifications**  
- Active master session.  
- Optional inactivity timeout per settings.

**Detailed Step**
1. Log in to dashboard as master.  
2. Invoke logout; confirm return to login screen.  
3. Attempt privileged action; verify blocked.  
4. (Optional) Wait for timeout; ensure auto-logout occurs.  
5. Re-login to confirm normal behavior.

**Expected Result**  
- Session cleared; privileged actions disabled post-logout.  
- Timeout triggers auto-logout if configured.  
- Re-login restores access without stale state.

**Actual Result (Pass/Fail/Exception)**  
Pending (GUI/manual).

**Comment (including references)**  
SDS session management; UI navigation flow.

---

### ST-PreArm-Ready — Ready check blocks arming when entry points open
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| System, SensorController, ControlPanel | Ready/not-ready gating before arming | TBD | TBD |

**Test Case Description**  
Validate that arming is blocked when any entry sensor is open and that status transitions to READY once all are closed.

**Input Specifications**  
- Zone with window/door sensors; one starts open.  
- ControlPanel arm command (Stay/Away).

**Detailed Step**
1. Ensure one door sensor reports open.  
2. Attempt to arm Stay; verify “Not Ready” shown and arming rejected.  
3. Close sensor; wait for status refresh.  
4. Arm Stay again; confirm success and sensors armed.  
5. Disarm to return to idle.

**Expected Result**  
- Arming rejected while any entry sensor open; “Not Ready” displayed.  
- After closing, arming succeeds and status becomes ARMED.  
- No partial arming occurs while not ready.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS ready/arm state diagram; SensorController readiness check.

---

### ST-Guest-Login-Perm — Guest login limited permissions
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| LoginWindow, MainDashboard, LoginManager | Guest access scope | TBD | TBD |

**Test Case Description**  
Validate that guest login succeeds but only exposes guest-allowed actions (e.g., view status, arm Stay) and hides restricted controls (password change, mode edits).

**Input Specifications**  
- Guest credentials provisioned (username/password).  
- Dashboard launched via LoginWindow.

**Detailed Step**
1. Seed guest account; open LoginWindow.  
2. Log in as guest.  
3. Inspect dashboard controls/menus.  
4. Attempt restricted action (e.g., change password or edit zones).  
5. Attempt allowed action (arm Stay) and logout.

**Expected Result**  
- Login succeeds; dashboard shows guest identity.  
- Restricted controls hidden/disabled; attempts blocked with message.  
- Allowed actions (arm Stay) succeed; logout works.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS permissions matrix; MainDashboard UI permissions build.

---

### ST-Pwd-Change-Alert — Password change triggers alert/email/log
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| System, LoginManager, ConfigurationManager | Password change notification | TBD | TBD |

**Test Case Description**  
Validate that changing a password updates credentials, logs the event, and attempts to send an email alert.

**Input Specifications**  
- Existing master account; SMTP configured (or mocked).  
- New password input.

**Detailed Step**
1. Log in as master.  
2. Invoke password change to a new value.  
3. Verify credentials updated by re-login with new password.  
4. Check log entries for password change.  
5. If email configured, confirm send attempt or logged failure.

**Expected Result**  
- Password updated and old password rejected.  
- Log entry recorded.  
- Email alert attempted; failures logged gracefully.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS password management flow; ConfigurationManager email alert behavior.

---

### ST-Alarm-Silence — Silence alarm then resume monitoring
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| System, Alarm, ControlPanel | Alarm silence/acknowledge | TBD | TBD |

**Test Case Description**  
Validate that silencing an active alarm stops ringing while keeping system state consistent, allowing re-arm or disarm per SDS.

**Input Specifications**  
- Armed system; intrusion triggers alarm.  
- Silence command via panel/dashboard.

**Detailed Step**
1. Arm Away; trigger intrusion to start alarm.  
2. Issue silence command.  
3. Verify alarm sound stops and status reflects silenced/acknowledged.  
4. Disarm system; confirm alarm cleared.  
5. Re-arm to ensure normal operation resumes.

**Expected Result**  
- Alarm.ring stops upon silence; no further sound.  
- System tracks alarm as handled; monitoring call already made once.  
- Subsequent arm/disarm works without stuck alarm state.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS alarm handling/state diagram; control panel silence flow.

---

### ST-Power-Loss-Recover — Abrupt power loss and restart recovery
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| System, StorageManager | Power loss and recovery | TBD | TBD |

**Test Case Description**  
Validate that an unexpected shutdown preserves persisted settings and that restart returns the system to a consistent ready state.

**Input Specifications**  
- Configured zones/modes; system armed or disarmed state recorded.  
- Simulated abrupt stop (no graceful shutdown).

**Detailed Step**
1. Configure system (zones, mode) and arm/disarm as desired.  
2. Simulate abrupt power loss (terminate process).  
3. Restart application.  
4. Verify configuration and last saved status reloaded.  
5. Check that sensors/alarm are in safe default before re-arming.

**Expected Result**  
- Persisted config intact; no corruption.  
- System boots to READY/SAFE state; no spurious alarms.  
- Re-arming works using restored config.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS power recovery; StorageManager persistence behavior.

---

### ST-Settings-UI-Persist — Update settings via UI and persist
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| MainDashboard, ConfigurationManager, StorageManager | Settings edit/persist | TBD | TBD |

**Test Case Description**  
Validate that changing settings (entry delay, alarm duration, email config) via UI saves to storage and takes effect after restart.

**Input Specifications**  
- New settings values entered in Settings dialog.  
- Storage backend (DB/JSON).

**Detailed Step**
1. Open Settings UI from dashboard.  
2. Change entry delay, alarm duration, and email sender settings.  
3. Save; observe confirmation.  
4. Restart application.  
5. Trigger behaviors to confirm new settings applied (e.g., entry delay length).

**Expected Result**  
- Settings saved without error.  
- Restart loads new values.  
- System behavior reflects updated settings.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS settings management; ConfigurationManager/StorageManager save/load.

---

### ST-DB-Rollback-Recover — DB error triggers rollback without corruption
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| DatabaseManager, StorageManager | Transaction rollback | TBD | TBD |

**Test Case Description**  
Validate that a database error during a multi-step operation triggers rollback and leaves data consistent.

**Input Specifications**  
- Operation that spans multiple statements (e.g., save mode + sensors).  
- Simulated DB failure on second statement.

**Detailed Step**
1. Begin save operation (mode with sensor mappings).  
2. Inject DB error during second statement (mock/patch).  
3. Verify rollback executed.  
4. Reload data to confirm no partial writes.  
5. Retry operation successfully.

**Expected Result**  
- Commit not applied; changes absent after failure.  
- System logs error but remains stable.  
- Subsequent retry succeeds and persists cleanly.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS database transaction handling; rollback/commit paths.

---

### ST-Camera-Enable-Persist — Enable/disable camera persists and enforces access
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| CameraController, SafeHomeCamera | Camera enable/disable persistence | TBD | TBD |

**Test Case Description**  
Validate that disabling a camera blocks viewing/PTZ, state is persisted, and re-enabling restores access with password enforcement.

**Input Specifications**  
- Camera with password set.  
- Enable/disable actions via UI or API.

**Detailed Step**
1. Disable camera; attempt to view or PTZ.  
2. Verify access denied.  
3. Restart application.  
4. Confirm camera remains disabled.  
5. Re-enable; enter correct password; verify view/PTZ restored.

**Expected Result**  
- Disabled cameras cannot be viewed/controlled.  
- State persists across restart.  
- Re-enable plus correct password restores normal access.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS camera management; CameraController enable/disable and persistence flow.

---

---

### ST-Mode-Mapping-UI — Edit mode sensor mapping via UI and apply
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| MainDashboard, ConfigurationManager | Mode sensor mapping edit/apply | TBD | TBD |

**Test Case Description**  
Validate that editing the mode-to-sensor mapping from the UI is persisted and affects subsequent arming behavior.

**Input Specifications**  
- Existing modes Stay/Away.  
- UI action to include/exclude specific sensors from Stay.

**Detailed Step**
1. Open mode configuration in dashboard.  
2. Change Stay mapping to include a motion sensor previously excluded.  
3. Save configuration.  
4. Arm Stay; verify the motion sensor is now armed/polled.  
5. Disarm; restart app; re-arm Stay to confirm persistence.

**Expected Result**  
- Mapping change saved without error.  
- Stay mode arms newly included sensor.  
- After restart, mapping still applied.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS mode mapping UI/logic; ConfigurationManager.configure_mode_sensors.

---

### ST-Log-Unseen-Retention — Unseen log counter, mark-seen, and clear
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| LogViewerWindow, LogManager, StorageManager | Unseen log handling | TBD | TBD |

**Test Case Description**  
Validate that unseen log counts increment on new events, decrease on mark-seen, and reset on clear, with UI in sync.

**Input Specifications**  
- New event logs generated (login, intrusion).  
- User opens log viewer and marks seen/clear.

**Detailed Step**
1. Trigger two events; check unseen count increases.  
2. Open LogViewerWindow; verify unseen badge matches storage.  
3. Mark logs as seen; confirm count drops to zero.  
4. Trigger another event; unseen increments again.  
5. Clear logs; unseen and list empty.

**Expected Result**  
- Unseen count tracks new events.  
- Mark-seen updates storage and UI.  
- Clear removes logs and unseen count resets.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS logging requirements; StorageManager get_unseen_logs/mark_logs_seen/clear_logs.

---

### ST-Backup-Fallback — Config save/load DB vs JSON fallback
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| ConfigurationManager, StorageManager, DatabaseManager | Persistence fallback | TBD | TBD |

**Test Case Description**  
Validate that when the DB is unavailable, configuration save/load falls back to JSON (or alternate store) without data loss.

**Input Specifications**  
- Config changes (zones/modes/sensors).  
- Simulated DB offline condition.

**Detailed Step**
1. Apply config changes.  
2. Simulate DB offline (connection failure).  
3. Save configuration; verify JSON fallback used.  
4. Restart with DB still offline; load config from fallback.  
5. Restore DB; save/load resumes to DB with data intact.

**Expected Result**  
- Save does not crash; writes to fallback store.  
- Load restores full config from fallback when DB down.  
- When DB returns, data preserved and sync resumes.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS persistence strategy; StorageManager save/load to DB/JSON.

---

### ST-Mixed-Zone-Intrusion — Intrusion in armed vs disarmed zones behaves correctly
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| System, SensorController, ConfigurationManager | Zone-specific arming effects | TBD | TBD |

**Test Case Description**  
Validate that only armed zones trigger entry delay/alarm while disarmed zones do not, even when sensors fire concurrently.

**Input Specifications**  
- Two zones: Zone A armed, Zone B disarmed.  
- Motion/door sensors in each zone.

**Detailed Step**
1. Arm system; arm Zone A only, leave Zone B disarmed.  
2. Trigger sensor in Zone B; verify no alarm/countdown.  
3. Trigger sensor in Zone A; verify entry delay/alarm path.  
4. Disarm; confirm status resets.  
5. Swap zones (arm B, disarm A) and repeat.

**Expected Result**  
- Disarmed zone events do not alarm.  
- Armed zone events follow delay/alarm rules.  
- Zone-specific arming respected consistently.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS multi-zone arming; System._get_sensors_for_mode and zone arming logic.

---

---

### ST-Init-Schema-Defaults — First launch initializes DB schema and defaults
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| DatabaseManager, StorageManager, ConfigurationManager | Initialize schema and seed defaults | TBD | TBD |

**Test Case Description**  
Validate that on a clean install the database schema is created and default data (modes, master credentials, baseline settings) are seeded without manual intervention.

**Input Specifications**  
- No existing database file (delete or use temp path).  
- Application first launch/startup.

**Detailed Step**
1. Remove existing DB or point to fresh DB path.  
2. Launch application/system initialization.  
3. Inspect DB schema tables existence.  
4. Verify default records: master user, default modes (Stay/Away), base settings.  
5. Log in with default credentials to confirm usability.

**Expected Result**  
- Schema created without errors.  
- Default data present.  
- Login with default credentials succeeds.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS installation/initialization requirements; DatabaseManager.initialize_schema.

---

### ST-Alarm-Duration-Expiry — Alarm auto-stops after configured duration
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| System, Alarm | Alarm duration enforcement | TBD | TBD |

**Test Case Description**  
Validate that an active alarm automatically stops after the configured duration if not silenced manually, and the system transitions to the correct post-alarm state.

**Input Specifications**  
- Armed system; intrusion triggers alarm.  
- Alarm duration configured (e.g., 30s).

**Detailed Step**
1. Arm system Away.  
2. Trigger intrusion to start alarm.  
3. Do not silence; wait for configured duration.  
4. Confirm alarm stops automatically.  
5. Verify system state transitions to ALARMED/READY per SDS and allows re-arm.

**Expected Result**  
- Alarm rings for configured duration then stops.  
- No further monitoring calls after stop.  
- System remains stable and can be disarmed/re-armed.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS Alarm duration setting; Alarm.set_duration behavior.

---

### ST-Session-Logging — Login sessions recorded and accessible
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| System, LoginManager, StorageManager | Session logging and retrieval | TBD | TBD |

**Test Case Description**  
Validate that each login/logout (and lock/unlock) creates session log entries that can be retrieved and viewed via UI or storage.

**Input Specifications**  
- Master and guest accounts.  
- Multiple login/logout attempts, including failed attempts triggering lock.

**Detailed Step**
1. Log in as master; perform actions; log out.  
2. Log in as guest; log out.  
3. Trigger failed logins to cause lock, then unlock.  
4. Retrieve session logs (StorageManager/get logs or UI).  
5. Verify entries for each session with correct user, timestamps, lock events.

**Expected Result**  
- Session entries recorded for login/logout and lock/unlock.  
- Data persisted and viewable.  
- No duplicate or missing entries.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS logging requirements; LoginManager _log_session and lock handling.

---

### ST-Factory-Reset — Factory reset clears config to defaults
| Class/Modules | Function/Feature | Author | Date |
| --- | --- | --- | --- |
| System, ConfigurationManager, StorageManager | Factory reset | TBD | TBD |

**Test Case Description**  
Validate that invoking factory reset wipes custom zones/modes/users/settings and restores baseline defaults without leaving residual data.

**Input Specifications**  
- Customized configuration: additional zones, modified modes, custom passwords.  
- Factory reset command (UI or API).

**Detailed Step**
1. Create custom zones/mappings and change passwords/settings.  
2. Invoke factory reset.  
3. Inspect storage/DB to confirm defaults restored and customs removed.  
4. Attempt login with old custom creds (should fail) and default creds (should succeed).  
5. Re-open UI to confirm only baseline configuration exists.

**Expected Result**  
- All custom data removed; defaults restored.  
- Default credentials work; custom ones rejected.  
- No orphaned sensors/zones remain.

**Actual Result (Pass/Fail/Exception)**  
Pending.

**Comment (including references)**  
SDS reset requirements; ConfigurationManager reset_configuration; System.reset.

---
