# streamlit_app.py
import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="MORVO - مساعدك التسويقي الذكي",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom theme with Saudi-inspired colors
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --saudi-green: #006D5B;
        --royal-purple: #6A0DAD;
        --dark-gray: #1F1F1F;
        --soft-white: #F8F8F8;
        --golden: #FFB800;
        --light-blue: #2DA8FF;
    }

    /* Override Streamlit's default theme */
    .stApp {
        background: linear-gradient(135deg, var(--soft-white) 0%, #E8F0ED 100%) !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background: transparent !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--saudi-green) 0%, #005347 100%) !important;
        border-radius: 0 20px 20px 0;
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: var(--soft-white) !important;
    }
    
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Make sidebar text white */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] div:not(.stProgress) {
        color: var(--soft-white) !important;
    }
</style>
""", unsafe_allow_html=True)

# Custom CSS for better colors and Arabic support
st.markdown("""
<style>
    /* Main header with Saudi theme */
    .main-header {
        text-align: center;
        font-size: 2.8rem;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, var(--saudi-green) 0%, var(--golden) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding: 20px;
        border-radius: 15px;
    }
    
    .arabic-text {
        direction: rtl;
        text-align: right;
        font-family: 'Segoe UI', 'Arial', sans-serif;
        font-size: 16px;
    }
    
    /* Chat message styling - Light Blue Theme */
    .chat-message {
        padding: 15px 20px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
        border: 1px solid #e0f2fe;
    }
    
    .user-message {
        background: linear-gradient(135deg, #9747FF 0%, #7E30CC 100%);
        color: white !important;
        margin-left: 15%;
        border-left: 4px solid var(--golden);
        box-shadow: 0 4px 15px rgba(106, 13, 173, 0.2);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .user-message strong, .user-message span {
        color: white !important;
    }
    
    .bot-message {
        background: linear-gradient(135deg, var(--saudi-green) 0%, #005347 100%);
        color: white !important;
        margin-right: 15%;
        border-right: 4px solid var(--golden);
        box-shadow: 0 4px 15px rgba(0, 109, 91, 0.2);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .bot-message strong, .bot-message span {
        color: white !important;
    }
    
    /* Input styling with Saudi theme */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid var(--saudi-green);
        padding: 12px 20px;
        font-size: 16px;
        background: var(--soft-white);
        color: var(--dark-gray) !important;
        box-shadow: 0 2px 10px rgba(0, 109, 91, 0.1);
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--golden);
        box-shadow: 0 2px 15px rgba(255, 184, 0, 0.2);
    }
    
    /* Button styling with Saudi theme */
    .stButton > button {
        background: linear-gradient(135deg, var(--saudi-green) 0%, #005347 100%);
        color: var(--soft-white);
        border: 2px solid var(--golden);
        border-radius: 25px;
        padding: 12px 30px;
        font-size: 16px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0, 109, 91, 0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 109, 91, 0.3);
        background: linear-gradient(135deg, var(--royal-purple) 0%, #4A0982 100%);
        border-color: var(--light-blue);
    }

    /* Primary button variation */
    .stButton > button[data-baseweb="button"][kind="primary"] {
        background: linear-gradient(135deg, var(--royal-purple) 0%, #4A0982 100%);
        border-color: var(--golden);
    }

    .stButton > button[data-baseweb="button"][kind="primary"]:hover {
        background: linear-gradient(135deg, var(--saudi-green) 0%, #005347 100%);
        border-color: var(--light-blue);
    }
    
    /* Sidebar styling - Light Blue Theme */
    .css-1d391kg {
        background: linear-gradient(180deg, #f0f9ff 0%, #e0f2fe 100%);
    }
    
    /* Tab styling - Light Blue Theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #f0f9ff;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-weight: bold;
        border: 1px solid #e0f2fe;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: white;
    }
    
    /* Metric styling - Light Blue Theme */
    .metric-card {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
    }
    
    /* Website analysis styling - Light Blue Theme */
    .website-info {
        background: #f0f9ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
        margin: 10px 0;
        border: 1px solid #e0f2fe;
    }
    
    .analysis-report {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #0ea5e9;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.15);
    }
    
    /* Loading spinner - Light Blue Theme */
    .loading {
        text-align: center;
        color: #3b82f6;
        font-size: 18px;
        font-weight: bold;
    }
    
    /* Success message - Light Blue Theme */
    .success-message {
        background: #dbeafe;
        color: #1e40af;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #93c5fd;
        margin: 10px 0;
    }
    
    /* Error message - Light Blue Theme */
    .error-message {
        background: #fef2f2;
        color: #dc2626;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #fca5a5;
        margin: 10px 0;
    }
    
    /* Main background - Light theme */
    .main .block-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        color: #1e293b;
    }
    
    /* Sidebar background - Light theme */
    .css-1d391kg {
        background: linear-gradient(180deg, #ffffff 0%, #f1f5f9 100%);
    }
    
    /* Force light theme for all elements */
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    }
    
    /* Text input styling - Dark text on light background */
    .stTextInput > div > div > input {
        background: #ffffff !important;
        color: #1e293b !important;
        border: 2px solid #3b82f6;
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        background: #ffffff !important;
        color: #1e293b !important;
        border: 2px solid #3b82f6;
    }
    
    /* All text should be dark */
    .stMarkdown, .stText, p, div, span {
        color: #1e293b !important;
    }
    
    /* Sidebar text */
    .css-1d391kg .stMarkdown, .css-1d391kg p, .css-1d391kg div {
        color: #1e293b !important;
    }
    
    /* Override Streamlit's dark theme */
    .stApp > header {
        background-color: #ffffff;
    }
    
    .stApp > div {
        background-color: #ffffff;
    }
    
    /* Force all containers to have light background */
    .stContainer, .stColumn, .stRow {
        background-color: transparent !important;
    }
    
    /* Info boxes styling with Saudi theme */
    .stInfo {
        background-color: rgba(45, 168, 255, 0.1) !important;
        border: 1px solid var(--light-blue) !important;
        color: var(--dark-gray) !important;
        border-radius: 15px !important;
    }
    
    .stSuccess {
        background-color: rgba(0, 109, 91, 0.1) !important;
        border: 1px solid var(--saudi-green) !important;
        color: var(--saudi-green) !important;
        border-radius: 15px !important;
    }
    
    .stWarning {
        background-color: rgba(255, 184, 0, 0.1) !important;
        border: 1px solid var(--golden) !important;
        color: var(--dark-gray) !important;
        border-radius: 15px !important;
    }
    
    .stError {
        background-color: rgba(106, 13, 173, 0.1) !important;
        border: 1px solid var(--royal-purple) !important;
        color: var(--royal-purple) !important;
        border-radius: 15px !important;
    }
    
    /* Make sure all text is visible */
    .stSelectbox > div > div, .stTextInput > div > div, .stTextArea > div > div {
        background-color: #ffffff !important;
        color: #1e293b !important;
    }
    
    /* Tab text */
    .stTabs [data-baseweb="tab"] {
        color: #1e293b !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Import configuration
from config import BACKEND_URL, IS_LOCAL

# API base URL - works both locally and in cloud
API_BASE = BACKEND_URL

# Show environment indicator in development
if IS_LOCAL:
    st.sidebar.info("🔧 Running in Development Mode", icon="⚙️")
else:
    st.sidebar.success("🌐 Running in Production Mode", icon="✨")

def call_api(endpoint, data=None):
    """Helper function to call FastAPI endpoints"""
    try:
        if data:
            response = requests.post(f"{API_BASE}{endpoint}", json=data, timeout=60)
        else:
            response = requests.get(f"{API_BASE}{endpoint}", timeout=60)
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.ConnectionError:
        return None
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def get_user_profile_status(user_id):
    """Get user profile status"""
    return call_api(f"/profile/{user_id}")

def main():
    # Header with better styling
    st.markdown('<h1 class="main-header">🤖 MORVO - مساعدك التسويقي الذكي</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'chat_count' not in st.session_state:
        st.session_state.chat_count = 0
    
    # Get profile status for the current user
    profile_status = get_user_profile_status(st.session_state.user_id) if st.session_state.user_id else None
    
    # Sidebar with improved styling
    with st.sidebar:
        st.markdown("### 👋 مرحباً بك في مورفو")
        
        if st.session_state.user_id is None:
            st.info("🌟 ابدأ رحلتك مع مورفو")
            if st.button("✨ مستخدم جديد", use_container_width=True):
                st.session_state.user_id = f"user_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                st.rerun()
        else:
            if profile_status and profile_status.get('profile'):
                profile = profile_status['profile']
                profile_complete = profile_status.get('conversation_status', {}).get('profile_complete', False)
                
                if profile_complete:
                    st.success("✅ أهلاً بعودتك!")
                    with st.expander("👤 معلوماتك الشخصية"):
                        st.markdown(f"**الاسم:** {profile.get('name', 'غير محدد')}")
                        st.markdown(f"**نوع العمل:** {profile.get('business_type', 'غير محدد')}")
                        if profile.get('industry'):
                            st.markdown(f"**الصناعة:** {profile.get('industry')}")
                else:
                    stage = profile_status.get('conversation_status', {}).get('stage', 'greeting')
                    st.warning("⏳ دعنا نتعرف عليك أكثر")
        
        st.markdown("### 📊 إحصائيات")
        
        # Custom metric display
        st.markdown(f'''
        <div class="metric-card">
            <h3>عدد المحادثات</h3>
            <h2>{st.session_state.chat_count}</h2>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.session_state.user_id:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ مسح المحادثة", help="مسح جميع الرسائل"):
                    st.session_state.messages = []
                    st.session_state.chat_count = 0
                    st.success("تم مسح المحادثة بنجاح!")
                    st.rerun()
            
            with col2:
                if st.button("✨ مستخدم جديد", help="بدء محادثة جديدة"):
                    # Clear all session state
                    st.session_state.messages = []
                    st.session_state.chat_count = 0
                    st.session_state.user_id = None
                    st.success("مرحباً بك! دعنا نبدأ من جديد.")
                    st.rerun()
        
        # Connection status
        st.markdown("### 🔗 حالة الاتصال")
        if call_api("/"):
            st.success("✅ متصل بالخادم")
        else:
            st.error("❌ غير متصل بالخادم")
    
    # Main content area with better tabs
    tab1, tab2 = st.tabs(["💬 محادثة ذكية", "🌐 تحليل المواقع"])
    
    with tab1:
        st.markdown('<div class="arabic-text">', unsafe_allow_html=True)
        
        # Display chat messages with better styling
        if st.session_state.messages:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f'<div class="chat-message user-message arabic-text"><strong>👤 أنت:</strong> {message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-message bot-message arabic-text"><strong>🤖 مورفو:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            # Show welcome message based on profile status
            if profile_status and profile_status.get('conversation_status', {}).get('profile_complete', False):
                st.info("👋 مرحباً! ملفك الشخصي مكتمل. كيف يمكنني مساعدتك اليوم؟")
            else:
                st.info("👋 مرحباً! أنا مورفو، مساعدك التسويقي الذكي. دعني أتعرف عليك أولاً!")
        
        # Chat input with better styling
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input("اكتب رسالتك هنا...", key="chat_input", placeholder="مثال: كيف يمكنني تحسين موقعي؟")
        
        with col2:
            if st.button("إرسال 📤", type="primary", use_container_width=True):
                if user_input:
                    # Add user message
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    
                    # Show loading
                    with st.spinner("جاري التفكير..."):
                        # Call API
                        response = call_api("/chat", {
                            "user_id": st.session_state.user_id,
                            "message": user_input
                        }) if st.session_state.user_id else None
                        
                        if response:
                            bot_response = response.get("response", "عذراً، حدث خطأ في الاستجابة")
                            st.session_state.messages.append({"role": "assistant", "content": bot_response})
                            st.session_state.chat_count += 1
                            
                            # Check if profile is complete
                            profile_complete = response.get("profile_complete", False)
                            if profile_complete:
                                st.success("🎉 تم إكمال ملفك الشخصي! الآن يمكنني مساعدتك بشكل أفضل.")
                            else:
                                st.success("تم إرسال الرسالة بنجاح!")
                        else:
                            st.session_state.messages.append({"role": "assistant", "content": "عذراً، لا يمكن الاتصال بالخادم. تأكد من تشغيل الخادم."})
                            st.error("خطأ في الاتصال بالخادم")
                    
                    st.rerun()
                else:
                    st.warning("يرجى كتابة رسالة")
        
        # Quick action buttons
        st.markdown("### 🚀 إجراءات سريعة")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💡 نصائح تسويقية", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "أعطني نصائح تسويقية مفيدة"})
                st.rerun()
        with col2:
            if st.button("📊 تحليل السوق", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "ساعدني في تحليل السوق"})
                st.rerun()
        with col3:
            if st.button("🎯 استراتيجية", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "ما هي أفضل استراتيجية تسويقية؟"})
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="arabic-text">', unsafe_allow_html=True)
        st.markdown("### 🔍 تحليل المواقع")
        
        if not st.session_state.user_id:
            st.warning("👋 مرحباً! لتحليل موقعك، نحتاج أولاً إلى التعرف عليك.")
            if st.button("✨ ابدأ رحلتك مع مورفو", use_container_width=True):
                st.session_state.user_id = f"user_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                st.rerun()
        else:
            if profile_status and profile_status.get('conversation_status', {}).get('profile_complete', False):
                st.markdown("أدخل رابط الموقع لتحليله والحصول على تقرير شامل")
            else:
                st.warning("⏳ دعنا نتعرف عليك أولاً!")
                st.info("انتقل إلى تبويب المحادثة وأجب على بعض الأسئلة البسيطة لنقدم لك تحليلاً مخصصاً")
        
        # Website input with better styling
        url_input = st.text_input("رابط الموقع:", placeholder="https://example.com", help="أدخل رابط الموقع الكامل")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔍 تحليل الموقع", type="primary", use_container_width=True, disabled=not (profile_status and profile_status.get('conversation_status', {}).get('profile_complete', False))):
                if url_input:
                    with st.spinner("جاري تحليل الموقع..."):
                        response = call_api("/analyze-website", {
                            "user_id": st.session_state.user_id,
                            "url": url_input
                        })
                        
                        if response:
                            website_data = response.get("website_data", {})
                            analysis_report = response.get("analysis_report", "")
                            
                            # Display website info with better styling
                            st.markdown("### 📋 معلومات الموقع")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown(f'''
                                <div class="website-info">
                                    <h4>🔗 الرابط</h4>
                                    <p>{website_data.get('url', 'غير متوفر')}</p>
                                    <h4>🌐 النطاق</h4>
                                    <p>{website_data.get('domain', 'غير متوفر')}</p>
                                </div>
                                ''', unsafe_allow_html=True)
                            
                            with col2:
                                st.markdown(f'''
                                <div class="website-info">
                                    <h4>📝 العنوان</h4>
                                    <p>{website_data.get('title', 'غير متوفر')}</p>
                                    <h4>🏷️ الكلمات المفتاحية</h4>
                                    <p>{website_data.get('keywords', 'غير متوفر')}</p>
                                </div>
                                ''', unsafe_allow_html=True)
                            
                            # Display analysis report with better styling
                            st.markdown("### 📊 تقرير التحليل")
                            st.markdown(f'<div class="analysis-report arabic-text">{analysis_report}</div>', unsafe_allow_html=True)
                            
                            # Add to chat history
                            st.session_state.messages.append({
                                "role": "user", 
                                "content": f"تحليل موقع: {url_input}"
                            })
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": analysis_report
                            })
                            st.session_state.chat_count += 1
                            
                            st.success("تم تحليل الموقع بنجاح!")
                        else:
                            st.error("عذراً، حدث خطأ في تحليل الموقع")
                else:
                    st.warning("يرجى إدخال رابط الموقع")
        
        with col2:
            if st.button("📋 مثال", use_container_width=True):
                st.info("مثال: https://www.google.com")
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()