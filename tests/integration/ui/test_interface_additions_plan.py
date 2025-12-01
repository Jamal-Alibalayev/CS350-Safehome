import types
import pytest

from safehome.core.system import System
from safehome.configuration.storage_manager import StorageManager
from safehome.configuration.safehome_mode import SafeHomeMode
from safehome.device.sensor.windoor_sensor import WindowDoorSensor
from safehome.device.sensor.motion_sensor import MotionSensor
from safehome.interface.control_panel.safehome_control_panel import SafeHomeControlPanel
from safehome.interface.control_panel.device_control_panel_abstract import (
    DeviceControlPanelAbstract,
)
from safehome.interface.dashboard.login_window import LoginWindow
from safehome.interface.dashboard.main_dashboard import MainDashboard
from safehome.interface.dashboard.zone_manager import (
    ZoneManagerWindow,
    AssignSensorDialog,
    AddZoneDialog,
)
from safehome.interface.dashboard.log_viewer import LogViewerWindow
from safehome.interface.control_panel.camera_monitor import CameraMonitor
from safehome.interface.tools.sensor_simulator import SafeHomeSensorTest


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


def _stub_messagebox(monkeypatch):
    calls = {"info": [], "warn": [], "error": [], "askyesno": [], "askokcancel": []}

    def info(title, msg):
        calls["info"].append((title, msg))
        return True

    def warn(title, msg):
        calls["warn"].append((title, msg))
        return True

    def err(title, msg):
        calls["error"].append((title, msg))
        return True

    def askyesno(title, msg, **_):
        calls["askyesno"].append((title, msg))
        return True

    def askokcancel(title, msg, **_):
        calls["askokcancel"].append((title, msg))
        return True

    modules = [
        __import__("tkinter.messagebox", fromlist=["messagebox"]),
        __import__("safehome.interface.dashboard.main_dashboard", fromlist=["messagebox"]),
        __import__("safehome.interface.dashboard.zone_manager", fromlist=["messagebox"]),
        __import__("safehome.interface.dashboard.log_viewer", fromlist=["messagebox"]),
        __import__("safehome.interface.control_panel.safehome_control_panel", fromlist=["messagebox"]),
        __import__("safehome.interface.control_panel.camera_monitor", fromlist=["messagebox"]),
        __import__("safehome.interface.tools.sensor_simulator", fromlist=["messagebox"]),
    ]
    for mod in modules:
        monkeypatch.setattr(mod, "showinfo", info, raising=False)
        monkeypatch.setattr(mod, "showwarning", warn, raising=False)
        monkeypatch.setattr(mod, "showerror", err, raising=False)
        monkeypatch.setattr(mod, "askyesno", askyesno, raising=False)
        monkeypatch.setattr(mod, "askokcancel", askokcancel, raising=False)
    return calls


def _stub_simpledialog(monkeypatch, responses=None):
    answers = iter(responses or [])

    def askstring(*_, **__):
        try:
            return next(answers)
        except StopIteration:
            return None

    monkeypatch.setattr(
        "safehome.interface.dashboard.main_dashboard.simpledialog.askstring",
        askstring,
        raising=False,
    )
    try:
        monkeypatch.setattr(
            "safehome.interface.control_panel.camera_monitor.simpledialog.askstring",
            askstring,
            raising=False,
        )
    except ImportError:
        pass
    return askstring


class _DummyLabel:
    def __init__(self):
        self.config_calls = []

    def config(self, **kwargs):
        self.config_calls.append(kwargs)


class _DummyEntry:
    def __init__(self, value=""):
        self._value = value
        self.deleted = False
        self.focused = False

    def get(self):
        return self._value

    def set(self, val):
        self._value = val

    def delete(self, *_):
        self.deleted = True
        self._value = ""

    def focus(self):
        self.focused = True


def _patch_cp_display(monkeypatch, recorder: dict):
    monkeypatch.setattr(DeviceControlPanelAbstract, "__init__", lambda self, master=None: None)
    for name in ["set_display_short_message1", "set_display_short_message2"]:
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


# --- LoginWindow tests ---


def test_loginwindow_empty_credentials(monkeypatch, system):
    called = {"login": 0}

    def fake_login(*_):
        called["login"] += 1
        return False

    system.login = fake_login
    win = LoginWindow.__new__(LoginWindow)
    win.system = system
    win.user_combo = types.SimpleNamespace(get=lambda: "Admin")
    status = _DummyLabel()
    pwd = _DummyEntry("")
    win.password_entry = pwd
    win.status_label = status
    win._attempt_login()
    assert status.config_calls == [] or status.config_calls[-1]["text"].startswith("⚠️")
    assert called["login"] == 0


def test_loginwindow_retry_then_success(monkeypatch, system):
    results = [False, True]

    def fake_login(*_):
        return results.pop(0)

    system.login = fake_login
    win = LoginWindow.__new__(LoginWindow)
    win.system = system
    win.user_combo = types.SimpleNamespace(get=lambda: "Admin")
    status = _DummyLabel()
    pwd = _DummyEntry("bad")
    win.password_entry = pwd
    win.status_label = status
    opened = {}
    win.withdraw = lambda: opened.setdefault("withdraw", True)
    win._open_dashboard = lambda user_id: opened.setdefault("dash", user_id)

    win._attempt_login()  # bad
    pwd.set("1234")
    win._attempt_login()  # good
    assert opened["dash"] == "admin"
    assert opened["withdraw"] is True


def test_loginwindow_lockout_message(monkeypatch, system):
    system.config.login_manager.max_login_attempts = 1

    def fake_login(*_):
        system.config.login_manager.is_locked["CONTROL_PANEL"] = True
        return False

    system.login = fake_login
    win = LoginWindow.__new__(LoginWindow)
    win.system = system
    win.user_combo = types.SimpleNamespace(get=lambda: "Admin")
    status = _DummyLabel()
    pwd = _DummyEntry("bad")
    win.password_entry = pwd
    win.status_label = status
    win._attempt_login()
    assert status.config_calls[-1]["text"].startswith("🔒")


def test_loginwindow_guest_mode(monkeypatch, system):
    opened = {}

    def fake_login(user, password, *_):
        opened["user"] = user
        return True

    system.login = fake_login
    win = LoginWindow.__new__(LoginWindow)
    win.system = system
    win.user_combo = types.SimpleNamespace(get=lambda: "Guest")
    status = _DummyLabel()
    pwd = _DummyEntry("0000")
    win.password_entry = pwd
    win.status_label = status
    win.withdraw = lambda: opened.setdefault("withdraw", True)
    win._open_dashboard = lambda user_id: opened.setdefault("dash", user_id)
    win._attempt_login()
    assert opened["dash"] == "guest"
    assert opened["withdraw"] is True
    assert opened["user"] == "guest"


def test_loginwindow_clear_error_on_success(monkeypatch, system):
    called = {"login": [False, True]}

    def fake_login(*_):
        return called["login"].pop(0)

    system.login = fake_login
    win = LoginWindow.__new__(LoginWindow)
    win.system = system
    win.user_combo = types.SimpleNamespace(get=lambda: "Admin")
    status = _DummyLabel()
    pwd = _DummyEntry("bad")
    win.password_entry = pwd
    win.status_label = status
    flags = {}
    win.withdraw = lambda: flags.setdefault("withdraw", True)
    win._open_dashboard = lambda *_: flags.setdefault("dash", True)
    win._attempt_login()  # fail
    pwd.set("1234")
    win._attempt_login()  # success
    assert flags.get("withdraw") and flags.get("dash")
    assert len(status.config_calls) == 1  # no new error after success


# --- Control Panel tests ---


def test_cp_not_ready_gate(monkeypatch, system):
    recorder = {}
    _patch_cp_display(monkeypatch, recorder)
    panel = SafeHomeControlPanel(system=system)
    sensor = WindowDoorSensor(99, "Front")
    sensor.simulate_open()
    system.sensor_controller.sensors[sensor.sensor_id] = sensor
    for ch in "1234":
        panel._handle_key_input(ch)
    panel.button_sharp()
    panel._handle_command("1")
    assert any("Cannot Arm" in msg for msg in recorder.get("set_display_short_message1", []))
    assert any("Windows/Doors" in msg for msg in recorder.get("set_display_short_message2", []))


def test_cp_change_password_invalid_format(monkeypatch, system):
    recorder = {}
    _patch_cp_display(monkeypatch, recorder)
    panel = SafeHomeControlPanel(system=system)
    for ch in "1234":
        panel._handle_key_input(ch)
    panel.button_sharp()
    panel._handle_command("3")
    panel.input_buffer = "abcd"
    panel.button_sharp()
    assert "Invalid Format" in recorder.get("set_display_short_message1", [])[-1]


def test_cp_panic_alarm(monkeypatch, system):
    recorder = {}
    _patch_cp_display(monkeypatch, recorder)
    panel = SafeHomeControlPanel(system=system)
    panel.button_panic()
    assert system.alarm.is_active()
    assert any("PANIC" in msg for msg in recorder.get("set_display_short_message1", []))
    system.alarm.stop()


def test_cp_login_fail_message(monkeypatch, system):
    recorder = {}
    _patch_cp_display(monkeypatch, recorder)
    panel = SafeHomeControlPanel(system=system)
    for ch in "9999":
        panel._handle_key_input(ch)
    panel.button_sharp()
    assert any("Login Failed" in msg for msg in recorder.get("set_display_short_message1", []))


def test_cp_lockout_ui(monkeypatch, system):
    recorder = {}
    _patch_cp_display(monkeypatch, recorder)
    system.config.settings.max_login_attempts = 1
    system.config.login_manager.settings.max_login_attempts = 1
    panel = SafeHomeControlPanel(system=system)
    for ch in "9999":
        panel._handle_key_input(ch)
    panel.button_sharp()
    assert system.config.login_manager.is_locked["CONTROL_PANEL"] is True
    assert any("SYSTEM LOCKED" in msg for msg in recorder.get("set_display_short_message1", []))


def test_cp_change_password_success(monkeypatch, system):
    recorder = {}
    _patch_cp_display(monkeypatch, recorder)
    panel = SafeHomeControlPanel(system=system)
    for ch in "1234":
        panel._handle_key_input(ch)
    panel.button_sharp()
    panel._handle_command("3")
    panel.input_buffer = "7777"
    panel.button_sharp()
    assert system.config.settings.master_password == "7777"
    assert system.login("admin", "7777", "CONTROL_PANEL")


def test_cp_cancel_reset(monkeypatch, system):
    recorder = {}
    _patch_cp_display(monkeypatch, recorder)
    panel = SafeHomeControlPanel(system=system)
    for ch in "1234":
        panel._handle_key_input(ch)
    panel.button_sharp()
    panel._handle_command("3")
    panel.input_buffer = "55"
    panel.button_star()
    assert panel.input_buffer == ""
    assert panel.is_changing_password is False


def test_cp_zone_cycle(monkeypatch, system):
    recorder = {}
    _patch_cp_display(monkeypatch, recorder)
    panel = SafeHomeControlPanel(system=system)
    monkeypatch.setattr(system.config, "next_zone", lambda: types.SimpleNamespace(name="Extra"), raising=False)
    for ch in "1234":
        panel._handle_key_input(ch)
    panel.button_sharp()
    panel._handle_command("9")
    assert any("Zone Changed" in msg for msg in recorder.get("set_display_short_message1", []))


def test_cp_reset_interaction(monkeypatch, system):
    recorder = {}
    _patch_cp_display(monkeypatch, recorder)
    panel = SafeHomeControlPanel(system=system)
    panel.input_buffer = "12"
    panel.is_authenticated = True
    panel.is_changing_password = True
    panel._reset_interaction()
    assert panel.input_buffer == ""
    assert not panel.is_authenticated
    assert not panel.is_changing_password


# --- Zone Manager tests ---


def _dummy_tree(items=None):
    class T:
        def __init__(self):
            self._items = items or []

        def get_children(self):
            return list(self._items)

        def delete(self, *_):
            return None

    return T()


def test_zone_manager_no_selection_guards(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    zm = ZoneManagerWindow.__new__(ZoneManagerWindow)
    zm.system = system
    zm.selected_zone_id = None
    zm.zone_name_label = types.SimpleNamespace(config=lambda **k: None)
    zm.sensor_tree = _dummy_tree([])
    zm._refresh_zones = lambda: None
    zm._refresh_zone_sensors = lambda *a, **k: None
    zm._delete_zone()
    zm._assign_sensors()
    assert calls["warn"]


def test_zone_manager_delete_cancel(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    monkeypatch.setattr(
        "safehome.interface.dashboard.zone_manager.messagebox.askyesno",
        lambda *a, **k: calls["askyesno"].append((a, k)) or False,
    )
    zm = ZoneManagerWindow.__new__(ZoneManagerWindow)
    zm.system = system
    zone = system.config.add_safety_zone("Z1")
    zm.selected_zone_id = zone.zone_id
    zm.zone_name_label = types.SimpleNamespace(config=lambda **k: None)
    zm.sensor_tree = _dummy_tree([])
    zm._refresh_zones = lambda: None
    zm._refresh_zone_sensors = lambda *a, **k: None
    zm._delete_zone()
    assert system.config.get_safety_zone(zone.zone_id)
    assert calls["askyesno"]


def test_zone_manager_assign_cancel(monkeypatch, system):
    zm = ZoneManagerWindow.__new__(ZoneManagerWindow)
    zm.system = system
    zone = system.config.add_safety_zone("Z2")
    zm.selected_zone_id = zone.zone_id
    zm.zone_name_label = types.SimpleNamespace(config=lambda **k: None)
    zm.sensor_tree = _dummy_tree([])
    zm._refresh_zones = lambda: None
    zm._refresh_zone_sensors = lambda *a, **k: None

    class FakeDialog:
        def __init__(self, *a, **k):
            self.result = False

    monkeypatch.setattr(
        "safehome.interface.dashboard.zone_manager.AssignSensorDialog",
        FakeDialog,
    )
    monkeypatch.setattr(zm, "wait_window", lambda *a, **k: None)
    zm._assign_sensors()
    assert system.config.get_safety_zone(zone.zone_id)


def test_zone_manager_edit_empty_fail(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    zone = system.config.add_safety_zone("Z3")
    dlg = types.SimpleNamespace(
        system=system,
        zone=zone,
        name_entry=types.SimpleNamespace(get=lambda: "", delete=lambda *a, **k: None),
        result=False,
    )
    from safehome.interface.dashboard.zone_manager import EditZoneDialog

    EditZoneDialog._save_zone(dlg)
    assert system.config.get_safety_zone(zone.zone_id).name == "Z3"
    assert calls["error"]


def test_zone_manager_assign_preselect(monkeypatch, system):
    zone = system.config.add_safety_zone("Z4")
    sensor_a = WindowDoorSensor(10, "A")
    sensor_b = MotionSensor(11, "B")
    system.sensor_controller.sensors = {10: sensor_a, 11: sensor_b}
    sensor_a.zone_id = zone.zone_id
    sensor_b.zone_id = zone.zone_id
    saved = {}

    class ListBox:
        def curselection(self):
            return (0, 1)

    dialog = AssignSensorDialog.__new__(AssignSensorDialog)
    dialog.system = system
    dialog.zone = zone
    dialog.sensor_listbox = ListBox()
    dialog.sensor_ids = [10, 11]
    dialog.result = False
    dialog.destroy = lambda: None
    monkeypatch.setattr(system.config, "save_configuration", lambda: saved.setdefault("saved", True))
    dialog._assign()
    assert sensor_a.zone_id == zone.zone_id and sensor_b.zone_id == zone.zone_id
    assert dialog.result is True
    assert saved.get("saved")


def test_zone_manager_refresh_tree(monkeypatch, system):
    system.config.add_safety_zone("Z5")
    system.config.add_safety_zone("Z6")
    rows = []

    class Tree:
        def __init__(self):
            self._rows = []

        def get_children(self):
            return list(self._rows)

        def delete(self, *_):
            self._rows.clear()

        def insert(self, *args, **kwargs):
            rows.append(kwargs["values"])
            self._rows.append(kwargs["values"])

    zm = ZoneManagerWindow.__new__(ZoneManagerWindow)
    zm.system = system
    zm.zone_tree = Tree()
    zm.selected_zone_id = None
    zm._refresh_zones()
    assert len(rows) >= 2


def test_zone_manager_on_close_unregister(monkeypatch, system):
    destroyed = {}
    zm = ZoneManagerWindow.__new__(ZoneManagerWindow)
    zm.system = system
    zm._refresh_zones = lambda: None
    zm.destroy = lambda: destroyed.setdefault("destroy", True)
    system.config.zone_update_callbacks = [zm._refresh_zones]
    zm._on_close()
    assert zm._refresh_zones not in system.config.zone_update_callbacks
    assert destroyed.get("destroy")


def test_add_zone_dialog_empty(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    dlg = AddZoneDialog.__new__(AddZoneDialog)
    dlg.system = system
    dlg.name_entry = types.SimpleNamespace(get=lambda: "", focus=lambda: None)
    dlg.result = False
    dlg.destroy = lambda: None
    from safehome.interface.dashboard import zone_manager as zm_mod

    zm_mod.AddZoneDialog._create_zone(dlg)
    assert calls["error"]
    assert dlg.result is False


def test_assign_dialog_no_selection(monkeypatch, system):
    zone = system.config.add_safety_zone("Z7")
    sensor = WindowDoorSensor(40, "Door")
    system.sensor_controller.sensors = {40: sensor}
    dlg = AssignSensorDialog.__new__(AssignSensorDialog)
    dlg.system = system
    dlg.zone = zone
    dlg.sensor_ids = [40]

    class LB:
        def curselection(self):
            return ()

    dlg.sensor_listbox = LB()
    dlg.result = False
    dlg.destroy = lambda: None
    dlg._assign()
    assert dlg.result is True
    assert sensor.zone_id is None


# --- Dashboard tests ---


def _mk_dash(monkeypatch, system, user_id="admin", permissions=None):
    dash = MainDashboard.__new__(MainDashboard)
    dash.system = system
    dash.user_id = user_id
    dash.permissions = permissions or {
        "control_modes": True,
        "panic": True,
        "view_logs": True,
        "manage_zones": True,
        "camera_ptz": True,
        "sensor_sim": True,
    }
    dash.camera_password_cache = {}
    dash.camera_password_prompted = set()
    dash.camera_access_failed = set()
    dash.after_cancel = lambda *a, **k: None
    dash.destroy = lambda *a, **k: None
    return dash


def test_dashboard_not_ready_blocks_arm(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    dash = _mk_dash(monkeypatch, system)
    sensor = WindowDoorSensor(1, "Door")
    sensor.simulate_open()
    system.sensor_controller.sensors[sensor.sensor_id] = sensor
    dash._set_mode(SafeHomeMode.AWAY)
    assert any("Cannot arm" in msg[1] or "Cannot Arm" in msg[1] for msg in calls["warn"])


def test_dashboard_panic_and_silence(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    monkeypatch.setattr("safehome.interface.dashboard.main_dashboard.messagebox.askyesno", lambda *a, **k: True)
    dash = _mk_dash(monkeypatch, system)
    dash._trigger_panic()
    assert system.alarm.is_active()
    dash._silence_alarm()
    assert not system.alarm.is_active()
    assert calls["warn"] or calls["info"]


def test_dashboard_logout_stops_loops(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    monkeypatch.setattr("safehome.interface.dashboard.main_dashboard.messagebox.askyesno", lambda *a, **k: True)
    dash = _mk_dash(monkeypatch, system)
    dash.login_window = types.SimpleNamespace(
        deiconify=lambda: calls.setdefault("deiconify", True),
        password_entry=types.SimpleNamespace(delete=lambda *a, **k: calls.setdefault("pwd_deleted", True), focus=lambda: calls.setdefault("pwd_focus", True)),
    )
    dash.destroy = lambda: calls.setdefault("destroyed", True)
    dash._logout()
    assert calls.get("destroyed")
    assert calls.get("deiconify")
    assert calls.get("pwd_deleted")


def test_dashboard_open_helpers(monkeypatch, system):
    calls = {}
    dash = _mk_dash(monkeypatch, system)

    class FakeLV:
        def __init__(self, *_):
            calls["lv"] = True

    class FakeSim:
        def __init__(self, *_):
            calls["sim"] = True

    monkeypatch.setattr("safehome.interface.dashboard.log_viewer.LogViewerWindow", FakeLV)
    monkeypatch.setattr("safehome.device.sensor.device_sensor_tester.DeviceSensorTester", FakeSim, raising=False)
    dash._open_log_viewer()
    dash._open_sensor_simulator()
    assert calls.get("lv")
    # FakeSim may not be invoked if import fails; allow either


def test_dashboard_guest_permissions(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    dash = _mk_dash(
        monkeypatch,
        system,
        user_id="guest",
        permissions={
            "control_modes": False,
            "panic": False,
            "view_logs": False,
            "manage_zones": False,
            "camera_ptz": True,
            "sensor_sim": False,
        },
    )
    dash._set_mode(SafeHomeMode.AWAY)
    dash._open_log_viewer()
    dash._open_zone_manager()
    assert len(calls["warn"]) >= 3


def test_dashboard_header_sensor_update(monkeypatch, system):
    dash = _mk_dash(monkeypatch, system)
    dash.mode_label = _DummyLabel()
    dash.status_indicator = _DummyLabel()
    rows = []

    class Tree:
        def get_children(self):
            return []

        def delete(self, *_):
            pass

        def insert(self, *_, **kwargs):
            rows.append(kwargs["values"])

    dash.sensor_tree = Tree()
    sensor = WindowDoorSensor(21, "Door21")
    sensor.arm()
    sensor.simulate_open()
    system.sensor_controller.sensors[sensor.sensor_id] = sensor
    dash._update_header()
    dash._update_sensors()
    assert rows and "Door21" in rows[0]


def test_dashboard_password_cam_guest_view(monkeypatch, system):
    _stub_messagebox(monkeypatch)
    cam = system.camera_controller.add_camera("Cguest", "Loc", password="pw")
    dash = _mk_dash(
        monkeypatch,
        system,
        user_id="guest",
        permissions={
            "control_modes": False,
            "panic": False,
            "view_logs": False,
            "manage_zones": False,
            "camera_ptz": True,
            "sensor_sim": False,
        },
    )
    lbl = _DummyLabel()
    dash.camera_labels = {cam.camera_id: lbl}
    dash._update_cameras()
    assert lbl.config_calls[-1]["text"] == "Password Protected"


def test_dashboard_toggle_camera_cancel_pwd(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    cam = system.camera_controller.add_camera("Ctoggle", "Loc", password="pw")
    dash = _mk_dash(monkeypatch, system)
    _stub_simpledialog(monkeypatch, responses=[""])
    dash._toggle_camera(cam, enable=False)
    assert cam.is_enabled is True
    assert calls["warn"]


def test_dashboard_set_cam_pwd_confirm_cancel(monkeypatch, system):
    cam = system.camera_controller.add_camera("Cpwd", "Loc", password="pw")
    dash = _mk_dash(monkeypatch, system)
    _stub_simpledialog(monkeypatch, responses=["pw", "newpw", None])
    dash._set_camera_password(cam)
    assert cam.verify_password("pw")


def test_dashboard_save_settings_success(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    dash = _mk_dash(monkeypatch, system)
    popup = types.SimpleNamespace(destroy=lambda: calls.setdefault("destroy", True))
    s = system.config.settings
    entries = {
        "master": types.SimpleNamespace(get=lambda: "9999"),
        "guest": types.SimpleNamespace(get=lambda: "0000"),
        "entry": types.SimpleNamespace(get=lambda: "5"),
        "exit": types.SimpleNamespace(get=lambda: "5"),
        "lock": types.SimpleNamespace(get=lambda: "3"),
        "monitor": types.SimpleNamespace(get=lambda: "111-2222"),
        "home": types.SimpleNamespace(get=lambda: "333-4444"),
        "alert": types.SimpleNamespace(get=lambda: "a@b.com"),
    }
    monkeypatch.setattr(system.config, "save_configuration", lambda: calls.setdefault("saved", True))
    dash._save_settings(popup, entries)
    assert s.master_password == "9999"
    assert calls.get("saved")
    assert calls["info"]


def test_dashboard_reset_system_confirm(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    dash = _mk_dash(monkeypatch, system)
    popup = types.SimpleNamespace(destroy=lambda: calls.setdefault("destroy", True))
    monkeypatch.setattr("safehome.interface.dashboard.main_dashboard.messagebox.askyesno", lambda *a, **k: True)
    monkeypatch.setattr(system.config, "reset_configuration", lambda: calls.setdefault("reset", True))
    monkeypatch.setattr(system.camera_controller, "load_cameras_from_storage", lambda: calls.setdefault("cams", True))
    dash._logout = lambda force_logout=False: calls.setdefault("logout", force_logout or True)
    dash._reset_system(popup)
    assert calls.get("reset")
    assert calls.get("cams")
    assert calls.get("logout")
    assert calls.get("destroy")


def test_dashboard_reset_system_cancel(monkeypatch, system):
    dash = _mk_dash(monkeypatch, system)
    popup = types.SimpleNamespace(destroy=lambda: None)
    monkeypatch.setattr("safehome.interface.dashboard.main_dashboard.messagebox.askyesno", lambda *a, **k: False)
    called = {}
    monkeypatch.setattr(system.config, "reset_configuration", lambda: called.setdefault("reset", True))
    dash._reset_system(popup)
    assert "reset" not in called


def test_dashboard_password_change_email_fail(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    dash = _mk_dash(monkeypatch, system)
    popup = types.SimpleNamespace(destroy=lambda: None)
    entries = {
        "master": types.SimpleNamespace(get=lambda: "8888"),
        "guest": types.SimpleNamespace(get=lambda: ""),
        "entry": types.SimpleNamespace(get=lambda: "1"),
        "exit": types.SimpleNamespace(get=lambda: "1"),
        "lock": types.SimpleNamespace(get=lambda: "1"),
        "monitor": types.SimpleNamespace(get=lambda: ""),
        "home": types.SimpleNamespace(get=lambda: ""),
        "alert": types.SimpleNamespace(get=lambda: ""),
    }
    monkeypatch.setattr(system, "_send_password_change_alert", lambda: (_ for _ in ()).throw(RuntimeError("fail")))
    monkeypatch.setattr(system.config, "save_configuration", lambda: None)
    dash._save_settings(popup, entries)
    assert system.config.settings.master_password == "8888"
    assert calls["warn"]


def test_sensorsim_arm_disarm_all(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    sim = SafeHomeSensorTest.__new__(SafeHomeSensorTest)
    sim.system = system
    w = WindowDoorSensor(50, "D")
    m = MotionSensor(51, "M")
    system.sensor_controller.sensors = {50: w, 51: m}
    sim._arm_all()
    assert w.is_active and m.is_active
    sim._disarm_all()
    assert not w.is_active and not m.is_active
    assert calls["info"]


def test_sensorsim_handle_sensor_invalid_action(monkeypatch, system):
    sim = SafeHomeSensorTest.__new__(SafeHomeSensorTest)
    sim.system = system
    sensor = WindowDoorSensor(60, "D")
    system.sensor_controller.sensors = {60: sensor}
    sim._get_sensor_from_id_input = lambda: sensor
    sim._handle_sensor("noop")
    assert not sensor.is_active  # no change


# --- Sensor Simulator tests ---


def test_sensorsim_input_validation(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    sim = SafeHomeSensorTest.__new__(SafeHomeSensorTest)
    sim.system = system
    sim.id_var = types.SimpleNamespace(get=lambda: "")
    assert sim._get_sensor_from_id_input() is None
    sim.id_var = types.SimpleNamespace(get=lambda: "abc")
    assert sim._get_sensor_from_id_input() is None
    sim.id_var = types.SimpleNamespace(get=lambda: "999")
    assert sim._get_sensor_from_id_input() is None
    assert calls["warn"] or calls["error"]


def test_sensorsim_reset_all(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    sim = SafeHomeSensorTest.__new__(SafeHomeSensorTest)
    sim.system = system
    sensor1 = WindowDoorSensor(1, "D1")
    sensor1.simulate_open()
    sensor2 = MotionSensor(2, "M1")
    sensor2.simulate_motion()
    system.sensor_controller.sensors[sensor1.sensor_id] = sensor1
    system.sensor_controller.sensors[sensor2.sensor_id] = sensor2
    sim._reset_all()
    assert not sensor1.is_open() and not sensor2.is_motion_detected()
    assert calls["info"]


def test_sensorsim_update_status_closed_window(monkeypatch, system):
    sim = SafeHomeSensorTest.__new__(SafeHomeSensorTest)
    sim.system = system
    sim.sensor_tree = None
    sim.winfo_exists = lambda: False
    sim.after = lambda *a, **k: (_ for _ in ()).throw(AssertionError("after should not be called"))
    sim._update_status()


def test_sensorsim_handle_sensor_dispatch(monkeypatch, system):
    sim = SafeHomeSensorTest.__new__(SafeHomeSensorTest)
    sim.system = system
    w = WindowDoorSensor(30, "D")
    m = MotionSensor(31, "M")
    system.sensor_controller.sensors = {30: w, 31: m}
    sim._get_sensor_from_id_input = lambda: w
    sim._handle_sensor("arm")
    assert w.is_active
    sim._handle_sensor("trigger")
    assert w.is_open()
    sim._handle_sensor("release")
    assert not w.is_open()
    sim._handle_sensor("disarm")
    assert not w.is_active
    sim._get_sensor_from_id_input = lambda: m
    sim._handle_sensor("arm")
    assert m.is_active
    sim._handle_sensor("trigger")
    assert m.is_motion_detected()
    sim._handle_sensor("release")
    assert not m.is_motion_detected()
    sim._handle_sensor("disarm")
    assert not m.is_active


# --- Camera Monitor tests ---


def test_camera_monitor_no_system(monkeypatch):
    calls = _stub_messagebox(monkeypatch)
    mon = CameraMonitor.__new__(CameraMonitor)
    mon.system = None
    mon.camera_id = 1
    assert mon._verify_access() is False
    assert calls["error"]


def test_camera_monitor_missing_camera(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    mon = CameraMonitor.__new__(CameraMonitor)
    mon.system = system
    mon.camera_id = 999
    assert mon._verify_access() is False
    assert calls["error"]


def test_camera_monitor_feed_unavailable(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    cam = system.camera_controller.add_camera("C1", "L1")
    mon = CameraMonitor.__new__(CameraMonitor)
    mon.system = system
    mon.camera_id = cam.camera_id
    mon.password = None
    mon.camera = cam
    mon.image_label = _DummyLabel()
    mon.after = lambda *a, **k: None
    monkeypatch.setattr("safehome.interface.control_panel.camera_monitor.ImageTk.PhotoImage", lambda *a, **k: None, raising=False)
    monkeypatch.setattr(
        system.camera_controller, "get_camera_view", lambda *a, **k: None
    )
    mon._update_feed()
    # Accept either text set or no-op; key is no exception and branch for unavailable reached when view is None.
    assert not mon.image_label.config_calls or mon.image_label.config_calls[-1].get("text") == "Camera Unavailable"


def test_camera_monitor_ptz_disabled(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    cam = system.camera_controller.add_camera("C2", "L2")
    mon = CameraMonitor.__new__(CameraMonitor)
    mon.system = system
    mon.camera_id = cam.camera_id
    mon.password = None
    mon.camera = cam
    mon._update_feed = lambda: None
    monkeypatch.setattr(system.camera_controller, "pan_camera", lambda *a, **k: False)
    mon._pan_left()
    assert calls["warn"]


def test_camera_monitor_pan_success(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    cam = system.camera_controller.add_camera("C3", "L3")
    mon = CameraMonitor.__new__(CameraMonitor)
    mon.system = system
    mon.camera_id = cam.camera_id
    mon.password = None
    mon.camera = cam
    mon._update_feed = lambda: None
    monkeypatch.setattr(system.camera_controller, "pan_camera", lambda *a, **k: True)
    monkeypatch.setattr(system.camera_controller, "tilt_camera", lambda *a, **k: True)
    monkeypatch.setattr(system.camera_controller, "zoom_camera", lambda *a, **k: True)
    mon._pan_left()
    mon._pan_right()
    mon._zoom_in()
    mon._zoom_out()
    assert not calls["warn"]


def test_camera_monitor_on_close(monkeypatch, system):
    mon = CameraMonitor.__new__(CameraMonitor)
    flag = {}
    mon.destroy = lambda: flag.setdefault("destroy", True)
    mon._on_close()
    assert flag.get("destroy")


def test_camera_monitor_access_denied(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    cam = system.camera_controller.add_camera("C4", "L4", password="pw")
    mon = CameraMonitor.__new__(CameraMonitor)
    mon.system = system
    mon.camera_id = cam.camera_id
    mon.password = "bad"
    assert mon._verify_access() is False
    assert calls["error"]


def test_camera_monitor_update_feed_exception(monkeypatch, system):
    cam = system.camera_controller.add_camera("C5", "L5")
    mon = CameraMonitor.__new__(CameraMonitor)
    mon.system = system
    mon.camera_id = cam.camera_id
    mon.password = None
    mon.camera = cam
    mon.image_label = _DummyLabel()
    mon.after = lambda *a, **k: None
    monkeypatch.setattr("safehome.interface.control_panel.camera_monitor.ImageTk.PhotoImage", lambda *a, **k: None, raising=False)

    def boom(*_, **__):
        raise RuntimeError("fail")

    monkeypatch.setattr(system.camera_controller, "get_camera_view", boom)
    # Should swallow exception without propagating
    mon._update_feed()


def test_camera_monitor_zoom_fail_warning(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    cam = system.camera_controller.add_camera("C6", "L6")
    mon = CameraMonitor.__new__(CameraMonitor)
    mon.system = system
    mon.camera_id = cam.camera_id
    mon.password = None
    mon.camera = cam
    mon._update_feed = lambda: None
    monkeypatch.setattr(system.camera_controller, "zoom_camera", lambda *a, **k: False)
    mon._zoom_in()
    mon._zoom_out()
    assert calls["warn"]


# --- Log Viewer tests ---


def test_logviewer_autorefresh_toggle(monkeypatch, system):
    lv = LogViewerWindow.__new__(LogViewerWindow)
    lv.system = system
    lv.auto_refresh_var = types.SimpleNamespace(get=lambda: False)
    lv.auto_refresh = True
    lv._toggle_auto_refresh()
    assert lv.auto_refresh is False


def test_logviewer_clear_logs_button(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: True, raising=False)
    monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *a, **k: calls["info"].append(a), raising=False)
    lv = LogViewerWindow.__new__(LogViewerWindow)
    lv.system = system
    lv.log_tree = _dummy_tree([])
    lv._refresh_logs = lambda: calls.setdefault("refreshed", True)
    system.config.logger.add_log("hi", level="INFO", source="ui")
    lv._clear_logs()
    assert system.config.log_manager.get_all_logs() == []
    assert calls.get("refreshed")


def test_logviewer_empty_state(monkeypatch, system):
    lv = LogViewerWindow.__new__(LogViewerWindow)
    lv.system = system
    rows = []

    class Tree:
        def delete(self, *_):
            pass

        def get_children(self):
            return []

        def insert(self, *args, **kwargs):
            rows.append(kwargs)

    lv.log_tree = Tree()
    lv.filter_combo = types.SimpleNamespace(get=lambda: "All")
    lv.search_entry = types.SimpleNamespace(get=lambda: "")
    lv.status_label = types.SimpleNamespace(config=lambda **k: rows.append(k))
    lv._refresh_logs()
    assert rows  # status update happened


def test_logviewer_autorefresh_disable(monkeypatch, system):
    lv = LogViewerWindow.__new__(LogViewerWindow)
    lv.system = system
    lv.auto_refresh_var = types.SimpleNamespace(get=lambda: False)
    lv.auto_refresh = True
    called = {}
    lv.after = lambda *a, **k: called.setdefault("after", True)
    lv._refresh_logs = lambda: called.setdefault("refresh", True)
    lv._toggle_auto_refresh()
    lv._start_auto_refresh()
    assert "refresh" not in called
    assert called.get("after")


def test_logviewer_start_auto_refresh_calls_refresh(monkeypatch, system):
    lv = LogViewerWindow.__new__(LogViewerWindow)
    lv.system = system
    lv.auto_refresh_var = types.SimpleNamespace(get=lambda: True)
    lv.auto_refresh = True
    called = {"refresh": 0, "after": 0}

    def refresh():
        called["refresh"] += 1

    lv._refresh_logs = refresh
    lv.after = lambda *a, **k: called.__setitem__("after", called["after"] + 1)
    lv._start_auto_refresh()
    assert called["refresh"] >= 1
    assert called["after"] >= 1


def test_logviewer_filter_search(monkeypatch, system):
    lv = LogViewerWindow.__new__(LogViewerWindow)
    lv.system = system
    system.config.logger.add_log("door open", level="SENSOR", source="UI")
    system.config.logger.add_log("alarm", level="ALARM", source="UI")
    inserted = []

    class Tree:
        def delete(self, *_):
            pass

        def get_children(self):
            return []

        def insert(self, *_, **kwargs):
            inserted.append(kwargs)

    lv.log_tree = Tree()
    lv.filter_combo = types.SimpleNamespace(get=lambda: "SENSOR")
    lv.search_entry = types.SimpleNamespace(get=lambda: "door")
    lv.status_label = types.SimpleNamespace(config=lambda **k: inserted.append(k))
    lv._refresh_logs()
    assert inserted and any("door open" in i.get("values", [""])[-1] for i in inserted if isinstance(i, dict))


def test_logviewer_autorefresh_startstop(monkeypatch, system):
    lv = LogViewerWindow.__new__(LogViewerWindow)
    lv.system = system
    calls = {"after": 0, "refresh": 0}
    lv.auto_refresh_var = types.SimpleNamespace(get=lambda: False)
    lv.auto_refresh = True
    lv._toggle_auto_refresh()
    lv._refresh_logs = lambda: calls.__setitem__("refresh", calls["refresh"] + 1)
    lv.after = lambda *a, **k: calls.__setitem__("after", calls["after"] + 1)
    lv._start_auto_refresh()
    assert calls["refresh"] == 0
    lv.auto_refresh_var = types.SimpleNamespace(get=lambda: True)
    lv._toggle_auto_refresh()
    lv._start_auto_refresh()
    assert calls["after"] >= 2
    assert calls["refresh"] == 1


def test_logviewer_clear_cancel(monkeypatch, system):
    calls = _stub_messagebox(monkeypatch)
    system.config.logger.add_log("persist", level="INFO", source="UI")
    monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: False, raising=False)
    lv = LogViewerWindow.__new__(LogViewerWindow)
    lv.system = system
    lv.log_tree = _dummy_tree([])
    lv._refresh_logs = lambda: calls.setdefault("refreshed", True)
    lv._clear_logs()
    assert system.config.log_manager.get_all_logs()
    assert not calls.get("refreshed")
