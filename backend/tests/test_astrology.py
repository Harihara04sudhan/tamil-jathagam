"""
Comprehensive tests for Vedic Astrology calculations
"""

import pytest
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.astrology import VedicAstrology


class TestVedicAstrology:
    """Test suite for Vedic Astrology calculations"""
    
    @pytest.fixture
    def astro(self):
        """Create astrology instance"""
        return VedicAstrology()
    
    def test_initialization(self, astro):
        """Test astrology engine initializes properly"""
        assert astro is not None
        assert astro.ts is not None
        assert astro.eph is not None
    
    def test_rasi_calculation(self, astro):
        """Test rasi (zodiac sign) calculation from longitude"""
        # Test each rasi boundary
        assert astro.get_rasi(0) == 1    # Aries
        assert astro.get_rasi(29.9) == 1  # Still Aries
        assert astro.get_rasi(30) == 2    # Taurus
        assert astro.get_rasi(60) == 3    # Gemini
        assert astro.get_rasi(180) == 7   # Libra
        assert astro.get_rasi(330) == 12  # Pisces
        assert astro.get_rasi(359) == 12  # Still Pisces
    
    def test_nakshatra_calculation(self, astro):
        """Test nakshatra calculation from longitude"""
        # Test first nakshatra
        nak = astro.get_nakshatra(0)
        assert nak['name'] == 'Ashwini'
        assert nak['tamil'] == 'அசுவினி'
        assert nak['lord'] == 'Ketu'
        assert nak['pada'] == 1
        
        # Test middle nakshatra
        nak = astro.get_nakshatra(120)
        assert nak['name'] == 'Magha'
        
        # Test last nakshatra
        nak = astro.get_nakshatra(359)
        assert nak['name'] == 'Revati'
    
    def test_ayanamsa_calculation(self, astro):
        """Test Lahiri ayanamsa calculation"""
        # J2000 epoch
        jd_2000 = 2451545.0
        ayanamsa = astro.calculate_ayanamsa(jd_2000)
        assert 23.8 < ayanamsa < 23.9  # Should be close to LAHIRI_AYANAMSA_2000
        
        # Future date (ayanamsa increases)
        jd_2025 = jd_2000 + (25 * 365.25)
        ayanamsa_2025 = astro.calculate_ayanamsa(jd_2025)
        assert ayanamsa_2025 > ayanamsa
    
    def test_tropical_to_sidereal(self, astro):
        """Test tropical to sidereal conversion"""
        tropical = 30.0
        ayanamsa = 24.0
        sidereal = astro.tropical_to_sidereal(tropical, ayanamsa)
        assert sidereal == 6.0
        
        # Test wrapping
        tropical = 10.0
        sidereal = astro.tropical_to_sidereal(tropical, ayanamsa)
        assert sidereal == 346.0
    
    def test_planetary_positions(self, astro):
        """Test planetary position calculation"""
        # Test date: January 1, 2000, 12:00 UTC
        dt = datetime(2000, 1, 1, 12, 0, 0)
        lat, lon = 13.0827, 80.2707  # Chennai
        
        positions = astro.calculate_planetary_positions(dt, lat, lon)
        
        # Check all 9 grahas are present
        expected_planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 
                          'Venus', 'Saturn', 'Rahu', 'Ketu']
        for planet in expected_planets:
            assert planet in positions
            
            # Check each planet has required fields
            pos = positions[planet]
            assert 'longitude' in pos
            assert 'rasi' in pos
            assert 'rasi_name' in pos
            assert 'degrees_in_rasi' in pos
            assert 'nakshatra' in pos
            assert 'nakshatra_tamil' in pos
            assert 'nakshatra_lord' in pos
            assert 'pada' in pos
            
            # Check data validity
            assert 0 <= pos['longitude'] < 360
            assert 1 <= pos['rasi'] <= 12
            assert 0 <= pos['degrees_in_rasi'] < 30
            assert 1 <= pos['pada'] <= 4
    
    def test_ascendant_calculation(self, astro):
        """Test ascendant (lagna) calculation"""
        dt = datetime(2000, 1, 1, 6, 0, 0)  # 6 AM
        lat, lon = 13.0827, 80.2707
        
        ascendant = astro.calculate_ascendant(dt, lat, lon)
        
        assert 'longitude' in ascendant
        assert 'rasi' in ascendant
        assert 'rasi_name' in ascendant
        assert 'nakshatra' in ascendant
        assert 'lord' in ascendant
        
        assert 0 <= ascendant['longitude'] < 360
        assert 1 <= ascendant['rasi'] <= 12
    
    def test_houses_calculation(self, astro):
        """Test 12 houses calculation"""
        ascendant_long = 45.0  # 15 degrees in Taurus
        houses = astro.calculate_houses(ascendant_long)
        
        assert len(houses) == 12
        
        # Check each house
        for i in range(1, 13):
            assert i in houses
            house = houses[i]
            assert 'house_number' in house
            assert 'cusp_longitude' in house
            assert 'rasi' in house
            assert 'lord' in house
            assert house['house_number'] == i
    
    def test_vimshottari_dasha(self, astro):
        """Test Vimshottari Dasha calculation"""
        birth_date = datetime(1990, 5, 15, 10, 30)
        moon_longitude = 120.0  # Magha nakshatra (Ketu lord)
        
        dashas = astro.calculate_vimshottari_dasha(moon_longitude, birth_date)
        
        assert len(dashas) == 9  # 9 planetary periods
        
        # Check first dasha is ruled by birth nakshatra lord
        first_dasha = dashas[0]
        nakshatra = astro.get_nakshatra(moon_longitude)
        assert first_dasha['planet'] == nakshatra['lord']
        
        # Check all required fields
        for dasha in dashas:
            assert 'planet' in dasha
            assert 'planet_tamil' in dasha
            assert 'start_date' in dasha
            assert 'end_date' in dasha
            assert 'years' in dasha
            
            # Verify dates are chronological
            start = datetime.strptime(dasha['start_date'], '%Y-%m-%d')
            end = datetime.strptime(dasha['end_date'], '%Y-%m-%d')
            assert end > start
    
    def test_yogas_calculation(self, astro):
        """Test yoga calculation"""
        dt = datetime(2000, 1, 1, 12, 0, 0)
        lat, lon = 13.0827, 80.2707
        
        positions = astro.calculate_planetary_positions(dt, lat, lon)
        ascendant = astro.calculate_ascendant(dt, lat, lon)
        
        yogas = astro.calculate_yogas(positions, ascendant)
        
        # Yogas is a list
        assert isinstance(yogas, list)
        
        # Check yoga structure
        for yoga in yogas:
            assert 'name' in yoga
            assert 'type' in yoga
            assert 'description' in yoga
            assert 'strength' in yoga
    
    def test_doshas_calculation(self, astro):
        """Test dosha calculation"""
        dt = datetime(2000, 1, 1, 12, 0, 0)
        lat, lon = 13.0827, 80.2707
        
        positions = astro.calculate_planetary_positions(dt, lat, lon)
        ascendant = astro.calculate_ascendant(dt, lat, lon)
        
        doshas = astro.calculate_doshas(positions, ascendant)
        
        # Doshas is a list
        assert isinstance(doshas, list)
        
        # Check dosha structure
        for dosha in doshas:
            assert 'name' in dosha
            assert 'severity' in dosha
            assert 'description' in dosha
    
    def test_birth_chart_generation(self, astro):
        """Test complete birth chart generation"""
        birth_dt = datetime(1990, 5, 15, 14, 30)
        lat, lon = 13.0827, 80.2707
        timezone = 'Asia/Kolkata'
        
        chart = astro.generate_birth_chart(birth_dt, lat, lon, timezone)
        
        # Check all main sections exist
        assert 'birth_info' in chart
        assert 'ascendant' in chart
        assert 'planetary_positions' in chart
        assert 'houses' in chart
        assert 'vimshottari_dasha' in chart
        assert 'yogas' in chart
        assert 'doshas' in chart
        assert 'predictions' in chart
        
        # Check predictions categories
        predictions = chart['predictions']
        assert 'personality' in predictions
        assert 'career' in predictions
        assert 'relationships' in predictions
        assert 'health' in predictions
        assert 'wealth' in predictions
        assert 'current_period' in predictions
    
    def test_nakshatra_data_integrity(self, astro):
        """Test nakshatra data is complete and correct"""
        assert len(astro.NAKSHATRAS) == 27
        
        for nak in astro.NAKSHATRAS:
            assert 'id' in nak
            assert 'name' in nak
            assert 'tamil' in nak
            assert 'lord' in nak
            assert 'start' in nak
            assert 1 <= nak['id'] <= 27
    
    def test_rasi_data_integrity(self, astro):
        """Test rasi data is complete"""
        assert len(astro.RASI_NAMES) == 12
        assert len(astro.RASI_LORDS) == 12
        
        for i in range(1, 13):
            assert i in astro.RASI_NAMES
            assert i in astro.RASI_LORDS
            assert 'en' in astro.RASI_NAMES[i]
            assert 'ta' in astro.RASI_NAMES[i]
    
    def test_dasha_periods_data(self, astro):
        """Test dasha period data"""
        assert len(astro.DASHA_PERIODS) == 9
        assert len(astro.DASHA_ORDER) == 9
        
        # Check total equals 120 years
        total_years = sum(astro.DASHA_PERIODS.values())
        assert total_years == 120
    
    def test_different_locations(self, astro):
        """Test calculations for different locations"""
        dt = datetime(2000, 1, 1, 12, 0, 0)
        
        # Chennai
        positions1 = astro.calculate_planetary_positions(dt, 13.0827, 80.2707)
        ascendant1 = astro.calculate_ascendant(dt, 13.0827, 80.2707)
        
        # New York
        positions2 = astro.calculate_planetary_positions(dt, 40.7128, -74.0060)
        ascendant2 = astro.calculate_ascendant(dt, 40.7128, -74.0060)
        
        # Planetary positions should be same (geocentric)
        assert positions1['Sun']['longitude'] == positions2['Sun']['longitude']
        
        # Ascendant should be different (local)
        assert ascendant1['longitude'] != ascendant2['longitude']
    
    def test_edge_cases(self, astro):
        """Test edge cases"""
        # Longitude at boundary
        assert astro.get_rasi(0) == 1
        assert astro.get_rasi(360) == 1  # Wraps around
        
        # Very old date
        old_dt = datetime(1900, 1, 1, 12, 0, 0)
        positions = astro.calculate_planetary_positions(old_dt, 13.0827, 80.2707)
        assert 'Sun' in positions
        
        # Future date
        future_dt = datetime(2050, 12, 31, 12, 0, 0)
        positions = astro.calculate_planetary_positions(future_dt, 13.0827, 80.2707)
        assert 'Sun' in positions


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
