"""
Muhurtham Finder Service
Finds auspicious times based on Panchangam data
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Optional
import calendar

from app.services.ephemeris import EphemerisService, NAKSHATRAS, RASIS
from app.services.panchangam_calculator import PanchangamCalculator


# Translations for muhurtham labels
TRANSLATIONS = {
    "ta": {  # Tamil
        # Time slot labels
        "brahma_muhurtham": "பிரம்ம முகூர்த்தம்",
        "abhijit_muhurtham": "அபிஜித் முகூர்த்தம்",
        "morning_good_time": "காலை நல்ல நேரம்",
        "afternoon_time": "மதிய நேரம்",
        "evening_time": "சாயங்கால நேரம்",
        "rahu_kalam": "ராகு காலம்",
        "yamagandam": "யமகண்டம்",
        "kuligai": "குளிகை",
        # Quality labels
        "excellent": "சிறந்தது",
        "good": "நல்லது",
        "average": "சாதாரணம்",
        # Factor names
        "tithi": "திதி",
        "nakshatra": "நட்சத்திரம்",
        "time": "நேரம்",
        # Warnings
        "rahu_kalam_avoid": "ராகு காலம் - தவிர்க்கவும்",
        "yamagandam_caution": "யமகண்டம் - கவனம்",
        # Event types
        "marriage": "திருமணம்",
        "griha_pravesam": "கிரகப்பிரவேசம்",
        "vehicle": "வாகனம்",
        "business": "வியாபாரம்",
        "travel": "பயணம்",
        "general": "பொது",
        # Festivals/Warnings
        "purnima": "பூர்ணிமா",
        "amavasya": "அமாவாசை",
        "tuesday": "செவ்வாய்",
        # Weekdays
        "sunday": "ஞாயிறு",
        "monday": "திங்கள்",
        "wednesday": "புதன்",
        "thursday": "வியாழன்",
        "friday": "வெள்ளி",
        "saturday": "சனி",
    },
    "en": {  # English
        # Time slot labels
        "brahma_muhurtham": "Brahma Muhurtham",
        "abhijit_muhurtham": "Abhijit Muhurtham",
        "morning_good_time": "Morning Auspicious Time",
        "afternoon_time": "Afternoon Time",
        "evening_time": "Evening Time",
        "rahu_kalam": "Rahu Kalam",
        "yamagandam": "Yamagandam",
        "kuligai": "Kuligai",
        # Quality labels
        "excellent": "Excellent",
        "good": "Good",
        "average": "Average",
        # Factor names
        "tithi": "Tithi",
        "nakshatra": "Nakshatra",
        "time": "Time",
        # Warnings
        "rahu_kalam_avoid": "Rahu Kalam - Avoid",
        "yamagandam_caution": "Yamagandam - Caution",
        # Event types
        "marriage": "Marriage",
        "griha_pravesam": "Housewarming",
        "vehicle": "Vehicle",
        "business": "Business",
        "travel": "Travel",
        "general": "General",
        # Festivals/Warnings
        "purnima": "Full Moon",
        "amavasya": "New Moon",
        "tuesday": "Tuesday",
        # Weekdays
        "sunday": "Sunday",
        "monday": "Monday",
        "wednesday": "Wednesday",
        "thursday": "Thursday",
        "friday": "Friday",
        "saturday": "Saturday",
    },
    "kn": {  # Kannada
        # Time slot labels
        "brahma_muhurtham": "ಬ್ರಹ್ಮ ಮುಹೂರ್ತ",
        "abhijit_muhurtham": "ಅಭಿಜಿತ್ ಮುಹೂರ್ತ",
        "morning_good_time": "ಬೆಳಿಗ್ಗೆ ಒಳ್ಳೆಯ ಸಮಯ",
        "afternoon_time": "ಮಧ್ಯಾಹ್ನದ ಸಮಯ",
        "evening_time": "ಸಂಜೆ ಸಮಯ",
        "rahu_kalam": "ರಾಹು ಕಾಲ",
        "yamagandam": "ಯಮಗಂಡ",
        "kuligai": "ಗುಳಿಕ",
        # Quality labels
        "excellent": "ಅತ್ಯುತ್ತಮ",
        "good": "ಒಳ್ಳೆಯದು",
        "average": "ಸಾಮಾನ್ಯ",
        # Factor names
        "tithi": "ತಿಥಿ",
        "nakshatra": "ನಕ್ಷತ್ರ",
        "time": "ಸಮಯ",
        # Warnings
        "rahu_kalam_avoid": "ರಾಹು ಕಾಲ - ತಪ್ಪಿಸಿ",
        "yamagandam_caution": "ಯಮಗಂಡ - ಎಚ್ಚರಿಕೆ",
        # Event types
        "marriage": "ಮದುವೆ",
        "griha_pravesam": "ಗೃಹಪ್ರವೇಶ",
        "vehicle": "ವಾಹನ",
        "business": "ವ್ಯಾಪಾರ",
        "travel": "ಪ್ರಯಾಣ",
        "general": "ಸಾಮಾನ್ಯ",
        # Festivals/Warnings
        "purnima": "ಹುಣ್ಣಿಮೆ",
        "amavasya": "ಅಮಾವಾಸ್ಯೆ",
        "tuesday": "ಮಂಗಳವಾರ",
        # Weekdays
        "sunday": "ಭಾನುವಾರ",
        "monday": "ಸೋಮವಾರ",
        "wednesday": "ಬುಧವಾರ",
        "thursday": "ಗುರುವಾರ",
        "friday": "ಶುಕ್ರವಾರ",
        "saturday": "ಶನಿವಾರ",
    }
}

# Nakshatra translations
NAKSHATRA_TRANSLATIONS = {
    "en": {
        "Ashwini": "Ashwini", "Bharani": "Bharani", "Krittika": "Krittika",
        "Rohini": "Rohini", "Mrigashira": "Mrigashira", "Ardra": "Ardra",
        "Punarvasu": "Punarvasu", "Pushya": "Pushya", "Ashlesha": "Ashlesha",
        "Magha": "Magha", "Purva Phalguni": "Purva Phalguni", "Uttara Phalguni": "Uttara Phalguni",
        "Hasta": "Hasta", "Chitra": "Chitra", "Swati": "Swati",
        "Vishakha": "Vishakha", "Anuradha": "Anuradha", "Jyeshtha": "Jyeshtha",
        "Mula": "Mula", "Purva Ashadha": "Purva Ashadha", "Uttara Ashadha": "Uttara Ashadha",
        "Shravana": "Shravana", "Dhanishta": "Dhanishta", "Shatabhisha": "Shatabhisha",
        "Purva Bhadrapada": "Purva Bhadrapada", "Uttara Bhadrapada": "Uttara Bhadrapada", "Revati": "Revati"
    },
    "ta": {
        "Ashwini": "அஸ்வினி", "Bharani": "பரணி", "Krittika": "கிருத்திகை",
        "Rohini": "ரோகிணி", "Mrigashira": "மிருகசீரிடம்", "Ardra": "திருவாதிரை",
        "Punarvasu": "புனர்பூசம்", "Pushya": "பூசம்", "Ashlesha": "ஆயில்யம்",
        "Magha": "மகம்", "Purva Phalguni": "பூரம்", "Uttara Phalguni": "உத்திரம்",
        "Hasta": "அஸ்தம்", "Chitra": "சித்திரை", "Swati": "சுவாதி",
        "Vishakha": "விசாகம்", "Anuradha": "அனுஷம்", "Jyeshtha": "கேட்டை",
        "Mula": "மூலம்", "Purva Ashadha": "பூராடம்", "Uttara Ashadha": "உத்திராடம்",
        "Shravana": "திருவோணம்", "Dhanishta": "அவிட்டம்", "Shatabhisha": "சதயம்",
        "Purva Bhadrapada": "பூரட்டாதி", "Uttara Bhadrapada": "உத்திரட்டாதி", "Revati": "ரேவதி"
    },
    "kn": {
        "Ashwini": "ಅಶ್ವಿನಿ", "Bharani": "ಭರಣಿ", "Krittika": "ಕೃತ್ತಿಕಾ",
        "Rohini": "ರೋಹಿಣಿ", "Mrigashira": "ಮೃಗಶಿರಾ", "Ardra": "ಆರ್ದ್ರಾ",
        "Punarvasu": "ಪುನರ್ವಸು", "Pushya": "ಪುಷ್ಯ", "Ashlesha": "ಆಶ್ಲೇಷಾ",
        "Magha": "ಮಘಾ", "Purva Phalguni": "ಪೂರ್ವ ಫಲ್ಗುಣಿ", "Uttara Phalguni": "ಉತ್ತರ ಫಲ್ಗುಣಿ",
        "Hasta": "ಹಸ್ತ", "Chitra": "ಚಿತ್ರಾ", "Swati": "ಸ್ವಾತಿ",
        "Vishakha": "ವಿಶಾಖಾ", "Anuradha": "ಅನುರಾಧಾ", "Jyeshtha": "ಜ್ಯೇಷ್ಠಾ",
        "Mula": "ಮೂಲಾ", "Purva Ashadha": "ಪೂರ್ವಾಷಾಢ", "Uttara Ashadha": "ಉತ್ತರಾಷಾಢ",
        "Shravana": "ಶ್ರವಣ", "Dhanishta": "ಧನಿಷ್ಠಾ", "Shatabhisha": "ಶತಭಿಷಾ",
        "Purva Bhadrapada": "ಪೂರ್ವಭಾದ್ರಪದ", "Uttara Bhadrapada": "ಉತ್ತರಭಾದ್ರಪದ", "Revati": "ರೇವತಿ"
    }
}

# Tithi translations
TITHI_TRANSLATIONS = {
    "en": {
        "Pratipada": "Pratipada", "Dwitiya": "Dwitiya", "Tritiya": "Tritiya",
        "Chaturthi": "Chaturthi", "Panchami": "Panchami", "Shashthi": "Shashthi",
        "Saptami": "Saptami", "Ashtami": "Ashtami", "Navami": "Navami",
        "Dashami": "Dashami", "Ekadashi": "Ekadashi", "Dwadashi": "Dwadashi",
        "Trayodashi": "Trayodashi", "Chaturdashi": "Chaturdashi",
        "Purnima": "Purnima (Full Moon)", "Amavasya": "Amavasya (New Moon)"
    },
    "ta": {
        "Pratipada": "பிரதமை", "Dwitiya": "துவிதியை", "Tritiya": "திருதியை",
        "Chaturthi": "சதுர்த்தி", "Panchami": "பஞ்சமி", "Shashthi": "சஷ்டி",
        "Saptami": "சப்தமி", "Ashtami": "அஷ்டமி", "Navami": "நவமி",
        "Dashami": "தசமி", "Ekadashi": "ஏகாதசி", "Dwadashi": "துவாதசி",
        "Trayodashi": "திரயோதசி", "Chaturdashi": "சதுர்தசி",
        "Purnima": "பூர்ணிமா", "Amavasya": "அமாவாசை"
    },
    "kn": {
        "Pratipada": "ಪಾಡ್ಯ", "Dwitiya": "ಬಿದಿಗೆ", "Tritiya": "ತದಿಗೆ",
        "Chaturthi": "ಚತುರ್ಥಿ", "Panchami": "ಪಂಚಮಿ", "Shashthi": "ಷಷ್ಠಿ",
        "Saptami": "ಸಪ್ತಮಿ", "Ashtami": "ಅಷ್ಟಮಿ", "Navami": "ನವಮಿ",
        "Dashami": "ದಶಮಿ", "Ekadashi": "ಏಕಾದಶಿ", "Dwadashi": "ದ್ವಾದಶಿ",
        "Trayodashi": "ತ್ರಯೋದಶಿ", "Chaturdashi": "ಚತುರ್ದಶಿ",
        "Purnima": "ಹುಣ್ಣಿಮೆ", "Amavasya": "ಅಮಾವಾಸ್ಯೆ"
    }
}

# Yoga translations
YOGA_TRANSLATIONS = {
    "en": {
        "Vishkumbha": "Vishkumbha", "Priti": "Priti", "Ayushman": "Ayushman",
        "Saubhagya": "Saubhagya", "Shobhana": "Shobhana", "Atiganda": "Atiganda",
        "Sukarma": "Sukarma", "Dhriti": "Dhriti", "Shula": "Shula",
        "Ganda": "Ganda", "Vriddhi": "Vriddhi", "Dhruva": "Dhruva",
        "Vyaghata": "Vyaghata", "Harshana": "Harshana", "Vajra": "Vajra",
        "Siddhi": "Siddhi", "Vyatipata": "Vyatipata", "Variyan": "Variyan",
        "Parigha": "Parigha", "Shiva": "Shiva", "Siddha": "Siddha",
        "Sadhya": "Sadhya", "Shubha": "Shubha", "Shukla": "Shukla",
        "Brahma": "Brahma", "Indra": "Indra", "Vaidhriti": "Vaidhriti"
    },
    "ta": {
        "Vishkumbha": "விஷ்கும்பம்", "Priti": "பிரீதி", "Ayushman": "ஆயுஷ்மான்",
        "Saubhagya": "சௌபாக்கியம்", "Shobhana": "சோபனம்", "Atiganda": "அதிகண்டம்",
        "Sukarma": "சுகர்மம்", "Dhriti": "திருதி", "Shula": "சூலம்",
        "Ganda": "கண்டம்", "Vriddhi": "விருத்தி", "Dhruva": "த்ருவம்",
        "Vyaghata": "வியாகாதம்", "Harshana": "ஹர்ஷணம்", "Vajra": "வஜ்ரம்",
        "Siddhi": "சித்தி", "Vyatipata": "வியதிபாதம்", "Variyan": "வரியான்",
        "Parigha": "பரிகம்", "Shiva": "சிவம்", "Siddha": "சித்தம்",
        "Sadhya": "சாத்தியம்", "Shubha": "சுபம்", "Shukla": "சுக்லம்",
        "Brahma": "பிரம்மம்", "Indra": "இந்திரம்", "Vaidhriti": "வைத்ருதி"
    },
    "kn": {
        "Vishkumbha": "ವಿಷ್ಕುಂಭ", "Priti": "ಪ್ರೀತಿ", "Ayushman": "ಆಯುಷ್ಮಾನ್",
        "Saubhagya": "ಸೌಭಾಗ್ಯ", "Shobhana": "ಶೋಭನ", "Atiganda": "ಅತಿಗಂಡ",
        "Sukarma": "ಸುಕರ್ಮ", "Dhriti": "ಧೃತಿ", "Shula": "ಶೂಲ",
        "Ganda": "ಗಂಡ", "Vriddhi": "ವೃದ್ಧಿ", "Dhruva": "ಧ್ರುವ",
        "Vyaghata": "ವ್ಯಾಘಾತ", "Harshana": "ಹರ್ಷಣ", "Vajra": "ವಜ್ರ",
        "Siddhi": "ಸಿದ್ಧಿ", "Vyatipata": "ವ್ಯತೀಪಾತ", "Variyan": "ವರಿಯಾನ್",
        "Parigha": "ಪರಿಘ", "Shiva": "ಶಿವ", "Siddha": "ಸಿದ್ಧ",
        "Sadhya": "ಸಾಧ್ಯ", "Shubha": "ಶುಭ", "Shukla": "ಶುಕ್ಲ",
        "Brahma": "ಬ್ರಹ್ಮ", "Indra": "ಇಂದ್ರ", "Vaidhriti": "ವೈಧೃತಿ"
    }
}


def get_translation(key: str, lang: str = "ta") -> str:
    """Get translation for a key"""
    translations = TRANSLATIONS.get(lang, TRANSLATIONS["ta"])
    return translations.get(key, TRANSLATIONS["ta"].get(key, key))


def translate_nakshatra(name: str, lang: str = "ta") -> str:
    """Translate nakshatra name"""
    translations = NAKSHATRA_TRANSLATIONS.get(lang, NAKSHATRA_TRANSLATIONS["ta"])
    return translations.get(name, name)


def translate_tithi(name: str, lang: str = "ta") -> str:
    """Translate tithi name"""
    translations = TITHI_TRANSLATIONS.get(lang, TITHI_TRANSLATIONS["ta"])
    return translations.get(name, name)


def translate_yoga(name: str, lang: str = "ta") -> str:
    """Translate yoga name"""
    translations = YOGA_TRANSLATIONS.get(lang, YOGA_TRANSLATIONS["ta"])
    return translations.get(name, name)


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

    def __init__(self, ephemeris: EphemerisService, lang: str = "ta"):
        self.ephemeris = ephemeris
        self.panchangam = PanchangamCalculator(ephemeris)
        self.lang = lang  # Language for translations

    def find_slots(
        self,
        event_type: str,
        start_date: date,
        end_date: date,
        lat: float,
        lon: float,
        user_nakshatra: Optional[str] = None,
        lang: Optional[str] = None
    ) -> List[Dict]:
        """
        Find auspicious time slots within a date range
        Returns list of MuhurthamSlot dictionaries
        """
        use_lang = lang or self.lang
        slots = []
        current = start_date

        while current <= end_date:
            day_slots = self._find_day_slots(current, event_type, lat, lon, user_nakshatra, use_lang)
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
        user_nakshatra: Optional[str] = None,
        lang: str = "ta"
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
        time_slots = self._get_good_time_slots(target_date, panchang, lat, lon, lang)

        for slot in time_slots:
            quality_score = min(100, day_score + slot["bonus"])

            factors = self._get_factors(panchang, slot, event_type, lang)
            conflicts = self._get_conflicts(slot, panchang, lang)

            if slot["is_rahu_kalam"]:
                continue  # Skip Rahu Kalam slots

            quality_label = get_translation("excellent", lang) if quality_score >= 80 else get_translation("good", lang) if quality_score >= 60 else get_translation("average", lang)

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

    def _get_good_time_slots(self, target_date: date, panchang: Dict, lat: float, lon: float, lang: str = "ta") -> List[Dict]:
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
            "name": get_translation("brahma_muhurtham", lang),
            "start": f"{max(4, brahma_start_h):02d}:{brahma_start_m:02d}",
            "end": sunrise,
            "bonus": 25,
            "is_rahu_kalam": False
        })

        # Abhijit Muhurta (around noon, ~48 minutes centered at local noon)
        noon_h = (sr_h + ss_h) // 2
        slots.append({
            "name": get_translation("abhijit_muhurtham", lang),
            "start": f"{noon_h - 1}:36",
            "end": f"{noon_h}:24",
            "bonus": 20,
            "is_rahu_kalam": in_rahu_kalam(noon_h, 0)
        })

        # Morning slot (after sunrise, before noon)
        morning_end_h = min(sr_h + 4, 12)
        slots.append({
            "name": get_translation("morning_good_time", lang),
            "start": f"{sr_h + 1:02d}:00",
            "end": f"{morning_end_h:02d}:00",
            "bonus": 10,
            "is_rahu_kalam": any(in_rahu_kalam(h, 0) for h in range(sr_h + 1, morning_end_h))
        })

        # Afternoon slot
        slots.append({
            "name": get_translation("afternoon_time", lang),
            "start": "14:00",
            "end": "16:00",
            "bonus": 5,
            "is_rahu_kalam": any(in_rahu_kalam(h, 0) for h in range(14, 16))
        })

        # Evening slot (before sunset)
        slots.append({
            "name": get_translation("evening_time", lang),
            "start": f"{ss_h - 2:02d}:00",
            "end": f"{ss_h:02d}:00",
            "bonus": 8,
            "is_rahu_kalam": any(in_rahu_kalam(h, 0) for h in range(ss_h - 2, ss_h))
        })

        return slots

    def _get_factors(self, panchang: Dict, slot: Dict, event_type: str, lang: str = "ta") -> List[Dict]:
        """Get contributing factors for display"""
        factors = []

        # Tithi factor
        tithi_name = panchang.get("tithi", {}).get("name", "Unknown")
        tithi_translated = translate_tithi(tithi_name, lang)
        is_good_tithi = tithi_name in GOOD_TITHIS

        factors.append({
            "name": get_translation("tithi", lang),
            "value": tithi_translated,
            "is_positive": is_good_tithi
        })

        # Nakshatra factor
        nakshatra_name = panchang.get("nakshatra", {}).get("name", "Unknown")
        nakshatra_translated = translate_nakshatra(nakshatra_name, lang)
        good_nakshatras = EVENT_NAKSHATRAS.get(event_type, EVENT_NAKSHATRAS["general"])
        is_good_nakshatra = nakshatra_name in good_nakshatras

        factors.append({
            "name": get_translation("nakshatra", lang),
            "value": nakshatra_translated,
            "is_positive": is_good_nakshatra
        })

        # Slot type factor
        factors.append({
            "name": get_translation("time", lang),
            "value": slot["name"],
            "is_positive": slot["bonus"] >= 15
        })

        return factors

    def _get_conflicts(self, slot: Dict, panchang: Dict, lang: str = "ta") -> List[str]:
        """Get any conflicts/warnings"""
        conflicts = []

        if slot.get("is_rahu_kalam"):
            conflicts.append(get_translation("rahu_kalam_avoid", lang))

        # Check for yamagandam overlap
        yama_start = panchang.get("yamagandam", {}).get("start", "")
        if yama_start and slot["start"] <= yama_start <= slot["end"]:
            conflicts.append(get_translation("yamagandam_caution", lang))

        return conflicts

    def get_month_calendar(self, month: int, year: int, lat: float, lon: float, lang: str = "ta") -> List[Dict]:
        """
        Get calendar heat map data for a month
        Returns list of CalendarDay objects with event-specific scores
        """
        days = []
        num_days = calendar.monthrange(year, month)[1]

        # Event types - use translations
        event_type_keys = ["marriage", "griha_pravesam", "vehicle", "business", "travel", "general"]

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

            for event_type in event_type_keys:
                score = self._calculate_day_score(target_date, panchang, event_type) if panchang else 50.0
                event_scores[event_type] = round(score, 1)

                # Mark as good if score >= 65
                if score >= 65:
                    good_for_events.append({
                        "type": event_type,
                        "label": get_translation(event_type, lang),
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
                festivals.append(get_translation("purnima", lang))
            elif tithi_name == "Amavasya":
                warnings.append(get_translation("amavasya", lang))

            if weekday == 1:  # Tuesday
                warnings.append(get_translation("tuesday", lang))

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

    def get_day_details(self, target_date: date, lat: float, lon: float, lang: str = "ta") -> Dict:
        """
        Get detailed muhurtham information for a specific day
        Used when user clicks on a calendar day
        """
        try:
            panchang = self.panchangam.calculate(target_date, lat, lon, "Asia/Kolkata")
        except Exception:
            return {"error": "Unable to calculate panchangam"}

        day_score = self._calculate_day_score(target_date, panchang, "general")
        time_slots = self._get_good_time_slots(target_date, panchang, lat, lon, lang)

        # Calculate event-specific scores
        event_type_keys = ["marriage", "griha_pravesam", "vehicle", "business", "travel", "general"]

        event_scores = {}
        good_for_events = []

        for event_type in event_type_keys:
            score = self._calculate_day_score(target_date, panchang, event_type)
            event_scores[event_type] = round(score, 1)

            if score >= 65:
                good_for_events.append({
                    "type": event_type,
                    "label": get_translation(event_type, lang),
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
            "label": get_translation("rahu_kalam", lang),
            "score": 0,
            "type": "avoid"
        })

        # Add Yamagandam and Kuligai as avoid slots
        yama_start = panchang.get("yamagandam", {}).get("start", "")
        yama_end = panchang.get("yamagandam", {}).get("end", "")
        if yama_start and yama_end:
            filtered_slots.append({
                "time": f"{yama_start} - {yama_end}",
                "label": get_translation("yamagandam", lang),
                "score": 0,
                "type": "caution"
            })

        kuligai_start = panchang.get("kuligai", {}).get("start", "")
        kuligai_end = panchang.get("kuligai", {}).get("end", "")
        if kuligai_start and kuligai_end:
            filtered_slots.append({
                "time": f"{kuligai_start} - {kuligai_end}",
                "label": get_translation("kuligai", lang),
                "score": 0,
                "type": "caution"
            })

        # Sort by score descending
        filtered_slots.sort(key=lambda x: x["score"], reverse=True)

        # Get weekday translation
        weekday_num = target_date.weekday()
        weekday_keys = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        weekday_key = weekday_keys[weekday_num] if weekday_num < 6 else "sunday"

        # Translate panchangam values
        tithi_data = panchang.get("tithi", {})
        nakshatra_data = panchang.get("nakshatra", {})
        yoga_data = panchang.get("yoga", {})

        translated_panchangam = {
            "tithi": {
                "name": translate_tithi(tithi_data.get("name", ""), lang),
                "paksha": tithi_data.get("paksha", ""),
                "number": tithi_data.get("number", 0)
            },
            "nakshatra": {
                "name": translate_nakshatra(nakshatra_data.get("name", ""), lang),
                "pada": nakshatra_data.get("pada", 0),
                "lord": nakshatra_data.get("lord", "")
            },
            "yoga": {
                "name": translate_yoga(yoga_data.get("name", ""), lang)
            },
            "vaaram": get_translation(weekday_key, lang),
            "sunrise": panchang.get("sunrise", ""),
            "sunset": panchang.get("sunset", ""),
            "sun_times": panchang.get("sun_times", {}),
            "moon_times": panchang.get("moon_times", {}),
            "inauspicious": panchang.get("inauspicious", {}),
            "auspicious": panchang.get("auspicious", {})
        }

        return {
            "date": target_date.isoformat(),
            "day_score": round(day_score, 1),
            "event_scores": event_scores,
            "good_for_events": good_for_events,
            "panchangam": translated_panchangam,
            "time_slots": filtered_slots,
            "recommendation": self._get_recommendation(day_score, panchang, lang)
        }

    def _get_recommendation(self, day_score: float, panchang: Dict, lang: str = "ta") -> str:
        """Generate AI-style recommendation for the day"""
        nakshatra_name = panchang.get("nakshatra", {}).get("name", "")
        tithi_name = panchang.get("tithi", {}).get("name", "")

        nakshatra_translated = translate_nakshatra(nakshatra_name, lang)
        tithi_translated = translate_tithi(tithi_name, lang)

        if lang == "en":
            if day_score >= 80:
                return (f"{nakshatra_translated} nakshatra and {tithi_translated} tithi "
                        "combine to make this a highly auspicious day. "
                        "Suitable for all good activities.")
            if day_score >= 60:
                return (f"Today is {nakshatra_translated} nakshatra. "
                        "Auspicious activities can be done during good times. "
                        "Avoid Rahu Kalam.")
            if day_score >= 40:
                return ("Average day. Take important decisions during Abhijit Muhurtham. "
                        "Avoid Rahu Kalam and Yamagandam.")
            return "Avoid starting new activities today. Do only essential tasks."

        if lang == "kn":
            if day_score >= 80:
                return (f"{nakshatra_translated} ನಕ್ಷತ್ರ ಮತ್ತು {tithi_translated} ತಿಥಿ "
                        "ಸೇರಿ ಅತ್ಯಂತ ಶುಭ ದಿನ. ಎಲ್ಲಾ ಶುಭ ಕಾರ್ಯಗಳಿಗೆ ಸೂಕ್ತ.")
            if day_score >= 60:
                return (f"ಇಂದು {nakshatra_translated} ನಕ್ಷತ್ರ. "
                        "ಒಳ್ಳೆಯ ಸಮಯದಲ್ಲಿ ಶುಭ ಕಾರ್ಯಗಳನ್ನು ಮಾಡಬಹುದು. ರಾಹು ಕಾಲ ತಪ್ಪಿಸಿ.")
            if day_score >= 40:
                return ("ಸಾಮಾನ್ಯ ದಿನ. ಅಭಿಜಿತ್ ಮುಹೂರ್ತದಲ್ಲಿ ಮುಖ್ಯ ನಿರ್ಧಾರಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳಿ. "
                        "ರಾಹು ಕಾಲ ಮತ್ತು ಯಮಗಂಡ ತಪ್ಪಿಸಿ.")
            return "ಇಂದು ಹೊಸ ಕಾರ್ಯಗಳನ್ನು ಪ್ರಾರಂಭಿಸುವುದನ್ನು ತಪ್ಪಿಸಿ. ಅಗತ್ಯ ಕೆಲಸಗಳನ್ನು ಮಾತ್ರ ಮಾಡಿ."

        # Tamil default
        if day_score >= 80:
            return (f"{nakshatra_translated} நட்சத்திரமும் {tithi_translated} திதியும் "
                    "சேர்ந்து மிகவும் சுபகரமான நாள். அனைத்து நற்காரியங்களுக்கும் ஏற்றது.")
        if day_score >= 60:
            return (f"இன்று {nakshatra_translated} நட்சத்திரம். "
                    "நல்ல நேரங்களில் சுப காரியங்கள் செய்யலாம். ராகு காலம் தவிர்க்கவும்.")
        if day_score >= 40:
            return ("சாதாரண நாள். முக்கிய முடிவுகளை அபிஜித் முகூர்த்தத்தில் எடுக்கவும். "
                    "ராகு காலம் மற்றும் யமகண்டம் தவிர்க்கவும்.")
        return "இன்று புதிய காரியங்கள் தொடங்குவதை தவிர்க்கவும். அவசியமான பணிகளை மட்டும் செய்யவும்."
