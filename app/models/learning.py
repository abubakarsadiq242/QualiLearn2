from app import db
from datetime import datetime

class LearningMaterial(db.Model):
    __tablename__ = 'learning_materials'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(10), default='en')
    material_type = db.Column(db.String(50))  # note, video_link, pdf_link
    resource_url = db.Column(db.String(500))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    education_level = db.Column(db.String(20), default='Academics') # Academics or Vocational
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'subject': self.subject,
            'education_level': self.education_level,
            'language': self.language,
            'material_type': self.material_type,
            'resource_url': self.resource_url,
            'topic_id': self.topic_id,
            'created_at': self.created_at.isoformat()
        }

class VocationalContent(db.Model):
    __tablename__ = 'vocational_content'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(10), default='en')
    resource_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'language': self.language,
            'resource_url': self.resource_url,
            'created_at': self.created_at.isoformat()
        }


