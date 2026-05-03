from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"success": False, "message": "Missing email or password"}), 400
    
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({"success": False, "message": "User already exists"}), 400
    
    try:
        user = User(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            education_level=data.get('education_level'),
            language=data.get('language', 'en')
        )
        user.set_password(data.get('password'))
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "User registered successfully",
            "data": user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": f"Error saving to database: {str(e)}"
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"success": False, "message": "Missing email or password"}), 400
    
    user = User.query.filter_by(email=data.get('email')).first()
    
    if user and user.check_password(data.get('password')):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            "success": True,
            "message": "Login successful",
            "data": {
                "token": access_token,
                "user": user.to_dict()
            }
        }), 200
    
    return jsonify({"success": False, "message": "Invalid email or password"}), 401
