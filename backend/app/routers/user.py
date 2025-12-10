"""
User Profile API Router
User-specific calculations and profile data
"""

from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.user import User, AstroProfile

router = APIRouter()

class BirthDetails(BaseModel):
    name: str
    date: str  # YYYY-MM-DD
    time: str  # HH:MM
    place: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class RasiInfo(BaseModel):
    index: int
    name: str
    tamil: str
    symbol: str

class NakshatraInfo(BaseModel):
    index: int
    name: str
    tamil: str
    pada: int
    lord: str
    lord_tamil: str

class DashaInfo(BaseModel):
    mahadasha: str
    mahadasha_tamil: str
    mahadasha_end: str
    mahadasha_remaining_years: float
    antardasha: str
    antardasha_tamil: str
    antardasha_end: str
    antardasha_remaining_months: float

class ProfileSummaryResponse(BaseModel):
    name: str
    moon_rasi: RasiInfo
    nakshatra: NakshatraInfo
    current_dasha: DashaInfo
    birth_details: dict

class RegisterUserRequest(BaseModel):
    """Request body for user registration (from onboarding)"""
    name: str
    gender: str  # male/female/other
    birth_date: str  # YYYY-MM-DD
    birth_time: Optional[str] = None  # HH:MM
    birth_place: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@router.post("/register")
async def register_user(
    request: Request,
    user_data: RegisterUserRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user from onboarding flow.
    Creates user record and astro profile with calculated rasi/nakshatra.
    """
    from app.services.jathagam_generator import JathagamGenerator
    from datetime import date, time as dt_time

    # Create user
    user = User(
        email=f"{user_data.name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}@local",
        name=user_data.name,
        gender=user_data.gender,
        is_active=True
    )
    db.add(user)
    db.flush()  # Get user ID

    # Parse dates
    birth_date_obj = date.fromisoformat(user_data.birth_date)
    birth_time_obj = None
    if user_data.birth_time:
        try:
            parts = user_data.birth_time.split(':')
            birth_time_obj = dt_time(int(parts[0]), int(parts[1]))
        except:
            pass

    # Create astro profile
    profile = AstroProfile(
        user_id=user.id,
        birth_date=birth_date_obj,
        birth_time=birth_time_obj,
        birth_time_known=user_data.birth_time is not None,
        birth_place=user_data.birth_place,
        birth_latitude=user_data.latitude,
        birth_longitude=user_data.longitude,
    )

    # Calculate astrology data
    try:
        generator = JathagamGenerator(request.app.state.ephemeris)
        birth = BirthDetails(
            name=user_data.name,
            date=user_data.birth_date,
            time=user_data.birth_time or "12:00",
            place=user_data.birth_place,
            latitude=user_data.latitude,
            longitude=user_data.longitude
        )
        summary = generator.get_profile_summary(birth)

        # Handle both dict and object responses
        if isinstance(summary, dict):
            moon_rasi = summary.get('moon_rasi', {})
            nakshatra = summary.get('nakshatra', {})
            dasha = summary.get('current_dasha', {})

            profile.rasi = moon_rasi.get('name') if isinstance(moon_rasi, dict) else getattr(moon_rasi, 'name', None)
            profile.rasi_tamil = moon_rasi.get('tamil') if isinstance(moon_rasi, dict) else getattr(moon_rasi, 'tamil', None)
            profile.nakshatra = nakshatra.get('name') if isinstance(nakshatra, dict) else getattr(nakshatra, 'name', None)
            profile.nakshatra_tamil = nakshatra.get('tamil') if isinstance(nakshatra, dict) else getattr(nakshatra, 'tamil', None)
            profile.nakshatra_pada = nakshatra.get('pada') if isinstance(nakshatra, dict) else getattr(nakshatra, 'pada', None)
            profile.current_mahadasha = dasha.get('mahadasha_tamil') if isinstance(dasha, dict) else getattr(dasha, 'mahadasha_tamil', None)
            profile.current_antardasha = dasha.get('antardasha_tamil') if isinstance(dasha, dict) else getattr(dasha, 'antardasha_tamil', None)
        else:
            # Object-style access
            profile.rasi = summary.moon_rasi.name
            profile.rasi_tamil = summary.moon_rasi.tamil
            profile.nakshatra = summary.nakshatra.name
            profile.nakshatra_tamil = summary.nakshatra.tamil
            profile.nakshatra_pada = summary.nakshatra.pada
            profile.current_mahadasha = summary.current_dasha.mahadasha_tamil
            profile.current_antardasha = summary.current_dasha.antardasha_tamil

        profile.is_complete = True
        profile.astro_computed_at = datetime.utcnow()
    except Exception as e:
        print(f"Failed to compute astrology: {e}")
        import traceback
        traceback.print_exc()

    db.add(profile)
    db.commit()
    db.refresh(user)
    db.refresh(profile)

    return {
        "success": True,
        "user_id": user.id,
        "uuid": user.uuid,
        "name": user.name,
        "rasi": profile.rasi_tamil,
        "nakshatra": profile.nakshatra_tamil
    }


@router.get("/list")
async def list_users(db: Session = Depends(get_db)):
    """List all registered users with their astro profiles"""
    users = db.query(User).all()
    result = []
    for user in users:
        profile = user.profile
        result.append({
            "id": user.id,
            "name": user.name,
            "gender": user.gender,
            "created_at": str(user.created_at) if user.created_at else None,
            "birth_date": str(profile.birth_date) if profile else None,
            "birth_place": profile.birth_place if profile else None,
            "rasi": profile.rasi_tamil if profile else None,
            "nakshatra": profile.nakshatra_tamil if profile else None,
            "mahadasha": profile.current_mahadasha if profile else None
        })
    return result


@router.post("/profile-summary", response_model=ProfileSummaryResponse)
async def get_profile_summary(request: Request, birth: BirthDetails):
    """
    Get user profile summary including:
    - Moon Rasi (zodiac sign)
    - Birth Nakshatra with Pada
    - Current Maha Dasha and Antar Dasha

    This is used for the UserProfileBanner component.
    """
    from app.services.jathagam_generator import JathagamGenerator

    generator = JathagamGenerator(request.app.state.ephemeris)
    return generator.get_profile_summary(birth)
