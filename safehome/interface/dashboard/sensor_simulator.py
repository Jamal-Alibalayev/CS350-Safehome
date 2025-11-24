"""
SafeHome Sensor Simulator GUI
Placed under interface/dashboard for better UI organization.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from PIL import Image, ImageTk
from safehome.device.sensor.device_sensor_tester import DeviceSensorTester


class SafeHomeSensorTest(tk.Toplevel):
    """
    Sensor simulator UI (floor plan + controls).
    """

    def __init__(self, master=None):
        super().__init__(master)
        self.title("SafeHome - Sensor Simulator")
        self.geometry("1200x700")
        self.resizable(True, True)

        # Track closure to allow reopening
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # 변수 초기화
        self.sensor_widgets = {}

        # UI 구성
        self._create_ui()

        # 센서 ID 범위 업데이트
        self._update_id_ranges()

        # 상태 업데이트 시작
        self._update_status()

    # === UI 구성 ===
    def _create_ui(self):
        header = tk.Frame(self, bg="#2c3e50", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🧪 Sensor Simulator",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(side="left", padx=20, pady=15)

        tk.Label(
            header,
            text="Test sensors based on fixed floor plan",
            font=("Arial", 11),
            bg="#2c3e50",
            fg="#bdc3c7"
        ).pack(side="left")

        main_container = tk.Frame(self, bg="#ecf0f1")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)

        left_panel = tk.Frame(main_container, bg="#ecf0f1")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self._create_floorplan_section(left_panel)
        self._create_sensor_list(left_panel)

        right_panel = tk.Frame(main_container, bg="#ecf0f1", width=400)
        right_panel.pack(side="right", fill="both", padx=(10, 0))
        right_panel.pack_propagate(False)

        self._create_control_panels(right_panel)

    def _create_floorplan_section(self, parent):
        floorplan_frame = tk.LabelFrame(
            parent,
            text="📐 Floor Plan",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        floorplan_frame.pack(fill="x", pady=(0, 10))

        try:
            base_dir = Path(__file__).resolve().parents[3]
            img_path = base_dir / "assets" / "images" / "floorplan.png"
            img = Image.open(img_path)
            img = img.resize((600, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            img_label = tk.Label(floorplan_frame, image=photo, bg="white")
            img_label.image = photo  # Keep reference
            img_label.pack(padx=10, pady=10)
        except Exception as e:
            tk.Label(
                floorplan_frame,
                text=f"Floor plan not available\n{str(e)}",
                font=("Arial", 10),
                bg="white",
                fg="#95a5a6"
            ).pack(pady=20)

        legend_frame = tk.Frame(floorplan_frame, bg="white")
        legend_frame.pack(fill="x", padx=10, pady=(0, 10))

        legend_items = [
            ("🔴", "Red dots = Windows (S₁-S₆)"),
            ("🔵", "Blue dots = Doors (D₁-D₂)"),
            ("📹", "Cameras (C₁-C₃)"),
            ("👁️", "Motion Detectors (M₁-M₂)")
        ]

        for emoji, text in legend_items:
            item_frame = tk.Frame(legend_frame, bg="white")
            item_frame.pack(side="left", padx=10)
            tk.Label(item_frame, text=emoji, font=("Arial", 12), bg="white").pack(side="left")
            tk.Label(item_frame, text=text, font=("Arial", 9), bg="white", fg="#7f8c8d").pack(side="left", padx=5)

    def _create_sensor_list(self, parent):
        list_frame = tk.LabelFrame(
            parent,
            text="📊 Sensor Status List",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        list_frame.pack(fill="both", expand=True)

        tree_container = tk.Frame(list_frame, bg="white")
        tree_container.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("ID", "Type", "Location", "Sensor", "State")
        self.sensor_tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show="headings",
            height=10
        )

        self.sensor_tree.heading("ID", text="ID")
        self.sensor_tree.heading("Type", text="Type")
        self.sensor_tree.heading("Location", text="Location")
        self.sensor_tree.heading("Sensor", text="Sensor")
        self.sensor_tree.heading("State", text="Door/Motion")

        self.sensor_tree.column("ID", width=50, anchor="center")
        self.sensor_tree.column("Type", width=100, anchor="center")
        self.sensor_tree.column("Location", width=120, anchor="w")
        self.sensor_tree.column("Sensor", width=100, anchor="center")
        self.sensor_tree.column("State", width=120, anchor="center")

        self.sensor_tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.sensor_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.sensor_tree.configure(yscrollcommand=scrollbar.set)

        style = ttk.Style()
        style.configure("Treeview", rowheight=28, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

    def _create_control_panels(self, parent):
        # Window/Door 제어
        wd_frame = tk.LabelFrame(
            parent,
            text="🚪 Window/Door Sensors",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        wd_frame.pack(fill="x", pady=(0, 15))

        wd_content = tk.Frame(wd_frame, bg="white")
        wd_content.pack(padx=15, pady=15)

        tk.Label(wd_content, text="Sensor ID:", font=("Arial", 11), bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.wd_id_var = tk.StringVar()
        tk.Entry(wd_content, textvariable=self.wd_id_var, font=("Arial", 11), width=15).grid(row=0, column=1, padx=5, pady=5)

        self.wd_range_label = tk.Label(wd_content, text="Available IDs: N/A", font=("Arial", 9), bg="white", fg="#7f8c8d")
        self.wd_range_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))

        tk.Label(wd_content, text="Sensor Control:", font=("Arial", 10, "bold"), bg="white").grid(row=2, column=0, columnspan=2, sticky="w", pady=(5, 5))

        btn_frame1 = tk.Frame(wd_content, bg="white")
        btn_frame1.grid(row=3, column=0, columnspan=2, pady=5)

        tk.Button(
            btn_frame1,
            text="🟢 ARM SENSOR",
            bg="#27ae60",
            fg="black",
            font=("Helvetica", 11, "bold"),
            width=15,
            height=2,
            command=lambda: self._handle_windoor_sensor("arm"),
            relief="groove",
            bd=3,
            cursor="hand2",
            activebackground="#229954",
            activeforeground="black"
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame1,
            text="🔴 DISARM SENSOR",
            bg="#e74c3c",
            fg="black",
            font=("Helvetica", 11, "bold"),
            width=15,
            height=2,
            command=lambda: self._handle_windoor_sensor("disarm"),
            relief="groove",
            bd=3,
            cursor="hand2",
            activebackground="#c0392b",
            activeforeground="black"
        ).pack(side="left", padx=5)

        tk.Label(wd_content, text="Door/Window State:", font=("Arial", 10, "bold"), bg="white").grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 5))

        btn_frame2 = tk.Frame(wd_content, bg="white")
        btn_frame2.grid(row=5, column=0, columnspan=2, pady=5)

        tk.Button(
            btn_frame2,
            text="🚪 OPEN",
            bg="#3498db",
            fg="black",
            font=("Helvetica", 11, "bold"),
            width=15,
            height=2,
            command=lambda: self._handle_windoor("open"),
            relief="groove",
            bd=3,
            cursor="hand2",
            activebackground="#2980b9",
            activeforeground="black"
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame2,
            text="🚪 CLOSE",
            bg="#95a5a6",
            fg="black",
            font=("Helvetica", 11, "bold"),
            width=15,
            height=2,
            command=lambda: self._handle_windoor("close"),
            relief="groove",
            bd=3,
            cursor="hand2",
            activebackground="#7f8c8d",
            activeforeground="black"
        ).pack(side="left", padx=5)

        # Motion Detector 제어
        md_frame = tk.LabelFrame(
            parent,
            text="👁️ Motion Detectors",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        md_frame.pack(fill="x", pady=(0, 15))

        md_content = tk.Frame(md_frame, bg="white")
        md_content.pack(padx=15, pady=15)

        tk.Label(md_content, text="Detector ID:", font=("Arial", 11), bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.md_id_var = tk.StringVar()
        tk.Entry(md_content, textvariable=self.md_id_var, font=("Arial", 11), width=15).grid(row=0, column=1, padx=5, pady=5)

        self.md_range_label = tk.Label(md_content, text="Available IDs: N/A", font=("Arial", 9), bg="white", fg="#7f8c8d")
        self.md_range_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))

        tk.Label(md_content, text="Sensor Control:", font=("Arial", 10, "bold"), bg="white").grid(row=2, column=0, columnspan=2, sticky="w", pady=(5, 5))

        btn_frame3 = tk.Frame(md_content, bg="white")
        btn_frame3.grid(row=3, column=0, columnspan=2, pady=5)

        tk.Button(
            btn_frame3,
            text="🟢 ARM SENSOR",
            bg="#27ae60",
            fg="black",
            font=("Helvetica", 11, "bold"),
            width=15,
            height=2,
            command=lambda: self._handle_motion_sensor("arm"),
            relief="groove",
            bd=3,
            cursor="hand2",
            activebackground="#229954",
            activeforeground="black"
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame3,
            text="🔴 DISARM SENSOR",
            bg="#e74c3c",
            fg="black",
            font=("Helvetica", 11, "bold"),
            width=15,
            height=2,
            command=lambda: self._handle_motion_sensor("disarm"),
            relief="groove",
            bd=3,
            cursor="hand2",
            activebackground="#c0392b",
            activeforeground="black"
        ).pack(side="left", padx=5)

        tk.Label(md_content, text="Motion State:", font=("Arial", 10, "bold"), bg="white").grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 5))

        btn_frame4 = tk.Frame(md_content, bg="white")
        btn_frame4.grid(row=5, column=0, columnspan=2, pady=5)

        tk.Button(
            btn_frame4,
            text="👁️ DETECT MOTION",
            bg="#9b59b6",
            fg="black",
            font=("Helvetica", 11, "bold"),
            width=15,
            height=2,
            command=lambda: self._handle_motion("detect"),
            relief="groove",
            bd=3,
            cursor="hand2",
            activebackground="#8e44ad",
            activeforeground="black"
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame4,
            text="⚪ CLEAR MOTION",
            bg="#95a5a6",
            fg="black",
            font=("Helvetica", 11, "bold"),
            width=15,
            height=2,
            command=lambda: self._handle_motion("clear"),
            relief="groove",
            bd=3,
            cursor="hand2",
            activebackground="#7f8c8d",
            activeforeground="black"
        ).pack(side="left", padx=5)

        quick_frame = tk.LabelFrame(
            parent,
            text="⚡ Quick Actions",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        quick_frame.pack(fill="x")

        quick_content = tk.Frame(quick_frame, bg="white")
        quick_content.pack(padx=15, pady=15)

        tk.Button(
            quick_content,
            text="🟢 ARM ALL SENSORS",
            bg="#27ae60",
            fg="black",
            font=("Helvetica", 12, "bold"),
            width=32,
            height=2,
            command=self._arm_all,
            relief="groove",
            bd=3,
            cursor="hand2",
            activebackground="#229954",
            activeforeground="black"
        ).pack(pady=5)

        tk.Button(
            quick_content,
            text="🔴 DISARM ALL SENSORS",
            bg="#e74c3c",
            fg="black",
            font=("Helvetica", 12, "bold"),
            width=32,
            height=2,
            command=self._disarm_all,
            relief="groove",
            bd=3,
            cursor="hand2",
            activebackground="#c0392b",
            activeforeground="black"
        ).pack(pady=5)

        tk.Button(
            quick_content,
            text="🔄 RESET ALL STATES",
            bg="#3498db",
            fg="black",
            font=("Helvetica", 12, "bold"),
            width=32,
            height=2,
            command=self._reset_all,
            relief="groove",
            bd=3,
            cursor="hand2",
            activebackground="#2980b9",
            activeforeground="black"
        ).pack(pady=5)

    # === Helpers & Actions ===
    def _update_id_ranges(self):
        wd_ids = []
        scan = DeviceSensorTester.head_WinDoorSensor
        while scan is not None:
            sensor_id = getattr(scan, "sensor_id", getattr(scan, "sensorID", None))
            if sensor_id is not None:
                wd_ids.append(sensor_id)
            scan = getattr(scan, "next", None)

        if wd_ids:
            wd_ids.sort()
            self.wd_range_label.config(text=f"Available IDs: {min(wd_ids)}-{max(wd_ids)} ({len(wd_ids)} sensors)")
        else:
            self.wd_range_label.config(text="Available IDs: No sensors registered")

        md_ids = []
        scan = DeviceSensorTester.head_MotionDetector
        while scan is not None:
            sensor_id = getattr(scan, "sensor_id", getattr(scan, "sensorID", None))
            if sensor_id is not None:
                md_ids.append(sensor_id)
            scan = getattr(scan, "next", None)

        if md_ids:
            md_ids.sort()
            self.md_range_label.config(text=f"Available IDs: {min(md_ids)}-{max(md_ids)} ({len(md_ids)} detectors)")
        else:
            self.md_range_label.config(text="Available IDs: No detectors registered")

    def _update_status(self):
        for item in self.sensor_tree.get_children():
            self.sensor_tree.delete(item)

        scan = DeviceSensorTester.head_WinDoorSensor
        while scan is not None:
            sensor_id = getattr(scan, "sensor_id", getattr(scan, "sensorID", "?"))
            name = getattr(scan, "name", getattr(scan, "location", f"WinDoor {sensor_id}"))

            if callable(getattr(scan, "test_armed_state", None)):
                try:
                    armed = bool(scan.test_armed_state())
                except Exception:
                    armed = False
            else:
                armed = getattr(scan, "armed", getattr(scan, "enabled", False))

            opened = getattr(scan, "opened", False)

            sensor_status = "🟢 Armed" if armed else "🔴 Disarmed"
            door_status = "🚪 Open" if opened else "🚪 Closed"

            self.sensor_tree.insert(
                "",
                "end",
                values=(sensor_id, "Window/Door", name, sensor_status, door_status)
            )

            scan = getattr(scan, "next", None)

        scan = DeviceSensorTester.head_MotionDetector
        while scan is not None:
            sensor_id = getattr(scan, "sensor_id", getattr(scan, "sensorID", "?"))
            name = getattr(scan, "name", getattr(scan, "location", f"Motion {sensor_id}"))

            if callable(getattr(scan, "test_armed_state", None)):
                try:
                    armed = bool(scan.test_armed_state())
                except Exception:
                    armed = False
            else:
                armed = getattr(scan, "enabled", getattr(scan, "armed", False))

            detected = getattr(scan, "detected", False)

            sensor_status = "🟢 Armed" if armed else "🔴 Disarmed"
            motion_status = "👁️ Detected" if detected else "⚪ Clear"

            self.sensor_tree.insert(
                "",
                "end",
                values=(sensor_id, "Motion", name, sensor_status, motion_status)
            )

            scan = getattr(scan, "next", None)

        self.after(500, self._update_status)

    def _handle_windoor_sensor(self, action):
        sensor_id = self._get_id_from_entry(self.wd_id_var)
        if sensor_id is None:
            return

        scan = DeviceSensorTester.head_WinDoorSensor
        while scan is not None and getattr(scan, "sensor_id", None) != sensor_id:
            scan = getattr(scan, "next", None)

        if scan is None:
            messagebox.showwarning("Sensor Not Found", f"ID {sensor_id} not exist")
            return

        if action == "arm":
            scan.arm()
        else:
            scan.disarm()

        self._update_status()

    def _handle_windoor(self, action):
        sensor_id = self._get_id_from_entry(self.wd_id_var)
        if sensor_id is None:
            return

        scan = DeviceSensorTester.head_WinDoorSensor
        while scan is not None and getattr(scan, "sensor_id", None) != sensor_id:
            scan = getattr(scan, "next", None)

        if scan is None:
            messagebox.showwarning("Sensor Not Found", f"ID {sensor_id} not exist")
        else:
            if action == "open":
                scan.intrude()
            else:
                scan.release()
        self._update_status()

    def _handle_motion_sensor(self, action):
        sensor_id = self._get_id_from_entry(self.md_id_var)
        if sensor_id is None:
            return

        scan = DeviceSensorTester.head_MotionDetector
        while scan is not None and getattr(scan, "sensor_id", None) != sensor_id:
            scan = getattr(scan, "next", None)

        if scan is None:
            messagebox.showwarning("Sensor Not Found", f"ID {sensor_id} not exist")
            return

        if action == "arm":
            scan.arm()
        else:
            scan.disarm()

        self._update_status()

    def _handle_motion(self, action):
        sensor_id = self._get_id_from_entry(self.md_id_var)
        if sensor_id is None:
            return

        scan = DeviceSensorTester.head_MotionDetector
        while scan is not None and getattr(scan, "sensor_id", None) != sensor_id:
            scan = getattr(scan, "next", None)

        if scan is None:
            messagebox.showwarning("Sensor Not Found", f"ID {sensor_id} not exist")
        else:
            if action == "detect":
                scan.intrude()
            else:
                scan.release()

        self._update_status()

    def _arm_all(self):
        scan = DeviceSensorTester.head_WinDoorSensor
        while scan is not None:
            scan.arm()
            scan = getattr(scan, "next", None)

        scan = DeviceSensorTester.head_MotionDetector
        while scan is not None:
            scan.arm()
            scan = getattr(scan, "next", None)

        self._update_status()

    def _disarm_all(self):
        scan = DeviceSensorTester.head_WinDoorSensor
        while scan is not None:
            scan.disarm()
            scan = getattr(scan, "next", None)

        scan = DeviceSensorTester.head_MotionDetector
        while scan is not None:
            scan.disarm()
            scan = getattr(scan, "next", None)

        self._update_status()

    def _reset_all(self):
        scan = DeviceSensorTester.head_WinDoorSensor
        while scan is not None:
            scan.disarm()
            scan.release()
            scan = getattr(scan, "next", None)

        scan = DeviceSensorTester.head_MotionDetector
        while scan is not None:
            scan.disarm()
            scan.release()
            scan = getattr(scan, "next", None)

        self._update_status()

    def _get_id_from_entry(self, var):
        input_number = var.get().strip()
        if not input_number:
            messagebox.showwarning("Input Error", "Please enter sensor ID")
            return None
        if not input_number.isdigit():
            messagebox.showwarning("Input Error", "Only digits allowed")
            return None
        return int(input_number)

    def _on_close(self):
        """Ensure tester reference resets so it can be reopened."""
        try:
            DeviceSensorTester.safeHomeSensorTest = None
            DeviceSensorTester.safehome_sensor_test = None
        except Exception:
            pass
        self.destroy()


# Backward compatibility alias
SensorSimulator = SafeHomeSensorTest

