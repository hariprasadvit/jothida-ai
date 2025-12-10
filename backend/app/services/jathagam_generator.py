"""
Jathagam (Birth Chart) Generator Service
Calculates complete birth chart with planetary positions, houses, dashas
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Optional
import math

from app.services.ephemeris import EphemerisService, NAKSHATRAS, RASIS, PLANETS
import swisseph as swe


# City coordinates database (expand as needed)
CITY_COORDINATES = {
    "சென்னை": {"lat": 13.0827, "lon": 80.2707, "tz": "Asia/Kolkata"},
    "chennai": {"lat": 13.0827, "lon": 80.2707, "tz": "Asia/Kolkata"},
    "மதுரை": {"lat": 9.9252, "lon": 78.1198, "tz": "Asia/Kolkata"},
    "madurai": {"lat": 9.9252, "lon": 78.1198, "tz": "Asia/Kolkata"},
    "கோயம்புத்தூர்": {"lat": 11.0168, "lon": 76.9558, "tz": "Asia/Kolkata"},
    "coimbatore": {"lat": 11.0168, "lon": 76.9558, "tz": "Asia/Kolkata"},
    "திருச்சி": {"lat": 10.7905, "lon": 78.7047, "tz": "Asia/Kolkata"},
    "trichy": {"lat": 10.7905, "lon": 78.7047, "tz": "Asia/Kolkata"},
    "சேலம்": {"lat": 11.6643, "lon": 78.1460, "tz": "Asia/Kolkata"},
    "salem": {"lat": 11.6643, "lon": 78.1460, "tz": "Asia/Kolkata"},
    "திருநெல்வேலி": {"lat": 8.7139, "lon": 77.7567, "tz": "Asia/Kolkata"},
    "tirunelveli": {"lat": 8.7139, "lon": 77.7567, "tz": "Asia/Kolkata"},
    "ஈரோடு": {"lat": 11.3410, "lon": 77.7172, "tz": "Asia/Kolkata"},
    "erode": {"lat": 11.3410, "lon": 77.7172, "tz": "Asia/Kolkata"},
    "வேலூர்": {"lat": 12.9165, "lon": 79.1325, "tz": "Asia/Kolkata"},
    "vellore": {"lat": 12.9165, "lon": 79.1325, "tz": "Asia/Kolkata"},
    "தஞ்சாவூர்": {"lat": 10.7870, "lon": 79.1378, "tz": "Asia/Kolkata"},
    "thanjavur": {"lat": 10.7870, "lon": 79.1378, "tz": "Asia/Kolkata"},
    "திண்டுக்கல்": {"lat": 10.3624, "lon": 77.9695, "tz": "Asia/Kolkata"},
    "dindigul": {"lat": 10.3624, "lon": 77.9695, "tz": "Asia/Kolkata"},
    "bangalore": {"lat": 12.9716, "lon": 77.5946, "tz": "Asia/Kolkata"},
    "mumbai": {"lat": 19.0760, "lon": 72.8777, "tz": "Asia/Kolkata"},
    "delhi": {"lat": 28.6139, "lon": 77.2090, "tz": "Asia/Kolkata"},
    "hyderabad": {"lat": 17.3850, "lon": 78.4867, "tz": "Asia/Kolkata"},
}

# Vimshottari Dasha periods in years
DASHA_PERIODS = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17,
}

# Dasha lord order
DASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]


class JathagamGenerator:
    """
    Generate complete birth chart (Jathagam) with:
    - Planetary positions in sidereal zodiac
    - Lagna (Ascendant) calculation
    - House placements
    - Vimshottari Dasha
    - Yogas (planetary combinations)
    """

    def __init__(self, ephemeris: EphemerisService):
        self.ephemeris = ephemeris

    def get_coordinates(self, place: str) -> Dict:
        """Get coordinates for a place name"""
        place_lower = place.lower().strip()
        if place_lower in CITY_COORDINATES:
            return CITY_COORDINATES[place_lower]
        # Check Tamil names
        for name, coords in CITY_COORDINATES.items():
            if place in name or name in place:
                return coords
        # Default to Chennai if not found
        return CITY_COORDINATES["chennai"]

    def generate(self, birth_details) -> Dict:
        """Generate complete birth chart"""
        # Parse birth datetime
        birth_date = datetime.strptime(birth_details.date, "%Y-%m-%d")
        time_parts = birth_details.time.split(":")
        birth_hour = int(time_parts[0])
        birth_minute = int(time_parts[1]) if len(time_parts) > 1 else 0

        birth_dt = datetime(
            birth_date.year, birth_date.month, birth_date.day,
            birth_hour, birth_minute, 0
        )

        # Get coordinates
        if hasattr(birth_details, 'latitude') and birth_details.latitude:
            lat = birth_details.latitude
            lon = birth_details.longitude
        else:
            coords = self.get_coordinates(birth_details.place)
            lat = coords["lat"]
            lon = coords["lon"]

        # Convert to Julian Day
        jd = self.ephemeris.datetime_to_jd(birth_dt)

        # Calculate Lagna (Ascendant)
        lagna = self._calculate_lagna(jd, lat, lon)

        # Get all planet positions
        planets = self.ephemeris.get_all_planets(jd)

        # Calculate strength for each planet
        for planet in planets:
            planet["strength"] = self.ephemeris.calculate_planet_strength(planet, jd)
            planet["trend"] = self._calculate_trend(planet)

        # Build Rasi chart (12 houses)
        rasi_chart = self._build_rasi_chart(planets, lagna)

        # Build Navamsa chart
        navamsa_chart = self._build_navamsa_chart(planets, lagna)

        # Calculate Vimshottari Dasha
        moon = next(p for p in planets if p["name"] == "Moon")
        dasha = self._calculate_vimshottari_dasha(moon, birth_dt)

        # Detect Yogas
        yogas = self._detect_yogas(planets, lagna)

        # Calculate overall strength
        overall_strength = sum(p["strength"] for p in planets) / len(planets)

        # Format planets for response
        formatted_planets = []
        for p in planets:
            formatted_planets.append({
                "planet": p["name"],
                "tamil_name": p["tamil_name"],
                "symbol": p["symbol"],
                "rasi": p["rasi"],
                "rasi_tamil": p["rasi_tamil"],
                "degree": round(p["degree_in_rasi"], 2),
                "nakshatra": p["nakshatra_tamil"],
                "nakshatra_pada": p["nakshatra_pada"],
                "is_retrograde": p["is_retrograde"],
                "strength": round(p["strength"], 1),
                "trend": p["trend"]
            })

        return {
            "name": birth_details.name,
            "birth_details": {
                "date": birth_details.date,
                "time": birth_details.time,
                "place": birth_details.place,
                "latitude": lat,
                "longitude": lon
            },
            "planets": formatted_planets,
            "lagna": {
                "rasi": lagna["rasi"],
                "rasi_tamil": lagna["rasi_tamil"],
                "degree": round(lagna["degree"], 2),
                "nakshatra": lagna["nakshatra_tamil"],
                "nakshatra_pada": lagna["nakshatra_pada"]
            },
            "moon_sign": {
                "rasi": moon["rasi"],
                "rasi_tamil": moon["rasi_tamil"],
                "nakshatra": moon["nakshatra_tamil"],
                "nakshatra_pada": moon["nakshatra_pada"]
            },
            "rasi_chart": rasi_chart,
            "navamsa_chart": navamsa_chart,
            "dasha": dasha,
            "overall_strength": round(overall_strength, 1),
            "yogas": yogas
        }

    def _calculate_lagna(self, jd: float, lat: float, lon: float) -> Dict:
        """Calculate Ascendant (Lagna)"""
        # Get houses using Placidus system
        cusps, ascmc = swe.houses(jd, lat, lon, b'P')

        # Get ayanamsha
        ayanamsha = self.ephemeris.get_ayanamsha(jd)

        # Convert to sidereal
        asc_tropical = ascmc[0]
        asc_sidereal = (asc_tropical - ayanamsha) % 360

        # Calculate rasi and nakshatra
        rasi_index = int(asc_sidereal / 30)
        nakshatra_index = int(asc_sidereal / (360/27))
        nakshatra_pada = int((asc_sidereal % (360/27)) / (360/108)) + 1

        return {
            "longitude": asc_sidereal,
            "degree": asc_sidereal % 30,
            "rasi_index": rasi_index,
            "rasi": RASIS[rasi_index]["name"],
            "rasi_tamil": RASIS[rasi_index]["tamil"],
            "nakshatra_index": nakshatra_index,
            "nakshatra": NAKSHATRAS[nakshatra_index]["name"],
            "nakshatra_tamil": NAKSHATRAS[nakshatra_index]["tamil"],
            "nakshatra_pada": nakshatra_pada
        }

    def _calculate_trend(self, planet: Dict) -> str:
        """Calculate trend based on planet strength"""
        strength = planet["strength"]
        if strength >= 70:
            return "up"
        elif strength <= 40:
            return "down"
        return "neutral"

    def _build_rasi_chart(self, planets: List[Dict], lagna: Dict) -> List[List[str]]:
        """Build 12-house Rasi chart starting from Lagna"""
        chart = [[] for _ in range(12)]

        # Add Lagna marker
        lagna_house = 0
        chart[lagna_house].append("Lg")

        # Place planets in houses relative to Lagna
        for planet in planets:
            # House = planet's rasi - lagna's rasi (mod 12)
            house = (planet["rasi_index"] - lagna["rasi_index"]) % 12
            chart[house].append(planet["symbol"])

        return chart

    def _build_navamsa_chart(self, planets: List[Dict], lagna: Dict) -> List[List[str]]:
        """Build Navamsa (D9) chart"""
        chart = [[] for _ in range(12)]

        def get_navamsa_rasi(longitude: float) -> int:
            """Calculate Navamsa rasi from longitude"""
            rasi = int(longitude / 30)
            degree_in_rasi = longitude % 30
            navamsa_num = int(degree_in_rasi / (30/9))

            # Navamsa starting rasi depends on the rasi type
            # Fire signs (0,4,8) start from Aries (0)
            # Earth signs (1,5,9) start from Capricorn (9)
            # Air signs (2,6,10) start from Libra (6)
            # Water signs (3,7,11) start from Cancer (3)

            if rasi % 4 == 0:  # Fire
                start = 0
            elif rasi % 4 == 1:  # Earth
                start = 9
            elif rasi % 4 == 2:  # Air
                start = 6
            else:  # Water
                start = 3

            return (start + navamsa_num) % 12

        # Calculate Navamsa Lagna
        navamsa_lagna = get_navamsa_rasi(lagna["longitude"])
        chart[0].append("Lg")

        # Place planets
        for planet in planets:
            navamsa_rasi = get_navamsa_rasi(planet["longitude"])
            house = (navamsa_rasi - navamsa_lagna) % 12
            chart[house].append(planet["symbol"])

        return chart

    def _calculate_vimshottari_dasha(self, moon: Dict, birth_dt: datetime) -> Dict:
        """Calculate Vimshottari Dasha periods"""
        nakshatra_index = moon["nakshatra_index"]
        nakshatra_lord = NAKSHATRAS[nakshatra_index]["lord"]

        # Find starting dasha
        dasha_start_index = DASHA_ORDER.index(nakshatra_lord)

        # Calculate elapsed portion of first dasha based on Moon's position
        nakshatra_span = 360 / 27
        moon_pos_in_nakshatra = moon["longitude"] % nakshatra_span
        elapsed_fraction = moon_pos_in_nakshatra / nakshatra_span

        # Calculate dasha periods
        dasha_periods = []
        current_date = birth_dt

        # First (balance) dasha
        first_dasha_lord = nakshatra_lord
        first_dasha_total_years = DASHA_PERIODS[first_dasha_lord]
        first_dasha_remaining = first_dasha_total_years * (1 - elapsed_fraction)

        end_date = current_date + timedelta(days=first_dasha_remaining * 365.25)
        dasha_periods.append({
            "lord": first_dasha_lord,
            "tamil_lord": self._get_tamil_planet_name(first_dasha_lord),
            "start": current_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d"),
            "years": round(first_dasha_remaining, 2),
            "is_current": current_date <= datetime.now() <= end_date
        })
        current_date = end_date

        # Remaining dashas (cycle through)
        for i in range(1, 9):
            lord = DASHA_ORDER[(dasha_start_index + i) % 9]
            years = DASHA_PERIODS[lord]
            end_date = current_date + timedelta(days=years * 365.25)

            is_current = current_date <= datetime.now() <= end_date

            dasha_periods.append({
                "lord": lord,
                "tamil_lord": self._get_tamil_planet_name(lord),
                "start": current_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
                "years": years,
                "is_current": is_current
            })
            current_date = end_date

        # Find current dasha
        current_dasha = next((d for d in dasha_periods if d["is_current"]), dasha_periods[0])

        return {
            "current": current_dasha,
            "all_periods": dasha_periods
        }

    def _get_tamil_planet_name(self, planet_name: str) -> str:
        """Get Tamil name for planet"""
        tamil_names = {
            "Sun": "சூரியன்", "Moon": "சந்திரன்", "Mars": "செவ்வாய்",
            "Mercury": "புதன்", "Jupiter": "குரு", "Venus": "சுக்கிரன்",
            "Saturn": "சனி", "Rahu": "ராகு", "Ketu": "கேது"
        }
        return tamil_names.get(planet_name, planet_name)

    def _detect_yogas(self, planets: List[Dict], lagna: Dict) -> List[Dict]:
        """Detect important Yogas in the chart"""
        yogas = []

        # Get planet positions by name
        planet_dict = {p["name"]: p for p in planets}

        # Gajakesari Yoga: Jupiter in kendra from Moon
        moon_rasi = planet_dict["Moon"]["rasi_index"]
        jupiter_rasi = planet_dict["Jupiter"]["rasi_index"]
        jupiter_from_moon = (jupiter_rasi - moon_rasi) % 12

        if jupiter_from_moon in [0, 3, 6, 9]:  # Kendra houses
            yogas.append({
                "name": "Gajakesari Yoga",
                "tamil_name": "கஜகேசரி யோகம்",
                "description": "குரு சந்திரனிலிருந்து கேந்திரத்தில் உள்ளார்",
                "effect": "புகழ், செல்வம், நல்ல பேச்சு திறன்",
                "strength": 85
            })

        # Budhaditya Yoga: Sun and Mercury in same sign
        if planet_dict["Sun"]["rasi_index"] == planet_dict["Mercury"]["rasi_index"]:
            yogas.append({
                "name": "Budhaditya Yoga",
                "tamil_name": "புதாதித்ய யோகம்",
                "description": "சூரியனும் புதனும் ஒரே ராசியில்",
                "effect": "நல்ல புத்திசாலித்தனம், தொழிலில் வெற்றி",
                "strength": 75
            })

        # Chandra-Mangala Yoga: Moon and Mars together or mutual aspect
        if planet_dict["Moon"]["rasi_index"] == planet_dict["Mars"]["rasi_index"]:
            yogas.append({
                "name": "Chandra-Mangala Yoga",
                "tamil_name": "சந்திர-மங்கள யோகம்",
                "description": "சந்திரனும் செவ்வாயும் சேர்க்கை",
                "effect": "செல்வம், துணிச்சல், தொழில் வெற்றி",
                "strength": 70
            })

        # Hamsa Yoga: Jupiter in own sign or exalted in kendra
        jupiter_in_kendra = (jupiter_rasi - lagna["rasi_index"]) % 12 in [0, 3, 6, 9]
        jupiter_strong = jupiter_rasi in [8, 11, 3]  # Sagittarius, Pisces, Cancer

        if jupiter_in_kendra and jupiter_strong:
            yogas.append({
                "name": "Hamsa Yoga",
                "tamil_name": "ஹம்ச யோகம்",
                "description": "குரு கேந்திரத்தில் பலமாக உள்ளார்",
                "effect": "ஆன்மீக சிந்தனை, கல்வி, நல்ல குணம்",
                "strength": 90
            })

        # Lakshmi Yoga: Venus in own/exalted sign in kendra/trikona
        venus_rasi = planet_dict["Venus"]["rasi_index"]
        venus_from_lagna = (venus_rasi - lagna["rasi_index"]) % 12
        venus_strong = venus_rasi in [1, 6, 11]  # Taurus, Libra, Pisces
        venus_good_house = venus_from_lagna in [0, 3, 4, 6, 8, 9]

        if venus_strong and venus_good_house:
            yogas.append({
                "name": "Lakshmi Yoga",
                "tamil_name": "லக்ஷ்மி யோகம்",
                "description": "சுக்கிரன் சுபஸ்தானத்தில் பலமாக",
                "effect": "செல்வம், அழகு, இல்லற சுகம்",
                "strength": 85
            })

        # If no special yogas found
        if not yogas:
            yogas.append({
                "name": "சாதாரண ஜாதகம்",
                "tamil_name": "சாதாரண ஜாதகம்",
                "description": "பெரிய யோகங்கள் இல்லை",
                "effect": "சராசரி வாழ்க்கை",
                "strength": 50
            })

        return yogas

    def get_profile_summary(self, birth_details) -> Dict:
        """
        Calculate user profile summary with Moon Rasi, Nakshatra, and current Dasha.
        Returns data for the UserProfileBanner component.
        """
        # Parse birth datetime
        birth_date = datetime.strptime(birth_details.date, "%Y-%m-%d")
        time_parts = birth_details.time.split(":")
        birth_hour = int(time_parts[0])
        birth_minute = int(time_parts[1]) if len(time_parts) > 1 else 0

        birth_dt = datetime(
            birth_date.year, birth_date.month, birth_date.day,
            birth_hour, birth_minute, 0
        )

        # Get coordinates
        if hasattr(birth_details, 'latitude') and birth_details.latitude:
            lat = birth_details.latitude
            lon = birth_details.longitude
        else:
            coords = self.get_coordinates(birth_details.place)
            lat = coords["lat"]
            lon = coords["lon"]

        # Convert to Julian Day
        jd = self.ephemeris.datetime_to_jd(birth_dt)

        # Get Moon position for Rasi and Nakshatra
        moon = self.ephemeris.get_planet_position(1, jd)  # 1 = Moon

        # Calculate nakshatra details
        moon_longitude = moon["longitude"]
        nakshatra_span = 360 / 27
        nakshatra_index = int(moon_longitude / nakshatra_span)
        nakshatra_pos_in_pada = (moon_longitude % nakshatra_span) / (nakshatra_span / 4)
        nakshatra_pada = int(nakshatra_pos_in_pada) + 1

        # Get nakshatra lord for dasha calculation
        nakshatra_lord = NAKSHATRAS[nakshatra_index]["lord"]

        # Calculate Vimshottari Dasha with Antar Dasha
        dasha_info = self._calculate_full_dasha(moon_longitude, birth_dt)

        # Rasi details
        rasi_index = int(moon_longitude / 30)

        return {
            "name": birth_details.name,
            "moon_rasi": {
                "index": rasi_index,
                "name": RASIS[rasi_index]["name"],
                "tamil": RASIS[rasi_index]["tamil"],
                "symbol": RASIS[rasi_index].get("symbol", "")
            },
            "nakshatra": {
                "index": nakshatra_index,
                "name": NAKSHATRAS[nakshatra_index]["name"],
                "tamil": NAKSHATRAS[nakshatra_index]["tamil"],
                "pada": nakshatra_pada,
                "lord": nakshatra_lord,
                "lord_tamil": self._get_tamil_planet_name(nakshatra_lord)
            },
            "current_dasha": {
                "mahadasha": dasha_info["mahadasha"]["lord"],
                "mahadasha_tamil": dasha_info["mahadasha"]["tamil_lord"],
                "mahadasha_end": dasha_info["mahadasha"]["end"],
                "mahadasha_remaining_years": dasha_info["mahadasha"]["remaining_years"],
                "antardasha": dasha_info["antardasha"]["lord"],
                "antardasha_tamil": dasha_info["antardasha"]["tamil_lord"],
                "antardasha_end": dasha_info["antardasha"]["end"],
                "antardasha_remaining_months": dasha_info["antardasha"]["remaining_months"]
            },
            "birth_details": {
                "date": birth_details.date,
                "time": birth_details.time,
                "place": birth_details.place
            }
        }

    def _calculate_full_dasha(self, moon_longitude: float, birth_dt: datetime) -> Dict:
        """
        Calculate complete Vimshottari Dasha with current Maha Dasha and Antar Dasha.
        Uses the proper nakshatra-based starting dasha.
        """
        # Nakshatra lord determines starting dasha
        nakshatra_span = 360 / 27
        nakshatra_index = int(moon_longitude / nakshatra_span)
        nakshatra_lord = NAKSHATRAS[nakshatra_index]["lord"]

        # Position within nakshatra determines elapsed portion
        moon_pos_in_nakshatra = moon_longitude % nakshatra_span
        elapsed_fraction = moon_pos_in_nakshatra / nakshatra_span

        # Find starting dasha index
        dasha_start_index = DASHA_ORDER.index(nakshatra_lord)

        # Calculate the balance of first dasha at birth
        first_dasha_total_years = DASHA_PERIODS[nakshatra_lord]
        first_dasha_balance = first_dasha_total_years * (1 - elapsed_fraction)

        # Build dasha timeline from birth
        dasha_timeline = []
        current_date = birth_dt

        # First (balance) dasha
        end_date = current_date + timedelta(days=first_dasha_balance * 365.25)
        dasha_timeline.append({
            "lord": nakshatra_lord,
            "tamil_lord": self._get_tamil_planet_name(nakshatra_lord),
            "start": current_date,
            "end": end_date,
            "years": first_dasha_balance
        })
        current_date = end_date

        # Remaining 8 dashas
        for i in range(1, 9):
            lord = DASHA_ORDER[(dasha_start_index + i) % 9]
            years = DASHA_PERIODS[lord]
            end_date = current_date + timedelta(days=years * 365.25)
            dasha_timeline.append({
                "lord": lord,
                "tamil_lord": self._get_tamil_planet_name(lord),
                "start": current_date,
                "end": end_date,
                "years": years
            })
            current_date = end_date

        # Find current Maha Dasha
        now = datetime.now()
        current_mahadasha = None

        for dasha in dasha_timeline:
            if dasha["start"] <= now <= dasha["end"]:
                current_mahadasha = dasha
                break

        # If not found (date is beyond timeline), use last dasha or cycle
        if not current_mahadasha:
            # Extend timeline if needed (120-year cycle repeats)
            total_cycle_days = 120 * 365.25
            days_from_birth = (now - birth_dt).days
            cycle_position = days_from_birth % total_cycle_days

            check_date = birth_dt + timedelta(days=cycle_position)
            for dasha in dasha_timeline:
                adjusted_start = dasha["start"]
                adjusted_end = dasha["end"]
                # Check within first cycle
                if adjusted_start <= check_date <= adjusted_end:
                    # Recalculate actual dates for current cycle
                    cycle_num = int(days_from_birth / total_cycle_days)
                    cycle_offset = timedelta(days=cycle_num * total_cycle_days)
                    current_mahadasha = {
                        "lord": dasha["lord"],
                        "tamil_lord": dasha["tamil_lord"],
                        "start": dasha["start"] + cycle_offset,
                        "end": dasha["end"] + cycle_offset,
                        "years": dasha["years"]
                    }
                    break

        if not current_mahadasha:
            current_mahadasha = dasha_timeline[0]

        # Calculate remaining years in Maha Dasha
        mahadasha_remaining_days = (current_mahadasha["end"] - now).days
        mahadasha_remaining_years = round(mahadasha_remaining_days / 365.25, 1)

        # Calculate Antar Dasha within current Maha Dasha
        antardasha_info = self._calculate_antardasha(current_mahadasha, now)

        return {
            "mahadasha": {
                "lord": current_mahadasha["lord"],
                "tamil_lord": current_mahadasha["tamil_lord"],
                "start": current_mahadasha["start"].strftime("%Y-%m-%d"),
                "end": current_mahadasha["end"].strftime("%Y-%m-%d"),
                "remaining_years": max(0, mahadasha_remaining_years)
            },
            "antardasha": antardasha_info
        }

    def _calculate_antardasha(self, mahadasha: Dict, current_date: datetime) -> Dict:
        """
        Calculate current Antar Dasha within a Maha Dasha.
        Antar dasha periods are proportional to their Maha Dasha periods.
        """
        mahadasha_lord = mahadasha["lord"]
        mahadasha_years = mahadasha["years"]
        mahadasha_start = mahadasha["start"]
        mahadasha_end = mahadasha["end"]

        # Total days in this Maha Dasha
        total_maha_days = (mahadasha_end - mahadasha_start).days

        # Find the starting index for Antar Dasha sequence
        # Antar Dasha sequence starts from the Maha Dasha lord
        maha_index = DASHA_ORDER.index(mahadasha_lord)

        # Calculate each Antar Dasha period
        antardasha_timeline = []
        current_antar_start = mahadasha_start

        for i in range(9):
            antar_lord = DASHA_ORDER[(maha_index + i) % 9]
            antar_years = DASHA_PERIODS[antar_lord]

            # Proportion of Maha Dasha = (Antar period / 120) * Maha period
            antar_proportion = (antar_years / 120) * mahadasha_years
            antar_days = antar_proportion * 365.25

            antar_end = current_antar_start + timedelta(days=antar_days)

            antardasha_timeline.append({
                "lord": antar_lord,
                "tamil_lord": self._get_tamil_planet_name(antar_lord),
                "start": current_antar_start,
                "end": antar_end,
                "months": round(antar_days / 30.44, 1)
            })

            current_antar_start = antar_end

        # Find current Antar Dasha
        current_antardasha = None
        for antar in antardasha_timeline:
            if antar["start"] <= current_date <= antar["end"]:
                current_antardasha = antar
                break

        if not current_antardasha:
            current_antardasha = antardasha_timeline[0]

        # Calculate remaining months
        remaining_days = (current_antardasha["end"] - current_date).days
        remaining_months = round(remaining_days / 30.44, 1)

        return {
            "lord": current_antardasha["lord"],
            "tamil_lord": current_antardasha["tamil_lord"],
            "start": current_antardasha["start"].strftime("%Y-%m-%d"),
            "end": current_antardasha["end"].strftime("%Y-%m-%d"),
            "remaining_months": max(0, remaining_months)
        }

    def get_life_areas(self, birth_details) -> Dict:
        """Calculate life area scores based on birth chart and current transits"""
        jathagam = self.generate(birth_details)

        # Get current transit positions
        now = datetime.now()
        jd_now = self.ephemeris.datetime_to_jd(now)
        current_planets = self.ephemeris.get_all_planets(jd_now)

        # Calculate scores for each life area
        # Based on relevant house lords and transits

        # Love: 7th house, Venus
        venus_birth = next(p for p in jathagam["planets"] if p["planet"] == "Venus")
        venus_transit = next(p for p in current_planets if p["name"] == "Venus")
        love_score = (venus_birth["strength"] + self.ephemeris.calculate_planet_strength(venus_transit, jd_now)) / 2

        # Career: 10th house, Saturn, Sun
        saturn_birth = next(p for p in jathagam["planets"] if p["planet"] == "Saturn")
        sun_birth = next(p for p in jathagam["planets"] if p["planet"] == "Sun")
        career_score = (saturn_birth["strength"] + sun_birth["strength"]) / 2

        # Education: 5th house, Jupiter, Mercury
        jupiter_birth = next(p for p in jathagam["planets"] if p["planet"] == "Jupiter")
        mercury_birth = next(p for p in jathagam["planets"] if p["planet"] == "Mercury")
        education_score = (jupiter_birth["strength"] + mercury_birth["strength"]) / 2

        # Family: 4th house, Moon
        moon_birth = next(p for p in jathagam["planets"] if p["planet"] == "Moon")
        family_score = moon_birth["strength"]

        return {
            "love": {
                "name": "காதல்",
                "score": round(love_score, 1),
                "status": "நல்லது" if love_score >= 60 else "சாதாரணம்"
            },
            "career": {
                "name": "தொழில்",
                "score": round(career_score, 1),
                "status": "நல்லது" if career_score >= 60 else "சாதாரணம்"
            },
            "education": {
                "name": "கல்வி",
                "score": round(education_score, 1),
                "status": "நல்லது" if education_score >= 60 else "சாதாரணம்"
            },
            "family": {
                "name": "குடும்பம்",
                "score": round(family_score, 1),
                "status": "நல்லது" if family_score >= 60 else "சாதாரணம்"
            }
        }
