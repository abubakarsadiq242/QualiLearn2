# QualiLearn Backend

A Flask-based RESTful API backend for the QualiLearn educational platform.

## Tech Stack
- **Python (Flask)**
- **SQLAlchemy** (ORM)
- **JWT Extended** (Authentication)
- **Bcrypt** (Password Hashing)
- **CORS** (Frontend Integration)
- **SQLite** (Default Database)

## Project Structure
```
app/
├── __init__.py      # App factory & extension initialization
├── models/          # Database models (User, Learning, Assessment, etc.)
├── routes/          # API Blueprints
├── services/        # Business logic (if needed)
├── utils/           # Helper functions
├── config.py        # Project configuration
seed.py              # Test data initialization
run.py               # Main entry point
requirements.txt     # Python dependencies
.env                 # Environment variables
```

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   Open `.env` and set your `SECRET_KEY` and `JWT_SECRET_KEY`.

3. **Initialize Database & Seed Data**
   ```bash
   python seed.py
   ```

4. **Run the Application**
   ```bash
   python run.py
   ```
   The API will be available at `http://localhost:5000/api/`

## API Documentation

### Authentication
- `POST /api/auth/register`: Register a new user.
- `POST /api/auth/login`: Login and receive JWT token.

### Users
- `GET /api/users/profile`: Get current user profile (JWT Required).
- `PUT /api/users/profile/update`: Update profile data (JWT Required).

### Learning Materials
- `GET /api/learning/materials`: Fetch materials. Supports `?subject=` and `?lang=` filters.
- `GET /api/learning/vocational`: Fetch vocational content. Supports `?category=` and `?lang=` filters.

### Assessments
- `GET /api/assessments/questions`: Fetch past questions. Supports `?subject=`, `?year=`, `?topic=`, `?lang=` filters.
- `POST /api/assessments/start`: Start an assessment.
- `POST /api/assessments/submit`: Submit answers and get automated grading.

### Dashboard
- `GET /api/dashboard/`: Get user statistics and recent activities.

### Flashcards
- `GET /api/flashcards/`: Fetch flashcards by subject/language.
- `POST /api/flashcards/`: Create a new flashcard (JWT Required).

### Chat
- `POST /api/chat/send`: Send message to AI tutor.
- `GET /api/chat/history`: Get chat history.

## Frontend Integration
The frontend connects via the `Front-End/api-config.js` file. Ensure `BASE_URL` matches your backend address.
All responses are in JSON format:
```json
{
  "success": true,
  "message": "Message here",
  "data": { ... }
}
```
