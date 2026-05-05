from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.assessment import Result
from app.models.user import User
from sqlalchemy import func
from app import db
from datetime import date, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    try:
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)
        
        from app.models.analytics import ActivityLog, Assessment, Streak, Progress
        
        # 1. Total Study Time (Unified with Analytics)
        total_sec = db.session.query(db.func.sum(ActivityLog.duration)).filter_by(user_id=user_id).scalar() or 0
        
        # 2. Today Study Time
        today_start = date.today().isoformat()
        today_sec = db.session.query(db.func.sum(ActivityLog.duration)).filter(
            ActivityLog.user_id == user_id,
            ActivityLog.start_time >= today_start
        ).scalar() or 0
        
        # 3. Accuracy
        total_q = db.session.query(db.func.sum(Assessment.total_questions)).filter_by(user_id=user_id).scalar() or 0
        total_c = db.session.query(db.func.sum(Assessment.correct_answers)).filter_by(user_id=user_id).scalar() or 0
        accuracy = (total_c / total_q * 100) if total_q > 0 else 0
        
        # 4. Progress
        prog = Progress.query.filter_by(user_id=user_id).first()
        progress_pct = (prog.completed_units / (prog.total_units or 100) * 100) if prog else 0
        
        # 5. Streak
        streak_obj = Streak.query.filter_by(user_id=user_id).first()
        
        # 6. Resume Topic
        resume_topic = None
        if user and user.resume_topic_id:
            from app.models.learning import LearningMaterial
            topic = db.session.get(LearningMaterial, int(user.resume_topic_id))
            if topic:
                resume_topic = topic.to_dict()

        # MANDATORY DEBUG LOGS
        print(f"TOTAL STUDY TIME: {total_sec}")
        print(f"PROGRESS: {progress_pct}%")
        print(f"STREAK: {streak_obj.current_streak if streak_obj else 0}")

        # 7. Recent Activities
        recent = ActivityLog.query.filter_by(user_id=user_id).order_by(ActivityLog.created_at.desc()).limit(5).all()
        recent_list = []
        for r in recent:
            recent_list.append({
                "type": r.activity_type,
                "module": r.module,
                "duration": f"{r.duration // 60}m" if r.duration else "0m",
                "score": r.score,
                "date": r.created_at[:10] if r.created_at else ""
            })

        return jsonify({
            "success": True,
            "data": {
                "overall_progress": round(progress_pct, 1),
                "study_time": f"{int(total_sec // 3600)}h {int((total_sec % 3600) // 60)}m",
                "daily_time": f"{round(today_sec / 60)}m",
                "assessments_passed": Assessment.query.filter_by(user_id=user_id, passed=True).count(),
                "accuracy": f"{round(accuracy, 1)}%",
                "current_streak": streak_obj.current_streak if streak_obj else 0,
                "resume_topic": resume_topic,
                "recent_activities": recent_list
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
