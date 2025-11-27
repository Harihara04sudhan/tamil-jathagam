#!/bin/bash

echo "🌟 Starting Tamil Jathagam - Vedic Astrology API 🌟"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Download ephemeris data if not present
if [ ! -f "de421.bsp" ]; then
    echo "Downloading NASA/JPL ephemeris data (first time only)..."
    python -c "from skyfield.api import load; load('de421.bsp')"
fi

echo ""
echo "✨ Starting FastAPI server..."
echo "API Documentation: http://localhost:8000/docs"
echo "API Endpoint: http://localhost:8000"
echo ""

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
