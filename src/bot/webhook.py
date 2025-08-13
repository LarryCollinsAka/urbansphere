from flask import Blueprint, request, jsonify, current_app
import os

bot_blueprint = Blueprint("bot", __name__)

@bot_blueprint.route("/", methods=["GET"])
def verify():
    # WhatsApp webhook verification
    verify_token = os.getenv("VERIFY_TOKEN")
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode and token:
        if mode == "subscribe" and token == verify_token:
            return challenge, 200
    return "Verification failed", 403

@bot_blueprint.route("/", methods=["POST"])
def webhook():
    # WhatsApp webhook receiver
    data = request.get_json()
    # TODO: Add logic to process incoming WhatsApp messages here
    print("Received WhatsApp message:", data)
    return jsonify(status="received"), 200