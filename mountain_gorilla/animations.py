"""
Terminal animations to add flavor to your CLI.
Example: spinner animation, typing effect, and loading bar.
"""

import sys
import time

def spinner_animation(duration=2.0, message="Processing"):
    """
    A simple spinner animation. Runs for 'duration' seconds.
    Prints 'message' followed by a rotating spinner in the terminal.
    """
    spinner_frames = ["-", "\\", "|", "/"]
    end_time = time.time() + duration
    idx = 0

    # Print the initial message
    sys.stdout.write(f"{message} ")
    sys.stdout.flush()

    while time.time() < end_time:
        frame = spinner_frames[idx % len(spinner_frames)]
        sys.stdout.write(f"\b{frame}")
        sys.stdout.flush()
        time.sleep(0.1)
        idx += 1

    # Remove the spinner symbol
    sys.stdout.write("\b")
    sys.stdout.flush()

def typing_effect(text, delay=0.03):
    """
    Prints text with a 'typing on screen' effect.
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()

def loading_bar(duration=2.0, message="Loading"):
    """
    A simple loading bar animation.
    """
    bar_length = 30
    end_time = time.time() + duration
    sys.stdout.write(f"{message} [")
    sys.stdout.flush()

    while time.time() < end_time:
        elapsed = duration - (end_time - time.time())
        filled_length = int(bar_length * elapsed // duration)
        bar = '=' * filled_length + '-' * (bar_length - filled_length)
        sys.stdout.write(f"\r{message} [{bar}]")
        sys.stdout.flush()
        time.sleep(0.1)

    sys.stdout.write("]\n")
    sys.stdout.flush()
