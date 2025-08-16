from flask import Flask, request
from app.whatsapp_handler import handle_whatsapp_webhook
import os

app = Flask(__name__)

META_VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN")

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
    handle_whatsapp_webhook(data)
    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run(debug=True)