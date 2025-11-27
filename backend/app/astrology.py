"""
Comprehensive Vedic Astrology Calculation Engine
Implements full Jathagam (Birth Chart) calculations with Tamil support
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, List, Tuple, Optional
import math
from skyfield.api import load, wgs84, N, E, W, S
from skyfield.almanac import find_discrete
import pytz

# Lahiri Ayanamsa (most common in Indian astrology)
LAHIRI_AYANAMSA_2000 = 23.85  # degrees at J2000
AYANAMSA_RATE = 0.01397  # degrees per year


class VedicAstrology:
    """Complete Vedic Astrology calculation system"""
    
    # Tamil names for celestial bodies
    GRAHA_NAMES_TAMIL = {
        'Sun': 'சூரியன்', 'Moon': 'சந்திரன்', 'Mars': 'செவ்வாய்',
        'Mercury': 'புதன்', 'Jupiter': 'குரு', 'Venus': 'சுக்ரன்',
        'Saturn': 'சனி', 'Rahu': 'ராகு', 'Ketu': 'கேது'
    }
    
    # Zodiac signs in English and Tamil
    RASI_NAMES = {
        1: {'en': 'Aries', 'ta': 'மேஷம்'},
        2: {'en': 'Taurus', 'ta': 'ரிஷபம்'},
        3: {'en': 'Gemini', 'ta': 'மிதுனம்'},
        4: {'en': 'Cancer', 'ta': 'கடகம்'},
        5: {'en': 'Leo', 'ta': 'சிம்மம்'},
        6: {'en': 'Virgo', 'ta': 'கன்னி'},
        7: {'en': 'Libra', 'ta': 'துலாம்'},
        8: {'en': 'Scorpio', 'ta': 'விருச்சிகம்'},
        9: {'en': 'Sagittarius', 'ta': 'தனுசு'},
        10: {'en': 'Capricorn', 'ta': 'மகரம்'},
        11: {'en': 'Aquarius', 'ta': 'கும்பம்'},
        12: {'en': 'Pisces', 'ta': 'மீனம்'}
    }
    
    # 27 Nakshatras with Tamil names
    NAKSHATRAS = [
        {'id': 1, 'name': 'Ashwini', 'tamil': 'அசுவினி', 'lord': 'Ketu', 'start': 0.0},
        {'id': 2, 'name': 'Bharani', 'tamil': 'பரணி', 'lord': 'Venus', 'start': 13.333},
        {'id': 3, 'name': 'Krittika', 'tamil': 'கார்த்திகை', 'lord': 'Sun', 'start': 26.666},
        {'id': 4, 'name': 'Rohini', 'tamil': 'ரோகிணி', 'lord': 'Moon', 'start': 40.0},
        {'id': 5, 'name': 'Mrigashira', 'tamil': 'மிருகசீரிடம்', 'lord': 'Mars', 'start': 53.333},
        {'id': 6, 'name': 'Ardra', 'tamil': 'திருவாதிரை', 'lord': 'Rahu', 'start': 66.666},
        {'id': 7, 'name': 'Punarvasu', 'tamil': 'புனர்பூசம்', 'lord': 'Jupiter', 'start': 80.0},
        {'id': 8, 'name': 'Pushya', 'tamil': 'பூசம்', 'lord': 'Saturn', 'start': 93.333},
        {'id': 9, 'name': 'Ashlesha', 'tamil': 'ஆயில்யம்', 'lord': 'Mercury', 'start': 106.666},
        {'id': 10, 'name': 'Magha', 'tamil': 'மகம்', 'lord': 'Ketu', 'start': 120.0},
        {'id': 11, 'name': 'Purva Phalguni', 'tamil': 'பூரம்', 'lord': 'Venus', 'start': 133.333},
        {'id': 12, 'name': 'Uttara Phalguni', 'tamil': 'உத்திரம்', 'lord': 'Sun', 'start': 146.666},
        {'id': 13, 'name': 'Hasta', 'tamil': 'ஹஸ்தம்', 'lord': 'Moon', 'start': 160.0},
        {'id': 14, 'name': 'Chitra', 'tamil': 'சித்திரை', 'lord': 'Mars', 'start': 173.333},
        {'id': 15, 'name': 'Swati', 'tamil': 'சுவாதி', 'lord': 'Rahu', 'start': 186.666},
        {'id': 16, 'name': 'Vishakha', 'tamil': 'விசாகம்', 'lord': 'Jupiter', 'start': 200.0},
        {'id': 17, 'name': 'Anuradha', 'tamil': 'அனுஷம்', 'lord': 'Saturn', 'start': 213.333},
        {'id': 18, 'name': 'Jyeshtha', 'tamil': 'கேட்டை', 'lord': 'Mercury', 'start': 226.666},
        {'id': 19, 'name': 'Mula', 'tamil': 'மூலம்', 'lord': 'Ketu', 'start': 240.0},
        {'id': 20, 'name': 'Purva Ashadha', 'tamil': 'பூராடம்', 'lord': 'Venus', 'start': 253.333},
        {'id': 21, 'name': 'Uttara Ashadha', 'tamil': 'உத்திராடம்', 'lord': 'Sun', 'start': 266.666},
        {'id': 22, 'name': 'Shravana', 'tamil': 'திருவோணம்', 'lord': 'Moon', 'start': 280.0},
        {'id': 23, 'name': 'Dhanishta', 'tamil': 'அவிட்டம்', 'lord': 'Mars', 'start': 293.333},
        {'id': 24, 'name': 'Shatabhisha', 'tamil': 'சதயம்', 'lord': 'Rahu', 'start': 306.666},
        {'id': 25, 'name': 'Purva Bhadrapada', 'tamil': 'பூரட்டாதி', 'lord': 'Jupiter', 'start': 320.0},
        {'id': 26, 'name': 'Uttara Bhadrapada', 'tamil': 'உத்திரட்டாதி', 'lord': 'Saturn', 'start': 333.333},
        {'id': 27, 'name': 'Revati', 'tamil': 'ரேவதி', 'lord': 'Mercury', 'start': 346.666}
    ]
    
    # House lords (which planet rules which sign)
    RASI_LORDS = {
        1: 'Mars', 2: 'Venus', 3: 'Mercury', 4: 'Moon',
        5: 'Sun', 6: 'Mercury', 7: 'Venus', 8: 'Mars',
        9: 'Jupiter', 10: 'Saturn', 11: 'Saturn', 12: 'Jupiter'
    }
    
    # Planet friendships for strength calculations
    PLANET_FRIENDS = {
        'Sun': ['Moon', 'Mars', 'Jupiter'],
        'Moon': ['Sun', 'Mercury'],
        'Mars': ['Sun', 'Moon', 'Jupiter'],
        'Mercury': ['Sun', 'Venus'],
        'Jupiter': ['Sun', 'Moon', 'Mars'],
        'Venus': ['Mercury', 'Saturn'],
        'Saturn': ['Mercury', 'Venus']
    }
    
    # Vimshottari Dasha periods (in years)
    DASHA_PERIODS = {
        'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10,
        'Mars': 7, 'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17
    }
    
    # Dasha order starting from birth nakshatra lord
    DASHA_ORDER = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
    
    def __init__(self):
        """Initialize ephemeris data"""
        self.ts = load.timescale()
        self.eph = load('de421.bsp')  # JPL planetary ephemeris
        
    def calculate_ayanamsa(self, jd: float) -> float:
        """Calculate Lahiri ayanamsa for given Julian Day"""
        # J2000 is JD 2451545.0
        years_from_2000 = (jd - 2451545.0) / 365.25
        ayanamsa = LAHIRI_AYANAMSA_2000 + (AYANAMSA_RATE * years_from_2000)
        return ayanamsa
    
    def tropical_to_sidereal(self, tropical_long: float, ayanamsa: float) -> float:
        """Convert tropical longitude to sidereal"""
        sidereal = tropical_long - ayanamsa
        return sidereal % 360
    
    def get_rasi(self, longitude: float) -> int:
        """Get rasi (zodiac sign) number from longitude (1-12)"""
        return int(longitude / 30) + 1
    
    def get_nakshatra(self, longitude: float) -> Dict:
        """Get nakshatra details from longitude"""
        # Each nakshatra is 13.333... degrees (360/27)
        nakshatra_span = 360 / 27
        nakshatra_num = int(longitude / nakshatra_span)
        nakshatra = self.NAKSHATRAS[nakshatra_num]
        
        # Calculate pada (quarter) - each nakshatra has 4 padas
        pada_span = nakshatra_span / 4
        degrees_in_nakshatra = longitude - nakshatra['start']
        pada = int(degrees_in_nakshatra / pada_span) + 1
        
        return {
            **nakshatra,
            'pada': pada,
            'degrees_in_nakshatra': degrees_in_nakshatra
        }
    
    def calculate_planetary_positions(self, dt: datetime, lat: float, lon: float) -> Dict:
        """Calculate positions of all 9 grahas (planets + nodes)"""
        # Convert to skyfield time
        t = self.ts.from_datetime(dt.replace(tzinfo=timezone.utc))
        
        # Create observer location
        location = wgs84.latlon(lat, lon)
        
        # Calculate ayanamsa
        ayanamsa = self.calculate_ayanamsa(t.tt)
        
        # Get planetary positions
        planets = {
            'Sun': self.eph['sun'],
            'Moon': self.eph['moon'],
            'Mercury': self.eph['mercury'],
            'Venus': self.eph['venus'],
            'Mars': self.eph['mars'],
            'Jupiter': self.eph['jupiter barycenter'],
            'Saturn': self.eph['saturn barycenter']
        }
        
        positions = {}
        earth = self.eph['earth']
        
        for name, planet in planets.items():
            # Get geocentric position
            astrometric = earth.at(t).observe(planet)
            ra, dec, distance = astrometric.radec()
            
            # Convert to ecliptic longitude (tropical)
            ecliptic_pos = astrometric.apparent().ecliptic_latlon()
            tropical_long = ecliptic_pos[1].degrees
            
            # Convert to sidereal
            sidereal_long = self.tropical_to_sidereal(tropical_long, ayanamsa)
            
            # Get rasi and nakshatra
            rasi_num = self.get_rasi(sidereal_long)
            nakshatra = self.get_nakshatra(sidereal_long)
            
            # Check for retrograde motion by comparing positions 1 day apart
            is_retrograde = False
            if name not in ['Sun', 'Moon']:  # Sun and Moon never retrograde
                try:
                    # Get position 1 day later
                    t_next = self.ts.from_datetime((dt + timedelta(days=1)).replace(tzinfo=timezone.utc))
                    astrometric_next = earth.at(t_next).observe(planet)
                    ecliptic_next = astrometric_next.apparent().ecliptic_latlon()
                    tropical_next = ecliptic_next[1].degrees
                    sidereal_next = self.tropical_to_sidereal(tropical_next, ayanamsa)
                    
                    # If tomorrow's longitude is less than today's, planet is retrograde
                    # Account for 360-degree wrap-around
                    diff = (sidereal_next - sidereal_long + 360) % 360
                    is_retrograde = diff > 180
                except:
                    is_retrograde = False
            
            positions[name] = {
                'longitude': sidereal_long,
                'rasi': rasi_num,
                'rasi_name': self.RASI_NAMES[rasi_num],
                'degrees_in_rasi': sidereal_long % 30,
                'nakshatra': nakshatra['name'],
                'nakshatra_tamil': nakshatra['tamil'],
                'nakshatra_lord': nakshatra['lord'],
                'pada': nakshatra['pada'],
                'nakshatra_id': nakshatra['id'],
                'is_retrograde': is_retrograde
            }
        
        # Calculate Rahu and Ketu (lunar nodes) - using Skyfield's true node
        # Get Moon's orbital elements to find the ascending node
        try:
            # Skyfield provides the Moon's mean ascending node
            # Calculate using the Moon's position relative to ecliptic
            moon_astrometric = earth.at(t).observe(self.eph['moon'])
            moon_ecliptic = moon_astrometric.apparent().ecliptic_latlon()
            
            # For a more accurate calculation, we use the moon's orbital elements
            # The ascending node (Rahu) is approximately 180 degrees from the mean anomaly
            # This is a simplified but more accurate approach than just moon_long + 180
            
            # Mean longitude of ascending node (Rahu) - traditional Vedic calculation
            # Using the formula from astronomical texts
            jd = t.tt
            T = (jd - 2451545.0) / 36525.0  # Julian centuries from J2000
            
            # Mean longitude of Moon's ascending node (in degrees)
            omega = 125.04452 - 1934.136261 * T + 0.0020708 * T**2 + T**3 / 450000.0
            omega = omega % 360
            
            # Apply ayanamsa to convert to sidereal
            rahu_long = self.tropical_to_sidereal(omega, ayanamsa)
            ketu_long = (rahu_long + 180) % 360
            
        except Exception as e:
            # Fallback to simplified calculation if detailed calculation fails
            moon_long = positions['Moon']['longitude']
            rahu_long = (moon_long + 180) % 360
            ketu_long = (rahu_long + 180) % 360
        
        # Rahu
        rasi_num = self.get_rasi(rahu_long)
        nakshatra = self.get_nakshatra(rahu_long)
        positions['Rahu'] = {
            'longitude': rahu_long,
            'rasi': rasi_num,
            'rasi_name': self.RASI_NAMES[rasi_num],
            'degrees_in_rasi': rahu_long % 30,
            'nakshatra': nakshatra['name'],
            'nakshatra_tamil': nakshatra['tamil'],
            'nakshatra_lord': nakshatra['lord'],
            'pada': nakshatra['pada'],
            'is_retrograde': True  # Always retrograde
        }
        
        # Ketu
        rasi_num = self.get_rasi(ketu_long)
        nakshatra = self.get_nakshatra(ketu_long)
        positions['Ketu'] = {
            'longitude': ketu_long,
            'rasi': rasi_num,
            'rasi_name': self.RASI_NAMES[rasi_num],
            'degrees_in_rasi': ketu_long % 30,
            'nakshatra': nakshatra['name'],
            'nakshatra_tamil': nakshatra['tamil'],
            'nakshatra_lord': nakshatra['lord'],
            'pada': nakshatra['pada'],
            'is_retrograde': True  # Always retrograde
        }
        
        return positions
    
    def calculate_ascendant(self, dt: datetime, lat: float, lon: float) -> Dict:
        """Calculate Lagna (Ascendant) - Rising sign at birth time and location"""
        t = self.ts.from_datetime(dt.replace(tzinfo=timezone.utc))
        
        # Calculate Local Sidereal Time (LST)
        # GAST = Greenwich Apparent Sidereal Time
        gast_hours = t.gast
        
        # Convert longitude to hours (15 degrees = 1 hour)
        longitude_hours = lon / 15.0
        
        # Local Sidereal Time = GAST + Longitude in hours
        lst_hours = gast_hours + longitude_hours
        lst_degrees = (lst_hours * 15.0) % 360  # Convert back to degrees
        
        # Calculate obliquity of ecliptic for the date
        jd = t.tt
        T = (jd - 2451545.0) / 36525.0  # Julian centuries from J2000
        epsilon = 23.439291 - 0.0130042 * T - 0.00000164 * T**2 + 0.000000504 * T**3
        epsilon_rad = math.radians(epsilon)
        
        # Convert latitude to radians
        lat_rad = math.radians(lat)
        
        # Calculate Right Ascension of Meridian (RAMC)
        ramc = lst_degrees
        ramc_rad = math.radians(ramc)
        
        # Calculate Ascendant using the formula:
        # tan(ASC) = cos(RAMC) / (-sin(RAMC) * cos(epsilon) - tan(lat) * sin(epsilon))
        numerator = math.cos(ramc_rad)
        denominator = -math.sin(ramc_rad) * math.cos(epsilon_rad) - math.tan(lat_rad) * math.sin(epsilon_rad)
        
        asc_rad = math.atan2(numerator, denominator)
        asc_tropical = math.degrees(asc_rad) % 360
        
        # Apply ayanamsa to get sidereal ascendant
        ayanamsa = self.calculate_ayanamsa(jd)
        asc_sidereal = self.tropical_to_sidereal(asc_tropical, ayanamsa)
        rasi_num = self.get_rasi(asc_sidereal)
        nakshatra = self.get_nakshatra(asc_sidereal)
        
        return {
            'longitude': asc_sidereal,
            'rasi': rasi_num,
            'rasi_name': self.RASI_NAMES[rasi_num],
            'degrees_in_rasi': asc_sidereal % 30,
            'nakshatra': nakshatra['name'],
            'nakshatra_tamil': nakshatra['tamil'],
            'lord': self.RASI_LORDS[rasi_num]
        }
    
    def calculate_houses(self, ascendant_long: float) -> Dict[int, Dict]:
        """Calculate 12 houses (Bhavas) from ascendant"""
        houses = {}
        
        for i in range(1, 13):
            house_long = (ascendant_long + (i - 1) * 30) % 360
            rasi_num = self.get_rasi(house_long)
            
            houses[i] = {
                'house_number': i,
                'cusp_longitude': house_long,
                'rasi': rasi_num,
                'rasi_name': self.RASI_NAMES[rasi_num],
                'lord': self.RASI_LORDS[rasi_num]
            }
        
        return houses
    
    def calculate_vimshottari_dasha(self, birth_moon_longitude: float, birth_date: datetime) -> List[Dict]:
        """Calculate Vimshottari Dasha periods"""
        # Find birth nakshatra
        nakshatra = self.get_nakshatra(birth_moon_longitude)
        start_lord = nakshatra['lord']
        
        # Calculate how much of the birth nakshatra has passed
        nakshatra_span = 360 / 27
        degrees_passed = nakshatra['degrees_in_nakshatra']
        fraction_passed = degrees_passed / nakshatra_span
        
        # Years of starting dasha already elapsed at birth
        start_dasha_total_years = self.DASHA_PERIODS[start_lord]
        years_elapsed = start_dasha_total_years * fraction_passed
        years_remaining = start_dasha_total_years - years_elapsed
        
        # Build dasha timeline
        dashas = []
        current_date = birth_date
        
        # Find starting position in dasha order
        start_index = self.DASHA_ORDER.index(start_lord)
        
        # First dasha (partial)
        from dateutil.relativedelta import relativedelta
        # Convert float years to days for accurate calculation
        days_remaining = int(years_remaining * 365.25)
        from datetime import timedelta
        end_date = current_date + timedelta(days=days_remaining)
        dashas.append({
            'planet': start_lord,
            'planet_tamil': self.GRAHA_NAMES_TAMIL.get(start_lord, start_lord),
            'start_date': current_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'years': round(years_remaining, 2)
        })
        current_date = end_date
        
        # Remaining dashas (120 year cycle)
        for i in range(1, 9):
            lord_index = (start_index + i) % 9
            lord = self.DASHA_ORDER[lord_index]
            years = self.DASHA_PERIODS[lord]
            
            # Convert integer years to days for accurate calculation
            days = int(years * 365.25)
            end_date = current_date + timedelta(days=days)
            dashas.append({
                'planet': lord,
                'planet_tamil': self.GRAHA_NAMES_TAMIL.get(lord, lord),
                'start_date': current_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'years': years
            })
            current_date = end_date
        
        return dashas
    
    def calculate_yogas(self, positions: Dict, ascendant: Dict) -> List[Dict]:
        """Calculate important yogas (planetary combinations)"""
        yogas = []
        
        # Raja Yoga: Lords of trikona (1,5,9) and kendra (1,4,7,10) together
        # Simplified version - check if benefics are in kendras
        
        benefics = ['Jupiter', 'Venus', 'Mercury', 'Moon']
        for planet in benefics:
            if planet in positions:
                rasi = positions[planet]['rasi']
                house_from_lagna = ((rasi - ascendant['rasi']) % 12) + 1
                if house_from_lagna in [1, 4, 7, 10]:
                    yogas.append({
                        'name': f'{planet} in Kendra',
                        'type': 'Benefic',
                        'description': f'{planet} is in a Kendra house ({house_from_lagna}), which strengthens the chart',
                        'strength': 'Good'
                    })
        
        # Gaja Kesari Yoga: Jupiter in kendra from Moon
        if 'Jupiter' in positions and 'Moon' in positions:
            jup_rasi = positions['Jupiter']['rasi']
            moon_rasi = positions['Moon']['rasi']
            diff = ((jup_rasi - moon_rasi) % 12) + 1
            if diff in [1, 4, 7, 10]:
                yogas.append({
                    'name': 'Gaja Kesari Yoga',
                    'type': 'Raja Yoga',
                    'description': 'Jupiter in Kendra from Moon - brings wisdom, prosperity and good character',
                    'strength': 'Excellent'
                })
        
        # Check for Rahu-Ketu axis (always opposite)
        if 'Rahu' in positions:
            rahu_house = ((positions['Rahu']['rasi'] - ascendant['rasi']) % 12) + 1
            ketu_house = ((positions['Ketu']['rasi'] - ascendant['rasi']) % 12) + 1
            yogas.append({
                'name': 'Rahu-Ketu Axis',
                'type': 'Karmic',
                'description': f'Rahu in house {rahu_house}, Ketu in house {ketu_house} - indicates karmic lessons and growth areas',
                'strength': 'Neutral'
            })
        
        return yogas
    
    def calculate_doshas(self, positions: Dict, ascendant: Dict) -> List[Dict]:
        """Calculate doshas (afflictions)"""
        doshas = []
        
        # Mangal Dosha (Kuja Dosha): Mars in houses 1,2,4,7,8,12 from Lagna
        if 'Mars' in positions:
            mars_house = ((positions['Mars']['rasi'] - ascendant['rasi']) % 12) + 1
            if mars_house in [1, 2, 4, 7, 8, 12]:
                doshas.append({
                    'name': 'Mangal Dosha (Kuja Dosha)',
                    'severity': 'Medium',
                    'description': f'Mars in house {mars_house} - may affect marriage and relationships. Remedies: worship Lord Hanuman, recite Hanuman Chalisa',
                    'house': mars_house
                })
        
        # Kala Sarpa Dosha: All planets between Rahu and Ketu
        if 'Rahu' in positions and 'Ketu' in positions:
            rahu_long = positions['Rahu']['longitude']
            ketu_long = positions['Ketu']['longitude']
            
            all_between = True
            for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
                if planet in positions:
                    planet_long = positions[planet]['longitude']
                    # Check if planet is between Rahu and Ketu
                    if ketu_long < rahu_long:
                        if not (ketu_long <= planet_long <= rahu_long):
                            all_between = False
                            break
                    else:
                        if not (planet_long >= rahu_long or planet_long <= ketu_long):
                            all_between = False
                            break
            
            if all_between:
                doshas.append({
                    'name': 'Kala Sarpa Dosha',
                    'severity': 'High',
                    'description': 'All planets hemmed between Rahu and Ketu - may cause delays and obstacles. Remedies: worship Lord Shiva, visit Rahu-Ketu temples',
                    'house': 'All'
                })
        
        # Pitra Dosha: Sun with Rahu/Ketu
        if 'Sun' in positions:
            sun_rasi = positions['Sun']['rasi']
            if 'Rahu' in positions and positions['Rahu']['rasi'] == sun_rasi:
                doshas.append({
                    'name': 'Pitra Dosha (Sun-Rahu)',
                    'severity': 'Medium',
                    'description': 'Sun conjunct Rahu - ancestral issues. Remedies: perform Shraddha, donate to charity',
                    'house': sun_rasi
                })
        
        return doshas
    
    def calculate_10_porutham(self, male_chart: Dict, female_chart: Dict) -> Dict:
        """
        Calculate 10 Porutham (பத்து பொருத்தம்) - Tamil marriage compatibility
        Returns detailed compatibility analysis based on traditional Tamil astrology
        """
        male_moon = male_chart['planetary_positions']['Moon']
        female_moon = female_chart['planetary_positions']['Moon']
        
        male_nakshatra_id = male_moon['nakshatra_id']
        female_nakshatra_id = female_moon['nakshatra_id']
        
        male_rasi = male_moon['rasi']
        female_rasi = female_moon['rasi']
        
        poruthams = []
        total_points = 0
        max_points = 0
        
        # 1. தினப் பொருத்தம் (Dina Porutham) - Daily compatibility / Health
        max_points += 3
        dina_diff = abs(female_nakshatra_id - male_nakshatra_id)
        if dina_diff % 9 not in [0, 1]:  # Should not be in 1st or 2nd position from each other
            dina_points = 3
            dina_status = "மிக நல்லது (Excellent)"
            total_points += 3
        elif dina_diff % 9 == 1:
            dina_points = 1.5
            dina_status = "நடுத்தரம் (Average)"
            total_points += 1.5
        else:
            dina_points = 0
            dina_status = "பொருந்தவில்லை (Not Compatible)"
        
        poruthams.append({
            'name': 'தினப் பொருத்தம் (Dina Porutham)',
            'name_en': 'Daily Compatibility',
            'points': dina_points,
            'max_points': 3,
            'status': dina_status,
            'description': 'Indicates physical health, well-being and daily harmony between the couple.',
            'importance': 'High'
        })
        
        # 2. கணப் பொருத்தம் (Gana Porutham) - Temperament compatibility
        max_points += 6
        gana_classification = {
            1: 'Deva', 2: 'Manushya', 3: 'Rakshasa', 4: 'Manushya', 5: 'Manushya',
            6: 'Deva', 7: 'Manushya', 8: 'Rakshasa', 9: 'Manushya', 10: 'Manushya',
            11: 'Rakshasa', 12: 'Rakshasa', 13: 'Deva', 14: 'Manushya', 15: 'Manushya',
            16: 'Rakshasa', 17: 'Manushya', 18: 'Rakshasa', 19: 'Manushya', 20: 'Rakshasa',
            21: 'Manushya', 22: 'Deva', 23: 'Deva', 24: 'Rakshasa', 25: 'Rakshasa',
            26: 'Deva', 27: 'Deva'
        }
        
        male_gana = gana_classification[male_nakshatra_id]
        female_gana = gana_classification[female_nakshatra_id]
        
        if male_gana == female_gana:
            gana_points = 6
            gana_status = "மிக நல்லது (Excellent)"
            total_points += 6
        elif (male_gana == 'Deva' and female_gana == 'Manushya') or \
             (male_gana == 'Manushya' and female_gana == 'Deva'):
            gana_points = 5
            gana_status = "நல்லது (Good)"
            total_points += 5
        elif (male_gana == 'Manushya' and female_gana == 'Rakshasa') or \
             (male_gana == 'Rakshasa' and female_gana == 'Manushya'):
            gana_points = 1
            gana_status = "சாதாரணம் (Fair)"
            total_points += 1
        else:
            gana_points = 0
            gana_status = "பொருந்தவில்லை (Not Compatible)"
        
        poruthams.append({
            'name': 'கணப் பொருத்தம் (Gana Porutham)',
            'name_en': 'Temperament Match',
            'points': gana_points,
            'max_points': 6,
            'status': gana_status,
            'description': f'Male: {male_gana}, Female: {female_gana}. Indicates nature and behavior compatibility.',
            'importance': 'Very High'
        })
        
        # 3. மகேந்திரப் பொருத்தம் (Mahendra Porutham) - Progeny & prosperity
        max_points += 2
        mahendra_diff = (female_nakshatra_id - male_nakshatra_id) % 27
        if mahendra_diff in [4, 7, 10, 13, 16, 19, 22, 25]:
            mahendra_points = 2
            mahendra_status = "நல்லது (Good)"
            total_points += 2
        else:
            mahendra_points = 0
            mahendra_status = "இல்லை (Not Present)"
        
        poruthams.append({
            'name': 'மகேந்திரப் பொருத்தம் (Mahendra Porutham)',
            'name_en': 'Progeny & Prosperity',
            'points': mahendra_points,
            'max_points': 2,
            'status': mahendra_status,
            'description': 'Ensures good children, wealth and prosperity in married life.',
            'importance': 'High'
        })
        
        # 4. ஸ்திரீ தீர்க்கப் பொருத்தம் (Stree Deergha Porutham) - Longevity of wife
        max_points += 3
        stree_diff = (female_nakshatra_id - male_nakshatra_id) % 27
        if stree_diff >= 13:  # Female nakshatra should be beyond 13 from male
            stree_points = 3
            stree_status = "நல்லது (Good)"
            total_points += 3
        else:
            stree_points = 0
            stree_status = "இல்லை (Not Present)"
        
        poruthams.append({
            'name': 'ஸ்திரீ தீர்க்கப் பொருத்தம் (Stree Deergha Porutham)',
            'name_en': 'Longevity & Well-being',
            'points': stree_points,
            'max_points': 3,
            'status': stree_status,
            'description': 'Indicates long life and good health of the wife.',
            'importance': 'High'
        })
        
        # 5. யோனிப் பொருத்தம் (Yoni Porutham) - Sexual compatibility
        max_points += 4
        yoni_classification = {
            1: 'Horse', 2: 'Elephant', 3: 'Sheep', 4: 'Serpent', 5: 'Dog',
            6: 'Cat', 7: 'Rat', 8: 'Cow', 9: 'Buffalo', 10: 'Tiger',
            11: 'Deer', 12: 'Horse', 13: 'Elephant', 14: 'Serpent', 15: 'Dog',
            16: 'Cat', 17: 'Rat', 18: 'Cow', 19: 'Buffalo', 20: 'Tiger',
            21: 'Deer', 22: 'Horse', 23: 'Lion', 24: 'Monkey', 25: 'Mongoose',
            26: 'Mongoose', 27: 'Monkey'
        }
        
        male_yoni = yoni_classification[male_nakshatra_id]
        female_yoni = yoni_classification[female_nakshatra_id]
        
        # Enemy yonis
        enemies = {
            'Horse': ['Buffalo'], 'Elephant': ['Lion'], 'Sheep': ['Monkey'],
            'Serpent': ['Mongoose'], 'Dog': ['Deer'], 'Cat': ['Rat'],
            'Cow': ['Tiger'], 'Buffalo': ['Horse'], 'Tiger': ['Cow'],
            'Deer': ['Dog'], 'Lion': ['Elephant'], 'Rat': ['Cat'],
            'Monkey': ['Sheep'], 'Mongoose': ['Serpent']
        }
        
        if male_yoni == female_yoni:
            yoni_points = 4
            yoni_status = "மிக நல்லது (Excellent)"
            total_points += 4
        elif female_yoni in enemies.get(male_yoni, []):
            yoni_points = 0
            yoni_status = "பொருந்தவில்லை (Not Compatible)"
        else:
            yoni_points = 2
            yoni_status = "நல்லது (Good)"
            total_points += 2
        
        poruthams.append({
            'name': 'யோனிப் பொருத்தம் (Yoni Porutham)',
            'name_en': 'Physical Compatibility',
            'points': yoni_points,
            'max_points': 4,
            'status': yoni_status,
            'description': f'Male: {male_yoni}, Female: {female_yoni}. Indicates physical and sexual compatibility.',
            'importance': 'Very High'
        })
        
        # 6. ராசிப் பொருத்தம் (Rasi Porutham) - Zodiac compatibility
        max_points += 7
        rasi_diff = abs(female_rasi - male_rasi)
        
        if rasi_diff == 0:  # Same rasi
            rasi_points = 1
            rasi_status = "சாதாரணம் (Fair)"
            total_points += 1
        elif rasi_diff in [2, 3, 4, 5, 6]:  # Good positions
            rasi_points = 7
            rasi_status = "மிக நல்லது (Excellent)"
            total_points += 7
        elif rasi_diff in [7, 8, 9]:  # Moderate
            rasi_points = 4
            rasi_status = "நல்லது (Good)"
            total_points += 4
        else:  # 1, 10, 11 - not ideal
            rasi_points = 1
            rasi_status = "சாதாரணம் (Fair)"
            total_points += 1
        
        poruthams.append({
            'name': 'ராசிப் பொருத்தம் (Rasi Porutham)',
            'name_en': 'Zodiac Sign Match',
            'points': rasi_points,
            'max_points': 7,
            'status': rasi_status,
            'description': 'Overall harmony based on Moon sign compatibility.',
            'importance': 'Very High'
        })
        
        # 7. ராசியதிபதிப் பொருத்தம் (Rasi Adhipathi Porutham) - Rasi Lord compatibility
        max_points += 5
        male_lord = self.RASI_LORDS[male_rasi]
        female_lord = self.RASI_LORDS[female_rasi]
        
        # Check if lords are friends
        male_lord_friends = self.PLANET_FRIENDS.get(male_lord, [])
        female_lord_friends = self.PLANET_FRIENDS.get(female_lord, [])
        
        if male_lord == female_lord:
            adhipathi_points = 5
            adhipathi_status = "மிக நல்லது (Excellent)"
            total_points += 5
        elif female_lord in male_lord_friends or male_lord in female_lord_friends:
            adhipathi_points = 4
            adhipathi_status = "நல்லது (Good)"
            total_points += 4
        else:
            adhipathi_points = 1
            adhipathi_status = "சாதாரணம் (Fair)"
            total_points += 1
        
        poruthams.append({
            'name': 'ராசியதிபதிப் பொருத்தம் (Rasi Adhipathi Porutham)',
            'name_en': 'Rasi Lord Match',
            'points': adhipathi_points,
            'max_points': 5,
            'status': adhipathi_status,
            'description': f'Male Rasi Lord: {male_lord}, Female Rasi Lord: {female_lord}. Indicates mutual understanding.',
            'importance': 'High'
        })
        
        # 8. வசியப் பொருத்தம் (Vasya Porutham) - Mutual attraction
        max_points += 2
        vasya_compatibility = {
            1: [1, 5, 9], 2: [2, 6, 10], 3: [3, 11], 4: [4, 8, 12],
            5: [1, 5, 9], 6: [2, 6, 10], 7: [3, 7, 11], 8: [4, 8, 12],
            9: [1, 5, 9], 10: [2, 6, 10], 11: [3, 7, 11], 12: [4, 8, 12]
        }
        
        if female_rasi in vasya_compatibility.get(male_rasi, []):
            vasya_points = 2
            vasya_status = "நல்லது (Good)"
            total_points += 2
        else:
            vasya_points = 0
            vasya_status = "இல்லை (Not Present)"
        
        poruthams.append({
            'name': 'வசியப் பொருத்தம் (Vasya Porutham)',
            'name_en': 'Mutual Attraction',
            'points': vasya_points,
            'max_points': 2,
            'status': vasya_status,
            'description': 'Indicates natural attraction and magnetic pull between partners.',
            'importance': 'Medium'
        })
        
        # 9. ரஜ்ஜுப் பொருத்தம் (Rajju Porutham) - Longevity & Safety
        max_points += 3
        rajju_classification = {
            1: 'Pada', 2: 'Pada', 3: 'Pada', 4: 'Kati', 5: 'Kati', 6: 'Kati',
            7: 'Nabhi', 8: 'Nabhi', 9: 'Nabhi', 10: 'Kanta', 11: 'Kanta', 12: 'Kanta',
            13: 'Kanta', 14: 'Kanta', 15: 'Kanta', 16: 'Uro', 17: 'Uro', 18: 'Uro',
            19: 'Siro', 20: 'Siro', 21: 'Siro', 22: 'Pada', 23: 'Pada', 24: 'Pada',
            25: 'Kati', 26: 'Kati', 27: 'Kati'
        }
        
        male_rajju = rajju_classification[male_nakshatra_id]
        female_rajju = rajju_classification[female_nakshatra_id]
        
        if male_rajju != female_rajju:
            rajju_points = 3
            rajju_status = "நல்லது (Good)"
            total_points += 3
        else:
            rajju_points = 0
            rajju_status = "பொருந்தவில்லை (Not Compatible)"
        
        poruthams.append({
            'name': 'ரஜ்ஜுப் பொருத்தம் (Rajju Porutham)',
            'name_en': 'Safety & Longevity',
            'points': rajju_points,
            'max_points': 3,
            'status': rajju_status,
            'description': f'Male: {male_rajju}, Female: {female_rajju}. Critical for longevity of relationship.',
            'importance': 'Very High'
        })
        
        # 10. வேதைப் பொருத்தம் (Vedha Porutham) - Absence of affliction
        max_points += 2
        vedha_pairs = [
            (1, 11), (2, 5), (3, 18), (4, 12), (6, 9), (7, 16), (8, 21),
            (10, 19), (13, 24), (14, 23), (15, 22), (17, 26), (20, 27), (25, 26)
        ]
        
        has_vedha = False
        for pair in vedha_pairs:
            if (male_nakshatra_id in pair and female_nakshatra_id in pair):
                has_vedha = True
                break
        
        if not has_vedha:
            vedha_points = 2
            vedha_status = "நல்லது (Good)"
            total_points += 2
        else:
            vedha_points = 0
            vedha_status = "வேதை உள்ளது (Vedha Present)"
        
        poruthams.append({
            'name': 'வேதைப் பொருத்தம் (Vedha Porutham)',
            'name_en': 'No Affliction',
            'points': vedha_points,
            'max_points': 2,
            'status': vedha_status,
            'description': 'Ensures no mutual affliction between the nakshatras.',
            'importance': 'High'
        })
        
        # Calculate overall compatibility
        percentage = (total_points / max_points) * 100
        
        if percentage >= 80:
            overall_status = "மிக நல்ல பொருத்தம் (Excellent Match)"
            recommendation = "This is an excellent match with strong compatibility across multiple factors. Marriage is highly recommended."
        elif percentage >= 60:
            overall_status = "நல்ல பொருத்தம் (Good Match)"
            recommendation = "This is a good match with favorable compatibility. Marriage can proceed with confidence."
        elif percentage >= 40:
            overall_status = "நடுத்தர பொருத்தம் (Average Match)"
            recommendation = "This is an average match. Consult an experienced astrologer for detailed analysis and remedies."
        else:
            overall_status = "பொருத்தம் குறைவு (Below Average Match)"
            recommendation = "The compatibility is below average. Detailed consultation and remedies are strongly recommended before proceeding."
        
        return {
            'poruthams': poruthams,
            'total_points': round(total_points, 1),
            'max_points': max_points,
            'percentage': round(percentage, 1),
            'overall_status': overall_status,
            'recommendation': recommendation,
            'male_nakshatra': male_moon['nakshatra'],
            'female_nakshatra': female_moon['nakshatra'],
            'male_rasi': male_moon['rasi_name'],
            'female_rasi': female_moon['rasi_name']
        }
    
    def generate_predictions(self, positions: Dict, ascendant: Dict, dashas: List[Dict], 
                           yogas: List[Dict], doshas: List[Dict]) -> Dict:
        """Generate horoscope predictions based on chart analysis"""
        predictions = {
            'personality': [],
            'career': [],
            'relationships': [],
            'health': [],
            'wealth': [],
            'current_period': []
        }
        
        # Personality based on Ascendant
        lagna_lord = ascendant['lord']
        predictions['personality'].append({
            'factor': 'Ascendant',
            'description': f"Your rising sign is {ascendant['rasi_name']['en']} ({ascendant['rasi_name']['ta']}), ruled by {lagna_lord}. This shapes your outward personality and physical appearance."
        })
        
        # Sun sign for soul and ego
        if 'Sun' in positions:
            sun_rasi = positions['Sun']['rasi_name']
            predictions['personality'].append({
                'factor': 'Sun Sign',
                'description': f"Sun in {sun_rasi['en']} ({sun_rasi['ta']}) represents your soul, ego, and life purpose."
            })
        
        # Moon sign for mind and emotions
        if 'Moon' in positions:
            moon_rasi = positions['Moon']['rasi_name']
            nakshatra = positions['Moon']['nakshatra']
            predictions['personality'].append({
                'factor': 'Moon Sign',
                'description': f"Moon in {moon_rasi['en']} ({moon_rasi['ta']}) in {nakshatra} nakshatra governs your emotions, mind, and mother."
            })
        
        # Career predictions based on 10th house and its lord
        tenth_house_from_lagna = (ascendant['rasi'] + 9) % 12
        if tenth_house_from_lagna == 0:
            tenth_house_from_lagna = 12
        tenth_lord = self.RASI_LORDS[tenth_house_from_lagna]
        
        predictions['career'].append({
            'factor': '10th House',
            'description': f"Your 10th house of career is {self.RASI_NAMES[tenth_house_from_lagna]['en']}, ruled by {tenth_lord}. This planet influences your career path."
        })
        
        # Check if career planets are well-placed
        if 'Saturn' in positions:
            predictions['career'].append({
                'factor': 'Saturn',
                'description': f"Saturn in {positions['Saturn']['rasi_name']['en']} affects discipline, hard work, and career stability."
            })
        
        if 'Jupiter' in positions:
            predictions['career'].append({
                'factor': 'Jupiter',
                'description': f"Jupiter in {positions['Jupiter']['rasi_name']['en']} influences wisdom, teaching, and higher knowledge careers."
            })
        
        # Relationship predictions (7th house)
        seventh_house_from_lagna = (ascendant['rasi'] + 6) % 12
        if seventh_house_from_lagna == 0:
            seventh_house_from_lagna = 12
        seventh_lord = self.RASI_LORDS[seventh_house_from_lagna]
        
        predictions['relationships'].append({
            'factor': '7th House',
            'description': f"Your 7th house of marriage and partnerships is {self.RASI_NAMES[seventh_house_from_lagna]['en']}, ruled by {seventh_lord}."
        })
        
        if 'Venus' in positions:
            predictions['relationships'].append({
                'factor': 'Venus',
                'description': f"Venus in {positions['Venus']['rasi_name']['en']} governs love, romance, and relationships."
            })
        
        # Health predictions (6th house and malefics)
        if 'Mars' in positions:
            predictions['health'].append({
                'factor': 'Mars',
                'description': f"Mars in {positions['Mars']['rasi_name']['en']} affects energy levels, accidents, and surgeries. Maintain physical activity."
            })
        
        if 'Saturn' in positions:
            predictions['health'].append({
                'factor': 'Saturn',
                'description': f"Saturn in {positions['Saturn']['rasi_name']['en']} may indicate chronic conditions. Focus on bone health and discipline."
            })
        
        # Wealth predictions (2nd and 11th house)
        if 'Jupiter' in positions:
            predictions['wealth'].append({
                'factor': 'Jupiter',
                'description': f"Jupiter in {positions['Jupiter']['rasi_name']['en']} influences prosperity, wisdom-based wealth, and blessings."
            })
        
        # Current dasha period predictions
        if dashas and len(dashas) > 0:
            current_dasha = dashas[0]
            predictions['current_period'].append({
                'factor': 'Current Mahadasha',
                'description': f"You are in {current_dasha['planet']} Mahadasha until {current_dasha['end_date']}. This is a {current_dasha['years']:.1f} year period."
            })
            
            # Dasha-specific predictions
            dasha_planet = current_dasha['planet']
            if dasha_planet in positions:
                dasha_rasi = positions[dasha_planet]['rasi_name']['en']
                predictions['current_period'].append({
                    'factor': f'{dasha_planet} Dasha Effects',
                    'description': f"{dasha_planet} is placed in {dasha_rasi}. During this period, themes related to {dasha_planet} will be prominent in your life."
                })
        
        # Add yoga effects
        for yoga in yogas:
            if yoga['strength'] in ['Good', 'Excellent']:
                predictions['personality'].append({
                    'factor': yoga['name'],
                    'description': yoga['description']
                })
        
        return predictions
    
    def generate_birth_chart(self, birth_datetime: datetime, latitude: float, 
                            longitude: float, timezone_str: str) -> Dict:
        """Generate complete birth chart (Jathagam)"""
        
        # Convert to UTC
        tz = pytz.timezone(timezone_str)
        local_dt = tz.localize(birth_datetime)
        utc_dt = local_dt.astimezone(pytz.UTC)
        
        # Calculate all components
        positions = self.calculate_planetary_positions(utc_dt, latitude, longitude)
        ascendant = self.calculate_ascendant(utc_dt, latitude, longitude)
        houses = self.calculate_houses(ascendant['longitude'])
        dashas = self.calculate_vimshottari_dasha(positions['Moon']['longitude'], birth_datetime)
        yogas = self.calculate_yogas(positions, ascendant)
        doshas = self.calculate_doshas(positions, ascendant)
        predictions = self.generate_predictions(positions, ascendant, dashas, yogas, doshas)
        
        # Organize chart data
        chart = {
            'birth_info': {
                'datetime': birth_datetime.isoformat(),
                'timezone': timezone_str,
                'latitude': latitude,
                'longitude': longitude
            },
            'ascendant': ascendant,
            'planetary_positions': positions,
            'houses': houses,
            'vimshottari_dasha': dashas,
            'yogas': yogas,
            'doshas': doshas,
            'predictions': predictions,
            'chart_type': 'South Indian Style'
        }
        
        return chart


def get_astrology_engine() -> VedicAstrology:
    """Get singleton instance of astrology engine"""
    return VedicAstrology()
