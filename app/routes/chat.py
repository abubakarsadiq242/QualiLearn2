import requests
import os
from dotenv import load_dotenv

# Ensure environment variables are loaded from root .env
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
load_dotenv(os.path.join(basedir, '.env'), override=True)

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.chat import ChatMessage
from app.models.user import User
from app.models.learning import LearningMaterial
from app import db

chat_bp = Blueprint('chat', __name__)

def call_groq_api(prompt):
    # Try app config first, then env vars
    api_key = current_app.config.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    
    if not api_key:
        return "I'm sorry, but my AI core is currently offline (API Key Missing). Please contact the administrator."

    url = "https://api.groq.com/openai/v1/chat/completions"
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "You are a professional educational tutor. Provide clear, accurate, and concise academic support."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_completion_tokens": 1024,
        "top_p": 1,
        "stream": False
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        print(f" * Groq Response Status: {response.status_code}")
        response.raise_for_status()
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            content = result['choices'][0]['message']['content']
            return content
        
        return "I understood your question, but I'm having trouble generating a response. Could you try asking in a different way?"
    except requests.exceptions.RequestException as e:
        print(f"Groq API Request Error: {e}")
        return "I'm having a brief technical moment connecting to my brain. Please try again in a few seconds!"
    except Exception as e:
        print(f"Groq Unexpected Error: {e}")
        return "I'm having a brief technical moment. Please try again in a few seconds!"

@chat_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    try:
        print(">>> CHAT SEND REQUEST START")
        user_id = int(get_jwt_identity())
        data = request.get_json()
        print(f"User ID: {user_id}, Message: {data.get('message')}")
        
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

        # Build prompt safely
        prompt_template = f"""
        You are {{persona_name}}, {{persona_role}}. 
        Your goal is to {{persona_goal}}.

        IMPORTANT: Respond ONLY in {{lang_name}}.

        STRICT GUIDELINES:
        - DIRECT ANSWER ONLY: Do NOT include greetings, introductions, or any conversational filler. Start the very first sentence with the answer.
        - NO META-COMMENTARY: Do NOT say "Sure, here is the answer" or "I can help with that".
        - Tone: Highly direct, professional, and concise.
        - {{persona_feature}}
        - CLEAN TEXT: Use ONLY plain text and LaTeX math. ABSOLUTELY NO markdown stars (*), bold markers (**), or headers (#).
        - Accuracy: Provide the exact, correct answer the user is looking for.
        - {{persona_context}}

        Context:
        {{context}}
        
        Student Inquiry: {{message}}
        """
        
        persona_feature = "Technical Guidance: Provide step-by-step practical instructions where applicable." if user_lvl == 'Vocational' else "Math Formulas: Use professional LaTeX formatting for all mathematical equations. Use $ formula $ for inline and $$ formula $$ for large block equations."
        
        prompt = prompt_template.replace("{persona_name}", persona_name) \
                                 .replace("{persona_role}", persona_role) \
                                 .replace("{persona_goal}", persona_goal) \
                                 .replace("{lang_name}", lang_name) \
                                 .replace("{persona_feature}", persona_feature) \
                                 .replace("{persona_context}", persona_context) \
                                 .replace("{context}", context) \
                                 .replace("{message}", data.get('message', ''))
        
        print("Calling Groq API...")
        bot_response = call_groq_api(prompt)
        print(f"Groq API returned: {bot_response[:100]}...")
        
        bot_msg = ChatMessage(user_id=user_id, message=bot_response, is_bot=True)
        db.session.add(bot_msg)
        
        # Reward progress
        if user:
            user.study_time = (user.study_time or 0) + 2
            user.overall_progress = min(100, (user.overall_progress or 0) + 0.05)
        
        db.session.commit()
        
        print("<<< CHAT SEND REQUEST END SUCCESS")
        return jsonify({
            "success": True,
            "data": bot_msg.to_dict()
        })
    except Exception as e:
        print(f"!!! CRITICAL CHAT ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"Server encountered an error processing your chat: {str(e)}"
        }), 500

@chat_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    user_id = int(get_jwt_identity())
    messages = ChatMessage.query.filter_by(user_id=user_id).order_by(ChatMessage.timestamp.asc()).all()
    return jsonify({
        "success": True,
        "data": [m.to_dict() for m in messages]
    })

@chat_bp.route('/clear', methods=['DELETE'])
@jwt_required()
def clear_history():
    user_id = int(get_jwt_identity())
    ChatMessage.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Chat history cleared"
    })
