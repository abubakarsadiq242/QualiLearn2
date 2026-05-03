import sqlite3

import os

def verify_storage():
    print(">>> VERIFYING SQLITE STORAGE")
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'qualilearn_v2.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Count logs
    cursor.execute("SELECT count(*) FROM activity_logs")
    log_count = cursor.fetchone()[0]
    print(f">>> DB TRACE: Total activity_logs = {log_count}")
    
    # 2. Check total duration
    cursor.execute("SELECT sum(duration) FROM activity_logs")
    total_dur = cursor.fetchone()[0]
    print(f">>> DB TRACE: Total study duration = {total_dur} seconds")
    
    # 3. Check streak
    cursor.execute("SELECT current_streak FROM streaks LIMIT 1")
    streak = cursor.fetchone()[0]
    print(f">>> DB TRACE: Current streak = {streak}")
    
    conn.close()

if __name__ == '__main__':
    verify_storage()
