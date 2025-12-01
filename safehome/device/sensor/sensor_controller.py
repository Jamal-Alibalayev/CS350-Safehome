from typing import Dict, List, Tuple, Optional
from .sensor import Sensor
from .windoor_sensor import WindowDoorSensor
from .motion_sensor import MotionSensor


class SensorController:
    """
    Sensor Controller manages all sensors in the system
    Provides centralized sensor management, polling, and intrusion detection
    Based on SRS requirements for sensor management
    """

    def __init__(self, storage_manager=None, logger=None):
        """
        Initialize Sensor Controller

        Args:
            storage_manager: StorageManager for persistence
            logger: LogManager for logging events
        """
        self.sensors: Dict[int, Sensor] = {}  # {sensor_id: Sensor instance}
        self.storage = storage_manager
        self.logger = logger
        self._next_sensor_id = 1  # Auto-increment sensor ID

    def add_sensor(
        self, sensor_type: str, location: str, zone_id: Optional[int] = None
    ) -> Sensor:
        """
        Add a new sensor to the system

        Args:
            sensor_type: Type of sensor ('WINDOOR' or 'MOTION')
            location: Physical location description
            zone_id: Optional safety zone ID

        Returns:
            Created sensor instance

        Raises:
            ValueError: If sensor_type is invalid
        """
        sensor_id = self._next_sensor_id
        self._next_sensor_id += 1

        # Create appropriate sensor type
        if sensor_type.upper() == "WINDOOR":
            sensor = WindowDoorSensor(sensor_id, location, zone_id)
        elif sensor_type.upper() == "MOTION":
            sensor = MotionSensor(sensor_id, location, zone_id)
        else:
            raise ValueError(
                f"Invalid sensor type: {sensor_type}. Must be 'WINDOOR' or 'MOTION'"
            )

        # Store sensor
        self.sensors[sensor_id] = sensor

        # Persist to database
        if self.storage:
            self.storage.save_sensor(sensor_id, sensor_type.upper(), location, zone_id)

        # Log event
        if self.logger:
            self.logger.add_log(
                f"Sensor {sensor_id} ({sensor_type}) added at {location}",
                source="SensorController",
            )

        return sensor

    def remove_sensor(self, sensor_id: int) -> bool:
        """
        Remove a sensor from the system

        Args:
            sensor_id: ID of sensor to remove

        Returns:
            True if removed, False if not found
        """
        if sensor_id not in self.sensors:
            return False

        sensor = self.sensors[sensor_id]

        # Disarm before removing
        sensor.disarm()

        # Remove from memory
        del self.sensors[sensor_id]

        # Remove from database
        if self.storage:
            self.storage.delete_sensor(sensor_id)

        # Log event
        if self.logger:
            self.logger.add_log(
                f"Sensor {sensor_id} removed", source="SensorController"
            )

        return True

    def get_sensor(self, sensor_id: int) -> Optional[Sensor]:
        """Get sensor by ID"""
        return self.sensors.get(sensor_id)

    def get_all_sensors(self) -> List[Sensor]:
        """Get list of all sensors"""
        return list(self.sensors.values())

    def get_sensors_by_zone(self, zone_id: int) -> List[Sensor]:
        """
        Get all sensors in a specific zone

        Args:
            zone_id: Zone ID to filter by

        Returns:
            List of sensors in the zone
        """
        return [s for s in self.sensors.values() if s.zone_id == zone_id]

    def get_sensors_by_type(self, sensor_type: str) -> List[Sensor]:
        """
        Get all sensors of a specific type

        Args:
            sensor_type: Type to filter by ('WINDOOR' or 'MOTION')

        Returns:
            List of sensors of that type
        """
        return [
            s for s in self.sensors.values() if s.sensor_type == sensor_type.upper()
        ]

    def arm_sensor(self, sensor_id: int):
        """Arm a specific sensor"""
        sensor = self.get_sensor(sensor_id)
        if sensor:
            sensor.arm()
            if self.logger:
                self.logger.add_log(
                    f"Sensor {sensor_id} armed", source="SensorController"
                )

    def disarm_sensor(self, sensor_id: int):
        """Disarm a specific sensor"""
        sensor = self.get_sensor(sensor_id)
        if sensor:
            sensor.disarm()
            if self.logger:
                self.logger.add_log(
                    f"Sensor {sensor_id} disarmed", source="SensorController"
                )

    def arm_sensors_in_zone(self, zone_id: int):
        """
        Arm all sensors in a specific zone

        Args:
            zone_id: Zone ID
        """
        sensors = self.get_sensors_by_zone(zone_id)
        for sensor in sensors:
            sensor.arm()

        if self.logger:
            self.logger.add_log(
                f"Armed {len(sensors)} sensors in zone {zone_id}",
                source="SensorController",
            )

    def disarm_sensors_in_zone(self, zone_id: int):
        """
        Disarm all sensors in a specific zone

        Args:
            zone_id: Zone ID
        """
        sensors = self.get_sensors_by_zone(zone_id)
        for sensor in sensors:
            sensor.disarm()

        if self.logger:
            self.logger.add_log(
                f"Disarmed {len(sensors)} sensors in zone {zone_id}",
                source="SensorController",
            )

    def arm_sensors(self, sensor_ids: List[int]):
        """
        Arm specific sensors by ID list

        Args:
            sensor_ids: List of sensor IDs to arm
        """
        for sensor_id in sensor_ids:
            self.arm_sensor(sensor_id)

    def disarm_all_sensors(self):
        """Disarm all sensors in the system"""
        for sensor in self.sensors.values():
            sensor.disarm()

        if self.logger:
            self.logger.add_log(
                f"All {len(self.sensors)} sensors disarmed", source="SensorController"
            )

    def close_all_windoor_sensors(self):
        """Ensure all window/door sensors are in a closed state."""
        for sensor in self.sensors.values():
            if isinstance(sensor, WindowDoorSensor):
                sensor.simulate_close()

        if self.logger:
            self.logger.add_log(
                "All window/door sensors set to 'closed' state",
                source="SensorController",
            )

    def poll_sensors(self) -> List[Tuple[int, Sensor]]:
        """
        Poll all active sensors for intrusion detection
        This is the core method for detecting unauthorized access

        Returns:
            List of (sensor_id, sensor) tuples for sensors that are triggered
        """
        detections = []

        for sensor_id, sensor in self.sensors.items():
            # Only check armed sensors
            if sensor.is_active and sensor.read():
                detections.append((sensor_id, sensor))

        return detections

    def check_all_windoor_closed(self) -> Tuple[bool, List[Sensor]]:
        """
        Check if all window/door sensors are closed
        Required before arming system (SRS UC8, UC9)

        Returns:
            Tuple of (all_closed: bool, open_sensors: List[Sensor])
        """
        windoor_sensors = self.get_sensors_by_type("WINDOOR")
        open_sensors = []

        for sensor in windoor_sensors:
            if isinstance(sensor, WindowDoorSensor) and sensor.is_open():
                open_sensors.append(sensor)

        all_closed = len(open_sensors) == 0
        return all_closed, open_sensors

    def get_sensor_status(self, sensor_id: int) -> Optional[dict]:
        """
        Get status of a specific sensor

        Args:
            sensor_id: Sensor ID

        Returns:
            Status dictionary or None if not found
        """
        sensor = self.get_sensor(sensor_id)
        if sensor:
            return sensor.get_status()
        return None

    def get_all_sensor_statuses(self) -> List[dict]:
        """
        Get status of all sensors

        Returns:
            List of status dictionaries
        """
        return [sensor.get_status() for sensor in self.sensors.values()]

    def load_sensors_from_storage(self):
        """Load sensors from database storage"""
        if not self.storage:
            return

        sensor_data = self.storage.load_all_sensors()

        for data in sensor_data:
            sensor_id = data["sensor_id"]
            sensor_type = data["sensor_type"]
            location = data["sensor_location"]
            zone_id = data.get("zone_id")

            # Update next ID
            if sensor_id >= self._next_sensor_id:
                self._next_sensor_id = sensor_id + 1

            # Create sensor
            if sensor_type == "WINDOOR":
                sensor = WindowDoorSensor(sensor_id, location, zone_id)
            elif sensor_type == "MOTION":
                sensor = MotionSensor(sensor_id, location, zone_id)
            else:
                continue

            self.sensors[sensor_id] = sensor

        if self.logger:
            self.logger.add_log(
                f"Loaded {len(sensor_data)} sensors from storage",
                source="SensorController",
            )
