"""
Mobile Authentication Router
OTP-based phone login (dummy SMS for development)
"""

import random
import string
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import jwt

from app.database import get_db
from app.models.user import User, AstroProfile, OTPVerification
from app.config import get_settings

router = APIRouter()
settings = get_settings()

# Store sent OTPs in memory for demo (in production use Redis/DB)
DEMO_OTPS = {}


class SendOTPRequest(BaseModel):
    phone_number: str  # Format: +91XXXXXXXXXX


class VerifyOTPRequest(BaseModel):
    phone_number: str
    otp_code: str


class RegisterWithPhoneRequest(BaseModel):
    phone_number: str
    otp_code: str
    name: str
    gender: str
    birth_date: str  # YYYY-MM-DD
    birth_time: Optional[str] = None  # HH:MM
    birth_place: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


def generate_otp() -> str:
    """Generate 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))


def create_access_token(user_id: int, phone: str) -> str:
    """Create JWT token for authenticated user"""
    expire = datetime.utcnow() + timedelta(days=30)
    to_encode = {
        "sub": str(user_id),
        "phone": phone,
        "exp": expire
    }
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")


@router.post("/send-otp")
async def send_otp(request: SendOTPRequest, db: Session = Depends(get_db)):
    """
    Send OTP to phone number.
    In development mode, OTP is returned in response (dummy SMS).
    In production, integrate with SMS gateway (Twilio, MSG91, etc.)
    """
    phone = request.phone_number.strip()

    # Validate phone format (Indian numbers)
    if not phone.startswith("+91") or len(phone) != 13:
        raise HTTPException(
            status_code=400,
            detail="Invalid phone number. Use format: +91XXXXXXXXXX"
        )

    # Generate OTP
    otp = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    # Store OTP in database
    existing = db.query(OTPVerification).filter(
        OTPVerification.phone_number == phone,
        OTPVerification.is_verified == False
    ).first()

    if existing:
        # Update existing OTP
        existing.otp_code = otp
        existing.expires_at = expires_at
        existing.attempts = 0
    else:
        # Create new OTP record
        otp_record = OTPVerification(
            phone_number=phone,
            otp_code=otp,
            expires_at=expires_at
        )
        db.add(otp_record)

    db.commit()

    # Store in memory for quick lookup (demo)
    DEMO_OTPS[phone] = otp

    # In production, send SMS here
    # sms_service.send(phone, f"Your ஜோதிட AI OTP is: {otp}")

    print(f"📱 OTP for {phone}: {otp}")  # Demo: print to console

    return {
        "success": True,
        "message": "OTP அனுப்பப்பட்டது",
        "message_en": "OTP sent successfully",
        "phone": phone,
        # DEMO MODE: Return OTP in response (remove in production!)
        "demo_otp": otp,
        "expires_in_seconds": 300
    }


@router.post("/verify-otp")
async def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    """
    Verify OTP and return auth token if user exists,
    or indicate that registration is needed.
    """
    phone = request.phone_number.strip()
    otp = request.otp_code.strip()

    # Get OTP record
    otp_record = db.query(OTPVerification).filter(
        OTPVerification.phone_number == phone,
        OTPVerification.is_verified == False
    ).order_by(OTPVerification.created_at.desc()).first()

    if not otp_record:
        raise HTTPException(status_code=400, detail="OTP not found. Request a new one.")

    # Check expiry
    if datetime.utcnow() > otp_record.expires_at:
        raise HTTPException(status_code=400, detail="OTP expired. Request a new one.")

    # Check attempts
    if otp_record.attempts >= otp_record.max_attempts:
        raise HTTPException(status_code=400, detail="Too many attempts. Request a new OTP.")

    # Verify OTP
    if otp_record.otp_code != otp:
        otp_record.attempts += 1
        db.commit()
        remaining = otp_record.max_attempts - otp_record.attempts
        raise HTTPException(
            status_code=400,
            detail=f"Invalid OTP. {remaining} attempts remaining."
        )

    # OTP verified
    otp_record.is_verified = True
    otp_record.verified_at = datetime.utcnow()
    db.commit()

    # Check if user exists
    user = db.query(User).filter(User.phone_number == phone).first()

    if user:
        # Existing user - return token
        token = create_access_token(user.id, phone)
        user.last_login = datetime.utcnow()
        user.phone_verified = True
        db.commit()

        profile = user.profile
        return {
            "success": True,
            "is_new_user": False,
            "token": token,
            "user": {
                "id": user.id,
                "uuid": user.uuid,
                "name": user.name,
                "phone": user.phone_number,
                "rasi": profile.rasi_tamil if profile else None,
                "nakshatra": profile.nakshatra_tamil if profile else None,
                "birth_date": str(profile.birth_date) if profile and profile.birth_date else None,
                "birth_time": str(profile.birth_time)[:5] if profile and profile.birth_time else None,
                "birth_place": profile.birth_place if profile else None,
                "latitude": profile.birth_latitude if profile else None,
                "longitude": profile.birth_longitude if profile else None
            }
        }
    else:
        # New user - needs registration
        return {
            "success": True,
            "is_new_user": True,
            "message": "OTP verified. Please complete registration.",
            "phone": phone
        }


@router.post("/register")
async def register_with_phone(
    request: Request,
    data: RegisterWithPhoneRequest,
    db: Session = Depends(get_db)
):
    """
    Register new user with phone number after OTP verification.
    Creates user and astro profile with calculated rasi/nakshatra.
    """
    from app.services.jathagam_generator import JathagamGenerator
    from app.routers.user import BirthDetails
    from datetime import date, time as dt_time

    phone = data.phone_number.strip()

    # Verify OTP was verified
    otp_record = db.query(OTPVerification).filter(
        OTPVerification.phone_number == phone,
        OTPVerification.is_verified == True
    ).order_by(OTPVerification.verified_at.desc()).first()

    if not otp_record or (datetime.utcnow() - otp_record.verified_at).total_seconds() > 600:
        raise HTTPException(
            status_code=400,
            detail="Please verify OTP first. Verification expired."
        )

    # Check if phone already registered
    existing = db.query(User).filter(User.phone_number == phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone number already registered.")

    # Create user
    user = User(
        phone_number=phone,
        phone_verified=True,
        name=data.name,
        gender=data.gender,
        is_active=True
    )
    db.add(user)
    db.flush()

    # Parse dates
    birth_date_obj = date.fromisoformat(data.birth_date)
    birth_time_obj = None
    if data.birth_time:
        try:
            parts = data.birth_time.split(':')
            birth_time_obj = dt_time(int(parts[0]), int(parts[1]))
        except:
            pass

    # Create astro profile
    profile = AstroProfile(
        user_id=user.id,
        birth_date=birth_date_obj,
        birth_time=birth_time_obj,
        birth_time_known=data.birth_time is not None,
        birth_place=data.birth_place,
        birth_latitude=data.latitude,
        birth_longitude=data.longitude,
    )

    # Calculate astrology data
    try:
        generator = JathagamGenerator(request.app.state.ephemeris)
        birth = BirthDetails(
            name=data.name,
            date=data.birth_date,
            time=data.birth_time or "12:00",
            place=data.birth_place,
            latitude=data.latitude,
            longitude=data.longitude
        )
        summary = generator.get_profile_summary(birth)

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

    # Create auth token
    token = create_access_token(user.id, phone)

    return {
        "success": True,
        "token": token,
        "user": {
            "id": user.id,
            "uuid": user.uuid,
            "name": user.name,
            "phone": user.phone_number,
            "rasi": profile.rasi_tamil,
            "nakshatra": profile.nakshatra_tamil
        }
    }


@router.get("/me")
async def get_current_user(request: Request, db: Session = Depends(get_db)):
    """Get current logged in user from token"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = user.profile
    return {
        "id": user.id,
        "uuid": user.uuid,
        "name": user.name,
        "phone": user.phone_number,
        "email": user.email,
        "gender": user.gender,
        "profile": {
            "birth_date": str(profile.birth_date) if profile else None,
            "birth_time": str(profile.birth_time) if profile and profile.birth_time else None,
            "birth_place": profile.birth_place if profile else None,
            "rasi": profile.rasi_tamil if profile else None,
            "nakshatra": profile.nakshatra_tamil if profile else None,
            "nakshatra_pada": profile.nakshatra_pada if profile else None,
            "mahadasha": profile.current_mahadasha if profile else None,
            "antardasha": profile.current_antardasha if profile else None
        } if profile else None
    }
