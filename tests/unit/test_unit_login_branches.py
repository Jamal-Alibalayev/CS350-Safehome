import time
import pytest

from safehome.configuration.login_manager import LoginManager
from safehome.configuration.system_settings import SystemSettings


def test_lock_interface_sets_timer_and_unlocks():
    """Cover _lock_interface timer creation and unlock after delay."""
    settings = SystemSettings(max_login_attempts=1, system_lock_time=0.05)
    lm = LoginManager(settings)
    assert not lm.validate_credentials("admin", "bad", "CONTROL_PANEL")
    # Should be locked and timer started
    assert lm.is_interface_locked("CONTROL_PANEL")
    time.sleep(0.06)
    lm.unlock_system("CONTROL_PANEL")
    assert not lm.is_interface_locked("CONTROL_PANEL")
