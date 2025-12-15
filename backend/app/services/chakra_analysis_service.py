"""
Chakra Analysis Service - Vedic Astrology Based Chakra Assessment
Maps planetary influences to the seven chakras using authentic Jyotish principles

SCORING FORMULA:
ChakraScore = (0.35 × PlanetShadbalaNorm) + (0.20 × BhavaStrength) +
              (0.20 × AshtakavargaWeighted) + (0.10 × TransitImpact) +
              (0.15 × DashaInfluence)

Based on traditional Vedic mappings:
- Muladhara (Root): Mars + Ketu, Houses 1, 4, 8
- Swadhisthana (Sacral): Venus, Houses 2, 7, 12
- Manipura (Solar Plexus): Sun + Jupiter, Houses 3, 6, 10
- Anahata (Heart): Moon, Houses 4, 5, 7
- Vishuddha (Throat): Mercury, Houses 2, 3, 5
- Ajna (Third Eye): Saturn + Rahu, Houses 8, 9, 12
- Sahasrara (Crown): Jupiter + Ketu, Houses 5, 9, 12
"""

from datetime import datetime, date
from typing import Dict, List, Optional, Any
import math


# Friend/Enemy relationships for Bhava strength calculation
PLANET_FRIENDS = {
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

PLANET_ENEMIES = {
    'Sun': ['Venus', 'Saturn'],
    'Moon': ['Rahu', 'Ketu'],
    'Mars': ['Mercury'],
    'Mercury': ['Moon'],
    'Jupiter': ['Mercury', 'Venus'],
    'Venus': ['Sun', 'Moon'],
    'Saturn': ['Sun', 'Moon', 'Mars'],
    'Rahu': ['Sun', 'Moon', 'Mars'],
    'Ketu': ['Moon']
}

# Personality manifestations per chakra and status
PERSONALITY_MANIFESTATIONS = {
    "Muladhara": {
        "balanced": {
            "en": "Grounded personality with strong sense of security. Practical approach to life, reliable, patient.",
            "ta": "வலுவான பாதுகாப்பு உணர்வுடன் நிலைபெற்ற ஆளுமை. நடைமுறை அணுகுமுறை, நம்பகமான, பொறுமையான.",
            "kn": "ಬಲವಾದ ಭದ್ರತಾ ಪ್ರಜ್ಞೆಯೊಂದಿಗೆ ಸ್ಥಿರ ವ್ಯಕ್ತಿತ್ವ. ಪ್ರಾಯೋಗಿಕ ವಿಧಾನ, ನಂಬಿಕಸ್ಥ, ತಾಳ್ಮೆಯುಳ್ಳ."
        },
        "overactive": {
            "en": "Excessive materialism, hoarding tendency, resistance to change. Stubbornness or workaholism.",
            "ta": "அதிக பொருளாசை, சேகரிக்கும் போக்கு, மாற்றத்தை எதிர்ப்பு. பிடிவாதம் அல்லது வேலை போதை.",
            "kn": "ಅತಿಯಾದ ಭೌತವಾದ, ಸಂಗ್ರಹಣೆಯ ಪ್ರವೃತ್ತಿ, ಬದಲಾವಣೆಗೆ ಪ್ರತಿರೋಧ. ಹಠಮಾರಿತನ."
        },
        "underactive": {
            "en": "Feelings of insecurity, anxiety about survival, disconnection from body. Financial instability.",
            "ta": "பாதுகாப்பின்மை உணர்வு, உயிர்வாழ்வு பற்றிய கவலை. நிலையற்ற நிதி நிலை.",
            "kn": "ಅಭದ್ರತೆಯ ಭಾವನೆಗಳು, ಬದುಕುಳಿಯುವ ಬಗ್ಗೆ ಆತಂಕ. ಆರ್ಥಿಕ ಅಸ್ಥಿರತೆ."
        },
        "blocked": {
            "en": "Deep-seated fear and survival anxiety. Chronic health issues related to legs, bones.",
            "ta": "ஆழமான பயம் மற்றும் உயிர்வாழ்வு கவலை. கால்கள், எலும்புகள் தொடர்பான பிரச்சினைகள்.",
            "kn": "ಆಳವಾದ ಭಯ ಮತ್ತು ಬದುಕುಳಿಯುವ ಆತಂಕ. ಕಾಲುಗಳು, ಮೂಳೆಗಳಿಗೆ ಸಂಬಂಧಿಸಿದ ಸಮಸ್ಯೆಗಳು."
        }
    },
    "Swadhisthana": {
        "balanced": {
            "en": "Creative, emotionally intelligent, healthy relationships. Adaptable and flowing with life.",
            "ta": "படைப்பாற்றல், உணர்வுபூர்வ புத்திசாலித்தனம், ஆரோக்கியமான உறவுகள். வாழ்க்கையுடன் தழுவல்.",
            "kn": "ಸೃಜನಶೀಲ, ಭಾವನಾತ್ಮಕವಾಗಿ ಬುದ್ಧಿವಂತ, ಆರೋಗ್ಯಕರ ಸಂಬಂಧಗಳು. ಹೊಂದಿಕೊಳ್ಳುವ."
        },
        "overactive": {
            "en": "Emotional volatility, addictive tendencies, excessive pleasure-seeking.",
            "ta": "உணர்வு மாறுபாடு, அடிமைத்தனப் போக்குகள், அதிக இன்பம் தேடுதல்.",
            "kn": "ಭಾವನಾತ್ಮಕ ಅಸ್ಥಿರತೆ, ವ್ಯಸನಕಾರಿ ಪ್ರವೃತ್ತಿಗಳು, ಅತಿಯಾದ ಸುಖ-ಹುಡುಕುವಿಕೆ."
        },
        "underactive": {
            "en": "Emotional numbness, creative blocks, difficulty with intimacy. Fear of pleasure.",
            "ta": "உணர்வு மரத்துப்போதல், படைப்பு தடைகள், நெருக்கத்தில் சிரமம். இன்பத்தின் பயம்.",
            "kn": "ಭಾವನಾತ್ಮಕ ಮರಗಟ್ಟುವಿಕೆ, ಸೃಜನಶೀಲ ತಡೆಗಳು, ಆತ್ಮೀಯತೆಯಲ್ಲಿ ಕಷ್ಟ."
        },
        "blocked": {
            "en": "Severe emotional repression, reproductive issues, complete disconnection from desires.",
            "ta": "கடுமையான உணர்வு அடக்குமுறை, இனப்பெருக்க பிரச்சினைகள், ஆசைகளிலிருந்து துண்டிப்பு.",
            "kn": "ತೀವ್ರ ಭಾವನಾತ್ಮಕ ದಮನ, ಸಂತಾನೋತ್ಪತ್ತಿ ಸಮಸ್ಯೆಗಳು, ಆಸೆಗಳಿಂದ ಸಂಪೂರ್ಣ ಬೇರ್ಪಡುವಿಕೆ."
        }
    },
    "Manipura": {
        "balanced": {
            "en": "Strong willpower, healthy self-esteem, ability to take action. Natural leadership.",
            "ta": "வலுவான மன உறுதி, ஆரோக்கியமான சுயமரியாதை, செயல்படும் திறன். இயற்கை தலைமை.",
            "kn": "ಬಲವಾದ ಇಚ್ಛಾಶಕ್ತಿ, ಆರೋಗ್ಯಕರ ಸ್ವಾಭಿಮಾನ, ಕ್ರಿಯೆಗೆ ಸಾಮರ್ಥ್ಯ. ಸಹಜ ನಾಯಕತ್ವ."
        },
        "overactive": {
            "en": "Domineering personality, excessive anger, control issues. Power hunger or perfectionism.",
            "ta": "ஆதிக்க ஆளுமை, அதிக கோபம், கட்டுப்பாட்டு பிரச்சினைகள். அதிகாரப் பசி அல்லது முழுமைவாதம்.",
            "kn": "ಅಧಿಕಾರಶಾಹಿ ವ್ಯಕ್ತಿತ್ವ, ಅತಿಯಾದ ಕೋಪ, ನಿಯಂತ್ರಣ ಸಮಸ್ಯೆಗಳು. ಅಧಿಕಾರದ ಹಸಿವು."
        },
        "underactive": {
            "en": "Low self-esteem, indecisiveness, victim mentality. Difficulty setting boundaries.",
            "ta": "குறைந்த சுயமரியாதை, முடிவெடுக்க இயலாமை, பாதிக்கப்பட்ட மனநிலை. எல்லைகள் அமைக்க சிரமம்.",
            "kn": "ಕಡಿಮೆ ಸ್ವಾಭಿಮಾನ, ನಿರ್ಣಯವಿಲ್ಲದಿರುವಿಕೆ, ಬಲಿಪಶು ಮನಸ್ಥಿತಿ. ಗಡಿಗಳನ್ನು ಹೊಂದಿಸಲು ಕಷ್ಟ."
        },
        "blocked": {
            "en": "Complete lack of personal power, chronic digestive disorders. Severe self-doubt.",
            "ta": "தனிப்பட்ட சக்தியின் முழு இல்லாமை, நாள்பட்ட செரிமான கோளாறுகள். கடுமையான சுய சந்தேகம்.",
            "kn": "ವೈಯಕ್ತಿಕ ಶಕ್ತಿಯ ಸಂಪೂರ್ಣ ಕೊರತೆ, ದೀರ್ಘಕಾಲಿಕ ಜೀರ್ಣಕ್ರಿಯೆ ಸಮಸ್ಯೆಗಳು."
        }
    },
    "Anahata": {
        "balanced": {
            "en": "Loving and compassionate nature, healthy relationships, emotional resilience.",
            "ta": "அன்பான மற்றும் கருணையான இயல்பு, ஆரோக்கியமான உறவுகள், உணர்வு மீள்திறன்.",
            "kn": "ಪ್ರೀತಿಯ ಮತ್ತು ಕರುಣಾಮಯ ಸ್ವಭಾವ, ಆರೋಗ್ಯಕರ ಸಂಬಂಧಗಳು, ಭಾವನಾತ್ಮಕ ಚೇತರಿಕೆ."
        },
        "overactive": {
            "en": "Codependency, excessive people-pleasing, lack of boundaries. Jealousy or smothering love.",
            "ta": "சார்பு உறவு, அதிக மக்களை மகிழ்விக்கும் போக்கு, எல்லைகள் இல்லாமை. பொறாமை.",
            "kn": "ಪರಸ್ಪರ ಅವಲಂಬನೆ, ಅತಿಯಾದ ಜನರನ್ನು ಮೆಚ್ಚಿಸುವಿಕೆ, ಗಡಿಗಳ ಕೊರತೆ. ಹೊಟ್ಟೆಕಿಚ್ಚು."
        },
        "underactive": {
            "en": "Difficulty trusting, fear of intimacy, emotional coldness. Isolation or bitterness.",
            "ta": "நம்பிக்கையில் சிரமம், நெருக்கத்தின் பயம், உணர்வு குளிர்ச்சி. தனிமை அல்லது கசப்பு.",
            "kn": "ನಂಬಿಕೆಯಲ್ಲಿ ಕಷ್ಟ, ಆತ್ಮೀಯತೆಯ ಭಯ, ಭಾವನಾತ್ಮಕ ತಣ್ಣಗಾಗುವಿಕೆ. ಪ್ರತ್ಯೇಕತೆ."
        },
        "blocked": {
            "en": "Deep grief, inability to love, heart health issues. Complete emotional shutdown.",
            "ta": "ஆழமான துக்கம், அன்பு செய்ய இயலாமை, இதய ஆரோக்கிய பிரச்சினைகள். உணர்வு நிறுத்தம்.",
            "kn": "ಆಳವಾದ ದುಃಖ, ಪ್ರೀತಿಸಲು ಅಸಮರ್ಥತೆ, ಹೃದಯ ಆರೋಗ್ಯ ಸಮಸ್ಯೆಗಳು. ಭಾವನಾತ್ಮಕ ಸ್ಥಗಿತ."
        }
    },
    "Vishuddha": {
        "balanced": {
            "en": "Clear communication, authentic self-expression, good listening skills. Speaks truth with compassion.",
            "ta": "தெளிவான தொடர்பு, உண்மையான சுய வெளிப்பாடு, நல்ல கேட்கும் திறன். கருணையுடன் உண்மை.",
            "kn": "ಸ್ಪಷ್ಟ ಸಂವಹನ, ಅಧಿಕೃತ ಸ್ವ-ಅಭಿವ್ಯಕ್ತಿ, ಉತ್ತಮ ಕೇಳುವ ಕೌಶಲ್ಯ. ಕರುಣೆಯಿಂದ ಸತ್ಯ."
        },
        "overactive": {
            "en": "Excessive talking, inability to listen, harsh criticism. Gossip or verbal aggression.",
            "ta": "அதிக பேச்சு, கேட்க இயலாமை, கடுமையான விமர்சனம். வதந்தி அல்லது வாய்மொழி ஆக்கிரமிப்பு.",
            "kn": "ಅತಿಯಾದ ಮಾತನಾಡುವಿಕೆ, ಕೇಳಲು ಅಸಮರ್ಥತೆ, ಕಠಿಣ ಟೀಕೆ. ಗಾಸಿಪ್ ಅಥವಾ ಮೌಖಿಕ ಆಕ್ರಮಣ."
        },
        "underactive": {
            "en": "Difficulty expressing oneself, fear of speaking up, quiet and withdrawn.",
            "ta": "தன்னை வெளிப்படுத்த சிரமம், பேச பயம், அமைதியான மற்றும் பின்வாங்கிய.",
            "kn": "ತನ್ನನ್ನು ತಾನು ವ್ಯಕ್ತಪಡಿಸಲು ಕಷ್ಟ, ಮಾತನಾಡುವ ಭಯ, ಮೌನ ಮತ್ತು ಹಿಂದೆಗೆದ."
        },
        "blocked": {
            "en": "Complete inability to express truth, chronic throat issues, severe social anxiety.",
            "ta": "உண்மையை வெளிப்படுத்த முழு இயலாமை, நாள்பட்ட தொண்டை பிரச்சினைகள், சமூக கவலை.",
            "kn": "ಸತ್ಯವನ್ನು ವ್ಯಕ್ತಪಡಿಸಲು ಸಂಪೂರ್ಣ ಅಸಮರ್ಥತೆ, ದೀರ್ಘಕಾಲಿಕ ಗಂಟಲು ಸಮಸ್ಯೆಗಳು."
        }
    },
    "Ajna": {
        "balanced": {
            "en": "Strong intuition, clear thinking, good judgment. Wise decision-making, vivid imagination.",
            "ta": "வலுவான உள்ளுணர்வு, தெளிவான சிந்தனை, நல்ல தீர்ப்பு. ஞானமான முடிவெடுத்தல்.",
            "kn": "ಬಲವಾದ ಅಂತಃಪ್ರಜ್ಞೆ, ಸ್ಪಷ್ಟ ಚಿಂತನೆ, ಉತ್ತಮ ತೀರ್ಪು. ಬುದ್ಧಿವಂತ ನಿರ್ಧಾರ."
        },
        "overactive": {
            "en": "Overthinking, analysis paralysis, detachment from reality. Intellectual arrogance.",
            "ta": "அதிக சிந்தனை, பகுப்பாய்வு முடக்கம், உண்மையிலிருந்து பிரிவு. அறிவார்ந்த ஆணவம்.",
            "kn": "ಅತಿಯಾದ ಚಿಂತನೆ, ವಿಶ್ಲೇಷಣೆ ಪಾರ್ಶ್ವವಾಯು, ವಾಸ್ತವದಿಂದ ಬೇರ್ಪಡುವಿಕೆ. ಬೌದ್ಧಿಕ ಅಹಂಕಾರ."
        },
        "underactive": {
            "en": "Lack of intuition, poor memory, difficulty visualizing. Rigid thinking, confusion.",
            "ta": "உள்ளுணர்வு இல்லாமை, மோசமான நினைவாற்றல், காட்சிப்படுத்த சிரமம். கடினமான சிந்தனை.",
            "kn": "ಅಂತಃಪ್ರಜ್ಞೆಯ ಕೊರತೆ, ಕಳಪೆ ಸ್ಮರಣೆ, ದೃಶ್ಯೀಕರಿಸಲು ಕಷ್ಟ. ಕಠಿಣ ಚಿಂತನೆ."
        },
        "blocked": {
            "en": "Complete disconnection from intuition, severe headaches, learning difficulties.",
            "ta": "உள்ளுணர்விலிருந்து முழு துண்டிப்பு, கடுமையான தலைவலி, கற்றல் சிரமங்கள்.",
            "kn": "ಅಂತಃಪ್ರಜ್ಞೆಯಿಂದ ಸಂಪೂರ್ಣ ಬೇರ್ಪಡುವಿಕೆ, ತೀವ್ರ ತಲೆನೋವು, ಕಲಿಕೆಯ ತೊಂದರೆಗಳು."
        }
    },
    "Sahasrara": {
        "balanced": {
            "en": "Spiritual awareness, sense of purpose, connection to higher self. Wisdom and open-mindedness.",
            "ta": "ஆன்மீக விழிப்புணர்வு, நோக்க உணர்வு, உயர்ந்த சுயத்துடன் தொடர்பு. ஞானம், திறந்த மனம்.",
            "kn": "ಆಧ್ಯಾತ್ಮಿಕ ಅರಿವು, ಉದ್ದೇಶದ ಪ್ರಜ್ಞೆ, ಉನ್ನತ ಸ್ವಯಂಗೆ ಸಂಪರ್ಕ. ಜ್ಞಾನ, ತೆರೆದ ಮನಸ್ಸು."
        },
        "overactive": {
            "en": "Spiritual bypassing, disconnection from physical reality, escapism. Spiritual superiority.",
            "ta": "ஆன்மீக தவிர்ப்பு, உடல் உண்மையிலிருந்து துண்டிப்பு, தப்பித்தல். ஆன்மீக உயர்வு.",
            "kn": "ಆಧ್ಯಾತ್ಮಿಕ ಬೈಪಾಸ್, ಭೌತಿಕ ವಾಸ್ತವದಿಂದ ಬೇರ್ಪಡುವಿಕೆ, ಪಲಾಯನವಾದ."
        },
        "underactive": {
            "en": "Lack of purpose, spiritual emptiness, closed-mindedness. Cynicism or existential depression.",
            "ta": "நோக்கமின்மை, ஆன்மீக வெறுமை, மூடிய மனம். சீனிசம் அல்லது இருத்தலியல் மனச்சோர்வு.",
            "kn": "ಉದ್ದೇಶದ ಕೊರತೆ, ಆಧ್ಯಾತ್ಮಿಕ ಶೂನ್ಯತೆ, ಮುಚ್ಚಿದ ಮನಸ್ಸು. ನಿಂದನೆ ಅಥವಾ ಅಸ್ತಿತ್ವದ ಖಿನ್ನತೆ."
        },
        "blocked": {
            "en": "Complete spiritual disconnection, severe depression, loss of will to live. Chronic apathy.",
            "ta": "முழு ஆன்மீக துண்டிப்பு, கடுமையான மனச்சோர்வு, வாழ விருப்பமின்மை. நாள்பட்ட அலட்சியம்.",
            "kn": "ಸಂಪೂರ್ಣ ಆಧ್ಯಾತ್ಮಿಕ ಬೇರ್ಪಡುವಿಕೆ, ತೀವ್ರ ಖಿನ್ನತೆ, ಬದುಕುವ ಇಚ್ಛೆಯ ನಷ್ಟ."
        }
    }
}

# Lifestyle alignment recommendations per chakra
LIFESTYLE_ALIGNMENTS = {
    "Muladhara": {
        "diet": ["Root vegetables (carrots, beets, potatoes)", "Protein-rich foods", "Red foods (tomatoes, red peppers)"],
        "diet_ta": ["கிழங்கு காய்கறிகள் (கேரட், பீட்ரூட், உருளைக்கிழங்கு)", "புரதம் நிறைந்த உணவுகள்", "சிவப்பு உணவுகள்"],
        "activities": ["Gardening", "Walking barefoot on earth", "Martial arts", "Strength training"],
        "activities_ta": ["தோட்டக்கலை", "மண்ணில் நடத்தல்", "தற்காப்பு கலைகள்", "வலிமை பயிற்சி"],
        "environment": ["Spend time in nature", "Keep house organized", "Use red/brown colors in decor"],
        "environment_ta": ["இயற்கையில் நேரம் செலவிடுங்கள்", "வீட்டை ஒழுங்கமைக்கவும்", "அலங்காரத்தில் சிவப்பு/பழுப்பு நிறங்கள்"],
        "timing": "Best to work on grounding during Mars/Saturn hora, or on Tuesdays/Saturdays",
        "timing_ta": "செவ்வாய்/சனி ஹோரை அல்லது செவ்வாய்/சனிக்கிழமைகளில் நிலைத்தன்மை பயிற்சி சிறந்தது"
    },
    "Swadhisthana": {
        "diet": ["Orange foods (oranges, mangoes, carrots)", "Plenty of water", "Seeds and nuts", "Sweet fruits"],
        "diet_ta": ["ஆரஞ்சு உணவுகள் (ஆரஞ்சு, மாம்பழம்)", "நிறைய தண்ணீர்", "விதைகள் மற்றும் கொட்டைகள்"],
        "activities": ["Dancing", "Swimming", "Creative arts", "Sensory experiences"],
        "activities_ta": ["நடனம்", "நீச்சல்", "படைப்பு கலைகள்", "உணர்வு அனுபவங்கள்"],
        "environment": ["Water features in home", "Orange/coral colors", "Comfortable textures"],
        "environment_ta": ["வீட்டில் நீர் அம்சங்கள்", "ஆரஞ்சு/பவள நிறங்கள்", "வசதியான அமைப்புகள்"],
        "timing": "Best during Venus/Moon hora, or on Fridays/Mondays",
        "timing_ta": "சுக்கிர/சந்திர ஹோரை அல்லது வெள்ளி/திங்கட்கிழமைகளில் சிறந்தது"
    },
    "Manipura": {
        "diet": ["Yellow foods (bananas, corn, pineapple)", "Complex carbohydrates", "Ginger, turmeric", "Avoid heavy meals"],
        "diet_ta": ["மஞ்சள் உணவுகள் (வாழைப்பழம், சோளம்)", "சிக்கலான கார்போஹைட்ரேட்கள்", "இஞ்சி, மஞ்சள்"],
        "activities": ["Core exercises", "Sun gazing at dawn", "Competitive sports", "Taking on challenges"],
        "activities_ta": ["மைய பயிற்சிகள்", "விடியற்காலை சூரிய தரிசனம்", "போட்டி விளையாட்டுகள்", "சவால்களை எதிர்கொள்ளுதல்"],
        "environment": ["Sunlight in workspace", "Yellow/gold accents", "Clear, organized space"],
        "environment_ta": ["பணியிடத்தில் சூரிய ஒளி", "மஞ்சள்/தங்க அலங்காரம்", "தெளிவான, ஒழுங்கமைக்கப்பட்ட இடம்"],
        "timing": "Best during Sun hora or on Sundays, especially at noon",
        "timing_ta": "சூரிய ஹோரை அல்லது ஞாயிற்றுக்கிழமைகளில், குறிப்பாக மதியம் சிறந்தது"
    },
    "Anahata": {
        "diet": ["Green leafy vegetables", "Green tea", "Herbs like basil, cilantro", "Heart-healthy foods"],
        "diet_ta": ["பச்சை இலை காய்கறிகள்", "பச்சை தேநீர்", "துளசி, கொத்தமல்லி போன்ற மூலிகைகள்"],
        "activities": ["Yoga (heart openers)", "Acts of service", "Spending time with loved ones", "Gratitude journaling"],
        "activities_ta": ["யோகா (இதய திறப்பு ஆசனங்கள்)", "சேவை செயல்கள்", "அன்புக்குரியவர்களுடன் நேரம்"],
        "environment": ["Plants and greenery", "Pink/green colors", "Family photos", "Peaceful atmosphere"],
        "environment_ta": ["தாவரங்கள் மற்றும் பசுமை", "இளஞ்சிவப்பு/பச்சை நிறங்கள்", "குடும்ப புகைப்படங்கள்"],
        "timing": "Best during Moon/Venus hora or on Mondays/Fridays",
        "timing_ta": "சந்திர/சுக்கிர ஹோரை அல்லது திங்கள்/வெள்ளிக்கிழமைகளில் சிறந்தது"
    },
    "Vishuddha": {
        "diet": ["Blue foods (blueberries)", "Fruits and juices", "Herbal teas", "Light, easily digestible foods"],
        "diet_ta": ["நீல உணவுகள் (புளூபெர்ரி)", "பழங்கள் மற்றும் சாறுகள்", "மூலிகை தேநீர்"],
        "activities": ["Singing", "Public speaking", "Journaling", "Learning new languages"],
        "activities_ta": ["பாடுதல்", "பொது பேச்சு", "நாட்குறிப்பு எழுதுதல்", "புதிய மொழிகள் கற்றல்"],
        "environment": ["Blue colors", "Music and sound", "Clear communication spaces"],
        "environment_ta": ["நீல நிறங்கள்", "இசை மற்றும் ஒலி", "தெளிவான தொடர்பு இடங்கள்"],
        "timing": "Best during Mercury hora or on Wednesdays",
        "timing_ta": "புதன் ஹோரை அல்லது புதன்கிழமைகளில் சிறந்தது"
    },
    "Ajna": {
        "diet": ["Purple foods (grapes, plums)", "Dark chocolate", "Omega-3 rich foods", "Fasting occasionally"],
        "diet_ta": ["ஊதா உணவுகள் (திராட்சை, பிளம்)", "டார்க் சாக்லேட்", "ஒமேகா-3 நிறைந்த உணவுகள்"],
        "activities": ["Meditation", "Dream journaling", "Studying sacred texts", "Stargazing"],
        "activities_ta": ["தியானம்", "கனவு பதிவு", "புனித நூல்கள் படித்தல்", "நட்சத்திரங்களை பார்த்தல்"],
        "environment": ["Quiet, dark spaces for meditation", "Indigo/purple colors", "Minimal distractions"],
        "environment_ta": ["தியானத்திற்கு அமைதியான, இருண்ட இடங்கள்", "நீலம்/ஊதா நிறங்கள்"],
        "timing": "Best during Saturn hora or on Saturdays, especially at twilight",
        "timing_ta": "சனி ஹோரை அல்லது சனிக்கிழமைகளில், குறிப்பாக அந்தி நேரத்தில் சிறந்தது"
    },
    "Sahasrara": {
        "diet": ["Light, sattvic foods", "Fasting", "Avoiding tamasic foods", "Pure water"],
        "diet_ta": ["லேசான, சாத்வீக உணவுகள்", "உபவாசம்", "தாமச உணவுகளை தவிர்த்தல்"],
        "activities": ["Silent meditation", "Prayer", "Selfless service", "Pilgrimage"],
        "activities_ta": ["மௌன தியானம்", "பிரார்த்தனை", "நிஸ்வார்த்த சேவை", "யாத்திரை"],
        "environment": ["Sacred spaces", "White/violet colors", "Altars and spiritual symbols"],
        "environment_ta": ["புனித இடங்கள்", "வெள்ளை/ஊதா நிறங்கள்", "பலிபீடங்கள் மற்றும் ஆன்மீக சின்னங்கள்"],
        "timing": "Best during Jupiter hora, on Thursdays, or during Brahma Muhurta (4-6 AM)",
        "timing_ta": "குரு ஹோரை, வியாழக்கிழமைகளில், அல்லது பிரம்ம முகூர்த்தத்தில் (காலை 4-6) சிறந்தது"
    }
}


# Chakra-Planet Mapping based on Vedic traditions
CHAKRA_KARAKA_MAP = {
    "Muladhara": {
        "name_en": "Root Chakra",
        "name_ta": "மூலாதாரம்",
        "name_kn": "ಮೂಲಾಧಾರ",
        "symbol": "॥",
        "color": "#FF0000",
        "element": "Earth",
        "element_ta": "பூமி",
        "element_kn": "ಭೂಮಿ",
        "primary_karakas": ["Mars", "Ketu"],
        "secondary_karakas": ["Saturn"],
        "associated_houses": [1, 4, 8],
        "body_area": "Base of spine, legs, bones",
        "body_area_ta": "முதுகெலும்பின் அடிப்பகுதி, கால்கள், எலும்புகள்",
        "body_area_kn": "ಬೆನ್ನೆಲುಬಿನ ಬುಡ, ಕಾಲುಗಳು, ಮೂಳೆಗಳು",
        "themes": ["survival", "security", "grounding", "physical energy"],
        "themes_ta": ["உயிர்வாழ்வு", "பாதுகாப்பு", "நிலைத்தன்மை", "உடல் ஆற்றல்"],
        "themes_kn": ["ಉಳಿವು", "ಭದ್ರತೆ", "ಸ್ಥಿರತೆ", "ದೈಹಿಕ ಶಕ್ತಿ"],
        "beeja_mantra": "LAM",
        "beeja_mantra_ta": "லம்",
        "beeja_mantra_kn": "ಲಂ"
    },
    "Swadhisthana": {
        "name_en": "Sacral Chakra",
        "name_ta": "ஸ்வாதிஷ்டானம்",
        "name_kn": "ಸ್ವಾಧಿಷ್ಠಾನ",
        "symbol": "॥॥",
        "color": "#FF7F00",
        "element": "Water",
        "element_ta": "நீர்",
        "element_kn": "ನೀರು",
        "primary_karakas": ["Venus"],
        "secondary_karakas": ["Moon", "Mars"],
        "associated_houses": [2, 7, 12],
        "body_area": "Lower abdomen, reproductive organs",
        "body_area_ta": "அடிவயிறு, இனப்பெருக்க உறுப்புகள்",
        "body_area_kn": "ಕೆಳ ಹೊಟ್ಟೆ, ಸಂತಾನೋತ್ಪತ್ತಿ ಅಂಗಗಳು",
        "themes": ["creativity", "pleasure", "emotions", "sexuality"],
        "themes_ta": ["படைப்பாற்றல்", "இன்பம்", "உணர்வுகள்", "பாலியல்"],
        "themes_kn": ["ಸೃಜನಶೀಲತೆ", "ಆನಂದ", "ಭಾವನೆಗಳು", "ಲೈಂಗಿಕತೆ"],
        "beeja_mantra": "VAM",
        "beeja_mantra_ta": "வம்",
        "beeja_mantra_kn": "ವಂ"
    },
    "Manipura": {
        "name_en": "Solar Plexus Chakra",
        "name_ta": "மணிபூரகம்",
        "name_kn": "ಮಣಿಪೂರ",
        "symbol": "॥॥॥",
        "color": "#FFFF00",
        "element": "Fire",
        "element_ta": "அக்னி",
        "element_kn": "ಅಗ್ನಿ",
        "primary_karakas": ["Sun", "Jupiter"],
        "secondary_karakas": ["Mars"],
        "associated_houses": [3, 10, 6],
        "body_area": "Solar plexus, digestive system",
        "body_area_ta": "சூரிய வலையம், செரிமான அமைப்பு",
        "body_area_kn": "ಸೋಲಾರ್ ಪ್ಲೆಕ್ಸಸ್, ಜೀರ್ಣಾಂಗ ವ್ಯವಸ್ಥೆ",
        "themes": ["willpower", "confidence", "personal power", "action"],
        "themes_ta": ["மன உறுதி", "தன்னம்பிக்கை", "தனிப்பட்ட ஆற்றல்", "செயல்"],
        "themes_kn": ["ಇಚ್ಛಾಶಕ್ತಿ", "ಆತ್ಮವಿಶ್ವಾಸ", "ವೈಯಕ್ತಿಕ ಶಕ್ತಿ", "ಕ್ರಿಯೆ"],
        "beeja_mantra": "RAM",
        "beeja_mantra_ta": "ரம்",
        "beeja_mantra_kn": "ರಂ"
    },
    "Anahata": {
        "name_en": "Heart Chakra",
        "name_ta": "அனாகதம்",
        "name_kn": "ಅನಾಹತ",
        "symbol": "॥॥॥॥",
        "color": "#00FF00",
        "element": "Air",
        "element_ta": "காற்று",
        "element_kn": "ಗಾಳಿ",
        "primary_karakas": ["Moon"],
        "secondary_karakas": ["Venus", "Jupiter"],
        "associated_houses": [4, 5, 7],
        "body_area": "Heart, lungs, chest",
        "body_area_ta": "இதயம், நுரையீரல், மார்பு",
        "body_area_kn": "ಹೃದಯ, ಶ್ವಾಸಕೋಶ, ಎದೆ",
        "themes": ["love", "compassion", "relationships", "emotional balance"],
        "themes_ta": ["அன்பு", "கருணை", "உறவுகள்", "உணர்வு சமநிலை"],
        "themes_kn": ["ಪ್ರೀತಿ", "ಕರುಣೆ", "ಸಂಬಂಧಗಳು", "ಭಾವನಾತ್ಮಕ ಸಮತೋಲನ"],
        "beeja_mantra": "YAM",
        "beeja_mantra_ta": "யம்",
        "beeja_mantra_kn": "ಯಂ"
    },
    "Vishuddha": {
        "name_en": "Throat Chakra",
        "name_ta": "விசுத்தி",
        "name_kn": "ವಿಶುದ್ಧ",
        "symbol": "॥॥॥॥॥",
        "color": "#00BFFF",
        "element": "Ether",
        "element_ta": "ஆகாயம்",
        "element_kn": "ಆಕಾಶ",
        "primary_karakas": ["Mercury"],
        "secondary_karakas": ["Jupiter", "Venus"],
        "associated_houses": [3, 5, 2],
        "body_area": "Throat, thyroid, neck",
        "body_area_ta": "தொண்டை, தைராய்டு, கழுத்து",
        "body_area_kn": "ಗಂಟಲು, ಥೈರಾಯ್ಡ್, ಕುತ್ತಿಗೆ",
        "themes": ["communication", "truth", "self-expression", "creativity"],
        "themes_ta": ["தொடர்பு", "உண்மை", "சுய வெளிப்பாடு", "படைப்பாற்றல்"],
        "themes_kn": ["ಸಂವಹನ", "ಸತ್ಯ", "ಸ್ವ-ಅಭಿವ್ಯಕ್ತಿ", "ಸೃಜನಶೀಲತೆ"],
        "beeja_mantra": "HAM",
        "beeja_mantra_ta": "ஹம்",
        "beeja_mantra_kn": "ಹಂ"
    },
    "Ajna": {
        "name_en": "Third Eye Chakra",
        "name_ta": "ஆக்ஞை",
        "name_kn": "ಆಜ್ಞಾ",
        "symbol": "॥॥॥॥॥॥",
        "color": "#4B0082",
        "element": "Light",
        "element_ta": "ஒளி",
        "element_kn": "ಬೆಳಕು",
        "primary_karakas": ["Saturn", "Rahu"],
        "secondary_karakas": ["Ketu", "Jupiter"],
        "associated_houses": [9, 12, 8],
        "body_area": "Pineal gland, eyes, brain",
        "body_area_ta": "பீனியல் சுரப்பி, கண்கள், மூளை",
        "body_area_kn": "ಪೈನಲ್ ಗ್ರಂಥಿ, ಕಣ್ಣುಗಳು, ಮೆದುಳು",
        "themes": ["intuition", "wisdom", "insight", "perception"],
        "themes_ta": ["உள்ளுணர்வு", "ஞானம்", "நுண்ணறிவு", "உணர்தல்"],
        "themes_kn": ["ಅಂತಃಪ್ರಜ್ಞೆ", "ಜ್ಞಾನ", "ಒಳನೋಟ", "ಗ್ರಹಿಕೆ"],
        "beeja_mantra": "OM",
        "beeja_mantra_ta": "ஓம்",
        "beeja_mantra_kn": "ಓಂ"
    },
    "Sahasrara": {
        "name_en": "Crown Chakra",
        "name_ta": "சஹஸ்ராரம்",
        "name_kn": "ಸಹಸ್ರಾರ",
        "symbol": "॥॥॥॥॥॥॥",
        "color": "#8B00FF",
        "element": "Consciousness",
        "element_ta": "உணர்வு",
        "element_kn": "ಪ್ರಜ್ಞೆ",
        "primary_karakas": ["Jupiter", "Ketu"],
        "secondary_karakas": ["Sun"],
        "associated_houses": [9, 12, 5],
        "body_area": "Crown of head, pituitary gland",
        "body_area_ta": "தலையின் உச்சி, பிட்யூட்டரி சுரப்பி",
        "body_area_kn": "ತಲೆಯ ಮುಕುಟ, ಪಿಟ್ಯುಟರಿ ಗ್ರಂಥಿ",
        "themes": ["spirituality", "enlightenment", "divine connection", "liberation"],
        "themes_ta": ["ஆன்மீகம்", "ஞானோதயம்", "தெய்வீக தொடர்பு", "முக்தி"],
        "themes_kn": ["ಆಧ್ಯಾತ್ಮಿಕತೆ", "ಜ್ಞಾನೋದಯ", "ದೈವಿಕ ಸಂಪರ್ಕ", "ಮೋಕ್ಷ"],
        "beeja_mantra": "AUM",
        "beeja_mantra_ta": "ஔம்",
        "beeja_mantra_kn": "ಔಂ"
    }
}

# Planet dignity scores for calculation (exalted=10, own=9, friend=7, neutral=5, enemy=3, debilitated=1)
DIGNITY_SCORES = {
    'exalted': 10,
    'own': 9,
    'mooltrikona': 8,
    'friend': 7,
    'neutral': 5,
    'enemy': 3,
    'debilitated': 1
}

# Exaltation signs (rasi number 1-12)
EXALTATION = {
    'Sun': 1, 'Moon': 2, 'Mars': 10, 'Mercury': 6,
    'Jupiter': 4, 'Venus': 12, 'Saturn': 7, 'Rahu': 3, 'Ketu': 9
}

# Debilitation signs
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

# Chakra status interpretations
CHAKRA_STATUS = {
    'blocked': {
        'min': 0, 'max': 3,
        'label_en': 'Blocked', 'label_ta': 'தடைபட்டது', 'label_kn': 'ತಡೆಹಿಡಿಯಲಾಗಿದೆ'
    },
    'underactive': {
        'min': 3, 'max': 5,
        'label_en': 'Underactive', 'label_ta': 'குறைவான செயல்பாடு', 'label_kn': 'ಕಡಿಮೆ ಚಟುವಟಿಕೆ'
    },
    'balanced': {
        'min': 5, 'max': 7,
        'label_en': 'Balanced', 'label_ta': 'சமநிலை', 'label_kn': 'ಸಮತೋಲಿತ'
    },
    'overactive': {
        'min': 7, 'max': 10,
        'label_en': 'Overactive', 'label_ta': 'அதிக செயல்பாடு', 'label_kn': 'ಅತಿಯಾದ ಚಟುವಟಿಕೆ'
    }
}

# Yogic corrections for each chakra
CHAKRA_CORRECTIONS = {
    "Muladhara": {
        "mudras": ["Muladhara Mudra", "Ashwini Mudra"],
        "mudras_ta": ["மூலாதார முத்திரை", "அஸ்வினி முத்திரை"],
        "mantras": ["LAM", "Om Gam Ganapataye Namaha"],
        "mantras_ta": ["லம்", "ஓம் கம் கணபதயே நமஹ"],
        "practices": ["Walking barefoot on earth", "Root vegetable diet", "Red color therapy"],
        "practices_ta": ["மண்ணில் நடத்தல்", "கிழங்கு உணவு", "சிவப்பு நிற சிகிச்சை"],
        "gemstone": "Red Coral / Hessonite",
        "gemstone_ta": "பவளம் / கோமேதகம்",
        "asanas": ["Malasana", "Tadasana", "Virabhadrasana I"],
        "asanas_ta": ["மாலாசனம்", "தாடாசனம்", "வீரபத்ராசனம் I"]
    },
    "Swadhisthana": {
        "mudras": ["Shakti Mudra", "Yoni Mudra"],
        "mudras_ta": ["சக்தி முத்திரை", "யோனி முத்திரை"],
        "mantras": ["VAM", "Om Shreem"],
        "mantras_ta": ["வம்", "ஓம் ஸ்ரீம்"],
        "practices": ["Hip-opening exercises", "Water therapy", "Orange color meditation"],
        "practices_ta": ["இடுப்பு திறக்கும் பயிற்சிகள்", "நீர் சிகிச்சை", "ஆரஞ்சு நிற தியானம்"],
        "gemstone": "Pearl / Diamond",
        "gemstone_ta": "முத்து / வைரம்",
        "asanas": ["Baddha Konasana", "Upavistha Konasana", "Bhujangasana"],
        "asanas_ta": ["பத்த கோணாசனம்", "உபவிஷ்ட கோணாசனம்", "புஜங்காசனம்"]
    },
    "Manipura": {
        "mudras": ["Agni Mudra", "Rudra Mudra"],
        "mudras_ta": ["அக்னி முத்திரை", "ருத்ர முத்திரை"],
        "mantras": ["RAM", "Om Suryaya Namaha"],
        "mantras_ta": ["ரம்", "ஓம் சூர்யாய நமஹ"],
        "practices": ["Surya Namaskar", "Kapalabhati", "Core strengthening"],
        "practices_ta": ["சூர்ய நமஸ்காரம்", "கபாலபாதி", "மையத்தை வலுப்படுத்துதல்"],
        "gemstone": "Ruby / Yellow Sapphire",
        "gemstone_ta": "மாணிக்கம் / புஷ்பராகம்",
        "asanas": ["Navasana", "Dhanurasana", "Ardha Matsyendrasana"],
        "asanas_ta": ["நாவாசனம்", "தனுராசனம்", "அர்த்த மத்ஸ்யேந்திராசனம்"]
    },
    "Anahata": {
        "mudras": ["Hridaya Mudra", "Padma Mudra"],
        "mudras_ta": ["ஹிருதய முத்திரை", "பத்ம முத்திரை"],
        "mantras": ["YAM", "Om Chandraya Namaha"],
        "mantras_ta": ["யம்", "ஓம் சந்த்ராய நமஹ"],
        "practices": ["Heart-opening yoga", "Green color therapy", "Loving-kindness meditation"],
        "practices_ta": ["இதயம் திறக்கும் யோகா", "பச்சை நிற சிகிச்சை", "அன்பு-இரக்க தியானம்"],
        "gemstone": "Emerald / Pearl",
        "gemstone_ta": "மரகதம் / முத்து",
        "asanas": ["Ustrasana", "Matsyasana", "Chakrasana"],
        "asanas_ta": ["உஷ்ட்ராசனம்", "மத்ஸ்யாசனம்", "சக்ராசனம்"]
    },
    "Vishuddha": {
        "mudras": ["Vishuddha Mudra", "Shankh Mudra"],
        "mudras_ta": ["விசுத்தி முத்திரை", "சங்கு முத்திரை"],
        "mantras": ["HAM", "Om Budhaya Namaha"],
        "mantras_ta": ["ஹம்", "ஓம் புதாய நமஹ"],
        "practices": ["Singing/Chanting", "Blue color therapy", "Journaling"],
        "practices_ta": ["பாடுதல்/மந்திர ஜபம்", "நீல நிற சிகிச்சை", "நாட்குறிப்பு எழுதுதல்"],
        "gemstone": "Blue Sapphire / Emerald",
        "gemstone_ta": "நீலம் / மரகதம்",
        "asanas": ["Sarvangasana", "Halasana", "Simhasana"],
        "asanas_ta": ["சர்வாங்காசனம்", "ஹலாசனம்", "சிம்ஹாசனம்"]
    },
    "Ajna": {
        "mudras": ["Gyan Mudra", "Shambhavi Mudra"],
        "mudras_ta": ["ஞான முத்திரை", "சாம்பவி முத்திரை"],
        "mantras": ["OM", "Om Shanaishcharaya Namaha"],
        "mantras_ta": ["ஓம்", "ஓம் சனைஸ்சராய நமஹ"],
        "practices": ["Trataka (candle gazing)", "Indigo color therapy", "Third eye meditation"],
        "practices_ta": ["திராடகம் (விளக்கு பார்த்தல்)", "நீலநிற சிகிச்சை", "மூன்றாம் கண் தியானம்"],
        "gemstone": "Blue Sapphire / Cat's Eye",
        "gemstone_ta": "நீலம் / வைடூர்யம்",
        "asanas": ["Balasana", "Makarasana", "Shavasana"],
        "asanas_ta": ["பாலாசனம்", "மகராசனம்", "சவாசனம்"]
    },
    "Sahasrara": {
        "mudras": ["Mahamudra", "Khechari Mudra"],
        "mudras_ta": ["மகாமுத்திரை", "கேசரி முத்திரை"],
        "mantras": ["AUM", "Om Gurave Namaha"],
        "mantras_ta": ["ஔம்", "ஓம் குருவே நமஹ"],
        "practices": ["Silent meditation", "Fasting", "Selfless service"],
        "practices_ta": ["மௌன தியானம்", "உபவாசம்", "நிஸ்வார்த்த சேவை"],
        "gemstone": "Yellow Sapphire / Cat's Eye",
        "gemstone_ta": "புஷ்பராகம் / வைடூர்யம்",
        "asanas": ["Sirsasana", "Padmasana", "Savasana"],
        "asanas_ta": ["சீர்ஷாசனம்", "பத்மாசனம்", "சவாசனம்"]
    }
}

# Dynamic intelligence rules
DYNAMIC_RULES = {
    "Moon_malefic_heart": {
        "condition": "Moon weak or afflicted",
        "effect": "Anahata drops",
        "description_ta": "சந்திரன் பலவீனம் → அனாகதம் குறைவு"
    },
    "Sun_strong_solar": {
        "condition": "Sun strong in Shadbala",
        "effect": "Manipura boosts",
        "description_ta": "சூரியன் வலிமை → மணிபூரகம் உயர்வு"
    },
    "Saturn_retrograde_ajna": {
        "condition": "Saturn retrograde or afflicted",
        "effect": "Ajna weakens",
        "description_ta": "சனி வக்கிரம்/பாதிப்பு → ஆக்ஞை குறைவு"
    },
    "Venus_combust_sacral": {
        "condition": "Venus combust",
        "effect": "Swadhisthana drops",
        "description_ta": "சுக்கிரன் அஸ்தமனம் → ஸ்வாதிஷ்டானம் குறைவு"
    },
    "Mars_Ketu_root": {
        "condition": "Mars + Ketu afflicted",
        "effect": "Muladhara unstable",
        "description_ta": "செவ்வாய் + கேது பாதிப்பு → மூலாதாரம் நிலையற்றது"
    },
    "Jupiter_strong_crown": {
        "condition": "Jupiter has strong Ashtakavarga",
        "effect": "Sahasrara rises",
        "description_ta": "குரு அஷ்டகவர்க்க பலம் → சஹஸ்ராரம் உயர்வு"
    },
    "Saturn_Moon_heart": {
        "condition": "Saturn aspects Moon",
        "effect": "Heart chakra stress",
        "description_ta": "சனி சந்திரனை பார்வை → இதய சக்கர அழுத்தம்"
    },
    "Rahu_Mercury_throat": {
        "condition": "Rahu aspects Mercury",
        "effect": "Vishuddha instability",
        "description_ta": "ராகு புதனை பார்வை → விசுத்தி நிலையற்றது"
    }
}


class ChakraAnalysisService:
    """
    Vedic Astrology based Chakra Analysis Service
    Calculates chakra activation levels based on planetary positions and strengths
    """

    def __init__(self, jathagam_generator=None, ephemeris=None):
        self.jathagam_gen = jathagam_generator
        self.ephemeris = ephemeris

    def analyze_chakras(
        self, chart_data: Dict, current_dasha: Dict = None, language: str = "ta"
    ) -> Dict:
        """
        Main method to analyze all seven chakras based on birth chart

        SCORING FORMULA:
        ChakraScore = (0.35 × ShadbalaNorm) + (0.20 × BhavaStrength) +
                      (0.20 × Ashtakavarga) + (0.10 × Transit) + (0.15 × Dasha)

        Args:
            chart_data: Dictionary containing planetary positions, strengths,
                       ashtakavarga, and transit data
            current_dasha: Current dasha/bhukti information
            language: 'ta' for Tamil, 'en' for English

        Returns:
            Complete chakra analysis report with detailed astrological reasoning
        """
        planets = self._normalize_planets(chart_data.get('planets', []))

        # Calculate individual chakra scores
        chakra_report = []
        total_score = 0

        for chakra_name, chakra_info in CHAKRA_KARAKA_MAP.items():
            analysis = self._analyze_single_chakra(
                chakra_name, chakra_info, planets, current_dasha,
                language, chart_data
            )
            chakra_report.append(analysis)
            total_score += analysis['score']

        # Determine dominant and weakest chakras
        sorted_chakras = sorted(chakra_report, key=lambda x: x['score'], reverse=True)
        dominant = sorted_chakras[0]
        weakest = sorted_chakras[-1]

        # Calculate energy alignment index (0-100)
        avg_score = total_score / 7
        energy_alignment = round((avg_score / 10) * 100)

        # Generate overall summary
        summary = self._generate_overall_summary(chakra_report, language)

        return {
            "chakra_report": chakra_report,
            "overall_energy_summary": summary,
            "dominant_chakra": {
                "name": dominant['chakra'],
                "name_ta": dominant['name_ta'],
                "score": dominant['score']
            },
            "weakest_chakra": {
                "name": weakest['chakra'],
                "name_ta": weakest['name_ta'],
                "score": weakest['score']
            },
            "energy_alignment_index": energy_alignment,
            "generated_at": datetime.now().isoformat()
        }

    def _normalize_planets(self, planets: Any) -> Dict:
        """Convert planets list to dictionary for easier lookup"""
        if isinstance(planets, dict):
            return planets

        planet_dict = {}
        if isinstance(planets, list):
            for p in planets:
                name = p.get('planet', p.get('name', ''))
                planet_dict[name] = {
                    'strength': p.get('strength', 50),
                    'rasi': p.get('rasi_num', p.get('house', 1)),
                    'rasi_name': p.get('rasi', p.get('sign', '')),
                    'is_retrograde': p.get('is_retrograde', False),
                    'is_combust': p.get('is_combust', False),
                    'dignity': self._get_dignity(name, p.get('rasi_num', p.get('house', 1)))
                }
        return planet_dict

    def _get_dignity(self, planet: str, rasi: int) -> str:
        """Determine planet dignity based on rasi position"""
        if rasi == EXALTATION.get(planet):
            return 'exalted'
        elif rasi == DEBILITATION.get(planet):
            return 'debilitated'
        elif rasi in OWN_SIGNS.get(planet, []):
            return 'own'
        return 'neutral'

    def _analyze_single_chakra(
        self,
        chakra_name: str,
        chakra_info: Dict,
        planets: Dict,
        current_dasha: Dict,
        language: str,
        chart_data: Dict = None
    ) -> Dict:
        """
        Analyze a single chakra based on karaka planets using the formula:
        ChakraScore = (0.35 × ShadbalaNorm) + (0.20 × BhavaStrength) +
                      (0.15 × Ashtakavarga) + (0.15 × Transit) + (0.15 × Dasha)
        """
        chart_data = chart_data or {}
        ashtakavarga = chart_data.get('ashtakavarga', {})

        # 1. Calculate Shadbala Normalized score (0.35 weight)
        shadbala_score = 0
        karaka_analysis = []
        astrological_reasoning = []

        for karaka in chakra_info['primary_karakas']:
            planet_data = planets.get(karaka, {'strength': 50, 'dignity': 'neutral'})
            strength = planet_data.get('strength', 50)
            dignity = planet_data.get('dignity', 'neutral')
            rasi_name = planet_data.get('rasi_name', '')

            # PlanetShadbalaNorm = Shadbala / 600 (normalized to 0-1, then to 0-10)
            shadbala_norm = min(10, (strength / 60) * 10)
            shadbala_score += shadbala_norm

            # Build reasoning
            dignity_text = {
                'exalted': 'உச்சம்/Exalted',
                'own': 'சொந்த வீடு/Own Sign',
                'friend': 'நட்பு/Friendly',
                'neutral': 'சமம்/Neutral',
                'enemy': 'பகை/Enemy',
                'debilitated': 'நீசம்/Debilitated'
            }.get(dignity, 'Neutral')

            karaka_analysis.append({
                'planet': karaka,
                'strength': strength,
                'shadbala_norm': round(shadbala_norm, 2),
                'dignity': dignity,
                'rasi': rasi_name,
                'contribution': round(shadbala_norm * 0.35 / len(chakra_info['primary_karakas']), 2)
            })

            astrological_reasoning.append(
                f"{karaka} in {rasi_name} ({dignity_text}) - "
                f"Shadbala: {strength:.1f}"
            )

        # Average shadbala for primary karakas
        avg_shadbala = shadbala_score / max(1, len(chakra_info['primary_karakas']))
        shadbala_component = avg_shadbala * 0.35

        # 2. Calculate Bhava Strength (0.20 weight)
        bhava_score = 5.0  # Base neutral score
        bhava_details = []

        for karaka in chakra_info['primary_karakas']:
            planet_data = planets.get(karaka, {})
            dignity = planet_data.get('dignity', 'neutral')
            rasi = planet_data.get('rasi', 0)

            # BhavaStrength based on dignity
            if dignity in ['exalted', 'own']:
                bhava_score += 1.5
                bhava_details.append(f"{karaka} strong in house {rasi}")
            elif dignity == 'friend':
                bhava_score += 0.8
            elif dignity == 'enemy':
                bhava_score -= 0.8
                bhava_details.append(f"{karaka} weak in enemy sign")
            elif dignity == 'debilitated':
                bhava_score -= 1.5
                bhava_details.append(f"{karaka} debilitated - weakens chakra")

            # Bonus if karaka in associated house
            if rasi in chakra_info.get('associated_houses', []):
                bhava_score += 1.0
                bhava_details.append(
                    f"{karaka} in associated house {rasi} - strengthens {chakra_name}"
                )

        bhava_score = max(0, min(10, bhava_score))
        bhava_component = bhava_score * 0.20

        # 3. Calculate Ashtakavarga Weighted score (0.15 weight)
        ashtaka_score = 5.0  # Default neutral
        ashtaka_details = []

        for karaka in chakra_info['primary_karakas']:
            # Get planet's BAV (Bhinna Ashtakavarga) for associated houses
            planet_bav = ashtakavarga.get(karaka, {})
            for house in chakra_info.get('associated_houses', []):
                house_points = planet_bav.get(str(house), planet_bav.get(house, 4))
                if isinstance(house_points, (int, float)):
                    if house_points >= 5:
                        ashtaka_score += 0.8
                        ashtaka_details.append(
                            f"{karaka} has {house_points} bindus in house {house} (strong)"
                        )
                    elif house_points <= 2:
                        ashtaka_score -= 0.5
                        ashtaka_details.append(
                            f"{karaka} has {house_points} bindus in house {house} (weak)"
                        )

        ashtaka_score = max(0, min(10, ashtaka_score))
        ashtaka_component = ashtaka_score * 0.20

        # 4. Calculate Transit Impact (0.10 weight)
        transit_score = 5.0  # Neutral default
        transit_details = []
        transits = chart_data.get('current_transits', {})

        for karaka in chakra_info['primary_karakas']:
            transit_data = transits.get(karaka, {})
            transit_rasi = transit_data.get('rasi', 0)
            natal_rasi = planets.get(karaka, {}).get('rasi', 0)

            # Check if transit is favorable
            if transit_rasi:
                # Transit over natal position or trine
                if transit_rasi == natal_rasi:
                    transit_score += 0.5
                    transit_details.append(f"{karaka} transiting natal position")
                elif transit_rasi in [(natal_rasi + 4) % 12 or 12,
                                       (natal_rasi + 8) % 12 or 12]:
                    transit_score += 0.3
                    transit_details.append(f"{karaka} in trine transit")

        transit_score = max(0, min(10, transit_score))
        transit_component = transit_score * 0.10

        # 5. Calculate Dasha Influence (0.15 weight)
        dasha_score = 5.0  # Neutral default
        dasha_details = []
        is_dasha_activated = False

        if current_dasha:
            dasha_lord = current_dasha.get('lord', current_dasha.get('mahadasha', ''))
            bhukti_lord = current_dasha.get('bhukti', current_dasha.get('antardasha', ''))

            # If Dasha Lord is chakra karaka → +2.0 (HIGH influence)
            if dasha_lord in chakra_info['primary_karakas']:
                dasha_score += 2.0
                is_dasha_activated = True
                dasha_details.append(
                    f"Mahadasha of {dasha_lord} (chakra karaka) - HIGH activation"
                )

            # If Bhukti Lord is chakra karaka → +1.0
            if bhukti_lord in chakra_info['primary_karakas']:
                dasha_score += 1.0
                is_dasha_activated = True
                dasha_details.append(
                    f"Antardasha of {bhukti_lord} (chakra karaka) - activation boost"
                )

            # If Dasha Lord debilitates karaka → negative impact
            dasha_planet_data = planets.get(dasha_lord, {})
            if dasha_planet_data.get('dignity') == 'debilitated':
                for karaka in chakra_info['primary_karakas']:
                    if dasha_lord == karaka:
                        dasha_score -= 1.5
                        dasha_details.append(
                            f"{dasha_lord} debilitated in Dasha - negative impact"
                        )

        dasha_score = max(0, min(10, dasha_score))
        dasha_component = dasha_score * 0.15

        # 6. Apply Dynamic Intelligence Rules
        dynamic_adjustments = self._apply_dynamic_rules(chakra_name, planets)

        # 7. Calculate Final Score
        raw_score = (shadbala_component + bhava_component + ashtaka_component +
                     transit_component + dasha_component)
        raw_score += dynamic_adjustments['adjustment']

        final_score = max(0, min(10, raw_score))

        # 8. Determine Status
        status = self._get_chakra_status(final_score)

        # 9. Get Personality Manifestation
        personality = self._get_personality_manifestation(
            chakra_name, status['key'], language
        )

        # 10. Generate Astrological Interpretation with chart data
        interpretation = self._generate_chart_based_interpretation(
            chakra_name, karaka_analysis, status, astrological_reasoning, language
        )

        # 11. Generate Future Projection (3 years)
        future_projection = self._generate_future_projection(
            chakra_name, final_score, current_dasha, language
        )

        # 12. Get Corrections with Lifestyle alignment
        corrections = self._get_comprehensive_corrections(
            chakra_name, status['key'], karaka_analysis, language
        )

        # Get localized name based on language
        if language == 'ta':
            local_name = chakra_info['name_ta']
            local_element = chakra_info['element_ta']
        elif language == 'kn':
            local_name = chakra_info.get('name_kn', chakra_info['name_en'])
            local_element = chakra_info.get('element_kn', chakra_info['element'])
        else:
            local_name = chakra_info['name_en']
            local_element = chakra_info['element']

        return {
            "chakra": chakra_name,
            "name_en": chakra_info['name_en'],
            "name_ta": chakra_info['name_ta'],
            "name_kn": chakra_info.get('name_kn', chakra_info['name_en']),
            "name_local": local_name,
            "symbol": chakra_info['symbol'],
            "color": chakra_info['color'],
            "element": local_element,
            "score": round(final_score, 1),
            "status": status.get(f'label_{language}', status['label_en']),
            "status_key": status['key'],
            "is_dasha_activated": is_dasha_activated,
            "astrological_factors": {
                "karaka_planets": karaka_analysis,
                "planet_strength": f"{avg_shadbala:.1f}/10 (normalized)",
                "bhava_influence": chakra_info['associated_houses'],
                "bhava_strength": round(bhava_score, 2),
                "bhava_details": bhava_details[:3],
                "ashtakavarga": round(ashtaka_score, 2),
                "ashtakavarga_details": ashtaka_details[:3],
                "transit_effects": round(transit_score, 2),
                "transit_details": transit_details[:3],
                "dasha_activation": round(dasha_score, 2),
                "dasha_details": dasha_details,
                "dynamic_effects": dynamic_adjustments['effects'],
                "score_breakdown": {
                    "shadbala_component": round(shadbala_component, 2),
                    "bhava_component": round(bhava_component, 2),
                    "ashtakavarga_component": round(ashtaka_component, 2),
                    "transit_component": round(transit_component, 2),
                    "dasha_component": round(dasha_component, 2),
                    "dynamic_adjustment": round(dynamic_adjustments['adjustment'], 2)
                }
            },
            "astrological_reasoning": astrological_reasoning,
            "personality_manifestation": personality,
            "themes": chakra_info['themes_ta'] if language == 'ta' else chakra_info['themes'],
            "body_area": chakra_info['body_area_ta'] if language == 'ta' else chakra_info['body_area'],
            "beeja_mantra": chakra_info['beeja_mantra'],
            "interpretation": interpretation,
            "future_projection": future_projection,
            "corrections": corrections
        }

    def _get_personality_manifestation(
        self, chakra_name: str, status_key: str, language: str
    ) -> str:
        """Get personality manifestation based on chakra status"""
        manifestations = PERSONALITY_MANIFESTATIONS.get(chakra_name, {})
        status_manifest = manifestations.get(status_key, {})
        # Support Tamil, Kannada and English
        lang_key = 'ta' if language == 'ta' else ('kn' if language == 'kn' else 'en')
        return status_manifest.get(lang_key, status_manifest.get('en', ''))

    def _generate_chart_based_interpretation(
        self,
        chakra_name: str,
        karaka_analysis: List,
        status: Dict,
        reasoning: List,
        language: str
    ) -> str:
        """Generate interpretation based on actual chart data"""
        status_key = status['key']

        # Build interpretation from actual chart factors
        karaka_str = ", ".join([
            f"{k['planet']} ({k['dignity']})"
            for k in karaka_analysis
        ])

        if language == 'ta':
            base = f"{CHAKRA_KARAKA_MAP[chakra_name]['name_ta']} - "
            base += f"காரக கிரகங்கள்: {karaka_str}. "

            if status_key == 'blocked':
                base += "தடைபட்ட நிலையில் உள்ளது. "
            elif status_key == 'underactive':
                base += "குறைவான செயல்பாட்டில் உள்ளது. "
            elif status_key == 'balanced':
                base += "சமநிலையில் உள்ளது. "
            else:
                base += "அதிக செயல்பாட்டில் உள்ளது. "

            # Add reasoning
            if reasoning:
                base += f"காரணம்: {reasoning[0]}"
        else:
            base = f"{chakra_name} - "
            base += f"Karaka planets: {karaka_str}. "

            if status_key == 'blocked':
                base += "Currently blocked. "
            elif status_key == 'underactive':
                base += "Underactive state. "
            elif status_key == 'balanced':
                base += "Well balanced. "
            else:
                base += "Overactive state. "

            if reasoning:
                base += f"Reason: {reasoning[0]}"

        return base

    def _get_comprehensive_corrections(
        self,
        chakra_name: str,
        status_key: str,
        karaka_analysis: List,
        language: str
    ) -> Dict:
        """Get comprehensive corrections including lifestyle alignment"""
        base_corrections = CHAKRA_CORRECTIONS.get(chakra_name, {})
        lifestyle = LIFESTYLE_ALIGNMENTS.get(chakra_name, {})

        # Determine if gemstone is recommended based on chart
        gemstone_recommended = False
        gemstone_note = ""
        for karaka in karaka_analysis:
            if karaka['dignity'] in ['debilitated', 'enemy']:
                gemstone_recommended = True
                gemstone_note = f"{karaka['planet']} weak - gemstone may help"
                break

        lang_suffix = '_ta' if language == 'ta' else ''

        return {
            "mantra": base_corrections.get(f'mantras{lang_suffix}',
                                            base_corrections.get('mantras', [])),
            "mudra": base_corrections.get(f'mudras{lang_suffix}',
                                           base_corrections.get('mudras', [])),
            "practice": base_corrections.get(f'practices{lang_suffix}',
                                              base_corrections.get('practices', [])),
            "asanas": base_corrections.get(f'asanas{lang_suffix}',
                                            base_corrections.get('asanas', [])),
            "gemstone": {
                "name": base_corrections.get(f'gemstone{lang_suffix}',
                                              base_corrections.get('gemstone', '')),
                "recommended": gemstone_recommended,
                "note": gemstone_note
            },
            "lifestyle": {
                "diet": lifestyle.get(f'diet{lang_suffix}', lifestyle.get('diet', [])),
                "activities": lifestyle.get(f'activities{lang_suffix}',
                                             lifestyle.get('activities', [])),
                "environment": lifestyle.get(f'environment{lang_suffix}',
                                              lifestyle.get('environment', [])),
                "timing": lifestyle.get(f'timing{lang_suffix}',
                                         lifestyle.get('timing', ''))
            }
        }

    def _apply_dynamic_rules(self, chakra_name: str, planets: Dict) -> Dict:
        """Apply dynamic intelligence rules for chakra adjustments"""
        adjustment = 0
        effects = []

        # Moon malefic/weak affects Heart
        if chakra_name == "Anahata":
            moon = planets.get('Moon', {})
            if moon.get('strength', 50) < 40 or moon.get('dignity') == 'debilitated':
                adjustment -= 1.0
                effects.append("Moon weak - Heart chakra reduced")

        # Sun strong boosts Solar Plexus
        if chakra_name == "Manipura":
            sun = planets.get('Sun', {})
            if sun.get('strength', 50) > 70 or sun.get('dignity') == 'exalted':
                adjustment += 1.0
                effects.append("Sun strong - Solar Plexus boosted")

        # Saturn retrograde weakens Third Eye
        if chakra_name == "Ajna":
            saturn = planets.get('Saturn', {})
            if saturn.get('is_retrograde', False) or saturn.get('strength', 50) < 35:
                adjustment -= 0.8
                effects.append("Saturn afflicted - Ajna reduced")

        # Venus combust drops Sacral
        if chakra_name == "Swadhisthana":
            venus = planets.get('Venus', {})
            if venus.get('is_combust', False) or venus.get('dignity') == 'debilitated':
                adjustment -= 1.0
                effects.append("Venus combust - Sacral chakra reduced")

        # Mars + Ketu affliction destabilizes Root
        if chakra_name == "Muladhara":
            mars = planets.get('Mars', {})
            ketu = planets.get('Ketu', {})
            if mars.get('strength', 50) < 40 and ketu.get('strength', 50) < 40:
                adjustment -= 0.8
                effects.append("Mars-Ketu weak - Root chakra unstable")

        # Jupiter strong enhances Crown
        if chakra_name == "Sahasrara":
            jupiter = planets.get('Jupiter', {})
            if jupiter.get('strength', 50) > 70 or jupiter.get('dignity') in ['exalted', 'own']:
                adjustment += 1.0
                effects.append("Jupiter strong - Crown chakra elevated")

        return {
            'adjustment': adjustment,
            'effects': effects
        }

    def _get_chakra_status(self, score: float) -> Dict:
        """Determine chakra status based on score"""
        if score < 3:
            return {
                'key': 'blocked',
                'label_en': 'Blocked',
                'label_ta': 'தடைபட்டது',
                'label_kn': 'ತಡೆಹಿಡಿಯಲಾಗಿದೆ'
            }
        elif score < 5:
            return {
                'key': 'underactive',
                'label_en': 'Underactive',
                'label_ta': 'குறைவான செயல்பாடு',
                'label_kn': 'ಕಡಿಮೆ ಚಟುವಟಿಕೆ'
            }
        elif score < 7:
            return {
                'key': 'balanced',
                'label_en': 'Balanced',
                'label_ta': 'சமநிலை',
                'label_kn': 'ಸಮತೋಲಿತ'
            }
        else:
            return {
                'key': 'overactive',
                'label_en': 'Overactive',
                'label_ta': 'அதிக செயல்பாடு',
                'label_kn': 'ಅತಿಯಾದ ಚಟುವಟಿಕೆ'
            }

    def _generate_interpretation(
        self,
        chakra_name: str,
        score: float,
        status: Dict,
        karaka_analysis: List,
        language: str
    ) -> str:
        """Generate personalized interpretation based on chart data"""

        interpretations = {
            "Muladhara": {
                "blocked": {
                    "en": "Your root chakra shows blockage due to weak Mars/Saturn. You may feel insecure about material stability. Focus on grounding practices.",
                    "ta": "செவ்வாய்/சனி பலவீனத்தால் மூலாதாரம் தடைபட்டுள்ளது. பொருள் நிலையற்ற உணர்வு இருக்கலாம். நிலைத்தன்மை பயிற்சிகளில் கவனம் செலுத்துங்கள்."
                },
                "underactive": {
                    "en": "Root chakra is underactive. Focus on physical activities and earthy practices to strengthen your foundation.",
                    "ta": "மூலாதாரம் குறைவான செயல்பாட்டில் உள்ளது. உடல் செயல்பாடுகள் மற்றும் பூமி சார்ந்த பயிற்சிகளில் கவனம் செலுத்துங்கள்."
                },
                "balanced": {
                    "en": "Your root chakra is well-balanced. You have good connection to physical world and material stability.",
                    "ta": "உங்கள் மூலாதாரம் நல்ல சமநிலையில் உள்ளது. உடல் உலகத்துடனும் பொருள் நிலைத்தன்மையுடனும் நல்ல தொடர்பு உள்ளது."
                },
                "overactive": {
                    "en": "Root chakra is overactive. May show as excessive materialism or rigidity. Practice detachment.",
                    "ta": "மூலாதாரம் அதிக செயல்பாட்டில் உள்ளது. அதிக பொருளாசை அல்லது விறைப்பாக இருக்கலாம். பற்றின்மை பயிலுங்கள்."
                }
            },
            "Swadhisthana": {
                "blocked": {
                    "en": "Sacral chakra blockage from Venus/Moon affliction affects creativity and emotional flow. Work on emotional expression.",
                    "ta": "சுக்கிரன்/சந்திரன் பாதிப்பால் ஸ்வாதிஷ்டானம் தடைபட்டுள்ளது. படைப்பாற்றல் மற்றும் உணர்வு வெளிப்பாட்டில் பணியுங்கள்."
                },
                "underactive": {
                    "en": "Sacral chakra needs activation. Engage in creative activities and allow emotional expression.",
                    "ta": "ஸ்வாதிஷ்டானத்திற்கு செயல்படுத்துதல் தேவை. படைப்பு செயல்பாடுகளில் ஈடுபடுங்கள்."
                },
                "balanced": {
                    "en": "Sacral chakra is balanced. Good creative flow and healthy emotional expression indicated.",
                    "ta": "ஸ்வாதிஷ்டானம் சமநிலையில் உள்ளது. நல்ல படைப்பாற்றல் மற்றும் ஆரோக்கியமான உணர்வு வெளிப்பாடு குறிக்கப்படுகிறது."
                },
                "overactive": {
                    "en": "Overactive sacral may manifest as emotional volatility or excessive attachment. Practice moderation.",
                    "ta": "அதிக செயல்பாடு உணர்வு மாறுபாடு அல்லது அதிக பற்றாக வெளிப்படலாம். மிதத்தன்மை பயிலுங்கள்."
                }
            },
            "Manipura": {
                "blocked": {
                    "en": "Solar plexus blockage shows as lack of confidence. Sun/Mars need strengthening for personal power.",
                    "ta": "மணிபூரக தடை தன்னம்பிக்கை குறைவாக வெளிப்படுகிறது. சூரியன்/செவ்வாய் பலப்படுத்த வேண்டும்."
                },
                "underactive": {
                    "en": "Solar plexus is underactive. Build willpower through discipline and physical exercise.",
                    "ta": "மணிபூரகம் குறைவான செயல்பாட்டில். ஒழுக்கம் மற்றும் உடற்பயிற்சி மூலம் மன உறுதி வளர்க்கவும்."
                },
                "balanced": {
                    "en": "Strong solar plexus gives you good willpower, confidence, and ability to take action.",
                    "ta": "வலுவான மணிபூரகம் நல்ல மன உறுதி, தன்னம்பிக்கை மற்றும் செயல்படும் திறனை தருகிறது."
                },
                "overactive": {
                    "en": "Overactive solar plexus may show as domination or anger. Channel energy constructively.",
                    "ta": "அதிக செயல்பாடு ஆதிக்கம் அல்லது கோபமாக வெளிப்படலாம். ஆற்றலை ஆக்கபூர்வமாக திருப்புங்கள்."
                }
            },
            "Anahata": {
                "blocked": {
                    "en": "Heart chakra blockage from Moon weakness affects emotional connections and compassion.",
                    "ta": "சந்திரன் பலவீனத்தால் அனாகத தடை உணர்வு தொடர்புகள் மற்றும் கருணையை பாதிக்கிறது."
                },
                "underactive": {
                    "en": "Heart chakra needs opening. Practice loving-kindness and allow vulnerability.",
                    "ta": "அனாகதம் திறக்க வேண்டும். அன்பு-இரக்க தியானம் பயிலுங்கள்."
                },
                "balanced": {
                    "en": "Balanced heart chakra brings harmonious relationships and emotional well-being.",
                    "ta": "சமநிலையான அனாகதம் இணக்கமான உறவுகளையும் உணர்வு நல்வாழ்வையும் தருகிறது."
                },
                "overactive": {
                    "en": "Overactive heart may lead to codependency. Maintain healthy boundaries.",
                    "ta": "அதிக செயல்பாடு சார்பு உறவுக்கு வழிவகுக்கலாம். ஆரோக்கியமான எல்லைகளை பராமரியுங்கள்."
                }
            },
            "Vishuddha": {
                "blocked": {
                    "en": "Throat chakra blockage from Mercury affliction affects communication and self-expression.",
                    "ta": "புதன் பாதிப்பால் விசுத்தி தடை தொடர்பு மற்றும் சுய வெளிப்பாட்டை பாதிக்கிறது."
                },
                "underactive": {
                    "en": "Throat chakra needs activation. Practice speaking your truth and creative expression.",
                    "ta": "விசுத்தி செயல்படுத்த வேண்டும். உண்மையை பேசுதல் மற்றும் படைப்பு வெளிப்பாட்டை பயிலுங்கள்."
                },
                "balanced": {
                    "en": "Balanced throat chakra enables clear communication and authentic self-expression.",
                    "ta": "சமநிலையான விசுத்தி தெளிவான தொடர்பு மற்றும் உண்மையான சுய வெளிப்பாட்டை செயல்படுத்துகிறது."
                },
                "overactive": {
                    "en": "Overactive throat may show as excessive talking or criticism. Practice listening.",
                    "ta": "அதிக செயல்பாடு அதிக பேச்சு அல்லது விமர்சனமாக வெளிப்படலாம். கேட்பதை பயிலுங்கள்."
                }
            },
            "Ajna": {
                "blocked": {
                    "en": "Third eye blockage from Saturn affliction affects intuition and clarity. Meditation helps.",
                    "ta": "சனி பாதிப்பால் ஆக்ஞை தடை உள்ளுணர்வு மற்றும் தெளிவை பாதிக்கிறது. தியானம் உதவும்."
                },
                "underactive": {
                    "en": "Third eye needs awakening. Practice meditation and trust your intuition.",
                    "ta": "ஆக்ஞை விழிப்பு தேவை. தியானம் பயிலுங்கள், உள்ளுணர்வை நம்புங்கள்."
                },
                "balanced": {
                    "en": "Balanced third eye provides good intuition, wisdom, and mental clarity.",
                    "ta": "சமநிலையான ஆக்ஞை நல்ல உள்ளுணர்வு, ஞானம் மற்றும் மன தெளிவை தருகிறது."
                },
                "overactive": {
                    "en": "Overactive third eye may lead to overthinking. Ground yourself in present moment.",
                    "ta": "அதிக செயல்பாடு அதிக சிந்தனைக்கு வழிவகுக்கலாம். நிகழ்காலத்தில் நிலைபெறுங்கள்."
                }
            },
            "Sahasrara": {
                "blocked": {
                    "en": "Crown chakra blockage may show as disconnection from higher purpose. Spiritual practices help.",
                    "ta": "சஹஸ்ரார தடை உயர்ந்த நோக்கத்திலிருந்து துண்டிப்பாக வெளிப்படலாம். ஆன்மீக பயிற்சிகள் உதவும்."
                },
                "underactive": {
                    "en": "Crown chakra needs activation. Engage in meditation and selfless service.",
                    "ta": "சஹஸ்ராரம் செயல்படுத்த வேண்டும். தியானம் மற்றும் நிஸ்வார்த்த சேவையில் ஈடுபடுங்கள்."
                },
                "balanced": {
                    "en": "Balanced crown chakra connects you to universal consciousness and spiritual wisdom.",
                    "ta": "சமநிலையான சஹஸ்ராரம் பிரபஞ்ச உணர்வு மற்றும் ஆன்மீக ஞானத்துடன் இணைக்கிறது."
                },
                "overactive": {
                    "en": "Overactive crown may cause disconnection from physical reality. Stay grounded.",
                    "ta": "அதிக செயல்பாடு உடல் உண்மையிலிருந்து துண்டிப்பை ஏற்படுத்தலாம். நிலைபெற்று இருங்கள்."
                }
            }
        }

        chakra_interps = interpretations.get(chakra_name, {})
        status_key = status['key']

        if language == 'ta':
            return chakra_interps.get(status_key, {}).get('ta', '')
        return chakra_interps.get(status_key, {}).get('en', '')

    def _generate_future_projection(
        self,
        chakra_name: str,
        score: float,
        current_dasha: Dict,
        language: str
    ) -> str:
        """Generate future projection for next 3 years based on dasha"""

        projections = {
            "Muladhara": {
                "improving": {
                    "en": "Root chakra energy will strengthen during upcoming Mars/Saturn favorable transits. Security and stability improve.",
                    "ta": "வரவிருக்கும் செவ்வாய்/சனி சாதகமான கோச்சாரத்தில் மூலாதார ஆற்றல் வலுப்படும். பாதுகாப்பு மற்றும் நிலைத்தன்மை மேம்படும்."
                },
                "stable": {
                    "en": "Root chakra maintains stability. Continue grounding practices for sustained balance.",
                    "ta": "மூலாதாரம் நிலைத்தன்மையை பராமரிக்கிறது. நிலையான சமநிலைக்கு நிலைத்தன்மை பயிற்சிகளை தொடருங்கள்."
                },
                "challenging": {
                    "en": "Some challenges expected. Remedial practices for Mars/Saturn recommended during this period.",
                    "ta": "சில சவால்கள் எதிர்பார்க்கப்படுகின்றன. இக்காலத்தில் செவ்வாய்/சனி பரிகாரங்கள் பரிந்துரைக்கப்படுகின்றன."
                }
            }
        }

        # Default projection based on score trend
        if score > 6:
            trend = "improving"
        elif score > 4:
            trend = "stable"
        else:
            trend = "challenging"

        chakra_projections = projections.get(chakra_name, {
            "improving": {
                "en": f"{chakra_name} energy strengthening over the next 3 years. Continue spiritual practices.",
                "ta": f"அடுத்த 3 ஆண்டுகளில் {CHAKRA_KARAKA_MAP[chakra_name]['name_ta']} ஆற்றல் வலுப்படும். ஆன்மீக பயிற்சிகளை தொடருங்கள்."
            },
            "stable": {
                "en": f"{chakra_name} remains stable. Maintain current practices for balance.",
                "ta": f"{CHAKRA_KARAKA_MAP[chakra_name]['name_ta']} நிலையாக உள்ளது. சமநிலைக்கு தற்போதைய பயிற்சிகளை பராமரியுங்கள்."
            },
            "challenging": {
                "en": f"{chakra_name} requires attention. Focus on remedial practices and karaka planet strengthening.",
                "ta": f"{CHAKRA_KARAKA_MAP[chakra_name]['name_ta']} கவனம் தேவை. பரிகாரங்கள் மற்றும் காரக கிரக பலப்படுத்துதலில் கவனம் செலுத்துங்கள்."
            }
        })

        return chakra_projections.get(trend, {}).get('ta' if language == 'ta' else 'en', '')

    def _generate_overall_summary(self, chakra_report: List[Dict], language: str) -> str:
        """Generate overall energy summary"""

        balanced_count = sum(1 for c in chakra_report if c['status_key'] == 'balanced')
        blocked_count = sum(1 for c in chakra_report if c['status_key'] in ['blocked', 'underactive'])
        overactive_count = sum(1 for c in chakra_report if c['status_key'] == 'overactive')

        avg_score = sum(c['score'] for c in chakra_report) / 7

        if balanced_count >= 5:
            summary_ta = "உங்கள் ஆற்றல் மையங்கள் நல்ல சமநிலையில் உள்ளன. ஆன்மீக வளர்ச்சிக்கு சாதகமான நேரம்."
            summary_en = "Your energy centers are well balanced. Favorable time for spiritual growth."
        elif blocked_count >= 3:
            weak_chakras = [c['name_ta'] for c in chakra_report if c['status_key'] in ['blocked', 'underactive']]
            summary_ta = f"சில சக்கரங்களில் தடை உள்ளது ({', '.join(weak_chakras[:2])}). பரிகாரங்கள் உதவும்."
            summary_en = f"Some chakras show blockage. Remedial practices recommended."
        elif overactive_count >= 2:
            summary_ta = "அதிக ஆற்றல் சமநிலைப்படுத்த வேண்டும். நிலைத்தன்மை பயிற்சிகள் தேவை."
            summary_en = "Excess energy needs balancing. Grounding practices recommended."
        else:
            summary_ta = "கலவையான ஆற்றல் நிலை. முக்கிய சக்கரங்களில் கவனம் செலுத்துங்கள்."
            summary_en = "Mixed energy state. Focus on key chakras needing attention."

        return summary_ta if language == 'ta' else summary_en


# Convenience function for direct use
def analyze_chakras_from_chart(chart_data: Dict, current_dasha: Dict = None, language: str = "ta") -> Dict:
    """
    Convenience function to analyze chakras from chart data

    Args:
        chart_data: Dictionary containing planetary positions and strengths
        current_dasha: Current dasha/bhukti information
        language: 'ta' for Tamil, 'en' for English

    Returns:
        Complete chakra analysis report
    """
    service = ChakraAnalysisService()
    return service.analyze_chakras(chart_data, current_dasha, language)
