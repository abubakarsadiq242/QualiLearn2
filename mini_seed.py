from app import create_app, db
from app.models.user import User
from app.models.analytics import ActivityLog
from datetime import datetime

app = create_app('development')
with app.app_context():
    user = User.query.filter_by(email='student@qualilearn.com').first()
    if user:
        # Clear existing to be sure
        ActivityLog.query.filter_by(user_id=user.id).delete()
        log = ActivityLog(
            user_id=user.id, 
            portal_type='secondary', 
            activity_type='study', 
            duration=60, # Exactly 1 minute
            start_time=datetime.utcnow().isoformat()+'Z',
            created_at=datetime.utcnow().isoformat()+'Z'
        )
        db.session.add(log)
        db.session.commit()
        print('Seeded exactly 1 min for student')
