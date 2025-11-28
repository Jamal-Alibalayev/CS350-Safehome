# SafeHome Security System - User Manual

This document provides a comprehensive guide to using the SafeHome Security System dashboard.

## 1. Getting Started

### 1.1. Running the Application

To start the SafeHome system, execute the main simulation script from your terminal:

```bash
python run_simulation.py
```

This will initialize the core system, set up the virtual hardware (sensors and cameras), and launch the login window.

## 2. Login

Upon startup, you will be presented with the login window. You can log in as one of two user types:

-   **Admin**: Has full control over the system, including system settings.
-   **Guest**: Has limited access, primarily for monitoring.

**Default Passwords:**
-   **Admin Password**: `1234`
-   **Guest Password**: `0000`

Select the user type, enter the password, and click "Login". After too many failed attempts, the system will temporarily lock you out.

## 3. The Main Dashboard

The main dashboard is the central hub for monitoring and controlling your SafeHome system.

![Main Dashboard](docs/dashboard_overview.png) (*Note: Image path is a placeholder.*)

### 3.1. Header Bar
-   **Title**: Displays the application name.
-   **System Status**: Shows the current system mode (e.g., `DISARMED`, `AWAY`) and running status.
-   **LOGS**: Opens the event log viewer to see a history of system activities, including intrusions.
-   **LOGOUT**: Logs you out and returns to the login screen.
-   **SETTINGS** (Admin only): Opens the system settings window.

### 32. Live Camera Feeds
This section displays the live video feeds from the system's cameras. For each camera, you can:
-   **Pan/Tilt/Zoom (PTZ)**: Use the `^`, `v`, `<`, `>` buttons to pan and tilt, and the `+`, `-` buttons to zoom.
-   **Enable/Disable**: Turn individual cameras on or off.

### 3.3. System Control
This panel allows you to change the system's security mode.
-   **Home**: Arms the system for when you are at home (e.g., perimeter sensors active).
-   **Away**: Arms the system for when you are away (all sensors active).
-   **Overnight / Extended**: Special modes for travel.
-   **Disarm**: Deactivates all sensors and stops any active alarms.
-   **OPEN SENSOR SIMULATOR**: Launches a tool that lets you manually trigger sensors to test the system's response.

### 3.4. Sensor Status
This table provides a real-time list of all sensors, their type, location, assigned zone, and current status (Armed/Disarmed).

### 3.5. Safety Zones
This box shows a quick overview of the configured safety zones and the number of sensors in each.
-   Click **MANAGE ZONES** to open the Zone Manager.

### 3.6. Quick Actions
-   **PANIC ALARM**: Immediately triggers the system alarm. Use this in an emergency.
-   **SILENCE ALARM**: Stops an active alarm siren. Note that this only silences the alarm; it does not disarm the system.

## 4. Zone Manager

The Zone Manager allows you to organize your sensors into logical groups called "Safety Zones".

-   **To Add a Zone**: Click the "Add Zone" button, enter a name, and click "Create".
-   **To Edit a Zone**: Select a zone from the list and click "Edit Zone". Enter the new name and click "Save".
-   **To Delete a Zone**: Select a zone from the list and click "Delete Zone". Confirm the deletion.
-   **To Assign Sensors**: Select a zone from the list and click "Assign Sensors". In the dialog, check the boxes next to the sensors you want to assign to that zone and click "Assign".

## 5. System Settings (Admin Only)

The settings window allows administrators to configure core system parameters.

-   **Passwords**: Change the Master (Admin) and Guest passwords.
-   **Timers**: Adjust the `Entry Delay` (time to disarm after entry) and `Exit Delay` (time to leave after arming).
-   **Contact Info**: Set phone numbers and email addresses for alerts.
-   **Reset System**: Click the **Reset System** button to restore all settings to their factory defaults. This includes passwords, zones, and timers. **This action is irreversible.**

Click **Save** to apply any changes.

## 6. Sensor Simulator

The sensor simulator is a powerful tool for testing. You can open it from the "System Control" panel on the main dashboard. It displays a list of all sensors. Clicking the "Trigger" button next to a sensor will simulate that sensor detecting an event (e.g., a door opening). This is useful for testing how the system responds to intrusions in different modes.
