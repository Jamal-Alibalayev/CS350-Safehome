# SafeHome 프로젝트 구현 가이드

## 📋 프로젝트 개요

### SRS & SDS 분석 요약

**SafeHome**은 가정용 보안 자동화 시스템으로, 다음 핵심 기능을 제공합니다:

1. **Security Functions (보안 기능)**
    - Arm/Disarm 시스템 (Control Panel & Web)
    - Safety Zone 관리 (Zone별 센서 그룹화)
    - Sensor 관리 (Window/Door, Motion Detector)
    - Alarm 처리 및 Monitoring Service 호출
    - Intrusion Log 관리

2. **Surveillance Functions (감시 기능)**
    - Camera 모니터링 (실시간 View)
    - Camera Pan/Zoom 제어
    - Camera Password 보호
    - Thumbnail/Floor Plan 뷰
    - Camera Enable/Disable

3. **Configuration Functions (설정 기능)**
    - System Settings (delay time, passwords, phone numbers)
    - Login 관리 (Master/Guest password)
    - Log 관리
    - Safety Zone 설정

---

## 🏗️ 권장 프로젝트 구조

SDS의 Architectural Structure를 기반으로 한 Python 프로젝트 구조:

```
safehome_project/
│
├── safehome/                          # 메인 패키지
│   │
│   ├── __init__.py
│   │
│   ├── configuration/                 # Configuration & Data Management
│   │   ├── __init__.py
│   │   ├── configuration_manager.py   # Facade 패턴 (중앙 관리)
│   │   ├── system_settings.py         # 시스템 설정 데이터 클래스
│   │   ├── storage_manager.py         # DB 접근 관리
│   │   ├── login_manager.py           # 로그인 관리
│   │   ├── login_interface.py         # 로그인 인터페이스 (추상)
│   │   ├── log_manager.py             # 로그 관리
│   │   ├── log.py                     # 로그 데이터 클래스
│   │   ├── safety_zone.py             # Safety Zone 클래스
│   │   └── safehome_mode.py           # SafeHome Mode (Enum)
│   │
│   ├── device/                        # Device Layer (Hardware 연동)
│   │   ├── __init__.py
│   │   │
│   │   ├── sensor/                    # Sensor 관련
│   │   │   ├── __init__.py
│   │   │   ├── sensor_controller.py   # Sensor 컨트롤러
│   │   │   ├── sensor.py              # 추상 Sensor 클래스
│   │   │   ├── motion_sensor.py       # Motion Sensor (wraps DeviceMotionDetector)
│   │   │   ├── windoor_sensor.py      # Window/Door Sensor (wraps DeviceWinDoorSensor)
│   │   │   ├── interface_sensor.py    # Sensor 인터페이스
│   │   │   ├── device_windoor_sensor.py    # (교수님 제공 API)
│   │   │   ├── device_motion_detector.py   # (교수님 제공 API)
│   │   │   ├── device_sensor_tester.py     # (교수님 제공 API)
│   │   │   ├── safehome_sensor_test.py     # (교수님 제공 API)
│   │   │   └── safehome_sensor_test_gui.py # (교수님 제공 API)
│   │   │
│   │   ├── camera/                    # Camera 관련
│   │   │   ├── __init__.py
│   │   │   ├── camera_controller.py   # Camera 컨트롤러
│   │   │   ├── safehome_camera.py     # SafeHome Camera 래퍼 클래스
│   │   │   ├── interface_camera.py    # Camera 인터페이스
│   │   │   └── device_camera.py       # (교수님 제공 API)
│   │   │
│   │   └── alarm/                     # Alarm 관련
│   │       ├── __init__.py
│   │       ├── alarm.py               # Alarm 클래스 (하드웨어 드라이버)
│   │       └── alarm_controller.py    # Alarm 컨트롤러 (옵션)
│   │
│   ├── core/                          # Core System Layer
│   │   ├── __init__.py
│   │   ├── system.py                  # Main System 클래스 (핵심 로직)
│   │   └── event_handler.py           # Event 처리 (옵션)
│   │
│   ├── interface/                     # User Interface Layer
│   │   ├── __init__.py
│   │   │
│   │   ├── control_panel/             # Control Panel (Tkinter GUI)
│   │   │   ├── __init__.py
│   │   │   ├── safehome_control_panel.py          # 실제 구현
│   │   │   ├── device_control_panel_abstract.py   # (교수님 제공 API)
│   │   │   └── camera_monitor.py                  # Camera 모니터 윈도우
│   │   │
│   │   └── web/                       # Web Interface (향후 확장용)
│   │       ├── __init__.py
│   │       ├── web_interface.py       # Web Interface 메인
│   │       ├── page.py                # 페이지 추상 클래스
│   │       ├── device_icon.py         # Device 아이콘 표현
│   │       ├── floor_plan.py          # Floor Plan 표현
│   │       └── pages/                 # 각종 페이지들
│   │           ├── __init__.py
│   │           ├── login_page.py
│   │           ├── main_page.py
│   │           ├── security_page.py
│   │           └── surveillance_page.py
│   │
│   └── database/                      # Database Layer
│       ├── __init__.py
│       ├── db_manager.py              # SQLite3 DB 관리
│       ├── models.py                  # DB 모델 정의 (ORM 스타일)
│       └── schema.sql                 # DB 스키마 정의
│
├── tests/                             # 테스트 코드 (나중에)
│   ├── __init__.py
│   ├── test_configuration.py
│   ├── test_sensor.py
│   ├── test_camera.py
│   └── test_system.py
│
├── data/                              # 데이터 파일
│   ├── safehome.db                    # SQLite3 데이터베이스
│   ├── safehome_config.json           # 설정 파일 (백업용)
│   └── safehome_events.log            # 이벤트 로그
│
├── assets/                            # 리소스 파일
│   ├── images/
│   │   ├── camera1.jpg
│   │   ├── camera2.jpg
│   │   ├── camera3.jpg
│   │   └── floorplan.png
│   └── icons/
│       └── (device icons)
│
├── docs/                              # 문서
│   ├── SRS_document.docx
│   ├── SDS_document.docx
│   └── implementation_notes.md
│
├── requirements.txt                   # Python 패키지 의존성
├── README.md                          # 프로젝트 설명
├── run_simulation.py                  # 시뮬레이션 실행 스크립트
└── setup.py                           # 패키지 설치 스크립트 (옵션)
```

---

## 📊 SQLite3 데이터베이스 설계

### 데이터베이스 스키마

```sql
-- 1. SystemSettings 테이블
CREATE TABLE system_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    master_password TEXT NOT NULL,
    guest_password TEXT,
    web_password TEXT NOT NULL,
    entry_delay INTEGER DEFAULT 30,      -- seconds
    exit_delay INTEGER DEFAULT 45,       -- seconds
    alarm_duration INTEGER DEFAULT 180,  -- seconds
    system_lock_time INTEGER DEFAULT 300, -- seconds
    monitoring_phone TEXT,
    homeowner_phone TEXT,
    max_login_attempts INTEGER DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. SafetyZones 테이블
CREATE TABLE safety_zones (
    zone_id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_name TEXT NOT NULL,
    is_armed BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. SafeHomeModes 테이블
CREATE TABLE safehome_modes (
    mode_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mode_name TEXT NOT NULL UNIQUE,  -- 'DISARMED', 'HOME', 'AWAY', 'OVERNIGHT', 'EXTENDED'
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Sensors 테이블
CREATE TABLE sensors (
    sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_type TEXT NOT NULL,        -- 'WINDOOR' or 'MOTION'
    sensor_location TEXT,
    zone_id INTEGER,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (zone_id) REFERENCES safety_zones(zone_id) ON DELETE SET NULL
);

-- 5. ModeSensorMapping 테이블 (Mode와 Sensor 다대다 관계)
CREATE TABLE mode_sensor_mapping (
    mode_id INTEGER NOT NULL,
    sensor_id INTEGER NOT NULL,
    PRIMARY KEY (mode_id, sensor_id),
    FOREIGN KEY (mode_id) REFERENCES safehome_modes(mode_id) ON DELETE CASCADE,
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id) ON DELETE CASCADE
);

-- 6. Cameras 테이블
CREATE TABLE cameras (
    camera_id INTEGER PRIMARY KEY AUTOINCREMENT,
    camera_name TEXT,
    camera_location TEXT,
    camera_password TEXT,
    pan_angle INTEGER DEFAULT 0,
    zoom_level INTEGER DEFAULT 2,
    is_enabled BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. EventLogs 테이블 (Intrusion Log 포함)
CREATE TABLE event_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,         -- 'INFO', 'WARNING', 'ALARM', 'ERROR', 'INTRUSION'
    event_message TEXT NOT NULL,
    sensor_id INTEGER,
    camera_id INTEGER,
    zone_id INTEGER,
    source TEXT,                      -- 'System', 'Sensor', 'Camera', 'User'
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id) ON DELETE SET NULL,
    FOREIGN KEY (camera_id) REFERENCES cameras(camera_id) ON DELETE SET NULL,
    FOREIGN KEY (zone_id) REFERENCES safety_zones(zone_id) ON DELETE SET NULL
);

-- 8. LoginSessions 테이블 (로그인 시도 추적)
CREATE TABLE login_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    interface_type TEXT NOT NULL,     -- 'CONTROL_PANEL', 'WEB'
    username TEXT,
    login_successful BOOLEAN,
    failed_attempts INTEGER DEFAULT 0,
    login_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    logout_timestamp TIMESTAMP
);

-- 인덱스 생성 (성능 최적화)
CREATE INDEX idx_sensors_zone ON sensors(zone_id);
CREATE INDEX idx_sensors_type ON sensors(sensor_type);
CREATE INDEX idx_event_logs_timestamp ON event_logs(event_timestamp DESC);
CREATE INDEX idx_event_logs_type ON event_logs(event_type);
CREATE INDEX idx_login_sessions_interface ON login_sessions(interface_type);
```

---

## 🔧 Implementation 순서 (단계별 가이드)

### **Phase 1: Foundation Setup (기반 구축)** ⏱️ 1-2일

#### Step 1.1: 프로젝트 환경 설정
```bash
# 1. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 필수 패키지 설치
pip install Pillow          # 이미지 처리 (Camera)
pip install tk              # Tkinter (GUI)
# SQLite3은 Python 기본 포함

# 3. requirements.txt 생성
pip freeze > requirements.txt
```

#### Step 1.2: 데이터베이스 초기화
**파일: `safehome/database/db_manager.py`**
```python
import sqlite3
import os
from pathlib import Path

class DatabaseManager:
    """SQLite3 데이터베이스 관리"""
    
    def __init__(self, db_path="data/safehome.db"):
        self.db_path = db_path
        self._ensure_db_directory()
        self.connection = None
        
    def _ensure_db_directory(self):
        """DB 디렉토리 생성"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
    def connect(self):
        """DB 연결"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # Dict-like access
        return self.connection
        
    def disconnect(self):
        """DB 연결 종료"""
        if self.connection:
            self.connection.close()
            
    def initialize_schema(self):
        """스키마 초기화 (위의 SQL 실행)"""
        # schema.sql 파일 읽어서 실행
        pass
```

#### Step 1.3: 기본 Configuration 클래스 구조
**목표:** Configuration 레이어의 뼈대 구축

**구현 순서:**
1. `system_settings.py` - 데이터 클래스만 먼저
2. `safety_zone.py` - 단순 데이터 클래스
3. `safehome_mode.py` - Enum 정의
4. `log.py` - 로그 데이터 클래스

---

### **Phase 2: Configuration Layer 구현** ⏱️ 2-3일

#### Step 2.1: Storage Manager 구현
**파일: `safehome/configuration/storage_manager.py`**

**핵심 기능:**
```python
class StorageManager:
    """JSON + SQLite3 하이브리드 저장"""
    
    def __init__(self, db_manager, json_config_path="data/safehome_config.json"):
        self.db = db_manager
        self.json_path = json_config_path
        
    # JSON 기반 (빠른 설정 로드/저장)
    def save_settings_to_json(self, settings_dict):
        """System Settings를 JSON에 저장 (백업용)"""
        pass
        
    def load_settings_from_json(self):
        """JSON에서 설정 로드"""
        pass
        
    # DB 기반 (영구 저장, 이력 관리)
    def save_settings_to_db(self, settings):
        """SystemSettings를 DB에 저장"""
        pass
        
    def load_settings_from_db(self):
        """DB에서 최신 설정 로드"""
        pass
        
    def save_safety_zone(self, zone):
        """SafetyZone DB 저장"""
        pass
        
    def load_all_safety_zones(self):
        """모든 SafetyZone 로드"""
        pass
        
    def save_log(self, log):
        """이벤트 로그 DB 저장"""
        pass
        
    def get_logs(self, limit=100, event_type=None):
        """로그 검색"""
        pass
```

#### Step 2.2: Login Manager 구현
**파일: `safehome/configuration/login_manager.py`**

**핵심 로직:**
```python
class LoginManager:
    """로그인 관리 (패스워드 검증, 시도 추적)"""
    
    def __init__(self, storage_manager, system_settings):
        self.storage = storage_manager
        self.settings = system_settings
        self.failed_attempts = 0
        self.is_locked = False
        
    def validate_credentials(self, interface_type, password):
        """
        패스워드 검증
        interface_type: 'CONTROL_PANEL' or 'WEB'
        """
        if self.is_locked:
            return False
            
        # DB에서 올바른 패스워드 가져오기
        correct_password = self._get_password_for_interface(interface_type)
        
        if password == correct_password:
            self.failed_attempts = 0
            self._log_login_attempt(interface_type, True)
            return True
        else:
            self.failed_attempts += 1
            if self.failed_attempts >= self.settings.max_login_attempts:
                self.is_locked = True
                # 일정 시간 후 자동 unlock (타이머 설정)
            self._log_login_attempt(interface_type, False)
            return False
            
    def change_password(self, interface_type, old_password, new_password):
        """패스워드 변경"""
        pass
        
    def unlock_system(self):
        """시스템 언락 (강제 또는 타이머 후)"""
        self.failed_attempts = 0
        self.is_locked = False
```

#### Step 2.3: Log Manager 구현
**파일: `safehome/configuration/log_manager.py`**

```python
class LogManager:
    """로그 관리 (메모리 + DB)"""
    
    def __init__(self, storage_manager):
        self.storage = storage_manager
        self.logs = []  # 메모리 캐시 (최근 로그)
        self.log_file = "data/safehome_events.log"
        
    def add_log(self, message, level="INFO", source="System", 
                sensor_id=None, camera_id=None, zone_id=None):
        """로그 추가 (DB + 파일 + 메모리)"""
        log = Log(message=message, level=level, source=source,
                  sensor_id=sensor_id, camera_id=camera_id, zone_id=zone_id)
        
        # 1. 메모리 캐시
        self.logs.append(log)
        if len(self.logs) > 1000:  # 메모리 제한
            self.logs.pop(0)
            
        # 2. 파일 기록
        self._write_to_file(log)
        
        # 3. DB 저장
        self.storage.save_log(log)
        
    def get_intrusion_logs(self, start_date=None, end_date=None):
        """침입 로그 조회"""
        return self.storage.get_logs(event_type='INTRUSION', ...)
```

#### Step 2.4: Configuration Manager (Facade) 구현
**파일: `safehome/configuration/configuration_manager.py`**

```python
class ConfigurationManager:
    """
    Configuration Subsystem의 Facade
    다른 서브시스템들은 이 클래스를 통해서만 Configuration에 접근
    """
    
    def __init__(self, db_path="data/safehome.db"):
        # 1. DB 초기화
        self.db_manager = DatabaseManager(db_path)
        self.db_manager.connect()
        self.db_manager.initialize_schema()
        
        # 2. Storage Manager
        self.storage = StorageManager(self.db_manager)
        
        # 3. System Settings 로드
        self.settings = self._load_or_create_settings()
        
        # 4. Login Manager
        self.login_manager = LoginManager(self.storage, self.settings)
        
        # 5. Log Manager
        self.logger = LogManager(self.storage)
        self.logger.add_log("System configuration loaded", source="ConfigManager")
        
        # 6. Safety Zones 로드
        self.safety_zones = self._load_safety_zones()
        
        # 7. SafeHome Modes 로드
        self.modes = self._load_safehome_modes()
        
        # 8. Current State
        self.current_mode = SafeHomeMode.DISARMED
        self.current_zone_index = 0
        
    def save_configuration(self):
        """전체 설정 저장"""
        self.storage.save_settings_to_db(self.settings)
        self.storage.save_settings_to_json(self.settings.to_dict())
        self.logger.add_log("Configuration saved", source="ConfigManager")
        
    # Safety Zone 관리
    def get_safety_zone(self, zone_id):
        pass
        
    def add_safety_zone(self, zone_name):
        pass
        
    def delete_safety_zone(self, zone_id):
        pass
        
    # Mode 관리
    def set_mode(self, mode):
        self.current_mode = mode
        self.logger.add_log(f"Mode changed to {mode.name}", source="ConfigManager")
        
    def get_mode(self):
        return self.current_mode
```

---

### **Phase 3: Device Layer 구현** ⏱️ 3-4일

#### Step 3.1: Sensor 래퍼 클래스 구현

**파일: `safehome/device/sensor/sensor.py`**
```python
from abc import ABC, abstractmethod

class Sensor(ABC):
    """추상 Sensor 클래스 (공통 로직)"""
    
    def __init__(self, sensor_id, sensor_type, location, zone_id=None):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type  # 'WINDOOR' or 'MOTION'
        self.location = location
        self.zone_id = zone_id
        self.is_active = False
        
    @abstractmethod
    def read(self):
        """센서 신호 읽기 (하드웨어에서)"""
        pass
        
    @abstractmethod
    def arm(self):
        """센서 활성화"""
        pass
        
    @abstractmethod
    def disarm(self):
        """센서 비활성화"""
        pass
        
    def get_status(self):
        """센서 상태 반환 (dict)"""
        return {
            'id': self.sensor_id,
            'type': self.sensor_type,
            'location': self.location,
            'is_active': self.is_active,
            'detected': self.read()
        }
```

**파일: `safehome/device/sensor/windoor_sensor.py`**
```python
from .sensor import Sensor
from .device_windoor_sensor import DeviceWinDoorSensor  # 교수님 API

class WindowDoorSensor(Sensor):
    """Window/Door Sensor 래퍼"""
    
    def __init__(self, sensor_id, location, zone_id=None):
        super().__init__(sensor_id, 'WINDOOR', location, zone_id)
        self.hardware = DeviceWinDoorSensor()  # 가상 하드웨어 연결
        
    def read(self):
        """하드웨어에서 신호 읽기"""
        return self.hardware.read() if self.is_active else False
        
    def arm(self):
        self.is_active = True
        self.hardware.arm()
        
    def disarm(self):
        self.is_active = False
        self.hardware.disarm()
```

**파일: `safehome/device/sensor/motion_sensor.py`**
```python
from .sensor import Sensor
from .device_motion_detector import DeviceMotionDetector  # 교수님 API

class MotionSensor(Sensor):
    """Motion Sensor 래퍼"""
    
    def __init__(self, sensor_id, location, zone_id=None):
        super().__init__(sensor_id, 'MOTION', location, zone_id)
        self.hardware = DeviceMotionDetector()
        
    def read(self):
        return self.hardware.read() if self.is_active else False
        
    def arm(self):
        self.is_active = True
        self.hardware.arm()
        
    def disarm(self):
        self.is_active = False
        self.hardware.disarm()
```

#### Step 3.2: Sensor Controller 구현

**파일: `safehome/device/sensor/sensor_controller.py`**
```python
class SensorController:
    """센서들을 관리하는 컨트롤러"""
    
    def __init__(self, storage_manager, logger):
        self.sensors = {}  # {sensor_id: Sensor 객체}
        self.storage = storage_manager
        self.logger = logger
        
    def add_sensor(self, sensor_type, location, zone_id=None):
        """새 센서 추가"""
        sensor_id = len(self.sensors) + 1  # 또는 DB에서 auto increment
        
        if sensor_type == 'WINDOOR':
            sensor = WindowDoorSensor(sensor_id, location, zone_id)
        elif sensor_type == 'MOTION':
            sensor = MotionSensor(sensor_id, location, zone_id)
        else:
            raise ValueError(f"Unknown sensor type: {sensor_type}")
            
        self.sensors[sensor_id] = sensor
        self.storage.save_sensor(sensor)  # DB 저장
        self.logger.add_log(f"Sensor {sensor_id} added", source="SensorController")
        return sensor
        
    def remove_sensor(self, sensor_id):
        """센서 제거"""
        if sensor_id in self.sensors:
            del self.sensors[sensor_id]
            self.storage.delete_sensor(sensor_id)
            
    def arm_sensors_in_zone(self, zone_id):
        """특정 Zone의 모든 센서 활성화"""
        for sensor in self.sensors.values():
            if sensor.zone_id == zone_id:
                sensor.arm()
                
    def disarm_all_sensors(self):
        """모든 센서 비활성화"""
        for sensor in self.sensors.values():
            sensor.disarm()
            
    def poll_sensors(self):
        """
        모든 활성화된 센서를 폴링하여 침입 감지
        Returns: List[(sensor_id, detected)]
        """
        detections = []
        for sensor_id, sensor in self.sensors.items():
            if sensor.is_active and sensor.read():
                detections.append((sensor_id, sensor))
        return detections
        
    def get_sensor_status(self, sensor_id):
        """센서 상태 조회"""
        return self.sensors.get(sensor_id).get_status()
```

#### Step 3.3: Camera 래퍼 클래스 구현

**파일: `safehome/device/camera/safehome_camera.py`**
```python
from .device_camera import DeviceCamera  # 교수님 API

class SafeHomeCamera:
    """Camera 래퍼 클래스"""
    
    def __init__(self, camera_id, location, password=None):
        self.camera_id = camera_id
        self.location = location
        self.password = password
        self.is_enabled = True
        
        # 하드웨어 연결
        self.hardware = DeviceCamera()
        self.hardware.set_id(camera_id)
        
    def get_view(self):
        """현재 카메라 화면 가져오기 (PIL Image)"""
        if not self.is_enabled:
            return None
        return self.hardware.get_view()
        
    def pan_left(self):
        return self.hardware.pan_left()
        
    def pan_right(self):
        return self.hardware.pan_right()
        
    def zoom_in(self):
        return self.hardware.zoom_in()
        
    def zoom_out(self):
        return self.hardware.zoom_out()
        
    def enable(self):
        self.is_enabled = True
        
    def disable(self):
        self.is_enabled = False
        
    def set_password(self, password):
        self.password = password
        
    def verify_password(self, password):
        return self.password is None or self.password == password
```

#### Step 3.4: Camera Controller 구현

**파일: `safehome/device/camera/camera_controller.py`**
```python
class CameraController:
    """카메라들을 관리하는 컨트롤러"""
    
    def __init__(self, storage_manager, logger):
        self.cameras = {}  # {camera_id: SafeHomeCamera 객체}
        self.storage = storage_manager
        self.logger = logger
        
    def add_camera(self, location, password=None):
        """카메라 추가"""
        camera_id = len(self.cameras) + 1
        camera = SafeHomeCamera(camera_id, location, password)
        self.cameras[camera_id] = camera
        self.storage.save_camera(camera)
        return camera
        
    def get_camera_view(self, camera_id, password=None):
        """카메라 화면 가져오기 (패스워드 보호)"""
        camera = self.cameras.get(camera_id)
        if camera and camera.verify_password(password):
            return camera.get_view()
        return None
        
    def pan_zoom_camera(self, camera_id, action, password=None):
        """카메라 Pan/Zoom (패스워드 필요)"""
        camera = self.cameras.get(camera_id)
        if not camera or not camera.verify_password(password):
            return False
            
        if action == 'PAN_LEFT':
            return camera.pan_left()
        elif action == 'PAN_RIGHT':
            return camera.pan_right()
        elif action == 'ZOOM_IN':
            return camera.zoom_in()
        elif action == 'ZOOM_OUT':
            return camera.zoom_out()
            
    def enable_all_cameras(self):
        """모든 카메라 활성화"""
        for camera in self.cameras.values():
            camera.enable()
            
    def disable_all_cameras(self):
        """모든 카메라 비활성화"""
        for camera in self.cameras.values():
            camera.disable()
```

#### Step 3.5: Alarm 클래스 구현

**파일: `safehome/device/alarm/alarm.py`**
```python
import threading
import time

class Alarm:
    """알람 하드웨어 드라이버 (시뮬레이션)"""
    
    def __init__(self, duration=180):
        self.duration = duration  # 알람 지속 시간 (초)
        self.is_ringing = False
        self._alarm_thread = None
        
    def ring(self):
        """알람 울리기 (별도 쓰레드에서)"""
        if self.is_ringing:
            return
            
        self.is_ringing = True
        self._alarm_thread = threading.Thread(target=self._ring_for_duration, daemon=True)
        self._alarm_thread.start()
        
    def _ring_for_duration(self):
        """지정된 시간 동안 알람"""
        print("🚨 ALARM RINGING! 🚨")
        time.sleep(self.duration)
        self.stop()
        
    def stop(self):
        """알람 중지"""
        self.is_ringing = False
        print("🔇 Alarm stopped.")
        
    def is_active(self):
        return self.is_ringing
```

---

### **Phase 4: Core System Layer 구현** ⏱️ 2-3일

#### Step 4.1: System 클래스 구현

**파일: `safehome/core/system.py`**
```python
import threading
import time

class System:
    """
    SafeHome의 핵심 System 클래스
    모든 서브시스템을 통합하고 제어
    """
    
    def __init__(self):
        # 1. Configuration Manager 초기화
        self.config = ConfigurationManager()
        
        # 2. Device Controllers 초기화
        self.sensor_controller = SensorController(
            self.config.storage, 
            self.config.logger
        )
        self.camera_controller = CameraController(
            self.config.storage,
            self.config.logger
        )
        self.alarm = Alarm(duration=self.config.settings.alarm_duration)
        
        # 3. State
        self.is_running = False
        self.is_system_locked = False
        
        # 4. Polling Thread
        self._polling_thread = None
        
    def turn_on(self):
        """시스템 켜기"""
        self.is_running = True
        self._start_sensor_polling()
        self.config.logger.add_log("System turned ON", source="System")
        
    def turn_off(self):
        """시스템 끄기"""
        self.is_running = False
        self._stop_sensor_polling()
        self.config.save_configuration()
        self.config.logger.add_log("System turned OFF", source="System")
        
    def reset(self):
        """시스템 리셋"""
        self.turn_off()
        time.sleep(1)
        self.turn_on()
        self.config.logger.add_log("System RESET", source="System")
        
    # ===== Sensor Polling =====
    def _start_sensor_polling(self):
        """센서 폴링 시작 (백그라운드 쓰레드)"""
        self._polling_thread = threading.Thread(
            target=self._sensor_polling_loop, 
            daemon=True
        )
        self._polling_thread.start()
        
    def _sensor_polling_loop(self):
        """센서를 주기적으로 폴링하여 침입 감지"""
        while self.is_running:
            detections = self.sensor_controller.poll_sensors()
            if detections:
                for sensor_id, sensor in detections:
                    self._handle_intrusion(sensor)
            time.sleep(1)  # 1초마다 폴링
            
    def _handle_intrusion(self, sensor):
        """침입 감지 처리"""
        self.config.logger.add_log(
            f"INTRUSION DETECTED at {sensor.location}",
            level="ALARM",
            source="System",
            sensor_id=sensor.sensor_id,
            zone_id=sensor.zone_id
        )
        
        # Entry Delay 체크 (사용자가 비활성화할 시간)
        self._start_entry_delay_countdown(sensor)
        
    def _start_entry_delay_countdown(self, sensor):
        """Entry Delay 카운트다운 후 알람"""
        delay = self.config.settings.entry_delay
        self.config.logger.add_log(
            f"Entry delay: {delay} seconds",
            source="System"
        )
        
        # Entry Delay 쓰레드
        def countdown():
            time.sleep(delay)
            # 여전히 센서가 감지 중이면 알람
            if self.is_running and sensor.read():
                self._trigger_alarm(sensor)
                
        threading.Thread(target=countdown, daemon=True).start()
        
    def _trigger_alarm(self, sensor):
        """알람 발동"""
        self.alarm.ring()
        self.call_monitoring_service(sensor)
        
    def call_monitoring_service(self, sensor):
        """모니터링 서비스 호출 (시뮬레이션)"""
        phone = self.config.settings.monitoring_phone
        self.config.logger.add_log(
            f"Calling monitoring service at {phone} - Intrusion at {sensor.location}",
            level="ALARM",
            source="System"
        )
        print(f"📞 Calling {phone}: INTRUSION at {sensor.location}")
        
    # ===== Mode Control =====
    def arm_system(self, mode):
        """시스템 Arm (특정 모드로)"""
        self.config.set_mode(mode)
        
        # Mode에 해당하는 센서들 활성화
        sensor_list = self._get_sensors_for_mode(mode)
        for sensor_id in sensor_list:
            sensor = self.sensor_controller.sensors.get(sensor_id)
            if sensor:
                sensor.arm()
                
        self.config.logger.add_log(
            f"System ARMED in {mode.name} mode",
            source="System"
        )
        
    def disarm_system(self):
        """시스템 Disarm"""
        self.sensor_controller.disarm_all_sensors()
        self.config.set_mode(SafeHomeMode.DISARMED)
        self.alarm.stop()
        self.config.logger.add_log("System DISARMED", source="System")
        
    def arm_zone(self, zone_id):
        """특정 Zone Arm"""
        self.sensor_controller.arm_sensors_in_zone(zone_id)
        zone = self.config.get_safety_zone(zone_id)
        zone.is_armed = True
        self.config.logger.add_log(
            f"Zone {zone.zone_name} ARMED",
            source="System"
        )
        
    def disarm_zone(self, zone_id):
        """특정 Zone Disarm"""
        # Zone의 센서들 비활성화
        for sensor in self.sensor_controller.sensors.values():
            if sensor.zone_id == zone_id:
                sensor.disarm()
        zone = self.config.get_safety_zone(zone_id)
        zone.is_armed = False
        
    # ===== Login Control =====
    def login(self, interface_type, password):
        """로그인 시도"""
        return self.config.login_manager.validate_credentials(
            interface_type, password
        )
        
    def change_password(self, interface_type, old_pass, new_pass):
        """패스워드 변경"""
        return self.config.login_manager.change_password(
            interface_type, old_pass, new_pass
        )
        
    # ===== Helper Methods =====
    def _get_sensors_for_mode(self, mode):
        """특정 Mode에 할당된 센서 ID 리스트 반환"""
        # DB에서 mode_sensor_mapping 조회
        return self.config.storage.get_sensors_for_mode(mode)
```

---

### **Phase 5: User Interface Layer 구현** ⏱️ 3-4일

#### Step 5.1: Control Panel 구현 (이미 일부 완료)

**현재 코드 (`safehome_control_panel.py`) 개선:**
```python
class SafeHomeControlPanel(DeviceControlPanelAbstract):
    """
    Control Panel 구현 (교수님 제공 GUI 기반)
    System과 연동하여 실제 기능 구현
    """
    
    def __init__(self, master=None, system=None):
        super().__init__(master)
        
        # System 인스턴스 주입
        self.system = system if system else System()
        
        # Internal state
        self.input_buffer = ""
        self.is_authenticated = False
        self.is_changing_password = False
        self.current_valid_password = None
        
        # UI 초기화
        self._refresh_status_display()
        self._reset_interaction()
        
    # ... (기존 코드 유지하되, System 메서드 호출로 변경)
    
    def _attempt_login(self):
        """로그인 시도"""
        success = self.system.login('CONTROL_PANEL', self.input_buffer)
        if success:
            self.is_authenticated = True
            self.current_valid_password = self.input_buffer
            self.set_display_short_message1("Login Success")
            self.set_display_short_message2("1:Away 2:Stay 3:Set 0:Disarm 9:Zone")
        else:
            # 실패 처리
            if self.system.config.login_manager.is_locked:
                self.set_display_short_message1("SYSTEM LOCKED")
            else:
                self.set_display_short_message1("Login Failed")
        self.input_buffer = ""
        
    def _handle_command(self, key):
        """명령 처리"""
        if key == "1":  # Arm Away
            self.system.arm_system(SafeHomeMode.ARMED_AWAY)
            self.set_display_short_message1("ARMED (AWAY)")
            self._refresh_status_display()
        elif key == "2":  # Arm Stay
            self.system.arm_system(SafeHomeMode.ARMED_STAY)
            self.set_display_short_message1("ARMED (STAY)")
            self._refresh_status_display()
        elif key == "0":  # Disarm
            self.system.disarm_system()
            self.set_display_short_message1("DISARMED")
            self._refresh_status_display()
        elif key == "3":  # Change Password
            self.is_changing_password = True
            # ... (기존 코드)
        elif key == "9":  # Zone change
            # Zone 전환
            pass
```

#### Step 5.2: Camera Monitor 개선

**현재 코드 (`camera_monitor.py`) 개선:**
```python
class CameraMonitor(tk.Toplevel):
    """Camera 모니터 윈도우 (System과 통합)"""
    
    def __init__(self, master=None, system=None, camera_id=1, password=None):
        super().__init__(master)
        self.system = system
        self.camera_id = camera_id
        self.password = password
        
        # 패스워드 확인
        if not self._verify_access():
            self.destroy()
            return
            
        # Camera 가져오기 (System의 CameraController를 통해)
        self.camera = self.system.camera_controller.cameras.get(camera_id)
        if not self.camera:
            messagebox.showerror("Error", f"Camera {camera_id} not found")
            self.destroy()
            return
            
        # GUI 설정
        self._setup_gui()
        
    def _verify_access(self):
        """카메라 접근 권한 확인"""
        camera = self.system.camera_controller.cameras.get(self.camera_id)
        if not camera:
            return False
        if camera.password and camera.password != self.password:
            messagebox.showerror("Access Denied", "Invalid camera password")
            return False
        return True
        
    def _update_feed(self):
        """카메라 화면 업데이트"""
        try:
            # System을 통해 카메라 화면 가져오기
            pil_image = self.system.camera_controller.get_camera_view(
                self.camera_id, self.password
            )
            if pil_image:
                self.tk_image = ImageTk.PhotoImage(pil_image)
                self.image_label.config(image=self.tk_image)
        except Exception as e:
            print(f"Camera Error: {e}")
        self.after(100, self._update_feed)
```

#### Step 5.3: Web Interface (Optional - 향후 확장)

**간단한 구조만 설계:**
```python
# safehome/interface/web/web_interface.py
class WebInterface:
    """Web Interface (Flask 또는 Tkinter 기반 웹뷰)"""
    
    def __init__(self, system):
        self.system = system
        self.pages = {}
        
    def show_login_page(self):
        pass
        
    def show_main_page(self):
        pass
        
    def show_security_page(self):
        pass
        
    def show_surveillance_page(self):
        pass
```

---

### **Phase 6: Integration & Main Entry Point** ⏱️ 1-2일

#### Step 6.1: 메인 실행 스크립트 개선

**파일: `run_simulation.py`**
```python
import tkinter as tk
from safehome.core.system import System
from safehome.interface.control_panel.safehome_control_panel import SafeHomeControlPanel
from safehome.interface.control_panel.camera_monitor import CameraMonitor
from safehome.device.sensor.device_sensor_tester import DeviceSensorTester

def setup_hardware(system):
    """가상 하드웨어 초기화"""
    print("\n[Setup] Initializing Virtual Hardware...")
    
    # 1. 센서 추가
    system.sensor_controller.add_sensor('WINDOOR', 'Living Room Window', zone_id=1)
    system.sensor_controller.add_sensor('WINDOOR', 'Front Door', zone_id=1)
    system.sensor_controller.add_sensor('MOTION', 'Living Room', zone_id=1)
    system.sensor_controller.add_sensor('MOTION', 'Bedroom', zone_id=2)
    
    # 2. 카메라 추가
    system.camera_controller.add_camera('Living Room')
    system.camera_controller.add_camera('Front Door')
    
    print("[Setup] Hardware initialized successfully!")

def main():
    # 1. Tkinter Root
    root = tk.Tk()
    root.withdraw()
    
    # 2. System 초기화
    print("="*60)
    print("SafeHome System Starting...")
    print("="*60)
    system = System()
    
    # 3. 하드웨어 설정
    setup_hardware(system)
    
    # 4. System 켜기
    system.turn_on()
    
    # 5. Sensor Test GUI 시작
    print("\n[GUI] Launching Sensor Simulator...")
    DeviceSensorTester.showSensorTester()
    
    # 6. Control Panel GUI 시작
    print("[GUI] Launching Control Panel...")
    control_panel = SafeHomeControlPanel(master=root, system=system)
    
    # 7. Camera Monitor 시작
    print("[GUI] Launching Camera Monitor...")
    camera_monitor = CameraMonitor(master=root, system=system, camera_id=1)
    
    # 8. 종료 처리
    def on_close():
        print("\n[System] Shutting down...")
        system.turn_off()
        try:
            if hasattr(camera_monitor, 'camera'):
                camera_monitor.camera.hardware.stop()
        except:
            pass
        root.destroy()
        print("[System] Goodbye!")
        
    control_panel.protocol("WM_DELETE_WINDOW", on_close)
    
    print("\n" + "="*60)
    print("SIMULATION READY")
    print("- Default Password: 1234")
    print("- Use Control Panel to Arm/Disarm")
    print("- Use Sensor Test to simulate intrusions")
    print("="*60 + "\n")
    
    root.mainloop()

if __name__ == "__main__":
    main()
```

---

### **Phase 7: Testing & Refinement** ⏱️ 2-3일

#### Step 7.1: Unit Tests
- `test_configuration.py` - Configuration Manager 테스트 (이미 존재)
- `test_sensor.py` - Sensor 로직 테스트
- `test_camera.py` - Camera 로직 테스트
- `test_system.py` - System 통합 테스트

#### Step 7.2: Integration Testing
- Control Panel ↔ System 연동 테스트
- Sensor Polling ↔ Alarm 발동 테스트
- Login ↔ System Lock 테스트
- DB 저장/로드 테스트

#### Step 7.3: Bug Fixing & Polish
- 에러 핸들링 강화
- 로그 메시지 개선
- GUI 반응성 개선

---

## 📝 Implementation 체크리스트

### Phase 1: Foundation ✅
- [ ] 프로젝트 폴더 구조 생성
- [ ] 데이터베이스 스키마 작성 (`schema.sql`)
- [ ] DatabaseManager 클래스 구현
- [ ] 기본 데이터 클래스 작성 (SystemSettings, SafetyZone, Log)

### Phase 2: Configuration Layer ✅
- [ ] StorageManager 구현 (JSON + SQLite3)
- [ ] LoginManager 구현 (패스워드 검증, 시도 추적)
- [ ] LogManager 구현 (로그 기록, 조회)
- [ ] ConfigurationManager (Facade) 구현

### Phase 3: Device Layer ✅
- [ ] Sensor 추상 클래스 및 래퍼 클래스 구현
- [ ] SensorController 구현
- [ ] SafeHomeCamera 래퍼 클래스 구현
- [ ] CameraController 구현
- [ ] Alarm 클래스 구현

### Phase 4: Core System ✅
- [ ] System 클래스 기본 구조
- [ ] Sensor Polling 로직 (백그라운드 쓰레드)
- [ ] Intrusion 감지 및 Alarm 발동
- [ ] Arm/Disarm 로직 (Mode별, Zone별)
- [ ] Login/Logout 로직

### Phase 5: User Interface ✅
- [ ] SafeHomeControlPanel 개선 (System 연동)
- [ ] CameraMonitor 개선 (패스워드 보호)
- [ ] GUI 상태 업데이트 로직

### Phase 6: Integration ✅
- [ ] run_simulation.py 메인 스크립트 완성
- [ ] 전체 시스템 통합 테스트
- [ ] 에러 핸들링 추가

### Phase 7: Testing ✅
- [ ] Unit Tests 작성
- [ ] Integration Tests
- [ ] Bug Fixing

---

## 🎯 핵심 설계 원칙

1. **Facade Pattern (ConfigurationManager)**
    - Configuration 서브시스템의 복잡성을 숨김
    - 다른 레이어는 ConfigurationManager를 통해서만 접근

2. **Wrapper Pattern (Sensor, Camera)**
    - 교수님이 제공한 가상 하드웨어 API를 래핑
    - 비즈니스 로직과 하드웨어 분리

3. **Controller Pattern (SensorController, CameraController)**
    - 디바이스들을 관리하는 중앙 컨트롤러
    - 리스트 관리, 상태 조회, 일괄 제어

4. **Layered Architecture**
    - Configuration ← Core System ← Device Layer
    - UI Layer는 System만 의존

5. **Database Strategy**
    - SQLite3: 영구 저장, 이력 관리, 복잡한 쿼리
    - JSON: 빠른 설정 로드/저장, 백업용
    - 메모리: 최근 로그 캐싱

---

## 💡 추가 제안

### 1. Error Handling Strategy
```python
# Custom Exception 정의
class SafeHomeException(Exception):
    pass

class LoginFailedException(SafeHomeException):
    pass

class SensorNotFoundException(SafeHomeException):
    pass

class CameraAccessDeniedException(SafeHomeException):
    pass
```

### 2. Configuration File (JSON 백업)
```json
{
  "master_password": "1234",
  "guest_password": "9999",
  "web_password": "webpass123",
  "entry_delay": 30,
  "exit_delay": 45,
  "alarm_duration": 180,
  "monitoring_phone": "911",
  "homeowner_phone": "010-1234-5678"
}
```

### 3. Logging Format
```
[2025-11-23 14:30:45] [INFO] System: System configuration loaded
[2025-11-23 14:31:12] [ALARM] System: INTRUSION DETECTED at Living Room Window
[2025-11-23 14:31:42] [INFO] System: Entry delay: 30 seconds
[2025-11-23 14:32:12] [ALARM] System: Alarm triggered
```

---

## 🚀 시작하기

### Step 1: 프로젝트 클론 및 구조 생성
```bash
# 1. 기존 코드 백업
cp -r safehome safehome_backup

# 2. 새 구조 생성
mkdir -p safehome/database
mkdir -p safehome/device/alarm
mkdir -p safehome/core
mkdir -p data
mkdir -p assets/images

# 3. 기존 코드 재배치
# (현재 코드를 위의 구조에 맞게 이동)
```

### Step 2: 데이터베이스 초기화
```python
# 간단한 테스트 스크립트
from safehome.database.db_manager import DatabaseManager

db = DatabaseManager("data/safehome.db")
db.connect()
db.initialize_schema()
print("Database initialized!")
```

### Step 3: Phase별 구현 시작
위의 단계를 순서대로 따라가면서 구현하세요!

---

## 📞 문의사항

구현 중 막히는 부분이나 설계 관련 질문이 있으면 언제든 물어보세요!
각 Phase별로 상세한 코드 예시나 도움이 필요하면 말씀해주세요.

**Good luck with implementation! 🎉**