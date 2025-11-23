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

    # 1. Add Sensors
    print("  [Sensors] Adding sensors to system...")
    # Living Room Zone (Zone 1)
    system.sensor_controller.add_sensor('WINDOOR', 'Living Room Window', zone_id=1)
    system.sensor_controller.add_sensor('WINDOOR', 'Front Door', zone_id=1)
    system.sensor_controller.add_sensor('MOTION', 'Living Room', zone_id=1)

    # Bedroom Zone (Zone 2)
    system.sensor_controller.add_sensor('MOTION', 'Bedroom', zone_id=2)
    system.sensor_controller.add_sensor('WINDOOR', 'Bedroom Window', zone_id=2)

    # Kitchen Zone (Zone 3)
    system.sensor_controller.add_sensor('WINDOOR', 'Back Door', zone_id=3)

    sensor_count = len(system.sensor_controller.sensors)
    print(f"  [Sensors] Added {sensor_count} sensors")

    # 2. Add Cameras
    print("  [Cameras] Adding cameras to system...")
    system.camera_controller.add_camera('Living Room Camera', 'Living Room')
    system.camera_controller.add_camera('Front Door Camera', 'Front Door', password='cam123')

    camera_count = len(system.camera_controller.cameras)
    print(f"  [Cameras] Added {camera_count} cameras")

    # 3. Configure Safety Zones
    print("  [Zones] Configuring safety zones...")
    # Zones should already exist from ConfigurationManager initialization
    # But we can verify/add if needed
    zones = system.config.get_all_zones()
    print(f"  [Zones] Configured {len(zones)} safety zones")

    print("[Setup] Hardware initialized successfully!\n")


def main():
    """Main entry point for SafeHome simulation"""
    # 1. Create Tkinter root window (hidden)
    root = tk.Tk()
    root.withdraw()

    # 2. Initialize System (this initializes all subsystems)
    print("=" * 60)
    print("SafeHome Security System")
    print("=" * 60)
    print("[System] Initializing Core System...")
    system = System()

    # 3. Setup virtual hardware
    setup_hardware(system)

    # 4. Turn on the system
    print("[System] Starting system...")
    system.turn_on()
    print("[System] System is now running (sensor polling active)")

    # 5. Launch Sensor Test GUI (simulates physical environment)
    print("\n[GUI] Launching Sensor Simulator...")
    DeviceSensorTester.showSensorTester()

    # 6. Launch Control Panel GUI (simulates wall-mounted keypad)
    print("[GUI] Launching Control Panel...")
    control_panel = SafeHomeControlPanel(master=root, system=system)

    # 7. Launch Camera Monitor (first camera)
    print("[GUI] Launching Camera Monitor...")
    if len(system.camera_controller.cameras) > 0:
        # Get first camera
        first_camera_id = list(system.camera_controller.cameras.keys())[0]
        camera_monitor = CameraMonitor(
            master=root,
            system=system,
            camera_id=first_camera_id
        )
    else:
        print("[GUI] No cameras available for monitoring")
        camera_monitor = None

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
    print("\n  3. Use 'Camera Monitor' to:")
    print("     - View live camera feed")
    print("     - Control Pan/Tilt/Zoom")
    print("\n[System Information]")
    print(f"  - Sensors: {len(system.sensor_controller.sensors)}")
    print(f"  - Cameras: {len(system.camera_controller.cameras)}")
    print(f"  - Safety Zones: {len(system.config.get_all_zones())}")
    print(f"  - Current Mode: {system.config.current_mode.name}")
    print(f"  - System Running: {system.is_running}")
    print("\n" + "=" * 60 + "\n")

    # Start Tkinter main loop
    root.mainloop()


if __name__ == "__main__":
    main()
