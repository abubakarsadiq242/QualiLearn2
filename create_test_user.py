from app import create_app, db, bcrypt
from app.models.user import User
from datetime import date

def create_test_user():
    app = create_app('development')
    with app.app_context():
        # Vocational User
        voc_pass = bcrypt.generate_password_hash('voc123').decode('utf-8')
        user = User(
            first_name="Tunde",
            last_name="Workshop",
            email="voc@qualilearn.com",
            password_hash=voc_pass,
            role="student",
            education_level="Vocational",
            language="en",
            overall_progress=10,
            study_time=300,
            current_streak=3,
            last_activity_date=date.today()
        )
        
        # Check if exists
        exists = User.query.filter_by(email=user.email).first()
        if not exists:
            db.session.add(user)
            db.session.commit()
            print(f"Created vocational user: {user.email}")
        else:
            print(f"User {user.email} already exists")

if __name__ == '__main__':
    create_test_user()
