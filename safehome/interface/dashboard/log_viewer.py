"""
SafeHome Log Viewer Window
View system event logs and history
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime


class LogViewerWindow(tk.Toplevel):
    """
    시스템 로그 뷰어
    - 모든 이벤트 로그 표시
    - 필터링 기능 (타입, 날짜)
    - 로그 검색 기능
    - 자동 새로고침
    """

    def __init__(self, system, parent):
        super().__init__(parent)
        self.system = system
        self.parent = parent

        # 윈도우 설정
        self.title("SafeHome - Event Log Viewer")
        self.geometry("1000x600")
        self.resizable(True, True)

        # 중앙 배치
        self._center_window()

        # 필터 설정
        self.filter_type = "All"
        self.auto_refresh = True

        # UI 구성
        self._create_ui()

        # 초기 로그 로드
        self._refresh_logs()

        # 자동 새로고침 시작
        self._start_auto_refresh()

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
            text="📋 Event Log Viewer",
            font=("Arial", 18, "bold"),
            bg="#34495e",
            fg="white"
        )
        title_label.pack(pady=15)

        # 컨트롤 바
        control_frame = tk.Frame(self, bg="#ecf0f1", height=60)
        control_frame.pack(fill="x", padx=20, pady=(10, 0))
        control_frame.pack_propagate(False)

        # 필터 선택
        tk.Label(
            control_frame,
            text="Filter:",
            font=("Arial", 11),
            bg="#ecf0f1"
        ).pack(side="left", padx=(0, 5))

        self.filter_combo = ttk.Combobox(
            control_frame,
            values=["All", "SENSOR", "CAMERA", "SYSTEM", "AUTH", "ALARM"],
            state="readonly",
            width=15,
            font=("Arial", 10)
        )
        self.filter_combo.set("All")
        self.filter_combo.pack(side="left", padx=5)
        self.filter_combo.bind("<<ComboboxSelected>>", lambda e: self._refresh_logs())

        # 검색
        tk.Label(
            control_frame,
            text="Search:",
            font=("Arial", 11),
            bg="#ecf0f1"
        ).pack(side="left", padx=(20, 5))

        self.search_entry = tk.Entry(
            control_frame,
            font=("Arial", 10),
            width=25
        )
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self._refresh_logs())

        # 새로고침 버튼
        refresh_btn = tk.Button(
            control_frame,
            text="🔄 Refresh",
            font=("Arial", 10),
            bg="#e0e7ff",
            fg="black",
            relief="flat",
            cursor="hand2",
            activebackground="#cbd6ff",
            activeforeground="black",
            command=self._refresh_logs
        )
        refresh_btn.pack(side="left", padx=10)

        # 자동 새로고침 체크박스
        self.auto_refresh_var = tk.BooleanVar(value=True)
        auto_refresh_check = tk.Checkbutton(
            control_frame,
            text="Auto-refresh",
            variable=self.auto_refresh_var,
            font=("Arial", 10),
            bg="#ecf0f1",
            command=self._toggle_auto_refresh
        )
        auto_refresh_check.pack(side="left", padx=5)

        # Clear 버튼
        clear_btn = tk.Button(
            control_frame,
            text="🗑️ Clear Logs",
            font=("Arial", 10),
            bg="#ffe0e0",
            fg="black",
            relief="flat",
            cursor="hand2",
            activebackground="#ffc2c2",
            activeforeground="black",
            command=self._clear_logs
        )
        clear_btn.pack(side="right", padx=5)

        # 로그 테이블
        table_frame = tk.Frame(self, bg="white", relief="solid", borderwidth=1)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame)
        y_scrollbar.pack(side="right", fill="y")

        x_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
        x_scrollbar.pack(side="bottom", fill="x")

        # Treeview
        self.log_tree = ttk.Treeview(
            table_frame,
            columns=("Timestamp", "Type", "Source", "Message"),
            show="headings",
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set
        )
        y_scrollbar.config(command=self.log_tree.yview)
        x_scrollbar.config(command=self.log_tree.xview)

        self.log_tree.heading("Timestamp", text="Timestamp")
        self.log_tree.heading("Type", text="Type")
        self.log_tree.heading("Source", text="Source")
        self.log_tree.heading("Message", text="Message")

        self.log_tree.column("Timestamp", width=180)
        self.log_tree.column("Type", width=100)
        self.log_tree.column("Source", width=150)
        self.log_tree.column("Message", width=500)

        self.log_tree.pack(fill="both", expand=True)

        # 태그 색상 설정
        self.log_tree.tag_configure("SENSOR", foreground="#27ae60")
        self.log_tree.tag_configure("CAMERA", foreground="#3498db")
        self.log_tree.tag_configure("SYSTEM", foreground="#95a5a6")
        self.log_tree.tag_configure("AUTH", foreground="#9b59b6")
        self.log_tree.tag_configure("ALARM", foreground="#e74c3c")

        # 하단 상태바
        status_frame = tk.Frame(self, bg="#ecf0f1", height=30)
        status_frame.pack(fill="x")
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            font=("Arial", 9),
            bg="#ecf0f1",
            fg="#7f8c8d"
        )
        self.status_label.pack(side="left", padx=10)

    def _refresh_logs(self):
        """로그 목록 새로고침"""
        # Clear existing items
        for item in self.log_tree.get_children():
            self.log_tree.delete(item)

        # Get filter and search parameters
        filter_type = self.filter_combo.get()
        search_text = self.search_entry.get().lower()

        # Get logs from system
        cfg = self.system.config
        log_mgr = getattr(cfg, "log_manager", None) or getattr(cfg, "logger", None)
        logs = log_mgr.get_all_logs() if log_mgr else []

        # Apply filters
        filtered_logs = []
        for log in logs:
            # Type filter
            if filter_type != "All" and log.event_type != filter_type:
                continue

            # Search filter
            if search_text:
                searchable_text = f"{log.timestamp} {log.event_type} {log.source} {log.message}".lower()
                if search_text not in searchable_text:
                    continue

            filtered_logs.append(log)

        # Sort by timestamp (newest first)
        filtered_logs.sort(key=lambda x: x.timestamp, reverse=True)

        # Insert into tree
        for log in filtered_logs:
            # Format timestamp
            try:
                dt = datetime.fromisoformat(log.timestamp)
                formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                formatted_time = log.timestamp

            # Insert with tag for coloring
            self.log_tree.insert(
                "",
                "end",
                values=(formatted_time, log.event_type, log.source, log.message),
                tags=(log.event_type,)
            )

        # Update status
        total_logs = len(logs)
        shown_logs = len(filtered_logs)
        self.status_label.config(
            text=f"Showing {shown_logs} of {total_logs} logs | Last updated: {datetime.now().strftime('%H:%M:%S')}"
        )

    def _toggle_auto_refresh(self):
        """자동 새로고침 토글"""
        self.auto_refresh = self.auto_refresh_var.get()

    def _start_auto_refresh(self):
        """자동 새로고침 시작"""
        if self.auto_refresh:
            self._refresh_logs()

        # Schedule next refresh (every 2 seconds)
        self.after(2000, self._start_auto_refresh)

    def _clear_logs(self):
        """모든 로그 삭제"""
        from tkinter import messagebox

        confirm = messagebox.askyesno(
            "Confirm Clear",
            "Are you sure you want to clear all event logs?\nThis action cannot be undone."
        )

        if confirm:
            self.system.config.log_manager.clear_logs()
            self._refresh_logs()
            messagebox.showinfo("Success", "All logs cleared successfully")
