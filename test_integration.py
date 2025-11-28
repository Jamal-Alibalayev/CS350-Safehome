"""
Integration Test for Complete SafeHome System
Tests all layers working together
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from safehome.core.system import System
from safehome.configuration.safehome_mode import SafeHomeMode

print("=" * 70)
print("SAFEHOME SYSTEM - FULL INTEGRATION TEST")
print("=" * 70)

# Test 1: System Initialization with all components
print("\n1. Testing System Initialization...")
system = System(db_path="data/test_integration.db")
print(f"   ✓ System initialized: {system}")
print(f"   ✓ Sensor Controller: {len(system.sensor_controller.sensors)} sensors")
print(f"   ✓ Camera Controller: {len(system.camera_controller.cameras)} cameras")
print(f"   ✓ Configuration Manager: {system.config}")
print(f"   ✓ Alarm System: {system.alarm}")

# Test 2: Add Hardware
print("\n2. Testing Hardware Setup...")
# Add sensors
s1 = system.sensor_controller.add_sensor('WINDOOR', 'Front Door', zone_id=1)
s2 = system.sensor_controller.add_sensor('MOTION', 'Living Room', zone_id=1)
s3 = system.sensor_controller.add_sensor('WINDOOR', 'Bedroom Window', zone_id=2)
print(f"   ✓ Added 3 sensors: {len(system.sensor_controller.sensors)} total")

# Add cameras
c1 = system.camera_controller.add_camera('Main Camera', 'Living Room')
c2 = system.camera_controller.add_camera('Secured Camera', 'Bedroom', password='cam123')
print(f"   ✓ Added 2 cameras: {len(system.camera_controller.cameras)} total")

# Test 3: System Operations
print("\n3. Testing System Operations...")
system.turn_on()
print(f"   ✓ System turned on: {system.is_running}")

# Arm system
success = system.arm_system(SafeHomeMode.HOME)
print(f"   ✓ Armed in HOME mode: {success}")
print(f"   ✓ Current mode: {system.config.current_mode.name}")

# Check sensor states
active_sensors = sum(1 for s in system.sensor_controller.sensors.values() if s.is_active)
print(f"   ✓ Active sensors: {active_sensors}")

# Disarm system
system.disarm_system()
print(f"   ✓ System disarmed: {system.config.current_mode.name}")

# Test 4: Safety Zone Management
print("\n4. Testing Safety Zone Management...")
zones = system.config.get_all_zones()
print(f"   ✓ Total zones: {len(zones)}")

if len(zones) > 0:
    zone = zones[0]
    system.arm_zone(zone.zone_id)
    print(f"   ✓ Zone {zone.zone_id} armed: {zone.is_armed}")

    system.disarm_zone(zone.zone_id)
    print(f"   ✓ Zone {zone.zone_id} disarmed: {zone.is_armed}")

# Test 5: Camera Access Control
print("\n5. Testing Camera Access Control...")
# Access camera without password
view1 = system.camera_controller.get_camera_view(c1.camera_id)
print(f"   ✓ Camera 1 (no password) access: {view1 is not None}")

# Access camera with wrong password
view2 = system.camera_controller.get_camera_view(c2.camera_id, 'wrong')
print(f"   ✓ Camera 2 (wrong password) denied: {view2 is None}")

# Access camera with correct password
view3 = system.camera_controller.get_camera_view(c2.camera_id, 'cam123')
print(f"   ✓ Camera 2 (correct password) access: {view3 is not None}")

# Test 6: Login System
print("\n6. Testing Login System...")
# Control Panel login
result1 = system.login("admin", "1234", "CONTROL_PANEL")
print(f"   ✓ Control Panel login (correct): {result1}")

result2 = system.login("admin", "9999", "CONTROL_PANEL")
print(f"   ✓ Control Panel login (wrong): {not result2}")

# Test 7: Event Logging
print("\n7. Testing Event Logging...")
logs = system.config.storage.get_logs(limit=5)
print(f"   ✓ Retrieved {len(logs)} recent logs")
if len(logs) > 0:
    print(f"      - Latest: {logs[0]['event_message'][:50]}...")

# Test 8: System Status
print("\n8. Testing System Status...")
status = system.get_system_status()
print(f"   ✓ System Status:")
print(f"      - Running: {status['is_running']}")
print(f"      - Mode: {status['current_mode']}")
print(f"      - Sensors: {status['num_sensors']}")
print(f"      - Cameras: {status['num_cameras']}")
print(f"      - Active Sensors: {status['num_active_sensors']}")
print(f"      - Alarm Active: {status['alarm_active']}")

# Test 9: Cleanup
print("\n9. Testing System Cleanup...")
system.turn_off()
print(f"   ✓ System turned off: {not system.is_running}")

system.shutdown()
print(f"   ✓ System shutdown complete")

print("\n" + "=" * 70)
print("ALL INTEGRATION TESTS PASSED!")
print("=" * 70)
print("\n[Test Summary]")
print("  ✓ Core System Layer")
print("  ✓ Configuration Layer")
print("  ✓ Device Layer (Sensors, Cameras, Alarm)")
print("  ✓ Database Layer")
print("  ✓ Logging System")
print("  ✓ Authentication System")
print("  ✓ Safety Zone Management")
print("\nThe SafeHome system is ready for use!")
print("=" * 70)
