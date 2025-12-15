"""
Future Projection Service - Dynamic Monthly & Yearly Predictions
================================================================
Uses the South Indian Astro-Percent Engine for accurate predictions
based on Dasha, Transits, Yogas, and House strengths.

v4.1 Enhancement: Supports TimeAdaptiveEngine for time-mode aware predictions
with POI/HAI tensor calculations and full explainability traces.
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional
import re
from .astro_percent_engine import AstroPercentEngine

# Try to import v4.1 engine (optional enhancement)
try:
    from .time_adaptive_engine import TimeAdaptiveEngine, TimeMode
    V41_ENGINE_AVAILABLE = True
except ImportError:
    V41_ENGINE_AVAILABLE = False
    TimeAdaptiveEngine = None
    TimeMode = None


# Multi-language translations
TRANSLATIONS = {
    'en': {
        # Month names
        'months': ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December'],
        # Year labels
        'current_year': 'Current Year',
        'next_year': 'Next Year',
        'third_year': 'Third Year',
        # Quality labels
        'excellent': 'Excellent',
        'good': 'Good',
        'average': 'Average',
        'challenging': 'Challenging',
        'difficult': 'Difficult',
        # Planet names
        'planets': {
            'Sun': 'Sun', 'Moon': 'Moon', 'Mars': 'Mars', 'Mercury': 'Mercury',
            'Jupiter': 'Jupiter', 'Venus': 'Venus', 'Saturn': 'Saturn',
            'Rahu': 'Rahu', 'Ketu': 'Ketu'
        },
        # Score recommendations
        'recommendations': {
            'excellent': {
                'general': 'This is an excellent period for you. Start new ventures with confidence.',
                'career': 'Great time for career growth. Promotions and salary hikes are possible.',
                'finance': 'Financial growth will be good. Great time for investments.',
                'health': 'Health will be excellent. You can start new exercise routines.',
                'relationships': 'Relationships will strengthen. Marriage and good news may come.'
            },
            'good': {
                'general': 'Good period. Planned activities will succeed.',
                'career': 'Steady career growth. You can start new projects.',
                'finance': 'Financial situation will be stable. Savings will increase.',
                'health': 'Health will be good. Minor precautions needed.',
                'relationships': 'Family relationships will be pleasant.'
            },
            'average': {
                'general': 'Average period. Be patient, efforts will not go waste.',
                'career': 'Career will be stable. Avoid major changes.',
                'finance': 'Control expenses. Avoid taking excessive loans.',
                'health': 'Watch your diet and sleep. Avoid stress.',
                'relationships': 'Be understanding with others.'
            },
            'challenging': {
                'general': 'Challenging period. Be cautious, avoid hasty decisions.',
                'career': 'Career challenges may come. Handle with patience.',
                'finance': 'Be careful with money matters. Avoid new investments.',
                'health': 'Take care of health. Get medical checkups.',
                'relationships': 'Avoid unnecessary arguments.'
            },
            'difficult': {
                'general': 'Difficult period. Have faith, perform remedies.',
                'career': 'Job loss/change may come. Keep backup plans.',
                'finance': 'Financial difficulties may arise. Cut expenses, avoid loans.',
                'health': 'Health may be affected. Consult doctor immediately.',
                'relationships': 'Family problems may arise. Be patient.'
            }
        },
        # Dasha recommendations
        'dasha_recommendations': {
            'Sun': 'Government-related matters will be favorable. Seek father\'s blessings.',
            'Moon': 'Keep your mind calm. Take care of mother.',
            'Mars': 'Act boldly, but control your anger.',
            'Mercury': 'Success in business, education, communication. Use your intellect.',
            'Jupiter': 'Guru\'s grace is with you. Progress in dharma, spirituality, education.',
            'Venus': 'Happiness in luxury, art, relationships. Marriage yoga exists.',
            'Saturn': 'Hard work will pay off. Challenges may come, be patient.',
            'Rahu': 'Unexpected changes may occur. Stay alert.',
            'Ketu': 'Spiritual growth. May feel detached from worldly matters.'
        },
        # Transit recommendations
        'transit_recommendations': {
            'sadesati': 'Sade Sati period. Fast on Saturdays, worship Hanuman.',
            'ashtama_shani': 'Ashtama Shani. Take care of health. Visit Thirunallaru Saneeswaran temple.',
            'kantaka_shani': 'Kantaka Shani. Patience needed in career and family.',
            'jupiter_good': 'Jupiter transit is favorable. Start new ventures.',
            'jupiter_bad': 'Jupiter transit is not favorable. Postpone major decisions.'
        },
        # Breakdown explanations
        'dasha_running': 'dasha is running',
        'very_favorable_dasha': 'Very favorable dasha period',
        'is_strong': 'is strong',
        'good_dasha': 'Good dasha period',
        'is_moderately_strong': 'is moderately strong',
        'average_dasha': 'Average dasha period. Act carefully.',
        'challenging_dasha': 'Challenging dasha period. Perform remedies.',
        'house_power': 'House power',
        'house_power_calculated': 'House power calculated',
        'transit_power': 'Transit power',
        'transit_power_calculated': 'Transit power calculated',
        'planet_power': 'Planet power',
        'planet_power_calculated': 'Planet power calculated',
        'yoga': 'Yoga',
        'dosha': 'Dosha',
        'yoga_dosha_power': 'Yoga/Dosha power',
        'yoga_dosha_calculated': 'Yoga/Dosha power calculated',
        'navamsa_power': 'Navamsa power',
    },
    'ta': {
        # Month names
        'months': ['ஜனவரி', 'பிப்ரவரி', 'மார்ச்', 'ஏப்ரல்', 'மே', 'ஜூன்',
                   'ஜூலை', 'ஆகஸ்ட்', 'செப்டம்பர்', 'அக்டோபர்', 'நவம்பர்', 'டிசம்பர்'],
        # Year labels
        'current_year': 'நடப்பு ஆண்டு',
        'next_year': 'அடுத்த ஆண்டு',
        'third_year': 'மூன்றாம் ஆண்டு',
        # Quality labels
        'excellent': 'சிறப்பு',
        'good': 'நல்லது',
        'average': 'சராசரி',
        'challenging': 'சவால்',
        'difficult': 'கடினம்',
        # Planet names
        'planets': {
            'Sun': 'சூரியன்', 'Moon': 'சந்திரன்', 'Mars': 'செவ்வாய்', 'Mercury': 'புதன்',
            'Jupiter': 'குரு', 'Venus': 'சுக்கிரன்', 'Saturn': 'சனி',
            'Rahu': 'ராகு', 'Ketu': 'கேது'
        },
        # Score recommendations
        'recommendations': {
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
        },
        # Dasha recommendations
        'dasha_recommendations': {
            'Sun': 'அரசு சம்பந்தமான காரியங்கள் சாதகம். தந்தையின் ஆசி பெறுங்கள்.',
            'Moon': 'மனதை அமைதியாக வைத்துக்கொள்ளுங்கள். தாயை கவனியுங்கள்.',
            'Mars': 'தைரியமாக செயல்படுங்கள், ஆனால் கோபத்தை கட்டுப்படுத்துங்கள்.',
            'Mercury': 'வியாபாரம், படிப்பு, தொடர்பாடலில் வெற்றி. புத்தியை பயன்படுத்துங்கள்.',
            'Jupiter': 'குரு கிருபை உள்ளது. தர்மம், ஆன்மீகம், கல்வியில் முன்னேற்றம்.',
            'Venus': 'சொகுசு, கலை, உறவுகளில் மகிழ்ச்சி. திருமண யோகம் உண்டு.',
            'Saturn': 'கடின உழைப்பு பலன் தரும். சோதனைகள் வரலாம், பொறுமையாக இருங்கள்.',
            'Rahu': 'எதிர்பாராத மாற்றங்கள் வரலாம். விழிப்பாக இருங்கள்.',
            'Ketu': 'ஆன்மீக வளர்ச்சி. உலக விஷயங்களில் சோர்வு வரலாம்.'
        },
        # Transit recommendations
        'transit_recommendations': {
            'sadesati': 'சடேசதி காலம். சனிக்கிழமை விரதம், ஹனுமான் வழிபாடு செய்யுங்கள்.',
            'ashtama_shani': 'அஷ்டம சனி. ஆரோக்கியம் கவனிக்கவும். திருநள்ளாறு சனீஸ்வரர் கோவில் செல்லுங்கள்.',
            'kantaka_shani': 'கண்டக சனி. தொழில் மற்றும் குடும்பத்தில் பொறுமை தேவை.',
            'jupiter_good': 'குரு கோச்சாரம் சாதகம். புதிய காரியங்கள் தொடங்கலாம்.',
            'jupiter_bad': 'குரு கோச்சாரம் சாதகமில்லை. பெரிய முடிவுகள் தள்ளி வையுங்கள்.'
        },
        # Breakdown explanations
        'dasha_running': 'தசை நடக்கிறது',
        'very_favorable_dasha': 'மிகவும் சாதகமான தசா காலம்',
        'is_strong': 'பலமாக உள்ளது',
        'good_dasha': 'நல்ல தசா காலம்',
        'is_moderately_strong': 'நடுத்தர பலத்தில் உள்ளது',
        'average_dasha': 'சராசரி தசா காலம். கவனமாக செயல்படுங்கள்.',
        'challenging_dasha': 'சவாலான தசா காலம். பரிகாரங்கள் செய்யுங்கள்.',
        'house_power': 'வீட்டு பலம்',
        'house_power_calculated': 'வீட்டு பலம் கணக்கிடப்பட்டது',
        'transit_power': 'கோச்சார பலம்',
        'transit_power_calculated': 'கோச்சார பலம் கணக்கிடப்பட்டது',
        'planet_power': 'கிரக பலம்',
        'planet_power_calculated': 'கிரக பலம் கணக்கிடப்பட்டது',
        'yoga': 'யோகம்',
        'dosha': 'தோஷம்',
        'yoga_dosha_power': 'யோக/தோஷ பலம்',
        'yoga_dosha_calculated': 'யோக/தோஷ பலம் கணக்கிடப்பட்டது',
        'navamsa_power': 'நவாம்ச பலம்',
    },
    'kn': {
        # Month names
        'months': ['ಜನವರಿ', 'ಫೆಬ್ರವರಿ', 'ಮಾರ್ಚ್', 'ಏಪ್ರಿಲ್', 'ಮೇ', 'ಜೂನ್',
                   'ಜುಲೈ', 'ಆಗಸ್ಟ್', 'ಸೆಪ್ಟೆಂಬರ್', 'ಅಕ್ಟೋಬರ್', 'ನವೆಂಬರ್', 'ಡಿಸೆಂಬರ್'],
        # Year labels
        'current_year': 'ಪ್ರಸ್ತುತ ವರ್ಷ',
        'next_year': 'ಮುಂದಿನ ವರ್ಷ',
        'third_year': 'ಮೂರನೇ ವರ್ಷ',
        # Quality labels
        'excellent': 'ಅತ್ಯುತ್ತಮ',
        'good': 'ಒಳ್ಳೆಯದು',
        'average': 'ಸಾಮಾನ್ಯ',
        'challenging': 'ಸವಾಲು',
        'difficult': 'ಕಷ್ಟಕರ',
        # Planet names
        'planets': {
            'Sun': 'ಸೂರ್ಯ', 'Moon': 'ಚಂದ್ರ', 'Mars': 'ಮಂಗಳ', 'Mercury': 'ಬುಧ',
            'Jupiter': 'ಗುರು', 'Venus': 'ಶುಕ್ರ', 'Saturn': 'ಶನಿ',
            'Rahu': 'ರಾಹು', 'Ketu': 'ಕೇತು'
        },
        # Score recommendations
        'recommendations': {
            'excellent': {
                'general': 'ಇದು ನಿಮಗೆ ಅತ್ಯುತ್ತಮ ಸಮಯ. ಹೊಸ ಪ್ರಯತ್ನಗಳನ್ನು ಧೈರ್ಯವಾಗಿ ಪ್ರಾರಂಭಿಸಿ.',
                'career': 'ವೃತ್ತಿ ಬೆಳವಣಿಗೆಗೆ ಉತ್ತಮ ಸಮಯ. ಬಡ್ತಿ, ಸಂಬಳ ಹೆಚ್ಚಳ ಸಾಧ್ಯ.',
                'finance': 'ಆರ್ಥಿಕ ಬೆಳವಣಿಗೆ ಉತ್ತಮವಾಗಿರುತ್ತದೆ. ಹೂಡಿಕೆಗೆ ಉತ್ತಮ ಸಮಯ.',
                'health': 'ಆರೋಗ್ಯ ಉತ್ತಮವಾಗಿರುತ್ತದೆ. ಹೊಸ ವ್ಯಾಯಾಮ ಪ್ರಾರಂಭಿಸಬಹುದು.',
                'relationships': 'ಸಂಬಂಧಗಳು ಬಲಗೊಳ್ಳುತ್ತವೆ. ಮದುವೆ, ಒಳ್ಳೆಯ ಸುದ್ದಿ ಬರಬಹುದು.'
            },
            'good': {
                'general': 'ಒಳ್ಳೆಯ ಸಮಯ. ಯೋಜಿತ ಕಾರ್ಯಗಳು ಯಶಸ್ವಿಯಾಗುತ್ತವೆ.',
                'career': 'ವೃತ್ತಿಯಲ್ಲಿ ಸ್ಥಿರ ಬೆಳವಣಿಗೆ. ಹೊಸ ಯೋಜನೆಗಳನ್ನು ಪ್ರಾರಂಭಿಸಬಹುದು.',
                'finance': 'ಆರ್ಥಿಕ ಪರಿಸ್ಥಿತಿ ಸ್ಥಿರವಾಗಿರುತ್ತದೆ. ಉಳಿತಾಯ ಹೆಚ್ಚಾಗುತ್ತದೆ.',
                'health': 'ಆರೋಗ್ಯ ಉತ್ತಮವಾಗಿರುತ್ತದೆ. ಸಣ್ಣ ಮುನ್ನೆಚ್ಚರಿಕೆ ಅಗತ್ಯ.',
                'relationships': 'ಕುಟುಂಬ ಸಂಬಂಧಗಳು ಸುಮಧುರವಾಗಿರುತ್ತವೆ.'
            },
            'average': {
                'general': 'ಸಾಮಾನ್ಯ ಸಮಯ. ತಾಳ್ಮೆಯಿಂದ ನಡೆಯಿರಿ, ಪ್ರಯತ್ನಗಳು ವ್ಯರ್ಥವಾಗುವುದಿಲ್ಲ.',
                'career': 'ವೃತ್ತಿ ಸ್ಥಿರವಾಗಿರುತ್ತದೆ. ದೊಡ್ಡ ಬದಲಾವಣೆಗಳನ್ನು ತಪ್ಪಿಸಿ.',
                'finance': 'ಖರ್ಚುಗಳನ್ನು ನಿಯಂತ್ರಿಸಿ. ಹೆಚ್ಚು ಸಾಲ ಪಡೆಯಬೇಡಿ.',
                'health': 'ಆಹಾರ, ನಿದ್ರೆ ಗಮನಿಸಿ. ಒತ್ತಡ ತಪ್ಪಿಸಿ.',
                'relationships': 'ತಿಳುವಳಿಕೆಯಿಂದ ನಡೆಯಿರಿ.'
            },
            'challenging': {
                'general': 'ಸವಾಲಿನ ಸಮಯ. ಎಚ್ಚರಿಕೆಯಿಂದಿರಿ, ಅವಸರದ ನಿರ್ಧಾರಗಳನ್ನು ತಪ್ಪಿಸಿ.',
                'career': 'ವೃತ್ತಿಯಲ್ಲಿ ಸವಾಲುಗಳು ಬರಬಹುದು. ತಾಳ್ಮೆಯಿಂದ ನಿಭಾಯಿಸಿ.',
                'finance': 'ಹಣದ ವಿಷಯಗಳಲ್ಲಿ ಜಾಗರೂಕರಾಗಿರಿ. ಹೊಸ ಹೂಡಿಕೆ ತಪ್ಪಿಸಿ.',
                'health': 'ಆರೋಗ್ಯ ಗಮನಿಸಿ. ವೈದ್ಯಕೀಯ ತಪಾಸಣೆ ಮಾಡಿಸಿ.',
                'relationships': 'ಅನಗತ್ಯ ವಾದಗಳನ್ನು ತಪ್ಪಿಸಿ.'
            },
            'difficult': {
                'general': 'ಕಷ್ಟಕರ ಸಮಯ. ದೇವರಲ್ಲಿ ನಂಬಿಕೆ ಇಡಿ, ಪರಿಹಾರಗಳನ್ನು ಮಾಡಿ.',
                'career': 'ಕೆಲಸ ಕಳೆದುಕೊಳ್ಳುವ/ಬದಲಾವಣೆ ಬರಬಹುದು. ಪರ್ಯಾಯ ಯೋಜನೆ ಇಟ್ಟುಕೊಳ್ಳಿ.',
                'finance': 'ಆರ್ಥಿಕ ಸಂಕಷ್ಟ ಬರಬಹುದು. ಖರ್ಚು ಕಡಿಮೆ ಮಾಡಿ, ಸಾಲ ತಪ್ಪಿಸಿ.',
                'health': 'ಆರೋಗ್ಯ ಹಾನಿಯಾಗಬಹುದು. ತಕ್ಷಣ ವೈದ್ಯರ ಸಲಹೆ ಪಡೆಯಿರಿ.',
                'relationships': 'ಕುಟುಂಬದಲ್ಲಿ ಸಮಸ್ಯೆಗಳು ಬರಬಹುದು. ತಾಳ್ಮೆ ಇರಲಿ.'
            }
        },
        # Dasha recommendations
        'dasha_recommendations': {
            'Sun': 'ಸರ್ಕಾರಿ ಕಾರ್ಯಗಳು ಅನುಕೂಲ. ತಂದೆಯ ಆಶೀರ್ವಾದ ಪಡೆಯಿರಿ.',
            'Moon': 'ಮನಸ್ಸನ್ನು ಶಾಂತವಾಗಿಡಿ. ತಾಯಿಯನ್ನು ನೋಡಿಕೊಳ್ಳಿ.',
            'Mars': 'ಧೈರ್ಯವಾಗಿ ಕಾರ್ಯ ನಿರ್ವಹಿಸಿ, ಆದರೆ ಕೋಪವನ್ನು ನಿಯಂತ್ರಿಸಿ.',
            'Mercury': 'ವ್ಯಾಪಾರ, ಶಿಕ್ಷಣ, ಸಂವಹನದಲ್ಲಿ ಯಶಸ್ಸು. ಬುದ್ಧಿಯನ್ನು ಬಳಸಿ.',
            'Jupiter': 'ಗುರು ಕೃಪೆ ಇದೆ. ಧರ್ಮ, ಆಧ್ಯಾತ್ಮ, ಶಿಕ್ಷಣದಲ್ಲಿ ಪ್ರಗತಿ.',
            'Venus': 'ಐಷಾರಾಮ, ಕಲೆ, ಸಂಬಂಧಗಳಲ್ಲಿ ಸಂತೋಷ. ಮದುವೆ ಯೋಗವಿದೆ.',
            'Saturn': 'ಕಠಿಣ ಪರಿಶ್ರಮ ಫಲ ನೀಡುತ್ತದೆ. ಪರೀಕ್ಷೆಗಳು ಬರಬಹುದು, ತಾಳ್ಮೆ ಇರಲಿ.',
            'Rahu': 'ಅನಿರೀಕ್ಷಿತ ಬದಲಾವಣೆಗಳು ಬರಬಹುದು. ಎಚ್ಚರಿಕೆಯಿಂದಿರಿ.',
            'Ketu': 'ಆಧ್ಯಾತ್ಮಿಕ ಬೆಳವಣಿಗೆ. ಲೌಕಿಕ ವಿಷಯಗಳಲ್ಲಿ ನಿರಾಸಕ್ತಿ ಬರಬಹುದು.'
        },
        # Transit recommendations
        'transit_recommendations': {
            'sadesati': 'ಸಡೇಸತಿ ಕಾಲ. ಶನಿವಾರ ಉಪವಾಸ, ಹನುಮಾನ್ ಪೂಜೆ ಮಾಡಿ.',
            'ashtama_shani': 'ಅಷ್ಟಮ ಶನಿ. ಆರೋಗ್ಯ ಗಮನಿಸಿ. ತಿರುನಲ್ಲಾರು ಶನೀಶ್ವರ ದೇವಸ್ಥಾನಕ್ಕೆ ಹೋಗಿ.',
            'kantaka_shani': 'ಕಂಟಕ ಶನಿ. ವೃತ್ತಿ ಮತ್ತು ಕುಟುಂಬದಲ್ಲಿ ತಾಳ್ಮೆ ಅಗತ್ಯ.',
            'jupiter_good': 'ಗುರು ಗೋಚಾರ ಅನುಕೂಲ. ಹೊಸ ಕಾರ್ಯಗಳನ್ನು ಪ್ರಾರಂಭಿಸಬಹುದು.',
            'jupiter_bad': 'ಗುರು ಗೋಚಾರ ಅನುಕೂಲವಲ್ಲ. ದೊಡ್ಡ ನಿರ್ಧಾರಗಳನ್ನು ಮುಂದೂಡಿ.'
        },
        # Breakdown explanations
        'dasha_running': 'ದಶೆ ನಡೆಯುತ್ತಿದೆ',
        'very_favorable_dasha': 'ಅತ್ಯಂತ ಅನುಕೂಲಕರ ದಶಾ ಕಾಲ',
        'is_strong': 'ಬಲಶಾಲಿ',
        'good_dasha': 'ಒಳ್ಳೆಯ ದಶಾ ಕಾಲ',
        'is_moderately_strong': 'ಮಧ್ಯಮ ಬಲದಲ್ಲಿದೆ',
        'average_dasha': 'ಸಾಮಾನ್ಯ ದಶಾ ಕಾಲ. ಜಾಗರೂಕರಾಗಿ ನಡೆಯಿರಿ.',
        'challenging_dasha': 'ಸವಾಲಿನ ದಶಾ ಕಾಲ. ಪರಿಹಾರಗಳನ್ನು ಮಾಡಿ.',
        'house_power': 'ಮನೆ ಬಲ',
        'house_power_calculated': 'ಮನೆ ಬಲ ಲೆಕ್ಕಾಚಾರ ಮಾಡಲಾಗಿದೆ',
        'transit_power': 'ಗೋಚಾರ ಬಲ',
        'transit_power_calculated': 'ಗೋಚಾರ ಬಲ ಲೆಕ್ಕಾಚಾರ ಮಾಡಲಾಗಿದೆ',
        'planet_power': 'ಗ್ರಹ ಬಲ',
        'planet_power_calculated': 'ಗ್ರಹ ಬಲ ಲೆಕ್ಕಾಚಾರ ಮಾಡಲಾಗಿದೆ',
        'yoga': 'ಯೋಗ',
        'dosha': 'ದೋಷ',
        'yoga_dosha_power': 'ಯೋಗ/ದೋಷ ಬಲ',
        'yoga_dosha_calculated': 'ಯೋಗ/ದೋಷ ಬಲ ಲೆಕ್ಕಾಚಾರ ಮಾಡಲಾಗಿದೆ',
        'navamsa_power': 'ನವಾಂಶ ಬಲ',
    }
}


def get_translation(key: str, lang: str = 'ta') -> str:
    """Get a translation by key"""
    trans = TRANSLATIONS.get(lang, TRANSLATIONS['ta'])
    return trans.get(key, TRANSLATIONS['ta'].get(key, key))


def get_month_name(month: int, lang: str = 'ta') -> str:
    """Get translated month name (1-indexed)"""
    trans = TRANSLATIONS.get(lang, TRANSLATIONS['ta'])
    months = trans.get('months', TRANSLATIONS['ta']['months'])
    return months[month - 1] if 1 <= month <= 12 else ''


def get_planet_name(planet: str, lang: str = 'ta') -> str:
    """Get translated planet name"""
    trans = TRANSLATIONS.get(lang, TRANSLATIONS['ta'])
    planets = trans.get('planets', TRANSLATIONS['ta']['planets'])
    return planets.get(planet, planet)


def get_year_label(index: int, lang: str = 'ta') -> str:
    """Get translated year label (0=current, 1=next, 2=third)"""
    keys = ['current_year', 'next_year', 'third_year']
    if 0 <= index < len(keys):
        return get_translation(keys[index], lang)
    return ''


def get_quality_label(quality: str, lang: str = 'ta') -> str:
    """Get translated quality label"""
    return get_translation(quality, lang)


def get_recommendation(quality: str, life_area: str, lang: str = 'ta') -> str:
    """Get recommendation for quality and life area"""
    trans = TRANSLATIONS.get(lang, TRANSLATIONS['ta'])
    recs = trans.get('recommendations', TRANSLATIONS['ta']['recommendations'])
    return recs.get(quality, {}).get(life_area, '')


def get_dasha_recommendation(dasha_lord: str, lang: str = 'ta') -> str:
    """Get dasha-specific recommendation"""
    trans = TRANSLATIONS.get(lang, TRANSLATIONS['ta'])
    recs = trans.get('dasha_recommendations', TRANSLATIONS['ta']['dasha_recommendations'])
    return recs.get(dasha_lord, '')


def get_transit_recommendation(transit_key: str, lang: str = 'ta') -> str:
    """Get transit-specific recommendation"""
    trans = TRANSLATIONS.get(lang, TRANSLATIONS['ta'])
    recs = trans.get('transit_recommendations', TRANSLATIONS['ta']['transit_recommendations'])
    return recs.get(transit_key, '')


# Tamil to English/Kannada factor translations for AstroPercentEngine output
FACTOR_TRANSLATIONS = {
    'en': {
        # Planet names
        'சூரியன்': 'Sun', 'சந்திரன்': 'Moon', 'செவ்வாய்': 'Mars',
        'புதன்': 'Mercury', 'குரு': 'Jupiter', 'சுக்கிரன்': 'Venus',
        'சனி': 'Saturn', 'ராகு': 'Rahu', 'கேது': 'Ketu',
        # Dasha/Bhukti terms
        'தசை': 'Dasha', 'புக்தி': 'Bhukti', 'பலகை': 'strength',
        'ஊடாட்டம்': 'interaction', 'பலம்': 'strength',
        # Rasi names
        'மேஷம்': 'Aries', 'ரிஷபம்': 'Taurus', 'மிதுனம்': 'Gemini',
        'கடகம்': 'Cancer', 'சிம்மம்': 'Leo', 'கன்னி': 'Virgo',
        'துலாம்': 'Libra', 'விருச்சிகம்': 'Scorpio', 'தனுசு': 'Sagittarius',
        'மகரம்': 'Capricorn', 'கும்பம்': 'Aquarius', 'மீனம்': 'Pisces',
        # House terms
        'திரிகோண வீடு': 'Trikona House', 'கேந்திர வீடு': 'Kendra House',
        'தன வீடு': 'Dhana House', 'உபச்சய வீடு': 'Upachaya House',
        'துஷ்டான வீடு': 'Dusthana House',
        'ஆம் வீட்டதிபதி': 'House Lord', 'வீட்டில்': 'in house',
        'ஆம் வீட்டில்': 'in house', 'ஆம் வீடு': 'house',
        'சொந்த வீடு': 'Own House', 'வீடு': 'House',
        'கேந்திரம் நல்லது': 'Kendra is good',
        # Dignity terms
        'உச்சம்': 'Exalted', 'சொந்த': 'Own Sign', 'நட்பு': 'Friendly',
        'சமம்': 'Neutral', 'பகை': 'Enemy', 'நீசம்': 'Debilitated',
        # Aspect terms
        'குரு பார்வை': 'Jupiter Aspect', 'சனி பார்வை': 'Saturn Aspect',
        'பார்வை': 'Aspect',
        # Transit/Sade Sati terms
        'சடேசதி': 'Sade Sati', 'சாதகமான சனி': 'Favorable Saturn',
        'கண்டக சனி': 'Kantaka Shani', 'அஷ்டம சனி': 'Ashtama Shani',
        'நடுப்பகுதி': 'Middle phase',
        # Quality terms
        'சாதகமான': 'Favorable', 'சவால்': 'Challenging',
        'சிறப்பு': 'Excellent', 'நல்லது': 'Good', 'கலப்பு': 'Mixed',
        'மிகச்சிறந்தது': 'Excellent', 'சராசரி': 'Average',
        'சவாலானது': 'Challenging', 'கடினமானது': 'Difficult',
        # Karaka terms
        'காரகன்': 'Karaka', 'தசை = காரகம்': 'Dasha = Karaka',
        # Yoga names
        'கஜகேசரி யோகம்': 'Gajakesari Yoga',
        'புத ஆதித்ய யோகம்': 'Budha Aditya Yoga',
        'சந்திர மங்கள யோகம்': 'Chandra Mangala Yoga',
        'ராஜ யோகம்': 'Raja Yoga',
        # Dosha names
        'கால சர்ப்ப தோஷம்': 'Kala Sarpa Dosha',
        'கேமத்ருமா தோஷம்': 'Kemadruma Dosha',
        # Other terms
        'யோகம்': 'Yoga', 'தோஷம்': 'Dosha',
        'நவாம்ச பலம்': 'Navamsa Strength', 'நவாம்ச': 'Navamsa',
        'ஆரம்பம்': 'Beginning', 'முடிவு': 'End',
        'இல்': 'in', 'பலவீனம்': 'Weakness',
        # Eclipse terms
        'சூரிய கிரகணம்': 'Solar Eclipse', 'சந்திர கிரகணம்': 'Lunar Eclipse',
        'கிரகண கால பாதிப்பு': 'Eclipse period effect',
        'வக்கிர கால பாதிப்பு': 'Retrograde period effect',
        # Rahu-Ketu terms
        'ராகு-கேது 1/7 அச்சு': 'Rahu-Ketu 1/7 axis',
        # Detailed message translations
        'பொறுமை தேவை': 'Patience needed',
        'கடின உழைப்பு வெற்றி தரும்': 'Hard work will bring success',
        'ஆரோக்கியம் கவனிக்க': 'Take care of health',
        'பெரிய முடிவுகள் தவிர்க்க': 'Avoid major decisions',
        'தொழில்/குடும்பத்தில் சவால்': 'Challenges in career/family',
        'திட்டமிட்டு செயல்படுக': 'Act with planning',
        'கடின உழைப்புக்கு பலன் கிடைக்கும்': 'Hard work will be rewarded',
        'மன குழப்பம்': 'Mental confusion',
        'முக்கிய முடிவுகள் தாமதிக்க': 'Delay important decisions',
        'திடீர் மாற்றங்கள்': 'Sudden changes',
        'எச்சரிக்கையாக இருக்க': 'Be cautious',
        'குழப்பம் வரலாம்': 'Confusion may arise',
        'தெளிவாக சிந்திக்க': 'Think clearly',
        'சக்தி மற்றும் துணிவு': 'Energy and courage',
        'புதிய தொடக்கங்கள் தவிர்க்க': 'Avoid new beginnings',
        'மன அமைதி பாதிப்பு': 'Mental peace affected',
        'முக்கிய முடிவுகள் தள்ளிவைக்க': 'Postpone important decisions',
        # House effect messages
        'உடல் ஆரோக்கியம் கவனிக்க': 'Take care of physical health',
        'நிதி நிலை சீராகும்': 'Financial situation will stabilize',
        'தைரியமும் வெற்றியும்': 'Courage and success',
        'மன அமைதி குறையும்': 'Mental peace may decrease',
        'புத்தி தெளிவு, நல்ல முடிவுகள்': 'Mental clarity, good decisions',
        'எதிரிகள் மீது வெற்றி': 'Victory over enemies',
        'உறவுகளில் சிக்கல் வரலாம்': 'Relationship issues may arise',
        'தடைகள், பொறுமை தேவை': 'Obstacles, patience needed',
        'அதிர்ஷ்டம், தர்மம் வளரும்': 'Luck, righteousness will grow',
        'தொழில் வெற்றி': 'Career success',
        'லாபம், ஆதாயம்': 'Profit, gain',
        'செலவுகள் அதிகரிக்கும்': 'Expenses will increase',
        # Confidence reasons
        'வலுவான ராசி ஆனால் நவாம்ச பலவீனம் - நம்பகத்தன்மை குறைவு': 'Strong rasi but weak navamsa - lower reliability',
        'வலுவான தசை கோசார பாதிப்பை குறைக்கிறது': 'Strong dasha reduces transit impact',
        'ஒரு வலுவான அம்சம் ஆதிக்கம் செலுத்துகிறது': 'One strong factor dominates',
        'அதிக மதிப்பெண்களுக்கு நிதான சரிசெய்தல்': 'Moderation adjustment for high scores',
        'யோகம் பலவீனங்களை சமன் செய்கிறது': 'Yoga compensates for weaknesses',
    },
    'kn': {
        # Planet names
        'சூரியன்': 'ಸೂರ್ಯ', 'சந்திரன்': 'ಚಂದ್ರ', 'செவ்வாய்': 'ಮಂಗಳ',
        'புதன்': 'ಬುಧ', 'குரு': 'ಗುರು', 'சுக்கிரன்': 'ಶುಕ್ರ',
        'சனி': 'ಶನಿ', 'ராகு': 'ರಾಹು', 'கேது': 'ಕೇತು',
        # Dasha/Bhukti terms
        'தசை': 'ದಶೆ', 'புக்தி': 'ಭುಕ್ತಿ', 'பலகை': 'ಬಲ',
        'ஊடாட்டம்': 'ಸಂಪರ್ಕ', 'பலம்': 'ಬಲ',
        # Rasi names
        'மேஷம்': 'ಮೇಷ', 'ரிஷபம்': 'ವೃಷಭ', 'மிதுனம்': 'ಮಿಥುನ',
        'கடகம்': 'ಕರ್ಕಾಟಕ', 'சிம்மம்': 'ಸಿಂಹ', 'கன்னி': 'ಕನ್ಯಾ',
        'துலாம்': 'ತುಲಾ', 'விருச்சிகம்': 'ವೃಶ್ಚಿಕ', 'தனுசு': 'ಧನು',
        'மகரம்': 'ಮಕರ', 'கும்பம்': 'ಕುಂಭ', 'மீனம்': 'ಮೀನ',
        # House terms
        'திரிகோண வீடு': 'ತ್ರಿಕೋಣ ಮನೆ', 'கேந்திர வீடு': 'ಕೇಂದ್ರ ಮನೆ',
        'தன வீடு': 'ಧನ ಮನೆ', 'உபச்சய வீடு': 'ಉಪಚಯ ಮನೆ',
        'துஷ்டான வீடு': 'ದುಷ್ಟಾನ ಮನೆ',
        'ஆம் வீட்டதிபதி': 'ಮನೆ ಅಧಿಪತಿ', 'வீட்டில்': 'ಮನೆಯಲ್ಲಿ',
        'ஆம் வீட்டில்': 'ಮನೆಯಲ್ಲಿ', 'ஆம் வீடு': 'ಮನೆ',
        'சொந்த வீடு': 'ಸ್ವಂತ ಮನೆ', 'வீடு': 'ಮನೆ',
        'கேந்திரம் நல்லது': 'ಕೇಂದ್ರ ಒಳ್ಳೆಯದು',
        # Dignity terms
        'உச்சம்': 'ಉಚ್ಚ', 'சொந்த': 'ಸ್ವಕ್ಷೇತ್ರ', 'நட்பு': 'ಮಿತ್ರ',
        'சமம்': 'ಸಮ', 'பகை': 'ಶತ್ರು', 'நீசம்': 'ನೀಚ',
        # Aspect terms
        'குரு பார்வை': 'ಗುರು ದೃಷ್ಟಿ', 'சனி பார்வை': 'ಶನಿ ದೃಷ್ಟಿ',
        'பார்வை': 'ದೃಷ್ಟಿ',
        # Transit/Sade Sati terms
        'சடேசதி': 'ಸಡೇಸತಿ', 'சாதகமான சனி': 'ಅನುಕೂಲ ಶನಿ',
        'கண்டக சனி': 'ಕಂಟಕ ಶನಿ', 'அஷ்டம சனி': 'ಅಷ್ಟಮ ಶನಿ',
        'நடுப்பகுதி': 'ಮಧ್ಯ ಹಂತ',
        # Quality terms
        'சாதகமான': 'ಅನುಕೂಲ', 'சவால்': 'ಸವಾಲು',
        'சிறப்பு': 'ಅತ್ಯುತ್ತಮ', 'நல்லது': 'ಒಳ್ಳೆಯದು', 'கலப்பு': 'ಮಿಶ್ರ',
        'மிகச்சிறந்தது': 'ಅತ್ಯುತ್ತಮ', 'சராசரி': 'ಸಾಮಾನ್ಯ',
        'சவாலானது': 'ಸವಾಲು', 'கடினமானது': 'ಕಷ್ಟಕರ',
        # Karaka terms
        'காரகன்': 'ಕಾರಕ', 'தசை = காரகம்': 'ದಶೆ = ಕಾರಕ',
        # Yoga names
        'கஜகேசரி யோகம்': 'ಗಜಕೇಸರಿ ಯೋಗ',
        'புத ஆதித்ய யோகம்': 'ಬುಧ ಆದಿತ್ಯ ಯೋಗ',
        'சந்திர மங்கள யோகம்': 'ಚಂದ್ರ ಮಂಗಳ ಯೋಗ',
        'ராஜ யோகம்': 'ರಾಜ ಯೋಗ',
        # Dosha names
        'கால சர்ப்ப தோஷம்': 'ಕಾಲ ಸರ್ಪ ದೋಷ',
        'கேமத்ருமா தோஷம்': 'ಕೇಮದ್ರುಮ ದೋಷ',
        # Other terms
        'யோகம்': 'ಯೋಗ', 'தோஷம்': 'ದೋಷ',
        'நவாம்ச பலம்': 'ನವಾಂಶ ಬಲ', 'நவாம்ச': 'ನವಾಂಶ',
        'ஆரம்பம்': 'ಆರಂಭ', 'முடிவு': 'ಅಂತ್ಯ',
        'இல்': 'ಅಲ್ಲಿ', 'பலவீனம்': 'ದೌರ್ಬಲ್ಯ',
        # Eclipse terms
        'சூரிய கிரகணம்': 'ಸೂರ್ಯ ಗ್ರಹಣ', 'சந்திர கிரகணம்': 'ಚಂದ್ರ ಗ್ರಹಣ',
        'கிரகண கால பாதிப்பு': 'ಗ್ರಹಣ ಕಾಲ ಪ್ರಭಾವ',
        'வக்கிர கால பாதிப்பு': 'ವಕ್ರ ಕಾಲ ಪ್ರಭಾವ',
        # Rahu-Ketu terms
        'ராகு-கேது 1/7 அச்சு': 'ರಾಹು-ಕೇತು 1/7 ಅಕ್ಷ',
        # Detailed message translations
        'பொறுமை தேவை': 'ತಾಳ್ಮೆ ಬೇಕು',
        'கடின உழைப்பு வெற்றி தரும்': 'ಕಠಿಣ ಪರಿಶ್ರಮ ಯಶಸ್ಸು ತರುತ್ತದೆ',
        'ஆரோக்கியம் கவனிக்க': 'ಆರೋಗ್ಯ ಗಮನಿಸಿ',
        'பெரிய முடிவுகள் தவிர்க்க': 'ದೊಡ್ಡ ನಿರ್ಧಾರಗಳನ್ನು ತಪ್ಪಿಸಿ',
        'தொழில்/குடும்பத்தில் சவால்': 'ವೃತ್ತಿ/ಕುಟುಂಬದಲ್ಲಿ ಸವಾಲು',
        'திட்டமிட்டு செயல்படுக': 'ಯೋಜನೆಯೊಂದಿಗೆ ಕಾರ್ಯನಿರ್ವಹಿಸಿ',
        'கடின உழைப்புக்கு பலன் கிடைக்கும்': 'ಕಠಿಣ ಪರಿಶ್ರಮಕ್ಕೆ ಫಲ ಸಿಗುತ್ತದೆ',
        'மன குழப்பம்': 'ಮಾನಸಿಕ ಗೊಂದಲ',
        'முக்கிய முடிவுகள் தாமதிக்க': 'ಮುಖ್ಯ ನಿರ್ಧಾರಗಳನ್ನು ತಡಮಾಡಿ',
        'திடீர் மாற்றங்கள்': 'ಇದ್ದಕ್ಕಿದ್ದಂತೆ ಬದಲಾವಣೆಗಳು',
        'எச்சரிக்கையாக இருக்க': 'ಎಚ್ಚರಿಕೆಯಿಂದಿರಿ',
        'குழப்பம் வரலாம்': 'ಗೊಂದಲ ಬರಬಹುದು',
        'தெளிவாக சிந்திக்க': 'ಸ್ಪಷ್ಟವಾಗಿ ಯೋಚಿಸಿ',
        'சக்தி மற்றும் துணிவு': 'ಶಕ್ತಿ ಮತ್ತು ಧೈರ್ಯ',
        'புதிய தொடக்கங்கள் தவிர்க்க': 'ಹೊಸ ಆರಂಭಗಳನ್ನು ತಪ್ಪಿಸಿ',
        'மன அமைதி பாதிப்பு': 'ಮಾನಸಿಕ ಶಾಂತಿ ಪ್ರಭಾವಿತ',
        'முக்கிய முடிவுகள் தள்ளிவைக்க': 'ಮುಖ್ಯ ನಿರ್ಧಾರಗಳನ್ನು ಮುಂದೂಡಿ',
        # House effect messages
        'உடல் ஆரோக்கியம் கவனிக்க': 'ದೈಹಿಕ ಆರೋಗ್ಯ ಗಮನಿಸಿ',
        'நிதி நிலை சீராகும்': 'ಆರ್ಥಿಕ ಸ್ಥಿತಿ ಸ್ಥಿರವಾಗುತ್ತದೆ',
        'தைரியமும் வெற்றியும்': 'ಧೈರ್ಯ ಮತ್ತು ಯಶಸ್ಸು',
        'மன அமைதி குறையும்': 'ಮಾನಸಿಕ ಶಾಂತಿ ಕಡಿಮೆಯಾಗಬಹುದು',
        'புத்தி தெளிவு, நல்ல முடிவுகள்': 'ಬುದ್ಧಿ ಸ್ಪಷ್ಟತೆ, ಒಳ್ಳೆಯ ನಿರ್ಧಾರಗಳು',
        'எதிரிகள் மீது வெற்றி': 'ಶತ್ರುಗಳ ಮೇಲೆ ಜಯ',
        'உறவுகளில் சிக்கல் வரலாம்': 'ಸಂಬಂಧಗಳಲ್ಲಿ ತೊಂದರೆ ಬರಬಹುದು',
        'தடைகள், பொறுமை தேவை': 'ಅಡೆತಡೆಗಳು, ತಾಳ್ಮೆ ಬೇಕು',
        'அதிர்ஷ்டம், தர்மம் வளரும்': 'ಅದೃಷ್ಟ, ಧರ್ಮ ಬೆಳೆಯುತ್ತದೆ',
        'தொழில் வெற்றி': 'ವೃತ್ತಿ ಯಶಸ್ಸು',
        'லாபம், ஆதாயம்': 'ಲಾಭ, ಪ್ರಯೋಜನ',
        'செலவுகள் அதிகரிக்கும்': 'ಖರ್ಚುಗಳು ಹೆಚ್ಚಾಗುತ್ತವೆ',
        # Confidence reasons
        'வலுவான ராசி ஆனால் நவாம்ச பலவீனம் - நம்பகத்தன்மை குறைவு': 'ಬಲಶಾಲಿ ರಾಶಿ ಆದರೆ ದುರ್ಬಲ ನವಾಂಶ - ಕಡಿಮೆ ವಿಶ್ವಾಸಾರ್ಹತೆ',
        'வலுவான தசை கோசார பாதிப்பை குறைக்கிறது': 'ಬಲಶಾಲಿ ದಶೆ ಗೋಚಾರ ಪ್ರಭಾವವನ್ನು ಕಡಿಮೆ ಮಾಡುತ್ತದೆ',
        'ஒரு வலுவான அம்சம் ஆதிக்கம் செலுத்துகிறது': 'ಒಂದು ಬಲಶಾಲಿ ಅಂಶ ಪ್ರಾಬಲ್ಯ ಹೊಂದಿದೆ',
        'அதிக மதிப்பெண்களுக்கு நிதான சரிசெய்தல்': 'ಹೆಚ್ಚಿನ ಅಂಕಗಳಿಗೆ ಸಂಯಮ ಹೊಂದಾಣಿಕೆ',
        'யோகம் பலவீனங்களை சமன் செய்கிறது': 'ಯೋಗ ದೌರ್ಬಲ್ಯಗಳನ್ನು ಸರಿದೂಗಿಸುತ್ತದೆ',
    }
}


def translate_factor_text(text: str, lang: str = 'ta') -> str:
    """Translate Tamil factor text to target language"""
    if lang == 'ta' or not text:
        return text

    translations = FACTOR_TRANSLATIONS.get(lang, {})
    result = text

    # Replace known terms - sort by length descending to replace longer phrases first
    sorted_terms = sorted(translations.items(), key=lambda x: len(x[0]), reverse=True)
    for tamil, translated in sorted_terms:
        result = result.replace(tamil, translated)

    return result


def translate_factors(factors: List[Dict], lang: str = 'ta') -> List[Dict]:
    """Translate a list of factors to the target language"""
    if lang == 'ta' or not factors:
        return factors

    translated = []
    for factor in factors:
        new_factor = factor.copy()
        if 'name' in new_factor:
            new_factor['name'] = translate_factor_text(new_factor['name'], lang)
        if 'detail' in new_factor:
            new_factor['detail'] = translate_factor_text(new_factor['detail'], lang)
        translated.append(new_factor)
    return translated


def translate_calculation_trace(trace: Dict, lang: str = 'ta') -> Dict:
    """Translate calculation_trace factors to the target language"""
    if lang == 'ta' or not trace:
        return trace

    translated_trace = trace.copy()

    # Translate step_by_step factors
    if 'step_by_step' in translated_trace:
        new_steps = []
        for step in translated_trace['step_by_step']:
            new_step = step.copy()
            if 'factors_detail' in new_step:
                new_step['factors_detail'] = translate_factors(new_step['factors_detail'], lang)
            new_steps.append(new_step)
        translated_trace['step_by_step'] = new_steps

    return translated_trace


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
        life_area: str = 'general',
        lang: str = 'ta'
    ) -> str:
        """Generate personalized recommendation based on all factors"""
        recommendations = []

        # Base recommendation from score (using translation function)
        base_rec = get_recommendation(quality, life_area, lang)
        if base_rec:
            recommendations.append(base_rec)

        # Dasha-specific advice (using translation function)
        dasha_rec = get_dasha_recommendation(dasha_lord, lang)
        if dasha_rec:
            recommendations.append(dasha_rec)

        # Transit-specific advice
        saturn_from_moon = transit_info.get('saturn_from_moon', 0)
        jupiter_from_moon = transit_info.get('jupiter_from_moon', 0)

        if saturn_from_moon in [12, 1, 2]:
            recommendations.append(get_transit_recommendation('sadesati', lang))
        elif saturn_from_moon == 8:
            recommendations.append(get_transit_recommendation('ashtama_shani', lang))
        elif saturn_from_moon in [4, 7, 10]:
            recommendations.append(get_transit_recommendation('kantaka_shani', lang))

        if jupiter_from_moon in [3, 5, 9, 10, 11]:
            recommendations.append(get_transit_recommendation('jupiter_good', lang))
        elif jupiter_from_moon in [1, 6, 8, 12]:
            recommendations.append(get_transit_recommendation('jupiter_bad', lang))

        return ' '.join(recommendations[:3])  # Max 3 recommendations

    def _get_score_quality_label(self, score: float, lang: str = 'ta') -> str:
        """Get quality label based on score - V6.2 thresholds for more positive output"""
        if score >= 75:
            quality = 'excellent'
        elif score >= 60:
            quality = 'good'
        elif score >= 45:
            quality = 'average'
        elif score >= 30:
            quality = 'challenging'
        else:
            quality = 'difficult'
        return get_quality_label(quality, lang)

    def _generate_detailed_breakdown(self, result: Dict, dasha_lord: str, lang: str = 'ta') -> Dict:
        """Generate detailed breakdown explanation"""
        breakdown = result.get('breakdown', {})

        planet_name = get_planet_name(dasha_lord, lang)
        dasha_running_text = get_translation('dasha_running', lang)

        explanations = {
            'dasha': {
                'score': breakdown.get('dasha', {}).get('score', 0),
                'weight': '30%',
                'explanation': f"{planet_name} {dasha_running_text}. " +
                              self._get_dasha_explanation(dasha_lord, breakdown.get('dasha', {}).get('raw', 0), lang)
            },
            'house': {
                'score': breakdown.get('house', {}).get('score', 0),
                'weight': '20%',
                'explanation': self._get_house_explanation(breakdown.get('house', {}), lang)
            },
            'transit': {
                'score': breakdown.get('transit', {}).get('score', 0),
                'weight': '15%',
                'explanation': self._get_transit_explanation(breakdown.get('transit', {}), lang)
            },
            'planet_strength': {
                'score': breakdown.get('planet_strength', {}).get('score', 0),
                'weight': '15%',
                'explanation': self._get_strength_explanation(breakdown.get('planet_strength', {}), lang)
            },
            'yoga': {
                'score': breakdown.get('yoga', {}).get('score', 0),
                'weight': '10%',
                'explanation': self._get_yoga_explanation(breakdown.get('yoga', {}), lang)
            },
            'navamsa': {
                'score': breakdown.get('navamsa', {}).get('score', 0),
                'weight': '10%',
                'explanation': get_translation('navamsa_power', lang)
            }
        }

        return explanations

    def _get_dasha_explanation(self, dasha_lord: str, raw_score: float, lang: str = 'ta') -> str:
        """Get explanation for dasha score"""
        planet_name = get_planet_name(dasha_lord, lang)
        if raw_score >= 25:
            return f"{get_translation('very_favorable_dasha', lang)}. {planet_name} {get_translation('is_strong', lang)}."
        elif raw_score >= 18:
            return f"{get_translation('good_dasha', lang)}. {planet_name} {get_translation('is_moderately_strong', lang)}."
        elif raw_score >= 10:
            return get_translation('average_dasha', lang)
        else:
            return get_translation('challenging_dasha', lang)

    def _get_house_explanation(self, house_info: Dict, lang: str = 'ta') -> str:
        """Get explanation for house score"""
        factors = house_info.get('factors', [])
        if factors:
            factor_names = [translate_factor_text(f.get('name', ''), lang) for f in factors[:2]]
            return f"{get_translation('house_power', lang)}: {', '.join(factor_names)}"
        return get_translation('house_power_calculated', lang)

    def _get_transit_explanation(self, transit_info: Dict, lang: str = 'ta') -> str:
        """Get explanation for transit score"""
        factors = transit_info.get('factors', [])
        explanations = []
        for f in factors[:2]:
            name = translate_factor_text(f.get('name', ''), lang)
            detail = translate_factor_text(f.get('detail', ''), lang)
            if detail:
                explanations.append(f"{name}: {detail}")
            else:
                explanations.append(name)
        return '. '.join(explanations) if explanations else get_translation('transit_power_calculated', lang)

    def _get_strength_explanation(self, strength_info: Dict, lang: str = 'ta') -> str:
        """Get explanation for planet strength"""
        factors = strength_info.get('factors', [])
        if factors:
            explanations = []
            for f in factors[:2]:
                name = translate_factor_text(f.get('name', ''), lang)
                detail = translate_factor_text(f.get('detail', ''), lang)
                if detail:
                    explanations.append(f"{name} {detail}")
            return ', '.join(explanations) if explanations else get_translation('planet_power_calculated', lang)
        return get_translation('planet_power_calculated', lang)

    def _get_yoga_explanation(self, yoga_info: Dict, lang: str = 'ta') -> str:
        """Get explanation for yoga score"""
        factors = yoga_info.get('factors', [])
        if factors:
            yoga_names = [translate_factor_text(f.get('name', ''), lang) for f in factors if f.get('positive', True)]
            dosha_names = [translate_factor_text(f.get('name', ''), lang) for f in factors if not f.get('positive', True)]
            parts = []
            if yoga_names:
                parts.append(f"{get_translation('yoga', lang)}: {', '.join(yoga_names)}")
            if dosha_names:
                parts.append(f"{get_translation('dosha', lang)}: {', '.join(dosha_names)}")
            return '. '.join(parts) if parts else get_translation('yoga_dosha_power', lang)
        return get_translation('yoga_dosha_calculated', lang)

    def calculate_monthly_projection(
        self,
        jathagam: Dict,
        dasha_info: Dict,
        month: int,
        year: int,
        lang: str = 'ta'
    ) -> Dict[str, Any]:
        """
        Calculate projection for a specific month using V5.0 TimeAdaptiveEngine.

        V5.0 UPGRADE: Now uses TimeAdaptiveEngine for month-specific calculations.
        All modules recalculate per month with proper transit overlay.
        """

        target_date = date(year, month, 15)  # Mid-month

        # Get dasha lords
        dasha_lord = dasha_info.get('mahadasha_lord') or dasha_info.get('mahadasha', 'Jupiter')
        bhukti_lord = dasha_info.get('antardasha_lord') or dasha_info.get('antardasha')

        # V5.0: Use TimeAdaptiveEngine if available
        if V41_ENGINE_AVAILABLE:
            engine = TimeAdaptiveEngine(jathagam)
        else:
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
            life_area='general',
            lang=lang
        )

        # Get translated quality label
        quality_label = get_quality_label(result.get('quality', 'average'), lang)

        # Translate factors and calculation_trace if not Tamil
        translated_factors = translate_factors(factors, lang)
        translated_trace = translate_calculation_trace(result.get('calculation_trace', {}), lang)

        return {
            'name': get_month_name(month, lang),
            'month': month,
            'year': year,
            'score': round(result['score'], 1),
            'quality': quality_label,
            'factors': translated_factors,
            'recommendation': recommendation,
            'breakdown': {
                'dasha': result['breakdown']['dasha']['score'],
                'transit': result['breakdown']['transit']['score'],
                'house': result['breakdown']['house']['score'],
                'planet_strength': result['breakdown']['planet_strength']['score'],
                'yoga': result['breakdown']['yoga']['score'],
                'navamsa': result['breakdown']['navamsa']['score'],
            },
            'calculation_trace': translated_trace,
            'dasha_lord': dasha_lord,
            'dasha_lord_label': get_planet_name(dasha_lord, lang),
            'bhukti_lord': bhukti_lord,
            'bhukti_lord_label': get_planet_name(bhukti_lord, lang) if bhukti_lord else None
        }

    def calculate_yearly_projection(
        self,
        jathagam: Dict,
        dasha_info: Dict,
        year: int,
        label: str,
        lang: str = 'ta'
    ) -> Dict[str, Any]:
        """
        Calculate projection for a specific year using V5.0 TimeAdaptiveEngine.

        V5.0 UPGRADE: Now uses TimeAdaptiveEngine for year-specific calculations.
        All modules (POI, HAI, Dasha, Transit, Yoga, Navamsa) recalculate per year.
        """

        target_date = date(year, 6, 15)  # Mid-year

        # Get dasha lords
        dasha_lord = dasha_info.get('mahadasha_lord') or dasha_info.get('mahadasha', 'Jupiter')
        bhukti_lord = dasha_info.get('antardasha_lord') or dasha_info.get('antardasha')

        # V5.0: Use TimeAdaptiveEngine if available
        if V41_ENGINE_AVAILABLE:
            engine = TimeAdaptiveEngine(jathagam)
        else:
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

            # Get area-specific recommendation (using translation function)
            area_quality = result.get('quality', 'average')
            area_rec = get_recommendation(area_quality, area, lang)
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

        # Generate detailed breakdown explanations (with translations)
        detailed_breakdown = self._generate_detailed_breakdown(general_result, dasha_lord, lang)

        # Generate personalized recommendation
        recommendation = self._get_personalized_recommendation(
            score=overall_score,
            quality=general_result.get('quality', 'average'),
            dasha_lord=dasha_lord,
            transit_info=transits,
            life_area='general',
            lang=lang
        )

        # Get translated quality label
        quality_label = get_quality_label(general_result.get('quality', 'average'), lang)

        # Translate factors and calculation_trace if not Tamil
        translated_factors = translate_factors(factors, lang)
        translated_trace = translate_calculation_trace(general_result.get('calculation_trace', {}), lang)

        return {
            'year': year,
            'label': label,
            'score': round(overall_score, 1),
            'quality': quality_label,
            'factors': translated_factors,
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
            'calculation_trace': translated_trace,
            'dasha_lord': dasha_lord,
            'dasha_lord_label': get_planet_name(dasha_lord, lang),
            'bhukti_lord': bhukti_lord,
            'bhukti_lord_label': get_planet_name(bhukti_lord, lang) if bhukti_lord else None
        }

    def calculate_projections(
        self,
        jathagam: Dict,
        dasha_info: Dict,
        lang: str = 'ta'
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
                jathagam, dasha_for_month, month, year, lang
            )
            monthly_projections.append(projection)

        # Generate 3 yearly projections with translated labels
        yearly_projections = []
        for i in range(3):
            target_year = current_year + i

            # Get translated year label
            label = get_year_label(i, lang)

            # Get correct dasha for mid-year of each year
            target_date = date(target_year, 6, 15)
            if dasha_timeline:
                dasha_for_year = self._get_dasha_for_date(target_date, dasha_timeline)
            else:
                dasha_for_year = dasha_info

            projection = self.calculate_yearly_projection(
                jathagam, dasha_for_year, target_year, label, lang
            )
            yearly_projections.append(projection)

        # Generate past 2 years using V6.2 TimeAdaptiveEngine with 'past' mode
        past_yearly_projections = []
        for i in range(2, 0, -1):  # 2 years ago, 1 year ago
            target_year = current_year - i
            target_date = date(target_year, 6, 15)  # Mid-year

            # Get correct dasha for that past year
            if dasha_timeline:
                dasha_for_year = self._get_dasha_for_date(target_date, dasha_timeline)
            else:
                dasha_for_year = dasha_info

            dasha_lord = dasha_for_year.get('mahadasha_lord') or dasha_for_year.get('mahadasha', 'Jupiter')

            # Use TimeAdaptiveEngine with 'past' mode for accurate past analysis
            if V41_ENGINE_AVAILABLE:
                engine = TimeAdaptiveEngine(jathagam)
                result = engine.calculate_prediction_v41(
                    target_date=target_date,
                    life_area='general',
                    mode_hint='past',
                    dasha_lord=dasha_lord
                )
                past_score = result.get('final_score', 50)
            else:
                engine = AstroPercentEngine(jathagam)
                result = engine.calculate_prediction_score(
                    target_date=target_date,
                    life_area='general',
                    dasha_lord=dasha_lord
                )
                past_score = result.get('score', 50)

            past_yearly_projections.append({
                'year': target_year,
                'score': round(past_score, 1),
                'dasha': dasha_lord,
                'dasha_label': get_planet_name(dasha_lord, lang),
                'quality': self._get_score_quality_label(past_score, lang),
                'is_past': True
            })

        # Summary statistics
        avg_monthly = sum(p['score'] for p in monthly_projections) / len(monthly_projections)
        best_month = max(monthly_projections, key=lambda x: x['score'])
        challenging_month = min(monthly_projections, key=lambda x: x['score'])

        return {
            'monthly': monthly_projections,
            'yearly': yearly_projections,
            'past_years': past_yearly_projections,
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
                    'lord_label': get_planet_name(d['lord'], lang),
                    'start': d['start'].strftime('%Y-%m-%d'),
                    'end': d['end'].strftime('%Y-%m-%d')
                }
                for d in dasha_timeline[:12]  # Show next 12 dasha periods
            ] if dasha_timeline else [],
            'generated_at': datetime.now().isoformat()
        }

    # ==================== V4.1 TIME-ADAPTIVE ENGINE METHODS ====================

    def calculate_projection_v41(
        self,
        jathagam: Dict,
        target_date: date,
        life_area: str = 'general',
        mode_hint: str = None,
        dasha_lord: str = None,
        bhukti_lord: str = None,
        antara_lord: str = None,
        lang: str = 'ta'
    ) -> Dict[str, Any]:
        """
        v4.1 Time-Adaptive prediction with full explainability trace.

        This method uses the TimeAdaptiveEngine which automatically:
        - Detects and applies time mode (past/present/future/monthly/yearly)
        - Adjusts weights based on temporal context
        - Calculates POI (Planet Operational Intensity) per planet
        - Calculates HAI (House Activation Index) per house
        - Provides full mathematical reasoning trace
        - Returns confidence score with breakdown

        Args:
            jathagam: Birth chart data
            target_date: Date for prediction
            life_area: Domain ('general', 'career', 'finance', 'health', 'relationships')
            mode_hint: Force specific mode ('past', 'future', 'monthly', 'yearly')
            dasha_lord: Mahadasha lord (auto-detected if not provided)
            bhukti_lord: Antardasha lord (auto-detected if not provided)
            antara_lord: Pratyantardasha lord (optional)
            lang: Language code ('ta', 'en', 'kn')

        Returns:
            Dict with v4.1 prediction including:
            - time_mode: Which mode was activated and weight modifications
            - module_scores: All 6 modules with tensor breakdowns
            - poi_values: Planet Operational Intensities
            - hai_values: House Activation Indices
            - final_score: Calculated prediction (0-100)
            - confidence: Confidence score with breakdown
            - reasoning_trace: Mathematical calculation steps
        """
        if not V41_ENGINE_AVAILABLE:
            # Fallback to v3.0 engine
            engine = AstroPercentEngine(jathagam)
            result = engine.calculate_prediction_score(
                target_date=target_date,
                life_area=life_area,
                dasha_lord=dasha_lord,
                bhukti_lord=bhukti_lord
            )
            result['engine_version'] = '3.0 (fallback)'
            result['v41_unavailable'] = True
            return result

        # Use v4.1 TimeAdaptiveEngine
        engine = TimeAdaptiveEngine(jathagam)

        result = engine.calculate_prediction_v41(
            target_date=target_date,
            life_area=life_area,
            mode_hint=mode_hint,
            dasha_lord=dasha_lord,
            bhukti_lord=bhukti_lord,
            antara_lord=antara_lord
        )

        # Apply translations if not Tamil
        if lang != 'ta':
            # Translate top drivers
            if 'top_positive_drivers' in result:
                for driver in result['top_positive_drivers']:
                    if 'module' in driver:
                        driver['module_label'] = get_translation(f"module_{driver['module']}", lang)

            if 'top_negative_drivers' in result:
                for driver in result['top_negative_drivers']:
                    if 'module' in driver:
                        driver['module_label'] = get_translation(f"module_{driver['module']}", lang)

            # Translate confidence interpretation
            if 'confidence' in result:
                conf = result['confidence']
                if conf['score'] >= 70:
                    conf['interpretation'] = get_translation('high_confidence', lang)
                elif conf['score'] >= 50:
                    conf['interpretation'] = get_translation('medium_confidence', lang)
                else:
                    conf['interpretation'] = get_translation('low_confidence', lang)

        return result

    def calculate_monthly_projections_v41(
        self,
        jathagam: Dict,
        year: int,
        life_area: str = 'general',
        dasha_lord: str = None,
        bhukti_lord: str = None,
        lang: str = 'ta'
    ) -> Dict[str, Any]:
        """
        v4.1 Month-wise projections with POI/HAI recalculation per month.

        Time Mode Applied: MONTH_WISE
        - Splits transits into 30-day arcs
        - Recomputes POI and HAI per month
        - Applies monthly smoothing (score ^ 0.92)
        - Navamsa multipliers constant across months
        - Yogas static but strength varies by transit support

        Returns:
            Dict with monthly array, summary, and engine metadata
        """
        if not V41_ENGINE_AVAILABLE:
            # Fallback to v3.0 engine via existing method
            dasha_info = {
                'mahadasha_lord': dasha_lord or 'Jupiter',
                'antardasha_lord': bhukti_lord
            }
            return self.calculate_projections(jathagam, dasha_info, lang)

        engine = TimeAdaptiveEngine(jathagam)
        result = engine.calculate_monthly_projections_v41(
            year=year,
            life_area=life_area,
            dasha_lord=dasha_lord,
            bhukti_lord=bhukti_lord
        )

        # Apply language translations
        if lang != 'ta':
            for month_data in result.get('monthly', []):
                month_num = month_data.get('month', 1)
                month_data['month_name'] = get_month_name(month_num, lang)

        return result

    def calculate_yearly_projection_v41(
        self,
        jathagam: Dict,
        year: int,
        life_area: str = 'general',
        dasha_lord: str = None,
        lang: str = 'ta'
    ) -> Dict[str, Any]:
        """
        v4.1 Yearly projection with Varshaphal (Solar Return) integration.

        Time Mode Applied: YEAR_OVERLAY
        - Adds VarshaphalInteractionScore to PlanetPower module
        - Reduces Transit module weight by 25% (macro-scale)
        - Adds year_trend_multiplier = Varshaphal_POI × 0.01
        - Includes Muntha sign and year lord calculations

        Returns:
            Dict with yearly prediction including Varshaphal data
        """
        if not V41_ENGINE_AVAILABLE:
            # Fallback
            dasha_info = {'mahadasha_lord': dasha_lord or 'Jupiter'}
            return self.calculate_yearly_projection(
                jathagam, dasha_info, year, get_year_label(0, lang), lang
            )

        engine = TimeAdaptiveEngine(jathagam)
        result = engine.calculate_yearly_projection_v41(
            year=year,
            life_area=life_area,
            dasha_lord=dasha_lord
        )

        # Apply language translations
        if lang != 'ta' and 'varshaphal' in result:
            vp = result['varshaphal']
            if 'year_lord' in vp:
                vp['year_lord_label'] = get_planet_name(vp['year_lord'], lang)

        return result

    def calculate_past_analysis_v41(
        self,
        jathagam: Dict,
        target_date: date,
        life_area: str = 'general',
        dasha_lord: str = None,
        lang: str = 'ta'
    ) -> Dict[str, Any]:
        """
        v4.1 Past event analysis with historical verification mode.

        Time Mode Applied: PAST_ANALYSIS
        - Uses actual historical transit data for that date
        - Uses exact running Dasha-Bhukti-Antara for that period
        - No forward-looking modifiers applied
        - Navamsa amplification reduced by 20%
        - Transit weight increased to 0.28 for event verification
        - Monthly-window compression (only monthly transit arc)

        Useful for:
        - Verifying past events against chart
        - Understanding past outcomes
        - Analyzing historical decisions
        - Retrospective dasha impact analysis

        Returns:
            Dict with past analysis result and verification score
        """
        if not V41_ENGINE_AVAILABLE:
            engine = AstroPercentEngine(jathagam)
            return engine.calculate_prediction_score(
                target_date=target_date,
                life_area=life_area,
                dasha_lord=dasha_lord
            )

        engine = TimeAdaptiveEngine(jathagam)
        return engine.calculate_prediction_v41(
            target_date=target_date,
            life_area=life_area,
            mode_hint='past',
            dasha_lord=dasha_lord
        )

    def is_v41_available(self) -> bool:
        """Check if v4.1 Time-Adaptive Engine is available"""
        return V41_ENGINE_AVAILABLE


# For backward compatibility
def calculate_projections(jathagam: Dict, dasha_info: Dict, lang: str = 'ta') -> Dict:
    """Backward compatible function"""
    service = FutureProjectionService()
    return service.calculate_projections(jathagam, dasha_info, lang)
