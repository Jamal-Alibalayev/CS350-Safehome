import unittest
import os
from safehome.database.db_manager import DatabaseManager
from safehome.database.models import SystemSettings, SafetyZone, Sensor, Camera, EventLog


class TestDatabaseLayer(unittest.TestCase):
    """Test database layer functionality"""

    def setUp(self):
        """Set up test database"""
        self.test_db_path = "data/test_safehome.db"
        # Remove test database if exists
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

        # Create database manager and initialize schema
        self.db = DatabaseManager(self.test_db_path)
        self.db.connect()
        self.db.initialize_schema()

    def tearDown(self):
        """Clean up test database"""
        self.db.disconnect()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_database_initialization(self):
        """Test that database initializes with correct schema"""
        # Check that tables exist
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        tables = [row[0] for row in self.db.execute_query(query, fetch_all=True)]

        expected_tables = [
            'system_settings',
            'safety_zones',
            'safehome_modes',
            'sensors',
            'mode_sensor_mapping',
            'cameras',
            'event_logs',
            'login_sessions'
        ]

        for table in expected_tables:
            self.assertIn(table, tables, f"Table {table} should exist")

    def test_default_system_settings(self):
        """Test that default system settings are inserted"""
        settings = self.db.get_system_settings()
        self.assertIsNotNone(settings)
        self.assertEqual(settings['master_password'], '1234')
        self.assertEqual(settings['web_password_1'], 'webpass1')
        self.assertEqual(settings['web_password_2'], 'webpass2')
        self.assertEqual(settings['entry_delay'], 300)  # 5 minutes

    def test_update_system_settings(self):
        """Test updating system settings"""
        # Update settings
        self.db.update_system_settings(
            master_password='9999',
            entry_delay=600,
            monitoring_phone='123-456-7890'
        )

        # Verify updates
        settings = self.db.get_system_settings()
        self.assertEqual(settings['master_password'], '9999')
        self.assertEqual(settings['entry_delay'], 600)
        self.assertEqual(settings['monitoring_phone'], '123-456-7890')

    def test_default_safehome_modes(self):
        """Test that default SafeHome modes are inserted"""
        modes = self.db.get_safehome_modes()
        self.assertEqual(len(modes), 4)

        mode_names = [mode['mode_name'] for mode in modes]
        self.assertIn('HOME', mode_names)
        self.assertIn('AWAY', mode_names)
        self.assertIn('OVERNIGHT', mode_names)
        self.assertIn('EXTENDED', mode_names)

    def test_safety_zone_crud(self):
        """Test safety zone create, read, update, delete"""
        # Create
        query = "INSERT INTO safety_zones (zone_name, is_armed) VALUES (?, ?)"
        self.db.execute_query(query, ('Living Room', False))
        self.db.commit()

        # Read
        zones = self.db.get_safety_zones()
        self.assertEqual(len(zones), 1)
        self.assertEqual(zones[0]['zone_name'], 'Living Room')

        zone_id = zones[0]['zone_id']

        # Update
        query = "UPDATE safety_zones SET is_armed = ? WHERE zone_id = ?"
        self.db.execute_query(query, (True, zone_id))
        self.db.commit()

        zones = self.db.get_safety_zones()
        self.assertTrue(bool(zones[0]['is_armed']))

        # Delete
        query = "DELETE FROM safety_zones WHERE zone_id = ?"
        self.db.execute_query(query, (zone_id,))
        self.db.commit()

        zones = self.db.get_safety_zones()
        self.assertEqual(len(zones), 0)

    def test_sensor_operations(self):
        """Test sensor database operations"""
        # Create safety zone first
        query = "INSERT INTO safety_zones (zone_name) VALUES (?)"
        self.db.execute_query(query, ('Zone 1',))
        self.db.commit()
        zone_id = self.db.get_last_insert_id()

        # Insert sensor
        query = """
            INSERT INTO sensors (sensor_type, sensor_location, zone_id)
            VALUES (?, ?, ?)
        """
        self.db.execute_query(query, ('WINDOOR', 'Front Door', zone_id))
        self.db.commit()

        # Get sensors
        sensors = self.db.get_sensors()
        self.assertEqual(len(sensors), 1)
        self.assertEqual(sensors[0]['sensor_type'], 'WINDOOR')
        self.assertEqual(sensors[0]['sensor_location'], 'Front Door')

        # Get sensors by zone
        zone_sensors = self.db.get_sensors(zone_id=zone_id)
        self.assertEqual(len(zone_sensors), 1)

    def test_camera_operations(self):
        """Test camera database operations"""
        # Insert camera
        query = """
            INSERT INTO cameras (camera_name, camera_location, camera_password)
            VALUES (?, ?, ?)
        """
        self.db.execute_query(query, ('Cam1', 'Front Yard', 'pass123'))
        self.db.commit()

        # Get cameras
        cameras = self.db.get_cameras()
        self.assertEqual(len(cameras), 1)
        self.assertEqual(cameras[0]['camera_name'], 'Cam1')
        self.assertEqual(cameras[0]['camera_password'], 'pass123')

    def test_event_log_operations(self):
        """Test event log database operations"""
        # Add log (without sensor_id to avoid FK constraint)
        log_id = self.db.add_event_log(
            event_type='INTRUSION',
            event_message='Unauthorized access detected',
            source='Sensor'
        )

        self.assertIsNotNone(log_id)

        # Get logs
        logs = self.db.get_event_logs(limit=10)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['event_type'], 'INTRUSION')

        # Filter by event type
        logs = self.db.get_event_logs(event_type='INTRUSION')
        self.assertEqual(len(logs), 1)

        logs = self.db.get_event_logs(event_type='INFO')
        self.assertEqual(len(logs), 0)

    def test_mode_sensor_mapping(self):
        """Test mode-sensor many-to-many mapping"""
        # Create sensors with explicit INSERT
        query = "INSERT INTO sensors (sensor_type, sensor_location) VALUES (?, ?)"
        cursor1 = self.db.execute_query(query, ('WINDOOR', 'Sensor 1'))
        self.db.commit()
        # Get ID from cursor
        sensor1_id = cursor1.lastrowid

        cursor2 = self.db.execute_query(query, ('MOTION', 'Sensor 2'))
        self.db.commit()
        sensor2_id = cursor2.lastrowid

        # Get AWAY mode
        query = "SELECT mode_id FROM safehome_modes WHERE mode_name = 'AWAY'"
        mode_row = self.db.execute_query(query, fetch_one=True)
        mode_id = mode_row['mode_id']

        # Map sensors to mode
        query = "INSERT INTO mode_sensor_mapping (mode_id, sensor_id) VALUES (?, ?)"
        self.db.execute_query(query, (mode_id, sensor1_id))
        self.db.execute_query(query, (mode_id, sensor2_id))
        self.db.commit()

        # Verify mapping
        query = "SELECT sensor_id FROM mode_sensor_mapping WHERE mode_id = ?"
        rows = self.db.execute_query(query, (mode_id,), fetch_all=True)
        sensor_ids = [row['sensor_id'] for row in rows]

        self.assertEqual(len(sensor_ids), 2)
        self.assertIn(sensor1_id, sensor_ids)
        self.assertIn(sensor2_id, sensor_ids)

    def test_context_manager(self):
        """Test database context manager"""
        with DatabaseManager(self.test_db_path) as db:
            db.initialize_schema()
            settings = db.get_system_settings()
            self.assertIsNotNone(settings)


if __name__ == '__main__':
    unittest.main()
