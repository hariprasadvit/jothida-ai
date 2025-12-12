"""
Ungal Jothidan (Your Astrologer) - Daily Intelligence Dashboard Service

Generates personalized daily insights based on:
- Natal chart (birth chart)
- Current transits (gochara)
- Dasha/Bhukti periods
- Panchang (tithi, nakshatra, yoga, karana)

Each insight card has a score (0-100) and confidence rating.
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple
import math

# Card definitions with signals and weights
CARD_DEFINITIONS = {
    "dasha_mood": {
        "id": "dasha_mood",
        "title_ta": "தசா மனநிலை",
        "title_en": "Dasha Mood",
        "title_kn": "ದಶಾ ಮನಸ್ಥಿತಿ",
        "icon": "moon-outline",
        "signals": ["dasha_strength", "dasha_lord_dignity", "transit_on_dasha_lord"],
        "weights": [0.5, 0.3, 0.2],
        "color": "#8b5cf6"
    },
    "transit_pressure": {
        "id": "transit_pressure",
        "title_ta": "கிரக அழுத்தம்",
        "title_en": "Transit Pressure",
        "title_kn": "ಗ್ರಹ ಒತ್ತಡ",
        "icon": "planet-outline",
        "signals": ["major_transit_power", "moon_phase_effect", "panchang_dosha"],
        "weights": [0.6, 0.2, 0.2],
        "color": "#ef4444"
    },
    "finance_outlook": {
        "id": "finance_outlook",
        "title_ta": "நிதி நிலை",
        "title_en": "Finance Outlook",
        "title_kn": "ಹಣಕಾಸು ದೃಷ್ಟಿಕೋನ",
        "icon": "wallet-outline",
        "signals": ["dhana_house_score", "dhana_karaka_influence", "transit_finance", "panchang_favorable"],
        "weights": [0.35, 0.35, 0.2, 0.1],
        "color": "#22c55e"
    },
    "work_career": {
        "id": "work_career",
        "title_ta": "தொழில் கவனம்",
        "title_en": "Work / Career",
        "title_kn": "ಕೆಲಸ / ವೃತ್ತಿ",
        "icon": "briefcase-outline",
        "signals": ["career_house_score", "mercury_sun_strength", "transit_career", "weekday_effect"],
        "weights": [0.4, 0.3, 0.2, 0.1],
        "color": "#3b82f6"
    },
    "relationship_energy": {
        "id": "relationship_energy",
        "title_ta": "உறவு சக்தி",
        "title_en": "Relationship Energy",
        "title_kn": "ಸಂಬಂಧ ಶಕ್ತಿ",
        "icon": "heart-outline",
        "signals": ["relationship_house_score", "venus_moon_dignity", "transit_relationship", "lunar_day_effect"],
        "weights": [0.4, 0.35, 0.15, 0.1],
        "color": "#ec4899"
    },
    "health_vibration": {
        "id": "health_vibration",
        "title_ta": "உடல்நலம்",
        "title_en": "Health Vibration",
        "title_kn": "ಆರೋಗ್ಯ ಕಂಪನ",
        "icon": "fitness-outline",
        "signals": ["health_house_score", "moon_nakshatra_stress", "malefic_transit_health"],
        "weights": [0.4, 0.35, 0.25],
        "color": "#14b8a6"
    },
    "lucky_window": {
        "id": "lucky_window",
        "title_ta": "அதிர்ஷ்ட நேரம்",
        "title_en": "Lucky Window",
        "title_kn": "ಅದೃಷ್ಟದ ಸಮಯ",
        "icon": "sunny-outline",
        "signals": ["moon_natal_alignment", "benefic_hours", "sunrise_alignment"],
        "weights": [0.5, 0.3, 0.2],
        "color": "#f59e0b"
    },
    "avoid_window": {
        "id": "avoid_window",
        "title_ta": "தவிர்க்க வேண்டிய நேரம்",
        "title_en": "Avoid Window",
        "title_kn": "ತಪ್ಪಿಸಬೇಕಾದ ಸಮಯ",
        "icon": "warning-outline",
        "signals": ["malefic_transit_time", "void_moon_segments", "panchang_conflict"],
        "weights": [0.6, 0.3, 0.1],
        "color": "#dc2626"
    },
    "opportunity_indicator": {
        "id": "opportunity_indicator",
        "title_ta": "வாய்ப்பு குறிகாட்டி",
        "title_en": "Opportunity",
        "title_kn": "ಅವಕಾಶ",
        "icon": "trending-up-outline",
        "signals": ["positive_delta_composite", "benefic_nakshatra"],
        "weights": [0.7, 0.3],
        "color": "#10b981"
    },
    "risk_indicator": {
        "id": "risk_indicator",
        "title_ta": "அபாய குறிகாட்டி",
        "title_en": "Risk Alert",
        "title_kn": "ಅಪಾಯ ಎಚ್ಚರಿಕೆ",
        "icon": "alert-circle-outline",
        "signals": ["negative_delta_composite", "malefic_trigger"],
        "weights": [0.7, 0.3],
        "color": "#f43f5e"
    },
    "color_direction": {
        "id": "color_direction",
        "title_ta": "நிறம் / திசை",
        "title_en": "Color / Direction",
        "title_kn": "ಬಣ್ಣ / ದಿಕ್ಕು",
        "icon": "color-palette-outline",
        "signals": ["nakshatra_ruler_lookup", "weekday_element"],
        "weights": [0.6, 0.4],
        "color": "#6366f1"
    },
    "personal_note": {
        "id": "personal_note",
        "title_ta": "தனிப்பட்ட குறிப்பு",
        "title_en": "Personal Note",
        "title_kn": "ವೈಯಕ್ತಿಕ ಟಿಪ್ಪಣಿ",
        "icon": "chatbubble-outline",
        "signals": ["summary_aggregator"],
        "weights": [1.0],
        "color": "#8b5cf6"
    }
}

# Planet rulership for colors
PLANET_COLORS = {
    "Sun": {"color": "#f97316", "color_ta": "ஆரஞ்சு", "color_en": "Orange", "color_kn": "ಕಿತ್ತಳೆ"},
    "Moon": {"color": "#f1f5f9", "color_ta": "வெள்ளை", "color_en": "White", "color_kn": "ಬಿಳಿ"},
    "Mars": {"color": "#ef4444", "color_ta": "சிவப்பு", "color_en": "Red", "color_kn": "ಕೆಂಪು"},
    "Mercury": {"color": "#22c55e", "color_ta": "பச்சை", "color_en": "Green", "color_kn": "ಹಸಿರು"},
    "Jupiter": {"color": "#eab308", "color_ta": "மஞ்சள்", "color_en": "Yellow", "color_kn": "ಹಳದಿ"},
    "Venus": {"color": "#f1f5f9", "color_ta": "வெள்ளை", "color_en": "White", "color_kn": "ಬಿಳಿ"},
    "Saturn": {"color": "#1e293b", "color_ta": "கருப்பு", "color_en": "Black", "color_kn": "ಕಪ್ಪು"},
    "Rahu": {"color": "#64748b", "color_ta": "நீலம்", "color_en": "Blue", "color_kn": "ನೀಲಿ"},
    "Ketu": {"color": "#a855f7", "color_ta": "ஊதா", "color_en": "Purple", "color_kn": "ನೇರಳೆ"}
}

# Direction mappings
PLANET_DIRECTIONS = {
    "Sun": {"direction_ta": "கிழக்கு", "direction_en": "East", "direction_kn": "ಪೂರ್ವ"},
    "Moon": {"direction_ta": "வடமேற்கு", "direction_en": "Northwest", "direction_kn": "ವಾಯುವ್ಯ"},
    "Mars": {"direction_ta": "தெற்கு", "direction_en": "South", "direction_kn": "ದಕ್ಷಿಣ"},
    "Mercury": {"direction_ta": "வடக்கு", "direction_en": "North", "direction_kn": "ಉತ್ತರ"},
    "Jupiter": {"direction_ta": "வடகிழக்கு", "direction_en": "Northeast", "direction_kn": "ಈಶಾನ್ಯ"},
    "Venus": {"direction_ta": "தென்கிழக்கு", "direction_en": "Southeast", "direction_kn": "ಆಗ್ನೇಯ"},
    "Saturn": {"direction_ta": "மேற்கு", "direction_en": "West", "direction_kn": "ಪಶ್ಚಿಮ"},
    "Rahu": {"direction_ta": "தென்மேற்கு", "direction_en": "Southwest", "direction_kn": "ನೈಋತ್ಯ"},
    "Ketu": {"direction_ta": "தென்மேற்கு", "direction_en": "Southwest", "direction_kn": "ನೈಋತ್ಯ"}
}

# Weekday planet rulers
WEEKDAY_RULERS = {
    0: "Moon",    # Monday
    1: "Mars",    # Tuesday
    2: "Mercury", # Wednesday
    3: "Jupiter", # Thursday
    4: "Venus",   # Friday
    5: "Saturn",  # Saturday
    6: "Sun"      # Sunday
}

# Nakshatra rulers
NAKSHATRA_RULERS = {
    "Ashwini": "Ketu", "Bharani": "Venus", "Krittika": "Sun",
    "Rohini": "Moon", "Mrigashira": "Mars", "Ardra": "Rahu",
    "Punarvasu": "Jupiter", "Pushya": "Saturn", "Ashlesha": "Mercury",
    "Magha": "Ketu", "Purva Phalguni": "Venus", "Uttara Phalguni": "Sun",
    "Hasta": "Moon", "Chitra": "Mars", "Swati": "Rahu",
    "Vishakha": "Jupiter", "Anuradha": "Saturn", "Jyeshtha": "Mercury",
    "Moola": "Ketu", "Purva Ashadha": "Venus", "Uttara Ashadha": "Sun",
    "Shravana": "Moon", "Dhanishta": "Mars", "Shatabhisha": "Rahu",
    "Purva Bhadrapada": "Jupiter", "Uttara Bhadrapada": "Saturn", "Revati": "Mercury"
}

# Tamil nakshatra names mapping
NAKSHATRA_TAMIL = {
    "அஸ்வினி": "Ashwini", "பரணி": "Bharani", "கார்த்திகை": "Krittika",
    "ரோகிணி": "Rohini", "மிருகசீரிடம்": "Mrigashira", "திருவாதிரை": "Ardra",
    "புனர்பூசம்": "Punarvasu", "பூசம்": "Pushya", "ஆயில்யம்": "Ashlesha",
    "மகம்": "Magha", "பூரம்": "Purva Phalguni", "உத்திரம்": "Uttara Phalguni",
    "ஹஸ்தம்": "Hasta", "சித்திரை": "Chitra", "சுவாதி": "Swati",
    "விசாகம்": "Vishakha", "அனுஷம்": "Anuradha", "கேட்டை": "Jyeshtha",
    "மூலம்": "Moola", "பூராடம்": "Purva Ashadha", "உத்திராடம்": "Uttara Ashadha",
    "திருவோணம்": "Shravana", "அவிட்டம்": "Dhanishta", "சதயம்": "Shatabhisha",
    "பூரட்டாதி": "Purva Bhadrapada", "உத்திரட்டாதி": "Uttara Bhadrapada", "ரேவதி": "Revati"
}


class UngalJothidanService:
    """
    Service to generate daily personalized astrological insights.

    Uses:
    - Birth chart data
    - Current transits
    - Dasha periods
    - Panchang data

    Produces 12 insight cards with scores and confidence ratings.
    """

    def __init__(self, ephemeris=None):
        self.ephemeris = ephemeris

    def generate_daily_insights(
        self,
        user_data: Dict,
        target_date: date = None,
        language: str = "ta"
    ) -> Dict:
        """
        Generate complete daily insights for a user.

        Args:
            user_data: Dict with birth_date, birth_time, birth_place, rasi, nakshatra, etc.
            target_date: Date for insights (default today)
            language: Language code (ta, en, kn)

        Returns:
            Dict with overall_confidence, summary, and 12 cards
        """
        if target_date is None:
            target_date = date.today()

        # Extract user birth details
        birth_date = user_data.get("birth_date")
        birth_time = user_data.get("birth_time", "06:00")
        birth_place = user_data.get("birth_place", "Chennai")
        user_rasi = user_data.get("rasi", "மேஷம்")
        user_nakshatra = user_data.get("nakshatra", "அஸ்வினி")

        # Compute base signals from birth data and current date
        base_signals = self._compute_base_signals(
            birth_date, birth_time, birth_place,
            user_rasi, user_nakshatra, target_date
        )

        # Assess data quality (affects confidence)
        data_quality = self._assess_data_quality(user_data)

        # Generate all 12 cards
        cards = []
        for card_id, card_def in CARD_DEFINITIONS.items():
            card = self._generate_card(
                card_def, base_signals, data_quality, language, target_date
            )
            cards.append(card)

        # Calculate overall confidence
        overall_confidence = round(sum(c["confidence"] for c in cards) / len(cards))

        # Generate summary
        summary = self._generate_summary(cards, language)

        # Get profile info
        profile = {
            "name": user_data.get("name", ""),
            "rasi": user_rasi,
            "nakshatra": user_nakshatra,
            "dob": birth_date
        }

        return {
            "user_id": user_data.get("id", ""),
            "date": target_date.isoformat(),
            "overall_confidence": overall_confidence,
            "summary": summary,
            "profile": profile,
            "cards": cards
        }

    def _compute_base_signals(
        self,
        birth_date: str,
        birth_time: str,
        birth_place: str,
        rasi: str,
        nakshatra: str,
        target_date: date
    ) -> Dict:
        """
        Compute all base signals needed for card calculations.

        This is where the actual astrological calculations happen.
        """
        # Get weekday (0=Monday, 6=Sunday)
        weekday = target_date.weekday()
        weekday_ruler = WEEKDAY_RULERS[weekday]

        # Get nakshatra ruler
        nakshatra_en = NAKSHATRA_TAMIL.get(nakshatra, "Ashwini")
        nakshatra_ruler = NAKSHATRA_RULERS.get(nakshatra_en, "Ketu")

        # Calculate moon phase (simplified)
        # In real implementation, use ephemeris
        day_of_month = target_date.day
        moon_phase_score = self._calculate_moon_phase_score(day_of_month)

        # Dasha calculations (simplified based on nakshatra)
        dasha_info = self._calculate_dasha_info(nakshatra, target_date)

        # Transit influences (simplified)
        transit_info = self._calculate_transit_effects(rasi, target_date)

        # Panchang-based calculations
        panchang_info = self._calculate_panchang_effects(target_date, weekday)

        # House activations (based on rasi and transits)
        house_scores = self._calculate_house_scores(rasi, target_date)

        # Calculate lucky/avoid times
        lucky_time = self._calculate_lucky_window(nakshatra_ruler, weekday, target_date)
        avoid_time = self._calculate_avoid_window(weekday, target_date)

        return {
            "weekday": weekday,
            "weekday_ruler": weekday_ruler,
            "nakshatra": nakshatra,
            "nakshatra_en": nakshatra_en,
            "nakshatra_ruler": nakshatra_ruler,
            "rasi": rasi,
            "moon_phase_score": moon_phase_score,
            "dasha": dasha_info,
            "transits": transit_info,
            "panchang": panchang_info,
            "houses": house_scores,
            "lucky_time": lucky_time,
            "avoid_time": avoid_time
        }

    def _calculate_moon_phase_score(self, day_of_month: int) -> int:
        """Calculate score based on lunar day (tithi)."""
        # Shukla paksha (waxing) days 1-15: generally favorable
        # Krishna paksha (waning) days 16-30: mixed
        # Amavasya (new moon) and Pournami (full moon) are special

        if day_of_month <= 15:
            # Waxing moon - generally good
            base = 60 + (day_of_month * 2)  # 62-90
        else:
            # Waning moon - more challenging
            adjusted_day = day_of_month - 15
            base = 70 - (adjusted_day * 2)  # 68-40

        # Cap between 40-95
        return max(40, min(95, base))

    def _calculate_dasha_info(self, nakshatra: str, target_date: date) -> Dict:
        """Calculate Dasha period influences."""
        nakshatra_en = NAKSHATRA_TAMIL.get(nakshatra, "Ashwini")
        dasha_lord = NAKSHATRA_RULERS.get(nakshatra_en, "Ketu")

        # Simplified dasha strength based on planet nature
        planet_strengths = {
            "Sun": 75, "Moon": 70, "Mars": 65, "Mercury": 80,
            "Jupiter": 85, "Venus": 82, "Saturn": 55, "Rahu": 50, "Ketu": 48
        }

        dasha_strength = planet_strengths.get(dasha_lord, 70)

        # Day-of-week alignment bonus
        weekday = target_date.weekday()
        if WEEKDAY_RULERS[weekday] == dasha_lord:
            dasha_strength = min(95, dasha_strength + 15)

        return {
            "lord": dasha_lord,
            "strength": dasha_strength,
            "dignity": min(95, dasha_strength + 5),
            "transit_effect": max(40, dasha_strength - 10)
        }

    def _calculate_transit_effects(self, rasi: str, target_date: date) -> Dict:
        """Calculate current transit effects on birth chart."""
        # Simplified transit calculations
        day_factor = target_date.day % 12
        month_factor = target_date.month

        # Major transit power (outer planets move slower = more impact)
        major_power = 60 + (month_factor * 2) + (day_factor * 1.5)
        major_power = max(50, min(90, major_power))

        # Finance house transits (2nd and 11th)
        finance_transit = 55 + (day_factor * 3)
        finance_transit = max(45, min(85, finance_transit))

        # Career house transits (10th and 6th)
        career_transit = 60 + (month_factor * 1.5)
        career_transit = max(50, min(88, career_transit))

        # Relationship transits (7th and 5th)
        relationship_transit = 50 + (day_factor * 2.5)
        relationship_transit = max(40, min(82, relationship_transit))

        # Health-related transits
        health_transit = 65 - (day_factor * 1.5) if day_factor > 6 else 65 + (day_factor * 2)
        health_transit = max(45, min(85, health_transit))

        return {
            "major_power": int(major_power),
            "finance": int(finance_transit),
            "career": int(career_transit),
            "relationship": int(relationship_transit),
            "health": int(health_transit),
            "malefic_intensity": max(20, 100 - int(major_power))
        }

    def _calculate_panchang_effects(self, target_date: date, weekday: int) -> Dict:
        """Calculate panchang-based effects."""
        day_of_month = target_date.day

        # Tithi effect (lunar day)
        tithi_score = self._calculate_moon_phase_score(day_of_month)

        # Weekday favorability
        weekday_scores = {
            0: 70,  # Monday - Moon day, emotional
            1: 60,  # Tuesday - Mars day, action but aggression
            2: 80,  # Wednesday - Mercury day, communication
            3: 85,  # Thursday - Jupiter day, auspicious
            4: 82,  # Friday - Venus day, pleasant
            5: 55,  # Saturday - Saturn day, challenges
            6: 78   # Sunday - Sun day, leadership
        }
        weekday_score = weekday_scores.get(weekday, 70)

        # Panchang doshas (simplified)
        # Check for inauspicious combinations
        dosha_penalty = 0
        if day_of_month in [4, 9, 14]:  # Chaturthi, Navami, Chaturdashi
            dosha_penalty = 10
        if weekday == 1 and day_of_month > 20:  # Tuesday in dark fortnight
            dosha_penalty += 8

        dosha_score = max(30, 100 - dosha_penalty - (20 if day_of_month == 30 else 0))

        return {
            "tithi_score": tithi_score,
            "weekday_score": weekday_score,
            "dosha_score": dosha_score,
            "favorable_window": tithi_score > 65 and weekday_score > 65
        }

    def _calculate_house_scores(self, rasi: str, target_date: date) -> Dict:
        """Calculate activation scores for different house domains."""
        day_factor = target_date.day % 12
        month_factor = target_date.month

        # Base scores with some variation
        return {
            "dhana": 55 + (day_factor * 2.5),  # 2nd/11th - wealth
            "career": 60 + (month_factor * 1.8),  # 10th/6th - career
            "relationship": 50 + (day_factor * 2),  # 7th/5th - relationships
            "health": 65 - (day_factor * 1.2) if day_factor > 6 else 65 + day_factor,  # 1st/6th
            "mercury_sun": 70 + (day_factor if day_factor < 6 else -day_factor + 12),
            "venus_moon": 60 + (month_factor * 1.5)
        }

    def _calculate_lucky_window(self, nakshatra_ruler: str, weekday: int, target_date: date) -> Dict:
        """Calculate the lucky time window for the day."""
        # Base lucky hours vary by weekday ruler
        lucky_hour_base = {
            "Sun": 6, "Moon": 7, "Mars": 9, "Mercury": 8,
            "Jupiter": 10, "Venus": 11, "Saturn": 5, "Rahu": 12, "Ketu": 4
        }

        base_hour = lucky_hour_base.get(nakshatra_ruler, 9)

        # Adjust based on weekday
        if WEEKDAY_RULERS[weekday] == nakshatra_ruler:
            # Aligned day - morning hours favorable
            start_hour = base_hour
        else:
            # Adjust to afternoon
            start_hour = base_hour + 6 if base_hour < 12 else base_hour - 6

        start_hour = max(6, min(18, start_hour))
        end_hour = start_hour + 2

        return {
            "start": f"{start_hour:02d}:00",
            "end": f"{end_hour:02d}:00",
            "strength": 75 + (10 if WEEKDAY_RULERS[weekday] == nakshatra_ruler else 0)
        }

    def _calculate_avoid_window(self, weekday: int, target_date: date) -> Dict:
        """Calculate the time window to avoid for the day."""
        # Rahu kalam and other inauspicious times vary by weekday
        rahu_kalam = {
            0: (7, 9),    # Monday: 7:30-9:00
            1: (15, 17),  # Tuesday: 3:00-4:30
            2: (12, 14),  # Wednesday: 12:00-1:30
            3: (14, 16),  # Thursday: 1:30-3:00
            4: (10, 12),  # Friday: 10:30-12:00
            5: (9, 11),   # Saturday: 9:00-10:30
            6: (16, 18)   # Sunday: 4:30-6:00
        }

        start, end = rahu_kalam.get(weekday, (15, 17))

        return {
            "start": f"{start:02d}:00",
            "end": f"{end:02d}:00",
            "reason_ta": "ராகு காலம்",
            "reason_en": "Rahu Kalam",
            "reason_kn": "ರಾಹು ಕಾಲ",
            "severity": 70 + (weekday * 3 if weekday < 4 else -weekday * 2)
        }

    def _assess_data_quality(self, user_data: Dict) -> int:
        """Assess quality of birth data (affects confidence)."""
        quality = 50  # Base

        if user_data.get("birth_date"):
            quality += 20
        if user_data.get("birth_time"):
            quality += 15
            # Exact time vs approximate
            if ":" in str(user_data.get("birth_time", "")):
                quality += 5
        if user_data.get("birth_place"):
            quality += 10
        if user_data.get("rasi"):
            quality += 5
        if user_data.get("nakshatra"):
            quality += 5

        return min(100, quality)

    def _generate_card(
        self,
        card_def: Dict,
        base_signals: Dict,
        data_quality: int,
        language: str,
        target_date: date
    ) -> Dict:
        """Generate a single insight card with score, confidence, and text."""
        card_id = card_def["id"]

        # Get signal values based on card type
        signal_values = self._get_signal_values(card_id, base_signals, target_date)

        # Calculate weighted score
        weights = card_def["weights"]
        weighted_sum = sum(
            signal_values[i] * weights[i]
            for i in range(min(len(signal_values), len(weights)))
        )
        score = int(round(weighted_sum))

        # Calculate confidence using agreement formula
        agreement = self._calculate_agreement(signal_values)
        confidence = int(round(0.5 * data_quality + 0.5 * agreement))

        # Generate text based on score
        text = self._generate_card_text(card_id, score, base_signals, language)

        # Build reasons array
        reasons = []
        signal_names = card_def["signals"]
        for i, signal_name in enumerate(signal_names):
            if i < len(signal_values):
                reasons.append({
                    "signal": signal_name,
                    "value": signal_values[i],
                    "weight": weights[i] if i < len(weights) else 0
                })

        # Get title based on language
        title_key = f"title_{language}"
        title = card_def.get(title_key, card_def.get("title_en", card_id))

        return {
            "id": card_id,
            "title": title,
            "icon": card_def["icon"],
            "color": card_def["color"],
            "score": score,
            "confidence": confidence,
            "text": text,
            "reasons": reasons
        }

    def _get_signal_values(self, card_id: str, base_signals: Dict, target_date: date) -> List[int]:
        """Get signal values for a specific card."""
        dasha = base_signals["dasha"]
        transits = base_signals["transits"]
        panchang = base_signals["panchang"]
        houses = base_signals["houses"]

        if card_id == "dasha_mood":
            return [
                dasha["strength"],
                dasha["dignity"],
                dasha["transit_effect"]
            ]

        elif card_id == "transit_pressure":
            return [
                transits["major_power"],
                base_signals["moon_phase_score"],
                panchang["dosha_score"]
            ]

        elif card_id == "finance_outlook":
            return [
                int(houses["dhana"]),
                int(houses["venus_moon"]),
                transits["finance"],
                panchang["tithi_score"]
            ]

        elif card_id == "work_career":
            return [
                int(houses["career"]),
                int(houses["mercury_sun"]),
                transits["career"],
                panchang["weekday_score"]
            ]

        elif card_id == "relationship_energy":
            return [
                int(houses["relationship"]),
                int(houses["venus_moon"]),
                transits["relationship"],
                panchang["tithi_score"]
            ]

        elif card_id == "health_vibration":
            return [
                int(houses["health"]),
                base_signals["moon_phase_score"],
                100 - transits["malefic_intensity"]
            ]

        elif card_id == "lucky_window":
            lucky = base_signals["lucky_time"]
            return [
                lucky["strength"],
                panchang["weekday_score"],
                base_signals["moon_phase_score"]
            ]

        elif card_id == "avoid_window":
            avoid = base_signals["avoid_time"]
            return [
                avoid["severity"],
                100 - panchang["dosha_score"],
                100 - panchang["weekday_score"]
            ]

        elif card_id == "opportunity_indicator":
            # Find best performing domain
            domain_scores = [
                houses["dhana"], houses["career"],
                houses["relationship"], houses["health"]
            ]
            best_score = max(domain_scores)
            return [int(best_score), panchang["tithi_score"]]

        elif card_id == "risk_indicator":
            # Find most challenged domain
            risk_scores = [
                transits["malefic_intensity"],
                100 - panchang["dosha_score"]
            ]
            return risk_scores

        elif card_id == "color_direction":
            # Use nakshatra and weekday for color/direction
            nakshatra_score = 75  # Base
            weekday_score = panchang["weekday_score"]
            return [nakshatra_score, weekday_score]

        elif card_id == "personal_note":
            # Aggregate of top scores
            all_scores = [
                dasha["strength"],
                transits["major_power"],
                panchang["tithi_score"]
            ]
            return [int(sum(all_scores) / len(all_scores))]

        return [70]  # Default

    def _calculate_agreement(self, signal_values: List[int]) -> int:
        """
        Calculate agreement score from signal values.

        Lower standard deviation = higher agreement = higher confidence.
        """
        if len(signal_values) < 2:
            return 85  # Single signal, assume good agreement

        # Calculate mean
        mean = sum(signal_values) / len(signal_values)

        # Calculate standard deviation
        variance = sum((v - mean) ** 2 for v in signal_values) / len(signal_values)
        std_dev = math.sqrt(variance)

        # Agreement score: 100 - (k * std_dev), k = 2
        agreement = max(0, 100 - (2 * std_dev))

        return int(round(agreement))

    def _generate_card_text(
        self,
        card_id: str,
        score: int,
        base_signals: Dict,
        language: str
    ) -> str:
        """Generate human-readable text for a card based on score."""

        # Text templates by language
        templates = {
            "dasha_mood": {
                "high": {
                    "ta": f"{base_signals['dasha']['lord']} தசை: மகிழ்ச்சியான தொடர்புகள்; பேச்சுவார்த்தைக்கு நல்லது.",
                    "en": f"{base_signals['dasha']['lord']} dasha: Pleasant interactions; good for negotiations.",
                    "kn": f"{base_signals['dasha']['lord']} ದಶೆ: ಆಹ್ಲಾದಕರ ಸಂವಹನ; ಮಾತುಕತೆಗೆ ಒಳ್ಳೆಯದು."
                },
                "medium": {
                    "ta": f"{base_signals['dasha']['lord']} தசை: சீரான நாள்; திட்டமிட்ட செயல்களுக்கு ஏற்றது.",
                    "en": f"{base_signals['dasha']['lord']} dasha: Balanced day; good for planned activities.",
                    "kn": f"{base_signals['dasha']['lord']} ದಶೆ: ಸಮತೋಲಿತ ದಿನ; ಯೋಜಿತ ಚಟುವಟಿಕೆಗಳಿಗೆ ಒಳ್ಳೆಯದು."
                },
                "low": {
                    "ta": f"{base_signals['dasha']['lord']} தசை: பொறுமையாக இருங்கள்; முக்கிய முடிவுகளை தவிர்க்கவும்.",
                    "en": f"{base_signals['dasha']['lord']} dasha: Stay patient; avoid major decisions.",
                    "kn": f"{base_signals['dasha']['lord']} ದಶೆ: ತಾಳ್ಮೆಯಿಂದಿರಿ; ಪ್ರಮುಖ ನಿರ್ಧಾರಗಳನ್ನು ತಪ್ಪಿಸಿ."
                }
            },
            "transit_pressure": {
                "high": {
                    "ta": "கிரக அழுத்தம் குறைவு — சுமுகமான நாள்.",
                    "en": "Low planetary pressure — smooth sailing today.",
                    "kn": "ಗ್ರಹ ಒತ್ತಡ ಕಡಿಮೆ — ಸುಗಮ ದಿನ."
                },
                "medium": {
                    "ta": "மிதமான கிரக அழுத்தம் — கவனமாக செயல்படுங்கள்.",
                    "en": "Moderate planetary influence — proceed with awareness.",
                    "kn": "ಮಧ್ಯಮ ಗ್ರಹ ಪ್ರಭಾವ — ಜಾಗರೂಕರಾಗಿ ಮುಂದುವರಿಯಿರಿ."
                },
                "low": {
                    "ta": "அதிக கிரக அழுத்தம் — புதிய முயற்சிகளை தவிர்க்கவும்.",
                    "en": "High planetary pressure — avoid new initiatives.",
                    "kn": "ಹೆಚ್ಚಿನ ಗ್ರಹ ಒತ್ತಡ — ಹೊಸ ಉಪಕ್ರಮಗಳನ್ನು ತಪ್ಪಿಸಿ."
                }
            },
            "finance_outlook": {
                "high": {
                    "ta": "நிதி நிலை சிறப்பு — முதலீடுகளுக்கு நல்ல நாள்.",
                    "en": "Excellent finance day — good for investments.",
                    "kn": "ಆರ್ಥಿಕ ಪರಿಸ್ಥಿತಿ ಉತ್ತಮ — ಹೂಡಿಕೆಗೆ ಒಳ್ಳೆಯ ದಿನ."
                },
                "medium": {
                    "ta": "சராசரி நிதி நாள் — பழைய விஷயங்களை முடிக்கவும்.",
                    "en": "Average finance day — follow up on pending matters.",
                    "kn": "ಸಾಮಾನ್ಯ ಹಣಕಾಸು ದಿನ — ಬಾಕಿ ವಿಷಯಗಳ ಅನುಸರಣೆ."
                },
                "low": {
                    "ta": "புதிய நிதி முடிவுகளை தவிர்க்கவும்.",
                    "en": "Avoid new financial commitments today.",
                    "kn": "ಹೊಸ ಆರ್ಥಿಕ ಬದ್ಧತೆಗಳನ್ನು ತಪ್ಪಿಸಿ."
                }
            },
            "work_career": {
                "high": {
                    "ta": "தொழில் வளர்ச்சிக்கு சிறந்த நாள் — முன்னெடுங்கள்.",
                    "en": "Excellent day for career growth — take initiative.",
                    "kn": "ವೃತ್ತಿ ಬೆಳವಣಿಗೆಗೆ ಅತ್ಯುತ್ತಮ ದಿನ — ಮುಂದುವರಿಯಿರಿ."
                },
                "medium": {
                    "ta": "நிலையான வேலை நாள் — வழக்கமான பணிகளை முடிக்கவும்.",
                    "en": "Steady work day — complete routine tasks.",
                    "kn": "ಸ್ಥಿರ ಕೆಲಸದ ದಿನ — ದಿನಚರಿ ಕಾರ್ಯಗಳನ್ನು ಮುಗಿಸಿ."
                },
                "low": {
                    "ta": "ஓய்வு எடுங்கள் — முக்கிய ஒப்பந்தங்களை தவிர்க்கவும்.",
                    "en": "Take it easy — avoid important deals.",
                    "kn": "ಸಾವಕಾಶವಾಗಿ ತೆಗೆದುಕೊಳ್ಳಿ — ಪ್ರಮುಖ ಒಪ್ಪಂದಗಳನ್ನು ತಪ್ಪಿಸಿ."
                }
            },
            "relationship_energy": {
                "high": {
                    "ta": "உறவுகளுக்கு சிறந்த நாள் — அன்பை பகிரவும்.",
                    "en": "Great day for relationships — share love.",
                    "kn": "ಸಂಬಂಧಗಳಿಗೆ ಉತ್ತಮ ದಿನ — ಪ್ರೀತಿಯನ್ನು ಹಂಚಿಕೊಳ್ಳಿ."
                },
                "medium": {
                    "ta": "சீரான உறவு சக்தி — கேளுங்கள், புரிந்துகொள்ளுங்கள்.",
                    "en": "Balanced relationship energy — listen and understand.",
                    "kn": "ಸಮತೋಲಿತ ಸಂಬಂಧ ಶಕ್ತಿ — ಆಲಿಸಿ ಮತ್ತು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಿ."
                },
                "low": {
                    "ta": "பொறுமை அவசியம் — வாதங்களை தவிர்க்கவும்.",
                    "en": "Patience needed — avoid arguments.",
                    "kn": "ತಾಳ್ಮೆ ಅಗತ್ಯ — ವಾದಗಳನ್ನು ತಪ್ಪಿಸಿ."
                }
            },
            "health_vibration": {
                "high": {
                    "ta": "ஆரோக்கிய சக்தி நல்லது — உடற்பயிற்சி செய்யவும்.",
                    "en": "Good health energy — exercise recommended.",
                    "kn": "ಆರೋಗ್ಯ ಶಕ್ತಿ ಒಳ್ಳೆಯದು — ವ್ಯಾಯಾಮ ಶಿಫಾರಸು."
                },
                "medium": {
                    "ta": "சராசரி ஆரோக்கிய நாள் — ஓய்வு எடுங்கள்.",
                    "en": "Average health day — take rest when needed.",
                    "kn": "ಸಾಮಾನ್ಯ ಆರೋಗ್ಯ ದಿನ — ಅಗತ್ಯವಿದ್ದಾಗ ವಿಶ್ರಾಂತಿ ತೆಗೆದುಕೊಳ್ಳಿ."
                },
                "low": {
                    "ta": "ஆரோக்கியத்தில் கவனம் — அதிக உழைப்பு வேண்டாம்.",
                    "en": "Watch your health — avoid overexertion.",
                    "kn": "ಆರೋಗ್ಯದ ಕಡೆ ಗಮನ — ಅತಿಯಾದ ಶ್ರಮ ತಪ್ಪಿಸಿ."
                }
            },
            "lucky_window": {
                "high": {
                    "ta": f"அதிர்ஷ்ட நேரம்: {base_signals['lucky_time']['start']} - {base_signals['lucky_time']['end']}",
                    "en": f"Lucky window: {base_signals['lucky_time']['start']} - {base_signals['lucky_time']['end']}",
                    "kn": f"ಅದೃಷ್ಟದ ಸಮಯ: {base_signals['lucky_time']['start']} - {base_signals['lucky_time']['end']}"
                },
                "medium": {
                    "ta": f"நல்ல நேரம்: {base_signals['lucky_time']['start']} - {base_signals['lucky_time']['end']}",
                    "en": f"Good time: {base_signals['lucky_time']['start']} - {base_signals['lucky_time']['end']}",
                    "kn": f"ಒಳ್ಳೆಯ ಸಮಯ: {base_signals['lucky_time']['start']} - {base_signals['lucky_time']['end']}"
                },
                "low": {
                    "ta": f"சாத்தியமான நேரம்: {base_signals['lucky_time']['start']} - {base_signals['lucky_time']['end']}",
                    "en": f"Possible window: {base_signals['lucky_time']['start']} - {base_signals['lucky_time']['end']}",
                    "kn": f"ಸಾಧ್ಯವಾದ ಸಮಯ: {base_signals['lucky_time']['start']} - {base_signals['lucky_time']['end']}"
                }
            },
            "avoid_window": {
                "high": {
                    "ta": f"ராகு காலம்: {base_signals['avoid_time']['start']} - {base_signals['avoid_time']['end']} — கவனம்.",
                    "en": f"Rahu Kalam: {base_signals['avoid_time']['start']} - {base_signals['avoid_time']['end']} — be cautious.",
                    "kn": f"ರಾಹು ಕಾಲ: {base_signals['avoid_time']['start']} - {base_signals['avoid_time']['end']} — ಎಚ್ಚರವಾಗಿರಿ."
                },
                "medium": {
                    "ta": f"தவிர்க்க: {base_signals['avoid_time']['start']} - {base_signals['avoid_time']['end']}",
                    "en": f"Avoid: {base_signals['avoid_time']['start']} - {base_signals['avoid_time']['end']}",
                    "kn": f"ತಪ்ಪಿಸಿ: {base_signals['avoid_time']['start']} - {base_signals['avoid_time']['end']}"
                },
                "low": {
                    "ta": f"கவனம்: {base_signals['avoid_time']['start']} - {base_signals['avoid_time']['end']}",
                    "en": f"Caution: {base_signals['avoid_time']['start']} - {base_signals['avoid_time']['end']}",
                    "kn": f"ಎಚ್ಚರಿಕೆ: {base_signals['avoid_time']['start']} - {base_signals['avoid_time']['end']}"
                }
            },
            "opportunity_indicator": {
                "high": {
                    "ta": "வலுவான வாய்ப்புகள் — தைரியமாக செயல்படுங்கள்.",
                    "en": "Strong opportunities — act confidently.",
                    "kn": "ಬಲವಾದ ಅವಕಾಶಗಳು — ಧೈರ್ಯದಿಂದ ಕಾರ್ಯನಿರ್ವಹಿಸಿ."
                },
                "medium": {
                    "ta": "மிதமான வாய்ப்புகள் — திட்டமிட்டு செயல்படுங்கள்.",
                    "en": "Moderate opportunities — proceed with planning.",
                    "kn": "ಮಧ್ಯಮ ಅವಕಾಶಗಳು — ಯೋಜನೆಯೊಂದಿಗೆ ಮುಂದುವರಿಯಿರಿ."
                },
                "low": {
                    "ta": "குறைவான வாய்ப்புகள் — காத்திருங்கள்.",
                    "en": "Limited opportunities — wait for better timing.",
                    "kn": "ಸೀಮಿತ ಅವಕಾಶಗಳು — ಉತ್ತಮ ಸಮಯಕ್ಕಾಗಿ ಕಾಯಿರಿ."
                }
            },
            "risk_indicator": {
                "high": {
                    "ta": "குறைவான அபாயம் — நிம்மதியாக இருங்கள்.",
                    "en": "Low risk — stay relaxed.",
                    "kn": "ಕಡಿಮೆ ಅಪಾಯ — ನಿಶ್ಚಿಂತೆಯಾಗಿರಿ."
                },
                "medium": {
                    "ta": "மிதமான அபாயம் — கவனமாக இருங்கள்.",
                    "en": "Moderate risk — stay cautious.",
                    "kn": "ಮಧ್ಯಮ ಅಪಾಯ — ಜಾಗರೂಕರಾಗಿರಿ."
                },
                "low": {
                    "ta": "உயர் அபாயம் — முக்கிய முடிவுகளை தவிர்க்கவும்.",
                    "en": "High risk alert — avoid major decisions.",
                    "kn": "ಹೆಚ್ಚಿನ ಅಪಾಯ — ಪ್ರಮುಖ ನಿರ್ಧಾರಗಳನ್ನು ತಪ್ಪಿಸಿ."
                }
            },
            "color_direction": {
                "high": {
                    "ta": self._get_color_direction_text(base_signals, "ta"),
                    "en": self._get_color_direction_text(base_signals, "en"),
                    "kn": self._get_color_direction_text(base_signals, "kn")
                },
                "medium": {
                    "ta": self._get_color_direction_text(base_signals, "ta"),
                    "en": self._get_color_direction_text(base_signals, "en"),
                    "kn": self._get_color_direction_text(base_signals, "kn")
                },
                "low": {
                    "ta": self._get_color_direction_text(base_signals, "ta"),
                    "en": self._get_color_direction_text(base_signals, "en"),
                    "kn": self._get_color_direction_text(base_signals, "kn")
                }
            },
            "personal_note": {
                "high": {
                    "ta": "சிறந்த நாள்! உங்கள் திட்டங்களை தைரியமாக செயல்படுத்துங்கள்.",
                    "en": "Great day! Execute your plans with confidence.",
                    "kn": "ಅದ್ಭುತ ದಿನ! ನಿಮ್ಮ ಯೋಜನೆಗಳನ್ನು ಧೈರ್ಯದಿಂದ ಕಾರ್ಯಗತಗೊಳಿಸಿ."
                },
                "medium": {
                    "ta": "நல்ல நாள். வழக்கமான பணிகளை முடிப்பதில் கவனம் செலுத்துங்கள்.",
                    "en": "Good day. Focus on completing routine tasks.",
                    "kn": "ಒಳ್ಳೆಯ ದಿನ. ದಿನಚರಿ ಕಾರ್ಯಗಳನ್ನು ಮುಗಿಸುವುದರ ಮೇಲೆ ಕೇಂದ್ರೀಕರಿಸಿ."
                },
                "low": {
                    "ta": "ஓய்வு எடுங்கள். முக்கிய முடிவுகளை நாளைக்கு தள்ளிவையுங்கள்.",
                    "en": "Take rest. Postpone major decisions to tomorrow.",
                    "kn": "ವಿಶ್ರಾಂತಿ ತೆಗೆದುಕೊಳ್ಳಿ. ಪ್ರಮುಖ ನಿರ್ಧಾರಗಳನ್ನು ನಾಳೆಗೆ ಮುಂದೂಡಿ."
                }
            }
        }

        # Determine score level
        if score >= 75:
            level = "high"
        elif score >= 50:
            level = "medium"
        else:
            level = "low"

        # Get template for this card
        card_templates = templates.get(card_id, {})
        level_templates = card_templates.get(level, card_templates.get("medium", {}))

        return level_templates.get(language, level_templates.get("en", ""))

    def _get_color_direction_text(self, base_signals: Dict, language: str) -> str:
        """Generate color and direction recommendation text."""
        nakshatra_ruler = base_signals["nakshatra_ruler"]
        weekday_ruler = base_signals["weekday_ruler"]

        # Use nakshatra ruler primarily
        color_info = PLANET_COLORS.get(nakshatra_ruler, PLANET_COLORS["Sun"])
        direction_info = PLANET_DIRECTIONS.get(weekday_ruler, PLANET_DIRECTIONS["Sun"])

        color_key = f"color_{language}"
        direction_key = f"direction_{language}"

        color = color_info.get(color_key, color_info.get("color_en", "Orange"))
        direction = direction_info.get(direction_key, direction_info.get("direction_en", "East"))

        if language == "ta":
            return f"நிறம்: {color} | திசை: {direction}"
        elif language == "kn":
            return f"ಬಣ್ಣ: {color} | ದಿಕ್ಕು: {direction}"
        else:
            return f"Color: {color} | Direction: {direction}"

    def _generate_summary(self, cards: List[Dict], language: str) -> str:
        """Generate a one-line summary from the cards."""
        # Find top 2 cards by score
        sorted_cards = sorted(cards, key=lambda x: x["score"], reverse=True)

        top_card = sorted_cards[0]
        second_card = sorted_cards[1]

        avg_score = sum(c["score"] for c in cards) / len(cards)

        if language == "ta":
            if avg_score >= 75:
                return f"சிறப்பான நாள்; {top_card['title']} மற்றும் {second_card['title']} சாதகம்."
            elif avg_score >= 50:
                return f"சீரான நாள்; பணிகளை முடிக்க நல்லது; அவசர முடிவுகளை தவிர்க்கவும்."
            else:
                return f"பொறுமையான நாள்; {sorted_cards[-1]['title']} கவனம் தேவை."
        elif language == "kn":
            if avg_score >= 75:
                return f"ಅದ್ಭುತ ದಿನ; {top_card['title']} ಮತ್ತು {second_card['title']} ಅನುಕೂಲ."
            elif avg_score >= 50:
                return f"ಸಮತೋಲಿತ ದಿನ; ಕಾರ್ಯಗಳನ್ನು ಮುಗಿಸಲು ಒಳ್ಳೆಯದು."
            else:
                return f"ತಾಳ್ಮೆಯ ದಿನ; {sorted_cards[-1]['title']} ಗಮನ ಬೇಕು."
        else:
            if avg_score >= 75:
                return f"Excellent day; {top_card['title']} and {second_card['title']} are favorable."
            elif avg_score >= 50:
                return f"Balanced day; good for completing tasks; avoid impulsive decisions."
            else:
                return f"Patient day; {sorted_cards[-1]['title']} needs attention."
