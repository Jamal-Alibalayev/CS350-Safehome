from typing import List
from .log import Log

class LogManager:
    """
    Centralized log manager.
    Persists logs to file and database (event_logs) and provides retrieval for UI.
    """
    def __init__(self, storage_manager=None):
        self.logs: List[Log] = []  # in-memory cache (recent session)
        self.log_file = "data/safehome_events.log"
        self.storage = storage_manager

    def add_log(
        self,
        message: str,
        level: str = "INFO",
        source: str = "System",
        sensor_id: int = None,
        camera_id: int = None,
        zone_id: int = None
    ):
        """Add a new log entry and persist it."""
        new_log = Log(
            message,
            level=level,
            source=source,
            sensor_id=sensor_id,
            camera_id=camera_id,
            zone_id=zone_id
        )
        self.logs.append(new_log)
        self._write_to_file(new_log)

        # Persist to DB if available
        if self.storage:
            try:
                self.storage.save_log(new_log)
            except Exception as e:
                # Fallback to file-only logging
                print(f"Error saving log to DB: {e}")

    def _write_to_file(self, log: Log):
        """Append to log file (simple backup)"""
        try:
            with open(self.log_file, "a", encoding='utf-8') as f:
                f.write(str(log) + "\n")
        except IOError as e:
            print(f"Error writing log: {e}")

    def get_recent_logs(self, count=10) -> List[Log]:
        """Return most recent logs from current session"""
        return self.logs[-count:]

    def get_all_logs(self, limit: int = 500) -> List[Log]:
        """
        Retrieve logs for UI (pull from DB when available).
        """
        if self.storage:
            rows = self.storage.get_logs(limit=limit)
            return [
                Log(
                    row.get("event_message", ""),
                    level=row.get("event_type", "INFO"),
                    source=row.get("source", "System"),
                    timestamp=row.get("event_timestamp"),
                    sensor_id=row.get("sensor_id"),
                    camera_id=row.get("camera_id"),
                    zone_id=row.get("zone_id")
                )
                for row in rows
            ]
        return list(self.logs)

    def clear_logs(self):
        """Delete all persisted logs and clear cache."""
        self.logs.clear()
        if self.storage:
            self.storage.clear_logs()
        try:
            with open(self.log_file, "w", encoding="utf-8") as f:
                f.write("")
        except IOError:
            pass
