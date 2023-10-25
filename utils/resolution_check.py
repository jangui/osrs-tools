import tkinter as tk
from pynput import mouse
from PIL import ImageGrab
from threading import Thread
import time
from screeninfo import get_monitors

# Function to handle mouse movement
def on_move(x, y):
    global positions
    x_scaled = int(x * scale_factor)
    y_scaled = int(y * scale_factor)
    positions.append((x_scaled, y_scaled))

# Function to take a screenshot and process it
def take_screenshot():
    global positions
    time.sleep(5)
    screenshot = ImageGrab.grab()
    pixels = screenshot.load()
    for pos in positions:
        if 0 <= pos[0] < screenshot.width and 0 <= pos[1] < screenshot.height:
            pixels[pos] = (255, 0, 0)
    screenshot.show()

# Create a square overlay
root = tk.Tk()
root.geometry("100x100+{}+{}".format(root.winfo_screenwidth() // 2 - 50, root.winfo_screenheight() // 2 - 50))
root.overrideredirect(True)
root.attributes("-topmost", True)
frame = tk.Frame(root, bg="black")
frame.pack(fill="both", expand="yes")

# Calculate scale factor using screeninfo
screen_width = get_monitors()[0].width
screen_height = get_monitors()[0].height
screenshot = ImageGrab.grab()
screenshot_width, screenshot_height = screenshot.size
scale_factor = screenshot_width / screen_width

# Set up mouse listener
positions = []
listener = mouse.Listener(on_move=on_move)
listener.start()

# Take a screenshot after 5 seconds
thread = Thread(target=take_screenshot)
thread.start()

# Start the Tkinter main loop
root.mainloop()

# Stop the mouse listener
listener.stop()
