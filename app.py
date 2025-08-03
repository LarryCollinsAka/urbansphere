import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# --- Load Specialized Agent Data (Simulated RAG) ---
# In a real app, this might be a database. For a hackathon, in-memory is fast.
try:
    with open('data/sanita_data.json', 'r') as f:
        sanita_data = json.load(f)
    with open('data/qumy_data.json', 'r') as f:
        qumy_data = json.load(f)
    # Load other agents' data here
except FileNotFoundError:
    print("WARNING: Datasets not found. Please create them in the 'data' directory.")
    sanita_data = {}
    qumy_data = {}

# --- Brenda's Core Logic (The Orchestrator) ---
# This is a simplified function for the MVP
# It will be much more sophisticated in the final version
def brenda_orchestrator(user_message):
    # This is Brenda's NLU/Intent Recognition
    # For now, we use simple keyword matching to simulate the LLM's role
    user_message_lower = user_message.lower()

    if "waste" in user_message_lower or "dumping" in user_message_lower or "recycling" in user_message_lower:
        print("Brenda: Delegating to Sanita...")
        return handle_sanita_request(user_message)
    elif "queue" in user_message_lower or "wait time" in user_message_lower:
        print("Brenda: Delegating to Qumy...")
        return handle_qumy_request(user_message)
    # Add other agents' logic here:
    # elif "food" in user_message_lower or "farming" in user_message_lower:
    #     print("Brenda: Delegating to Nura...")
    #     return handle_nura_request(user_message)
    # ... and so on for Uby and Zati

    # Fallback response if no agent is a good fit
    return "Hi there! I'm Brenda, your UrbanSphere assistant. I can help with issues related to waste, queues, food, urban planning, or safety. How can I assist you today?"

# --- Specialized Agent Logic (The Workers) ---
# These functions will contain RAG and LLM calls
def handle_sanita_request(message):
    # Placeholder: In the final version, this will call the watsonx.ai LLM
    # with context from `sanita_data`.
    return f"Hello from Sanita! I've received your request about waste. I can help you report it or find recycling information."

def handle_qumy_request(message):
    # Placeholder: In the final version, this will call the watsonx.ai LLM
    # with context from `qumy_data`.
    return "Hi, this is Qumy! I've received your request about queues. I can check wait times or help you join a virtual queue."

# --- WhatsApp Webhook Routes ---

# Verification endpoint for Meta
@app.route('/webhook', methods=['GET'])
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

# Main endpoint to receive messages
@app.route('/webhook', methods=['POST'])
def process_message():
    data = request.json
    print(f"Received data: {data}")

    # Check if the message is from a valid source (implementation for hackathon)
    if not data or 'object' not in data or 'entry' not in data:
        return jsonify({'status': 'ok'}), 200

    # Extract the user's message
    try:
        message_info = data['entry'][0]['changes'][0]['value']['messages'][0]
        user_message = message_info['text']['body']
        sender_id = message_info['from']
        print(f"User message from {sender_id}: {user_message}")

        # Let Brenda handle the message
        brenda_response = brenda_orchestrator(user_message)

        # Send the response back to the user
        send_whatsapp_message(sender_id, brenda_response)

    except (KeyError, IndexError) as e:
        print(f"Error processing message data: {e}")
        # Return a 200 OK to prevent re-sending by Meta
        return jsonify({'status': 'ok'}), 200

    return jsonify({'status': 'ok'}), 200

# --- Function to Send a WhatsApp Message ---
def send_whatsapp_message(to_number, message_text):
    # This function will use the requests library to call the Meta API
    # Placeholder for hackathon MVP
    print(f"Sending message to {to_number}: '{message_text}'")
    # In the final version, we'll replace this with the actual API call
    # import requests
    # url = f"https://graph.facebook.com/v19.0/{os.getenv('META_WA_PHONE_ID')}/messages"
    # headers = {"Authorization": f"Bearer {os.getenv('META_ACCESS_TOKEN')}", ...}
    # payload = {"messaging_product": "whatsapp", "to": to_number, ...}
    # response = requests.post(url, headers=headers, json=payload)
    # print(response.json())
    pass # for now, we just print the action

# --- Main entry point to run the Flask app ---
if __name__ == '__main__':
    # we will use local tunnel to expose this port to the internet
    app.run(host='0.0.0.0', port=5000, debug=True)