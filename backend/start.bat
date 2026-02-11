@echo off
REM Quick start script for Phase III AI Chatbot Backend

echo ========================================
echo Phase III AI Chatbot - Backend Server
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and configure your settings.
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist .venv (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv .venv
    echo.
    pause
    exit /b 1
)

echo Starting backend server...
echo Backend will be available at: http://localhost:8000
echo API documentation: http://localhost:8000/docs
echo.

REM Activate virtual environment and start server
call .venv\Scripts\activate.bat
uvicorn src.main:app --reload --port 8000
