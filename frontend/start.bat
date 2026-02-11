@echo off
REM Quick start script for Phase III AI Chatbot Frontend

echo ========================================
echo Phase III AI Chatbot - Frontend Server
echo ========================================
echo.

REM Check if .env.local exists
if not exist .env.local (
    echo ERROR: .env.local file not found!
    echo Please create .env.local with your configuration.
    echo.
    pause
    exit /b 1
)

REM Check if node_modules exists
if not exist node_modules (
    echo ERROR: Dependencies not installed!
    echo Please run: npm install
    echo.
    pause
    exit /b 1
)

echo Starting frontend server...
echo Frontend will be available at: http://localhost:3000
echo.

npm run dev
