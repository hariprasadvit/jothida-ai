"""
Panchangam API Router
Daily Tamil calendar calculations
"""

from fastapi import APIRouter, Query, Request
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel

from app.services.ephemeris import EphemerisService
from app.services.panchangam_calculator import PanchangamCalculator

router = APIRouter()

class PanchangamResponse(BaseModel):
    date: str
    tamil_date: str
    tamil_month: str
    tamil_year: str
    vaaram: str  # Day of week in Tamil
    tithi: dict
    nakshatra: dict
    yoga: dict
    karana: dict
    # New structured fields
    sun_times: dict
    moon_times: dict
    inauspicious: dict
    auspicious: dict
    # Legacy flat fields (for backwards compatibility)
    sunrise: str
    sunset: str
    rahu_kalam: dict
    yamagandam: dict
    kuligai: dict
    nalla_neram: list
    overall_score: float  # 0-100 score for the day

class TimeEnergyResponse(BaseModel):
    time: str
    energy_score: float
    is_rahu_kalam: bool
    is_nalla_neram: bool
    recommendation: str

class ScoreFactor(BaseModel):
    name: str
    tamil_name: str
    value: str
    points: int
    max_points: int
    description: str

class ScoreBreakdownResponse(BaseModel):
    total_score: int
    score_label: str
    base_score: int
    factors: list[ScoreFactor]
    calculated_at: str

@router.get("/today", response_model=PanchangamResponse)
async def get_today_panchangam(
    request: Request,
    lat: float = Query(default=13.0827, description="Latitude"),
    lon: float = Query(default=80.2707, description="Longitude"),
    timezone: str = Query(default="Asia/Kolkata", description="Timezone")
):
    """Get today's panchangam"""
    calculator = PanchangamCalculator(request.app.state.ephemeris)
    return calculator.calculate(date.today(), lat, lon, timezone)

@router.get("/date/{target_date}", response_model=PanchangamResponse)
async def get_panchangam_by_date(
    request: Request,
    target_date: date,
    lat: float = Query(default=13.0827),
    lon: float = Query(default=80.2707),
    timezone: str = Query(default="Asia/Kolkata")
):
    """Get panchangam for a specific date"""
    calculator = PanchangamCalculator(request.app.state.ephemeris)
    return calculator.calculate(target_date, lat, lon, timezone)

@router.get("/time-energy")
async def get_time_energy(
    request: Request,
    target_date: Optional[date] = None,
    lat: float = Query(default=13.0827),
    lon: float = Query(default=80.2707)
) -> list[TimeEnergyResponse]:
    """Get hourly energy levels for visualization (stock chart style)"""
    if target_date is None:
        target_date = date.today()
    
    calculator = PanchangamCalculator(request.app.state.ephemeris)
    return calculator.get_hourly_energy(target_date, lat, lon)

@router.get("/week-forecast")
async def get_week_forecast(
    request: Request,
    lat: float = Query(default=13.0827),
    lon: float = Query(default=80.2707)
):
    """Get 7-day forecast with daily scores"""
    calculator = PanchangamCalculator(request.app.state.ephemeris)
    return calculator.get_week_forecast(lat, lon)

@router.get("/score-breakdown", response_model=ScoreBreakdownResponse)
async def get_score_breakdown(
    request: Request,
    target_date: Optional[date] = None,
    lat: float = Query(default=13.0827, description="Latitude"),
    lon: float = Query(default=80.2707, description="Longitude")
):
    """
    Get detailed breakdown of today's score showing all contributing factors.
    Explains WHY the score is what it is.
    """
    if target_date is None:
        target_date = date.today()

    calculator = PanchangamCalculator(request.app.state.ephemeris)
    return calculator.get_score_breakdown(target_date, lat, lon)
