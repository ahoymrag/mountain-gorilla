"""
CLI command definitions using the 'click' library, with a fun animated dashboard.
"""

import time
import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
from rich.table import Table
from mountain_gorilla.command_center import CommandCenter
from mountain_gorilla.bot_manager import bot_manager
from mountain_gorilla.security import vault_manager, transaction_signer, backup_manager, audit_manager
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

# Bot Deployment Layer Commands
@mgcc_cli.group()
def bots():
    """Manage Silverback-style trading bots."""
    pass

@bots.command()
@click.option("--name", required=True, help="Bot name")
@click.option("--strategy", required=True, help="Trading strategy (eth-dca, momentum, etc.)")
@click.option("--risk-level", default="medium", help="Risk level (low, medium, high)")
@click.option("--intervals", default="1h", help="Trading intervals")
@click.option("--gas-budget", default=0.01, type=float, help="Gas budget in ETH")
@click.option("--max-position", default=0.1, type=float, help="Maximum position size")
def deploy(name, strategy, risk_level, intervals, gas_budget, max_position):
    """Deploy a new trading bot."""
    success = bot_manager.deploy_bot(
        name=name,
        strategy=strategy,
        risk_level=risk_level,
        intervals=intervals,
        gas_budget=gas_budget,
        max_position_size=max_position
    )
    if success:
        console.print(f"[green]✅ Bot '{name}' deployed successfully![/green]")

@bots.command()
def list():
    """List all deployed bots and their status."""
    bot_manager.list_bots()

@bots.command()
@click.argument("bot_name")
@click.option("--limit", default=20, help="Number of log entries to show")
def log(bot_name, limit):
    """View bot execution logs."""
    bot_manager.show_bot_logs(bot_name, limit)

@bots.command()
@click.argument("bot_name")
def start(bot_name):
    """Start a bot."""
    bot_manager.start_bot(bot_name)

@bots.command()
@click.argument("bot_name")
def stop(bot_name):
    """Stop a bot."""
    bot_manager.stop_bot(bot_name)

@bots.command()
@click.argument("bot_name")
def pause(bot_name):
    """Pause a bot."""
    bot_manager.pause_bot(bot_name)

@bots.command()
@click.argument("bot_name")
def resume(bot_name):
    """Resume a paused bot."""
    bot_manager.resume_bot(bot_name)

@bots.command()
@click.argument("bot_name")
def kill(bot_name):
    """Kill a bot (force stop)."""
    bot_manager.stop_bot(bot_name)

@bots.command()
@click.argument("bot_name")
@click.option("--risk-level", help="Set risk level")
@click.option("--intervals", help="Set trading intervals")
@click.option("--gas-budget", type=float, help="Set gas budget")
@click.option("--max-position", type=float, help="Set max position size")
@click.option("--stop-loss", type=float, help="Set stop loss percentage")
@click.option("--take-profit", type=float, help="Set take profit percentage")
def config(bot_name, risk_level, intervals, gas_budget, max_position, stop_loss, take_profit):
    """Configure bot parameters."""
    config_updates = {}
    if risk_level:
        config_updates["risk_level"] = risk_level
    if intervals:
        config_updates["intervals"] = intervals
    if gas_budget:
        config_updates["gas_budget"] = gas_budget
    if max_position:
        config_updates["max_position_size"] = max_position
    if stop_loss:
        config_updates["stop_loss"] = stop_loss
    if take_profit:
        config_updates["take_profit"] = take_profit
    
    if config_updates:
        bot_manager.configure_bot(bot_name, **config_updates)
    else:
        console.print("[yellow]No configuration parameters provided. Use --help for options.[/yellow]")

@bots.command()
@click.option("--strategy", default="rsi", help="Market scan strategy")
def market_scan(strategy):
    """Run market analysis and return trading signals."""
    signals = bot_manager.market_scan(strategy)
    
    table = Table(title=f"📊 Market Scan Results ({strategy.upper()})")
    table.add_column("Token", style="cyan")
    table.add_column("Signal", style="magenta")
    table.add_column("Strength", style="yellow")
    table.add_column("Reason", style="white")
    
    for signal in signals["signals"]:
        signal_color = {
            "BUY": "green",
            "SELL": "red",
            "HOLD": "yellow"
        }.get(signal["signal"], "white")
        
        table.add_row(
            signal["token"],
            f"[{signal_color}]{signal['signal']}[/{signal_color}]",
            f"{signal['strength']:.2f}",
            signal["reason"]
        )
    
    console.print(table)
    
    # Market conditions
    conditions = signals["market_conditions"]
    console.print(f"\n[blue]Market Conditions:[/blue]")
    console.print(f"  Volatility: {conditions['volatility']}")
    console.print(f"  Trend: {conditions['trend']}")
    console.print(f"  Gas Fees: {conditions['gas_fees']}")

@bots.command()
@click.argument("bot_name")
@click.option("--dry-run", is_flag=True, default=True, help="Run in dry-run mode")
def test(bot_name, dry_run):
    """Test bot strategy with historical data."""
    results = bot_manager.test_strategy(bot_name, dry_run)
    
    if not results:
        return
    
    table = Table(title=f"🧪 Strategy Test Results: {bot_name}")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Strategy", results["strategy"])
    table.add_row("Test Period", results["test_period"])
    table.add_row("Total Trades", str(results["total_trades"]))
    table.add_row("Win Rate", f"{results['win_rate']:.2%}")
    table.add_row("Total PnL", f"${results['total_pnl']:.2f}")
    table.add_row("Max Drawdown", f"{results['max_drawdown']:.2%}")
    table.add_row("Sharpe Ratio", f"{results['sharpe_ratio']:.2f}")
    table.add_row("Dry Run", "✅" if results["dry_run"] else "❌")
    
    console.print(table)

# Security Commands
@mgcc_cli.group()
def vault():
    """Manage secure wallet storage."""
    pass

@vault.command()
@click.option("--name", required=True, help="Wallet name")
@click.option("--key", required=True, help="Private key")
@click.option("--description", help="Wallet description")
def store(name, key, description):
    """Store a private key securely in the vault."""
    vault_manager.store_private_key(name, key, description or "")

@vault.command()
@click.option("--name", required=True, help="Wallet name")
def get(name):
    """Retrieve a private key from the vault."""
    private_key = vault_manager.get_private_key(name)
    if private_key:
        console.print(f"[green]Private key retrieved for '{name}'[/green]")

@vault.command()
def list():
    """List all wallets in the vault."""
    wallets = vault_manager.list_wallets()
    
    if not wallets:
        console.print("[yellow]No wallets found in vault[/yellow]")
        return
    
    table = Table(title="🔐 Vault Wallets")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="magenta")
    table.add_column("Created", style="blue")
    table.add_column("Last Accessed", style="green")
    
    for wallet in wallets:
        table.add_row(
            wallet["name"],
            wallet["description"],
            wallet["created_at"][:19],
            wallet["last_accessed"][:19]
        )
    
    console.print(table)

@vault.command()
@click.option("--name", required=True, help="Wallet name")
def remove(name):
    """Remove a wallet from vault."""
    vault_manager.remove_wallet(name)

@mgcc_cli.group()
def sign():
    """Manage transaction signing and approval."""
    pass

@sign.command()
@click.option("--wallet", required=True, help="Wallet name")
@click.option("--to", required=True, help="Recipient address")
@click.option("--value", required=True, type=float, help="Amount in ETH")
@click.option("--gas", default=21000, help="Gas limit")
@click.option("--data", default="", help="Transaction data")
def create(wallet, to, value, gas, data):
    """Create a new transaction for approval."""
    tx_id = transaction_signer.create_transaction(wallet, to, value, gas, data)
    console.print(f"[green]Transaction {tx_id} created[/green]")

@sign.command()
def pending():
    """List pending transactions."""
    transaction_signer.list_pending_transactions()

@sign.command()
@click.option("--tx-id", required=True, help="Transaction ID")
def approve(tx_id):
    """Approve and sign a transaction."""
    transaction_signer.approve_transaction(tx_id)

@sign.command()
@click.option("--tx-id", required=True, help="Transaction ID")
def reject(tx_id):
    """Reject a pending transaction."""
    transaction_signer.reject_transaction(tx_id)

@mgcc_cli.group()
def backup():
    """Manage system backup and restore."""
    pass

@backup.command()
@click.option("--include-vault", is_flag=True, default=True, help="Include vault in backup")
@click.option("--password", help="Encrypt backup with password")
def create(include_vault, password):
    """Create a system backup."""
    backup_file = backup_manager.create_backup(include_vault, password)
    if backup_file:
        console.print(f"[green]Backup created: {backup_file}[/green]")

@backup.command()
@click.option("--file", required=True, help="Backup file path")
@click.option("--password", help="Backup password")
def restore(file, password):
    """Restore system from backup."""
    backup_manager.restore_backup(file, password)

@mgcc_cli.command()
def audit():
    """Run security audit on contract approvals."""
    audit_manager.show_audit_report()

def animate_banner(text: str, delay: float = 0.001) -> None:
    """
    Print a string character-by-character with a very small delay to simulate animation.
    Speed increased by 2000% (from 0.05 to 0.001).
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
    animate_banner("Welcome to the Mountain Gorilla Command Center!", delay=0.001)
    time.sleep(0.2)  # Reduced wait time

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
    time.sleep(0.5)  # Reduced wait time

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
                    "  [5] Bot Management\n"
                    "  [6] Market Analysis\n"
                    "  [7] Security & Vault\n"
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
        elif choice == "5":
            console.print("[bold blue]Bot Management Options:[/bold blue]")
            console.print("  [1] List Trading Bots")
            console.print("  [2] Deploy New Bot")
            console.print("  [3] Start/Stop Bot")
            console.print("  [4] View Bot Logs")
            console.print("  [5] Configure Bot")
            console.print("  [Enter] Return to Main Menu")
            bot_choice = console.input("[bold yellow]Bot action[/]: ")
            
            if bot_choice == "1":
                bot_manager.list_bots()
            elif bot_choice == "2":
                name = console.input("Bot name: ")
                strategy = console.input("Strategy (eth-dca, momentum): ")
                bot_manager.deploy_bot(name, strategy)
            elif bot_choice == "3":
                name = console.input("Bot name: ")
                action = console.input("Action (start/stop/pause/resume): ")
                if action == "start":
                    bot_manager.start_bot(name)
                elif action == "stop":
                    bot_manager.stop_bot(name)
                elif action == "pause":
                    bot_manager.pause_bot(name)
                elif action == "resume":
                    bot_manager.resume_bot(name)
            elif bot_choice == "4":
                name = console.input("Bot name: ")
                bot_manager.show_bot_logs(name)
            elif bot_choice == "5":
                name = console.input("Bot name: ")
                risk = console.input("Risk level (low/medium/high): ")
                if risk:
                    bot_manager.configure_bot(name, risk_level=risk)
            elif bot_choice == "" or bot_choice == "back" or bot_choice == "b":
                continue
        elif choice == "6":
            console.print("[bold blue]Market Analysis:[/bold blue]")
            console.print("  [1] Market Scan")
            console.print("  [2] Test Strategy")
            console.print("  [Enter] Return to Main Menu")
            market_choice = console.input("[bold yellow]Analysis type[/]: ")
            
            if market_choice == "1":
                strategy = console.input("Strategy (rsi, momentum): ") or "rsi"
                bot_manager.market_scan(strategy)
            elif market_choice == "2":
                name = console.input("Bot name: ")
                bot_manager.test_strategy(name)
            elif market_choice == "" or market_choice == "back" or market_choice == "b":
                continue
        elif choice == "7":
            console.print("[bold blue]Security & Vault:[/bold blue]")
            console.print("  [1] List Wallets")
            console.print("  [2] Store Private Key")
            console.print("  [3] Create Backup")
            console.print("  [4] Security Audit")
            console.print("  [Enter] Return to Main Menu")
            security_choice = console.input("[bold yellow]Security action[/]: ")
            
            if security_choice == "1":
                vault_manager.list_wallets()
            elif security_choice == "2":
                name = console.input("Wallet name: ")
                key = console.input("Private key: ")
                desc = console.input("Description (optional): ")
                vault_manager.store_private_key(name, key, desc)
            elif security_choice == "3":
                include_vault = console.input("Include vault? (y/n): ").lower() == 'y'
                password = console.input("Password (optional): ") or None
                backup_manager.create_backup(include_vault, password)
            elif security_choice == "4":
                audit_manager.show_audit_report()
            elif security_choice == "" or security_choice == "back" or security_choice == "b":
                continue
        elif choice.lower() == "q":
            console.print("[bold red]Exiting dashboard...[/bold red]")
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")
            console.print("[bold blue]Type 'q' to quit or select a valid option[/bold blue]")

        if choice.lower() != "q":
            console.print("")
            console.print("[bold green]Action complete! Returning to dashboard...[/bold green]")
            time.sleep(0.5)  # Reduced wait time
            console.clear()
            animate_banner("Welcome back to the Mountain Gorilla Command Center!", delay=0.001)
            console.print(Panel.fit(gorilla_face, title="MGCC Dashboard", border_style="magenta"))
            time.sleep(0.2)  # Reduced wait time
