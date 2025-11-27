#!/bin/bash

# Tamil Jathagam System - Single Command Startup Script
# This script starts both backend and frontend automatically

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

echo "🌟 Starting Tamil Jathagam System..."
echo ""

# Check if we're in the right directory
if [ ! -d "$BACKEND_DIR" ]; then
    echo "❌ Error: Backend directory not found!"
    exit 1
fi

if [ ! -d "$FRONTEND_DIR" ]; then
    echo "❌ Error: Frontend directory not found!"
    exit 1
fi

# Change to backend directory
cd "$BACKEND_DIR"

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "✓ Using existing virtual environment"
    source venv/bin/activate
else
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo "📥 Installing dependencies..."
    pip install -q --upgrade pip setuptools wheel
    echo "   Installing packages (this may take a minute)..."
    pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        echo "💡 Try using conda environment instead:"
        echo "   conda create -n jathagam python=3.11 -y"
        echo "   conda activate jathagam"
        echo "   pip install -r requirements.txt"
        exit 1
    fi
    
    echo "✓ Dependencies installed"
fi

echo ""
echo "🔮 Starting Backend API Server..."
echo "   Backend will run at: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo ""

# Start backend in background
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/jathagam_backend.log 2>&1 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Backend failed to start. Check /tmp/jathagam_backend.log for errors"
    exit 1
fi

echo "✓ Backend started successfully (PID: $BACKEND_PID)"
echo ""

# Start frontend server
cd "$FRONTEND_DIR"
echo "🎨 Starting Frontend Server..."
echo "   Frontend will run at: http://localhost:8080"
echo ""

# Start frontend in background
python3 -m http.server 8080 > /tmp/jathagam_frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait a moment for frontend to start
sleep 1

echo "✓ Frontend started successfully (PID: $FRONTEND_PID)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Tamil Jathagam System is Ready!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 Open your browser and go to:"
echo "   → http://localhost:8080"
echo ""
echo "📚 API Documentation available at:"
echo "   → http://localhost:8000/docs"
echo ""
echo "🛑 To stop the servers, press Ctrl+C or run:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "📋 Process IDs:"
echo "   Backend PID: $BACKEND_PID"
echo "   Frontend PID: $FRONTEND_PID"
echo ""
echo "வாழ்க வளமுடன் 🙏"
echo ""

# Try to open browser automatically
sleep 1
if command -v xdg-open &> /dev/null; then
    echo "🌐 Opening browser..."
    xdg-open http://localhost:8080 2>/dev/null &
elif command -v firefox &> /dev/null; then
    firefox http://localhost:8080 2>/dev/null &
elif command -v google-chrome &> /dev/null; then
    google-chrome http://localhost:8080 2>/dev/null &
fi

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Shutting down Tamil Jathagam System..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✓ All servers stopped"
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM

echo "✨ System running... Press Ctrl+C to stop"
echo ""

# Wait for user interrupt
while true; do
    sleep 1
done
