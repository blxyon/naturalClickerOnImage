import time
import keyboard
import pyautogui
import random
import math
from pynput.mouse import Controller, Button
import pydirectinput

# Initialize the mouse controller
mouse = Controller()

# Pause/resume flag
paused = False

def toggle_pause():
    """
    Toggle the pause/resume state when 'q' is pressed.
    """
    global paused
    paused = not paused
    if paused:
        print("Script paused.")
    else:
        print("Script resumed.")

# Set up the 'q' key to toggle pause/resume
keyboard.on_press_key('q', lambda _: toggle_pause())

time.sleep(5)

def natural_move_to(target_x, target_y, duration=1):
    """
    Move the mouse to the target position using a Bezier curve for natural movement.
    :param target_x: Target X coordinate.
    :param target_y: Target Y coordinate.
    :param duration: Total time for the movement in seconds.
    """
    start_x, start_y = mouse.position  # Get the current mouse position
    steps = int(duration * 100)  # Number of steps (higher = smoother)
    delay = duration / steps  # Delay between each step

    # Control points for the Bezier curve (add randomness for natural movement)
    control_x1 = start_x + random.uniform(-50, 50)
    control_y1 = start_y + random.uniform(-50, 50)
    control_x2 = target_x + random.uniform(-50, 50)
    control_y2 = target_y + random.uniform(-50, 50)

    for step in range(steps):
        if paused:  # Check if the script is paused
            while paused:
                time.sleep(0.1)  # Sleep briefly to avoid high CPU usage
        t = step / steps
        # Calculate the Bezier curve position
        x = (1 - t) ** 3 * start_x + 3 * (1 - t) ** 2 * t * control_x1 + 3 * (1 - t) * t ** 2 * control_x2 + t ** 3 * target_x
        y = (1 - t) ** 3 * start_y + 3 * (1 - t) ** 2 * t * control_y1 + 3 * (1 - t) * t ** 2 * control_y2 + t ** 3 * target_y

        # Move the mouse to the calculated position
        mouse.position = (int(x), int(y))
        time.sleep(delay)

def small_adjustment():
    """
    Move the mouse 2 pixels up and 2 pixels down to simulate a small human-like adjustment.
    """
    current_x, current_y = pyautogui.position()
    pydirectinput.move(0, -2)  # Move 2 pixels up
    time.sleep(random.uniform(0.05, 0.1))  # Small delay
    pydirectinput.move(0, 2)  # Move 2 pixels down
    time.sleep(random.uniform(0.05, 0.1))  # Small delay

def natural_click():
    """
    Simulate a natural mouse click with randomized delays.
    """
    if paused:  # Check if the script is paused
        while paused:
            time.sleep(0.1)  # Sleep briefly to avoid high CPU usage

    # Perform a small adjustment before clicking
    small_adjustment()

    # Random delay before pressing the mouse button
    time.sleep(random.uniform(0.05, 0.2))
    
    mouse.press(Button.left)  # Press the left mouse button
    time.sleep(random.uniform(0.05, 0.15))  # Random delay for holding the click
    mouse.release(Button.left)  # Release the left mouse button
    
    # Random delay after releasing the mouse button
    time.sleep(random.uniform(0.05, 0.2))

while True:
    try:
        if not paused:  # Only execute if the script is not paused
            # Try to locate the image on the screen
            start = pyautogui.locateCenterOnScreen('capture.PNG', region=(0, 0, 1920, 1080), grayscale=True, confidence=0.70)
            if start is not None:
                print(f"Image found at: {start}")
                natural_move_to(start.x, start.y, duration=1)  # Move naturally to the target
                natural_click()  # Perform a natural click
        else:
            time.sleep(0.1)  # Sleep briefly to avoid high CPU usage while paused
    except pyautogui.ImageNotFoundException:
        # If the image is not found, ignore the exception and continue the loop
        print("Image not found, retrying...")
        time.sleep(4)  # Add a small delay to avoid spamming the loop
