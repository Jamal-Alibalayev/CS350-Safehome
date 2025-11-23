import json
import os
from typing import Optional, List
from .system_settings import SystemSettings
from .safety_zone import SafetyZone


class StorageManager:
    """
    Hybrid storage manager supporting both JSON (backup) and SQLite3 (primary)
    """
    CONFIG_FILE = "data/safehome_config.json"

    def __init__(self, db_manager=None):
        """
        Initialize StorageManager

        Args:
            db_manager: DatabaseManager instance (optional)
        """
        self.db = db_manager

    # ===== JSON-based methods (backward compatibility) =====

    def save_settings_to_json(self, settings: SystemSettings):
        """Save SystemSettings to JSON (backup)"""
        data = {
            "master_password": settings.master_password,
            "entry_delay": settings.entry_delay,
            "exit_delay": settings.exit_delay,
            "alarm_duration": settings.alarm_duration
        }
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            print("Settings saved to JSON successfully.")
        except IOError as e:
            print(f"Error saving settings to JSON: {e}")

    def load_settings_from_json(self) -> dict:
        """Load settings from JSON"""
        if not os.path.exists(self.CONFIG_FILE):
            return {}

        try:
            with open(self.CONFIG_FILE, 'r') as f:
                return json.load(f)
        except IOError:
            return {}

    # Legacy aliases for backward compatibility
    def save_settings(self, settings: SystemSettings):
        """Legacy method - saves to both JSON and DB if available"""
        self.save_settings_to_json(settings)
        if self.db:
            self.save_settings_to_db(settings)

    def load_settings(self) -> dict:
        """Legacy method - loads from DB if available, otherwise JSON"""
        if self.db:
            db_settings = self.load_settings_from_db()
            if db_settings:
                return db_settings
        return self.load_settings_from_json()

    # ===== Database-based methods =====

    def save_settings_to_db(self, settings: SystemSettings):
        """Save SystemSettings to database"""
        if not self.db:
            return

        self.db.update_system_settings(
            master_password=settings.master_password,
            entry_delay=settings.entry_delay,
            exit_delay=settings.exit_delay,
            alarm_duration=settings.alarm_duration
        )

    def load_settings_from_db(self) -> Optional[dict]:
        """Load settings from database"""
        if not self.db:
            return None

        row = self.db.get_system_settings()
        if not row:
            return None

        return {
            "master_password": row['master_password'],
            "guest_password": row['guest_password'],
            "web_password_1": row['web_password_1'],
            "web_password_2": row['web_password_2'],
            "entry_delay": row['entry_delay'],
            "exit_delay": row['exit_delay'],
            "alarm_duration": row['alarm_duration'],
            "system_lock_time": row['system_lock_time'],
            "monitoring_phone": row['monitoring_phone'],
            "homeowner_phone": row['homeowner_phone'],
            "max_login_attempts": row['max_login_attempts']
        }

    def save_safety_zone(self, zone: SafetyZone):
        """Save or update a SafetyZone to database"""
        if not self.db:
            return

        if zone.zone_id is None:
            # Insert new zone
            query = """
                INSERT INTO safety_zones (zone_name, is_armed)
                VALUES (?, ?)
            """
            self.db.execute_query(query, (zone.name, zone.is_armed))
            self.db.commit()
            zone.zone_id = self.db.get_last_insert_id()
        else:
            # Update existing zone
            query = """
                UPDATE safety_zones
                SET zone_name = ?, is_armed = ?, updated_at = CURRENT_TIMESTAMP
                WHERE zone_id = ?
            """
            self.db.execute_query(query, (zone.name, zone.is_armed, zone.zone_id))
            self.db.commit()

    def load_all_safety_zones(self) -> List[SafetyZone]:
        """Load all SafetyZones from database"""
        if not self.db:
            return []

        rows = self.db.get_safety_zones()
        zones = []
        for row in rows:
            zone = SafetyZone(row['zone_id'], row['zone_name'])
            zone.is_armed = bool(row['is_armed'])
            zones.append(zone)
        return zones

    def delete_safety_zone(self, zone_id: int):
        """Delete a SafetyZone from database"""
        if not self.db:
            return

        query = "DELETE FROM safety_zones WHERE zone_id = ?"
        self.db.execute_query(query, (zone_id,))
        self.db.commit()

    def save_sensor(self, sensor_id: int, sensor_type: str, location: str, zone_id: Optional[int] = None):
        """Save sensor to database"""
        if not self.db:
            return

        query = """
            INSERT INTO sensors (sensor_id, sensor_type, sensor_location, zone_id)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(sensor_id) DO UPDATE SET
                sensor_type = excluded.sensor_type,
                sensor_location = excluded.sensor_location,
                zone_id = excluded.zone_id
        """
        self.db.execute_query(query, (sensor_id, sensor_type, location, zone_id))
        self.db.commit()

    def load_all_sensors(self) -> List[dict]:
        """Load all sensors from database"""
        if not self.db:
            return []

        rows = self.db.get_sensors()
        return [dict(row) for row in rows]

    def delete_sensor(self, sensor_id: int):
        """Delete sensor from database"""
        if not self.db:
            return

        query = "DELETE FROM sensors WHERE sensor_id = ?"
        self.db.execute_query(query, (sensor_id,))
        self.db.commit()

    def save_camera(self, camera_id: int, name: str, location: str, password: Optional[str] = None):
        """Save camera to database"""
        if not self.db:
            return

        query = """
            INSERT INTO cameras (camera_id, camera_name, camera_location, camera_password)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(camera_id) DO UPDATE SET
                camera_name = excluded.camera_name,
                camera_location = excluded.camera_location,
                camera_password = excluded.camera_password
        """
        self.db.execute_query(query, (camera_id, name, location, password))
        self.db.commit()

    def load_all_cameras(self) -> List[dict]:
        """Load all cameras from database"""
        if not self.db:
            return []

        rows = self.db.get_cameras()
        return [dict(row) for row in rows]

    def delete_camera(self, camera_id: int):
        """Delete a camera from database"""
        if not self.db:
            return

        query = "DELETE FROM cameras WHERE camera_id = ?"
        self.db.execute_query(query, (camera_id,))
        self.db.commit()

    def update_camera_password(self, camera_id: int, password: Optional[str]):
        """Update camera password"""
        if not self.db:
            return

        query = "UPDATE cameras SET camera_password = ? WHERE camera_id = ?"
        self.db.execute_query(query, (password, camera_id))
        self.db.commit()

    def save_log(self, log):
        """Save log entry to database"""
        if not self.db:
            return

        self.db.add_event_log(
            event_type=log.level,
            event_message=log.message,
            source=log.source
        )

    def get_logs(self, limit: int = 100, event_type: Optional[str] = None,
                  start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[dict]:
        """Get logs from database with filters"""
        if not self.db:
            return []

        rows = self.db.get_event_logs(
            event_type=event_type,
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )
        return [dict(row) for row in rows]

    def get_sensors_for_mode(self, mode_name: str) -> List[int]:
        """Get list of sensor IDs for a given SafeHomeMode"""
        if not self.db:
            return []

        query = """
            SELECT mss.sensor_id
            FROM mode_sensor_mapping mss
            JOIN safehome_modes sm ON mss.mode_id = sm.mode_id
            WHERE sm.mode_name = ?
        """
        rows = self.db.execute_query(query, (mode_name,), fetch_all=True)
        return [row['sensor_id'] for row in rows]

    def save_mode_sensor_mapping(self, mode_name: str, sensor_ids: List[int]):
        """Save sensor mapping for a SafeHomeMode"""
        if not self.db:
            return

        # Get mode_id
        query = "SELECT mode_id FROM safehome_modes WHERE mode_name = ?"
        row = self.db.execute_query(query, (mode_name,), fetch_one=True)
        if not row:
            return

        mode_id = row['mode_id']

        # Delete existing mappings
        query = "DELETE FROM mode_sensor_mapping WHERE mode_id = ?"
        self.db.execute_query(query, (mode_id,))

        # Insert new mappings
        if sensor_ids:
            query = "INSERT INTO mode_sensor_mapping (mode_id, sensor_id) VALUES (?, ?)"
            params_list = [(mode_id, sensor_id) for sensor_id in sensor_ids]
            self.db.execute_many(query, params_list)

        self.db.commit()