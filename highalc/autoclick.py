import time
import random
import threading
from PIL import ImageGrab
from screeninfo import get_monitors
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

# 5 seconds to get spell book open
start_delay = 5
print("Starting auto clicker...")
print("In  ", end='')
for i in range(start_delay):
    print(f"\b{5-i}", end="", flush=True)
    time.sleep(1)
print("\b\b\b\b     ")

# Toggle key
TOGGLE_KEY = KeyCode(char="s")
clicking = True
mouse = Controller()

# x and y coordinates for flagging when spell book open
# based on color values at this point when spell book open/closed
x_flag = 1276
y_flag = 695

# Calculate scale factor using screeninfo
screen_width = get_monitors()[0].width
screen_height = get_monitors()[0].height
screenshot = ImageGrab.grab()
screenshot_width, screenshot_height = screenshot.size
scale_factor = screenshot_width / screen_width
x  = x_flag * scale_factor
y = y_flag * scale_factor

# set 'desired_color' so we know when spell book open
screenshot = ImageGrab.grab()
desired_color = screenshot.getpixel((x, y))
del screenshot

def clicker():
    global clicking


    delay1 = 0
    delay2 = 2000;
    time_waited = 0
    mouse_press_min = 80
    mouse_press_max = 150
    alch_min_time = 3005
    alch_max_time = 3275
    slow_alc_chance = 0.05

    while True:
        if clicking:
            # click spell
            mouse.press(Button.left)
            click_delay = random.uniform(mouse_press_min, mouse_press_max)
            time.sleep(click_delay / 1000)
            mouse.release(Button.left)
            time_waited += click_delay

            # roll for a 'slow' alch
            if random.random() < slow_alc_chance:
                alch_min_time = 3100
                alch_max_time = 3500
                if slow_alc_chance == 0.05:
                    # boost probability to slow alc after a slow alch
                    slow_alc_chance = 0.75
                else:
                    slow_alc_chance = 0.05

            # calculate when the previous high alch spell should be finished
            time_alching = time_waited + delay2 + click_delay
            if time_alching >= alch_max_time: #
                time_alching = 1000
            delay1 = random.uniform(alch_min_time-time_alching, alch_max_time-time_alching)
            time.sleep(delay1 / 1000)

            # click item (alching spell starts - 3000 ms starts when mouse releases)
            mouse.press(Button.left)
            click_delay = random.uniform(mouse_press_min, mouse_press_max)
            time.sleep(click_delay / 1000)
            mouse.release(Button.left)

            # check if spell book is open (based on pixel color que's)
            screenshot = ImageGrab.grab()
            color = screenshot.getpixel((x, y))
            time_waited = 0
            wait_interval = 50
            while color != desired_color:
                print("waiting for spell book...")
                time.sleep(wait_interval / 1000)
                time_waited += wait_interval
                screenshot = ImageGrab.grab()
                color = screenshot.getpixel((x, y))


            # spell book now open, delay before loop restarts and spell clicked
            delay2_min = 300
            delay2_max = 400
            slow_click_chance = 0.5
            if random.random() < slow_click_chance:
                delay2_min = 300
                delay2_max = 1000
                if slow_click_chance == 0.05:
                    # boost probability to slow alc after a slow alch
                    slow_click_chance = 0.8
                else:
                    slow_click_chance = 0.05

            delay2 = random.uniform(delay2_min, delay2_max)
            time.sleep(delay2 / 1000)

def toggle_event(key):
    global clicking
    if key == TOGGLE_KEY:
        clicking = not clicking

click_thread = threading.Thread(target=clicker)
click_thread.start()

with Listener(on_press=toggle_event) as listener:
    listener.join()
