"""
FinanBot - A bot specialized in financial management and tracking.
"""

from typing import List, Dict, Any
from decimal import Decimal
from .base_bot import BaseBot

class FinanBot(BaseBot):
    def __init__(self, level: int = 1):
        super().__init__("FinanBot", level)
        self.abilities = ["Budget Tracking", "Expense Analysis", "Financial Planning"]
        self.balance: Dict[str, Decimal] = {
            "ETH": Decimal("0.0"),
            "BTC": Decimal("0.0")
        }
        self.transactions: List[Dict[str, Any]] = []
        
    def get_ascii_art(self) -> str:
        return r"""
      ____
     (💰💰)
      |  |
      ||||
    """
    
    def update_balance(self, currency: str, amount: Decimal) -> None:
        """Update the balance for a specific currency."""
        if currency not in self.balance:
            self.balance[currency] = Decimal("0.0")
        self.balance[currency] += amount
        
    def record_transaction(self, 
                          currency: str, 
                          amount: Decimal, 
                          transaction_type: str,
                          description: str) -> None:
        """Record a new transaction."""
        transaction = {
            "currency": currency,
            "amount": amount,
            "type": transaction_type,
            "description": description,
            "timestamp": "2024-03-21"  # TODO: Use actual datetime
        }
        self.transactions.append(transaction)
        self.update_balance(currency, amount)
        
    def get_balance(self, currency: str = None) -> Dict[str, Decimal]:
        """Get balance for specific currency or all currencies."""
        if currency:
            return {currency: self.balance.get(currency, Decimal("0.0"))}
        return self.balance.copy()
    
    def analyze_expenses(self, currency: str = None) -> Dict[str, Any]:
        """Analyze expenses and return insights."""
        if currency:
            transactions = [t for t in self.transactions 
                          if t["currency"] == currency and t["amount"] < 0]
        else:
            transactions = [t for t in self.transactions if t["amount"] < 0]
            
        return {
            "total_expenses": sum(abs(t["amount"]) for t in transactions),
            "transaction_count": len(transactions),
            "expenses_by_type": {
                t["type"]: sum(abs(tr["amount"]) for tr in transactions if tr["type"] == t["type"])
                for t in transactions
            }
        } 