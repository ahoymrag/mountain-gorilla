"""
Terminal animations to add flavor to your CLI.
Includes a spinner example and a simple 'typing' effect.
"""

import sys
import time

def spinner_animation(duration=2.0, message="Training in progress"):
    """
    A simple spinner animation. Runs for 'duration' seconds, 
    printing a spinner to the terminal.
    """
    spinner_frames = ["-", "\\", "|", "/"]
    end_time = time.time() + duration
    idx = 0

    sys.stdout.write(f"{message} ")
    sys.stdout.flush()

    while time.time() < end_time:
        frame = spinner_frames[idx % len(spinner_frames)]
        sys.stdout.write(f"\b{frame}")
        sys.stdout.flush()
        time.sleep(0.1)
        idx += 1

    # Clear spinner symbol
    sys.stdout.write("\b")
    sys.stdout.flush()

def typing_effect(text, delay=0.03):
    """
    Prints text with a 'typing' effect.
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
