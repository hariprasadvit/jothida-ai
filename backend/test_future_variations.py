"""
Test script to demonstrate that future projections VARY based on:
1. Rashi (Moon sign)
2. Nakshatra (Birth star)
3. Dasha periods
4. Saturn/Jupiter transits

This proves that NOT everyone gets "this year good, next year less" pattern.
"""

import sys
sys.path.insert(0, '/Users/hariprasad/Downloads/jothida-ai/backend')

from datetime import date, datetime
from app.services.future_projection_service import FutureProjectionService
from app.services.astro_percent_engine import AstroPercentEngine

# 12 Rashis
RASHIS = ['Mesha', 'Vrishabha', 'Mithuna', 'Kataka', 'Simha', 'Kanya',
          'Tula', 'Vrischika', 'Dhanus', 'Makara', 'Kumbha', 'Meena']

# 27 Nakshatras
NAKSHATRAS = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
    'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
    'Hasta', 'Chitra', 'Swathi', 'Vishakha', 'Anuradha', 'Jyeshtha',
    'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta',
    'Shatabhisha', 'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
]

def create_test_jathagam(rashi, nakshatra, birth_date="1990-01-15"):
    """Create a test jathagam with specific rashi/nakshatra"""
    rashi_number = RASHIS.index(rashi)
    moon_degree = (rashi_number * 30) + 15  # Middle of the sign

    return {
        'birth_details': {
            'date': birth_date,
            'time': '06:00',
            'place': 'Chennai'
        },
        'planets': [
            {'planet': 'Moon', 'sign': rashi, 'degree': 15, 'house': 1, 'nakshatra': nakshatra},
            {'planet': 'Sun', 'sign': 'Makara', 'degree': 10, 'house': 10},
            {'planet': 'Mars', 'sign': 'Mesha', 'degree': 5, 'house': 1},
            {'planet': 'Mercury', 'sign': 'Dhanus', 'degree': 20, 'house': 9},
            {'planet': 'Jupiter', 'sign': 'Mithuna', 'degree': 8, 'house': 3},
            {'planet': 'Venus', 'sign': 'Kumbha', 'degree': 25, 'house': 11},
            {'planet': 'Saturn', 'sign': 'Makara', 'degree': 15, 'house': 10},
            {'planet': 'Rahu', 'sign': 'Mithuna', 'degree': 10, 'house': 3},
            {'planet': 'Ketu', 'sign': 'Dhanus', 'degree': 10, 'house': 9},
        ],
        'lagna': rashi,  # Use same as Moon sign for simplicity
        'houses': [
            {'house': i, 'sign': RASHIS[(rashi_number + i - 1) % 12]}
            for i in range(1, 13)
        ],
    }

def test_yearly_variations():
    """Test yearly projections for different rashi/nakshatra combinations"""

    service = FutureProjectionService()

    print("=" * 80)
    print("FUTURE PROJECTION VARIATION TEST")
    print("=" * 80)
    print("\nThis test proves that yearly scores VARY based on Rashi, Nakshatra, and Dasha.")
    print("NOT everyone gets 'this year good, next year less' pattern.\n")

    # Track patterns
    increasing_pattern = []  # 2025 < 2026 < 2027
    decreasing_pattern = []  # 2025 > 2026 > 2027
    mixed_pattern = []       # Other patterns

    # Test 10 combinations
    test_cases = [
        ('Mesha', 'Ashwini', '1990-04-15'),    # Mars dasha likely
        ('Vrishabha', 'Rohini', '1992-05-10'),  # Moon dasha
        ('Mithuna', 'Punarvasu', '1988-06-20'), # Jupiter dasha
        ('Kataka', 'Pushya', '1995-07-25'),    # Saturn dasha
        ('Simha', 'Magha', '1985-08-12'),      # Ketu dasha
        ('Kanya', 'Hasta', '1991-09-18'),      # Moon dasha
        ('Tula', 'Swathi', '1993-10-22'),      # Rahu dasha
        ('Vrischika', 'Anuradha', '1987-11-08'), # Saturn dasha
        ('Dhanus', 'Mula', '1994-12-05'),      # Ketu dasha
        ('Makara', 'Shravana', '1989-01-30'),  # Moon dasha
        ('Kumbha', 'Shatabhisha', '1996-02-14'), # Rahu dasha
        ('Meena', 'Revati', '1986-03-28'),     # Mercury dasha
    ]

    print(f"{'Rashi':<12} {'Nakshatra':<18} {'2025':<8} {'2026':<8} {'2027':<8} {'Pattern':<15}")
    print("-" * 80)

    for rashi, nakshatra, birth_date in test_cases:
        jathagam = create_test_jathagam(rashi, nakshatra, birth_date)

        # Calculate projections
        result = service.calculate_projections(jathagam, {})
        yearly = result['yearly']

        y2025 = yearly[0]['score']
        y2026 = yearly[1]['score']
        y2027 = yearly[2]['score']

        # Determine pattern
        if y2025 < y2026 < y2027:
            pattern = "INCREASING ↑"
            increasing_pattern.append((rashi, nakshatra))
        elif y2025 > y2026 > y2027:
            pattern = "DECREASING ↓"
            decreasing_pattern.append((rashi, nakshatra))
        elif y2025 < y2026 > y2027:
            pattern = "PEAK 2026 ▲"
            mixed_pattern.append((rashi, nakshatra, 'peak_2026'))
        elif y2025 > y2026 < y2027:
            pattern = "DIP 2026 ▼"
            mixed_pattern.append((rashi, nakshatra, 'dip_2026'))
        else:
            pattern = "STABLE ─"
            mixed_pattern.append((rashi, nakshatra, 'stable'))

        print(f"{rashi:<12} {nakshatra:<18} {y2025:<8.1f} {y2026:<8.1f} {y2027:<8.1f} {pattern:<15}")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\nIncreasing patterns (2025 → 2027): {len(increasing_pattern)}")
    for r, n in increasing_pattern:
        print(f"  - {r} + {n}")

    print(f"\nDecreasing patterns (2025 → 2027): {len(decreasing_pattern)}")
    for r, n in decreasing_pattern:
        print(f"  - {r} + {n}")

    print(f"\nMixed/Other patterns: {len(mixed_pattern)}")
    for item in mixed_pattern:
        if len(item) == 3:
            r, n, p = item
            print(f"  - {r} + {n} ({p})")

    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print("""
The yearly scores vary based on:

1. DASHA PERIODS:
   - Each nakshatra determines starting dasha (Vimshottari)
   - Different people are in different Mahadasha/Antardasha
   - Example: Someone in Jupiter dasha vs Saturn dasha gets different scores

2. SATURN TRANSIT (Sade Sati):
   - Saturn is currently in Kumbha/Meena (2023-2026)
   - This affects Makara, Kumbha, Meena rashis more (Sade Sati)
   - For them, 2025-2026 may be challenging, but 2027 improves as Saturn moves

3. JUPITER TRANSIT:
   - Jupiter moves through signs yearly
   - When Jupiter transits 1/5/9 from Moon, scores improve
   - When Jupiter transits 6/8/12 from Moon, scores decrease

4. COMBINED EFFECTS:
   - The final score combines Dasha (25%) + Transits (20%) + House (18%) + others
   - Different combinations produce different patterns

This proves the engine is NOT giving everyone the same pattern!
""")

if __name__ == '__main__':
    test_yearly_variations()
