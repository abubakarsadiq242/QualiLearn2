from app import create_app, db
from app.models.learning import LearningMaterial

app = create_app('development')
with app.app_context():
    mats = LearningMaterial.query.filter_by(subject='Mathematics').all()
    print(f"Math Materials: {len(mats)}")
    for m in mats:
        print(f"ID: {m.id}, Title: {m.title}")
