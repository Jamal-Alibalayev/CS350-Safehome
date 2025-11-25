"""
Simple GUI test to verify Tkinter windows open correctly
"""

import tkinter as tk
from safehome.core.system import System
from safehome.interface.control_panel.safehome_control_panel import SafeHomeControlPanel

print("Creating Tkinter root...")
root = tk.Tk()
root.withdraw()
print("Root window created (hidden)")

print("\nInitializing System...")
system = System(db_path="data/test_gui.db")
print("System initialized")

print("\nCreating Control Panel...")
try:
    control_panel = SafeHomeControlPanel(master=root, system=system)
    print("Control Panel created successfully!")
    print("Control Panel window should be visible now.")
except Exception as e:
    print(f"Error creating Control Panel: {e}")
    import traceback
    traceback.print_exc()

print("\nStarting Tkinter mainloop...")
print("(Close the Control Panel window to exit)")

def on_close():
    print("\nShutting down...")
    system.shutdown()
    root.destroy()

control_panel.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
print("Program ended.")
