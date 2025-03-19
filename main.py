#!/usr/bin/env python
"""
Entry point script for the Mountain Gorilla Command Center CLI.
After placing all files in the recommended structure, simply run:
  python main.py
from the 'mountain-gorilla' folder to start the CLI.
"""

import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
from mountain_gorilla.cli import mgcc_cli

console = Console()

def animate_banner(text: str, delay: float = 0.04) -> None:
    """
    Prints a string character-by-character with a small delay for a typing animation.
    """
    for char in text:
        console.print(char, end="", style="bold magenta")
        time.sleep(delay)
    console.print()  # Move to the next line

def main_menu():
    """
    Immediately display a dramatic introduction and show a menu of MGCC actions,
    without needing an extra CLI argument.
    """
    console.clear()

    # Dramatic ASCII Gorilla Banner
    gorilla_banner = Text(r"""
     __  ___         _                  _       _____                             __  
    /  |/  /___ ____(_)________ _____  (_)___  / ___/__  ______  ___  ___  ____  / /__
   / /|_/ / __ `/ __/ / ___/ __ `/ __ \/ / __ \/ __ \/ / / / __ \/ _ \/ _ \/ __ \/ //_/
  / /  / / /_/ / /_/ / /  / /_/ / /_/ / / / / / /_/ / /_/ / /_/ /  __/  __/ / / / ,<   
 /_/  /_/\__,_/\__/_/_/   \__,_/ .___/_/_/ /_/\____/\__,_/ .___/\___/\___/_/ /_/_/|_|  
                             /_/                    /____/                             
    """, style=Style(color="cyan", bold=True))

    console.print(gorilla_banner)
    animate_banner("Welcome to the Mountain Gorilla Command Center!\n")
    time.sleep(0.5)

    # Menu loop
    while True:
        console.print(
            Panel(
                Text(
                    "[1] List all Bots\n"
                    "[2] Summon a Bot\n"
                    "[3] Train a Bot\n"
                    "[4] Show MGCC Version\n"
                    "[5] Launch Dashboard\n"
                    "[q] Quit\n",
                    style="bold cyan"
                ),
                title="MGCC Main Menu",
                border_style="magenta"
            )
        )

        choice = console.input("[bold yellow]Your choice[/]: ").strip().lower()

        if choice == "1":
            # call the CLI subcommand "list"
            mgcc_cli(standalone_mode=False, args=["list"])
        elif choice == "2":
            bot_name = console.input("[bold magenta]Enter the bot name to summon[/]: ")
            mgcc_cli(standalone_mode=False, args=["summon", bot_name])
        elif choice == "3":
            bot_name = console.input("[bold magenta]Enter the bot name to train[/]: ")
            mgcc_cli(standalone_mode=False, args=["train", bot_name])
        elif choice == "4":
            mgcc_cli(standalone_mode=False, args=["version"])
        elif choice == "5":
            mgcc_cli(standalone_mode=False, args=["dashboard"])
        elif choice == "q":
            console.print("[bold red]Exiting Mountain Gorilla Command Center. Farewell![/bold red]")
            sys.exit(0)
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")

        console.print("")
        console.print("[bold green]Returning to main menu...[/bold green]")
        time.sleep(1)
        console.clear()

if __name__ == "__main__":
    main_menu()
