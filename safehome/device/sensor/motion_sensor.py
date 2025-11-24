from typing import Optional
from .sensor import Sensor
from .device_motion_detector import DeviceMotionDetector


class MotionSensor(Sensor):
    """
    Motion Sensor wrapper
    Wraps DeviceMotionDetector hardware and provides high-level interface
    """

    def __init__(self, sensor_id: int, location: str, zone_id: Optional[int] = None):
        """
        Initialize Motion Sensor

        Args:
            sensor_id: Unique sensor identifier
            location: Physical location (e.g., "Living Room", "Hallway")
            zone_id: Safety zone this sensor belongs to
        """
        super().__init__(sensor_id, 'MOTION', location, zone_id)

        # Create hardware device instance
        self.hardware = DeviceMotionDetector()
        # Provide metadata so external tools (simulator) can show friendly info
        self.hardware.location = location
        self.hardware.name = location
        self.hardware.is_motion = True

    def read(self) -> bool:
        """
        Read sensor state from hardware
        Only returns True if sensor is armed AND motion is detected

        Returns:
            True if armed and motion detected, False otherwise
        """
        if not self.is_active:
            return False
        return self.hardware.read()

    def arm(self):
        """Arm the sensor (enable motion detection)"""
        self.is_active = True
        self.hardware.arm()

    def disarm(self):
        """Disarm the sensor (disable motion detection)"""
        self.is_active = False
        self.hardware.disarm()

    def test_armed_state(self) -> bool:
        """
        Test if sensor is armed

        Returns:
            True if armed, False otherwise
        """
        return self.hardware.test_armed_state()

    def is_motion_detected(self) -> bool:
        """
        Check if motion is currently detected (regardless of armed state)

        Returns:
            True if motion detected, False otherwise
        """
        return self.hardware.detected

    def simulate_motion(self):
        """Simulate motion detection (for testing)"""
        if hasattr(self.hardware, 'intrude'):
            self.hardware.intrude()

    def simulate_clear(self):
        """Simulate motion clearing (for testing)"""
        if hasattr(self.hardware, 'release'):
            self.hardware.release()
