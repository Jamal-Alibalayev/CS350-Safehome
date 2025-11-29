# run_simulation.py
"""
SafeHome System Main Entry Point
Initializes and runs the complete SafeHome security system with all components

"""

import tkinter as tk
from safehome.core.system import System
from safehome.interface.dashboard import LoginWindow
from safehome.device.sensor.device_sensor_tester import DeviceSensorTester


def setup_hardware(system: System):
    """
    Initialize virtual hardware based on fixed floor plan
    This function now calls the system's reset configuration to ensure a clean slate.
    """
    print("\n[Setup] Resetting system to default hardware configuration...")
    # This single call robustly clears the DB, resets ID counters, and creates default zones.
    system.config.reset_configuration()
    print("  [Zones] System reset. Default zones created.")

    zones = system.config.get_all_zones()
    print(f"  [Zones] Total zones: {len(zones)}")

    # Get zone IDs by name
    zone_map = {z.name: z.zone_id for z in zones}
    dr_zone = zone_map.get("Dining Room")
    kit_zone = zone_map.get("Kitchen")
    lr_zone = zone_map.get("Living Room")

    # 2. Add Sensors based on floor plan
    print("  [Sensors] Adding sensors to system...")

    # Reset sensor ID counter to ensure IDs start from 1
    system.sensor_controller._next_sensor_id = 1

    # Window Sensors (6 total)
    # Dining Room: S₁, S₂ (2 windows)
    system.sensor_controller.add_sensor("WINDOOR", "DR Window 1", zone_id=dr_zone)
    system.sensor_controller.add_sensor("WINDOOR", "DR Window 2", zone_id=dr_zone)

    # Kitchen: S₂, S₃ (1 window - using only S₃ for kitchen window)
    system.sensor_controller.add_sensor("WINDOOR", "Kitchen Window", zone_id=kit_zone)

    # Living Room: S₄, S₅, S₆ (3 windows)
    system.sensor_controller.add_sensor("WINDOOR", "LR Window 1", zone_id=lr_zone)
    system.sensor_controller.add_sensor("WINDOOR", "LR Window 2", zone_id=lr_zone)
    system.sensor_controller.add_sensor("WINDOOR", "LR Window 3", zone_id=lr_zone)

    # Door Sensors (2 total)
    # Door 1: Hallway (between DR and LR - north end)
    system.sensor_controller.add_sensor("WINDOOR", "Hallway Door", zone_id=dr_zone)

    # Door 2: Kitchen door
    system.sensor_controller.add_sensor("WINDOOR", "Kitchen Door", zone_id=kit_zone)

    # Motion Detectors (2 total)
    # M₁: Dining Room to Living Room (crosses zones)
    # Since motion detectors can span zones, we'll assign to DR but note it covers both
    system.sensor_controller.add_sensor("MOTION", "Motion DR-LR", zone_id=dr_zone)

    # M₂: Kitchen (diagonal, within kitchen only)
    system.sensor_controller.add_sensor("MOTION", "Motion Kitchen", zone_id=kit_zone)

    sensor_count = len(system.sensor_controller.sensors)
    print(f"  [Sensors] Added {sensor_count} sensors (6 windows, 2 doors, 2 motion)")

    # 3. Add Cameras - 3 fixed cameras based on floor plan
    print("  [Cameras] Adding cameras to system...")

    # Reset camera ID counter to ensure IDs start from 1
    system.camera_controller._next_camera_id = 1

    # Camera 1: Dining Room (camera1.jpg)
    cam1 = system.camera_controller.add_camera("Dining Room Camera", "Dining Room")
    print(f"      - Camera 1: {cam1.name} (ID: {cam1.camera_id})")

    # Camera 2: Kitchen (camera2.jpg)
    cam2 = system.camera_controller.add_camera("Kitchen Camera", "Kitchen")
    print(f"      - Camera 2: {cam2.name} (ID: {cam2.camera_id})")

    # Camera 3: Living Room (camera3.jpg - NOT .png!)
    cam3 = system.camera_controller.add_camera("Living Room Camera", "Living Room")
    print(f"      - Camera 3: {cam3.name} (ID: {cam3.camera_id})")

    camera_count = len(system.camera_controller.cameras)
    print(f"  [Cameras] Added {camera_count} cameras (DR, Kitchen, LR)")

    print("[Setup] Hardware initialized successfully!\n")


def main():
    """Main entry point for SafeHome simulation"""
    try:
        # 1. Initialize System (this initializes all subsystems)
        print("=" * 60)
        print("SafeHome Security System")
        print("=" * 60)
        print("[System] Initializing Core System...")
        system = System()
        print("✓ System initialized\n")

        # 2. Setup virtual hardware
        setup_hardware(system)

        # 3. Turn on the system
        print("[System] Starting system...")
        system.turn_on()
        print("[System] System is now running (sensor polling active)\n")

        # 4. Launch Login Window (Main Entry Point)
        # Note: Sensor Test GUI will be available from within the dashboard
        print("[GUI] Launching SafeHome Dashboard...")
        login_window = LoginWindow(system)
        print("✓ Dashboard launched\n")

        # Window close handler
        def on_close():
            print("\n[System] Shutting down...")
            print("[System] Saving configuration...")
            system.config.save_configuration()

            print("[System] Stopping all services...")
            system.shutdown()

            print("[System] Cleanup complete. Goodbye!")
            login_window.destroy()
            exit()

        login_window.protocol("WM_DELETE_WINDOW", on_close)

        # Print usage instructions
        print("\n" + "=" * 60)
        print("SIMULATION STARTED")
        print("=" * 60)
        print("\n[Usage Instructions]")
        print("  1. Login to SafeHome Dashboard:")
        print("     - Default Admin password: 1234")
        print("     - Default Guest password: 0000")
        print("\n  2. Main Dashboard features:")
        print("     - View all 3 camera feeds (Dining Room, Kitchen, Living Room)")
        print("     - Monitor 10 sensors (6 windows, 2 doors, 2 motion detectors)")
        print("     - Arm/Disarm system (Away/Home/Disarm modes)")
        print("     - Manage 3 safety zones (Dining Room, Kitchen, Living Room)")
        print("     - Open Sensor Simulator to test sensors")
        print("     - View event logs")
        print("     - Control camera PTZ")
        print("\n[System Information - Fixed Floor Plan]")
        print(f"  - Cameras: {len(system.camera_controller.cameras)} (DR, Kitchen, LR)")
        print(
            f"  - Sensors: {len(system.sensor_controller.sensors)} (6 Win, 2 Door, 2 Motion)"
        )
        print(
            f"  - Safety Zones: {len(system.config.get_all_zones())} (DR, Kitchen, LR)"
        )
        print(f"  - Current Mode: {system.config.current_mode.name}")
        print(f"  - System Running: {system.is_running}")
        print("\n" + "=" * 60 + "\n")

        # Start Tkinter main loop
        print("[System] Starting GUI event loop...")
        login_window.mainloop()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        print("\n[System] Exiting due to error...")


if __name__ == "__main__":
    main()
