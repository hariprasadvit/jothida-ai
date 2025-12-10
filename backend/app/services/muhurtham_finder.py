"""
Muhurtham Finder Service
Finds auspicious times based on Panchangam data
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Optional
import calendar

from app.services.ephemeris import EphemerisService, NAKSHATRAS, RASIS
from app.services.panchangam_calculator import PanchangamCalculator


# Excellent nakshatras for different events
EVENT_NAKSHATRAS = {
    "marriage": ["Rohini", "Mrigashira", "Magha", "Uttara Phalguni", "Hasta", "Swati",
                 "Anuradha", "Mula", "Uttara Ashadha", "Shravana", "Uttara Bhadrapada", "Revati"],
    "griha_pravesam": ["Rohini", "Mrigashira", "Pushya", "Uttara Phalguni", "Hasta", "Chitra",
                       "Swati", "Anuradha", "Uttara Ashadha", "Shravana", "Dhanishta", "Uttara Bhadrapada", "Revati"],
    "vehicle": ["Ashwini", "Rohini", "Mrigashira", "Punarvasu", "Pushya", "Hasta",
                "Chitra", "Swati", "Anuradha", "Shravana", "Dhanishta", "Revati"],
    "business": ["Ashwini", "Rohini", "Mrigashira", "Punarvasu", "Pushya", "Magha",
                 "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Anuradha", "Uttara Ashadha", "Shravana", "Revati"],
    "travel": ["Ashwini", "Mrigashira", "Punarvasu", "Pushya", "Hasta", "Anuradha",
               "Shravana", "Dhanishta", "Revati"],
    "general": ["Ashwini", "Rohini", "Mrigashira", "Punarvasu", "Pushya", "Uttara Phalguni",
                "Hasta", "Chitra", "Swati", "Anuradha", "Uttara Ashadha", "Shravana", "Dhanishta",
                "Uttara Bhadrapada", "Revati"],
}

# Bad nakshatras to avoid
BAD_NAKSHATRAS = ["Bharani", "Krittika", "Ardra", "Ashlesha", "Magha", "Purva Phalguni",
                  "Vishakha", "Jyeshtha", "Purva Ashadha", "Purva Bhadrapada"]

# Good tithis
GOOD_TITHIS = ["Dwitiya", "Tritiya", "Panchami", "Saptami", "Dashami", "Ekadashi", "Trayodashi"]
BAD_TITHIS = ["Chaturthi", "Ashtami", "Navami", "Chaturdashi", "Amavasya"]

# Days good for specific events
GOOD_DAYS = {
    "marriage": [0, 2, 3, 4],  # Monday, Wednesday, Thursday, Friday
    "griha_pravesam": [0, 2, 3, 4],
    "vehicle": [2, 3, 4, 5],  # Wednesday, Thursday, Friday, Saturday
    "business": [0, 2, 3, 4],
    "travel": [0, 2, 4],  # Monday, Wednesday, Friday
    "general": [0, 2, 3, 4],
}

# Days to avoid
AVOID_DAYS = {
    "marriage": [1, 5],  # Tuesday, Saturday
    "general": [1],  # Tuesday
}


class MuhurthamFinder:
    """
    Find auspicious times (Muhurthams) for various events
    Uses Panchangam data to calculate quality scores
    """

    def __init__(self, ephemeris: EphemerisService):
        self.ephemeris = ephemeris
        self.panchangam = PanchangamCalculator(ephemeris)

    def find_slots(
        self,
        event_type: str,
        start_date: date,
        end_date: date,
        lat: float,
        lon: float,
        user_nakshatra: Optional[str] = None
    ) -> List[Dict]:
        """
        Find auspicious time slots within a date range
        Returns list of MuhurthamSlot dictionaries
        """
        slots = []
        current = start_date

        while current <= end_date:
            day_slots = self._find_day_slots(current, event_type, lat, lon, user_nakshatra)
            slots.extend(day_slots)
            current += timedelta(days=1)

        # Sort by quality score descending
        slots.sort(key=lambda x: x["quality_score"], reverse=True)

        return slots[:20]  # Return top 20 slots

    def _find_day_slots(
        self,
        target_date: date,
        event_type: str,
        lat: float,
        lon: float,
        user_nakshatra: Optional[str] = None
    ) -> List[Dict]:
        """Find auspicious slots for a specific day"""
        slots = []

        try:
            # Get panchangam for the day
            panchang = self.panchangam.calculate(target_date, lat, lon, "Asia/Kolkata")
        except Exception as e:
            # If panchangam calculation fails, return empty slots
            return slots

        # Calculate base day score
        day_score = self._calculate_day_score(target_date, panchang, event_type)

        # If day is completely bad, skip it
        if day_score < 30:
            return slots

        # Get good time slots for this day
        time_slots = self._get_good_time_slots(target_date, panchang, lat, lon)

        for slot in time_slots:
            quality_score = min(100, day_score + slot["bonus"])

            factors = self._get_factors(panchang, slot, event_type)
            conflicts = self._get_conflicts(slot, panchang)

            if slot["is_rahu_kalam"]:
                continue  # Skip Rahu Kalam slots

            quality_label = "சிறந்தது" if quality_score >= 80 else "நல்லது" if quality_score >= 60 else "சாதாரணம்"

            slots.append({
                "date": target_date.isoformat(),
                "start_time": slot["start"],
                "end_time": slot["end"],
                "quality_score": round(quality_score, 1),
                "quality_label": quality_label,
                "factors": factors,
                "conflicts": conflicts
            })

        return slots

    def _calculate_day_score(self, target_date: date, panchang: Dict, event_type: str) -> float:
        """Calculate overall day quality score"""
        score = 50.0  # Base score

        weekday = target_date.weekday()

        # Weekday scoring
        good_days = GOOD_DAYS.get(event_type, GOOD_DAYS["general"])
        avoid_days = AVOID_DAYS.get(event_type, AVOID_DAYS["general"])

        if weekday in good_days:
            score += 15
        elif weekday in avoid_days:
            score -= 20

        # Tithi scoring
        tithi_name = panchang.get("tithi", {}).get("name", "")
        if tithi_name in GOOD_TITHIS:
            score += 15
        elif tithi_name in BAD_TITHIS:
            score -= 15

        # Nakshatra scoring
        nakshatra_name = panchang.get("nakshatra", {}).get("name", "")
        good_nakshatras = EVENT_NAKSHATRAS.get(event_type, EVENT_NAKSHATRAS["general"])

        if nakshatra_name in good_nakshatras:
            score += 20
        elif nakshatra_name in BAD_NAKSHATRAS:
            score -= 20

        # Yoga scoring - check for good/bad yogas
        yoga_name = panchang.get("yoga", {}).get("name", "")
        good_yogas = ["Siddhi", "Shubha", "Amrita", "Priti", "Ayushman"]
        bad_yogas = ["Vyatipata", "Vaidhriti", "Parigha", "Vajra"]

        if yoga_name in good_yogas:
            score += 10
        elif yoga_name in bad_yogas:
            score -= 10

        return max(0, min(100, score))

    def _get_good_time_slots(self, target_date: date, panchang: Dict, lat: float, lon: float) -> List[Dict]:
        """Get good time slots for the day"""
        slots = []

        sunrise = panchang.get("sunrise", "06:00")
        sunset = panchang.get("sunset", "18:00")

        # Parse times
        def parse_time(t):
            parts = t.split(":")
            return int(parts[0]), int(parts[1]) if len(parts) > 1 else 0

        sr_h, sr_m = parse_time(sunrise)
        ss_h, ss_m = parse_time(sunset)

        # Rahu Kalam check
        rahu_start = panchang.get("rahu_kalam", {}).get("start", "15:00")
        rahu_end = panchang.get("rahu_kalam", {}).get("end", "16:30")
        rk_start_h, rk_start_m = parse_time(rahu_start)
        rk_end_h, rk_end_m = parse_time(rahu_end)

        def in_rahu_kalam(h, m):
            time_mins = h * 60 + m
            rk_start_mins = rk_start_h * 60 + rk_start_m
            rk_end_mins = rk_end_h * 60 + rk_end_m
            return rk_start_mins <= time_mins < rk_end_mins

        # Brahma Muhurta (1.5 hours before sunrise)
        brahma_start_h = sr_h - 2 if sr_m < 30 else sr_h - 1
        brahma_start_m = (sr_m + 30) % 60 if sr_m >= 30 else sr_m + 30
        slots.append({
            "name": "பிரம்ம முகூர்த்தம்",
            "start": f"{max(4, brahma_start_h):02d}:{brahma_start_m:02d}",
            "end": sunrise,
            "bonus": 25,
            "is_rahu_kalam": False
        })

        # Abhijit Muhurta (around noon, ~48 minutes centered at local noon)
        noon_h = (sr_h + ss_h) // 2
        slots.append({
            "name": "அபிஜித் முகூர்த்தம்",
            "start": f"{noon_h - 1}:36",
            "end": f"{noon_h}:24",
            "bonus": 20,
            "is_rahu_kalam": in_rahu_kalam(noon_h, 0)
        })

        # Morning slot (after sunrise, before noon)
        morning_end_h = min(sr_h + 4, 12)
        slots.append({
            "name": "காலை நல்ல நேரம்",
            "start": f"{sr_h + 1:02d}:00",
            "end": f"{morning_end_h:02d}:00",
            "bonus": 10,
            "is_rahu_kalam": any(in_rahu_kalam(h, 0) for h in range(sr_h + 1, morning_end_h))
        })

        # Afternoon slot
        slots.append({
            "name": "மதிய நேரம்",
            "start": "14:00",
            "end": "16:00",
            "bonus": 5,
            "is_rahu_kalam": any(in_rahu_kalam(h, 0) for h in range(14, 16))
        })

        # Evening slot (before sunset)
        slots.append({
            "name": "சாயங்கால நேரம்",
            "start": f"{ss_h - 2:02d}:00",
            "end": f"{ss_h:02d}:00",
            "bonus": 8,
            "is_rahu_kalam": any(in_rahu_kalam(h, 0) for h in range(ss_h - 2, ss_h))
        })

        return slots

    def _get_factors(self, panchang: Dict, slot: Dict, event_type: str) -> List[Dict]:
        """Get contributing factors for display"""
        factors = []

        # Tithi factor
        tithi_name = panchang.get("tithi", {}).get("name", "Unknown")
        tithi_tamil = panchang.get("tithi", {}).get("tamil", tithi_name)
        is_good_tithi = tithi_name in GOOD_TITHIS

        factors.append({
            "name": "திதி",
            "value": tithi_tamil,
            "is_positive": is_good_tithi
        })

        # Nakshatra factor
        nakshatra_name = panchang.get("nakshatra", {}).get("name", "Unknown")
        nakshatra_tamil = panchang.get("nakshatra", {}).get("tamil", nakshatra_name)
        good_nakshatras = EVENT_NAKSHATRAS.get(event_type, EVENT_NAKSHATRAS["general"])
        is_good_nakshatra = nakshatra_name in good_nakshatras

        factors.append({
            "name": "நட்சத்திரம்",
            "value": nakshatra_tamil,
            "is_positive": is_good_nakshatra
        })

        # Slot type factor
        factors.append({
            "name": "நேரம்",
            "value": slot["name"],
            "is_positive": slot["bonus"] >= 15
        })

        return factors

    def _get_conflicts(self, slot: Dict, panchang: Dict) -> List[str]:
        """Get any conflicts/warnings"""
        conflicts = []

        if slot.get("is_rahu_kalam"):
            conflicts.append("ராகு காலம் - தவிர்க்கவும்")

        # Check for yamagandam overlap
        yama_start = panchang.get("yamagandam", {}).get("start", "")
        if yama_start and slot["start"] <= yama_start <= slot["end"]:
            conflicts.append("யமகண்டம் - கவனம்")

        return conflicts

    def get_month_calendar(self, month: int, year: int, lat: float, lon: float) -> List[Dict]:
        """
        Get calendar heat map data for a month
        Returns list of CalendarDay objects with event-specific scores
        """
        days = []
        num_days = calendar.monthrange(year, month)[1]

        # Event types with Tamil names
        EVENT_TYPES = {
            "marriage": "திருமணம்",
            "griha_pravesam": "கிரகப்பிரவேசம்",
            "vehicle": "வாகனம்",
            "business": "வியாபாரம்",
            "travel": "பயணம்",
            "general": "பொது"
        }

        for day in range(1, num_days + 1):
            target_date = date(year, month, day)

            try:
                panchang = self.panchangam.calculate(target_date, lat, lon, "Asia/Kolkata")
            except Exception:
                panchang = {}

            weekday = target_date.weekday()

            # Calculate scores for each event type
            event_scores = {}
            good_for_events = []

            for event_type, tamil_name in EVENT_TYPES.items():
                score = self._calculate_day_score(target_date, panchang, event_type) if panchang else 50.0
                event_scores[event_type] = round(score, 1)

                # Mark as good if score >= 65
                if score >= 65:
                    good_for_events.append({
                        "type": event_type,
                        "tamil": tamil_name,
                        "score": round(score, 1)
                    })

            # General day score
            day_score = event_scores.get("general", 50.0)
            is_auspicious = day_score >= 60

            # Get any festivals/warnings
            festivals = []
            warnings = []

            tithi_name = panchang.get("tithi", {}).get("name", "")
            if tithi_name == "Purnima":
                festivals.append("பூர்ணிமா")
            elif tithi_name == "Amavasya":
                warnings.append("அமாவாசை")

            if weekday == 1:  # Tuesday
                warnings.append("செவ்வாய்")

            days.append({
                "date": target_date.isoformat(),
                "day_score": round(day_score, 1),
                "is_auspicious": is_auspicious,
                "has_muhurtham": day_score >= 70,
                "event_scores": event_scores,
                "good_for_events": good_for_events,
                "festivals": festivals,
                "warnings": warnings
            })

        return days

    def get_day_details(self, target_date: date, lat: float, lon: float) -> Dict:
        """
        Get detailed muhurtham information for a specific day
        Used when user clicks on a calendar day
        """
        try:
            panchang = self.panchangam.calculate(target_date, lat, lon, "Asia/Kolkata")
        except Exception:
            return {"error": "Unable to calculate panchangam"}

        day_score = self._calculate_day_score(target_date, panchang, "general")
        time_slots = self._get_good_time_slots(target_date, panchang, lat, lon)

        # Calculate event-specific scores
        EVENT_TYPES = {
            "marriage": "திருமணம்",
            "griha_pravesam": "கிரகப்பிரவேசம்",
            "vehicle": "வாகனம்",
            "business": "வியாபாரம்",
            "travel": "பயணம்",
            "general": "பொது"
        }

        event_scores = {}
        good_for_events = []

        for event_type, tamil_name in EVENT_TYPES.items():
            score = self._calculate_day_score(target_date, panchang, event_type)
            event_scores[event_type] = round(score, 1)

            if score >= 65:
                good_for_events.append({
                    "type": event_type,
                    "tamil": tamil_name,
                    "score": round(score, 1)
                })

        # Filter out Rahu Kalam slots and add quality info
        filtered_slots = []
        for slot in time_slots:
            if not slot.get("is_rahu_kalam"):
                slot_score = min(100, day_score + slot["bonus"])
                filtered_slots.append({
                    "time": f"{slot['start']} - {slot['end']}",
                    "label": slot["name"],
                    "score": round(slot_score, 1),
                    "type": "excellent" if slot_score >= 80 else "good" if slot_score >= 60 else "average"
                })

        # Add Rahu Kalam as avoid slot
        rahu_start = panchang.get("rahu_kalam", {}).get("start", "15:00")
        rahu_end = panchang.get("rahu_kalam", {}).get("end", "16:30")
        filtered_slots.append({
            "time": f"{rahu_start} - {rahu_end}",
            "label": "ராகு காலம்",
            "score": 0,
            "type": "avoid"
        })

        # Add Yamagandam and Kuligai as avoid slots
        yama_start = panchang.get("yamagandam", {}).get("start", "")
        yama_end = panchang.get("yamagandam", {}).get("end", "")
        if yama_start and yama_end:
            filtered_slots.append({
                "time": f"{yama_start} - {yama_end}",
                "label": "யமகண்டம்",
                "score": 0,
                "type": "caution"
            })

        kuligai_start = panchang.get("kuligai", {}).get("start", "")
        kuligai_end = panchang.get("kuligai", {}).get("end", "")
        if kuligai_start and kuligai_end:
            filtered_slots.append({
                "time": f"{kuligai_start} - {kuligai_end}",
                "label": "குளிகை",
                "score": 0,
                "type": "caution"
            })

        # Sort by score descending
        filtered_slots.sort(key=lambda x: x["score"], reverse=True)

        return {
            "date": target_date.isoformat(),
            "day_score": round(day_score, 1),
            "event_scores": event_scores,
            "good_for_events": good_for_events,
            "panchangam": {
                "tithi": panchang.get("tithi", {}),
                "nakshatra": panchang.get("nakshatra", {}),
                "yoga": panchang.get("yoga", {}),
                "vaaram": panchang.get("vaaram", ""),
                "sunrise": panchang.get("sunrise", ""),
                "sunset": panchang.get("sunset", ""),
                "sun_times": panchang.get("sun_times", {}),
                "moon_times": panchang.get("moon_times", {}),
                "inauspicious": panchang.get("inauspicious", {}),
                "auspicious": panchang.get("auspicious", {})
            },
            "time_slots": filtered_slots,
            "recommendation": self._get_recommendation(day_score, panchang)
        }

    def _get_recommendation(self, day_score: float, panchang: Dict) -> str:
        """Generate AI-style recommendation for the day"""
        nakshatra_tamil = panchang.get("nakshatra", {}).get("tamil", "")
        tithi_tamil = panchang.get("tithi", {}).get("tamil", "")

        if day_score >= 80:
            return f"{nakshatra_tamil} நட்சத்திரமும் {tithi_tamil} திதியும் சேர்ந்து மிகவும் சுபகரமான நாள். அனைத்து நற்காரியங்களுக்கும் ஏற்றது."
        elif day_score >= 60:
            return f"இன்று {nakshatra_tamil} நட்சத்திரம். நல்ல நேரங்களில் சுப காரியங்கள் செய்யலாம். ராகு காலம் தவிர்க்கவும்."
        elif day_score >= 40:
            return f"சாதாரண நாள். முக்கிய முடிவுகளை அபிஜித் முகூர்த்தத்தில் எடுக்கவும். ராகு காலம் மற்றும் யமகண்டம் தவிர்க்கவும்."
        else:
            return "இன்று புதிய காரியங்கள் தொடங்குவதை தவிர்க்கவும். அவசியமான பணிகளை மட்டும் செய்யவும்."
