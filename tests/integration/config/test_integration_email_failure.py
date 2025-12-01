import pytest

from safehome.configuration.storage_manager import StorageManager
from safehome.core.system import System


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


def test_it_email_alert_failure(monkeypatch, system):
    """IT-Email-Alert-Failure: SMTP error returns False and logs error."""
    cfg = system.config
    cfg.settings.alert_email = "to@test"

    class FailingSMTP:
        def __init__(self, host, port, timeout):
            raise RuntimeError("smtp fail")

    monkeypatch.setattr("smtplib.SMTP", FailingSMTP)
    assert cfg.send_email_alert("subj", "body") is False
    logs = cfg.logger.get_recent_logs(1)
    assert any("Email alert failed" in log.message for log in logs)
