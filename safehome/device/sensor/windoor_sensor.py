from typing import Optional

from .device_windoor_sensor import DeviceWinDoorSensor
from .sensor import Sensor


class WindowDoorSensor(Sensor):
    """
    Window/Door Sensor wrapper
    Wraps DeviceWinDoorSensor hardware and provides high-level interface
    """

    def __init__(self, sensor_id: int, location: str, zone_id: Optional[int] = None):
        """
        Initialize Window/Door Sensor

        Args:
            sensor_id: Unique sensor identifier
            location: Physical location (e.g., "Front Door", "Living Room Window")
            zone_id: Safety zone this sensor belongs to
        """
        super().__init__(sensor_id, "WINDOOR", location, zone_id)

        # Create hardware device instance
        self.hardware = DeviceWinDoorSensor()

    def read(self) -> bool:
        """
        Read sensor state from hardware
        Only returns True if sensor is armed AND window/door is open

        Returns:
            True if armed and opened, False otherwise
        """
        if not self.is_active:
            return False
        return self.hardware.read()

    def arm(self):
        """Arm the sensor (enable detection)"""
        self.is_active = True
        self.hardware.arm()

    def disarm(self):
        """Disarm the sensor (disable detection)"""
        self.is_active = False
        self.hardware.disarm()

    def test_armed_state(self) -> bool:
        """
        Test if sensor is armed

        Returns:
            True if armed, False otherwise
        """
        return self.hardware.test_armed_state()

    def is_open(self) -> bool:
        """
        Check if window/door is currently open (regardless of armed state)

        Returns:
            True if open, False if closed
        """
        return self.hardware.opened

    def simulate_open(self):
        """Simulate window/door opening (for testing)"""
        if hasattr(self.hardware, "intrude"):
            self.hardware.intrude()

    def simulate_close(self):
        """Simulate window/door closing (for testing)"""
        if hasattr(self.hardware, "release"):
            self.hardware.release()
