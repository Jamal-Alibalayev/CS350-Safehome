import pytest

from safehome.configuration.configuration_manager import ConfigurationManager
from safehome.configuration.storage_manager import StorageManager


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def config_mgr(tmp_path, monkeypatch):
    db_path = tmp_path / "safehome.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    cm = ConfigurationManager(db_path=str(db_path))
    yield cm
    cm.shutdown()


def test_notify_zone_update_handles_exception(config_mgr, capsys):
    """Cover _notify_zone_update branch where callback raises."""
    def bad_cb():
        raise RuntimeError("boom")
    config_mgr.register_zone_update_callback(bad_cb)
    config_mgr._notify_zone_update()
    captured = capsys.readouterr()
    assert "Error in zone update callback" in captured.out


def test_reset_configuration_clear_camera_passwords_error(monkeypatch, config_mgr, capsys):
    """Force clear_camera_passwords error path in reset_configuration."""
    def raise_err():
        raise RuntimeError("fail")
    monkeypatch.setattr(config_mgr.storage, "clear_camera_passwords", raise_err)
    config_mgr.reset_configuration()
    logs = config_mgr.logger.get_recent_logs(3)
    assert any("Failed to clear camera passwords" in log.message for log in logs)
