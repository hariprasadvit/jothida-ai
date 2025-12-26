"""
PDF Report Generation Router
Generate and download comprehensive astrology reports
"""

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, AstroProfile
from app.services.pdf_report_v6 import generate_v6_report

router = APIRouter()


class ReportRequest(BaseModel):
    """Request body for generating report"""
    name: str
    birth_date: str  # YYYY-MM-DD
    birth_time: str  # HH:MM
    birth_place: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    language: Optional[str] = 'ta'  # 'en', 'ta', or 'kn'


@router.post("/generate")
async def generate_report(request: Request, data: ReportRequest):
    """
    Generate comprehensive PDF astrology report.
    Returns PDF file as download.
    """
    from app.services.jathagam_generator import JathagamGenerator
    from app.routers.user import BirthDetails

    # Get chart data from jathagam generator
    try:
        generator = JathagamGenerator(request.app.state.ephemeris)
        birth = BirthDetails(
            name=data.name,
            date=data.birth_date,
            time=data.birth_time,
            place=data.birth_place,
            latitude=data.latitude,
            longitude=data.longitude
        )

        # Get full chart data
        chart_data = generator.generate(birth)

        # Also get profile summary for rasi/nakshatra
        profile_summary = generator.get_profile_summary(birth)

        # Merge data
        if isinstance(profile_summary, dict):
            chart_data['moon_rasi'] = profile_summary.get('moon_rasi', {})
            chart_data['nakshatra'] = profile_summary.get('nakshatra', {})
            chart_data['current_dasha'] = profile_summary.get('current_dasha', {})
        else:
            chart_data['moon_rasi'] = {
                'name': profile_summary.moon_rasi.name,
                'tamil': profile_summary.moon_rasi.tamil,
                'symbol': profile_summary.moon_rasi.symbol
            }
            chart_data['nakshatra'] = {
                'name': profile_summary.nakshatra.name,
                'tamil': profile_summary.nakshatra.tamil,
                'pada': profile_summary.nakshatra.pada
            }
            chart_data['current_dasha'] = {
                'mahadasha': profile_summary.current_dasha.mahadasha,
                'mahadasha_tamil': profile_summary.current_dasha.mahadasha_tamil,
                'antardasha': profile_summary.current_dasha.antardasha,
                'antardasha_tamil': profile_summary.current_dasha.antardasha_tamil
            }

    except Exception as e:
        print(f"Error generating chart data: {e}")
        import traceback
        traceback.print_exc()
        # Use empty chart data - report will use sample data
        chart_data = {}

    # Prepare user data
    user_data = {
        'name': data.name,
        'birth_date': data.birth_date,
        'birth_time': data.birth_time,
        'birth_place': data.birth_place,
        'latitude': data.latitude or 13.0827,
        'longitude': data.longitude or 80.2707
    }

    # Generate PDF with V6 Super Jyotish Engine
    language = data.language or 'ta'
    print(f"[REPORT] Generating PDF with language: '{language}' (received: '{data.language}')")
    try:
        pdf_bytes = generate_v6_report(chart_data, user_data, language)
    except Exception as e:
        print(f"Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")

    # Return PDF as download
    filename = f"Jathagam_Report_{data.name.replace(' ', '_')}_{data.birth_date}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.get("/download/{user_id}")
async def download_user_report(
    request: Request,
    user_id: int,
    language: str = 'ta',
    db: Session = Depends(get_db)
):
    """
    Download report for registered user by user ID.
    """
    # Get user and profile
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = user.profile
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    # Prepare birth details
    from app.services.jathagam_generator import JathagamGenerator
    from app.routers.user import BirthDetails

    birth_time_str = str(profile.birth_time) if profile.birth_time else "12:00"
    if birth_time_str and len(birth_time_str) > 5:
        birth_time_str = birth_time_str[:5]

    # Get chart data
    try:
        generator = JathagamGenerator(request.app.state.ephemeris)
        birth = BirthDetails(
            name=user.name or "User",
            date=str(profile.birth_date),
            time=birth_time_str,
            place=profile.birth_place or "Chennai",
            latitude=profile.birth_latitude,
            longitude=profile.birth_longitude
        )

        chart_data = generator.generate(birth)
        profile_summary = generator.get_profile_summary(birth)

        if isinstance(profile_summary, dict):
            chart_data['moon_rasi'] = profile_summary.get('moon_rasi', {})
            chart_data['nakshatra'] = profile_summary.get('nakshatra', {})
            chart_data['current_dasha'] = profile_summary.get('current_dasha', {})
        else:
            chart_data['moon_rasi'] = {'tamil': profile_summary.moon_rasi.tamil}
            chart_data['nakshatra'] = {'tamil': profile_summary.nakshatra.tamil, 'pada': profile_summary.nakshatra.pada}
            chart_data['current_dasha'] = {'mahadasha_tamil': profile_summary.current_dasha.mahadasha_tamil}

    except Exception as e:
        print(f"Error generating chart: {e}")
        chart_data = {
            'moon_rasi': {'tamil': profile.rasi_tamil or 'மேஷம்'},
            'nakshatra': {'tamil': profile.nakshatra_tamil or 'அசுவினி', 'pada': profile.nakshatra_pada or 1},
            'current_dasha': {'mahadasha_tamil': profile.current_mahadasha or 'சுக்கிரன்'}
        }

    user_data = {
        'name': user.name or "User",
        'birth_date': str(profile.birth_date),
        'birth_time': birth_time_str,
        'birth_place': profile.birth_place or "Chennai",
        'latitude': profile.birth_latitude or 13.0827,
        'longitude': profile.birth_longitude or 80.2707
    }

    # Generate PDF with V6 Super Jyotish Engine
    try:
        pdf_bytes = generate_v6_report(chart_data, user_data, language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")

    filename = f"Jathagam_Report_{user.name.replace(' ', '_') if user.name else 'User'}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.get("/debug")
async def debug_report_engine():
    """Debug endpoint to check V7 engine availability"""
    from app.services.pdf_report_v6 import TIME_ADAPTIVE_AVAILABLE, FUTURE_PROJECTION_AVAILABLE
    try:
        from app.services.time_adaptive_engine import TimeAdaptiveEngine, TimeMode
        v7_import_ok = True
        v7_version = getattr(TimeAdaptiveEngine, 'ENGINE_VERSION', 'unknown')
        time_modes = [m.name for m in TimeMode] if TimeMode else []
    except Exception as e:
        v7_import_ok = False
        v7_version = str(e)
        time_modes = []

    return {
        "TIME_ADAPTIVE_AVAILABLE": TIME_ADAPTIVE_AVAILABLE,
        "FUTURE_PROJECTION_AVAILABLE": FUTURE_PROJECTION_AVAILABLE,
        "v7_import_ok": v7_import_ok,
        "v7_version": v7_version,
        "time_modes": time_modes
    }


@router.get("/preview")
async def preview_report_info():
    """
    Get information about the report contents.
    """
    return {
        "report_name": "Comprehensive Jathagam Report",
        "pages": "44 pages (V6.2 + V7.0)",
        "sections": [
            "Cover Page with Birth Details",
            "Table of Contents",
            "Birth Details & Astronomical Data",
            "Rasi Chart (South Indian Style)",
            "Navamsa Chart (D-9)",
            "Planetary Positions",
            "12 House Analysis",
            "Nakshatra Analysis",
            "Dasha Periods (Vimshottari)",
            "Yogas (Auspicious Combinations)",
            "Doshas (Afflictions)",
            "Life Predictions",
            "Career & Profession",
            "Marriage & Family",
            "Health Analysis",
            "Wealth & Finance",
            "Remedies (Planet-wise)",
            "Favorable Periods",
            "Yearly Predictions",
            "Glossary & Appendix"
        ],
        "languages": ["English", "Tamil", "Kannada"],
        "format": "PDF (A4 size)"
    }
