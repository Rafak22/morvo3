# user_profile.py
import sqlite3
import os
from datetime import datetime
import json

DB_FILE = os.getenv("DB_FILE", "user_profiles.db")

def _ensure_columns(cursor):
    """Ensure required columns exist on the user_profiles table (idempotent)."""
    cursor.execute("PRAGMA table_info(user_profiles)")
    existing_columns = {row[1] for row in cursor.fetchall()}
    required_columns = [
        ('website_url', "TEXT"),
        ('website_analysis', "TEXT"),
        ('conversation_stage', "TEXT DEFAULT 'greeting'")
    ]
    for column_name, column_type in required_columns:
        if column_name not in existing_columns:
            cursor.execute(f"ALTER TABLE user_profiles ADD COLUMN {column_name} {column_type}")

# Create user profile table and run lightweight migration
def init_user_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            business_type TEXT,
            goals TEXT,
            website_url TEXT,
            website_analysis TEXT,
            created_at TEXT,
            updated_at TEXT,
            conversation_stage TEXT DEFAULT 'greeting'
        )
    """)
    # Ensure new columns exist for older databases (idempotent migration)
    _ensure_columns(c)
    conn.commit()
    conn.close()

# Get user profile
def get_user_profile(user_id: str) -> dict:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM user_profiles WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    
    if result:
        columns = [description[0] for description in c.description]
        data = dict(zip(columns, result))
        conn.close()
        return data
    conn.close()
    return None

# Update user profile
def update_user_profile(user_id: str, **kwargs):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Get existing profile
    existing = get_user_profile(user_id)
    if not existing:
        # Create new profile
        c.execute("""
            INSERT INTO user_profiles (user_id, created_at, updated_at)
            VALUES (?, ?, ?)
        """, (user_id, datetime.utcnow().isoformat(), datetime.utcnow().isoformat()))
    
    # Update fields
    for key, value in kwargs.items():
        if key in ['name', 'business_type', 'goals', 'website_url', 
                   'website_analysis', 'conversation_stage']:
            try:
                c.execute(f"""
                    UPDATE user_profiles 
                    SET {key} = ?, updated_at = ?
                    WHERE user_id = ?
                """, (value, datetime.utcnow().isoformat(), user_id))
            except sqlite3.OperationalError as e:
                # If a column is missing (older DB), add it and retry once
                if 'no such column' in str(e):
                    _ensure_columns(c)
                    c.execute(f"""
                        UPDATE user_profiles 
                        SET {key} = ?, updated_at = ?
                        WHERE user_id = ?
                    """, (value, datetime.utcnow().isoformat(), user_id))
                else:
                    raise
    
    conn.commit()
    conn.close()

# Get conversation stage
def get_conversation_stage(user_id: str) -> str:
    profile = get_user_profile(user_id)
    return profile.get('conversation_stage', 'greeting') if profile else 'greeting'

# Update conversation stage
def update_conversation_stage(user_id: str, stage: str):
    update_user_profile(user_id, conversation_stage=stage)

# Get next question based on stage
def get_next_question(user_id: str) -> str:
    stage = get_conversation_stage(user_id)
    profile = get_user_profile(user_id)
    
    questions = {
        'greeting': "مرحباً! أنا مورفو، مساعدك التسويقي الذكي. ما اسمك؟",
        'name': "أهلاً وسهلاً {name}! ما هي وظيفتك أو دورك في الشركة؟".format(name=profile.get('name', '') if profile else ''),
        'business_type': "ممتاز! ما هي أهدافك التسويقية الرئيسية؟",
        'goals': "شكراً لك! الآن أريد رابط موقع شركتك الإلكتروني لأحلل معلومات الشركة وأساعدك بشكل أفضل.",
        'complete': "ممتاز! تم تحليل موقع شركتك. الآن يمكنني مساعدتك في التسويق بناءً على معلومات شركتك. كيف يمكنني مساعدتك اليوم؟"
    }
    
    return questions.get(stage, "كيف يمكنني مساعدتك اليوم؟")

# Check if profile is complete
def is_profile_complete(user_id: str) -> bool:
    profile = get_user_profile(user_id)
    if not profile:
        return False
    
    # Require 4 essential fields including website
    required_fields = ['name', 'business_type', 'goals', 'website_url']
    
    return all(profile.get(field) for field in required_fields)

# Get profile summary for LLM
def get_profile_summary(user_id: str) -> str:
    profile = get_user_profile(user_id)
    if not profile or not is_profile_complete(user_id):
        return ""
    
    summary = f"""
    معلومات المستخدم الأساسية:
    - الاسم: {profile.get('name', 'غير محدد')}
    - الوظيفة: {profile.get('business_type', 'غير محدد')}
    - الأهداف التسويقية: {profile.get('goals', 'غير محدد')}
    - موقع الشركة: {profile.get('website_url', 'غير محدد')}
    """
    
    # Add website analysis if available
    if profile.get('website_analysis'):
        summary += f"\nتحليل الموقع:\n{profile.get('website_analysis')}"
    
    return summary

# Initialize database on import
init_user_db()
