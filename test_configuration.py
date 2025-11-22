import unittest
import os
import time
from configuration.configuration_manager import ConfigurationManager
from configuration.safehome_mode import SafeHomeMode
from configuration.safety_zone import SafetyZone

class TestSafeHomeConfiguration(unittest.TestCase):
    """
    测试 SafeHome 配置子系统
    """

    def setUp(self):
        """
        每次测试前运行。初始化 ConfigurationManager。
        """
        # 为了保证测试环境干净，先清理可能存在的配置文件
        self.clean_up_files()
        self.config_manager = ConfigurationManager()

    def tearDown(self):
        """
        每次测试后运行。清理生成的文件。
        """
        self.clean_up_files()

    def clean_up_files(self):
        """辅助方法：清理测试产生的文件"""
        files_to_remove = ["safehome_config.json", "safehome_events.log"]
        for f in files_to_remove:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except PermissionError:
                    pass

    # ---------------------------------------------------------
    # 1. 测试 ConfigurationManager (Facade) 和 SystemSettings
    # ---------------------------------------------------------
    def test_default_settings(self):
        """测试系统是否加载了默认设置"""
        print("\n[Test] Default Settings")
        settings = self.config_manager.settings
        self.assertEqual(settings.master_password, "1234")
        self.assertEqual(settings.entry_delay, 30)
        self.assertEqual(self.config_manager.get_mode(), SafeHomeMode.DISARMED)

    def test_update_and_save_settings(self):
        """测试更新设置并持久化到 JSON 文件"""
        print("\n[Test] Persistence (Save/Load)")
        
        # 1. 修改设置
        new_pass = "9999"
        new_delay = 60
        self.config_manager.settings.update_settings(
            master_password=new_pass, 
            entry_delay=new_delay
        )
        
        # 2. 保存
        self.config_manager.save_configuration()
        self.assertTrue(os.path.exists("safehome_config.json"), "Config file should be created")

        # 3. 重新创建一个 Manager (模拟重启系统)
        new_manager = ConfigurationManager()
        
        # 4. 验证新 Manager 是否读取了保存的值
        self.assertEqual(new_manager.settings.master_password, new_pass)
        self.assertEqual(new_manager.settings.entry_delay, new_delay)

    def test_mode_change(self):
        """测试系统模式切换"""
        print("\n[Test] Mode Change")
        self.config_manager.set_mode(SafeHomeMode.ARMED_AWAY)
        self.assertEqual(self.config_manager.get_mode(), SafeHomeMode.ARMED_AWAY)

    # ---------------------------------------------------------
    # 2. 测试 LoginManager (登录与安全锁定)
    # ---------------------------------------------------------
    def test_login_success(self):
        """测试正确的密码登录"""
        print("\n[Test] Login Success")
        # 默认密码是 1234
        result = self.config_manager.login_manager.validate_credentials("admin", "1234")
        self.assertTrue(result)

    def test_login_failure_and_lockout(self):
        """测试密码错误多次后的系统锁定逻辑"""
        print("\n[Test] Login Lockout")
        lm = self.config_manager.login_manager
        
        # 1. 尝试错误密码 (默认最大尝试次数为 3)
        self.assertFalse(lm.validate_credentials("admin", "wrong"))
        self.assertFalse(lm.validate_credentials("admin", "wrong"))
        self.assertFalse(lm.validate_credentials("admin", "wrong"))
        
        # 2. 确认此时系统已锁定
        self.assertTrue(lm.is_locked, "System should be locked after 3 failed attempts")

        # 3. 即使输入正确密码，也应被拒绝
        self.assertFalse(lm.validate_credentials("admin", "1234"), "Should reject correct password when locked")

        # 4. 解锁
        lm.unlock_system()
        self.assertFalse(lm.is_locked)
        self.assertTrue(lm.validate_credentials("admin", "1234"))

    def test_change_password(self):
        """测试修改密码"""
        print("\n[Test] Change Password")
        lm = self.config_manager.login_manager
        
        # 验证旧密码失败，无法修改
        success = lm.change_password("wrong_old", "new_pass")
        self.assertFalse(success)
        
        # 验证旧密码成功，修改密码
        success = lm.change_password("1234", "5678")
        self.assertTrue(success)
        self.assertEqual(self.config_manager.settings.master_password, "5678")

    # ---------------------------------------------------------
    # 3. 测试 LogManager (日志记录)
    # ---------------------------------------------------------
    def test_logging(self):
        """测试日志记录和检索"""
        print("\n[Test] Logging")
        logger = self.config_manager.logger
        
        msg = "Test log message"
        logger.add_log(msg, level="WARNING")
        
        # 验证内存中的日志
        recent_logs = logger.get_recent_logs()
        self.assertTrue(len(recent_logs) > 0)
        self.assertIn(msg, recent_logs[-1].message)
        self.assertEqual(recent_logs[-1].level, "WARNING")
        
        # 验证文件写入
        self.assertTrue(os.path.exists("safehome_events.log"))
        with open("safehome_events.log", "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("WARNING", content)
            self.assertIn(msg, content)

    # ---------------------------------------------------------
    # 4. 测试 SafetyZone (独立类)
    # ---------------------------------------------------------
    def test_safety_zone_operations(self):
        """测试安全区域的传感器管理"""
        print("\n[Test] Safety Zone")
        zone = SafetyZone(1, "Living Room")
        
        # 添加传感器
        zone.add_sensor(101)
        zone.add_sensor(102)
        zone.add_sensor(101) # 重复添加
        
        self.assertEqual(len(zone.sensors), 2, "Duplicate sensors should not be added")
        self.assertIn(101, zone.sensors)
        
        # 移除传感器
        zone.remove_sensor(101)
        self.assertNotIn(101, zone.sensors)
        self.assertEqual(len(zone.sensors), 1)

if __name__ == "__main__":
    unittest.main()