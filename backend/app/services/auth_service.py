"""
Authentication Service
Handles Google OAuth and JWT token management
"""

from datetime import datetime, timedelta
from typing import Optional
import httpx
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy import func
import hashlib

from app.config import get_settings
from app.models.user import User, AstroProfile, UserSession

settings = get_settings()

# Google OAuth URLs
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
GOOGLE_PEOPLE_API_URL = "https://people.googleapis.com/v1/people/me"


class AuthService:
    """Handles authentication operations"""

    def __init__(self, db: Session):
        self.db = db

    def get_google_auth_url(self, state: str = None) -> str:
        """Generate Google OAuth authorization URL"""
        params = {
            "client_id": settings.google_client_id,
            "redirect_uri": settings.google_redirect_uri,
            "response_type": "code",
            "scope": " ".join([
                "openid",
                "email",
                "profile",
                "https://www.googleapis.com/auth/user.birthday.read",
                "https://www.googleapis.com/auth/user.gender.read"
            ]),
            "access_type": "offline",
            "prompt": "consent"
        }
        if state:
            params["state"] = state

        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{GOOGLE_AUTH_URL}?{query}"

    async def exchange_code_for_tokens(self, code: str) -> dict:
        """Exchange authorization code for access tokens"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "client_id": settings.google_client_id,
                    "client_secret": settings.google_client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": settings.google_redirect_uri
                }
            )
            if response.status_code != 200:
                raise Exception(f"Token exchange failed: {response.text}")
            return response.json()

    async def get_google_user_info(self, access_token: str) -> dict:
        """Get user info from Google"""
        async with httpx.AsyncClient() as client:
            # Get basic user info
            response = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            if response.status_code != 200:
                raise Exception(f"Failed to get user info: {response.text}")

            user_info = response.json()

            # Try to get birthday and gender from People API
            try:
                people_response = await client.get(
                    f"{GOOGLE_PEOPLE_API_URL}?personFields=birthdays,genders",
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                if people_response.status_code == 200:
                    people_data = people_response.json()

                    # Extract birthday
                    birthdays = people_data.get("birthdays", [])
                    for bday in birthdays:
                        date_info = bday.get("date", {})
                        if all(k in date_info for k in ["year", "month", "day"]):
                            user_info["birthday"] = f"{date_info['year']}-{date_info['month']:02d}-{date_info['day']:02d}"
                            break

                    # Extract gender
                    genders = people_data.get("genders", [])
                    if genders:
                        user_info["gender"] = genders[0].get("value", "").lower()

            except Exception as e:
                print(f"Could not fetch extended profile: {e}")

            return user_info

    def create_or_update_user(self, google_user: dict) -> User:
        """Create new user or update existing one from Google data"""
        # Check if user exists by Google ID
        user = self.db.query(User).filter(User.google_id == google_user["sub"]).first()

        if not user:
            # Check by email (might have been created differently)
            user = self.db.query(User).filter(User.email == google_user["email"]).first()

        birthday = None
        if google_user.get("birthday"):
            try:
                birthday = datetime.strptime(google_user["birthday"], "%Y-%m-%d").date()
            except:
                pass

        if user:
            # Update existing user
            user.name = google_user.get("name", user.name)
            user.picture = google_user.get("picture", user.picture)
            user.google_id = google_user["sub"]
            user.last_login = datetime.utcnow()
            if birthday:
                user.google_birthday = birthday
            if google_user.get("gender"):
                user.gender = google_user["gender"]
        else:
            # Create new user
            user = User(
                email=google_user["email"],
                google_id=google_user["sub"],
                name=google_user.get("name"),
                picture=google_user.get("picture"),
                google_birthday=birthday,
                gender=google_user.get("gender"),
                is_verified=google_user.get("email_verified", False),
                last_login=datetime.utcnow()
            )
            self.db.add(user)

        self.db.commit()
        self.db.refresh(user)
        return user

    def create_jwt_token(self, user: User, device_info: str = None, ip_address: str = None) -> str:
        """Create JWT token for user session"""
        expires = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

        payload = {
            "sub": user.uuid,
            "email": user.email,
            "name": user.name,
            "exp": expires,
            "iat": datetime.utcnow()
        }

        token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

        # Store session
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        session = UserSession(
            user_id=user.id,
            token_hash=token_hash,
            device_info=device_info,
            ip_address=ip_address,
            expires_at=expires
        )
        self.db.add(session)
        self.db.commit()

        return token

    def verify_token(self, token: str) -> Optional[User]:
        """Verify JWT token and return user"""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            user_uuid = payload.get("sub")
            if not user_uuid:
                return None

            # Check if session is still valid
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            session = self.db.query(UserSession).filter(
                UserSession.token_hash == token_hash,
                UserSession.is_active == True,
                UserSession.expires_at > datetime.utcnow()
            ).first()

            if not session:
                return None

            # Get user
            user = self.db.query(User).filter(User.uuid == user_uuid).first()
            return user

        except JWTError:
            return None

    def invalidate_token(self, token: str):
        """Invalidate a session token"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        session = self.db.query(UserSession).filter(UserSession.token_hash == token_hash).first()
        if session:
            session.is_active = False
            self.db.commit()

    def get_user_by_uuid(self, uuid: str) -> Optional[User]:
        """Get user by UUID"""
        return self.db.query(User).filter(User.uuid == uuid).first()

    def create_astro_profile(
        self,
        user: User,
        birth_date: str,
        birth_time: str,
        birth_place: str,
        latitude: float = None,
        longitude: float = None
    ) -> AstroProfile:
        """Create or update astrology profile for user"""
        profile = self.db.query(AstroProfile).filter(AstroProfile.user_id == user.id).first()

        birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()
        birth_time_obj = datetime.strptime(birth_time, "%H:%M").time() if birth_time else None

        if profile:
            profile.birth_date = birth_date_obj
            profile.birth_time = birth_time_obj
            profile.birth_place = birth_place
            profile.birth_latitude = latitude
            profile.birth_longitude = longitude
            profile.is_complete = True
            profile.updated_at = datetime.utcnow()
        else:
            profile = AstroProfile(
                user_id=user.id,
                birth_date=birth_date_obj,
                birth_time=birth_time_obj,
                birth_place=birth_place,
                birth_latitude=latitude,
                birth_longitude=longitude,
                is_complete=True
            )
            self.db.add(profile)

        self.db.commit()
        self.db.refresh(profile)
        return profile

    def update_computed_astro_data(
        self,
        profile: AstroProfile,
        rasi: str,
        rasi_tamil: str,
        nakshatra: str,
        nakshatra_tamil: str,
        nakshatra_pada: int,
        lagna: str = None,
        mahadasha: str = None,
        antardasha: str = None,
        mahadasha_end: str = None
    ):
        """Update computed astrology data in profile"""
        profile.rasi = rasi
        profile.rasi_tamil = rasi_tamil
        profile.nakshatra = nakshatra
        profile.nakshatra_tamil = nakshatra_tamil
        profile.nakshatra_pada = nakshatra_pada
        profile.lagna = lagna
        profile.current_mahadasha = mahadasha
        profile.current_antardasha = antardasha
        if mahadasha_end:
            profile.mahadasha_end_date = datetime.strptime(mahadasha_end, "%Y-%m-%d").date()
        profile.astro_computed_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(profile)
        return profile
