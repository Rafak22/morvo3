import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Backend URL configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
