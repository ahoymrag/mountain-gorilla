"""
ASCII art for each bot. 
Feel free to add or modify these as you wish.
"""

bot_ascii = {
    "MemoriBot": r"""
      ____
     (o  o)  📝 
      |  |
      ||||
    """,
    "FinanBot": r"""
      ____
     (💰💰)
      |  |
      ||||
    """,
    "TradeBot": r"""
      ____
     (📈📉)
      |  |
      ||||
    """,
    "TaskBot": r"""
      ____
     (✔ ✔)
      |  |
      ||||
    """,
    "CoachBot": r"""
      ____
     (💪 🤖)
      |  |
      ||||
    """
}

def get_ascii_bot(name: str) -> str:
    return bot_ascii.get(name, "🤖 [Unknown Bot]")
