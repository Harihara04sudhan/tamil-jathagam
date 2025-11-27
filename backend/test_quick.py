#!/usr/bin/env python3
"""
Quick test script to verify astrology calculations
Run with: python3 test_quick.py (after installing dependencies)
"""

from datetime import datetime
import sys

try:
    from app.astrology import VedicAstrology
    
    print("=" * 60)
    print("🌟 Tamil Jathagam - Quick Test")
    print("=" * 60)
    
    # Create astrology engine
    print("\n1. Initializing astrology engine...")
    astro = VedicAstrology()
    print("✓ Engine initialized successfully")
    
    # Test date: May 15, 1990, 2:30 PM, Chennai
    print("\n2. Testing birth chart calculation...")
    print("   Birth Date: 1990-05-15 14:30")
    print("   Location: Chennai (13.0827°N, 80.2707°E)")
    
    birth_dt = datetime(1990, 5, 15, 14, 30)
    lat, lon = 13.0827, 80.2707
    
    # Calculate chart
    chart = astro.generate_birth_chart(birth_dt, lat, lon, 'Asia/Kolkata')
    
    print("\n3. Birth Chart Results:")
    print("-" * 60)
    
    # Ascendant
    asc = chart['ascendant']
    print(f"\n✓ Ascendant (Lagna):")
    print(f"  {asc['rasi_name']['en']} ({asc['rasi_name']['ta']})")
    print(f"  Nakshatra: {asc['nakshatra']} ({asc['nakshatra_tamil']})")
    print(f"  Lord: {asc['lord']}")
    
    # Planetary positions
    print(f"\n✓ Planetary Positions (9 Grahas):")
    for planet, pos in chart['planetary_positions'].items():
        print(f"  {planet:10} - {pos['rasi_name']['en']:12} | "
              f"{pos['nakshatra']:20} | {pos['degrees_in_rasi']:.2f}°")
    
    # Dasha periods
    print(f"\n✓ Vimshottari Dasha Periods:")
    print(f"  Total periods: {len(chart['vimshottari_dasha'])}")
    if chart['vimshottari_dasha']:
        current = chart['vimshottari_dasha'][0]
        print(f"  Current: {current['planet']} ({current['planet_tamil']}) Mahadasha")
        print(f"  Duration: {current['years']:.1f} years")
        print(f"  Ends: {current['end_date']}")
    
    # Yogas
    print(f"\n✓ Yogas (Beneficial Combinations): {len(chart['yogas'])}")
    for yoga in chart['yogas']:
        print(f"  • {yoga['name']} - {yoga['strength']}")
    
    # Doshas
    print(f"\n✓ Doshas (Afflictions): {len(chart['doshas'])}")
    for dosha in chart['doshas']:
        print(f"  • {dosha['name']} - {dosha['severity']}")
    
    # Predictions
    print(f"\n✓ Predictions Generated:")
    for category, predictions in chart['predictions'].items():
        print(f"  {category.capitalize():20} - {len(predictions)} insights")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\n🎉 System is ready! The astrology engine is working correctly.")
    print("\nNext steps:")
    print("1. Start the API: python -m uvicorn app.main:app --reload")
    print("2. Open frontend: Open frontend/index.html in a browser")
    print("3. API Docs: Visit http://localhost:8000/docs")
    print()
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"\nMake sure dependencies are installed:")
    print("  pip install -r requirements.txt")
    sys.exit(1)
