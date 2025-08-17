import requests
import os
import json

# --- Configurations from environment variables ---
IBM_GRANITE_API_URL = os.getenv("IBM_GRANITE_API_URL", "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29")
IBM_GRANITE_PROJECT_ID = os.getenv("IBM_GRANITE_PROJECT_ID", "b012ad9b-5420-4b92-a637-354512fd7685")
IBM_GRANITE_TOKEN = os.getenv("IBM_GRANITE_TOKEN")

def ask_brenda_with_curl_style(user_message):
    """
    Makes a request to the IBM watsonx Granite API using the exact payload from the cURL command.
    """
    if not IBM_GRANITE_TOKEN:
        print("IBM_GRANITE_TOKEN not set!")
        return None

    # The full payload body, including the system message and user's prompt
    body = {
        "messages": [
            {
                "role": "system",
                "content": "Your name is Brenda. You are an AI assistant for an Urban SDG platform. \nYour role is to help city residents and officials by answering questions about urban sustainability, air quality, housing upgrades, and civic feedback.\nProvide clear, actionable, and context-aware responses. \nIf asked for suggestions or feedback, base them on sustainable development goals and best practices in urban planning.\nAlways introduce yourself as Brenda when appropriate, and respond in a friendly, helpful tone."
            },
            {
                "role": "user",
                "content": user_message # The user's message is inserted here
            }
        ],
        "project_id": IBM_GRANITE_PROJECT_ID,
        "model_id": "ibm/granite-3-3-8b-instruct",
        "frequency_penalty": 0,
        "max_tokens": 2000,
        "presence_penalty": 0,
        "temperature": 0,
        "top_p": 1,
        "seed": None,
        "stop": []
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {IBM_GRANITE_TOKEN}"
    }

    try:
        response = requests.post(
            IBM_GRANITE_API_URL,
            headers=headers,
            json=body
        )
        response.raise_for_status() # Raises an HTTPError if the status is 4xx or 5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling IBM watsonx API: {e}")
        return None
