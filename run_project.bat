@echo off
cd /d %~dp0
if not exist .venv (
    python -m venv .venv
)
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
start "ResumeIQ Backend" cmd /k "call .venv\Scripts\activate && cd backend && python -m uvicorn app.main:app --reload --port 8000"
timeout /t 3 /nobreak >nul
start "ResumeIQ Frontend" cmd /k "call .venv\Scripts\activate && streamlit run frontend\app.py"
