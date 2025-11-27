"""
FastAPI Backend for Vedic Astrology System
Tamil Jathagam with Horoscope Predictions
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, Dict, List
import logging

from app.astrology import get_astrology_engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Vedic Astrology API",
    description="Complete Tamil Jathagam system with horoscope predictions",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class BirthDetails(BaseModel):
    """Birth details for chart calculation"""
    date: str = Field(..., description="Birth date in YYYY-MM-DD format", example="1990-05-15")
    time: str = Field(..., description="Birth time in HH:MM format (24-hour)", example="14:30")
    latitude: float = Field(..., description="Birth place latitude", example=13.0827, ge=-90, le=90)
    longitude: float = Field(..., description="Birth place longitude", example=80.2707, ge=-180, le=180)
    timezone: str = Field(default="Asia/Kolkata", description="Timezone", example="Asia/Kolkata")
    name: Optional[str] = Field(None, description="Person's name")
    place: Optional[str] = Field(None, description="Birth place name")
    
    @validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
    
    @validator('time')
    def validate_time(cls, v):
        try:
            datetime.strptime(v, '%H:%M')
            return v
        except ValueError:
            raise ValueError('Time must be in HH:MM format (24-hour)')


class CompatibilityRequest(BaseModel):
    """Request for compatibility check between two people"""
    person1: BirthDetails
    person2: BirthDetails


# Initialize astrology engine
astrology = get_astrology_engine()


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Vedic Astrology API - Tamil Jathagam System",
        "version": "1.0.0",
        "endpoints": {
            "birth_chart": "/api/birth-chart",
            "predictions": "/api/predictions",
            "dasha_periods": "/api/dasha-periods",
            "compatibility": "/api/compatibility",
            "current_transit": "/api/transit",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "vedic-astrology-api"}


@app.post("/api/birth-chart")
async def calculate_birth_chart(details: BirthDetails):
    """
    Calculate complete birth chart (Jathagam)
    
    Returns:
    - Planetary positions (9 grahas)
    - Ascendant (Lagna)
    - 12 Houses (Bhavas)
    - Nakshatras and Padas
    - Vimshottari Dasha periods
    - Yogas and Doshas
    - Detailed predictions
    """
    try:
        # Parse datetime
        dt_str = f"{details.date} {details.time}"
        birth_dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
        
        # Generate chart
        chart = astrology.generate_birth_chart(
            birth_dt,
            details.latitude,
            details.longitude,
            details.timezone
        )
        
        # Add person details
        chart['person'] = {
            'name': details.name,
            'place': details.place
        }
        
        logger.info(f"Birth chart calculated for {details.name or 'unknown'}")
        return chart
        
    except Exception as e:
        logger.error(f"Error calculating birth chart: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error calculating chart: {str(e)}")


@app.post("/api/predictions")
async def get_predictions(details: BirthDetails):
    """
    Get detailed horoscope predictions
    
    Returns predictions for:
    - Personality traits
    - Career and profession
    - Relationships and marriage
    - Health and wellness
    - Wealth and finances
    - Current planetary period effects
    """
    try:
        dt_str = f"{details.date} {details.time}"
        birth_dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
        
        chart = astrology.generate_birth_chart(
            birth_dt,
            details.latitude,
            details.longitude,
            details.timezone
        )
        
        return {
            'person': {
                'name': details.name,
                'birth_date': details.date,
                'birth_time': details.time
            },
            'predictions': chart['predictions'],
            'current_dasha': chart['vimshottari_dasha'][0] if chart['vimshottari_dasha'] else None,
            'yogas': chart['yogas'],
            'doshas': chart['doshas']
        }
        
    except Exception as e:
        logger.error(f"Error generating predictions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating predictions: {str(e)}")


@app.post("/api/dasha-periods")
async def get_dasha_periods(details: BirthDetails):
    """
    Get Vimshottari Dasha periods (planetary periods)
    
    Returns the 120-year cycle of Mahadasha periods showing:
    - Planet ruling each period
    - Start and end dates
    - Duration in years
    - Tamil names
    """
    try:
        dt_str = f"{details.date} {details.time}"
        birth_dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
        
        chart = astrology.generate_birth_chart(
            birth_dt,
            details.latitude,
            details.longitude,
            details.timezone
        )
        
        # Find current dasha
        now = datetime.now()
        current_dasha = None
        for dasha in chart['vimshottari_dasha']:
            end = datetime.strptime(dasha['end_date'], '%Y-%m-%d')
            if end > now:
                current_dasha = dasha
                break
        
        return {
            'person': {
                'name': details.name,
                'birth_date': details.date
            },
            'birth_nakshatra': chart['planetary_positions']['Moon']['nakshatra'],
            'birth_nakshatra_tamil': chart['planetary_positions']['Moon']['nakshatra_tamil'],
            'current_dasha': current_dasha,
            'all_dashas': chart['vimshottari_dasha']
        }
        
    except Exception as e:
        logger.error(f"Error calculating dasha periods: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error calculating dasha: {str(e)}")


@app.post("/api/compatibility")
async def check_compatibility(request: CompatibilityRequest):
    """
    Check compatibility between two people for marriage/partnership
    
    Analyzes:
    - Moon sign compatibility (Rasi match)
    - Nakshatra compatibility (Star match)
    - Guna Milan (Ashtakoot system - 36 points)
    - Mangal Dosha match
    - Dasha compatibility
    """
    try:
        # Calculate both charts
        dt1 = datetime.strptime(f"{request.person1.date} {request.person1.time}", '%Y-%m-%d %H:%M')
        chart1 = astrology.generate_birth_chart(
            dt1, request.person1.latitude, request.person1.longitude, request.person1.timezone
        )
        
        dt2 = datetime.strptime(f"{request.person2.date} {request.person2.time}", '%Y-%m-%d %H:%M')
        chart2 = astrology.generate_birth_chart(
            dt2, request.person2.latitude, request.person2.longitude, request.person2.timezone
        )
        
        # Calculate 10 Porutham (Tamil marriage compatibility)
        porutham_result = astrology.calculate_10_porutham(chart1, chart2)
        
        # Also calculate basic compatibility for reference
        basic_compatibility = calculate_compatibility_score(chart1, chart2)
        
        return {
            'person1': {
                'name': request.person1.name,
                'moon_sign': chart1['planetary_positions']['Moon']['rasi_name'],
                'nakshatra': chart1['planetary_positions']['Moon']['nakshatra'],
                'nakshatra_tamil': chart1['planetary_positions']['Moon']['nakshatra_tamil']
            },
            'person2': {
                'name': request.person2.name,
                'moon_sign': chart2['planetary_positions']['Moon']['rasi_name'],
                'nakshatra': chart2['planetary_positions']['Moon']['nakshatra'],
                'nakshatra_tamil': chart2['planetary_positions']['Moon']['nakshatra_tamil']
            },
            'porutham': porutham_result,
            'basic_compatibility': basic_compatibility
        }
        
    except Exception as e:
        logger.error(f"Error calculating compatibility: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error calculating compatibility: {str(e)}")


@app.get("/api/transit")
async def current_transit():
    """
    Get current planetary transits
    
    Returns current positions of all planets for transit predictions
    """
    try:
        now = datetime.now()
        
        # Calculate current positions
        positions = astrology.calculate_planetary_positions(now, 13.0827, 80.2707)  # Chennai as default
        
        return {
            'date': now.strftime('%Y-%m-%d'),
            'time': now.strftime('%H:%M:%S'),
            'planetary_positions': positions,
            'note': 'Current transit positions (geocentric, sidereal zodiac)'
        }
        
    except Exception as e:
        logger.error(f"Error calculating transit: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error calculating transit: {str(e)}")


@app.get("/api/nakshatras")
async def get_nakshatra_info():
    """Get information about all 27 nakshatras"""
    return {
        'count': 27,
        'nakshatras': astrology.NAKSHATRAS,
        'description': 'The 27 lunar mansions (nakshatras) used in Vedic astrology'
    }


@app.get("/api/zodiac-signs")
async def get_zodiac_signs():
    """Get information about 12 zodiac signs (Rasis)"""
    return {
        'count': 12,
        'signs': [
            {
                'number': k,
                'english': v['en'],
                'tamil': v['ta'],
                'lord': astrology.RASI_LORDS[k]
            }
            for k, v in astrology.RASI_NAMES.items()
        ]
    }


def calculate_compatibility_score(chart1: Dict, chart2: Dict) -> Dict:
    """Calculate compatibility score between two charts"""
    
    moon1 = chart1['planetary_positions']['Moon']['rasi']
    moon2 = chart2['planetary_positions']['Moon']['rasi']
    
    nak1 = chart1['planetary_positions']['Moon']['nakshatra']
    nak2 = chart2['planetary_positions']['Moon']['nakshatra']
    
    # Rasi compatibility (simplified)
    rasi_distance = abs(moon1 - moon2)
    if rasi_distance in [0, 6]:  # Same or opposite
        rasi_score = 0
    elif rasi_distance in [1, 11]:  # Adjacent
        rasi_score = 3
    elif rasi_distance in [2, 10]:
        rasi_score = 4
    elif rasi_distance in [3, 9]:
        rasi_score = 5
    elif rasi_distance in [4, 8]:
        rasi_score = 6
    else:  # 5 or 7
        rasi_score = 7
    
    # Nakshatra compatibility (simplified - real system is more complex)
    nakshatra_score = 15  # Base score
    
    # Gana compatibility
    gana_score = 6
    
    # Total score out of 36 (Ashtakoot system)
    total_score = rasi_score + nakshatra_score + gana_score
    
    # Interpretation
    if total_score >= 28:
        interpretation = "Excellent match - Very compatible"
    elif total_score >= 24:
        interpretation = "Good match - Compatible"
    elif total_score >= 18:
        interpretation = "Average match - Acceptable with effort"
    else:
        interpretation = "Below average - May face challenges"
    
    # Check Mangal Dosha
    person1_mangal = any(d['name'] == 'Mangal Dosha (Kuja Dosha)' for d in chart1['doshas'])
    person2_mangal = any(d['name'] == 'Mangal Dosha (Kuja Dosha)' for d in chart2['doshas'])
    
    mangal_match = "Both have Mangal Dosha - Cancels out" if person1_mangal and person2_mangal else \
                   "Mangal Dosha mismatch - Consider remedies" if person1_mangal or person2_mangal else \
                   "No Mangal Dosha - Good"
    
    return {
        'total_score': total_score,
        'max_score': 36,
        'percentage': round((total_score / 36) * 100, 1),
        'interpretation': interpretation,
        'breakdown': {
            'rasi_koota': rasi_score,
            'nakshatra_koota': nakshatra_score,
            'gana_koota': gana_score
        },
        'mangal_dosha': mangal_match,
        'moon_signs': {
            'person1': chart1['planetary_positions']['Moon']['rasi_name']['en'],
            'person2': chart2['planetary_positions']['Moon']['rasi_name']['en']
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
