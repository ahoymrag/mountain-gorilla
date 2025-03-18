"""
ASCII art for each bot. Feel free to change or expand these.
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

def get_ascii_bot(bot_name: str) -> str:
    """
    Return ASCII art for the given bot name, or a default if not found.
    """
    return bot_ascii.get(bot_name, "🤖 [Unknown Bot]")
