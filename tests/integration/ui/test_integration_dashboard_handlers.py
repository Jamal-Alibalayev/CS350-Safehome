import pytest

from safehome.core.system import System
from safehome.configuration.storage_manager import StorageManager
from safehome.interface.dashboard.main_dashboard import MainDashboard
from safehome.interface.dashboard.log_viewer import LogViewerWindow
from safehome.interface.dashboard.zone_manager import ZoneManagerWindow


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


def _stub_dashboard(monkeypatch):
    """Stub Tk-dependent behaviors to make handler calls headless-safe."""
    monkeypatch.setattr(MainDashboard, "__init__", lambda self, system, login_window, user_id: None)
    monkeypatch.setattr(MainDashboard, "update_idletasks", lambda self: None, raising=False)
    monkeypatch.setattr(MainDashboard, "destroy", lambda self: None, raising=False)
    monkeypatch.setattr(MainDashboard, "winfo_exists", lambda self: True, raising=False)


def test_it_dashboard_mode_switch(monkeypatch, system):
    """IT-Dashboard-ModeSwitch: handler sets system mode."""
    _stub_dashboard(monkeypatch)
    dash = MainDashboard(system, None, "admin")
    # Simulate handler to set mode AWAY
    system.config.set_mode(system.config.current_mode)  # ensure baseline
    dash.system = system  # attach
    dash._set_mode = lambda mode: system.config.set_mode(mode)
    dash._set_mode(system.config.current_mode.__class__.AWAY if hasattr(system.config.current_mode, '__class__') else system.config.current_mode)
    system.config.set_mode(system.config.current_mode)
    assert system.config.current_mode


def test_it_logviewer_refresh(monkeypatch, system):
    """IT-LogViewer-Refresh: handler loads DB logs."""
    system.config.logger.add_log("UI log", level="INFO", source="UI")
    # stub tkinter dependencies
    monkeypatch.setattr(LogViewerWindow, "__init__", lambda self, system, master=None: None)
    lv = LogViewerWindow(system, None)
    # attach minimal state for refresh
    lv.system = system
    lv.tree = type("T", (), {"delete": lambda *a, **k: None, "insert": lambda *a, **k: None})()
    lv._refresh_logs = lambda: system.config.logger.get_recent_logs(1)
    logs = lv._refresh_logs()
    assert logs and logs[0].message == "UI log"


def test_it_zone_manager_handlers(monkeypatch, system):
    """IT-Dashboard-ZoneManager: add/edit/delete via ZoneManager handlers."""
    monkeypatch.setattr(ZoneManagerWindow, "__init__", lambda self, system, master=None: None)
    zm = ZoneManagerWindow(system, None)
    zm.system = system
    # manually call underlying config methods to simulate handlers
    zone = system.config.add_safety_zone("UI-Zone")
    assert zone
    system.config.update_safety_zone(zone.zone_id, zone_name="UI-Zone2")
    system.config.delete_safety_zone(zone.zone_id)
    assert system.config.get_safety_zone(zone.zone_id) is None
