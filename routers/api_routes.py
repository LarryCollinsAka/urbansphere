from flask import Blueprint, jsonify
from data.loader import load_agent_configs
from services import db_service # Import our db service

api_bp = Blueprint('api', __name__)

@api_bp.route('/data')
def get_dashboard_data():
    """
    Returns a JSON object with all the data needed for the dashboard.
    """
    # Prepare agent status data dynamically from the config folder
    agent_configs = load_agent_configs()
    agent_status = [{"name": name, "status": "Online"} for name in agent_configs.keys()]

    # Fetch all conversations from the database
    all_conversations = db_service.get_all_conversations()

    # Format the conversation history for display
    conversation_log = []
    for conversation in all_conversations:
        sender_id = conversation['_id']
        history = conversation.get('history', [])
        for interaction in history:
            if interaction['agent'] != 'processing...':
                conversation_log.append({
                    "user": interaction['user'],
                    "agent": interaction['agent'],
                    "sender_id": sender_id
                })

    return jsonify({
        "agent_status": agent_status,
        "conversations": conversation_log
    })
