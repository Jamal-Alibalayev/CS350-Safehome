"""
Quick integration test for Core System Layer
Tests basic system functionality
"""

import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from safehome.core.system import System
from safehome.configuration.safehome_mode import SafeHomeMode


def test_system_initialization():
    """Test system initialization"""
    print("=" * 60)
    print("Test 1: System Initialization")
    print("=" * 60)

    system = System(db_path="data/test_core_system.db")

    print(f"✓ System created: {system}")
    print(f"✓ Sensor Controller: {len(system.sensor_controller.sensors)} sensors")
    print(f"✓ Camera Controller: {len(system.camera_controller.cameras)} cameras")
    print(f"✓ Alarm: {system.alarm}")
    print(f"✓ Current Mode: {system.config.current_mode.name}")

    system.shutdown()
    print()


def test_sensor_operations():
    """Test sensor operations"""
    print("=" * 60)
    print("Test 2: Sensor Operations")
    print("=" * 60)

    system = System(db_path="data/test_core_system.db")

    # Add sensors
    sensor1 = system.sensor_controller.add_sensor('WINDOOR', 'Front Door')
    sensor2 = system.sensor_controller.add_sensor('MOTION', 'Living Room')

    print(f"✓ Added Window/Door sensor: {sensor1}")
    print(f"✓ Added Motion sensor: {sensor2}")
    print(f"✓ Total sensors: {len(system.sensor_controller.sensors)}")

    # Arm sensor
    system.sensor_controller.arm_sensor(sensor1.sensor_id)
    print(f"✓ Sensor {sensor1.sensor_id} armed: {sensor1.is_active}")

    # Disarm all
    system.sensor_controller.disarm_all_sensors()
    print(f"✓ All sensors disarmed")

    system.shutdown()
    print()


def test_camera_operations():
    """Test camera operations"""
    print("=" * 60)
    print("Test 3: Camera Operations")
    print("=" * 60)

    system = System(db_path="data/test_core_system.db")

    # Add cameras
    camera1 = system.camera_controller.add_camera('Front Entrance', 'Front Door', password='cam123')
    camera2 = system.camera_controller.add_camera('Back Yard', 'Back Door')

    print(f"✓ Added camera with password: {camera1}")
    print(f"✓ Added camera without password: {camera2}")
    print(f"✓ Total cameras: {len(system.camera_controller.cameras)}")

    # Test password protection
    view1 = system.camera_controller.get_camera_view(camera1.camera_id, 'wrong_pass')
    print(f"✓ Camera access with wrong password: {view1 is None}")

    view2 = system.camera_controller.get_camera_view(camera1.camera_id, 'cam123')
    print(f"✓ Camera access with correct password: {view2 is not None}")

    system.shutdown()
    print()


def test_alarm():
    """Test alarm functionality"""
    print("=" * 60)
    print("Test 4: Alarm Functionality")
    print("=" * 60)

    system = System(db_path="data/test_core_system.db")

    print(f"✓ Alarm initial state: ringing={system.alarm.is_ringing}")

    # Trigger alarm
    system.alarm.ring()
    print(f"✓ Alarm triggered: ringing={system.alarm.is_ringing}")

    time.sleep(1)

    # Stop alarm
    system.alarm.stop()
    print(f"✓ Alarm stopped: ringing={system.alarm.is_ringing}")

    system.shutdown()
    print()


def test_system_modes():
    """Test system mode operations"""
    print("=" * 60)
    print("Test 5: System Mode Operations")
    print("=" * 60)

    system = System(db_path="data/test_core_system.db")

    print(f"✓ Initial mode: {system.config.current_mode.name}")

    # Turn on system
    system.turn_on()
    print(f"✓ System turned on: running={system.is_running}")

    time.sleep(0.5)

    # Arm system
    success = system.arm_system(SafeHomeMode.HOME)
    print(f"✓ System armed in HOME mode: success={success}")
    print(f"✓ Current mode: {system.config.current_mode.name}")

    time.sleep(0.5)

    # Disarm system
    system.disarm_system()
    print(f"✓ System disarmed")
    print(f"✓ Current mode: {system.config.current_mode.name}")

    # Turn off system
    system.turn_off()
    print(f"✓ System turned off: running={system.is_running}")

    system.shutdown()
    print()


def test_login():
    """Test login functionality"""
    print("=" * 60)
    print("Test 6: Login Functionality")
    print("=" * 60)

    system = System(db_path="data/test_core_system.db")

    # Test master password
    result = system.login("admin", "1234", "CONTROL_PANEL")
    print(f"✓ Login with correct master password: {result}")

    # Test wrong password
    result = system.login("admin", "9999", "CONTROL_PANEL")
    print(f"✓ Login with wrong password: {result}")

    # Test web interface login
    result = system.login("admin", "webpass1:webpass2", "WEB")
    print(f"✓ Web login with correct password: {result}")

    system.shutdown()
    print()


def test_safety_zones():
    """Test safety zone operations"""
    print("=" * 60)
    print("Test 7: Safety Zone Operations")
    print("=" * 60)

    system = System(db_path="data/test_core_system.db")

    # Add safety zone
    zone = system.config.add_safety_zone("First Floor")
    print(f"✓ Added safety zone: {zone.zone_name} (ID: {zone.zone_id})")

    # Add sensors to zone
    sensor1 = system.sensor_controller.add_sensor('WINDOOR', 'Kitchen Window', zone.zone_id)
    sensor2 = system.sensor_controller.add_sensor('MOTION', 'Kitchen', zone.zone_id)
    print(f"✓ Added sensors to zone: {sensor1.location}, {sensor2.location}")

    # Arm zone
    system.arm_zone(zone.zone_id)
    print(f"✓ Zone armed: {zone.is_armed}")
    print(f"✓ Sensor 1 active: {sensor1.is_active}")
    print(f"✓ Sensor 2 active: {sensor2.is_active}")

    # Disarm zone
    system.disarm_zone(zone.zone_id)
    print(f"✓ Zone disarmed: {zone.is_armed}")

    system.shutdown()
    print()


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("CORE SYSTEM LAYER INTEGRATION TESTS")
    print("=" * 60 + "\n")

    try:
        test_system_initialization()
        test_sensor_operations()
        test_camera_operations()
        test_alarm()
        test_system_modes()
        test_login()
        test_safety_zones()

        print("=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
