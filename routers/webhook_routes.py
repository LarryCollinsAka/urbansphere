import os
from flask import Blueprint, request, jsonify
from controllers.brenda_controller import brenda_orchestrator
# Import from the new globals module instead of app.py
import globals as app_globals

from services.whatsapp_service import send_whatsapp_message

# Create a Blueprint for our webhook routes
webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode and token:
        if mode == 'subscribe' and token == os.getenv('META_VERIFY_TOKEN'):
            print('WEBHOOK_VERIFIED')
            return challenge, 200
        else:
            return jsonify({'error': 'Verification failed'}), 403
    return jsonify({'error': 'Invalid request'}), 400

@webhook_bp.route('', methods=['POST'])
def process_message():
    data = request.json
    print(f"Received data: {data}")

    if not data or 'object' not in data or 'entry' not in data:
        return jsonify({'status': 'ok'}), 200

    try:
        message_info = data['entry'][0]['changes'][0]['value']['messages'][0]
        sender_id = message_info['from']
        
        # Use the session_store from the new globals module
        conversation_history = app_globals.session_store.get(sender_id, [])

        if message_info['type'] == 'text':
            user_message = message_info['text']['body']
            print(f"User text message from {sender_id}: {user_message}")
            
            # --- Call Brenda's Orchestration Logic ---
            brenda_response, updated_history = brenda_orchestrator(user_message, conversation_history)
            
            # Update the session_store from the new globals module
            app_globals.session_store[sender_id] = updated_history
            send_whatsapp_message(sender_id, brenda_response)
        
        # Add logic here for image and audio inputs
        elif message_info['type'] == 'image':
            send_whatsapp_message(sender_id, "I'm currently processing that image with our Vision AI. Please hold!")
        elif message_info['type'] == 'audio':
            send_whatsapp_message(sender_id, "I'm currently transcribing that voice note with our Speech-to-Text service. Please hold!")

    except (KeyError, IndexError) as e:
        print(f"Error processing message data: {e}")
        return jsonify({'status': 'ok'}), 200

    return jsonify({'status': 'ok'}), 200
