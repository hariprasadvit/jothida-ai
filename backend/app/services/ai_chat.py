"""
AI Chat Service
Tamil Astrology Chatbot using RAG + LLM
"""

from typing import Dict, List, Optional
import json
import re
from datetime import datetime, date


class AIChatService:
    """
    AI Chat Service for Tamil Astrology
    Uses RAG (Retrieval Augmented Generation) with:
    - ChromaDB for vector storage
    - Tamil-LLaMA or Gemma for generation
    - Custom knowledge base for astrology
    """
    
    # Intent patterns for smart query understanding
    # Order matters! More specific patterns should come first
    INTENT_PATTERNS = {
        "three_year_prediction": [
            r"3 வருடம்", r"மூன்று வருடம்", r"three year", r"3 year", r"next 3", r"அடுத்த 3", r"3year", r"3-year"
        ],
        "yearly_prediction": [
            r"வருடம்", r"year", r"இந்த வருடம்", r"this year", r"yearly", r"annual"
        ],
        "monthly_prediction": [
            r"மாதம்", r"month", r"இந்த மாதம்", r"this month", r"monthly", r"30 days"
        ],
        "weekly_prediction": [
            r"வாரம்", r"week", r"இந்த வாரம்", r"this week", r"7 days"
        ],
        "daily_prediction": [
            r"இன்று", r"today", r"daily", r"தினம்", r"நாள்"
        ],
        "nalla_neram": [
            r"நல்ல நேரம்", r"nalla neram", r"good time", r"auspicious",
            r"சுப முகூர்த்தம்", r"subha muhurtham"
        ],
        "rahu_kalam": [
            r"ராகு", r"rahu", r"yamagandam", r"யமகண்டம்"
        ],
        "career": [
            r"தொழில்", r"வேலை", r"job", r"career", r"interview",
            r"office", r"ஆபீஸ்", r"business", r"தொழில்"
        ],
        "love": [
            r"காதல்", r"love", r"relationship", r"marriage", r"திருமணம்"
        ],
        "health": [
            r"உடல்", r"health", r"medical", r"சிகிச்சை", r"ஆரோக்கியம்"
        ],
        "muhurtham": [
            r"முகூர்த்தம்", r"muhurtham", r"நல்ல நாள்", r"போகலாமா"
        ],
        "rasipalan": [
            r"ராசி", r"rasi", r"horoscope", r"பலன்"
        ]
    }
    
    def __init__(self, kb_path: str = "knowledge_base", ephemeris=None):
        """Initialize with knowledge base path and optional ephemeris service"""
        self.kb_path = kb_path
        self.conversation_history = {}
        self.ephemeris = ephemeris
        self.panchangam = None

        # Initialize panchangam calculator if ephemeris is available
        if ephemeris:
            from app.services.panchangam_calculator import PanchangamCalculator
            self.panchangam = PanchangamCalculator(ephemeris)
    
    async def process_message(
        self,
        message: str,
        user_id: str,
        conversation_id: Optional[str] = None,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Process user message and generate response
        
        1. Detect intent
        2. Extract entities (dates, times, topics)
        3. Retrieve relevant knowledge
        4. Generate personalized response
        5. Include rich data for UI
        """
        
        # Detect intent
        intent = self._detect_intent(message)
        
        # Extract entities
        entities = self._extract_entities(message)
        
        # Get relevant context from knowledge base
        kb_context = self._retrieve_knowledge(message, intent)
        
        # Generate response based on intent
        response = await self._generate_response(
            message=message,
            intent=intent,
            entities=entities,
            kb_context=kb_context,
            user_context=context
        )
        
        # Store in conversation history
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        self.conversation_history[user_id].append({
            "role": "assistant",
            "content": response["message"],
            "timestamp": datetime.now().isoformat()
        })
        
        return response
    
    def _detect_intent(self, message: str) -> str:
        """Detect user intent from message"""
        message_lower = message.lower()
        
        for intent, patterns in self.INTENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, message_lower, re.IGNORECASE):
                    return intent
        
        return "general"
    
    def _extract_entities(self, message: str) -> Dict:
        """Extract entities like dates, times, topics"""
        entities = {
            "date": None,
            "time": None,
            "event_type": None
        }
        
        # Date patterns
        if "நாளை" in message or "tomorrow" in message.lower():
            entities["date"] = "tomorrow"
        elif "இன்று" in message or "today" in message.lower():
            entities["date"] = "today"
        elif "இந்த வாரம்" in message or "this week" in message.lower():
            entities["date"] = "this_week"
        
        # Event types
        event_keywords = {
            "interview": "career",
            "வேலை": "career",
            "திருமணம்": "marriage",
            "marriage": "marriage",
            "பயணம்": "travel",
            "travel": "travel"
        }
        
        for keyword, event_type in event_keywords.items():
            if keyword in message.lower():
                entities["event_type"] = event_type
                break
        
        return entities
    
    def _retrieve_knowledge(self, query: str, intent: str) -> str:
        """Retrieve relevant knowledge from vector store"""
        # Placeholder - implement with actual vector search
        
        # For now, return static knowledge based on intent
        KNOWLEDGE = {
            "nalla_neram": """
நல்ல நேரம் என்பது கோவிரி பஞ்சாங்கத்தின் படி சுப காரியங்களுக்கு 
ஏற்ற நேரமாகும். ஒவ்வொரு நாளும் சூரிய உதயம் முதல் சூரிய அஸ்தமனம் வரை 
8 காலங்களாக பிரிக்கப்படும். இதில் சில காலங்கள் நல்லவை, சில தீயவை.
            """,
            "rahu_kalam": """
ராகு காலம் என்பது தினமும் ஒன்றரை மணி நேரம் நீடிக்கும் அசுப காலமாகும்.
இந்த நேரத்தில் புதிய காரியங்களை தொடங்குவது நல்லதல்ல.
ஞாயிறு: 4:30-6:00 PM, திங்கள்: 7:30-9:00 AM போன்று மாறும்.
            """,
            "career": """
தொழில் சம்பந்தமான விஷயங்களுக்கு 10வது வீடு முக்கியம். 
இந்த வீட்டின் அதிபதி பலமாக இருந்தால் தொழில் முன்னேற்றம் உண்டு.
புதன் மற்றும் குரு பலமாக இருக்கும் நேரம் interview-க்கு சிறந்தது.
            """
        }
        
        return KNOWLEDGE.get(intent, "")
    
    async def _generate_response(
        self,
        message: str,
        intent: str,
        entities: Dict,
        kb_context: str,
        user_context: Optional[Dict]
    ) -> Dict:
        """Generate AI response with rich data using real panchangam"""

        # Get today's panchangam if available
        panchang_data = None
        if self.panchangam:
            try:
                lat = user_context.get("latitude", 13.0827) if user_context else 13.0827
                lon = user_context.get("longitude", 80.2707) if user_context else 80.2707
                panchang_data = self.panchangam.calculate(date.today(), lat, lon, "Asia/Kolkata")
            except Exception as e:
                print(f"Error getting panchangam: {e}")

        if intent == "nalla_neram" or intent == "daily_prediction":
            # Build time slots from real panchangam data
            slots = []
            warning = None

            if panchang_data:
                # Get nalla neram slots
                nalla_neram = panchang_data.get("nalla_neram", [])
                for i, slot in enumerate(nalla_neram[:3]):
                    slots.append({
                        "start": slot.get("start", "09:00"),
                        "end": slot.get("end", "10:30"),
                        "quality": 92 - (i * 10),
                        "label": "சிறந்த நேரம்" if i == 0 else "நல்ல நேரம்"
                    })

                # Get auspicious times
                auspicious = panchang_data.get("auspicious", {})
                if auspicious.get("abhijit"):
                    slots.append({
                        "start": auspicious["abhijit"].get("start", "11:45"),
                        "end": auspicious["abhijit"].get("end", "12:30"),
                        "quality": 95,
                        "label": "அபிஜித் முகூர்த்தம் ⭐"
                    })

                # Get Rahu Kalam warning
                rahu = panchang_data.get("rahu_kalam", {}) or panchang_data.get("inauspicious", {}).get("rahu_kalam", {})
                if rahu:
                    warning = {
                        "start": rahu.get("start", "15:00"),
                        "end": rahu.get("end", "16:30"),
                        "label": "ராகு காலம் - தவிர்க்கவும்"
                    }

                nakshatra = panchang_data.get("nakshatra", {}).get("tamil", "")
                tithi = panchang_data.get("tithi", {}).get("tamil", "")
                insight = f"இன்று {nakshatra} நட்சத்திரம், {tithi} திதி. "

                score = panchang_data.get("overall_score", 70)
                if score >= 75:
                    insight += "மிகவும் சுபகரமான நாள். முக்கிய காரியங்களுக்கு ஏற்றது."
                elif score >= 60:
                    insight += "நல்ல நாள். அபிஜித் முகூர்த்தத்தில் முக்கிய முடிவுகள் எடுங்கள்."
                else:
                    insight += "சாதாரண நாள். ராகு காலம் தவிர்க்கவும்."
            else:
                # Fallback if panchangam not available
                slots = [
                    {"start": "09:00", "end": "10:30", "quality": 92, "label": "சிறந்த நேரம்"},
                    {"start": "14:00", "end": "15:30", "quality": 78, "label": "நல்ல நேரம்"}
                ]
                warning = {"start": "15:00", "end": "16:30", "label": "ராகு காலம் - தவிர்க்கவும்"}
                insight = "குரு & சுக்கிரன் இணைவால் காலை நேரம் மிகவும் சிறப்பு."

            return {
                "message": "இன்று உங்களுக்கு சிறந்த நேரங்கள்:",
                "data": {
                    "type": "time_slots",
                    "slots": slots,
                    "warning": warning
                },
                "insight": insight,
                "action": None
            }

        elif intent == "rahu_kalam":
            rahu = {}
            yama = {}
            kuligai = {}

            if panchang_data:
                inauspicious = panchang_data.get("inauspicious", {})
                rahu = inauspicious.get("rahu_kalam", panchang_data.get("rahu_kalam", {}))
                yama = inauspicious.get("yamagandam", panchang_data.get("yamagandam", {}))
                kuligai = inauspicious.get("kuligai", panchang_data.get("kuligai", {}))

            return {
                "message": "இன்றைய தவிர்க்க வேண்டிய நேரங்கள்:",
                "data": {
                    "type": "time_slots",
                    "slots": [],
                    "warning": {
                        "start": rahu.get("start", "15:00"),
                        "end": rahu.get("end", "16:30"),
                        "label": "ராகு காலம்"
                    }
                },
                "insight": f"ராகு காலம்: {rahu.get('start', '-')} - {rahu.get('end', '-')}\nயமகண்டம்: {yama.get('start', '-')} - {yama.get('end', '-')}\nகுளிகை: {kuligai.get('start', '-')} - {kuligai.get('end', '-')}",
                "action": None
            }

        elif intent == "career":
            score = 85
            if panchang_data:
                score = min(95, int(panchang_data.get("overall_score", 70) + 15))

            return {
                "message": "தொழில் சம்பந்தமான விஷயங்களுக்கு இன்று நல்ல நாள்!",
                "data": {
                    "type": "recommendation",
                    "score": score,
                    "factors": [
                        {"name": "புதன் பலம்", "value": 88, "positive": True},
                        {"name": "10ம் வீடு", "value": 75, "positive": True},
                        {"name": "குரு பார்வை", "value": 92, "positive": True}
                    ]
                },
                "insight": "10ம் வீட்டில் குரு பார்வை உள்ளதால் தொழில் முன்னேற்றத்திற்கு நல்ல நேரம். காலை 9-11 மணிக்குள் முக்கிய முடிவுகள் எடுங்கள்.",
                "action": {
                    "type": "muhurtham",
                    "text": "சரியான நேரத்தை அமைக்கவும்"
                }
            }

        elif intent == "love":
            return {
                "message": "காதல் & திருமண விஷயங்களுக்கு:",
                "data": {
                    "type": "recommendation",
                    "score": 72,
                    "factors": [
                        {"name": "சுக்கிரன் பலம்", "value": 78, "positive": True},
                        {"name": "7ம் வீடு", "value": 70, "positive": True},
                        {"name": "சந்திரன்", "value": 68, "positive": True}
                    ]
                },
                "insight": "சுக்கிரன் நல்ல நிலையில் உள்ளார். காதல் உறவுகளுக்கு சாதகமான நேரம். மாலை நேரத்தில் முக்கிய உரையாடல்கள் சிறப்பாக அமையும்.",
                "action": None
            }

        elif intent == "rasipalan":
            user_rasi = user_context.get("rasi", "") if user_context else ""
            score = int(panchang_data.get("overall_score", 72)) if panchang_data else 72

            # Only return horoscope type - no duplicate scores
            return {
                "message": f"{'உங்கள் ' + user_rasi + ' ' if user_rasi else ''}இன்றைய ராசிபலன்:",
                "data": {
                    "type": "horoscope",
                    "overall_score": score,
                    "areas": {
                        "தொழில்": min(100, score + 8),
                        "காதல்": max(50, score - 7),
                        "ஆரோக்கியம்": min(100, score + 3),
                        "நிதி": max(50, score - 4)
                    }
                },
                "insight": None,  # Remove separate insight to avoid duplicate display
                "action": None
            }

        elif intent == "weekly_prediction":
            # Get weekly forecast from ForecastService
            user_rasi = user_context.get("rasi", "மேஷம்") if user_context else "மேஷம்"
            user_nakshatra = user_context.get("nakshatra", "") if user_context else ""

            try:
                from app.services.forecast_service import ForecastService
                forecast_service = ForecastService(ephemeris=self.ephemeris)
                rasi_num = forecast_service.RASI_NUMBERS.get(user_rasi, 1)
                weekly = forecast_service._get_weekly_forecast(rasi_num, user_nakshatra, date.today())

                return {
                    "message": f"இந்த வாரம் உங்கள் பலன் ({user_rasi}):",
                    "data": {
                        "type": "weekly_forecast",
                        "average_score": weekly["average_score"],
                        "days": weekly["days"],
                        "best_day": weekly["best_day"],
                        "worst_day": weekly["worst_day"]
                    },
                    "insight": weekly["advice"],
                    "action": {
                        "type": "navigate",
                        "text": "முழு பலன் பார்க்க",
                        "path": "/"
                    }
                }
            except Exception as e:
                print(f"Weekly forecast error: {e}")
                return {
                    "message": "இந்த வாரத்தின் முக்கிய அம்சங்கள்:",
                    "data": {
                        "type": "recommendation",
                        "score": 75,
                        "factors": [
                            {"name": "தொழில்", "value": 80, "positive": True},
                            {"name": "ஆரோக்கியம்", "value": 75, "positive": True},
                            {"name": "நிதி", "value": 70, "positive": True}
                        ]
                    },
                    "insight": "இந்த வாரம் பொதுவாக நல்ல வாரம். வியாழன் மற்றும் வெள்ளி சிறந்த நாட்கள்.",
                    "action": None
                }

        elif intent == "monthly_prediction":
            # Get monthly forecast from ForecastService
            user_rasi = user_context.get("rasi", "மேஷம்") if user_context else "மேஷம்"
            user_nakshatra = user_context.get("nakshatra", "") if user_context else ""

            try:
                from app.services.forecast_service import ForecastService
                forecast_service = ForecastService(ephemeris=self.ephemeris)
                rasi_num = forecast_service.RASI_NUMBERS.get(user_rasi, 1)
                monthly = forecast_service._get_monthly_forecast(rasi_num, user_nakshatra, date.today())

                return {
                    "message": f"{monthly['month_name']} மாத பலன் ({user_rasi}):",
                    "data": {
                        "type": "monthly_forecast",
                        "month_name": monthly["month_name"],
                        "average_score": monthly["average_score"],
                        "good_days_count": monthly["good_days_count"],
                        "caution_days_count": monthly["caution_days_count"],
                        "best_periods": monthly.get("best_periods", [])
                    },
                    "insight": monthly["advice"],
                    "action": {
                        "type": "navigate",
                        "text": "முழு பலன் பார்க்க",
                        "path": "/"
                    }
                }
            except Exception as e:
                print(f"Monthly forecast error: {e}")
                return {
                    "message": "இந்த மாதத்தின் பலன்:",
                    "data": {
                        "type": "recommendation",
                        "score": 72,
                        "factors": [
                            {"name": "சிறந்த நாட்கள்", "value": 10, "positive": True},
                            {"name": "கவனம் தேவை", "value": 5, "positive": False}
                        ]
                    },
                    "insight": "இந்த மாதம் பொதுவாக நல்ல மாதம். முதல் வாரம் சிறப்பாக இருக்கும்.",
                    "action": None
                }

        elif intent == "yearly_prediction":
            # Get yearly forecast from ForecastService
            user_rasi = user_context.get("rasi", "மேஷம்") if user_context else "மேஷம்"
            user_nakshatra = user_context.get("nakshatra", "") if user_context else ""

            try:
                from app.services.forecast_service import ForecastService
                forecast_service = ForecastService(ephemeris=self.ephemeris)
                rasi_num = forecast_service.RASI_NUMBERS.get(user_rasi, 1)
                yearly = forecast_service._get_yearly_forecast(rasi_num, user_nakshatra, date.today())

                return {
                    "message": f"{yearly['year']} வருட பலன் ({user_rasi}):",
                    "data": {
                        "type": "yearly_forecast",
                        "year": yearly["year"],
                        "average_score": yearly["average_score"],
                        "months": yearly["months"],
                        "best_months": yearly["best_months"],
                        "challenging_months": yearly["challenging_months"]
                    },
                    "insight": yearly["advice"],
                    "action": {
                        "type": "navigate",
                        "text": "முழு பலன் பார்க்க",
                        "path": "/"
                    }
                }
            except Exception as e:
                print(f"Yearly forecast error: {e}")
                return {
                    "message": "இந்த வருடத்தின் பலன்:",
                    "data": {
                        "type": "recommendation",
                        "score": 70,
                        "factors": [
                            {"name": "சிறந்த மாதங்கள்", "value": 4, "positive": True},
                            {"name": "கவனம் தேவை", "value": 2, "positive": False}
                        ]
                    },
                    "insight": "இந்த வருடம் பொதுவாக நல்ல வருடம்.",
                    "action": None
                }

        elif intent == "three_year_prediction":
            # Get 3-year forecast from ForecastService
            user_rasi = user_context.get("rasi", "மேஷம்") if user_context else "மேஷம்"
            user_nakshatra = user_context.get("nakshatra", "") if user_context else ""

            try:
                from app.services.forecast_service import ForecastService
                forecast_service = ForecastService(ephemeris=self.ephemeris)
                rasi_num = forecast_service.RASI_NUMBERS.get(user_rasi, 1)
                three_years = forecast_service._get_three_year_forecast(rasi_num, user_nakshatra, date.today())

                return {
                    "message": f"அடுத்த 3 வருட பலன் ({user_rasi}):",
                    "data": {
                        "type": "three_year_forecast",
                        "years": three_years
                    },
                    "insight": "அடுத்த மூன்று வருடங்களின் மாதவாரி பலன் விவரங்கள். டாஷ்போர்டில் முழு விவரம் பார்க்கலாம்.",
                    "action": {
                        "type": "navigate",
                        "text": "முழு பலன் பார்க்க",
                        "path": "/"
                    }
                }
            except Exception as e:
                print(f"Three year forecast error: {e}")
                return {
                    "message": "அடுத்த 3 வருட பலன்:",
                    "data": None,
                    "insight": "டாஷ்போர்டில் 3 வருட பலன் பார்க்கலாம்.",
                    "action": {
                        "type": "navigate",
                        "text": "டாஷ்போர்டு செல்ல",
                        "path": "/"
                    }
                }

        elif intent == "muhurtham":
            return {
                "message": "முகூர்த்த நாள் கண்டுபிடிக்க:",
                "data": None,
                "insight": "திருமணம், கிரஹப்பிரவேசம், வாகனம் வாங்குதல் போன்ற காரியங்களுக்கு சரியான நாளை முகூர்த்தம் பக்கத்தில் கண்டுபிடிக்கலாம்.",
                "action": {
                    "type": "navigate",
                    "text": "முகூர்த்தம் பக்கம் செல்ல",
                    "path": "/muhurtham"
                }
            }

        else:
            # General response with today's summary
            if panchang_data:
                nakshatra = panchang_data.get("nakshatra", {}).get("tamil", "")
                tithi = panchang_data.get("tithi", {}).get("tamil", "")
                vaaram = panchang_data.get("vaaram", "")
                score = panchang_data.get("overall_score", 70)

                return {
                    "message": f"இன்று {vaaram}, {nakshatra} நட்சத்திரம், {tithi} திதி.",
                    "data": {
                        "type": "recommendation",
                        "score": int(score),
                        "factors": []
                    },
                    "insight": f"இன்றைய மொத்த மதிப்பெண்: {int(score)}%. நல்ல நேரம், ராகு காலம் பற்றி கேளுங்கள்.",
                    "action": None
                }

            return {
                "message": "உங்கள் கேள்விக்கு பதில்:",
                "data": None,
                "insight": "இன்று நல்ல நேரம், ராசிபலன், தொழில் பலன் போன்றவை பற்றி கேளுங்கள்.",
                "action": None
            }
    
    def get_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get conversation history for a user"""
        history = self.conversation_history.get(user_id, [])
        return history[-limit:]
