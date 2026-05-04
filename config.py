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
    db_filename = 'qualilearn_v2.db'
    source_db = os.path.join(instance_path, db_filename)
    
    # Check if we are in a read-only environment (like Vercel)
    # Vercel typically uses /var/task as the root
    if os.environ.get('VERCEL') or not os.access(basedir, os.W_OK):
        import shutil
        db_path = f'/tmp/{db_filename}'
        # Copy the pre-filled database to the writable /tmp folder if it exists in the codebase
        # but don't overwrite if it's already there (to persist across hot-reloads in the same container)
        if not os.path.exists(db_path) and os.path.exists(source_db):
            try:
                shutil.copy2(source_db, db_path)
                print(f" * Copied DB to {db_path} for writable access.")
            except Exception as e:
                print(f" * Failed to copy DB: {e}")
        elif not os.path.exists(db_path):
            # If source doesn't exist, we'll let SQLAlchemy create it empty in /tmp
            pass
    else:
        # Local development environment
        os.makedirs(instance_path, exist_ok=True)
        db_path = source_db
    
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
