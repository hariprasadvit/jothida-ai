"""
Muhurtham (Auspicious Time) Finder API Router
"""

from fastapi import APIRouter, Request, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

router = APIRouter()

class MuhurthamSlot(BaseModel):
    date: str
    start_time: str
    end_time: str
    quality_score: float  # 0-100
    quality_label: str  # Excellent, Good, Average
    factors: List[dict]  # Contributing factors
    conflicts: List[str]  # Any warnings (Rahu kalam overlap etc)

class EventType(BaseModel):
    id: str
    name_tamil: str
    name_english: str
    icon: str
    description: str

class EventScore(BaseModel):
    type: str
    tamil: str
    score: float

class CalendarDay(BaseModel):
    date: str
    day_score: float  # For heat map coloring
    is_auspicious: bool
    has_muhurtham: bool
    event_scores: Optional[dict] = None  # Scores for each event type
    good_for_events: Optional[List[EventScore]] = None  # Events this day is good for
    festivals: List[str]
    warnings: List[str]

@router.get("/event-types")
async def get_event_types() -> List[EventType]:
    """Get list of supported event types for muhurtham"""
    return [
        EventType(id="marriage", name_tamil="திருமணம்", name_english="Marriage", icon="💒", description=""),
        EventType(id="griha_pravesam", name_tamil="கிரஹ பிரவேசம்", name_english="House Warming", icon="🏠", description=""),
        EventType(id="vehicle", name_tamil="வாகனம் வாங்குதல்", name_english="Vehicle Purchase", icon="🚗", description=""),
        EventType(id="business", name_tamil="தொழில் தொடக்கம்", name_english="Business Start", icon="💼", description=""),
        EventType(id="education", name_tamil="கல்வி தொடக்கம்", name_english="Education Start", icon="📚", description=""),
        EventType(id="travel", name_tamil="பயணம்", name_english="Travel", icon="✈️", description=""),
        EventType(id="medical", name_tamil="சிகிச்சை", name_english="Medical Procedure", icon="🏥", description=""),
        EventType(id="naming", name_tamil="நாமகரணம்", name_english="Naming Ceremony", icon="👶", description=""),
        EventType(id="jewelry", name_tamil="நகை வாங்குதல்", name_english="Jewelry Purchase", icon="💎", description=""),
        EventType(id="general", name_tamil="பொது", name_english="General Auspicious", icon="⭐", description=""),
    ]

@router.get("/find")
async def find_muhurtham(
    request: Request,
    event_type: str,
    start_date: date,
    end_date: date,
    lat: float = Query(default=13.0827),
    lon: float = Query(default=80.2707),
    user_nakshatra: Optional[str] = None
) -> List[MuhurthamSlot]:
    """
    Find auspicious times for an event within date range
    Returns slots sorted by quality score
    """
    from app.services.muhurtham_finder import MuhurthamFinder
    
    finder = MuhurthamFinder(request.app.state.ephemeris)
    return finder.find_slots(
        event_type=event_type,
        start_date=start_date,
        end_date=end_date,
        lat=lat,
        lon=lon,
        user_nakshatra=user_nakshatra
    )

@router.get("/calendar")
async def get_calendar_view(
    request: Request,
    month: int,
    year: int,
    lat: float = Query(default=13.0827),
    lon: float = Query(default=80.2707),
    lang: str = Query(default="ta", description="Language: ta, en, kn")
) -> List[CalendarDay]:
    """
    Get calendar heat map data for a month
    Each day has a score for coloring (green/yellow/red)
    """
    from app.services.muhurtham_finder import MuhurthamFinder
    import calendar as cal

    try:
        finder = MuhurthamFinder(request.app.state.ephemeris, lang=lang)
        return finder.get_month_calendar(month, year, lat, lon, lang=lang)
    except Exception as e:
        print(f"Error in get_calendar_view: {e}")
        # Return basic calendar data with neutral scores as fallback
        num_days = cal.monthrange(year, month)[1]
        return [
            CalendarDay(
                date=f"{year}-{month:02d}-{day:02d}",
                day_score=50.0,
                is_auspicious=False,
                has_muhurtham=False,
                event_scores={"general": 50.0, "marriage": 50.0, "griha_pravesam": 50.0, "vehicle": 50.0, "business": 50.0, "travel": 50.0},
                good_for_events=[],
                festivals=[],
                warnings=[]
            )
            for day in range(1, num_days + 1)
        ]

@router.get("/best-time-today")
async def get_best_time_today(
    request: Request,
    event_type: str = "general",
    lat: float = Query(default=13.0827),
    lon: float = Query(default=80.2707)
) -> MuhurthamSlot:
    """Quick endpoint: Get the best time slot for today"""
    from app.services.muhurtham_finder import MuhurthamFinder

    finder = MuhurthamFinder(request.app.state.ephemeris)
    slots = finder.find_slots(
        event_type=event_type,
        start_date=date.today(),
        end_date=date.today(),
        lat=lat,
        lon=lon
    )
    return slots[0] if slots else None

@router.get("/day-details/{target_date}")
async def get_day_details(
    request: Request,
    target_date: date,
    lat: float = Query(default=13.0827),
    lon: float = Query(default=80.2707),
    lang: str = Query(default="ta", description="Language: ta, en, kn")
):
    """
    Get detailed muhurtham info for a specific day
    Used when user selects a date in calendar
    """
    from app.services.muhurtham_finder import MuhurthamFinder

    try:
        finder = MuhurthamFinder(request.app.state.ephemeris, lang=lang)
        return finder.get_day_details(target_date, lat, lon, lang=lang)
    except Exception as e:
        print(f"Error in get_day_details: {e}")
        # Return basic fallback data
        return {
            "date": target_date.isoformat(),
            "day_score": 50.0,
            "event_scores": {"general": 50.0},
            "good_for_events": [],
            "panchangam": {
                "tithi": {"name": "-", "paksha": "", "number": 0},
                "nakshatra": {"name": "-", "pada": 0, "lord": ""},
                "yoga": {"name": "-"},
                "vaaram": "-"
            },
            "time_slots": [],
            "recommendation": "Unable to calculate muhurtham data for this day."
        }
