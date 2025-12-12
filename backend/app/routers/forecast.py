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


class LifeTimelineRequest(BaseModel):
    name: str
    birth_date: str  # YYYY-MM-DD
    birth_time: str  # HH:MM
    birth_place: str
    latitude: Optional[float] = 13.0827
    longitude: Optional[float] = 80.2707
    years_ahead: Optional[int] = 10  # Number of years to predict


@router.post("/life-timeline")
async def get_life_timeline(request: Request, data: LifeTimelineRequest):
    """
    Get comprehensive life timeline prediction showing:
    - High/low periods
    - Major life events (career, relationships, finances, health)
    - Year-by-year scores and insights
    - Dasha-based predictions
    """
    from app.services.life_timeline_service import LifeTimelineService
    from app.services.jathagam_generator import JathagamGenerator

    ephemeris = getattr(request.app.state, 'ephemeris', None)
    jathagam_gen = JathagamGenerator(ephemeris)
    timeline_service = LifeTimelineService(jathagam_gen, ephemeris)

    return timeline_service.generate_life_timeline(data)


class PlanetAuraRequest(BaseModel):
    name: str
    birth_date: str  # YYYY-MM-DD
    birth_time: str  # HH:MM
    birth_place: str
    latitude: Optional[float] = 13.0827
    longitude: Optional[float] = 80.2707


@router.post("/planet-aura")
async def get_planet_aura(request: Request, data: PlanetAuraRequest):
    """
    Get planet strength visualization data for Aura Heatmap showing:
    - Individual planet strengths (0-100)
    - Favorable vs unfavorable influences
    - Current transit effects
    - Overall aura score
    - Color mappings for visualization
    """
    from app.services.planet_aura_service import PlanetAuraService
    from app.services.jathagam_generator import JathagamGenerator

    ephemeris = getattr(request.app.state, 'ephemeris', None)
    jathagam_gen = JathagamGenerator(ephemeris)
    aura_service = PlanetAuraService(jathagam_gen, ephemeris)

    return aura_service.calculate_planet_aura(data)


@router.get("/transits-map")
async def get_transits_map(
    request: Request,
    lat: float = Query(13.0827, description="Latitude"),
    lon: float = Query(80.2707, description="Longitude"),
    rasi: str = Query("", description="User's rasi for personalized alerts")
):
    """
    Get live transits map showing:
    - Current planetary positions
    - Moon transit timer (time until next sign change)
    - Live planetary shifts
    - Retrograde countdown and status
    - Upcoming transit alerts
    """
    from app.services.transits_map_service import TransitsMapService

    ephemeris = getattr(request.app.state, 'ephemeris', None)
    transits_service = TransitsMapService(ephemeris)

    return transits_service.get_transits_map(lat, lon, rasi)


class LifeAreasRequest(BaseModel):
    name: str
    birth_date: str  # YYYY-MM-DD
    birth_time: str  # HH:MM
    birth_place: str
    latitude: Optional[float] = 13.0827
    longitude: Optional[float] = 80.2707


@router.post("/life-areas")
async def get_life_areas(request: Request, data: LifeAreasRequest):
    """
    Get dynamic life area scores based on birth chart:
    - Love (7th house, Venus)
    - Career (10th house, Saturn)
    - Education (4th, 5th house, Mercury/Jupiter)
    - Family (4th house, Moon)
    - Health (1st, 6th house, Sun)

    Scores are calculated based on:
    - Karaka planet strengths
    - House lord placements
    - Current dasha period
    - Transits over natal positions
    """
    from app.services.life_areas_service import LifeAreasService
    from app.services.jathagam_generator import JathagamGenerator
    from pydantic import BaseModel as PM

    ephemeris = getattr(request.app.state, 'ephemeris', None)
    jathagam_gen = JathagamGenerator(ephemeris)
    life_areas_service = LifeAreasService(jathagam_gen, ephemeris)

    # Create birth details object
    class BirthDetails(PM):
        name: str
        date: str
        time: str
        place: str
        latitude: float
        longitude: float

    birth = BirthDetails(
        name=data.name,
        date=data.birth_date,
        time=data.birth_time,
        place=data.birth_place,
        latitude=data.latitude or 13.0827,
        longitude=data.longitude or 80.2707
    )

    # Generate birth chart
    try:
        jathagam = jathagam_gen.generate(birth)

        # Get current transits
        from datetime import datetime
        jd = ephemeris.datetime_to_jd(datetime.now()) if ephemeris else None
        current_transits = ephemeris.get_all_planets(jd) if ephemeris and jd else None

        # Get dasha lord
        dasha_lord = None
        if jathagam.get('dasha', {}).get('current'):
            dasha_lord = jathagam['dasha']['current'].get('lord')

        # Calculate life areas
        result = life_areas_service.calculate_life_areas(
            planets=jathagam.get('planets', []),
            lagna_rasi=jathagam.get('lagna', {}).get('rasi', 'Aries'),
            moon_rasi=jathagam.get('moon_sign', {}).get('rasi', 'Aries'),
            dasha_lord=dasha_lord,
            current_transits=current_transits
        )

        return {
            "name": data.name,
            "life_areas": result
        }
    except Exception as e:
        # Return fallback data if calculation fails
        return {
            "name": data.name,
            "life_areas": {
                "love": {"score": 65, "status": "good", "status_tamil": "நல்லது", "factors": [], "suggestion": "வெள்ளிக்கிழமை விரதம் இருங்கள்"},
                "career": {"score": 70, "status": "good", "status_tamil": "நல்லது", "factors": [], "suggestion": "சனிக்கிழமை ஹனுமான் வழிபாடு செய்யுங்கள்"},
                "education": {"score": 68, "status": "good", "status_tamil": "நல்லது", "factors": [], "suggestion": "புதன்கிழமை விஷ்ணு வழிபாடு செய்யுங்கள்"},
                "family": {"score": 72, "status": "good", "status_tamil": "நல்லது", "factors": [], "suggestion": "திங்கள்கிழமை சிவ வழிபாடு செய்யுங்கள்"},
                "health": {"score": 60, "status": "average", "status_tamil": "சாதாரணம்", "factors": [], "suggestion": "ஞாயிறு காயத்ரி ஜபம் செய்யுங்கள்"}
            },
            "error": str(e)
        }


class FutureProjectionRequest(BaseModel):
    name: str
    birth_date: str  # YYYY-MM-DD
    birth_time: str  # HH:MM
    birth_place: str
    latitude: Optional[float] = 13.0827
    longitude: Optional[float] = 80.2707


@router.post("/future-projections")
async def get_future_projections(request: Request, data: FutureProjectionRequest):
    """
    Get personalized monthly and yearly projections based on birth chart:
    - 12 monthly projections with scores and factors
    - 3 yearly projections (current, next, third year)

    Calculations based on:
    - User's natal chart planetary positions
    - Current dasha/antardasha period
    - Jupiter and Saturn transits
    - Transit effects from user's Moon sign
    """
    from app.services.future_projection_service import FutureProjectionService
    from app.services.jathagam_generator import JathagamGenerator
    from pydantic import BaseModel as PM

    ephemeris = getattr(request.app.state, 'ephemeris', None)
    jathagam_gen = JathagamGenerator(ephemeris)
    projection_service = FutureProjectionService(ephemeris)

    # Create birth details object
    class BirthDetails(PM):
        name: str
        date: str
        time: str
        place: str
        latitude: float
        longitude: float

    birth = BirthDetails(
        name=data.name,
        date=data.birth_date,
        time=data.birth_time,
        place=data.birth_place,
        latitude=data.latitude or 13.0827,
        longitude=data.longitude or 80.2707
    )

    try:
        # Generate birth chart
        jathagam = jathagam_gen.generate(birth)

        # Build dasha info from jathagam
        dasha_info = {
            'mahadasha_lord': 'Jupiter',  # Default
            'antardasha_lord': 'Saturn'
        }

        dasha_data = jathagam.get('dasha', {})
        if dasha_data.get('current'):
            dasha_info['mahadasha_lord'] = dasha_data['current'].get('lord', 'Jupiter')
            # Get antardasha if available
            dasha_info['antardasha_lord'] = dasha_data['current'].get('antardasha_lord', 'Saturn')
        if dasha_data.get('all_periods'):
            # Get current dasha from periods
            for period in dasha_data.get('all_periods', []):
                if period.get('is_current'):
                    dasha_info['mahadasha_lord'] = period.get('lord', dasha_info['mahadasha_lord'])

        # Calculate projections with full jathagam (not partial natal_chart)
        result = projection_service.calculate_projections(jathagam, dasha_info)

        return {
            "name": data.name,
            "projections": result
        }

    except Exception as e:
        # Return fallback projections if calculation fails
        from datetime import date
        current_year = date.today().year
        current_month = date.today().month

        tamil_months = [
            'ஜனவரி', 'பிப்ரவரி', 'மார்ச்', 'ஏப்ரல்', 'மே', 'ஜூன்',
            'ஜூலை', 'ஆகஸ்ட்', 'செப்டம்பர்', 'அக்டோபர்', 'நவம்பர்', 'டிசம்பர்'
        ]

        fallback_monthly = []
        for i in range(12):
            month = ((current_month - 1 + i) % 12) + 1
            year = current_year + ((current_month - 1 + i) // 12)
            fallback_monthly.append({
                'name': tamil_months[month - 1],
                'month': month,
                'year': year,
                'score': 65 + (i % 5) * 3,
                'factors': [{'name': 'கிரக சஞ்சாரம்', 'value': 10, 'positive': True}]
            })

        return {
            "name": data.name,
            "projections": {
                "monthly": fallback_monthly,
                "yearly": [
                    {"year": current_year, "label": "நடப்பு ஆண்டு", "score": 68, "factors": []},
                    {"year": current_year + 1, "label": "அடுத்த ஆண்டு", "score": 72, "factors": []},
                    {"year": current_year + 2, "label": "மூன்றாம் ஆண்டு", "score": 75, "factors": []}
                ]
            },
            "error": str(e)
        }
