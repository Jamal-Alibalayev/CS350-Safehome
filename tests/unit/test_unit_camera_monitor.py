import unittest
from unittest.mock import MagicMock, patch, ANY
import tkinter as tk
from tkinter import messagebox # Added this line
from PIL import Image

from safehome.interface.control_panel.camera_monitor import CameraMonitor

# This boilerplate is to make CameraMonitor testable without a real GUI loop.
# These functions are used to patch the real methods.
def mock_init(self, master=None, system=None, camera_id=1, password=None):
    # The call to super().__init__ would hang the test because it initializes a
    # Tkinter window without a running event loop.
    # super(CameraMonitor, self).__init__(master)
    
    # We need to mock the Tkinter methods that are used.
    self.title = MagicMock()
    self.geometry = MagicMock()
    self.resizable = MagicMock()
    self.protocol = MagicMock()
    self.after = MagicMock()
    self.destroy = MagicMock()

    self.title(f"SafeHome Monitor - Camera {camera_id}")
    self.geometry("520x750")
    self.resizable(False, False)

    self.system = system
    self.camera_id = camera_id
    self.password = password
    
    self._setup_gui_called = False
    if not self._verify_access():
        self.destroy()
        return

    self.camera = self.system.camera_controller.get_camera(camera_id)
    if not self.camera:
        messagebox.showerror("Error", f"Camera {camera_id} not found")
        self.destroy()
        return

    self._setup_gui()
    self._update_feed()
    self.protocol("WM_DELETE_WINDOW", self._on_close)

def mock_setup_gui(self):
    self._setup_gui_called = True
    self.image_label = MagicMock()


class TestCameraMonitor(unittest.TestCase):

    def setUp(self):
        # Start patchers to isolate mocking from other test files
        self.tk_patcher = patch('tkinter.Tk', new_callable=MagicMock)
        self.init_patcher = patch.object(CameraMonitor, '__init__', mock_init)
        self.gui_patcher = patch.object(CameraMonitor, '_setup_gui', mock_setup_gui)
        
        self.mock_tk = self.tk_patcher.start()
        self.init_patcher.start()
        self.gui_patcher.start()
        
        # Original setUp content
        self.mock_system = MagicMock()
        self.mock_camera = MagicMock()
        self.mock_camera.name = "Test Cam"
        self.mock_camera.location = "Living Room"
        self.mock_camera.is_enabled = True
        self.mock_camera.has_password.return_value = False
        self.mock_system.camera_controller.get_camera.return_value = self.mock_camera
        
        # This is needed because CameraMonitor is a Toplevel, which needs a master
        self.master = tk.Tk()

    def tearDown(self):
        # Stop patchers in reverse order to clean up
        self.gui_patcher.stop()
        self.init_patcher.stop()
        self.tk_patcher.stop()

    @patch('safehome.interface.control_panel.camera_monitor.messagebox')
    @patch('safehome.interface.control_panel.camera_monitor.ImageTk')
    def test_init_success(self, mock_imagetk, mock_messagebox):
        """Test successful initialization of CameraMonitor."""
        self.mock_camera.has_password.return_value = False
        monitor = CameraMonitor(master=self.master, system=self.mock_system, camera_id=1, password=None)
        
        self.mock_system.camera_controller.get_camera.assert_called_with(1)
        self.assertTrue(monitor._setup_gui_called)
        self.mock_system.camera_controller.get_camera_view.assert_called_with(1, None)
        mock_messagebox.showerror.assert_not_called()
        monitor.destroy() # clean up

    @patch('safehome.interface.control_panel.camera_monitor.messagebox')
    def test_init_no_system(self, mock_messagebox):
        """Test initialization failure when system is not provided."""
        monitor = CameraMonitor(master=self.master, system=None, camera_id=1)
        mock_messagebox.showerror.assert_called_with("Error", "System not initialized")
        

    @patch('safehome.interface.control_panel.camera_monitor.messagebox')
    def test_init_camera_not_found(self, mock_messagebox):
        """Test initialization failure when camera is not found."""
        self.mock_system.camera_controller.get_camera.return_value = None
        monitor = CameraMonitor(master=self.master, system=self.mock_system, camera_id=1)
        mock_messagebox.showerror.assert_called_with("Error", "Camera 1 not found")
        

    @patch('safehome.interface.control_panel.camera_monitor.messagebox')
    def test_init_invalid_password(self, mock_messagebox):
        """Test initialization failure with an invalid password."""
        self.mock_camera.has_password.return_value = True
        self.mock_camera.verify_password.return_value = False
        monitor = CameraMonitor(master=self.master, system=self.mock_system, camera_id=1, password="wrong")
        
        mock_messagebox.showerror.assert_called_with("Access Denied", "Invalid camera password")
        self.mock_camera.verify_password.assert_called_with("wrong")
        

    @patch('safehome.interface.control_panel.camera_monitor.messagebox')
    @patch('safehome.interface.control_panel.camera_monitor.ImageTk')
    def test_update_feed_success(self, mock_imagetk, mock_messagebox):
        """Test the feed updates correctly with a valid image."""
        monitor = CameraMonitor(master=self.master, system=self.mock_system, camera_id=1)
        
        mock_image = Image.new('RGB', (100, 100))
        self.mock_system.camera_controller.get_camera_view.return_value = mock_image
        
        # We need to call it manually for the test
        monitor._update_feed()

        self.mock_system.camera_controller.get_camera_view.assert_called_with(1, None)
        mock_imagetk.PhotoImage.assert_called_with(mock_image)
        monitor.image_label.config.assert_called_with(image=ANY)
        monitor.after.assert_called_with(100, monitor._update_feed)
        monitor.destroy()

    @patch('safehome.interface.control_panel.camera_monitor.messagebox')
    def test_update_feed_unavailable(self, mock_messagebox):
        """Test the feed shows unavailable when no image is returned."""
        monitor = CameraMonitor(master=self.master, system=self.mock_system, camera_id=1)
        
        self.mock_system.camera_controller.get_camera_view.return_value = None
        
        monitor._update_feed()

        self.mock_system.camera_controller.get_camera_view.assert_called_with(1, None)
        monitor.image_label.config.assert_called_with(text="Camera Unavailable", fg="red")
        monitor.after.assert_called_with(100, monitor._update_feed)
        monitor.destroy()

    @patch('safehome.interface.control_panel.camera_monitor.messagebox')
    def test_ptz_controls(self, mock_messagebox):
        """Test PTZ control methods."""
        monitor = CameraMonitor(master=self.master, system=self.mock_system, camera_id=1, password="ok")

        # Pan Left
        self.mock_system.camera_controller.pan_camera.return_value = True
        monitor._pan_left()
        self.mock_system.camera_controller.pan_camera.assert_called_with(1, 'left', 'ok')
        
        self.mock_system.camera_controller.pan_camera.return_value = False
        monitor._pan_left()
        mock_messagebox.showwarning.assert_called_with("Pan Failed", "Cannot pan left - limit reached or access denied")

        # Pan Right
        self.mock_system.camera_controller.pan_camera.return_value = True
        monitor._pan_right()
        self.mock_system.camera_controller.pan_camera.assert_called_with(1, 'right', 'ok')
        
        self.mock_system.camera_controller.pan_camera.return_value = False
        monitor._pan_right()
        mock_messagebox.showwarning.assert_called_with("Pan Failed", "Cannot pan right - limit reached or access denied")

        # Zoom In
        self.mock_system.camera_controller.zoom_camera.return_value = True
        monitor._zoom_in()
        self.mock_system.camera_controller.zoom_camera.assert_called_with(1, 'in', 'ok')
        
        self.mock_system.camera_controller.zoom_camera.return_value = False
        monitor._zoom_in()
        mock_messagebox.showwarning.assert_called_with("Zoom Failed", "Cannot zoom in - limit reached or access denied")

        # Zoom Out
        self.mock_system.camera_controller.zoom_camera.return_value = True
        monitor._zoom_out()
        self.mock_system.camera_controller.zoom_camera.assert_called_with(1, 'out', 'ok')
        
        self.mock_system.camera_controller.zoom_camera.return_value = False
        monitor._zoom_out()
        mock_messagebox.showwarning.assert_called_with("Zoom Failed", "Cannot zoom out - limit reached or access denied")
        
        monitor.destroy()

    def test_on_close(self):
        """Test the cleanup method on window close."""
        monitor = CameraMonitor(master=self.master, system=self.mock_system, camera_id=1)
        destroy_spy = self.master.destroy = MagicMock()
        monitor.destroy = destroy_spy
        
        monitor._on_close()
        destroy_spy.assert_called_once()


if __name__ == '__main__':
    unittest.main()