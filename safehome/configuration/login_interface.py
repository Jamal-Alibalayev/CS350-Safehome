from abc import ABC, abstractmethod

class LoginInterface(ABC):
    """
    认证接口抽象类
    """
    @abstractmethod
    def validate_credentials(self, user_id: str, password: str) -> bool:
        pass

    @abstractmethod
    def change_password(self, old_password: str, new_password: str) -> bool:
        pass