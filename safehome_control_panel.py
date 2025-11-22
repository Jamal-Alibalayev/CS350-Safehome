# safehome/interfaces/control_panel/safehome_control_panel.py

from configuration.configuration_manager import ConfigurationManager
from configuration.safehome_mode import SafeHomeMode
from virtual_device_v3.virtual_device_v3.device.device_control_panel_abstract import DeviceControlPanelAbstract

class SafeHomeControlPanel(DeviceControlPanelAbstract):
    """
    SafeHome 控制面板的具体实现。
    连接 GUI 按钮事件与 ConfigurationManager 的业务逻辑。
    """

    def __init__(self, master=None, config_manager: ConfigurationManager = None):
        super().__init__(master)
        
        # 注入配置管理器
        self.config_manager = config_manager if config_manager else ConfigurationManager()
        
        # 内部状态
        self.input_buffer = ""
        self.is_authenticated = False
        
        # 初始化界面状态
        self._refresh_status_display()
        self._reset_interaction()

    def _refresh_status_display(self):
        """根据 ConfigurationManager 的状态刷新 LED 和 LCD"""
        mode = self.config_manager.get_mode()
        
        # 1. 更新 LED 状态
        is_armed = mode in [SafeHomeMode.ARMED_AWAY, SafeHomeMode.ARMED_STAY]
        self.set_armed_led(is_armed)
        self.set_powered_led(True)  # 假设电源始终正常
        
        # 2. 更新 LCD 状态文字 (Away / Stay / Not Ready)
        self.set_display_away(mode == SafeHomeMode.ARMED_AWAY)
        self.set_display_stay(mode == SafeHomeMode.ARMED_STAY)
        
        # 如果是撤防状态，显示 Not Ready (或 Ready，这里简化处理)
        if mode == SafeHomeMode.DISARMED:
            self.set_display_not_ready(True)
        else:
            self.set_display_not_ready(False)

    def _reset_interaction(self):
        """重置交互状态"""
        self.input_buffer = ""
        self.is_authenticated = False
        self.set_display_short_message1("Welcome SafeHome")
        self.set_display_short_message2("Enter Code + #")

    def _handle_key_input(self, key):
        """处理数字键输入"""
        if self.is_authenticated:
            # 已登录状态：数字键代表指令
            self._handle_command(key)
        else:
            # 未登录状态：数字键代表密码
            self.input_buffer += key
            # 屏幕显示掩码 (****)
            mask = "*" * len(self.input_buffer)
            self.set_display_short_message2(f"Code: {mask}")

    def _handle_command(self, key):
        """处理指令 (仅在登录后有效)"""
        msg = ""
        success = False
        
        if key == "1":   # 1 = 外出布防
            self.config_manager.set_mode(SafeHomeMode.ARMED_AWAY)
            msg = "ARMED (AWAY)"
            success = True
        elif key == "2": # 2 = 在家布防
            self.config_manager.set_mode(SafeHomeMode.ARMED_STAY)
            msg = "ARMED (STAY)"
            success = True
        elif key == "0": # 0 = 撤防
            self.config_manager.set_mode(SafeHomeMode.DISARMED)
            msg = "DISARMED"
            success = True
        else:
            msg = "Invalid Cmd"
        
        self.set_display_short_message1(msg)
        
        if success:
            self.set_display_short_message2("Session Ended")
            self._refresh_status_display()
            # 操作完成后，为了安全，自动登出
            self.is_authenticated = False 
            self.input_buffer = ""
        else:
            self.set_display_short_message2("1:Away 2:Stay 0:Off")

    def _attempt_login(self):
        """验证密码"""
        if not self.input_buffer:
            return

        user_id = "admin" # 简化处理
        password = self.input_buffer
        
        # 调用 LoginManager 进行验证
        success = self.config_manager.login_manager.validate_credentials(user_id, password)
        
        if success:
            self.is_authenticated = True
            self.set_display_short_message1("Login Success")
            self.set_display_short_message2("1:Away 2:Stay 0:Off")
            self.input_buffer = "" 
        else:
            self.is_authenticated = False
            self.input_buffer = ""
            
            if self.config_manager.login_manager.is_locked:
                self.set_display_short_message1("SYSTEM LOCKED")
                self.set_display_short_message2("Too many attempts")
            else:
                self.set_display_short_message1("Login Failed")
                self.set_display_short_message2("Try Again")

    # --- 实现抽象基类的所有按钮方法 ---

    def button1(self): self._handle_key_input("1")
    def button2(self): self._handle_key_input("2")
    def button3(self): self._handle_key_input("3")
    def button4(self): self._handle_key_input("4")
    def button5(self): self._handle_key_input("5")
    def button6(self): self._handle_key_input("6")
    def button7(self): self._handle_key_input("7")
    def button8(self): self._handle_key_input("8")
    def button9(self): self._handle_key_input("9")
    def button0(self): self._handle_key_input("0")

    def button_star(self):
        """ * 键：取消/重置 """
        self._reset_interaction()

    def button_sharp(self):
        """ # 键：确认 """
        if not self.is_authenticated:
            self._attempt_login()

    def button_panic(self):
        """ 紧急按钮 (GUI上没有单独绑定，如果未来有可扩展) """
        self.config_manager.set_mode(SafeHomeMode.PANIC)
        self.set_display_short_message1("ALARM TRIGGERED!")
        self._refresh_status_display()