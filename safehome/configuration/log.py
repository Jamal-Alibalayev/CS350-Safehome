from dataclasses import dataclass
from datetime import datetime

@dataclass
class Log:
    """
    Log entry entity.
    Aligns with event_logs schema (message, level/type, source, optional device refs).
    """
    message: str
    level: str = "INFO"  # INFO, WARNING, ALARM, ERROR
    source: str = "System"
    timestamp: datetime = None
    sensor_id: int = None
    camera_id: int = None
    zone_id: int = None

    def __post_init__(self):
        # Accept string timestamps from DB or generate now
        if isinstance(self.timestamp, str):
            try:
                self.timestamp = datetime.fromisoformat(self.timestamp)
            except Exception:
                self.timestamp = datetime.now()
        if self.timestamp is None:
            self.timestamp = datetime.now()

    @property
    def event_type(self):
        """Alias to keep UI filter code working."""
        return self.level

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] [{self.level}] {self.source}: {self.message}"
