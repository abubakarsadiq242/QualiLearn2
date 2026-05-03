from app import db, bcrypt
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='student')  # student, admin
    education_level = db.Column(db.String(50))
    language = db.Column(db.String(10), default='en')  # en, ha, yo, ig
    overall_progress = db.Column(db.Float, default=0.0)
    study_time = db.Column(db.Integer, default=0)  # Total minutes
    daily_study_time = db.Column(db.Integer, default=0) # Daily minutes
    assessments_passed = db.Column(db.Integer, default=0)
    resume_topic_id = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    last_activity_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        hours = self.study_time // 60
        minutes = self.study_time % 60
        
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'role': self.role,
            'education_level': self.education_level,
            'language': self.language,
            'overall_progress': self.overall_progress,
            'study_time_raw': self.study_time,
            'study_time': f"{hours}h {minutes}m",
            'assessments_passed': self.assessments_passed,
            'resume_topic_id': self.resume_topic_id,
            'current_streak': self.current_streak,
            'last_activity_date': self.last_activity_date.isoformat() if self.last_activity_date else None,
            'created_at': self.created_at.isoformat()
        }
