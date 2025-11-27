"""
SafeHome Main Dashboard
Unified monitoring and control interface
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from safehome.configuration.safehome_mode import SafeHomeMode


class MainDashboard(tk.Toplevel):
    """
    통합 메인 대시보드
    - 시스템 상태 실시간 모니터링
    - 센서/카메라 상태 한눈에 보기
    - 빠른 Arm/Disarm 액션
    - Zone 관리
    """

    def __init__(self, system, login_window):
        super().__init__()
        self.system = system
        self.login_window = login_window

        # 윈도우 설정
        self.title("SafeHome - Dashboard")
        self.geometry("1400x900")
        self.state('zoomed')  # 최대화

        # UI 구성
        self._create_ui()

        # 자동 업데이트 시작
        self._update_loop()

        # 종료 처리
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _create_ui(self):
        """UI 구성"""
        # 상단 헤더
        self._create_header()

        # 메인 컨텐츠 영역
        main_container = tk.Frame(self, bg="#ecf0f1")
        main_container.pack(fill="both", expand=True)

        # 좌측: 카메라 뷰 + 제어
        left_panel = tk.Frame(main_container, bg="#ecf0f1")
        left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self._create_camera_section(left_panel)
        self._create_control_buttons(left_panel)

        # 우측: 센서 상태 + Zone 관리
        right_panel = tk.Frame(main_container, bg="#ecf0f1", width=500)
        right_panel.pack(side="right", fill="both", padx=10, pady=10)
        right_panel.pack_propagate(False)

        self._create_sensor_section(right_panel)
        self._create_zone_section(right_panel)
        self._create_quick_actions(right_panel)

    def _create_header(self):
        """상단 헤더 바"""
        header = tk.Frame(self, bg="#34495e", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        # 좌측: 타이틀
        title_frame = tk.Frame(header, bg="#34495e")
        title_frame.pack(side="left", padx=20, pady=10)

        tk.Label(
            title_frame,
            text="🏠 SafeHome Dashboard",
            font=("Arial", 22, "bold"),
            bg="#34495e",
            fg="white"
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="Security Monitoring System",
            font=("Arial", 11),
            bg="#34495e",
            fg="#bdc3c7"
        ).pack(anchor="w")

        # 중앙: 시스템 상태
        status_frame = tk.Frame(header, bg="#34495e")
        status_frame.pack(side="left", expand=True)

        self.mode_label = tk.Label(
            status_frame,
            text=f"Mode: {self.system.config.current_mode.name}",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="#3498db"
        )
        self.mode_label.pack()

        self.status_indicator = tk.Label(
            status_frame,
            text="● SYSTEM RUNNING",
            font=("Arial", 12),
            bg="#34495e",
            fg="#2ecc71"
        )
        self.status_indicator.pack()

        # 우측: 액션 버튼
        button_frame = tk.Frame(header, bg="#34495e")
        button_frame.pack(side="right", padx=20)

        tk.Button(
            button_frame,
            text="📊 LOGS",
            command=self._open_log_viewer,
            bg="#f39c12",
            fg="black",
            font=("Helvetica", 12, "bold"),
            width=10,
            relief="groove",
            bd=3,
            cursor="hand2",
            activebackground="#e67e22",
            activeforeground="black"
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="🚪 LOGOUT",
            command=self._logout,
            bg="#e74c3c",
            fg="black",
            font=("Helvetica", 12, "bold"),
            width=10,
            relief="groove",
            bd=3,
            cursor="hand2",
            activebackground="#c0392b",
            activeforeground="black"
        ).pack(side="left", padx=5)

    def _create_camera_section(self, parent):
        """카메라 뷰 섹션"""
        camera_frame = tk.LabelFrame(
            parent,
            text="📹 Live Camera Feeds",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        camera_frame.pack(fill="both", expand=True, pady=(0, 10))

        # 카메라 그리드 컨테이너
        grid_container = tk.Frame(camera_frame, bg="white")
        grid_container.pack(fill="both", expand=True, padx=10, pady=10)

        # 3개 카메라를 위한 컬럼 가중치 설정
        grid_container.grid_columnconfigure(0, weight=1)
        grid_container.grid_columnconfigure(1, weight=1)
        grid_container.grid_columnconfigure(2, weight=1)
        grid_container.grid_rowconfigure(0, weight=1)

        self.camera_labels = {}
        cameras = list(self.system.camera_controller.cameras.values())

        if not cameras:
            tk.Label(
                grid_container,
                text="No cameras available",
                font=("Arial", 14),
                bg="white",
                fg="#95a5a6"
            ).pack(expand=True)
            return

        # 카메라 그리드 (3개 고정 - 1행 3열 레이아웃)
        # Dining Room, Kitchen, Living Room 순서로 표시
        for i, camera in enumerate(cameras[:3]):
            col = i

            cam_container = tk.Frame(grid_container, bg="#ecf0f1", relief="solid", borderwidth=2)
            cam_container.grid(row=0, column=col, padx=8, pady=8, sticky="nsew")

            # 카메라 제목
            title_frame = tk.Frame(cam_container, bg="#34495e")
            title_frame.pack(fill="x")

            tk.Label(
                title_frame,
                text=f"📷 {camera.name}",
                font=("Arial", 11, "bold"),
                bg="#34495e",
                fg="white"
            ).pack(side="left", padx=10, pady=5)

            tk.Label(
                title_frame,
                text=camera.location,
                font=("Arial", 9),
                bg="#34495e",
                fg="#bdc3c7"
            ).pack(side="left")

            # 카메라 이미지
            img_label = tk.Label(cam_container, bg="black")
            img_label.pack(padx=5, pady=5, fill="both", expand=True)
            self.camera_labels[camera.camera_id] = img_label

            # PTZ 제어 버튼
            control_frame = tk.Frame(cam_container, bg="#ecf0f1")
            control_frame.pack(fill="x", padx=5, pady=5)
            control_frame.grid_columnconfigure((0, 1, 2), weight=1)

            # Cross-key layout
            tk.Button(control_frame, text="^", command=lambda c=camera: self._tilt_camera(c, "up")).grid(row=0, column=1, sticky="ew")
            tk.Button(control_frame, text="<", command=lambda c=camera: self._pan_camera(c, "left")).grid(row=1, column=0, sticky="ew")
            tk.Button(control_frame, text=">", command=lambda c=camera: self._pan_camera(c, "right")).grid(row=1, column=2, sticky="ew")
            tk.Button(control_frame, text="v", command=lambda c=camera: self._tilt_camera(c, "down")).grid(row=2, column=1, sticky="ew")
            
            # Zoom buttons
            tk.Button(control_frame, text="+", command=lambda c=camera: self._zoom_camera(c, "in")).grid(row=0, column=2, sticky="ew")
            tk.Button(control_frame, text="-", command=lambda c=camera: self._zoom_camera(c, "out")).grid(row=2, column=0, sticky="ew")

    def _create_control_buttons(self, parent):
        """Arm/Disarm 제어 버튼 및 센서 시뮬레이터"""
        control_frame = tk.LabelFrame(
            parent,
            text="🎛️ System Control",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        control_frame.pack(fill="x", pady=(0, 10))

        button_container = tk.Frame(control_frame, bg="white")
        button_container.pack(padx=15, pady=15)

        modes = [
            ("🏠 Home", SafeHomeMode.HOME, "#3498db"),
            ("🚗 Away", SafeHomeMode.AWAY, "#9b59b6"),
            ("🌙 Overnight", SafeHomeMode.OVERNIGHT, "#34495e"),
            ("✈️ Extended", SafeHomeMode.EXTENDED, "#16a085"),
            ("🔓 Disarm", SafeHomeMode.DISARMED, "#e74c3c")
        ]

        for text, mode, color in modes:
            btn = tk.Button(
                button_container,
                text=text,
                bg=color,
                fg="black",  # 검은색으로 변경 (최대 가독성)
                font=("Helvetica", 12, "bold"),
                width=14,
                height=2,
                relief="groove",
                bd=3,
                cursor="hand2",
                activebackground=color,
                activeforeground="black",
                command=lambda m=mode: self._set_mode(m)
            )
            btn.pack(side="left", padx=5)

        # 센서 시뮬레이터 버튼 추가
        simulator_container = tk.Frame(control_frame, bg="white")
        simulator_container.pack(padx=15, pady=(0, 15))

        tk.Button(
            simulator_container,
            text="🧪 OPEN SENSOR SIMULATOR",
            bg="#f39c12",
            fg="black",
            font=("Helvetica", 13, "bold"),
            width=30,
            height=2,
            relief="groove",
            bd=4,
            cursor="hand2",
            activebackground="#e67e22",
            activeforeground="black",
            command=self._open_sensor_simulator
        ).pack()

    def _create_sensor_section(self, parent):
        """센서 상태 섹션"""
        sensor_frame = tk.LabelFrame(
            parent,
            text="🔍 Sensor Status",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        sensor_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Treeview
        tree_frame = tk.Frame(sensor_frame, bg="white")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("Type", "Location", "Zone", "Status")
        self.sensor_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=12
        )

        # 컬럼 설정
        column_widths = {"Type": 80, "Location": 150, "Zone": 80, "Status": 100}
        for col in columns:
            self.sensor_tree.heading(col, text=col)
            self.sensor_tree.column(col, width=column_widths[col], anchor="center")

        self.sensor_tree.pack(side="left", fill="both", expand=True)

        # 스크롤바
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.sensor_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.sensor_tree.configure(yscrollcommand=scrollbar.set)

        # 스타일 설정
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

    def _create_zone_section(self, parent):
        """Zone 관리 섹션"""
        zone_frame = tk.LabelFrame(
            parent,
            text="📍 Safety Zones",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        zone_frame.pack(fill="x", pady=(0, 10))

        content = tk.Frame(zone_frame, bg="white")
        content.pack(padx=10, pady=10, fill="x")

        self.zone_listbox = tk.Listbox(
            content,
            height=4,
            font=("Arial", 10),
            relief="solid",
            borderwidth=1
        )
        self.zone_listbox.pack(fill="x", pady=(0, 10))

        # Zone 버튼
        btn_frame = tk.Frame(content, bg="white")
        btn_frame.pack(fill="x")

        tk.Button(
            btn_frame,
            text="🗺️ MANAGE ZONES",
            command=self._open_zone_manager,
            bg="#48c9b0",
            fg="black",
            font=("Helvetica", 11, "bold"),
            relief="groove",
            bd=3,
            height=2,
            cursor="hand2",
            activebackground="#16a085",
            activeforeground="black"
        ).pack(fill="x")

    def _create_quick_actions(self, parent):
        """빠른 액션 버튼"""
        action_frame = tk.LabelFrame(
            parent,
            text="⚡ Quick Actions",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        action_frame.pack(fill="x")

        content = tk.Frame(action_frame, bg="white")
        content.pack(padx=10, pady=10, fill="x")

        actions = [
            ("🚨 Panic Alarm", self._trigger_panic, "#c0392b"),
            ("🔕 Silence Alarm", self._silence_alarm, "#7f8c8d"),
        ]

        for text, command, color in actions:
            # 더 밝은 배경색으로 변경
            if "Panic" in text:
                bg_color = "#e74c3c"  # 빨간색
            else:
                bg_color = "#95a5a6"  # 회색

            tk.Button(
                content,
                text=text.upper(),  # 대문자로 표시
                command=command,
                bg=bg_color,
                fg="black",  # 검은색 텍스트
                font=("Helvetica", 11, "bold"),
                height=2,
                relief="groove",
                bd=3,
                cursor="hand2",
                activebackground=color,
                activeforeground="black"
            ).pack(fill="x", pady=5)

    def _update_loop(self):
        """주기적 UI 업데이트"""
        try:
            # 카메라 이미지 업데이트
            self._update_cameras()

            # 센서 상태 업데이트
            self._update_sensors()

            # Zone 목록 업데이트
            self._update_zones()

            # 헤더 업데이트
            self._update_header()

        except Exception as e:
            print(f"Update error: {e}")

        # 500ms 후 재실행
        self.after(500, self._update_loop)

    def _update_cameras(self):
        """카메라 이미지 갱신"""
        for cam_id, label in self.camera_labels.items():
            try:
                img = self.system.camera_controller.get_camera_view(cam_id)
                if img:
                    # 리사이즈
                    img_resized = img.resize((400, 300), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img_resized)
                    label.config(image=photo)
                    label.image = photo
            except Exception as e:
                label.config(text=f"Camera Error\n{str(e)[:30]}", fg="red")

    def _update_sensors(self):
        """센서 리스트 갱신"""
        self.sensor_tree.delete(*self.sensor_tree.get_children())

        for sensor in self.system.sensor_controller.get_all_sensors():
            status = "🟢 Armed" if sensor.is_active else "⚪ Disarmed"
            zone_name = f"Zone {sensor.zone_id}" if sensor.zone_id else "-"

            self.sensor_tree.insert("", "end", values=(
                sensor.sensor_type,
                sensor.location,
                zone_name,
                status
            ))

    def _update_zones(self):
        """Zone 목록 갱신"""
        self.zone_listbox.delete(0, tk.END)

        for zone in self.system.config.get_all_zones():
            sensors = self.system.sensor_controller.get_sensors_by_zone(zone.zone_id)
            status = "🟢" if zone.is_armed else "⚪"
            self.zone_listbox.insert(
                tk.END,
                f"{status} {zone.name} ({len(sensors)} sensors)"
            )

    def _update_header(self):
        """헤더 상태 갱신"""
        self.mode_label.config(text=f"Mode: {self.system.config.current_mode.name}")

        if self.system.is_running:
            self.status_indicator.config(
                text="● SYSTEM RUNNING",
                fg="#2ecc71"
            )
        else:
            self.status_indicator.config(
                text="○ SYSTEM STOPPED",
                fg="#e74c3c"
            )

    def _set_mode(self, mode):
        """모드 설정"""
        if mode == SafeHomeMode.DISARMED:
            self.system.disarm_system()
            messagebox.showinfo("Success", "System Disarmed")
        else:
            success = self.system.arm_system(mode)
            if success:
                messagebox.showinfo("Success", f"System Armed in {mode.name} mode")
            else:
                messagebox.showwarning(
                    "Cannot Arm",
                    "Cannot arm system!\nSome windows/doors are open."
                )

    def _pan_camera(self, camera, direction):
        """카메라 패닝"""
        self.system.camera_controller.pan_camera(camera.camera_id, direction)

    def _tilt_camera(self, camera, direction):
        """카메라 틸팅"""
        self.system.camera_controller.tilt_camera(camera.camera_id, direction)

    def _zoom_camera(self, camera, direction):
        """카메라 줌"""
        self.system.camera_controller.zoom_camera(camera.camera_id, direction)

    def _open_zone_manager(self):
        """Zone 관리자 열기"""
        from .zone_manager import ZoneManagerWindow
        ZoneManagerWindow(self.system, self)

    def _open_log_viewer(self):
        """로그 뷰어 열기"""
        from .log_viewer import LogViewerWindow
        LogViewerWindow(self.system, self)

    def _trigger_panic(self):
        """패닉 알람"""
        if messagebox.askyesno("Panic Alarm", "Trigger panic alarm?"):
            self.system.config.set_mode(SafeHomeMode.PANIC)
            self.system.alarm.ring()
            messagebox.showwarning("Panic Alarm", "🚨 PANIC ALARM ACTIVATED!")

    def _silence_alarm(self):
        """알람 끄기"""
        self.system.alarm.stop()
        messagebox.showinfo("Alarm", "Alarm silenced")

    def _open_sensor_simulator(self):
        """센서 시뮬레이터 열기"""
        try:
            from safehome.device.sensor.device_sensor_tester import DeviceSensorTester
            DeviceSensorTester.showSensorTester()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Sensor Simulator: {e}")

    def _logout(self):
        """로그아웃"""
        if messagebox.askyesno("Logout", "Logout and return to login screen?"):
            self.destroy()
            self.login_window.deiconify()
            self.login_window.password_entry.delete(0, tk.END)
            self.login_window.password_entry.focus()

    def _on_close(self):
        """윈도우 종료"""
        if messagebox.askokcancel("Quit", "Shutdown SafeHome System?"):
            self.system.shutdown()
            self.login_window.destroy()

