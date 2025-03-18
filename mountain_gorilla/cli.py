"""
CLI command definitions using the 'click' library.
"""

import click
from mountain_gorilla.command_center import CommandCenter

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
    from mountain_gorilla import __version__
    click.echo(f"Mountain Gorilla Command Center (MGCC) Version: {__version__}")
