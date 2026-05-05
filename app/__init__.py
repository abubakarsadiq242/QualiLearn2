from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config_by_name

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name):
    # Set static folder to the public directory
    app = Flask(__name__, static_folder='../public', static_url_path='')
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)  # Allow all origins for development
    
    # Ensure tables are created (Safe for SQLite, won't overwrite existing data)
    with app.app_context():
        db.create_all()

    # Error handling
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        # Pass through HTTP errors
        from werkzeug.exceptions import HTTPException
        if isinstance(e, HTTPException):
            return e
        
        # Log the error (would be captured by Vercel logs)
        print(f"Unhandled Exception: {str(e)}")
        
        return jsonify({
            "success": False,
            "message": f"Server error: {str(e)}"
        }), 500

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "message": "Unauthorized access - please login again"
        }), 401

    # JWT specific error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "success": False,
            "message": "The token has expired",
            "error": "token_expired"
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "success": False,
            "message": "Signature verification failed",
            "error": "invalid_token"
        }), 422

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "success": False,
            "message": "Request does not contain an access token",
            "error": "authorization_required"
        }), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "success": False,
            "message": "The token has been revoked",
            "error": "token_revoked"
        }), 401

    @app.route('/')
    def index():
        # Show landing page by default
        return app.send_static_file('index.html')

    @app.route('/api/')
    def api_index():
        return jsonify({
            "success": True,
            "message": "Welcome to QualiLearn API",
            "version": "1.0.0"
        })

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    from app.routes.learning import learning_bp
    from app.routes.assessments import assessments_bp
    from app.routes.flashcards import flashcards_bp
    from app.routes.chat import chat_bp
    from app.routes.dashboard import dashboard_bp
    
    from app.routes.analytics import analytics_bp
    from app.routes.topics import topics_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(learning_bp, url_prefix='/api/learning')
    app.register_blueprint(assessments_bp, url_prefix='/api/assessments')
    app.register_blueprint(flashcards_bp, url_prefix='/api/flashcards')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(topics_bp, url_prefix='/api/topics')

    return app
