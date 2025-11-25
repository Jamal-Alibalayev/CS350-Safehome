from abc import ABC, abstractmethod
from typing import Optional


class Sensor(ABC):
    """
    Abstract base class for all sensors
    Wraps hardware sensor implementations and provides common interface
    """

    def __init__(self, sensor_id: int, sensor_type: str, location: str, zone_id: Optional[int] = None):
        """
        Initialize Sensor

        Args:
            sensor_id: Unique sensor identifier
            sensor_type: Type of sensor (WINDOOR or MOTION)
            location: Physical location description
            zone_id: Safety zone this sensor belongs to
        """
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.location = location
        self.zone_id = zone_id
        self.is_active = False  # Whether sensor is armed/active
        self.hardware = None    # Hardware device instance

    @abstractmethod
    def read(self) -> bool:
        """
        Read sensor state from hardware

        Returns:
            True if sensor is triggered (intrusion detected), False otherwise
        """
        pass

    @abstractmethod
    def arm(self):
        """Arm/activate the sensor"""
        pass

    @abstractmethod
    def disarm(self):
        """Disarm/deactivate the sensor"""
        pass

    @abstractmethod
    def test_armed_state(self) -> bool:
        """
        Test if sensor is armed

        Returns:
            True if armed, False otherwise
        """
        pass

    def get_id(self) -> int:
        """Get sensor ID"""
        return self.sensor_id

    def get_type(self) -> str:
        """Get sensor type"""
        return self.sensor_type

    def get_location(self) -> str:
        """Get sensor location"""
        return self.location

    def get_zone_id(self) -> Optional[int]:
        """Get zone ID"""
        return self.zone_id

    def set_zone_id(self, zone_id: Optional[int]):
        """Set zone ID"""
        self.zone_id = zone_id

    def get_status(self) -> dict:
        """
        Get sensor status as dictionary

        Returns:
            Dictionary with sensor status information
        """
        return {
            'id': self.sensor_id,
            'type': self.sensor_type,
            'location': self.location,
            'zone_id': self.zone_id,
            'is_active': self.is_active,
            'is_triggered': self.read() if self.is_active else False
        }

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.sensor_id}, location='{self.location}', active={self.is_active})"
