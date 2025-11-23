import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
import sys

# 引入老师的 Camera API
from safehome.device.camera.device_camera import DeviceCamera

class CameraMonitor(tk.Toplevel):
    """
    独立的监控窗口，用于显示 DeviceCamera 的画面
    """
    def __init__(self, master=None, camera_id=1):
        super().__init__(master)
        self.title(f"SafeHome Monitor - Cam {camera_id}")
        self.geometry("520x750")
        self.resizable(False, False)
        
        # 1. 初始化虚拟摄像头
        self.camera = DeviceCamera()
        self.camera.set_id(camera_id) # 这会加载 camera{id}.jpg
        
        # 2. 图像显示区域
        self.image_label = tk.Label(self, bg="black")
        self.image_label.pack(pady=10)
        
        # 3. 控制面板 (Pan/Zoom)
        control_frame = ttk.LabelFrame(self, text="PTZ Controls")
        control_frame.pack(fill="x", padx=10, pady=5)
        
        # 缩放按钮
        ttk.Button(control_frame, text="Zoom In (+)", command=self.camera.zoom_in).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(control_frame, text="Zoom Out (-)", command=self.camera.zoom_out).grid(row=0, column=2, padx=5, pady=5)
        
        # 移动按钮
        ttk.Button(control_frame, text="< Pan Left", command=self.camera.pan_left).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(control_frame, text="Pan Right >", command=self.camera.pan_right).grid(row=1, column=2, padx=5, pady=5)
        
        # 说明标签
        ttk.Label(control_frame, text="Control").grid(row=1, column=1)

        # 4. 启动画面刷新循环
        self._update_feed()

        # 窗口关闭时停止摄像头线程
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _update_feed(self):
        """定时获取摄像头的新帧并显示"""
        try:
            # 获取 PIL Image
            pil_image = self.camera.get_view()
            if pil_image:
                # 转换为 Tkinter 可用的 PhotoImage
                self.tk_image = ImageTk.PhotoImage(pil_image)
                self.image_label.config(image=self.tk_image)
        except Exception as e:
            print(f"Camera Error: {e}")
            
        # 每 100ms 刷新一次 (10 FPS)
        self.after(100, self._update_feed)

    def _on_close(self):
        """清理资源"""
        self.camera.stop() # 停止摄像头内部线程
        self.destroy()