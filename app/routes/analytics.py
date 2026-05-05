from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.analytics import ActivityLog, Assessment, Streak, Progress, CompletedItem, StudySession
from app.models.user import User
from app.models.learning import LearningMaterial, VocationalContent
from app.models.topics import Topic
from app import db
from datetime import datetime, date, timedelta
import json

analytics_bp = Blueprint('analytics', __name__)

def process_track_data(user_id, data):
    portal_type = data.get('portal_type', 'secondary')
    
    # 1. Determine Duration
    duration = data.get('duration')
    if duration is None:
        try:
            st_str = data.get('start_time')
            if st_str:
                st = datetime.fromisoformat(st_str.replace('Z', '+00:00'))
                en_str = data.get('end_time') or datetime.utcnow().isoformat()
                en = datetime.fromisoformat(en_str.replace('Z', '+00:00'))
                duration = int((en - st).total_seconds())
            else:
                duration = 60 # Default
        except:
            duration = 60
    else:
        duration = int(duration)

    t_id = data.get('topic_id') or data.get('id')
    try:
        t_id = int(t_id) if t_id else None
    except:
        t_id = None
        
    log = ActivityLog(
        user_id=user_id,
        portal_type=portal_type,
        session_id=data.get('session_id'),
        activity_type=data.get('activity_type'),
        module=data.get('module'),
        start_time=data.get('start_time') or datetime.utcnow().isoformat(),
        end_time=data.get('end_time'),
        duration=duration,
        score=data.get('score', 0),
        topic_id=t_id,
        video_id=data.get('video_id')
    )
    db.session.add(log)
    
    # Update Resume Topic Bookmark
    user = db.session.get(User, user_id)
    if user:
        r_id = data.get('topic_id') or data.get('id')
        if r_id:
            user.resume_topic_id = int(r_id)
    
    # Update Streak per Portal
    today = date.today()
    today_str = today.isoformat()
    yesterday_str = (today - timedelta(days=1)).isoformat()
    
    streak_obj = Streak.query.filter_by(user_id=user_id, portal_type=portal_type).first()
    if not streak_obj:
        streak_obj = Streak(user_id=user_id, portal_type=portal_type, current_streak=1, last_active_date=today_str)
        db.session.add(streak_obj)
    else:
        if streak_obj.last_active_date == yesterday_str:
            streak_obj.current_streak += 1
            streak_obj.longest_streak = max(streak_obj.longest_streak, streak_obj.current_streak)
        elif streak_obj.last_active_date != today_str:
            streak_obj.current_streak = 1
        streak_obj.last_active_date = today_str

    # Progress Logic per Portal
    completed = data.get('completed', False)
    if completed:
        # Determine unique item identity
        video_id = data.get('video_id')
        topic_id = data.get('topic_id')
        material_id = data.get('id')
        
        item_id = 0
        item_type = 'unknown'
        
        if video_id:
            item_id = int(video_id)
            item_type = 'video'
        elif topic_id and data.get('module') == 'assessment':
            item_id = int(topic_id)
            item_type = 'assessment'
        elif data.get('module') == 'games':
            # Use hash of module/type for game ID
            game_map = {'ttt': 1, 'memory': 2, 'math': 3}
            item_id = game_map.get(data.get('game_type', 'math'), 3)
            item_type = 'game'
        elif data.get('module') == 'vocational':
            item_id = int(material_id) if material_id else 0
            item_type = 'material' # Count as learning material for progress calculation
        elif material_id:
            item_id = int(material_id)
            item_type = 'material'
        elif topic_id:
            item_id = int(topic_id)
            item_type = 'topic'
            
        exists = CompletedItem.query.filter_by(user_id=user_id, portal_type=portal_type, item_id=item_id, item_type=item_type).first()
        if not exists:
            db.session.add(CompletedItem(user_id=user_id, portal_type=portal_type, item_id=item_id, item_type=item_type))
            
            # Update Progress Count for this portal
            prog = Progress.query.filter_by(user_id=user_id, portal_type=portal_type).first()
            if not prog:
                prog = Progress(user_id=user_id, portal_type=portal_type, completed_units=1, total_units=100)
                db.session.add(prog)
            else:
                prog.completed_units = CompletedItem.query.filter_by(user_id=user_id, portal_type=portal_type).count()
                prog.last_updated = datetime.utcnow()

@analytics_bp.route('/track-activity', methods=['POST'])
@jwt_required()
def track_activity():
    data = request.json
    user_id = int(get_jwt_identity())
    if not data: return jsonify({"success": False}), 400
    process_track_data(user_id, data)
    db.session.commit()
    return jsonify({"success": True})

@analytics_bp.route('/batch-track', methods=['POST'])
@jwt_required()
def batch_track():
    data = request.json
    user_id = int(get_jwt_identity())
    events = data.get('events', [])
    for event in events:
        process_track_data(user_id, event)
    db.session.commit()
    return jsonify({"success": True, "count": len(events)})

@analytics_bp.route('/start-session', methods=['POST'])
@jwt_required()
def start_session():
    data = request.json or {}
    portal_type = data.get('portal_type', 'secondary')
    user_id = int(get_jwt_identity())
    
    # Close previous active sessions for this user in this portal
    StudySession.query.filter_by(user_id=user_id, portal_type=portal_type, is_active=True).update({"is_active": False, "end_time": datetime.utcnow()})
    
    new_session = StudySession(user_id=user_id, portal_type=portal_type)
    db.session.add(new_session)
    db.session.commit()
    return jsonify({"success": True, "session_id": new_session.id})

@analytics_bp.route('/end-session', methods=['POST'])
@jwt_required()
def end_session():
    data = request.json or {}
    session_id = data.get('session_id')
    if session_id:
        sess = db.session.get(StudySession, session_id)
        if sess:
            sess.is_active = False
            sess.end_time = datetime.utcnow()
            db.session.commit()
    return jsonify({"success": True})

@analytics_bp.route('/dashboard-stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    try:
        user_id = int(get_jwt_identity())
        portal = request.args.get('portal', 'secondary')
        
        from datetime import date, datetime
        now = datetime.utcnow()
        # 1. Study Time This Month Filtered by Portal
        from sqlalchemy import and_
        
        # Use ISO strings for robust filtering against String-based SQLite columns
        month_iso = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat()
        today_iso = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()

        total_sec = db.session.query(db.func.sum(ActivityLog.duration)).filter(
            ActivityLog.user_id == user_id,
            ActivityLog.portal_type == portal,
            db.func.coalesce(ActivityLog.start_time, ActivityLog.created_at) >= month_iso
        ).scalar() or 0
        
        # 2. Today Study Time Filtered by Portal
        today_sec = db.session.query(db.func.sum(ActivityLog.duration)).filter(
            ActivityLog.user_id == user_id,
            ActivityLog.portal_type == portal,
            db.func.coalesce(ActivityLog.start_time, ActivityLog.created_at) >= today_iso
        ).scalar() or 0
        
        # 3. Accuracy Calculation (SQL Aggregation for scalability)
        acc_stats = db.session.query(
            db.func.sum(Assessment.correct_answers),
            db.func.sum(Assessment.total_questions)
        ).filter(Assessment.user_id == user_id, Assessment.portal_type == portal).first()
        
        if acc_stats and acc_stats[1] and acc_stats[1] > 0:
            accuracy = (acc_stats[0] / acc_stats[1]) * 100
        else:
            accuracy = 0
        
        # 4. Refined Progress Logic (Multi-Category Weighted Progress)
        from app.models.learning import LearningMaterial, VocationalContent
        from app.models.flashcard import Flashcard
        from app.models.assessment import AssessmentTemplate
        
        # Define Category Totals
        if portal == 'vocational':
            total_learning = VocationalContent.query.count() or 0
            total_flashcards = Flashcard.query.filter_by(education_level='Vocational').count() or 0
            total_exams = 0
            total_games = 0 # Vocational might not have games yet
        else:
            total_learning = LearningMaterial.query.count() or 0
            total_flashcards = Flashcard.query.count() or 0
            total_exams = AssessmentTemplate.query.count() or 0
            total_games = 3 # Tic-Tac-Toe, Memory Match, Math Challenge
        
        # Get Completion Counts per Category
        comp_learning = CompletedItem.query.filter_by(user_id=user_id, portal_type=portal, item_type='material').count()
        comp_flashcards = CompletedItem.query.filter_by(user_id=user_id, portal_type=portal, item_type='flashcard').count()
        comp_exams = CompletedItem.query.filter_by(user_id=user_id, portal_type=portal, item_type='assessment').count()
        comp_games = CompletedItem.query.filter_by(user_id=user_id, portal_type=portal, item_type='game').count()
        
        # Calculate Category Percentages (avoid division by zero)
        pct_learning = (comp_learning / total_learning * 100) if total_learning > 0 else 100
        pct_flashcards = (comp_flashcards / total_flashcards * 100) if total_flashcards > 0 else 100
        pct_exams = (comp_exams / total_exams * 100) if total_exams > 0 else 100
        pct_games = (comp_games / total_games * 100) if total_games > 0 else 100
        
        # Overall Progress = Weighted Average (25% each if applicable)
        active_categories = []
        if total_learning > 0: active_categories.append(pct_learning)
        if total_flashcards > 0: active_categories.append(pct_flashcards)
        if total_exams > 0: active_categories.append(pct_exams)
        if total_games > 0: active_categories.append(pct_games)
        
        if active_categories:
            progress_pct = sum(active_categories) / len(active_categories)
        else:
            progress_pct = 0
            
        # Sync with Progress table for persistence
        prog = Progress.query.filter_by(user_id=user_id, portal_type=portal).first()
        if not prog:
            prog = Progress(user_id=user_id, portal_type=portal, completed_units=int(progress_pct), total_units=100)
            db.session.add(prog)
        else:
            prog.completed_units = int(progress_pct)
            prog.total_units = 100
            prog.last_updated = datetime.utcnow()
        
        # Update User Model for global reference
        user = db.session.get(User, user_id)
        if user and portal == 'secondary':
            user.overall_progress = progress_pct
        
        db.session.commit()
        
        # 5. Resume Topic (Portal-Aware resolution)
        last_act = ActivityLog.query.filter(
            ActivityLog.user_id == user_id,
            ActivityLog.portal_type == portal,
            ActivityLog.topic_id != None
        ).order_by(ActivityLog.created_at.desc()).first()
        
        resume_topic = None
        if last_act:
            if portal == 'vocational':
                mat = db.session.get(VocationalContent, last_act.topic_id)
            else:
                mat = db.session.get(LearningMaterial, last_act.topic_id)
                
            if mat:
                resume_topic = mat.to_dict()
                resume_topic['type'] = 'vocational' if portal == 'vocational' else 'material'

        streak_obj = Streak.query.filter_by(user_id=user_id, portal_type=portal).first()
        
        # Formatting Time
        def format_time(seconds):
            h = int(seconds // 3600)
            m = int((seconds % 3600) // 60)
            if h > 0:
                return f"{h}h {m}m"
            return f"{m}m"

        stats = {
            "overall_progress": round(min(progress_pct, 100.0), 1),
            "study_time": format_time(total_sec),
            "daily_time": format_time(today_sec),
            "assessments_passed": Assessment.query.filter_by(user_id=user_id, portal_type=portal, passed=True).count(),
            "accuracy": f"{round(accuracy, 1)}%",
            "current_streak": streak_obj.current_streak if streak_obj else 0,
            "longest_streak": streak_obj.longest_streak if streak_obj else 0,
            "resume_topic": resume_topic,
            "portal": portal
        }
        
        return jsonify({"success": True, "data": stats})
    except Exception as e:
        print(">>> TRACE ERROR: STATS FAILED:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500

@analytics_bp.route('/subject-progress', methods=['GET'])
@jwt_required()
def get_subject_progress():
    try:
        user_id = int(get_jwt_identity())
        subject = request.args.get('subject')
        portal = request.args.get('portal', 'secondary')
        
        if not subject:
            return jsonify({"success": False, "message": "Subject is required"}), 400
            
        # Define subject groups (e.g. Science Hub includes Physics, Chemistry, Biology)
        subjects = [subject]
        if subject.lower() == 'science':
            subjects = ['Science', 'General Science', 'Physics', 'Chemistry', 'Biology']

        from app.models.learning import LearningMaterial
        from app.models.topics import Topic, TopicVideo
        from app.models.assessment import AssessmentTemplate

        # 1. Total Units for this subject (Filtered by language if provided)
        lang = request.args.get('lang')
        mats_query = LearningMaterial.query.filter(LearningMaterial.subject.in_(subjects))
        if lang:
            mats_query = mats_query.filter_by(language=lang)
        mats_count = mats_query.count()
        
        # Videos count (Topic -> TopicVideo join)
        vids_count = TopicVideo.query.join(Topic).filter(Topic.subject.in_(subjects)).count()
        
        # Assessments count
        exams_count = AssessmentTemplate.query.filter(AssessmentTemplate.subject.in_(subjects)).count()
        
        total_units = max(1, mats_count + vids_count + exams_count)

        # 2. Completed Units for this subject
        from app.models.analytics import CompletedItem
        
        # Completed Materials
        comp_mats = CompletedItem.query.join(LearningMaterial, 
            (CompletedItem.item_id == LearningMaterial.id) & 
            (CompletedItem.item_type == 'material')
        ).filter(
            CompletedItem.user_id == user_id,
            CompletedItem.portal_type == portal,
            LearningMaterial.subject.in_(subjects)
        ).count()

        # Completed Assessments
        comp_exams = CompletedItem.query.join(AssessmentTemplate,
            (CompletedItem.item_id == AssessmentTemplate.id) &
            (CompletedItem.item_type == 'assessment')
        ).filter(
            CompletedItem.user_id == user_id,
            CompletedItem.portal_type == portal,
            AssessmentTemplate.subject.in_(subjects)
        ).count()

        # Completed Videos (Join CompletedItem -> TopicVideo -> Topic)
        comp_vids = CompletedItem.query.join(TopicVideo,
            (CompletedItem.item_id == TopicVideo.id) &
            (CompletedItem.item_type == 'video')
        ).join(Topic).filter(
            CompletedItem.user_id == user_id,
            CompletedItem.portal_type == portal,
            Topic.subject.in_(subjects)
        ).count()
        
        completed_units = comp_mats + comp_exams + comp_vids
        progress_pct = round(min((completed_units / total_units) * 100, 100.0), 1)

        return jsonify({
            "success": True,
            "data": {
                "subject": subject,
                "progress": progress_pct,
                "completed": completed_units,
                "total": total_units
            }
        })
    except Exception as e:
        print(f">>> SUBJECT PROGRESS ERROR ({subject}):", str(e))
        return jsonify({"success": False, "error": str(e)}), 500

@analytics_bp.route('/leaderboard', methods=['GET'])
@jwt_required()
def get_leaderboard():
    try:
        from datetime import datetime, timedelta
        seven_days_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()
        
        # 1. Study time and Game scores from ActivityLog
        logs = db.session.query(
            ActivityLog.user_id,
            db.func.sum(ActivityLog.duration).label('total_duration'),
            db.func.sum(ActivityLog.score).label('total_game_score')
        ).filter(ActivityLog.created_at >= seven_days_ago).group_by(ActivityLog.user_id).all()
        
        # 2. Assessment scores
        assessments = db.session.query(
            Assessment.user_id,
            db.func.sum(Assessment.correct_answers).label('total_correct')
        ).filter(Assessment.created_at >= seven_days_ago).group_by(Assessment.user_id).all()
        
        # Combine data
        user_stats = {}
        for l in logs:
            user_stats[l.user_id] = {
                'points': ( (l.total_duration or 0) / 60 * 10 ) + (l.total_game_score or 0),
                'duration': l.total_duration or 0
            }
            
        for a in assessments:
            if a.user_id not in user_stats:
                user_stats[a.user_id] = {'points': 0, 'duration': 0}
            user_stats[a.user_id]['points'] += (a.total_correct or 0) * 50
            
        # Get user names and sort
        leaderboard = []
        for u_id, stats in user_stats.items():
            user = db.session.get(User, u_id)
            if user and user.role != 'admin':
                # Get portal-specific progress
                prog_obj = Progress.query.filter_by(user_id=u_id, portal_type=portal).first()
                display_progress = 0
                if prog_obj:
                    display_progress = (prog_obj.completed_units / max(prog_obj.total_units, 1)) * 100
                else:
                    # Fallback to model field for secondary if no specific row exists
                    display_progress = user.overall_progress if portal == 'secondary' else 0

                leaderboard.append({
                    'id': u_id,
                    'name': f"{user.first_name} {user.last_name}",
                    'initial': user.first_name[0] if user.first_name else 'U',
                    'points': int(stats['points']),
                    'duration': stats['duration'],
                    'progress': round(display_progress, 1)
                })
                
        leaderboard.sort(key=lambda x: x['progress'], reverse=True)
        
        return jsonify({
            "success": True,
            "data": leaderboard[:10]
        })
    except Exception as e:
        print(">>> LEADERBOARD ERROR:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500
