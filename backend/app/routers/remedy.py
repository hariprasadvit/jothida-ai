"""
AI Remedy Engine Router
Provides personalized astrological remedies based on:
- Current dasha period
- Planet strengths
- Dosha impact
- User goals (love/job/wealth/peace)
"""

from fastapi import APIRouter, Request, Query
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

router = APIRouter()


class UserGoal(str, Enum):
    LOVE = "love"
    JOB = "job"
    WEALTH = "wealth"
    PEACE = "peace"
    HEALTH = "health"
    EDUCATION = "education"


class RemedyRequest(BaseModel):
    name: str
    birth_date: str  # YYYY-MM-DD
    birth_time: str  # HH:MM
    birth_place: str
    latitude: Optional[float] = 13.0827
    longitude: Optional[float] = 80.2707
    goal: Optional[UserGoal] = None


class RemedyItem(BaseModel):
    id: str
    type: str  # mantra, gemstone, donation, worship, fasting, color, direction
    title: str
    title_tamil: str
    description: str
    description_tamil: str
    planet: str
    planet_tamil: str
    priority: int  # 1-5, 1 being highest
    effectiveness: int  # 1-100
    timing: Optional[str] = None
    duration: Optional[str] = None


class RemedyResponse(BaseModel):
    user_name: str
    current_dasha: dict
    weak_planets: List[dict]
    doshas: List[dict]
    goal_analysis: Optional[dict]
    remedies: List[dict]
    daily_routine: dict
    lucky_items: dict


@router.post("/personalized", response_model=RemedyResponse)
async def get_personalized_remedies(request: Request, data: RemedyRequest):
    """
    Get AI-powered personalized remedies based on:
    1. Current Maha Dasha and Antar Dasha
    2. Weak planets in the birth chart
    3. Doshas (Mangal Dosha, Kaal Sarp, etc.)
    4. User's specific goal
    """
    from app.services.remedy_engine import RemedyEngine
    from app.services.jathagam_generator import JathagamGenerator

    # Get ephemeris from app state
    ephemeris = getattr(request.app.state, 'ephemeris', None)

    # Initialize services
    jathagam_gen = JathagamGenerator(ephemeris)
    remedy_engine = RemedyEngine(jathagam_gen)

    return remedy_engine.get_personalized_remedies(data)


@router.get("/for-planet/{planet}")
async def get_planet_remedies(
    request: Request,
    planet: str,
    language: str = Query("ta", description="Language: ta, en, kn")
):
    """Get remedies for a specific planet"""
    from app.services.remedy_engine import RemedyEngine

    remedy_engine = RemedyEngine(None)
    return remedy_engine.get_planet_remedies(planet, language)


@router.get("/for-dosha/{dosha}")
async def get_dosha_remedies(
    request: Request,
    dosha: str,
    language: str = Query("ta", description="Language: ta, en, kn")
):
    """Get remedies for a specific dosha"""
    from app.services.remedy_engine import RemedyEngine

    remedy_engine = RemedyEngine(None)
    return remedy_engine.get_dosha_remedies(dosha, language)


@router.get("/daily")
async def get_daily_remedies(
    request: Request,
    rasi: str = Query(..., description="User's rasi"),
    nakshatra: str = Query(..., description="User's nakshatra"),
    language: str = Query("ta", description="Language: ta, en, kn")
):
    """Get simple daily remedies based on rasi and today's panchangam"""
    from app.services.remedy_engine import RemedyEngine
    from app.services.panchangam_calculator import PanchangamCalculator

    ephemeris = getattr(request.app.state, 'ephemeris', None)
    panchangam = PanchangamCalculator(ephemeris) if ephemeris else None

    remedy_engine = RemedyEngine(None, panchangam)
    return remedy_engine.get_daily_remedies(rasi, nakshatra, language)


@router.get("/goal/{goal}")
async def get_goal_remedies(
    request: Request,
    goal: UserGoal,
    rasi: str = Query(..., description="User's rasi"),
    language: str = Query("ta", description="Language: ta, en, kn")
):
    """Get remedies for achieving a specific goal"""
    from app.services.remedy_engine import RemedyEngine

    remedy_engine = RemedyEngine(None)
    return remedy_engine.get_goal_remedies(goal.value, rasi, language)
