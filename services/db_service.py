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
    if client is not None:
        return client.urbansphere_db
    print("WARNING: Database client is not connected.")
    return None

def save_conversation(conversation_id, conversation_data):
    """
    Saves a conversation to the 'conversations' collection.
    """
    db = get_db()
    if db is not None:
        try:
            conversations_collection = db.conversations
            conversations_collection.update_one(
                {"_id": conversation_id},
                {"$set": conversation_data},
                upsert=True
            )
            print(f"Conversation with ID '{conversation_id}' successfully saved to database.")
        except Exception as e:
            print(f"ERROR: Failed to save conversation with ID '{conversation_id}'. Reason: {e}")
    else:
        print(f"WARNING: Could not save conversation with ID '{conversation_id}'. Database connection not available.")

def get_conversation_history(conversation_id):
    """
    Retrieves a conversation's history from the 'conversations' collection.
    """
    db = get_db()
    if db is not None:
        try:
            conversations_collection = db.conversations
            conversation = conversations_collection.find_one({"_id": conversation_id})
            if conversation:
                print(f"Successfully retrieved conversation history for ID '{conversation_id}'.")
                return conversation.get('history', [])
            else:
                print(f"No conversation history found for ID '{conversation_id}'.")
                return []
        except Exception as e:
            print(f"ERROR: Failed to retrieve conversation with ID '{conversation_id}'. Reason: {e}")
            return []
    else:
        print(f"WARNING: Could not retrieve conversation history. Database connection not available.")
    return []
    
def get_all_conversations():
    """
    Retrieves all conversations from the 'conversations' collection.
    """
    db = get_db()
    if db is not None:
        try:
            conversations_collection = db.conversations
            all_conversations = list(conversations_collection.find({}))
            print("Successfully retrieved all conversations from the database.")
            return all_conversations
        except Exception as e:
            print(f"ERROR: Failed to retrieve all conversations. Reason: {e}")
            return []
    else:
        print(f"WARNING: Could not retrieve all conversations. Database connection not available.")
    return []