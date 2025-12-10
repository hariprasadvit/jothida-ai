"""
Forecast Service
Provides daily, weekly, monthly, and yearly predictions based on user's birth chart
"""

from typing import Dict, List, Optional
from datetime import date, datetime, timedelta
from calendar import monthrange
import math


class ForecastService:
    """
    Generates personalized forecasts based on:
    - Birth chart (Rasi, Nakshatra, Lagna)
    - Current planetary transits
    - Dasha periods
    - Panchangam data
    """

    # Nakshatra lords for Vimshottari Dasha
    NAKSHATRA_LORDS = [
        'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury',
        'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury',
        'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury'
    ]

    # Rasi compatibility for transit effects
    RASI_NUMBERS = {
        'Mesha': 1, 'மேஷம்': 1, 'Aries': 1,
        'Vrishabha': 2, 'ரிஷபம்': 2, 'Taurus': 2,
        'Mithuna': 3, 'மிதுனம்': 3, 'Gemini': 3,
        'Kataka': 4, 'கடகம்': 4, 'Cancer': 4,
        'Simha': 5, 'சிம்மம்': 5, 'Leo': 5,
        'Kanya': 6, 'கன்னி': 6, 'Virgo': 6,
        'Tula': 7, 'துலாம்': 7, 'Libra': 7,
        'Vrischika': 8, 'விருச்சிகம்': 8, 'Scorpio': 8,
        'Dhanus': 9, 'தனுசு': 9, 'Sagittarius': 9,
        'Makara': 10, 'மகரம்': 10, 'Capricorn': 10,
        'Kumbha': 11, 'கும்பம்': 11, 'Aquarius': 11,
        'Meena': 12, 'மீனம்': 12, 'Pisces': 12
    }

    RASI_TAMIL = ['', 'மேஷம்', 'ரிஷபம்', 'மிதுனம்', 'கடகம்', 'சிம்மம்', 'கன்னி',
                  'துலாம்', 'விருச்சிகம்', 'தனுசு', 'மகரம்', 'கும்பம்', 'மீனம்']

    MONTH_TAMIL = ['', 'ஜனவரி', 'பிப்ரவரி', 'மார்ச்', 'ஏப்ரல்', 'மே', 'ஜூன்',
                   'ஜூலை', 'ஆகஸ்ட்', 'செப்டம்பர்', 'அக்டோபர்', 'நவம்பர்', 'டிசம்பர்']

    def __init__(self, ephemeris=None, panchangam_calculator=None):
        self.ephemeris = ephemeris
        self.panchangam = panchangam_calculator

    def get_user_forecast(
        self,
        user_rasi: str,
        user_nakshatra: str,
        birth_date: Optional[date] = None,
        lat: float = 13.0827,
        lon: float = 80.2707
    ) -> Dict:
        """
        Get comprehensive forecast for user including:
        - Today's forecast
        - This week's forecast
        - This month's forecast
        - Next 3 years month-wise
        """
        today = date.today()
        rasi_num = self.RASI_NUMBERS.get(user_rasi, 1)

        # Calculate base scores from transit positions
        base_score = self._calculate_base_score(rasi_num, today)

        return {
            "today": self._get_daily_forecast(rasi_num, user_nakshatra, today, lat, lon),
            "week": self._get_weekly_forecast(rasi_num, user_nakshatra, today),
            "month": self._get_monthly_forecast(rasi_num, user_nakshatra, today),
            "year": self._get_yearly_forecast(rasi_num, user_nakshatra, today),
            "three_years": self._get_three_year_forecast(rasi_num, user_nakshatra, today),
            "generated_at": datetime.now().isoformat()
        }

    def _calculate_base_score(self, rasi_num: int, target_date: date) -> float:
        """Calculate base score from planetary transits"""
        # Simplified transit calculation
        # In production, use actual ephemeris data
        day_of_year = target_date.timetuple().tm_yday

        # Create variation based on rasi and date
        base = 65 + (rasi_num * 2.5) % 15
        variation = 10 * math.sin(day_of_year * 0.017 + rasi_num)

        return max(40, min(90, base + variation))

    def _get_daily_forecast(
        self,
        rasi_num: int,
        nakshatra: str,
        target_date: date,
        lat: float,
        lon: float
    ) -> Dict:
        """Get detailed daily forecast"""
        # Get panchangam data if available
        panchang = {}
        if self.panchangam:
            try:
                panchang = self.panchangam.calculate(target_date, lat, lon, "Asia/Kolkata")
            except Exception:
                pass

        # Calculate overall score
        overall_score = panchang.get("overall_score", self._calculate_base_score(rasi_num, target_date))

        # Calculate area-wise scores
        areas = self._calculate_life_areas(rasi_num, target_date, overall_score)

        return {
            "date": target_date.isoformat(),
            "overall_score": round(overall_score),
            "score_label": self._get_score_label(overall_score),
            "rasi": self.RASI_TAMIL[rasi_num] if rasi_num <= 12 else "",
            "areas": areas,
            "panchangam": {
                "tithi": panchang.get("tithi", {}).get("tamil", "-"),
                "nakshatra": panchang.get("nakshatra", {}).get("tamil", nakshatra),
                "yoga": panchang.get("yoga", {}).get("tamil", "-"),
                "vaaram": panchang.get("vaaram", "-")
            },
            "lucky_time": self._get_lucky_times(panchang),
            "avoid_time": self._get_avoid_times(panchang),
            "advice": self._generate_daily_advice(overall_score, areas)
        }

    def _get_weekly_forecast(self, rasi_num: int, nakshatra: str, start_date: date) -> Dict:
        """Get 7-day forecast"""
        days = []
        total_score = 0

        for i in range(7):
            day_date = start_date + timedelta(days=i)
            score = self._calculate_base_score(rasi_num, day_date)
            total_score += score

            # Weekday-based adjustments
            weekday = day_date.weekday()
            if weekday == 3:  # Thursday - Jupiter day
                score = min(95, score + 5)
            elif weekday == 4:  # Friday - Venus day
                score = min(95, score + 3)
            elif weekday == 1:  # Tuesday - Mars day
                score = max(40, score - 3)

            days.append({
                "date": day_date.isoformat(),
                "day": self._get_tamil_weekday(weekday),
                "score": round(score),
                "is_good": score >= 65,
                "highlight": self._get_day_highlight(score, weekday)
            })

        avg_score = total_score / 7
        best_day = max(days, key=lambda x: x["score"])
        worst_day = min(days, key=lambda x: x["score"])

        return {
            "start_date": start_date.isoformat(),
            "end_date": (start_date + timedelta(days=6)).isoformat(),
            "average_score": round(avg_score),
            "score_label": self._get_score_label(avg_score),
            "days": days,
            "best_day": {
                "date": best_day["date"],
                "day": best_day["day"],
                "score": best_day["score"]
            },
            "worst_day": {
                "date": worst_day["date"],
                "day": worst_day["day"],
                "score": worst_day["score"]
            },
            "advice": self._generate_weekly_advice(avg_score, best_day, worst_day)
        }

    def _get_monthly_forecast(self, rasi_num: int, nakshatra: str, ref_date: date) -> Dict:
        """Get current month forecast with daily scores"""
        year = ref_date.year
        month = ref_date.month
        num_days = monthrange(year, month)[1]

        days = []
        total_score = 0
        good_days = 0
        bad_days = 0

        for day in range(1, num_days + 1):
            day_date = date(year, month, day)
            score = self._calculate_base_score(rasi_num, day_date)
            total_score += score

            if score >= 70:
                good_days += 1
            elif score < 50:
                bad_days += 1

            days.append({
                "date": day_date.isoformat(),
                "day": day,
                "score": round(score),
                "type": "good" if score >= 70 else "caution" if score < 50 else "normal"
            })

        avg_score = total_score / num_days

        return {
            "month": month,
            "year": year,
            "month_name": self.MONTH_TAMIL[month],
            "average_score": round(avg_score),
            "score_label": self._get_score_label(avg_score),
            "good_days_count": good_days,
            "caution_days_count": bad_days,
            "days": days,
            "best_periods": self._find_best_periods(days),
            "advice": self._generate_monthly_advice(avg_score, good_days, bad_days)
        }

    def _get_yearly_forecast(self, rasi_num: int, nakshatra: str, ref_date: date) -> Dict:
        """Get current year forecast by month"""
        year = ref_date.year
        months = []
        total_score = 0

        for month in range(1, 13):
            # Calculate monthly average
            num_days = monthrange(year, month)[1]
            month_total = 0

            for day in range(1, num_days + 1):
                day_date = date(year, month, day)
                month_total += self._calculate_base_score(rasi_num, day_date)

            avg_score = month_total / num_days
            total_score += avg_score

            months.append({
                "month": month,
                "name": self.MONTH_TAMIL[month],
                "score": round(avg_score),
                "type": "excellent" if avg_score >= 75 else "good" if avg_score >= 60 else "caution"
            })

        yearly_avg = total_score / 12
        best_months = sorted(months, key=lambda x: x["score"], reverse=True)[:3]
        challenging_months = sorted(months, key=lambda x: x["score"])[:3]

        return {
            "year": year,
            "average_score": round(yearly_avg),
            "score_label": self._get_score_label(yearly_avg),
            "months": months,
            "best_months": [{"month": m["name"], "score": m["score"]} for m in best_months],
            "challenging_months": [{"month": m["name"], "score": m["score"]} for m in challenging_months],
            "advice": self._generate_yearly_advice(yearly_avg, best_months, challenging_months)
        }

    def _get_three_year_forecast(self, rasi_num: int, nakshatra: str, ref_date: date) -> List[Dict]:
        """Get 3-year month-wise forecast"""
        forecasts = []
        current_year = ref_date.year

        for year_offset in range(3):
            year = current_year + year_offset
            year_data = {
                "year": year,
                "months": []
            }

            for month in range(1, 13):
                # Skip past months in current year
                if year == current_year and month < ref_date.month:
                    continue

                num_days = monthrange(year, month)[1]
                month_total = 0

                for day in range(1, num_days + 1):
                    day_date = date(year, month, day)
                    month_total += self._calculate_base_score(rasi_num, day_date)

                avg_score = month_total / num_days

                year_data["months"].append({
                    "month": month,
                    "name": self.MONTH_TAMIL[month],
                    "year": year,
                    "score": round(avg_score),
                    "type": "excellent" if avg_score >= 75 else "good" if avg_score >= 60 else "normal" if avg_score >= 50 else "caution"
                })

            forecasts.append(year_data)

        return forecasts

    def _calculate_life_areas(self, rasi_num: int, target_date: date, base_score: float) -> Dict:
        """Calculate scores for different life areas"""
        day_offset = target_date.timetuple().tm_yday

        return {
            "career": {
                "score": round(min(100, max(40, base_score + 8 + (day_offset % 5)))),
                "tamil": "தொழில்"
            },
            "love": {
                "score": round(min(100, max(40, base_score - 5 + (day_offset % 7)))),
                "tamil": "காதல்"
            },
            "health": {
                "score": round(min(100, max(40, base_score + 3 + (day_offset % 4)))),
                "tamil": "ஆரோக்கியம்"
            },
            "finance": {
                "score": round(min(100, max(40, base_score - 2 + (day_offset % 6)))),
                "tamil": "நிதி"
            },
            "education": {
                "score": round(min(100, max(40, base_score + 5 + (day_offset % 5)))),
                "tamil": "கல்வி"
            }
        }

    def _get_lucky_times(self, panchang: Dict) -> List[str]:
        """Get lucky time periods"""
        times = []
        auspicious = panchang.get("auspicious", {})

        if auspicious.get("abhijit"):
            times.append(f"அபிஜித்: {auspicious['abhijit'].get('start', '')} - {auspicious['abhijit'].get('end', '')}")

        if auspicious.get("amrit_kalam"):
            times.append(f"அமிர்த காலம்: {auspicious['amrit_kalam'].get('start', '')} - {auspicious['amrit_kalam'].get('end', '')}")

        nalla_neram = panchang.get("nalla_neram", [])
        for i, slot in enumerate(nalla_neram[:2]):
            times.append(f"நல்ல நேரம் {i+1}: {slot.get('start', '')} - {slot.get('end', '')}")

        return times if times else ["காலை 9:00 - 10:30", "மாலை 4:30 - 6:00"]

    def _get_avoid_times(self, panchang: Dict) -> List[str]:
        """Get times to avoid"""
        times = []
        inauspicious = panchang.get("inauspicious", {})

        if inauspicious.get("rahu_kalam"):
            times.append(f"ராகு காலம்: {inauspicious['rahu_kalam'].get('start', '')} - {inauspicious['rahu_kalam'].get('end', '')}")

        if inauspicious.get("yamagandam"):
            times.append(f"யமகண்டம்: {inauspicious['yamagandam'].get('start', '')} - {inauspicious['yamagandam'].get('end', '')}")

        rahu = panchang.get("rahu_kalam", {})
        if rahu and not inauspicious.get("rahu_kalam"):
            times.append(f"ராகு காலம்: {rahu.get('start', '')} - {rahu.get('end', '')}")

        return times if times else ["ராகு காலம்: 15:00 - 16:30"]

    def _get_score_label(self, score: float) -> str:
        """Get Tamil label for score"""
        if score >= 80:
            return "மிகச்சிறந்த"
        elif score >= 70:
            return "சிறந்த"
        elif score >= 60:
            return "நல்ல"
        elif score >= 50:
            return "சாதாரண"
        else:
            return "கவனம்"

    def _get_tamil_weekday(self, weekday: int) -> str:
        """Get Tamil weekday name"""
        days = ['திங்கள்', 'செவ்வாய்', 'புதன்', 'வியாழன்', 'வெள்ளி', 'சனி', 'ஞாயிறு']
        return days[weekday]

    def _get_day_highlight(self, score: float, weekday: int) -> str:
        """Get highlight for the day"""
        if score >= 80:
            return "முக்கிய முடிவுகளுக்கு சிறந்த நாள்"
        elif score >= 70:
            return "புதிய தொடக்கங்களுக்கு நல்ல நாள்"
        elif score < 50:
            return "பொறுமையாக இருங்கள்"
        return ""

    def _find_best_periods(self, days: List[Dict]) -> List[Dict]:
        """Find consecutive good day periods"""
        periods = []
        start = None
        current_streak = 0

        for day in days:
            if day["score"] >= 70:
                if start is None:
                    start = day["day"]
                current_streak += 1
            else:
                if current_streak >= 3:
                    periods.append({
                        "start": start,
                        "end": day["day"] - 1,
                        "days": current_streak
                    })
                start = None
                current_streak = 0

        if current_streak >= 3:
            periods.append({
                "start": start,
                "end": days[-1]["day"],
                "days": current_streak
            })

        return periods[:3]

    def _generate_daily_advice(self, score: float, areas: Dict) -> str:
        """Generate daily advice in Tamil"""
        best_area = max(areas.items(), key=lambda x: x[1]["score"])
        worst_area = min(areas.items(), key=lambda x: x[1]["score"])

        if score >= 75:
            return f"இன்று மிகவும் நல்ல நாள். {best_area[1]['tamil']} துறையில் சிறப்பான முன்னேற்றம் காணலாம். முக்கிய முடிவுகளை எடுக்க ஏற்ற நாள்."
        elif score >= 60:
            return f"இன்று நல்ல நாள். {best_area[1]['tamil']} சம்பந்தமான செயல்களில் கவனம் செலுத்துங்கள். ராகு காலம் தவிர்க்கவும்."
        else:
            return f"இன்று சற்று கவனமாக இருங்கள். {worst_area[1]['tamil']} விஷயங்களில் முக்கிய முடிவுகளை தள்ளி வையுங்கள்."

    def _generate_weekly_advice(self, avg_score: float, best_day: Dict, worst_day: Dict) -> str:
        """Generate weekly advice in Tamil"""
        return f"இந்த வாரம் {best_day['day']} சிறந்த நாள் (மதிப்பெண்: {best_day['score']}%). முக்கிய வேலைகளை அன்று திட்டமிடுங்கள். {worst_day['day']} கவனமாக இருக்கவும்."

    def _generate_monthly_advice(self, avg_score: float, good_days: int, bad_days: int) -> str:
        """Generate monthly advice in Tamil"""
        return f"இந்த மாதம் {good_days} நல்ல நாட்கள் உள்ளன. சராசரி மதிப்பெண் {round(avg_score)}%. திருமணம், கிரஹப்பிரவேசம் போன்ற முக்கிய காரியங்களுக்கு நல்ல நாட்களை தேர்வு செய்யுங்கள்."

    def _generate_yearly_advice(self, avg_score: float, best_months: List, challenging_months: List) -> str:
        """Generate yearly advice in Tamil"""
        best_names = ", ".join([m["name"] for m in best_months[:2]])
        return f"இந்த ஆண்டு {best_names} மாதங்கள் மிகவும் சிறப்பாக இருக்கும். முக்கிய முடிவுகளை இந்த காலத்தில் எடுக்கலாம்."
