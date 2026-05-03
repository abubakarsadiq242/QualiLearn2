from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.topics import Topic, TopicVideo
from app import db
from app.utils.auth import admin_required

topics_bp = Blueprint('topics', __name__)

@topics_bp.route('/create', methods=['POST'])
@admin_required()
def create_topic():
    data = request.get_json()
    name = data.get('name')
    subject = data.get('subject')
    
    if not name or not subject:
        return jsonify({"success": False, "message": "Name and Subject are required"}), 400
        
    topic = Topic(name=name, subject=subject)
    db.session.add(topic)
    db.session.commit()
    
    return jsonify({"success": True, "message": "Topic created", "data": topic.to_dict()}), 201

@topics_bp.route('/', methods=['GET'])
@jwt_required()
def get_topics():
    topics = Topic.query.filter_by(is_deleted=False).all()
    grouped = {}
    for t in topics:
        if t.subject not in grouped:
            grouped[t.subject] = []
        grouped[t.subject].append(t.to_dict())
    return jsonify({"success": True, "data": grouped})

@topics_bp.route('/delete/<int:topic_id>', methods=['POST'])
@admin_required()
def delete_topic(topic_id):
    topic = Topic.query.get(topic_id)
    if not topic:
        return jsonify({"success": False, "message": "Topic not found"}), 404
        
    # Soft delete
    topic.is_deleted = True
    db.session.commit()
    return jsonify({"success": True, "message": "Topic deleted safely"})

@topics_bp.route('/update/<int:topic_id>', methods=['PUT'])
@admin_required()
def update_topic(topic_id):
    topic = Topic.query.get(topic_id)
    if not topic:
        return jsonify({"success": False, "message": "Topic not found"}), 404
    
    data = request.get_json()
    if 'name' in data: topic.name = data['name']
    if 'subject' in data: topic.subject = data['subject']
    
    db.session.commit()
    return jsonify({"success": True, "message": "Topic updated", "data": topic.to_dict()})

@topics_bp.route('/<int:topic_id>/add-video', methods=['POST'])
@admin_required()
def add_video(topic_id):
    topic = Topic.query.get(topic_id)
    if not topic or topic.is_deleted:
        return jsonify({"success": False, "message": "Topic not found"}), 404
        
    data = request.get_json()
    url = data.get('video_url')
    title = data.get('video_title')
    
    if not url:
        return jsonify({"success": False, "message": "Video URL is required"}), 400
        
    # Check for duplicates
    existing = TopicVideo.query.filter_by(topic_id=topic_id, video_url=url).first()
    if existing:
        return jsonify({"success": False, "message": "Video already exists for this topic"}), 400

    video = TopicVideo(topic_id=topic_id, video_url=url, video_title=title)
    if not video.get_video_id():
        return jsonify({"success": False, "message": "Invalid YouTube URL"}), 400
        
    db.session.add(video)
    db.session.commit()
    return jsonify({"success": True, "message": "Video added", "data": video.to_dict()})

@topics_bp.route('/<int:topic_id>/videos', methods=['GET'])
@jwt_required()
def get_topic_videos(topic_id):
    videos = TopicVideo.query.filter_by(topic_id=topic_id).all()
    return jsonify({"success": True, "data": [v.to_dict() for v in videos]})

@topics_bp.route('/videos/delete/<int:video_id>', methods=['POST'])
@admin_required()
def delete_video(video_id):
    video = TopicVideo.query.get(video_id)
    if not video:
        return jsonify({"success": False, "message": "Video not found"}), 404
        
    db.session.delete(video)
    db.session.commit()
    return jsonify({"success": True, "message": "Video removed"})
