import sqlite3
import os

db_path = os.path.join('instance', 'qualilearn_v2.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

tables = ['topics', 'learning_materials', 'past_questions', 'assessment_templates']
total_updated = 0

for table in tables:
    try:
        cursor.execute(f"UPDATE {table} SET subject = 'Science' WHERE subject IN ('Physics', 'Chemistry');")
        total_updated += cursor.rowcount
        print(f"Updated {cursor.rowcount} rows in table '{table}'")
    except sqlite3.OperationalError as e:
        print(f"Skipping table '{table}': {e}")

conn.commit()
print(f"\nTotal rows updated across all tables: {total_updated}")
conn.close()
