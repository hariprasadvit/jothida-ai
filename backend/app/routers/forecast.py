"""
Forecast Router - Daily, Weekly, Monthly, Yearly Predictions
"""

from fastapi import APIRouter, Request, Query
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import date

router = APIRouter()


class ForecastRequest(BaseModel):
    rasi: str
    nakshatra: str
    birth_date: Optional[str] = None
    latitude: Optional[float] = 13.0827
    longitude: Optional[float] = 80.2707


@router.post("/user")
async def get_user_forecast(request: Request, data: ForecastRequest):
    """
    Get comprehensive forecast for a user including:
    - Today's forecast
    - This week's forecast
    - This month's forecast
    - Current year forecast
    - Next 3 years month-wise
    """
    from app.services.forecast_service import ForecastService
    from app.services.panchangam_calculator import PanchangamCalculator

    ephemeris = getattr(request.app.state, 'ephemeris', None)
    panchangam = PanchangamCalculator(ephemeris) if ephemeris else None

    forecast_service = ForecastService(ephemeris=ephemeris, panchangam_calculator=panchangam)

    birth_date_obj = None
    if data.birth_date:
        try:
            birth_date_obj = date.fromisoformat(data.birth_date)
        except:
            pass

    return forecast_service.get_user_forecast(
        user_rasi=data.rasi,
        user_nakshatra=data.nakshatra,
        birth_date=birth_date_obj,
        lat=data.latitude or 13.0827,
        lon=data.longitude or 80.2707
    )


@router.get("/daily")
async def get_daily_forecast(
    request: Request,
    rasi: str = Query(..., description="User's rasi"),
    nakshatra: str = Query("", description="User's nakshatra"),
    lat: float = Query(13.0827, description="Latitude"),
    lon: float = Query(80.2707, description="Longitude")
):
    """Get today's detailed forecast"""
    from app.services.forecast_service import ForecastService
    from app.services.panchangam_calculator import PanchangamCalculator

    ephemeris = getattr(request.app.state, 'ephemeris', None)
    panchangam = PanchangamCalculator(ephemeris) if ephemeris else None

    forecast_service = ForecastService(ephemeris=ephemeris, panchangam_calculator=panchangam)

    rasi_num = forecast_service.RASI_NUMBERS.get(rasi, 1)
    return forecast_service._get_daily_forecast(rasi_num, nakshatra, date.today(), lat, lon)


@router.get("/weekly")
async def get_weekly_forecast(
    request: Request,
    rasi: str = Query(..., description="User's rasi"),
    nakshatra: str = Query("", description="User's nakshatra")
):
    """Get 7-day forecast"""
    from app.services.forecast_service import ForecastService

    ephemeris = getattr(request.app.state, 'ephemeris', None)
    forecast_service = ForecastService(ephemeris=ephemeris)

    rasi_num = forecast_service.RASI_NUMBERS.get(rasi, 1)
    return forecast_service._get_weekly_forecast(rasi_num, nakshatra, date.today())


@router.get("/monthly")
async def get_monthly_forecast(
    request: Request,
    rasi: str = Query(..., description="User's rasi"),
    nakshatra: str = Query("", description="User's nakshatra"),
    month: Optional[int] = Query(None, description="Month (1-12)"),
    year: Optional[int] = Query(None, description="Year")
):
    """Get monthly forecast with daily scores"""
    from app.services.forecast_service import ForecastService

    ephemeris = getattr(request.app.state, 'ephemeris', None)
    forecast_service = ForecastService(ephemeris=ephemeris)

    rasi_num = forecast_service.RASI_NUMBERS.get(rasi, 1)

    ref_date = date.today()
    if month and year:
        ref_date = date(year, month, 1)

    return forecast_service._get_monthly_forecast(rasi_num, nakshatra, ref_date)


@router.get("/yearly")
async def get_yearly_forecast(
    request: Request,
    rasi: str = Query(..., description="User's rasi"),
    nakshatra: str = Query("", description="User's nakshatra"),
    year: Optional[int] = Query(None, description="Year")
):
    """Get yearly forecast by month"""
    from app.services.forecast_service import ForecastService

    ephemeris = getattr(request.app.state, 'ephemeris', None)
    forecast_service = ForecastService(ephemeris=ephemeris)

    rasi_num = forecast_service.RASI_NUMBERS.get(rasi, 1)

    ref_date = date.today()
    if year:
        ref_date = date(year, 1, 1)

    return forecast_service._get_yearly_forecast(rasi_num, nakshatra, ref_date)


@router.get("/three-years")
async def get_three_year_forecast(
    request: Request,
    rasi: str = Query(..., description="User's rasi"),
    nakshatra: str = Query("", description="User's nakshatra")
):
    """Get 3-year month-wise forecast"""
    from app.services.forecast_service import ForecastService

    ephemeris = getattr(request.app.state, 'ephemeris', None)
    forecast_service = ForecastService(ephemeris=ephemeris)

    rasi_num = forecast_service.RASI_NUMBERS.get(rasi, 1)
    return forecast_service._get_three_year_forecast(rasi_num, nakshatra, date.today())
