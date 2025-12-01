import time
import pytest

from safehome.core.system import System
from safehome.configuration.storage_manager import StorageManager


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    """Avoid GUI popups during system-level flows."""
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def system(tmp_path, monkeypatch):
    db_path = tmp_path / "auth.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "auth.json"))
    sys = System(db_path=str(db_path))
    # Shorten lock for tests
    sys.config.settings.system_lock_time = 0.1
    sys.config.settings.max_login_attempts = 2
    yield sys
    sys.shutdown()


def test_st_login_web_success(system):
    """
    ST-Login-Web-Su: web login with two-level password succeeds.
    """
    creds = f"{system.config.settings.web_password_1}:{system.config.settings.web_password_2}"
    assert system.login("admin", creds, interface_type="WEB")


def test_st_login_cp_lockout_and_recover(system):
    """
    ST-Login-CP-Lock: wrong PIN triggers lockout; unlocks after timeout; correct PIN then succeeds.
    """
    assert not system.login("admin", "0000", "CONTROL_PANEL")
    assert not system.login("admin", "0000", "CONTROL_PANEL")
    assert system.config.login_manager.is_interface_locked("CONTROL_PANEL")

    time.sleep(0.15)
    assert system.login("admin", system.config.settings.master_password, "CONTROL_PANEL")
    assert not system.config.login_manager.is_interface_locked("CONTROL_PANEL")


def test_st_password_change_alert(system, monkeypatch):
    """
    ST-Pwd-Change-Alert: password changes, logs, and triggers alert hook.
    """
    called = {}

    def fake_alert():
        called["sent"] = True
        return True

    monkeypatch.setattr(system.config, "send_email_alert", lambda *args, **kwargs: fake_alert())
    assert system.change_password("1234", "4321", interface_type="CONTROL_PANEL")
    assert called.get("sent")
    # new password works, old fails
    assert not system.login("admin", "1234", "CONTROL_PANEL")
    assert system.login("admin", "4321", "CONTROL_PANEL")


def test_st_session_logging(system):
    """
    ST-Session-Logging: login attempts recorded in login_sessions.
    """
    # one success, one failure
    system.login("admin", system.config.settings.master_password, "CONTROL_PANEL")
    system.login("admin", "bad", "CONTROL_PANEL")

    rows = system.config.db_manager.execute_query(
        "SELECT username, login_successful FROM login_sessions", fetch_all=True
    )
    summary = [(row["username"], row["login_successful"]) for row in rows]
    assert ("admin", 1) in summary
    assert ("admin", 0) in summary


def test_st_guest_login_permissions_logic(system):
    """
    ST-Guest-Login-Perm: guest login works; restricted action (change password) blocked.
    """
    system.config.settings.guest_password = "0000"
    assert system.login("guest", "0000", "CONTROL_PANEL")
    # guest cannot change master password
    assert not system.change_password("0000", "2222", interface_type="CONTROL_PANEL")
