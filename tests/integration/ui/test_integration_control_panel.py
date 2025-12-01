import pytest

from safehome.configuration.storage_manager import StorageManager
from safehome.core.system import System
from safehome.interface.control_panel.device_control_panel_abstract import (
    DeviceControlPanelAbstract,
)
from safehome.interface.control_panel.safehome_control_panel import SafeHomeControlPanel


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def system(tmp_path, monkeypatch):
    db_path = tmp_path / "safehome.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    sys = System(db_path=str(db_path))
    yield sys
    sys.shutdown()


def _patch_cp_display(monkeypatch, recorder: dict):
    """Patch DeviceControlPanelAbstract display methods to record messages."""
    monkeypatch.setattr(
        DeviceControlPanelAbstract, "__init__", lambda self, master=None: None
    )
    for name in [
        "set_display_short_message1",
        "set_display_short_message2",
    ]:
        monkeypatch.setattr(
            DeviceControlPanelAbstract,
            name,
            lambda self, msg, _name=name: recorder.setdefault(_name, []).append(msg),
        )
    for name in [
        "set_display_away",
        "set_display_stay",
        "set_display_not_ready",
        "set_armed_led",
        "set_powered_led",
        "set_security_zone_number",
        "_update_display_text",
    ]:
        monkeypatch.setattr(DeviceControlPanelAbstract, name, lambda *a, **k: None)


def test_it_cp_change_password_headless(monkeypatch, system):
    """IT-CP-ChangePwd (headless): change password via panel and verify login."""
    recorder = {}
    _patch_cp_display(monkeypatch, recorder)
    panel = SafeHomeControlPanel(system=system)
    for ch in "1234":
        panel._handle_key_input(ch)
    panel.button_sharp()  # login
    # Enter change password command '3'
    panel._handle_command("3")
    for ch in "8888":
        panel._handle_key_input(ch)
    panel.button_sharp()  # confirm new password
    assert system.login("admin", "8888", "CONTROL_PANEL")


def test_it_cp_invalid_command_headless(monkeypatch, system):
    """IT-CP-Invalid-Cmd (headless): invalid command shows message, state handled."""
    recorder = {}
    _patch_cp_display(monkeypatch, recorder)
    panel = SafeHomeControlPanel(system=system)
    for ch in "1234":
        panel._handle_key_input(ch)
    panel.button_sharp()  # login
    panel._handle_command("7")  # invalid
    # Expect message recorded as "Invalid Cmd"
    assert any(
        "Invalid" in msg for msg in recorder.get("set_display_short_message1", [])
    )
    # Session may remain active; ensure no exception and panel still exists
    assert panel is not None
