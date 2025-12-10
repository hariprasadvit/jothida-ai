"""
Ephemeris Service
Core astronomical calculations using Swiss Ephemeris
"""

import swisseph as swe
from datetime import datetime, date, timedelta
from typing import Dict, List, Tuple, Optional
import math
from zoneinfo import ZoneInfo

# Constants
PLANETS = {
    swe.SUN: {"name": "Sun", "tamil": "சூரியன்", "symbol": "☉"},
    swe.MOON: {"name": "Moon", "tamil": "சந்திரன்", "symbol": "☽"},
    swe.MARS: {"name": "Mars", "tamil": "செவ்வாய்", "symbol": "♂"},
    swe.MERCURY: {"name": "Mercury", "tamil": "புதன்", "symbol": "☿"},
    swe.JUPITER: {"name": "Jupiter", "tamil": "குரு", "symbol": "♃"},
    swe.VENUS: {"name": "Venus", "tamil": "சுக்கிரன்", "symbol": "♀"},
    swe.SATURN: {"name": "Saturn", "tamil": "சனி", "symbol": "♄"},
    swe.TRUE_NODE: {"name": "Rahu", "tamil": "ராகு", "symbol": "☊"},
}

RASIS = [
    {"name": "Aries", "tamil": "மேஷம்", "lord": swe.MARS},
    {"name": "Taurus", "tamil": "ரிஷபம்", "lord": swe.VENUS},
    {"name": "Gemini", "tamil": "மிதுனம்", "lord": swe.MERCURY},
    {"name": "Cancer", "tamil": "கடகம்", "lord": swe.MOON},
    {"name": "Leo", "tamil": "சிம்மம்", "lord": swe.SUN},
    {"name": "Virgo", "tamil": "கன்னி", "lord": swe.MERCURY},
    {"name": "Libra", "tamil": "துலாம்", "lord": swe.VENUS},
    {"name": "Scorpio", "tamil": "விருச்சிகம்", "lord": swe.MARS},
    {"name": "Sagittarius", "tamil": "தனுசு", "lord": swe.JUPITER},
    {"name": "Capricorn", "tamil": "மகரம்", "lord": swe.SATURN},
    {"name": "Aquarius", "tamil": "கும்பம்", "lord": swe.SATURN},
    {"name": "Pisces", "tamil": "மீனம்", "lord": swe.JUPITER},
]

NAKSHATRAS = [
    {"name": "Ashwini", "tamil": "அஸ்வினி", "lord": "Ketu"},
    {"name": "Bharani", "tamil": "பரணி", "lord": "Venus"},
    {"name": "Krittika", "tamil": "கார்த்திகை", "lord": "Sun"},
    {"name": "Rohini", "tamil": "ரோகிணி", "lord": "Moon"},
    {"name": "Mrigashira", "tamil": "மிருகசீரிடம்", "lord": "Mars"},
    {"name": "Ardra", "tamil": "திருவாதிரை", "lord": "Rahu"},
    {"name": "Punarvasu", "tamil": "புனர்பூசம்", "lord": "Jupiter"},
    {"name": "Pushya", "tamil": "பூசம்", "lord": "Saturn"},
    {"name": "Ashlesha", "tamil": "ஆயில்யம்", "lord": "Mercury"},
    {"name": "Magha", "tamil": "மகம்", "lord": "Ketu"},
    {"name": "Purva Phalguni", "tamil": "பூரம்", "lord": "Venus"},
    {"name": "Uttara Phalguni", "tamil": "உத்திரம்", "lord": "Sun"},
    {"name": "Hasta", "tamil": "ஹஸ்தம்", "lord": "Moon"},
    {"name": "Chitra", "tamil": "சித்திரை", "lord": "Mars"},
    {"name": "Swati", "tamil": "சுவாதி", "lord": "Rahu"},
    {"name": "Vishakha", "tamil": "விசாகம்", "lord": "Jupiter"},
    {"name": "Anuradha", "tamil": "அனுஷம்", "lord": "Saturn"},
    {"name": "Jyeshtha", "tamil": "கேட்டை", "lord": "Mercury"},
    {"name": "Mula", "tamil": "மூலம்", "lord": "Ketu"},
    {"name": "Purva Ashadha", "tamil": "பூராடம்", "lord": "Venus"},
    {"name": "Uttara Ashadha", "tamil": "உத்திராடம்", "lord": "Sun"},
    {"name": "Shravana", "tamil": "திருவோணம்", "lord": "Moon"},
    {"name": "Dhanishta", "tamil": "அவிட்டம்", "lord": "Mars"},
    {"name": "Shatabhisha", "tamil": "சதயம்", "lord": "Rahu"},
    {"name": "Purva Bhadrapada", "tamil": "பூரட்டாதி", "lord": "Jupiter"},
    {"name": "Uttara Bhadrapada", "tamil": "உத்திரட்டாதி", "lord": "Saturn"},
    {"name": "Revati", "tamil": "ரேவதி", "lord": "Mercury"},
]

# Lahiri Ayanamsha for Vedic calculations
AYANAMSHA = swe.SIDM_LAHIRI


class EphemerisService:
    """
    Core service for all astronomical calculations
    Uses Swiss Ephemeris with Lahiri Ayanamsha
    """
    
    def __init__(self, ephe_path: str = None):
        """Initialize ephemeris with data files path"""
        if ephe_path:
            swe.set_ephe_path(ephe_path)
        swe.set_sid_mode(AYANAMSHA)
    
    def datetime_to_jd(self, dt: datetime, timezone: str = "Asia/Kolkata") -> float:
        """
        Convert datetime to Julian Day.
        Swiss Ephemeris requires Universal Time (UT/UTC).
        If the datetime is naive (no timezone), it's assumed to be in the specified timezone.
        """
        if dt.tzinfo is None:
            # Naive datetime - assume it's in the specified timezone (default: IST)
            local_tz = ZoneInfo(timezone)
            dt = dt.replace(tzinfo=local_tz)

        # Convert to UTC
        utc_dt = dt.astimezone(ZoneInfo("UTC"))

        return swe.julday(
            utc_dt.year, utc_dt.month, utc_dt.day,
            utc_dt.hour + utc_dt.minute/60 + utc_dt.second/3600
        )
    
    def get_ayanamsha(self, jd: float) -> float:
        """Get Lahiri Ayanamsha for given Julian Day"""
        return swe.get_ayanamsa(jd)
    
    def get_planet_position(self, planet_id: int, jd: float) -> Dict:
        """
        Get sidereal position of a planet
        Returns longitude, latitude, speed, and derived info
        """
        # Get tropical position
        result = swe.calc_ut(jd, planet_id)
        tropical_lon = result[0][0]
        lat = result[0][1]
        speed = result[0][3]
        
        # Convert to sidereal
        ayanamsha = self.get_ayanamsha(jd)
        sidereal_lon = (tropical_lon - ayanamsha) % 360
        
        # Calculate Rasi and Nakshatra
        rasi_index = int(sidereal_lon / 30)
        nakshatra_index = int(sidereal_lon / (360/27))
        nakshatra_pada = int((sidereal_lon % (360/27)) / (360/108)) + 1
        
        # Is retrograde?
        is_retrograde = speed < 0
        
        planet_info = PLANETS.get(planet_id, {"name": "Unknown", "tamil": "Unknown", "symbol": "?"})
        
        return {
            "planet_id": planet_id,
            "name": planet_info["name"],
            "tamil_name": planet_info["tamil"],
            "symbol": planet_info["symbol"],
            "longitude": sidereal_lon,
            "latitude": lat,
            "speed": speed,
            "is_retrograde": is_retrograde,
            "rasi_index": rasi_index,
            "rasi": RASIS[rasi_index]["name"],
            "rasi_tamil": RASIS[rasi_index]["tamil"],
            "nakshatra_index": nakshatra_index,
            "nakshatra": NAKSHATRAS[nakshatra_index]["name"],
            "nakshatra_tamil": NAKSHATRAS[nakshatra_index]["tamil"],
            "nakshatra_pada": nakshatra_pada,
            "degree_in_rasi": sidereal_lon % 30,
        }
    
    def get_all_planets(self, jd: float) -> List[Dict]:
        """Get positions of all 9 planets (including Rahu/Ketu)"""
        planets = []
        
        for planet_id in PLANETS.keys():
            planets.append(self.get_planet_position(planet_id, jd))
        
        # Add Ketu (opposite of Rahu)
        rahu = next(p for p in planets if p["name"] == "Rahu")
        ketu_lon = (rahu["longitude"] + 180) % 360
        ketu_rasi_index = int(ketu_lon / 30)
        ketu_nakshatra_index = int(ketu_lon / (360/27))
        
        planets.append({
            "planet_id": -1,  # Custom ID for Ketu
            "name": "Ketu",
            "tamil_name": "கேது",
            "symbol": "☋",
            "longitude": ketu_lon,
            "latitude": 0,
            "speed": rahu["speed"],
            "is_retrograde": True,  # Nodes are always retrograde
            "rasi_index": ketu_rasi_index,
            "rasi": RASIS[ketu_rasi_index]["name"],
            "rasi_tamil": RASIS[ketu_rasi_index]["tamil"],
            "nakshatra_index": ketu_nakshatra_index,
            "nakshatra": NAKSHATRAS[ketu_nakshatra_index]["name"],
            "nakshatra_tamil": NAKSHATRAS[ketu_nakshatra_index]["tamil"],
            "nakshatra_pada": int((ketu_lon % (360/27)) / (360/108)) + 1,
            "degree_in_rasi": ketu_lon % 30,
        })
        
        return planets
    
    def get_sunrise_sunset(self, jd: float, lat: float, lon: float) -> Dict:
        """Calculate sunrise and sunset times"""
        try:
            # Sunrise - using swe.rise_trans with correct parameters
            # Signature: rise_trans(tjdut, body, rsmi, geopos, atpress=0.0, attemp=0.0, flags=FLG_SWIEPH)
            sunrise_result = swe.rise_trans(
                jd,                                    # tjdut: Julian day UT
                swe.SUN,                               # body: planet (int)
                swe.CALC_RISE | swe.BIT_DISC_CENTER,   # rsmi: rise with disc center
                [lon, lat, 0],                         # geopos: [longitude, latitude, altitude]
                1013.25,                               # atpress: atmospheric pressure in mbar
                15.0                                   # attemp: atmospheric temperature in celsius
            )
            sunrise_jd = sunrise_result[1][0] if sunrise_result[0] >= 0 else jd + 0.25

            # Sunset
            sunset_result = swe.rise_trans(
                jd,
                swe.SUN,
                swe.CALC_SET | swe.BIT_DISC_CENTER,
                [lon, lat, 0],
                1013.25,
                15.0
            )
            sunset_jd = sunset_result[1][0] if sunset_result[0] >= 0 else jd + 0.75

            return {
                "sunrise_jd": sunrise_jd,
                "sunset_jd": sunset_jd,
                "sunrise": self._jd_to_time_string(sunrise_jd),
                "sunset": self._jd_to_time_string(sunset_jd),
                "day_duration_hours": (sunset_jd - sunrise_jd) * 24
            }
        except Exception as e:
            # Fallback to approximate times if calculation fails
            return {
                "sunrise_jd": jd + 0.25,  # ~6 AM
                "sunset_jd": jd + 0.75,   # ~6 PM
                "sunrise": "06:00",
                "sunset": "18:00",
                "day_duration_hours": 12.0
            }

    def get_moonrise_moonset(self, jd: float, lat: float, lon: float) -> Dict:
        """Calculate moonrise and moonset times"""
        try:
            # Moonrise
            moonrise_result = swe.rise_trans(
                jd, swe.MOON, swe.CALC_RISE | swe.BIT_DISC_CENTER,
                [lon, lat, 0], 1013.25, 15.0
            )
            moonrise_jd = moonrise_result[1][0] if moonrise_result[0] >= 0 else None

            # Moonset - search from moonrise or from jd
            search_start = moonrise_jd if moonrise_jd else jd
            moonset_result = swe.rise_trans(
                search_start, swe.MOON, swe.CALC_SET | swe.BIT_DISC_CENTER,
                [lon, lat, 0], 1013.25, 15.0
            )
            moonset_jd = moonset_result[1][0] if moonset_result[0] >= 0 else None

            return {
                "moonrise_jd": moonrise_jd,
                "moonset_jd": moonset_jd,
                "moonrise": self._jd_to_datetime_string(moonrise_jd) if moonrise_jd else None,
                "moonset": self._jd_to_datetime_string(moonset_jd) if moonset_jd else None,
            }
        except Exception as e:
            return {
                "moonrise_jd": None,
                "moonset_jd": None,
                "moonrise": None,
                "moonset": None,
            }

    def _jd_to_datetime_string(self, jd: float, timezone_offset: float = 5.5) -> str:
        """Convert Julian Day to datetime string 'Mon DD HH:MM AM/PM' in local timezone."""
        result = swe.revjul(jd)
        year, month, day, hours_ut = int(result[0]), int(result[1]), int(result[2]), result[3]

        # Convert UT to local time
        hours_local = hours_ut + timezone_offset
        if hours_local >= 24:
            hours_local -= 24
            day += 1
        elif hours_local < 0:
            hours_local += 24
            day -= 1

        h = int(hours_local)
        m = int((hours_local - h) * 60)

        # Format with AM/PM
        period = "AM" if h < 12 else "PM"
        h12 = h if h <= 12 else h - 12
        if h12 == 0:
            h12 = 12

        month_names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        return f"{month_names[month]} {day:02d} {h12}:{m:02d} {period}"

    def get_moon_phase(self, jd: float) -> Dict:
        """Calculate moon phase and tithi"""
        sun = self.get_planet_position(swe.SUN, jd)
        moon = self.get_planet_position(swe.MOON, jd)
        
        # Moon-Sun angular distance
        diff = (moon["longitude"] - sun["longitude"]) % 360
        
        # Tithi (each tithi is 12 degrees)
        tithi_index = int(diff / 12)
        tithi_progress = (diff % 12) / 12  # Progress within current tithi
        
        TITHIS = [
            "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
            "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
            "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima/Amavasya"
        ]
        
        # Paksha (waxing/waning)
        paksha = "Shukla" if diff < 180 else "Krishna"
        tithi_in_paksha = tithi_index % 15
        
        return {
            "tithi_index": tithi_index,
            "tithi": TITHIS[tithi_in_paksha],
            "paksha": paksha,
            "moon_sun_angle": diff,
            "tithi_progress": tithi_progress,
        }
    
    def _jd_to_time_string(self, jd: float, timezone_offset: float = 5.5) -> str:
        """
        Convert Julian Day to time string HH:MM in local timezone.
        Default timezone_offset is 5.5 hours for IST (UTC+5:30).
        """
        result = swe.revjul(jd)
        hours_ut = result[3]
        # Convert UT to local time
        hours_local = hours_ut + timezone_offset
        # Handle day overflow
        if hours_local >= 24:
            hours_local -= 24
        elif hours_local < 0:
            hours_local += 24
        h = int(hours_local)
        m = int((hours_local - h) * 60)
        return f"{h:02d}:{m:02d}"
    
    def calculate_planet_strength(self, planet: Dict, jd: float) -> float:
        """
        Calculate a simplified strength score (0-100) for visual display
        Based on: dignity, retrograde status, and house placement
        """
        score = 50  # Base score
        
        rasi_index = planet["rasi_index"]
        planet_id = planet["planet_id"]
        
        # Exaltation/Debilitation
        EXALTATION = {swe.SUN: 0, swe.MOON: 1, swe.MARS: 9, swe.MERCURY: 5, 
                      swe.JUPITER: 3, swe.VENUS: 11, swe.SATURN: 6}
        DEBILITATION = {swe.SUN: 6, swe.MOON: 7, swe.MARS: 3, swe.MERCURY: 11,
                        swe.JUPITER: 9, swe.VENUS: 5, swe.SATURN: 0}
        
        if planet_id in EXALTATION:
            if rasi_index == EXALTATION[planet_id]:
                score += 30
            elif rasi_index == DEBILITATION[planet_id]:
                score -= 25
        
        # Own sign
        rasi_lord = RASIS[rasi_index]["lord"]
        if rasi_lord == planet_id:
            score += 20
        
        # Retrograde penalty (except for Rahu/Ketu)
        if planet["is_retrograde"] and planet_id not in [swe.TRUE_NODE, -1]:
            score -= 10
        
        # Clamp to 0-100
        return max(0, min(100, score))
