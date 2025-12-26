"""
Thirumana Porutham (Marriage Matching) API Router
"""

from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class PersonDetails(BaseModel):
    name: str
    date: str  # YYYY-MM-DD
    time: str  # HH:MM
    place: str
    latitude: float
    longitude: float
    gender: str  # male/female

class MatchingRequest(BaseModel):
    bride: PersonDetails
    groom: PersonDetails

class PoruttamScore(BaseModel):
    name: str
    tamil_name: str
    english_name: str
    score: float  # 0-100
    max_score: float
    status: str  # excellent, good, warning, critical
    description: str
    ai_insight: Optional[str] = None

class DoshaStatus(BaseModel):
    name: str
    tamil_name: str
    bride_has: bool
    groom_has: bool
    is_compatible: bool
    remedy: Optional[str] = None

class MatchingResponse(BaseModel):
    overall_score: float
    overall_status: str
    ai_verdict: dict  # Contains verdict, verdict_en, explanation, explanation_en, recommendation
    poruthams: list  # Porutham details
    doshas: list  # Dosha details
    compatibility_radar: dict  # For radar chart
    future_timeline: list[dict]  # Predicted events
    recommendations: list[str]
    bride_details: dict
    groom_details: dict

@router.post("/check", response_model=MatchingResponse)
async def check_matching(request: Request, data: MatchingRequest):
    """
    Full marriage compatibility check with 10-14 poruthams
    Returns visual-ready data with scores and insights
    """
    from app.services.matching_calculator import MatchingCalculator
    
    calculator = MatchingCalculator(request.app.state.ephemeris)
    return calculator.calculate_full_matching(data.bride, data.groom)

@router.post("/quick-check")
async def quick_matching(
    bride_nakshatra: str,
    bride_rasi: str,
    groom_nakshatra: str,
    groom_rasi: str
):
    """
    Quick matching by just nakshatra and rasi
    For initial screening without full birth details
    """
    from app.services.matching_calculator import MatchingCalculator
    
    calculator = MatchingCalculator(None)
    return calculator.quick_check(
        bride_nakshatra, bride_rasi,
        groom_nakshatra, groom_rasi
    )

@router.get("/porutham-details/{porutham_name}")
async def get_porutham_details(porutham_name: str):
    """Get detailed explanation of a specific porutham"""
    from app.services.matching_calculator import MatchingCalculator
    
    return MatchingCalculator.get_porutham_info(porutham_name)
