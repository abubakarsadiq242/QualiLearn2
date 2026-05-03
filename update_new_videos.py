from app import create_app, db
from app.models.learning import LearningMaterial

def update_new_links():
    app = create_app('development')
    with app.app_context():
        # Newton's Laws
        mats = LearningMaterial.query.filter(LearningMaterial.title.like("%Newton%")).all()
        for m in mats:
            m.resource_url = 'https://www.youtube.com/embed/g550H4e5FCY'
            print(f"Updated {m.title} ({m.language})")
            
        # Atomic Structure
        mats = LearningMaterial.query.filter(LearningMaterial.title.like("%Atomic Structure%")).all()
        for m in mats:
            m.resource_url = 'https://www.youtube.com/embed/OH-aSu-rWgk'
            print(f"Updated {m.title} ({m.language})")
            
        db.session.commit()
        print("Done")

if __name__ == '__main__':
    update_new_links()
