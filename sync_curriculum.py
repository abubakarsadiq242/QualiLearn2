from app import create_app, db
from app.models.topics import Topic
from app.models.learning import LearningMaterial
import os

app = create_app('development')
with app.app_context():
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Check topics
    topics = Topic.query.all()
    subjects = set(t.subject for t in topics)
    print(f"Distinct subjects in topics: {subjects}")
    
    # Check materials
    mats = LearningMaterial.query.all()
    mat_subjects = set(m.subject for m in mats)
    print(f"Distinct subjects in learning_materials: {mat_subjects}")
    
    # Perform update
    updated_topics = Topic.query.filter(Topic.subject.in_(['Physics', 'Chemistry'])).update({Topic.subject: 'Science'}, synchronize_session=False)
    updated_mats = LearningMaterial.query.filter(LearningMaterial.subject.in_(['Physics', 'Chemistry'])).update({LearningMaterial.subject: 'Science'}, synchronize_session=False)
    
    db.session.commit()
    print(f"Updated {updated_topics} topics and {updated_mats} materials to 'Science'.")
