"""
SafeHome Sensor Simulator GUI
Modern interface for testing sensors based on the live system state.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from pathlib import Path
from safehome.device.sensor.windoor_sensor import WindowDoorSensor
from safehome.device.sensor.motion_sensor import MotionSensor

class SafeHomeSensorTest(tk.Toplevel):
    """
    현대적인 센서 시뮬레이터 GUI
    - 시스템의 실제 센서 객체를 직접 제어
    - 실시간 상태 동기화
    """

    def __init__(self, system, master=None):
        super().__init__(master)
        self.system = system
        self.title("SafeHome - Sensor Simulator (Live Mode)")
        self.geometry("1200x700")
        self.resizable(True, True)

        # UI 구성
        self._create_ui()

        # 상태 업데이트 시작
        self._update_status()

    def _create_ui(self):
        """UI 구성"""
        # 상단 헤더
        header = tk.Frame(self, bg="#2c3e50", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🧪 Sensor Simulator (Live Mode)",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white",
        ).pack(side="left", padx=20, pady=15)

        tk.Label(
            header,
            text="Directly control live sensors in the system",
            font=("Arial", 11),
            bg="#2c3e50",
            fg="#bdc3c7",
        ).pack(side="left")

        # 메인 컨테이너
        paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned_window.pack(fill="both", expand=True, padx=15, pady=15)

        # 좌측: Floor Plan 및 센서 목록
        left_panel = tk.Frame(paned_window, bg="#ecf0f1")
        paned_window.add(left_panel, weight=2)

        self._create_floorplan_section(left_panel)
        self._create_sensor_list(left_panel)

        # 우측: 센서 제어 패널
        right_panel = tk.Frame(paned_window, bg="#ecf0f1")
        paned_window.add(right_panel, weight=1)

        self._create_right_panel(right_panel)

    def _create_floorplan_section(self, parent):
        """Floor Plan 이미지 표시"""
        floorplan_frame = tk.LabelFrame(
            parent,
            text="📐 Floor Plan",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50",
        )
        floorplan_frame.pack(fill="x", pady=(0, 10))

        try:
            script_dir = Path(__file__).parent
            img_path = (
                script_dir / ".." / ".." / ".." / "assets" / "images" / "floorplan.png"
            ).resolve()
            img = Image.open(img_path)
            img = img.resize((600, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            img_label = tk.Label(floorplan_frame, image=photo, bg="white")
            img_label.image = photo
            img_label.pack(padx=10, pady=10)
        except Exception as e:
            tk.Label(
                floorplan_frame,
                text=f"Floor plan not available\n{str(e)}",
                font=("Arial", 10),
                bg="white",
                fg="#95a5a6",
            ).pack(pady=20)

    def _create_sensor_list(self, parent):
        """센서 목록 테이블"""
        list_frame = tk.LabelFrame(
            parent,
            text="📊 Live Sensor Status List",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50",
        )
        list_frame.pack(fill="both", expand=True)

        tree_container = tk.Frame(list_frame, bg="white")
        tree_container.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("ID", "Type", "Location", "Armed State", "Physical State")
        self.sensor_tree = ttk.Treeview(
            tree_container, columns=columns, show="headings", height=10
        )

        for col in columns:
            self.sensor_tree.heading(col, text=col)
        self.sensor_tree.column("ID", width=50, anchor="center")
        self.sensor_tree.column("Type", width=100, anchor="center")
        self.sensor_tree.column("Location", width=200, anchor="w")
        self.sensor_tree.column("Armed State", width=120, anchor="center")
        self.sensor_tree.column("Physical State", width=120, anchor="center")

        self.sensor_tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            tree_container, orient="vertical", command=self.sensor_tree.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.sensor_tree.configure(yscrollcommand=scrollbar.set)

        style = ttk.Style()
        style.configure("Treeview", rowheight=28, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

    def _create_right_panel(self, parent):
        """Create a scrollable right panel for controls."""
        canvas = tk.Canvas(parent, bg="#ecf0f1", highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ecf0f1")

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_mousewheel(event):
            delta = event.delta // 120 if hasattr(event, "delta") else -1 if event.num == 4 else 1
            canvas.yview_scroll(-delta, "units")

        def _bind_mousewheel_recursively(widget):
            widget.bind("<MouseWheel>", _on_mousewheel)
            widget.bind("<Button-4>", _on_mousewheel)
            widget.bind("<Button-5>", _on_mousewheel)
            for child in widget.winfo_children():
                _bind_mousewheel_recursively(child)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._create_control_panels(scrollable_frame)
        self.after(100, lambda: _bind_mousewheel_recursively(scrollable_frame))

    def _create_control_panels(self, parent):
        """센서 제어 패널"""
        # Combined Control Panel
        main_frame = tk.LabelFrame(
            parent,
            text="🕹️ Sensor Controls",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50",
        )
        main_frame.pack(fill="x", pady=(0, 15), padx=10)

        main_content = tk.Frame(main_frame, bg="white")
        main_content.pack(padx=15, pady=15)

        tk.Label(main_content, text="Sensor ID:", font=("Arial", 11), bg="white").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.id_var = tk.StringVar()
        tk.Entry(main_content, textvariable=self.id_var, font=("Arial", 11), width=15).grid(
            row=0, column=1, padx=5, pady=5
        )

        tk.Label(main_content, text="Sensor Control:", font=("Arial", 10, "bold"), bg="white").grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(10, 5)
        )
        btn_frame1 = tk.Frame(main_content, bg="white")
        btn_frame1.grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(btn_frame1, text="🟢 ARM", command=lambda: self._handle_sensor("arm"), width=15, height=2).pack(side="left", padx=5)
        tk.Button(btn_frame1, text="🔴 DISARM", command=lambda: self._handle_sensor("disarm"), width=15, height=2).pack(side="left", padx=5)

        tk.Label(main_content, text="Physical State:", font=("Arial", 10, "bold"), bg="white").grid(
            row=3, column=0, columnspan=2, sticky="w", pady=(10, 5)
        )
        btn_frame2 = tk.Frame(main_content, bg="white")
        btn_frame2.grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(btn_frame2, text="🚪 OPEN / DETECT", command=lambda: self._handle_sensor("trigger"), width=15, height=2).pack(side="left", padx=5)
        tk.Button(btn_frame2, text="⚪ CLOSE / CLEAR", command=lambda: self._handle_sensor("release"), width=15, height=2).pack(side="left", padx=5)
        
        # Quick Actions
        quick_frame = tk.LabelFrame(
            parent,
            text="⚡ Quick Actions",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50",
        )
        quick_frame.pack(fill="x", padx=10)
        quick_content = tk.Frame(quick_frame, bg="white")
        quick_content.pack(padx=15, pady=15, fill="x")
        tk.Button(quick_content, text="🟢 ARM ALL", command=self._arm_all, height=2).pack(pady=5, fill="x")
        tk.Button(quick_content, text="🔴 DISARM ALL", command=self._disarm_all, height=2).pack(pady=5, fill="x")
        tk.Button(quick_content, text="🔄 CLOSE/CLEAR ALL", command=self._reset_all, height=2).pack(pady=5, fill="x")

    def _update_status(self):
        """Periodically update the sensor status tree from the live system controller."""
        try:
            # Clear existing items
            for item in self.sensor_tree.get_children():
                self.sensor_tree.delete(item)

            # Get live sensors from the controller
            all_sensors = self.system.sensor_controller.get_all_sensors()

            for sensor in sorted(all_sensors, key=lambda s: s.sensor_id):
                sensor_type = sensor.sensor_type
                armed_state = "🟢 Armed" if sensor.is_active else "🔴 Disarmed"
                
                if isinstance(sensor, WindowDoorSensor):
                    physical_state = "🚪 Open" if sensor.is_open() else "🚪 Closed"
                elif isinstance(sensor, MotionSensor):
                    physical_state = "👁️ Detected" if sensor.is_motion_detected() else "⚪ Clear"
                else:
                    physical_state = "N/A"
                
                self.sensor_tree.insert(
                    "",
                    "end",
                    values=(sensor.sensor_id, sensor_type, sensor.location, armed_state, physical_state),
                )
        except Exception as e:
            # Handle case where window is closed while loop is running
            if not self.winfo_exists():
                return
            print(f"Error updating sensor simulator UI: {e}")

        self.after(500, self._update_status)

    def _get_sensor_from_id_input(self):
        """Helper to get a sensor object from the ID text input."""
        id_str = self.id_var.get().strip()
        if not id_str:
            messagebox.showwarning("Input Required", "Please enter a Sensor ID.")
            return None
        try:
            sensor_id = int(id_str)
            sensor = self.system.sensor_controller.get_sensor(sensor_id)
            if not sensor:
                messagebox.showerror("Not Found", f"Sensor with ID {sensor_id} not found in the system.")
                return None
            return sensor
        except ValueError:
            messagebox.showerror("Invalid Input", "Sensor ID must be a number.")
            return None

    def _handle_sensor(self, action: str):
        """Unified handler for sensor actions."""
        sensor = self._get_sensor_from_id_input()
        if not sensor:
            return

        if action == "arm":
            sensor.arm()
        elif action == "disarm":
            sensor.disarm()
        elif action == "trigger":
            if isinstance(sensor, WindowDoorSensor):
                sensor.simulate_open()
            elif isinstance(sensor, MotionSensor):
                sensor.simulate_motion()
        elif action == "release":
            if isinstance(sensor, WindowDoorSensor):
                sensor.simulate_close()
            elif isinstance(sensor, MotionSensor):
                sensor.simulate_clear()

    def _arm_all(self):
        """Arm all sensors in the system."""
        sensors = self.system.sensor_controller.get_all_sensors()
        for sensor in sensors:
            sensor.arm()
        messagebox.showinfo("Success", f"Armed {len(sensors)} sensors.")

    def _disarm_all(self):
        """Disarm all sensors in the system."""
        self.system.sensor_controller.disarm_all_sensors()
        sensors = self.system.sensor_controller.get_all_sensors()
        messagebox.showinfo("Success", f"Disarmed {len(sensors)} sensors.")

    def _reset_all(self):
        """Set all sensors to a default 'released' state (closed/clear)."""
        sensors = self.system.sensor_controller.get_all_sensors()
        count = 0
        for sensor in sensors:
            if isinstance(sensor, WindowDoorSensor):
                sensor.simulate_close()
                count += 1
            elif isinstance(sensor, MotionSensor):
                sensor.simulate_clear()
                count += 1
        messagebox.showinfo("Success", f"Reset {count} sensors to default state.")
