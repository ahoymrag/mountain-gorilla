"""
CoachBot - A bot specialized in providing motivation and coaching.
"""

from typing import List, Dict, Any
from .base_bot import BaseBot

class CoachBot(BaseBot):
    def __init__(self, level: int = 1):
        super().__init__("CoachBot", level)
        self.abilities = ["Motivational Tips", "Goal Setting", "Progress Tracking"]
        self.goals: List[Dict[str, Any]] = []
        self.motivational_quotes = [
            "The only way to do great work is to love what you do.",
            "Success is not final, failure is not fatal: it is the courage to continue that counts.",
            "Believe you can and you're halfway there.",
            "The future belongs to those who believe in the beauty of their dreams.",
            "Don't watch the clock; do what it does. Keep going."
        ]
        
    def get_ascii_art(self) -> str:
        return r"""
      ____
     (💪 🤖)
      |  |
      ||||
    """
    
    def add_goal(self, 
                 title: str, 
                 description: str, 
                 target_date: str = None) -> None:
        """Add a new goal to track."""
        goal = {
            "id": len(self.goals) + 1,
            "title": title,
            "description": description,
            "target_date": target_date,
            "status": "in_progress",
            "progress": 0,
            "created_at": "2024-03-21"  # TODO: Use actual datetime
        }
        self.goals.append(goal)
        
    def update_goal_progress(self, goal_id: int, progress: int) -> None:
        """Update the progress of a goal."""
        for goal in self.goals:
            if goal["id"] == goal_id:
                goal["progress"] = max(0, min(100, progress))
                if goal["progress"] >= 100:
                    goal["status"] = "completed"
                break
                
    def get_goals(self, status: str = None) -> List[Dict[str, Any]]:
        """Get goals, optionally filtered by status."""
        if not status:
            return self.goals.copy()
        return [g for g in self.goals if g["status"] == status]
    
    def get_motivational_quote(self) -> str:
        """Get a random motivational quote."""
        import random
        return random.choice(self.motivational_quotes)
    
    def analyze_goals(self) -> Dict[str, Any]:
        """Analyze goals and return insights."""
        return {
            "total_goals": len(self.goals),
            "completed_goals": len([g for g in self.goals if g["status"] == "completed"]),
            "in_progress_goals": len([g for g in self.goals if g["status"] == "in_progress"]),
            "average_progress": sum(g["progress"] for g in self.goals) / len(self.goals) if self.goals else 0
        } 