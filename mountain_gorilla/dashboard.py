"""
Terminal Dashboard UI / TUI Components for Mountain Gorilla
Live price tickers, position dashboards, bot status monitors, and portfolio growth graphs.
"""

import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.rule import Rule
from rich.columns import Columns
from mountain_gorilla.bot_manager import bot_manager

console = Console()

class LivePriceTicker:
    """Simulates live price data for cryptocurrencies"""
    
    def __init__(self):
        self.prices = {
            "ETH": 3200.0,
            "BTC": 65000.0,
            "USDC": 1.0,
            "WETH": 3200.0,
            "UNI": 12.5,
            "LINK": 18.2
        }
        self.price_history = {token: [] for token in self.prices.keys()}
    
    def update_prices(self):
        """Simulate price movements"""
        for token in self.prices:
            # Simulate realistic price movements
            change = random.uniform(-0.02, 0.02)  # ±2% change
            self.prices[token] *= (1 + change)
            
            # Keep price history for charts
            self.price_history[token].append(self.prices[token])
            if len(self.price_history[token]) > 50:
                self.price_history[token].pop(0)
    
    def get_price_change(self, token: str) -> tuple:
        """Get current price and 24h change"""
        if len(self.price_history[token]) < 2:
            return self.prices[token], 0.0
        
        current = self.prices[token]
        previous = self.price_history[token][-2] if len(self.price_history[token]) > 1 else current
        change_pct = ((current - previous) / previous) * 100
        return current, change_pct

class PortfolioTracker:
    """Tracks portfolio positions and performance"""
    
    def __init__(self):
        self.positions = {
            "ETH": {"amount": 2.5, "avg_price": 3000.0},
            "USDC": {"amount": 5000.0, "avg_price": 1.0},
            "WETH": {"amount": 1.0, "avg_price": 3100.0}
        }
        self.total_value = 0.0
        self.daily_pnl = 0.0
    
    def update_portfolio(self, price_ticker: LivePriceTicker):
        """Update portfolio value based on current prices"""
        self.total_value = 0.0
        for token, position in self.positions.items():
            current_price = price_ticker.prices.get(token, 0)
            position_value = position["amount"] * current_price
            self.total_value += position_value
            
            # Calculate unrealized PnL
            position["unrealized_pnl"] = (current_price - position["avg_price"]) * position["amount"]
        
        # Simulate daily PnL
        self.daily_pnl = random.uniform(-500, 1000)

class GasTracker:
    """Tracks gas fees and optimal transaction windows"""
    
    def __init__(self):
        self.current_gas = 25  # gwei
        self.gas_history = []
    
    def update_gas(self):
        """Simulate gas fee changes"""
        # Simulate realistic gas fee patterns
        change = random.uniform(-5, 10)
        self.current_gas = max(5, min(100, self.current_gas + change))
        self.gas_history.append(self.current_gas)
        
        if len(self.gas_history) > 20:
            self.gas_history.pop(0)
    
    def get_gas_status(self) -> str:
        """Get gas fee status"""
        if self.current_gas < 15:
            return "low"
        elif self.current_gas < 40:
            return "medium"
        else:
            return "high"

class TerminalDashboard:
    """Main terminal dashboard with live updates"""
    
    def __init__(self):
        self.price_ticker = LivePriceTicker()
        self.portfolio = PortfolioTracker()
        self.gas_tracker = GasTracker()
        self.layout = self._create_layout()
    
    def _create_layout(self) -> Layout:
        """Create the dashboard layout"""
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        
        layout["main"].split_row(
            Layout(name="left", ratio=2),
            Layout(name="right", ratio=1)
        )
        
        layout["left"].split_column(
            Layout(name="prices"),
            Layout(name="portfolio")
        )
        
        layout["right"].split_column(
            Layout(name="bots"),
            Layout(name="gas")
        )
        
        return layout
    
    def _create_header(self) -> Panel:
        """Create the header panel"""
        title = Text("🦍 Mountain Gorilla Command Center", style="bold cyan")
        timestamp = Text(f"Last Updated: {datetime.now().strftime('%H:%M:%S')}", style="dim")
        
        return Panel(
            Align.center(Columns([title, timestamp])),
            border_style="magenta"
        )
    
    def _create_price_ticker(self) -> Panel:
        """Create live price ticker"""
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Token", style="cyan")
        table.add_column("Price", style="white")
        table.add_column("24h Change", style="green")
        table.add_column("Status", style="yellow")
        
        for token in ["ETH", "BTC", "USDC", "WETH", "UNI", "LINK"]:
            price, change = self.price_ticker.get_price_change(token)
            
            # Color code the change
            if change > 0:
                change_text = f"[green]+{change:.2f}%[/green]"
                status = "📈"
            elif change < 0:
                change_text = f"[red]{change:.2f}%[/red]"
                status = "📉"
            else:
                change_text = f"[white]{change:.2f}%[/white]"
                status = "➡️"
            
            table.add_row(
                token,
                f"${price:.2f}",
                change_text,
                status
            )
        
        return Panel(table, title="📊 Live Prices", border_style="green")
    
    def _create_portfolio_panel(self) -> Panel:
        """Create portfolio overview"""
        self.portfolio.update_portfolio(self.price_ticker)
        
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Asset", style="cyan")
        table.add_column("Amount", style="white")
        table.add_column("Value", style="green")
        table.add_column("PnL", style="yellow")
        
        for token, position in self.portfolio.positions.items():
            current_price = self.price_ticker.prices.get(token, 0)
            value = position["amount"] * current_price
            pnl = position.get("unrealized_pnl", 0)
            
            pnl_color = "green" if pnl >= 0 else "red"
            pnl_text = f"[{pnl_color}]{pnl:+.2f}[/{pnl_color}]"
            
            table.add_row(
                token,
                f"{position['amount']:.4f}",
                f"${value:.2f}",
                pnl_text
            )
        
        # Add total row
        table.add_row(
            "[bold]TOTAL[/bold]",
            "",
            f"[bold]${self.portfolio.total_value:.2f}[/bold]",
            f"[bold]{'green' if self.portfolio.daily_pnl >= 0 else 'red'}${self.portfolio.daily_pnl:+.2f}[/bold]"
        )
        
        return Panel(table, title="💼 Portfolio", border_style="blue")
    
    def _create_bot_status(self) -> Panel:
        """Create bot status monitor"""
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Bot", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Trades", style="white")
        table.add_column("PnL", style="yellow")
        
        for name, config in bot_manager.bots.items():
            status = bot_manager.statuses.get(name, None)
            if status:
                status_color = {
                    "running": "green",
                    "paused": "yellow",
                    "stopped": "red",
                    "error": "red"
                }.get(status.status, "white")
                
                table.add_row(
                    name,
                    f"[{status_color}]{status.status}[/{status_color}]",
                    str(status.total_trades),
                    f"${status.pnl:.2f}"
                )
        
        if not bot_manager.bots:
            table.add_row("No bots", "deployed", "", "")
        
        return Panel(table, title="🤖 Bot Status", border_style="magenta")
    
    def _create_gas_panel(self) -> Panel:
        """Create gas fee tracker"""
        self.gas_tracker.update_gas()
        gas_status = self.gas_tracker.get_gas_status()
        
        status_color = {
            "low": "green",
            "medium": "yellow",
            "high": "red"
        }.get(gas_status, "white")
        
        gas_text = f"[{status_color}]{self.gas_tracker.current_gas:.1f} gwei[/{status_color}]"
        status_text = f"[{status_color}]{gas_status.upper()}[/{status_color}]"
        
        content = f"""
Current Gas: {gas_text}
Status: {status_text}

Optimal Window: {'Now' if gas_status == 'low' else 'Wait'}
        """
        
        return Panel(content, title="⛽ Gas Tracker", border_style="yellow")
    
    def _create_footer(self) -> Panel:
        """Create footer with quick actions"""
        actions = [
            "[1] Deploy Bot",
            "[2] Market Scan", 
            "[3] Portfolio",
            "[4] Bot Logs",
            "[q] Quit"
        ]
        
        return Panel(
            Align.center(Text(" | ".join(actions), style="dim")),
            border_style="cyan"
        )
    
    def update_dashboard(self) -> Layout:
        """Update all dashboard components"""
        self.price_ticker.update_prices()
        
        self.layout["header"].update(self._create_header())
        self.layout["prices"].update(self._create_price_ticker())
        self.layout["portfolio"].update(self._create_portfolio_panel())
        self.layout["bots"].update(self._create_bot_status())
        self.layout["gas"].update(self._create_gas_panel())
        self.layout["footer"].update(self._create_footer())
        
        return self.layout
    
    def run(self):
        """Run the live dashboard"""
        console.clear()
        console.print("[bold cyan]Starting Mountain Gorilla Dashboard...[/bold cyan]")
        
        with Live(self.update_dashboard(), refresh_per_second=2, screen=True) as live:
            while True:
                try:
                    # Check for user input
                    if console.input_timeout(timeout=0.5) == "q":
                        break
                    
                    # Update dashboard
                    live.update(self.update_dashboard())
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    console.print(f"[red]Dashboard error: {e}[/red]")
                    break
        
        console.print("[bold green]Dashboard closed.[/bold green]")

def create_simple_dashboard():
    """Create a simpler dashboard for the main menu"""
    price_ticker = LivePriceTicker()
    portfolio = PortfolioTracker()
    
    # Update data
    price_ticker.update_prices()
    portfolio.update_portfolio(price_ticker)
    
    # Create summary table
    table = Table(title="🦍 Quick Portfolio Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Total Portfolio Value", f"${portfolio.total_value:.2f}")
    table.add_row("Daily PnL", f"${portfolio.daily_pnl:+.2f}")
    table.add_row("Active Bots", str(len([b for b in bot_manager.statuses.values() if b.status == "running"])))
    table.add_row("ETH Price", f"${price_ticker.prices['ETH']:.2f}")
    
    console.print(table)
    
    # Show recent bot activity
    if bot_manager.bots:
        console.print("\n[bold blue]Recent Bot Activity:[/bold blue]")
        for name, status in list(bot_manager.statuses.items())[:3]:
            console.print(f"  {name}: {status.status} (Last: {status.last_execution[:19]})")

if __name__ == "__main__":
    dashboard = TerminalDashboard()
    dashboard.run() 