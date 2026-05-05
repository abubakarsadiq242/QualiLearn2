import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'), override=True)

print(f"GEMINI_API_KEY: {'[SET]' if os.getenv('GEMINI_API_KEY') else '[MISSING]'}")
print(f"SECRET_KEY: {'[SET]' if os.getenv('SECRET_KEY') else '[MISSING]'}")
