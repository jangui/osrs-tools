import tkinter as tk
from pynput.keyboard import Listener, KeyCode

# Toggle key
TOGGLE_KEY = KeyCode(char="o")
overlays = []
overlays_visible = False
toggle_requested = False

def create_overlay(x_start, x_end, y_start, y_end, color='red'):
    root = tk.Tk()
    root.geometry(f"{x_end - x_start}x{y_end - y_start}+{x_start}+{y_start}")
    root.overrideredirect(1)
    root.attributes('-alpha', 0.3)
    root.attributes("-topmost", True)

    frame = tk.Frame(root, bg=color, bd=0, highlightthickness=2, highlightbackground="red")
    frame.pack(fill=tk.BOTH, expand=True)
    overlays.append(root)


def toggle_overlays():
    global overlays_visible
    overlays_visible = not overlays_visible
    for overlay in overlays:
        if overlays_visible:
            overlay.deiconify()
        else:
            overlay.withdraw()

def on_press(key):
    global toggle_requested
    if key == TOGGLE_KEY:
        toggle_requested = True

def check_toggle_request():
    global toggle_requested
    if toggle_requested:
        toggle_overlays()
        toggle_requested = False
    overlays[0].after(100, check_toggle_request)  # Check every 100ms

listener = Listener(on_press=on_press)
listener.start()

# Create overlays
create_overlay(500, 600, 500, 600, color='green')
create_overlay(1440, 1461, 775, 795, color='blue')

# Initially, withdraw all overlays
for overlay in overlays:
    overlay.withdraw()

# Start the checking mechanism
overlays[0].after(100, check_toggle_request)

# Start the main Tkinter loop for the first overlay
overlays[0].mainloop()
