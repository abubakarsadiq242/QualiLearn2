from app import db
from datetime import datetime

class StudySession(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    portal_type = db.Column(db.String(20), default='secondary') # 'secondary' or 'vocational'
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    portal_type = db.Column(db.String(20), default='secondary')
    session_id = db.Column(db.String(50))
    activity_type = db.Column(db.String(50))
    module = db.Column(db.String(100))
    start_time = db.Column(db.String(50), default=lambda: datetime.utcnow().isoformat())
    end_time = db.Column(db.String(50))
    duration = db.Column(db.Integer)
    score = db.Column(db.Integer)
    topic_id = db.Column(db.Integer)
    video_id = db.Column(db.Integer)
    created_at = db.Column(db.String(50), default=lambda: datetime.utcnow().isoformat())

class Assessment(db.Model):
    __tablename__ = 'assessments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    portal_type = db.Column(db.String(20), default='secondary')
    total_questions = db.Column(db.Integer)
    correct_answers = db.Column(db.Integer)
    passed = db.Column(db.Boolean)
    created_at = db.Column(db.String(50), default=lambda: datetime.utcnow().isoformat())

class Streak(db.Model):
    __tablename__ = 'streaks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    portal_type = db.Column(db.String(20), default='secondary')
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_active_date = db.Column(db.String(20))
    __table_args__ = (db.UniqueConstraint('user_id', 'portal_type', name='_user_portal_streak_uc'),)

class Progress(db.Model):
    __tablename__ = 'progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    portal_type = db.Column(db.String(20), default='secondary')
    completed_units = db.Column(db.Integer, default=0)
    total_units = db.Column(db.Integer, default=100)
    __table_args__ = (db.UniqueConstraint('user_id', 'portal_type', name='_user_portal_progress_uc'),)

class CompletedItem(db.Model):
    __tablename__ = 'completed_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    portal_type = db.Column(db.String(20), default='secondary')
    item_id = db.Column(db.Integer)
    item_type = db.Column(db.String(50)) # 'subject', 'flashcard', 'video', 'assessment'
    __table_args__ = (db.UniqueConstraint('user_id', 'portal_type', 'item_id', 'item_type', name='_user_portal_item_uc'),)
