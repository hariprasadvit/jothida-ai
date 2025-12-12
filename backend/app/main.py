"""
ஜோதிட AI - Backend API
Tamil Astrology AI Platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers import panchangam, jathagam, matching, chat, muhurtham, user, forecast
from app.routers import auth, admin, mobile_auth, report, remedy, ungal_jothidan
from app.services.ephemeris import EphemerisService
from app.database import init_db

# Lifespan for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    try:
        init_db()
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️ Database initialization skipped: {e}")

    # Initialize ephemeris
    app.state.ephemeris = EphemerisService()
    print("✅ Ephemeris service initialized")
    yield
    # Shutdown
    print("👋 Shutting down...")

app = FastAPI(
    title="ஜோதிட AI API",
    description="Tamil Astrology AI Platform - Backend API",
    version="0.1.0",
    lifespan=lifespan
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(panchangam.router, prefix="/api/panchangam", tags=["Panchangam"])
app.include_router(jathagam.router, prefix="/api/jathagam", tags=["Jathagam"])
app.include_router(matching.router, prefix="/api/matching", tags=["Matching"])
app.include_router(chat.router, prefix="/api/chat", tags=["AI Chat"])
app.include_router(muhurtham.router, prefix="/api/muhurtham", tags=["Muhurtham"])
app.include_router(user.router, prefix="/api/user", tags=["User"])
app.include_router(forecast.router, prefix="/api/forecast", tags=["Forecast"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(mobile_auth.router, prefix="/api/mobile", tags=["Mobile Auth"])
app.include_router(report.router, prefix="/api/report", tags=["PDF Reports"])
app.include_router(remedy.router, prefix="/api/remedy", tags=["AI Remedy Engine"])
app.include_router(ungal_jothidan.router, prefix="/api/ungal-jothidan", tags=["Ungal Jothidan"])

@app.get("/")
async def root():
    return {
        "message": "ஜோதிட AI API",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
