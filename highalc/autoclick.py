import time
import random
import threading
import numpy as np
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

def jitter_mouse(top_left, bottom_right, speed=0.001, min_speed=0.0001):
    current_x, current_y = mouse.position

    if not (top_left[0] <= current_x <= bottom_right[0] and top_left[1] <= current_y <= bottom_right[1]):
        print(f'mouse no bueno, x: {current_x} , y: {current_y}', top_left[0], top_left[1], bottom_right[0], bottom_right[1])
        return  # Mouse is not within the specified rectangle, so don't move it

    target_x, target_y = random_point_in_rectangle(top_left, bottom_right)
    ease_out_move_mouse(target_x, target_y, speed, min_speed)

def random_point_in_rectangle(top_left, bottom_right):
    center_x = (top_left[0] + bottom_right[0]) / 2
    center_y = (top_left[1] + bottom_right[1]) / 2
    width = bottom_right[0] - top_left[0]
    height = bottom_right[1] - top_left[1]

    x = np.random.normal(center_x, width / 16)
    y = np.random.normal(center_y, height / 16)

    # Clamp the values to be within the rectangle
    x = max(top_left[0], min(x, bottom_right[0]))
    y = max(top_left[1], min(y, bottom_right[1]))

    return x, y

def ease_out_move_mouse(target_x, target_y, speed, min_speed):
    current_x, current_y = mouse.position

    while abs(current_x - target_x) > 1 or abs(current_y - target_y) > 1:
        current_x, current_y = mouse.position
        distance_x = abs(target_x - current_x)
        distance_y = abs(target_y - current_y)

        if random.choice([True, False]) and distance_x > 1:
            step_x = np.sign(target_x - current_x)
            new_x = current_x + step_x
            mouse.position = (new_x, current_y)
            current_x = new_x

            # Apply ease-out effect to the speed
            eased_speed = max(min_speed, speed * np.log10(distance_x + 1))
            time.sleep(eased_speed)

        if random.choice([True, False]) and distance_y > 1:
            step_y = np.sign(target_y - current_y)
            new_y = current_y + step_y
            mouse.position = (current_x, new_y)
            current_y = new_y

            # Apply ease-out effect to the speed
            eased_speed = max(min_speed, speed * np.log10(distance_y + 1))
            time.sleep(eased_speed)

        if random.choice([True, False]):
            time.sleep(random.uniform(min_speed, speed))

    mouse.position = (target_x, target_y)

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

    #mouse_jitter_chance = 0.177398

    while True:
        if clicking:
            # jitter mouse
            #if random.random() < mouse_jitter_chance:
            top_left = (1423, 781)
            bottom_right = (1430, 792)
            jitter_mouse(top_left, bottom_right)


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
