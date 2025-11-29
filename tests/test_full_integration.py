
import unittest
import os
import time

from safehome.core.system import System
from safehome.configuration.safehome_mode import SafeHomeMode

class TestFullIntegration(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Set up for all tests in this class."""
        cls.test_db_path = "test_full_integration.db"
        # Ensure there's no old test DB before starting
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)
        
        # Initialize the system once for all tests in this suite
        cls.system = System(db_path=cls.test_db_path)
        cls.system.turn_on()

    @classmethod
    def tearDownClass(cls):
        """Tear down after all tests in this class."""
        cls.system.shutdown()
        time.sleep(0.2)
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def test_1_initialization(self):
        """Test that the system initializes correctly."""
        self.assertIsNotNone(self.system)
        self.assertIsNotNone(self.system.config)
        self.assertIsNotNone(self.system.sensor_controller)
        self.assertIsNotNone(self.system.camera_controller)

    def test_2_hardware_setup(self):
        """Test adding sensors and cameras."""
        # Add sensors
        s1 = self.system.sensor_controller.add_sensor('WINDOOR', 'Front Door', zone_id=1)
        s2 = self.system.sensor_controller.add_sensor('MOTION', 'Living Room', zone_id=1)
        s3 = self.system.sensor_controller.add_sensor('WINDOOR', 'Bedroom Window', zone_id=2)
        self.assertEqual(len(self.system.sensor_controller.get_all_sensors()), 3)
        
        # Add cameras and store their IDs
        c1 = self.system.camera_controller.add_camera('Main Camera', 'Living Room')
        c2 = self.system.camera_controller.add_camera('Secured Camera', 'Bedroom', password='cam123')
        self.assertEqual(len(self.system.camera_controller.cameras), 2)
        
        # Store camera IDs for other tests to use
        self.__class__.cam_no_pass_id = c1.camera_id
        self.__class__.cam_with_pass_id = c2.camera_id

    def test_3_system_operations(self):
        """Test arming and disarming the system."""
        self.assertTrue(self.system.is_running)
        
        # Mock the sensor check to pass
        self.system.sensor_controller.check_all_windoor_closed = lambda: (True, [])
        success = self.system.arm_system(SafeHomeMode.HOME)
        self.assertTrue(success)
        self.assertEqual(self.system.config.current_mode, SafeHomeMode.HOME)
        
        # Disarm system
        self.system.disarm_system()
        self.assertEqual(self.system.config.current_mode, SafeHomeMode.DISARMED)

    def test_4_camera_access(self):
        """Test camera access control with and without password."""
        # Access camera without password
        view1 = self.system.camera_controller.get_camera_view(self.cam_no_pass_id)
        self.assertIsNotNone(view1)
        
        # Access camera with wrong password
        view2 = self.system.camera_controller.get_camera_view(self.cam_with_pass_id, 'wrong')
        self.assertIsNone(view2)
        
        # Access camera with correct password
        view3 = self.system.camera_controller.get_camera_view(self.cam_with_pass_id, 'cam123')
        self.assertIsNotNone(view3)

    def test_5_login(self):
        """Test the login system for different interfaces."""
        # Control Panel login
        self.assertTrue(self.system.login("admin", "1234", "CONTROL_PANEL"))
        self.assertFalse(self.system.login("admin", "9999", "CONTROL_PANEL"))
        
        # Web login
        self.assertTrue(self.system.login("admin", "webpass1:webpass2", "WEB"))
        self.assertFalse(self.system.login("admin", "wrong:wrong", "WEB"))

    def test_6_status_and_final_check(self):
        """Test the get_system_status method and do a final check."""
        status = self.system.get_system_status()
        self.assertTrue(status['is_running'])
        self.assertEqual(status['num_sensors'], 3)
        self.assertEqual(status['num_cameras'], 2)

        # A final check to ensure system is still in a valid state
        self.assertEqual(self.system.config.current_mode, SafeHomeMode.DISARMED)

if __name__ == '__main__':
    unittest.main()
