@echo off
cd /d %~dp0
call .venv\Scripts\activate
cd backend
python -m uvicorn app.main:app --reload --port 8000
pause
