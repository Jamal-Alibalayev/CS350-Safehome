"""
SafeHome Zone Manager Window
Manage safety zones and sensor assignments
"""

import tkinter as tk
from tkinter import ttk, messagebox


class ZoneManagerWindow(tk.Toplevel):
    """
    Safety Zone 관리 창
    - Zone 추가/수정/삭제
    - Sensor 할당 관리
    - Zone별 센서 목록 표시
    """

    def __init__(self, system, parent):
        super().__init__(parent)
        self.system = system
        self.parent = parent

        # 윈도우 설정
        self.title("SafeHome - Zone Manager")
        self.geometry("900x600")
        self.resizable(True, True)

        # 중앙 배치
        self._center_window()

        # 선택된 zone
        self.selected_zone_id = None

        # UI 구성
        self._create_ui()

        # 초기 데이터 로드
        self._refresh_zones()

    def _center_window(self):
        """윈도우를 화면 중앙에 배치"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _create_ui(self):
        """UI 구성"""
        # 상단 헤더
        header_frame = tk.Frame(self, bg="#34495e", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🗺️ Safety Zone Manager",
            font=("Arial", 18, "bold"),
            bg="#34495e",
            fg="white"
        )
        title_label.pack(pady=15)

        # 메인 컨텐츠
        content_frame = tk.Frame(self, bg="#ecf0f1")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 좌측: Zone 목록
        left_frame = tk.Frame(content_frame, bg="#ecf0f1")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        zones_label = tk.Label(
            left_frame,
            text="Safety Zones",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        zones_label.pack(anchor="w", pady=(0, 10))

        # Zone 목록 (Treeview)
        tree_frame = tk.Frame(left_frame, bg="white", relief="solid", borderwidth=1)
        tree_frame.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")

        # Treeview
        self.zone_tree = ttk.Treeview(
            tree_frame,
            columns=("Name", "Sensors", "Status"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.zone_tree.yview)

        self.zone_tree.heading("Name", text="Zone Name")
        self.zone_tree.heading("Sensors", text="Sensors")
        self.zone_tree.heading("Status", text="Status")

        self.zone_tree.column("Name", width=200)
        self.zone_tree.column("Sensors", width=100)
        self.zone_tree.column("Status", width=100)

        self.zone_tree.pack(fill="both", expand=True)

        # Zone 선택 이벤트
        self.zone_tree.bind("<<TreeviewSelect>>", self._on_zone_select)

        # Zone 관리 버튼
        btn_frame = tk.Frame(left_frame, bg="#ecf0f1")
        btn_frame.pack(fill="x", pady=(10, 0))

        add_btn = tk.Button(
            btn_frame,
            text="➕ Add Zone",
            font=("Arial", 11),
            bg="#27ae60",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self._add_zone
        )
        add_btn.pack(side="left", padx=(0, 5))

        edit_btn = tk.Button(
            btn_frame,
            text="✏️ Edit Zone",
            font=("Arial", 11),
            bg="#3498db",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self._edit_zone
        )
        edit_btn.pack(side="left", padx=5)

        delete_btn = tk.Button(
            btn_frame,
            text="🗑️ Delete Zone",
            font=("Arial", 11),
            bg="#e74c3c",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self._delete_zone
        )
        delete_btn.pack(side="left", padx=5)

        # 우측: Zone 세부정보 및 센서 할당
        right_frame = tk.Frame(content_frame, bg="#ecf0f1")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        detail_label = tk.Label(
            right_frame,
            text="Zone Details",
            font=("Arial", 14, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        detail_label.pack(anchor="w", pady=(0, 10))

        # Zone 정보 표시
        info_frame = tk.Frame(right_frame, bg="white", relief="solid", borderwidth=1)
        info_frame.pack(fill="x", pady=(0, 15))

        self.zone_name_label = tk.Label(
            info_frame,
            text="Select a zone to view details",
            font=("Arial", 12),
            bg="white",
            fg="#7f8c8d",
            anchor="w"
        )
        self.zone_name_label.pack(fill="x", padx=15, pady=15)

        # 센서 목록
        sensors_label = tk.Label(
            right_frame,
            text="Sensors in this Zone",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        sensors_label.pack(anchor="w", pady=(0, 10))

        sensor_tree_frame = tk.Frame(right_frame, bg="white", relief="solid", borderwidth=1)
        sensor_tree_frame.pack(fill="both", expand=True)

        # Sensor Treeview
        sensor_scrollbar = ttk.Scrollbar(sensor_tree_frame)
        sensor_scrollbar.pack(side="right", fill="y")

        self.sensor_tree = ttk.Treeview(
            sensor_tree_frame,
            columns=("Type", "Name", "Status"),
            show="headings",
            yscrollcommand=sensor_scrollbar.set
        )
        sensor_scrollbar.config(command=self.sensor_tree.yview)

        self.sensor_tree.heading("Type", text="Type")
        self.sensor_tree.heading("Name", text="Name")
        self.sensor_tree.heading("Status", text="Status")

        self.sensor_tree.column("Type", width=100)
        self.sensor_tree.column("Name", width=150)
        self.sensor_tree.column("Status", width=100)

        self.sensor_tree.pack(fill="both", expand=True)

        # 센서 할당 버튼
        assign_btn_frame = tk.Frame(right_frame, bg="#ecf0f1")
        assign_btn_frame.pack(fill="x", pady=(10, 0))

        assign_btn = tk.Button(
            assign_btn_frame,
            text="📍 Assign Sensors",
            font=("Arial", 11),
            bg="#9b59b6",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self._assign_sensors
        )
        assign_btn.pack(side="left")

    def _refresh_zones(self):
        """Zone 목록 새로고침"""
        # Clear existing items
        for item in self.zone_tree.get_children():
            self.zone_tree.delete(item)

        # Get all zones
        zones = self.system.config.get_all_zones()

        for zone in zones:
            # Count sensors in this zone
            sensor_count = sum(
                1 for sensor in self.system.sensor_controller.sensors.values()
                if sensor.zone_id == zone.zone_id
            )

            # Determine status
            status = "Active" if zone.is_armed else "Inactive"

            # Insert into tree
            self.zone_tree.insert(
                "",
                "end",
                iid=str(zone.zone_id),
                values=(zone.name, sensor_count, status)
            )

    def _on_zone_select(self, event):
        """Zone 선택 이벤트 핸들러"""
        selection = self.zone_tree.selection()
        if not selection:
            return

        zone_id = int(selection[0])
        self.selected_zone_id = zone_id

        # Get zone info
        zone = self.system.config.get_safety_zone(zone_id)
        if not zone:
            return

        # Update zone info display
        self.zone_name_label.config(
            text=f"Zone: {zone.name} (ID: {zone.zone_id})\n"
                 f"Status: {'Armed' if zone.is_armed else 'Disarmed'}"
        )

        # Update sensor list for this zone
        self._refresh_zone_sensors(zone_id)

    def _refresh_zone_sensors(self, zone_id):
        """특정 Zone의 센서 목록 새로고침"""
        # Clear existing items
        for item in self.sensor_tree.get_children():
            self.sensor_tree.delete(item)

        # Get sensors in this zone
        for sensor in self.system.sensor_controller.sensors.values():
            if sensor.zone_id == zone_id:
                sensor_type = "Motion" if sensor.sensor_type == "MOTION" else "Door/Window"
                status = "Active" if sensor.get_status() else "Inactive"

                self.sensor_tree.insert(
                    "",
                    "end",
                    values=(sensor_type, sensor.location, status)
                )

    def _add_zone(self):
        """새 Zone 추가"""
        dialog = AddZoneDialog(self, self.system)
        self.wait_window(dialog)

        if dialog.result:
            self._refresh_zones()

    def _edit_zone(self):
        """Zone 편집"""
        if not self.selected_zone_id:
            messagebox.showwarning("No Selection", "Please select a zone to edit")
            return

        zone = self.system.config.get_safety_zone(self.selected_zone_id)
        if not zone:
            return

        dialog = EditZoneDialog(self, self.system, zone)
        self.wait_window(dialog)

        if dialog.result:
            self._refresh_zones()

    def _delete_zone(self):
        """Zone 삭제"""
        if not self.selected_zone_id:
            messagebox.showwarning("No Selection", "Please select a zone to delete")
            return

        zone = self.system.config.get_safety_zone(self.selected_zone_id)
        if not zone:
            return

        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete zone '{zone.name}'?\n"
            f"All sensors in this zone will be unassigned."
        )

        if confirm:
            # Unassign all sensors in this zone
            for sensor in self.system.sensor_controller.sensors.values():
                if sensor.zone_id == self.selected_zone_id:
                    sensor.zone_id = None

            # Delete zone
            success = self.system.config.delete_safety_zone(self.selected_zone_id)

            if success:
                messagebox.showinfo("Success", f"Zone '{zone.name}' deleted successfully")
                self.selected_zone_id = None
                self.zone_name_label.config(text="Select a zone to view details")
                self._refresh_zones()
            else:
                messagebox.showerror("Error", "Failed to delete zone")

    def _assign_sensors(self):
        """센서를 Zone에 할당"""
        if not self.selected_zone_id:
            messagebox.showwarning("No Selection", "Please select a zone first")
            return

        zone = self.system.config.get_safety_zone(self.selected_zone_id)
        if not zone:
            return

        dialog = AssignSensorDialog(self, self.system, zone)
        self.wait_window(dialog)

        if dialog.result:
            self._refresh_zones()
            self._refresh_zone_sensors(self.selected_zone_id)


class AddZoneDialog(tk.Toplevel):
    """새 Zone 추가 다이얼로그"""

    def __init__(self, parent, system):
        super().__init__(parent)
        self.system = system
        self.result = False

        self.title("Add New Zone")
        self.geometry("400x200")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self._create_ui()

    def _create_ui(self):
        # Zone name input
        tk.Label(
            self,
            text="Zone Name:",
            font=("Arial", 12)
        ).pack(pady=(20, 5))

        self.name_entry = tk.Entry(
            self,
            font=("Arial", 12),
            width=30
        )
        self.name_entry.pack(pady=5)
        self.name_entry.focus()

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=30)

        tk.Button(
            btn_frame,
            text="Create",
            font=("Arial", 11),
            bg="#27ae60",
            fg="white",
            width=10,
            command=self._create_zone
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Cancel",
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            width=10,
            command=self.destroy
        ).pack(side="left", padx=5)

    def _create_zone(self):
        name = self.name_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Zone name cannot be empty")
            return

        # Create zone
        zone = self.system.config.add_safety_zone(name)

        if zone:
            messagebox.showinfo("Success", f"Zone '{name}' created successfully")
            self.result = True
            self.destroy()
        else:
            messagebox.showerror("Error", "Failed to create zone")


class EditZoneDialog(tk.Toplevel):
    """Zone 편집 다이얼로그"""

    def __init__(self, parent, system, zone):
        super().__init__(parent)
        self.system = system
        self.zone = zone
        self.result = False

        self.title("Edit Zone")
        self.geometry("400x200")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self._create_ui()

    def _create_ui(self):
        # Zone name input
        tk.Label(
            self,
            text="Zone Name:",
            font=("Arial", 12)
        ).pack(pady=(20, 5))

        self.name_entry = tk.Entry(
            self,
            font=("Arial", 12),
            width=30
        )
        self.name_entry.insert(0, self.zone.name)
        self.name_entry.pack(pady=5)
        self.name_entry.focus()

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=30)

        tk.Button(
            btn_frame,
            text="Save",
            font=("Arial", 11),
            bg="#3498db",
            fg="white",
            width=10,
            command=self._save_zone
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Cancel",
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            width=10,
            command=self.destroy
        ).pack(side="left", padx=5)

    def _save_zone(self):
        new_name = self.name_entry.get().strip()

        if not new_name:
            messagebox.showerror("Error", "Zone name cannot be empty")
            return

        # Update zone name
        success = self.system.config.update_safety_zone(self.zone.zone_id, zone_name=new_name)

        if success:
            messagebox.showinfo("Success", "Zone updated successfully")
            self.result = True
            self.destroy()
        else:
            messagebox.showerror("Error", f"Failed to update zone '{self.zone.name}'")


class AssignSensorDialog(tk.Toplevel):
    """센서 할당 다이얼로그"""

    def __init__(self, parent, system, zone):
        super().__init__(parent)
        self.system = system
        self.zone = zone
        self.result = False

        self.title(f"Assign Sensors - {zone.name}")
        self.geometry("500x400")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self._create_ui()

    def _create_ui(self):
        # Header
        tk.Label(
            self,
            text=f"Select sensors to assign to '{self.zone.name}'",
            font=("Arial", 12, "bold")
        ).pack(pady=15)

        # Sensor listbox with checkboxes
        listbox_frame = tk.Frame(self)
        listbox_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side="right", fill="y")

        self.sensor_listbox = tk.Listbox(
            listbox_frame,
            font=("Arial", 11),
            selectmode="multiple",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.sensor_listbox.yview)
        self.sensor_listbox.pack(fill="both", expand=True)

        # Populate with all sensors
        self.sensor_ids = []
        for sensor_id, sensor in self.system.sensor_controller.sensors.items():
            self.sensor_ids.append(sensor_id)
            sensor_type = "Motion" if sensor.sensor_type == "MOTION" else "Door/Window"
            zone_info = f"(Zone: {self.system.config.get_safety_zone(sensor.zone_id).name})" if sensor.zone_id else "(Unassigned)"

            self.sensor_listbox.insert("end", f"{sensor.location} - {sensor_type} {zone_info}")

            # Pre-select sensors already in this zone
            if sensor.zone_id == self.zone.zone_id:
                self.sensor_listbox.selection_set(len(self.sensor_ids) - 1)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame,
            text="Assign",
            font=("Arial", 11),
            bg="#9b59b6",
            fg="white",
            width=10,
            command=self._assign
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Cancel",
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            width=10,
            command=self.destroy
        ).pack(side="left", padx=5)

    def _assign(self):
        # Get selected sensors
        selected_indices = self.sensor_listbox.curselection()

        # First, unassign all sensors currently in this zone
        for sensor in self.system.sensor_controller.sensors.values():
            if sensor.zone_id == self.zone.zone_id:
                sensor.zone_id = None

        # Assign selected sensors to this zone
        for index in selected_indices:
            sensor_id = self.sensor_ids[index]
            sensor = self.system.sensor_controller.sensors[sensor_id]
            sensor.zone_id = self.zone.zone_id

        # Save configuration
        self.system.config.save_configuration()

        messagebox.showinfo("Success", f"Sensors assigned to '{self.zone.name}' successfully")
        self.result = True
        self.destroy()
