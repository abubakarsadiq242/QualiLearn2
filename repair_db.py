import sqlite3
import os

db_path = os.path.join('instance', 'qualilearn_v2.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print(f"Repairing database: {db_path}")

# 1. Ensure topics table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    is_deleted BOOLEAN DEFAULT 0 NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
print("Ensured 'topics' table exists.")

# 2. Ensure topic_videos table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS topic_videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER NOT NULL,
    video_url VARCHAR(500) NOT NULL,
    video_title VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(topic_id) REFERENCES topics(id)
)
""")
print("Ensured 'topic_videos' table exists.")

# 3. Add topic_id to learning_materials if missing
cursor.execute("PRAGMA table_info(learning_materials)")
columns = [col[1] for col in cursor.fetchall()]
if 'topic_id' not in columns:
    cursor.execute("ALTER TABLE learning_materials ADD COLUMN topic_id INTEGER REFERENCES topics(id)")
    print("Added 'topic_id' column to 'learning_materials'.")
else:
    print("'topic_id' already exists in 'learning_materials'.")

# 4. Consolidate subjects (as requested before)
tables = ['topics', 'learning_materials', 'past_questions', 'assessment_templates']
total_updated = 0
for table in tables:
    try:
        cursor.execute(f"UPDATE {table} SET subject = 'Science' WHERE subject IN ('Physics', 'Chemistry');")
        total_updated += cursor.rowcount
    except sqlite3.OperationalError:
        pass

conn.commit()
print(f"Consolidated subjects. Total rows updated: {total_updated}")
conn.close()
print("Database repair complete.")
