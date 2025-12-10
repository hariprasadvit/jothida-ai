"""
Jathagam (Birth Chart) API Router
"""

from fastapi import APIRouter, Request
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class BirthDetails(BaseModel):
    name: str
    date: str  # YYYY-MM-DD
    time: str  # HH:MM
    place: str
    latitude: float
    longitude: float
    timezone: str = "Asia/Kolkata"

class PlanetPosition(BaseModel):
    planet: str
    tamil_name: str
    symbol: str
    rasi: str
    rasi_tamil: str
    degree: float
    nakshatra: str
    nakshatra_pada: int
    is_retrograde: bool
    strength: float  # 0-100 for visual display
    trend: str  # up, down, neutral

class MoonSign(BaseModel):
    rasi: str
    rasi_tamil: str
    nakshatra: str
    nakshatra_pada: int

class JathagamResponse(BaseModel):
    name: str
    birth_details: dict
    planets: list[PlanetPosition]
    lagna: dict
    moon_sign: MoonSign  # User's rasi based on moon position
    rasi_chart: list[list[str]]  # 12 houses with planets
    navamsa_chart: list[list[str]]
    dasha: dict
    overall_strength: float
    yogas: list[dict]

@router.post("/generate", response_model=JathagamResponse)
async def generate_jathagam(request: Request, birth: BirthDetails):
    """Generate full birth chart (Jathagam)"""
    from app.services.jathagam_generator import JathagamGenerator
    
    generator = JathagamGenerator(request.app.state.ephemeris)
    return generator.generate(birth)

@router.get("/planets-portfolio")
async def get_planets_portfolio(request: Request, user_id: str):
    """
    Get user's planets as a stock portfolio view
    Returns strength changes compared to yesterday (like stock gains/losses)
    """
    from app.services.jathagam_generator import JathagamGenerator
    
    generator = JathagamGenerator(request.app.state.ephemeris)
    return generator.get_portfolio_view(user_id)

@router.get("/dasha-timeline/{user_id}")
async def get_dasha_timeline(request: Request, user_id: str):
    """Get Vimshottari Dasha timeline for visualization"""
    from app.services.jathagam_generator import JathagamGenerator
    
    generator = JathagamGenerator(request.app.state.ephemeris)
    return generator.get_dasha_timeline(user_id)

@router.get("/life-areas/{user_id}")
async def get_life_areas(request: Request, user_id: str):
    """
    Get life area scores (Love, Career, Health, Family)
    Based on current transits over birth chart
    """
    from app.services.jathagam_generator import JathagamGenerator
    
    generator = JathagamGenerator(request.app.state.ephemeris)
    return generator.get_life_areas(user_id)
