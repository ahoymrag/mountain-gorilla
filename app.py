"""
Flask web application for Mountain Gorilla Command Center.
"""

from flask import Flask, render_template, jsonify, request, session
from mountain_gorilla.bots import (
    MemoriBot, FinanBot, TradeBot, TaskBot, CoachBot
)
from mountain_gorilla.ai_module import AIModule
from rich.console import Console
from rich.text import Text
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Initialize bots
bots = {
    "MemoriBot": MemoriBot(),
    "FinanBot": FinanBot(),
    "TradeBot": TradeBot(),
    "TaskBot": TaskBot(),
    "CoachBot": CoachBot()
}

# Initialize AI module
ai_module = AIModule()

# Register existing bots with AI module
for name, bot in bots.items():
    ai_module.register_bot(
        name,
        capabilities=bot.abilities,
        personality=f"Level {bot.level} {name}"
    )

@app.route('/')
def index():
    """Render the main dashboard."""
    return render_template('index.html', bots=bots)

@app.route('/api/bots')
def list_bots():
    """Get list of all bots and their stats."""
    return jsonify({
        name: {
            "level": bot.level,
            "abilities": bot.abilities,
            "ascii_art": bot.get_ascii_art()
        }
        for name, bot in bots.items()
    })

@app.route('/api/bots/<bot_name>')
def get_bot(bot_name):
    """Get specific bot details."""
    if bot_name not in bots:
        return jsonify({"error": "Bot not found"}), 404
    bot = bots[bot_name]
    return jsonify({
        "name": bot.name,
        "level": bot.level,
        "abilities": bot.abilities,
        "ascii_art": bot.get_ascii_art(),
        "stats": bot.get_stats()
    })

@app.route('/api/bots/<bot_name>/train', methods=['POST'])
def train_bot(bot_name):
    """Train (level up) a specific bot."""
    if bot_name not in bots:
        return jsonify({"error": "Bot not found"}), 404
    bot = bots[bot_name]
    bot.level_up()
    return jsonify({
        "name": bot.name,
        "new_level": bot.level
    })

# MemoriBot endpoints
@app.route('/api/bots/MemoriBot/memories', methods=['GET'])
def get_memories():
    """Get all memories from MemoriBot."""
    bot = bots["MemoriBot"]
    tags = request.args.getlist('tags')
    return jsonify(bot.retrieve_memories(tags))

@app.route('/api/bots/MemoriBot/memories', methods=['POST'])
def store_memory():
    """Store a new memory in MemoriBot."""
    bot = bots["MemoriBot"]
    data = request.json
    bot.store_memory(
        content=data.get('content'),
        tags=data.get('tags', [])
    )
    return jsonify({"status": "success"})

# FinanBot endpoints
@app.route('/api/bots/FinanBot/balance', methods=['GET'])
def get_balance():
    """Get current balance from FinanBot."""
    bot = bots["FinanBot"]
    currency = request.args.get('currency')
    return jsonify(bot.get_balance(currency))

@app.route('/api/bots/FinanBot/transactions', methods=['POST'])
def record_transaction():
    """Record a new transaction in FinanBot."""
    bot = bots["FinanBot"]
    data = request.json
    bot.record_transaction(
        currency=data.get('currency'),
        amount=data.get('amount'),
        transaction_type=data.get('type'),
        description=data.get('description')
    )
    return jsonify({"status": "success"})

# TaskBot endpoints
@app.route('/api/bots/TaskBot/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks from TaskBot."""
    bot = bots["TaskBot"]
    status = request.args.get('status')
    return jsonify(bot.get_tasks(status))

@app.route('/api/bots/TaskBot/tasks', methods=['POST'])
def add_task():
    """Add a new task to TaskBot."""
    bot = bots["TaskBot"]
    data = request.json
    bot.add_task(
        title=data.get('title'),
        description=data.get('description'),
        priority=data.get('priority', 'medium'),
        due_date=data.get('due_date')
    )
    return jsonify({"status": "success"})

# CoachBot endpoints
@app.route('/api/bots/CoachBot/goals', methods=['GET'])
def get_goals():
    """Get all goals from CoachBot."""
    bot = bots["CoachBot"]
    status = request.args.get('status')
    return jsonify(bot.get_goals(status))

@app.route('/api/bots/CoachBot/quote', methods=['GET'])
def get_quote():
    """Get a motivational quote from CoachBot."""
    bot = bots["CoachBot"]
    return jsonify({"quote": bot.get_motivational_quote()})

@app.route('/api/ai/collaborate', methods=['POST'])
def create_collaboration():
    """Create a new AI-powered collaboration between bots."""
    data = request.get_json()
    task = data.get('task')
    required_capabilities = data.get('capabilities', [])

    if not task:
        return jsonify({'error': 'Task is required'}), 400

    collaboration = ai_module.create_collaboration(task, required_capabilities)
    return jsonify(collaboration)

@app.route('/api/ai/collaborations/<int:collaboration_id>', methods=['GET'])
def get_collaboration_status(collaboration_id):
    """Get the status of a collaboration."""
    status = ai_module.get_collaboration_status(collaboration_id)
    return jsonify(status)

@app.route('/api/ai/bots/suggest', methods=['POST'])
def get_bot_suggestions():
    """Get AI-powered suggestions for which bots to use for a task."""
    data = request.get_json()
    task = data.get('task')

    if not task:
        return jsonify({'error': 'Task is required'}), 400

    suggestions = ai_module.get_bot_suggestions(task)
    return jsonify({'suggestions': suggestions})

@app.route('/api/ai/tasks/plan', methods=['POST'])
def generate_task_plan():
    """Generate an AI-powered plan for bot collaboration."""
    data = request.get_json()
    task = data.get('task')
    selected_bots = data.get('bots', [])

    if not task or not selected_bots:
        return jsonify({'error': 'Task and selected bots are required'}), 400

    plan = ai_module.generate_task_plan(task, selected_bots)
    return jsonify(plan)

@app.route('/api/ai/collaborations/<int:collaboration_id>/insights', methods=['GET'])
def get_collaboration_insights(collaboration_id):
    """Get AI-powered insights about a collaboration."""
    insights = ai_module.get_ai_insights(collaboration_id)
    return jsonify(insights)

@app.route('/api/ai/bots/message', methods=['POST'])
def process_bot_message():
    """Process a message from a bot in a collaboration."""
    data = request.get_json()
    bot_name = data.get('bot')
    message = data.get('message')
    collaboration_id = data.get('collaboration_id')

    if not bot_name or not message:
        return jsonify({'error': 'Bot name and message are required'}), 400

    result = ai_module.process_bot_message(bot_name, message, collaboration_id)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True) 