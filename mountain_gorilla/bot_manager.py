"""
Silverback-style Bot Deployment Layer for Mountain Gorilla
Manages bot lifecycle, deployment, monitoring, and configuration.
"""

import json
import time
import threading
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align

console = Console()

@dataclass
class BotConfig:
    """Configuration for a trading bot"""
    name: str
    strategy: str
    risk_level: str = "medium"
    intervals: str = "1h"
    token_list: List[str] = None
    gas_budget: float = 0.01
    max_position_size: float = 0.1
    stop_loss: float = 0.05
    take_profit: float = 0.15
    enabled: bool = True
    created_at: str = None
    
    def __post_init__(self):
        if self.token_list is None:
            self.token_list = ["ETH", "USDC", "WETH"]
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

@dataclass
class BotStatus:
    """Current status of a bot"""
    name: str
    status: str  # running, paused, stopped, error
    last_execution: str
    total_trades: int = 0
    pnl: float = 0.0
    current_position: Dict[str, float] = None
    error_message: str = None
    
    def __post_init__(self):
        if self.current_position is None:
            self.current_position = {}

class BotManager:
    """Manages bot deployment, lifecycle, and monitoring"""
    
    def __init__(self, db_path: str = "bots.db"):
        self.db_path = db_path
        self.bots: Dict[str, BotConfig] = {}
        self.statuses: Dict[str, BotStatus] = {}
        self.running_bots: Dict[str, threading.Thread] = {}
        self._init_database()
        self._load_bots()
    
    def _init_database(self):
        """Initialize SQLite database for bot storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Bot configurations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bots (
                name TEXT PRIMARY KEY,
                config TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        
        # Bot execution logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bot_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_name TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                FOREIGN KEY (bot_name) REFERENCES bots (name)
            )
        ''')
        
        # Market data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token TEXT NOT NULL,
                price REAL NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_bots(self):
        """Load existing bots from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, config FROM bots")
        
        for name, config_json in cursor.fetchall():
            config_data = json.loads(config_json)
            self.bots[name] = BotConfig(**config_data)
            self.statuses[name] = BotStatus(
                name=name,
                status="stopped",
                last_execution=datetime.now().isoformat()
            )
        
        conn.close()
    
    def deploy_bot(self, name: str, strategy: str, **kwargs) -> bool:
        """Deploy a new bot with specified strategy"""
        if name in self.bots:
            console.print(f"[red]Bot '{name}' already exists![/red]")
            return False
        
        config = BotConfig(name=name, strategy=strategy, **kwargs)
        self.bots[name] = config
        self.statuses[name] = BotStatus(
            name=name,
            status="stopped",
            last_execution=datetime.now().isoformat()
        )
        
        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bots (name, config, created_at) VALUES (?, ?, ?)",
            (name, json.dumps(asdict(config)), config.created_at)
        )
        conn.commit()
        conn.close()
        
        self._log_action(name, "deployed", f"Strategy: {strategy}")
        console.print(f"[green]Bot '{name}' deployed successfully with {strategy} strategy![/green]")
        return True
    
    def start_bot(self, name: str) -> bool:
        """Start a bot"""
        if name not in self.bots:
            console.print(f"[red]Bot '{name}' not found![/red]")
            return False
        
        if name in self.running_bots and self.running_bots[name].is_alive():
            console.print(f"[yellow]Bot '{name}' is already running![/yellow]")
            return False
        
        config = self.bots[name]
        if not config.enabled:
            console.print(f"[red]Bot '{name}' is disabled![/red]")
            return False
        
        # Start bot thread
        bot_thread = threading.Thread(
            target=self._run_bot,
            args=(name,),
            daemon=True
        )
        bot_thread.start()
        self.running_bots[name] = bot_thread
        self.statuses[name].status = "running"
        
        self._log_action(name, "started", "Bot execution started")
        console.print(f"[green]Bot '{name}' started successfully![/green]")
        return True
    
    def stop_bot(self, name: str) -> bool:
        """Stop a bot"""
        if name not in self.bots:
            console.print(f"[red]Bot '{name}' not found![/red]")
            return False
        
        if name in self.running_bots:
            # In a real implementation, you'd have a stop flag
            self.running_bots.pop(name, None)
        
        self.statuses[name].status = "stopped"
        self._log_action(name, "stopped", "Bot execution stopped")
        console.print(f"[yellow]Bot '{name}' stopped![/yellow]")
        return True
    
    def pause_bot(self, name: str) -> bool:
        """Pause a bot"""
        if name not in self.bots:
            console.print(f"[red]Bot '{name}' not found![/red]")
            return False
        
        self.statuses[name].status = "paused"
        self._log_action(name, "paused", "Bot execution paused")
        console.print(f"[yellow]Bot '{name}' paused![/yellow]")
        return True
    
    def resume_bot(self, name: str) -> bool:
        """Resume a paused bot"""
        if name not in self.bots:
            console.print(f"[red]Bot '{name}' not found![/red]")
            return False
        
        if self.statuses[name].status == "paused":
            self.statuses[name].status = "running"
            self._log_action(name, "resumed", "Bot execution resumed")
            console.print(f"[green]Bot '{name}' resumed![/green]")
            return True
        else:
            console.print(f"[red]Bot '{name}' is not paused![/red]")
            return False
    
    def list_bots(self) -> None:
        """Display all bots and their status"""
        if not self.bots:
            console.print("[yellow]No bots deployed yet![/yellow]")
            return
        
        table = Table(title="🦍 Mountain Gorilla Bots")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Strategy", style="magenta")
        table.add_column("Status", style="green")
        table.add_column("Risk Level", style="yellow")
        table.add_column("Last Execution", style="blue")
        table.add_column("Total Trades", style="white")
        table.add_column("PnL", style="red")
        
        for name, config in self.bots.items():
            status = self.statuses.get(name, BotStatus(name, "unknown", ""))
            status_color = {
                "running": "green",
                "paused": "yellow", 
                "stopped": "red",
                "error": "red"
            }.get(status.status, "white")
            
            table.add_row(
                name,
                config.strategy,
                f"[{status_color}]{status.status}[/{status_color}]",
                config.risk_level,
                status.last_execution[:19] if status.last_execution else "Never",
                str(status.total_trades),
                f"${status.pnl:.2f}"
            )
        
        console.print(table)
    
    def get_bot_logs(self, name: str, limit: int = 50) -> List[Dict]:
        """Get execution logs for a specific bot"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT timestamp, action, details FROM bot_logs WHERE bot_name = ? ORDER BY timestamp DESC LIMIT ?",
            (name, limit)
        )
        
        logs = []
        for timestamp, action, details in cursor.fetchall():
            logs.append({
                "timestamp": timestamp,
                "action": action,
                "details": details
            })
        
        conn.close()
        return logs
    
    def show_bot_logs(self, name: str, limit: int = 20) -> None:
        """Display bot logs in a formatted table"""
        if name not in self.bots:
            console.print(f"[red]Bot '{name}' not found![/red]")
            return
        
        logs = self.get_bot_logs(name, limit)
        if not logs:
            console.print(f"[yellow]No logs found for bot '{name}'[/yellow]")
            return
        
        table = Table(title=f"📋 Logs for {name}")
        table.add_column("Timestamp", style="cyan")
        table.add_column("Action", style="magenta")
        table.add_column("Details", style="white")
        
        for log in logs:
            table.add_row(
                log["timestamp"][:19],
                log["action"],
                log["details"] or ""
            )
        
        console.print(table)
    
    def configure_bot(self, name: str, **kwargs) -> bool:
        """Update bot configuration"""
        if name not in self.bots:
            console.print(f"[red]Bot '{name}' not found![/red]")
            return False
        
        config = self.bots[name]
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        # Update database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE bots SET config = ? WHERE name = ?",
            (json.dumps(asdict(config)), name)
        )
        conn.commit()
        conn.close()
        
        self._log_action(name, "configured", f"Updated: {', '.join(kwargs.keys())}")
        console.print(f"[green]Bot '{name}' configuration updated![/green]")
        return True
    
    def market_scan(self, strategy: str = "rsi") -> Dict[str, Any]:
        """Run market analysis and return signals"""
        console.print(f"[blue]Running {strategy.upper()} market scan...[/blue]")
        
        # Simulate market data analysis
        signals = {
            "timestamp": datetime.now().isoformat(),
            "strategy": strategy,
            "signals": [
                {
                    "token": "ETH",
                    "signal": "BUY",
                    "strength": 0.8,
                    "reason": "RSI oversold, bullish divergence"
                },
                {
                    "token": "USDC",
                    "signal": "HOLD",
                    "strength": 0.3,
                    "reason": "Stable coin, minimal volatility"
                }
            ],
            "market_conditions": {
                "volatility": "medium",
                "trend": "bullish",
                "gas_fees": "low"
            }
        }
        
        return signals
    
    def test_strategy(self, name: str, dry_run: bool = True) -> Dict[str, Any]:
        """Test bot strategy with historical data"""
        if name not in self.bots:
            console.print(f"[red]Bot '{name}' not found![/red]")
            return {}
        
        config = self.bots[name]
        console.print(f"[blue]Testing {name} strategy ({config.strategy})...[/blue]")
        
        # Simulate backtesting results
        results = {
            "bot_name": name,
            "strategy": config.strategy,
            "test_period": "30 days",
            "total_trades": 45,
            "win_rate": 0.67,
            "total_pnl": 0.23,
            "max_drawdown": -0.08,
            "sharpe_ratio": 1.45,
            "dry_run": dry_run
        }
        
        return results
    
    def _run_bot(self, name: str):
        """Internal method to run bot logic"""
        config = self.bots[name]
        status = self.statuses[name]
        
        while status.status == "running":
            try:
                # Simulate bot execution
                if config.strategy == "eth-dca":
                    self._execute_dca_strategy(name, config)
                elif config.strategy == "momentum":
                    self._execute_momentum_strategy(name, config)
                else:
                    self._execute_generic_strategy(name, config)
                
                status.last_execution = datetime.now().isoformat()
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                status.status = "error"
                status.error_message = str(e)
                self._log_action(name, "error", str(e))
                break
    
    def _execute_dca_strategy(self, name: str, config: BotConfig):
        """Execute Dollar Cost Averaging strategy"""
        # Simulate DCA execution
        amount = config.max_position_size * 0.1  # 10% of max position
        self._log_action(name, "dca_execution", f"Bought {amount} ETH at market price")
        self.statuses[name].total_trades += 1
    
    def _execute_momentum_strategy(self, name: str, config: BotConfig):
        """Execute momentum trading strategy"""
        # Simulate momentum analysis and execution
        self._log_action(name, "momentum_analysis", "Analyzing price momentum")
        self.statuses[name].total_trades += 1
    
    def _execute_generic_strategy(self, name: str, config: BotConfig):
        """Execute generic strategy"""
        self._log_action(name, "strategy_execution", f"Executing {config.strategy}")
        self.statuses[name].total_trades += 1
    
    def _log_action(self, bot_name: str, action: str, details: str = None):
        """Log bot action to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bot_logs (bot_name, timestamp, action, details) VALUES (?, ?, ?, ?)",
            (bot_name, datetime.now().isoformat(), action, details)
        )
        conn.commit()
        conn.close()

# Global bot manager instance
bot_manager = BotManager() 