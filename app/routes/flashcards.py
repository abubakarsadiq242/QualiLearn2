from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.flashcard import Flashcard
from app import db
from app.utils.auth import admin_required

flashcards_bp = Blueprint('flashcards', __name__)

@flashcards_bp.route('/', methods=['GET'])
def get_flashcards():
    subject = request.args.get('subject')
    lang = request.args.get('lang', 'en')
    
    query = Flashcard.query.filter_by(language=lang)
    if subject:
        query = query.filter_by(subject=subject)
        
    flashcards = query.all()
    
    return jsonify({
        "success": True,
        "message": "Flashcards fetched successfully",
        "data": [f.to_dict() for f in flashcards]
    }), 200

@flashcards_bp.route('/', methods=['POST'])
@jwt_required()
def create_flashcard():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('front') or not data.get('back'):
        return jsonify({"success": False, "message": "Missing front or back content"}), 400
        
    flashcard = Flashcard(
        user_id=user_id,
        front=data.get('front'),
        back=data.get('back'),
        subject=data.get('subject'),
        language=data.get('language', 'en')
    )
    
    db.session.add(flashcard)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Flashcard created successfully",
        "data": flashcard.to_dict()
    }), 201
@flashcards_bp.route('/<int:card_id>/review', methods=['PATCH'])
@jwt_required()
def review_flashcard(card_id):
    from datetime import datetime, timedelta
    data = request.get_json()
    is_correct = data.get('correct', False)
    
    flashcard = Flashcard.query.get_or_404(card_id)
    
    if is_correct:
        # Simple Spaced Repetition: Push review date further
        flashcard.next_review_date = datetime.utcnow() + timedelta(days=2)
        flashcard.difficulty_score = max(0, flashcard.difficulty_score - 1)
    else:
        # Review again sooner
        flashcard.next_review_date = datetime.utcnow() + timedelta(hours=4)
        flashcard.difficulty_score += 1

    from app.models.user import User
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    if user:
        user.study_time = (user.study_time or 0) + 2 # Add 2 minutes per review session
        user.overall_progress = min(100, (user.overall_progress or 0) + 0.05) # Reduced from 0.5 to 0.05
        
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Review recorded",
        "data": flashcard.to_dict()
    }), 200

# Admin CRUD for Flashcards
@flashcards_bp.route('/<int:card_id>', methods=['PUT'])
@admin_required()
def update_flashcard(card_id):
    card = Flashcard.query.get(card_id)
    if not card: return jsonify({"success": False, "message": "Not found"}), 404
    
    data = request.get_json()
    for key in ['front', 'back', 'subject', 'language']:
        if key in data: setattr(card, key, data[key])
    
    db.session.commit()
    return jsonify({"success": True, "message": "Flashcard updated", "data": card.to_dict()})

@flashcards_bp.route('/<int:card_id>', methods=['DELETE'])
@admin_required()
def delete_flashcard(card_id):
    card = Flashcard.query.get(card_id)
    if not card: return jsonify({"success": False, "message": "Not found"}), 404
    db.session.delete(card)
    db.session.commit()
    return jsonify({"success": True, "message": "Flashcard deleted"})
