from typing import List, Optional


class SafetyZone:
    """
    Represents a physical security zone (e.g., Living Room, Bedrooms)
    Used to group multiple sensors for selective arming/disarming
    Based on SRS UC10, UC12, UC13, UC14, UC15
    """

    def __init__(self, zone_id: Optional[int], name: str):
        """
        Initialize SafetyZone

        Args:
            zone_id: Unique zone identifier (None for new zones)
            name: Human-readable zone name
        """
        self.zone_id = zone_id
        self.name = name
        self.sensors: List[int] = []  # List of sensor IDs in this zone
        self.is_armed: bool = False  # Armed status of this zone

    def add_sensor(self, sensor_id: int):
        """
        Add sensor ID to this zone

        Args:
            sensor_id: ID of sensor to add
        """
        if sensor_id not in self.sensors:
            self.sensors.append(sensor_id)

    def remove_sensor(self, sensor_id: int):
        """
        Remove sensor ID from this zone

        Args:
            sensor_id: ID of sensor to remove
        """
        if sensor_id in self.sensors:
            self.sensors.remove(sensor_id)

    def get_sensors(self) -> List[int]:
        """Get list of sensor IDs in this zone"""
        return self.sensors.copy()

    def arm(self):
        """Arm this zone (activate all sensors)"""
        self.is_armed = True

    def disarm(self):
        """Disarm this zone (deactivate all sensors)"""
        self.is_armed = False

    def to_dict(self) -> dict:
        """Convert zone to dictionary"""
        return {
            "zone_id": self.zone_id,
            "name": self.name,
            "sensors": self.sensors,
            "is_armed": self.is_armed,
        }

    def __repr__(self):
        return f"SafetyZone(id={self.zone_id}, name='{self.name}', sensors={self.sensors}, armed={self.is_armed})"
