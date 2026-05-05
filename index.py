import os
from dotenv import load_dotenv

# Initialize environment variables at the very beginning
load_dotenv(override=True)

from app import create_app, db

app = create_app(os.getenv('FLASK_ENV') or 'development')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=int(os.getenv('PORT', 5000)))
