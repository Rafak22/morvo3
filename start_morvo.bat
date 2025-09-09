@echo off
echo Starting MORVO...

REM Start backend server
start cmd /k "cd /d %~dp0 && (
set OPENAI_API_KEY=your_api_key_here
uvicorn main:app --reload
)"

REM Wait a moment for the backend to start
timeout /t 2 /nobreak >nul

REM Start Streamlit frontend
start cmd /k "cd /d %~dp0 && python -m streamlit run streamlit_app.py"

echo MORVO is running!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8501