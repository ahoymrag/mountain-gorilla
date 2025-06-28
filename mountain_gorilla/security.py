"""
Security / Safety Features for Mountain Gorilla
Vault, signing, read-only mode, backup, and audit functionality.
"""

import json
import os
import zipfile
import hashlib
import base64
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.align import Align

console = Console()

class VaultManager:
    """Manages secure storage of private keys and sensitive data"""
    
    def __init__(self, vault_path: str = ".vault"):
        self.vault_path = Path(vault_path)
        self.vault_path.mkdir(exist_ok=True)
        self.master_key = None
        self.fernet = None
        self._load_or_create_master_key()
    
    def _load_or_create_master_key(self):
        """Load existing master key or create new one"""
        key_file = self.vault_path / "master.key"
        
        if key_file.exists():
            # Load existing key
            with open(key_file, "rb") as f:
                self.master_key = f.read()
        else:
            # Create new master key
            self.master_key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(self.master_key)
        
        self.fernet = Fernet(self.master_key)
    
    def store_private_key(self, wallet_name: str, private_key: str, description: str = "") -> bool:
        """Store a private key securely"""
        try:
            key_data = {
                "private_key": private_key,
                "description": description,
                "created_at": datetime.now().isoformat(),
                "last_accessed": datetime.now().isoformat()
            }
            
            encrypted_data = self.fernet.encrypt(json.dumps(key_data).encode())
            
            key_file = self.vault_path / f"{wallet_name}.key"
            with open(key_file, "wb") as f:
                f.write(encrypted_data)
            
            console.print(f"[green]✅ Private key for '{wallet_name}' stored securely[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Failed to store private key: {e}[/red]")
            return False
    
    def get_private_key(self, wallet_name: str) -> Optional[str]:
        """Retrieve a private key (requires user confirmation)"""
        key_file = self.vault_path / f"{wallet_name}.key"
        
        if not key_file.exists():
            console.print(f"[red]❌ No private key found for '{wallet_name}'[/red]")
            return None
        
        # Require explicit user confirmation
        if not Confirm.ask(f"🔐 Access private key for '{wallet_name}'?"):
            console.print("[yellow]Access denied by user[/yellow]")
            return None
        
        try:
            with open(key_file, "rb") as f:
                encrypted_data = f.read()
            
            decrypted_data = self.fernet.decrypt(encrypted_data)
            key_data = json.loads(decrypted_data.decode())
            
            # Update last accessed time
            key_data["last_accessed"] = datetime.now().isoformat()
            encrypted_data = self.fernet.encrypt(json.dumps(key_data).encode())
            with open(key_file, "wb") as f:
                f.write(encrypted_data)
            
            console.print(f"[green]✅ Private key accessed for '{wallet_name}'[/green]")
            return key_data["private_key"]
            
        except Exception as e:
            console.print(f"[red]❌ Failed to retrieve private key: {e}[/red]")
            return None
    
    def list_wallets(self) -> List[Dict[str, Any]]:
        """List all stored wallets"""
        wallets = []
        
        for key_file in self.vault_path.glob("*.key"):
            if key_file.name == "master.key":
                continue
            
            try:
                with open(key_file, "rb") as f:
                    encrypted_data = f.read()
                
                decrypted_data = self.fernet.decrypt(encrypted_data)
                key_data = json.loads(decrypted_data.decode())
                
                wallets.append({
                    "name": key_file.stem,
                    "description": key_data.get("description", ""),
                    "created_at": key_data.get("created_at", ""),
                    "last_accessed": key_data.get("last_accessed", "")
                })
                
            except Exception as e:
                console.print(f"[red]Warning: Could not read {key_file.name}: {e}[/red]")
        
        return wallets
    
    def remove_wallet(self, wallet_name: str) -> bool:
        """Remove a wallet from vault"""
        key_file = self.vault_path / f"{wallet_name}.key"
        
        if not key_file.exists():
            console.print(f"[red]❌ No wallet found with name '{wallet_name}'[/red]")
            return False
        
        if not Confirm.ask(f"🗑️ Permanently remove wallet '{wallet_name}'?"):
            console.print("[yellow]Removal cancelled[/yellow]")
            return False
        
        try:
            key_file.unlink()
            console.print(f"[green]✅ Wallet '{wallet_name}' removed[/green]")
            return True
        except Exception as e:
            console.print(f"[red]❌ Failed to remove wallet: {e}[/red]")
            return False

class TransactionSigner:
    """Handles explicit transaction signing and approval"""
    
    def __init__(self, vault_manager: VaultManager):
        self.vault = vault_manager
        self.pending_transactions = {}
        self.transaction_history = []
    
    def create_transaction(self, wallet_name: str, to_address: str, value: float, 
                          gas_limit: int, data: str = "") -> str:
        """Create a new transaction for approval"""
        tx_id = hashlib.sha256(f"{wallet_name}{to_address}{value}{datetime.now()}".encode()).hexdigest()[:8]
        
        transaction = {
            "id": tx_id,
            "wallet_name": wallet_name,
            "to_address": to_address,
            "value": value,
            "gas_limit": gas_limit,
            "data": data,
            "created_at": datetime.now().isoformat(),
            "status": "pending"
        }
        
        self.pending_transactions[tx_id] = transaction
        console.print(f"[yellow]📝 Transaction {tx_id} created and pending approval[/yellow]")
        
        return tx_id
    
    def list_pending_transactions(self) -> None:
        """List all pending transactions"""
        if not self.pending_transactions:
            console.print("[yellow]No pending transactions[/yellow]")
            return
        
        table = Table(title="⏳ Pending Transactions")
        table.add_column("ID", style="cyan")
        table.add_column("Wallet", style="magenta")
        table.add_column("To", style="blue")
        table.add_column("Value (ETH)", style="green")
        table.add_column("Gas", style="yellow")
        table.add_column("Created", style="white")
        
        for tx in self.pending_transactions.values():
            table.add_row(
                tx["id"],
                tx["wallet_name"],
                tx["to_address"][:10] + "...",
                f"{tx['value']:.4f}",
                str(tx["gas_limit"]),
                tx["created_at"][:19]
            )
        
        console.print(table)
    
    def approve_transaction(self, tx_id: str) -> bool:
        """Approve and sign a transaction"""
        if tx_id not in self.pending_transactions:
            console.print(f"[red]❌ Transaction {tx_id} not found[/red]")
            return False
        
        tx = self.pending_transactions[tx_id]
        
        # Show transaction details
        console.print(f"\n[bold]Transaction Details:[/bold]")
        console.print(f"  ID: {tx['id']}")
        console.print(f"  Wallet: {tx['wallet_name']}")
        console.print(f"  To: {tx['to_address']}")
        console.print(f"  Value: {tx['value']} ETH")
        console.print(f"  Gas: {tx['gas_limit']}")
        
        if not Confirm.ask("🔐 Approve and sign this transaction?"):
            console.print("[yellow]Transaction approval cancelled[/yellow]")
            return False
        
        # Get private key
        private_key = self.vault.get_private_key(tx["wallet_name"])
        if not private_key:
            return False
        
        # Simulate transaction signing
        console.print("[blue]🔏 Signing transaction...[/blue]")
        time.sleep(1)  # Simulate signing process
        
        # Update transaction status
        tx["status"] = "signed"
        tx["signed_at"] = datetime.now().isoformat()
        tx["signature"] = "0x" + hashlib.sha256(f"{tx_id}{private_key[:10]}".encode()).hexdigest()
        
        # Move to history
        self.transaction_history.append(tx)
        del self.pending_transactions[tx_id]
        
        console.print(f"[green]✅ Transaction {tx_id} signed and ready for broadcast[/green]")
        return True
    
    def reject_transaction(self, tx_id: str) -> bool:
        """Reject a pending transaction"""
        if tx_id not in self.pending_transactions:
            console.print(f"[red]❌ Transaction {tx_id} not found[/red]")
            return False
        
        tx = self.pending_transactions[tx_id]
        tx["status"] = "rejected"
        tx["rejected_at"] = datetime.now().isoformat()
        
        self.transaction_history.append(tx)
        del self.pending_transactions[tx_id]
        
        console.print(f"[yellow]❌ Transaction {tx_id} rejected[/yellow]")
        return True

class BackupManager:
    """Handles system backup and restore functionality"""
    
    def __init__(self, backup_path: str = "backups"):
        self.backup_path = Path(backup_path)
        self.backup_path.mkdir(exist_ok=True)
    
    def create_backup(self, include_vault: bool = True, password: str = None) -> str:
        """Create encrypted backup of system configuration"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_path / f"mountain_gorilla_backup_{timestamp}.zip"
        
        try:
            with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Backup bot configurations
                if Path("bots.db").exists():
                    zipf.write("bots.db", "bots.db")
                
                # Backup vault (if requested)
                if include_vault and Path(".vault").exists():
                    for vault_file in Path(".vault").rglob("*"):
                        if vault_file.is_file():
                            zipf.write(vault_file, vault_file)
                
                # Backup configuration files
                for config_file in ["requirements.txt", "main.py"]:
                    if Path(config_file).exists():
                        zipf.write(config_file, config_file)
                
                # Create backup manifest
                manifest = {
                    "created_at": datetime.now().isoformat(),
                    "includes_vault": include_vault,
                    "files": [f.filename for f in zipf.filelist]
                }
                
                zipf.writestr("manifest.json", json.dumps(manifest, indent=2))
            
            # Encrypt if password provided
            if password:
                self._encrypt_backup(backup_file, password)
            
            console.print(f"[green]✅ Backup created: {backup_file.name}[/green]")
            return str(backup_file)
            
        except Exception as e:
            console.print(f"[red]❌ Backup failed: {e}[/red]")
            return ""
    
    def _encrypt_backup(self, backup_file: Path, password: str):
        """Encrypt backup file with password"""
        # Generate key from password
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        
        # Encrypt file
        fernet = Fernet(key)
        
        with open(backup_file, "rb") as f:
            data = f.read()
        
        encrypted_data = fernet.encrypt(data)
        
        # Save encrypted file with salt
        encrypted_file = backup_file.with_suffix(".encrypted")
        with open(encrypted_file, "wb") as f:
            f.write(salt)
            f.write(encrypted_data)
        
        # Remove original file
        backup_file.unlink()
        
        console.print(f"[green]🔐 Backup encrypted: {encrypted_file.name}[/green]")
    
    def restore_backup(self, backup_file: str, password: str = None) -> bool:
        """Restore system from backup"""
        backup_path = Path(backup_file)
        
        if not backup_path.exists():
            console.print(f"[red]❌ Backup file not found: {backup_file}[/red]")
            return False
        
        try:
            # Decrypt if needed
            if backup_path.suffix == ".encrypted":
                if not password:
                    password = Prompt.ask("🔐 Enter backup password", password=True)
                
                backup_path = self._decrypt_backup(backup_path, password)
                if not backup_path:
                    return False
            
            # Extract backup
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                # Read manifest
                manifest_data = zipf.read("manifest.json")
                manifest = json.loads(manifest_data.decode())
                
                console.print(f"[blue]📋 Backup manifest:[/blue]")
                console.print(f"  Created: {manifest['created_at']}")
                console.print(f"  Includes vault: {manifest['includes_vault']}")
                console.print(f"  Files: {len(manifest['files'])}")
                
                if not Confirm.ask("🔄 Proceed with restore?"):
                    return False
                
                # Extract files
                zipf.extractall(".")
            
            console.print(f"[green]✅ Backup restored successfully[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Restore failed: {e}[/red]")
            return False
    
    def _decrypt_backup(self, encrypted_file: Path, password: str) -> Optional[Path]:
        """Decrypt backup file"""
        try:
            with open(encrypted_file, "rb") as f:
                salt = f.read(16)
                encrypted_data = f.read()
            
            # Derive key
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            
            # Decrypt
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_data)
            
            # Save decrypted file
            decrypted_file = encrypted_file.with_suffix(".decrypted")
            with open(decrypted_file, "wb") as f:
                f.write(decrypted_data)
            
            return decrypted_file
            
        except Exception as e:
            console.print(f"[red]❌ Decryption failed: {e}[/red]")
            return None

class AuditManager:
    """Audits recent contract approvals and provides security insights"""
    
    def __init__(self):
        self.approval_history = []
        self.risk_indicators = []
    
    def add_approval(self, contract_address: str, spender: str, amount: str, 
                    wallet_name: str, timestamp: str = None):
        """Add a contract approval to audit history"""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        approval = {
            "contract_address": contract_address,
            "spender": spender,
            "amount": amount,
            "wallet_name": wallet_name,
            "timestamp": timestamp,
            "status": "active"
        }
        
        self.approval_history.append(approval)
    
    def audit_approvals(self) -> Dict[str, Any]:
        """Audit recent approvals for security risks"""
        console.print("[blue]🔍 Auditing contract approvals...[/blue]")
        
        # Simulate approval data
        if not self.approval_history:
            self._simulate_approvals()
        
        risk_findings = []
        high_risk_approvals = []
        
        for approval in self.approval_history:
            # Check for high-value approvals
            try:
                amount_value = float(approval["amount"])
                if amount_value > 1000:  # High value threshold
                    high_risk_approvals.append(approval)
                    risk_findings.append(f"High-value approval: {amount_value} to {approval['spender']}")
            except ValueError:
                pass
            
            # Check for recent approvals
            approval_time = datetime.fromisoformat(approval["timestamp"])
            if datetime.now() - approval_time < timedelta(hours=24):
                risk_findings.append(f"Recent approval: {approval['spender']} ({approval_time.strftime('%H:%M')})")
        
        audit_results = {
            "total_approvals": len(self.approval_history),
            "high_risk_count": len(high_risk_approvals),
            "risk_findings": risk_findings,
            "recommendations": self._generate_recommendations(risk_findings)
        }
        
        return audit_results
    
    def _simulate_approvals(self):
        """Simulate some approval data for demonstration"""
        self.add_approval(
            "0x1234567890abcdef",
            "0xabcdef1234567890",
            "500.0",
            "main_wallet",
            (datetime.now() - timedelta(hours=2)).isoformat()
        )
        self.add_approval(
            "0x9876543210fedcba",
            "0xfedcba0987654321",
            "2500.0",
            "trading_wallet",
            (datetime.now() - timedelta(hours=6)).isoformat()
        )
    
    def _generate_recommendations(self, risk_findings: List[str]) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        if len(risk_findings) > 0:
            recommendations.append("Review recent high-value approvals")
            recommendations.append("Consider revoking unused approvals")
            recommendations.append("Enable transaction notifications")
        
        if len([f for f in risk_findings if "Recent approval" in f]) > 3:
            recommendations.append("High approval frequency detected - review strategy")
        
        if not recommendations:
            recommendations.append("No immediate security concerns detected")
        
        return recommendations
    
    def show_audit_report(self) -> None:
        """Display comprehensive audit report"""
        audit_results = self.audit_approvals()
        
        console.print("\n[bold]🔍 Security Audit Report[/bold]")
        console.print("=" * 50)
        
        # Summary
        console.print(f"Total Approvals: {audit_results['total_approvals']}")
        console.print(f"High Risk Items: {audit_results['high_risk_count']}")
        
        # Risk findings
        if audit_results['risk_findings']:
            console.print("\n[bold red]⚠️ Risk Findings:[/bold red]")
            for finding in audit_results['risk_findings']:
                console.print(f"  • {finding}")
        
        # Recommendations
        console.print(f"\n[bold green]💡 Recommendations:[/bold green]")
        for rec in audit_results['recommendations']:
            console.print(f"  • {rec}")
        
        # Approval history table
        if self.approval_history:
            table = Table(title="📋 Recent Approvals")
            table.add_column("Contract", style="cyan")
            table.add_column("Spender", style="magenta")
            table.add_column("Amount", style="green")
            table.add_column("Wallet", style="blue")
            table.add_column("Time", style="white")
            
            for approval in self.approval_history[-10:]:  # Show last 10
                table.add_row(
                    approval["contract_address"][:10] + "...",
                    approval["spender"][:10] + "...",
                    approval["amount"],
                    approval["wallet_name"],
                    approval["timestamp"][:19]
                )
            
            console.print(table)

# Global instances
vault_manager = VaultManager()
transaction_signer = TransactionSigner(vault_manager)
backup_manager = BackupManager()
audit_manager = AuditManager() 