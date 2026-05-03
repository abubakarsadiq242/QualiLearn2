from app import create_app, db
from app.models.user import User

app = create_app('development')
with app.app_context():
    users = User.query.all()
    for u in users:
        print(f"ID: {u.id}, Name: {u.first_name} {u.last_name}, Email: {u.email}")
