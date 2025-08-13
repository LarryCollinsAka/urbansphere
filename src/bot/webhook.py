import os
import requests
from flask import Blueprint, request, jsonify

bot_blueprint = Blueprint("bot", __name__)

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

def brenda_route_and_reply(message_text):
    if "waste" in message_text.lower() or "bin" in message_text.lower():
        agent = "Sanita"
        response = "Sanita here! I can help with waste and bins. What do you need?"
    elif "bus" in message_text.lower() or "transport" in message_text.lower():
        agent = "Qumy"
        response = "Qumy here! I handle transport and mobility queries."
    elif "light" in message_text.lower() or "safety" in message_text.lower():
        agent = "Uby"
        response = "Uby here! I can assist with city safety or lighting issues."
    else:
        agent = "Brenda"
        response = ("Hi, I'm Brenda, your city's digital coordinator. "
                    "You can ask about waste (Sanita), mobility (Qumy), or city safety (Uby).")
    return agent, response

@bot_blueprint.route("", methods=["GET"])
def verify():
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
    try:
        entry = data["entry"][0]
        change = entry["changes"][0]
        value = change["value"]
        messages = value.get("messages")
        if messages:
            message = messages[0]
            text_body = message["text"]["body"]
            wa_id = message["from"]
            contact_name = value["contacts"][0]["profile"]["name"]
            print(f"Received WhatsApp message from {contact_name} ({wa_id}): {text_body}")

            # Route to Brenda, get response
            agent, reply_text = brenda_route_and_reply(text_body)
            print(f"Routed to agent: {agent}, Reply: {reply_text}")

            # Send WhatsApp reply
            send_whatsapp_message(wa_id, reply_text)
        else:
            print("No message found in payload")
    except Exception as e:
        print("Error parsing WhatsApp message:", e)
    return jsonify(status="received"), 200