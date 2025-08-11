from flask import Blueprint, request
import os
import json
from controllers.brenda_controller import brenda_orchestrator
from services import db_service

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('', methods=['GET', 'POST'])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode and token:
            if mode == "subscribe" and token == os.environ.get("META_VERIFY_TOKEN"):
                print("WEBHOOK_VERIFIED")
                return challenge, 200
            else:
                return "Verification token mismatch", 403
        else:
            return "Missing parameters", 400

    if request.method == "POST":
        data = request.get_json()
        print("Received webhook data:")
        print(json.dumps(data, indent=2))
        
        # Check if it's a valid WhatsApp message event
        if data.get("object") == "whatsapp_business_account":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    # Make sure it's a new message
                    if "messages" in value:
                        for message in value.get("messages", []):
                            if message["type"] == "text":
                                user_message = message["text"]["body"]
                                user_id = message["from"]

                                # Retrieve conversation history from the database
                                conversation_history = db_service.get_conversation_history(user_id)
                                
                                # Call the orchestrator with the retrieved history
                                brenda_response, new_history = brenda_orchestrator(user_message, conversation_history)
                                
                                # Save the updated conversation history to the database
                                db_service.save_conversation(user_id, {"history": new_history})

                                print(f"Brenda response: {brenda_response}")
        return {"status": "ok"}, 200

    return "Method not allowed", 405