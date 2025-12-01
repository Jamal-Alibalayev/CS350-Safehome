import tkinter as tk
import pytest
from unittest.mock import MagicMock, patch

from safehome.interface.dashboard.main_dashboard import MainDashboard
from safehome.configuration.safehome_mode import SafeHomeMode

@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    """Set headless environment to prevent actual UI windows from opening."""
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")

@pytest.fixture
def mock_system():
    """Create a mock of the core System object."""
    system = MagicMock()
    system.config.current_mode.name = "DISARMED"
    system.is_running = True
    system.camera_controller.cameras.values.return_value = []
    system.sensor_controller.get_all_sensors.return_value = []
    system.config.get_all_zones.return_value = []
    return system

@pytest.fixture(scope="function")
def admin_dashboard(mock_system):
    """Fixture to create a MainDashboard instance for an admin user."""
    with patch('safehome.interface.dashboard.main_dashboard.tk.Toplevel'), \
         patch('safehome.interface.dashboard.main_dashboard.tk.Frame'), \
         patch('safehome.interface.dashboard.main_dashboard.tk.Label'), \
         patch('safehome.interface.dashboard.main_dashboard.tk.Button'), \
         patch('safehome.interface.dashboard.main_dashboard.tk.Listbox'), \
         patch('safehome.interface.dashboard.main_dashboard.ttk.Treeview'), \
         patch('safehome.interface.dashboard.main_dashboard.ImageTk'), \
         patch('safehome.interface.dashboard.main_dashboard.messagebox') as mock_messagebox, \
         patch('safehome.interface.dashboard.main_dashboard.simpledialog') as mock_simpledialog:

        with patch.object(MainDashboard, '_update_loop', lambda self: None):
            dash = MainDashboard(system=mock_system, login_window=MagicMock(), user_id="admin")
            dash.mock_messagebox = mock_messagebox
            dash.mock_simpledialog = mock_simpledialog
            dash.user_id = "admin"
            yield dash

@pytest.fixture(scope="function")
def guest_dashboard(mock_system):
    """Fixture to create a MainDashboard instance for a guest user."""
    with patch('safehome.interface.dashboard.main_dashboard.tk.Toplevel'), \
         patch('safehome.interface.dashboard.main_dashboard.tk.Frame'), \
         patch('safehome.interface.dashboard.main_dashboard.tk.Label'), \
         patch('safehome.interface.dashboard.main_dashboard.tk.Button'), \
         patch('safehome.interface.dashboard.main_dashboard.tk.Listbox'), \
         patch('safehome.interface.dashboard.main_dashboard.ttk.Treeview'), \
         patch('safehome.interface.dashboard.main_dashboard.ImageTk'), \
         patch('safehome.interface.dashboard.main_dashboard.messagebox') as mock_messagebox, \
         patch('safehome.interface.dashboard.main_dashboard.simpledialog') as mock_simpledialog:

        with patch.object(MainDashboard, '_update_loop', lambda self: None):
            dash = MainDashboard(system=mock_system, login_window=MagicMock(), user_id="guest")
            dash.mock_messagebox = mock_messagebox
            dash.mock_simpledialog = mock_simpledialog
            dash.user_id = "guest"
            yield dash

def test_dashboard_logout_force(admin_dashboard):
    """
    UT-Dashboard-LogoutForce: Test the forced logout path.
    测试强制登出。
    """
    admin_dashboard.destroy = MagicMock()
    admin_dashboard.login_window.deiconify = MagicMock()
    
    admin_dashboard._logout(force_logout=True)
    
    admin_dashboard.destroy.assert_called_once()
    admin_dashboard.login_window.deiconify.assert_called_once()
    admin_dashboard.mock_messagebox.askyesno.assert_not_called()

def test_dashboard_logout_confirm(admin_dashboard):
    """
    UT-Dashboard-LogoutConfirm: Test the user-confirmed logout path.
    测试用户确认登出。
    """
    admin_dashboard.destroy = MagicMock()
    admin_dashboard.login_window.deiconify = MagicMock()
    admin_dashboard.mock_messagebox.askyesno.return_value = True
    
    admin_dashboard._logout(force_logout=False)
    
    admin_dashboard.mock_messagebox.askyesno.assert_called_once()
    admin_dashboard.destroy.assert_called_once()
    admin_dashboard.login_window.deiconify.assert_called_once()

def test_dashboard_logout_cancel(admin_dashboard):
    """
    UT-Dashboard-LogoutCancel: Test when user cancels the logout dialog.
    测试用户取消登出。
    """
    admin_dashboard.destroy = MagicMock()
    admin_dashboard.login_window.deiconify = MagicMock()
    admin_dashboard.mock_messagebox.askyesno.return_value = False
    
    admin_dashboard._logout(force_logout=False)
    
    admin_dashboard.mock_messagebox.askyesno.assert_called_once()
    admin_dashboard.destroy.assert_not_called()
    admin_dashboard.login_window.deiconify.assert_not_called()

def test_dashboard_on_close(admin_dashboard):
    """
    UT-Dashboard-OnClose: Test the window close handler.
    测试窗口关闭事件的处理。
    """
    admin_dashboard.system.shutdown = MagicMock()
    admin_dashboard.login_window.destroy = MagicMock()
    
    # User confirms quit
    admin_dashboard.mock_messagebox.askokcancel.return_value = True
    admin_dashboard._on_close()
    admin_dashboard.system.shutdown.assert_called_once()
    admin_dashboard.login_window.destroy.assert_called_once()
    
    # User cancels quit
    admin_dashboard.system.shutdown.reset_mock()
    admin_dashboard.login_window.destroy.reset_mock()
    admin_dashboard.mock_messagebox.askokcancel.return_value = False
    admin_dashboard._on_close()
    admin_dashboard.system.shutdown.assert_not_called()
    admin_dashboard.login_window.destroy.assert_not_called()

def test_dashboard_permission_denied_actions(guest_dashboard):
    """
    UT-Dashboard-Permissions: Test that actions are blocked for guest users.
    测试访客用户执行受限操作时的权限拒绝逻辑。
    """
    # List of methods and their expected permission error messages
    actions = [
        (guest_dashboard._set_mode, (SafeHomeMode.AWAY,), "Guest account cannot change system mode."),
        (guest_dashboard._trigger_panic, (), "Guest account cannot trigger panic alarm."),
        (guest_dashboard._silence_alarm, (), "Guest account cannot silence the alarm."),
        (guest_dashboard._open_zone_manager, (), "Guest account cannot manage zones."),
        (guest_dashboard._open_log_viewer, (), "Guest account cannot view system logs."),
        (guest_dashboard._open_sensor_simulator, (), "Guest account cannot open the sensor simulator."),
        (guest_dashboard._toggle_camera, (MagicMock(), True), "Guest users do not have permission to change camera status."),
        (guest_dashboard._set_camera_password, (MagicMock(),), "Only admin can change camera passwords."),
        (guest_dashboard._delete_camera_password, (MagicMock(),), "Only admin can delete camera passwords."),
    ]

    for action, args, expected_msg in actions:
        guest_dashboard.mock_messagebox.showwarning.reset_mock()
        
        action(*args)
        
        try:
            guest_dashboard.mock_messagebox.showwarning.assert_called_once()
            # We only check the second argument (the message) because the title can vary slightly
            called_args = guest_dashboard.mock_messagebox.showwarning.call_args[0]
            assert called_args[1] == expected_msg
        except AssertionError as e:
            # Provide more context on failure
            raise AssertionError(f"Action '{action.__name__}' failed assertion. Expected msg: '{expected_msg}', Got: {guest_dashboard.mock_messagebox.showwarning.call_args}") from e

def test_set_mode_admin(admin_dashboard):
    """
    UT-Dashboard-SetMode: Test mode setting logic for admin.
    测试管理员设置系统模式的逻辑。
    """
    # Test disarming
    admin_dashboard._set_mode(SafeHomeMode.DISARMED)
    admin_dashboard.system.disarm_system.assert_called_once()
    admin_dashboard.mock_messagebox.showinfo.assert_called_with("Success", "System Disarmed")

    # Test arming success
    admin_dashboard.system.arm_system.return_value = True
    admin_dashboard._set_mode(SafeHomeMode.AWAY)
    admin_dashboard.system.arm_system.assert_called_with(SafeHomeMode.AWAY)
    admin_dashboard.mock_messagebox.showinfo.assert_called_with("Success", "System Armed in AWAY mode")

    # Test arming failure
    admin_dashboard.system.arm_system.return_value = False
    admin_dashboard._set_mode(SafeHomeMode.HOME)
    admin_dashboard.system.arm_system.assert_called_with(SafeHomeMode.HOME)
    admin_dashboard.mock_messagebox.showwarning.assert_called_with("Cannot Arm", "Cannot arm system!\nSome windows/doors are open.")

def test_trigger_panic_admin(admin_dashboard):
    """
    UT-Dashboard-Panic: Test panic button logic for admin.
    测试管理员触发紧急警报的逻辑。
    """
    # User cancels panic
    admin_dashboard.mock_messagebox.askyesno.return_value = False
    admin_dashboard._trigger_panic()
    admin_dashboard.system.config.set_mode.assert_not_called()

    # User confirms panic
    admin_dashboard.mock_messagebox.askyesno.return_value = True
    admin_dashboard._trigger_panic()
    admin_dashboard.system.config.set_mode.assert_called_with(SafeHomeMode.PANIC)
    admin_dashboard.system.alarm.ring.assert_called_once()
    admin_dashboard.mock_messagebox.showwarning.assert_called_with("Panic Alarm", "🚨 PANIC ALARM ACTIVATED!")

def test_silence_alarm_admin(admin_dashboard):
    """
    UT-Dashboard-Silence: Test alarm silence logic for admin.
    测试管理员关闭警报的逻辑。
    """
    admin_dashboard._silence_alarm()
    admin_dashboard.system.alarm.stop.assert_called_once()
    admin_dashboard.mock_messagebox.showinfo.assert_called_with("Alarm", "Alarm silenced")

