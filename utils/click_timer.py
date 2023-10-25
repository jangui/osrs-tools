from pynput import mouse
import time

class ClickTimer:
    def __init__(self):
        self.start_time = None
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left:
            if pressed:
                self.start_time = time.time()
            else:
                end_time = time.time()
                elapsed_time = (end_time - self.start_time) * 1000  # convert to milliseconds
                print(f"Time elapsed: {elapsed_time:.3f} ms")

if __name__ == "__main__":
    click_timer = ClickTimer()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        click_timer.listener.stop()
