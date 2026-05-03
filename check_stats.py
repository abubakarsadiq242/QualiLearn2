from app import create_app, db
from app.models.analytics import ActivityLog, Assessment, Progress, CompletedItem
from app.models.user import User

app = create_app('development')
with app.app_context():
    print("--- Diagnostic Report ---")
    users = User.query.count()
    print(f"Total Users: {users}")
    
    logs_count = ActivityLog.query.count()
    print(f"Total Activity Logs: {logs_count}")
    
    if logs_count > 0:
        last_log = ActivityLog.query.order_by(ActivityLog.id.desc()).first()
        print(f"Last Log - Type: {last_log.activity_type}, StartTime: {last_log.start_time}, Portal: {last_log.portal_type}, Duration: {last_log.duration}")
        
        # Check for NULL start_times
        null_starts = ActivityLog.query.filter(ActivityLog.start_time == None).count()
        print(f"Logs with NULL StartTime: {null_starts}")
        
    assessments = Assessment.query.count()
    print(f"Total Assessment Results: {assessments}")
    
    items = CompletedItem.query.count()
    print(f"Total Completed Items: {items}")
    
    progs = Progress.query.count()
    print(f"Total Progress Rows: {progs}")
    
    if progs > 0:
        last_prog = Progress.query.first()
        print(f"Sample Progress - User: {last_prog.user_id}, Portal: {last_prog.portal_type}, Units: {last_prog.completed_units}/{last_prog.total_units}")

    print("--- End Report ---")
