"""
MemoriBot - A bot specialized in storing and retrieving memories.
"""

from typing import List, Dict, Any
from .base_bot import BaseBot

class MemoriBot(BaseBot):
    def __init__(self, level: int = 1):
        super().__init__("MemoriBot", level)
        self.abilities = ["Store Memories", "Retrieve Memories", "Memory Analysis"]
        self.memories: List[Dict[str, Any]] = []
        
    def get_ascii_art(self) -> str:
        return r"""
      ____
     (o  o)  📝
      |  |
      ||||
    """
    
    def store_memory(self, content: str, tags: List[str] = None) -> None:
        """Store a new memory with optional tags."""
        memory = {
            "content": content,
            "tags": tags or [],
            "timestamp": "2024-03-21"  # TODO: Use actual datetime
        }
        self.memories.append(memory)
        
    def retrieve_memories(self, tags: List[str] = None) -> List[Dict[str, Any]]:
        """Retrieve memories, optionally filtered by tags."""
        if not tags:
            return self.memories
        return [m for m in self.memories if any(tag in m["tags"] for tag in tags)]
    
    def analyze_memories(self) -> Dict[str, Any]:
        """Analyze stored memories and return insights."""
        return {
            "total_memories": len(self.memories),
            "unique_tags": list(set(tag for m in self.memories for tag in m["tags"])),
            "memory_count_by_tag": {
                tag: len([m for m in self.memories if tag in m["tags"]])
                for tag in set(tag for m in self.memories for tag in m["tags"])
            }
        } 