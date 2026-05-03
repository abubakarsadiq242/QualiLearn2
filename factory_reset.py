from app import create_app, db
from app.models.analytics import ActivityLog, Assessment, Progress, CompletedItem, Streak, StudySession
from app.models.user import User

app = create_app('development')
with app.app_context():
    print("--- Starting Factory Reset of Analytics Data ---")
    
    try:
        # 1. Clear Activity Logs
        logs_deleted = ActivityLog.query.delete()
        print(f"Deleted {logs_deleted} Activity Logs.")
        
        # 2. Clear Assessment Results
        assess_deleted = Assessment.query.delete()
        print(f"Deleted {assess_deleted} Assessment Results.")
        
        # 3. Clear Completed Items
        items_deleted = CompletedItem.query.delete()
        print(f"Deleted {items_deleted} Completed Items.")
        
        # 4. Clear Progress Rows
        prog_deleted = Progress.query.delete()
        print(f"Deleted {prog_deleted} Progress Rows.")
        
        # 5. Clear Streaks
        streaks_deleted = Streak.query.delete()
        print(f"Deleted {streaks_deleted} Streaks.")
        
        # 6. Clear Study Sessions
        sessions_deleted = StudySession.query.delete()
        print(f"Deleted {sessions_deleted} Sessions.")
        
        # 7. Reset User-specific summary fields if any
        users = User.query.all()
        for u in users:
            u.resume_topic_id = None
            # Reset legacy fields if they exist
            if hasattr(u, 'study_time'): u.study_time = 0
            if hasattr(u, 'overall_progress'): u.overall_progress = 0
        
        db.session.commit()
        print(f"Reset user profile fields for {len(users)} users.")
        print("--- Factory Reset Complete ---")
        print("All dashboard metrics should now be 0% and fresh.")
        
    except Exception as e:
        db.session.rollback()
        print(f"ERROR DURING RESET: {str(e)}")
