"""
Ungal Jothidan (Your Astrologer) - Daily Intelligence Dashboard API
"""

from fastapi import APIRouter, Request, HTTPException
from datetime import date
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class DailyInsightsRequest(BaseModel):
    user_id: str
    name: Optional[str] = ""
    birth_date: str  # YYYY-MM-DD
    birth_time: Optional[str] = "06:00"
    birth_place: Optional[str] = "Chennai"
    rasi: str
    nakshatra: str
    language: Optional[str] = "ta"  # ta, en, kn
    target_date: Optional[str] = None  # YYYY-MM-DD, defaults to today


class CardResponse(BaseModel):
    id: str
    title: str
    icon: str
    color: str
    score: int  # 0-100
    confidence: int  # 0-100
    text: str
    reasons: list


class DailyInsightsResponse(BaseModel):
    user_id: str
    date: str
    overall_confidence: int
    summary: str
    profile: dict
    cards: list[CardResponse]


@router.post("/daily-insights", response_model=DailyInsightsResponse)
async def get_daily_insights(request: Request, data: DailyInsightsRequest):
    """
    Generate personalized daily insights for a user.

    Returns 12 insight cards with scores and confidence ratings:
    - Dasha Mood
    - Transit Pressure
    - Finance Outlook
    - Work / Career
    - Relationship Energy
    - Health Vibration
    - Lucky Window
    - Avoid Window
    - Opportunity Indicator
    - Risk Alert
    - Color / Direction
    - Personal Note
    """
    from app.services.ungal_jothidan_service import UngalJothidanService

    service = UngalJothidanService(request.app.state.ephemeris)

    # Parse target date
    target_date_obj = None
    if data.target_date:
        try:
            target_date_obj = date.fromisoformat(data.target_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid target_date format. Use YYYY-MM-DD.")

    # Prepare user data
    user_data = {
        "id": data.user_id,
        "name": data.name,
        "birth_date": data.birth_date,
        "birth_time": data.birth_time,
        "birth_place": data.birth_place,
        "rasi": data.rasi,
        "nakshatra": data.nakshatra
    }

    # Generate insights
    result = service.generate_daily_insights(
        user_data=user_data,
        target_date=target_date_obj,
        language=data.language
    )

    return result


@router.get("/daily-insights/{user_id}")
async def get_daily_insights_by_user(
    request: Request,
    user_id: str,
    language: str = "ta",
    target_date: Optional[str] = None
):
    """
    Get daily insights for a user by their ID (fetches profile from database).
    """
    from app.services.ungal_jothidan_service import UngalJothidanService
    from app.database import get_db_connection

    service = UngalJothidanService(request.app.state.ephemeris)

    # Parse target date
    target_date_obj = None
    if target_date:
        try:
            target_date_obj = date.fromisoformat(target_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid target_date format. Use YYYY-MM-DD.")

    # Fetch user profile from database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, name, birth_date, birth_time, birth_place, rasi, nakshatra
            FROM users WHERE id = ?
            """,
            (user_id,)
        )
        row = cursor.fetchone()
        conn.close()

        if not row:
            raise HTTPException(status_code=404, detail="User not found")

        user_data = {
            "id": row[0],
            "name": row[1],
            "birth_date": row[2],
            "birth_time": row[3] or "06:00",
            "birth_place": row[4] or "Chennai",
            "rasi": row[5] or "மேஷம்",
            "nakshatra": row[6] or "அஸ்வினி"
        }
    except HTTPException:
        raise
    except Exception as e:
        # If database is not available, return demo data
        user_data = {
            "id": user_id,
            "name": "Demo User",
            "birth_date": "1990-01-15",
            "birth_time": "06:00",
            "birth_place": "Chennai",
            "rasi": "மேஷம்",
            "nakshatra": "அஸ்வினி"
        }

    # Generate insights
    result = service.generate_daily_insights(
        user_data=user_data,
        target_date=target_date_obj,
        language=language
    )

    return result


@router.get("/card-details/{card_id}")
async def get_card_details(
    request: Request,
    card_id: str,
    user_id: str,
    language: str = "ta"
):
    """
    Get detailed explanation for a specific card.
    Returns expanded reasoning and recommendations.
    """
    from app.services.ungal_jothidan_service import CARD_DEFINITIONS

    if card_id not in CARD_DEFINITIONS:
        raise HTTPException(status_code=404, detail="Card not found")

    card_def = CARD_DEFINITIONS[card_id]

    # Get title based on language
    title_key = f"title_{language}"
    title = card_def.get(title_key, card_def.get("title_en", card_id))

    # Detailed explanations by card type
    explanations = {
        "dasha_mood": {
            "ta": "தசா காலம் உங்கள் வாழ்க்கையின் முக்கிய கட்டங்களை குறிக்கிறது. தற்போதைய தசா நாதனின் பலம் மற்றும் கிரக தொடர்புகள் உங்கள் அன்றாட மனநிலையை பாதிக்கும்.",
            "en": "The Dasha period represents major phases in your life. The strength of your current Dasha lord and planetary aspects influence your daily mood.",
            "kn": "ದಶಾ ಅವಧಿ ನಿಮ್ಮ ಜೀವನದ ಪ್ರಮುಖ ಹಂತಗಳನ್ನು ಪ್ರತಿನಿಧಿಸುತ್ತದೆ."
        },
        "transit_pressure": {
            "ta": "கோள்களின் தற்போதைய நிலை உங்கள் ஜாதகத்துடன் எவ்வாறு தொடர்பு கொள்கிறது என்பதை அடிப்படையாகக் கொண்டது.",
            "en": "Based on how current planetary positions interact with your birth chart.",
            "kn": "ಪ್ರಸ್ತುತ ಗ್ರಹ ಸ್ಥಾನಗಳು ನಿಮ್ಮ ಜನ್ಮ ಕುಂಡಲಿಯೊಂದಿಗೆ ಹೇಗೆ ಸಂವಹನ ನಡೆಸುತ್ತವೆ ಎಂಬುದರ ಆಧಾರದ ಮೇಲೆ."
        },
        "finance_outlook": {
            "ta": "2ம் மற்றும் 11ம் வீடுகளின் பலம், குரு-சுக்கிரன் நிலை, மற்றும் தற்போதைய கிரக மாற்றங்கள் அடிப்படையில்.",
            "en": "Based on 2nd and 11th house strengths, Jupiter-Venus positions, and current transits.",
            "kn": "2ನೇ ಮತ್ತು 11ನೇ ಮನೆಗಳ ಶಕ್ತಿ, ಗುರು-ಶುಕ್ರ ಸ್ಥಾನಗಳ ಆಧಾರದ ಮೇಲೆ."
        },
        "work_career": {
            "ta": "10ம் வீடு, 6ம் வீடு நிலைகள் மற்றும் சூரியன்-புதன் பலம் அடிப்படையில்.",
            "en": "Based on 10th house, 6th house positions, and Sun-Mercury strength.",
            "kn": "10ನೇ ಮನೆ, 6ನೇ ಮನೆ ಸ್ಥಾನಗಳ ಮತ್ತು ಸೂರ್ಯ-ಬುಧ ಶಕ್ತಿಯ ಆಧಾರದ ಮೇಲೆ."
        },
        "relationship_energy": {
            "ta": "7ம் வீடு, 5ம் வீடு, சுக்கிரன்-சந்திரன் நிலைகள் அடிப்படையில்.",
            "en": "Based on 7th house, 5th house, and Venus-Moon positions.",
            "kn": "7ನೇ ಮನೆ, 5ನೇ ಮನೆ, ಮತ್ತು ಶುಕ್ರ-ಚಂದ್ರ ಸ್ಥಾನಗಳ ಆಧಾರದ ಮೇಲೆ."
        },
        "health_vibration": {
            "ta": "லக்னம், 6ம் வீடு, சந்திரன் நிலை, மற்றும் பாபகிரக தாக்கம் அடிப்படையில்.",
            "en": "Based on Ascendant, 6th house, Moon position, and malefic influences.",
            "kn": "ಲಗ್ನ, 6ನೇ ಮನೆ, ಚಂದ್ರ ಸ್ಥಾನ ಮತ್ತು ಪಾಪಗ್ರಹ ಪ್ರಭಾವದ ಆಧಾರದ ಮೇಲೆ."
        },
        "lucky_window": {
            "ta": "உங்கள் நட்சத்திர அதிபதி, வாரத்தின் நாள், மற்றும் சுபகிரக நேரங்கள் அடிப்படையில்.",
            "en": "Based on your Nakshatra lord, day of week, and benefic planetary hours.",
            "kn": "ನಿಮ್ಮ ನಕ್ಷತ್ರ ಅಧಿಪತಿ, ವಾರದ ದಿನ ಮತ್ತು ಶುಭ ಗ್ರಹ ಸಮಯಗಳ ಆಧಾರದ ಮೇಲೆ."
        },
        "avoid_window": {
            "ta": "ராகு காலம், எமகண்டம், மற்றும் பஞ்சாங்க தோஷங்கள் அடிப்படையில்.",
            "en": "Based on Rahu Kalam, Yamaganda, and Panchang doshas.",
            "kn": "ರಾಹು ಕಾಲ, ಯಮಗಂಡ ಮತ್ತು ಪಂಚಾಂಗ ದೋಷಗಳ ಆಧಾರದ ಮೇಲೆ."
        },
        "opportunity_indicator": {
            "ta": "உங்கள் சிறந்த வாழ்க்கை துறை மதிப்பெண்கள் மற்றும் சுப நட்சத்திர நிலை அடிப்படையில்.",
            "en": "Based on your best performing life area scores and benefic nakshatra positions.",
            "kn": "ನಿಮ್ಮ ಅತ್ಯುತ್ತಮ ಜೀವನ ಕ್ಷೇತ್ರ ಅಂಕಗಳ ಆಧಾரದ ಮೇಲೆ."
        },
        "risk_indicator": {
            "ta": "பாபகிரக தாக்கம் மற்றும் பஞ்சாங்க தோஷங்கள் அடிப்படையில்.",
            "en": "Based on malefic influences and Panchang doshas.",
            "kn": "ಪಾಪಗ್ರಹ ಪ್ರಭಾವ ಮತ್ತು ಪಂಚಾಂಗ ದೋಷಗಳ ಆಧಾರದ ಮೇಲೆ."
        },
        "color_direction": {
            "ta": "உங்கள் நட்சத்திர அதிபதி மற்றும் வாரத்தின் நாள் அதிபதி அடிப்படையில்.",
            "en": "Based on your Nakshatra lord and day lord.",
            "kn": "ನಿಮ್ಮ ನಕ್ಷತ್ರ ಅಧಿಪತಿ ಮತ್ತು ದಿನದ ಅಧಿಪತಿಯ ಆಧಾರದ ಮೇಲೆ."
        },
        "personal_note": {
            "ta": "அனைத்து குறிகாட்டிகளின் ஒட்டுமொத்த சுருக்கம்.",
            "en": "Overall summary of all indicators.",
            "kn": "ಎಲ್ಲಾ ಸೂಚಕಗಳ ಒಟ್ಟಾರೆ ಸಾರಾಂಶ."
        }
    }

    explanation = explanations.get(card_id, {}).get(language, explanations.get(card_id, {}).get("en", ""))

    return {
        "id": card_id,
        "title": title,
        "icon": card_def["icon"],
        "color": card_def["color"],
        "signals": card_def["signals"],
        "weights": card_def["weights"],
        "explanation": explanation
    }
