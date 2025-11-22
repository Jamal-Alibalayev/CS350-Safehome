from dataclasses import dataclass

@dataclass
class SystemSettings:
    """
    保存系统的全局配置参数
    """
    master_password: str = "1234"     # 主密码
    entry_delay: int = 30             # 进入延迟 (秒)
    exit_delay: int = 45              # 离开延迟 (秒)
    alarm_duration: int = 180         # 报警持续时间 (秒)
    max_login_attempts: int = 3       # 最大登录尝试次数
    
    def update_settings(self, **kwargs):
        """允许动态更新设置"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)