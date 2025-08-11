from flask import Blueprint, render_template
from services import db_service

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/dashboard')
def dashboard():
    """
    Renders the dashboard and passes conversation data from MongoDB.
    """
    db = db_service.get_db()
    conversations = []
    
    # CORRECTED: Use 'is not None' for truth value testing
    if db is not None:
        # Get all conversations from the 'conversations' collection
        conversations_collection = db.conversations
        conversations = list(conversations_collection.find({}))
    
    # We pass the conversation data to the dashboard template.
    return render_template('dashboard.html', conversations=conversations)