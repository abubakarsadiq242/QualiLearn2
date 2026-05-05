from app import create_app, db
from app.models.analytics import ActivityLog, Assessment, Progress, CompletedItem, Streak
from app.models.user import User
from datetime import datetime, timedelta

app = create_app('development')
with app.app_context():
    # 1. CLEAN UP ADMIN DATA
    admin = User.query.filter_by(email='qualilearn@qualilearn.com').first()
    if admin:
        ActivityLog.query.filter_by(user_id=admin.id).delete()
        Assessment.query.filter_by(user_id=admin.id).delete()
        CompletedItem.query.filter_by(user_id=admin.id).delete()
        Progress.query.filter_by(user_id=admin.id).delete()
        Streak.query.filter_by(user_id=admin.id).delete()
        print("Cleaned up Admin test data.")

    # 2. SEED STUDENT DATA
    student_email = 'student@qualilearn.com'
    user = User.query.filter_by(email=student_email).first()
    
    if not user:
        # Create student if not exists
        user = User(first_name="Sadiq", last_name="Abubakar", email=student_email, education_level="Academics")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        print(f"Created Student user: {student_email}")

    user_id = user.id
    now = datetime.utcnow()
    
    # Study Time: 3.5 hours
    for i in range(7):
        log = ActivityLog(
            user_id=user_id,
            portal_type='secondary',
            activity_type='subject_learning',
            module='Physics',
            duration=1800, 
            start_time=(now - timedelta(hours=i)).isoformat() + "Z",
            created_at=(now - timedelta(hours=i)).isoformat() + "Z"
        )
        db.session.add(log)

    # Assessments: 5 Passed
    for i in range(5):
        res = Assessment(
            user_id=user_id,
            portal_type='secondary',
            total_questions=10,
            correct_answers=10,
            passed=True,
            created_at=(now - timedelta(days=i)).isoformat() + "Z"
        )
        db.session.add(res)

    # Progress: 24 units
    for i in range(24):
        item = CompletedItem(
            user_id=user_id,
            portal_type='secondary',
            item_id=200 + i,
            item_type='subject'
        )
        db.session.add(item)
    
    # Streak: 7 days
    streak = Streak.query.filter_by(user_id=user_id, portal_type='secondary').first()
    if not streak:
        streak = Streak(user_id=user_id, portal_type='secondary', current_streak=7, last_active_date=now.date().isoformat())
        db.session.add(streak)
    else:
        streak.current_streak = 7
        streak.last_active_date = now.date().isoformat()

    db.session.commit()
    print(f"Successfully seeded sample data for {student_email}")
