# 🌟 Tamil Jathagam - Comprehensive Vedic Astrology System

A complete Vedic astrology system with Tamil support for birth chart generation (Jathagam), horoscope predictions, and astrological analysis.

## ✨ Features

### Complete Vedic Astrology Calculations
- **9 Grahas (Planets)**: Sun (சூரியன்), Moon (சந்திரன்), Mars (செவ்வாய்), Mercury (புதன்), Jupiter (குரு), Venus (சுக்ரன்), Saturn (சனி), Rahu (ராகு), Ketu (கேது)
- **27 Nakshatras**: Complete lunar mansion calculations with pada divisions
- **12 Rasis (Zodiac Signs)**: Sidereal zodiac with Lahiri Ayanamsa
- **12 Bhavas (Houses)**: House cusps and significations
- **Ascendant (Lagna)**: Rising sign calculation
- **Vimshottari Dasha**: 120-year planetary period system
- **Yogas**: Beneficial planetary combinations (Raja Yoga, Gaja Kesari Yoga, etc.)
- **Doshas**: Afflictions (Mangal Dosha, Kala Sarpa Dosha, Pitra Dosha)

### Horoscope Predictions
- **Personality Analysis**: Based on Ascendant, Sun, and Moon placements
- **Career Predictions**: 10th house analysis with planetary influences
- **Relationship Insights**: 7th house and Venus analysis
- **Health Indicators**: 6th house and malefic planets
- **Wealth Prospects**: 2nd and 11th house analysis
- **Current Period Effects**: Dasha-based predictions

### Tamil Language Support
- Tamil names for all planets (grahas)
- Tamil names for all zodiac signs (rasis)
- Tamil names for all nakshatras
- Bilingual interface (English & Tamil)

### Visualizations
- **South Indian Style Chart**: Traditional diamond-shaped chart
- **Planetary Position Tables**: Detailed degree and nakshatra information
- **Dasha Timeline**: Visual representation of planetary periods
- **Yoga & Dosha Display**: Highlighted beneficial and challenging combinations

### API Endpoints
- `/api/birth-chart` - Complete birth chart calculation
- `/api/predictions` - Detailed horoscope predictions
- `/api/dasha-periods` - Vimshottari Dasha timeline
- `/api/compatibility` - Compatibility analysis between two people
- `/api/transit` - Current planetary transits
- `/api/nakshatras` - Information about all 27 nakshatras
- `/api/zodiac-signs` - Information about 12 zodiac signs

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone or download this repository**
```bash
cd artro
```

2. **Set up Python virtual environment (recommended)**
```bash
cd backend
python -m venv venv

# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **Download astronomical data (first time only)**
```bash
python -c "from skyfield.api import load; load('de421.bsp')"
```

### Running the Application

1. **Start the backend server**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

2. **Open the frontend**
```bash
cd ../frontend
# Open index.html in your web browser
# Or use a simple HTTP server:
python -m http.server 8080
```

Then visit: `http://localhost:8080`

## 📖 Usage Guide

### Generating a Birth Chart

1. Enter the following birth details:
   - **Name**: Person's name (optional)
   - **Birth Date**: YYYY-MM-DD format
   - **Birth Time**: 24-hour format (HH:MM)
   - **Birth Place**: Location name (optional)
   - **Latitude**: Decimal degrees (-90 to 90)
   - **Longitude**: Decimal degrees (-180 to 180)
   - **Timezone**: Select from dropdown

2. Click "Calculate Jathagam"

3. View results in different tabs:
   - **Birth Chart**: South Indian style chart visualization
   - **Planetary Positions**: Detailed positions with nakshatras
   - **Predictions**: Comprehensive horoscope predictions
   - **Dasha Periods**: Current and future planetary periods
   - **Yogas & Doshas**: Special combinations and afflictions

### Example Birth Details

**Chennai, Tamil Nadu**
- Date: 1990-05-15
- Time: 14:30
- Latitude: 13.0827
- Longitude: 80.2707
- Timezone: Asia/Kolkata

**New York, USA**
- Date: 1995-08-20
- Time: 08:15
- Latitude: 40.7128
- Longitude: -74.0060
- Timezone: America/New_York

## 🔧 Technical Details

### Astronomical Calculations

- **Ephemeris**: JPL DE421 planetary ephemeris (high precision)
- **Ayanamsa**: Lahiri (Chitrapaksha) - most commonly used in Indian astrology
- **Coordinate System**: Geocentric sidereal zodiac
- **Time System**: UTC with timezone conversion
- **Library**: Skyfield (NASA/JPL quality astronomical calculations)

### Astrological System

- **Tradition**: Vedic (Jyotish) astrology
- **House System**: Equal house (Whole Sign)
- **Dasha System**: Vimshottari (120-year cycle)
- **Nakshatra Division**: 27 lunar mansions, 4 padas each
- **Regional Style**: South Indian chart format

### API Architecture

- **Framework**: FastAPI (Python)
- **Data Validation**: Pydantic models
- **CORS**: Enabled for frontend integration
- **Error Handling**: Comprehensive error messages
- **Documentation**: Auto-generated OpenAPI/Swagger docs

### Frontend Technology

- **Framework**: React 18 (via CDN)
- **Styling**: Custom CSS with responsive design
- **State Management**: React Hooks
- **Chart Rendering**: Pure CSS with transforms

## 🧪 Testing

Run comprehensive test suite:

```bash
cd backend
pytest tests/test_astrology.py -v
```

Test coverage includes:
- Planetary position calculations
- Nakshatra and rasi calculations
- Ascendant computation
- House calculations
- Dasha period generation
- Yoga and dosha detection
- Complete birth chart generation
- Edge cases and boundary conditions

## 📚 Understanding Your Jathagam

### Key Components

**Ascendant (Lagna - லக்னம்)**
- Rising sign at birth time
- Represents physical appearance and personality
- Starting point of the 12 houses

**Moon Sign (Rasi - ராசி)**
- Zodiac sign containing the Moon
- Represents mind, emotions, and mother
- Used for daily predictions

**Nakshatra (நட்சத்திரம்)**
- Lunar mansion (27 divisions)
- Each divided into 4 padas
- Determines Vimshottari Dasha starting point

**Houses (Bhavas - பாவங்கள்)**
1. Self, personality, physical body
2. Wealth, family, speech
3. Siblings, courage, communication
4. Mother, home, emotions
5. Children, education, creativity
6. Enemies, disease, service
7. Marriage, partnerships
8. Longevity, transformation
9. Father, religion, fortune
10. Career, status, authority
11. Gains, friends, aspirations
12. Loss, liberation, foreign lands

**Planetary Periods (Dasha - தசை)**
- Vimshottari: 120-year cycle
- Each planet rules for specific years
- Sub-periods (Antardasha) for detailed timing
- Current dasha influences life events

### Yogas (Beneficial Combinations)

**Raja Yoga (ராஜ யோகம்)**
- Combination for power and status
- Formed by lords of kendras and trikonas

**Gaja Kesari Yoga (கஜகேசரி யோகம்)**
- Jupiter in kendra from Moon
- Brings wisdom, prosperity, good character

**Pancha Mahapurusha Yogas**
- Five combinations for greatness
- Each planet in specific positions

### Doshas (Challenges)

**Mangal Dosha / Kuja Dosha (குஜ தோஷம்)**
- Mars in houses 1,2,4,7,8,12 from Lagna
- Affects marriage and relationships
- Remedies: Hanuman worship, charity

**Kala Sarpa Dosha (காலசர்ப தோஷம்)**
- All planets between Rahu and Ketu
- Creates obstacles and delays
- Remedies: Rahu-Ketu temple worship, Shiva puja

**Pitra Dosha (பித்ரு தோஷம்)**
- Sun with Rahu or Ketu
- Ancestral karmic issues
- Remedies: Shraddha, charity, tarpana

## 🎯 Advanced Features

### Compatibility Analysis

Check marriage compatibility between two people:

```bash
POST /api/compatibility
```

Analyzes:
- Rasi (moon sign) compatibility
- Nakshatra matching
- Guna Milan (36-point system)
- Mangal Dosha cancellation
- Dasha period harmony

### Current Transits

Get current planetary positions:

```bash
GET /api/transit
```

Useful for:
- Daily predictions
- Timing important events
- Understanding current influences

## 🌍 Location Coordinates

Common Indian cities:

| City | Latitude | Longitude |
|------|----------|-----------|
| Chennai | 13.0827 | 80.2707 |
| Mumbai | 19.0760 | 72.8777 |
| Delhi | 28.7041 | 77.1025 |
| Bangalore | 12.9716 | 77.5946 |
| Kolkata | 22.5726 | 88.3639 |
| Hyderabad | 17.3850 | 78.4867 |
| Madurai | 9.9252 | 78.1198 |
| Coimbatore | 11.0168 | 76.9558 |

## ⚠️ Important Notes

### Accuracy
- Astronomical calculations are highly accurate (NASA/JPL quality)
- Astrological interpretations follow traditional Vedic principles
- Predictions are general guidelines, not deterministic

### Limitations
- Rahu/Ketu positions use simplified mean node calculation
- House system uses equal houses (not advanced systems like Placidus)
- Predictions are based on birth chart only (not transits or progressions)
- Divisional charts (Varga charts) not yet implemented

### Ethical Use
- Use for educational and personal insight purposes
- Don't make major life decisions based solely on astrology
- Consult professional astrologers for serious concerns
- Respect cultural and religious sensitivities

## 🔮 Future Enhancements

Planned features:
- [ ] Divisional charts (D9 Navamsa, D10 Dasamsa, etc.)
- [ ] Advanced strength calculations (Shadbala, Ashtakavarga)
- [ ] Planetary aspects and conjunctions
- [ ] Transit predictions
- [ ] Antardasha (sub-periods) calculations
- [ ] Muhurta (auspicious timing) selection
- [ ] Prashna (horary) astrology
- [ ] North Indian chart style
- [ ] Export to PDF
- [ ] Save and compare multiple charts
- [ ] Database for saved charts
- [ ] Advanced compatibility (Ashtakoot in detail)

## 🛠️ Development

### Project Structure
```
artro/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI application
│   │   └── astrology.py      # Core calculations
│   ├── tests/
│   │   └── test_astrology.py # Test suite
│   ├── requirements.txt      # Python dependencies
│   └── run.sh               # Startup script
├── frontend/
│   └── index.html           # React SPA
└── README.md                # This file
```

### Adding New Features

1. **Backend calculations**: Edit `backend/app/astrology.py`
2. **API endpoints**: Edit `backend/app/main.py`
3. **Frontend UI**: Edit `frontend/index.html`
4. **Tests**: Add to `backend/tests/test_astrology.py`

### Contributing

Contributions welcome! Areas needing improvement:
- More accurate Rahu/Ketu calculations
- Additional yoga combinations
- More detailed predictions
- UI/UX enhancements
- Tamil translations
- Documentation improvements

## 📄 License

This project is for educational purposes. Feel free to use and modify.

## 🙏 Credits

- **Astronomical Calculations**: Skyfield library by Brandon Rhodes
- **Ephemeris Data**: NASA/JPL DE421
- **Astrological Knowledge**: Traditional Vedic astrology texts
- **Tamil Translations**: Native speakers and classical texts

## 📞 Support

For issues, questions, or suggestions:
- Check the API documentation at `/docs`
- Review test cases for usage examples
- Consult traditional Vedic astrology texts

## 🌟 Example Output

A complete birth chart includes:

```json
{
  "ascendant": {
    "rasi": 5,
    "rasi_name": {"en": "Leo", "ta": "சிம்மம்"},
    "nakshatra": "Magha",
    "lord": "Sun"
  },
  "planetary_positions": {
    "Sun": {
      "rasi": 1,
      "nakshatra": "Ashwini",
      "pada": 2,
      "degrees_in_rasi": 15.23
    }
    // ... 8 more planets
  },
  "vimshottari_dasha": [
    {
      "planet": "Ketu",
      "start_date": "1990-05-15",
      "end_date": "1993-12-15",
      "years": 3.58
    }
    // ... 8 more periods
  ],
  "yogas": [...],
  "doshas": [...],
  "predictions": {
    "personality": [...],
    "career": [...],
    "relationships": [...],
    "health": [...],
    "wealth": [...]
  }
}
```

---

**Made with ❤️ for Vedic Astrology enthusiasts**

வாழ்க வளமுடன் 🙏 (Live Prosperously!)
