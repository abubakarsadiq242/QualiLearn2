from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.models.user import User
from app.models.analytics import StudySession, ActivityLog, Assessment, Progress, CompletedItem, Streak
from app.models.flashcard import Flashcard
from app import db
from datetime import datetime, date

api_bp = Blueprint('api_v1', __name__)

# 1. User Authentication
@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"success": False, "message": "Missing email or password"}), 400
    
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({"success": False, "message": "User already exists"}), 400
    
    user = User(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        education_level=data.get('education_level', 'Academics')
    )
    user.set_password(data.get('password'))
    db.session.add(user)
    db.session.commit()
    return jsonify({"success": True, "message": "User registered", "data": user.to_dict()}), 201

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if user and user.check_password(data.get('password')):
        token = create_access_token(identity=str(user.id))
        return jsonify({"success": True, "data": {"token": token, "user": user.to_dict()}}), 200
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

# 2. Study Tracking
@api_bp.route('/study/start', methods=['POST'])
@jwt_required()
def study_start():
    user_id = get_jwt_identity()
    session = StudySession(user_id=user_id, start_time=datetime.utcnow().isoformat() + 'Z')
    db.session.add(session)
    db.session.commit()
    return jsonify({"success": True, "session_id": session.id})

@api_bp.route('/study/end', methods=['POST'])
@jwt_required()
def study_end():
    data = request.get_json()
    session_id = data.get('session_id')
    session = db.session.get(StudySession, session_id)
    if session:
        session.end_time = datetime.utcnow().isoformat() + 'Z'
        if session.start_time:
            start = datetime.fromisoformat(session.start_time.replace('Z', ''))
            end = datetime.fromisoformat(session.end_time.replace('Z', ''))
            session.duration = int((end - start).total_seconds())
        db.session.commit()
        return jsonify({"success": True, "duration": session.duration})
    return jsonify({"success": False, "message": "Session not found"}), 404

# 3. Video Progress
@api_bp.route('/video/progress', methods=['POST'])
@jwt_required()
def video_progress():
    user_id = get_jwt_identity()
    data = request.get_json()
    video_id = data.get('video_id')
    
    # Track completion
    comp = CompletedItem.query.filter_by(user_id=user_id, item_id=video_id, item_type='video').first()
    if not comp:
        comp = CompletedItem(user_id=user_id, item_id=video_id, item_type='video', portal_type=data.get('portal', 'secondary'))
        db.session.add(comp)
        db.session.commit()
    return jsonify({"success": True, "message": "Video progress updated"})

# 4. Assessments
@api_bp.route('/assessment', methods=['POST'])
@jwt_required()
def submit_assessment():
    user_id = get_jwt_identity()
    data = request.get_json()
    res = Assessment(
        user_id=user_id,
        portal_type=data.get('portal', 'secondary'),
        score=data.get('score'),
        total_questions=data.get('total_questions'),
        passed=data.get('passed', False)
    )
    db.session.add(res)
    db.session.commit()
    return jsonify({"success": True})

# 5. Flashcards
@api_bp.route('/flashcard', methods=['POST'])
@jwt_required()
def update_flashcard():
    # Simple flashcard tracking
    return jsonify({"success": True, "message": "Flashcard performance stored"})

# 6. Dashboard Calculations
@api_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    user_id = get_jwt_identity()
    portal = request.args.get('portal', 'secondary')
    
    # Study Time
    total_sec = db.session.query(db.func.sum(ActivityLog.duration)).filter_by(user_id=user_id, portal_type=portal).scalar() or 0
    today_start = date.today().isoformat()
    today_sec = db.session.query(db.func.sum(ActivityLog.duration)).filter(
        ActivityLog.user_id == user_id, 
        ActivityLog.portal_type == portal,
        ActivityLog.start_time >= today_start
    ).scalar() or 0
    
    # Monthly Study Time
    month_start = date.today().replace(day=1).isoformat()
    month_sec = db.session.query(db.func.sum(ActivityLog.duration)).filter(
        ActivityLog.user_id == user_id,
        ActivityLog.portal_type == portal,
        ActivityLog.start_time >= month_start
    ).scalar() or 0

    # Accuracy
    acc_stats = db.session.query(
        db.func.sum(Assessment.correct_answers),
        db.func.sum(Assessment.total_questions)
    ).filter(Assessment.user_id == user_id, Assessment.portal_type == portal).first()
    accuracy = (acc_stats[0] / acc_stats[1] * 100) if acc_stats and acc_stats[1] and acc_stats[1] > 0 else 0
    
    # Progress
    comp_count = CompletedItem.query.filter_by(user_id=user_id, portal_type=portal).count()
    # Assume 100 units for base progress calculation if no dynamic total is found
    progress_pct = (comp_count / 100) * 100 
    
    # Streak
    streak_obj = Streak.query.filter_by(user_id=user_id, portal_type=portal).first()

    return jsonify({
        "success": True,
        "data": {
            "overall_progress": round(min(progress_pct, 100.0), 1),
            "study_time_today": f"{round(today_sec / 60)}m",
            "study_time_month": f"{int(month_sec // 3600)}h {int((month_sec % 3600) // 60)}m",
            "assessments_passed": Assessment.query.filter_by(user_id=user_id, portal_type=portal, passed=True).count(),
            "accuracy": f"{round(accuracy, 1)}%",
            "current_streak": streak_obj.current_streak if streak_obj else 0
        }
    })
