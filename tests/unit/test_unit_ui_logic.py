import pytest

from safehome.configuration.storage_manager import StorageManager
from safehome.core.system import System
from safehome.interface.control_panel.device_control_panel_abstract import (
    DeviceControlPanelAbstract,
)
from safehome.interface.control_panel.safehome_control_panel import SafeHomeControlPanel
from safehome.interface.dashboard.main_dashboard import MainDashboard


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def system(tmp_path, monkeypatch):
    """Isolated System with temp DB for control panel logic tests."""
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    sys = System(db_path=str(tmp_path / "safehome.db"))
    yield sys
    sys.shutdown()


def _patch_control_panel_base(monkeypatch):
    """Patch DeviceControlPanelAbstract UI methods to no-op for headless testing."""
    monkeypatch.setattr(
        DeviceControlPanelAbstract, "__init__", lambda self, master=None: None
    )
    for name in [
        "set_display_short_message1",
        "set_display_short_message2",
        "set_display_away",
        "set_display_stay",
        "set_display_not_ready",
        "set_armed_led",
        "set_powered_led",
        "set_security_zone_number",
        "_update_display_text",
    ]:
        monkeypatch.setattr(
            DeviceControlPanelAbstract, name, lambda *args, **kwargs: None
        )


def test_safehome_control_panel_login_and_arm_disarm(monkeypatch, system):
    """UT-CP-LoginArm: control panel login then arm/disarm command handling."""
    _patch_control_panel_base(monkeypatch)
    panel = SafeHomeControlPanel(system=system)
    # Simulate entering password 1234 and pressing #
    for ch in "1234":
        panel._handle_key_input(ch)
    panel.button_sharp()  # confirm login
    assert panel.is_authenticated
    # Command 0 => disarm
    panel._handle_command("0")
    assert not panel.is_authenticated


def test_safehome_control_panel_change_password_flow(monkeypatch, system):
    """UT-CP-ChangePwd: enter change mode and update password via #."""
    _patch_control_panel_base(monkeypatch)
    panel = SafeHomeControlPanel(system=system)
    # Login first
    for ch in "1234":
        panel._handle_key_input(ch)
    panel.button_sharp()
    assert panel.is_authenticated
    # Enter change password mode (command 3)
    panel._handle_command("3")
    assert panel.is_changing_password
    for ch in "9999":
        panel._handle_key_input(ch)
    panel.button_sharp()  # confirm new password
    assert not panel.is_authenticated
    assert system.login("admin", "9999", "CONTROL_PANEL")


def test_main_dashboard_build_permissions():
    """UT-Dashboard-Permissions: verify admin vs guest permission sets."""
    perms_admin = MainDashboard._build_permissions(None, "admin")
    perms_guest = MainDashboard._build_permissions(None, "guest")
    assert perms_admin["control_modes"] is True
    assert perms_guest["control_modes"] is False
    assert perms_guest["camera_ptz"] is True
