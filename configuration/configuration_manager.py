from .system_settings import SystemSettings
from .storage_manager import StorageManager
from .log_manager import LogManager
from .login_manager import LoginManager
from .safehome_mode import SafeHomeMode

class ConfigurationManager:
    """
    配置子系统的门面类 (Facade)。
    系统其它部分应主要通过此类与配置模块交互。
    """
    def __init__(self):
        # 1. 初始化存储管理器
        self.storage = StorageManager()
        
        # 2. 初始化系统设置 (尝试从文件加载)
        self.settings = SystemSettings()
        loaded_data = self.storage.load_settings()
        if loaded_data:
            self.settings.update_settings(**loaded_data)
            
        # 3. 初始化日志管理器
        self.logger = LogManager()
        self.logger.add_log("System configuration loaded", source="ConfigManager")

        # 4. 初始化登录管理器
        self.login_manager = LoginManager(self.settings)
        
        # 5. 初始状态
        self.current_mode = SafeHomeMode.DISARMED

    def save_configuration(self):
        """保存当前所有配置"""
        self.storage.save_settings(self.settings)
        self.logger.add_log("Configuration saved manually", source="ConfigManager")

    def set_mode(self, mode: SafeHomeMode):
        """更改系统模式"""
        self.current_mode = mode
        self.logger.add_log(f"System mode changed to {mode.name}", source="ConfigManager")

    def get_mode(self) -> SafeHomeMode:
        return self.current_mode