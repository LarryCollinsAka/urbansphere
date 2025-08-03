import os
import json
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Initialize Flask app ---
app = Flask(__name__)

# --- Load all agent configurations ---
agent_configs = {}
try:
    for filename in os.listdir('agent_config'):
        if filename.endswith('.json'):
            agent_name = filename.split('.')[0]
            with open(f'agent_config/{filename}', 'r') as f:
                agent_configs[agent_name] = json.load(f)
    print("Agent configurations loaded successfully.")
except FileNotFoundError:
    print("WARNING: 'config' directory not found. Please create it.")
    agent_configs = {}

# --- Load all agent RAG knowledge bases ---
knowledge_bases = {}
try:
    for filename in os.listdir('knowledge_base'):
        if filename.endswith('.json'):
            agent_name = filename.split('_data')[0]
            with open(f'knowledge_base/{filename}', 'r') as f:
                knowledge_bases[agent_name] = json.load(f)
    print("Knowledge bases loaded successfully.")
except FileNotFoundError:
    print("WARNING: 'knowledge_base' directory not found. Please create it.")
    knowledge_bases = {}


# --- A simple, in-memory store for conversational history (from our new memory.py module) ---
session_store = {}

# --- Import agent modules (e.g., from agents/sanita.py) ---
def handle_sanita_request(message, entities, conversation_history):
    return f"Sanita here! I received your message about {entities.get('topic', 'waste')}. I'll use our knowledge base to help you."

def handle_qumy_request(message, entities, conversation_history):
    return f"Qumy at your service! I've logged your request about {entities.get('topic', 'a queue')}. I can find the wait time for you."


# --- Brenda's Core Orchestration Logic ---
def brenda_orchestrator(user_message, conversation_history):
    # This is the central hub. It uses an LLM for NLU and routes to agents.
    if "waste" in user_message.lower():
        intent = "sanita_waste_report"
        entities = {"topic": "waste", "location": "unspecified"}
    elif "queue" in user_message.lower():
        intent = "qumy_queue_status"
        entities = {"topic": "queue", "service": "unspecified"}
    else:
        intent = "fallback_unclear"
        entities = {}

    updated_history = conversation_history + [{'user': user_message, 'agent': 'processing...'}]

    agent_response = "I'm sorry, I couldn't understand that."
    if intent == "sanita_waste_report":
        agent_response = handle_sanita_request(user_message, entities, updated_history)
    elif intent == "qumy_queue_status":
        agent_response = handle_qumy_request(user_message, entities, updated_history)
    
    updated_history[-1]['agent'] = agent_response

    return agent_response, updated_history


# --- WhatsApp Webhook Routes ---
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

@app.route('/webhook', methods=['POST'])
def process_message():
    data = request.json
    print(f"Received data: {data}")

    if not data or 'object' not in data or 'entry' not in data:
        return jsonify({'status': 'ok'}), 200

    try:
        message_info = data['entry'][0]['changes'][0]['value']['messages'][0]
        sender_id = message_info['from']
        
        conversation_history = session_store.get(sender_id, [])

        if message_info['type'] == 'text':
            user_message = message_info['text']['body']
            print(f"User text message from {sender_id}: {user_message}")
            
            brenda_response, updated_history = brenda_orchestrator(user_message, conversation_history)
            
            session_store[sender_id] = updated_history
            send_whatsapp_message(sender_id, brenda_response)
        
        elif message_info['type'] == 'image':
            send_whatsapp_message(sender_id, "I'm currently processing that image with our Vision AI. Please hold!")
        elif message_info['type'] == 'audio':
            send_whatsapp_message(sender_id, "I'm currently transcribing that voice note with our Speech-to-Text service. Please hold!")

    except (KeyError, IndexError) as e:
        print(f"Error processing message data: {e}")
        return jsonify({'status': 'ok'}), 200

    return jsonify({'status': 'ok'}), 200

# --- NEW API ROUTE FOR THE DASHBOARD ---
@app.route('/api/data')
def get_dashboard_data():
    """
    Returns a JSON object with all the data needed for the dashboard.
    This includes agent status and the full conversation history.
    """
    # Prepare agent status data dynamically from the config folder
    agent_status = [{"name": name, "status": "Online"} for name in agent_configs.keys()]

    # Format the conversation history for display
    conversation_log = []
    for sender_id, history in session_store.items():
        for interaction in history:
            # We can't use the 'processing...' placeholder here
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


# --- Main entry point to run the Flask app (UPDATED) ---
@app.route('/')
def home():
    return "UrbanSphere is running! Your webhook is at /webhook."

@app.route('/dashboard')
def show_dashboard():
    return render_template('views/dashboard.html')

def send_whatsapp_message(to_number, message_text):
    print(f"Sending message to {to_number}: '{message_text}'")
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
