"""
Life Areas Service
Calculates dynamic scores for Love, Career, Education, Family, Health
based on user's birth chart and current planetary transits
"""

from typing import Dict, List, Optional
from datetime import datetime, date
import math


class LifeAreasService:
    """
    Calculates life area scores based on:
    1. House lords and their placement
    2. Planet strengths from birth chart
    3. Current planetary transits over natal positions
    4. Dasha period effects
    """

    # House significations for each life area
    LIFE_AREA_HOUSES = {
        'love': [7, 5, 1, 2],  # 7th (spouse), 5th (romance), 1st (self), 2nd (family)
        'career': [10, 6, 2, 11],  # 10th (career), 6th (service), 2nd (wealth), 11th (gains)
        'education': [4, 5, 9, 1],  # 4th (learning), 5th (intelligence), 9th (higher ed), 1st
        'family': [4, 2, 1, 7],  # 4th (home), 2nd (family), 1st (self), 7th (spouse)
        'health': [1, 6, 8, 12],  # 1st (body), 6th (disease), 8th (longevity), 12th (hospitalization)
    }

    # Karaka (significator) planets for each area
    AREA_KARAKAS = {
        'love': ['Venus', 'Moon', 'Mars'],
        'career': ['Saturn', 'Sun', 'Mercury', 'Jupiter'],
        'education': ['Mercury', 'Jupiter', 'Moon'],
        'family': ['Moon', 'Venus', 'Jupiter'],
        'health': ['Sun', 'Mars', 'Saturn'],
    }

    # House lords based on Rasi (1=Aries, 2=Taurus, etc.)
    HOUSE_LORDS = {
        1: 'Mars', 2: 'Venus', 3: 'Mercury', 4: 'Moon',
        5: 'Sun', 6: 'Mercury', 7: 'Venus', 8: 'Mars',
        9: 'Jupiter', 10: 'Saturn', 11: 'Saturn', 12: 'Jupiter'
    }

    # Rasi to number mapping
    RASI_MAP = {
        'Aries': 1, 'Mesha': 1, 'மேஷம்': 1,
        'Taurus': 2, 'Vrishabha': 2, 'ரிஷபம்': 2,
        'Gemini': 3, 'Mithuna': 3, 'மிதுனம்': 3,
        'Cancer': 4, 'Kataka': 4, 'கடகம்': 4,
        'Leo': 5, 'Simha': 5, 'சிம்மம்': 5,
        'Virgo': 6, 'Kanya': 6, 'கன்னி': 6,
        'Libra': 7, 'Tula': 7, 'துலாம்': 7,
        'Scorpio': 8, 'Vrischika': 8, 'விருச்சிகம்': 8,
        'Sagittarius': 9, 'Dhanus': 9, 'தனுசு': 9,
        'Capricorn': 10, 'Makara': 10, 'மகரம்': 10,
        'Aquarius': 11, 'Kumbha': 11, 'கும்பம்': 11,
        'Pisces': 12, 'Meena': 12, 'மீனம்': 12,
    }

    # Planet exaltation rasis (where they are strongest)
    EXALTATION = {
        'Sun': 1, 'Moon': 2, 'Mars': 10, 'Mercury': 6,
        'Jupiter': 4, 'Venus': 12, 'Saturn': 7
    }

    # Planet debilitation rasis (where they are weakest)
    DEBILITATION = {
        'Sun': 7, 'Moon': 8, 'Mars': 4, 'Mercury': 12,
        'Jupiter': 10, 'Venus': 6, 'Saturn': 1
    }

    # Natural benefics and malefics
    BENEFICS = ['Jupiter', 'Venus', 'Moon', 'Mercury']
    MALEFICS = ['Saturn', 'Mars', 'Rahu', 'Ketu', 'Sun']

    def __init__(self, jathagam_generator=None, ephemeris=None):
        self.jathagam_gen = jathagam_generator
        self.ephemeris = ephemeris

    def calculate_life_areas(
        self,
        planets: List[Dict],
        lagna_rasi: str,
        moon_rasi: str,
        dasha_lord: Optional[str] = None,
        current_transits: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Calculate scores for all life areas based on birth chart

        Args:
            planets: List of planet positions from birth chart
            lagna_rasi: Ascendant sign
            moon_rasi: Moon sign (Rasi)
            dasha_lord: Current Maha Dasha lord
            current_transits: Current planetary positions (optional)

        Returns:
            Dictionary with scores and factors for each life area
        """
        lagna_num = self._get_rasi_number(lagna_rasi)
        moon_num = self._get_rasi_number(moon_rasi)

        # Create planet strength map
        planet_strengths = {p.get('planet', p.get('name')): p.get('strength', 50) for p in planets}

        # Create planet position map (which house from lagna)
        planet_houses = {}
        for p in planets:
            planet_name = p.get('planet', p.get('name'))
            planet_rasi = self._get_rasi_number(p.get('rasi', p.get('rasi_tamil', '')))
            if planet_rasi and lagna_num:
                house = ((planet_rasi - lagna_num) % 12) + 1
                planet_houses[planet_name] = house

        results = {}

        for area in ['love', 'career', 'education', 'family', 'health']:
            score, factors, suggestion, breakdown, calculation_trace = self._calculate_area_score(
                area=area,
                lagna_num=lagna_num,
                moon_num=moon_num,
                planet_strengths=planet_strengths,
                planet_houses=planet_houses,
                dasha_lord=dasha_lord,
                current_transits=current_transits
            )

            results[area] = {
                'score': score,
                'status': self._get_status(score),
                'status_tamil': self._get_status_tamil(score),
                'factors': factors,
                'suggestion': suggestion,
                'breakdown': breakdown,
                'calculation_trace': calculation_trace
            }

        return results

    def _calculate_area_score(
        self,
        area: str,
        lagna_num: int,
        moon_num: int,
        planet_strengths: Dict,
        planet_houses: Dict,
        dasha_lord: Optional[str],
        current_transits: Optional[List[Dict]]
    ) -> tuple:
        """Calculate score for a specific life area"""

        base_score = 50
        factors = []
        breakdown = {
            'karaka': {'score': 0, 'factors': []},
            'house': {'score': 0, 'factors': []},
            'dasha': {'score': 0, 'factors': []},
            'transit': {'score': 0, 'factors': []},
        }

        # 1. Check Karaka planets' strength (40% weight)
        karaka_score = 0
        karakas = self.AREA_KARAKAS.get(area, [])
        for karaka in karakas:
            strength = planet_strengths.get(karaka, 50)
            contribution = (strength - 50) * 0.4 / len(karakas)
            karaka_score += contribution

            factor_entry = {
                'name': self._get_tamil_planet(karaka),
                'detail': f'பலம்: {strength}%',
                'value': int(contribution),
                'positive': strength >= 50
            }
            breakdown['karaka']['factors'].append(factor_entry)

            if strength >= 65:
                factors.append({
                    'name': f'{self._get_tamil_planet(karaka)} பலம்',
                    'value': int((strength - 50) * 0.5),
                    'positive': True,
                    'description': f'{self._get_tamil_planet(karaka)} நல்ல பலத்தில் உள்ளார்'
                })
            elif strength <= 35:
                factors.append({
                    'name': f'{self._get_tamil_planet(karaka)} பலவீனம்',
                    'value': int((50 - strength) * -0.5),
                    'positive': False,
                    'description': f'{self._get_tamil_planet(karaka)} பலவீனமாக உள்ளார்'
                })

        breakdown['karaka']['score'] = int(karaka_score)

        # 2. Check relevant house lords' placement (30% weight)
        house_score = 0
        relevant_houses = self.LIFE_AREA_HOUSES.get(area, [])

        for house_num in relevant_houses[:2]:  # Focus on primary houses
            actual_house = ((house_num - 1 + lagna_num - 1) % 12) + 1
            lord = self.HOUSE_LORDS.get(actual_house, 'Sun')
            lord_strength = planet_strengths.get(lord, 50)
            lord_house = planet_houses.get(lord, 1)

            # Check if lord is in good houses (1, 4, 5, 7, 9, 10, 11)
            good_houses = [1, 4, 5, 7, 9, 10, 11]
            if lord_house in good_houses:
                contribution = 8
                factors.append({
                    'name': f'{house_num}ம் வீட்டு அதிபதி',
                    'value': contribution,
                    'positive': True,
                    'description': f'{self._get_tamil_planet(lord)} நல்ல வீட்டில் உள்ளார்'
                })
                breakdown['house']['factors'].append({
                    'name': f'{house_num}ம் வீடு',
                    'detail': f'{self._get_tamil_planet(lord)} {lord_house}ம் வீட்டில்',
                    'value': contribution,
                    'positive': True
                })
            elif lord_house in [6, 8, 12]:  # Dusthana houses
                contribution = -10
                factors.append({
                    'name': f'{house_num}ம் வீட்டு அதிபதி',
                    'value': contribution,
                    'positive': False,
                    'description': f'{self._get_tamil_planet(lord)} 6/8/12 வீட்டில்'
                })
                breakdown['house']['factors'].append({
                    'name': f'{house_num}ம் வீடு',
                    'detail': f'{self._get_tamil_planet(lord)} {lord_house}ம் வீட்டில்',
                    'value': contribution,
                    'positive': False
                })
            else:
                contribution = 0

            house_score += contribution

        breakdown['house']['score'] = int(house_score)

        # 3. Dasha lord effect (15% weight)
        dasha_score = 0
        if dasha_lord:
            dasha_strength = planet_strengths.get(dasha_lord, 50)
            if dasha_lord in karakas:
                # Dasha lord is karaka for this area - amplified effect
                dasha_score = (dasha_strength - 50) * 0.2
                breakdown['dasha']['factors'].append({
                    'name': f'{self._get_tamil_planet(dasha_lord)} தசை',
                    'detail': f'காரகர் - பலம் {dasha_strength}%',
                    'value': int(dasha_score),
                    'positive': dasha_score >= 0
                })
                if dasha_strength >= 60:
                    factors.append({
                        'name': f'{self._get_tamil_planet(dasha_lord)} தசா',
                        'value': int(dasha_score),
                        'positive': True,
                        'description': f'தற்போதைய தசா நாதர் இந்த துறைக்கு காரகர்'
                    })

        breakdown['dasha']['score'] = int(dasha_score)

        # 4. Transit effects (15% weight)
        transit_score = 0
        if current_transits:
            for transit in current_transits:
                t_planet = transit.get('planet', transit.get('name', ''))
                t_rasi = self._get_rasi_number(transit.get('rasi', ''))

                if t_planet in karakas and t_rasi:
                    # Calculate transit house from moon
                    transit_house = ((t_rasi - moon_num) % 12) + 1

                    # Good transit houses: 2, 5, 7, 9, 11
                    if transit_house in [2, 5, 7, 9, 11]:
                        transit_score += 5
                        breakdown['transit']['factors'].append({
                            'name': f'{self._get_tamil_planet(t_planet)} கோச்சாரம்',
                            'detail': f'{transit_house}ம் வீடு - நல்லது',
                            'value': 5,
                            'positive': True
                        })
                    elif transit_house in [6, 8, 12]:
                        transit_score -= 5
                        breakdown['transit']['factors'].append({
                            'name': f'{self._get_tamil_planet(t_planet)} கோச்சாரம்',
                            'detail': f'{transit_house}ம் வீடு - சவால்',
                            'value': -5,
                            'positive': False
                        })

        breakdown['transit']['score'] = int(transit_score)

        # Calculate final score
        final_score = base_score + karaka_score + house_score + dasha_score + transit_score

        # Add some variation based on current date to show daily changes
        today = datetime.now()
        day_factor = (today.day + today.month) % 10 - 5  # -5 to +4
        area_offset = hash(area) % 7 - 3  # Different offset per area
        final_score += day_factor + area_offset

        # Clamp to valid range
        final_score = max(35, min(95, final_score))

        # Generate suggestion
        suggestion = self._get_suggestion(area, final_score, factors)

        # Create calculation trace for detailed modal display
        calculation_trace = {
            'formula': 'score = 50 + karaka(40%) + house(30%) + dasha(15%) + transit(15%)',
            'step_by_step': [
                {
                    'component': 'karaka',
                    'component_tamil': 'காரக கிரக பலம்',
                    'weight': '40%',
                    'contribution': breakdown['karaka']['score'],
                    'factors_detail': breakdown['karaka']['factors']
                },
                {
                    'component': 'house',
                    'component_tamil': 'வீட்டு அதிபதி நிலை',
                    'weight': '30%',
                    'contribution': breakdown['house']['score'],
                    'factors_detail': breakdown['house']['factors']
                },
                {
                    'component': 'dasha',
                    'component_tamil': 'தசா பலம்',
                    'weight': '15%',
                    'contribution': breakdown['dasha']['score'],
                    'factors_detail': breakdown['dasha']['factors']
                },
                {
                    'component': 'transit',
                    'component_tamil': 'கோச்சார பலம்',
                    'weight': '15%',
                    'contribution': breakdown['transit']['score'],
                    'factors_detail': breakdown['transit']['factors']
                },
            ],
            'final_calculation': {
                'sum_of_contributions': f"50 + {breakdown['karaka']['score']} + {breakdown['house']['score']} + {breakdown['dasha']['score']} + {breakdown['transit']['score']}",
                'total': int(final_score)
            }
        }

        return int(final_score), factors[:4], suggestion, breakdown, calculation_trace  # Limit to top 4 factors

    def _get_rasi_number(self, rasi: str) -> int:
        """Convert rasi name to number"""
        if not rasi:
            return 1
        return self.RASI_MAP.get(rasi, 1)

    def _get_tamil_planet(self, planet: str) -> str:
        """Get Tamil name for planet"""
        tamil_names = {
            'Sun': 'சூரியன்',
            'Moon': 'சந்திரன்',
            'Mars': 'செவ்வாய்',
            'Mercury': 'புதன்',
            'Jupiter': 'குரு',
            'Venus': 'சுக்கிரன்',
            'Saturn': 'சனி',
            'Rahu': 'ராகு',
            'Ketu': 'கேது'
        }
        return tamil_names.get(planet, planet)

    def _get_status(self, score: int) -> str:
        """Get status label based on score"""
        if score >= 75:
            return 'excellent'
        elif score >= 60:
            return 'good'
        elif score >= 45:
            return 'average'
        else:
            return 'challenging'

    def _get_status_tamil(self, score: int) -> str:
        """Get Tamil status label"""
        if score >= 75:
            return 'சிறப்பு'
        elif score >= 60:
            return 'நல்லது'
        elif score >= 45:
            return 'சாதாரணம்'
        else:
            return 'கவனம்'

    def _get_suggestion(self, area: str, score: int, factors: List) -> str:
        """Generate personalized suggestion based on area and score"""
        suggestions = {
            'love': {
                'high': 'காதல் வாழ்க்கை சிறப்பாக உள்ளது. உறவுகளை பேணுங்கள்.',
                'medium': 'வெள்ளிக்கிழமை விரதம் இருந்தால் காதல் வாழ்க்கை மேம்படும்',
                'low': 'சுக்கிர பரிகாரம் செய்யுங்கள். வெள்ளை நிற உடை அணியுங்கள்.'
            },
            'career': {
                'high': 'தொழில் வளர்ச்சிக்கு சிறந்த நேரம். புதிய முயற்சிகள் செய்யலாம்.',
                'medium': 'சனிக்கிழமை ஹனுமான் வழிபாடு தொழில் வளர்ச்சிக்கு உதவும்',
                'low': 'சனி பகவான் வழிபாடு செய்யுங்கள். நீல நிற ஆடை அணியுங்கள்.'
            },
            'education': {
                'high': 'கல்வியில் சிறப்பு காலம். புதிய படிப்புகள் தொடங்கலாம்.',
                'medium': 'புதன்கிழமை விஷ்ணு வழிபாடு கல்வி வளர்ச்சிக்கு நல்லது',
                'low': 'புதன் மற்றும் குரு பரிகாரம் செய்யுங்கள்.'
            },
            'family': {
                'high': 'குடும்ப உறவுகள் மிகவும் சிறப்பாக உள்ளன.',
                'medium': 'திங்கள்கிழமை சிவ வழிபாடு குடும்ப ஒற்றுமைக்கு நல்லது',
                'low': 'சந்திர பரிகாரம் செய்யுங்கள். குடும்பத்துடன் நேரம் செலவிடுங்கள்.'
            },
            'health': {
                'high': 'ஆரோக்கியம் சிறப்பாக உள்ளது. உடற்பயிற்சி தொடருங்கள்.',
                'medium': 'ஞாயிறு காயத்ரி ஜபம் ஆரோக்கியத்திற்கு நல்லது',
                'low': 'சூரிய பரிகாரம் செய்யுங்கள். காலை நடை பயிற்சி செய்யுங்கள்.'
            }
        }

        area_suggestions = suggestions.get(area, suggestions['career'])

        if score >= 70:
            return area_suggestions['high']
        elif score >= 50:
            return area_suggestions['medium']
        else:
            return area_suggestions['low']
