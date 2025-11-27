# 🚀 Quick Setup Guide - Tamil Jathagam System

## Complete Installation Steps

### Method 1: Using fish shell (Your current shell)

```fish
# Navigate to project
cd /home/hari/Videos/artro/backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment (fish)
source venv/bin/activate.fish

# Install dependencies
pip install -r requirements.txt

# Download ephemeris data (first time only)
python -c "from skyfield.api import load; load('de421.bsp')"

# Run quick test
python test_quick.py

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Method 2: Using bash script

```fish
cd /home/hari/Videos/artro/backend

# Make script executable
chmod +x run.sh

# Run the script (it will create venv and install everything)
bash run.sh
```

### Method 3: Manual step-by-step

1. **Install Python packages**
```fish
cd /home/hari/Videos/artro/backend
pip install --user fastapi uvicorn pydantic python-dateutil pytz skyfield numpy pytest httpx
```

2. **Download astronomical data**
```fish
python3 -c "from skyfield.api import load; load('de421.bsp')"
```

3. **Test the system**
```fish
python3 test_quick.py
```

4. **Start the API server**
```fish
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. **Open the frontend**
```fish
cd ../frontend
# Option A: Just open index.html in browser
open index.html  # or double-click in file manager

# Option B: Use a web server
python3 -m http.server 8080
# Then visit: http://localhost:8080
```

## Verify Installation

### Test 1: Check Python packages
```fish
python3 -c "import fastapi, uvicorn, skyfield, pydantic; print('✓ All packages installed')"
```

### Test 2: Run quick test
```fish
cd /home/hari/Videos/artro/backend
python3 test_quick.py
```

### Test 3: Check API
```fish
# Start server in one terminal
cd /home/hari/Videos/artro/backend
python3 -m uvicorn app.main:app --reload

# In another terminal, test the API
curl http://localhost:8000/health
```

## Access Points

Once running:

- **API Documentation**: http://localhost:8000/docs
- **API Endpoint**: http://localhost:8000
- **Frontend**: Open `frontend/index.html` in browser
- **Health Check**: http://localhost:8000/health

## Quick Test API Call

```fish
# Test birth chart calculation
curl -X POST http://localhost:8000/api/birth-chart \
  -H "Content-Type: application/json" \
  -d '{
    "date": "1990-05-15",
    "time": "14:30",
    "latitude": 13.0827,
    "longitude": 80.2707,
    "timezone": "Asia/Kolkata",
    "name": "Test User"
  }'
```

## Troubleshooting

### Issue: "Module not found"
```fish
# Solution: Use virtual environment
python3 -m venv venv
source venv/bin/activate.fish  # for fish shell
pip install -r requirements.txt
```

### Issue: "Cannot connect to API"
```fish
# Check if server is running
curl http://localhost:8000/health

# Check what's using port 8000
lsof -i :8000

# Use different port if needed
uvicorn app.main:app --reload --port 8001
```

### Issue: "CORS error in browser"
The API has CORS enabled. If you still face issues:
1. Use a local web server for frontend (python -m http.server)
2. Or install a CORS browser extension

### Issue: "Ephemeris file not found"
```fish
cd /home/hari/Videos/artro/backend
python3 -c "from skyfield.api import load; load('de421.bsp')"
```

## Development Mode

For development with auto-reload:

```fish
# Terminal 1: Backend with auto-reload
cd /home/hari/Videos/artro/backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend web server
cd /home/hari/Videos/artro/frontend
python3 -m http.server 8080
```

## Production Deployment

For production use:

```fish
# Install production server
pip install gunicorn

# Run with gunicorn
cd /home/hari/Videos/artro/backend
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Running Tests

```fish
cd /home/hari/Videos/artro/backend

# Run all tests
pytest tests/test_astrology.py -v

# Run specific test
pytest tests/test_astrology.py::TestVedicAstrology::test_planetary_positions -v

# Run with coverage
pytest tests/test_astrology.py --cov=app --cov-report=html
```

## File Structure

```
artro/
├── README.md                 # Complete documentation
├── SETUP.md                  # This file
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI endpoints
│   │   └── astrology.py     # Core calculations
│   ├── tests/
│   │   └── test_astrology.py # Test suite
│   ├── requirements.txt     # Python dependencies
│   ├── run.sh              # Startup script
│   ├── test_quick.py       # Quick verification
│   └── de421.bsp           # Ephemeris data (auto-downloaded)
└── frontend/
    └── index.html          # React SPA
```

## Features Overview

✅ **Complete Vedic Astrology**
- 9 Grahas (including Rahu & Ketu)
- 27 Nakshatras with padas
- 12 Rasis (Sidereal zodiac)
- Ascendant calculation
- Vimshottari Dasha
- Yogas & Doshas

✅ **Tamil Support**
- Tamil names for all elements
- Bilingual interface

✅ **Rich Predictions**
- Personality analysis
- Career guidance
- Relationship insights
- Health indicators
- Wealth prospects

✅ **Modern Interface**
- South Indian chart visualization
- Responsive design
- Real-time calculations
- REST API

## Next Steps

After installation:

1. Generate your birth chart
2. Explore different API endpoints
3. Try compatibility analysis
4. Check current transits
5. Read the comprehensive README.md

## Support

- Check API docs: http://localhost:8000/docs
- Run quick test: `python3 test_quick.py`
- Review examples in README.md

---

**Made with ❤️ for Vedic Astrology**

வாழ்க வளமுடன் 🙏
