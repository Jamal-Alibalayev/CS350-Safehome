import pytest

from safehome.core.system import System
from safehome.configuration.storage_manager import StorageManager
from safehome.configuration.safehome_mode import SafeHomeMode


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def system(tmp_path, monkeypatch):
    db_path = tmp_path / "config.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "config.json"))
    sys = System(db_path=str(db_path))
    yield sys
    sys.shutdown()


def test_st_init_schema_defaults(system):
    """
    ST-Init-Schema-Defaults: defaults seeded on fresh DB.
    """
    modes = system.config.modes
    assert "HOME" in modes and "AWAY" in modes
    assert system.config.settings.master_password == "1234"


def test_st_factory_reset(system):
    """
    ST-Factory-Reset: reset clears custom zones and restores defaults.
    """
    cm = system.config
    zone = cm.add_safety_zone("CustomZone")
    assert zone.zone_id
    cm.settings.master_password = "9999"
    cm.reset_configuration()

    zones = cm.get_all_safety_zones()
    assert any(z.name == "Living Room" for z in zones)
    assert any(z.name == "Bedroom" for z in zones)
    assert not any(z.name == "CustomZone" for z in zones)
    assert cm.settings.master_password == "1234"


def test_st_settings_persist_entry_delay(system):
    """
    ST-Settings-UI-Persist (headless): settings saved and loaded after restart.
    """
    cm = system.config
    cm.settings.entry_delay = 12
    cm.settings.exit_delay = 34
    cm.save_configuration()
    system.shutdown()

    # Restart
    sys2 = System(db_path=cm.db_manager.db_path)
    assert sys2.config.settings.entry_delay == 12
    assert sys2.config.settings.exit_delay == 34
    sys2.shutdown()


def test_st_email_alert_failover(monkeypatch, tmp_path):
    """
    ST-Email-Alert-Failover: failure to send is handled and returns False.
    """
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")
    sys = System(db_path=str(tmp_path / "email.db"))

    class FailingSMTP:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("smtp down")

    monkeypatch.setattr("smtplib.SMTP", FailingSMTP)
    sys.config.settings.alert_email = "user@example.com"
    sent = sys.config.send_email_alert("subject", "body")
    assert sent is False
    sys.shutdown()

def test_st_db_rollback_recover(system):
    """
    ST-DB-Rollback-Recover: uncommitted insert rolled back leaves no residue.
    """
    db = system.config.db_manager
    db.connect()
    db.connection.execute("BEGIN")
    db.execute_query(
        "INSERT INTO event_logs (event_type, event_message, source) VALUES (?, ?, ?)",
        ("TEST", "rollback-check", "Test"),
    )
    db.rollback()
    rows = db.get_event_logs(event_type="TEST", limit=5)
    assert not any(row["event_message"] == "rollback-check" for row in rows)

def test_st_backup_fallback_json(tmp_path, monkeypatch):
    """
    ST-Backup-Fallback: when no DB, settings persist via JSON.
    """
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "fallback.json"))
    sm = StorageManager(db_manager=None)
    from safehome.configuration.system_settings import SystemSettings

    settings = SystemSettings()
    settings.entry_delay = 42
    sm.save_settings(settings)

    loaded = sm.load_settings_from_json()
    assert loaded.get("entry_delay") == 42


def test_st_mode_mapping_edit_and_apply(system):
    """
    ST-Mode-Mapping-UI: edit mapping and ensure it affects arming.
    """
    sc = system.sensor_controller
    door = sc.add_sensor("WINDOOR", "Entry")
    system.config.storage.save_mode_sensor_mapping("HOME", [])
    system.config.configure_mode_sensors("HOME", [door.sensor_id])
    system.turn_on()
    assert system.arm_system(SafeHomeMode.HOME)
    assert door.is_active
    system.disarm_system()
