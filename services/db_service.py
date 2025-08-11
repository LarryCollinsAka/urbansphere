from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
from urllib.parse import quote_plus
import os

# Get the connection URI from the environment variables.
# We'll use quote_plus to handle special characters in the password.
password = quote_plus(os.environ.get('MONGO_DB_PASSWORD', ''))
uri = f"mongodb+srv://{os.environ.get('MONGO_DB_USER', '')}:{password}@{os.environ.get('MONGO_DB_CLUSTER', '')}/?retryWrites=true&w=majority"

# Create a new client and connect to the server
try:
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except ConnectionFailure:
    print("Failed to connect to MongoDB.")
    client = None

def get_db():
    """
    Returns the MongoDB database object for UrbanSphere.
    """
    if client:
        return client.urbansphere_db
    return None

def save_conversation(conversation_id, conversation_data):
    """
    Saves a conversation to the 'conversations' collection.
    """
    db = get_db()
    if db:
        conversations_collection = db.conversations
        conversations_collection.update_one(
            {"_id": conversation_id},
            {"$set": conversation_data},
            upsert=True
        )
        print(f"Conversation with ID '{conversation_id}' saved to database.")

def get_conversation_history(conversation_id):
    """
    Retrieves a conversation's history from the 'conversations' collection.
    """
    db = get_db()
    if db:
        conversations_collection = db.conversations
        conversation = conversations_collection.find_one({"_id": conversation_id})
        return conversation.get('history', []) if conversation else []
    return []