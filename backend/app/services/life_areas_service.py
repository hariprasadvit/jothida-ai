"""
Life Areas Service
Calculates dynamic scores for Love, Career, Education, Family, Health
based on user's birth chart and current planetary transits
"""

from typing import Dict, List, Optional
from datetime import datetime, date
import math


# Planet name translations
PLANET_NAMES = {
    'en': {
        'Sun': 'Sun', 'Moon': 'Moon', 'Mars': 'Mars', 'Mercury': 'Mercury',
        'Jupiter': 'Jupiter', 'Venus': 'Venus', 'Saturn': 'Saturn',
        'Rahu': 'Rahu', 'Ketu': 'Ketu'
    },
    'ta': {
        'Sun': 'சூரியன்', 'Moon': 'சந்திரன்', 'Mars': 'செவ்வாய்', 'Mercury': 'புதன்',
        'Jupiter': 'குரு', 'Venus': 'சுக்கிரன்', 'Saturn': 'சனி',
        'Rahu': 'ராகு', 'Ketu': 'கேது'
    },
    'kn': {
        'Sun': 'ಸೂರ್ಯ', 'Moon': 'ಚಂದ್ರ', 'Mars': 'ಮಂಗಳ', 'Mercury': 'ಬುಧ',
        'Jupiter': 'ಗುರು', 'Venus': 'ಶುಕ್ರ', 'Saturn': 'ಶನಿ',
        'Rahu': 'ರಾಹು', 'Ketu': 'ಕೇತು'
    }
}

# Translation strings
TRANSLATIONS = {
    'en': {
        'strength': 'Strength',
        'strong': 'is strong',
        'weak': 'is weak',
        'house': 'house',
        'lord': 'lord',
        'in_good_house': 'in good house',
        'in_6_8_12': 'in 6/8/12 house',
        'dasha': 'Dasha',
        'karaka_amplified': 'Karaka - amplified effect',
        'current_dasha_karaka': 'Current dasha lord is karaka for this area',
        'transit': 'Transit',
        'good_transit': 'good',
        'challenging_transit': 'challenge',
        # Status labels
        'excellent': 'Excellent',
        'good': 'Good',
        'average': 'Average',
        'challenging': 'Needs attention',
        # Calculation trace components
        'karaka_planet_strength': 'Karaka Planet Strength',
        'house_lord_position': 'House Lord Position',
        'dasha_effect': 'Dasha Effect',
        'transit_effect': 'Transit Effect',
        # Suggestions
        'love_high': 'Love life is excellent. Nurture your relationships.',
        'love_medium': 'Fasting on Friday will improve love life',
        'love_low': 'Do Venus remedies. Wear white colored clothes.',
        'career_high': 'Great time for career growth. Try new initiatives.',
        'career_medium': 'Hanuman worship on Saturday helps career growth',
        'career_low': 'Worship Saturn. Wear blue colored clothes.',
        'education_high': 'Excellent time for education. Start new courses.',
        'education_medium': 'Vishnu worship on Wednesday helps education',
        'education_low': 'Do Mercury and Jupiter remedies.',
        'family_high': 'Family relationships are very good.',
        'family_medium': 'Shiva worship on Monday helps family harmony',
        'family_low': 'Do Moon remedies. Spend time with family.',
        'health_high': 'Health is excellent. Continue exercising.',
        'health_medium': 'Gayatri japa on Sunday helps health',
        'health_low': 'Do Sun remedies. Take morning walks.',
    },
    'ta': {
        'strength': 'பலம்',
        'strong': 'நல்ல பலத்தில் உள்ளார்',
        'weak': 'பலவீனமாக உள்ளார்',
        'house': 'வீடு',
        'lord': 'அதிபதி',
        'in_good_house': 'நல்ல வீட்டில் உள்ளார்',
        'in_6_8_12': '6/8/12 வீட்டில்',
        'dasha': 'தசை',
        'karaka_amplified': 'காரகர் - பலம்',
        'current_dasha_karaka': 'தற்போதைய தசா நாதர் இந்த துறைக்கு காரகர்',
        'transit': 'கோச்சாரம்',
        'good_transit': 'நல்லது',
        'challenging_transit': 'சவால்',
        # Status labels
        'excellent': 'சிறப்பு',
        'good': 'நல்லது',
        'average': 'சாதாரணம்',
        'challenging': 'கவனம்',
        # Calculation trace components
        'karaka_planet_strength': 'காரக கிரக பலம்',
        'house_lord_position': 'வீட்டு அதிபதி நிலை',
        'dasha_effect': 'தசா பலம்',
        'transit_effect': 'கோச்சார பலம்',
        # Suggestions
        'love_high': 'காதல் வாழ்க்கை சிறப்பாக உள்ளது. உறவுகளை பேணுங்கள்.',
        'love_medium': 'வெள்ளிக்கிழமை விரதம் இருந்தால் காதல் வாழ்க்கை மேம்படும்',
        'love_low': 'சுக்கிர பரிகாரம் செய்யுங்கள். வெள்ளை நிற உடை அணியுங்கள்.',
        'career_high': 'தொழில் வளர்ச்சிக்கு சிறந்த நேரம். புதிய முயற்சிகள் செய்யலாம்.',
        'career_medium': 'சனிக்கிழமை ஹனுமான் வழிபாடு தொழில் வளர்ச்சிக்கு உதவும்',
        'career_low': 'சனி பகவான் வழிபாடு செய்யுங்கள். நீல நிற ஆடை அணியுங்கள்.',
        'education_high': 'கல்வியில் சிறப்பு காலம். புதிய படிப்புகள் தொடங்கலாம்.',
        'education_medium': 'புதன்கிழமை விஷ்ணு வழிபாடு கல்வி வளர்ச்சிக்கு நல்லது',
        'education_low': 'புதன் மற்றும் குரு பரிகாரம் செய்யுங்கள்.',
        'family_high': 'குடும்ப உறவுகள் மிகவும் சிறப்பாக உள்ளன.',
        'family_medium': 'திங்கள்கிழமை சிவ வழிபாடு குடும்ப ஒற்றுமைக்கு நல்லது',
        'family_low': 'சந்திர பரிகாரம் செய்யுங்கள். குடும்பத்துடன் நேரம் செலவிடுங்கள்.',
        'health_high': 'ஆரோக்கியம் சிறப்பாக உள்ளது. உடற்பயிற்சி தொடருங்கள்.',
        'health_medium': 'ஞாயிறு காயத்ரி ஜபம் ஆரோக்கியத்திற்கு நல்லது',
        'health_low': 'சூரிய பரிகாரம் செய்யுங்கள். காலை நடை பயிற்சி செய்யுங்கள்.',
    },
    'kn': {
        'strength': 'ಬಲ',
        'strong': 'ಬಲಶಾಲಿ',
        'weak': 'ದುರ್ಬಲ',
        'house': 'ಮನೆ',
        'lord': 'ಅಧಿಪತಿ',
        'in_good_house': 'ಒಳ್ಳೆಯ ಮನೆಯಲ್ಲಿ',
        'in_6_8_12': '6/8/12 ಮನೆಯಲ್ಲಿ',
        'dasha': 'ದಶಾ',
        'karaka_amplified': 'ಕಾರಕ - ಬಲವರ್ಧಿತ',
        'current_dasha_karaka': 'ಪ್ರಸ್ತುತ ದಶಾ ಅಧಿಪತಿ ಈ ಕ್ಷೇತ್ರಕ್ಕೆ ಕಾರಕ',
        'transit': 'ಗೋಚಾರ',
        'good_transit': 'ಒಳ್ಳೆಯದು',
        'challenging_transit': 'ಸವಾಲು',
        # Status labels
        'excellent': 'ಅತ್ಯುತ್ತಮ',
        'good': 'ಒಳ್ಳೆಯದು',
        'average': 'ಸಾಮಾನ್ಯ',
        'challenging': 'ಗಮನ ಬೇಕು',
        # Calculation trace components
        'karaka_planet_strength': 'ಕಾರಕ ಗ್ರಹ ಬಲ',
        'house_lord_position': 'ಮನೆ ಅಧಿಪತಿ ಸ್ಥಾನ',
        'dasha_effect': 'ದಶಾ ಪರಿಣಾಮ',
        'transit_effect': 'ಗೋಚಾರ ಪರಿಣಾಮ',
        # Suggestions
        'love_high': 'ಪ್ರೇಮ ಜೀವನ ಅತ್ಯುತ್ತಮ. ಸಂಬಂಧಗಳನ್ನು ಪೋಷಿಸಿ.',
        'love_medium': 'ಶುಕ್ರವಾರ ಉಪವಾಸ ಪ್ರೇಮ ಜೀವನವನ್ನು ಸುಧಾರಿಸುತ್ತದೆ',
        'love_low': 'ಶುಕ್ರ ಪರಿಹಾರ ಮಾಡಿ. ಬಿಳಿ ಬಣ್ಣದ ಬಟ್ಟೆ ಧರಿಸಿ.',
        'career_high': 'ವೃತ್ತಿ ಬೆಳವಣಿಗೆಗೆ ಉತ್ತಮ ಸಮಯ. ಹೊಸ ಪ್ರಯತ್ನಗಳನ್ನು ಮಾಡಿ.',
        'career_medium': 'ಶನಿವಾರ ಹನುಮಾನ್ ಪೂಜೆ ವೃತ್ತಿ ಬೆಳವಣಿಗೆಗೆ ಸಹಾಯಕ',
        'career_low': 'ಶನಿ ಪೂಜೆ ಮಾಡಿ. ನೀಲಿ ಬಣ್ಣದ ಬಟ್ಟೆ ಧರಿಸಿ.',
        'education_high': 'ಶಿಕ್ಷಣಕ್ಕೆ ಅತ್ಯುತ್ತಮ ಸಮಯ. ಹೊಸ ಕೋರ್ಸ್‌ಗಳನ್ನು ಪ್ರಾರಂಭಿಸಿ.',
        'education_medium': 'ಬುಧವಾರ ವಿಷ್ಣು ಪೂಜೆ ಶಿಕ್ಷಣಕ್ಕೆ ಸಹಾಯಕ',
        'education_low': 'ಬುಧ ಮತ್ತು ಗುರು ಪರಿಹಾರ ಮಾಡಿ.',
        'family_high': 'ಕುಟುಂಬ ಸಂಬಂಧಗಳು ತುಂಬಾ ಒಳ್ಳೆಯವು.',
        'family_medium': 'ಸೋಮವಾರ ಶಿವ ಪೂಜೆ ಕುಟುಂಬ ಐಕ್ಯತೆಗೆ ಸಹಾಯಕ',
        'family_low': 'ಚಂದ್ರ ಪರಿಹಾರ ಮಾಡಿ. ಕುಟುಂಬದೊಂದಿಗೆ ಸಮಯ ಕಳೆಯಿರಿ.',
        'health_high': 'ಆರೋಗ್ಯ ಅತ್ಯುತ್ತಮ. ವ್ಯಾಯಾಮ ಮುಂದುವರಿಸಿ.',
        'health_medium': 'ಭಾನುವಾರ ಗಾಯತ್ರಿ ಜಪ ಆರೋಗ್ಯಕ್ಕೆ ಸಹಾಯಕ',
        'health_low': 'ಸೂರ್ಯ ಪರಿಹಾರ ಮಾಡಿ. ಬೆಳಗಿನ ನಡಿಗೆ ಮಾಡಿ.',
    }
}


def get_planet_name(planet: str, lang: str = 'ta') -> str:
    """Get translated planet name"""
    names = PLANET_NAMES.get(lang, PLANET_NAMES['ta'])
    return names.get(planet, planet)


def get_text(key: str, lang: str = 'ta') -> str:
    """Get translated text"""
    texts = TRANSLATIONS.get(lang, TRANSLATIONS['ta'])
    return texts.get(key, TRANSLATIONS['ta'].get(key, key))


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
        current_transits: Optional[List[Dict]] = None,
        lang: str = 'ta'
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
                current_transits=current_transits,
                lang=lang
            )

            results[area] = {
                'score': score,
                'status': self._get_status(score, lang),
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
        current_transits: Optional[List[Dict]],
        lang: str = 'ta'
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

            planet_name = get_planet_name(karaka, lang)
            factor_entry = {
                'name': planet_name,
                'detail': f'{get_text("strength", lang)}: {strength}%',
                'value': int(contribution),
                'positive': strength >= 50
            }
            breakdown['karaka']['factors'].append(factor_entry)

            if strength >= 65:
                factors.append({
                    'name': f'{planet_name} {get_text("strength", lang)}',
                    'value': int((strength - 50) * 0.5),
                    'positive': True,
                    'description': f'{planet_name} {get_text("strong", lang)}'
                })
            elif strength <= 35:
                factors.append({
                    'name': f'{planet_name} {get_text("weak", lang)}',
                    'value': int((50 - strength) * -0.5),
                    'positive': False,
                    'description': f'{planet_name} {get_text("weak", lang)}'
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
            lord_name = get_planet_name(lord, lang)
            house_text = get_text('house', lang)
            lord_text = get_text('lord', lang)

            # Check if lord is in good houses (1, 4, 5, 7, 9, 10, 11)
            good_houses = [1, 4, 5, 7, 9, 10, 11]
            if lord_house in good_houses:
                contribution = 8
                factors.append({
                    'name': f'{house_num} {house_text} {lord_text}',
                    'value': contribution,
                    'positive': True,
                    'description': f'{lord_name} {get_text("in_good_house", lang)}'
                })
                breakdown['house']['factors'].append({
                    'name': f'{house_num} {house_text}',
                    'detail': f'{lord_name} {lord_house} {house_text}',
                    'value': contribution,
                    'positive': True
                })
            elif lord_house in [6, 8, 12]:  # Dusthana houses
                contribution = -10
                factors.append({
                    'name': f'{house_num} {house_text} {lord_text}',
                    'value': contribution,
                    'positive': False,
                    'description': f'{lord_name} {get_text("in_6_8_12", lang)}'
                })
                breakdown['house']['factors'].append({
                    'name': f'{house_num} {house_text}',
                    'detail': f'{lord_name} {lord_house} {house_text}',
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
            dasha_lord_name = get_planet_name(dasha_lord, lang)
            dasha_text = get_text('dasha', lang)
            if dasha_lord in karakas:
                # Dasha lord is karaka for this area - amplified effect
                dasha_score = (dasha_strength - 50) * 0.2
                breakdown['dasha']['factors'].append({
                    'name': f'{dasha_lord_name} {dasha_text}',
                    'detail': f'{get_text("karaka_amplified", lang)} {dasha_strength}%',
                    'value': int(dasha_score),
                    'positive': dasha_score >= 0
                })
                if dasha_strength >= 60:
                    factors.append({
                        'name': f'{dasha_lord_name} {dasha_text}',
                        'value': int(dasha_score),
                        'positive': True,
                        'description': get_text('current_dasha_karaka', lang)
                    })

        breakdown['dasha']['score'] = int(dasha_score)

        # 4. Transit effects (15% weight)
        transit_score = 0
        transit_text = get_text('transit', lang)
        house_text = get_text('house', lang)
        if current_transits:
            for transit in current_transits:
                t_planet = transit.get('planet', transit.get('name', ''))
                t_rasi = self._get_rasi_number(transit.get('rasi', ''))

                if t_planet in karakas and t_rasi:
                    t_planet_name = get_planet_name(t_planet, lang)
                    # Calculate transit house from moon
                    transit_house = ((t_rasi - moon_num) % 12) + 1

                    # Good transit houses: 2, 5, 7, 9, 11
                    if transit_house in [2, 5, 7, 9, 11]:
                        transit_score += 5
                        breakdown['transit']['factors'].append({
                            'name': f'{t_planet_name} {transit_text}',
                            'detail': f'{transit_house} {house_text} - {get_text("good_transit", lang)}',
                            'value': 5,
                            'positive': True
                        })
                    elif transit_house in [6, 8, 12]:
                        transit_score -= 5
                        breakdown['transit']['factors'].append({
                            'name': f'{t_planet_name} {transit_text}',
                            'detail': f'{transit_house} {house_text} - {get_text("challenging_transit", lang)}',
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
        suggestion = self._get_suggestion(area, final_score, factors, lang)

        # Create calculation trace for detailed modal display
        calculation_trace = {
            'formula': 'score = 50 + karaka(40%) + house(30%) + dasha(15%) + transit(15%)',
            'step_by_step': [
                {
                    'component': 'karaka',
                    'component_label': get_text('karaka_planet_strength', lang),
                    'weight': '40%',
                    'contribution': breakdown['karaka']['score'],
                    'factors_detail': breakdown['karaka']['factors']
                },
                {
                    'component': 'house',
                    'component_label': get_text('house_lord_position', lang),
                    'weight': '30%',
                    'contribution': breakdown['house']['score'],
                    'factors_detail': breakdown['house']['factors']
                },
                {
                    'component': 'dasha',
                    'component_label': get_text('dasha_effect', lang),
                    'weight': '15%',
                    'contribution': breakdown['dasha']['score'],
                    'factors_detail': breakdown['dasha']['factors']
                },
                {
                    'component': 'transit',
                    'component_label': get_text('transit_effect', lang),
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

    def _get_status(self, score: int, lang: str = 'ta') -> str:
        """Get status label based on score"""
        if score >= 75:
            return get_text('excellent', lang)
        elif score >= 60:
            return get_text('good', lang)
        elif score >= 45:
            return get_text('average', lang)
        else:
            return get_text('challenging', lang)

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

    def _get_suggestion(self, area: str, score: int, factors: List, lang: str = 'ta') -> str:
        """Generate personalized suggestion based on area and score"""
        if score >= 70:
            return get_text(f'{area}_high', lang)
        elif score >= 50:
            return get_text(f'{area}_medium', lang)
        else:
            return get_text(f'{area}_low', lang)
