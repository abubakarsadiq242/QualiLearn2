from app import create_app, db
from app.models.assessment import PastQuestion

def check():
    app = create_app('development')
    with app.app_context():
        subjects = ['Mathematics', 'Science', 'English', 'Physics', 'Chemistry']
        for sub in subjects:
            count = PastQuestion.query.filter_by(subject=sub).count()
            print(f"{sub}: {count} questions")

if __name__ == '__main__':
    check()
