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
    
    # Database selection logic
    if os.environ.get('VERCEL'):
        # On Vercel, we MUST use /tmp for SQLite, but warn that it's ephemeral
        import shutil
        db_path = f'/tmp/{db_filename}'
        if not os.path.exists(db_path) and os.path.exists(source_db):
            try:
                shutil.copy2(source_db, db_path)
                print(f" * Vercel detected: Copied DB to {db_path} (Warning: Data will NOT persist across restarts).")
            except Exception as e:
                print(f" * Failed to copy DB to /tmp: {e}")
    else:
        # Local or persistent server
        os.makedirs(instance_path, exist_ok=True)
        db_path = source_db
        print(f" * Using persistent DB at: {db_path}")
    
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
