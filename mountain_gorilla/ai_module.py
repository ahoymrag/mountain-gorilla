"""
AI Module for bot collaboration and task management.
"""

from typing import List, Dict, Any
import json
from datetime import datetime

class AIModule:
    def __init__(self):
        self.conversation_history = []
        self.task_queue = []
        self.bot_capabilities = {}
        self.active_collaborations = []

    def register_bot(self, bot_name: str, capabilities: List[str], personality: str):
        """Register a bot with its capabilities and personality."""
        self.bot_capabilities[bot_name] = {
            'capabilities': capabilities,
            'personality': personality,
            'last_active': datetime.now()
        }

    def create_collaboration(self, task: str, required_capabilities: List[str]) -> Dict[str, Any]:
        """Create a new collaboration task and assign bots based on capabilities."""
        available_bots = []
        for bot_name, info in self.bot_capabilities.items():
            if any(cap in info['capabilities'] for cap in required_capabilities):
                available_bots.append(bot_name)

        if not available_bots:
            return {'success': False, 'message': 'No suitable bots available'}

        collaboration = {
            'id': len(self.active_collaborations) + 1,
            'task': task,
            'bots': available_bots,
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'progress': 0
        }
        
        self.active_collaborations.append(collaboration)
        return collaboration

    def process_bot_message(self, bot_name: str, message: str, collaboration_id: int = None) -> Dict[str, Any]:
        """Process a message from a bot and update the conversation history."""
        if bot_name not in self.bot_capabilities:
            return {'success': False, 'message': 'Bot not registered'}

        message_entry = {
            'bot': bot_name,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'collaboration_id': collaboration_id
        }
        
        self.conversation_history.append(message_entry)
        
        # If this is part of a collaboration, update progress
        if collaboration_id:
            collaboration = next((c for c in self.active_collaborations if c['id'] == collaboration_id), None)
            if collaboration:
                collaboration['progress'] += 1
                if collaboration['progress'] >= len(collaboration['bots']) * 2:  # Each bot contributes twice
                    collaboration['status'] = 'completed'

        return {'success': True, 'message': 'Message processed'}

    def get_collaboration_status(self, collaboration_id: int) -> Dict[str, Any]:
        """Get the current status of a collaboration."""
        collaboration = next((c for c in self.active_collaborations if c['id'] == collaboration_id), None)
        if not collaboration:
            return {'success': False, 'message': 'Collaboration not found'}

        return {
            'success': True,
            'collaboration': collaboration,
            'conversation': [msg for msg in self.conversation_history if msg['collaboration_id'] == collaboration_id]
        }

    def get_bot_suggestions(self, task: str) -> List[str]:
        """Get AI-powered suggestions for which bots to use for a task."""
        # This would typically use more sophisticated AI to analyze task requirements
        # and match them with bot capabilities
        suggestions = []
        for bot_name, info in self.bot_capabilities.items():
            if any(cap.lower() in task.lower() for cap in info['capabilities']):
                suggestions.append(bot_name)
        return suggestions

    def generate_task_plan(self, task: str, selected_bots: List[str]) -> Dict[str, Any]:
        """Generate an AI-powered plan for how bots should collaborate on a task."""
        plan = {
            'task': task,
            'bots': selected_bots,
            'steps': [],
            'estimated_duration': '5-10 minutes',
            'created_at': datetime.now().isoformat()
        }

        # Generate steps based on bot capabilities
        for bot in selected_bots:
            if bot in self.bot_capabilities:
                capabilities = self.bot_capabilities[bot]['capabilities']
                for cap in capabilities:
                    plan['steps'].append({
                        'bot': bot,
                        'action': f'Use {cap} capability',
                        'order': len(plan['steps']) + 1
                    })

        return plan

    def get_ai_insights(self, collaboration_id: int) -> Dict[str, Any]:
        """Generate AI-powered insights about a collaboration's performance."""
        collaboration = next((c for c in self.active_collaborations if c['id'] == collaboration_id), None)
        if not collaboration:
            return {'success': False, 'message': 'Collaboration not found'}

        messages = [msg for msg in self.conversation_history if msg['collaboration_id'] == collaboration_id]
        
        insights = {
            'collaboration_id': collaboration_id,
            'total_messages': len(messages),
            'messages_per_bot': {},
            'collaboration_duration': None,
            'efficiency_score': 0.8,  # This would be calculated based on actual metrics
            'suggestions': []
        }

        # Calculate messages per bot
        for msg in messages:
            bot = msg['bot']
            insights['messages_per_bot'][bot] = insights['messages_per_bot'].get(bot, 0) + 1

        # Calculate collaboration duration
        if messages:
            start_time = datetime.fromisoformat(messages[0]['timestamp'])
            end_time = datetime.fromisoformat(messages[-1]['timestamp'])
            insights['collaboration_duration'] = str(end_time - start_time)

        return insights 