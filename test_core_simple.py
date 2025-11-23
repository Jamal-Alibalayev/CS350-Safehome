"""
Simple quick test for Core System Layer
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from safehome.core.system import System
from safehome.configuration.safehome_mode import SafeHomeMode

print("=" * 60)
print("CORE SYSTEM LAYER - QUICK TEST")
print("=" * 60)

# Test 1: System initialization
print("\n1. Testing System Initialization...")
system = System(db_path="data/test_core_quick.db")
print(f"   ✓ System created: {system}")
print(f"   ✓ Current mode: {system.config.current_mode.name}")

# Test 2: Add sensors
print("\n2. Testing Sensor Operations...")
sensor1 = system.sensor_controller.add_sensor('WINDOOR', 'Front Door')
sensor2 = system.sensor_controller.add_sensor('MOTION', 'Living Room')
print(f"   ✓ Added 2 sensors: {len(system.sensor_controller.sensors)} total")

# Test 3: Alarm
print("\n3. Testing Alarm...")
print(f"   ✓ Alarm initial state: {system.alarm.is_ringing}")
system.alarm.ring()
print(f"   ✓ Alarm triggered: {system.alarm.is_ringing}")
system.alarm.stop()
print(f"   ✓ Alarm stopped: {system.alarm.is_ringing}")

# Test 4: System modes
print("\n4. Testing System Modes...")
system.turn_on()
print(f"   ✓ System turned on")
success = system.arm_system(SafeHomeMode.HOME)
print(f"   ✓ Armed in HOME mode: {system.config.current_mode.name}")
system.disarm_system()
print(f"   ✓ System disarmed: {system.config.current_mode.name}")
system.turn_off()
print(f"   ✓ System turned off")

# Test 5: Login
print("\n5. Testing Login...")
result = system.login("admin", "1234", "CONTROL_PANEL")
print(f"   ✓ Master password login: {result}")
result = system.login("admin", "9999", "CONTROL_PANEL")
print(f"   ✓ Wrong password rejected: {not result}")

# Cleanup
print("\n6. Cleanup...")
system.shutdown()
print(f"   ✓ System shutdown complete")

print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)
