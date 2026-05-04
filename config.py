import os
from datetime import timedelta
from dotenv import load_dotenv

# Ensure .env is loaded from the project root
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'), override=True)
print(f" * JWT_SECRET_KEY loaded: {'Yes' if os.environ.get('JWT_SECRET_KEY') else 'No'}")

class Config:
    # Force both to be identical to ensure signature consistency across all routes
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'qualilearn-secure-shared-key-2026'
    _db_url = os.environ.get('DATABASE_URL')
    if _db_url and _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)
        
    instance_path = os.path.join(basedir, 'instance')
    try:
        os.makedirs(instance_path, exist_ok=True)
        db_path = os.path.join(instance_path, 'qualilearn_v2.db')
    except OSError:
        # Fallback to /tmp for serverless read-only environments (e.g. Vercel)
        db_path = '/tmp/qualilearn_v2.db'
    
    SQLALCHEMY_DATABASE_URI = _db_url or 'sqlite:///' + db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = SECRET_KEY 
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    CORS_HEADERS = 'Content-Type'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
