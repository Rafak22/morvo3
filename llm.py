# llm.py
import os
from dotenv import load_dotenv
from openai import OpenAI
from rag_retriever import retrieve_context
from conversation_flow import process_user_response, should_continue_profile_building, get_personalized_response
from user_profile import get_profile_summary, get_conversation_stage

load_dotenv()
OPENAI_MODEL = "gpt-4"
_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        _client = OpenAI(api_key=api_key)
    return _client

def generate_response(message: str, history: list[str], user_id: str = "default") -> str:
    """
    Generate a smart response using GPT-4o with user profile and conversation flow.
    """
    # Check if we need to continue profile building
    if should_continue_profile_building(user_id):
        # Process user response for profile building
        flow_result = process_user_response(user_id, message)
        
        if flow_result['next_question']:
            return flow_result['next_question']
        else:
            # Profile is complete, continue with normal conversation
            pass
    
    # Get user profile summary
    profile_summary = get_profile_summary(user_id)
    
    # Step 1: Retrieve semantic memory from RAG (optional)
    try:
        context = retrieve_context(message)
    except Exception as e:
        print(f"RAG context retrieval failed: {e}")
        context = ""

    # Step 2: Build prompt with RAG + profile + history
    system_prompt = "أنت مورفو، مساعد تسويقي ذكي. جاوب بإجابات قصيرة دقيقة وسياقية."
    
    if profile_summary:
        system_prompt += f"\n\n{profile_summary}\nاستخدم هذه المعلومات لتقديم نصائح مخصصة."
    
    messages = [{"role": "system", "content": system_prompt}]
    
    if context:
        messages.append({"role": "system", "content": context})

    for i, text in enumerate(history[-6:]):  # Keep last 3 user-bot pairs
        role = "user" if i % 2 == 0 else "assistant"
        messages.append({"role": role, "content": text})

    # Add current message
    messages.append({"role": "user", "content": message})

    # Step 3: Send to OpenAI
    client = get_client()
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()

def get_conversation_status(user_id: str) -> dict:
    """
    Get current conversation status and next steps
    """
    from user_profile import get_conversation_stage, is_profile_complete, get_user_profile
    
    stage = get_conversation_stage(user_id)
    profile_complete = is_profile_complete(user_id)
    profile = get_user_profile(user_id)
    
    return {
        'stage': stage,
        'profile_complete': profile_complete,
        'profile': profile,
        'next_question': get_next_question(user_id) if not profile_complete else None
    }

def get_next_question(user_id: str) -> str:
    """
    Get the next question for profile building
    """
    from conversation_flow import get_next_question
    return get_next_question(user_id)