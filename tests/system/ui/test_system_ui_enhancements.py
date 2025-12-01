import pytest
from PIL import Image

from safehome.core.system import System
from safehome.configuration.storage_manager import StorageManager
from safehome.configuration.safehome_mode import SafeHomeMode
from safehome.interface.dashboard import main_dashboard as dashboard_module
from safehome.interface.dashboard.main_dashboard import MainDashboard
from safehome.device.sensor import device_sensor_tester as tester_module


@pytest.fixture(autouse=True)
def headless_env(monkeypatch):
    monkeypatch.setenv("SAFEHOME_HEADLESS", "1")


@pytest.fixture
def system(tmp_path, monkeypatch):
    db_path = tmp_path / "ui_enhance.db"
    monkeypatch.setattr(StorageManager, "CONFIG_FILE", str(tmp_path / "ui_enhance.json"))
    sys = System(db_path=str(db_path))
    yield sys
    sys.shutdown()


def _make_dashboard_stub(system, user_id):
    dash = MainDashboard.__new__(MainDashboard)
    dash.system = system
    dash.user_id = user_id
    dash.permissions = MainDashboard._build_permissions(dash, user_id)
    dash.camera_password_cache = {}
    dash.camera_password_prompted = set()
    dash.camera_access_failed = set()
    dash.camera_labels = {}
    return dash


class _DummyLabel:
    def __init__(self):
        self.history = []
        self.image = None

    def config(self, **kwargs):
        self.history.append(kwargs)
        if "image" in kwargs:
            self.image = kwargs["image"]


def test_st_camera_password_dashboard_flow(system):
    """ST-Camera-Password-Management: set/change/delete flow matches storage and access gating."""
    cc = system.camera_controller
    cam = cc.add_camera("Garage", "Garage Entry")

    # Set initial password
    assert cc.set_camera_password(cam.camera_id, new_password="firstPwd", confirm_password="firstPwd")
    assert cc.get_camera_view(cam.camera_id) is None
    assert cc.get_camera_view(cam.camera_id, password="firstPwd") is not None

    # Change password (old password required)
    assert cc.set_camera_password(
        cam.camera_id,
        new_password="secondPwd",
        old_password="firstPwd",
        confirm_password="secondPwd",
    )
    assert cc.get_camera_view(cam.camera_id, password="firstPwd") is None
    assert cc.get_camera_view(cam.camera_id, password="secondPwd") is not None

    # Delete password and ensure persistence cleared
    assert cc.delete_camera_password(cam.camera_id, old_password="secondPwd")
    assert cc.get_camera_view(cam.camera_id) is not None

    rows = system.config.db_manager.get_cameras()
    stored = [row for row in rows if row["camera_id"] == cam.camera_id][0]
    assert stored["camera_password"] in (None, "")


def test_st_dashboard_quick_actions_permissions(monkeypatch, system):
    """ST-Dashboard-Quick-Actions: guest blocked, admin triggers panic/silence/simulator."""
    warnings = []
    infos = []
    ask_calls = []

    monkeypatch.setattr(
        dashboard_module.messagebox,
        "showwarning",
        lambda *args, **kwargs: warnings.append(args[0]),
    )
    monkeypatch.setattr(
        dashboard_module.messagebox,
        "showinfo",
        lambda *args, **kwargs: infos.append(args[0]),
    )
    monkeypatch.setattr(
        dashboard_module.messagebox,
        "askyesno",
        lambda *args, **kwargs: ask_calls.append(args[0]) or True,
    )

    sim_calls = []
    monkeypatch.setattr(
        tester_module.DeviceSensorTester,
        "showSensorTester",
        lambda sys_obj: sim_calls.append(sys_obj),
    )

    guest_dash = _make_dashboard_stub(system, "guest")
    guest_dash._trigger_panic()
    guest_dash._silence_alarm()
    guest_dash._open_sensor_simulator()
    assert not system.alarm.is_active()
    assert len(sim_calls) == 0
    assert warnings  # guest received warnings
    assert not ask_calls  # guest never asked to confirm panic

    admin_dash = _make_dashboard_stub(system, "admin")
    system.turn_on()
    admin_dash._trigger_panic()
    assert system.config.current_mode == SafeHomeMode.PANIC
    assert system.alarm.is_active()

    admin_dash._silence_alarm()
    assert not system.alarm.is_active()

    admin_dash._open_sensor_simulator()
    assert sim_calls[-1] is system

    system.turn_off()


def test_st_zone_list_refresh_callbacks(system):
    """ST-Zone-List-Refresh: zone callback invoked on add/update/delete events."""
    zone_snapshots = []

    def capture():
        zone_snapshots.append([z.name for z in system.config.get_all_zones()])

    system.config.register_zone_update_callback(capture)

    new_zone = system.config.add_safety_zone("Temp Zone")
    assert any("Temp Zone" in names for names in zone_snapshots)

    system.config.update_safety_zone(new_zone.zone_id, zone_name="Renamed Zone", is_armed=True)
    assert any("Renamed Zone" in names for names in zone_snapshots)

    system.config.delete_safety_zone(new_zone.zone_id)
    assert "Temp Zone" not in zone_snapshots[-1]
    assert "Renamed Zone" not in zone_snapshots[-1]


def test_st_camera_password_cache_and_guest_labels(monkeypatch, system):
    """ST-Camera-Password-Cache: admin cache reused, failure clears cache, guests see protected label."""
    cam = system.camera_controller.add_camera("Deck", "Back Deck", password="1234")

    sample_img = Image.new("RGB", (20, 20), color="blue")
    call_log = []

    def fake_get_view(cam_id, password=None):
        call_log.append(password)
        camera = system.camera_controller.get_camera(cam_id)
        if camera.has_password() and not camera.verify_password(password):
            return None
        return sample_img

    monkeypatch.setattr(system.camera_controller, "get_camera_view", fake_get_view)
    monkeypatch.setattr(dashboard_module.ImageTk, "PhotoImage", lambda img: img)

    # Admin flow
    admin_dash = _make_dashboard_stub(system, "admin")
    label = _DummyLabel()
    admin_dash.camera_labels = {cam.camera_id: label}
    admin_dash.camera_password_cache[cam.camera_id] = "1234"

    admin_dash._update_cameras()
    assert call_log[-1] == "1234"
    assert label.image is not None

    # Password changes without cache update -> should show access denied and clear cache
    assert system.camera_controller.set_camera_password(
        cam.camera_id,
        new_password="5678",
        old_password="1234",
        confirm_password="5678",
    )
    admin_dash._update_cameras()
    assert admin_dash.camera_password_cache.get(cam.camera_id) is None
    assert label.history[-1]["text"] == "Access Denied"

    # Provide new password and ensure cache used again
    admin_dash.camera_password_cache[cam.camera_id] = "5678"
    admin_dash._update_cameras()
    assert call_log[-1] == "5678"

    # Guest sees password-protected label without prompt
    guest_dash = _make_dashboard_stub(system, "guest")
    guest_label = _DummyLabel()
    guest_dash.camera_labels = {cam.camera_id: guest_label}
    guest_dash._update_cameras()
    assert guest_label.history[-1]["text"] == "Password Protected"


def test_st_dashboard_mode_permissions(monkeypatch, system):
    """ST-Dashboard-Mode-Permissions: guests blocked from mode changes, admins can arm/disarm."""
    warnings = []
    infos = []

    monkeypatch.setattr(
        dashboard_module.messagebox,
        "showwarning",
        lambda title, message: warnings.append(message),
    )
    monkeypatch.setattr(
        dashboard_module.messagebox,
        "showinfo",
        lambda title, message: infos.append(message),
    )

    guest_dash = _make_dashboard_stub(system, "guest")
    guest_dash.permissions["control_modes"] = False
    guest_dash._set_mode(SafeHomeMode.AWAY)
    assert warnings and "Guest account cannot change system mode" in warnings[-1]
    assert system.config.current_mode == SafeHomeMode.DISARMED

    admin_dash = _make_dashboard_stub(system, "admin")
    admin_dash.permissions["control_modes"] = True
    admin_dash._set_mode(SafeHomeMode.AWAY)
    assert system.config.current_mode == SafeHomeMode.AWAY
    assert infos and "System Armed" in infos[-1]

    admin_dash._set_mode(SafeHomeMode.DISARMED)
    assert system.config.current_mode == SafeHomeMode.DISARMED


def test_st_dashboard_toggle_camera_permissions(monkeypatch, system):
    """ST-Dashboard-Camera-Toggle: guest denied, admin can disable/enable with password prompt."""
    warnings = []
    monkeypatch.setattr(
        dashboard_module.messagebox,
        "showwarning",
        lambda title, message: warnings.append(message),
    )
    monkeypatch.setattr(
        dashboard_module.messagebox,
        "showinfo",
        lambda title, message: warnings.append(message),
    )

    responses = {"count": 0}

    def fake_askstring(*args, **kwargs):
        responses["count"] += 1
        return "abcd"

    monkeypatch.setattr(dashboard_module.simpledialog, "askstring", fake_askstring)

    cam = system.camera_controller.add_camera("Porch", "Front Porch")
    system.camera_controller.set_camera_password(
        cam.camera_id, new_password="abcd", confirm_password="abcd"
    )

    guest_dash = _make_dashboard_stub(system, "guest")
    guest_dash._toggle_camera(cam, False)
    assert "Guest users do not have permission" in warnings[-1]
    assert cam.is_enabled

    admin_dash = _make_dashboard_stub(system, "admin")
    admin_dash._toggle_camera(cam, False)
    assert not cam.is_enabled
    assert responses["count"] == 1  # password prompt used

    admin_dash._toggle_camera(cam, True)
    assert cam.is_enabled
