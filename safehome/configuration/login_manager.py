from .login_interface import LoginInterface
from .system_settings import SystemSettings

class LoginManager(LoginInterface):
    """
    具体的登录逻辑实现
    """
    def __init__(self, settings: SystemSettings):
        self.settings = settings
        self.failed_attempts = 0
        self.is_locked = False

    def validate_credentials(self, user_id: str, password: str) -> bool:
        """
        验证密码。
        注：此处的 user_id 在简单系统中可能仅作为占位符，或者区分 Admin/User
        """
        if self.is_locked:
            print("System is locked due to too many failed attempts.")
            return False

        # 简单示例：直接比对主密码
        if password == self.settings.master_password:
            self.failed_attempts = 0
            return True
        else:
            self.failed_attempts += 1
            if self.failed_attempts >= self.settings.max_login_attempts:
                self.is_locked = True
                print("Max login attempts reached. System locked.")
            return False

    def change_password(self, old_password: str, new_password: str) -> bool:
        if self.validate_credentials("admin", old_password):
            self.settings.master_password = new_password
            return True
        return False
    
    def unlock_system(self):
        self.failed_attempts = 0
        self.is_locked = False