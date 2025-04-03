"""
TaskBot - A bot specialized in task management and organization.
"""

from typing import List, Dict, Any
from datetime import datetime
from .base_bot import BaseBot

class TaskBot(BaseBot):
    def __init__(self, level: int = 1):
        super().__init__("TaskBot", level)
        self.abilities = ["Manage Tasks", "Task Prioritization", "Progress Tracking"]
        self.tasks: List[Dict[str, Any]] = []
        
    def get_ascii_art(self) -> str:
        return r"""
      ____
     (✔ ✔)
      |  |
      ||||
    """
    
    def add_task(self, 
                 title: str, 
                 description: str, 
                 priority: str = "medium",
                 due_date: str = None) -> None:
        """Add a new task to the list."""
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "status": "pending",
            "created_at": "2024-03-21",  # TODO: Use actual datetime
            "completed_at": None
        }
        self.tasks.append(task)
        
    def complete_task(self, task_id: int) -> None:
        """Mark a task as completed."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = "completed"
                task["completed_at"] = "2024-03-21"  # TODO: Use actual datetime
                break
                
    def get_tasks(self, status: str = None) -> List[Dict[str, Any]]:
        """Get tasks, optionally filtered by status."""
        if not status:
            return self.tasks.copy()
        return [t for t in self.tasks if t["status"] == status]
    
    def analyze_tasks(self) -> Dict[str, Any]:
        """Analyze tasks and return insights."""
        return {
            "total_tasks": len(self.tasks),
            "completed_tasks": len([t for t in self.tasks if t["status"] == "completed"]),
            "pending_tasks": len([t for t in self.tasks if t["status"] == "pending"]),
            "tasks_by_priority": {
                p: len([t for t in self.tasks if t["priority"] == p])
                for p in set(t["priority"] for t in self.tasks)
            }
        } 