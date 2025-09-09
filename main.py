# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from llm import generate_response, get_conversation_status
from session_memory import SessionMemory
from db_logger import log_chat
from website_analyzer import analyze_website, generate_analysis_report
from user_profile import get_user_profile, is_profile_complete
import re

load_dotenv()
app = FastAPI()

# CORS to allow Streamlit (port 8501) to call FastAPI (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
memory = SessionMemory()

# Request schemas
class ChatInput(BaseModel):
    user_id: str
    message: str

class WebsiteAnalysisInput(BaseModel):
    user_id: str
    url: str

# Root endpoint - Greet user
@app.get("/")
async def greet():
    return {
        "message": "مرحباً! أنا مورفو، مساعدك التسويقي الذكي. دعني أتعرف عليك أولاً!",
        "available_actions": [
            "بدء المحادثة",
            "تحليل موقع ويب",
            "استشارة تسويقية"
        ]
    }

# GET /profile/{user_id} - Get user profile status
@app.get("/profile/{user_id}")
async def get_profile(user_id: str):
    profile = get_user_profile(user_id)
    status = get_conversation_status(user_id)
    
    return {
        "user_id": user_id,
        "profile": profile,
        "conversation_status": status
    }

# POST /chat endpoint with conversation flow
@app.post("/chat")
async def chat(input: ChatInput):
    history = memory.get_history(input.user_id)
    
    # If the message contains a URL and profile is complete, run website analysis directly
    url_match = re.search(r"https?://[^\s]+", input.message.strip())
    if url_match and is_profile_complete(input.user_id):
        try:
            user_profile = get_user_profile(input.user_id)
            url = url_match.group(0)
            website_data = analyze_website(url)
            analysis_report = generate_analysis_report(website_data, user_profile)
            response = analysis_report
        except Exception as e:
            response = f"عذراً، حدث خطأ أثناء تحليل الموقع: {str(e)}"
    else:
        # Generate response with user profile context
        response = generate_response(input.message, history, input.user_id)
    
    # Store in memory
    memory.append(input.user_id, input.message, response)
    
    # Log the interaction
    log_chat(input.user_id, input.message, response)
    
    # Get conversation status
    status = get_conversation_status(input.user_id)
    
    return {
        "response": response,
        "history": memory.get_history(input.user_id),
        "conversation_status": status,
        "profile_complete": is_profile_complete(input.user_id)
    }

# POST /analyze-website endpoint
@app.post("/analyze-website")
async def analyze_website_endpoint(input: WebsiteAnalysisInput):
    # Check if profile is complete
    if not is_profile_complete(input.user_id):
        return {
            "error": "يرجى إكمال ملفك الشخصي أولاً",
            "message": "دعني أتعرف عليك أكثر قبل تحليل المواقع"
        }
    
    # Get user profile for personalized analysis
    user_profile = get_user_profile(input.user_id)
    
    # Analyze the website
    website_data = analyze_website(input.url)
    
    # Generate smart analysis report with user profile
    analysis_report = generate_analysis_report(website_data, user_profile)
    
    # Log the interaction
    log_chat(input.user_id, f"تحليل موقع: {input.url}", analysis_report)
    
    return {
        "website_data": website_data,
        "analysis_report": analysis_report,
        "user_id": input.user_id,
        "user_profile": user_profile
    }

# POST /reset-profile - Reset user profile
@app.post("/reset-profile/{user_id}")
async def reset_profile(user_id: str):
    from user_profile import update_conversation_stage
    update_conversation_stage(user_id, 'greeting')
    memory.clear(user_id)
    
    return {
        "message": "تم إعادة تعيين ملفك الشخصي",
        "user_id": user_id
    }