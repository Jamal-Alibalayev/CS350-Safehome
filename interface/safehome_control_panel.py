# safehome/interfaces/control_panel/safehome_control_panel.py

from safehome.configuration.configuration_manager import ConfigurationManager
from safehome.configuration.safehome_mode import SafeHomeMode
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
        
        # [新增] 修改密码模式的状态标志
        self.is_changing_password = False
        # [新增] 暂存当前登录成功的旧密码，用于授权修改
        self.current_valid_password = None 
        
        # 初始化界面状态
        self._refresh_status_display()
        self._reset_interaction()

    def _refresh_status_display(self):
        """根据 ConfigurationManager 的状态刷新 LED 和 LCD"""
        mode = self.config_manager.get_mode()
        
        # 1. 更新 LED 状态
        is_armed = mode in [SafeHomeMode.ARMED_AWAY, SafeHomeMode.ARMED_STAY]
        self.set_armed_led(is_armed)
        self.set_powered_led(True)
        
        # 2. 更新 LCD 状态文字
        self.set_display_away(mode == SafeHomeMode.ARMED_AWAY)
        self.set_display_stay(mode == SafeHomeMode.ARMED_STAY)
        
        if mode == SafeHomeMode.DISARMED:
            self.set_display_not_ready(True)
        else:
            self.set_display_not_ready(False)

        # [新增] 更新 Security Zone 显示
        current_zone = self.config_manager.get_current_zone()
        # 调用父类方法设置左上角的数字
        self.set_security_zone_number(current_zone.zone_id)

    def _reset_interaction(self):
        """重置交互状态"""
        self.input_buffer = ""
        self.is_authenticated = False
        self.is_changing_password = False # 重置修改模式
        self.current_valid_password = None
        
        self.set_display_short_message1("Welcome To SafeHome System(Testing)")
        self.set_display_short_message2("Enter Code + #")

    def _handle_key_input(self, key):
        """处理数字键输入"""
        # 场景 1: 正在修改密码模式下，输入的是新密码
        if self.is_changing_password:
            self.input_buffer += key
            mask = "*" * len(self.input_buffer)
            self.set_display_short_message2(f"New: {mask}")
            
        # 场景 2: 已登录，输入的是菜单指令
        elif self.is_authenticated:
            self._handle_command(key)
            
        # 场景 3: 未登录，输入的是登录密码
        else:
            self.input_buffer += key
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
        elif key == "3": # [新增] 3 = 修改密码
            self.is_changing_password = True
            self.input_buffer = "" # 清空缓存以输入新密码
            self.set_display_short_message1("CHANGE PASSWORD")
            self.set_display_short_message2("Enter New Password + #")
        elif key == "9": 
            new_zone = self.config_manager.next_zone()
            self.set_display_short_message1(f"Zone Changed:")
            self.set_display_short_message2(new_zone.name)
            self._refresh_status_display()
            return # 此时不结束会话，进入修改模式
        else:
            msg = "Invalid Cmd"
        
        self.set_display_short_message1(msg)
        
        if success:
            self.set_display_short_message2("Session Ended")
            self._refresh_status_display()
            # 只有布防/撤防操作完成后自动退出，修改密码不在这里退出
            self.is_authenticated = False 
            self.input_buffer = ""
        else:
            # 如果指令无效，保持菜单显示
            self.set_display_short_message2("1:Away armed 2:Stay armed 3:Set Password 0:Disarm")

    def _attempt_login(self):
        """尝试登录"""
        if not self.input_buffer:
            return

        user_id = "admin"
        password = self.input_buffer
        
        success = self.config_manager.login_manager.validate_credentials(user_id, password)
        
        if success:
            self.is_authenticated = True
            self.current_valid_password = password # [重要] 保存旧密码用于修改验证
            self.set_display_short_message1("Login Success")
            # [修改] 更新菜单提示，增加 3:Set
            self.set_display_short_message2("1:Away armed 2:Stay armed 3:Set Password 0:Disarm") 
            self.input_buffer = "" 
        else:
            self.is_authenticated = False
            self.current_valid_password = None
            self.input_buffer = ""
            
            if self.config_manager.login_manager.is_locked:
                self.set_display_short_message1("SYSTEM LOCKED")
                self.set_display_short_message2("Too many attempts")
            else:
                self.set_display_short_message1("Login Failed")
                self.set_display_short_message2("Try Again")

    def _attempt_change_password(self):
        """[新增] 尝试执行修改密码逻辑"""
        new_password = self.input_buffer
        
        # 简单校验：密码不能为空且必须是数字
        if not new_password or not new_password.isdigit():
            self.set_display_short_message1("Invalid Format")
            self.set_display_short_message2("Digits Only")
            self.input_buffer = ""
            return

        # 调用 LoginManager 修改密码
        # 注意：我们需要传入旧密码 (self.current_valid_password)
        result = self.config_manager.login_manager.change_password(
            self.current_valid_password, 
            new_password
        )
        
        if result:
            self.set_display_short_message1("PASSWORD CHANGED")
            self.set_display_short_message2("Please Relogin")
            
            # 保存配置到文件
            self.config_manager.save_configuration()
            
            # 强制登出，重置所有状态
            self.is_authenticated = False
            self.is_changing_password = False
            self.current_valid_password = None
            self.input_buffer = ""
        else:
            # 理论上不应该走到这里，因为我们是登录后操作的
            self.set_display_short_message1("Change Failed")
            self.set_display_short_message2("System Error")
            self.is_changing_password = False
            self.input_buffer = ""

    # --- 按钮事件实现 ---

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
        if self.is_changing_password:
            # 如果在修改密码模式，# 号代表确认新密码
            self._attempt_change_password()
        elif not self.is_authenticated:
            # 如果未登录，# 号代表确认登录
            self._attempt_login()
        # 如果已登录且不是修改模式，# 号暂无功能（或者可以作为登出键）

    def button_panic(self):
        self.config_manager.set_mode(SafeHomeMode.PANIC)
        self.set_display_short_message1("ALARM TRIGGERED!")
        self._refresh_status_display()