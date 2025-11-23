import json
import os
from .system_settings import SystemSettings

class StorageManager:
    """
    负责配置和数据的持久化存储
    """
    CONFIG_FILE = "data/safehome_config.json"

    def save_settings(self, settings: SystemSettings):
        """将 SystemSettings 保存到 JSON"""
        data = {
            "master_password": settings.master_password,
            "entry_delay": settings.entry_delay,
            "exit_delay": settings.exit_delay,
            "alarm_duration": settings.alarm_duration
        }
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            print("Settings saved successfully.")
        except IOError as e:
            print(f"Error saving settings: {e}")

    def load_settings(self) -> dict:
        """从 JSON 加载设置 loasd settings from JSON"""
        if not os.path.exists(self.CONFIG_FILE):
            return {}
        
        try:
            with open(self.CONFIG_FILE, 'r') as f:
                return json.load(f)
        except IOError:
            return {}