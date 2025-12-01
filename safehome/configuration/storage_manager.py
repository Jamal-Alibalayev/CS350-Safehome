import json
import os
from typing import List, Optional

from .safety_zone import SafetyZone
from .system_settings import SystemSettings


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

    def _check_db(self):
        """Raise an exception if the database is not initialized."""
        if not self.db:
            raise ValueError("Database connection is not available in StorageManager")

    # ===== JSON-based methods (backward compatibility) =====

    def save_settings_to_json(self, settings: SystemSettings):
        """Save SystemSettings to JSON (backup)"""
        data = {
            "master_password": settings.master_password,
            "entry_delay": settings.entry_delay,
            "exit_delay": settings.exit_delay,
            "alarm_duration": settings.alarm_duration,
        }
        try:
            with open(self.CONFIG_FILE, "w") as f:
                json.dump(data, f, indent=4)
            print("Settings saved to JSON successfully.")
        except IOError as e:
            print(f"Error saving settings to JSON: {e}")

    def load_settings_from_json(self) -> dict:
        """Load settings from JSON"""
        if not os.path.exists(self.CONFIG_FILE):
            return {}

        try:
            with open(self.CONFIG_FILE, "r") as f:
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
        self._check_db()
        self.db.update_system_settings(
            master_password=settings.master_password,
            guest_password=settings.guest_password,
            web_password_1=settings.web_password_1,
            web_password_2=settings.web_password_2,
            entry_delay=settings.entry_delay,
            exit_delay=settings.exit_delay,
            alarm_duration=settings.alarm_duration,
            system_lock_time=settings.system_lock_time,
            monitoring_phone=settings.monitoring_phone,
            homeowner_phone=settings.homeowner_phone,
            alert_email=settings.alert_email,
            smtp_host=settings.smtp_host,
            smtp_port=settings.smtp_port,
            smtp_user=settings.smtp_user,
            smtp_password=settings.smtp_password,
            max_login_attempts=settings.max_login_attempts,
        )

    def load_settings_from_db(self) -> Optional[dict]:
        """Load settings from database"""
        self._check_db()
        row = self.db.get_system_settings()
        if not row:
            return None

        row_dict = dict(row)
        return {
            "master_password": row_dict.get("master_password"),
            "guest_password": row_dict.get("guest_password"),
            "web_password_1": row_dict.get("web_password_1"),
            "web_password_2": row_dict.get("web_password_2"),
            "entry_delay": row_dict.get("entry_delay"),
            "exit_delay": row_dict.get("exit_delay"),
            "alarm_duration": row_dict.get("alarm_duration"),
            "system_lock_time": row_dict.get("system_lock_time"),
            "monitoring_phone": row_dict.get("monitoring_phone"),
            "homeowner_phone": row_dict.get("homeowner_phone"),
            "alert_email": row_dict.get("alert_email"),
            "smtp_host": row_dict.get("smtp_host"),
            "smtp_port": row_dict.get("smtp_port"),
            "smtp_user": row_dict.get("smtp_user"),
            "smtp_password": row_dict.get("smtp_password"),
            "max_login_attempts": row_dict.get("max_login_attempts", 3),
        }

    def save_safety_zone(self, zone: SafetyZone) -> Optional[int]:
        """Save or update a SafetyZone to database and return its ID."""
        self._check_db()
        if zone.zone_id is None:
            # Insert new zone and get the new ID reliably
            query = """
                INSERT INTO safety_zones (zone_name, is_armed)
                VALUES (?, ?)
            """
            new_id = self.db.execute_insert_query(query, (zone.name, zone.is_armed))
            self.db.commit()
            return new_id
        else:
            # Update existing zone
            query = """
                UPDATE safety_zones
                SET zone_name = ?, is_armed = ?, updated_at = CURRENT_TIMESTAMP
                WHERE zone_id = ?
            """
            self.db.execute_query(query, (zone.name, zone.is_armed, zone.zone_id))
            self.db.commit()
            return zone.zone_id

    def load_all_safety_zones(self) -> List[SafetyZone]:
        """Load all SafetyZones from database"""
        self._check_db()
        rows = self.db.get_safety_zones()
        zones = []
        for row in rows:
            zone = SafetyZone(row["zone_id"], row["zone_name"])
            zone.is_armed = bool(row["is_armed"])
            zones.append(zone)
        return zones

    def load_safety_zone_by_id(self, zone_id: int) -> Optional[SafetyZone]:
        """Load a single SafetyZone from database by its ID."""
        self._check_db()
        row = self.db.execute_query(
            "SELECT * FROM safety_zones WHERE zone_id = ?", (zone_id,), fetch_one=True
        )
        if row:
            zone = SafetyZone(row["zone_id"], row["zone_name"])
            zone.is_armed = bool(row["is_armed"])
            return zone
        return None

    def delete_safety_zone(self, zone_id: int):
        """Delete a SafetyZone from database"""
        self._check_db()
        query = "DELETE FROM safety_zones WHERE zone_id = ?"
        self.db.execute_query(query, (zone_id,))
        self.db.commit()

    def delete_all_safety_zones(self):
        """Delete all SafetyZones from database and reset the auto-increment counter."""
        self._check_db()
        # Delete all rows from the table
        delete_query = "DELETE FROM safety_zones"
        self.db.execute_query(delete_query)

        # Reset the auto-increment counter for the table
        # This is specific to SQLite
        reset_query = "DELETE FROM sqlite_sequence WHERE name='safety_zones'"
        try:
            self.db.execute_query(reset_query)
        except Exception as e:
            # This might fail if the table was not created with AUTOINCREMENT, which is fine.
            print(
                f"Could not reset sequence for safety_zones, this might be expected: {e}"
            )

        self.db.commit()

    def save_sensor(
        self,
        sensor_id: int,
        sensor_type: str,
        location: str,
        zone_id: Optional[int] = None,
    ):
        """Save sensor to database"""
        self._check_db()
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
        self._check_db()
        rows = self.db.get_sensors()
        return [dict(row) for row in rows]

    def delete_sensor(self, sensor_id: int):
        """Delete sensor from database"""
        self._check_db()
        query = "DELETE FROM sensors WHERE sensor_id = ?"
        self.db.execute_query(query, (sensor_id,))
        self.db.commit()

    def save_camera(
        self, camera_id: int, name: str, location: str, password: Optional[str] = None
    ):
        """Save camera to database"""
        self._check_db()
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
        self._check_db()
        rows = self.db.get_cameras()
        return [dict(row) for row in rows]

    def delete_camera(self, camera_id: int):
        """Delete a camera from database"""
        self._check_db()
        query = "DELETE FROM cameras WHERE camera_id = ?"
        self.db.execute_query(query, (camera_id,))
        self.db.commit()

    def update_camera_password(self, camera_id: int, password: Optional[str]):
        """Update camera password"""
        self._check_db()
        query = "UPDATE cameras SET camera_password = ? WHERE camera_id = ?"
        self.db.execute_query(query, (password, camera_id))
        self.db.commit()

    def clear_camera_passwords(self):
        """Remove all camera passwords (used for system reset)."""
        self._check_db()
        self.db.execute_query("UPDATE cameras SET camera_password = NULL")
        self.db.commit()

    def save_log(self, log, **kwargs):
        """Save log entry to database"""
        self._check_db()
        self.db.add_event_log(
            event_type=log.level,
            event_message=log.message,
            source=log.source,
            sensor_id=kwargs.get("sensor_id"),
            camera_id=kwargs.get("camera_id"),
            zone_id=kwargs.get("zone_id"),
        )

    def get_logs(
        self,
        limit: int = 100,
        event_type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[dict]:
        """Get logs from database with filters"""
        self._check_db()
        rows = self.db.get_event_logs(
            event_type=event_type, start_date=start_date, end_date=end_date, limit=limit
        )
        return [dict(row) for row in rows]

    def get_unseen_logs(
        self, limit: int = 100, event_type: Optional[str] = "ALARM"
    ) -> List[dict]:
        """Get logs not marked as seen"""
        self._check_db()
        query = """
            SELECT e.*
            FROM event_logs e
            LEFT JOIN event_log_seen s ON e.log_id = s.log_id
            WHERE s.log_id IS NULL
        """
        params = []
        if event_type:
            query += " AND e.event_type = ?"
            params.append(event_type)
        query += " ORDER BY e.event_timestamp DESC LIMIT ?"
        params.append(limit)

        rows = self.db.execute_query(query, tuple(params), fetch_all=True)
        return [dict(row) for row in rows]

    def mark_logs_seen(self, log_ids: List[int]):
        """Mark specified log IDs as seen"""
        self._check_db()
        if not log_ids:
            return
        values = [(lid,) for lid in log_ids]
        self.db.execute_many(
            "INSERT OR IGNORE INTO event_log_seen (log_id) VALUES (?)", values
        )
        self.db.commit()

    def clear_logs(self):
        """Delete all event logs and seen markers."""
        self._check_db()
        self.db.clear_event_logs()

    def get_sensors_for_mode(self, mode_name: str) -> List[int]:
        """Get list of sensor IDs for a given SafeHomeMode"""
        self._check_db()
        query = """
            SELECT mss.sensor_id
            FROM mode_sensor_mapping mss
            JOIN safehome_modes sm ON mss.mode_id = sm.mode_id
            WHERE sm.mode_name = ?
        """
        rows = self.db.execute_query(query, (mode_name,), fetch_all=True)
        return [row["sensor_id"] for row in rows]

    def save_mode_sensor_mapping(self, mode_name: str, sensor_ids: List[int]):
        """Save sensor mapping for a SafeHomeMode"""
        self._check_db()
        # Get mode_id
        query = "SELECT mode_id FROM safehome_modes WHERE mode_name = ?"
        row = self.db.execute_query(query, (mode_name,), fetch_one=True)
        if not row:
            return

        mode_id = row["mode_id"]

        # Delete existing mappings
        query = "DELETE FROM mode_sensor_mapping WHERE mode_id = ?"
        self.db.execute_query(query, (mode_id,))

        # Insert new mappings
        if sensor_ids:
            query = "INSERT INTO mode_sensor_mapping (mode_id, sensor_id) VALUES (?, ?)"
            params_list = [(mode_id, sensor_id) for sensor_id in sensor_ids]
            self.db.execute_many(query, params_list)

        self.db.commit()
