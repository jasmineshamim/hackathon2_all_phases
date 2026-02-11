#!/bin/bash
echo "Starting FastAPI Backend Server on Port 8001..."
echo ""
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8001
