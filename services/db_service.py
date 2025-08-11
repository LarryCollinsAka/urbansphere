from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
from urllib.parse import quote_plus
import os

# A global variable to store the database client once it's created.
client = None

def initialize_db_client():
    """
    Initializes the MongoDB client.
    This function will only run once to create a single client instance.
    """
    global client
    if client is not None:
        return client

    # Get the connection URI from the environment variables.
    password = quote_plus(os.environ.get('MONGO_DB_PASSWORD', ''))
    uri = f"mongodb+srv://{os.environ.get('MONGO_DB_USER', '')}:{password}@{os.environ.get('MONGO_DB_CLUSTER', '')}/?retryWrites=true&w=majority"

    try:
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB. Reason: {e}")
        client = None
    except Exception as e:
        print(f"An unexpected error occurred during MongoDB connection: {e}")
        client = None

    return client

def get_db():
    """
    Returns the MongoDB database object for UrbanSphere.
    It will first ensure the client is initialized.
    """
    db_client = initialize_db_client()
    if db_client is not None:
        return db_client.urbansphere_db
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