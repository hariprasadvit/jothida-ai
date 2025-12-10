"""
Authentication Router
Google OAuth login and user management
"""

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import date

from app.database import get_db
from app.config import get_settings
from app.services.auth_service import AuthService
from app.models.user import User, AstroProfile

router = APIRouter()
settings = get_settings()


# Pydantic models for requests/responses
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserResponse(BaseModel):
    uuid: str
    email: str
    name: Optional[str]
    picture: Optional[str]
    gender: Optional[str]
    google_birthday: Optional[date]
    has_astro_profile: bool
    astro_profile: Optional[dict] = None


class AstroProfileRequest(BaseModel):
    birth_date: str  # YYYY-MM-DD
    birth_time: Optional[str] = None  # HH:MM
    birth_place: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class AstroProfileResponse(BaseModel):
    id: int
    birth_date: date
    birth_time: Optional[str]
    birth_place: str
    rasi: Optional[str]
    rasi_tamil: Optional[str]
    nakshatra: Optional[str]
    nakshatra_tamil: Optional[str]
    is_complete: bool


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """Dependency to get current authenticated user"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = auth_header.replace("Bearer ", "")
    auth_service = AuthService(db)
    user = auth_service.verify_token(token)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user


def get_optional_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    """Dependency to get current user if authenticated, None otherwise"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.replace("Bearer ", "")
    auth_service = AuthService(db)
    return auth_service.verify_token(token)


@router.get("/google/login")
async def google_login(db: Session = Depends(get_db)):
    """
    Get Google OAuth login URL
    Frontend redirects user to this URL
    """
    auth_service = AuthService(db)
    auth_url = auth_service.get_google_auth_url()
    return {"auth_url": auth_url}


@router.get("/google/callback")
async def google_callback(
    code: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Handle Google OAuth callback
    Exchanges code for tokens and creates/updates user
    """
    auth_service = AuthService(db)

    try:
        # Exchange code for tokens
        tokens = await auth_service.exchange_code_for_tokens(code)
        access_token = tokens.get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to get access token")

        # Get user info from Google
        google_user = await auth_service.get_google_user_info(access_token)

        # Create or update user
        user = auth_service.create_or_update_user(google_user)

        # Create JWT token
        device_info = request.headers.get("User-Agent", "")[:500]
        ip_address = request.client.host if request.client else None
        jwt_token = auth_service.create_jwt_token(user, device_info, ip_address)

        # Check if user has astro profile
        has_profile = user.profile is not None and user.profile.is_complete

        # Redirect to frontend with token
        redirect_url = f"{settings.frontend_url}/auth/callback?token={jwt_token}&new_user={not has_profile}"
        return RedirectResponse(url=redirect_url)

    except Exception as e:
        print(f"Google callback error: {e}")
        redirect_url = f"{settings.frontend_url}/auth/callback?error=auth_failed"
        return RedirectResponse(url=redirect_url)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current authenticated user info"""
    # Get astro profile if exists
    astro_profile = None
    if current_user.profile and current_user.profile.is_complete:
        profile = current_user.profile
        astro_profile = {
            "birth_date": profile.birth_date.isoformat() if profile.birth_date else None,
            "birth_time": profile.birth_time.strftime("%H:%M") if profile.birth_time else None,
            "birth_place": profile.birth_place,
            "rasi": profile.rasi,
            "rasi_tamil": profile.rasi_tamil,
            "nakshatra": profile.nakshatra,
            "nakshatra_tamil": profile.nakshatra_tamil,
            "nakshatra_pada": profile.nakshatra_pada,
            "current_mahadasha": profile.current_mahadasha,
            "current_antardasha": profile.current_antardasha
        }

    return UserResponse(
        uuid=current_user.uuid,
        email=current_user.email,
        name=current_user.name,
        picture=current_user.picture,
        gender=current_user.gender,
        google_birthday=current_user.google_birthday,
        has_astro_profile=current_user.profile is not None and current_user.profile.is_complete,
        astro_profile=astro_profile
    )


@router.post("/profile/astro", response_model=AstroProfileResponse)
async def create_astro_profile(
    profile_data: AstroProfileRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create or update astrology profile
    Called after Google login to collect birth location
    """
    auth_service = AuthService(db)

    # Create/update astro profile
    profile = auth_service.create_astro_profile(
        user=current_user,
        birth_date=profile_data.birth_date,
        birth_time=profile_data.birth_time,
        birth_place=profile_data.birth_place,
        latitude=profile_data.latitude,
        longitude=profile_data.longitude
    )

    # Compute astrology data using jathagam generator
    try:
        from app.services.jathagam_generator import JathagamGenerator
        ephemeris = getattr(request.app.state, 'ephemeris', None)

        if ephemeris:
            generator = JathagamGenerator(ephemeris)
            birth_details = {
                "name": current_user.name,
                "date": profile_data.birth_date,
                "time": profile_data.birth_time or "12:00",
                "place": profile_data.birth_place,
                "latitude": profile_data.latitude or 13.0827,
                "longitude": profile_data.longitude or 80.2707,
                "timezone": "Asia/Kolkata"
            }

            # Generate jathagam
            from pydantic import BaseModel
            class BirthDetails(BaseModel):
                name: str
                date: str
                time: str
                place: str
                latitude: float
                longitude: float
                timezone: str = "Asia/Kolkata"

            jathagam = generator.generate(BirthDetails(**birth_details))

            # Update profile with computed data
            if jathagam:
                moon_sign = jathagam.get("moon_sign", {})
                dasha = jathagam.get("dasha", {}).get("current", {})

                auth_service.update_computed_astro_data(
                    profile=profile,
                    rasi=moon_sign.get("rasi", ""),
                    rasi_tamil=moon_sign.get("rasi_tamil", ""),
                    nakshatra=moon_sign.get("nakshatra", ""),
                    nakshatra_tamil=moon_sign.get("nakshatra", ""),  # Same as nakshatra
                    nakshatra_pada=moon_sign.get("nakshatra_pada", 1),
                    lagna=jathagam.get("lagna", {}).get("rasi", ""),
                    mahadasha=dasha.get("mahadasha", ""),
                    antardasha=dasha.get("antardasha", "")
                )
    except Exception as e:
        print(f"Failed to compute astrology data: {e}")

    return AstroProfileResponse(
        id=profile.id,
        birth_date=profile.birth_date,
        birth_time=profile.birth_time.strftime("%H:%M") if profile.birth_time else None,
        birth_place=profile.birth_place,
        rasi=profile.rasi,
        rasi_tamil=profile.rasi_tamil,
        nakshatra=profile.nakshatra,
        nakshatra_tamil=profile.nakshatra_tamil,
        is_complete=profile.is_complete
    )


@router.post("/logout")
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout current user (invalidate token)"""
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")

    auth_service = AuthService(db)
    auth_service.invalidate_token(token)

    return {"message": "Logged out successfully"}


@router.get("/check")
async def check_auth(
    user: Optional[User] = Depends(get_optional_user)
):
    """Check if current request is authenticated"""
    if user:
        return {
            "authenticated": True,
            "user": {
                "uuid": user.uuid,
                "name": user.name,
                "email": user.email,
                "has_astro_profile": user.profile is not None and user.profile.is_complete
            }
        }
    return {"authenticated": False}
