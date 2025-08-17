import os
from flask import Flask, request, render_template
import requests
import json

# Define the absolute path to the templates folder.
# This ensures it works correctly on any server, including Render,
# by looking for 'templates' one directory up from 'app'.
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))

# Create the Flask app instance with the specified template folder.
app = Flask(__name__, template_folder=template_dir)

# Load configurations from environment variables
META_VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")

# --- Route to serve the Dashboard ---
@app.route("/")
def dashboard():
    """
    Renders the index.html file from the templates folder.
    This serves as the main entry point for the dashboard.
    """
    return render_template("index.html")

# --- WhatsApp Webhook Routes ---
@app.route("/webhook/whatsapp", methods=["GET"])
def whatsapp_verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == META_VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403

@app.route("/webhook/whatsapp", methods=["POST"])
def whatsapp_webhook():
    data = request.get_json()
    # Assuming you have a handle_whatsapp_webhook function
    # from your previous whatsapp_handler.py file.
    # You would need to import and call it here.
    # from app.whatsapp_handler import handle_whatsapp_webhook
    # handle_whatsapp_webhook(data)
    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run(debug=True)