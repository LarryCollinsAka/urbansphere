import os
import requests
import json

# Load Granite configurations from environment
IBM_GRANITE_API_URL = os.getenv("IBM_GRANITE_API_URL", "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29")
IBM_GRANITE_PROJECT_ID = os.getenv("IBM_GRANITE_PROJECT_ID")
IBM_GRANITE_MODEL_ID = os.getenv("IBM_GRANITE_MODEL_ID", "ibm/granite-3-3-8b-instruct")
IBM_GRANITE_TOKEN = os.getenv("IBM_GRANITE_TOKEN")

# Path to knowledge base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_PATH = os.path.join(BASE_DIR, 'knowledge_base.json')

def load_knowledge_base():
    with open(KB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def make_context_messages(kb):
    """
    Converts KB sections to context messages for Brenda prompt.
    """
    context_msgs = []
    if "urban_best_practices" in kb:
        context_msgs.append({
            "role": "system",
            "content": "Urban best practices: " + "; ".join(kb["urban_best_practices"])
        })
    if "air_quality_actions" in kb:
        context_msgs.append({
            "role": "system",
            "content": "Air quality improvement actions: " + "; ".join(kb["air_quality_actions"])
        })
    if "housing_upgrade_tips" in kb:
        context_msgs.append({
            "role": "system",
            "content": "Housing upgrade tips: " + "; ".join(kb["housing_upgrade_tips"])
        })
    if "civic_feedback_examples" in kb:
        context_msgs.append({
            "role": "system",
            "content": "Civic feedback examples: " + "; ".join(kb["civic_feedback_examples"])
        })
    # Add SDGs if present
    if "sdgs" in kb:
        sdg_summaries = [
            f"SDG {num}: {info.get('title', '')} - {info.get('description', '')}"
            for num, info in kb["sdgs"].items()
        ]
        context_msgs.append({
            "role": "system",
            "content": "Sustainable Development Goals context: " + "; ".join(sdg_summaries)
        })
    return context_msgs

def ask_brenda(user_message):
    """
    Sends a message to Brenda (Granite LLM) and returns the response.
    Appends knowledge base as context.
    """
    if not all([IBM_GRANITE_API_URL, IBM_GRANITE_PROJECT_ID, IBM_GRANITE_MODEL_ID, IBM_GRANITE_TOKEN]):
        raise RuntimeError("One or more Granite config variables are missing in environment.")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {IBM_GRANITE_TOKEN}"
    }

    # Load KB and build context
    kb = load_knowledge_base()
    context_messages = make_context_messages(kb)

    # System prompt for Brenda
    system_message = {
        "role": "system",
        "content": (
            "Your name is Brenda. You are an AI assistant for an Urban SDG platform. "
            "Your role is to help city residents and officials by answering questions about urban sustainability, "
            "air quality, housing upgrades, and civic feedback. "
            "Provide clear, actionable, and context-aware responses. "
            "If asked for suggestions or feedback, base them on sustainable development goals and best practices in urban planning. "
            "Always introduce yourself as Brenda when appropriate, and respond in a friendly, helpful tone."
        )
    }

    messages = [system_message] + context_messages + [{"role": "user", "content": user_message}]

    payload = {
        "messages": messages,
        "project_id": IBM_GRANITE_PROJECT_ID,
        "model_id": IBM_GRANITE_MODEL_ID,
        "frequency_penalty": 0,
        "max_tokens": 2000,
        "presence_penalty": 0,
        "temperature": 0,
        "top_p": 1,
        "seed": None,
        "stop": []
    }

    response = requests.post(IBM_GRANITE_API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

# Example usage (for testing):
# reply = ask_brenda("How can I improve air quality in my neighborhood?")
# print(json.dumps(reply, indent=2))