"""
CLI command definitions using the 'click' library, with a fun animated dashboard.
"""

import time
import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
from mountain_gorilla.command_center import CommandCenter
from mountain_gorilla import __version__

console = Console()

@click.group()
def mgcc_cli():
    """Mountain Gorilla Command Center (MGCC) - Manage your ASCII-based AI Bots."""
    pass

@mgcc_cli.command()
def list():
    """List all available bots."""
    CommandCenter.list_bots()

@mgcc_cli.command()
@click.argument("bot_name")
def summon(bot_name):
    """
    Summon a bot by name.
    Example: python main.py summon MemoriBot
    """
    CommandCenter.summon(bot_name)

@mgcc_cli.command()
@click.argument("bot_name")
def train(bot_name):
    """
    Train (level up) a bot by name.
    Example: python main.py train FinanBot
    """
    CommandCenter.train(bot_name)

@mgcc_cli.command()
def version():
    """Show MGCC version info."""
    console.print(f"[bold magenta]Mountain Gorilla Command Center (MGCC) Version:[/bold magenta] {__version__}")

def animate_banner(text: str, delay: float = 0.05) -> None:
    """
    Print a string character-by-character with a small delay to simulate animation.
    """
    for char in text:
        console.print(char, end="", style="bold cyan")
        time.sleep(delay)
    console.print()  # Move to the next line

@mgcc_cli.command()
def dashboard():
    """
    Displays a beautiful, animated terminal dashboard.
    Press 1-9 to navigate commands. Press q to quit.
    """
    console.clear()
    animate_banner("Welcome to the Mountain Gorilla Command Center!")
    time.sleep(0.5)

    # Simple ASCII art gorilla face (feel free to replace with something even fancier):
    gorilla_face = Text("""
          .-"-.
         /|6 6|\\
         \\|_-_/|
         //   \\ \\
        ((     ))
         \\\\___//
          '-^-'
    """, style=Style(color="white", bold=True))

    console.print(Panel.fit(gorilla_face, title="MGCC Dashboard", border_style="magenta"))
    time.sleep(1.0)

    choice = None
    while choice != "q":
        console.print(
            Panel(
                Text(
                    "Please select an action:\n"
                    "  [1] List all Bots\n"
                    "  [2] Summon a Bot\n"
                    "  [3] Train a Bot\n"
                    "  [4] Show MGCC Version\n"
                    "  [q] Quit\n",
                    style="cyan"
                ),
                border_style="green",
            )
        )
        choice = console.input("[bold yellow]Your choice[/]: ")

        if choice == "1":
            console.print("[bold magenta]Listing all bots...[/]")
            CommandCenter.list_bots()
        elif choice == "2":
            bot_name = console.input("[bold magenta]Enter the bot name to summon[/]: ")
            CommandCenter.summon(bot_name)
        elif choice == "3":
            bot_name = console.input("[bold magenta]Enter the bot name to train[/]: ")
            CommandCenter.train(bot_name)
        elif choice == "4":
            console.print(f"[bold magenta]MGCC Version:[/bold magenta] {__version__}")
        elif choice.lower() == "q":
            console.print("[bold red]Exiting dashboard...[/bold red]")
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")

        if choice.lower() != "q":
            console.print("")
            console.print("[bold green]Action complete! Returning to dashboard...[/bold green]")
            time.sleep(1)
            console.clear()
            animate_banner("Welcome back to the Mountain Gorilla Command Center!")
            console.print(Panel.fit(gorilla_face, title="MGCC Dashboard", border_style="magenta"))
            time.sleep(0.5)
