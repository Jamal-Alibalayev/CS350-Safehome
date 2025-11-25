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
            'max_login_attempts': self.max_login_attempts
        }