"""
SafeHome Login Window
Initial entry point for the application
"""

import tkinter as tk
from tkinter import ttk


class LoginWindow(tk.Tk):
    """
    SafeHome 로그인 화면
    - 애플리케이션 시작점
    - 패스워드 인증 후 Dashboard로 전환
    """

    def __init__(self, system):
        super().__init__()
        self.system = system

        # 윈도우 설정
        self.title("SafeHome Security System - Login")
        self.geometry("600x450")
        self.resizable(False, False)

        # 중앙 배치
        self._center_window()

        # UI 구성
        self._create_ui()

    def _center_window(self):
        """윈도우를 화면 중앙에 배치"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _create_ui(self):
        # 상단 헤더
        header_frame = tk.Frame(self, bg="#2c3e50", height=100)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🏠 SafeHome",
            font=("Arial", 28, "bold"),
            bg="#2c3e50",
            fg="white",
        )
        title_label.pack(pady=10)

        subtitle_label = tk.Label(
            header_frame,
            text="Security System",
            font=("Arial", 14),
            bg="#2c3e50",
            fg="#ecf0f1",
        )
        subtitle_label.pack()

        # 메인 컨텐츠
        content_frame = tk.Frame(self, bg="white")
        content_frame.pack(fill="both", expand=True)

        # 로그인 폼 (중앙 배치)
        form_frame = tk.Frame(content_frame, bg="white")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        # 환영 메시지
        welcome_label = tk.Label(
            form_frame,
            text="Welcome Back",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#2c3e50",
        )
        welcome_label.grid(row=0, column=0, columnspan=2, pady=(0, 30))

        # 사용자 선택
        user_label = tk.Label(
            form_frame, text="User:", font=("Arial", 12), bg="white", fg="#34495e"
        )
        user_label.grid(row=1, column=0, pady=15, sticky="e", padx=(0, 10))

        self.user_combo = ttk.Combobox(
            form_frame,
            values=["Admin", "Guest"],
            state="readonly",
            width=22,
            font=("Arial", 11),
        )
        self.user_combo.set("Admin")
        self.user_combo.grid(row=1, column=1, pady=15)

        # 패스워드 입력
        password_label = tk.Label(
            form_frame, text="Password:", font=("Arial", 12), bg="white", fg="#34495e"
        )
        password_label.grid(row=2, column=0, pady=15, sticky="e", padx=(0, 10))

        self.password_entry = tk.Entry(
            form_frame,
            show="●",
            font=("Arial", 12),
            width=24,
            relief="solid",
            borderwidth=1,
        )
        self.password_entry.grid(row=2, column=1, pady=15)
        self.password_entry.bind("<Return>", lambda e: self._attempt_login())
        self.password_entry.focus()

        # 로그인 버튼
        login_btn = tk.Button(
            form_frame,
            text="Login",
            font=("Arial", 13, "bold"),
            bg="#e0f4e0",
            fg="black",
            activebackground="#c2e6c2",
            activeforeground="black",
            width=20,
            height=2,
            relief="ridge",
            bd=2,
            cursor="hand2",
            command=self._attempt_login,
        )
        login_btn.grid(row=3, column=0, columnspan=2, pady=30)

        # 상태 메시지
        self.status_label = tk.Label(
            form_frame, text="", font=("Arial", 10), bg="white", fg="#e74c3c"
        )
        self.status_label.grid(row=4, column=0, columnspan=2)

        # 하단 정보
        info_frame = tk.Frame(self, bg="#ecf0f1", height=40)
        info_frame.pack(side="bottom", fill="x")

        info_label = tk.Label(
            info_frame,
            text=f"System Status: {'🟢 Running' if self.system.is_running else '⚪ Stopped'} | "
            f"Mode: {self.system.config.current_mode.name}",
            font=("Arial", 9),
            bg="#ecf0f1",
            fg="#7f8c8d",
        )
        info_label.pack(pady=10)

    def _attempt_login(self):
        """로그인 시도"""
        user_id = "admin" if self.user_combo.get() == "Admin" else "guest"
        password = self.password_entry.get()

        if not password:
            self.status_label.config(text="⚠️ Please enter password")
            return

        # 시스템 로그인 시도
        success = self.system.login(user_id, password, "CONTROL_PANEL")

        if success:
            # 로그인 성공
            self.withdraw()  # 로그인 창 숨김
            self._open_dashboard(user_id)
        else:
            # 로그인 실패
            locked = self.system.config.login_manager.is_locked.get(
                "CONTROL_PANEL", False
            )

            if locked:
                self.status_label.config(text="🔒 System locked - Too many attempts")
            else:
                self.status_label.config(text="❌ Invalid password - Please try again")

            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()

    def _open_dashboard(self, user_id: str):
        """Dashboard 열기"""
        from .main_dashboard import MainDashboard

        dashboard = MainDashboard(self.system, self, user_id)
