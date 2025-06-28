#!/usr/bin/env python
"""
Example usage script for Mountain Gorilla Command Center
Demonstrates the new Silverback-style bot deployment and security features.
"""

import time
from mountain_gorilla.bot_manager import bot_manager
from mountain_gorilla.security import vault_manager, transaction_signer, backup_manager, audit_manager
from mountain_gorilla.dashboard import create_simple_dashboard
from rich.console import Console

console = Console()

def demo_bot_deployment():
    """Demonstrate bot deployment and management"""
    console.print("\n[bold cyan]🤖 Bot Deployment Demo[/bold cyan]")
    console.print("=" * 50)
    
    # Deploy a DCA bot
    console.print("[blue]Deploying ETH DCA bot...[/blue]")
    bot_manager.deploy_bot(
        name="eth_dca_demo",
        strategy="eth-dca",
        risk_level="medium",
        intervals="1h",
        gas_budget=0.01,
        max_position_size=0.1
    )
    
    # Deploy a momentum bot
    console.print("[blue]Deploying momentum trading bot...[/blue]")
    bot_manager.deploy_bot(
        name="momentum_demo",
        strategy="momentum",
        risk_level="high",
        intervals="15m",
        gas_budget=0.02,
        max_position_size=0.2
    )
    
    # List all bots
    console.print("\n[blue]Listing deployed bots:[/blue]")
    bot_manager.list_bots()
    
    # Start a bot
    console.print("\n[blue]Starting ETH DCA bot...[/blue]")
    bot_manager.start_bot("eth_dca_demo")
    
    # Show bot logs
    console.print("\n[blue]Recent bot logs:[/blue]")
    bot_manager.show_bot_logs("eth_dca_demo", limit=5)
    
    # Run market scan
    console.print("\n[blue]Running market scan...[/blue]")
    signals = bot_manager.market_scan("rsi")
    console.print(f"Found {len(signals['signals'])} trading signals")
    
    # Test strategy
    console.print("\n[blue]Testing bot strategy...[/blue]")
    results = bot_manager.test_strategy("eth_dca_demo", dry_run=True)
    console.print(f"Test results: {results['win_rate']:.1%} win rate")

def demo_security_features():
    """Demonstrate security and vault features"""
    console.print("\n[bold cyan]🛡️ Security Features Demo[/bold cyan]")
    console.print("=" * 50)
    
    # Store a private key
    console.print("[blue]Storing private key in vault...[/blue]")
    vault_manager.store_private_key(
        "demo_wallet",
        "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "Demo wallet for testing"
    )
    
    # List wallets
    console.print("\n[blue]Listing stored wallets:[/blue]")
    wallets = vault_manager.list_wallets()
    for wallet in wallets:
        console.print(f"  - {wallet['name']}: {wallet['description']}")
    
    # Create a transaction
    console.print("\n[blue]Creating transaction for approval...[/blue]")
    tx_id = transaction_signer.create_transaction(
        wallet_name="demo_wallet",
        to_address="0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
        value=0.01,
        gas_limit=21000
    )
    
    # List pending transactions
    console.print("\n[blue]Pending transactions:[/blue]")
    transaction_signer.list_pending_transactions()
    
    # Create backup
    console.print("\n[blue]Creating encrypted backup...[/blue]")
    backup_file = backup_manager.create_backup(
        include_vault=True,
        password="demo_password"
    )
    console.print(f"Backup created: {backup_file}")
    
    # Run security audit
    console.print("\n[blue]Running security audit...[/blue]")
    audit_manager.show_audit_report()

def demo_dashboard():
    """Demonstrate dashboard features"""
    console.print("\n[bold cyan]📊 Dashboard Demo[/bold cyan]")
    console.print("=" * 50)
    
    # Show simple dashboard
    console.print("[blue]Portfolio summary:[/blue]")
    create_simple_dashboard()
    
    console.print("\n[blue]Note: For live dashboard, run:[/blue]")
    console.print("python main.py")
    console.print("Then select option 7 for Live Terminal Dashboard")

def main():
    """Run all demos"""
    console.print("[bold green]🦍 Mountain Gorilla Command Center Demo[/bold green]")
    console.print("=" * 60)
    
    try:
        # Bot deployment demo
        demo_bot_deployment()
        time.sleep(2)
        
        # Security features demo
        demo_security_features()
        time.sleep(2)
        
        # Dashboard demo
        demo_dashboard()
        
        console.print("\n[bold green]✅ Demo completed successfully![/bold green]")
        console.print("\n[blue]To explore more features:[/blue]")
        console.print("  python main.py")
        console.print("  python main.py --help")
        
    except Exception as e:
        console.print(f"[bold red]❌ Demo error: {e}[/bold red]")
        console.print("[yellow]Make sure all dependencies are installed:[/yellow]")
        console.print("  pip install -r requirements.txt")

if __name__ == "__main__":
    main() 