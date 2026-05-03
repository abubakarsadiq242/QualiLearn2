from app import create_app, db
from app.models.analytics import ActivityLog, Assessment, Progress, CompletedItem, Streak
from app.models.user import User
from datetime import datetime, timedelta

app = create_app('development')
with app.app_context():
    # Target the admin user specifically
    admin_email = 'qualilearn@qualilearn.com'
    user = User.query.filter_by(email=admin_email).first()
    
    if not user:
        print(f"User {admin_email} not found. Seeding failed.")
        exit()

    user_id = user.id
    now = datetime.utcnow()
    month_start = now.replace(day=1).isoformat() + "Z"
    
    # 1. Seed 2 hours of study time (7200 seconds)
    # Split into a few sessions
    for i in range(4):
        log = ActivityLog(
            user_id=user_id,
            portal_type='secondary',
            activity_type='subject_learning',
            module='Mathematics',
            duration=1800, # 30 mins each
            start_time=(now - timedelta(hours=i)).isoformat() + "Z",
            created_at=(now - timedelta(hours=i)).isoformat() + "Z"
        )
        db.session.add(log)

    # 2. Seed 3 passed assessments
    for i in range(3):
        res = Assessment(
            user_id=user_id,
            portal_type='secondary',
            total_questions=10,
            correct_answers=9,
            passed=True,
            created_at=(now - timedelta(days=i)).isoformat() + "Z"
        )
        db.session.add(res)

    # 3. Seed Progress (15 units)
    # Add some completed items first
    for i in range(15):
        item = CompletedItem(
            user_id=user_id,
            portal_type='secondary',
            item_id=100 + i,
            item_type='subject'
        )
        db.session.add(item)
    
    prog = Progress.query.filter_by(user_id=user_id, portal_type='secondary').first()
    if not prog:
        prog = Progress(user_id=user_id, portal_type='secondary', completed_units=15, total_units=200)
        db.session.add(prog)
    else:
        prog.completed_units = 15
        prog.total_units = 200

    # 4. Seed Streak
    streak = Streak.query.filter_by(user_id=user_id, portal_type='secondary').first()
    if not streak:
        streak = Streak(user_id=user_id, portal_type='secondary', current_streak=5, last_active_date=now.date().isoformat())
        db.session.add(streak)
    else:
        streak.current_streak = 5
        streak.last_active_date = now.date().isoformat()

    db.session.commit()
    print(f"Successfully seeded sample data for {admin_email}")
    print("Refresh your dashboard to see the results!")
