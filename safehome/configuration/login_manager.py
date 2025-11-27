import threading
import time
from datetime import datetime
from .login_interface import LoginInterface
from .system_settings import SystemSettings


class LoginManager(LoginInterface):
    """
    Login Manager with support for both Control Panel and Web interfaces
    Implements password validation, lockout mechanism, and session tracking
    """

    def __init__(self, settings: SystemSettings, storage_manager=None):
        """
        Initialize Login Manager

        Args:
            settings: System settings containing passwords
            storage_manager: Optional storage manager for session tracking
        """
        self.settings = settings
        self.storage = storage_manager
        self.failed_attempts = {}  # Track attempts per interface type
        self.is_locked = {}  # Track lock status per interface type
        self.lock_timers = {}  # Track unlock timers per interface type

    def validate_credentials(self, user_id: str, password: str,
                             interface_type: str = "CONTROL_PANEL") -> bool:
        """
        Validate credentials for a given interface type

        Args:
            user_id: User identifier (e.g., "admin", "guest")
            password: Password to validate
            interface_type: "CONTROL_PANEL" or "WEB"

        Returns:
            True if credentials are valid and system not locked
        """
        # Initialize tracking for this interface if needed
        if interface_type not in self.failed_attempts:
            self.failed_attempts[interface_type] = 0
            self.is_locked[interface_type] = False

        # Check if locked
        if self.is_locked.get(interface_type, False):
            self._log_session(interface_type, user_id, False)
            return False

        # Validate based on interface type
        is_valid = False

        if interface_type == "CONTROL_PANEL":
            is_valid = self._validate_control_panel(user_id, password)
        elif interface_type == "WEB":
            is_valid = self._validate_web(user_id, password)

        # Handle result
        if is_valid:
            self.failed_attempts[interface_type] = 0
            self._log_session(interface_type, user_id, True)
            return True
        else:
            self.failed_attempts[interface_type] += 1
            self._log_session(interface_type, user_id, False)

            # Check if should lock
            if self.failed_attempts[interface_type] >= self.settings.max_login_attempts:
                self._lock_interface(interface_type)

            return False

    def _validate_control_panel(self, user_id: str, password: str) -> bool:
        """
        Validate control panel credentials (4-digit password)

        Args:
            user_id: "admin" (master) or "guest"
            password: 4-digit password

        Returns:
            True if valid
        """
        if user_id == "admin":
            return password == self.settings.master_password
        elif user_id == "guest":
            # Guest password is optional
            if self.settings.guest_password:
                return password == self.settings.guest_password
            elif password == "0000":
                return True
            return False
        return False

    def _validate_web(self, user_id: str, password: str) -> bool:
        """
        Validate web interface credentials (two-level password)

        Args:
            user_id: User ID
            password: Format "password1:password2" (two 8-char passwords)

        Returns:
            True if valid
        """
        # Parse two-level password
        if ':' not in password:
            return False

        parts = password.split(':', 1)
        if len(parts) != 2:
            return False

        password1, password2 = parts

        # Validate both passwords
        return (password1 == self.settings.web_password_1 and
                password2 == self.settings.web_password_2)

    def _lock_interface(self, interface_type: str):
        """Lock interface and start unlock timer"""
        self.is_locked[interface_type] = True
        print(f"{interface_type} locked due to failed login attempts")

        # Start timer to auto-unlock
        lock_duration = self.settings.system_lock_time

        def unlock_after_delay():
            time.sleep(lock_duration)
            self.unlock_system(interface_type)

        timer = threading.Thread(target=unlock_after_delay, daemon=True)
        timer.start()
        self.lock_timers[interface_type] = timer

    def _log_session(self, interface_type: str, username: str, success: bool):
        """Log login session to database"""
        if not self.storage or not self.storage.db:
            return

        query = """
            INSERT INTO login_sessions
            (interface_type, username, login_successful, failed_attempts)
            VALUES (?, ?, ?, ?)
        """
        self.storage.db.execute_query(
            query,
            (interface_type, username, success, self.failed_attempts.get(interface_type, 0))
        )
        self.storage.db.commit()

    def change_password(self, old_password: str, new_password: str,
                        interface_type: str = "CONTROL_PANEL") -> bool:
        """
        Change password for a given interface

        Args:
            old_password: Current password
            new_password: New password
            interface_type: Which interface password to change

        Returns:
            True if password changed successfully
        """
        # Validate old password first
        if not self.validate_credentials("admin", old_password, interface_type):
            return False

        # Update password based on interface type
        if interface_type == "CONTROL_PANEL":
            self.settings.master_password = new_password
        elif interface_type == "WEB":
            # For web, new_password should be "pass1:pass2"
            if ':' in new_password:
                parts = new_password.split(':', 1)
                if len(parts) == 2:
                    self.settings.web_password_1 = parts[0]
                    self.settings.web_password_2 = parts[1]
                else:
                    return False
            else:
                return False

        return True

    def change_guest_password(self, master_password: str, new_guest_password: str) -> bool:
        """
        Change guest password (requires master password)

        Args:
            master_password: Master password for authorization
            new_guest_password: New guest password (can be empty to disable)

        Returns:
            True if changed successfully
        """
        if master_password != self.settings.master_password:
            return False

        self.settings.guest_password = new_guest_password if new_guest_password else None
        return True

    def unlock_system(self, interface_type: str = None):
        """
        Unlock system (manual or automatic)

        Args:
            interface_type: Specific interface to unlock, or None for all
        """
        if interface_type:
            self.failed_attempts[interface_type] = 0
            self.is_locked[interface_type] = False
            print(f"{interface_type} unlocked")
        else:
            # Unlock all interfaces
            for iface in list(self.failed_attempts.keys()):
                self.failed_attempts[iface] = 0
                self.is_locked[iface] = False
            print("All interfaces unlocked")

    def is_interface_locked(self, interface_type: str) -> bool:
        """Check if a specific interface is locked"""
        return self.is_locked.get(interface_type, False)

    def get_failed_attempts(self, interface_type: str) -> int:
        """Get number of failed attempts for an interface"""
        return self.failed_attempts.get(interface_type, 0)