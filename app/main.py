import os
import json
from flask import Flask, render_template, jsonify, request
from brenda import ask_brenda

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, '..', 'static')
KB_PATH = os.path.join(BASE_DIR, 'app/knowledge_base.json')

# Load Meta Cloud verify token from environment
META_VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN")

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
    data = request.get_json()
    question = data.get("question", "")
    print(f"[Brenda Prompt Lab] User question: {question}")
    try:
        brenda_response = ask_brenda(question)
        print(f"[Brenda Response] {json.dumps(brenda_response, indent=2)}")
        # Return only the assistant's reply text for convenience
        answer = brenda_response.get("choices", [{}])[0].get("message", {}).get("content", "")
        return jsonify({"answer": answer, "raw": brenda_response})
    except Exception as e:
        print(f"[Brenda Error] {e}")
        return jsonify({"error": str(e)}), 500

# --- WhatsApp Webhook Verification (GET) with debugging ---
@app.route("/webhook/whatsapp", methods=["GET"])
def whatsapp_verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    print("---- WhatsApp Webhook Verification ----")
    print(f"Received GET /webhook/whatsapp with:")
    print(f"  hub.mode = {mode}")
    print(f"  hub.verify_token = {token}")
    print(f"  hub.challenge = {challenge}")
    print(f"  META_VERIFY_TOKEN (env) = {META_VERIFY_TOKEN}")
    if mode == "subscribe" and token == META_VERIFY_TOKEN:
        print("  Verification successful! Returning challenge.")
        return challenge, 200
    print("  Verification failed! Returning 403 Forbidden.")
    return "Forbidden", 403

# --- WhatsApp Webhook for Incoming Messages (POST) with Brenda integration ---
@app.route("/webhook/whatsapp", methods=["POST"])
def whatsapp_webhook():
    print("---- WhatsApp Webhook Message Received ----")
    try:
        data = request.get_json()
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
            # Call Brenda (Granite)
            brenda_response = ask_brenda(text)
            answer = brenda_response.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"Brenda response: {answer}")
            # TODO: Send 'answer' back to WhatsApp using Meta Cloud API (outbound)
        else:
            print("No WhatsApp message found in webhook payload.")
    except Exception as e:
        print(f"Error processing WhatsApp webhook: {e}")

    # Meta expects a 200 OK and "EVENT_RECEIVED"
    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run(debug=True)