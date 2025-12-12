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
        context: Optional[Dict] = None,
        language: str = "ta"
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
            user_context=context,
            language=language
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
    
    def _get_text(self, key: str, language: str) -> str:
        """Get localized text based on language"""
        TEXTS = {
            "best_times_today": {
                "ta": "இன்று உங்களுக்கு சிறந்த நேரங்கள்:",
                "en": "Best times for you today:",
                "kn": "ಇಂದು ನಿಮಗೆ ಉತ್ತಮ ಸಮಯಗಳು:"
            },
            "best_time": {
                "ta": "சிறந்த நேரம்",
                "en": "Best time",
                "kn": "ಅತ್ಯುತ್ತಮ ಸಮಯ"
            },
            "good_time": {
                "ta": "நல்ல நேரம்",
                "en": "Good time",
                "kn": "ಒಳ್ಳೆಯ ಸಮಯ"
            },
            "abhijit_muhurtham": {
                "ta": "அபிஜித் முகூர்த்தம் ⭐",
                "en": "Abhijit Muhurtham ⭐",
                "kn": "ಅಭಿಜಿತ್ ಮುಹೂರ್ತ ⭐"
            },
            "rahu_kalam_avoid": {
                "ta": "ராகு காலம் - தவிர்க்கவும்",
                "en": "Rahu Kalam - Avoid",
                "kn": "ರಾಹು ಕಾಲ - ತಪ್ಪಿಸಿ"
            },
            "today_nakshatra_tithi": {
                "ta": "இன்று {nakshatra} நட்சத்திரம், {tithi} திதி. ",
                "en": "Today is {nakshatra} nakshatra, {tithi} tithi. ",
                "kn": "ಇಂದು {nakshatra} ನಕ್ಷತ್ರ, {tithi} ತಿಥಿ. "
            },
            "very_auspicious_day": {
                "ta": "மிகவும் சுபகரமான நாள். முக்கிய காரியங்களுக்கு ஏற்றது.",
                "en": "Very auspicious day. Suitable for important tasks.",
                "kn": "ಅತ್ಯಂತ ಶುಭ ದಿನ. ಪ್ರಮುಖ ಕಾರ್ಯಗಳಿಗೆ ಸೂಕ್ತ."
            },
            "good_day": {
                "ta": "நல்ல நாள். அபிஜித் முகூர்த்தத்தில் முக்கிய முடிவுகள் எடுங்கள்.",
                "en": "Good day. Take important decisions during Abhijit Muhurtham.",
                "kn": "ಒಳ್ಳೆಯ ದಿನ. ಅಭಿಜಿತ್ ಮುಹೂರ್ತದಲ್ಲಿ ಪ್ರಮುಖ ನಿರ್ಧಾರಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳಿ."
            },
            "normal_day": {
                "ta": "சாதாரண நாள். ராகு காலம் தவிர்க்கவும்.",
                "en": "Normal day. Avoid Rahu Kalam.",
                "kn": "ಸಾಮಾನ್ಯ ದಿನ. ರಾಹು ಕಾಲ ತಪ್ಪಿಸಿ."
            },
            "morning_special": {
                "ta": "குரு & சுக்கிரன் இணைவால் காலை நேரம் மிகவும் சிறப்பு.",
                "en": "Morning time is very special due to Jupiter & Venus conjunction.",
                "kn": "ಗುರು ಮತ್ತು ಶುಕ್ರ ಸಂಯೋಗದಿಂದ ಬೆಳಗಿನ ಸಮಯ ತುಂಬಾ ವಿಶೇಷ."
            },
            "inauspicious_times": {
                "ta": "இன்றைய தவிர்க்க வேண்டிய நேரங்கள்:",
                "en": "Times to avoid today:",
                "kn": "ಇಂದು ತಪ್ಪಿಸಬೇಕಾದ ಸಮಯಗಳು:"
            },
            "rahu_kalam": {
                "ta": "ராகு காலம்",
                "en": "Rahu Kalam",
                "kn": "ರಾಹು ಕಾಲ"
            },
            "career_good_day": {
                "ta": "தொழில் சம்பந்தமான விஷயங்களுக்கு இன்று நல்ல நாள்!",
                "en": "Today is a good day for career-related matters!",
                "kn": "ವೃತ್ತಿ ಸಂಬಂಧಿತ ವಿಷಯಗಳಿಗೆ ಇಂದು ಒಳ್ಳೆಯ ದಿನ!"
            },
            "career_insight": {
                "ta": "10ம் வீட்டில் குரு பார்வை உள்ளதால் தொழில் முன்னேற்றத்திற்கு நல்ல நேரம். காலை 9-11 மணிக்குள் முக்கிய முடிவுகள் எடுங்கள்.",
                "en": "Good time for career progress due to Jupiter's aspect on 10th house. Take important decisions between 9-11 AM.",
                "kn": "10ನೇ ಮನೆಯಲ್ಲಿ ಗುರುವಿನ ದೃಷ್ಟಿಯಿಂದ ವೃತ್ತಿ ಪ್ರಗತಿಗೆ ಒಳ್ಳೆಯ ಸಮಯ. ಬೆಳಿಗ್ಗೆ 9-11 ಗಂಟೆಯೊಳಗೆ ಪ್ರಮುಖ ನಿರ್ಧಾರಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳಿ."
            },
            "love_matters": {
                "ta": "காதல் & திருமண விஷயங்களுக்கு:",
                "en": "For love & marriage matters:",
                "kn": "ಪ್ರೀತಿ ಮತ್ತು ಮದುವೆ ವಿಷಯಗಳಿಗೆ:"
            },
            "love_insight": {
                "ta": "சுக்கிரன் நல்ல நிலையில் உள்ளார். காதல் உறவுகளுக்கு சாதகமான நேரம். மாலை நேரத்தில் முக்கிய உரையாடல்கள் சிறப்பாக அமையும்.",
                "en": "Venus is in good position. Favorable time for love relationships. Important conversations will go well in the evening.",
                "kn": "ಶುಕ್ರ ಒಳ್ಳೆಯ ಸ್ಥಿತಿಯಲ್ಲಿದೆ. ಪ್ರೀತಿ ಸಂಬಂಧಗಳಿಗೆ ಅನುಕೂಲಕರ ಸಮಯ. ಸಂಜೆ ಪ್ರಮುಖ ಸಂಭಾಷಣೆಗಳು ಚೆನ್ನಾಗಿ ನಡೆಯುತ್ತವೆ."
            },
            "set_right_time": {
                "ta": "சரியான நேரத்தை அமைக்கவும்",
                "en": "Set the right time",
                "kn": "ಸರಿಯಾದ ಸಮಯವನ್ನು ಹೊಂದಿಸಿ"
            },
            "mercury_strength": {
                "ta": "புதன் பலம்",
                "en": "Mercury strength",
                "kn": "ಬುಧ ಬಲ"
            },
            "tenth_house": {
                "ta": "10ம் வீடு",
                "en": "10th house",
                "kn": "10ನೇ ಮನೆ"
            },
            "jupiter_aspect": {
                "ta": "குரு பார்வை",
                "en": "Jupiter aspect",
                "kn": "ಗುರು ದೃಷ್ಟಿ"
            },
            "venus_strength": {
                "ta": "சுக்கிரன் பலம்",
                "en": "Venus strength",
                "kn": "ಶುಕ್ರ ಬಲ"
            },
            "seventh_house": {
                "ta": "7ம் வீடு",
                "en": "7th house",
                "kn": "7ನೇ ಮನೆ"
            },
            "moon": {
                "ta": "சந்திரன்",
                "en": "Moon",
                "kn": "ಚಂದ್ರ"
            },
            "today_horoscope": {
                "ta": "இன்றைய ராசிபலன்:",
                "en": "Today's horoscope:",
                "kn": "ಇಂದಿನ ರಾಶಿಫಲ:"
            },
            "your_horoscope": {
                "ta": "உங்கள் {rasi} இன்றைய ராசிபலன்:",
                "en": "Your {rasi} horoscope for today:",
                "kn": "ನಿಮ್ಮ {rasi} ಇಂದಿನ ರಾಶಿಫಲ:"
            },
            "career": {
                "ta": "தொழில்",
                "en": "Career",
                "kn": "ವೃತ್ತಿ"
            },
            "love": {
                "ta": "காதல்",
                "en": "Love",
                "kn": "ಪ್ರೀತಿ"
            },
            "health": {
                "ta": "ஆரோக்கியம்",
                "en": "Health",
                "kn": "ಆರೋಗ್ಯ"
            },
            "finance": {
                "ta": "நிதி",
                "en": "Finance",
                "kn": "ಹಣಕಾಸು"
            },
            "general_response": {
                "ta": "உங்கள் கேள்விக்கு பதில்:",
                "en": "Answer to your question:",
                "kn": "ನಿಮ್ಮ ಪ್ರಶ್ನೆಗೆ ಉತ್ತರ:"
            },
            "ask_about_time": {
                "ta": "இன்று நல்ல நேரம், ராசிபலன், தொழில் பலன் போன்றவை பற்றி கேளுங்கள்.",
                "en": "Ask about good time, horoscope, career predictions, etc.",
                "kn": "ಒಳ್ಳೆಯ ಸಮಯ, ರಾಶಿಫಲ, ವೃತ್ತಿ ಭವಿಷ್ಯ ಇತ್ಯಾದಿಗಳ ಬಗ್ಗೆ ಕೇಳಿ."
            },
            "total_score_today": {
                "ta": "இன்றைய மொத்த மதிப்பெண்: {score}%. நல்ல நேரம், ராகு காலம் பற்றி கேளுங்கள்.",
                "en": "Today's overall score: {score}%. Ask about good times, Rahu Kalam.",
                "kn": "ಇಂದಿನ ಒಟ್ಟು ಅಂಕ: {score}%. ಒಳ್ಳೆಯ ಸಮಯ, ರಾಹು ಕಾಲದ ಬಗ್ಗೆ ಕೇಳಿ."
            },
            "weekly_forecast_for": {
                "ta": "இந்த வாரம் உங்கள் பலன் ({rasi}):",
                "en": "This week's forecast ({rasi}):",
                "kn": "ಈ ವಾರದ ಭವಿಷ್ಯ ({rasi}):"
            },
            "view_full_forecast": {
                "ta": "முழு பலன் பார்க்க",
                "en": "View full forecast",
                "kn": "ಪೂರ್ಣ ಭವಿಷ್ಯ ನೋಡಿ"
            },
            "weekly_main_aspects": {
                "ta": "இந்த வாரத்தின் முக்கிய அம்சங்கள்:",
                "en": "Main aspects of this week:",
                "kn": "ಈ ವಾರದ ಪ್ರಮುಖ ಅಂಶಗಳು:"
            },
            "weekly_good": {
                "ta": "இந்த வாரம் பொதுவாக நல்ல வாரம். வியாழன் மற்றும் வெள்ளி சிறந்த நாட்கள்.",
                "en": "This week is generally good. Thursday and Friday are the best days.",
                "kn": "ಈ ವಾರ ಸಾಮಾನ್ಯವಾಗಿ ಒಳ್ಳೆಯದು. ಗುರುವಾರ ಮತ್ತು ಶುಕ್ರವಾರ ಅತ್ಯುತ್ತಮ ದಿನಗಳು."
            },
            "monthly_forecast_for": {
                "ta": "{month} மாத பலன் ({rasi}):",
                "en": "{month} monthly forecast ({rasi}):",
                "kn": "{month} ತಿಂಗಳ ಭವಿಷ್ಯ ({rasi}):"
            },
            "monthly_main_aspects": {
                "ta": "இந்த மாதத்தின் பலன்:",
                "en": "This month's forecast:",
                "kn": "ಈ ತಿಂಗಳ ಭವಿಷ್ಯ:"
            },
            "monthly_good": {
                "ta": "இந்த மாதம் பொதுவாக நல்ல மாதம். முதல் வாரம் சிறப்பாக இருக்கும்.",
                "en": "This month is generally good. The first week will be excellent.",
                "kn": "ಈ ತಿಂಗಳು ಸಾಮಾನ್ಯವಾಗಿ ಒಳ್ಳೆಯದು. ಮೊದಲ ವಾರ ಅತ್ಯುತ್ತಮವಾಗಿರುತ್ತದೆ."
            },
            "good_days": {
                "ta": "சிறந்த நாட்கள்",
                "en": "Best days",
                "kn": "ಅತ್ಯುತ್ತಮ ದಿನಗಳು"
            },
            "caution_needed": {
                "ta": "கவனம் தேவை",
                "en": "Caution needed",
                "kn": "ಎಚ್ಚರಿಕೆ ಅಗತ್ಯ"
            },
            "yearly_forecast_for": {
                "ta": "{year} வருட பலன் ({rasi}):",
                "en": "{year} yearly forecast ({rasi}):",
                "kn": "{year} ವಾರ್ಷಿಕ ಭವಿಷ್ಯ ({rasi}):"
            },
            "yearly_main_aspects": {
                "ta": "இந்த வருடத்தின் பலன்:",
                "en": "This year's forecast:",
                "kn": "ಈ ವರ್ಷದ ಭವಿಷ್ಯ:"
            },
            "yearly_good": {
                "ta": "இந்த வருடம் பொதுவாக நல்ல வருடம்.",
                "en": "This year is generally good.",
                "kn": "ಈ ವರ್ಷ ಸಾಮಾನ್ಯವಾಗಿ ಒಳ್ಳೆಯದು."
            },
            "best_months": {
                "ta": "சிறந்த மாதங்கள்",
                "en": "Best months",
                "kn": "ಅತ್ಯುತ್ತಮ ತಿಂಗಳುಗಳು"
            },
            "three_year_forecast_for": {
                "ta": "அடுத்த 3 வருட பலன் ({rasi}):",
                "en": "Next 3 years forecast ({rasi}):",
                "kn": "ಮುಂದಿನ 3 ವರ್ಷಗಳ ಭವಿಷ್ಯ ({rasi}):"
            },
            "three_year_insight": {
                "ta": "அடுத்த மூன்று வருடங்களின் மாதவாரி பலன் விவரங்கள். டாஷ்போர்டில் முழு விவரம் பார்க்கலாம்.",
                "en": "Monthly forecast details for the next three years. View full details in Dashboard.",
                "kn": "ಮುಂದಿನ ಮೂರು ವರ್ಷಗಳ ಮಾಸಿಕ ಭವಿಷ್ಯ ವಿವರಗಳು. ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ನಲ್ಲಿ ಪೂರ್ಣ ವಿವರಗಳನ್ನು ನೋಡಿ."
            },
            "three_year_fallback": {
                "ta": "அடுத்த 3 வருட பலன்:",
                "en": "Next 3 years forecast:",
                "kn": "ಮುಂದಿನ 3 ವರ್ಷಗಳ ಭವಿಷ್ಯ:"
            },
            "view_three_year_dashboard": {
                "ta": "டாஷ்போர்டில் 3 வருட பலன் பார்க்கலாம்.",
                "en": "View 3-year forecast in Dashboard.",
                "kn": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ನಲ್ಲಿ 3 ವರ್ಷಗಳ ಭವಿಷ್ಯ ನೋಡಿ."
            },
            "go_to_dashboard": {
                "ta": "டாஷ்போர்டு செல்ல",
                "en": "Go to Dashboard",
                "kn": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗೆ ಹೋಗಿ"
            },
            "muhurtham_find": {
                "ta": "முகூர்த்த நாள் கண்டுபிடிக்க:",
                "en": "Find auspicious date:",
                "kn": "ಶುಭ ದಿನಾಂಕ ಹುಡುಕಿ:"
            },
            "muhurtham_insight": {
                "ta": "திருமணம், கிரஹப்பிரவேசம், வாகனம் வாங்குதல் போன்ற காரியங்களுக்கு சரியான நாளை முகூர்த்தம் பக்கத்தில் கண்டுபிடிக்கலாம்.",
                "en": "Find the right date for marriage, housewarming, vehicle purchase, etc. in the Muhurtham page.",
                "kn": "ಮದುವೆ, ಗೃಹಪ್ರವೇಶ, ವಾಹನ ಖರೀದಿ ಮುಂತಾದವುಗಳಿಗೆ ಸರಿಯಾದ ದಿನಾಂಕವನ್ನು ಮುಹೂರ್ತ ಪುಟದಲ್ಲಿ ಹುಡುಕಿ."
            },
            "go_to_muhurtham": {
                "ta": "முகூர்த்தம் பக்கம் செல்ல",
                "en": "Go to Muhurtham page",
                "kn": "ಮುಹೂರ್ತ ಪುಟಕ್ಕೆ ಹೋಗಿ"
            },
            "yamagandam": {
                "ta": "யமகண்டம்",
                "en": "Yamagandam",
                "kn": "ಯಮಗಂಡ"
            },
            "kuligai": {
                "ta": "குளிகை",
                "en": "Kuligai",
                "kn": "ಕುಳಿಗೆ"
            }
        }
        text_dict = TEXTS.get(key, {})
        return text_dict.get(language, text_dict.get("ta", key))

    async def _generate_response(
        self,
        message: str,
        intent: str,
        entities: Dict,
        kb_context: str,
        user_context: Optional[Dict],
        language: str = "ta"
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
                        "label": self._get_text("best_time", language) if i == 0 else self._get_text("good_time", language)
                    })

                # Get auspicious times
                auspicious = panchang_data.get("auspicious", {})
                if auspicious.get("abhijit"):
                    slots.append({
                        "start": auspicious["abhijit"].get("start", "11:45"),
                        "end": auspicious["abhijit"].get("end", "12:30"),
                        "quality": 95,
                        "label": self._get_text("abhijit_muhurtham", language)
                    })

                # Get Rahu Kalam warning
                rahu = panchang_data.get("rahu_kalam", {}) or panchang_data.get("inauspicious", {}).get("rahu_kalam", {})
                if rahu:
                    warning = {
                        "start": rahu.get("start", "15:00"),
                        "end": rahu.get("end", "16:30"),
                        "label": self._get_text("rahu_kalam_avoid", language)
                    }

                # Get nakshatra - use name for English, tamil for Tamil
                nakshatra_data = panchang_data.get("nakshatra", {})
                nakshatra = nakshatra_data.get("name" if language == "en" else "tamil", nakshatra_data.get("name", ""))
                tithi_data = panchang_data.get("tithi", {})
                tithi = tithi_data.get("name" if language == "en" else "tamil", tithi_data.get("name", ""))
                insight = self._get_text("today_nakshatra_tithi", language).format(nakshatra=nakshatra, tithi=tithi)

                score = panchang_data.get("overall_score", 70)
                if score >= 75:
                    insight += self._get_text("very_auspicious_day", language)
                elif score >= 60:
                    insight += self._get_text("good_day", language)
                else:
                    insight += self._get_text("normal_day", language)
            else:
                # Fallback if panchangam not available
                slots = [
                    {"start": "09:00", "end": "10:30", "quality": 92, "label": self._get_text("best_time", language)},
                    {"start": "14:00", "end": "15:30", "quality": 78, "label": self._get_text("good_time", language)}
                ]
                warning = {"start": "15:00", "end": "16:30", "label": self._get_text("rahu_kalam_avoid", language)}
                insight = self._get_text("morning_special", language)

            return {
                "message": self._get_text("best_times_today", language),
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
                "message": self._get_text("inauspicious_times", language),
                "data": {
                    "type": "time_slots",
                    "slots": [],
                    "warning": {
                        "start": rahu.get("start", "15:00"),
                        "end": rahu.get("end", "16:30"),
                        "label": self._get_text("rahu_kalam", language)
                    }
                },
                "insight": f"{self._get_text('rahu_kalam', language)}: {rahu.get('start', '-')} - {rahu.get('end', '-')}\nYamagandam: {yama.get('start', '-')} - {yama.get('end', '-')}\nKuligai: {kuligai.get('start', '-')} - {kuligai.get('end', '-')}",
                "action": None
            }

        elif intent == "career":
            score = 85
            if panchang_data:
                score = min(95, int(panchang_data.get("overall_score", 70) + 15))

            return {
                "message": self._get_text("career_good_day", language),
                "data": {
                    "type": "recommendation",
                    "score": score,
                    "factors": [
                        {"name": self._get_text("mercury_strength", language), "value": 88, "positive": True},
                        {"name": self._get_text("tenth_house", language), "value": 75, "positive": True},
                        {"name": self._get_text("jupiter_aspect", language), "value": 92, "positive": True}
                    ]
                },
                "insight": self._get_text("career_insight", language),
                "action": {
                    "type": "muhurtham",
                    "text": self._get_text("set_right_time", language)
                }
            }

        elif intent == "love":
            return {
                "message": self._get_text("love_matters", language),
                "data": {
                    "type": "recommendation",
                    "score": 72,
                    "factors": [
                        {"name": self._get_text("venus_strength", language), "value": 78, "positive": True},
                        {"name": self._get_text("seventh_house", language), "value": 70, "positive": True},
                        {"name": self._get_text("moon", language), "value": 68, "positive": True}
                    ]
                },
                "insight": self._get_text("love_insight", language),
                "action": None
            }

        elif intent == "rasipalan":
            user_rasi = user_context.get("rasi", "") if user_context else ""
            score = int(panchang_data.get("overall_score", 72)) if panchang_data else 72

            # Generate horoscope message based on language
            if user_rasi:
                message = self._get_text("your_horoscope", language).format(rasi=user_rasi)
            else:
                message = self._get_text("today_horoscope", language)

            return {
                "message": message,
                "data": {
                    "type": "horoscope",
                    "overall_score": score,
                    "areas": {
                        self._get_text("career", language): min(100, score + 8),
                        self._get_text("love", language): max(50, score - 7),
                        self._get_text("health", language): min(100, score + 3),
                        self._get_text("finance", language): max(50, score - 4)
                    }
                },
                "insight": None,
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
                    "message": self._get_text("weekly_forecast_for", language).format(rasi=user_rasi),
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
                        "text": self._get_text("view_full_forecast", language),
                        "path": "/"
                    }
                }
            except Exception as e:
                print(f"Weekly forecast error: {e}")
                return {
                    "message": self._get_text("weekly_main_aspects", language),
                    "data": {
                        "type": "recommendation",
                        "score": 75,
                        "factors": [
                            {"name": self._get_text("career", language), "value": 80, "positive": True},
                            {"name": self._get_text("health", language), "value": 75, "positive": True},
                            {"name": self._get_text("finance", language), "value": 70, "positive": True}
                        ]
                    },
                    "insight": self._get_text("weekly_good", language),
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
                    "message": self._get_text("monthly_forecast_for", language).format(month=monthly['month_name'], rasi=user_rasi),
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
                        "text": self._get_text("view_full_forecast", language),
                        "path": "/"
                    }
                }
            except Exception as e:
                print(f"Monthly forecast error: {e}")
                return {
                    "message": self._get_text("monthly_main_aspects", language),
                    "data": {
                        "type": "recommendation",
                        "score": 72,
                        "factors": [
                            {"name": self._get_text("good_days", language), "value": 10, "positive": True},
                            {"name": self._get_text("caution_needed", language), "value": 5, "positive": False}
                        ]
                    },
                    "insight": self._get_text("monthly_good", language),
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
                    "message": self._get_text("yearly_forecast_for", language).format(year=yearly['year'], rasi=user_rasi),
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
                        "text": self._get_text("view_full_forecast", language),
                        "path": "/"
                    }
                }
            except Exception as e:
                print(f"Yearly forecast error: {e}")
                return {
                    "message": self._get_text("yearly_main_aspects", language),
                    "data": {
                        "type": "recommendation",
                        "score": 70,
                        "factors": [
                            {"name": self._get_text("best_months", language), "value": 4, "positive": True},
                            {"name": self._get_text("caution_needed", language), "value": 2, "positive": False}
                        ]
                    },
                    "insight": self._get_text("yearly_good", language),
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
                    "message": self._get_text("three_year_forecast_for", language).format(rasi=user_rasi),
                    "data": {
                        "type": "three_year_forecast",
                        "years": three_years
                    },
                    "insight": self._get_text("three_year_insight", language),
                    "action": {
                        "type": "navigate",
                        "text": self._get_text("view_full_forecast", language),
                        "path": "/"
                    }
                }
            except Exception as e:
                print(f"Three year forecast error: {e}")
                return {
                    "message": self._get_text("three_year_fallback", language),
                    "data": None,
                    "insight": self._get_text("view_three_year_dashboard", language),
                    "action": {
                        "type": "navigate",
                        "text": self._get_text("go_to_dashboard", language),
                        "path": "/"
                    }
                }

        elif intent == "muhurtham":
            return {
                "message": self._get_text("muhurtham_find", language),
                "data": None,
                "insight": self._get_text("muhurtham_insight", language),
                "action": {
                    "type": "navigate",
                    "text": self._get_text("go_to_muhurtham", language),
                    "path": "/muhurtham"
                }
            }

        else:
            # General response with today's summary
            if panchang_data:
                nakshatra_data = panchang_data.get("nakshatra", {})
                nakshatra = nakshatra_data.get("name" if language == "en" else "tamil", nakshatra_data.get("name", ""))
                tithi_data = panchang_data.get("tithi", {})
                tithi = tithi_data.get("name" if language == "en" else "tamil", tithi_data.get("name", ""))
                vaaram = panchang_data.get("vaaram", "")
                score = panchang_data.get("overall_score", 70)

                msg_template = self._get_text("today_nakshatra_tithi", language)
                return {
                    "message": msg_template.format(nakshatra=nakshatra, tithi=tithi),
                    "data": {
                        "type": "recommendation",
                        "score": int(score),
                        "factors": []
                    },
                    "insight": self._get_text("total_score_today", language).format(score=int(score)),
                    "action": None
                }

            return {
                "message": self._get_text("general_response", language),
                "data": None,
                "insight": self._get_text("ask_about_time", language),
                "action": None
            }
    
    def get_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get conversation history for a user"""
        history = self.conversation_history.get(user_id, [])
        return history[-limit:]
