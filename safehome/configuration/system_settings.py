from dataclasses import dataclass
from typing import Optional


@dataclass
class SystemSettings:
    """
    System global configuration parameters
    Supports both Control Panel and Web interface settings
    """
    # Control Panel passwords
    master_password: str = "1234"           # Master password (4 digits)
    guest_password: Optional[str] = None    # Guest password (4 digits, optional)

    # Web interface passwords
    web_password_1: str = "webpass1"        # Web password 1 (8 characters)
    web_password_2: str = "webpass2"        # Web password 2 (8 characters)

    # Timing settings
    entry_delay: int = 300                  # Entry delay (seconds, min 300 = 5 min)
    exit_delay: int = 45                    # Exit delay (seconds)
    alarm_duration: int = 180               # Alarm duration (seconds)
    system_lock_time: int = 300             # System lock duration (seconds)

    # Phone numbers
    monitoring_phone: str = "911"           # Monitoring service phone
    homeowner_phone: str = "000-0000-0000"  # Homeowner phone
    alert_email: str = "safehomejongyoon@gmail.com"  # Default recipient email

    # Email SMTP defaults (Gmail app password provided)
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = "safehomejongyoon@gmail.com"
    smtp_password: str = "lfzj nkxr dqsa czal"

    # Security settings
    max_login_attempts: int = 3             # Max login attempts before lock

    def update_settings(self, **kwargs):
        """Dynamically update settings"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self) -> dict:
        """Convert settings to dictionary"""
        return {
            'master_password': self.master_password,
            'guest_password': self.guest_password,
            'web_password_1': self.web_password_1,
            'web_password_2': self.web_password_2,
            'entry_delay': self.entry_delay,
            'exit_delay': self.exit_delay,
            'alarm_duration': self.alarm_duration,
            'system_lock_time': self.system_lock_time,
            'monitoring_phone': self.monitoring_phone,
            'homeowner_phone': self.homeowner_phone,
            'alert_email': self.alert_email,
            'smtp_host': self.smtp_host,
            'smtp_port': self.smtp_port,
            'smtp_user': self.smtp_user,
            'smtp_password': self.smtp_password,
            'max_login_attempts': self.max_login_attempts
        }
