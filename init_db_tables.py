from app import create_app, db
from app.models.user import User
from app.models.analytics import ActivityLog, Assessment, Streak, Progress

def init_tables():
    app = create_app('development')
    with app.app_context():
        # Drop and recreate to apply schema changes
        db.drop_all()
        db.create_all()
        print("Success: All tables have been recreated with the latest schema.")

if __name__ == '__main__':
    init_tables()
