from app import create_app, db
from app.models.learning import LearningMaterial

def update_video():
    app = create_app('development')
    with app.app_context():
        # Update English
        mat = LearningMaterial.query.filter_by(title='Calculus: Integration', subject='Mathematics').first()
        if mat:
            mat.resource_url = 'https://www.youtube.com/embed/6WUjbJEeJwM'
            print("Updated English Integration")
        
        # Update others
        mats = LearningMaterial.query.filter(LearningMaterial.title.like('%Integration%')).all()
        for m in mats:
            m.resource_url = 'https://www.youtube.com/embed/6WUjbJEeJwM'
            print(f"Updated {m.title} ({m.language})")
            
        db.session.commit()
        print("Done")

if __name__ == '__main__':
    update_video()
