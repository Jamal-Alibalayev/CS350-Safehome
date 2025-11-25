"""
Web Interface for SafeHome System
Basic structure for future web-based control
Currently a placeholder for Phase 4/5 implementation
"""

from typing import Optional
from safehome.core.system import System
from safehome.configuration.safehome_mode import SafeHomeMode


class WebInterface:
    """
    Web Interface for SafeHome System
    Provides web-based access to security and surveillance functions
    Requires two 8-character passwords for authentication (SRS requirement)
    """

    def __init__(self, system: System):
        """
        Initialize Web Interface

        Args:
            system: System instance to control
        """
        self.system = system
        self.pages = {}
        self.is_authenticated = False
        self.current_user = None

    def authenticate(self, password1: str, password2: str) -> bool:
        """
        Authenticate web user with two passwords
        SRS requires two 8-character passwords for web interface

        Args:
            password1: First password (8 characters)
            password2: Second password (8 characters)

        Returns:
            True if authentication successful, False otherwise
        """
        if len(password1) != 8 or len(password2) != 8:
            return False

        # Combine passwords for system login
        combined_password = f"{password1}:{password2}"
        success = self.system.login("admin", combined_password, "WEB")

        if success:
            self.is_authenticated = True
            self.current_user = "admin"

        return success

    def logout(self):
        """Logout current user"""
        self.is_authenticated = False
        self.current_user = None

    # --- Security Functions (SRS Security Page) ---

    def arm_system(self, mode: str) -> dict:
        """
        Arm system in specified mode

        Args:
            mode: Mode name ("HOME", "AWAY", "OVERNIGHT", "EXTENDED")

        Returns:
            Status dictionary
        """
        if not self.is_authenticated:
            return {"success": False, "error": "Not authenticated"}

        try:
            mode_enum = SafeHomeMode[mode.upper()]
            success = self.system.arm_system(mode_enum)
            return {
                "success": success,
                "mode": mode,
                "message": "System armed" if success else "Cannot arm - windows/doors open"
            }
        except KeyError:
            return {"success": False, "error": f"Invalid mode: {mode}"}

    def disarm_system(self) -> dict:
        """
        Disarm the system

        Returns:
            Status dictionary
        """
        if not self.is_authenticated:
            return {"success": False, "error": "Not authenticated"}

        self.system.disarm_system()
        return {"success": True, "message": "System disarmed"}

    def get_sensor_status(self) -> dict:
        """
        Get status of all sensors

        Returns:
            Dictionary with sensor information
        """
        if not self.is_authenticated:
            return {"success": False, "error": "Not authenticated"}

        sensors = self.system.sensor_controller.get_all_sensor_statuses()
        return {
            "success": True,
            "sensors": sensors,
            "count": len(sensors)
        }

    def arm_zone(self, zone_id: int) -> dict:
        """
        Arm specific safety zone

        Args:
            zone_id: Zone ID to arm

        Returns:
            Status dictionary
        """
        if not self.is_authenticated:
            return {"success": False, "error": "Not authenticated"}

        self.system.arm_zone(zone_id)
        return {"success": True, "message": f"Zone {zone_id} armed"}

    def disarm_zone(self, zone_id: int) -> dict:
        """
        Disarm specific safety zone

        Args:
            zone_id: Zone ID to disarm

        Returns:
            Status dictionary
        """
        if not self.is_authenticated:
            return {"success": False, "error": "Not authenticated"}

        self.system.disarm_zone(zone_id)
        return {"success": True, "message": f"Zone {zone_id} disarmed"}

    # --- Surveillance Functions (SRS Surveillance Page) ---

    def get_camera_list(self) -> dict:
        """
        Get list of all cameras

        Returns:
            Dictionary with camera information
        """
        if not self.is_authenticated:
            return {"success": False, "error": "Not authenticated"}

        cameras = self.system.camera_controller.get_all_camera_statuses()
        return {
            "success": True,
            "cameras": cameras,
            "count": len(cameras)
        }

    def get_camera_view(self, camera_id: int, password: Optional[str] = None) -> dict:
        """
        Get camera view (requires camera password if set)

        Args:
            camera_id: Camera ID
            password: Camera password (if required)

        Returns:
            Status dictionary with image data
        """
        if not self.is_authenticated:
            return {"success": False, "error": "Not authenticated"}

        image = self.system.camera_controller.get_camera_view(camera_id, password)
        if image:
            return {
                "success": True,
                "camera_id": camera_id,
                "has_image": True
            }
        else:
            return {
                "success": False,
                "error": "Access denied or camera unavailable"
            }

    def control_camera(self, camera_id: int, action: str, password: Optional[str] = None) -> dict:
        """
        Control camera (pan/zoom)

        Args:
            camera_id: Camera ID
            action: Action to perform ("pan_left", "pan_right", "zoom_in", "zoom_out")
            password: Camera password (if required)

        Returns:
            Status dictionary
        """
        if not self.is_authenticated:
            return {"success": False, "error": "Not authenticated"}

        if action in ["pan_left", "pan_right"]:
            direction = action.split("_")[1]
            success = self.system.camera_controller.pan_camera(camera_id, direction, password)
        elif action in ["zoom_in", "zoom_out"]:
            direction = action.split("_")[1]
            success = self.system.camera_controller.zoom_camera(camera_id, direction, password)
        else:
            return {"success": False, "error": f"Invalid action: {action}"}

        return {
            "success": success,
            "message": f"Camera {camera_id} {action}" if success else "Action failed"
        }

    # --- Configuration Functions ---

    def get_system_status(self) -> dict:
        """
        Get overall system status

        Returns:
            Dictionary with system information
        """
        if not self.is_authenticated:
            return {"success": False, "error": "Not authenticated"}

        status = self.system.get_system_status()
        status["success"] = True
        return status

    def get_event_logs(self, limit: int = 50) -> dict:
        """
        Get recent event logs

        Args:
            limit: Maximum number of logs to return

        Returns:
            Dictionary with log entries
        """
        if not self.is_authenticated:
            return {"success": False, "error": "Not authenticated"}

        logs = self.system.config.storage.get_logs(limit=limit)
        return {
            "success": True,
            "logs": logs,
            "count": len(logs)
        }

    def change_password(self, old_password: str, new_password1: str, new_password2: str) -> dict:
        """
        Change web interface password

        Args:
            old_password: Current password (password1:password2 format)
            new_password1: New first password (8 characters)
            new_password2: New second password (8 characters)

        Returns:
            Status dictionary
        """
        if not self.is_authenticated:
            return {"success": False, "error": "Not authenticated"}

        if len(new_password1) != 8 or len(new_password2) != 8:
            return {"success": False, "error": "Passwords must be 8 characters"}

        new_password = f"{new_password1}:{new_password2}"
        success = self.system.change_password(old_password, new_password, "WEB")

        return {
            "success": success,
            "message": "Password changed" if success else "Password change failed"
        }

    # --- Page Rendering Placeholders (for future Flask/Django implementation) ---

    def show_login_page(self):
        """Placeholder for login page rendering"""
        return {
            "page": "login",
            "title": "SafeHome Web Interface - Login",
            "requires_passwords": 2,
            "password_length": 8
        }

    def show_main_page(self):
        """Placeholder for main dashboard page"""
        if not self.is_authenticated:
            return self.show_login_page()

        return {
            "page": "dashboard",
            "title": "SafeHome - Dashboard",
            "system_status": self.get_system_status()
        }

    def show_security_page(self):
        """Placeholder for security control page"""
        if not self.is_authenticated:
            return self.show_login_page()

        return {
            "page": "security",
            "title": "SafeHome - Security",
            "sensors": self.get_sensor_status(),
            "current_mode": self.system.config.current_mode.name
        }

    def show_surveillance_page(self):
        """Placeholder for surveillance page"""
        if not self.is_authenticated:
            return self.show_login_page()

        return {
            "page": "surveillance",
            "title": "SafeHome - Surveillance",
            "cameras": self.get_camera_list()
        }
