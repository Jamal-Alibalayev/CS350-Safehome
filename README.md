# SafeHome Security System

A comprehensive, simulated smart home security system featuring a graphical dashboard for real-time monitoring and control of sensors and cameras.

## ✨ Key Features

-   **Real-time GUI Dashboard:** A central dashboard to monitor all system activity.
-   **Multi-User Access:** Role-based access control with **Admin** (full control) and **Guest** (monitoring-only) roles.
-   **Comprehensive Security Modes:** Includes `Home`, `Away`, `Overnight`, `Extended`, and `Disarmed` modes to suit different scenarios.
-   **Live Camera Surveillance:** Monitor multiple live camera feeds with Pan-Tilt-Zoom (PTZ) controls and password protection capabilities.
-   **Sensor Network:** Simulates a network of window/door and motion sensors.
-   **Safety Zone Management:** Group sensors into logical zones (e.g., "Living Room", "Upstairs") for targeted arming/disarming.
-   **Event Logging:** View a detailed history of system events, from sensor triggers to mode changes.
-   **System Configuration:** Admins can configure system timers, user passwords, **email alerts and contact information**. **Includes automated email notifications for critical security events like master password changes.**
-   **Emergency Features:** Includes an admin-only **Panic Alarm** for immediate alerts and a **Silence Alarm** function.
-   **Built-in Sensor Simulator:** A utility to manually trigger virtual sensors to test system responses.

## 🚀 Getting Started

### Prerequisites

-   Python 3.x
-   Python Library Requirnments:
    -   Pillow
    -   Flask
    -   pytest

### Installation & Running

1.  **Clone the repository**
    ```bash
    git clone <https://github.com/Jamal-Alibalayev/CS350-Safehome.git>
    ```

2.  **Navigate to the project directory**
    ```bash
    cd CS350-Safehome
    ```

3.  **Install dependencies**
    Install the required libraries from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application**
    ```bash
    python main.py
    ```
    Executing this command will start the system and launch the login window.

## 📖 Usage

1.  Log in to the system using the default credentials (see `USER_MANUAL.md` for details).
2.  Use the main dashboard to monitor camera feeds and sensor statuses.
3.  Admins can change security modes, manage safety zones, and access system settings.

For a complete guide on how to use the application, please refer to the **[User Manual (USER_MANUAL.md)](USER_MANUAL.md)**.

## 🧪 Testing

This project uses `pytest` for automated testing. The tests are organized into `unit`, `integration`, and `system` directories.

To run all tests, execute the following command in the project root directory:
```bash
pytest
```

## 📂 Project Structure

```
CS350-Safehome/
├── safehome/               # Main application source code
│   ├── core/               # Core system logic
│   ├── interface/          # GUI components (dashboard, windows)
│   ├── device/             # Simulated device logic (cameras, sensors)
│   ├── configuration/      # Configuration and data management
│   └── database/           # Database interaction
├── tests/                  # Automated tests
│   ├── unit/
│   ├── integration/
│   └── system/
├── data/                   # Default data and assets
├── main.py                 # Application entry point
├── requirements.txt        # Project dependencies
└── README.md               # This README file
```

## 📚 Documentation
-   **[User Manual](https://github.com/Jamal-Alibalayev/CS350-Safehome/blob/alan/docs/USER_MANUAL.md):** Provides detailed instructions on how to use the application.
