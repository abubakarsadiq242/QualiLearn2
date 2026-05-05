import os
from datetime import datetime, date, timedelta
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.learning import LearningMaterial, VocationalContent
from app.models.flashcard import Flashcard
from app.models.user import User
from app import db
from app.utils.auth import admin_required

learning_bp = Blueprint('learning', __name__)

UPLOAD_FOLDER = os.path.join('public', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'txt', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@learning_bp.route('/upload', methods=['POST'])
@admin_required()
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to filename to avoid collisions
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
            
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # Return the public URL
        return jsonify({
            "success": True,
            "message": "File uploaded successfully",
            "url": f"/uploads/{filename}"
        }), 201
    
    return jsonify({"success": False, "message": "File type not allowed"}), 400

@learning_bp.route('/materials', methods=['GET'])
@jwt_required(optional=True)
def get_materials():
    subject = request.args.get('subject')
    lang = request.args.get('lang', 'en')
    search = request.args.get('search')
    level = request.args.get('level')
    
    # Auto-infer level from user profile if not provided
    user_id = get_jwt_identity()
    if not level and user_id:
        user = db.session.get(User, int(user_id))
        if user and user.education_level:
            u_level = user.education_level.upper()
            if 'VOCATIONAL' in u_level: level = 'Vocational'
            else: level = 'Academics'

    query = LearningMaterial.query.filter_by(language=lang)
    if subject:
        query = query.filter_by(subject=subject)
    if level:
        query = query.filter_by(education_level=level)
        
    if search:
        query = query.filter(
            (LearningMaterial.title.ilike(f'%{search}%')) | 
            (LearningMaterial.content.ilike(f'%{search}%'))
        )
        
    materials = query.all()
    
    return jsonify({
        "success": True,
        "message": "Materials fetched successfully",
        "data": [m.to_dict() for m in materials]
    }), 200

@learning_bp.route('/vocational', methods=['GET'])
def get_vocational():
    lang = request.args.get('lang', 'en')
    category = request.args.get('category')
    search = request.args.get('search')
    
    query = VocationalContent.query.filter_by(language=lang)
    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(
            (VocationalContent.title.ilike(f'%{search}%')) | 
            (VocationalContent.description.ilike(f'%{search}%'))
        )
        
    content = query.all()
    
    return jsonify({
        "success": True,
        "message": "Vocational content fetched successfully",
        "data": [c.to_dict() for c in content]
    }), 200


@learning_bp.route('/material/<int:material_id>', methods=['GET'])
def get_material(material_id):
    material = LearningMaterial.query.get(material_id)
    if not material:
        return jsonify({"success": False, "message": "Material not found"}), 404
    
    return jsonify({
        "success": True,
        "message": "Material fetched successfully",
        "data": material.to_dict()
    }), 200

@learning_bp.route('/progress', methods=['POST'])
@jwt_required()
def track_learning_progress():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    topic_id = data.get('topic_id')
    portal_type = data.get('portal_type', 'secondary')
    study_minutes = data.get('minutes', 5) # Default 5 mins per progress point
    
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    
    # Update Resume Topic
    if topic_id:
        user.resume_topic_id = topic_id
    
    from app.models.analytics import ActivityLog, CompletedItem, Progress, Streak
    
    # 1. Log Activity
    log = ActivityLog(
        user_id=user_id,
        portal_type=portal_type,
        activity_type='subject_learning',
        module='learning',
        duration=study_minutes * 60,
        start_time=datetime.utcnow().isoformat(),
        topic_id=topic_id
    )
    db.session.add(log)
    
    # 2. Record Completion in CompletedItem
    if topic_id:
        exists = CompletedItem.query.filter_by(user_id=user_id, portal_type=portal_type, item_id=topic_id, item_type='material').first()
        if not exists:
            db.session.add(CompletedItem(user_id=user_id, portal_type=portal_type, item_id=topic_id, item_type='material'))
            
    # 3. Update Streak per Portal
    today = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    
    streak_obj = Streak.query.filter_by(user_id=user_id, portal_type=portal_type).first()
    if not streak_obj:
        db.session.add(Streak(user_id=user_id, portal_type=portal_type, current_streak=1, last_active_date=today))
    else:
        if streak_obj.last_active_date == yesterday:
            streak_obj.current_streak += 1
            streak_obj.longest_streak = max(streak_obj.longest_streak, streak_obj.current_streak)
        elif streak_obj.last_active_date != today:
            streak_obj.current_streak = 1
        streak_obj.last_active_date = today

    db.session.commit()

    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Progress tracked successfully",
        "data": user.to_dict()
    }), 200

# Admin CRUD for Learning Materials
@learning_bp.route('/materials/create', methods=['POST'])
@admin_required()
def create_material():
    data = request.get_json()
    material = LearningMaterial(
        title=data.get('title'),
        content=data.get('content'),
        subject=data.get('subject'),
        language=data.get('language', 'en'),
        material_type=data.get('material_type'),
        resource_url=data.get('resource_url'),
        topic_id=data.get('topic_id')
    )
    db.session.add(material)
    db.session.commit()
    return jsonify({"success": True, "message": "Material created", "data": material.to_dict()}), 201

@learning_bp.route('/materials/<int:material_id>', methods=['PUT'])
@admin_required()
def update_material(material_id):
    material = LearningMaterial.query.get(material_id)
    if not material: return jsonify({"success": False, "message": "Not found"}), 404
    
    data = request.get_json()
    for key in ['title', 'content', 'subject', 'language', 'material_type', 'resource_url', 'topic_id']:
        if key in data: setattr(material, key, data[key])
    
    db.session.commit()
    return jsonify({"success": True, "message": "Material updated", "data": material.to_dict()})

@learning_bp.route('/materials/<int:material_id>', methods=['DELETE'])
@admin_required()
def delete_material(material_id):
    material = LearningMaterial.query.get(material_id)
    if not material: return jsonify({"success": False, "message": "Not found"}), 404
    db.session.delete(material)
    db.session.commit()
    return jsonify({"success": True, "message": "Material deleted"})

# Admin CRUD for Vocational Content
@learning_bp.route('/vocational/create', methods=['POST'])
@admin_required()
def create_vocational():
    data = request.get_json()
    content = VocationalContent(
        title=data.get('title'),
        description=data.get('description'),
        category=data.get('category'),
        language=data.get('language', 'en'),
        resource_url=data.get('resource_url')
    )
    db.session.add(content)
    db.session.commit()
    return jsonify({"success": True, "message": "Vocational content created", "data": content.to_dict()}), 201

@learning_bp.route('/vocational/<int:content_id>', methods=['PUT'])
@admin_required()
def update_vocational(content_id):
    content = VocationalContent.query.get(content_id)
    if not content: return jsonify({"success": False, "message": "Not found"}), 404
    
    data = request.get_json()
    for key in ['title', 'description', 'category', 'language', 'resource_url']:
        if key in data: setattr(content, key, data[key])
    
    db.session.commit()
    return jsonify({"success": True, "message": "Vocational content updated", "data": content.to_dict()})

@learning_bp.route('/vocational/<int:content_id>', methods=['DELETE'])
@admin_required()
def delete_vocational(content_id):
    content = VocationalContent.query.get(content_id)
    if not content: return jsonify({"success": False, "message": "Not found"}), 404
    db.session.delete(content)
    db.session.commit()
    return jsonify({"success": True, "message": "Vocational content deleted"})
