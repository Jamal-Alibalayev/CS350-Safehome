# SafeHome Security System - User Manual

This document provides a comprehensive guide to using the SafeHome Security System dashboard.

## 1. Getting Started

### 1.1. Running the Application

To start the SafeHome system, execute the main simulation script from your terminal:

```bash
python main.py
```

This will initialize the core system with default sensors and mode configurations, set up the virtual hardware (sensors and cameras), and launch the login window.

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

![Main Dashboard](https://github.com/Jamal-Alibalayev/CS350-Safehome/blob/alan/docs/images/main_dashborad_win.png) (*Note: this screenshot is for windows system*)

### 3.1. Header Bar
-   **Title**: Displays the application name and subtitle.
-   **System Status**: Shows the current system mode (e.g., `DISARMED`, `AWAY`) and running status (`SYSTEM RUNNING` or `SYSTEM STOPPED`).
-   **LOGS**: Opens the event log viewer to see a history of system activities, including intrusions.
-   **LOGOUT**: Logs you out and returns to the login screen.
-   **SETTINGS** (Admin only): Opens the system settings window.

### 3.2. Live Camera Feeds
This section displays the live video feeds from the system's cameras.

**Camera Controls:**
-   **Pan/Tilt/Zoom (PTZ)**: Use the `^`, `v`, `<`, `>` buttons to pan and tilt, and the `+`, `-` buttons to zoom. This is available to both Admin and Guest users.
-   **Enable/Disable**: Turn individual cameras on or off (Admin only).

**Camera Status Indicators:**
The camera view will display different statuses to keep you informed:
-   **Password Required**: (Admin) You need to enter a password to view this feed.
-   **Password Protected**: (Guest) This camera is password-protected and cannot be viewed by guests.
-   **Access Denied**: The password you entered was incorrect.
-   **Disabled**: The camera has been manually turned off.
-   **No Signal**: The camera is experiencing a connection issue.

**Camera Password Management (Admin only):**
Below each camera, administrators will find two buttons for managing security:
-   **Set/Change**: Set a new password for the camera or change an existing one.
-   **Delete**: Remove the password from the camera.

### 3.3. System Control
This panel allows you to change the system's security mode, which directly controls the armed/disarmed state of associated sensors.
-   **Home**: Arms the system for when you are at home (e.g., perimeter sensors active).
-   **Away**: Arms the system for when you are away (all sensors active).
-   **Overnight / Extended**: Special modes for travel.
-   **Disarm**: Deactivates all sensors and stops any active alarms.
-   **OPEN SENSOR SIMULATOR**: Launches a tool that lets you manually trigger sensors to test the system's response.

### 3.4. Sensor Status
This table provides a real-time list of all sensors, their type, location, assigned zone, and current status (`● Armed` or `○ Disarmed`).

### 3.5. Safety Zones
This box shows a quick overview of the configured safety zones. Each zone in the list displays its armed status (`●` or `○`) and the number of sensors it contains.
-   Click **MANAGE ZONES** to open the Zone Manager.

### 3.6. Quick Actions (Admin Only)
These actions are available only to administrators for immediate response.
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
    -   **Security Note**: When the Master (Admin) password is changed, the system will automatically send a notification email to the configured "Alert Email" address.
-   **Timers**: Adjust system time-based behaviors:
    -   `Entry Delay`: The grace period in seconds to disarm the system after an entry sensor is triggered.
    -   `Exit Delay`: The grace period in seconds to leave the premises after arming the system.
    -   `Lock Time`: The duration in seconds the system will lock you out after too many failed login attempts.
-   **Contact Info**: Set phone numbers and email addresses for alerts.
-   **Reset System**: Click the **Reset System** button to restore all settings to their factory defaults. This includes passwords, zones, and timers. **This action is irreversible.**

Click **Save** to apply any changes.

## 6. Sensor Simulator (Live Mode)

The Sensor Simulator is now a powerful, real-time diagnostic and control tool that directly interacts with the live sensors in your SafeHome system. You can open it from the "System Control" panel on the main dashboard.

**Key Features:**
-   **Live Sensor Status:** Displays a real-time list of all sensors, showing their current Armed/Disarmed state and their physical state (e.g., "Open"/"Closed" for window/door sensors, "Detected"/"Clear" for motion sensors). This status is synchronized with the main system.
-   **Direct Control:** You can directly arm/disarm individual sensors or trigger/release their physical state (e.g., simulate a door opening or motion detection). Any actions taken here will immediately affect the actual system's sensor states and be reflected on the main dashboard.
-   **Quick Actions:** Use "ARM ALL", "DISARM ALL", or "CLOSE/CLEAR ALL" to quickly manage all sensors.

This tool is invaluable for testing how the system responds to different sensor states and security modes.
