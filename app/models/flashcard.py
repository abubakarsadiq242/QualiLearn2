from app import db
from datetime import datetime

class Flashcard(db.Model):
    __tablename__ = 'flashcards'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Nullable for public cards
    front = db.Column(db.Text, nullable=False)
    back = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(100))
    language = db.Column(db.String(10), default='en')
    next_review_date = db.Column(db.DateTime, default=datetime.utcnow)
    difficulty_score = db.Column(db.Integer, default=0) # Simple rating
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'front': self.front,
            'back': self.back,
            'subject': self.subject,
            'language': self.language,
            'next_review_date': self.next_review_date.isoformat() if self.next_review_date else None,
            'difficulty_score': self.difficulty_score,
            'created_at': self.created_at.isoformat()
        }
