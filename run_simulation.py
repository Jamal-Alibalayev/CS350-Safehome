# run_simulation.py
import tkinter as tk
from safehome.configuration.configuration_manager import ConfigurationManager
from interface.safehome_control_panel import SafeHomeControlPanel
# 导入摄像头监控窗口
from interface.camera_monitor import CameraMonitor

# 导入你提供的虚拟硬件 API
from device.device_windoor_sensor import DeviceWinDoorSensor
from device.device_motion_detector import DeviceMotionDetector
from device.device_sensor_tester import DeviceSensorTester

def setup_virtual_hardware():
    """创建一些虚拟传感器用于测试"""
    print("Initializing Virtual Sensors...")
    
    # 创建 2 个门窗传感器 (ID 会自动生成: 1, 2)
    w1 = DeviceWinDoorSensor()
    w2 = DeviceWinDoorSensor()
    print(f"  - Created WinDoor Sensors: IDs {w1.get_id()}, {w2.get_id()}")
    
    # 创建 2 个动作探测器 (ID 会自动生成: 1, 2)
    m1 = DeviceMotionDetector()
    m2 = DeviceMotionDetector()
    print(f"  - Created Motion Detectors: IDs {m1.get_id()}, {m2.get_id()}")
    
    # 注意：在这个简易版本中，我们还没有把 sensors 注册给 System 类，
    # 但它们已经注册到了 DeviceSensorTester 的链表中，可以在 Sensor GUI 中看到。

def main():
    # 1. 创建 Tkinter 根窗口 (隐藏)
    root = tk.Tk()
    root.withdraw() 
    
    # 2. 初始化配置系统
    print("[System] Loading Configuration...")
    config = ConfigurationManager()
    
    # 3. 初始化虚拟硬件
    setup_virtual_hardware()
    
    # 4. 启动 Sensor Test GUI (模拟物理环境)
    # 利用你提供的 API: DeviceSensorTester.showSensorTester()
    print("[GUI] Launching Sensor Simulator...")
    DeviceSensorTester.showSensorTester()
    
    # 5. 启动 Control Panel GUI (模拟墙上的键盘)
    print("[GUI] Launching Control Panel...")
    control_panel = SafeHomeControlPanel(master=root, config_manager=config)

    # F. Launch [Camera Monitor] Window
    print("[GUI] Launching Camera Monitor...")
    # Ensure 'camera1.jpg' exists in the root directory
    camera_monitor = CameraMonitor(master=root, camera_id=1)
    
    # 窗口关闭处理
    def on_close():
        print("[System] Saving configuration and exiting...")
        config.save_configuration()
        root.destroy()
        exit()

        # cleanup camera resources 
        try:
            if hasattr(camera_monitor, 'camera'):
                camera_monitor.camera.stop()
        except Exception as e:
            print(f"Camera cleanup warning: {e}")

    control_panel.protocol("WM_DELETE_WINDOW", on_close)
    
    print("\n" + "="*50)
    print("SIMULATION STARTED")
    print("1. Use 'Sensor Test' window to simulate intruders.")
    print("2. Use 'Control Panel' to Arm/Disarm system.")
    print("   Default Password: 1234")
    print("="*50 + "\n")
    
    root.mainloop()

if __name__ == "__main__":
    main()