from typing import Dict, List, Optional
from PIL import Image
from .safehome_camera import SafeHomeCamera


class CameraController:
    """
    Camera Controller manages all cameras in the system
    Provides centralized camera management with password protection
    Based on SRS requirements UC19-25 for camera access control
    """

    def __init__(self, storage_manager=None, logger=None):
        """
        Initialize Camera Controller

        Args:
            storage_manager: StorageManager for persistence
            logger: LogManager for logging events
        """
        self.cameras: Dict[int, SafeHomeCamera] = {}  # {camera_id: SafeHomeCamera instance}
        self.storage = storage_manager
        self.logger = logger
        self._next_camera_id = 1  # Auto-increment camera ID

    def add_camera(self, name: str, location: str, password: Optional[str] = None) -> SafeHomeCamera:
        """
        Add a new camera to the system

        Args:
            name: Camera name
            location: Physical location description
            password: Optional password for camera access

        Returns:
            Created camera instance
        """
        camera_id = self._next_camera_id
        self._next_camera_id += 1

        # Create camera
        camera = SafeHomeCamera(camera_id, name, location, password)

        # Store camera
        self.cameras[camera_id] = camera

        # Persist to database
        if self.storage:
            self.storage.save_camera(camera_id, name, location, password)

        # Log event
        if self.logger:
            self.logger.add_log(
                f"Camera {camera_id} ({name}) added at {location}",
                source="CameraController"
            )

        return camera

    def remove_camera(self, camera_id: int) -> bool:
        """
        Remove a camera from the system

        Args:
            camera_id: ID of camera to remove

        Returns:
            True if removed, False if not found
        """
        if camera_id not in self.cameras:
            return False

        camera = self.cameras[camera_id]

        # Stop camera hardware
        camera.stop()

        # Remove from memory
        del self.cameras[camera_id]

        # Remove from database
        if self.storage:
            self.storage.delete_camera(camera_id)

        # Log event
        if self.logger:
            self.logger.add_log(
                f"Camera {camera_id} removed",
                source="CameraController"
            )

        return True

    def get_camera(self, camera_id: int) -> Optional[SafeHomeCamera]:
        """Get camera by ID"""
        return self.cameras.get(camera_id)

    def get_all_cameras(self) -> List[SafeHomeCamera]:
        """Get list of all cameras"""
        return list(self.cameras.values())

    def get_camera_view(self, camera_id: int, password: Optional[str] = None) -> Optional[Image.Image]:
        """
        Get camera view with password verification
        Implements SRS UC19-25 camera password protection

        Args:
            camera_id: Camera ID
            password: Password for camera access (if required)

        Returns:
            PIL Image if access granted, None otherwise
        """
        camera = self.get_camera(camera_id)
        if not camera:
            if self.logger:
                self.logger.add_log(
                    f"Camera access denied: Camera {camera_id} not found",
                    level="WARNING",
                    source="CameraController"
                )
            return None

        # Check password if camera has one
        if camera.has_password():
            if not camera.verify_password(password):
                if self.logger:
                    self.logger.add_log(
                        f"Camera {camera_id} access denied: Invalid password",
                        level="WARNING",
                        source="CameraController"
                    )
                return None

        # Get camera view
        view = camera.get_view()

        # Log successful access
        if view and self.logger:
            self.logger.add_log(
                f"Camera {camera_id} view accessed",
                source="CameraController"
            )

        return view

    def pan_camera(self, camera_id: int, direction: str, password: Optional[str] = None) -> bool:
        """
        Pan camera left or right with password verification

        Args:
            camera_id: Camera ID
            direction: 'left' or 'right'
            password: Password for camera access (if required)

        Returns:
            True if successful, False otherwise
        """
        camera = self.get_camera(camera_id)
        if not camera:
            return False

        # Check password if camera has one
        if camera.has_password() and not camera.verify_password(password):
            if self.logger:
                self.logger.add_log(
                    f"Camera {camera_id} pan denied: Invalid password",
                    level="WARNING",
                    source="CameraController"
                )
            return False

        # Pan camera
        success = False
        if direction.lower() == 'left':
            success = camera.pan_left()
        elif direction.lower() == 'right':
            success = camera.pan_right()

        # Log action
        if success and self.logger:
            self.logger.add_log(
                f"Camera {camera_id} panned {direction}",
                source="CameraController"
            )

        return success

    def zoom_camera(self, camera_id: int, direction: str, password: Optional[str] = None) -> bool:
        """
        Zoom camera in or out with password verification

        Args:
            camera_id: Camera ID
            direction: 'in' or 'out'
            password: Password for camera access (if required)

        Returns:
            True if successful, False otherwise
        """
        camera = self.get_camera(camera_id)
        if not camera:
            return False

        # Check password if camera has one
        if camera.has_password() and not camera.verify_password(password):
            if self.logger:
                self.logger.add_log(
                    f"Camera {camera_id} zoom denied: Invalid password",
                    level="WARNING",
                    source="CameraController"
                )
            return False

        # Zoom camera
        success = False
        if direction.lower() == 'in':
            success = camera.zoom_in()
        elif direction.lower() == 'out':
            success = camera.zoom_out()

        # Log action
        if success and self.logger:
            self.logger.add_log(
                f"Camera {camera_id} zoomed {direction}",
                source="CameraController"
            )

        return success

    def enable_camera(self, camera_id: int) -> bool:
        """
        Enable a camera

        Args:
            camera_id: Camera ID

        Returns:
            True if enabled, False if not found
        """
        camera = self.get_camera(camera_id)
        if not camera:
            return False

        camera.enable()

        if self.logger:
            self.logger.add_log(
                f"Camera {camera_id} enabled",
                source="CameraController"
            )

        return True

    def disable_camera(self, camera_id: int) -> bool:
        """
        Disable a camera

        Args:
            camera_id: Camera ID

        Returns:
            True if disabled, False if not found
        """
        camera = self.get_camera(camera_id)
        if not camera:
            return False

        camera.disable()

        if self.logger:
            self.logger.add_log(
                f"Camera {camera_id} disabled",
                source="CameraController"
            )

        return True

    def set_camera_password(self, camera_id: int, password: Optional[str]) -> bool:
        """
        Set or change camera password

        Args:
            camera_id: Camera ID
            password: New password (None to remove password protection)

        Returns:
            True if successful, False if camera not found
        """
        camera = self.get_camera(camera_id)
        if not camera:
            return False

        camera.set_password(password)

        # Update in database
        if self.storage:
            self.storage.update_camera_password(camera_id, password)

        # Log event
        if self.logger:
            action = "set" if password else "removed"
            self.logger.add_log(
                f"Camera {camera_id} password {action}",
                source="CameraController"
            )

        return True

    def get_camera_status(self, camera_id: int) -> Optional[dict]:
        """
        Get status of a specific camera

        Args:
            camera_id: Camera ID

        Returns:
            Status dictionary or None if not found
        """
        camera = self.get_camera(camera_id)
        if camera:
            return camera.get_status()
        return None

    def get_all_camera_statuses(self) -> List[dict]:
        """
        Get status of all cameras

        Returns:
            List of status dictionaries
        """
        return [camera.get_status() for camera in self.cameras.values()]

    def load_cameras_from_storage(self):
        """Load cameras from database storage"""
        if not self.storage:
            return

        camera_data = self.storage.load_all_cameras()

        for data in camera_data:
            camera_id = data['camera_id']
            name = data['camera_name']
            location = data['camera_location']
            password = data.get('camera_password')

            # Update next ID
            if camera_id >= self._next_camera_id:
                self._next_camera_id = camera_id + 1

            # Create camera
            camera = SafeHomeCamera(camera_id, name, location, password)
            self.cameras[camera_id] = camera

        if self.logger:
            self.logger.add_log(
                f"Loaded {len(camera_data)} cameras from storage",
                source="CameraController"
            )

    def shutdown(self):
        """Stop all camera hardware threads"""
        for camera in self.cameras.values():
            camera.stop()

        if self.logger:
            self.logger.add_log(
                "All cameras stopped",
                source="CameraController"
            )
