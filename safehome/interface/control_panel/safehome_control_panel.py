# safehome/interface/control_panel/safehome_control_panel.py

from safehome.configuration.safehome_mode import SafeHomeMode
from safehome.core.system import System

from .device_control_panel_abstract import DeviceControlPanelAbstract


class SafeHomeControlPanel(DeviceControlPanelAbstract):
    """
    SafeHome Control Panel implementation
    Connects GUI button events with System business logic
    Integrates with Core System Layer for full functionality
    """

    def __init__(self, master=None, system: System = None):
        super().__init__(master)

        # Inject System instance
        self.system = system if system else System()

        # Internal state
        self.input_buffer = ""
        self.is_authenticated = False

        # Password change mode state
        self.is_changing_password = False
        # Store current valid password for change authorization
        self.current_valid_password = None

        # Initialize UI state
        self._refresh_status_display()
        self._reset_interaction()

    def _refresh_status_display(self):
        """Refresh LED and LCD based on System state"""
        mode = self.system.config.current_mode

        # 1. Update LED status
        is_armed = mode in [
            SafeHomeMode.ARMED_AWAY,
            SafeHomeMode.ARMED_STAY,
            SafeHomeMode.HOME,
            SafeHomeMode.AWAY,
            SafeHomeMode.OVERNIGHT,
            SafeHomeMode.EXTENDED,
        ]
        self.set_armed_led(is_armed)
        self.set_powered_led(self.system.is_running)

        # 2. Update LCD status text
        self.set_display_away(
            mode in [SafeHomeMode.ARMED_AWAY, SafeHomeMode.AWAY, SafeHomeMode.EXTENDED]
        )
        self.set_display_stay(
            mode in [SafeHomeMode.ARMED_STAY, SafeHomeMode.HOME, SafeHomeMode.OVERNIGHT]
        )

        if mode == SafeHomeMode.DISARMED:
            self.set_display_not_ready(True)
        else:
            self.set_display_not_ready(False)

        # Update Security Zone display
        try:
            current_zone = self.system.config.get_current_zone()
            if current_zone:
                self.set_security_zone_number(current_zone.zone_id)
        except Exception as e:
            print(f"Warning: Could not set security zone number: {e}")

    def _reset_interaction(self):
        """Reset interaction state"""
        self.input_buffer = ""
        self.is_authenticated = False
        self.is_changing_password = False
        self.current_valid_password = None

        self.set_display_short_message1("Welcome To SafeHome System")
        self.set_display_short_message2("Enter Code + #")

    def _handle_key_input(self, key):
        """Handle numeric key input"""
        # Scenario 1: In password change mode, input is new password
        if self.is_changing_password:
            self.input_buffer += key
            mask = "*" * len(self.input_buffer)
            self.set_display_short_message2(f"New: {mask}")

        # Scenario 2: Already logged in, input is menu command
        elif self.is_authenticated:
            self._handle_command(key)

        # Scenario 3: Not logged in, input is login password
        else:
            self.input_buffer += key
            mask = "*" * len(self.input_buffer)
            self.set_display_short_message2(f"Code: {mask}")

    def _handle_command(self, key):
        """Handle commands (only valid after login)"""
        msg = ""
        success = False

        if key == "1":  # 1 = Arm Away
            arm_success = self.system.arm_system(SafeHomeMode.AWAY)
            if arm_success:
                msg = "ARMED (AWAY)"
                success = True
            else:
                msg = "Cannot Arm"
                self.set_display_short_message1(msg)
                self.set_display_short_message2("Windows/Doors Open")
                return  # Exit early to preserve the specific error message

        elif key == "2":  # 2 = Arm Stay (Home)
            arm_success = self.system.arm_system(SafeHomeMode.HOME)
            if arm_success:
                msg = "ARMED (HOME)"
                success = True
            else:
                msg = "Cannot Arm"
                self.set_display_short_message1(msg)
                self.set_display_short_message2("Windows/Doors Open")
                return  # Exit early to preserve the specific error message

        elif key == "0":  # 0 = Disarm
            self.system.disarm_system()
            msg = "DISARMED"
            success = True

        elif key == "3":  # 3 = Change Password
            self.is_changing_password = True
            self.input_buffer = ""
            self.set_display_short_message1("CHANGE PASSWORD")
            self.set_display_short_message2("Enter New Password + #")
            return  # Don't end session, enter change mode

        elif key == "9":  # 9 = Change Zone
            new_zone = self.system.config.next_zone()
            self.set_display_short_message1("Zone Changed:")
            self.set_display_short_message2(new_zone.name if new_zone else "None")
            self._refresh_status_display()
            return  # Don't end session

        else:
            msg = "Invalid Cmd"

        self.set_display_short_message1(msg)

        if success:
            self.set_display_short_message2("Session Ended")
            self._refresh_status_display()
            # Logout after arm/disarm operation
            self.is_authenticated = False
            self.input_buffer = ""
        else:
            # If command invalid, keep menu displayed
            self.set_display_short_message2("1:Away 2:Home 3:Set 0:Disarm 9:Zone")

    def _attempt_login(self):
        """Attempt login"""
        if not self.input_buffer:
            return

        user_id = "admin"
        password = self.input_buffer

        success = self.system.login(user_id, password, "CONTROL_PANEL")

        if success:
            self.is_authenticated = True
            self.current_valid_password = (
                password  # Save old password for change verification
            )
            self.set_display_short_message1("Login Success")
            self.set_display_short_message2("1:Away 2:Home 3:Set 0:Disarm 9:Zone")
            self.input_buffer = ""
        else:
            self.is_authenticated = False
            self.current_valid_password = None
            self.input_buffer = ""

            # Check if system is locked
            if self.system.config.login_manager.is_locked.get("CONTROL_PANEL", False):
                self.set_display_short_message1("SYSTEM LOCKED")
                self.set_display_short_message2("Too many attempts")
            else:
                self.set_display_short_message1("Login Failed")
                self.set_display_short_message2("Try Again")

    def _attempt_change_password(self):
        """Attempt to change password"""
        new_password = self.input_buffer

        # Simple validation: password must not be empty and must be digits
        if not new_password or not new_password.isdigit():
            self.set_display_short_message1("Invalid Format")
            self.set_display_short_message2("Digits Only")
            self.input_buffer = ""
            return

        # Call System to change password
        result = self.system.change_password(
            self.current_valid_password, new_password, "CONTROL_PANEL"
        )

        if result:
            self.set_display_short_message1("PASSWORD CHANGED")
            self.set_display_short_message2("Please Relogin")

            # Save configuration
            self.system.config.save_configuration()

            # Force logout, reset all state
            self.is_authenticated = False
            self.is_changing_password = False
            self.current_valid_password = None
            self.input_buffer = ""
        else:
            self.set_display_short_message1("Change Failed")
            self.set_display_short_message2("System Error")
            self.is_changing_password = False
            self.input_buffer = ""

    # --- Button event implementations ---

    def button1(self):
        self._handle_key_input("1")

    def button2(self):
        self._handle_key_input("2")

    def button3(self):
        self._handle_key_input("3")

    def button4(self):
        self._handle_key_input("4")

    def button5(self):
        self._handle_key_input("5")

    def button6(self):
        self._handle_key_input("6")

    def button7(self):
        self._handle_key_input("7")

    def button8(self):
        self._handle_key_input("8")

    def button9(self):
        self._handle_key_input("9")

    def button0(self):
        self._handle_key_input("0")

    def button_star(self):
        """* key: Cancel/Reset"""
        self._reset_interaction()

    def button_sharp(self):
        """# key: Confirm"""
        if self.is_changing_password:
            # In password change mode, # confirms new password
            self._attempt_change_password()
        elif not self.is_authenticated:
            # Not logged in, # confirms login
            self._attempt_login()
        # If logged in and not in change mode, # has no function (or could be logout)

    def button_panic(self):
        """Panic button: Trigger alarm immediately"""
        self.system.config.set_mode(SafeHomeMode.PANIC)
        self.system.alarm.ring()
        self.set_display_short_message1("PANIC ALARM!")
        self.set_display_short_message2("Emergency Services Called")
        self._refresh_status_display()
