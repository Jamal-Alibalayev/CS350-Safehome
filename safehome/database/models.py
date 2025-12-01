"""
Database Models for SafeHome System
ORM-style classes representing database tables
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class SystemSettings:
    """System Settings Model"""

    id: int
    master_password: str
    guest_password: Optional[str]
    web_password_1: str
    web_password_2: str
    entry_delay: int  # seconds
    exit_delay: int  # seconds
    alarm_duration: int  # seconds
    system_lock_time: int  # seconds
    monitoring_phone: str
    homeowner_phone: str
    max_login_attempts: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_db_row(cls, row):
        """Create instance from database row"""
        if row is None:
            return None
        return cls(
            id=row["id"],
            master_password=row["master_password"],
            guest_password=row["guest_password"],
            web_password_1=row["web_password_1"],
            web_password_2=row["web_password_2"],
            entry_delay=row["entry_delay"],
            exit_delay=row["exit_delay"],
            alarm_duration=row["alarm_duration"],
            system_lock_time=row["system_lock_time"],
            monitoring_phone=row["monitoring_phone"],
            homeowner_phone=row["homeowner_phone"],
            max_login_attempts=row["max_login_attempts"],
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )


@dataclass
class SafetyZone:
    """Safety Zone Model"""

    zone_id: Optional[int]
    zone_name: str
    is_armed: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_db_row(cls, row):
        """Create instance from database row"""
        if row is None:
            return None
        return cls(
            zone_id=row["zone_id"],
            zone_name=row["zone_name"],
            is_armed=bool(row["is_armed"]),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )


@dataclass
class SafeHomeMode:
    """SafeHome Mode Model"""

    mode_id: Optional[int]
    mode_name: str  # HOME, AWAY, OVERNIGHT, EXTENDED
    description: Optional[str] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_db_row(cls, row):
        """Create instance from database row"""
        if row is None:
            return None
        return cls(
            mode_id=row["mode_id"],
            mode_name=row["mode_name"],
            description=row.get("description"),
            created_at=row.get("created_at"),
        )


@dataclass
class Sensor:
    """Sensor Model"""

    sensor_id: Optional[int]
    sensor_type: str  # WINDOOR or MOTION
    sensor_location: str
    zone_id: Optional[int] = None
    is_active: bool = True
    created_at: Optional[datetime] = None

    @classmethod
    def from_db_row(cls, row):
        """Create instance from database row"""
        if row is None:
            return None
        return cls(
            sensor_id=row["sensor_id"],
            sensor_type=row["sensor_type"],
            sensor_location=row["sensor_location"],
            zone_id=row.get("zone_id"),
            is_active=bool(row["is_active"]),
            created_at=row.get("created_at"),
        )


@dataclass
class Camera:
    """Camera Model"""

    camera_id: Optional[int]
    camera_name: str
    camera_location: str
    camera_password: Optional[str] = None
    pan_angle: int = 0
    zoom_level: int = 2
    is_enabled: bool = True
    created_at: Optional[datetime] = None

    @classmethod
    def from_db_row(cls, row):
        """Create instance from database row"""
        if row is None:
            return None
        return cls(
            camera_id=row["camera_id"],
            camera_name=row["camera_name"],
            camera_location=row["camera_location"],
            camera_password=row.get("camera_password"),
            pan_angle=row["pan_angle"],
            zoom_level=row["zoom_level"],
            is_enabled=bool(row["is_enabled"]),
            created_at=row.get("created_at"),
        )


@dataclass
class EventLog:
    """Event Log Model"""

    log_id: Optional[int]
    event_type: str  # INFO, WARNING, ALARM, ERROR, INTRUSION
    event_message: str
    sensor_id: Optional[int] = None
    camera_id: Optional[int] = None
    zone_id: Optional[int] = None
    source: str = "System"
    event_timestamp: Optional[datetime] = None

    @classmethod
    def from_db_row(cls, row):
        """Create instance from database row"""
        if row is None:
            return None
        return cls(
            log_id=row["log_id"],
            event_type=row["event_type"],
            event_message=row["event_message"],
            sensor_id=row.get("sensor_id"),
            camera_id=row.get("camera_id"),
            zone_id=row.get("zone_id"),
            source=row["source"],
            event_timestamp=row.get("event_timestamp"),
        )


@dataclass
class LoginSession:
    """Login Session Model"""

    session_id: Optional[int]
    interface_type: str  # CONTROL_PANEL or WEB
    username: Optional[str] = None
    login_successful: bool = False
    failed_attempts: int = 0
    login_timestamp: Optional[datetime] = None
    logout_timestamp: Optional[datetime] = None

    @classmethod
    def from_db_row(cls, row):
        """Create instance from database row"""
        if row is None:
            return None
        return cls(
            session_id=row["session_id"],
            interface_type=row["interface_type"],
            username=row.get("username"),
            login_successful=bool(row["login_successful"]),
            failed_attempts=row["failed_attempts"],
            login_timestamp=row.get("login_timestamp"),
            logout_timestamp=row.get("logout_timestamp"),
        )
