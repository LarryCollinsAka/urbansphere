import os
import requests
import json
from app.brenda import ask_brenda

WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")

def send_whatsapp_message(to, message):
    if not WHATSAPP_PHONE_NUMBER_ID or not WHATSAPP_ACCESS_TOKEN:
        print("WhatsApp Cloud API credentials missing!")
        return None
    url = f"https://graph.facebook.com/v19.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": { "body": message }
    }
    response = requests.post(url, headers=headers, json=payload)
    try:
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"WhatsApp send error: {e}")
        print(f"Response: {response.text}")
        return None

def handle_whatsapp_webhook(data):
    try:
        print("Raw JSON payload:", json.dumps(data, indent=2))
        entry = data.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])
        if messages:
            msg = messages[0]
            text = msg.get("text", {}).get("body", "")
            sender = msg.get("from", "")
            print(f"Incoming WhatsApp message from {sender}: {text}")

            # Brenda now acts as a solo consultant.
            # Her response is the final answer, so we don't need to parse for tools.
            brenda_response = ask_brenda(text)
            
            # Assuming ask_brenda returns a string, we use it directly.
            answer = brenda_response

            print(f"Brenda response: {answer}")
            send_result = send_whatsapp_message(sender, answer)
            print(f"WhatsApp send result: {send_result}")
        else:
            print("No WhatsApp message found in webhook payload.")
    except Exception as e:
        print(f"Error processing WhatsApp webhook: {e}")