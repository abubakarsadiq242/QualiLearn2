import requests
import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.chat import ChatMessage
from app.models.user import User
from app.models.learning import LearningMaterial
from app import db
from datetime import datetime

chat_bp = Blueprint('chat', __name__)

def call_gemini_api(prompt):
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "I'm sorry, but my AI core is currently offline (API Key Missing). Please contact the administrator."

    # Using the stable 1.5 flash model
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "topP": 0.8,
            "topK": 40,
            "maxOutputTokens": 2048,
        }
    }
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if 'candidates' in result and len(result['candidates']) > 0:
            part = result['candidates'][0]['content']['parts'][0]
            if 'text' in part:
                return part['text']
        
        return "I understood your question, but I'm having trouble generating a response. Could you try asking in a different way?"
    except requests.exceptions.RequestException as e:
        print(f"Gemini API Request Error: {e}")
        if response.status_code == 429:
            return "I'm receiving too many questions at once! Please wait about 10 seconds and try again — I'll be ready."
        if response.status_code >= 500:
            return "Google's AI service is currently taking a short break (500 Error). Please try again in a few moments."
        return "I'm having a brief technical moment connecting to my brain. Please try again in a few seconds!"
    except Exception as e:
        print(f"Gemini Unexpected Error: {e}")
        return "I'm having a brief technical moment. Please try again in a few seconds!"

@chat_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data or not data.get('message'):
        return jsonify({"success": False, "message": "Missing message content"}), 400
        
    user_msg = ChatMessage(user_id=user_id, message=data.get('message'), is_bot=False)
    db.session.add(user_msg)
    
    # Fetch user details for personalization
    user = db.session.get(User, user_id)
    user_lang = user.language if user else 'en'
    user_lvl = user.education_level if user else 'Secondary'
    
    # Fetch some context from learning materials
    materials = LearningMaterial.query.filter_by(language=user_lang).limit(3).all()
    if not materials:
        materials = LearningMaterial.query.filter_by(language='en').limit(3).all()
        
    context = "\n".join([f"{m.subject}: {m.content[:300]}" for m in materials])
    
    # Map language codes to names for the AI
    lang_map = {
        'en': 'English', 'ha': 'Hausa', 'yo': 'Yoruba', 'ig': 'Igbo', 'pi': 'Nigerian Pidgin'
    }
    lang_name = lang_map.get(user_lang, 'English')

    # Determine Persona based on user level
    if user_lvl == 'Vocational':
        persona_name = "Workshop Expert"
        persona_role = "a master craftsman and professional vocational mentor"
        persona_goal = "provide expert-level technical guidance, troubleshooting, and career advice for vocational skills"
        persona_context = "Your focus is purely on practical skills, industrial standards, and hands-on craftsmanship."
    else:
        persona_name = "QualiLearn AI"
        persona_role = "a professional academic mentor for Nigerian students"
        persona_goal = f"provide clear, expert-level, and supportive guidance for a {user_lvl} student"
        persona_context = "Your focus is on academic excellence, curriculum mastery, and exam preparation."

    # Build prompt safely: AI should ALWAYS respond in English per user requirement
    prompt_template = f"""
    You are {persona_name}, {persona_role}. 
    Your goal is to {persona_goal}.

    IMPORTANT: Respond ONLY in {lang_name}.

    STRICT GUIDELINES:
    - DIRECT ANSWER ONLY: Do NOT include greetings, introductions, or any conversational filler. Start the very first sentence with the answer.
    - NO META-COMMENTARY: Do NOT say "Sure, here is the answer" or "I can help with that".
    - Tone: Highly direct, professional, and concise.
    - { "Technical Guidance: Provide step-by-step practical instructions where applicable." if user_lvl == 'Vocational' else "Math Formulas: Use professional LaTeX formatting for all mathematical equations. Use $ formula $ for inline and $$ formula $$ for large block equations." }
    - CLEAN TEXT: Use ONLY plain text and LaTeX math. ABSOLUTELY NO markdown stars (*), bold markers (**), or headers (#).
    - Accuracy: Provide the exact, correct answer the user is looking for.
    - {persona_context}

    Context (Curriculum/Workshop Reference):
    {{context}}
    
    Student Inquiry: {{message}}
    """
    
    prompt = prompt_template.replace("{context}", context) \
                             .replace("{message}", data.get('message', '')) \
                             .replace("{lang_name}", lang_name)
    
    bot_response = call_gemini_api(prompt)
    
    bot_msg = ChatMessage(user_id=user_id, message=bot_response, is_bot=True)
    db.session.add(bot_msg)
    
    # Reward progress
    if user:
        user.study_time = (user.study_time or 0) + 2 # Add 2 mins per interaction
        user.overall_progress = min(100, (user.overall_progress or 0) + 0.05)
        
        # Log to detailed ActivityLog
        from app.models.analytics import ActivityLog
        log = ActivityLog(
            user_id=user_id,
            portal_type='vocational' if user_lvl == 'Vocational' else 'secondary',
            activity_type="ai_chat",
            module="Workshop Support" if user_lvl == 'Vocational' else "AI Support",
            duration=120, 
            start_time=datetime.utcnow().isoformat(),
            end_time=datetime.utcnow().isoformat(),
            score=0
        )
        db.session.add(log)
    
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Message sent and response received",
        "data": {
            "user_message": user_msg.to_dict(),
            "bot_message": bot_msg.to_dict()
        }
    }), 201

@chat_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    user_id = get_jwt_identity()
    messages = ChatMessage.query.filter_by(user_id=user_id).order_by(ChatMessage.created_at.asc()).all()
    
    return jsonify({
        "success": True,
        "message": "Chat history fetched successfully",
        "data": [m.to_dict() for m in messages]
    }), 200

@chat_bp.route('/clear', methods=['DELETE'])
@jwt_required()
def clear_history():
    user_id = get_jwt_identity()
    ChatMessage.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Chat history cleared successfully"
    }), 200
