"""
Base class for all Mountain Gorilla bots.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseBot(ABC):
    def __init__(self, name: str, level: int = 1):
        self.name = name
        self.level = level
        self.abilities: List[str] = []
        
    @abstractmethod
    def get_ascii_art(self) -> str:
        """Return the ASCII art representation of the bot."""
        pass
    
    def level_up(self) -> None:
        """Increase the bot's level by 1."""
        self.level += 1
        
    def get_abilities(self) -> List[str]:
        """Return the list of bot abilities."""
        return self.abilities
    
    def get_stats(self) -> Dict[str, Any]:
        """Return the bot's current stats."""
        return {
            "name": self.name,
            "level": self.level,
            "abilities": self.abilities
        } 