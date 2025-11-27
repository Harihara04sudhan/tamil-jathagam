# 📘 User Guide - Tamil Jathagam System

## Getting Started

### What You Need

1. **Birth Information:**
   - Date of birth (YYYY-MM-DD)
   - Time of birth (HH:MM in 24-hour format)
   - Place of birth
   - Coordinates (latitude and longitude)
   - Timezone

2. **How to Find Coordinates:**
   - Google Maps: Right-click location → See coordinates
   - Search online: "latitude longitude of [city name]"
   - Use the table below for common Indian cities

### Common Indian City Coordinates

| City | Latitude | Longitude | Timezone |
|------|----------|-----------|----------|
| Chennai | 13.0827 | 80.2707 | Asia/Kolkata |
| Mumbai | 19.0760 | 72.8777 | Asia/Kolkata |
| Delhi | 28.7041 | 77.1025 | Asia/Kolkata |
| Bangalore | 12.9716 | 77.5946 | Asia/Kolkata |
| Kolkata | 22.5726 | 88.3639 | Asia/Kolkata |
| Hyderabad | 17.3850 | 78.4867 | Asia/Kolkata |
| Ahmedabad | 23.0225 | 72.5714 | Asia/Kolkata |
| Pune | 18.5204 | 73.8567 | Asia/Kolkata |
| Jaipur | 26.9124 | 75.7873 | Asia/Kolkata |
| Madurai | 9.9252 | 78.1198 | Asia/Kolkata |
| Coimbatore | 11.0168 | 76.9558 | Asia/Kolkata |
| Kochi | 9.9312 | 76.2673 | Asia/Kolkata |
| Trivandrum | 8.5241 | 76.9366 | Asia/Kolkata |
| Visakhapatnam | 17.6868 | 83.2185 | Asia/Kolkata |
| Nagpur | 21.1458 | 79.0882 | Asia/Kolkata |

## Step-by-Step Tutorial

### Step 1: Start the System

```fish
# Navigate to backend folder
cd /home/hari/Videos/artro/backend

# Start the server (choose one method):

# Method 1: Using fish script
./run.fish

# Method 2: Using bash script
bash run.sh

# Method 3: Direct command
python3 -m uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Step 2: Open the Frontend

1. **Option A: Direct file**
   - Navigate to `artro/frontend/`
   - Double-click `index.html`
   - Opens in your default browser

2. **Option B: Web server (recommended)**
   ```fish
   cd /home/hari/Videos/artro/frontend
   python3 -m http.server 8080
   ```
   - Visit: http://localhost:8080

### Step 3: Enter Birth Details

Fill in the form:

**Example 1: Chennai Birth**
```
Name: Ravi Kumar
Birth Date: 1990-05-15
Birth Time: 14:30
Birth Place: Chennai, Tamil Nadu
Latitude: 13.0827
Longitude: 80.2707
Timezone: Asia/Kolkata
```

**Example 2: Mumbai Birth**
```
Name: Priya Sharma
Birth Date: 1995-08-20
Birth Time: 08:15
Birth Place: Mumbai, Maharashtra
Latitude: 19.0760
Longitude: 72.8777
Timezone: Asia/Kolkata
```

**Example 3: USA Birth**
```
Name: John Smith
Birth Date: 1988-12-10
Birth Time: 18:45
Birth Place: New York, USA
Latitude: 40.7128
Longitude: -74.0060
Timezone: America/New_York
```

### Step 4: Generate Jathagam

1. Click "Calculate Jathagam" button
2. Wait 2-3 seconds for calculation
3. Results appear in tabs

## Understanding Your Results

### Tab 1: Birth Chart

**South Indian Style Chart**

The diamond-shaped chart shows:
- **H1** (top): Ascendant house - always here
- Each house: Contains planets in that sign
- **Asc**: Ascendant (Lagna)
- **Sun, Moon, Mar, Mer, Jup, Ven, Sat**: 7 planets
- **Rah, Ket**: North and South nodes

**How to Read:**
- Find your Ascendant (Asc) - usually in H1
- See which planets are in same house
- Planets in same house influence each other
- Empty houses are also significant

**Example Chart:**
```
        H12[Ket]         H1[Asc,Sun]        H2[Moon]
        
H11[Sat]                    •                  H3[Mar]
        
H10[Rah]                    •                  H4[Mer]
        
        H9[Jup]          H8[Ven]            H7[]
```

### Tab 2: Planetary Positions

**Table shows:**
- Planet name (English)
- Rasi (Sign) in English and Tamil
- Nakshatra (Star) with pada
- Exact degree position
- (R) = Retrograde motion

**Example:**
```
Sun    - Aries (மேஷம்)       | Ashwini (அசுவினி)     | 15.23°
Moon   - Cancer (கடகம்)      | Pushya (பூசம்)        | 8.45°
Mars   - Gemini (மிதுனம்)    | Mrigashira (மிருகசீரிடம்) | 22.67°
```

**What to Look For:**
- Your Moon sign (Rasi) - for daily horoscope
- Your Nakshatra - for Dasha calculation
- Exalted planets - extra strong
- Debilitated planets - challenging

### Tab 3: Predictions

**Six Categories:**

**1. Personality**
- Based on Ascendant, Sun, Moon
- Your nature, character, appearance
- Mental tendencies

**2. Career**
- 10th house analysis
- Suitable professions
- Success periods
- Saturn and Jupiter effects

**3. Relationships**
- 7th house for marriage
- Venus placement
- Spouse characteristics
- Compatibility factors

**4. Health**
- 6th house indicators
- Mars and Saturn placement
- Vulnerable areas
- Preventive care

**5. Wealth**
- 2nd and 11th houses
- Jupiter and Venus effects
- Income sources
- Financial prosperity

**6. Current Period**
- Active Mahadasha
- Duration and effects
- Opportunities now
- Challenges to face

**Example Prediction:**
```
Personality - Ascendant:
"Your rising sign is Leo (சிம்மம்), ruled by Sun.
This shapes your outward personality and physical 
appearance. You have natural leadership qualities 
and commanding presence."
```

### Tab 4: Dasha Periods

**Vimshottari Dasha Timeline**

Shows:
- Planet ruling each period
- Tamil name (மகாதசை)
- Start and end dates
- Duration in years
- **CURRENT PERIOD** highlighted

**Example:**
```
Ketu Mahadasha (கேது மகாதசை)
7.0 years
1990-05-15 to 1997-05-15

Venus Mahadasha (சுக்ரன் மகாதசை) [CURRENT]
20.0 years
1997-05-15 to 2017-05-15

Sun Mahadasha (சூரியன் மகாதசை)
6.0 years
2017-05-15 to 2023-05-15
```

**Understanding Dasha:**
- Your life is divided into planetary periods
- Each planet rules for specific years
- Current Dasha affects your life now
- Plan important events during favorable Dashas

**Planet Period Effects:**
- **Ketu (7 years)**: Spirituality, detachment
- **Venus (20 years)**: Love, luxury, arts
- **Sun (6 years)**: Authority, recognition
- **Moon (10 years)**: Emotions, travel
- **Mars (7 years)**: Action, courage
- **Rahu (18 years)**: Ambition, foreign
- **Jupiter (16 years)**: Wisdom, expansion
- **Saturn (19 years)**: Discipline, karma
- **Mercury (17 years)**: Intelligence, business

### Tab 5: Yogas & Doshas

**Left Side: Yogas (Good)**

Green cards showing beneficial combinations:

**Example:**
```
Gaja Kesari Yoga
Type: Raja Yoga
Jupiter in Kendra from Moon - brings wisdom, 
prosperity and good character
Strength: Excellent
```

**Common Yogas:**
- **Raja Yoga**: Power and status
- **Gaja Kesari**: Wisdom and prosperity
- **Benefics in Kendra**: General success
- **Planet in own sign**: Strength

**Right Side: Doshas (Challenges)**

Red cards showing afflictions:

**Example:**
```
Mangal Dosha (Kuja Dosha)
Severity: Medium
Mars in house 7 - may affect marriage and 
relationships. Remedies: worship Lord Hanuman, 
recite Hanuman Chalisa
```

**Common Doshas:**
- **Mangal Dosha**: Marriage challenges
- **Kala Sarpa Dosha**: Obstacles in life
- **Pitra Dosha**: Ancestral karma

**Important:** Doshas are not curses! They are:
- Areas needing attention
- Karmic lessons
- Growth opportunities
- Can be remedied

## Advanced Features

### Compatibility Check

For marriage matching:

1. Generate birth chart for Person 1
2. Note down their birth details
3. Use API endpoint `/api/compatibility`
4. Or generate separately and compare:
   - Moon signs (Rasi)
   - Nakshatras
   - Mangal Dosha status
   - Current Dashas

**Good Match Indicators:**
- Compatible Moon signs
- Harmonious Nakshatras
- Both have or both don't have Mangal Dosha
- Guna Milan score > 24/36
- Complementary Dashas

### Current Transits

Check today's planetary positions:

Visit: `http://localhost:8000/api/transit`

Shows:
- Where each planet is TODAY
- Current zodiac signs
- Nakshatra transits
- Useful for daily predictions

**Use for:**
- Planning important events
- Understanding current influences
- Muhurta (auspicious timing)
- Daily horoscope context

## Remedies Guide

### For Doshas:

**Mangal Dosha (Mars):**
- Chant: Hanuman Chalisa
- Fast: Tuesdays
- Donate: Red items, jaggery
- Visit: Hanuman temples
- Wear: Red coral (consult astrologer)

**Kala Sarpa Dosha (Rahu-Ketu):**
- Chant: Maha Mrityunjaya Mantra
- Visit: Rahu-Ketu temples (Kalahasti, etc.)
- Perform: Naga Puja
- Offer: Milk to Shiva lingam
- Worship: Lord Shiva

**Pitra Dosha (Ancestral):**
- Perform: Shraddha ceremonies
- Offer: Tarpana (water offerings)
- Feed: Brahmins on Amavasya
- Donate: In ancestors' names
- Visit: Holy pilgrimage sites

### General Strengthening:

**For Weak Planets:**
- Chant respective mantras
- Worship deity of planet
- Wear gemstone (after consultation)
- Donate items related to planet
- Perform specific pujas

**Gemstones by Planet:**
- Sun: Ruby
- Moon: Pearl
- Mars: Red Coral
- Mercury: Emerald
- Jupiter: Yellow Sapphire
- Venus: Diamond/White Sapphire
- Saturn: Blue Sapphire
- Rahu: Hessonite
- Ketu: Cat's Eye

**⚠️ Important:** Always consult a qualified astrologer before wearing gemstones!

## Common Questions

### Q: How accurate are the calculations?
A: Astronomical positions are NASA/JPL quality (very accurate). Astrological interpretations follow traditional Vedic principles.

### Q: Why is my chart different from other websites?
A: Different ayanamsa, house systems, or calculation methods. We use Lahiri ayanamsa (most common in India).

### Q: Can I change my destiny?
A: Astrology shows tendencies, not fixed destiny. Free will and karma both matter. Use insights for growth.

### Q: What if I don't know exact birth time?
A: Exact time is crucial for Ascendant and houses. If unknown, try birth time rectification with an astrologer.

### Q: Is Mangal Dosha serious?
A: It's common (40% of people have it). Not a curse. Manageable with awareness and remedies.

### Q: How often should I check my chart?
A: Birth chart doesn't change. Check transits daily/weekly for current influences.

## API Usage Examples

### Using curl:

**Get Birth Chart:**
```bash
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

**Get Predictions:**
```bash
curl -X POST http://localhost:8000/api/predictions \
  -H "Content-Type: application/json" \
  -d '{
    "date": "1990-05-15",
    "time": "14:30",
    "latitude": 13.0827,
    "longitude": 80.2707,
    "timezone": "Asia/Kolkata"
  }'
```

**Get Current Transits:**
```bash
curl http://localhost:8000/api/transit
```

### Using Python:

```python
import requests

# Birth details
data = {
    "date": "1990-05-15",
    "time": "14:30",
    "latitude": 13.0827,
    "longitude": 80.2707,
    "timezone": "Asia/Kolkata",
    "name": "Ravi Kumar"
}

# Get birth chart
response = requests.post(
    "http://localhost:8000/api/birth-chart",
    json=data
)

chart = response.json()
print(f"Ascendant: {chart['ascendant']['rasi_name']['en']}")
print(f"Moon Sign: {chart['planetary_positions']['Moon']['rasi_name']['en']}")
```

## Tips for Best Results

### DO:
✅ Use accurate birth time (from birth certificate)
✅ Verify coordinates for birth place
✅ Select correct timezone
✅ Read all prediction categories
✅ Consider remedies for doshas
✅ Use for self-improvement
✅ Consult professional for serious matters

### DON'T:
❌ Make major decisions based solely on astrology
❌ Use wrong birth time
❌ Worry excessively about doshas
❌ Ignore free will and effort
❌ Use for superstitious purposes
❌ Spread fear about predictions

## Troubleshooting

### Issue: Chart not loading
- Check if backend is running (port 8000)
- Verify birth details are complete
- Check browser console for errors
- Try refreshing page

### Issue: Wrong coordinates
- Double-check latitude/longitude
- Use decimal format (not degrees/minutes)
- Negative values for West and South

### Issue: Unexpected predictions
- Verify birth time is accurate
- Check timezone selection
- Different time = different Ascendant
- Consider birth time rectification

## Next Steps

After understanding your chart:

1. **Study Your Dasha**
   - Which planet rules now?
   - How many years remaining?
   - What to expect?

2. **Check Transits**
   - How are planets moving?
   - When do they affect your chart?
   - Plan accordingly

3. **Apply Remedies**
   - For any doshas found
   - Strengthen weak planets
   - Regular spiritual practice

4. **Consult Professional**
   - For specific questions
   - Marriage timing
   - Career decisions
   - Health concerns

5. **Learn More**
   - Read Vedic astrology books
   - Understand planetary effects
   - Study your Dasha periods
   - Follow traditional texts

## Resources

### Books:
- Brihat Parashara Hora Shastra
- Jataka Parijata
- Phaladeepika
- Light on Life (Hart deFouw)
- The Art and Science of Vedic Astrology

### Websites:
- astrology.com
- vedic astrology research portal
- saptarishisastrology.com

### Learn Tamil Terms:
- ஜாதகம் (Jathagam) - Birth chart
- லக்னம் (Lagna) - Ascendant
- ராசி (Rasi) - Zodiac sign
- நட்சத்திரம் (Natchathiram) - Nakshatra
- தசை (Dasai) - Period
- யோகம் (Yogam) - Combination
- தோஷம் (Dosham) - Affliction

---

**Happy Exploring!**

May the stars guide you on your journey! 🌟

வாழ்க வளமுடன் 🙏 (Live Prosperously!)
