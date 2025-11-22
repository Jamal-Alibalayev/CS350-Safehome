from .log import Log

class LogManager:
    """
    管理系统的日志记录
    """
    def __init__(self):
        self.logs = []  # 内存日志缓存
        self.log_file = "safehome_events.log"

    def add_log(self, message: str, level: str = "INFO", source: str = "System"):
        """添加一条新日志"""
        new_log = Log(message, level=level, source=source)
        self.logs.append(new_log)
        self._write_to_file(new_log)
        # print(new_log)  # 可选：控制台输出

    def _write_to_file(self, log: Log):
        """追加写入文件"""
        try:
            with open(self.log_file, "a", encoding='utf-8') as f:
                f.write(str(log) + "\n")
        except IOError as e:
            print(f"Error writing log: {e}")

    def get_recent_logs(self, count=10):
        """获取最近的日志"""
        return self.logs[-count:]