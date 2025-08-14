import os
import requests
import json
from flask import Blueprint, request, jsonify
from src.agents.brenda import Brenda
from src.agents.qumy import Qumy
from src.agents.sanita import Sanita
from src.agents.uby import Uby
from src.models.watsonx_service import WatsonxService

bot_blueprint = Blueprint("bot", __name__)

# Initialize the agents and services once
watsonx_service = WatsonxService(
    api_key=os.getenv("WATSONX_API_KEY"),
    project_id=os.getenv("WATSONX_PROJECT_ID")
)
brenda = Brenda(watsonx_client=watsonx_service)
qumy = Qumy(watsonx_client=watsonx_service) # You'll need to update Qumy to accept watsonx_client
sanita = Sanita(watsonx_client=watsonx_service, qumy_client=qumy)
uby = Uby(watsonx_client=watsonx_service)

def send_whatsapp_message(recipient_wa_id, message_text):
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    token = os.getenv("WHATSAPP_TOKEN")
    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_wa_id,
        "type": "text",
        "text": {"body": message_text}
    }
    resp = requests.post(url, headers=headers, json=payload)
    print("WhatsApp API response:", resp.status_code, resp.text)
    return resp

@bot_blueprint.route("", methods=["GET"])
def verify():
    # Your verification logic remains the same
    verify_token = os.getenv("VERIFY_TOKEN")
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode and token:
        if mode == "subscribe" and token == verify_token:
            return challenge, 200
    return "Verification failed", 403

@bot_blueprint.route("", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Received WhatsApp message:", data)
    wa_id = None
    try:
        entry = data["entry"][0]
        change = entry["changes"][0]
        value = change["value"]
        messages = value.get("messages")
        if messages:
            message = messages[0]
            wa_id = message["from"]
            text_body = message["text"]["body"] # Assumes text for now
            
            # Use Brenda's function calling to get a structured response
            brenda_response = brenda.orchestrate_message(text_body)
            tool_name = brenda_response.get('tool')
            arguments = brenda_response.get('arguments', {})
            
            # For testing, we'll just send back a message confirming the routing
            if tool_name == "add_task":
                final_response = f"Brenda has routed your request to add a task. Issue: {arguments.get('issue')}, Location: {arguments.get('location')}."
            elif tool_name == "get_task_status":
                final_response = f"Brenda has routed your request to get task status. Ticket ID: {arguments.get('ticket_id')}."
            elif tool_name == "greet":
                final_response = "Hi there! I'm Brenda. It's nice to meet you! How can I assist?"
            elif tool_name == "get_bin_location":
                final_response = f"Brenda has routed your request to find a bin near: {arguments.get('user_location')}."
            else:
                final_response = f"Brenda didn't understand that and has routed your request as unknown. Reason: {arguments.get('reason')}."

            print(f"Final response: {final_response}")
            send_whatsapp_message(wa_id, final_response)
        else:
            print("No message found in payload")
    except Exception as e:
        print("Error processing WhatsApp message:", e)
        if wa_id:
            send_whatsapp_message(wa_id, "I'm sorry, an unexpected error occurred.")
        
    return jsonify(status="received"), 200