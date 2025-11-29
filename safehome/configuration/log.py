from dataclasses import dataclass
from datetime import datetime


@dataclass
class Log:
    """
    单条日志记录
    """

    message: str
    level: str = "INFO"  # INFO, WARNING, ALARM, ERROR
    timestamp: datetime = None
    source: str = "System"

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] [{self.level}] {self.source}: {self.message}"

    # Backward-compatible aliases
    @property
    def event_type(self):
        return self.level
