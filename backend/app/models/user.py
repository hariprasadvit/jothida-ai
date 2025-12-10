"""
User and Profile database models
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    """User account - stores Google OAuth or Mobile login data"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True, default=generate_uuid, index=True)

    # Google OAuth fields
    email = Column(String(255), unique=True, index=True, nullable=True)
    google_id = Column(String(255), unique=True, index=True, nullable=True)

    # Mobile login fields
    phone_number = Column(String(15), unique=True, index=True, nullable=True)
    phone_verified = Column(Boolean, default=False)

    # Basic info from Google
    name = Column(String(255))
    picture = Column(String(500))  # Profile picture URL

    # From Google (if available)
    google_birthday = Column(Date, nullable=True)  # DOB from Google
    gender = Column(String(20), nullable=True)  # male/female from Google

    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))

    # Relationships
    profile = relationship("AstroProfile", back_populates="user", uselist=False)
    sessions = relationship("UserSession", back_populates="user")


class AstroProfile(Base):
    """Astrology profile - birth details needed for calculations"""
    __tablename__ = "astro_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    # Birth details (required for astrology)
    birth_date = Column(Date, nullable=False)
    birth_time = Column(Time, nullable=True)  # Can be approximate
    birth_time_known = Column(Boolean, default=True)  # Whether time is exact

    # Birth location (collected after Google login)
    birth_place = Column(String(255), nullable=False)
    birth_latitude = Column(Float, nullable=True)
    birth_longitude = Column(Float, nullable=True)
    timezone = Column(String(50), default="Asia/Kolkata")

    # Computed astrology data (cached from calculations)
    rasi = Column(String(50), nullable=True)  # Moon sign
    rasi_tamil = Column(String(50), nullable=True)
    nakshatra = Column(String(50), nullable=True)
    nakshatra_tamil = Column(String(50), nullable=True)
    nakshatra_pada = Column(Integer, nullable=True)
    lagna = Column(String(50), nullable=True)  # Ascendant

    # Current dasha (cached, updated periodically)
    current_mahadasha = Column(String(50), nullable=True)
    current_antardasha = Column(String(50), nullable=True)
    mahadasha_end_date = Column(Date, nullable=True)

    # Profile completion status
    is_complete = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    astro_computed_at = Column(DateTime(timezone=True), nullable=True)  # When calculations were last done

    # Relationship
    user = relationship("User", back_populates="profile")


class UserSession(Base):
    """User sessions for JWT token management"""
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Session token
    token_hash = Column(String(255), unique=True, index=True)

    # Device info
    device_info = Column(String(500), nullable=True)
    ip_address = Column(String(50), nullable=True)

    # Session validity
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationship
    user = relationship("User", back_populates="sessions")


class OTPVerification(Base):
    """OTP codes for mobile phone verification"""
    __tablename__ = "otp_verifications"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(15), index=True, nullable=False)
    otp_code = Column(String(6), nullable=False)

    # Verification status
    is_verified = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=3)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    verified_at = Column(DateTime(timezone=True), nullable=True)
