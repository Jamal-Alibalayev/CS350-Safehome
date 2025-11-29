"""
SafeHome Sensor Simulator GUI
Modern interface for testing sensors based on fixed floor plan
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from safehome.device.sensor.device_sensor_tester import DeviceSensorTester
from pathlib import Path

WINDOW_IDS = tuple(range(1, 7))
DOOR_IDS = (7, 8)
MOTION_USER_IDS = (9, 10)

WINDOW_LOCATIONS = {
    1: "Dining Room",
    2: "Dining Room",
    3: "Kitchen",
    4: "Living Room",
    5: "Living Room",
    6: "Living Room",
}

DOOR_LOCATIONS = {7: "Entrance", 8: "Kitchen"}

MOTION_LOCATIONS = {
    9: "Dining→Entrance→Living (cross-room)",
    10: "Kitchen diagonal (top-right to bottom-left)",
}


class SafeHomeSensorTest(tk.Toplevel):
    """
    현대적인 센서 시뮬레이터 GUI
    - Floor plan 기반 센서 배치
    - 10개 고정 센서 (6 windows, 2 doors, 2 motion)
    - 실시간 상태 업데이트
    """

    def __init__(self, master=None):
        super().__init__(master)
        self.title("SafeHome - Sensor Simulator")
        self.geometry("1200x700")
        self.resizable(True, True)

        # 변수 초기화
        self.sensor_widgets = {}

        # UI 구성
        self._create_ui()

        # 센서 ID 범위 업데이트
        self._update_id_ranges()

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
            text="🧪 Sensor Simulator",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white",
        ).pack(side="left", padx=20, pady=15)

        tk.Label(
            header,
            text="Test sensors based on fixed floor plan",
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
            # Floor plan 이미지 로드
            script_dir = Path(__file__).parent
            img_path = (
                script_dir / ".." / ".." / ".." / "assets" / "images" / "floorplan.png"
            ).resolve()
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
                fg="#95a5a6",
            ).pack(pady=20)

        # Legend
        legend_frame = tk.Frame(floorplan_frame, bg="white")
        legend_frame.pack(fill="x", padx=10, pady=(0, 10))

        legend_items = [
            ("🔴", "Red dots = Windows (S₁-S₆)"),
            ("🔵", "Blue dots = Doors (D₁-D₂)"),
            ("📹", "Cameras (C₁-C₃)"),
            ("👁️", "Motion Detectors (M₁-M₂)"),
        ]

        for emoji, text in legend_items:
            item_frame = tk.Frame(legend_frame, bg="white")
            item_frame.pack(side="left", padx=10)
            tk.Label(item_frame, text=emoji, font=("Arial", 12), bg="white").pack(
                side="left"
            )
            tk.Label(
                item_frame, text=text, font=("Arial", 9), bg="white", fg="#7f8c8d"
            ).pack(side="left", padx=5)

    def _create_sensor_list(self, parent):
        """센서 목록 테이블"""
        list_frame = tk.LabelFrame(
            parent,
            text="📊 Sensor Status List",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50",
        )
        list_frame.pack(fill="both", expand=True)

        # Treeview
        tree_container = tk.Frame(list_frame, bg="white")
        tree_container.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("ID", "Type", "Location", "Sensor", "State")
        self.sensor_tree = ttk.Treeview(
            tree_container, columns=columns, show="headings", height=10
        )

        # 컬럼 설정
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

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            tree_container, orient="vertical", command=self.sensor_tree.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.sensor_tree.configure(yscrollcommand=scrollbar.set)

        # 스타일
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
            if event.num == 4 or (hasattr(event, "delta") and event.delta > 0):
                canvas.yview_scroll(-1, "units")
            elif event.num == 5 or (hasattr(event, "delta") and event.delta < 0):
                canvas.yview_scroll(1, "units")

        def _bind_mousewheel_recursively(widget):
            widget.bind("<MouseWheel>", _on_mousewheel)
            widget.bind("<Button-4>", _on_mousewheel)
            widget.bind("<Button-5>", _on_mousewheel)
            for child in widget.winfo_children():
                _bind_mousewheel_recursively(child)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._create_control_panels(scrollable_frame)

        # Bind events after a short delay to ensure all widgets are created
        self.after(100, lambda: _bind_mousewheel_recursively(scrollable_frame))

    def _create_control_panels(self, parent):
        """센서 제어 패널"""
        # Window/Door 제어 (combined IDs 1-8)
        wd_frame = tk.LabelFrame(
            parent,
            text="🚪 Window/Door Sensors (IDs 1-8)",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50",
        )
        wd_frame.pack(fill="x", pady=(0, 15), padx=10)

        wd_content = tk.Frame(wd_frame, bg="white")
        wd_content.pack(padx=15, pady=15)

        # ID 입력
        tk.Label(
            wd_content, text="Sensor ID (1-8):", font=("Arial", 11), bg="white"
        ).grid(row=0, column=0, sticky="w", pady=5)
        self.wd_id_var = tk.StringVar()
        tk.Entry(
            wd_content, textvariable=self.wd_id_var, font=("Arial", 11), width=15
        ).grid(row=0, column=1, padx=5, pady=5)

        # ID 범위 표시
        self.wd_range_label = tk.Label(
            wd_content,
            text="Available IDs: 1-8 (1-6 windows, 7-8 doors)",
            font=("Arial", 9),
            bg="white",
            fg="#7f8c8d",
        )
        self.wd_range_label.grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )

        # 센서 제어
        tk.Label(
            wd_content, text="Sensor Control:", font=("Arial", 10, "bold"), bg="white"
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(5, 5))

        btn_frame1 = tk.Frame(wd_content, bg="white")
        btn_frame1.grid(row=3, column=0, columnspan=2, pady=5)

        tk.Button(
            btn_frame1,
            text="🟢 ARM (1-8)",
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
            activeforeground="black",
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame1,
            text="🔴 DISARM (1-8)",
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
            activeforeground="black",
        ).pack(side="left", padx=5)

        # Door/Window 제어
        tk.Label(
            wd_content,
            text="Door/Window State:",
            font=("Arial", 10, "bold"),
            bg="white",
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 5))

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
            activeforeground="black",
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
            activeforeground="black",
        ).pack(side="left", padx=5)

        # Motion Detector 제어
        md_frame = tk.LabelFrame(
            parent,
            text="👁️ Motion Detectors",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50",
        )
        md_frame.pack(fill="x", pady=(0, 15), padx=10)

        md_content = tk.Frame(md_frame, bg="white")
        md_content.pack(padx=15, pady=15)

        # ID 입력
        tk.Label(
            md_content, text="Detector ID (9-10):", font=("Arial", 11), bg="white"
        ).grid(row=0, column=0, sticky="w", pady=5)
        self.md_id_var = tk.StringVar()
        tk.Entry(
            md_content, textvariable=self.md_id_var, font=("Arial", 11), width=15
        ).grid(row=0, column=1, padx=5, pady=5)

        # ID 범위 표시
        self.md_range_label = tk.Label(
            md_content,
            text="Available IDs: 9-10",
            font=("Arial", 9),
            bg="white",
            fg="#7f8c8d",
        )
        self.md_range_label.grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )

        # 센서 제어
        tk.Label(
            md_content, text="Sensor Control:", font=("Arial", 10, "bold"), bg="white"
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(5, 5))

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
            activeforeground="black",
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
            activeforeground="black",
        ).pack(side="left", padx=5)

        # Motion 제어
        tk.Label(
            md_content, text="Motion State:", font=("Arial", 10, "bold"), bg="white"
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 5))

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
            activeforeground="black",
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
            activeforeground="black",
        ).pack(side="left", padx=5)

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
        quick_content.pack(padx=15, pady=15)

        tk.Button(
            quick_content,
            text="🟢 ARM ALL SENSORS",
            bg="#27ae60",
            fg="black",
            font=("Helvetica", 12, "bold"),
            height=2,
            command=self._arm_all,
            relief="groove",
            bd=3,
            cursor="hand2",
            activebackground="#229954",
            activeforeground="black",
        ).pack(pady=5, fill="x", expand=True)

        tk.Button(
            quick_content,
            text="🔴 DISARM ALL SENSORS",
            bg="#e74c3c",
            fg="black",
            font=("Helvetica", 12, "bold"),
            height=2,
            command=self._disarm_all,
            relief="groove",
            bd=3,
            cursor="hand2",
            activebackground="#c0392b",
            activeforeground="black",
        ).pack(pady=5, fill="x", expand=True)

        tk.Button(
            quick_content,
            text="🔄 RESET ALL STATES",
            bg="#3498db",
            fg="black",
            font=("Helvetica", 12, "bold"),
            height=2,
            command=self._reset_all,
            relief="groove",
            bd=3,
            cursor="hand2",
            activebackground="#2980b9",
            activeforeground="black",
        ).pack(pady=5, fill="x", expand=True)

    def _create_control_panels(self, parent):
        """센서 제어 패널"""
        # Window/Door 제어
        wd_frame = tk.LabelFrame(
            parent,
            text="🚪 Window/Door Sensors",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50",
        )
        wd_frame.pack(fill="x", pady=(0, 15), padx=10)

        wd_content = tk.Frame(wd_frame, bg="white")
        wd_content.pack(padx=15, pady=15)

        # ID 입력
        tk.Label(wd_content, text="Sensor ID:", font=("Arial", 11), bg="white").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.wd_id_var = tk.StringVar()
        tk.Entry(
            wd_content, textvariable=self.wd_id_var, font=("Arial", 11), width=15
        ).grid(row=0, column=1, padx=5, pady=5)

        # ID 범위 표시
        self.wd_range_label = tk.Label(
            wd_content,
            text="Available IDs: N/A",
            font=("Arial", 9),
            bg="white",
            fg="#7f8c8d",
        )
        self.wd_range_label.grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )

        # 센서 제어
        tk.Label(
            wd_content, text="Sensor Control:", font=("Arial", 10, "bold"), bg="white"
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(5, 5))

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
            activeforeground="black",
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
            activeforeground="black",
        ).pack(side="left", padx=5)

        # Door/Window 제어
        tk.Label(
            wd_content,
            text="Door/Window State:",
            font=("Arial", 10, "bold"),
            bg="white",
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 5))

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
            activeforeground="black",
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
            activeforeground="black",
        ).pack(side="left", padx=5)

        # Motion Detector 제어
        md_frame = tk.LabelFrame(
            parent,
            text="👁️ Motion Detectors",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50",
        )
        md_frame.pack(fill="x", pady=(0, 15), padx=10)

        md_content = tk.Frame(md_frame, bg="white")
        md_content.pack(padx=15, pady=15)

        # ID 입력
        tk.Label(md_content, text="Detector ID:", font=("Arial", 11), bg="white").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.md_id_var = tk.StringVar()
        tk.Entry(
            md_content, textvariable=self.md_id_var, font=("Arial", 11), width=15
        ).grid(row=0, column=1, padx=5, pady=5)

        # ID 범위 표시
        self.md_range_label = tk.Label(
            md_content,
            text="Available IDs: N/A",
            font=("Arial", 9),
            bg="white",
            fg="#7f8c8d",
        )
        self.md_range_label.grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )

        # 센서 제어
        tk.Label(
            md_content, text="Sensor Control:", font=("Arial", 10, "bold"), bg="white"
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(5, 5))

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
            activeforeground="black",
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
            activeforeground="black",
        ).pack(side="left", padx=5)

        # Motion 제어
        tk.Label(
            md_content, text="Motion State:", font=("Arial", 10, "bold"), bg="white"
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 5))

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
            activeforeground="black",
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
            activeforeground="black",
        ).pack(side="left", padx=5)

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
        quick_content.pack(padx=15, pady=15)

        tk.Button(
            quick_content,
            text="🟢 ARM ALL SENSORS",
            bg="#27ae60",
            fg="black",
            font=("Helvetica", 12, "bold"),
            height=2,
            command=self._arm_all,
            relief="groove",
            bd=3,
            cursor="hand2",
            activebackground="#229954",
            activeforeground="black",
        ).pack(pady=5, fill="x", expand=True)

        tk.Button(
            quick_content,
            text="🔴 DISARM ALL SENSORS",
            bg="#e74c3c",
            fg="black",
            font=("Helvetica", 12, "bold"),
            height=2,
            command=self._disarm_all,
            relief="groove",
            bd=3,
            cursor="hand2",
            activebackground="#c0392b",
            activeforeground="black",
        ).pack(pady=5, fill="x", expand=True)

        tk.Button(
            quick_content,
            text="🔄 RESET ALL STATES",
            bg="#3498db",
            fg="black",
            font=("Helvetica", 12, "bold"),
            height=2,
            command=self._reset_all,
            relief="groove",
            bd=3,
            cursor="hand2",
            activebackground="#2980b9",
            activeforeground="black",
        ).pack(pady=5, fill="x", expand=True)

    def _update_id_ranges(self):
        """센서 ID 범위 업데이트 (고정 개수)"""
        # Fixed ranges by requirement
        self.wd_range_label.config(text="Fixed Window/Door IDs: 1-8")
        if hasattr(self, "door_range_label"):
            self.door_range_label.config(text="Fixed Door IDs: 1-2")
        self.md_range_label.config(text="Fixed Motion IDs: 9-10")

    def _update_status(self):
        """센서 상태 업데이트 (500ms마다)"""
        # Clear tree
        for item in self.sensor_tree.get_children():
            self.sensor_tree.delete(item)

        windoor_map = self._collect_windoor_map()
        motion_map = self._collect_motion_map()

        # Windows
        for row in self._build_window_rows(windoor_map):
            self.sensor_tree.insert("", "end", values=row)

        # Doors
        for row in self._build_door_rows(windoor_map):
            self.sensor_tree.insert("", "end", values=row)

        # Motions
        for row in self._build_motion_rows(motion_map):
            self.sensor_tree.insert("", "end", values=row)

        # Schedule next update
        self.after(500, self._update_status)

    # ===== Helpers for status building =====
    def _collect_windoor_map(self) -> dict:
        """Build ID->sensor map for window/door chain."""
        result = {}
        scan = DeviceSensorTester.head_WinDoorSensor
        while scan is not None:
            sid = getattr(scan, "sensor_id", getattr(scan, "sensorID", None))
            if sid is not None:
                result[sid] = scan
            scan = getattr(scan, "next", getattr(scan, "next_sensor", None))
        return result

    def _collect_motion_map(self) -> dict:
        """Build ID->sensor map for motion chain."""
        result = {}
        scan = DeviceSensorTester.head_MotionDetector
        while scan is not None:
            sid = getattr(scan, "sensor_id", getattr(scan, "sensorID", None))
            if sid is not None:
                result[sid] = scan
            scan = getattr(scan, "next", getattr(scan, "next_sensor", None))
        return result

    def _build_window_rows(self, windoor_map: dict):
        for sid in WINDOW_IDS:
            sensor = windoor_map.get(sid)
            name = f"Window {sid} ({WINDOW_LOCATIONS.get(sid,'')})"
            sensor_status, door_status = self._get_sensor_states(sensor)
            yield (sid, "Window", name, sensor_status, door_status)

    def _build_door_rows(self, windoor_map: dict):
        for sid in DOOR_IDS:
            display_id = sid - 6
            name = f"Door {display_id} ({DOOR_LOCATIONS.get(sid,'')})"
            sensor = windoor_map.get(sid)
            sensor_status, door_status = self._get_sensor_states(sensor)
            yield (sid, "Door", name, sensor_status, door_status)

    def _build_motion_rows(self, motion_map: dict):
        for user_sid in MOTION_USER_IDS:
            actual_id = user_sid - 8  # underlying id 1-2
            sensor = motion_map.get(actual_id)
            name = f"Motion {user_sid} ({MOTION_LOCATIONS.get(user_sid,'')})"
            if sensor:
                armed = False
                if callable(getattr(sensor, "test_armed_state", None)):
                    try:
                        armed = bool(sensor.test_armed_state())
                    except Exception:
                        armed = False
                else:
                    armed = getattr(sensor, "enabled", getattr(sensor, "armed", False))
                detected = getattr(sensor, "detected", False)
                sensor_status = "🟢 Armed" if armed else "🔴 Disarmed"
                motion_status = "👁️ Detected" if detected else "⚪ Clear"
            else:
                sensor_status = "⚪ Not Connected"
                motion_status = "N/A"
            yield (user_sid, "Motion", name, sensor_status, motion_status)

    def _get_sensor_states(self, sensor):
        """Return (armed_state, open_state text) for window/door sensor."""
        if sensor:
            armed = False
            if callable(getattr(sensor, "test_armed_state", None)):
                try:
                    armed = bool(sensor.test_armed_state())
                except Exception:
                    armed = False
            else:
                armed = getattr(sensor, "armed", getattr(sensor, "enabled", False))
            opened = getattr(sensor, "opened", False)
            sensor_status = "🟢 Armed" if armed else "🔴 Disarmed"
            door_status = "🚪 Open" if opened else "🚪 Closed"
        else:
            sensor_status = "⚪ Not Connected"
            door_status = "N/A"
        return sensor_status, door_status

    def _handle_windoor_sensor(self, action: str):
        """Window/Door 센서 arm/disarm"""
        sensor_id_str = self.wd_id_var.get().strip()
        if not sensor_id_str:
            messagebox.showwarning("Input Required", "Please enter a sensor ID")
            return

        try:
            sensor_id = int(sensor_id_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Sensor ID must be a number")
            return

        # Validate fixed range
        if sensor_id < 1 or sensor_id > 8:
            messagebox.showerror(
                "Invalid Input",
                "Valid Window/Door IDs are 1-8 (1-6 windows, 7-8 doors)",
            )
            return

        # Find sensor
        scan = DeviceSensorTester.head_WinDoorSensor
        found = False
        while scan is not None:
            sid = getattr(scan, "sensor_id", getattr(scan, "sensorID", None))
            if sid == sensor_id:
                found = True
                if action == "arm":
                    if hasattr(scan, "arm"):
                        scan.arm()
                    elif hasattr(scan, "enable"):
                        scan.enable()
                elif action == "disarm":
                    if hasattr(scan, "disarm"):
                        scan.disarm()
                    elif hasattr(scan, "disable"):
                        scan.disable()
                break
            scan = getattr(scan, "next", None)

        if not found:
            messagebox.showerror(
                "Not Found", f"Window/Door sensor ID {sensor_id} not found"
            )

    def _handle_windoor(self, action: str):
        """Window/Door 열기/닫기"""
        sensor_id_str = self.wd_id_var.get().strip()
        if not sensor_id_str:
            messagebox.showwarning("Input Required", "Please enter a sensor ID")
            return

        try:
            sensor_id = int(sensor_id_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Sensor ID must be a number")
            return

        # Find sensor
        scan = DeviceSensorTester.head_WinDoorSensor
        found = False
        while scan is not None:
            sid = getattr(scan, "sensor_id", getattr(scan, "sensorID", None))
            if sid == sensor_id:
                found = True
                if action == "open":
                    if hasattr(scan, "intrude"):
                        scan.intrude()
                    elif hasattr(scan, "open"):
                        scan.open()
                elif action == "close":
                    if hasattr(scan, "release"):
                        scan.release()
                    elif hasattr(scan, "close"):
                        scan.close()
                break
            scan = getattr(scan, "next", None)

        if not found:
            messagebox.showerror(
                "Not Found", f"Window/Door sensor ID {sensor_id} not found"
            )

    def _handle_motion_sensor(self, action: str):
        """Motion detector arm/disarm"""
        sensor_id_str = self.md_id_var.get().strip()
        if not sensor_id_str:
            messagebox.showwarning("Input Required", "Please enter a detector ID")
            return

        try:
            sensor_id = int(sensor_id_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Detector ID must be a number")
            return

        if sensor_id < 9 or sensor_id > 10:
            messagebox.showerror("Invalid Input", "Valid Motion IDs are 9-10")
            return

        actual_id = sensor_id - 8  # underlying id

        # Find detector
        scan = DeviceSensorTester.head_MotionDetector
        found = False
        while scan is not None:
            sid = getattr(scan, "sensor_id", getattr(scan, "sensorID", None))
            if sid == actual_id:
                found = True
                if action == "arm":
                    if hasattr(scan, "arm"):
                        scan.arm()
                    elif hasattr(scan, "enable"):
                        scan.enable()
                elif action == "disarm":
                    if hasattr(scan, "disarm"):
                        scan.disarm()
                    elif hasattr(scan, "disable"):
                        scan.disable()
                break
            scan = getattr(scan, "next", None)

        if not found:
            messagebox.showerror(
                "Not Found", f"Motion detector ID {sensor_id} not found"
            )

    def _handle_motion(self, action: str):
        """Motion 감지/해제"""
        sensor_id_str = self.md_id_var.get().strip()
        if not sensor_id_str:
            messagebox.showwarning("Input Required", "Please enter a detector ID")
            return

        try:
            sensor_id = int(sensor_id_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Detector ID must be a number")
            return

        if sensor_id < 9 or sensor_id > 10:
            messagebox.showerror("Invalid Input", "Valid Motion IDs are 9-10")
            return

        actual_id = sensor_id - 8

        # Find detector
        scan = DeviceSensorTester.head_MotionDetector
        found = False
        while scan is not None:
            sid = getattr(scan, "sensor_id", getattr(scan, "sensorID", None))
            if sid == actual_id:
                found = True
                if action == "detect":
                    if hasattr(scan, "intrude"):
                        scan.intrude()
                    elif hasattr(scan, "detect"):
                        scan.detect()
                elif action == "clear":
                    if hasattr(scan, "release"):
                        scan.release()
                    elif hasattr(scan, "clear"):
                        scan.clear()
                break
            scan = getattr(scan, "next", None)

        if not found:
            messagebox.showerror(
                "Not Found", f"Motion detector ID {sensor_id} not found"
            )

    def _arm_all(self):
        """모든 센서 arm"""
        count = 0

        # Arm all Window/Door sensors
        scan = DeviceSensorTester.head_WinDoorSensor
        while scan is not None:
            if hasattr(scan, "arm"):
                scan.arm()
            elif hasattr(scan, "enable"):
                scan.enable()
            count += 1
            scan = getattr(scan, "next", None)

        # Arm all Motion detectors
        scan = DeviceSensorTester.head_MotionDetector
        while scan is not None:
            if hasattr(scan, "arm"):
                scan.arm()
            elif hasattr(scan, "enable"):
                scan.enable()
            count += 1
            scan = getattr(scan, "next", None)

        messagebox.showinfo("Success", f"Armed {count} sensors")

    def _disarm_all(self):
        """모든 센서 disarm"""
        count = 0

        # Disarm all Window/Door sensors
        scan = DeviceSensorTester.head_WinDoorSensor
        while scan is not None:
            if hasattr(scan, "disarm"):
                scan.disarm()
            elif hasattr(scan, "disable"):
                scan.disable()
            count += 1
            scan = getattr(scan, "next", None)

        # Disarm all Motion detectors
        scan = DeviceSensorTester.head_MotionDetector
        while scan is not None:
            if hasattr(scan, "disarm"):
                scan.disarm()
            elif hasattr(scan, "disable"):
                scan.disable()
            count += 1
            scan = getattr(scan, "next", None)

        messagebox.showinfo("Success", f"Disarmed {count} sensors")

    def _reset_all(self):
        """모든 센서 상태 초기화"""
        count = 0

        # Reset all Window/Door sensors
        scan = DeviceSensorTester.head_WinDoorSensor
        while scan is not None:
            if hasattr(scan, "release"):
                scan.release()
            elif hasattr(scan, "close"):
                scan.close()
            count += 1
            scan = getattr(scan, "next", None)

        # Reset all Motion detectors
        scan = DeviceSensorTester.head_MotionDetector
        while scan is not None:
            if hasattr(scan, "release"):
                scan.release()
            elif hasattr(scan, "clear"):
                scan.clear()
            count += 1
            scan = getattr(scan, "next", None)

        messagebox.showinfo("Success", f"Reset {count} sensors to default state")
