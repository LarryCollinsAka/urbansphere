from flask import Blueprint, jsonify
# Import from the new globals module instead of app.py
import globals as app_globals

# Create a Blueprint for our API routes
api_bp = Blueprint('api', __name__)

@api_bp.route('/data')
def get_dashboard_data():
    """
    Returns a JSON object with all the data needed for the dashboard.
    """
    # Prepare agent status data dynamically from the config folder
    agent_status = [{"name": name, "status": "Online"} for name in app_globals.agent_configs.keys()]

    # Format the conversation history for display
    conversation_log = []
    for sender_id, history in app_globals.session_store.items():
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
