from src.app import db
from datetime import datetime

class Task(db.Model):
    """
    Database model for a task in the agent's queue.
    """
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.String(50), nullable=False)
    message_body = db.Column(db.String(500), nullable=False)
    intent = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='New', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.id} | Intent: {self.intent} | Status: {self.status}>"