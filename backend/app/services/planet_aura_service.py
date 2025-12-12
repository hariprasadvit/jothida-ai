"""
Planet Aura Service - Calculate planet strengths for visualization
Provides data for the Aura Heatmap radial graph
Uses Astro-Percent Engine v3.0 for accurate calculations
"""

from datetime import datetime, date
from typing import Dict, List, Optional
import math

# Import Astro-Percent Engine v3.0
try:
    from .astro_percent_engine import AstroPercentEngine
except ImportError:
    AstroPercentEngine = None

# Planet data with colors, Tamil names, and base characteristics
PLANET_DATA = {
    'Sun': {
        'tamil': 'சூரியன்',
        'symbol': '☉',
        'color_strong': '#FF6B35',  # Vibrant orange
        'color_weak': '#FFB088',
        'color_afflicted': '#8B4513',
        'angle': 0,  # Position in radial chart (degrees)
        'domain': 'ஆன்மா',
        'domain_en': 'soul',
        'keywords': ['அதிகாரம்', 'உயிர்ச்சக்தி', 'தந்தை', 'அரசு'],
        'keywords_en': ['authority', 'vitality', 'father', 'government']
    },
    'Moon': {
        'tamil': 'சந்திரன்',
        'symbol': '☽',
        'color_strong': '#E8E8E8',  # Silver white
        'color_weak': '#B8B8B8',
        'color_afflicted': '#696969',
        'angle': 40,
        'domain': 'மனம்',
        'domain_en': 'mind',
        'keywords': ['உணர்வுகள்', 'தாய்', 'மனம்', 'பொது'],
        'keywords_en': ['emotions', 'mother', 'mind', 'public']
    },
    'Mars': {
        'tamil': 'செவ்வாய்',
        'symbol': '♂',
        'color_strong': '#DC143C',  # Crimson red
        'color_weak': '#F08080',
        'color_afflicted': '#8B0000',
        'angle': 80,
        'domain': 'சக்தி',
        'domain_en': 'energy',
        'keywords': ['தைரியம்', 'சொத்து', 'உடன்பிறப்பு', 'செயல்'],
        'keywords_en': ['courage', 'property', 'siblings', 'action']
    },
    'Mercury': {
        'tamil': 'புதன்',
        'symbol': '☿',
        'color_strong': '#32CD32',  # Lime green
        'color_weak': '#90EE90',
        'color_afflicted': '#556B2F',
        'angle': 120,
        'domain': 'அறிவு',
        'domain_en': 'intellect',
        'keywords': ['தொடர்பு', 'வியாபாரம்', 'கல்வி', 'திறமை'],
        'keywords_en': ['communication', 'business', 'education', 'skills']
    },
    'Jupiter': {
        'tamil': 'குரு',
        'symbol': '♃',
        'color_strong': '#FFD700',  # Gold
        'color_weak': '#FFEC8B',
        'color_afflicted': '#B8860B',
        'angle': 160,
        'domain': 'ஞானம்',
        'domain_en': 'wisdom',
        'keywords': ['ஞானம்', 'குழந்தைகள்', 'அதிர்ஷ்டம்', 'தர்மம்'],
        'keywords_en': ['wisdom', 'children', 'luck', 'dharma']
    },
    'Venus': {
        'tamil': 'சுக்கிரன்',
        'symbol': '♀',
        'color_strong': '#FF69B4',  # Hot pink
        'color_weak': '#FFB6C1',
        'color_afflicted': '#C71585',
        'angle': 200,
        'domain': 'இன்பம்',
        'domain_en': 'pleasure',
        'keywords': ['காதல்', 'ஆடம்பரம்', 'கலை', 'வாழ்க்கைத்துணை'],
        'keywords_en': ['love', 'luxury', 'art', 'spouse']
    },
    'Saturn': {
        'tamil': 'சனி',
        'symbol': '♄',
        'color_strong': '#4169E1',  # Royal blue
        'color_weak': '#87CEEB',
        'color_afflicted': '#191970',
        'angle': 240,
        'domain': 'கர்மம்',
        'domain_en': 'karma',
        'keywords': ['ஒழுக்கம்', 'நீண்ட ஆயுள்', 'சேவை', 'தாமதம்'],
        'keywords_en': ['discipline', 'longevity', 'service', 'delays']
    },
    'Rahu': {
        'tamil': 'ராகு',
        'symbol': '☊',
        'color_strong': '#9370DB',  # Medium purple
        'color_weak': '#DDA0DD',
        'color_afflicted': '#4B0082',
        'angle': 280,
        'domain': 'ஆசைகள்',
        'domain_en': 'desires',
        'keywords': ['லட்சியம்', 'வெளிநாடு', 'ஆவேசம்', 'மாயை'],
        'keywords_en': ['ambition', 'foreign', 'obsession', 'illusion']
    },
    'Ketu': {
        'tamil': 'கேது',
        'symbol': '☋',
        'color_strong': '#8B4513',  # Saddle brown
        'color_weak': '#D2B48C',
        'color_afflicted': '#3D2314',
        'angle': 320,
        'domain': 'முக்தி',
        'domain_en': 'liberation',
        'keywords': ['ஆன்மீகம்', 'பற்றின்மை', 'பழைய கர்மம்', 'மோட்சம்'],
        'keywords_en': ['spirituality', 'detachment', 'past karma', 'moksha']
    }
}

# Planetary friendships for strength calculation
PLANETARY_FRIENDS = {
    'Sun': ['Moon', 'Mars', 'Jupiter'],
    'Moon': ['Sun', 'Mercury'],
    'Mars': ['Sun', 'Moon', 'Jupiter'],
    'Mercury': ['Sun', 'Venus'],
    'Jupiter': ['Sun', 'Moon', 'Mars'],
    'Venus': ['Mercury', 'Saturn'],
    'Saturn': ['Mercury', 'Venus'],
    'Rahu': ['Mercury', 'Venus', 'Saturn'],
    'Ketu': ['Mars', 'Jupiter']
}

PLANETARY_ENEMIES = {
    'Sun': ['Saturn', 'Venus', 'Rahu'],
    'Moon': ['Rahu', 'Ketu'],
    'Mars': ['Mercury'],
    'Mercury': ['Moon'],
    'Jupiter': ['Mercury', 'Venus'],
    'Venus': ['Sun', 'Moon'],
    'Saturn': ['Sun', 'Moon', 'Mars'],
    'Rahu': ['Sun', 'Moon'],
    'Ketu': ['Sun', 'Moon']
}

# Exaltation and debilitation signs
EXALTATION = {
    'Sun': 1, 'Moon': 2, 'Mars': 10, 'Mercury': 6,
    'Jupiter': 4, 'Venus': 12, 'Saturn': 7, 'Rahu': 3, 'Ketu': 9
}

DEBILITATION = {
    'Sun': 7, 'Moon': 8, 'Mars': 4, 'Mercury': 12,
    'Jupiter': 10, 'Venus': 6, 'Saturn': 1, 'Rahu': 9, 'Ketu': 3
}

# Own signs
OWN_SIGNS = {
    'Sun': [5],
    'Moon': [4],
    'Mars': [1, 8],
    'Mercury': [3, 6],
    'Jupiter': [9, 12],
    'Venus': [2, 7],
    'Saturn': [10, 11],
    'Rahu': [11],
    'Ketu': [8]
}


class PlanetAuraService:
    """Service to calculate planet strengths for Aura Heatmap visualization"""

    def __init__(self, jathagam_generator=None, ephemeris=None):
        self.jathagam_gen = jathagam_generator
        self.ephemeris = ephemeris

    def calculate_planet_aura(self, request) -> Dict:
        """Calculate planet strengths and aura data for visualization"""
        try:
            # Parse birth details
            birth_date = datetime.strptime(request.birth_date, '%Y-%m-%d').date()
            birth_time = request.birth_time if request.birth_time else "12:00"

            # Get birth chart positions
            chart_data = self._get_chart_positions(
                birth_date, birth_time,
                request.latitude, request.longitude
            )

            # Get current transit positions
            transit_data = self._get_transit_positions(
                request.latitude, request.longitude
            )

            # Calculate individual planet strengths
            planets = []
            total_strength = 0
            favorable_count = 0
            unfavorable_count = 0

            for planet_name, planet_info in PLANET_DATA.items():
                strength_data = self._calculate_planet_strength(
                    planet_name, chart_data, transit_data
                )

                # Determine influence type
                influence = 'neutral'
                if strength_data['strength'] >= 70:
                    influence = 'favorable'
                    favorable_count += 1
                elif strength_data['strength'] < 40:
                    influence = 'unfavorable'
                    unfavorable_count += 1

                # Get appropriate color based on strength
                if strength_data['strength'] >= 60:
                    color = planet_info['color_strong']
                elif strength_data['strength'] >= 40:
                    color = planet_info['color_weak']
                else:
                    color = planet_info['color_afflicted']

                planet_data = {
                    'name': planet_name,
                    'tamil': planet_info['tamil'],
                    'symbol': planet_info['symbol'],
                    'strength': strength_data['strength'],
                    'influence': influence,
                    'color': color,
                    'angle': planet_info['angle'],
                    'domain': planet_info['domain'],
                    'transit_effect': strength_data.get('transit_effect', 'neutral'),
                    'transit_boost': strength_data.get('transit_boost', 0),
                    'natal_sign': strength_data.get('natal_sign', 1),
                    'current_sign': strength_data.get('current_sign', 1),
                    'keywords': planet_info['keywords'],
                    'insight': self._generate_planet_insight(
                        planet_name, strength_data['strength'], influence
                    )
                }

                planets.append(planet_data)
                total_strength += strength_data['strength']

            # Calculate overall aura
            avg_strength = total_strength / len(PLANET_DATA)
            aura_level = self._determine_aura_level(avg_strength)

            # Get dominant planets (top 3 strongest)
            sorted_planets = sorted(planets, key=lambda x: x['strength'], reverse=True)
            dominant = sorted_planets[:3]

            # Get challenged planets (weakest)
            challenged = sorted_planets[-2:]

            return {
                'planets': planets,
                'overall': {
                    'aura_score': round(avg_strength),
                    'aura_level': aura_level['level'],
                    'aura_label': aura_level['label'],
                    'aura_tamil': aura_level['tamil'],
                    'aura_color': aura_level['color'],
                    'favorable_count': favorable_count,
                    'unfavorable_count': unfavorable_count,
                    'neutral_count': 9 - favorable_count - unfavorable_count
                },
                'dominant_planets': [
                    {'name': p['name'], 'tamil': p['tamil'], 'strength': p['strength']}
                    for p in dominant
                ],
                'challenged_planets': [
                    {'name': p['name'], 'tamil': p['tamil'], 'strength': p['strength']}
                    for p in challenged
                ],
                'transit_summary': self._generate_transit_summary(planets),
                'generated_at': datetime.now().isoformat()
            }

        except Exception as e:
            # Return fallback data
            return self._generate_fallback_aura(str(e))

    def _get_chart_positions(self, birth_date, birth_time, lat, lon) -> Dict:
        """Get natal chart planetary positions"""
        if self.jathagam_gen:
            try:
                chart = self.jathagam_gen.generate({
                    'name': 'User',
                    'date': birth_date.strftime('%Y-%m-%d'),
                    'time': birth_time,
                    'place': 'Location',
                    'latitude': lat,
                    'longitude': lon
                })
                return chart.get('planets', {})
            except:
                pass

        # Fallback calculation based on birth date
        return self._estimate_positions(birth_date)

    def _get_transit_positions(self, lat, lon) -> Dict:
        """Get current transit planetary positions"""
        if self.ephemeris:
            try:
                positions = self.ephemeris.get_planet_positions(
                    datetime.now(), lat, lon
                )
                return positions
            except:
                pass

        # Estimate current positions
        return self._estimate_positions(date.today())

    def _estimate_positions(self, ref_date) -> Dict:
        """Estimate planetary positions based on date"""
        # Simple estimation based on average planetary speeds
        day_of_year = ref_date.timetuple().tm_yday
        year = ref_date.year

        base_offset = (year - 2000) * 365 + day_of_year

        positions = {}
        # Average daily motion (approximate)
        speeds = {
            'Sun': 1.0, 'Moon': 13.2, 'Mars': 0.52,
            'Mercury': 1.2, 'Jupiter': 0.083,
            'Venus': 1.2, 'Saturn': 0.033,
            'Rahu': -0.053, 'Ketu': -0.053
        }

        for planet, speed in speeds.items():
            # Calculate approximate sign (1-12)
            degrees = (base_offset * speed) % 360
            sign = int(degrees / 30) + 1
            positions[planet] = {'sign': sign, 'degrees': degrees % 30}

        return positions

    def _calculate_planet_strength(self, planet_name: str,
                                    natal: Dict, transit: Dict) -> Dict:
        """Calculate strength score for a planet (0-100) using v3.0 tables"""
        strength = 50  # Base strength

        # Get natal position
        natal_pos = natal.get(planet_name, {})
        natal_sign = natal_pos.get('sign', 1) if isinstance(natal_pos, dict) else 1

        # Get transit position
        transit_pos = transit.get(planet_name, {})
        current_sign = transit_pos.get('sign', 1) if isinstance(transit_pos, dict) else 1

        # 1. Dignity using v3.0 table if available
        dignity_score = 5  # Neutral default
        if AstroPercentEngine:
            if natal_sign == EXALTATION.get(planet_name):
                dignity_score = AstroPercentEngine.DIGNITY_TABLE_V3.get('exalted', 10)
            elif natal_sign == DEBILITATION.get(planet_name):
                dignity_score = AstroPercentEngine.DIGNITY_TABLE_V3.get('debilitated', 1)
            elif natal_sign in OWN_SIGNS.get(planet_name, []):
                dignity_score = AstroPercentEngine.DIGNITY_TABLE_V3.get('own', 9)
            else:
                dignity_score = AstroPercentEngine.DIGNITY_TABLE_V3.get('neutral', 5)
        else:
            if natal_sign == EXALTATION.get(planet_name):
                dignity_score = 10
            elif natal_sign == DEBILITATION.get(planet_name):
                dignity_score = 1
            elif natal_sign in OWN_SIGNS.get(planet_name, []):
                dignity_score = 9

        # Scale dignity to strength points (0-10 -> 0-25)
        strength += (dignity_score - 5) * 5

        # 2. Transit effects using v3.0 tables
        transit_boost = 0
        transit_effect = 'neutral'
        house_from_natal = ((current_sign - natal_sign) % 12) + 1

        # Use v3.0 Jupiter transit table logic for Jupiter
        if planet_name == 'Jupiter' and AstroPercentEngine:
            jupiter_score = 5  # Default
            for category, config in AstroPercentEngine.JUPITER_TRANSIT_TABLE_V3.items():
                if house_from_natal in config['houses']:
                    jupiter_score = config['score']
                    break
            transit_boost = (jupiter_score - 5) * 2
            transit_effect = 'favorable' if jupiter_score >= 6 else 'challenging' if jupiter_score <= 4 else 'neutral'

        # Use v3.0 Saturn transit rules for Saturn
        elif planet_name == 'Saturn' and AstroPercentEngine:
            saturn_rules = AstroPercentEngine.SATURN_TRANSIT_RULES_V3
            if house_from_natal in saturn_rules['sade_sati']['houses']:
                transit_boost = saturn_rules['sade_sati']['penalty'] * 3
                transit_effect = 'challenging'
            elif house_from_natal in saturn_rules['kantaka']['houses']:
                transit_boost = saturn_rules['kantaka']['penalty'] * 3
                transit_effect = 'challenging'
            elif house_from_natal in saturn_rules['ashtama']['houses']:
                transit_boost = saturn_rules['ashtama']['penalty'] * 3
                transit_effect = 'challenging'
            elif house_from_natal in saturn_rules['favorable']['houses']:
                transit_boost = saturn_rules['favorable']['bonus'] * 3
                transit_effect = 'favorable'
        else:
            # General transit effects
            if house_from_natal in [1, 5, 9]:  # Trikona
                transit_boost = 12
                transit_effect = 'favorable'
            elif house_from_natal in [3, 6, 10, 11]:  # Good houses
                transit_boost = 8
                transit_effect = 'favorable'
            elif house_from_natal in [4, 7, 8, 12]:  # Challenging
                transit_boost = -8
                transit_effect = 'challenging'

        strength += transit_boost

        # 3. Current transit dignity
        if current_sign == EXALTATION.get(planet_name):
            strength += 10
        elif current_sign == DEBILITATION.get(planet_name):
            strength -= 10

        # 4. Add some variation based on specific combinations
        variation = (hash(f"{planet_name}{natal_sign}{current_sign}") % 16) - 8
        strength += variation

        # Ensure within bounds
        strength = max(10, min(95, strength))

        return {
            'strength': round(strength),
            'natal_sign': natal_sign,
            'current_sign': current_sign,
            'transit_effect': transit_effect,
            'transit_boost': transit_boost,
            'dignity_score': dignity_score
        }

    def _determine_aura_level(self, avg_strength: float) -> Dict:
        """Determine overall aura level based on average strength"""
        if avg_strength >= 75:
            return {
                'level': 'radiant',
                'label': 'Radiant Aura',
                'tamil': 'ஒளிர்வான் ஒளி',
                'color': '#FFD700'
            }
        elif avg_strength >= 60:
            return {
                'level': 'strong',
                'label': 'Strong Aura',
                'tamil': 'வலிமையான ஒளி',
                'color': '#32CD32'
            }
        elif avg_strength >= 45:
            return {
                'level': 'balanced',
                'label': 'Balanced Aura',
                'tamil': 'சமநிலை ஒளி',
                'color': '#4169E1'
            }
        elif avg_strength >= 30:
            return {
                'level': 'developing',
                'label': 'Developing Aura',
                'tamil': 'வளரும் ஒளி',
                'color': '#FFA500'
            }
        else:
            return {
                'level': 'challenged',
                'label': 'Needs Strengthening',
                'tamil': 'பலப்படுத்த வேண்டும்',
                'color': '#DC143C'
            }

    def _generate_planet_insight(self, planet: str, strength: int,
                                  influence: str) -> str:
        """Generate brief insight for each planet in Tamil"""
        insights = {
            'Sun': {
                'favorable': 'தலைமைப் பண்புகள் ஒளிர்கின்றன',
                'unfavorable': 'தன்னம்பிக்கையை வளர்க்கவும்',
                'neutral': 'நிலையான உயிர்ச்சக்தி மற்றும் அதிகாரம்'
            },
            'Moon': {
                'favorable': 'உணர்வு சமநிலை மற்றும் உள்ளுணர்வு உச்சத்தில்',
                'unfavorable': 'மனதிற்கு அமைதி தேவை',
                'neutral': 'உணர்வுகள் மிதமான நிலையில்'
            },
            'Mars': {
                'favorable': 'உயர் ஆற்றல் மற்றும் தைரியம் உள்ளது',
                'unfavorable': 'ஆற்றலை கவனமாக பயன்படுத்தவும்',
                'neutral': 'செயல் சார்ந்த ஆனால் அளவான'
            },
            'Mercury': {
                'favorable': 'சிறந்த தொடர்பு காலம்',
                'unfavorable': 'பேசும் முன் சிந்திக்கவும்',
                'neutral': 'அறிவுத்திறன் சாதாரண நிலையில்'
            },
            'Jupiter': {
                'favorable': 'ஞானமும் அதிர்ஷ்டமும் துணை நிற்கின்றன',
                'unfavorable': 'பெரியோர் வழிகாட்டுதல் பெறவும்',
                'neutral': 'வளர்ச்சி வாய்ப்புகள் உள்ளன'
            },
            'Venus': {
                'favorable': 'காதலும் படைப்பாற்றலும் செழிக்கின்றன',
                'unfavorable': 'உறவுகளுக்கு கவனம் தேவை',
                'neutral': 'இன்பங்கள் மிதமாக'
            },
            'Saturn': {
                'favorable': 'ஒழுக்கம் வெகுமதி அளிக்கிறது',
                'unfavorable': 'பொறுமை முக்கியம்',
                'neutral': 'கர்மம் படிப்படியாக வெளிப்படுகிறது'
            },
            'Rahu': {
                'favorable': 'லட்சியங்கள் திசை காண்கின்றன',
                'unfavorable': 'குறுக்கு வழிகளை தவிர்க்கவும்',
                'neutral': 'ஆசைகளுக்கு தெளிவு தேவை'
            },
            'Ketu': {
                'favorable': 'ஆன்மீக உணர்வுகள் ஆழமாகின்றன',
                'unfavorable': 'பொருள் உலகத்துடன் இணையவும்',
                'neutral': 'பழைய கர்மம் செயல்படுகிறது'
            }
        }

        return insights.get(planet, {}).get(influence, 'ஆற்றல் மாற்றத்தில் உள்ளது')

    def _generate_transit_summary(self, planets: List[Dict]) -> str:
        """Generate a summary of current transits in Tamil"""
        favorable = [p['tamil'] for p in planets if p['transit_effect'] == 'favorable']
        challenging = [p['tamil'] for p in planets if p['transit_effect'] == 'challenging']

        if len(favorable) > len(challenging):
            return f"தற்போது {', '.join(favorable[:2])} இலிருந்து நல்ல கோச்சாரம்"
        elif len(challenging) > len(favorable):
            return f"{', '.join(challenging[:2])} கோச்சாரம் சவாலானது - பரிகாரம் உதவும்"
        else:
            return "கலவையான கோச்சார தாக்கம் - சமநிலையான அணுகுமுறை நல்லது"

    def _generate_fallback_aura(self, error: str = "") -> Dict:
        """Generate fallback aura data when calculation fails"""
        planets = []
        for planet_name, info in PLANET_DATA.items():
            strength = 50 + (hash(planet_name) % 30)
            planets.append({
                'name': planet_name,
                'tamil': info['tamil'],
                'symbol': info['symbol'],
                'strength': strength,
                'influence': 'neutral',
                'color': info['color_weak'],
                'angle': info['angle'],
                'domain': info['domain'],
                'transit_effect': 'neutral',
                'transit_boost': 0,
                'keywords': info['keywords'],
                'insight': 'Energy being evaluated'
            })

        return {
            'planets': planets,
            'overall': {
                'aura_score': 55,
                'aura_level': 'balanced',
                'aura_label': 'Balanced Aura',
                'aura_tamil': 'சமநிலை ஒளி',
                'aura_color': '#4169E1',
                'favorable_count': 3,
                'unfavorable_count': 2,
                'neutral_count': 4
            },
            'dominant_planets': [],
            'challenged_planets': [],
            'transit_summary': 'Transit data loading',
            'generated_at': datetime.now().isoformat(),
            'fallback': True
        }
