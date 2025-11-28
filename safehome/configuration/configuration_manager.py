from typing import List, Optional
from .system_settings import SystemSettings
from .storage_manager import StorageManager
from .log_manager import LogManager
from .login_manager import LoginManager
from .safehome_mode import SafeHomeMode
from .safety_zone import SafetyZone
import smtplib
from email.message import EmailMessage


class ConfigurationManager:
    """
    Configuration Subsystem Facade
    Central access point for all configuration-related operations
    Integrates with database for persistent storage
    """

    def __init__(self, db_path: str = "data/safehome.db"):
        """
        Initialize Configuration Manager

        Args:
            db_path: Path to SQLite database file
        """
        # 1. Initialize Database Manager
        from safehome.database.db_manager import DatabaseManager
        self.db_manager = DatabaseManager(db_path)
        self.db_manager.connect()
        self.db_manager.initialize_schema()

        # 2. Initialize Storage Manager with DB
        self.storage = StorageManager(self.db_manager)

        # 3. Initialize System Settings (load from DB or use defaults)
        self.settings = SystemSettings()
        loaded_data = self.storage.load_settings()
        if loaded_data:
            self.settings.update_settings(**loaded_data)

        # 4. Initialize Log Manager
        self.logger = LogManager()
        self.logger.add_log("System configuration loaded", source="ConfigManager")
        # Backward-compatible alias
        self.log_manager = self.logger

        # 5. Initialize Login Manager
        self.login_manager = LoginManager(self.settings, self.storage)

        # 6. Initialize Safety Zones in DB if they don't exist
        if not self.storage.load_all_safety_zones():
            self.logger.add_log("No safety zones found in DB, creating defaults.", source="ConfigManager")
            zone1 = SafetyZone(None, "Living Room")
            zone2 = SafetyZone(None, "Bedroom")
            self.storage.save_safety_zone(zone1)
            self.storage.save_safety_zone(zone2)

        # 7. Load SafeHome Modes from database
        self.modes = self._load_safehome_modes()

        # 8. Current state
        self.current_mode = SafeHomeMode.DISARMED

        # 9. UI Callbacks
        self.zone_update_callbacks = []

    def register_zone_update_callback(self, callback):
        """Register a callback function to be called when zones are updated."""
        self.zone_update_callbacks.append(callback)

    def _notify_zone_update(self):
        """Notify all registered callbacks about a zone update."""
        for callback in self.zone_update_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error in zone update callback: {e}")

    def send_email_alert(self, subject: str, body: str) -> bool:
        """
        Send an email alert using SMTP settings

        Returns:
            True if sent, False otherwise
        """
        settings = self.settings
        if not settings.alert_email:
            self.logger.add_log("Email alert skipped: no alert_email configured",
                                level="WARNING", source="ConfigManager")
            return False
        try:
            port = int(settings.smtp_port) if settings.smtp_port else 587
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = settings.smtp_user
            msg["To"] = settings.alert_email
            msg.set_content(body)

            with smtplib.SMTP(settings.smtp_host, port, timeout=10) as server:
                server.starttls()
                server.login(settings.smtp_user, settings.smtp_password)
                server.send_message(msg)
            self.logger.add_log(f"Alert email sent to {settings.alert_email}",
                                source="ConfigManager")
            return True
        except Exception as e:
            self.logger.add_log(f"Email alert failed: {e}", level="ERROR", source="ConfigManager")
            print(f"[Email] Failed to send alert: {e}")
            return False

    def _load_safehome_modes(self) -> dict:
        """Load SafeHome modes from database"""
        modes_data = self.db_manager.get_safehome_modes()
        modes = {}
        for mode_row in modes_data:
            mode_name = mode_row['mode_name']
            modes[mode_name] = {
                'id': mode_row['mode_id'],
                'name': mode_name,
                'description': mode_row['description']
            }
        return modes

    def save_configuration(self):
        """Save all configuration to database"""
        self.storage.save_settings(self.settings)
        self.logger.add_log("Configuration saved", source="ConfigManager")

    def reset_configuration(self):
        """Reset all system settings to their default values"""
        # 1. Reset settings to default by creating a new SystemSettings instance
        self.settings = SystemSettings()

        # 2. Delete all existing safety zones from the database
        self.storage.delete_all_safety_zones()

        # 3. Re-create the default safety zones in the database
        zone1 = SafetyZone(None, "Living Room")
        zone2 = SafetyZone(None, "Bedroom")
        self.storage.save_safety_zone(zone1)
        self.storage.save_safety_zone(zone2)

        # 4. Clear all camera passwords (reset to no protection)
        try:
            self.storage.clear_camera_passwords()
        except Exception as e:
            self.logger.add_log(f"Failed to clear camera passwords on reset: {e}",
                                level="ERROR", source="ConfigManager")

        # 5. Save the new default configuration to the database
        self.save_configuration()

        self.logger.add_log("System configuration has been reset to defaults",
                            level="WARNING", source="ConfigManager")
        self._notify_zone_update()

    # ===== Mode Management =====

    def set_mode(self, mode: SafeHomeMode):
        """Change system mode"""
        self.current_mode = mode
        self.logger.add_log(f"System mode changed to {mode.name}", source="ConfigManager")

    def get_mode(self) -> SafeHomeMode:
        """Get current system mode"""
        return self.current_mode

    def get_safehome_modes(self) -> dict:
        """Get all available SafeHome modes"""
        return self.modes

    def get_sensors_for_mode(self, mode_name: str) -> List[int]:
        """Get list of sensor IDs configured for a given mode"""
        return self.storage.get_sensors_for_mode(mode_name)

    def configure_mode_sensors(self, mode_name: str, sensor_ids: List[int]):
        """Configure which sensors are active for a given mode"""
        self.storage.save_mode_sensor_mapping(mode_name, sensor_ids)
        self.logger.add_log(
            f"Mode {mode_name} configured with {len(sensor_ids)} sensors",
            source="ConfigManager"
        )

    # ===== Safety Zone Management =====

    def get_safety_zone(self, zone_id: int) -> Optional[SafetyZone]:
        """Get a single safety zone by ID directly from the database."""
        # This could be optimized by adding a `load_one_zone` method to StorageManager
        all_zones = self.get_all_safety_zones()
        for zone in all_zones:
            if zone.zone_id == zone_id:
                return zone
        return None

    def get_all_safety_zones(self) -> List[SafetyZone]:
        """Get all safety zones directly from the database."""
        return self.storage.load_all_safety_zones()

    def add_safety_zone(self, zone_name: str) -> Optional[SafetyZone]:
        """Adds a new safety zone to the database."""
        zone = SafetyZone(None, zone_name)
        new_id = self.storage.save_safety_zone(zone)
        
        if new_id is not None:
            zone.zone_id = new_id
            self.logger.add_log(f"Safety zone '{zone_name}' created with ID {new_id}", source="ConfigManager")
            self._notify_zone_update()
            return zone

        # This should now only be reached if the DB insert truly fails
        return None

    def update_safety_zone(self, zone_id: int, zone_name: Optional[str] = None,
                           is_armed: Optional[bool] = None) -> bool:
        """Update safety zone properties in the database."""
        # First, get the current state of the zone to prevent overwriting attributes
        zone_to_update = self.get_safety_zone(zone_id)
        if not zone_to_update:
            return False

        # Apply the changes
        if zone_name is not None:
            zone_to_update.name = zone_name
        if is_armed is not None:
            zone_to_update.is_armed = is_armed
        
        # Save the fully updated object
        self.storage.save_safety_zone(zone_to_update)
        self.logger.add_log(f"Safety zone {zone_id} updated", source="ConfigManager")
        self._notify_zone_update()
        return True

    def delete_safety_zone(self, zone_id: int) -> bool:
        """Delete a safety zone from the database."""
        self.storage.delete_safety_zone(zone_id)
        self.logger.add_log(f"Safety zone {zone_id} deleted", source="ConfigManager")
        self._notify_zone_update()
        return True

    def get_all_zones(self) -> List[SafetyZone]:
        """Alias for get_all_safety_zones for backward compatibility."""
        return self.get_all_safety_zones()

    # ===== System Management =====

    def shutdown(self):
        """Gracefully shutdown configuration manager"""
        self.save_configuration()
        if self.db_manager:
            self.db_manager.disconnect()
        self.logger.add_log("Configuration Manager shutdown", source="ConfigManager")
