from app import db
from datetime import datetime

class PastQuestion(db.Model):
    __tablename__ = 'past_questions'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    topic = db.Column(db.String(200))
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(500))
    option_b = db.Column(db.String(500))
    option_c = db.Column(db.String(500))
    option_d = db.Column(db.String(500))
    correct_answer = db.Column(db.String(1), nullable=False)  # A, B, C, D
    explanation = db.Column(db.Text)
    language = db.Column(db.String(10), default='en')
    education_level = db.Column(db.String(50), default='SSS') # JSS, SSS, Primary

    def to_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'year': self.year,
            'topic': self.topic,
            'education_level': self.education_level,
            'question_text': self.question_text,
            'options': {
                'A': self.option_a,
                'B': self.option_b,
                'C': self.option_c,
                'D': self.option_d
            },
            'correct_answer': self.correct_answer,
            'explanation': self.explanation,
            'language': self.language
        }

class AssessmentTemplate(db.Model):
    __tablename__ = 'assessment_templates'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    time_limit = db.Column(db.Integer)  # in minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    questions = db.relationship('Question', backref='template', lazy=True)

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment_templates.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(500))
    option_b = db.Column(db.String(500))
    option_c = db.Column(db.String(500))
    option_d = db.Column(db.String(500))
    correct_option = db.Column(db.String(1), nullable=False)

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment_templates.id'), nullable=True)
    score = db.Column(db.Float, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        template = AssessmentTemplate.query.get(self.assessment_id)
        return {
            'id': self.id,
            'assessment_title': template.title if template else f"Assessment #{self.assessment_id}",
            'score': self.score,
            'total_questions': self.total_questions,
            'completed_at': self.completed_at.isoformat()
        }
