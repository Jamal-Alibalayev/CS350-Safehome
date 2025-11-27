"""
SafeHome Dashboard (with visible Settings popup)
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from safehome.configuration.safehome_mode import SafeHomeMode

CAM_VIEW_SIZE = (320, 200)
REFRESH_MS = 800


class MainDashboard(tk.Toplevel):
    def __init__(self, system, login_window):
        super().__init__()
        self.system = system
        self.login_window = login_window
        self.title("SafeHome Dashboard")
        self.geometry("1600x1000")
        try:
            self.state("zoomed")
        except Exception:
            pass
        self.configure(bg="#0b1220")

        self._camera_images = {}
        self._camera_passwords = {}

        self._build_ui()
        self._update_loop()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # UI ------------------------------------------------------------------
    def _build_ui(self):
        self._build_header()

        body = tk.Frame(self, bg="#0b1220")
        body.pack(fill="both", expand=True, padx=14, pady=10)

        self._build_cameras(body)

        right = tk.Frame(body, bg="#0b1220")
        right.pack(side="right", fill="y", padx=(10, 0))
        self._build_mode_mapping(right)
        self._build_sensors(right)
        self._build_zones(right)
        self._build_logs(right)

    def _build_header(self):
        header = tk.Frame(self, bg="#0f172a", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="SafeHome", font=("Segoe UI", 20, "bold"),
                 bg="#0f172a", fg="#e2e8f0").pack(anchor="w", padx=16, pady=(10, 0))
        tk.Label(header, text="Security & Surveillance", font=("Segoe UI", 11),
                 bg="#0f172a", fg="#94a3b8").pack(anchor="w", padx=16)

        status_frame = tk.Frame(header, bg="#0f172a")
        status_frame.pack(side="right", padx=16)
        self.mode_label = tk.Label(status_frame, text=f"Mode: {self.system.config.current_mode.name}",
                                   font=("Segoe UI", 11, "bold"), bg="#0f172a", fg="#38bdf8")
        self.run_label = tk.Label(status_frame, text="● RUNNING" if self.system.is_running else "○ STOPPED",
                                  font=("Segoe UI", 10, "bold"), bg="#0f172a",
                                  fg="#10b981" if self.system.is_running else "#f97316")
        self.mode_label.pack(anchor="e")
        self.run_label.pack(anchor="e")

    def _build_cameras(self, parent):
        card = tk.Frame(parent, bg="#0f172a")
        card.pack(side="left", fill="both", expand=True)

        tk.Label(card, text="Cameras", font=("Segoe UI", 14, "bold"),
                 bg="#0f172a", fg="#e5e7eb").pack(anchor="w", padx=8, pady=(0, 6))

        grid = tk.Frame(card, bg="#0f172a")
        grid.pack(fill="both", expand=True)
        grid.grid_rowconfigure(0, weight=1, uniform="camrow")
        grid.grid_rowconfigure(1, weight=1, uniform="camrow")
        grid.grid_columnconfigure(0, weight=1, uniform="camcol")
        grid.grid_columnconfigure(1, weight=1, uniform="camcol")

        cameras = list(self.system.camera_controller.cameras.values())
        for idx, cam in enumerate(cameras[:3]):
            row, col = divmod(idx, 2)
            cell = tk.Frame(grid, bg="#111827", bd=1, relief="solid")
            cell.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

            tk.Label(cell, text=f"{cam.name} • {cam.location}", font=("Segoe UI", 10, "bold"),
                     bg="#111827", fg="#e5e7eb").pack(anchor="w", padx=8, pady=4)

            img_label = tk.Label(cell, bg="#0b0f1a", width=CAM_VIEW_SIZE[0], height=CAM_VIEW_SIZE[1])
            img_label.pack(fill="both", padx=8, pady=4, expand=True)
            self._camera_images[cam.camera_id] = img_label

            controls = tk.Frame(cell, bg="#111827")
            controls.pack(fill="x", padx=8, pady=6)
            self._add_ptz_controls(controls, cam)

        # Bottom-right slot for quick actions
        qa_cell = tk.Frame(grid, bg="#0f172a")
        qa_cell.grid(row=1, column=1, padx=8, pady=8, sticky="nsew")
        qa_card = tk.Frame(qa_cell, bg="#111827", bd=1, relief="solid")
        qa_card.pack(fill="both", expand=True)
        tk.Label(qa_card, text="Quick Actions", font=("Segoe UI", 11, "bold"),
                 bg="#111827", fg="#e5e7eb").pack(anchor="w", padx=8, pady=(6, 4))
        self._build_quick_controls(qa_card, embed=True)

    def _add_ptz_controls(self, parent, cam):
        """Compact cross-style PTZ controls (↑ ↓ ← → with zoom +/- corners)."""
        grid = tk.Frame(parent, bg="#111827")
        grid.grid(row=0, column=0, sticky="nsew")

        def make_btn(txt, cmd, bg="#1e293b", fg="#e5e7eb"):
            return tk.Button(grid, text=txt, command=cmd,
                             font=("Segoe UI", 9, "bold"), width=5, height=1,
                             bg=bg, fg=fg, relief="flat", bd=1, cursor="hand2",
                             activebackground=bg, activeforeground=fg)

        # Layout similar to the reference UI
        make_btn("↑", lambda c=cam: self._tilt_camera(c, "up")).grid(row=0, column=1, padx=2, pady=2, sticky="nsew")
        make_btn("←", lambda c=cam: self._pan_camera(c, "left")).grid(row=1, column=0, padx=2, pady=2, sticky="nsew")
        make_btn("→", lambda c=cam: self._pan_camera(c, "right")).grid(row=1, column=2, padx=2, pady=2, sticky="nsew")
        make_btn("↓", lambda c=cam: self._tilt_camera(c, "down")).grid(row=2, column=1, padx=2, pady=2, sticky="nsew")
        make_btn("+", lambda c=cam: self._zoom_camera(c, "in"), bg="#16a34a", fg="#111827").grid(row=0, column=2, padx=2, pady=2, sticky="nsew")
        make_btn("-", lambda c=cam: self._zoom_camera(c, "out"), bg="#f59e0b", fg="#111827").grid(row=2, column=0, padx=2, pady=2, sticky="nsew")

        for r in range(3):
            grid.grid_rowconfigure(r, weight=1)
        for c in range(3):
            grid.grid_columnconfigure(c, weight=1)

        # Camera enable/disable/password controls
        ctrl_row = tk.Frame(parent, bg="#111827")
        ctrl_row.grid(row=1, column=0, sticky="ew", pady=(4, 0))
        small_btn = dict(font=("Segoe UI", 8, "bold"), width=6, height=1, relief="ridge", bd=1, cursor="hand2")
        tk.Button(ctrl_row, text="Enable", command=lambda c=cam: self._toggle_camera(c, True),
                  bg="#0ea5e9", fg="white", **small_btn).pack(side="left", padx=2)
        tk.Button(ctrl_row, text="Disable", command=lambda c=cam: self._toggle_camera(c, False),
                  bg="#9ca3af", fg="black", **small_btn).pack(side="left", padx=2)
        tk.Button(ctrl_row, text="Set Pwd", command=lambda c=cam: self._set_camera_password(c),
                  bg="#22c55e", fg="white", **small_btn).pack(side="left", padx=2)
        tk.Button(ctrl_row, text="Clear Pwd", command=lambda c=cam: self._clear_camera_password(c),
                  bg="#f87171", fg="white", **small_btn).pack(side="left", padx=2)
        tk.Button(ctrl_row, text="Unlock", command=lambda c=cam: self._unlock_camera(c),
                  bg="#fcd34d", fg="black", **small_btn).pack(side="left", padx=2)

    def _build_quick_controls(self, parent, embed=False):
        container = parent if embed else self._panel(parent, "Quick Actions")
        btn_cfg = dict(font=("Segoe UI", 10 if embed else 11, "bold"),
                       width=16, height=2, relief="flat", cursor="hand2")
        tk.Button(container, text="Arm Home", bg="#2563eb", fg="white",
                  command=lambda: self._set_mode(SafeHomeMode.HOME), **btn_cfg).pack(fill="x", pady=3)
        tk.Button(container, text="Arm Away", bg="#7c3aed", fg="white",
                  command=lambda: self._set_mode(SafeHomeMode.AWAY), **btn_cfg).pack(fill="x", pady=3)
        tk.Button(container, text="Disarm", bg="#dc2626", fg="white",
                  command=lambda: self._set_mode(SafeHomeMode.DISARMED), **btn_cfg).pack(fill="x", pady=3)
        tk.Button(container, text="Sensor Simulator", bg="#f59e0b", fg="black",
                  command=self._open_sensor_simulator, **btn_cfg).pack(fill="x", pady=3)
        tk.Button(container, text="Settings", bg="#0ea5e9", fg="white",
                  command=self._open_settings, **btn_cfg).pack(fill="x", pady=3)
        tk.Button(container, text="Logout", bg="#4b5563", fg="white",
                  command=self._logout, **btn_cfg).pack(fill="x", pady=3)

    def _build_sensors(self, parent):
        card = self._panel(parent, "Sensors")
        columns = ("Type", "Location", "Zone", "State")
        self.sensor_tree = ttk.Treeview(card, columns=columns, show="headings", height=6)
        for col, w in zip(columns, (70, 150, 80, 90)):
            self.sensor_tree.heading(col, text=col)
            self.sensor_tree.column(col, width=w, anchor="center")
        vsb = ttk.Scrollbar(card, orient="vertical", command=self.sensor_tree.yview)
        self.sensor_tree.configure(yscrollcommand=vsb.set)
        self.sensor_tree.pack(side="left", fill="x", expand=True)
        vsb.pack(side="right", fill="y")

    def _build_mode_mapping(self, parent):
        card = self._panel(parent, "Mode Sensor Mapping")
        frame = tk.Frame(card, bg="#111827")
        frame.pack(fill="x", padx=8, pady=4)

        modes = ["HOME", "AWAY", "OVERNIGHT", "EXTENDED"]
        self.mode_var = tk.StringVar(value="HOME")
        tk.OptionMenu(frame, self.mode_var, *modes).grid(row=0, column=0, sticky="w", pady=4)

        self.sensor_listbox = tk.Listbox(frame, selectmode="multiple", height=6, width=28,
                                         font=("Segoe UI", 10))
        self.sensor_listbox.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=4)
        tk.Button(frame, text="Save Mapping", bg="#2563eb", fg="white",
                  font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                  command=self._save_mode_mapping).grid(row=2, column=0, columnspan=2, sticky="ew", pady=4)

        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self._refresh_mode_mapping()

    def _build_zones(self, parent):
        card = self._panel(parent, "Zones")
        self.zone_list = tk.Listbox(card, height=5, font=("Segoe UI", 10))
        self.zone_list.pack(fill="both", expand=True)
        tk.Button(card, text="Manage Zones", bg="#10b981", fg="white",
                  font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                  command=self._open_zone_manager).pack(fill="x", pady=6)

    def _build_logs(self, parent):
        card = self._panel(parent, "Logs")
        tk.Button(card, text="Open Log Viewer", bg="#f97316", fg="black",
                  font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                  command=self._open_log_viewer).pack(fill="x", pady=6)
        tk.Button(card, text="Silence Alarm", bg="#ef4444", fg="white",
                  font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2",
                  command=self._silence_alarm).pack(fill="x", pady=6)

    def _panel(self, parent, title):
        frame = tk.Frame(parent, bg="#111827", bd=1, relief="solid")
        frame.pack(fill="x", pady=6)
        tk.Label(frame, text=title, font=("Segoe UI", 12, "bold"),
                 bg="#111827", fg="#e5e7eb").pack(anchor="w", padx=10, pady=6)
        return frame

    # EVENTS / ACTIONS ---------------------------------------------------
    def _update_loop(self):
        try:
            self._update_cameras()
            self._update_sensors()
            self._update_zones()
            self._refresh_mode_mapping()
            self._update_header()
        except Exception as e:
            print(f"Update error: {e}")
        self.after(REFRESH_MS, self._update_loop)

    def _update_cameras(self):
        for cam_id, label in self._camera_images.items():
            try:
                cam_obj = self.system.camera_controller.get_camera(cam_id)
                pwd = self._camera_passwords.get(cam_id)
                if cam_obj and cam_obj.has_password() and not pwd:
                    label.config(text="🔒 Locked", fg="#f97316", image="")
                    continue
                img = self.system.camera_controller.get_camera_view(cam_id, pwd)
                if img:
                    resized = img.resize(CAM_VIEW_SIZE, Image.BILINEAR)
                    photo = ImageTk.PhotoImage(resized)
                    label.config(image=photo)
                    label.image = photo
            except Exception as e:
                label.config(text=f"Error: {e}", fg="red")

    def _update_sensors(self):
        self.sensor_tree.delete(*self.sensor_tree.get_children())
        for s in self.system.sensor_controller.get_all_sensors():
            state = "🟢 Armed" if s.is_active else "⚪ Disarmed"
            zone = f"Zone {s.zone_id}" if s.zone_id else "-"
            self.sensor_tree.insert("", "end", values=(s.sensor_type, s.location, zone, state))

    def _update_zones(self):
        self.zone_list.delete(0, tk.END)
        for z in self.system.config.get_all_zones():
            status = "🟢" if z.is_armed else "⚪"
            self.zone_list.insert(tk.END, f"{status} {z.name}")

    def _refresh_mode_mapping(self):
        if not hasattr(self, "sensor_listbox"):
            return
        selected_mode = self.mode_var.get()
        self.sensor_listbox.delete(0, tk.END)
        sensors = self.system.sensor_controller.get_all_sensors()
        mapped = set(self.system.config.storage.get_sensors_for_mode(selected_mode))
        for s in sensors:
            label = f"{s.sensor_id}: {s.location} ({s.sensor_type})"
            self.sensor_listbox.insert(tk.END, label)
            if s.sensor_id in mapped:
                self.sensor_listbox.selection_set(tk.END)

    def _save_mode_mapping(self):
        try:
            mode_name = self.mode_var.get()
            selections = self.sensor_listbox.curselection()
            sensors = self.system.sensor_controller.get_all_sensors()
            sensor_ids = []
            for idx in selections:
                if 0 <= idx < len(sensors):
                    sensor_ids.append(sensors[idx].sensor_id)
            self.system.config.configure_mode_sensors(mode_name, sensor_ids)
            messagebox.showinfo("Mode Mapping", f"Saved {len(sensor_ids)} sensors for {mode_name}")
        except Exception as e:
            messagebox.showerror("Mode Mapping", f"Failed to save mapping: {e}")

    # SETTINGS POPUP ------------------------------------------------------
    def _save_settings(self, popup, entries):
        s = self.system.config.settings
        old_master = s.master_password
        try:
            s.master_password = entries["master"].get()
            s.guest_password = entries["guest"].get() or None
            s.entry_delay = int(entries["entry"].get())
            s.exit_delay = int(entries["exit"].get())
            s.system_lock_time = int(entries["lock"].get())
            s.monitoring_phone = entries["monitor"].get()
            s.homeowner_phone = entries["home"].get()
            s.alert_email = entries["alert"].get()
            self.system.config.save_configuration()
            if s.master_password != old_master:
                # Trigger email alert for admin password change
                sent = False
                try:
                    sent = self.system._send_password_change_alert()
                except Exception as e:
                    self.system.config.logger.add_log(f"Password change email failed: {e}",
                                                      level="ERROR", source="Dashboard")
                if not sent:
                    messagebox.showwarning("Settings",
                                           "Password updated, but email alert was not sent.\n"
                                           "Please check Alert Email/SMTP settings.")
            messagebox.showinfo("Settings", "Settings saved.")
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Settings", f"Failed to save settings: {e}")

    def _open_settings(self):
        popup = tk.Toplevel(self)
        popup.title("Settings")
        popup.configure(bg="#0f172a")
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()
        width, height = 500, 520
        try:
            # center relative to dashboard
            self.update_idletasks()
            x = self.winfo_rootx() + (self.winfo_width() // 2) - (width // 2)
            y = self.winfo_rooty() + (self.winfo_height() // 2) - (height // 2)
            popup.geometry(f"{width}x{height}+{x}+{y}")
        except Exception:
            popup.geometry(f"{width}x{height}")
        popup.lift()

        container = tk.Frame(popup, bg="#0f172a", padx=16, pady=12)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Settings", font=("Segoe UI", 15, "bold"),
                 bg="#0f172a", fg="#e5e7eb").grid(row=0, column=0, columnspan=2,
                                                 sticky="w", pady=(0, 12))

        entries = {}

        def add_row(row, label, key, show=None, default=""):
            tk.Label(container, text=label, font=("Segoe UI", 10),
                     bg="#0f172a", fg="#cbd5e1").grid(row=row, column=0, sticky="w", pady=6, padx=(0, 10))
            ent = tk.Entry(container, font=("Segoe UI", 10), show=show, width=30)
            ent.grid(row=row, column=1, sticky="ew", pady=6)
            ent.insert(0, "" if default is None else str(default))
            entries[key] = ent

        add_row(1, "Master Password", "master", show="*", default=self.system.config.settings.master_password)
        add_row(2, "Guest Password", "guest", show="*", default=self.system.config.settings.guest_password or "")
        add_row(3, "Entry Delay (s)", "entry", default=str(self.system.config.settings.entry_delay))
        add_row(4, "Exit Delay (s)", "exit", default=str(self.system.config.settings.exit_delay))
        add_row(5, "Lock Time (s)", "lock", default=str(self.system.config.settings.system_lock_time))
        add_row(6, "Monitor Phone", "monitor", default=self.system.config.settings.monitoring_phone)
        add_row(7, "Home Phone", "home", default=self.system.config.settings.homeowner_phone)
        add_row(8, "Alert Email", "alert", default=self.system.config.settings.alert_email)

        # button row inside the same grid to guarantee visibility
        btn_row = tk.Frame(container, bg="#0f172a")
        btn_row.grid(row=9, column=0, columnspan=2, sticky="ew", pady=(14, 6))
        tk.Button(btn_row, text="Save", bg="#22c55e", fg="white",
                  font=("Segoe UI", 11, "bold"), relief="flat", cursor="hand2",
                  command=lambda: self._save_settings(popup, entries)).pack(side="left", padx=6, ipadx=14, ipady=6)
        tk.Button(btn_row, text="Close", bg="#4b5563", fg="white",
                  font=("Segoe UI", 11, "bold"), relief="flat", cursor="hand2",
                  command=popup.destroy).pack(side="right", padx=6, ipadx=14, ipady=6)

        container.grid_columnconfigure(1, weight=1)

    # CAMERA ACCESS ------------------------------------------------------
    def _set_mode(self, mode):
        if mode == SafeHomeMode.DISARMED:
            self.system.disarm_system()
            messagebox.showinfo("Success", "System disarmed")
        else:
            ok = self.system.arm_system(mode)
            if ok:
                messagebox.showinfo("Success", f"Armed in {mode.name}")
            else:
                messagebox.showwarning("Cannot arm", "Check windows/doors (open)")

    def _pan_camera(self, cam, direction):
        if not self._ensure_camera_access(cam):
            return
        self.system.camera_controller.pan_camera(cam.camera_id, direction,
                                                 self._camera_passwords.get(cam.camera_id))

    def _tilt_camera(self, cam, direction):
        if not self._ensure_camera_access(cam):
            return
        self.system.camera_controller.tilt_camera(cam.camera_id, direction,
                                                  self._camera_passwords.get(cam.camera_id))

    def _zoom_camera(self, cam, direction):
        if not self._ensure_camera_access(cam):
            return
        self.system.camera_controller.zoom_camera(cam.camera_id, direction,
                                                  self._camera_passwords.get(cam.camera_id))

    def _toggle_camera(self, cam, enable: bool):
        if enable:
            self.system.camera_controller.enable_camera(cam.camera_id)
        else:
            self.system.camera_controller.disable_camera(cam.camera_id)

    def _set_camera_password(self, cam):
        pwd = simpledialog.askstring("Set Camera Password", "Enter new password:", show="*")
        if pwd is None:
            return
        self.system.camera_controller.set_camera_password(cam.camera_id, pwd)
        self._camera_passwords[cam.camera_id] = pwd

    def _clear_camera_password(self, cam):
        self.system.camera_controller.set_camera_password(cam.camera_id, None)
        self._camera_passwords.pop(cam.camera_id, None)

    def _unlock_camera(self, cam):
        if not cam.has_password():
            messagebox.showinfo("Camera", "Camera has no password.")
            return
        pwd = simpledialog.askstring("Camera Password", f"Enter password for {cam.name}:", show="*")
        if pwd:
            self._camera_passwords[cam.camera_id] = pwd

    def _ensure_camera_access(self, cam):
        if cam.has_password() and cam.camera_id not in self._camera_passwords:
            pwd = simpledialog.askstring("Camera Password", f"Enter password for {cam.name}:", show="*")
            if not pwd:
                return False
            self._camera_passwords[cam.camera_id] = pwd
        return True

    # OTHER WINDOWS ------------------------------------------------------
    def _open_zone_manager(self):
        from .zone_manager import ZoneManagerWindow
        ZoneManagerWindow(self.system, self)

    def _open_log_viewer(self):
        from .log_viewer import LogViewerWindow
        LogViewerWindow(self.system, self)

    def _open_sensor_simulator(self):
        try:
            from safehome.device.sensor.device_sensor_tester import DeviceSensorTester
            DeviceSensorTester.showSensorTester()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open simulator: {e}")

    def _silence_alarm(self):
        self.system.alarm.stop()
        messagebox.showinfo("Alarm", "Alarm silenced")

    def _logout(self):
        if messagebox.askyesno("Logout", "Return to login screen?"):
            self.destroy()
            self.login_window.deiconify()
            self.login_window.password_entry.delete(0, tk.END)
            self.login_window.password_entry.focus()

    def _on_close(self):
        if messagebox.askokcancel("Quit", "Shutdown SafeHome?"):
            self.system.shutdown()
            self.login_window.destroy()
            self.destroy()
