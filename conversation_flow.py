# conversation_flow.py
from user_profile import (
    get_conversation_stage, update_conversation_stage, 
    get_next_question, update_user_profile, is_profile_complete,
    get_profile_summary
)
import re

def process_user_response(user_id: str, message: str) -> dict:
    """
    Process user response and determine next action
    """
    stage = get_conversation_stage(user_id)
    
    # Extract information based on current stage
    extracted_info = extract_information(stage, message)
    
    # Update user profile with extracted information
    if extracted_info:
        update_user_profile(user_id, **extracted_info)
    
    # If this is a website URL, analyze it
    if stage == 'goals' and extracted_info.get('website_url'):
        website_analysis = analyze_website_for_profile(extracted_info['website_url'])
        if website_analysis:
            update_user_profile(user_id, website_analysis=website_analysis)
    
    # Move to next stage only if we extracted information
    if extracted_info:
        next_stage = get_next_stage(stage)
        update_conversation_stage(user_id, next_stage)
    else:
        next_stage = stage  # Stay in current stage if no info extracted
    
    # Check if profile is complete
    profile_complete = is_profile_complete(user_id)
    
    return {
        'stage': next_stage,
        'extracted_info': extracted_info,
        'profile_complete': profile_complete,
        'next_question': get_next_question(user_id) if not profile_complete else None
    }

def analyze_website_for_profile(website_url: str) -> str:
    """
    Analyze website and extract company information for profile
    """
    try:
        from website_analyzer import analyze_website, generate_analysis_report
        
        # Analyze the website
        website_data = analyze_website(website_url)
        
        if website_data.get('status') == 'success':
            # Generate analysis report
            analysis_report = generate_analysis_report(website_data)
            return analysis_report
        else:
            return f"عذراً، لم أتمكن من تحليل الموقع: {website_data.get('error', 'خطأ غير معروف')}"
            
    except Exception as e:
        return f"عذراً، حدث خطأ في تحليل الموقع: {str(e)}"

def extract_information(stage: str, message: str) -> dict:
    """
    Extract relevant information from user message based on current stage
    """
    info = {}
    
    if stage == 'greeting':
        # Extract name from greeting message
        name = extract_name(message)
        if name:
            info['name'] = name
    
    elif stage == 'name':
        # Extract job role/position
        job_role = extract_job_role(message)
        if job_role:
            info['business_type'] = job_role
    
    elif stage == 'business_type':
        # Extract goals
        goals = extract_goals(message)
        if goals:
            info['goals'] = goals
    
    elif stage == 'goals':
        # Extract website URL
        website_url = extract_website_url(message)
        if website_url:
            info['website_url'] = website_url
    
    return info

def extract_name(message: str) -> str:
    """Extract name from message with improved validation"""
    # Clean and prepare the message
    message = message.strip()
    
    # Check for URLs - if found, return empty to trigger error message
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    if re.search(url_pattern, message):
        return ""
        
    # Remove common prefixes that might confuse name extraction
    prefixes_to_remove = [
        "انا ", "أنا ", "اسمي ", "إسمي ",
        "مرحبا ", "مرحباً ", "السلام عليكم",
        "http", "www", ".com", ".net", ".org"
    ]
    
    for prefix in prefixes_to_remove:
        if message.startswith(prefix):
            message = message[len(prefix):].strip()
    
    # Split into words and get the first word as name
    words = message.split()
    if not words:
        return ""
        
    potential_name = words[0].strip()
    
    # Validate the potential name
    # Check if it's too long (probably a sentence)
    if len(potential_name) > 20:
        return ""
        
    # Check if it contains numbers or special characters
    if re.search(r'[0-9@#$%^&*(),.?":{}|<>]', potential_name):
        return ""
        
    # Check if it's too short
    if len(potential_name) < 2:
        return ""
        
    return potential_name

def extract_job_role(message: str) -> str:
    """Extract job role/position from message"""
    return message  # Return the full message as job role

def extract_website_url(message: str) -> str:
    """Extract website URL from message"""
    import re
    # Look for URLs in the message
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, message)
    if urls:
        return urls[0]
    
    # If no URL found, return the message (might be a domain name)
    return message

def extract_goals(message: str) -> str:
    """Extract marketing goals from message"""
    return message

def get_next_stage(current_stage: str) -> str:
    """Get the next conversation stage - 4 stages including website"""
    stages = ['greeting', 'name', 'business_type', 'goals', 'complete']
    
    try:
        current_index = stages.index(current_stage)
        if current_index < len(stages) - 1:
            return stages[current_index + 1]
        else:
            return 'complete'
    except ValueError:
        return 'greeting'

def should_continue_profile_building(user_id: str) -> bool:
    """Check if we should continue building the profile"""
    return not is_profile_complete(user_id)

def get_personalized_response(user_id: str, message: str) -> str:
    """Get personalized response based on user profile"""
    profile_summary = get_profile_summary(user_id)
    
    if profile_summary:
        return f"بناءً على معلوماتك، {message}"
    else:
        return message