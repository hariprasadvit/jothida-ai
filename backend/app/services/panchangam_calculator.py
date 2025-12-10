"""
Panchangam Calculator Service
Calculates daily Tamil calendar data
"""

from datetime import date, datetime, timedelta
from typing import List, Dict
from app.services.ephemeris import EphemerisService, NAKSHATRAS, RASIS


class PanchangamCalculator:
    """
    Calculate Tamil Panchangam data
    Includes tithi, nakshatra, yoga, karana, and time periods
    """
    
    TAMIL_MONTHS = [
        "சித்திரை", "வைகாசி", "ஆனி", "ஆடி", "ஆவணி", "புரட்டாசி",
        "ஐப்பசி", "கார்த்திகை", "மார்கழி", "தை", "மாசி", "பங்குனி"
    ]
    
    # Index = Python weekday (0=Monday, 1=Tuesday, ..., 6=Sunday)
    TAMIL_DAYS = [
        "திங்கள்", "செவ்வாய்", "புதன்", "வியாழன்",
        "வெள்ளி", "சனி", "ஞாயிறு"
    ]
    
    YOGAS = [
        "Vishkumbha", "Priti", "Ayushman", "Saubhagya", "Shobhana",
        "Atiganda", "Sukarma", "Dhriti", "Shula", "Ganda",
        "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
        "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
        "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
        "Indra", "Vaidhriti"
    ]
    
    KARANAS = [
        "Bava", "Balava", "Kaulava", "Taitila", "Gara",
        "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga", "Kimstughna"
    ]
    
    # Rahu Kalam timings (1/8th of day, varies by weekday)
    # Index = Python weekday (0=Monday, 1=Tuesday, ..., 6=Sunday)
    # Traditional order: Mon=2nd, Tue=7th, Wed=5th, Thu=6th, Fri=4th, Sat=3rd, Sun=8th
    RAHU_KALAM_PERIODS = [2, 7, 5, 6, 4, 3, 8]  # Mon, Tue, Wed, Thu, Fri, Sat, Sun
    YAMAGANDAM_PERIODS = [4, 3, 2, 1, 7, 6, 5]  # Mon, Tue, Wed, Thu, Fri, Sat, Sun
    KULIGAI_PERIODS = [6, 5, 4, 3, 2, 1, 7]     # Mon, Tue, Wed, Thu, Fri, Sat, Sun
    
    def __init__(self, ephemeris: EphemerisService):
        self.ephemeris = ephemeris
    
    def calculate(self, target_date: date, lat: float, lon: float, timezone: str = "Asia/Kolkata") -> Dict:
        """Calculate full panchangam for a date"""

        # Get Julian Day for midnight local time (IST = UTC+5:30)
        # We need to use the JD at local midnight to correctly find sunrise/sunset for this day
        # Local midnight IST = previous day 18:30 UTC
        dt_midnight_utc = datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0)
        # Subtract 5.5 hours to get UTC equivalent of local midnight
        from datetime import timedelta
        dt_midnight_utc = dt_midnight_utc - timedelta(hours=5, minutes=30)

        # Use direct JD calculation for the UTC time
        jd_midnight = self.ephemeris.datetime_to_jd(dt_midnight_utc, timezone="UTC")

        # Sunrise/Sunset from local midnight
        sun_times = self.ephemeris.get_sunrise_sunset(jd_midnight, lat, lon)

        # For planetary calculations, use noon local time
        dt_noon = datetime(target_date.year, target_date.month, target_date.day, 12, 0, 0)
        jd = self.ephemeris.datetime_to_jd(dt_noon, timezone)
        
        # Moon phase and Tithi
        moon_phase = self.ephemeris.get_moon_phase(jd)
        
        # Moon position for Nakshatra
        moon = self.ephemeris.get_planet_position(1, jd)  # 1 = Moon
        
        # Calculate Yoga (Sun + Moon longitude / 13.33)
        sun = self.ephemeris.get_planet_position(0, jd)
        yoga_index = int((sun["longitude"] + moon["longitude"]) / (360/27)) % 27
        
        # Calculate Karana
        karana_index = int(moon_phase["moon_sun_angle"] / 6) % 11
        
        # Tamil date (approximate - simplified calculation)
        tamil_month = self._get_tamil_month(sun["longitude"])
        tamil_day = int(moon_phase["tithi_index"]) + 1
        
        # Time periods (Rahu Kalam, etc.)
        weekday = target_date.weekday()
        time_periods = self._calculate_time_periods(
            sun_times["sunrise_jd"],
            sun_times["sunset_jd"],
            weekday
        )

        # Nalla Neram (Gowri Panchangam - simplified)
        nalla_neram = self._calculate_nalla_neram(
            sun_times["sunrise_jd"],
            sun_times["sunset_jd"],
            weekday
        )

        # Moonrise/Moonset
        moon_times = self.ephemeris.get_moonrise_moonset(jd_midnight, lat, lon)

        # Durmuhurtham (inauspicious periods based on weekday)
        durmuhurtham = self._calculate_durmuhurtham(
            sun_times["sunrise_jd"],
            sun_times["sunset_jd"],
            weekday
        )

        # Thyajyam (based on nakshatra)
        thyajyam = self._calculate_thyajyam(moon, sun_times["sunrise_jd"])

        # Abhijit Muhurta (midday auspicious time)
        abhijit = self._calculate_abhijit(
            sun_times["sunrise_jd"],
            sun_times["sunset_jd"]
        )

        # Amrit Kalam (based on weekday and nakshatra)
        amrit_kalam = self._calculate_amrit_kalam(
            sun_times["sunrise_jd"],
            weekday,
            moon["nakshatra_index"]
        )

        # Calculate overall day score
        overall_score = self._calculate_day_score(moon_phase, yoga_index, moon)

        return {
            "date": target_date.isoformat(),
            "tamil_date": f"{tamil_day}",
            "tamil_month": tamil_month,
            "tamil_year": "விகாரி",  # Current Tamil year - should be calculated
            "vaaram": self.TAMIL_DAYS[weekday],
            "tithi": {
                "name": moon_phase["tithi"],
                "tamil": self._get_tithi_tamil(moon_phase["tithi"]),
                "paksha": moon_phase["paksha"],
                "progress": moon_phase["tithi_progress"]
            },
            "nakshatra": {
                "name": moon["nakshatra"],
                "tamil": moon["nakshatra_tamil"],
                "pada": moon["nakshatra_pada"]
            },
            "yoga": {
                "name": self.YOGAS[yoga_index],
                "tamil": self._get_yoga_tamil(self.YOGAS[yoga_index]),
                "index": yoga_index
            },
            "karana": {
                "name": self.KARANAS[karana_index],
                "tamil": self._get_karana_tamil(self.KARANAS[karana_index]),
                "index": karana_index
            },
            "sun_times": {
                "sunrise": sun_times["sunrise"],
                "sunset": sun_times["sunset"]
            },
            "moon_times": {
                "moonrise": moon_times["moonrise"],
                "moonset": moon_times["moonset"]
            },
            "inauspicious": {
                "rahu_kalam": time_periods["rahu_kalam"],
                "yamagandam": time_periods["yamagandam"],
                "kuligai": time_periods["kuligai"],
                "durmuhurtham": durmuhurtham,
                "thyajyam": thyajyam
            },
            "auspicious": {
                "abhijit": abhijit,
                "amrit_kalam": amrit_kalam,
                "nalla_neram": nalla_neram
            },
            # Keep flat structure for backward compatibility
            "sunrise": sun_times["sunrise"],
            "sunset": sun_times["sunset"],
            "rahu_kalam": time_periods["rahu_kalam"],
            "yamagandam": time_periods["yamagandam"],
            "kuligai": time_periods["kuligai"],
            "nalla_neram": nalla_neram,
            "overall_score": overall_score
        }
    
    def get_hourly_energy(self, target_date: date, lat: float, lon: float) -> List[Dict]:
        """
        Get hourly energy levels for stock-chart style visualization
        Returns data for each hour from 6 AM to 9 PM
        """
        # Use midnight local time for sunrise/sunset calculation
        dt_midnight_utc = datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0)
        dt_midnight_utc = dt_midnight_utc - timedelta(hours=5, minutes=30)
        jd_midnight = self.ephemeris.datetime_to_jd(dt_midnight_utc, timezone="UTC")
        sun_times = self.ephemeris.get_sunrise_sunset(jd_midnight, lat, lon)
        weekday = target_date.weekday()
        
        time_periods = self._calculate_time_periods(
            sun_times["sunrise_jd"],
            sun_times["sunset_jd"],
            weekday
        )
        
        nalla_neram = self._calculate_nalla_neram(
            sun_times["sunrise_jd"],
            sun_times["sunset_jd"],
            weekday
        )
        
        hourly_data = []
        
        for hour in range(6, 22):  # 6 AM to 9 PM
            time_str = f"{hour:02d}:00"
            
            # Check if in Rahu Kalam
            is_rahu = self._time_in_period(time_str, time_periods["rahu_kalam"])
            is_yama = self._time_in_period(time_str, time_periods["yamagandam"])
            
            # Check if in Nalla Neram
            is_nalla = any(self._time_in_period(time_str, slot) for slot in nalla_neram)
            
            # Calculate energy score
            if is_rahu:
                energy = 20 + (hash(f"{target_date}{hour}") % 15)
                recommendation = "தவிர்க்கவும் - ராகு காலம்"
            elif is_yama:
                energy = 35 + (hash(f"{target_date}{hour}") % 15)
                recommendation = "எச்சரிக்கை - யமகண்டம்"
            elif is_nalla:
                energy = 85 + (hash(f"{target_date}{hour}") % 15)
                recommendation = "சிறந்த நேரம்"
            else:
                energy = 50 + (hash(f"{target_date}{hour}") % 30)
                recommendation = "சாதாரண நேரம்"
            
            hourly_data.append({
                "time": time_str,
                "energy_score": min(100, energy),
                "is_rahu_kalam": is_rahu,
                "is_nalla_neram": is_nalla,
                "recommendation": recommendation
            })
        
        return hourly_data
    
    def get_week_forecast(self, lat: float, lon: float) -> List[Dict]:
        """Get 7-day forecast with daily scores"""
        forecasts = []
        today = date.today()
        
        for i in range(7):
            target = today + timedelta(days=i)
            panchangam = self.calculate(target, lat, lon)
            
            forecasts.append({
                "date": target.isoformat(),
                "day": self.TAMIL_DAYS[target.weekday()][:3],
                "score": panchangam["overall_score"],
                "tithi": panchangam["tithi"]["name"],
                "nakshatra": panchangam["nakshatra"]["tamil"]
            })
        
        return forecasts
    
    def _calculate_time_periods(self, sunrise_jd: float, sunset_jd: float, weekday: int) -> Dict:
        """Calculate Rahu Kalam, Yamagandam, Kuligai"""
        day_duration = sunset_jd - sunrise_jd
        period_duration = day_duration / 8
        
        def get_period_times(period_num: int) -> Dict:
            start_jd = sunrise_jd + (period_num - 1) * period_duration
            end_jd = start_jd + period_duration
            return {
                "start": self.ephemeris._jd_to_time_string(start_jd),
                "end": self.ephemeris._jd_to_time_string(end_jd)
            }
        
        return {
            "rahu_kalam": get_period_times(self.RAHU_KALAM_PERIODS[weekday]),
            "yamagandam": get_period_times(self.YAMAGANDAM_PERIODS[weekday]),
            "kuligai": get_period_times(self.KULIGAI_PERIODS[weekday])
        }
    
    def _calculate_nalla_neram(self, sunrise_jd: float, sunset_jd: float, weekday: int) -> List[Dict]:
        """
        Calculate Nalla Neram (Gowri Panchangam)
        Simplified version - returns 2-3 good periods
        """
        day_duration = sunset_jd - sunrise_jd
        period_duration = day_duration / 8
        
        # Gowri good periods vary by weekday (simplified)
        GOOD_PERIODS = {
            0: [1, 2, 5],  # Sunday
            1: [2, 3, 6],  # Monday
            2: [3, 4, 7],  # Tuesday
            3: [4, 5, 8],  # Wednesday
            4: [1, 5, 6],  # Thursday
            5: [2, 6, 7],  # Friday
            6: [3, 7, 8],  # Saturday
        }
        
        nalla_neram = []
        for period_num in GOOD_PERIODS.get(weekday, [1, 5]):
            start_jd = sunrise_jd + (period_num - 1) * period_duration
            end_jd = start_jd + period_duration
            nalla_neram.append({
                "start": self.ephemeris._jd_to_time_string(start_jd),
                "end": self.ephemeris._jd_to_time_string(end_jd)
            })
        
        return nalla_neram
    
    def _calculate_day_score(self, moon_phase: Dict, yoga_index: int, moon: Dict) -> float:
        """Calculate overall day score (0-100) for visual display"""
        score = 50  # Base
        
        # Good tithis
        good_tithis = ["Dwitiya", "Tritiya", "Panchami", "Saptami", "Dashami", "Ekadashi", "Trayodashi"]
        if moon_phase["tithi"] in good_tithis:
            score += 15
        
        # Bad tithis
        bad_tithis = ["Chaturthi", "Ashtami", "Navami", "Chaturdashi"]
        if moon_phase["tithi"] in bad_tithis:
            score -= 15
        
        # Good yogas
        if yoga_index in [1, 2, 3, 4, 6, 7, 10, 11, 13, 15, 19, 20, 21, 22]:
            score += 10
        
        # Bad yogas
        if yoga_index in [5, 8, 9, 12, 16, 18, 26]:
            score -= 10
        
        # Good nakshatras (Rohini, Mrigashira, Pushya, etc.)
        good_nakshatras = [3, 4, 7, 10, 11, 12, 21, 26]
        if moon["nakshatra_index"] in good_nakshatras:
            score += 10
        
        return max(0, min(100, score))
    
    def _get_tamil_month(self, sun_longitude: float) -> str:
        """Get Tamil month from Sun's longitude"""
        # Tamil months start when Sun enters each sign
        month_index = int(sun_longitude / 30)
        return self.TAMIL_MONTHS[month_index]
    
    def _time_in_period(self, time_str: str, period: Dict) -> bool:
        """Check if a time is within a period"""
        def to_minutes(t: str) -> int:
            h, m = map(int, t.split(":"))
            return h * 60 + m
        
        time_mins = to_minutes(time_str)
        start_mins = to_minutes(period["start"])
        end_mins = to_minutes(period["end"])
        
        return start_mins <= time_mins < end_mins

    def get_score_breakdown(self, target_date: date, lat: float, lon: float, current_time: datetime = None) -> Dict:
        """
        Calculate detailed score breakdown with all contributing factors.
        Returns structured data for frontend display.
        """
        if current_time is None:
            current_time = datetime.now()

        # Use midnight local time for sunrise/sunset calculation
        dt_midnight_utc = datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0)
        dt_midnight_utc = dt_midnight_utc - timedelta(hours=5, minutes=30)
        jd_midnight = self.ephemeris.datetime_to_jd(dt_midnight_utc, timezone="UTC")
        sun_times = self.ephemeris.get_sunrise_sunset(jd_midnight, lat, lon)

        # For planetary calculations, use noon local time
        dt = datetime(target_date.year, target_date.month, target_date.day, 12, 0, 0)
        jd = self.ephemeris.datetime_to_jd(dt)
        moon_phase = self.ephemeris.get_moon_phase(jd)
        moon = self.ephemeris.get_planet_position(1, jd)
        sun = self.ephemeris.get_planet_position(0, jd)
        yoga_index = int((sun["longitude"] + moon["longitude"]) / (360/27)) % 27
        karana_index = int(moon_phase["moon_sun_angle"] / 6) % 11
        weekday = target_date.weekday()

        time_periods = self._calculate_time_periods(
            sun_times["sunrise_jd"],
            sun_times["sunset_jd"],
            weekday
        )

        nalla_neram = self._calculate_nalla_neram(
            sun_times["sunrise_jd"],
            sun_times["sunset_jd"],
            weekday
        )

        factors = []
        base_score = 50

        # 1. TITHI SCORE (-15 to +15)
        tithi_name = moon_phase["tithi"]
        excellent_tithis = ["Dwitiya", "Tritiya", "Panchami", "Saptami", "Dashami", "Ekadashi", "Trayodashi", "Purnima"]
        bad_tithis = ["Chaturthi", "Ashtami", "Navami", "Chaturdashi", "Amavasya"]

        tithi_tamil_names = {
            "Pratipada": "பிரதமை", "Dwitiya": "துவிதியை", "Tritiya": "திருதியை",
            "Chaturthi": "சதுர்த்தி", "Panchami": "பஞ்சமி", "Shashthi": "சஷ்டி",
            "Saptami": "சப்தமி", "Ashtami": "அஷ்டமி", "Navami": "நவமி",
            "Dashami": "தசமி", "Ekadashi": "ஏகாதசி", "Dwadashi": "துவாதசி",
            "Trayodashi": "திரயோதசி", "Chaturdashi": "சதுர்தசி", "Purnima": "பூர்ணிமா",
            "Amavasya": "அமாவாசை"
        }

        if tithi_name in excellent_tithis:
            tithi_points = 15
            tithi_reason = f"{tithi_tamil_names.get(tithi_name, tithi_name)} சுப திதி - நல்ல காரியங்களுக்கு ஏற்றது"
        elif tithi_name in bad_tithis:
            tithi_points = -15
            tithi_reason = f"{tithi_tamil_names.get(tithi_name, tithi_name)} - புதிய காரியங்கள் தவிர்க்கவும்"
        else:
            tithi_points = 0
            tithi_reason = f"{tithi_tamil_names.get(tithi_name, tithi_name)} - சாதாரண திதி"

        factors.append({
            "id": "tithi",
            "name_tamil": "திதி",
            "value": tithi_tamil_names.get(tithi_name, tithi_name),
            "points": tithi_points,
            "reason_tamil": tithi_reason,
            "is_positive": tithi_points > 0
        })

        # 2. NAKSHATRA SCORE (-15 to +15)
        nakshatra_name = moon["nakshatra"]
        nakshatra_tamil = moon["nakshatra_tamil"]

        excellent_nakshatras = ["Rohini", "Mrigashira", "Pushya", "Hasta", "Chitra", "Swati",
                               "Anuradha", "Mula", "Shravana", "Dhanishta", "Revati"]
        bad_nakshatras = ["Bharani", "Krittika", "Ardra", "Ashlesha", "Magha", "Purva Phalguni",
                         "Vishakha", "Jyeshtha", "Purva Ashadha", "Purva Bhadrapada"]

        if nakshatra_name in excellent_nakshatras:
            nakshatra_points = 15
            nakshatra_reason = f"{nakshatra_tamil} - சுப நட்சத்திரம், நல்ல பலன்கள்"
        elif nakshatra_name in bad_nakshatras:
            nakshatra_points = -15
            nakshatra_reason = f"{nakshatra_tamil} - கவனமாக இருக்கவும்"
        else:
            nakshatra_points = 0
            nakshatra_reason = f"{nakshatra_tamil} - சாதாரண நட்சத்திரம்"

        factors.append({
            "id": "nakshatra",
            "name_tamil": "நட்சத்திரம்",
            "value": nakshatra_tamil,
            "points": nakshatra_points,
            "reason_tamil": nakshatra_reason,
            "is_positive": nakshatra_points > 0
        })

        # 3. YOGA SCORE (-10 to +10)
        yoga_name = self.YOGAS[yoga_index]
        good_yogas = ["Siddhi", "Shubha", "Amrita", "Priti", "Ayushman", "Saubhagya", "Shobhana"]
        bad_yogas = ["Vyatipata", "Vaidhriti", "Parigha", "Vajra", "Vyaghata", "Ganda", "Atiganda"]

        yoga_tamil_names = {
            "Vishkumbha": "விஷ்கும்பம்", "Priti": "பிரீதி", "Ayushman": "ஆயுஷ்மான்",
            "Saubhagya": "சௌபாக்யம்", "Shobhana": "சோபனம்", "Atiganda": "அதிகண்டம்",
            "Sukarma": "சுகர்மா", "Dhriti": "திருதி", "Shula": "சூலம்", "Ganda": "கண்டம்",
            "Vriddhi": "விருத்தி", "Dhruva": "த்ருவம்", "Vyaghata": "வியாகாதம்",
            "Harshana": "ஹர்ஷணம்", "Vajra": "வஜ்ரம்", "Siddhi": "சித்தி",
            "Vyatipata": "வியதிபாதம்", "Variyan": "வரீயான்", "Parigha": "பரிகம்",
            "Shiva": "சிவம்", "Siddha": "சித்தம்", "Sadhya": "சாத்யம்", "Shubha": "சுபம்",
            "Shukla": "சுக்லம்", "Brahma": "பிரம்மம்", "Indra": "இந்திரம்", "Vaidhriti": "வைத்ருதி"
        }

        if yoga_name in good_yogas:
            yoga_points = 10
            yoga_reason = f"{yoga_tamil_names.get(yoga_name, yoga_name)} - நல்ல யோகம்"
        elif yoga_name in bad_yogas:
            yoga_points = -10
            yoga_reason = f"{yoga_tamil_names.get(yoga_name, yoga_name)} - தீய யோகம், கவனம் தேவை"
        else:
            yoga_points = 0
            yoga_reason = f"{yoga_tamil_names.get(yoga_name, yoga_name)} - சாதாரண யோகம்"

        factors.append({
            "id": "yoga",
            "name_tamil": "யோகம்",
            "value": yoga_tamil_names.get(yoga_name, yoga_name),
            "points": yoga_points,
            "reason_tamil": yoga_reason,
            "is_positive": yoga_points > 0
        })

        # 4. KARANA SCORE (-5 to +5)
        karana_name = self.KARANAS[karana_index]
        good_karanas = ["Bava", "Balava", "Kaulava", "Taitila"]
        bad_karanas = ["Vishti"]  # Bhadra

        karana_tamil_names = {
            "Bava": "பவம்", "Balava": "பாலவம்", "Kaulava": "கௌலவம்", "Taitila": "தைதுலம்",
            "Gara": "கரம்", "Vanija": "வணிஜம்", "Vishti": "விஷ்டி", "Shakuni": "சகுனி",
            "Chatushpada": "சதுஷ்பாதம்", "Naga": "நாகம்", "Kimstughna": "கிம்ஸ்துக்னம்"
        }

        if karana_name in good_karanas:
            karana_points = 5
            karana_reason = f"{karana_tamil_names.get(karana_name, karana_name)} - சுப கரணம்"
        elif karana_name in bad_karanas:
            karana_points = -5
            karana_reason = f"{karana_tamil_names.get(karana_name, karana_name)} (பத்ரை) - புதிய காரியங்கள் தவிர்க்கவும்"
        else:
            karana_points = 0
            karana_reason = f"{karana_tamil_names.get(karana_name, karana_name)} - சாதாரண கரணம்"

        factors.append({
            "id": "karana",
            "name_tamil": "கரணம்",
            "value": karana_tamil_names.get(karana_name, karana_name),
            "points": karana_points,
            "reason_tamil": karana_reason,
            "is_positive": karana_points > 0
        })

        # 5. CURRENT TIME FACTOR (-20 to +20)
        current_time_str = current_time.strftime("%H:%M")
        time_points = 0
        time_value = "சாதாரண நேரம்"
        time_reason = "சாதாரண நேரம்"

        if self._time_in_period(current_time_str, time_periods["rahu_kalam"]):
            time_points = -20
            time_value = "ராகு காலம்"
            time_reason = "ராகு காலத்தில் புதிய காரியங்கள் தவிர்க்கவும்"
        elif self._time_in_period(current_time_str, time_periods["yamagandam"]):
            time_points = -15
            time_value = "யமகண்டம்"
            time_reason = "யமகண்டத்தில் முக்கிய முடிவுகள் தவிர்க்கவும்"
        elif self._time_in_period(current_time_str, time_periods["kuligai"]):
            time_points = -10
            time_value = "குளிகை காலம்"
            time_reason = "குளிகை நேரத்தில் கவனமாக இருக்கவும்"
        else:
            # Check if in Nalla Neram
            for slot in nalla_neram:
                if self._time_in_period(current_time_str, slot):
                    time_points = 20
                    time_value = "நல்ல நேரம்"
                    time_reason = "சுப நேரம் - எல்லா காரியங்களுக்கும் ஏற்றது"
                    break

            # Check for Abhijit Muhurta (around noon, 11:36 AM - 12:24 PM approx)
            hour = current_time.hour
            minute = current_time.minute
            total_mins = hour * 60 + minute
            if 696 <= total_mins <= 744:  # 11:36 AM to 12:24 PM
                time_points = 15
                time_value = "அபிஜித் முகூர்த்தம்"
                time_reason = "அபிஜித் முகூர்த்தம் - மிகவும் சுபமான நேரம்"

        factors.append({
            "id": "current_time",
            "name_tamil": "தற்போதைய நேரம்",
            "value": time_value,
            "points": time_points,
            "reason_tamil": time_reason,
            "is_positive": time_points > 0
        })

        # 6. VAARAM (Day) SCORE (-5 to +10)
        day_points = 0
        day_name = self.TAMIL_DAYS[weekday]

        if weekday == 3:  # Thursday (Guru)
            day_points = 10
            day_reason = f"{day_name} - குரு பகவான் நாள், சுபமான நாள்"
        elif weekday == 4:  # Friday (Sukra)
            day_points = 10
            day_reason = f"{day_name} - சுக்ர பகவான் நாள், நல்ல நாள்"
        elif weekday == 0:  # Monday (Chandra)
            day_points = 5
            day_reason = f"{day_name} - சந்திர நாள், மன அமைதி"
        elif weekday == 2:  # Wednesday (Budha)
            day_points = 5
            day_reason = f"{day_name} - புத நாள், கல்வி/வியாபாரத்திற்கு நல்லது"
        elif weekday == 6:  # Sunday (Surya)
            day_points = 0
            day_reason = f"{day_name} - சூரிய நாள்"
        elif weekday == 5:  # Saturday (Sani)
            day_points = 0
            day_reason = f"{day_name} - சனி நாள்"
        elif weekday == 1:  # Tuesday (Sevvai)
            day_points = -5
            day_reason = f"{day_name} - செவ்வாய் நாள், புதிய காரியங்களில் கவனம்"

        factors.append({
            "id": "vaaram",
            "name_tamil": "கிழமை",
            "value": day_name,
            "points": day_points,
            "reason_tamil": day_reason,
            "is_positive": day_points > 0
        })

        # Calculate total score
        total_points = sum(f["points"] for f in factors)
        total_score = max(0, min(100, base_score + total_points))

        # Determine score label
        if total_score >= 70:
            score_label = "நல்லது"
        elif total_score >= 40:
            score_label = "சாதாரணம்"
        else:
            score_label = "கவனம்"

        return {
            "total_score": total_score,
            "score_label": score_label,
            "base_score": base_score,
            "factors": factors,
            "calculated_at": current_time.isoformat()
        }

    def _calculate_durmuhurtham(self, sunrise_jd: float, sunset_jd: float, weekday: int) -> List[Dict]:
        """
        Calculate Durmuhurtham (inauspicious muhurtas) for the day.
        Each muhurta is 1/15th of daytime (approximately 48 minutes).
        Durmuhurtham varies by weekday.
        """
        day_duration = sunset_jd - sunrise_jd
        muhurta_duration = day_duration / 15  # 15 muhurtas in daytime

        # Durmuhurtham periods by weekday (1-indexed muhurta numbers)
        # Index = Python weekday (0=Monday, 1=Tuesday, ..., 6=Sunday)
        # These are traditional durmuhurtham periods
        DURMUHURTHAM_MUHURTAS = {
            0: [2, 7],      # Monday: 2nd and 7th muhurta
            1: [4, 11],     # Tuesday: 4th and 11th muhurta
            2: [6, 3],      # Wednesday: 6th and 3rd muhurta
            3: [5, 10],     # Thursday: 5th and 10th muhurta
            4: [4, 9],      # Friday: 4th and 9th muhurta
            5: [1, 8],      # Saturday: 1st and 8th muhurta
            6: [10, 15],    # Sunday: 10th and 15th muhurta
        }

        muhurtas = DURMUHURTHAM_MUHURTAS.get(weekday, [2, 7])
        durmuhurtham_periods = []

        for muhurta_num in muhurtas:
            start_jd = sunrise_jd + (muhurta_num - 1) * muhurta_duration
            end_jd = start_jd + muhurta_duration

            # Check if this period is during daytime
            if end_jd <= sunset_jd:
                durmuhurtham_periods.append({
                    "start": self.ephemeris._jd_to_time_string(start_jd),
                    "end": self.ephemeris._jd_to_time_string(end_jd)
                })

        # Also add night durmuhurtham (typically one period after sunset)
        # Night muhurtas: First muhurta after sunset is often considered
        night_muhurta_duration = (1 - day_duration) / 15  # 15 muhurtas at night
        night_muhurta_num = DURMUHURTHAM_MUHURTAS.get(weekday, [2, 7])[1] if len(DURMUHURTHAM_MUHURTAS.get(weekday, [])) > 1 else 7

        # Calculate night durmuhurtham (simplified - using fixed evening period)
        night_start_jd = sunset_jd + 4 * night_muhurta_duration  # Around 10-11 PM
        night_end_jd = night_start_jd + night_muhurta_duration

        durmuhurtham_periods.append({
            "start": self.ephemeris._jd_to_time_string(night_start_jd),
            "end": self.ephemeris._jd_to_time_string(night_end_jd)
        })

        return durmuhurtham_periods

    def _calculate_thyajyam(self, moon: Dict, sunrise_jd: float) -> List[Dict]:
        """
        Calculate Thyajyam (to be avoided) periods.
        Based on nakshatra - certain nakshatras have specific thyajyam periods.
        Thyajyam is 4 ghatikas (96 minutes) during specific parts of nakshatra.
        """
        nakshatra_index = moon["nakshatra_index"]

        # Thyajyam timings vary by nakshatra (in terms of ghatikas from nakshatra start)
        # This is a simplified calculation based on traditional rules
        # Each nakshatra has a specific thyajyam period (1 ghatika = 24 minutes)

        # Thyajyam start ghatikas for each nakshatra (0-26)
        # These are approximate traditional values
        THYAJYAM_START_GHATIKAS = [
            50, 4, 30, 56, 6, 32, 50, 4, 30,   # Ashwini to Ashlesha
            56, 6, 32, 50, 4, 30, 56, 6, 32,   # Magha to Jyeshtha
            50, 4, 30, 56, 6, 32, 50, 4, 30    # Mula to Revati
        ]

        # Duration is 4 ghatikas = 96 minutes
        thyajyam_duration_days = (4 * 24) / (24 * 60)  # 96 minutes in fraction of day

        # Calculate based on nakshatra
        start_ghatika = THYAJYAM_START_GHATIKAS[nakshatra_index % 27]

        # Convert ghatikas from sunrise to JD
        ghatika_in_days = (start_ghatika * 24) / (24 * 60)  # ghatika to fraction of day

        start_jd = sunrise_jd + ghatika_in_days
        end_jd = start_jd + thyajyam_duration_days

        return [{
            "start": self.ephemeris._jd_to_time_string(start_jd),
            "end": self.ephemeris._jd_to_time_string(end_jd)
        }]

    def _calculate_abhijit(self, sunrise_jd: float, sunset_jd: float) -> Dict:
        """
        Calculate Abhijit Muhurta (most auspicious muhurta of the day).
        It is the 8th muhurta of the day (middle of 15 muhurtas).
        Spans approximately 24 minutes before and after local noon.
        """
        day_duration = sunset_jd - sunrise_jd
        muhurta_duration = day_duration / 15

        # Abhijit is the 8th muhurta (middle of day)
        abhijit_start_jd = sunrise_jd + 7 * muhurta_duration
        abhijit_end_jd = abhijit_start_jd + muhurta_duration

        return {
            "start": self.ephemeris._jd_to_time_string(abhijit_start_jd),
            "end": self.ephemeris._jd_to_time_string(abhijit_end_jd)
        }

    def _calculate_amrit_kalam(self, sunrise_jd: float, weekday: int, nakshatra_index: int) -> Dict:
        """
        Calculate Amrit Kalam (nectar time - highly auspicious).
        Based on combination of weekday and nakshatra.
        Duration is typically 90-96 minutes.
        """
        # Amrit Kalam varies by weekday
        # Each day has specific time slots considered as Amrit Kalam
        # These are in ghatikas from sunrise (1 ghatika = 24 minutes)

        AMRIT_KALAM_START = {
            0: 6,   # Monday: 6th ghatika from sunrise (around 2.5 hours after sunrise)
            1: 18,  # Tuesday: 18th ghatika
            2: 12,  # Wednesday: 12th ghatika
            3: 30,  # Thursday: 30th ghatika
            4: 24,  # Friday: 24th ghatika
            5: 42,  # Saturday: 42nd ghatika (night time)
            6: 36,  # Sunday: 36th ghatika
        }

        start_ghatika = AMRIT_KALAM_START.get(weekday, 6)

        # Convert to JD (1 ghatika = 24 minutes = 24/(24*60) days)
        ghatika_in_days = 24 / (24 * 60)  # One ghatika in fraction of day

        start_jd = sunrise_jd + start_ghatika * ghatika_in_days
        # Amrit Kalam duration is typically 4 ghatikas (96 minutes)
        end_jd = start_jd + 4 * ghatika_in_days

        return {
            "start": self.ephemeris._jd_to_time_string(start_jd),
            "end": self.ephemeris._jd_to_time_string(end_jd)
        }

    def _get_tithi_tamil(self, tithi_name: str) -> str:
        """Get Tamil name for tithi"""
        TITHI_TAMIL = {
            "Pratipada": "பிரதமை", "Dwitiya": "துவிதியை", "Tritiya": "திருதியை",
            "Chaturthi": "சதுர்த்தி", "Panchami": "பஞ்சமி", "Shashthi": "சஷ்டி",
            "Saptami": "சப்தமி", "Ashtami": "அஷ்டமி", "Navami": "நவமி",
            "Dashami": "தசமி", "Ekadashi": "ஏகாதசி", "Dwadashi": "துவாதசி",
            "Trayodashi": "திரயோதசி", "Chaturdashi": "சதுர்தசி",
            "Purnima": "பூர்ணிமா", "Amavasya": "அமாவாசை"
        }
        return TITHI_TAMIL.get(tithi_name, tithi_name)

    def _get_yoga_tamil(self, yoga_name: str) -> str:
        """Get Tamil name for yoga"""
        YOGA_TAMIL = {
            "Vishkumbha": "விஷ்கும்பம்", "Priti": "பிரீதி", "Ayushman": "ஆயுஷ்மான்",
            "Saubhagya": "சௌபாக்யம்", "Shobhana": "சோபனம்", "Atiganda": "அதிகண்டம்",
            "Sukarma": "சுகர்மா", "Dhriti": "திருதி", "Shula": "சூலம்",
            "Ganda": "கண்டம்", "Vriddhi": "விருத்தி", "Dhruva": "த்ருவம்",
            "Vyaghata": "வியாகாதம்", "Harshana": "ஹர்ஷணம்", "Vajra": "வஜ்ரம்",
            "Siddhi": "சித்தி", "Vyatipata": "வியதிபாதம்", "Variyan": "வரீயான்",
            "Parigha": "பரிகம்", "Shiva": "சிவம்", "Siddha": "சித்தம்",
            "Sadhya": "சாத்யம்", "Shubha": "சுபம்", "Shukla": "சுக்லம்",
            "Brahma": "பிரம்மம்", "Indra": "இந்திரம்", "Vaidhriti": "வைத்ருதி"
        }
        return YOGA_TAMIL.get(yoga_name, yoga_name)

    def _get_karana_tamil(self, karana_name: str) -> str:
        """Get Tamil name for karana"""
        KARANA_TAMIL = {
            "Bava": "பவம்", "Balava": "பாலவம்", "Kaulava": "கௌலவம்",
            "Taitila": "தைதுலம்", "Gara": "கரம்", "Vanija": "வணிஜம்",
            "Vishti": "விஷ்டி", "Shakuni": "சகுனி", "Chatushpada": "சதுஷ்பாதம்",
            "Naga": "நாகம்", "Kimstughna": "கிம்ஸ்துக்னம்"
        }
        return KARANA_TAMIL.get(karana_name, karana_name)
