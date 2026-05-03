from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models.user import User
from app import db

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = db.session.get(User, int(user_id))
            
            if not user or user.role != 'admin':
                return jsonify({
                    "success": False,
                    "message": "Admin privileges required"
                }), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper
