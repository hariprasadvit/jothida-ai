"""
Transits Map Service - Live Planetary Movements
Provides real-time transit data for the sky map visualization
Uses Astro-Percent Engine v3.0 tables for accurate transit scoring
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Optional
import math

# Import Astro-Percent Engine v3.0
try:
    from .astro_percent_engine import AstroPercentEngine
except ImportError:
    AstroPercentEngine = None

# Rasi (zodiac sign) data
RASI_DATA = {
    1: {'name': 'மேஷம்', 'name_en': 'Aries', 'symbol': '♈', 'element': 'நெருப்பு', 'ruler': 'செவ்வாய்'},
    2: {'name': 'ரிஷபம்', 'name_en': 'Taurus', 'symbol': '♉', 'element': 'நிலம்', 'ruler': 'சுக்கிரன்'},
    3: {'name': 'மிதுனம்', 'name_en': 'Gemini', 'symbol': '♊', 'element': 'காற்று', 'ruler': 'புதன்'},
    4: {'name': 'கடகம்', 'name_en': 'Cancer', 'symbol': '♋', 'element': 'நீர்', 'ruler': 'சந்திரன்'},
    5: {'name': 'சிம்மம்', 'name_en': 'Leo', 'symbol': '♌', 'element': 'நெருப்பு', 'ruler': 'சூரியன்'},
    6: {'name': 'கன்னி', 'name_en': 'Virgo', 'symbol': '♍', 'element': 'நிலம்', 'ruler': 'புதன்'},
    7: {'name': 'துலாம்', 'name_en': 'Libra', 'symbol': '♎', 'element': 'காற்று', 'ruler': 'சுக்கிரன்'},
    8: {'name': 'விருச்சிகம்', 'name_en': 'Scorpio', 'symbol': '♏', 'element': 'நீர்', 'ruler': 'செவ்வாய்'},
    9: {'name': 'தனுசு', 'name_en': 'Sagittarius', 'symbol': '♐', 'element': 'நெருப்பு', 'ruler': 'குரு'},
    10: {'name': 'மகரம்', 'name_en': 'Capricorn', 'symbol': '♑', 'element': 'நிலம்', 'ruler': 'சனி'},
    11: {'name': 'கும்பம்', 'name_en': 'Aquarius', 'symbol': '♒', 'element': 'காற்று', 'ruler': 'சனி'},
    12: {'name': 'மீனம்', 'name_en': 'Pisces', 'symbol': '♓', 'element': 'நீர்', 'ruler': 'குரு'},
}

# Planet data with average speeds and colors
PLANET_TRANSIT_DATA = {
    'Sun': {
        'tamil': 'சூரியன்',
        'symbol': '☉',
        'color': '#FF6B35',
        'avg_daily_motion': 0.9856,  # degrees per day
        'sign_duration_days': 30,
        'can_retrograde': False
    },
    'Moon': {
        'tamil': 'சந்திரன்',
        'symbol': '☽',
        'color': '#E8E8E8',
        'avg_daily_motion': 13.176,
        'sign_duration_days': 2.5,
        'can_retrograde': False
    },
    'Mars': {
        'tamil': 'செவ்வாய்',
        'symbol': '♂',
        'color': '#DC143C',
        'avg_daily_motion': 0.524,
        'sign_duration_days': 45,
        'can_retrograde': True,
        'retrograde_duration': 72
    },
    'Mercury': {
        'tamil': 'புதன்',
        'symbol': '☿',
        'color': '#32CD32',
        'avg_daily_motion': 1.383,
        'sign_duration_days': 25,
        'can_retrograde': True,
        'retrograde_duration': 21
    },
    'Jupiter': {
        'tamil': 'குரு',
        'symbol': '♃',
        'color': '#FFD700',
        'avg_daily_motion': 0.083,
        'sign_duration_days': 365,
        'can_retrograde': True,
        'retrograde_duration': 120
    },
    'Venus': {
        'tamil': 'சுக்கிரன்',
        'symbol': '♀',
        'color': '#FF69B4',
        'avg_daily_motion': 1.2,
        'sign_duration_days': 30,
        'can_retrograde': True,
        'retrograde_duration': 42
    },
    'Saturn': {
        'tamil': 'சனி',
        'symbol': '♄',
        'color': '#4169E1',
        'avg_daily_motion': 0.033,
        'sign_duration_days': 912,  # ~2.5 years
        'can_retrograde': True,
        'retrograde_duration': 140
    },
    'Rahu': {
        'tamil': 'ராகு',
        'symbol': '☊',
        'color': '#9370DB',
        'avg_daily_motion': -0.053,  # retrograde motion
        'sign_duration_days': 547,  # ~18 months
        'can_retrograde': False  # Always retrograde
    },
    'Ketu': {
        'tamil': 'கேது',
        'symbol': '☋',
        'color': '#8B4513',
        'avg_daily_motion': -0.053,
        'sign_duration_days': 547,
        'can_retrograde': False
    }
}

# Retrograde periods for 2024-2025 (approximate)
RETROGRADE_PERIODS = {
    'Mercury': [
        {'start': '2024-12-13', 'end': '2025-01-02', 'sign': 9},
        {'start': '2025-03-14', 'end': '2025-04-07', 'sign': 12},
        {'start': '2025-07-18', 'end': '2025-08-11', 'sign': 5},
        {'start': '2025-11-09', 'end': '2025-11-29', 'sign': 8},
    ],
    'Venus': [
        {'start': '2025-03-01', 'end': '2025-04-12', 'sign': 12},
    ],
    'Mars': [
        {'start': '2024-12-06', 'end': '2025-02-23', 'sign': 4},
    ],
    'Jupiter': [
        {'start': '2024-10-09', 'end': '2025-02-04', 'sign': 3},
        {'start': '2025-11-11', 'end': '2026-03-10', 'sign': 4},
    ],
    'Saturn': [
        {'start': '2025-07-13', 'end': '2025-11-27', 'sign': 12},
    ]
}


class TransitsMapService:
    """Service for live planetary transit data"""

    def __init__(self, ephemeris=None):
        self.ephemeris = ephemeris

    def get_transits_map(self, lat: float, lon: float, user_rasi: str = "") -> Dict:
        """Get comprehensive transits map data"""
        now = datetime.now()
        today = date.today()

        # Get current planetary positions
        planets = self._get_current_positions(now, lat, lon)

        # Calculate moon transit details
        moon_transit = self._get_moon_transit_details(planets.get('Moon', {}), now)

        # Get retrograde status for all planets
        retrogrades = self._get_retrograde_status(today)

        # Get upcoming sign changes
        upcoming_transits = self._get_upcoming_transits(planets, now)

        # Generate alerts based on user's rasi
        alerts = self._generate_transit_alerts(planets, user_rasi, now)

        # Get sky positions for visualization (angles)
        sky_positions = self._calculate_sky_positions(planets)

        return {
            'timestamp': now.isoformat(),
            'planets': planets,
            'moon_transit': moon_transit,
            'retrogrades': retrogrades,
            'upcoming_transits': upcoming_transits,
            'alerts': alerts,
            'sky_positions': sky_positions,
            'current_nakshatra': self._get_moon_nakshatra(planets.get('Moon', {})),
            'auspicious_time': self._get_current_muhurtham(now)
        }

    def _get_current_positions(self, now: datetime, lat: float, lon: float) -> Dict:
        """Calculate current planetary positions"""
        positions = {}

        # Try ephemeris first
        if self.ephemeris:
            try:
                eph_positions = self.ephemeris.get_planet_positions(now, lat, lon)
                if eph_positions:
                    for planet, data in eph_positions.items():
                        if planet in PLANET_TRANSIT_DATA:
                            sign = data.get('sign', 1)
                            degree = data.get('degrees', 0)
                            positions[planet] = self._format_planet_position(
                                planet, sign, degree, now
                            )
                    if positions:
                        return positions
            except:
                pass

        # Fallback: estimate positions
        return self._estimate_positions(now)

    def _estimate_positions(self, now: datetime) -> Dict:
        """Estimate planetary positions based on average motion"""
        positions = {}
        base_date = datetime(2024, 1, 1)
        days_elapsed = (now - base_date).days + (now.hour / 24)

        # Base positions on Jan 1, 2024 (approximate)
        base_positions = {
            'Sun': 260,      # Sagittarius
            'Moon': 0,       # Varies daily
            'Mars': 270,     # Capricorn
            'Mercury': 250,  # Sagittarius
            'Jupiter': 45,   # Taurus
            'Venus': 240,    # Scorpio
            'Saturn': 330,   # Aquarius
            'Rahu': 25,      # Aries
            'Ketu': 205,     # Libra
        }

        for planet, data in PLANET_TRANSIT_DATA.items():
            base = base_positions.get(planet, 0)
            motion = data['avg_daily_motion'] * days_elapsed
            current_degree = (base + motion) % 360

            sign = int(current_degree / 30) + 1
            degree_in_sign = current_degree % 30

            positions[planet] = self._format_planet_position(
                planet, sign, degree_in_sign, now
            )

        return positions

    def _format_planet_position(self, planet: str, sign: int, degree: float, now: datetime) -> Dict:
        """Format planet position data"""
        planet_data = PLANET_TRANSIT_DATA.get(planet, {})
        rasi_data = RASI_DATA.get(sign, {})

        # Calculate time until next sign
        degrees_remaining = 30 - degree
        daily_motion = abs(planet_data.get('avg_daily_motion', 1))
        hours_to_next = (degrees_remaining / daily_motion) * 24 if daily_motion > 0 else 0

        # Check if retrograde
        is_retrograde = self._is_currently_retrograde(planet, now.date())

        return {
            'name': planet,
            'tamil': planet_data.get('tamil', planet),
            'symbol': planet_data.get('symbol', ''),
            'color': planet_data.get('color', '#888'),
            'sign': sign,
            'sign_name': rasi_data.get('name', ''),
            'sign_symbol': rasi_data.get('symbol', ''),
            'degree': round(degree, 2),
            'degree_display': f"{int(degree)}° {int((degree % 1) * 60)}'",
            'is_retrograde': is_retrograde,
            'hours_to_next_sign': round(hours_to_next, 1),
            'motion': 'வக்ர' if is_retrograde else 'நேர்',  # Retrograde or Direct
            'speed': 'மெதுவாக' if daily_motion < 0.5 else 'சாதாரணம்' if daily_motion < 2 else 'வேகமாக'
        }

    def _get_moon_transit_details(self, moon_pos: Dict, now: datetime) -> Dict:
        """Get detailed moon transit information"""
        if not moon_pos:
            return {}

        current_sign = moon_pos.get('sign', 1)
        degree = moon_pos.get('degree', 0)
        hours_remaining = moon_pos.get('hours_to_next_sign', 0)

        # Calculate next sign
        next_sign = (current_sign % 12) + 1
        next_rasi = RASI_DATA.get(next_sign, {})

        # Time formatting
        hours = int(hours_remaining)
        minutes = int((hours_remaining % 1) * 60)

        # Determine moon phase (approximate)
        day_of_month = now.day
        if day_of_month <= 7:
            phase = 'வளர்பிறை'  # Waxing
            phase_icon = '🌒'
        elif day_of_month <= 14:
            phase = 'வளர்பிறை'
            phase_icon = '🌓'
        elif day_of_month <= 21:
            phase = 'தேய்பிறை'  # Waning
            phase_icon = '🌔'
        else:
            phase = 'தேய்பிறை'
            phase_icon = '🌘'

        # Emotional/energy indicator based on current sign
        sign_energy = self._get_moon_sign_energy(current_sign)

        return {
            'current_sign': current_sign,
            'current_sign_name': RASI_DATA.get(current_sign, {}).get('name', ''),
            'current_sign_symbol': RASI_DATA.get(current_sign, {}).get('symbol', ''),
            'degree': round(degree, 2),
            'next_sign': next_sign,
            'next_sign_name': next_rasi.get('name', ''),
            'next_sign_symbol': next_rasi.get('symbol', ''),
            'time_to_transit': {
                'hours': hours,
                'minutes': minutes,
                'display': f"{hours} மணி {minutes} நிமிடம்",
                'total_hours': round(hours_remaining, 1)
            },
            'phase': phase,
            'phase_icon': phase_icon,
            'energy': sign_energy,
            'transit_message': self._get_moon_transit_message(current_sign, next_sign, hours)
        }

    def _get_moon_sign_energy(self, sign: int) -> Dict:
        """Get energy/mood based on moon's sign"""
        energies = {
            1: {'level': 'high', 'mood': 'தீவிரம்', 'color': '#ef4444', 'icon': '🔥'},
            2: {'level': 'stable', 'mood': 'நிலையானது', 'color': '#22c55e', 'icon': '🌿'},
            3: {'level': 'active', 'mood': 'சுறுசுறுப்பு', 'color': '#eab308', 'icon': '💨'},
            4: {'level': 'emotional', 'mood': 'உணர்வுபூர்வம்', 'color': '#3b82f6', 'icon': '💧'},
            5: {'level': 'confident', 'mood': 'தன்னம்பிக்கை', 'color': '#f97316', 'icon': '👑'},
            6: {'level': 'analytical', 'mood': 'பகுப்பாய்வு', 'color': '#84cc16', 'icon': '🔍'},
            7: {'level': 'balanced', 'mood': 'சமநிலை', 'color': '#ec4899', 'icon': '⚖️'},
            8: {'level': 'intense', 'mood': 'ஆழமான', 'color': '#7c3aed', 'icon': '🦂'},
            9: {'level': 'optimistic', 'mood': 'நம்பிக்கை', 'color': '#f59e0b', 'icon': '🏹'},
            10: {'level': 'focused', 'mood': 'கவனமான', 'color': '#6b7280', 'icon': '🎯'},
            11: {'level': 'innovative', 'mood': 'புதுமையான', 'color': '#06b6d4', 'icon': '💡'},
            12: {'level': 'intuitive', 'mood': 'உள்ளுணர்வு', 'color': '#8b5cf6', 'icon': '🔮'},
        }
        return energies.get(sign, {'level': 'neutral', 'mood': 'சாதாரணம்', 'color': '#888', 'icon': '⭐'})

    def _get_moon_transit_message(self, current: int, next_sign: int, hours: int) -> str:
        """Generate transit notification message"""
        next_name = RASI_DATA.get(next_sign, {}).get('name', '')
        energy = self._get_moon_sign_energy(next_sign)

        if hours <= 2:
            return f"🌙 சந்திரன் {next_name} இல் நுழையப்போகிறார் - {energy['mood']} நேரம் வருகிறது!"
        elif hours <= 6:
            return f"சந்திரன் {hours} மணி நேரத்தில் {next_name} ராசிக்கு மாறும்"
        else:
            return f"சந்திரன் தற்போது நிலையாக உள்ளது"

    def _get_retrograde_status(self, today: date) -> List[Dict]:
        """Get current retrograde status for all planets using v3.0 penalties"""
        retrogrades = []

        # Get v3.0 retrograde penalties if available
        retro_penalties = {}
        if AstroPercentEngine:
            retro_penalties = AstroPercentEngine.RETROGRADE_PENALTIES_V3

        for planet, periods in RETROGRADE_PERIODS.items():
            planet_data = PLANET_TRANSIT_DATA.get(planet, {})

            for period in periods:
                start = datetime.strptime(period['start'], '%Y-%m-%d').date()
                end = datetime.strptime(period['end'], '%Y-%m-%d').date()

                # Get v3.0 penalty for this planet
                penalty = retro_penalties.get(planet, -0.5)
                impact_level = 'high' if abs(penalty) >= 1.0 else 'medium' if abs(penalty) >= 0.7 else 'low'

                # Currently retrograde
                if start <= today <= end:
                    days_remaining = (end - today).days
                    retrogrades.append({
                        'planet': planet,
                        'tamil': planet_data.get('tamil', planet),
                        'symbol': planet_data.get('symbol', ''),
                        'color': planet_data.get('color', '#888'),
                        'status': 'retrograde',
                        'status_tamil': 'வக்ரம்',
                        'sign': period['sign'],
                        'sign_name': RASI_DATA.get(period['sign'], {}).get('name', ''),
                        'days_remaining': days_remaining,
                        'end_date': period['end'],
                        'message': f"{planet_data.get('tamil', planet)} வக்ரம் - {days_remaining} நாட்கள் மீதம்",
                        'v3_penalty': penalty,
                        'impact_level': impact_level,
                        'impact_tamil': 'அதிக தாக்கம்' if impact_level == 'high' else 'மிதமான தாக்கம்' if impact_level == 'medium' else 'குறைந்த தாக்கம்'
                    })
                    break

                # Upcoming retrograde
                elif start > today and (start - today).days <= 30:
                    days_until = (start - today).days
                    retrogrades.append({
                        'planet': planet,
                        'tamil': planet_data.get('tamil', planet),
                        'symbol': planet_data.get('symbol', ''),
                        'color': planet_data.get('color', '#888'),
                        'status': 'upcoming',
                        'status_tamil': 'வரவிருக்கிறது',
                        'sign': period['sign'],
                        'sign_name': RASI_DATA.get(period['sign'], {}).get('name', ''),
                        'days_until': days_until,
                        'start_date': period['start'],
                        'message': f"{planet_data.get('tamil', planet)} வக்ரம் {days_until} நாட்களில் தொடங்கும்",
                        'v3_penalty': penalty,
                        'impact_level': impact_level,
                        'impact_tamil': 'அதிக தாக்கம்' if impact_level == 'high' else 'மிதமான தாக்கம்' if impact_level == 'medium' else 'குறைந்த தாக்கம்'
                    })
                    break

        return retrogrades

    def _is_currently_retrograde(self, planet: str, today: date) -> bool:
        """Check if a planet is currently retrograde"""
        if planet in ['Rahu', 'Ketu']:
            return True  # Always retrograde

        periods = RETROGRADE_PERIODS.get(planet, [])
        for period in periods:
            start = datetime.strptime(period['start'], '%Y-%m-%d').date()
            end = datetime.strptime(period['end'], '%Y-%m-%d').date()
            if start <= today <= end:
                return True
        return False

    def _get_upcoming_transits(self, planets: Dict, now: datetime) -> List[Dict]:
        """Get upcoming significant transits"""
        upcoming = []

        for planet_name, pos in planets.items():
            hours_to_next = pos.get('hours_to_next_sign', 0)

            # Only include transits happening within 48 hours
            if hours_to_next <= 48:
                current_sign = pos.get('sign', 1)
                next_sign = (current_sign % 12) + 1
                next_rasi = RASI_DATA.get(next_sign, {})

                transit_time = now + timedelta(hours=hours_to_next)

                upcoming.append({
                    'planet': planet_name,
                    'tamil': pos.get('tamil', planet_name),
                    'symbol': pos.get('symbol', ''),
                    'color': pos.get('color', '#888'),
                    'from_sign': current_sign,
                    'from_sign_name': RASI_DATA.get(current_sign, {}).get('name', ''),
                    'to_sign': next_sign,
                    'to_sign_name': next_rasi.get('name', ''),
                    'to_sign_symbol': next_rasi.get('symbol', ''),
                    'hours_remaining': round(hours_to_next, 1),
                    'transit_time': transit_time.isoformat(),
                    'priority': 'high' if planet_name == 'Moon' else 'medium'
                })

        # Sort by time remaining
        upcoming.sort(key=lambda x: x['hours_remaining'])
        return upcoming[:5]  # Return top 5

    def _generate_transit_alerts(self, planets: Dict, user_rasi: str, now: datetime) -> List[Dict]:
        """Generate personalized transit alerts"""
        alerts = []

        # Moon transit alert
        moon = planets.get('Moon', {})
        if moon:
            hours = moon.get('hours_to_next_sign', 0)
            if hours <= 3:
                next_sign = (moon.get('sign', 1) % 12) + 1
                next_name = RASI_DATA.get(next_sign, {}).get('name', '')
                energy = self._get_moon_sign_energy(next_sign)

                alerts.append({
                    'type': 'moon_transit',
                    'priority': 'high',
                    'icon': '🌙',
                    'title': f'சந்திரன் {next_name} நுழைவு',
                    'message': f'{int(hours)} மணி நேரத்தில் {energy["mood"]} காலம் வருகிறது!',
                    'color': energy['color'],
                    'action': 'view_moon'
                })

        # Retrograde alerts
        retrogrades = self._get_retrograde_status(now.date())
        for retro in retrogrades:
            if retro['status'] == 'retrograde':
                alerts.append({
                    'type': 'retrograde',
                    'priority': 'medium',
                    'icon': '⚠️',
                    'title': f'{retro["tamil"]} வக்ரம்',
                    'message': retro['message'],
                    'color': retro['color'],
                    'action': 'view_retrograde'
                })

        # Sun transit (once a month)
        sun = planets.get('Sun', {})
        if sun and sun.get('hours_to_next_sign', 0) <= 24:
            next_sign = (sun.get('sign', 1) % 12) + 1
            alerts.append({
                'type': 'sun_transit',
                'priority': 'medium',
                'icon': '☀️',
                'title': 'சூரிய பெயர்ச்சி',
                'message': f'சூரியன் {RASI_DATA.get(next_sign, {}).get("name", "")} ராசிக்கு மாறப்போகிறார்',
                'color': '#FF6B35',
                'action': 'view_sun'
            })

        return alerts[:5]

    def _calculate_sky_positions(self, planets: Dict) -> List[Dict]:
        """Calculate angular positions for sky visualization"""
        sky = []
        for planet_name, pos in planets.items():
            sign = pos.get('sign', 1)
            degree = pos.get('degree', 0)

            # Calculate total degrees from 0 (Aries)
            total_degrees = ((sign - 1) * 30) + degree
            # Convert to angle for visualization (0 at top, clockwise)
            angle = (total_degrees - 90) % 360

            sky.append({
                'planet': planet_name,
                'tamil': pos.get('tamil', planet_name),
                'symbol': pos.get('symbol', ''),
                'color': pos.get('color', '#888'),
                'angle': round(angle, 1),
                'radius_factor': 0.7 if planet_name in ['Sun', 'Moon'] else 0.85,
                'size': 'large' if planet_name in ['Sun', 'Moon', 'Jupiter'] else 'medium'
            })

        return sky

    def _get_moon_nakshatra(self, moon_pos: Dict) -> Dict:
        """Get current moon nakshatra"""
        if not moon_pos:
            return {}

        sign = moon_pos.get('sign', 1)
        degree = moon_pos.get('degree', 0)

        # Calculate total degrees
        total_degrees = ((sign - 1) * 30) + degree

        # Each nakshatra spans 13°20' (13.333 degrees)
        nakshatra_num = int(total_degrees / 13.333) + 1

        nakshatras = [
            'அசுவினி', 'பரணி', 'கார்த்திகை', 'ரோகிணி', 'மிருகசீரிஷம்',
            'திருவாதிரை', 'புனர்பூசம்', 'பூசம்', 'ஆயில்யம்', 'மகம்',
            'பூரம்', 'உத்திரம்', 'ஹஸ்தம்', 'சித்திரை', 'சுவாதி',
            'விசாகம்', 'அனுஷம்', 'கேட்டை', 'மூலம்', 'பூராடம்',
            'உத்திராடம்', 'திருவோணம்', 'அவிட்டம்', 'சதயம்', 'பூரட்டாதி',
            'உத்திரட்டாதி', 'ரேவதி'
        ]

        nakshatra_name = nakshatras[min(nakshatra_num - 1, 26)]

        return {
            'number': nakshatra_num,
            'name': nakshatra_name,
            'pada': ((total_degrees % 13.333) / 3.333) + 1
        }

    def _get_current_muhurtham(self, now: datetime) -> Dict:
        """Get current muhurtham quality"""
        hour = now.hour

        # Simplified muhurtham based on time
        if 4 <= hour < 6:
            return {'name': 'பிரம்ம முகூர்த்தம்', 'quality': 'excellent', 'color': '#22c55e'}
        elif 6 <= hour < 8:
            return {'name': 'காலை முகூர்த்தம்', 'quality': 'good', 'color': '#84cc16'}
        elif 8 <= hour < 10:
            return {'name': 'பகல் முகூர்த்தம்', 'quality': 'average', 'color': '#eab308'}
        elif 10 <= hour < 12:
            return {'name': 'மத்தியானம்', 'quality': 'caution', 'color': '#f97316'}
        elif 12 <= hour < 14:
            return {'name': 'அபிஜித்', 'quality': 'good', 'color': '#84cc16'}
        elif 14 <= hour < 16:
            return {'name': 'பிற்பகல்', 'quality': 'average', 'color': '#eab308'}
        elif 16 <= hour < 18:
            return {'name': 'மாலை', 'quality': 'good', 'color': '#84cc16'}
        elif 18 <= hour < 20:
            return {'name': 'சந்தியா காலம்', 'quality': 'caution', 'color': '#f97316'}
        else:
            return {'name': 'இரவு', 'quality': 'rest', 'color': '#6b7280'}
