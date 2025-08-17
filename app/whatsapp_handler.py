import os
import requests
import json
from app.brenda import ask_brenda_with_curl_style

WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")

def send_whatsapp_message(to, message):
    """
    Sends a text message via the WhatsApp Cloud API.
    """
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
    """
    Processes incoming WhatsApp webhook data, gets a response from Brenda,
    and sends it back to the user.
    """
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

            # Call Brenda's model using the function from brenda.py
            brenda_response = ask_brenda_with_curl_style(text)
            
            # Now, use a robust parsing block to safely extract the string content.
            # This handles different API response formats and is the key to solving the error.
            answer = "Sorry, I couldn't process your request. Please try again later."
            
            if brenda_response and isinstance(brenda_response, dict):
                try:
                    # The most common response format has a nested list inside "content"
                    content_parts = brenda_response.get("choices", [{}])[0].get("message", {}).get("content", [])
                    if isinstance(content_parts, list) and content_parts and isinstance(content_parts[0], dict):
                        answer = content_parts[0].get("text", answer)
                    elif isinstance(content_parts, str):
                        # This handles cases where the "content" is a simple string
                        answer = content_parts
                except (IndexError, AttributeError, TypeError):
                    # Fallback for unexpected response structures
                    print("Error parsing Brenda's response.")
            
            print(f"Brenda response: {answer}")
            send_result = send_whatsapp_message(sender, answer)
            print(f"WhatsApp send result: {send_result}")
        else:
            print("No WhatsApp message found in webhook payload.")
    except Exception as e:
        print(f"Error processing WhatsApp webhook: {e}")