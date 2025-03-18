"""
CommandCenter - a Pokédex-like manager for your ASCII AI bots.
"""

from mountain_gorilla.ascii_bots import get_ascii_bot
from mountain_gorilla.animations import spinner_animation, typing_effect, loading_bar

class CommandCenter:
    # Simple dictionary representing your bots.
    # Each bot has a 'level' and some 'abilities'.
    bots = {
        "MemoriBot": {"level": 1, "abilities": ["Store Memories"]},
        "FinanBot":  {"level": 1, "abilities": ["Budget Tracking"]},
        "TradeBot":  {"level": 1, "abilities": ["Stock Watchlist"]},
        "TaskBot":   {"level": 1, "abilities": ["Manage Tasks"]},
        "CoachBot":  {"level": 1, "abilities": ["Motivational Tips"]},
    }

    @classmethod
    def list_bots(cls):
        print("🦍  Mountain Gorilla Command Center - Available Bots:")
        for bot_name, stats in cls.bots.items():
            level = stats["level"]
            abilities = ", ".join(stats["abilities"])
            print(f"  - {bot_name} (Lvl {level}) | Abilities: {abilities}")

    @classmethod
    def summon(cls, bot_name):
        if bot_name not in cls.bots:
            print(f"❌  Bot '{bot_name}' not found!")
            return

        typing_effect(f"Summoning {bot_name}...\n")
        loading_bar(duration=3.0, message="Preparing")
        ascii_art = get_ascii_bot(bot_name)
        print(ascii_art)

        level = cls.bots[bot_name]["level"]
        abilities = ", ".join(cls.bots[bot_name]["abilities"])
        print(f"🤖  {bot_name} (Lvl {level}) summoned! Abilities: {abilities}")

    @classmethod
    def train(cls, bot_name):
        if bot_name not in cls.bots:
            print(f"❌  Bot '{bot_name}' not found!")
            return

        # Spinner animation to simulate "training"
        spinner_animation(duration=2.0, message=f"Training {bot_name}")
        cls.bots[bot_name]["level"] += 1
        new_level = cls.bots[bot_name]["level"]
        print(f"📈  {bot_name} leveled up! Now at Level {new_level}.")
