import time
import random
import threading
from PIL import ImageGrab
from screeninfo import get_monitors
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

# TODO
"""
- refractor and clean up

mayb
- compile the python code?
- setup script? 
"""


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

    alc_start = time.perf_counter()
    first_alc_delay = random.uniform(2.5, 2.8)
    alc_start -= first_alc_delay

    alc_duration = 3.0
    alc_reaction_time_min = 75
    alc_reaction_time_max = 375

    spell_reaction_time_min = 290
    spell_reaction_time_max = 400

    slow_reaction_chance = 0.05
    slow_reaction_time_increase = 700
    slow_reaction = False

    consecutive_slow_reaction_chance = 0.75
    previous_slow_reaction = False

    mouse_release_min = 80
    mouse_release_max = 150

    while True:
        if clicking:
            # roll for a slow reaction times
            if previous_slow_reaction:
                slow_reaction_chance += consecutive_slow_reaction_chance
            if random.random() < slow_reaction_chance:
                slow_reaction = True
                alc_reaction_time_max += slow_reaction_time_increase
                spell_reaction_time_max += slow_reaction_time_increase
            if previous_slow_reaction:
                slow_reaction_chance -= consecutive_slow_reaction_chance
                previous_slow_reaction = False

            # click spell
            mouse.press(Button.left)
            mouse_release_delay = random.uniform(mouse_release_min, mouse_release_max)
            time.sleep(mouse_release_delay / 1000)
            mouse.release(Button.left)

            # spin until previous alch finishes
            time_alching = time.perf_counter() - alc_start
            while time_alching < alc_duration:
                time_alching = time.perf_counter() - alc_start

            # delay to mimic human's reaction times
            alc_reaction_time = random.uniform(alc_reaction_time_min, alc_reaction_time_max)
            time.sleep(alc_reaction_time / 1000)

            # click item (alching spell starts)
            mouse.press(Button.left)
            mouse_release_delay = random.uniform(mouse_release_min, mouse_release_max)
            time.sleep(mouse_release_delay / 1000)
            mouse.release(Button.left)
            alc_start = time.perf_counter()

            # check if spell book is open (based on checking certain pixels' color)
            screenshot = ImageGrab.grab()
            color = screenshot.getpixel((x, y))
            wait_interval = 150
            while color != desired_color:
                #print("waiting for spell book...")
                time.sleep(wait_interval / 1000)
                screenshot = ImageGrab.grab()
                color = screenshot.getpixel((x, y))

            # once spell book is open, sleep to mimic human reaction time
            spell_reaction_time = random.uniform(spell_reaction_time_min, spell_reaction_time_max)
            time.sleep(alc_reaction_time / 1000)

            # reset reaction times if we had a slow reaction
            if slow_reaction:
                alc_reaction_time_max -= slow_reaction_time_increase
                spell_reaction_time_max -= slow_reaction_time_increase
                slow_reaction = False
                previous_slow_reaction = True


def toggle_event(key):
    global clicking
    if key == TOGGLE_KEY:
        clicking = not clicking

click_thread = threading.Thread(target=clicker)
click_thread.start()

with Listener(on_press=toggle_event) as listener:
    listener.join()
