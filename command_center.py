"""
CommandCenter - the 'Pokédex-like' manager for your ASCII AI bots.
Handles listing, summoning, and training them.
"""

from mountain_gorilla.ascii_bots import get_ascii_bot
from mountain_gorilla.animations import spinner_animation, typing_effect

class CommandCenter:
    # Simple in-memory representation of the bots.
    # Each bot has a level and list of abilities.
    bots = {
        "MemoriBot":  {"level": 1, "abilities": ["Store Memories"]},
        "FinanBot":   {"level": 1, "abilities": ["Track Budget"]},
        "TradeBot":   {"level": 1, "abilities": ["Stock Watchlist"]},
        "TaskBot":    {"level": 1, "abilities": ["Manage Tasks"]},
        "CoachBot":   {"level": 1, "abilities": ["Motivational Tips"]},
    }

    @classmethod
    def list_bots(cls):
        print("🦍  Available Bots in Mountain Gorilla Command Center:")
        for name, stats in cls.bots.items():
            lvl = stats["level"]
            abilities = ", ".join(stats["abilities"])
            print(f"  - {name} (Lvl {lvl}) | Abilities: {abilities}")

    @classmethod
    def summon(cls, bot_name):
        bot = cls.bots.get(bot_name)
        if not bot:
            print(f"❌  Bot '{bot_name}' not found.")
            return
        # Print ASCII art for the bot
        ascii_art = get_ascii_bot(bot_name)
        typing_effect(f"Summoning {bot_name}...\n")
        print(ascii_art)
        lvl = bot["level"]
        abilities = ", ".join(bot["abilities"])
        print(f"🤖  {bot_name} (Lvl {lvl}) is online! Abilities: {abilities}")

    @classmethod
    def train(cls, bot_name):
        bot = cls.bots.get(bot_name)
        if not bot:
            print(f"❌  Bot '{bot_name}' not found.")
            return

        # Show a spinner animation to simulate "training"
        spinner_animation(message=f"Training {bot_name}")
        bot["level"] += 1
        print(f"📈  {bot_name} leveled up to Level {bot['level']}!")
