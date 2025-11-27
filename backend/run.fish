#!/usr/bin/env fish

# Tamil Jathagam - Fish Shell Startup Script

echo "🌟 Tamil Jathagam - Vedic Astrology System 🌟"
echo ""

set backend_dir (dirname (status --current-filename))

# Check if virtual environment exists
if not test -d "$backend_dir/venv"
    echo "Creating virtual environment..."
    python3 -m venv "$backend_dir/venv"
end

# Activate virtual environment
echo "Activating virtual environment..."
source "$backend_dir/venv/bin/activate.fish"

# Install requirements
echo "Installing dependencies..."
pip install -q -r "$backend_dir/requirements.txt"

# Download ephemeris data if not present
if not test -f "$backend_dir/de421.bsp"
    echo "Downloading NASA/JPL ephemeris data..."
    python -c "from skyfield.api import load; load('de421.bsp')"
end

echo ""
echo "✨ Starting FastAPI server..."
echo "API Documentation: http://localhost:8000/docs"
echo "API Endpoint: http://localhost:8000"
echo "Frontend: Open frontend/index.html in browser"
echo ""

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
