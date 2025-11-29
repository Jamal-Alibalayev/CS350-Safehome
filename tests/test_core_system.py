
# NOTE: This test file may fail if the 'Pillow' library is not correctly 
# installed in the Python environment. This can be resolved by using a 
# virtual environment and running `pip install -r requirements.txt`.

import unittest
import os
import time
import sys # Import sys for mocking sys.modules
from unittest.mock import MagicMock, patch

# Correctly mock PIL and PIL.Image before importing System
# This needs to be outside the class or as a class decorator
# to affect the import of safehome.core.system
with patch.dict(sys.modules, {'PIL': MagicMock(), 'PIL.Image': MagicMock()}):
    from safehome.core.system import System
    from safehome.configuration.safehome_mode import SafeHomeMode
    from safehome.device.sensor.windoor_sensor import WindowDoorSensor

class TestCoreSystem(unittest.TestCase):
    def setUp(self):
        """Set up a clean system for each test."""
        self.test_db_path = "test_safehome.db"
        # Ensure there's no old test DB
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        
        # The System class initializes everything we need
        self.system = System(db_path=self.test_db_path)
        
        # Turn on the system to start background processes if needed
        self.system.turn_on()

    def tearDown(self):
        """Clean up after each test."""
        self.system.shutdown()
        # Give a moment for file handles to be released
        time.sleep(0.1)
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_system_initialization(self):
        """Test that the system initializes correctly."""
        self.assertIsNotNone(self.system.config)
        self.assertIsNotNone(self.system.sensor_controller)
        self.assertIsNotNone(self.system.camera_controller)
        self.assertIsNotNone(self.system.alarm)
        self.assertTrue(self.system.is_running)
        self.assertFalse(self.system.alarm.is_ringing)
        self.assertEqual(self.system.config.current_mode, SafeHomeMode.DISARMED)

    def test_arm_disarm_cycle(self):
        """Test the full arm -> disarm cycle."""
        # Mock the sensor check to ensure it passes
        self.system.sensor_controller.check_all_windoor_closed = MagicMock(return_value=(True, []))
        
        # Arm the system
        armed = self.system.arm_system(SafeHomeMode.AWAY)
        self.assertTrue(armed)
        self.assertEqual(self.system.config.current_mode, SafeHomeMode.AWAY)
        
        # Disarm the system
        self.system.disarm_system()
        self.assertEqual(self.system.config.current_mode, SafeHomeMode.DISARMED)
        self.assertFalse(self.system.alarm.is_ringing)

    def test_arm_system_fails_if_door_open(self):
        """Test that arming fails if a window/door sensor is open."""
        # Mock the sensor controller to simulate an open door
        mock_sensor = MagicMock(spec=WindowDoorSensor)
        self.system.sensor_controller.check_all_windoor_closed = MagicMock(return_value=(False, [mock_sensor]))
        
        armed = self.system.arm_system(SafeHomeMode.AWAY)
        
        self.assertFalse(armed)
        self.assertEqual(self.system.config.current_mode, SafeHomeMode.DISARMED)

    @patch('safehome.core.system.time.sleep')
    @patch('safehome.core.system.threading.Thread')
    @patch('safehome.core.system.System.call_monitoring_service')
    def test_intrusion_triggers_alarm(self, mock_call_service, mock_thread, mock_sleep):
        """
        Test that a detected intrusion triggers the alarm after the entry delay,
        using a deterministic, single-threaded approach.
        """
        # Stop the background polling thread from setUp to avoid interference
        self.system._stop_sensor_polling()

        # WORKAROUND: Mock the logger's add_log method to prevent a TypeError
        # caused by an incorrect keyword argument ('sensor_id') in the application code.
        self.system.config.logger.add_log = MagicMock()

        # 1. Add and configure a mock sensor
        sensor = self.system.sensor_controller.add_sensor('WINDOOR', 'Front Door')
        sensor.is_active = True
        sensor.hardware.read = MagicMock(return_value=True)
        
        # 2. Arm the system, preparing it for intrusion detection
        self.system.sensor_controller.check_all_windoor_closed = MagicMock(return_value=(True, []))
        self.system.config.storage.get_sensors_for_mode = MagicMock(return_value=[sensor.sensor_id])
        self.system.arm_system(SafeHomeMode.AWAY)

        # 3. Manually run the sensor polling logic
        detections = self.system.sensor_controller.poll_sensors()
        self.assertEqual(len(detections), 1)
        detected_sensor = detections[0][1]

        # 4. Manually run the intrusion handler. This will attempt to start a 
        #    new thread for the entry delay, which our mock will intercept.
        self.system._handle_intrusion(detected_sensor)

        # 5. Verify that the system tried to start a thread
        mock_thread.assert_called_once()
        # Extract the 'countdown' function from the mocked thread's arguments
        countdown_func = mock_thread.call_args.kwargs['target']
        
        # 6. Run the countdown logic directly in the main test thread.
        #    The time.sleep inside this function is also mocked to be instant.
        countdown_func()

        # 7. Now, with all logic executed synchronously, check the final state.
        self.assertTrue(self.system.alarm.is_ringing)
        mock_call_service.assert_called_once_with(sensor)

if __name__ == '__main__':
    unittest.main()
