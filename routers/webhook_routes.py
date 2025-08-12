import os
from flask import Blueprint, request, jsonify
from controllers.brenda_controller import brenda_orchestrator
from services import db_service
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

    # Check for a real WhatsApp payload structure
    try:
        # This block handles a real WhatsApp webhook payload
        message_info = data['entry'][0]['changes'][0]['value']['messages'][0]
    except (KeyError, IndexError):
        # Fallback to handle our test payload structure
        try:
            message_info = data['value']['messages'][0]
        except (KeyError, IndexError) as e:
            print(f"Error processing message data: {e}")
            return jsonify({'status': 'ok'}), 200
            
    try:
        sender_id = message_info['from']
        
        # Get conversation history from the database
        conversation_history = db_service.get_conversation_history(sender_id)

        if message_info['type'] == 'text':
            user_message = message_info['text']['body']
            print(f"User text message from {sender_id}: {user_message}")
            
            brenda_response, updated_history = brenda_orchestrator(user_message, conversation_history)
            
            # Save the updated history to the database
            db_service.save_conversation(sender_id, {"history": updated_history})
            send_whatsapp_message(sender_id, brenda_response)
        
        elif message_info['type'] == 'image':
            send_whatsapp_message(sender_id, "I'm currently processing that image with our Vision AI. Please hold!")
        elif message_info['type'] == 'audio':
            send_whatsapp_message(sender_id, "I'm currently transcribing that voice note with our Speech-to-Text service. Please hold!")

    except (KeyError, IndexError) as e:
        print(f"Error processing message data: {e}")
        return jsonify({'status': 'ok'}), 200

    return jsonify({'status': 'ok'}), 200
