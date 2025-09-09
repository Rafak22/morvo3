import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Backend URL configuration - use environment variable or default to local for development
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Determine if we're running locally or in the cloud
IS_LOCAL = BACKEND_URL == "http://127.0.0.1:8000"