"""
Admin Router - View database contents
For development/debugging only
"""

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, AstroProfile

router = APIRouter()

# Rasi symbols for display
RASI_SYMBOLS = {
    'மேஷம்': '♈', 'ரிஷபம்': '♉', 'மிதுனம்': '♊', 'கடகம்': '♋',
    'சிம்மம்': '♌', 'கன்னி': '♍', 'துலாம்': '♎', 'விருச்சிகம்': '♏',
    'தனுசு': '♐', 'மகரம்': '♑', 'கும்பம்': '♒', 'மீனம்': '♓'
}


@router.get("/", response_class=HTMLResponse)
async def admin_dashboard(db: Session = Depends(get_db)):
    """
    Simple HTML admin dashboard to view registered users with rasi/nakshatra
    """
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ஜோதிட AI - Admin</title>
        <meta charset="UTF-8">
        <style>
            * { box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #fff7ed 0%, #ffffff 50%, #fff7ed 100%);
                min-height: 100vh;
            }
            h1 { color: #ea580c; margin-bottom: 5px; }
            .subtitle { color: #9a3412; margin-bottom: 30px; font-size: 14px; }
            h2 { color: #c2410c; margin-top: 30px; display: flex; align-items: center; gap: 10px; }

            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
                margin-bottom: 30px;
            }
            .stat-card {
                background: white;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(234, 88, 12, 0.1);
                border: 1px solid #fed7aa;
                text-align: center;
            }
            .stat-value { font-size: 32px; font-weight: bold; color: #ea580c; }
            .stat-label { font-size: 12px; color: #9a3412; text-transform: uppercase; }

            table {
                width: 100%;
                border-collapse: collapse;
                background: white;
                margin: 15px 0;
                box-shadow: 0 2px 12px rgba(0,0,0,0.08);
                border-radius: 12px;
                overflow: hidden;
            }
            th {
                background: linear-gradient(135deg, #ea580c, #dc2626);
                color: white;
                text-align: left;
                padding: 14px 16px;
                font-weight: 600;
                font-size: 13px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            td {
                padding: 14px 16px;
                border-bottom: 1px solid #fed7aa;
                font-size: 14px;
            }
            tr:last-child td { border-bottom: none; }
            tr:hover { background: #fff7ed; }

            .rasi-badge {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                background: linear-gradient(135deg, #fef3c7, #fde68a);
                padding: 6px 12px;
                border-radius: 20px;
                font-weight: 500;
                color: #92400e;
            }
            .rasi-symbol { font-size: 18px; }

            .nakshatra-badge {
                display: inline-flex;
                align-items: center;
                gap: 4px;
                background: linear-gradient(135deg, #dbeafe, #bfdbfe);
                padding: 6px 12px;
                border-radius: 20px;
                font-weight: 500;
                color: #1e40af;
            }

            .dasha-badge {
                background: linear-gradient(135deg, #dcfce7, #bbf7d0);
                padding: 4px 10px;
                border-radius: 12px;
                font-size: 12px;
                color: #166534;
            }

            .gender-male { color: #3b82f6; }
            .gender-female { color: #ec4899; }

            .count {
                background: #ea580c;
                color: white;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 13px;
                font-weight: 600;
            }
            .empty {
                color: #9ca3af;
                font-style: italic;
                text-align: center;
                padding: 40px;
            }
            .nav {
                background: linear-gradient(135deg, #ea580c, #dc2626);
                padding: 15px 25px;
                border-radius: 12px;
                margin-bottom: 25px;
                box-shadow: 0 4px 12px rgba(234, 88, 12, 0.3);
            }
            .nav a {
                color: white;
                text-decoration: none;
                margin-right: 25px;
                font-weight: 500;
                opacity: 0.9;
                transition: opacity 0.2s;
            }
            .nav a:hover { opacity: 1; text-decoration: underline; }

            .place-badge {
                background: #f3f4f6;
                padding: 4px 10px;
                border-radius: 8px;
                font-size: 12px;
                color: #4b5563;
            }

            .date-text {
                font-family: monospace;
                color: #6b7280;
            }

            .refresh-btn {
                background: #ea580c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 500;
                margin-left: auto;
            }
            .refresh-btn:hover { background: #c2410c; }

            .header-row {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="nav">
            <a href="/">🏠 API Home</a>
            <a href="/docs">📚 API Docs</a>
            <a href="/api/admin">👤 Admin Dashboard</a>
        </div>

        <div class="header-row">
            <div>
                <h1>🪔 ஜோதிட AI - Admin Dashboard</h1>
                <p class="subtitle">Registered Users &amp; Astrology Profiles</p>
            </div>
            <button class="refresh-btn" onclick="location.reload()">🔄 Refresh</button>
        </div>
    """

    try:
        # Get counts
        user_count = db.query(User).count()
        profile_count = db.query(AstroProfile).filter(AstroProfile.is_complete == True).count()

        # Stats cards
        html += f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{user_count}</div>
                <div class="stat-label">Total Users</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{profile_count}</div>
                <div class="stat-label">Complete Profiles</div>
            </div>
        </div>
        """

        # Users table with astro data
        html += f'<h2>👤 Registered Users <span class="count">{user_count}</span></h2>'

        if user_count > 0:
            users = db.query(User).order_by(User.created_at.desc()).limit(100).all()

            html += """
            <table>
                <tr>
                    <th>#</th>
                    <th>Name</th>
                    <th>Gender</th>
                    <th>Birth Date</th>
                    <th>Birth Place</th>
                    <th>Rasi (ராசி)</th>
                    <th>Nakshatra (நட்சத்திரம்)</th>
                    <th>Mahadasha</th>
                    <th>Registered</th>
                </tr>
            """

            for i, user in enumerate(users, 1):
                profile = user.profile

                # Gender display
                gender_class = "gender-male" if user.gender == "male" else "gender-female" if user.gender == "female" else ""
                gender_display = "👨 ஆண்" if user.gender == "male" else "👩 பெண்" if user.gender == "female" else user.gender or "-"

                # Rasi with symbol
                rasi_display = "-"
                if profile and profile.rasi_tamil:
                    symbol = RASI_SYMBOLS.get(profile.rasi_tamil, "⭐")
                    rasi_display = f'<span class="rasi-badge"><span class="rasi-symbol">{symbol}</span> {profile.rasi_tamil}</span>'

                # Nakshatra
                nakshatra_display = "-"
                if profile and profile.nakshatra_tamil:
                    pada = f" (பாதம் {profile.nakshatra_pada})" if profile.nakshatra_pada else ""
                    nakshatra_display = f'<span class="nakshatra-badge">⭐ {profile.nakshatra_tamil}{pada}</span>'

                # Dasha
                dasha_display = "-"
                if profile and profile.current_mahadasha:
                    dasha_display = f'<span class="dasha-badge">{profile.current_mahadasha}</span>'

                # Birth date
                birth_date = f'<span class="date-text">{profile.birth_date}</span>' if profile and profile.birth_date else "-"

                # Birth place
                birth_place = f'<span class="place-badge">📍 {profile.birth_place}</span>' if profile and profile.birth_place else "-"

                # Registration date
                reg_date = str(user.created_at)[:10] if user.created_at else "-"

                html += f"""
                <tr>
                    <td>{i}</td>
                    <td><strong>{user.name or '-'}</strong></td>
                    <td class="{gender_class}">{gender_display}</td>
                    <td>{birth_date}</td>
                    <td>{birth_place}</td>
                    <td>{rasi_display}</td>
                    <td>{nakshatra_display}</td>
                    <td>{dasha_display}</td>
                    <td><span class="date-text">{reg_date}</span></td>
                </tr>
                """

            html += "</table>"
        else:
            html += '<p class="empty">No users registered yet. Complete the onboarding flow to add users.</p>'

    except Exception as e:
        html += f"""
        <div style="background: #fef2f2; border: 1px solid #fecaca; padding: 20px; border-radius: 12px; margin: 20px 0;">
            <h3 style="color: #dc2626; margin-top: 0;">⚠️ Database Error</h3>
            <p style="color: #991b1b;">{str(e)}</p>
            <p style="color: #6b7280;">The database tables will be created automatically when the server starts.</p>
        </div>
        """

    html += """
    </body>
    </html>
    """

    return html


@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get database statistics as JSON"""
    try:
        user_count = db.query(User).count()
        profile_count = db.query(AstroProfile).filter(AstroProfile.is_complete == True).count()

        return {
            "status": "ok",
            "stats": {
                "users": user_count,
                "complete_profiles": profile_count
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/users")
async def get_users_json(db: Session = Depends(get_db)):
    """Get all users as JSON (for API access)"""
    try:
        users = db.query(User).order_by(User.created_at.desc()).all()
        result = []

        for user in users:
            profile = user.profile
            result.append({
                "id": user.id,
                "uuid": user.uuid,
                "name": user.name,
                "gender": user.gender,
                "created_at": str(user.created_at) if user.created_at else None,
                "profile": {
                    "birth_date": str(profile.birth_date) if profile and profile.birth_date else None,
                    "birth_time": str(profile.birth_time) if profile and profile.birth_time else None,
                    "birth_place": profile.birth_place if profile else None,
                    "rasi": profile.rasi_tamil if profile else None,
                    "nakshatra": profile.nakshatra_tamil if profile else None,
                    "nakshatra_pada": profile.nakshatra_pada if profile else None,
                    "mahadasha": profile.current_mahadasha if profile else None,
                    "antardasha": profile.current_antardasha if profile else None,
                    "is_complete": profile.is_complete if profile else False
                } if profile else None
            })

        return {"users": result, "count": len(result)}
    except Exception as e:
        return {"error": str(e)}
