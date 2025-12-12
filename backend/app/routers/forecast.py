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
    language: Optional[str] = 'ta'  # Language: ta, en, kn


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
            current_transits=current_transits,
            lang=data.language or 'ta'
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
    language: Optional[str] = 'ta'  # Language: ta, en, kn


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

        # Calculate projections with full jathagam and language
        lang = data.language or 'ta'
        result = projection_service.calculate_projections(jathagam, dasha_info, lang)

        return {
            "name": data.name,
            "projections": result
        }

    except Exception as e:
        # Log the actual error for debugging
        import traceback
        print(f"[FUTURE-PROJECTIONS ERROR] {str(e)}")
        traceback.print_exc()

        # Return fallback projections if calculation fails
        from datetime import date
        from app.services.future_projection_service import get_month_name, get_year_label

        current_year = date.today().year
        current_month = date.today().month
        lang = data.language or 'ta'

        fallback_monthly = []
        for i in range(12):
            month = ((current_month - 1 + i) % 12) + 1
            year = current_year + ((current_month - 1 + i) // 12)
            fallback_monthly.append({
                'name': get_month_name(month, lang),
                'month': month,
                'year': year,
                'score': 65 + (i % 5) * 3,
                'factors': [{'name': 'Transit effect' if lang == 'en' else ('ಗೋಚಾರ ಪರಿಣಾಮ' if lang == 'kn' else 'கிரக சஞ்சாரம்'), 'value': 10, 'positive': True}]
            })

        return {
            "name": data.name,
            "projections": {
                "monthly": fallback_monthly,
                "yearly": [
                    {"year": current_year, "label": get_year_label(0, lang), "score": 68, "factors": []},
                    {"year": current_year + 1, "label": get_year_label(1, lang), "score": 72, "factors": []},
                    {"year": current_year + 2, "label": get_year_label(2, lang), "score": 75, "factors": []}
                ]
            },
            "error": str(e)
        }


class PredictionV41Request(BaseModel):
    name: str
    birth_date: str  # YYYY-MM-DD
    birth_time: str  # HH:MM
    birth_place: str
    target_date: str  # YYYY-MM-DD - Date to predict for
    latitude: Optional[float] = 13.0827
    longitude: Optional[float] = 80.2707
    life_area: Optional[str] = 'general'  # general, career, finance, health, relationships
    mode_hint: Optional[str] = None  # past, future, monthly, yearly (auto-detected if None)
    language: Optional[str] = 'ta'  # Language: ta, en, kn


@router.post("/prediction-v41")
async def get_prediction_v41(request: Request, data: PredictionV41Request):
    """
    v4.1 Time-Adaptive Prediction with full explainability.

    This endpoint uses the Astro Engine v4.1 which automatically:
    - Detects time mode (past/present/future/monthly/yearly)
    - Adjusts module weights based on temporal context
    - Calculates POI (Planet Operational Intensity) per planet
    - Calculates HAI (House Activation Index) per house
    - Returns full mathematical reasoning trace
    - Provides confidence score with breakdown

    Returns:
    - time_mode: Which mode was activated and weight modifications applied
    - module_scores: All 6 modules with tensor breakdowns
    - final_score: Prediction score (0-100)
    - confidence: Reliability score with component breakdown
    - reasoning_trace: Mathematical calculation steps
    - top_positive_drivers: Factors boosting the score
    - top_negative_drivers: Factors reducing the score
    """
    from app.services.future_projection_service import FutureProjectionService
    from app.services.jathagam_generator import JathagamGenerator
    from pydantic import BaseModel as PM
    from datetime import date

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
        # Parse target date
        target_date = date.fromisoformat(data.target_date)

        # Generate birth chart
        jathagam = jathagam_gen.generate(birth)

        # Check if v4.1 engine is available
        v41_available = projection_service.is_v41_available()

        # Get dasha info from jathagam
        dasha_lord = None
        bhukti_lord = None
        dasha_data = jathagam.get('dasha', {})
        if dasha_data.get('current'):
            dasha_lord = dasha_data['current'].get('lord')
            bhukti_lord = dasha_data['current'].get('antardasha_lord')

        # Calculate v4.1 prediction
        lang = data.language or 'ta'
        result = projection_service.calculate_projection_v41(
            jathagam=jathagam,
            target_date=target_date,
            life_area=data.life_area or 'general',
            mode_hint=data.mode_hint,
            dasha_lord=dasha_lord,
            bhukti_lord=bhukti_lord,
            lang=lang
        )

        return {
            "name": data.name,
            "target_date": data.target_date,
            "v41_engine_available": v41_available,
            "prediction": result
        }

    except Exception as e:
        return {
            "name": data.name,
            "target_date": data.target_date,
            "v41_engine_available": False,
            "prediction": {
                "final_score": 65,
                "confidence": {"score": 50, "interpretation": "Error occurred"},
                "error": str(e)
            }
        }


@router.get("/engine-info")
async def get_engine_info():
    """
    Get information about the available prediction engines.

    Returns engine versions, capabilities, and configuration.
    """
    from app.services.future_projection_service import FutureProjectionService, V41_ENGINE_AVAILABLE

    return {
        "engines": {
            "v3.0": {
                "name": "Astro-Percent Engine v3.0",
                "status": "available",
                "features": [
                    "Monthly ephemeris integration",
                    "Eclipse detection and penalties",
                    "Jupiter/Saturn transit tables",
                    "Retrograde penalties",
                    "Longitude-based yoga validation",
                    "Navamsa cross-validation",
                    "Peak/worst month detection"
                ]
            },
            "v4.1": {
                "name": "Time-Adaptive Tensor Engine v4.1",
                "status": "available" if V41_ENGINE_AVAILABLE else "unavailable",
                "features": [
                    "Automatic time mode detection",
                    "POI (Planet Operational Intensity) calculation",
                    "HAI (House Activation Index) calculation",
                    "Dynamic weight adjustment by temporal context",
                    "Varshaphal (Solar Return) integration",
                    "Full explainability trace",
                    "Confidence scoring with breakdown",
                    "Past analysis mode with event verification",
                    "Future prediction mode with expanded transit window",
                    "Month-wise mode with POI/HAI recalculation",
                    "Year overlay mode with Muntha calculation"
                ],
                "time_modes": [
                    {"mode": "past_analysis", "transit_weight": 0.28, "navamsa_reduction": "20%"},
                    {"mode": "future_prediction", "navamsa_boost": "15%", "retrograde_softening": "30%"},
                    {"mode": "month_wise", "smoothing_power": 0.92, "poi_recalculation": "per_month"},
                    {"mode": "year_overlay", "transit_reduction": "25%", "varshaphal": True}
                ]
            }
        },
        "default_weights": {
            "dasha_bhukti": 0.25,
            "house_power": 0.18,
            "planet_power": 0.12,
            "transit": 0.20,
            "yoga_dosha": 0.12,
            "navamsa": 0.13
        }
    }
