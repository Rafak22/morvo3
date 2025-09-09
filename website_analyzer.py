# website_analyzer.py
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
from openai import OpenAI
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        _client = OpenAI(api_key=api_key)
    return _client

def analyze_website(url: str) -> dict:
    """
    Analyze a website and extract key information.
    """
    try:
        # Validate URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        print(f"Fetching URL: {url}")  # Debug log
        
        # Simple GET request with increased timeout
        response = requests.get(
            url,
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=60,  # Increased timeout
            verify=False  # Skip SSL verification
        )
        response.raise_for_status()
        
        # Basic HTML parsing
        soup = BeautifulSoup(response.text, 'html.parser')
        print("Successfully parsed HTML")  # Debug log
        
        # Initialize variables
        title = "No title found"
        description = "No description found"
        content = "Could not extract content"
        
        # Extract title
        try:
            if soup.title and soup.title.string:
                title = soup.title.string.strip()
        except Exception as e:
            print(f"Error extracting title: {e}")
        
        # Extract description
        try:
            meta_desc = soup.find('meta', {'name': ['description', 'Description']})
            if meta_desc and meta_desc.get('content'):
                description = meta_desc['content'].strip()
        except Exception as e:
            print(f"Error extracting description: {e}")
        
        # Extract content
        try:
            paragraphs = []
            for p in soup.find_all('p', limit=2):
                if p.get_text():
                    paragraphs.append(p.get_text().strip())
            if paragraphs:
                content = ' '.join(paragraphs)
        except Exception as e:
            print(f"Error extracting content: {e}")
        
        return {
            'url': url,
            'domain': urlparse(url).netloc,
            'title': title,
            'description': description,
            'content_preview': content[:300] + '...' if len(content) > 300 else content,
            'status': 'success'
        }
        
    except requests.Timeout:
        print(f"Timeout error for URL: {url}")  # Debug log
        return {
            'url': url,
            'status': 'error',
            'error': 'الموقع يستغرق وقتاً طويلاً للرد. يرجى المحاولة مرة أخرى.'
        }
    except requests.RequestException as e:
        print(f"Request error for URL {url}: {str(e)}")  # Debug log
        return {
            'url': url,
            'status': 'error',
            'error': f'خطأ في الوصول للموقع: {str(e)}'
        }
    except Exception as e:
        print(f"Analysis error for URL {url}: {str(e)}")  # Debug log
        return {
            'url': url,
            'status': 'error',
            'error': f'خطأ في تحليل الموقع: {str(e)}'
        }

def generate_analysis_report(website_data: dict, user_profile: dict = None) -> str:
    """
    Generate a smart analysis report using GPT with user profile context.
    """
    if website_data['status'] == 'error':
        return f"عذراً، لم أتمكن من تحليل الموقع {website_data['url']}. الخطأ: {website_data['error']}"
    
    # Prepare context for GPT
    context = f"""
    تحليل موقع: {website_data['domain']}
    العنوان: {website_data['title']}
    الوصف: {website_data['description']}
    محتوى أولي: {website_data['content_preview']}
    """
    
    # Add user profile context if available
    profile_context = ""
    if user_profile:
        profile_context = f"""
    معلومات المستخدم:
    - الاسم: {user_profile.get('name', 'غير محدد')}
    - نوع العمل: {user_profile.get('business_type', 'غير محدد')}
    - الأهداف: {user_profile.get('goals', 'غير محدد')}
    """
    
    # Generate analysis using GPT
    client = get_client()
    
    try:
        system_prompt = """أنت مورفو، مساعد تسويقي ذكي. قم بتحليل الموقع المقدم وقدم تقريراً شاملاً باللغة العربية يتضمن:
        1. تقييم عام للموقع
        2. نقاط القوة والضعف
        3. اقتراحات للتحسين
        4. توصيات تسويقية مخصصة
        5. استخراج معلومات عن نوع العمل والصناعة من الموقع
        اجعل التقرير مفيداً ومهنياً ومخصصاً للمستخدم."""
        
        if user_profile:
            system_prompt += f"\n\nاستخدم معلومات المستخدم التالية لتخصيص التوصيات:\n{profile_context}"
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"يرجى تحليل هذا الموقع:\n{context}"},
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()
        
    except Exception as e:
        return f"عذراً، حدث خطأ في تحليل الموقع: {str(e)}"