import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk
from typing import Optional
from safehome.core.system import System


class CameraMonitor(tk.Toplevel):
    """
    Camera monitor window - displays camera feed with password protection
    Integrates with System's CameraController
    """

    def __init__(self, master=None, system: System = None, camera_id: int = 1, password: Optional[str] = None):
        super().__init__(master)
        self.title(f"SafeHome Monitor - Camera {camera_id}")
        self.geometry("520x750")
        self.resizable(False, False)

        self.system = system
        self.camera_id = camera_id
        self.password = password

        # Verify camera access
        if not self._verify_access():
            self.destroy()
            return

        # Get camera from System's CameraController
        self.camera = self.system.camera_controller.get_camera(camera_id)
        if not self.camera:
            messagebox.showerror("Error", f"Camera {camera_id} not found")
            self.destroy()
            return

        # Setup GUI
        self._setup_gui()

        # Start feed update loop
        self._update_feed()

        # Clean up on window close
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _verify_access(self):
        """Verify camera access with password protection"""
        if not self.system:
            messagebox.showerror("Error", "System not initialized")
            return False

        camera = self.system.camera_controller.get_camera(self.camera_id)
        if not camera:
            messagebox.showerror("Error", f"Camera {self.camera_id} not found")
            return False

        if camera.has_password() and not camera.verify_password(self.password):
            messagebox.showerror("Access Denied", "Invalid camera password")
            return False

        return True

    def _setup_gui(self):
        """Setup GUI components"""
        # 1. Image display area
        self.image_label = tk.Label(self, bg="black")
        self.image_label.pack(pady=10)

        # 2. Camera info frame
        info_frame = ttk.LabelFrame(self, text="Camera Info")
        info_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(info_frame, text=f"Name: {self.camera.name}").pack(anchor="w", padx=5)
        ttk.Label(info_frame, text=f"Location: {self.camera.location}").pack(anchor="w", padx=5)
        status_text = "Enabled" if self.camera.is_enabled else "Disabled"
        ttk.Label(info_frame, text=f"Status: {status_text}").pack(anchor="w", padx=5)

        # 3. PTZ Control panel
        control_frame = ttk.LabelFrame(self, text="PTZ Controls")
        control_frame.pack(fill="x", padx=10, pady=5)

        # Zoom buttons
        ttk.Button(control_frame, text="Zoom In (+)", command=self._zoom_in).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(control_frame, text="Zoom Out (-)", command=self._zoom_out).grid(row=0, column=2, padx=5, pady=5)

        # Pan buttons
        ttk.Button(control_frame, text="< Pan Left", command=self._pan_left).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(control_frame, text="Pan Right >", command=self._pan_right).grid(row=1, column=2, padx=5, pady=5)

        # Control label
        ttk.Label(control_frame, text="Camera Control").grid(row=1, column=1)

    def _pan_left(self):
        """Pan camera left"""
        success = self.system.camera_controller.pan_camera(
            self.camera_id, "left", self.password
        )
        if not success:
            messagebox.showwarning("Pan Failed", "Cannot pan left - limit reached or access denied")

    def _pan_right(self):
        """Pan camera right"""
        success = self.system.camera_controller.pan_camera(
            self.camera_id, "right", self.password
        )
        if not success:
            messagebox.showwarning("Pan Failed", "Cannot pan right - limit reached or access denied")

    def _zoom_in(self):
        """Zoom camera in"""
        success = self.system.camera_controller.zoom_camera(
            self.camera_id, "in", self.password
        )
        if not success:
            messagebox.showwarning("Zoom Failed", "Cannot zoom in - limit reached or access denied")

    def _zoom_out(self):
        """Zoom camera out"""
        success = self.system.camera_controller.zoom_camera(
            self.camera_id, "out", self.password
        )
        if not success:
            messagebox.showwarning("Zoom Failed", "Cannot zoom out - limit reached or access denied")

    def _update_feed(self):
        """Periodically get new frame from camera and display"""
        try:
            # Get camera view through System's CameraController
            pil_image = self.system.camera_controller.get_camera_view(
                self.camera_id, self.password
            )
            if pil_image:
                # Convert to Tkinter PhotoImage
                self.tk_image = ImageTk.PhotoImage(pil_image)
                self.image_label.config(image=self.tk_image)
            else:
                # Access denied or camera disabled
                self.image_label.config(text="Camera Unavailable", fg="red")
        except Exception as e:
            print(f"Camera Error: {e}")

        # Refresh every 100ms (10 FPS)
        self.after(100, self._update_feed)

    def _on_close(self):
        """Clean up resources"""
        # Camera cleanup is handled by System's CameraController
        self.destroy()
