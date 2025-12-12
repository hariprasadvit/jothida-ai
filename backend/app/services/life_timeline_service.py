"""
Life Timeline Service
Generates comprehensive life event predictions based on:
- South Indian Astro-Percent Engine
- Dasha periods with dignity analysis
- Transit analysis (Gocharam)
- House lord positions
- Yogas and Doshas
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Optional
import math

# Import Astro-Percent Engine and V6.0 TimeAdaptiveEngine
try:
    from .astro_percent_engine import AstroPercentEngine
except ImportError:
    AstroPercentEngine = None

# V6.0: Prefer TimeAdaptiveEngine for more positive output
try:
    from .time_adaptive_engine import TimeAdaptiveEngine
    V60_ENGINE_AVAILABLE = True
except ImportError:
    TimeAdaptiveEngine = None
    V60_ENGINE_AVAILABLE = False

# Dasha periods and their general effects
DASHA_EFFECTS = {
    "Sun": {
        "career": 75,
        "relationships": 55,
        "finances": 70,
        "health": 65,
        "keywords": ["leadership", "recognition", "authority", "father"],
        "keywords_tamil": ["தலைமைத்துவம்", "அங்கீகாரம்", "அதிகாரம்", "தந்தை"],
    },
    "Moon": {
        "career": 60,
        "relationships": 80,
        "finances": 65,
        "health": 70,
        "keywords": ["emotions", "mother", "home", "travel"],
        "keywords_tamil": ["உணர்வுகள்", "தாய்", "வீடு", "பயணம்"],
    },
    "Mars": {
        "career": 70,
        "relationships": 50,
        "finances": 65,
        "health": 60,
        "keywords": ["courage", "property", "siblings", "energy"],
        "keywords_tamil": ["தைரியம்", "சொத்து", "உடன்பிறப்புகள்", "சக்தி"],
    },
    "Mercury": {
        "career": 80,
        "relationships": 65,
        "finances": 75,
        "health": 70,
        "keywords": ["communication", "business", "education", "intellect"],
        "keywords_tamil": ["தொடர்பு", "வணிகம்", "கல்வி", "அறிவு"],
    },
    "Jupiter": {
        "career": 85,
        "relationships": 75,
        "finances": 80,
        "health": 80,
        "keywords": ["wisdom", "expansion", "children", "spirituality"],
        "keywords_tamil": ["ஞானம்", "வளர்ச்சி", "குழந்தைகள்", "ஆன்மீகம்"],
    },
    "Venus": {
        "career": 70,
        "relationships": 90,
        "finances": 85,
        "health": 75,
        "keywords": ["love", "luxury", "art", "marriage"],
        "keywords_tamil": ["காதல்", "ஆடம்பரம்", "கலை", "திருமணம்"],
    },
    "Saturn": {
        "career": 65,
        "relationships": 45,
        "finances": 55,
        "health": 50,
        "keywords": ["discipline", "delays", "karma", "hard work"],
        "keywords_tamil": ["ஒழுக்கம்", "தாமதம்", "கர்மா", "கடின உழைப்பு"],
    },
    "Rahu": {
        "career": 70,
        "relationships": 55,
        "finances": 75,
        "health": 55,
        "keywords": ["foreign", "innovation", "desire", "sudden gains"],
        "keywords_tamil": ["வெளிநாடு", "புதுமை", "ஆசை", "திடீர் லாபம்"],
    },
    "Ketu": {
        "career": 55,
        "relationships": 45,
        "finances": 50,
        "health": 60,
        "keywords": ["spirituality", "detachment", "past karma", "liberation"],
        "keywords_tamil": ["ஆன்மீகம்", "பற்றின்மை", "முன்வினை", "விடுதலை"],
    },
}

# Event types with their indicators
EVENT_TYPES = {
    "career_rise": {
        "icon": "trending-up",
        "color": "#22c55e",
        "label": "Career Rise",
        "label_tamil": "தொழில் உயர்வு",
    },
    "career_challenge": {
        "icon": "trending-down",
        "color": "#ef4444",
        "label": "Career Challenge",
        "label_tamil": "தொழில் சவால்",
    },
    "relationship_bloom": {
        "icon": "heart",
        "color": "#ec4899",
        "label": "Relationship Bloom",
        "label_tamil": "உறவு மலர்ச்சி",
    },
    "relationship_test": {
        "icon": "heart-dislike",
        "color": "#f97316",
        "label": "Relationship Test",
        "label_tamil": "உறவு சோதனை",
    },
    "financial_gain": {
        "icon": "cash",
        "color": "#22c55e",
        "label": "Financial Gain",
        "label_tamil": "பண வளர்ச்சி",
    },
    "financial_caution": {
        "icon": "wallet",
        "color": "#f59e0b",
        "label": "Financial Caution",
        "label_tamil": "பண எச்சரிக்கை",
    },
    "health_good": {
        "icon": "fitness",
        "color": "#22c55e",
        "label": "Health Peak",
        "label_tamil": "உடல்நலம் சிறப்பு",
    },
    "health_care": {
        "icon": "medkit",
        "color": "#ef4444",
        "label": "Health Care Needed",
        "label_tamil": "உடல்நல கவனிப்பு",
    },
    "spiritual_growth": {
        "icon": "sparkles",
        "color": "#8b5cf6",
        "label": "Spiritual Growth",
        "label_tamil": "ஆன்மீக வளர்ச்சி",
    },
    "travel_opportunity": {
        "icon": "airplane",
        "color": "#3b82f6",
        "label": "Travel/Relocation",
        "label_tamil": "பயணம்/இடமாற்றம்",
    },
    "education_success": {
        "icon": "school",
        "color": "#8b5cf6",
        "label": "Education Success",
        "label_tamil": "கல்வி வெற்றி",
    },
    "marriage_yoga": {
        "icon": "heart-circle",
        "color": "#ec4899",
        "label": "Marriage Yoga",
        "label_tamil": "திருமண யோகம்",
    },
    "child_blessing": {
        "icon": "people",
        "color": "#f97316",
        "label": "Child Blessing",
        "label_tamil": "சந்தான பாக்கியம்",
    },
    "property_gain": {
        "icon": "home",
        "color": "#22c55e",
        "label": "Property/Asset",
        "label_tamil": "சொத்து வாங்குதல்",
    },
}


class LifeTimelineService:
    """Generate life timeline predictions"""

    def __init__(self, jathagam_generator, ephemeris):
        self.jathagam_gen = jathagam_generator
        self.ephemeris = ephemeris

    def generate_life_timeline(self, data) -> Dict:
        """Generate comprehensive life timeline"""
        # Create birth details object
        class BirthDetails:
            def __init__(self, d):
                self.name = d.name
                self.date = d.birth_date
                self.time = d.birth_time
                self.place = d.birth_place
                self.latitude = d.latitude
                self.longitude = d.longitude

        birth_details = BirthDetails(data)

        # Generate jathagam for base data
        jathagam = self.jathagam_gen.generate(birth_details)

        # Get dasha periods
        dasha_periods = jathagam["dasha"]["all_periods"]
        current_dasha = jathagam["dasha"]["current"]

        # Calculate birth year
        birth_year = int(data.birth_date.split("-")[0])
        current_year = datetime.now().year
        years_ahead = data.years_ahead or 10

        # Generate yearly predictions (including past 2 years)
        yearly_timeline = []
        past_years = []

        # Generate past 2 years
        for year in range(current_year - 2, current_year):
            year_data = self._generate_year_prediction(
                year, birth_year, jathagam, dasha_periods
            )
            year_data["is_past"] = True
            past_years.append(year_data)

        # Generate future years
        for year in range(current_year, current_year + years_ahead + 1):
            year_data = self._generate_year_prediction(
                year, birth_year, jathagam, dasha_periods
            )
            year_data["is_past"] = False
            yearly_timeline.append(year_data)

        # Find peak and low periods
        peaks = self._find_peak_periods(yearly_timeline)
        lows = self._find_low_periods(yearly_timeline)

        # Generate major events
        major_events = self._predict_major_events(yearly_timeline, jathagam, dasha_periods)

        # Calculate overall life score trend
        life_trend = self._calculate_life_trend(yearly_timeline)

        return {
            "user_name": data.name,
            "birth_year": birth_year,
            "current_year": current_year,
            "current_dasha": {
                "lord": current_dasha["lord"],
                "lord_tamil": current_dasha["tamil_lord"],
                "end": current_dasha["end"],
                "effects": DASHA_EFFECTS.get(current_dasha["lord"], {}),
            },
            "past_years": past_years,
            "yearly_timeline": yearly_timeline,
            "peak_periods": peaks,
            "low_periods": lows,
            "major_events": major_events,
            "life_trend": life_trend,
            "summary": self._generate_summary(yearly_timeline, major_events, current_dasha),
        }

    def _generate_year_prediction(
        self, year: int, birth_year: int, jathagam: Dict, dasha_periods: List
    ) -> Dict:
        """Generate prediction for a specific year using Astro-Percent Engine"""
        age = year - birth_year

        # Find active dasha for this year
        year_start = datetime(year, 1, 1)
        active_dasha = self._find_active_dasha(year_start, dasha_periods)

        # Get dasha effects (for keywords)
        dasha_effects = DASHA_EFFECTS.get(active_dasha, DASHA_EFFECTS["Sun"])

        # Use Astro-Percent Engine if available
        if AstroPercentEngine:
            return self._generate_year_with_engine(
                year, age, active_dasha, dasha_effects, jathagam
            )

        # Fallback to basic calculation
        planets = {p["planet"]: p for p in jathagam["planets"]}
        dasha_planet = planets.get(active_dasha, {})
        strength_modifier = (dasha_planet.get("strength", 50) - 50) / 100

        # Calculate scores for each area
        career_score = min(100, max(20, dasha_effects["career"] + strength_modifier * 20 + self._year_variation(year, "career")))
        relationship_score = min(100, max(20, dasha_effects["relationships"] + strength_modifier * 15 + self._year_variation(year, "love")))
        finance_score = min(100, max(20, dasha_effects["finances"] + strength_modifier * 20 + self._year_variation(year, "finance")))
        health_score = min(100, max(20, dasha_effects["health"] + strength_modifier * 10 + self._year_variation(year, "health")))

        # Overall score
        overall_score = (career_score * 0.3 + relationship_score * 0.25 + finance_score * 0.25 + health_score * 0.2)

        # Determine period type
        period_type = "high" if overall_score >= 70 else "low" if overall_score < 50 else "normal"

        # Generate events for this year
        events = self._generate_year_events(year, career_score, relationship_score, finance_score, health_score, age, active_dasha)

        return {
            "year": year,
            "age": age,
            "dasha": active_dasha,
            "dasha_tamil": self._get_tamil_planet_name(active_dasha),
            "overall_score": round(overall_score, 1),
            "period_type": period_type,
            "scores": {
                "career": round(career_score, 1),
                "relationships": round(relationship_score, 1),
                "finances": round(finance_score, 1),
                "health": round(health_score, 1),
            },
            "keywords": dasha_effects.get("keywords_tamil", [])[:3],
            "events": events,
            "insight": self._generate_year_insight(year, overall_score, active_dasha, events),
        }

    def _generate_year_with_engine(
        self, year: int, age: int, active_dasha: str, dasha_effects: Dict, jathagam: Dict
    ) -> Dict:
        """Generate year prediction using V6.0 TimeAdaptiveEngine (strongly positive output)"""
        target_date = date(year, 6, 15)  # Mid-year

        # V6.0: Use TimeAdaptiveEngine for more positive output
        if V60_ENGINE_AVAILABLE and TimeAdaptiveEngine:
            engine = TimeAdaptiveEngine(jathagam)
            engine_version = "6.0"
        else:
            engine = AstroPercentEngine(jathagam)
            engine_version = "3.0"

        # Calculate scores for each life area
        life_areas = {
            'career': 'career',
            'relationships': 'relationships',
            'finances': 'finance',
            'health': 'health',
        }

        area_scores = {}
        all_factors = []
        calculation_trace = None
        v3_transit_details = {}
        v3_yoga_details = {}

        for area_key, engine_area in life_areas.items():
            result = engine.calculate_prediction_score(
                target_date=target_date,
                life_area=engine_area,
                dasha_lord=active_dasha,
            )
            area_scores[area_key] = result['score']
            all_factors.extend(result.get('top_factors', []))

            # Store calculation trace from first result
            if calculation_trace is None and result.get('calculation_trace'):
                calculation_trace = result['calculation_trace']

        # Use v3.0 methods for enhanced detail (if available)
        try:
            # v3.0 Transit scoring with detailed tables
            transit_v3 = engine.calculate_transit_score_v3(target_date, 'general')
            v3_transit_details = transit_v3.get('v3_details', {})

            # v3.0 Yoga scoring with longitude validation
            yoga_v3 = engine.calculate_yoga_score_v3()
            v3_yoga_details = {
                'yogas': yoga_v3.get('yogas', []),
                'doshas': yoga_v3.get('doshas', []),
                'longitude_validated': yoga_v3.get('longitude_based', False)
            }
        except Exception:
            pass

        # Calculate overall score (weighted average)
        overall_score = (
            area_scores['career'] * 0.30 +
            area_scores['relationships'] * 0.25 +
            area_scores['finances'] * 0.25 +
            area_scores['health'] * 0.20
        )

        # V6.0: Adjust thresholds for more positive output
        # "high" now includes scores >= 60 (was 70)
        # "low" only for scores < 40 (was 45)
        if overall_score >= 60:
            period_type = "high"
        elif overall_score < 40:
            period_type = "low"
        else:
            period_type = "normal"

        # Generate events based on area scores
        events = self._generate_year_events(
            year,
            area_scores['career'],
            area_scores['relationships'],
            area_scores['finances'],
            area_scores['health'],
            age,
            active_dasha
        )

        # Get top factors for insight
        unique_factors = []
        seen_names = set()
        for f in all_factors:
            if f.get('name') not in seen_names:
                unique_factors.append(f)
                seen_names.add(f.get('name'))

        # Build calculation trace for transparency (v3.0)
        trace_data = {
            "engine_version": engine.ENGINE_VERSION,
            "formula": "(career×30% + relationships×25% + finances×25% + health×20%)",
            "weights": {
                "career": "30%",
                "relationships": "25%",
                "finances": "25%",
                "health": "20%"
            },
            "breakdown": {
                "dasha": calculation_trace.get('step_by_step', [{}])[0] if calculation_trace else {},
                "transit": calculation_trace.get('step_by_step', [{}])[3] if calculation_trace and len(calculation_trace.get('step_by_step', [])) > 3 else {},
                "house": calculation_trace.get('step_by_step', [{}])[1] if calculation_trace and len(calculation_trace.get('step_by_step', [])) > 1 else {},
                "yoga": calculation_trace.get('step_by_step', [{}])[4] if calculation_trace and len(calculation_trace.get('step_by_step', [])) > 4 else {},
            },
            "v3_details": {
                "jupiter_transit_score": v3_transit_details.get('jupiter_table_score'),
                "saturn_condition": v3_transit_details.get('saturn_condition'),
                "retrograde_planets": v3_transit_details.get('retrograde_planets', []),
                "eclipse_applied": v3_transit_details.get('eclipse_applied', False),
                "yogas_found": v3_yoga_details.get('yogas', []),
                "doshas_found": v3_yoga_details.get('doshas', []),
            },
            "meta_multiplier": calculation_trace.get('final_calculation', {}).get('v23_meta_multiplier', 1.0) if calculation_trace else 1.0,
            "provenance": calculation_trace.get('provenance', {}) if calculation_trace else {},
        }

        return {
            "year": year,
            "age": age,
            "dasha": active_dasha,
            "dasha_tamil": self._get_tamil_planet_name(active_dasha),
            "overall_score": round(overall_score, 1),
            "period_type": period_type,
            "scores": {
                "career": round(area_scores['career'], 1),
                "relationships": round(area_scores['relationships'], 1),
                "finances": round(area_scores['finances'], 1),
                "health": round(area_scores['health'], 1),
            },
            "keywords": dasha_effects.get("keywords_tamil", [])[:3],
            "events": events,
            "insight": self._generate_year_insight(
                year, overall_score, active_dasha, events
            ),
            "factors": unique_factors[:5],
            "calculation_trace": trace_data,
            "v3_transit": v3_transit_details,
            "v3_yoga": v3_yoga_details,
        }

    def _find_active_dasha(self, check_date: datetime, dasha_periods: List) -> str:
        """Find which dasha is active on a given date"""
        for dasha in dasha_periods:
            start = datetime.strptime(dasha["start"], "%Y-%m-%d")
            end = datetime.strptime(dasha["end"], "%Y-%m-%d")
            if start <= check_date <= end:
                return dasha["lord"]
        return dasha_periods[0]["lord"] if dasha_periods else "Sun"

    def _year_variation(self, year: int, area: str) -> float:
        """Add natural variation to predictions"""
        import hashlib
        seed = int(hashlib.md5(f"{year}{area}".encode()).hexdigest()[:8], 16)
        return ((seed % 30) - 15)  # -15 to +15 variation

    def _generate_year_events(
        self, year: int, career: float, love: float, finance: float, health: float, age: int, dasha: str
    ) -> List[Dict]:
        """Generate predicted events for a year"""
        events = []

        # Career events
        if career >= 75:
            events.append({"type": "career_rise", **EVENT_TYPES["career_rise"]})
        elif career < 45:
            events.append({"type": "career_challenge", **EVENT_TYPES["career_challenge"]})

        # Relationship events
        if love >= 80:
            events.append({"type": "relationship_bloom", **EVENT_TYPES["relationship_bloom"]})
            # Marriage yoga in prime age during Venus/Jupiter dasha
            if 24 <= age <= 35 and dasha in ["Venus", "Jupiter", "Moon"]:
                events.append({"type": "marriage_yoga", **EVENT_TYPES["marriage_yoga"]})
        elif love < 50:
            events.append({"type": "relationship_test", **EVENT_TYPES["relationship_test"]})

        # Financial events
        if finance >= 75:
            events.append({"type": "financial_gain", **EVENT_TYPES["financial_gain"]})
            # Property opportunity during Jupiter/Venus/Mars dasha
            if dasha in ["Jupiter", "Venus", "Mars"] and finance >= 80:
                events.append({"type": "property_gain", **EVENT_TYPES["property_gain"]})
        elif finance < 50:
            events.append({"type": "financial_caution", **EVENT_TYPES["financial_caution"]})

        # Health events
        if health >= 75:
            events.append({"type": "health_good", **EVENT_TYPES["health_good"]})
        elif health < 45:
            events.append({"type": "health_care", **EVENT_TYPES["health_care"]})

        # Special events based on dasha
        if dasha == "Ketu":
            events.append({"type": "spiritual_growth", **EVENT_TYPES["spiritual_growth"]})
        if dasha in ["Rahu", "Moon", "Venus"]:
            events.append({"type": "travel_opportunity", **EVENT_TYPES["travel_opportunity"]})
        if dasha in ["Mercury", "Jupiter"] and 15 <= age <= 30:
            events.append({"type": "education_success", **EVENT_TYPES["education_success"]})
        if dasha in ["Jupiter", "Venus"] and 28 <= age <= 40:
            events.append({"type": "child_blessing", **EVENT_TYPES["child_blessing"]})

        return events[:5]  # Limit to 5 events per year

    def _generate_year_insight(self, year: int, score: float, dasha: str, events: List) -> Dict:
        """Generate insight text for a year"""
        dasha_tamil = self._get_tamil_planet_name(dasha)

        if score >= 75:
            return {
                "text": f"{dasha_tamil} தசையில் சிறந்த பலன்கள். வாய்ப்புகளை பயன்படுத்துங்கள்.",
                "text_en": f"Excellent results in {dasha} dasha. Utilize opportunities.",
                "mood": "positive",
            }
        elif score >= 60:
            return {
                "text": f"{dasha_tamil} தசையில் நல்ல முன்னேற்றம். தொடர்ந்து முயற்சி செய்யுங்கள்.",
                "text_en": f"Good progress in {dasha} dasha. Keep up the effort.",
                "mood": "good",
            }
        elif score >= 45:
            return {
                "text": f"{dasha_tamil} தசையில் கலவையான பலன்கள். பொறுமையாக இருங்கள்.",
                "text_en": f"Mixed results in {dasha} dasha. Stay patient.",
                "mood": "neutral",
            }
        else:
            return {
                "text": f"{dasha_tamil} தசையில் சவால்கள் எதிர்பார்க்கலாம். பரிகாரங்கள் செய்யுங்கள்.",
                "text_en": f"Challenges expected in {dasha} dasha. Perform remedies.",
                "mood": "challenging",
            }

    def _find_peak_periods(self, timeline: List[Dict]) -> List[Dict]:
        """Find peak periods in the timeline"""
        peaks = []
        for year_data in timeline:
            if year_data["overall_score"] >= 72:
                peaks.append({
                    "year": year_data["year"],
                    "score": year_data["overall_score"],
                    "dasha": year_data["dasha"],
                    "dasha_tamil": year_data["dasha_tamil"],
                    "highlight": year_data["keywords"][:2] if year_data["keywords"] else [],
                })
        return sorted(peaks, key=lambda x: x["score"], reverse=True)[:5]

    def _find_low_periods(self, timeline: List[Dict]) -> List[Dict]:
        """Find challenging periods in the timeline"""
        lows = []
        for year_data in timeline:
            if year_data["overall_score"] < 48:
                lows.append({
                    "year": year_data["year"],
                    "score": year_data["overall_score"],
                    "dasha": year_data["dasha"],
                    "dasha_tamil": year_data["dasha_tamil"],
                    "caution_areas": [
                        area for area, score in year_data["scores"].items() if score < 50
                    ],
                })
        return sorted(lows, key=lambda x: x["score"])[:3]

    def _predict_major_events(self, timeline: List[Dict], jathagam: Dict, dasha_periods: List) -> List[Dict]:
        """Predict major life events"""
        major_events = []

        for year_data in timeline:
            for event in year_data.get("events", []):
                if event["type"] in ["marriage_yoga", "child_blessing", "property_gain", "career_rise"]:
                    major_events.append({
                        "year": year_data["year"],
                        "age": year_data["age"],
                        "event_type": event["type"],
                        "label": event["label"],
                        "label_tamil": event["label_tamil"],
                        "icon": event["icon"],
                        "color": event["color"],
                        "probability": min(95, year_data["overall_score"] + 10),
                    })

        # Sort by year and remove duplicates
        seen = set()
        unique_events = []
        for event in sorted(major_events, key=lambda x: x["year"]):
            key = f"{event['year']}_{event['event_type']}"
            if key not in seen:
                seen.add(key)
                unique_events.append(event)

        return unique_events[:10]

    def _calculate_life_trend(self, timeline: List[Dict]) -> Dict:
        """Calculate overall life trend"""
        if not timeline:
            return {"direction": "stable", "change": 0}

        scores = [y["overall_score"] for y in timeline]
        first_half_avg = sum(scores[:len(scores)//2]) / max(1, len(scores)//2)
        second_half_avg = sum(scores[len(scores)//2:]) / max(1, len(scores) - len(scores)//2)

        change = second_half_avg - first_half_avg

        if change > 5:
            direction = "ascending"
            direction_tamil = "உயர்வு நிலை"
        elif change < -5:
            direction = "descending"
            direction_tamil = "சவால் நிலை"
        else:
            direction = "stable"
            direction_tamil = "நிலையான நிலை"

        return {
            "direction": direction,
            "direction_tamil": direction_tamil,
            "change": round(change, 1),
            "average_score": round(sum(scores) / len(scores), 1),
            "highest_year": max(timeline, key=lambda x: x["overall_score"])["year"],
            "lowest_year": min(timeline, key=lambda x: x["overall_score"])["year"],
        }

    def _generate_summary(self, timeline: List[Dict], events: List[Dict], current_dasha: Dict) -> Dict:
        """Generate overall summary"""
        if not timeline:
            return {}

        avg_score = sum(y["overall_score"] for y in timeline) / len(timeline)
        high_years = [y for y in timeline if y["overall_score"] >= 70]
        challenging_years = [y for y in timeline if y["overall_score"] < 50]

        # Count event types
        career_events = len([e for e in events if "career" in e.get("event_type", "")])
        relationship_events = len([e for e in events if e.get("event_type", "") in ["marriage_yoga", "relationship_bloom", "child_blessing"]])
        financial_events = len([e for e in events if e.get("event_type", "") in ["financial_gain", "property_gain"]])

        return {
            "overall_outlook": "positive" if avg_score >= 60 else "moderate" if avg_score >= 45 else "challenging",
            "overall_outlook_tamil": "நல்ல எதிர்காலம்" if avg_score >= 60 else "சராசரி எதிர்காலம்" if avg_score >= 45 else "சவாலான எதிர்காலம்",
            "average_score": round(avg_score, 1),
            "high_period_count": len(high_years),
            "challenging_period_count": len(challenging_years),
            "career_opportunities": career_events,
            "relationship_milestones": relationship_events,
            "financial_opportunities": financial_events,
            "current_dasha_advice": self._get_dasha_advice(current_dasha["lord"]),
        }

    def _get_dasha_advice(self, dasha_lord: str) -> Dict:
        """Get advice for current dasha"""
        advice = {
            "Sun": {
                "focus": "Focus on leadership and recognition opportunities",
                "focus_tamil": "தலைமைத்துவம் மற்றும் அங்கீகார வாய்ப்புகளில் கவனம் செலுத்துங்கள்",
                "avoid": "Avoid ego conflicts",
                "avoid_tamil": "ஆணவ மோதல்களை தவிர்க்கவும்",
            },
            "Moon": {
                "focus": "Nurture relationships and emotional well-being",
                "focus_tamil": "உறவுகளையும் மன நலனையும் பேணுங்கள்",
                "avoid": "Avoid over-sensitivity",
                "avoid_tamil": "அதிக உணர்ச்சிவசப்படுவதை தவிர்க்கவும்",
            },
            "Mars": {
                "focus": "Take bold actions in career and property matters",
                "focus_tamil": "தொழில் மற்றும் சொத்து விஷயங்களில் தைரியமான முடிவுகள் எடுங்கள்",
                "avoid": "Avoid aggression and hasty decisions",
                "avoid_tamil": "ஆத்திரமும் அவசர முடிவுகளும் தவிர்க்கவும்",
            },
            "Mercury": {
                "focus": "Expand business and communication skills",
                "focus_tamil": "வணிகம் மற்றும் தொடர்பு திறன்களை விரிவுபடுத்துங்கள்",
                "avoid": "Avoid scattered focus",
                "avoid_tamil": "கவனம் சிதறுவதை தவிர்க்கவும்",
            },
            "Jupiter": {
                "focus": "Pursue education, spirituality, and expansion",
                "focus_tamil": "கல்வி, ஆன்மீகம், வளர்ச்சியில் கவனம் செலுத்துங்கள்",
                "avoid": "Avoid over-optimism",
                "avoid_tamil": "அதிக நம்பிக்கையை தவிர்க்கவும்",
            },
            "Venus": {
                "focus": "Focus on relationships, art, and luxury",
                "focus_tamil": "உறவுகள், கலை, ஆடம்பரத்தில் கவனம் செலுத்துங்கள்",
                "avoid": "Avoid overindulgence",
                "avoid_tamil": "அதிக இன்பம் தேடுவதை தவிர்க்கவும்",
            },
            "Saturn": {
                "focus": "Work hard with discipline and patience",
                "focus_tamil": "ஒழுக்கத்துடன் கடினமாக உழையுங்கள்",
                "avoid": "Avoid shortcuts and laziness",
                "avoid_tamil": "குறுக்கு வழிகளையும் சோம்பலையும் தவிர்க்கவும்",
            },
            "Rahu": {
                "focus": "Explore foreign opportunities and innovation",
                "focus_tamil": "வெளிநாட்டு வாய்ப்புகளையும் புதுமைகளையும் ஆராயுங்கள்",
                "avoid": "Avoid deception and shortcuts",
                "avoid_tamil": "ஏமாற்றமும் குறுக்கு வழிகளும் தவிர்க்கவும்",
            },
            "Ketu": {
                "focus": "Focus on spirituality and letting go",
                "focus_tamil": "ஆன்மீகத்திலும் விட்டுவிடுதலிலும் கவனம் செலுத்துங்கள்",
                "avoid": "Avoid attachment to material things",
                "avoid_tamil": "பொருள் ஆசையை தவிர்க்கவும்",
            },
        }
        return advice.get(dasha_lord, advice["Sun"])

    def _get_tamil_planet_name(self, planet: str) -> str:
        """Get Tamil name for planet"""
        tamil_names = {
            "Sun": "சூரியன்",
            "Moon": "சந்திரன்",
            "Mars": "செவ்வாய்",
            "Mercury": "புதன்",
            "Jupiter": "குரு",
            "Venus": "சுக்கிரன்",
            "Saturn": "சனி",
            "Rahu": "ராகு",
            "Ketu": "கேது",
        }
        return tamil_names.get(planet, planet)
