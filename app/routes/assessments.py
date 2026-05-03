from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.assessment import PastQuestion, AssessmentTemplate, Result
from app import db
from app.utils.auth import admin_required

assessments_bp = Blueprint('assessments', __name__)

@assessments_bp.route('/questions', methods=['GET'])
def get_questions():
    subject = request.args.get('subject')
    year = request.args.get('year')
    topic = request.args.get('topic')
    lang = request.args.get('lang', 'en')
    
    query = PastQuestion.query.filter_by(language=lang)
    if subject:
        query = query.filter_by(subject=subject)
    if year:
        query = query.filter_by(year=year)
    if topic:
        query = query.filter_by(topic=topic)
        
    questions = query.all()
    
    return jsonify({
        "success": True,
        "message": "Questions fetched successfully",
        "data": [q.to_dict() for q in questions]
    }), 200

@assessments_bp.route('/start', methods=['POST'])
@jwt_required()
def start_assessment():
    data = request.get_json()
    assessment_id = data.get('assessment_id')
    
    assessment = AssessmentTemplate.query.get(assessment_id)
    if not assessment:
        return jsonify({"success": False, "message": "AssessmentTemplate not found"}), 404
        
    return jsonify({
        "success": True,
        "message": "AssessmentTemplate started",
        "data": {
            "id": assessment.id,
            "title": assessment.title,
            "questions": [{"id": q.id, "text": q.text, "options": {"A": q.option_a, "B": q.option_b, "C": q.option_c, "D": q.option_d}} for q in assessment.questions]
        }
    }), 200

@assessments_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_assessment():
    from app.models.user import User
    from app.models.analytics import Assessment, Streak, CompletedItem, Progress
    
    user_id = int(get_jwt_identity())
    data = request.get_json()
    assessment_id = data.get('assessment_id')
    answers = data.get('answers')  # Expected formatted as {question_id: "A/B/C/D"}
    portal_type = data.get('portal_type', 'secondary')
    
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
        
    assessment = AssessmentTemplate.query.get(assessment_id)
    if not assessment:
        # Practice mode (Past Question or Quiz)
        correct_count = 0
        total_questions = len(answers) if answers else 0
        if answers:
            for q_id, u_ans in answers.items():
                try:
                    q = db.session.get(PastQuestion, int(q_id))
                    if q and u_ans == q.correct_answer:
                        correct_count += 1
                except:
                    continue
    else:
        # Full Exam Mode
        correct_count = 0
        total_questions = len(assessment.questions)
        if total_questions > 0 and answers:
            for q in assessment.questions:
                user_ans = answers.get(str(q.id)) or answers.get(int(q.id))
                if user_ans == q.correct_option:
                    correct_count += 1
                
    score = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    is_passed = score >= 50
    
    from datetime import date, timedelta
    today = date.today()
    today_str = today.isoformat()
    yesterday_str = (today - timedelta(days=1)).isoformat()

    # 1. Update Analytics History (Passed Counter)
    hist = Assessment(
        user_id=user_id,
        portal_type=portal_type,
        total_questions=total_questions,
        correct_answers=correct_count,
        passed=is_passed
    )
    db.session.add(hist)
    
    # 2. Update Streak per Portal
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

    # 3. Mark Completion if passed
    if is_passed and assessment_id:
        exists = CompletedItem.query.filter_by(user_id=user_id, portal_type=portal_type, item_id=assessment_id, item_type='assessment').first()
        if not exists:
            db.session.add(CompletedItem(user_id=user_id, portal_type=portal_type, item_id=assessment_id, item_type='assessment'))
            prog = Progress.query.filter_by(user_id=user_id, portal_type=portal_type).first()
            if prog:
                prog.completed_units = CompletedItem.query.filter_by(user_id=user_id, portal_type=portal_type).count()

    # Save practice result
    res_obj = Result(user_id=user_id, assessment_id=assessment_id, score=score, total_questions=total_questions)
    db.session.add(res_obj)
    
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Assessment graded successfully",
        "data": {
            "score": score,
            "correct_count": correct_count,
            "total_questions": total_questions,
            "passed": is_passed
        }
    }), 200

@assessments_bp.route('/check', methods=['POST'])
@jwt_required()
def check_answer():
    data = request.get_json()
    question_id = data.get('question_id')
    user_answer = data.get('answer')
    
    from app.models.assessment import Question
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"success": False, "message": "Question not found"}), 404
        
    is_correct = (user_answer == question.correct_option)
    
    return jsonify({
        "success": True,
        "is_correct": is_correct,
        "correct_option": question.correct_option,
        "explanation": question.explanation or "No explanation available."
    }), 200

# Admin CRUD for Past Questions
@assessments_bp.route('/questions/create', methods=['POST'])
@admin_required()
def create_question():
    data = request.get_json()
    q = PastQuestion(
        subject=data.get('subject'),
        year=data.get('year'),
        topic=data.get('topic'),
        question_text=data.get('question_text'),
        option_a=data.get('option_a'),
        option_b=data.get('option_b'),
        option_c=data.get('option_c'),
        option_d=data.get('option_d'),
        correct_answer=data.get('correct_answer'),
        explanation=data.get('explanation'),
        language=data.get('language', 'en')
    )
    db.session.add(q)
    db.session.commit()
    return jsonify({"success": True, "message": "Question created", "data": q.to_dict()}), 201

@assessments_bp.route('/questions/<int:q_id>', methods=['PUT'])
@admin_required()
def update_question(q_id):
    q = PastQuestion.query.get(q_id)
    if not q: return jsonify({"success": False, "message": "Not found"}), 404
    
    data = request.get_json()
    for key in ['subject', 'year', 'topic', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'explanation', 'language']:
        if key in data: setattr(q, key, data[key])
    
    db.session.commit()
    return jsonify({"success": True, "message": "Question updated", "data": q.to_dict()})

@assessments_bp.route('/questions/<int:q_id>', methods=['DELETE'])
@admin_required()
def delete_question(q_id):
    q = PastQuestion.query.get(q_id)
    if not q: return jsonify({"success": False, "message": "Not found"}), 404
    db.session.delete(q)
    db.session.commit()
    return jsonify({"success": True, "message": "Question deleted"})
