import threading
import time
from typing import Optional, List
from ..configuration.configuration_manager import ConfigurationManager
from ..configuration.safehome_mode import SafeHomeMode
from ..device.sensor.sensor_controller import SensorController
from ..device.camera.camera_controller import CameraController
from ..device.alarm.alarm import Alarm


class System:
    """
    SafeHome's core System class
    Integrates and controls all subsystems
    Implements main system logic for security monitoring
    Based on SRS requirements for system control and intrusion detection
    """

    def __init__(self, db_path: str = "data/safehome.db"):
        """
        Initialize System

        Args:
            db_path: Path to SQLite database
        """
        # 1. Configuration Manager initialization
        self.config = ConfigurationManager(db_path=db_path)

        # 2. Device Controllers initialization
        self.sensor_controller = SensorController(
            storage_manager=self.config.storage,
            logger=self.config.logger
        )
        self.camera_controller = CameraController(
            storage_manager=self.config.storage,
            logger=self.config.logger,
            login_manager=self.config.login_manager
        )
        self.alarm = Alarm(duration=self.config.settings.alarm_duration)

        # 3. State
        self.is_running = False
        self.is_system_locked = False

        # 4. Polling Thread
        self._polling_thread: Optional[threading.Thread] = None
        self._stop_polling = threading.Event()

        # Load existing sensors and cameras from storage
        self.sensor_controller.load_sensors_from_storage()
        self.camera_controller.load_cameras_from_storage()

    def turn_on(self):
        """Turn on the system"""
        self.is_running = True
        self._start_sensor_polling()
        self.config.logger.add_log("System turned ON", source="System")

    def turn_off(self):
        """Turn off the system"""
        self.is_running = False
        self._stop_sensor_polling()
        self.config.save_configuration()
        self.config.logger.add_log("System turned OFF", source="System")

    def reset(self):
        """Reset the system"""
        self.turn_off()
        time.sleep(1)
        self.turn_on()
        self.config.logger.add_log("System RESET", source="System")

    def shutdown(self):
        """
        Gracefully shutdown the system
        Stops all threads, saves state, and closes connections
        """
        self.turn_off()
        self.camera_controller.shutdown()
        self.config.shutdown()

    # ===== Sensor Polling =====
    def _start_sensor_polling(self):
        """Start sensor polling (background thread)"""
        self._stop_polling.clear()
        self._polling_thread = threading.Thread(
            target=self._sensor_polling_loop,
            daemon=True
        )
        self._polling_thread.start()

    def _stop_sensor_polling(self):
        """Stop sensor polling thread"""
        self._stop_polling.set()
        if self._polling_thread and self._polling_thread.is_alive():
            self._polling_thread.join(timeout=2)

    def _sensor_polling_loop(self):
        """
        Periodically poll sensors to detect intrusions
        Runs in separate thread while system is running
        """
        while self.is_running and not self._stop_polling.is_set():
            detections = self.sensor_controller.poll_sensors()
            if detections:
                for sensor_id, sensor in detections:
                    self._handle_intrusion(sensor)
            time.sleep(1)  # Poll every 1 second

    def _handle_intrusion(self, sensor):
        """
        Handle intrusion detection
        Logs event and starts entry delay countdown

        Args:
            sensor: Sensor that detected intrusion
        """
        self.config.logger.add_log(
            f"INTRUSION DETECTED at {sensor.location}",
            level="ALARM",
            source="System",
            sensor_id=sensor.sensor_id,
            zone_id=sensor.zone_id
        )

        # Start entry delay countdown
        self._start_entry_delay_countdown(sensor)

    def _start_entry_delay_countdown(self, sensor):
        """
        Start entry delay countdown before triggering alarm
        Allows user time to disarm system (SRS UC8, UC9)

        Args:
            sensor: Sensor that detected intrusion
        """
        delay = self.config.settings.entry_delay
        self.config.logger.add_log(
            f"Entry delay: {delay} seconds",
            source="System"
        )

        # Entry delay thread
        def countdown():
            time.sleep(delay)
            # If sensor still detecting and system still armed, trigger alarm
            if self.is_running and sensor.is_active and sensor.read():
                self._trigger_alarm(sensor)

        threading.Thread(target=countdown, daemon=True).start()

    def _trigger_alarm(self, sensor):
        """
        Trigger alarm and call monitoring service

        Args:
            sensor: Sensor that triggered alarm
        """
        self.alarm.ring()
        self.call_monitoring_service(sensor)

    def call_monitoring_service(self, sensor):
        """
        Call monitoring service (simulation)
        In real system, would dial monitoring phone number

        Args:
            sensor: Sensor that triggered alarm
        """
        phone = self.config.settings.monitoring_phone
        self.config.logger.add_log(
            f"Calling monitoring service at {phone} - Intrusion at {sensor.location}",
            level="ALARM",
            source="System"
        )
        print(f"📞 Calling {phone}: INTRUSION at {sensor.location}")

    # ===== Mode Control =====
    def arm_system(self, mode: SafeHomeMode):
        """
        Arm system in specified mode
        Activates sensors according to mode configuration (SRS UC8, UC9, UC16)

        Args:
            mode: SafeHomeMode to activate

        Returns:
            True if armed successfully, False if windows/doors are open
        """
        # Check if all window/door sensors are closed (SRS requirement)
        all_closed, open_sensors = self.sensor_controller.check_all_windoor_closed()
        if not all_closed:
            self.config.logger.add_log(
                f"Cannot arm: {len(open_sensors)} windows/doors are open",
                level="WARNING",
                source="System"
            )
            return False

        # Set mode
        self.config.set_mode(mode)

        # Activate sensors for this mode
        sensor_ids = self._get_sensors_for_mode(mode)
        for sensor_id in sensor_ids:
            sensor = self.sensor_controller.get_sensor(sensor_id)
            if sensor:
                sensor.arm()

        self.config.logger.add_log(
            f"System ARMED in {mode.name} mode",
            source="System"
        )
        return True

    def disarm_system(self):
        """
        Disarm the system
        Deactivates all sensors and stops alarm
        """
        self.sensor_controller.disarm_all_sensors()
        self.config.set_mode(SafeHomeMode.DISARMED)
        self.alarm.stop()
        self.config.logger.add_log("System DISARMED", source="System")

    def arm_zone(self, zone_id: int):
        """
        Arm specific safety zone
        Activates all sensors in the zone (SRS UC10, UC12-15)

        Args:
            zone_id: Zone ID to arm
        """
        self.sensor_controller.arm_sensors_in_zone(zone_id)
        zone = self.config.get_safety_zone(zone_id)
        if zone:
            zone.arm()
            self.config.logger.add_log(
                f"Zone {zone.name} ARMED",
                source="System"
            )

    def disarm_zone(self, zone_id: int):
        """
        Disarm specific safety zone
        Deactivates all sensors in the zone

        Args:
            zone_id: Zone ID to disarm
        """
        self.sensor_controller.disarm_sensors_in_zone(zone_id)
        zone = self.config.get_safety_zone(zone_id)
        if zone:
            zone.disarm()
            self.config.logger.add_log(
                f"Zone {zone.name} DISARMED",
                source="System"
            )

    # ===== Login Control =====
    def login(self, user_id: str, password: str, interface_type: str = "CONTROL_PANEL") -> bool:
        """
        Attempt login
        Validates credentials and handles lockout

        Args:
            user_id: User identifier (e.g., "admin", "guest")
            password: Password to verify
            interface_type: Interface type ("CONTROL_PANEL" or "WEB")

        Returns:
            True if login successful, False otherwise
        """
        return self.config.login_manager.validate_credentials(
            user_id, password, interface_type
        )

    def change_password(self, old_password: str, new_password: str, interface_type: str = "CONTROL_PANEL") -> bool:
        """
        Change password

        Args:
            old_password: Current password
            new_password: New password
            interface_type: Interface type ("CONTROL_PANEL" or "WEB")

        Returns:
            True if password changed successfully, False otherwise
        """
        changed = self.config.login_manager.change_password(
            old_password, new_password, interface_type
        )
        if changed:
            # Persist and notify
            self.config.save_configuration()
            self.config.logger.add_log(
                f"{interface_type} password changed",
                level="INFO",
                source="System"
            )
            if interface_type == "CONTROL_PANEL":
                self._send_password_change_alert()
        return changed

    def _send_password_change_alert(self) -> bool:
        """Send an email alert when the admin (control panel) password changes."""
        return self.config.send_email_alert(
            "SafeHome password changed",
            "Your SafeHome control panel password was changed.\n"
            "If you did not make this change, please reset it immediately."
        )

    # ===== Helper Methods =====
    def _get_sensors_for_mode(self, mode: SafeHomeMode) -> List[int]:
        """
        Get sensor IDs assigned to specific mode

        Args:
            mode: SafeHomeMode

        Returns:
            List of sensor IDs for this mode
        """
        mode_name = SafeHomeMode.get_db_mode_name(mode)
        return self.config.storage.get_sensors_for_mode(mode_name)

    def get_system_status(self) -> dict:
        """
        Get comprehensive system status

        Returns:
            Dictionary with system status information
        """
        return {
            'is_running': self.is_running,
            'is_locked': self.is_system_locked,
            'current_mode': self.config.current_mode.name,
            'alarm_active': self.alarm.is_active(),
            'num_sensors': len(self.sensor_controller.sensors),
            'num_cameras': len(self.camera_controller.cameras),
            'num_active_sensors': sum(1 for s in self.sensor_controller.sensors.values() if s.is_active),
        }

    def __repr__(self):
        return f"System(running={self.is_running}, mode={self.config.current_mode.name})"
