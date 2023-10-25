import pyautogui

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y}) with {button}")

# Set up the mouse listener
with pyautogui.hooks.MouseWatcher(on_click=on_click) as listener:
    listener.join()
