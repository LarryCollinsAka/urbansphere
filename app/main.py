import os
import json
from flask import Flask, render_template, jsonify, request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, '..', 'static')
KB_PATH = os.path.join(BASE_DIR, 'knowledge_base.json')

# Replace with your Meta Cloud verify token
META_VERIFY_TOKEN = "YOUR_VERIFY_TOKEN"

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

def load_knowledge_base():
    with open(KB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/sdg/<sdg_number>")
def sdg(sdg_number):
    kb = load_knowledge_base()
    sdg_info = kb.get("sdgs", {}).get(sdg_number, {})
    return jsonify(sdg_info)

@app.route("/api/best_practices")
def best_practices():
    kb = load_knowledge_base()
    return jsonify(kb.get("urban_best_practices", []))

@app.route("/api/air_quality_actions")
def air_quality_actions():
    kb = load_knowledge_base()
    return jsonify(kb.get("air_quality_actions", []))

@app.route("/api/housing_upgrade_tips")
def housing_upgrade_tips():
    kb = load_knowledge_base()
    return jsonify(kb.get("housing_upgrade_tips", []))

@app.route("/api/civic_feedback_examples")
def civic_feedback_examples():
    kb = load_knowledge_base()
    return jsonify(kb.get("civic_feedback_examples", []))

@app.route("/api/brenda", methods=["POST"])
def brenda_answer():
    kb = load_knowledge_base()
    data = request.get_json()
    question = data.get("question", "")

    context = {
        "best_practices": kb.get("urban_best_practices", []),
        "air_quality": kb.get("air_quality_actions", []),
        "housing": kb.get("housing_upgrade_tips", []),
        "feedback_examples": kb.get("civic_feedback_examples", [])
    }

    brenda_response = {
        "answer": f"Brenda (stub): I received your question: '{question}'. My knowledge base contains helpful info!",
        "context": context
    }

    return jsonify(brenda_response)

# --- WhatsApp Webhook Verification (GET) ---
@app.route("/webhook/whatsapp", methods=["GET"])
def whatsapp_verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == META_VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403

# --- WhatsApp Webhook for Incoming Messages (POST) ---
@app.route("/webhook/whatsapp", methods=["POST"])
def whatsapp_webhook():
    data = request.get_json()
    # The structure below is typical for Meta WhatsApp Cloud API
    try:
        entry = data.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])
        if messages:
            msg = messages[0]
            text = msg.get("text", {}).get("body", "")
            sender = msg.get("from", "")
            # Call Brenda (stub)
            kb = load_knowledge_base()
            context = {
                "best_practices": kb.get("urban_best_practices", []),
                "air_quality": kb.get("air_quality_actions", []),
                "housing": kb.get("housing_upgrade_tips", []),
                "feedback_examples": kb.get("civic_feedback_examples", [])
            }
            # TODO: Replace with call to Granite LLM
            answer = f"Brenda (stub): You said '{text}'. Here's a tip: {context['best_practices'][0]}"
            # Log or process as needed
            print(f"WhatsApp message from {sender}: {text}")
        else:
            print("No WhatsApp message found in webhook payload.")
    except Exception as e:
        print(f"Error processing WhatsApp webhook: {e}")

    # Meta expects a 200 OK and "EVENT_RECEIVED"
    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run(debug=True)