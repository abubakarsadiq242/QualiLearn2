from app import db
from datetime import datetime
import re

class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    education_level = db.Column(db.String(20), default='Academics') # Academics or Vocational
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    videos = db.relationship('TopicVideo', backref='topic', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "subject": self.subject,
            "education_level": self.education_level,
            "created_at": self.created_at.isoformat()
        }

class TopicVideo(db.Model):
    __tablename__ = 'topic_videos'
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    video_url = db.Column(db.String(500), nullable=False)
    video_title = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_video_id(self):
        # Regex to extract YouTube ID from Various formats
        regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
        match = re.search(regex, self.video_url)
        return match.group(1) if match else None

    def to_dict(self):
        video_id = self.get_video_id()
        return {
            "id": self.id,
            "topic_id": self.topic_id,
            "video_url": self.video_url,
            "video_id": video_id,
            "embed_url": f"https://www.youtube.com/embed/{video_id}" if video_id else None,
            "video_title": self.video_title or f"Video {self.id}",
            "created_at": self.created_at.isoformat()
        }
