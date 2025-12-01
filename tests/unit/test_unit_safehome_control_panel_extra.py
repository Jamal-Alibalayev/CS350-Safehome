
# tests/unit/test_unit_safehome_control_panel_extra.py

import pytest
from unittest.mock import MagicMock, patch
from safehome.interface.control_panel.safehome_control_panel import SafeHomeControlPanel
from safehome.configuration.safehome_mode import SafeHomeMode

@pytest.fixture
def mock_system():
    """Fixture for a mocked System object."""
    system = MagicMock()
    # Mock configuration attributes that are accessed directly
    system.is_running = True
    system.config.current_mode = SafeHomeMode.DISARMED
    system.config.login_manager.is_locked.get.return_value = False
    system.config.get_current_zone.return_value = MagicMock(zone_id=1, name="Default Zone")
    system.config.next_zone.return_value = MagicMock(zone_id=2, name="Next Zone")
    return system

@pytest.fixture
def panel(mock_system):
    """Fixture for a SafeHomeControlPanel instance with a mocked system."""
    # Patch all methods called during the constructor that access UI components.
    # This includes the base class __init__ and methods called within the
    # SafeHomeControlPanel's own __init__.
    with patch('safehome.interface.control_panel.device_control_panel_abstract.DeviceControlPanelAbstract.__init__') as mock_base_init, \
         patch('safehome.interface.control_panel.safehome_control_panel.SafeHomeControlPanel._refresh_status_display') as mock_refresh, \
         patch('safehome.interface.control_panel.safehome_control_panel.SafeHomeControlPanel._reset_interaction') as mock_reset:
        
        mock_base_init.return_value = None
        panel_instance = SafeHomeControlPanel(system=mock_system)

        # Manually mock the methods from the abstract base class that are called in the tests.
        # These would normally access UI components, but here they are simple mocks.
        panel_instance.set_display_short_message1 = MagicMock()
        panel_instance.set_display_short_message2 = MagicMock()
        
        # Re-attach the mocked methods so their calls can be asserted in tests
        panel_instance._refresh_status_display = mock_refresh
        panel_instance._reset_interaction = mock_reset
        
        return panel_instance

def test_panel_change_password_flow_and_logout(panel: SafeHomeControlPanel, mock_system: MagicMock):
    """Test the full password change flow, including success and forced logout."""
    # 1. Login first
    panel.input_buffer = "1234"
    mock_system.login.return_value = True
    panel.button_sharp()
    assert panel.is_authenticated is True
    mock_system.login.assert_called_with("admin", "1234", "CONTROL_PANEL")
    panel.set_display_short_message1.assert_called_with("Login Success")

    # 2. Initiate password change
    panel.button3()
    assert panel.is_changing_password is True
    panel.set_display_short_message1.assert_called_with("CHANGE PASSWORD")
    panel.set_display_short_message2.assert_called_with("Enter New Password + #")
    
    # 3. Enter new password
    panel.input_buffer = "5678"
    mock_system.change_password.return_value = True
    
    # 4. Confirm new password
    panel.button_sharp()

    # 5. Verify outcome
    mock_system.change_password.assert_called_with("1234", "5678", "CONTROL_PANEL")
    mock_system.config.save_configuration.assert_called_once()
    panel.set_display_short_message1.assert_called_with("PASSWORD CHANGED")
    panel.set_display_short_message2.assert_called_with("Please Relogin")
    
    # 6. Check that user is logged out and state is reset
    assert panel.is_authenticated is False
    assert panel.is_changing_password is False
    assert panel.current_valid_password is None
    assert panel.input_buffer == ""

def test_panel_change_password_invalid_format(panel: SafeHomeControlPanel, mock_system: MagicMock):
    """Test that changing password to an invalid format is handled correctly."""
    # 1. Login and initiate password change
    panel.input_buffer = "1234"
    mock_system.login.return_value = True
    panel.button_sharp()
    panel.button3()

    # 2. Enter invalid new password (non-digit)
    panel.input_buffer = "abcd"
    panel.button_sharp()

    # 3. Verify that the change was rejected and system was not called
    mock_system.change_password.assert_not_called()
    panel.set_display_short_message1.assert_called_with("Invalid Format")
    panel.set_display_short_message2.assert_called_with("Digits Only")
    assert panel.input_buffer == "" # Buffer should be cleared

def test_panel_login_fail_and_system_lock(panel: SafeHomeControlPanel, mock_system: MagicMock):
    """Test that the panel displays a system lock message after too many failed logins."""
    # 1. Simulate a failed login
    panel.input_buffer = "wrong"
    mock_system.login.return_value = False
    panel.button_sharp()
    panel.set_display_short_message1.assert_called_with("Login Failed")

    # Reset mock call history before the next call
    panel.set_display_short_message1.reset_mock()

    # 2. Simulate system being locked
    mock_system.config.login_manager.is_locked.get.return_value = True
    
    # 3. Simulate another failed login
    panel.input_buffer = "wrong_again" # Must provide input again
    panel.button_sharp()
    
    # 4. Verify lock message is displayed
    panel.set_display_short_message1.assert_called_with("SYSTEM LOCKED")

def test_panel_arm_fail(panel: SafeHomeControlPanel, mock_system: MagicMock):
    """Test that the panel displays a failure message if arming is unsuccessful."""
    # 1. Login
    panel.input_buffer = "1234"
    mock_system.login.return_value = True
    panel.button_sharp()

    # 2. Attempt to arm, but system returns failure
    mock_system.arm_system.return_value = False
    panel.button1() # Arm Away

    # 3. Verify failure message
    mock_system.arm_system.assert_called_with(SafeHomeMode.AWAY)
    panel.set_display_short_message1.assert_called_with("Cannot Arm")
    panel.set_display_short_message2.assert_called_with("Windows/Doors Open")
    # User should remain authenticated to try another command
    assert panel.is_authenticated is True

def test_panel_panic_button(panel: SafeHomeControlPanel, mock_system: MagicMock):
    """Test that the panic button triggers the system's panic mode."""
    panel.button_panic()
    mock_system.config.set_mode.assert_called_once_with(SafeHomeMode.PANIC)
    mock_system.alarm.ring.assert_called_once()
    panel.set_display_short_message1.assert_called_with("PANIC ALARM!")

def test_panel_change_zone(panel: SafeHomeControlPanel, mock_system: MagicMock):
    """Test the change security zone functionality."""
    # 1. Login
    panel.input_buffer = "1234"
    mock_system.login.return_value = True
    panel.button_sharp()

    # 2. Press button to change zone
    panel.button9()

    # 3. Verify zone was changed and UI updated
    mock_system.config.next_zone.assert_called_once()
    panel.set_display_short_message1.assert_called_with("Zone Changed:")
    # Assert using the mock's actual name attribute
    panel.set_display_short_message2.assert_called_with(mock_system.config.next_zone.return_value.name)
    # User should remain authenticated
    assert panel.is_authenticated is True

def test_panel_cancel_button(panel: SafeHomeControlPanel):
    """Test that the star/cancel button resets the interaction by calling the reset method."""
    # Reset mock from the __init__ call
    panel._reset_interaction.reset_mock()
    # Enter some data into the buffer
    panel.input_buffer = "123"
    panel.button_star()
    # Assert that the reset method (which is mocked by the fixture) was called
    panel._reset_interaction.assert_called_once()
