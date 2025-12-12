"""
Future Projection Service - Dynamic Monthly & Yearly Predictions
================================================================
Uses the South Indian Astro-Percent Engine for accurate predictions
based on Dasha, Transits, Yogas, and House strengths.
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Any
import re
from .astro_percent_engine import AstroPercentEngine


class FutureProjectionService:
    """Service to calculate personalized future projections using Astro-Percent Engine"""

    # Tamil month names
    TAMIL_MONTHS = [
        'ஜனவரி', 'பிப்ரவரி', 'மார்ச்', 'ஏப்ரல்', 'மே', 'ஜூன்',
        'ஜூலை', 'ஆகஸ்ட்', 'செப்டம்பர்', 'அக்டோபர்', 'நவம்பர்', 'டிசம்பர்'
    ]

    PLANET_TAMIL = {
        'Sun': 'சூரியன்', 'Moon': 'சந்திரன்', 'Mars': 'செவ்வாய்',
        'Mercury': 'புதன்', 'Jupiter': 'குரு', 'Venus': 'சுக்கிரன்',
        'Saturn': 'சனி', 'Rahu': 'ராகு', 'Ketu': 'கேது',
    }

    # Score-based recommendations
    SCORE_RECOMMENDATIONS = {
        'excellent': {
            'general': 'இது உங்களுக்கு சிறந்த காலம். புதிய முயற்சிகளை தைரியமாக தொடங்கலாம்.',
            'career': 'தொழில் வளர்ச்சிக்கு ஏற்ற நேரம். பதவி உயர்வு, ஊதிய உயர்வு சாத்தியம்.',
            'finance': 'நிதி வளர்ச்சி நன்றாக இருக்கும். முதலீடு செய்ய சிறந்த காலம்.',
            'health': 'ஆரோக்கியம் நன்றாக இருக்கும். புதிய உடற்பயிற்சி தொடங்கலாம்.',
            'relationships': 'உறவுகள் வலுப்படும். திருமணம், நல்ல செய்திகள் வரலாம்.'
        },
        'good': {
            'general': 'நல்ல காலம். திட்டமிட்ட செயல்கள் வெற்றி பெறும்.',
            'career': 'தொழிலில் நிலையான வளர்ச்சி. புதிய திட்டங்கள் தொடங்கலாம்.',
            'finance': 'நிதி நிலை சீராக இருக்கும். சேமிப்பு அதிகரிக்கும்.',
            'health': 'ஆரோக்கியம் நன்றாக இருக்கும். சிறிய பாதுகாப்பு நடவடிக்கைகள் தேவை.',
            'relationships': 'குடும்ப உறவுகள் இனிமையாக இருக்கும்.'
        },
        'average': {
            'general': 'சராசரி காலம். பொறுமையாக செயல்படுங்கள், முயற்சிகள் வீண் போகாது.',
            'career': 'தொழிலில் நிலையாக இருக்கும். பெரிய மாற்றங்கள் தவிர்க்கவும்.',
            'finance': 'செலவுகளை கட்டுப்படுத்துங்கள். அதிக கடன் வாங்க வேண்டாம்.',
            'health': 'உணவு, உறக்கம் கவனிக்கவும். மன அழுத்தம் தவிர்க்கவும்.',
            'relationships': 'புரிந்துணர்வுடன் நடந்துகொள்ளுங்கள்.'
        },
        'challenging': {
            'general': 'சவாலான காலம். எச்சரிக்கையாக இருங்கள், அவசர முடிவுகள் தவிர்க்கவும்.',
            'career': 'தொழிலில் சவால்கள் வரலாம். பொறுமையாக சமாளிக்கவும்.',
            'finance': 'பண விஷயங்களில் கவனமாக இருங்கள். புதிய முதலீடு தவிர்க்கவும்.',
            'health': 'ஆரோக்கியம் கவனிக்கவும். மருத்துவ பரிசோதனை செய்யுங்கள்.',
            'relationships': 'தேவையற்ற விவாதங்கள் தவிர்க்கவும்.'
        },
        'difficult': {
            'general': 'கடினமான காலம். இறைவன் மீது நம்பிக்கை வையுங்கள், பரிகாரங்கள் செய்யுங்கள்.',
            'career': 'வேலை இழப்பு/மாற்றம் வரலாம். மாற்று திட்டம் வைத்திருங்கள்.',
            'finance': 'நிதி நெருக்கடி வரலாம். செலவு குறைக்கவும், கடன் தவிர்க்கவும்.',
            'health': 'உடல் நலம் பாதிக்கப்படலாம். உடனடியாக மருத்துவர் ஆலோசனை பெறுங்கள்.',
            'relationships': 'குடும்பத்தில் பிரச்சனைகள் வரலாம். பொறுமையாக இருங்கள்.'
        }
    }

    # Dasha-specific recommendations
    DASHA_RECOMMENDATIONS = {
        'Sun': 'அரசு சம்பந்தமான காரியங்கள் சாதகம். தந்தையின் ஆசி பெறுங்கள்.',
        'Moon': 'மனதை அமைதியாக வைத்துக்கொள்ளுங்கள். தாயை கவனியுங்கள்.',
        'Mars': 'தைரியமாக செயல்படுங்கள், ஆனால் கோபத்தை கட்டுப்படுத்துங்கள்.',
        'Mercury': 'வியாபாரம், படிப்பு, தொடர்பாடலில் வெற்றி. புத்தியை பயன்படுத்துங்கள்.',
        'Jupiter': 'குரு கிருபை உள்ளது. தர்மம், ஆன்மீகம், கல்வியில் முன்னேற்றம்.',
        'Venus': 'சொகுசு, கலை, உறவுகளில் மகிழ்ச்சி. திருமண யோகம் உண்டு.',
        'Saturn': 'கடின உழைப்பு பலன் தரும். சோதனைகள் வரலாம், பொறுமையாக இருங்கள்.',
        'Rahu': 'எதிர்பாராத மாற்றங்கள் வரலாம். விழிப்பாக இருங்கள்.',
        'Ketu': 'ஆன்மீக வளர்ச்சி. உலக விஷயங்களில் சோர்வு வரலாம்.'
    }

    # Transit-based recommendations
    TRANSIT_RECOMMENDATIONS = {
        'sadesati': 'சடேசதி காலம். சனிக்கிழமை விரதம், ஹனுமான் வழிபாடு செய்யுங்கள்.',
        'ashtama_shani': 'அஷ்டம சனி. ஆரோக்கியம் கவனிக்கவும். திருநள்ளாறு சனீஸ்வரர் கோவில் செல்லுங்கள்.',
        'kantaka_shani': 'கண்டக சனி. தொழில் மற்றும் குடும்பத்தில் பொறுமை தேவை.',
        'jupiter_good': 'குரு கோச்சாரம் சாதகம். புதிய காரியங்கள் தொடங்கலாம்.',
        'jupiter_bad': 'குரு கோச்சாரம் சாதகமில்லை. பெரிய முடிவுகள் தள்ளி வையுங்கள்.'
    }

    # Vimshottari Dasha order and periods (in years)
    DASHA_ORDER = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
    DASHA_PERIODS = {
        'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10, 'Mars': 7,
        'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17
    }

    # Nakshatra lords for dasha starting calculation
    NAKSHATRA_LORDS = [
        'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury',  # 1-9
        'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury',  # 10-18
        'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury'   # 19-27
    ]

    def __init__(self, ephemeris=None):
        self.ephemeris = ephemeris

    def _calculate_dasha_timeline(self, jathagam: Dict) -> List[Dict]:
        """Calculate complete dasha timeline from birth to 120 years"""

        # Get moon longitude and birth date
        moon_data = None
        for planet in jathagam.get('planets', []):
            if planet.get('planet') == 'Moon':
                moon_data = planet
                break

        if not moon_data:
            return []

        # Get birth date
        birth_info = jathagam.get('birth_details', {})
        birth_date_str = birth_info.get('date', '1990-01-01')
        try:
            birth_dt = datetime.strptime(birth_date_str, '%Y-%m-%d')
        except:
            birth_dt = datetime.now() - timedelta(days=35*365)  # Assume 35 years old

        # Get moon longitude (degree)
        moon_degree = moon_data.get('degree', 0)
        moon_sign = moon_data.get('sign', 'Mesha')

        # Convert sign to number
        sign_numbers = {
            'Mesha': 0, 'Aries': 0, 'Vrishabha': 1, 'Taurus': 1, 'Mithuna': 2, 'Gemini': 2,
            'Kataka': 3, 'Cancer': 3, 'Simha': 4, 'Leo': 4, 'Kanya': 5, 'Virgo': 5,
            'Tula': 6, 'Libra': 6, 'Vrischika': 7, 'Scorpio': 7, 'Dhanus': 8, 'Sagittarius': 8,
            'Makara': 9, 'Capricorn': 9, 'Kumbha': 10, 'Aquarius': 10, 'Meena': 11, 'Pisces': 11
        }
        sign_num = sign_numbers.get(moon_sign, 0)
        moon_longitude = sign_num * 30 + moon_degree

        # Calculate nakshatra and starting dasha
        nakshatra_span = 360 / 27
        nakshatra_index = int(moon_longitude / nakshatra_span)
        nakshatra_lord = self.NAKSHATRA_LORDS[nakshatra_index % 27]

        # Position within nakshatra for elapsed fraction
        moon_pos_in_nakshatra = moon_longitude % nakshatra_span
        elapsed_fraction = moon_pos_in_nakshatra / nakshatra_span

        # Find starting dasha index
        dasha_start_index = self.DASHA_ORDER.index(nakshatra_lord)

        # Calculate balance of first dasha at birth
        first_dasha_years = self.DASHA_PERIODS[nakshatra_lord]
        first_dasha_balance = first_dasha_years * (1 - elapsed_fraction)

        # Build dasha timeline
        dasha_timeline = []
        current_date = birth_dt

        # First (balance) dasha
        end_date = current_date + timedelta(days=first_dasha_balance * 365.25)
        dasha_timeline.append({
            'lord': nakshatra_lord,
            'start': current_date,
            'end': end_date,
            'years': first_dasha_balance
        })
        current_date = end_date

        # Remaining 8 dashas (then cycle continues)
        for cycle in range(3):  # 3 cycles = 360 years coverage
            for i in range(1 if cycle == 0 else 0, 9):
                lord = self.DASHA_ORDER[(dasha_start_index + i) % 9]
                years = self.DASHA_PERIODS[lord]
                end_date = current_date + timedelta(days=years * 365.25)
                dasha_timeline.append({
                    'lord': lord,
                    'start': current_date,
                    'end': end_date,
                    'years': years
                })
                current_date = end_date

        return dasha_timeline

    def _get_dasha_for_date(self, target_date: date, dasha_timeline: List[Dict]) -> Dict:
        """Get the dasha lord and antardasha lord for a specific date"""
        target_dt = datetime.combine(target_date, datetime.min.time())

        # Find current mahadasha
        current_maha = None
        for dasha in dasha_timeline:
            if dasha['start'] <= target_dt <= dasha['end']:
                current_maha = dasha
                break

        if not current_maha:
            # Default to first dasha if not found
            current_maha = dasha_timeline[0] if dasha_timeline else {'lord': 'Jupiter', 'start': target_dt, 'end': target_dt, 'years': 16}

        maha_lord = current_maha['lord']

        # Calculate antardasha within mahadasha
        maha_start = current_maha['start']
        maha_years = current_maha['years']
        maha_index = self.DASHA_ORDER.index(maha_lord)

        # Build antardasha timeline
        antar_start = maha_start
        antar_lord = maha_lord

        for i in range(9):
            antar_lord_candidate = self.DASHA_ORDER[(maha_index + i) % 9]
            antar_years = self.DASHA_PERIODS[antar_lord_candidate]
            antar_proportion = (antar_years / 120) * maha_years
            antar_end = antar_start + timedelta(days=antar_proportion * 365.25)

            if antar_start <= target_dt <= antar_end:
                antar_lord = antar_lord_candidate
                break
            antar_start = antar_end

        return {
            'mahadasha_lord': maha_lord,
            'antardasha_lord': antar_lord
        }

    def _get_personalized_recommendation(
        self,
        score: float,
        quality: str,
        dasha_lord: str,
        transit_info: Dict,
        life_area: str = 'general'
    ) -> str:
        """Generate personalized recommendation based on all factors"""
        recommendations = []

        # Base recommendation from score
        base_rec = self.SCORE_RECOMMENDATIONS.get(quality, {}).get(life_area, '')
        if base_rec:
            recommendations.append(base_rec)

        # Dasha-specific advice
        dasha_rec = self.DASHA_RECOMMENDATIONS.get(dasha_lord, '')
        if dasha_rec:
            recommendations.append(dasha_rec)

        # Transit-specific advice
        saturn_from_moon = transit_info.get('saturn_from_moon', 0)
        jupiter_from_moon = transit_info.get('jupiter_from_moon', 0)

        if saturn_from_moon in [12, 1, 2]:
            recommendations.append(self.TRANSIT_RECOMMENDATIONS['sadesati'])
        elif saturn_from_moon == 8:
            recommendations.append(self.TRANSIT_RECOMMENDATIONS['ashtama_shani'])
        elif saturn_from_moon in [4, 7, 10]:
            recommendations.append(self.TRANSIT_RECOMMENDATIONS['kantaka_shani'])

        if jupiter_from_moon in [3, 5, 9, 10, 11]:
            recommendations.append(self.TRANSIT_RECOMMENDATIONS['jupiter_good'])
        elif jupiter_from_moon in [1, 6, 8, 12]:
            recommendations.append(self.TRANSIT_RECOMMENDATIONS['jupiter_bad'])

        return ' '.join(recommendations[:3])  # Max 3 recommendations

    def _generate_detailed_breakdown(self, result: Dict, dasha_lord: str) -> Dict:
        """Generate detailed breakdown explanation"""
        breakdown = result.get('breakdown', {})

        explanations = {
            'dasha': {
                'score': breakdown.get('dasha', {}).get('score', 0),
                'weight': '30%',
                'explanation': f"{self.PLANET_TAMIL.get(dasha_lord, dasha_lord)} தசை நடக்கிறது. " +
                              self._get_dasha_explanation(dasha_lord, breakdown.get('dasha', {}).get('raw', 0))
            },
            'house': {
                'score': breakdown.get('house', {}).get('score', 0),
                'weight': '20%',
                'explanation': self._get_house_explanation(breakdown.get('house', {}))
            },
            'transit': {
                'score': breakdown.get('transit', {}).get('score', 0),
                'weight': '15%',
                'explanation': self._get_transit_explanation(breakdown.get('transit', {}))
            },
            'planet_strength': {
                'score': breakdown.get('planet_strength', {}).get('score', 0),
                'weight': '15%',
                'explanation': self._get_strength_explanation(breakdown.get('planet_strength', {}))
            },
            'yoga': {
                'score': breakdown.get('yoga', {}).get('score', 0),
                'weight': '10%',
                'explanation': self._get_yoga_explanation(breakdown.get('yoga', {}))
            },
            'navamsa': {
                'score': breakdown.get('navamsa', {}).get('score', 0),
                'weight': '10%',
                'explanation': 'நவாம்ச பலம்'
            }
        }

        return explanations

    def _get_dasha_explanation(self, dasha_lord: str, raw_score: float) -> str:
        """Get explanation for dasha score"""
        if raw_score >= 25:
            return f"மிகவும் சாதகமான தசா காலம். {dasha_lord} பலமாக உள்ளது."
        elif raw_score >= 18:
            return f"நல்ல தசா காலம். {dasha_lord} நடுத்தர பலத்தில் உள்ளது."
        elif raw_score >= 10:
            return f"சராசரி தசா காலம். கவனமாக செயல்படுங்கள்."
        else:
            return f"சவாலான தசா காலம். பரிகாரங்கள் செய்யுங்கள்."

    def _get_house_explanation(self, house_info: Dict) -> str:
        """Get explanation for house score"""
        factors = house_info.get('factors', [])
        if factors:
            factor_names = [f.get('name', '') for f in factors[:2]]
            return f"வீட்டு பலம்: {', '.join(factor_names)}"
        return "வீட்டு பலம் கணக்கிடப்பட்டது"

    def _get_transit_explanation(self, transit_info: Dict) -> str:
        """Get explanation for transit score"""
        factors = transit_info.get('factors', [])
        explanations = []
        for f in factors[:2]:
            name = f.get('name', '')
            detail = f.get('detail', '')
            if detail:
                explanations.append(f"{name}: {detail}")
            else:
                explanations.append(name)
        return '. '.join(explanations) if explanations else 'கோச்சார பலம் கணக்கிடப்பட்டது'

    def _get_strength_explanation(self, strength_info: Dict) -> str:
        """Get explanation for planet strength"""
        factors = strength_info.get('factors', [])
        if factors:
            explanations = []
            for f in factors[:2]:
                name = f.get('name', '')
                detail = f.get('detail', '')
                if detail:
                    explanations.append(f"{name} {detail}")
            return ', '.join(explanations) if explanations else 'கிரக பலம் கணக்கிடப்பட்டது'
        return 'கிரக பலம் கணக்கிடப்பட்டது'

    def _get_yoga_explanation(self, yoga_info: Dict) -> str:
        """Get explanation for yoga score"""
        factors = yoga_info.get('factors', [])
        if factors:
            yoga_names = [f.get('name', '') for f in factors if f.get('positive', True)]
            dosha_names = [f.get('name', '') for f in factors if not f.get('positive', True)]
            parts = []
            if yoga_names:
                parts.append(f"யோகம்: {', '.join(yoga_names)}")
            if dosha_names:
                parts.append(f"தோஷம்: {', '.join(dosha_names)}")
            return '. '.join(parts) if parts else 'யோக/தோஷ பலம்'
        return 'யோக/தோஷ பலம் கணக்கிடப்பட்டது'

    def calculate_monthly_projection(
        self,
        jathagam: Dict,
        dasha_info: Dict,
        month: int,
        year: int
    ) -> Dict[str, Any]:
        """Calculate projection for a specific month using Astro-Percent Engine"""

        target_date = date(year, month, 15)  # Mid-month

        # Get dasha lords
        dasha_lord = dasha_info.get('mahadasha_lord') or dasha_info.get('mahadasha', 'Jupiter')
        bhukti_lord = dasha_info.get('antardasha_lord') or dasha_info.get('antardasha')

        # Use Astro-Percent Engine for calculation
        engine = AstroPercentEngine(jathagam)
        result = engine.calculate_prediction_score(
            target_date=target_date,
            life_area='general',  # Monthly is general prediction
            dasha_lord=dasha_lord,
            bhukti_lord=bhukti_lord
        )

        # Format factors for display with detail
        factors = []
        for factor in result.get('top_factors', [])[:4]:
            factors.append({
                'name': factor.get('name', ''),
                'value': abs(int(factor.get('value', 0))),
                'positive': factor.get('positive', True),
                'detail': factor.get('detail', '')
            })

        # Get transit info for recommendation
        transit_info = result['breakdown'].get('transit', {})

        # Get transits from breakdown if available
        transits = {}
        if isinstance(transit_info, dict):
            # Try to get from factors detail
            for f in transit_info.get('factors', []):
                if 'குரு' in f.get('name', ''):
                    # Extract house number from name like "குரு மேஷம்இல் - 5ஆம் வீடு"
                    match = re.search(r'(\d+)ஆம் வீடு', f.get('name', ''))
                    if match:
                        transits['jupiter_from_moon'] = int(match.group(1))
                elif 'சனி' in f.get('name', '') or 'சடேசதி' in f.get('name', '') or 'அஷ்டம' in f.get('name', ''):
                    match = re.search(r'(\d+)ஆம் வீடு', f.get('name', ''))
                    if match:
                        transits['saturn_from_moon'] = int(match.group(1))
                    elif 'சடேசதி' in f.get('name', ''):
                        transits['saturn_from_moon'] = 1  # Sade sati
                    elif 'அஷ்டம' in f.get('name', ''):
                        transits['saturn_from_moon'] = 8

        # Generate personalized recommendation
        recommendation = self._get_personalized_recommendation(
            score=result['score'],
            quality=result.get('quality', 'average'),
            dasha_lord=dasha_lord,
            transit_info=transits,
            life_area='general'
        )

        return {
            'name': self.TAMIL_MONTHS[month - 1],
            'month': month,
            'year': year,
            'score': round(result['score'], 1),
            'quality': result.get('quality_tamil', 'சராசரி'),
            'factors': factors,
            'recommendation': recommendation,
            'breakdown': {
                'dasha': result['breakdown']['dasha']['score'],
                'transit': result['breakdown']['transit']['score'],
                'house': result['breakdown']['house']['score'],
                'planet_strength': result['breakdown']['planet_strength']['score'],
                'yoga': result['breakdown']['yoga']['score'],
                'navamsa': result['breakdown']['navamsa']['score'],
            },
            'calculation_trace': result.get('calculation_trace', {}),
            'dasha_lord': dasha_lord,
            'bhukti_lord': bhukti_lord
        }

    def calculate_yearly_projection(
        self,
        jathagam: Dict,
        dasha_info: Dict,
        year: int,
        label: str
    ) -> Dict[str, Any]:
        """Calculate projection for a specific year using Astro-Percent Engine"""

        target_date = date(year, 6, 15)  # Mid-year

        # Get dasha lords
        dasha_lord = dasha_info.get('mahadasha_lord') or dasha_info.get('mahadasha', 'Jupiter')
        bhukti_lord = dasha_info.get('antardasha_lord') or dasha_info.get('antardasha')

        engine = AstroPercentEngine(jathagam)

        # Get general prediction first - this is the main score (same as monthly)
        general_result = engine.calculate_prediction_score(
            target_date=target_date,
            life_area='general',
            dasha_lord=dasha_lord,
            bhukti_lord=bhukti_lord
        )

        # Use general score as the overall score (consistent with monthly)
        overall_score = general_result['score']

        # Also calculate area-specific scores for breakdown display
        life_areas = ['career', 'finance', 'health', 'relationships']
        area_scores = {}
        area_recommendations = {}

        for area in life_areas:
            result = engine.calculate_prediction_score(
                target_date=target_date,
                life_area=area,
                dasha_lord=dasha_lord,
                bhukti_lord=bhukti_lord
            )
            area_scores[area] = round(result['score'], 1)

            # Get area-specific recommendation
            area_quality = result.get('quality', 'average')
            area_rec = self.SCORE_RECOMMENDATIONS.get(area_quality, {}).get(area, '')
            if area_rec:
                area_recommendations[area] = area_rec

        # Format factors with detail
        factors = []
        for factor in general_result.get('top_factors', [])[:4]:
            factors.append({
                'name': factor.get('name', ''),
                'value': abs(int(factor.get('value', 0))),
                'positive': factor.get('positive', True),
                'detail': factor.get('detail', '')
            })

        # Get transit info for recommendation
        transit_info = general_result['breakdown'].get('transit', {})
        transits = {}
        if isinstance(transit_info, dict):
            for f in transit_info.get('factors', []):
                if 'குரு' in f.get('name', ''):
                    match = re.search(r'(\d+)ஆம் வீடு', f.get('name', ''))
                    if match:
                        transits['jupiter_from_moon'] = int(match.group(1))
                elif 'சனி' in f.get('name', '') or 'சடேசதி' in f.get('name', '') or 'அஷ்டம' in f.get('name', ''):
                    match = re.search(r'(\d+)ஆம் வீடு', f.get('name', ''))
                    if match:
                        transits['saturn_from_moon'] = int(match.group(1))
                    elif 'சடேசதி' in f.get('name', ''):
                        transits['saturn_from_moon'] = 1
                    elif 'அஷ்டம' in f.get('name', ''):
                        transits['saturn_from_moon'] = 8

        # Generate detailed breakdown explanations
        detailed_breakdown = self._generate_detailed_breakdown(general_result, dasha_lord)

        # Generate personalized recommendation
        recommendation = self._get_personalized_recommendation(
            score=overall_score,
            quality=general_result.get('quality', 'average'),
            dasha_lord=dasha_lord,
            transit_info=transits,
            life_area='general'
        )

        return {
            'year': year,
            'label': label,
            'score': round(overall_score, 1),
            'quality': general_result.get('quality_tamil', 'சராசரி'),
            'factors': factors,
            'recommendation': recommendation,
            'area_scores': area_scores,
            'area_recommendations': area_recommendations,
            'breakdown': {
                'dasha': general_result['breakdown']['dasha']['score'],
                'transit': general_result['breakdown']['transit']['score'],
                'house': general_result['breakdown']['house']['score'],
                'planet_strength': general_result['breakdown']['planet_strength']['score'],
                'yoga': general_result['breakdown']['yoga']['score'],
                'navamsa': general_result['breakdown']['navamsa']['score'],
            },
            'detailed_breakdown': detailed_breakdown,
            'calculation_trace': general_result.get('calculation_trace', {}),
            'dasha_lord': dasha_lord,
            'bhukti_lord': bhukti_lord
        }

    def calculate_projections(
        self,
        jathagam: Dict,
        dasha_info: Dict
    ) -> Dict[str, Any]:
        """Calculate all monthly and yearly projections with dynamic dasha lookup"""

        current_date = date.today()
        current_year = current_date.year
        current_month = current_date.month

        # Build dasha timeline for accurate future/past predictions
        dasha_timeline = self._calculate_dasha_timeline(jathagam)

        # Generate 12 monthly projections starting from current month
        monthly_projections = []
        for i in range(12):
            month = ((current_month - 1 + i) % 12) + 1
            year = current_year + ((current_month - 1 + i) // 12)

            # Get correct dasha for this specific month
            target_date = date(year, month, 15)
            if dasha_timeline:
                dasha_for_month = self._get_dasha_for_date(target_date, dasha_timeline)
            else:
                dasha_for_month = dasha_info

            projection = self.calculate_monthly_projection(
                jathagam, dasha_for_month, month, year
            )
            monthly_projections.append(projection)

        # Generate 3 yearly projections
        yearly_labels = ['நடப்பு ஆண்டு', 'அடுத்த ஆண்டு', 'மூன்றாம் ஆண்டு']
        yearly_projections = []
        for i, label in enumerate(yearly_labels):
            target_year = current_year + i

            # Get correct dasha for mid-year of each year
            target_date = date(target_year, 6, 15)
            if dasha_timeline:
                dasha_for_year = self._get_dasha_for_date(target_date, dasha_timeline)
            else:
                dasha_for_year = dasha_info

            projection = self.calculate_yearly_projection(
                jathagam, dasha_for_year, target_year, label
            )
            yearly_projections.append(projection)

        # Summary statistics
        avg_monthly = sum(p['score'] for p in monthly_projections) / len(monthly_projections)
        best_month = max(monthly_projections, key=lambda x: x['score'])
        challenging_month = min(monthly_projections, key=lambda x: x['score'])

        return {
            'monthly': monthly_projections,
            'yearly': yearly_projections,
            'summary': {
                'average_score': round(avg_monthly, 1),
                'best_month': best_month['name'],
                'best_month_score': best_month['score'],
                'challenging_month': challenging_month['name'],
                'challenging_month_score': challenging_month['score'],
            },
            'dasha_timeline': [
                {
                    'lord': d['lord'],
                    'start': d['start'].strftime('%Y-%m-%d'),
                    'end': d['end'].strftime('%Y-%m-%d')
                }
                for d in dasha_timeline[:12]  # Show next 12 dasha periods
            ] if dasha_timeline else [],
            'generated_at': datetime.now().isoformat()
        }


# For backward compatibility
def calculate_projections(jathagam: Dict, dasha_info: Dict) -> Dict:
    """Backward compatible function"""
    service = FutureProjectionService()
    return service.calculate_projections(jathagam, dasha_info)
