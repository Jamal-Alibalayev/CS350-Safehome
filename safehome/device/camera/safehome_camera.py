from typing import Optional
import time
from PIL import Image
from .device_camera import DeviceCamera


class SafeHomeCamera:
    """
    SafeHome Camera wrapper class
    Wraps DeviceCamera hardware and provides high-level interface
    Implements camera control with password protection (SRS UC19-25)
    """

    def __init__(
        self,
        camera_id: int,
        name: str,
        location: str,
        password: Optional[str] = None,
        max_attempts: int = 3,
        lockout_seconds: int = 300,
    ):
        """
        Initialize SafeHome Camera

        Args:
            camera_id: Unique camera identifier
            name: Camera name
            location: Physical location description
            password: Optional password for camera access
            max_attempts: How many wrong tries before lock
            lockout_seconds: Lock duration in seconds
        """
        self.camera_id = camera_id
        self.name = name
        self.location = location
        self.password = password
        self.is_enabled = True
        self.max_attempts = max_attempts
        self.lockout_seconds = lockout_seconds
        self.failed_attempts = 0
        self.locked_until = 0.0

        # Create hardware device instance
        self.hardware = DeviceCamera()
        self.hardware.set_id(camera_id)

    def get_id(self) -> int:
        """Get camera ID"""
        return self.camera_id

    def get_name(self) -> str:
        """Get camera name"""
        return self.name

    def get_location(self) -> str:
        """Get camera location"""
        return self.location

    def get_view(self) -> Optional[Image.Image]:
        """
        Get current camera view as PIL Image

        Returns:
            PIL Image if camera is enabled, None otherwise
        """
        if not self.is_enabled or self._is_locked():
            return None

        try:
            return self.hardware.get_view()
        except Exception as e:
            print(f"Error getting camera view: {e}")
            return None

    def pan_left(self) -> bool:
        """
        Pan camera to the left

        Returns:
            True if successful, False if limit reached
        """
        if not self.is_enabled or self._is_locked():
            return False

        try:
            return self.hardware.pan_left()
        except Exception as e:
            print(f"Error panning left: {e}")
            return False

    def pan_right(self) -> bool:
        """
        Pan camera to the right

        Returns:
            True if successful, False if limit reached
        """
        if not self.is_enabled or self._is_locked():
            return False

        try:
            return self.hardware.pan_right()
        except Exception as e:
            print(f"Error panning right: {e}")
            return False

    def tilt_up(self) -> bool:
        """
        Tilt camera up

        Returns:
            True if successful, False if limit reached
        """
        if not self.is_enabled or self._is_locked():
            return False

        try:
            return self.hardware.tilt_up()
        except Exception as e:
            print(f"Error tilting up: {e}")
            return False

    def tilt_down(self) -> bool:
        """
        Tilt camera down

        Returns:
            True if successful, False if limit reached
        """
        if not self.is_enabled or self._is_locked():
            return False

        try:
            return self.hardware.tilt_down()
        except Exception as e:
            print(f"Error tilting down: {e}")
            return False

    def zoom_in(self) -> bool:
        """
        Zoom camera in

        Returns:
            True if successful, False if limit reached
        """
        if not self.is_enabled or self._is_locked():
            return False

        try:
            return self.hardware.zoom_in()
        except Exception as e:
            print(f"Error zooming in: {e}")
            return False

    def zoom_out(self) -> bool:
        """
        Zoom camera out

        Returns:
            True if successful, False if limit reached
        """
        if not self.is_enabled or self._is_locked():
            return False

        try:
            return self.hardware.zoom_out()
        except Exception as e:
            print(f"Error zooming out: {e}")
            return False

    def enable(self):
        """Enable camera (turn on)"""
        self.is_enabled = True

    def disable(self):
        """Disable camera (turn off)"""
        self.is_enabled = False

    def set_password(self, password: Optional[str]):
        """
        Set camera password

        Args:
            password: New password (None to remove password protection)
        """
        self.password = password
        # Reset lock state on password change/removal
        self.failed_attempts = 0
        self.locked_until = 0.0

    def verify_password(self, password: Optional[str]) -> bool:
        """
        Verify camera password

        Args:
            password: Password to verify

        Returns:
            True if password is correct or no password set, False otherwise
        """
        # No password set - allow access
        if self.password is None:
            self.failed_attempts = 0
            self.locked_until = 0.0
            return True

        # Check lock
        if self._is_locked():
            return False

        # Password required
        if self.password == password:
            self.failed_attempts = 0
            return True

        # Wrong password handling
        self.failed_attempts += 1
        if self.failed_attempts >= self.max_attempts:
            self.locked_until = time.time() + self.lockout_seconds
        return False

    def has_password(self) -> bool:
        """Check if camera has password protection"""
        return self.password is not None

    def is_locked(self) -> bool:
        """Public method to check if camera is in lockout state."""
        return self._is_locked()

    def _is_locked(self) -> bool:
        """Check if camera is in lockout state."""
        if self.locked_until and time.time() < self.locked_until:
            return True
        if self.locked_until and time.time() >= self.locked_until:
            # Auto unlock after timeout
            self.locked_until = 0.0
            self.failed_attempts = 0
        return False

    def get_status(self) -> dict:
        """
        Get camera status as dictionary

        Returns:
            Dictionary with camera status information
        """
        return {
            "id": self.camera_id,
            "name": self.name,
            "location": self.location,
            "is_enabled": self.is_enabled,
            "has_password": self.has_password(),
            "pan_angle": getattr(self.hardware, "pan", 0),
            "zoom_level": getattr(self.hardware, "zoom", 2),
        }

    def stop(self):
        """Stop camera hardware thread"""
        if self.hardware:
            self.hardware.stop()

    def __repr__(self):
        return f"SafeHomeCamera(id={self.camera_id}, name='{self.name}', location='{self.location}', enabled={self.is_enabled})"
