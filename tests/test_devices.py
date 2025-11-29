
import unittest
from unittest.mock import MagicMock, patch
import time

from safehome.device.alarm.alarm import Alarm
from safehome.device.sensor.sensor_controller import SensorController
from safehome.device.sensor.windoor_sensor import WindowDoorSensor
from safehome.device.sensor.motion_sensor import MotionSensor


class TestAlarm(unittest.TestCase):
    def setUp(self):
        """Set up for test"""
        self.alarm = Alarm()

    def test_initial_state(self):
        """Test that the alarm is initially off."""
        self.assertFalse(self.alarm.is_ringing)

    @patch('time.sleep', side_effect=lambda t: None)
    def test_ring_and_stop(self, mock_sleep):
        """Test ringing and stopping the alarm."""
        self.alarm.ring()
        self.assertTrue(self.alarm.is_ringing)
        self.alarm.stop()
        self.assertFalse(self.alarm.is_ringing)

    @patch('time.sleep', side_effect=lambda t: None)
    def test_ring_duration(self, mock_sleep):
        """Test that the alarm stops ringing after the duration."""
        alarm_with_duration = Alarm(duration=10)
        
        # Directly call the method that runs in a thread to test its logic
        alarm_with_duration.is_ringing = True # Manually set state as ring() would
        alarm_with_duration._ring_for_duration()
        
        # Check that sleep was called with the correct duration
        mock_sleep.assert_called_once_with(10)
        # Check that stop() was called, which sets is_ringing to False
        self.assertFalse(alarm_with_duration.is_ringing)


if __name__ == '__main__':
    unittest.main()


class TestSensorController(unittest.TestCase):
    def setUp(self):
        """Set up for test"""
        self.mock_storage = MagicMock()
        self.mock_logger = MagicMock()
        self.controller = SensorController(storage_manager=self.mock_storage, logger=self.mock_logger)

    def test_add_windoor_sensor(self):
        """Test adding a window/door sensor."""
        sensor = self.controller.add_sensor('WINDOOR', 'Front Door', zone_id=1)
        self.assertIn(sensor.sensor_id, self.controller.sensors)
        self.assertIsInstance(sensor, WindowDoorSensor)
        self.assertEqual(sensor.location, 'Front Door')
        self.mock_storage.save_sensor.assert_called_once()
        self.mock_logger.add_log.assert_called_once()

    def test_add_motion_sensor(self):
        """Test adding a motion sensor."""
        sensor = self.controller.add_sensor('MOTION', 'Living Room', zone_id=2)
        self.assertIn(sensor.sensor_id, self.controller.sensors)
        self.assertIsInstance(sensor, MotionSensor)
        self.assertEqual(sensor.location, 'Living Room')
        self.mock_storage.save_sensor.assert_called_once()
        self.mock_logger.add_log.assert_called_once()

    def test_remove_sensor(self):
        """Test removing a sensor."""
        sensor = self.controller.add_sensor('WINDOOR', 'Front Door')
        sensor_id = sensor.sensor_id
        
        # Mock the disarm method
        sensor.disarm = MagicMock()

        result = self.controller.remove_sensor(sensor_id)
        
        self.assertTrue(result)
        self.assertNotIn(sensor_id, self.controller.sensors)
        sensor.disarm.assert_called_once()
        self.mock_storage.delete_sensor.assert_called_with(sensor_id)
        # 2 calls: one for adding, one for removing
        self.assertEqual(self.mock_logger.add_log.call_count, 2)

    def test_poll_sensors_detection(self):
        """Test polling sensors with one triggered."""
        # Add a sensor and mock it
        mock_sensor = MagicMock(spec=WindowDoorSensor)
        mock_sensor.is_active = True
        mock_sensor.read.return_value = True # Simulate detection
        
        self.controller.sensors = {1: mock_sensor}

        detections = self.controller.poll_sensors()
        self.assertEqual(len(detections), 1)
        self.assertEqual(detections[0][0], 1)
        self.assertEqual(detections[0][1], mock_sensor)
        mock_sensor.read.assert_called_once()

    def test_poll_sensors_no_detection(self):
        """Test polling sensors with none triggered."""
        # Add a sensor and mock it
        mock_sensor = MagicMock(spec=WindowDoorSensor)
        mock_sensor.is_active = True
        mock_sensor.read.return_value = False # Simulate no detection
        
        self.controller.sensors = {1: mock_sensor}

        detections = self.controller.poll_sensors()
        self.assertEqual(len(detections), 0)
        mock_sensor.read.assert_called_once()

    def test_check_all_windoor_closed_when_all_are_closed(self):
        """Test checking window/door sensors when all are closed."""
        mock_sensor1 = MagicMock(spec=WindowDoorSensor)
        mock_sensor1.is_open.return_value = False
        
        mock_sensor2 = MagicMock(spec=WindowDoorSensor)
        mock_sensor2.is_open.return_value = False

        self.controller.get_sensors_by_type = MagicMock(return_value=[mock_sensor1, mock_sensor2])
        
        all_closed, open_sensors = self.controller.check_all_windoor_closed()

        self.assertTrue(all_closed)
        self.assertEqual(len(open_sensors), 0)

    def test_check_all_windoor_closed_when_one_is_open(self):
        """Test checking window/door sensors when one is open."""
        mock_sensor1 = MagicMock(spec=WindowDoorSensor)
        mock_sensor1.is_open.return_value = False
        
        mock_sensor2 = MagicMock(spec=WindowDoorSensor)
        mock_sensor2.is_open.return_value = True

        self.controller.get_sensors_by_type = MagicMock(return_value=[mock_sensor1, mock_sensor2])
        
        all_closed, open_sensors = self.controller.check_all_windoor_closed()

        self.assertFalse(all_closed)
        self.assertEqual(len(open_sensors), 1)
        self.assertIn(mock_sensor2, open_sensors)
