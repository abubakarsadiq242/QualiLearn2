from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app import db
from app.utils.auth import admin_required

users_bp = Blueprint('users', __name__)

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    
    return jsonify({
        "success": True,
        "message": "Profile fetched successfully",
        "data": user.to_dict()
    }), 200

@users_bp.route('/profile/update', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
        
    data = request.get_json()
    
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'education_level' in data:
        user.education_level = data['education_level']
    if 'language' in data:
        user.language = data['language']
        
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Profile updated successfully",
        "data": user.to_dict()
    }), 200

@users_bp.route('/', methods=['GET'])
@admin_required()
def get_all_users():
    users = User.query.all()
    return jsonify({
        "success": True,
        "data": [u.to_dict() for u in users]
    })
