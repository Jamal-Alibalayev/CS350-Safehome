from typing import Optional, List
from .log import Log

class LogManager:
    """
    管理系统的日志记录
    """
    def __init__(self, storage_manager=None):
        self.logs = []  # 内存日志缓存
        self.log_file = "data/safehome_events.log"
        self.storage = storage_manager
        # Preload logs from storage if available
        if self.storage:
            try:
                stored_logs = self.storage.get_logs(limit=500)
                for row in stored_logs:
                    log = Log(
                        message=row.get("event_message", ""),
                        level=row.get("event_type", "INFO"),
                        source=row.get("source", "System"),
                        timestamp=row.get("event_timestamp")
                    )
                    self.logs.append(log)
            except Exception as e:
                print(f"Error preloading logs: {e}")

    def add_log(self, message: str, level: str = "INFO", source: str = "System", **kwargs):
        """添加一条新日志"""
        new_log = Log(message, level=level, source=source)
        self.logs.append(new_log)
        self._write_to_file(new_log)
        if self.storage and self.storage.db:
            try:
                # Pass sensor_id, camera_id, etc. if they exist
                self.storage.save_log(new_log, **kwargs)
            except Exception as e:
                print(f"Error saving log to storage: {e}")
        # print(new_log)  # 可选：控制台输出

    def _write_to_file(self, log: Log):
        """追加写入文件"""
        try:
            with open(self.log_file, "a", encoding='utf-8') as f:
                f.write(str(log) + "\n")
        except IOError as e:
            print(f"Error writing log: {e}")

    def get_recent_logs(self, count=10) -> List[Log]:
        """获取最近的日志"""
        return self.logs[-count:]

    def get_all_logs(self) -> List[Log]:
        """获取内存中的全部日志"""
        return list(self.logs)

    def clear_logs(self):
        """Clear in-memory, file, and DB logs."""
        self.logs = []
        # Truncate log file
        try:
            with open(self.log_file, "w", encoding="utf-8") as f:
                f.write("")  # empty file
        except IOError as e:
            print(f"Error clearing log file: {e}")
        # Clear DB logs if storage present
        if self.storage:
            try:
                self.storage.clear_logs()
            except Exception as e:
                print(f"Error clearing logs in storage: {e}")
