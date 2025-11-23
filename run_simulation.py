# run_simulation.py
"""
SafeHome System Main Entry Point
Initializes and runs the complete SafeHome security system with all components
"""

import tkinter as tk
from safehome.core.system import System
from safehome.interface.control_panel.safehome_control_panel import SafeHomeControlPanel
from safehome.interface.control_panel.camera_monitor import CameraMonitor
from safehome.device.sensor.device_sensor_tester import DeviceSensorTester


def setup_hardware(system: System):
    """
    Initialize virtual hardware (sensors and cameras)
    Sets up a complete home security system for testing
    """
    print("\n[Setup] Initializing Virtual Hardware...")

    # 1. Setup Safety Zones (ensure they exist before adding sensors)
    print("  [Zones] Setting up safety zones...")
    zones = system.config.get_all_zones()

    # Create additional zone if needed (Kitchen)
    if len(zones) < 3:
        kitchen_zone = system.config.add_safety_zone("Kitchen")
        print(f"      - Created zone: Kitchen (ID: {kitchen_zone.zone_id})")

    zones = system.config.get_all_zones()
    print(f"  [Zones] Total zones: {len(zones)}")

    # Get zone IDs for reference
    zone_ids = [z.zone_id for z in zones]
    zone1_id = zone_ids[0] if len(zone_ids) > 0 else 1
    zone2_id = zone_ids[1] if len(zone_ids) > 1 else 2
    zone3_id = zone_ids[2] if len(zone_ids) > 2 else 3

    # 2. Add Sensors
    print("  [Sensors] Adding sensors to system...")
    # Living Room Zone (First zone)
    system.sensor_controller.add_sensor('WINDOOR', 'Living Room Window', zone_id=zone1_id)
    system.sensor_controller.add_sensor('WINDOOR', 'Front Door', zone_id=zone1_id)
    system.sensor_controller.add_sensor('MOTION', 'Living Room', zone_id=zone1_id)

    # Bedroom Zone (Second zone)
    system.sensor_controller.add_sensor('MOTION', 'Bedroom', zone_id=zone2_id)
    system.sensor_controller.add_sensor('WINDOOR', 'Bedroom Window', zone_id=zone2_id)

    # Kitchen Zone (Third zone)
    system.sensor_controller.add_sensor('WINDOOR', 'Back Door', zone_id=zone3_id)

    sensor_count = len(system.sensor_controller.sensors)
    print(f"  [Sensors] Added {sensor_count} sensors")

    # 3. Add Cameras
    print("  [Cameras] Adding cameras to system...")
    system.camera_controller.add_camera('Living Room Camera', 'Living Room')
    system.camera_controller.add_camera('Front Door Camera', 'Front Door', password='cam123')

    camera_count = len(system.camera_controller.cameras)
    print(f"  [Cameras] Added {camera_count} cameras")

    print("[Setup] Hardware initialized successfully!\n")


def main():
    """Main entry point for SafeHome simulation"""
    try:
        # 1. Create Tkinter root window (hidden)
        print("Creating Tkinter root window...")
        root = tk.Tk()
        root.withdraw()
        print("✓ Tkinter root created\n")

        # 2. Initialize System (this initializes all subsystems)
        print("=" * 60)
        print("SafeHome Security System")
        print("=" * 60)
        print("[System] Initializing Core System...")
        system = System()
        print("✓ System initialized\n")

        # 3. Setup virtual hardware
        setup_hardware(system)

        # 4. Turn on the system
        print("[System] Starting system...")
        system.turn_on()
        print("[System] System is now running (sensor polling active)\n")

        # 5. Launch Sensor Test GUI (simulates physical environment)
        print("[GUI] Launching Sensor Simulator...")
        try:
            DeviceSensorTester.showSensorTester()
            print("✓ Sensor Simulator launched")
        except Exception as e:
            print(f"⚠ Warning: Could not launch Sensor Simulator: {e}")

        # 6. Launch Control Panel GUI (simulates wall-mounted keypad)
        print("[GUI] Launching Control Panel...")
        control_panel = SafeHomeControlPanel(master=root, system=system)
        print("✓ Control Panel launched\n")

        # 7. Camera Monitor will be launched on demand
        # Note: To open camera monitor, you can manually create it after the system starts
        # Example: camera_monitor = CameraMonitor(master=root, system=system, camera_id=1)
        print("[INFO] Camera Monitor available (can be opened manually if needed)")

        # Window close handler
        def on_close():
            print("\n[System] Shutting down...")
            print("[System] Saving configuration...")
            system.config.save_configuration()

            print("[System] Stopping all services...")
            system.shutdown()

            print("[System] Cleanup complete. Goodbye!")
            root.destroy()
            exit()

        control_panel.protocol("WM_DELETE_WINDOW", on_close)

        # Print usage instructions
        print("\n" + "=" * 60)
        print("SIMULATION STARTED")
        print("=" * 60)
        print("\n[Usage Instructions]")
        print("  1. Use 'Sensor Test' window to simulate door/window opening")
        print("     and motion detection.")
        print("\n  2. Use 'Control Panel' to:")
        print("     - Login (Default password: 1234)")
        print("     - Arm/Disarm system (1=Away, 2=Home, 0=Disarm)")
        print("     - Change password (3=Set Password)")
        print("     - Switch zones (9=Zone Change)")
        print("\n  3. Camera Monitor:")
        print("     - Available in the code for manual opening")
        print("     - Can view live feed and control PTZ")
        print("\n[System Information]")
        print(f"  - Sensors: {len(system.sensor_controller.sensors)}")
        print(f"  - Cameras: {len(system.camera_controller.cameras)}")
        print(f"  - Safety Zones: {len(system.config.get_all_zones())}")
        print(f"  - Current Mode: {system.config.current_mode.name}")
        print(f"  - System Running: {system.is_running}")
        print("\n" + "=" * 60 + "\n")

        # Start Tkinter main loop
        print("[System] Starting GUI event loop...")
        root.mainloop()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print("\n[System] Exiting due to error...")


if __name__ == "__main__":
    main()
