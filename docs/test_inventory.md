# SafeHome Test Inventory (per SDS/SRS mapping)
이 문서는 템플릿의 모듈 구분(External Communication → Control Panel/Web, Surveillance, Security, Configuration/Data)에 맞춰 SafeHome 코드의 클래스/함수를 매핑하고, 각 기능이 근거하는 SDS 시퀀스/상태/클래스 다이어그램 페이지를 함께 적어 테스트 설계 시 참조할 수 있도록 정리한 목록입니다. pytest/coverage 환경은 `python -m pytest`, `coverage run --branch -m pytest` 기준으로 설정합니다.

## External Communication Management
### Control Panel Management
- `safehome/interface/control_panel/DeviceControlPanelAbstract`: Tk GUI 버튼/LED/LCD 표시자. 버튼 이벤트 훅 `button0..button9`, `button_star`, `button_sharp`, `button_panic`가 상속 대상으로 제공. (SDS Common seq: 로그인 p47, Turn on p50, Turn off p52, Reset p53)
- `SafeHomeControlPanel`: 실제 CP 로직.  
  - 입력 처리: `_handle_key_input`, `_handle_command`, `_attempt_login`, `_attempt_change_password`, `_reset_interaction`, `_refresh_status_display`.  
  - 버튼 이벤트: `button0..button9`, `button_star`, `button_sharp`, `button_panic`.  
  - 시스템 연계: `system.login`, `system.arm_system`, `system.disarm_system`, `system.change_password`, `system.config.next_zone()`(미구현 주의), `system.alarm.ring`.  
  - SDS 근거: Common seq “Log onto the system through control panel” p47, “Turn the system on” p50, “Change master password through control panel” p54, Security seq “Arm/disarm system through control panel” p55, “Call monitoring service through control panel” p65, Alarm condition p58.

### Dashboard / (Web Interface 대체)
- `safehome/interface/dashboard/LoginWindow`: 로그인 UI, `LoginWindow._attempt_login` → `system.login("admin"/"guest", pwd, "CONTROL_PANEL")`. (SDS Common seq: p47 로그온)  
- `safehome/interface/dashboard/MainDashboard`: 대시보드/운영 인터페이스.  
  - 초기화/루프: `_update_loop` (주기적 상태/카메라 갱신), `_on_close`.  
  - 권한 설정: `_build_permissions`.  
  - 카메라 영역: `_create_camera_section`, `refresh_cameras`, `open_camera_password_prompt`, `handle_camera_action` (PTZ/zoom), uses `system.camera_controller.get_camera_view/pan/tilt/zoom/set_password`.  
  - 센서/존: `_create_sensor_section`, `_update_sensors`, `_update_zones`, `_create_zone_section`, `prompt_zone_add/update/delete`, calls `system.config` zone CRUD + `sensor_controller`.  
  - 시스템 제어: `_create_quick_actions`, `_arm_mode`, `_panic`, `_open_settings` (entry delay 등).  
  - 로그 뷰/센서 시뮬레이터: `_open_log_viewer`, `_open_sensor_simulator`.  
  - SDS 근거: Common seq p47(로그인), p49(Configure system setting), Security seq p55(Arm/disarm), p59~63(Configure/Create/Delete/Update zone, Configure modes), p64(View intrusion log), Surveillance seq p66~73(카메라 뷰/ PTZ/비밀번호/enable/disable).

### Tools
- `safehome/interface/tools/sensor_simulator.SafeHomeSensorTest`: 시뮬레이터 UI, `DeviceSensorTester`와 연동해 센서 상태를 수동 전환. 테스트 시 센서 하드웨어 모사에 사용. (지원 시 SDS seq p58 알람 조건/ p59~63 존 구성 영향 확인)

## Surveillance (Camera)
- `safehome/device/camera/CameraController`:  
  - CRUD: `add_camera`, `remove_camera`, `load_cameras_from_storage`, `get_camera`, `get_all_cameras`.  
  - Access/controls: `get_camera_view`, `pan_camera`, `tilt_camera`, `zoom_camera`, `enable_camera`, `disable_camera`, `set_camera_password`, `delete_camera_password`, `get_camera_status`, `get_all_camera_statuses`, `shutdown`.  
  - SDS 근거: Surveillance seq p66(뷰), p67(Pan/Zoom), p68(Set password), p69(Delete password), p72(enable), p73(disable), p71(thumbnail analog).  
- `CameraAccessGuard`: `require_access` 비밀번호/락 검증 헬퍼 (camera password/lockout).  
- `SafeHomeCamera`:  
  - 뷰/조작: `get_view`, `pan_left/right`, `tilt_up/down`, `zoom_in/out`.  
  - 보안: `set_password`, `verify_password`, `has_password`, `is_locked`, lockout 관리(`failed_attempts`, `locked_until`).  
  - 전원/상태: `enable`, `disable`, `get_status`, `stop`.  
  - SDS 근거: Surveillance state diagrams p38(SafeHomeCamera), seq p66~69, p72~73.  
- `DeviceCamera`: 하드웨어 시뮬레이터, `set_id`, `get_view`, PTZ/zoom, `stop`. (하드웨어 계층; 화이트박스 테스트 시 mock/patch 대상)

## Security (Sensors + Alarm)
- `safehome/device/sensor/SensorController`:  
  - CRUD/로드: `add_sensor`, `remove_sensor`, `load_sensors_from_storage`, `get_sensor`, `get_all_sensors`, `get_sensors_by_zone/type`.  
  - 무장/해제: `arm_sensor`, `disarm_sensor`, `arm_sensors_in_zone`, `disarm_sensors_in_zone`, `arm_sensors`, `disarm_all_sensors`.  
  - 상태/검출: `poll_sensors`(주기폴링), `check_all_windoor_closed`, `get_sensor_status`, `get_all_sensor_statuses`.  
  - SDS 근거: State diagrams p35~42 (SensorController p40, Sensor p39, MotionSensor p37, WindowDoorSensor p42), Security seq p55~58(arm/disarm, alarm condition), p59~63(zone/mode), p65(monitoring).  
- `Sensor` (abstract): 공통 인터페이스 `read`, `arm`, `disarm`, `test_armed_state`, `get_status`.  
- `WindowDoorSensor`: `read`, `arm/disarm`, `test_armed_state`, `is_open`, `simulate_open/close`.  
- `MotionSensor`: `read`, `arm/disarm`, `test_armed_state`, `is_motion_detected`, `simulate_motion/clear`.  
- `DeviceMotionDetector`, `DeviceWinDoorSensor`: 하드웨어 시뮬레이션, `read`, `arm/disarm`, `intrude/release`, `test_armed_state`.  
- `safehome/device/alarm/Alarm`: `ring`, `stop`, `_ring_for_duration`, `is_active`, `set_duration`, `get_duration`, `get_status`.  
  - SDS 근거: Alarm state diagram p35, Security seq p58(알람 조건), Common seq p65(모니터링 서비스 호출).

## Configuration and Data Management
- `safehome/configuration/ConfigurationManager`:  
  - 초기화/리셋: `__init__`, `reset_configuration`, `shutdown`.  
  - 모드: `set_mode`, `get_mode`, `get_safehome_modes`, `configure_mode_sensors`, `get_sensors_for_mode`.  
  - 존: `get_all_safety_zones/get_all_zones`, `get_safety_zone`, `add_safety_zone`, `update_safety_zone`, `delete_safety_zone`, callbacks `register_zone_update_callback`, `_notify_zone_update`.  
  - 설정/저장: `save_configuration`, `send_email_alert`.  
  - SDS 근거: Architectural p12, Class diagrams p13~15, State diagrams p26(ConfMgr), p33(StorageMgr), p34(SystemSettings), p31(SafetyZone), Seq p49(Configure settings), p59~63(zone/mode), p53(reset).  
- `SystemSettings`: 데이터 홀더, `update_settings`, `to_dict`. (SDS state p34)  
- `SafeHomeMode` (enum): `get_db_mode_name`, `from_db_mode_name`. (State p32)  
- `SafetyZone`: `add_sensor/remove_sensor`, `get_sensors`, `arm/disarm`, `to_dict`. (State p31)  
- `StorageManager`:  
  - 설정: `save_settings`, `load_settings`, DB/JSON 저장/로드.  
  - 존: `save_safety_zone`, `load_all_safety_zones`, `load_safety_zone_by_id`, `delete_safety_zone`, `delete_all_safety_zones`.  
  - 센서/카메라: `save_sensor`, `load_all_sensors`, `delete_sensor`; `save_camera`, `load_all_cameras`, `delete_camera`, `update_camera_password`, `clear_camera_passwords`.  
  - 로그: `save_log`, `get_logs`, `get_unseen_logs`, `mark_logs_seen`, `clear_logs`.  
  - 모드 매핑: `get_sensors_for_mode`, `save_mode_sensor_mapping`.  
  - SDS state p33(StorageManager), seq p59~63(존/모드), p66~73(카메라 비밀번호/enable/disable), p64(로그).  
- `LoginManager`:  
  - 인증: `validate_credentials` (CONTROL_PANEL/WEB), `_validate_control_panel`, `_validate_web`.  
  - 비밀번호 변경: `change_password`, `change_guest_password`.  
  - 잠금: `_lock_interface`, `unlock_system`, `is_interface_locked`, `get_failed_attempts`.  
  - 세션 로깅: `_log_session`.  
  - SDS state p29~30(LoginInterface/LoginManager), seq p47(pwd login), p54(change master password), p48(web login), p65(lock/unlock timing via SystemSettings.system_lock_time).  
- `LogManager` + `Log`: `add_log`, `get_recent_logs`, `get_all_logs`, `clear_logs`; `Log.__str__`, `event_type`. (State p27~28 Log/LogManager, seq p64 intrusion log)  
- `DatabaseManager`: 연결/스키마/쿼리, CRUD 헬퍼 (`connect`, `initialize_schema`, `execute_query/insert`, `get_system_settings`, `get_safety_zones`, `get_safehome_modes`, `get_sensors`, `get_cameras`, `add_event_log`, `get_event_logs`, `clear_event_logs`). (Architectural p12, state p33 StorageMgr backend)

## Core Orchestration
- `safehome/core/System`:  
  - 전원/상태: `turn_on`, `turn_off`, `_start_sensor_polling`, `_stop_sensor_polling`, `_sensor_polling_loop`.  
  - 보안 이벤트: `_handle_intrusion`, `_start_entry_delay_countdown`, `_trigger_alarm`, `call_monitoring_service`.  
  - 모드/존: `arm_system`, `disarm_system`, `arm_zone`, `disarm_zone`, `_get_sensors_for_mode`.  
  - 인증: `login`, `change_password`, `_send_password_change_alert`.  
  - 조회: `get_system_status`, `__repr__`.  
  - SDS class/state p41(System), seq p47(로그인), p50/52/53(on/off/reset), p55(arm/disarm), p58(알람), p65(모니터링 서비스), p49(설정 저장).  
- `main.py`: 시스템 부트스트랩, `setup_hardware`(기본 센서/카메라 구성), `main`(GUI 시작). Seq 근거: p50 Turn on, p52 Turn off, p53 Reset, Security/Surveillance flows.

## Environment readiness
- Python: 3.12.4 (`python3 -V` 확인).  
- PyPI tools: `pytest 7.4.4`, `coverage 7.12.0` 설치됨.  
- Pytest import 경로: 루트에서 `python -m pytest` 사용; `tests/__init__.py` 추가로 패키지 경로 안정화.  
- 커버리지 실행 예시:  
  - `coverage run --branch -m pytest`  
  - `coverage report -m` (파일/클래스/메서드별 수치 템플릿 표에 기입)  
  - `coverage html` (필요 시 htmlcov/index.html 확인)
