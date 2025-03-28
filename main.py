#!/usr/bin/env python
"""
Entry point script for the Mountain Gorilla Command Center CLI.
After placing all files in the recommended structure, simply run:
  python main.py
from the 'mountain-gorilla' folder to start the CLI.

This enhanced version transforms the MGCC into a playful fintech-like program,
letting you check balances, see how much you are spending, and adopt strategies
—all in a dramatic ASCII-driven terminal UI.
"""

import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
from rich.live import Live
from rich.table import Table
from mountain_gorilla.cli import mgcc_cli

console = Console()

def animate_banner(text: str, delay: float = 0.03) -> None:
    """
    Print a string character-by-character with a small delay for a typing-like animation.
    """
    for char in text:
        console.print(char, end="", style="bold magenta")
        time.sleep(delay)
    console.print()  # Move to the next line

def show_ascii_title():
    """
    Display a large, bordered ASCII title reading 'MOUNTAIN GORILLA'.
    """
    title = r"""
Mountain Gorilla
    """
    console.print(Text(title, style=Style(color="cyan", bold=True)))

def finance_portal():
    """
    A mock fintech-like menu for viewing balances, spending, and adopting strategies,
    shown directly in the terminal UI. This is just a placeholder for illustration.
    """
    console.clear()
    show_ascii_title()
    animate_banner("MOUNTAIN GORILLA FINANCE PORTAL\n", delay=0.02)

    console.print(
        Panel(
            "[bold green]Welcome to the MGCC Finance Portal![/bold green]\n"
            "Here, you can view your balance, track your spending, and adopt\n"
            "various budgeting or investment strategies.\n\n"
            "[bold]Select an action below:[/bold]\n"
            "  [1] Check Balance\n"
            "  [2] Show Monthly Spending\n"
            "  [3] Adopt a Strategy\n"
            "  [r] Return to Main Menu\n",
            border_style="magenta",
            title="Finance Portal",
        )
    )

    while True:
        choice = console.input("[bold yellow]Finance Action[/]: ").strip().lower()
        if choice == "1":
            console.print("[bold cyan]Your current balance is: $3,141.59[/bold cyan]")
        elif choice == "2":
            console.print("[bold cyan]Current monthly spending: $314.15[/bold cyan]")
        elif choice == "3":
            console.print("[bold cyan]Strategy adopted! Plan: 'Aggressive Gorilla Growth'[/bold cyan]")
        elif choice == "r":
            break
        else:
            console.print("[bold red]Invalid choice. Please try again![/bold red]")

        console.print("[bold green]Action complete![/bold green]\n")
        time.sleep(1)
    console.print("[bold blue]Returning to the MGCC Main Menu...[/bold blue]")
    time.sleep(1)

def tutorial_sequence():
    """
    A fun tutorial sequence for an example. Demonstrates how to animate ASCII art
    for each bot, including newly introduced finance concepts.
    """
    console.clear()
    animate_banner("[bold cyan]MOUNTAIN GORILLA TUTORIAL[/bold cyan]\n", delay=0.02)
    show_ascii_title()
    console.print(Panel("[bold magenta]Welcome to the MGCC Tutorial![/bold magenta]", border_style="magenta"))
    time.sleep(1.0)

    with Live(refresh_per_second=4) as live:
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Bot Name", style="bold yellow")
        table.add_column("ASCII Art", style="bold green")
        table.title = "[bold purple]Mountain Gorilla Bots[/bold purple]"
        table.caption = "[italic]Showcasing each of your magnificent ASCII bots![/italic]"

        # Bot #1: MemoriBot
        memori_ascii = r"""
        /^^\   <( I'm MemoriBot! )
        (  @ @ )         I remember everything you taught me...
         (  __  )
        """
        table.add_row("[bold magenta]MemoriBot[/bold magenta]", f"[white]{memori_ascii}[/white]")
        live.update(table)
        time.sleep(2.5)

        # Bot #2: FinanBot
        finan_ascii = r"""
           __
          /  \--_  <( I'm FinanBot! )
          \__/  \    Let me handle your finances...
          (    )
        """
        table.add_row("[bold magenta]FinanBot[/bold magenta]", f"[white]{finan_ascii}[/white]")
        live.update(table)
        time.sleep(2.5)

        # Bot #3: ChronoBot
        chrono_ascii = """
          .-\"\"\"-.
         /       \\   <( I'm ChronoBot! )
         | (@) (@) |   I'll keep perfect time for your events...
         \\   ^   /
          '-...-'
        """
        table.add_row("[bold magenta]ChronoBot[/bold magenta]", f"[white]{chrono_ascii}[/white]")
        live.update(table)
        time.sleep(2.5)

    console.print("[bold green]\nTutorial Complete![/bold green]")
    console.print("Use the MGCC main menu to [bold cyan]Summon, Train, or Interact[/bold cyan] with each bot.\n")
    console.print("[bold blue]Returning to the main menu shortly...[/bold blue]")
    time.sleep(2)

def main_menu():
    """
    Immediately display a dramatic introduction and show a menu of MGCC actions,
    including a basic "Finance Portal" for checking balance, spending,
    adopting strategies, plus a 'Tutorial' option for an animated in-terminal overview.
    """
    console.clear()
    show_ascii_title()
    animate_banner("Welcome to the Mountain Gorilla Command Center!\n", delay=0.02)
    time.sleep(0.5)

    while True:
        console.print(
            Panel(
                Text(
                    "[1] List all Bots\n"
                    "[2] Summon a Bot\n"
                    "[3] Train a Bot\n"
                    "[4] Show MGCC Version\n"
                    "[5] Launch Dashboard\n"
                    "[6] Finance Portal\n"
                    "[T] Tutorial\n"
                    "[q] Quit\n",
                    style="bold cyan"
                ),
                title="MGCC Main Menu",
                border_style="magenta"
            )
        )

        choice = console.input("[bold yellow]Your choice[/]: ").strip().lower()

        if choice == "1":
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
        elif choice == "6":
            finance_portal()
        elif choice == "t":
            tutorial_sequence()
        elif choice == "q":
            console.print("[bold red]Exiting Mountain Gorilla Command Center. Farewell![/bold red]")
            sys.exit(0)
        else:
            console.print("[bold red]Invalid choice. Please try again![/bold red]")

        console.print("")
        console.print("[bold green]Returning to main menu...[/bold green]")
        time.sleep(1)
        console.clear()
        show_ascii_title()
        animate_banner("Welcome back to the Mountain Gorilla Command Center!", delay=0.02)
        console.print()

if __name__ == "__main__":
    main_menu()
