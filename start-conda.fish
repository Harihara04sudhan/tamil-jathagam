#!/usr/bin/env fish

# Tamil Jathagam System - Conda-based Startup Script
# This uses your existing conda environment

set SCRIPT_DIR (dirname (realpath (status --current-filename)))
set BACKEND_DIR "$SCRIPT_DIR/backend"
set FRONTEND_DIR "$SCRIPT_DIR/frontend"

echo "🌟 Starting Tamil Jathagam System (Conda Version)..."
echo ""

# Check if we're in the right directory
if not test -d "$BACKEND_DIR"
    echo "❌ Error: Backend directory not found!"
    exit 1
end

if not test -d "$FRONTEND_DIR"
    echo "❌ Error: Frontend directory not found!"
    exit 1
end

# Change to backend directory
cd "$BACKEND_DIR"

# Check if conda is available
if not type -q conda
    echo "❌ Conda not found!"
    echo "💡 Please use ./start.fish instead or activate conda manually"
    exit 1
end

echo "📦 Using conda base environment..."

# Find conda's Python
set CONDA_PYTHON "$HOME/anaconda3/bin/python"
if not test -f "$CONDA_PYTHON"
    echo "❌ Conda Python not found at $CONDA_PYTHON"
    echo "💡 Please check your conda installation path"
    exit 1
end

echo "   Using: $CONDA_PYTHON"
echo "📥 Installing dependencies if needed..."
$CONDA_PYTHON -m pip install -q -r requirements.txt

if test $status -ne 0
    echo "❌ Failed to install dependencies"
    exit 1
end

echo "✓ Dependencies ready"
echo ""

echo "🔮 Starting Backend API Server..."
echo "   Backend will run at: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo ""

# Start backend in background using conda python
$CONDA_PYTHON -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/jathagam_backend.log 2>&1 &
set BACKEND_PID $last_pid

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if not kill -0 $BACKEND_PID 2>/dev/null
    echo "❌ Backend failed to start. Check /tmp/jathagam_backend.log for errors:"
    tail -n 20 /tmp/jathagam_backend.log
    exit 1
end

echo "✓ Backend started successfully (PID: $BACKEND_PID)"
echo ""

# Start frontend server
cd "$FRONTEND_DIR"
echo "🎨 Starting Frontend Server..."
echo "   Frontend will run at: http://localhost:8080"
echo ""

# Start frontend in background - use conda python
$CONDA_PYTHON -m http.server 8080 > /tmp/jathagam_frontend.log 2>&1 &
set FRONTEND_PID $last_pid

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
if command -v xdg-open > /dev/null
    echo "🌐 Opening browser..."
    xdg-open http://localhost:8080 2>/dev/null &
else if command -v firefox > /dev/null
    firefox http://localhost:8080 2>/dev/null &
else if command -v google-chrome > /dev/null
    google-chrome http://localhost:8080 2>/dev/null &
end

# Keep script running and wait for Ctrl+C
function cleanup
    echo ""
    echo "🛑 Shutting down Tamil Jathagam System..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✓ All servers stopped"
    exit 0
end

trap cleanup SIGINT SIGTERM

echo "✨ System running... Press Ctrl+C to stop"
echo ""

# Wait for user interrupt
while true
    sleep 1
end
