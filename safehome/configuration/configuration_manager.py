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

        # 5. Initialize Login Manager
        self.login_manager = LoginManager(self.settings, self.storage)

        # 6. Load Safety Zones from database
        self.zones = self._load_or_create_zones()
        self.current_zone_index = 0

        # 7. Load SafeHome Modes from database
        self.modes = self._load_safehome_modes()

        # 8. Current state
        self.current_mode = SafeHomeMode.DISARMED

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

    def _load_or_create_zones(self) -> List[SafetyZone]:
        """Load safety zones from database or create defaults"""
        zones = self.storage.load_all_safety_zones()
        if not zones:
            # Create default zones
            zone1 = SafetyZone(None, "Living Room")
            zone2 = SafetyZone(None, "Bedroom")
            self.storage.save_safety_zone(zone1)
            self.storage.save_safety_zone(zone2)
            zones = [zone1, zone2]
        return zones

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
        """Save all configuration to database and JSON"""
        self.storage.save_settings(self.settings)
        # Save all zones
        for zone in self.zones:
            self.storage.save_safety_zone(zone)
        self.logger.add_log("Configuration saved", source="ConfigManager")

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

    def get_current_zone(self) -> SafetyZone:
        """Get currently selected safety zone"""
        if 0 <= self.current_zone_index < len(self.zones):
            return self.zones[self.current_zone_index]
        return None

    def next_zone(self) -> SafetyZone:
        """Switch to next zone and return it"""
        if self.zones:
            self.current_zone_index = (self.current_zone_index + 1) % len(self.zones)
            return self.get_current_zone()
        return None

    def get_safety_zone(self, zone_id: int) -> Optional[SafetyZone]:
        """Get safety zone by ID"""
        for zone in self.zones:
            if zone.zone_id == zone_id:
                return zone
        return None

    def get_all_safety_zones(self) -> List[SafetyZone]:
        """Get all safety zones"""
        return self.zones

    def add_safety_zone(self, zone_name: str) -> SafetyZone:
        """Add a new safety zone"""
        zone = SafetyZone(None, zone_name)
        self.storage.save_safety_zone(zone)
        self.zones.append(zone)
        self.logger.add_log(f"Safety zone '{zone_name}' created", source="ConfigManager")
        return zone

    def update_safety_zone(self, zone_id: int, zone_name: Optional[str] = None,
                           is_armed: Optional[bool] = None):
        """Update safety zone properties"""
        zone = self.get_safety_zone(zone_id)
        if not zone:
            return False

        if zone_name is not None:
            zone.name = zone_name
        if is_armed is not None:
            zone.is_armed = is_armed

        self.storage.save_safety_zone(zone)
        self.logger.add_log(f"Safety zone {zone_id} updated", source="ConfigManager")
        return True

    def delete_safety_zone(self, zone_id: int) -> bool:
        """Delete a safety zone"""
        zone = self.get_safety_zone(zone_id)
        if not zone:
            return False

        self.storage.delete_safety_zone(zone_id)
        self.zones = [z for z in self.zones if z.zone_id != zone_id]
        self.logger.add_log(f"Safety zone {zone_id} deleted", source="ConfigManager")
        return True

    def get_all_zones(self) -> List[SafetyZone]:
        """Get list of all safety zones"""
        return self.zones

    # ===== System Management =====

    def shutdown(self):
        """Gracefully shutdown configuration manager"""
        self.save_configuration()
        if self.db_manager:
            self.db_manager.disconnect()
        self.logger.add_log("Configuration Manager shutdown", source="ConfigManager")