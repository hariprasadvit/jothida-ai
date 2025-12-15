"""
AI Remedy Engine Service
Generates personalized astrological remedies based on:
- Current dasha period
- Planet strengths
- Dosha impact
- User goals
"""

from datetime import datetime, date
from typing import Dict, List, Optional
import random


# Planet data with PRACTICAL remedies (simple, achievable actions)
PLANET_REMEDIES = {
    "Sun": {
        "tamil": "சூரியன்",
        "day": "Sunday",
        "day_tamil": "ஞாயிறு",
        "color": "red",
        "color_tamil": "சிவப்பு/ஆரஞ்சு",
        "gemstone": "Ruby",
        "gemstone_tamil": "மாணிக்கம்",
        "mantra": "ॐ सूर्याय नमः",
        "mantra_tamil": "ஓம் சூர்யாய நமஹ",
        "mantra_count": 11,  # Practical: 11 times only
        "deity": "Lord Surya",
        "deity_tamil": "சூரிய பகவான்",
        "donation": ["Wheat", "Jaggery"],
        "donation_tamil": ["கோதுமை", "வெல்லம்"],
        "fasting": "Sunday",
        "direction": "East",
        "direction_tamil": "கிழக்கு",
        "temple": "Suryanar Koil",
        "temple_tamil": "சூரியனார் கோவில்",
        # NEW: Simple daily actions
        "simple_actions": [
            {"icon": "☀️", "action": "Wake up at sunrise", "action_tamil": "சூரிய உதயத்தில் எழுங்கள்", "difficulty": "easy"},
            {"icon": "🙏", "action": "Offer water to Sun", "action_tamil": "சூரியனுக்கு அர்க்கியம் செய்யுங்கள்", "difficulty": "easy"},
            {"icon": "👕", "action": "Wear orange/red color", "action_tamil": "ஆரஞ்சு/சிவப்பு ஆடை அணியுங்கள்", "difficulty": "easy"},
        ],
        "weekly_action": {"icon": "🍯", "action": "Donate jaggery or wheat", "action_tamil": "வெல்லம் அல்லது கோதுமை தானம்"}
    },
    "Moon": {
        "tamil": "சந்திரன்",
        "day": "Monday",
        "day_tamil": "திங்கள்",
        "color": "white",
        "color_tamil": "வெள்ளை",
        "gemstone": "Pearl",
        "gemstone_tamil": "முத்து",
        "mantra": "ॐ चंद्राय नमः",
        "mantra_tamil": "ஓம் சந்த்ராய நமஹ",
        "mantra_count": 11,
        "deity": "Lord Shiva",
        "deity_tamil": "சிவபெருமான்",
        "donation": ["Rice", "Milk"],
        "donation_tamil": ["அரிசி", "பால்"],
        "fasting": "Monday",
        "direction": "North-West",
        "direction_tamil": "வடமேற்கு",
        "temple": "Thingaloor",
        "temple_tamil": "திங்களூர்",
        "simple_actions": [
            {"icon": "🥛", "action": "Drink milk in morning", "action_tamil": "காலையில் பால் குடியுங்கள்", "difficulty": "easy"},
            {"icon": "👕", "action": "Wear white clothes", "action_tamil": "வெள்ளை ஆடை அணியுங்கள்", "difficulty": "easy"},
            {"icon": "🧘", "action": "5 mins calm meditation", "action_tamil": "5 நிமிடம் அமைதியாக தியானம்", "difficulty": "easy"},
        ],
        "weekly_action": {"icon": "🍚", "action": "Donate rice to needy", "action_tamil": "ஏழைகளுக்கு அரிசி தானம்"}
    },
    "Mars": {
        "tamil": "செவ்வாய்",
        "day": "Tuesday",
        "day_tamil": "செவ்வாய்",
        "color": "red",
        "color_tamil": "சிவப்பு",
        "gemstone": "Red Coral",
        "gemstone_tamil": "பவளம்",
        "mantra": "ॐ अंगारकाय नमः",
        "mantra_tamil": "ஓம் அங்காரகாய நமஹ",
        "mantra_count": 11,
        "deity": "Lord Muruga",
        "deity_tamil": "முருகப்பெருமான்",
        "donation": ["Red lentils", "Jaggery"],
        "donation_tamil": ["சிவப்பு பருப்பு", "வெல்லம்"],
        "fasting": "Tuesday",
        "direction": "South",
        "direction_tamil": "தெற்கு",
        "temple": "Vaitheeswaran Koil",
        "temple_tamil": "வைத்தீஸ்வரன் கோவில்",
        "simple_actions": [
            {"icon": "🏃", "action": "Do physical exercise", "action_tamil": "உடற்பயிற்சி செய்யுங்கள்", "difficulty": "medium"},
            {"icon": "👕", "action": "Wear red color", "action_tamil": "சிவப்பு ஆடை அணியுங்கள்", "difficulty": "easy"},
            {"icon": "🙏", "action": "Visit Murugan temple", "action_tamil": "முருகன் கோவில் செல்லுங்கள்", "difficulty": "medium"},
        ],
        "weekly_action": {"icon": "🫘", "action": "Donate red lentils", "action_tamil": "சிவப்பு பருப்பு தானம்"}
    },
    "Mercury": {
        "tamil": "புதன்",
        "day": "Wednesday",
        "day_tamil": "புதன்",
        "color": "green",
        "color_tamil": "பச்சை",
        "gemstone": "Emerald",
        "gemstone_tamil": "மரகதம்",
        "mantra": "ॐ बुधाय नमः",
        "mantra_tamil": "ஓம் புதாய நமஹ",
        "mantra_count": 11,
        "deity": "Lord Vishnu",
        "deity_tamil": "விஷ்ணு பெருமான்",
        "donation": ["Green gram", "Books"],
        "donation_tamil": ["பச்சைப் பருப்பு", "புத்தகங்கள்"],
        "fasting": "Wednesday",
        "direction": "North",
        "direction_tamil": "வடக்கு",
        "temple": "Thiruvenkadu",
        "temple_tamil": "திருவேங்காடு",
        "simple_actions": [
            {"icon": "📚", "action": "Read for 15 mins", "action_tamil": "15 நிமிடம் வாசியுங்கள்", "difficulty": "easy"},
            {"icon": "👕", "action": "Wear green color", "action_tamil": "பச்சை ஆடை அணியுங்கள்", "difficulty": "easy"},
            {"icon": "✍️", "action": "Write something positive", "action_tamil": "நல்லதை எழுதுங்கள்", "difficulty": "easy"},
        ],
        "weekly_action": {"icon": "📖", "action": "Donate books to students", "action_tamil": "மாணவர்களுக்கு புத்தகம் தானம்"}
    },
    "Jupiter": {
        "tamil": "குரு",
        "day": "Thursday",
        "day_tamil": "வியாழன்",
        "color": "yellow",
        "color_tamil": "மஞ்சள்",
        "gemstone": "Yellow Sapphire",
        "gemstone_tamil": "புஷ்பராகம்",
        "mantra": "ॐ बृहस्पतये नमः",
        "mantra_tamil": "ஓம் குருவே நமஹ",
        "mantra_count": 11,
        "deity": "Lord Dakshinamurthy",
        "deity_tamil": "தட்சிணாமூர்த்தி",
        "donation": ["Yellow cloth", "Turmeric", "Bananas"],
        "donation_tamil": ["மஞ்சள் துணி", "மஞ்சள்", "வாழைப்பழம்"],
        "fasting": "Thursday",
        "direction": "North-East",
        "direction_tamil": "வடகிழக்கு",
        "temple": "Alangudi",
        "temple_tamil": "ஆலங்குடி",
        "simple_actions": [
            {"icon": "🍌", "action": "Offer banana to temple", "action_tamil": "கோவிலில் வாழைப்பழம் படையுங்கள்", "difficulty": "easy"},
            {"icon": "👕", "action": "Wear yellow color", "action_tamil": "மஞ்சள் ஆடை அணியுங்கள்", "difficulty": "easy"},
            {"icon": "🎓", "action": "Learn something new", "action_tamil": "புதியதை கற்றுக்கொள்ளுங்கள்", "difficulty": "easy"},
        ],
        "weekly_action": {"icon": "🍌", "action": "Feed bananas to needy", "action_tamil": "ஏழைகளுக்கு வாழைப்பழம் தானம்"}
    },
    "Venus": {
        "tamil": "சுக்கிரன்",
        "day": "Friday",
        "day_tamil": "வெள்ளி",
        "color": "white",
        "color_tamil": "வெள்ளை/இளஞ்சிவப்பு",
        "gemstone": "Diamond",
        "gemstone_tamil": "வைரம்",
        "mantra": "ॐ शुक्राय नमः",
        "mantra_tamil": "ஓம் சுக்ராய நமஹ",
        "mantra_count": 11,
        "deity": "Goddess Lakshmi",
        "deity_tamil": "மகாலட்சுமி",
        "donation": ["Rice", "Sugar", "White flowers"],
        "donation_tamil": ["அரிசி", "சர்க்கரை", "வெள்ளை மலர்"],
        "fasting": "Friday",
        "direction": "South-East",
        "direction_tamil": "தென்கிழக்கு",
        "temple": "Kanjanur",
        "temple_tamil": "கஞ்சனூர்",
        "simple_actions": [
            {"icon": "🌸", "action": "Keep home clean & decorated", "action_tamil": "வீட்டை சுத்தமாக வைக்கவும்", "difficulty": "easy"},
            {"icon": "👕", "action": "Wear white/pink color", "action_tamil": "வெள்ளை/இளஞ்சிவப்பு ஆடை", "difficulty": "easy"},
            {"icon": "💐", "action": "Offer flowers to Lakshmi", "action_tamil": "லட்சுமிக்கு மலர் சாற்றுங்கள்", "difficulty": "easy"},
        ],
        "weekly_action": {"icon": "🍬", "action": "Donate sweets", "action_tamil": "இனிப்பு தானம்"}
    },
    "Saturn": {
        "tamil": "சனி",
        "day": "Saturday",
        "day_tamil": "சனி",
        "color": "black/blue",
        "color_tamil": "கருப்பு/நீலம்",
        "gemstone": "Blue Sapphire",
        "gemstone_tamil": "நீலம்",
        "mantra": "ॐ शनैश्चराय नमः",
        "mantra_tamil": "ஓம் சனைஸ்சராய நமஹ",
        "mantra_count": 11,
        "deity": "Lord Hanuman",
        "deity_tamil": "ஆஞ்சநேயர்",
        "donation": ["Sesame oil", "Black cloth"],
        "donation_tamil": ["எள் எண்ணெய்", "கருப்பு துணி"],
        "fasting": "Saturday",
        "direction": "West",
        "direction_tamil": "மேற்கு",
        "temple": "Thirunallar",
        "temple_tamil": "திருநள்ளாறு",
        "simple_actions": [
            {"icon": "🪔", "action": "Light sesame oil lamp", "action_tamil": "எள் எண்ணெய் விளக்கு ஏற்றுங்கள்", "difficulty": "easy"},
            {"icon": "👕", "action": "Wear dark blue/black", "action_tamil": "கருப்பு/நீலம் ஆடை அணியுங்கள்", "difficulty": "easy"},
            {"icon": "🐕", "action": "Feed a stray dog", "action_tamil": "தெரு நாய்க்கு உணவளியுங்கள்", "difficulty": "easy"},
        ],
        "weekly_action": {"icon": "🛢️", "action": "Donate sesame oil", "action_tamil": "எள் எண்ணெய் தானம்"}
    },
    "Rahu": {
        "tamil": "ராகு",
        "day": "Saturday",
        "day_tamil": "சனி",
        "color": "blue",
        "color_tamil": "நீலம்",
        "gemstone": "Hessonite",
        "gemstone_tamil": "கோமேதகம்",
        "mantra": "ॐ राहवे नमः",
        "mantra_tamil": "ஓம் ராகவே நமஹ",
        "mantra_count": 11,
        "deity": "Goddess Durga",
        "deity_tamil": "துர்கா தேவி",
        "donation": ["Blanket", "Blue cloth"],
        "donation_tamil": ["போர்வை", "நீல துணி"],
        "fasting": "Saturday",
        "direction": "South-West",
        "direction_tamil": "தென்மேற்கு",
        "temple": "Thirunageswaram",
        "temple_tamil": "திருநாகேஸ்வரம்",
        "simple_actions": [
            {"icon": "🧘", "action": "Meditate for 5 mins", "action_tamil": "5 நிமிடம் தியானம்", "difficulty": "easy"},
            {"icon": "👕", "action": "Wear blue color", "action_tamil": "நீல ஆடை அணியுங்கள்", "difficulty": "easy"},
            {"icon": "🙏", "action": "Pray to Durga", "action_tamil": "துர்கா தேவியை வழிபடுங்கள்", "difficulty": "easy"},
        ],
        "weekly_action": {"icon": "🛏️", "action": "Donate blanket to poor", "action_tamil": "ஏழைகளுக்கு போர்வை தானம்"}
    },
    "Ketu": {
        "tamil": "கேது",
        "day": "Tuesday",
        "day_tamil": "செவ்வாய்",
        "color": "grey/brown",
        "color_tamil": "சாம்பல்/பழுப்பு",
        "gemstone": "Cat's Eye",
        "gemstone_tamil": "வைடூர்யம்",
        "mantra": "ॐ केतवे नमः",
        "mantra_tamil": "ஓம் கேதவே நமஹ",
        "mantra_count": 11,
        "deity": "Lord Ganesha",
        "deity_tamil": "விநாயகர்",
        "donation": ["Blanket", "Food"],
        "donation_tamil": ["போர்வை", "உணவு"],
        "fasting": "Tuesday",
        "direction": "South-West",
        "direction_tamil": "தென்மேற்கு",
        "temple": "Keezhperumpallam",
        "temple_tamil": "கீழ்பெரும்பள்ளம்",
        "simple_actions": [
            {"icon": "🐘", "action": "Pray to Ganesha", "action_tamil": "விநாயகரை வழிபடுங்கள்", "difficulty": "easy"},
            {"icon": "🧘", "action": "Practice deep breathing", "action_tamil": "ஆழ்ந்த சுவாசம் பயிலுங்கள்", "difficulty": "easy"},
            {"icon": "🍽️", "action": "Feed someone hungry", "action_tamil": "பசித்தவருக்கு உணவளியுங்கள்", "difficulty": "easy"},
        ],
        "weekly_action": {"icon": "🍛", "action": "Donate food", "action_tamil": "அன்னதானம் செய்யுங்கள்"}
    }
}

# Dosha definitions
DOSHAS = {
    "mangal_dosha": {
        "name": "Mangal Dosha",
        "tamil": "செவ்வாய் தோஷம்",
        "description": "Mars in 1st, 4th, 7th, 8th, or 12th house",
        "description_tamil": "செவ்வாய் 1, 4, 7, 8, 12 ஆம் வீட்டில்",
        "affects": ["marriage", "relationships"],
        "remedies": [
            "Worship Lord Hanuman on Tuesdays",
            "Chant Hanuman Chalisa daily",
            "Donate red cloth and lentils on Tuesday",
            "Visit Vaitheeswaran Koil"
        ],
        "remedies_tamil": [
            "செவ்வாயன்று ஹனுமானை வழிபடுங்கள்",
            "தினமும் ஹனுமான் சாலிசா படியுங்கள்",
            "செவ்வாய்கிழமை சிவப்பு துணி, பருப்பு தானம் செய்யுங்கள்",
            "வைத்தீஸ்வரன் கோவில் செல்லுங்கள்"
        ]
    },
    "kaal_sarp": {
        "name": "Kaal Sarp Dosha",
        "tamil": "கால சர்ப்ப தோஷம்",
        "description": "All planets between Rahu and Ketu",
        "description_tamil": "எல்லா கிரகங்களும் ராகு-கேது இடையே",
        "affects": ["overall life", "obstacles"],
        "remedies": [
            "Perform Kaal Sarp Puja at Trimbakeshwar",
            "Visit Rahu-Ketu temples on Saturdays",
            "Offer milk to snake idol",
            "Chant Maha Mrityunjaya Mantra"
        ],
        "remedies_tamil": [
            "திரிம்பகேஸ்வரில் கால சர்ப்ப பூஜை செய்யுங்கள்",
            "சனிக்கிழமை ராகு-கேது கோவில் செல்லுங்கள்",
            "நாக சிலைக்கு பால் அபிஷேகம் செய்யுங்கள்",
            "மகா மிருத்யுஞ்சய மந்திரம் ஜபியுங்கள்"
        ]
    },
    "pitra_dosha": {
        "name": "Pitra Dosha",
        "tamil": "பித்ரு தோஷம்",
        "description": "Sun afflicted by Rahu/Ketu or Saturn",
        "description_tamil": "சூரியன் ராகு/கேது அல்லது சனியால் பாதிப்பு",
        "affects": ["career", "father's health", "ancestral issues"],
        "remedies": [
            "Perform Shraddha rituals",
            "Donate food to Brahmins on Amavasya",
            "Visit Gaya and perform Pind Daan",
            "Feed crows and dogs"
        ],
        "remedies_tamil": [
            "சிராத்த கர்மங்கள் செய்யுங்கள்",
            "அமாவாசையில் பிராமணர்களுக்கு அன்னதானம்",
            "காயா சென்று பிண்ட தானம் செய்யுங்கள்",
            "காகங்கள், நாய்களுக்கு உணவளியுங்கள்"
        ]
    },
    "shani_dosha": {
        "name": "Shani Dosha",
        "tamil": "சனி தோஷம்",
        "description": "Saturn in adverse position or Sade Sati period",
        "description_tamil": "சனி பகவான் பாதிப்பு அல்லது சாடே சாதி காலம்",
        "affects": ["career", "health", "mental peace"],
        "remedies": [
            "Light sesame oil lamp on Saturdays",
            "Donate black items on Saturday",
            "Visit Thirunallar temple",
            "Chant Shani mantra 11 times"
        ],
        "remedies_tamil": [
            "சனிக்கிழமை எள் எண்ணெய் விளக்கு ஏற்றுங்கள்",
            "சனிக்கிழமை கருப்பு பொருட்கள் தானம்",
            "திருநள்ளாறு கோவில் செல்லுங்கள்",
            "சனி மந்திரம் 11 முறை ஜபியுங்கள்"
        ]
    }
}

# Goal-based remedies
GOAL_REMEDIES = {
    "love": {
        "planets": ["Venus", "Moon"],
        "houses": [5, 7],
        "deities": ["Goddess Parvati", "Lord Krishna"],
        "deities_tamil": ["பார்வதி தேவி", "கிருஷ்ணர்"],
        "rituals": [
            "Worship Venus on Fridays",
            "Offer white flowers to Goddess Lakshmi",
            "Chant Kamdev Gayatri mantra",
            "Wear white on Fridays"
        ],
        "rituals_tamil": [
            "வெள்ளிக்கிழமை சுக்கிரனை வழிபடுங்கள்",
            "லட்சுமி தேவிக்கு வெள்ளை மலர் சாற்றுங்கள்",
            "காமதேவ காயத்ரி மந்திரம் ஜபியுங்கள்",
            "வெள்ளிக்கிழமை வெள்ளை உடை அணியுங்கள்"
        ]
    },
    "job": {
        "planets": ["Sun", "Saturn", "Jupiter"],
        "houses": [10, 6, 2],
        "deities": ["Lord Surya", "Lord Shiva"],
        "deities_tamil": ["சூரிய பகவான்", "சிவபெருமான்"],
        "rituals": [
            "Offer water to Sun at sunrise",
            "Recite Aditya Hridayam on Sundays",
            "Worship Lord Ganesha before starting work",
            "Light ghee lamp facing East"
        ],
        "rituals_tamil": [
            "அதிகாலை சூரியனுக்கு அர்க்கியம் செய்யுங்கள்",
            "ஞாயிறன்று ஆதித்ய ஹிருதயம் படியுங்கள்",
            "வேலை தொடங்கும் முன் விநாயகரை வழிபடுங்கள்",
            "கிழக்கு நோக்கி நெய் விளக்கு ஏற்றுங்கள்"
        ]
    },
    "wealth": {
        "planets": ["Jupiter", "Venus", "Mercury"],
        "houses": [2, 11, 9],
        "deities": ["Goddess Lakshmi", "Lord Kubera"],
        "deities_tamil": ["மகாலட்சுமி", "குபேரன்"],
        "rituals": [
            "Worship Goddess Lakshmi on Fridays",
            "Keep money in North direction",
            "Chant Sri Suktam daily",
            "Light lamp with cow ghee in evening"
        ],
        "rituals_tamil": [
            "வெள்ளிக்கிழமை மகாலட்சுமியை வழிபடுங்கள்",
            "வடக்கு திசையில் பணம் வைக்கவும்",
            "தினமும் ஸ்ரீ சூக்தம் படியுங்கள்",
            "மாலையில் பசு நெய் விளக்கு ஏற்றுங்கள்"
        ]
    },
    "peace": {
        "planets": ["Moon", "Jupiter"],
        "houses": [4, 9, 12],
        "deities": ["Lord Shiva", "Goddess Saraswati"],
        "deities_tamil": ["சிவபெருமான்", "சரஸ்வதி தேவி"],
        "rituals": [
            "Meditate during Brahma Muhurta",
            "Chant Om Namah Shivaya 11 times",
            "Visit Shiva temple on Mondays",
            "Practice pranayama daily"
        ],
        "rituals_tamil": [
            "பிரம்ம முகூர்த்தத்தில் தியானம் செய்யுங்கள்",
            "ஓம் நமசிவாய 11 முறை ஜபியுங்கள்",
            "திங்களன்று சிவன் கோவில் செல்லுங்கள்",
            "தினமும் பிராணாயாமம் பயிற்சி செய்யுங்கள்"
        ]
    },
    "health": {
        "planets": ["Sun", "Mars", "Moon"],
        "houses": [1, 6, 8],
        "deities": ["Lord Dhanvantari", "Lord Hanuman"],
        "deities_tamil": ["தன்வந்திரி", "ஆஞ்சநேயர்"],
        "rituals": [
            "Chant Maha Mrityunjaya Mantra",
            "Worship Lord Dhanvantari",
            "Practice Surya Namaskar at sunrise",
            "Donate medicines to needy"
        ],
        "rituals_tamil": [
            "மகா மிருத்யுஞ்சய மந்திரம் ஜபியுங்கள்",
            "தன்வந்திரியை வழிபடுங்கள்",
            "அதிகாலை சூர்ய நமஸ்காரம் செய்யுங்கள்",
            "ஏழைகளுக்கு மருந்து தானம் செய்யுங்கள்"
        ]
    },
    "education": {
        "planets": ["Jupiter", "Mercury"],
        "houses": [4, 5, 9],
        "deities": ["Goddess Saraswati", "Lord Hayagriva"],
        "deities_tamil": ["சரஸ்வதி தேவி", "ஹயக்ரீவர்"],
        "rituals": [
            "Worship Goddess Saraswati on Wednesdays",
            "Chant Saraswati Vandana before studying",
            "Keep books in North-East direction",
            "Light lamp while studying"
        ],
        "rituals_tamil": [
            "புதனன்று சரஸ்வதியை வழிபடுங்கள்",
            "படிக்கும் முன் சரஸ்வதி வந்தனம் சொல்லுங்கள்",
            "வடகிழக்கில் புத்தகங்கள் வைக்கவும்",
            "படிக்கும்போது விளக்கு ஏற்றுங்கள்"
        ]
    }
}


class RemedyEngine:
    """
    AI-powered remedy engine that generates personalized remedies
    """

    def __init__(self, jathagam_generator=None, panchangam_calculator=None):
        self.jathagam_gen = jathagam_generator
        self.panchangam = panchangam_calculator

    def get_personalized_remedies(self, data) -> Dict:
        """Generate comprehensive personalized remedies"""
        # Create birth details object
        class BirthDetails:
            def __init__(self, d):
                self.name = d.name
                self.date = d.birth_date
                self.time = d.birth_time
                self.place = d.birth_place
                self.latitude = d.latitude
                self.longitude = d.longitude

        birth_details = BirthDetails(data)
        language = getattr(data, 'language', 'ta') or 'ta'

        # Generate jathagam
        jathagam = self.jathagam_gen.generate(birth_details)

        # Get current dasha
        current_dasha = jathagam["dasha"]["current"]

        # Find weak planets (strength < 50) - language aware
        weak_planets = [
            {
                "planet": p["planet"] if language == "en" else p["tamil_name"],
                "planet_tamil": p["tamil_name"],
                "planet_en": p["planet"],
                "strength": p["strength"],
                "rasi": p["rasi"] if language == "en" else p["rasi_tamil"]
            }
            for p in jathagam["planets"] if p["strength"] < 50
        ]

        # Detect doshas
        doshas = self._detect_doshas(jathagam, language)

        # Get goal-specific analysis if goal provided
        goal_analysis = None
        if data.goal:
            goal_analysis = self._analyze_goal(jathagam, data.goal.value, language)

        # Generate remedies
        remedies = self._generate_remedies(
            current_dasha,
            weak_planets,
            doshas,
            data.goal.value if data.goal else None,
            language
        )

        # Generate daily routine
        daily_routine = self._generate_daily_routine(current_dasha, weak_planets, language)

        # Generate lucky items
        lucky_items = self._generate_lucky_items(jathagam, language)

        return {
            "user_name": data.name,
            "current_dasha": {
                "mahadasha": current_dasha["lord"] if language == "en" else current_dasha["tamil_lord"],
                "mahadasha_tamil": current_dasha["tamil_lord"],
                "mahadasha_en": current_dasha["lord"],
                "period": f"{current_dasha['start']} to {current_dasha['end']}",
                "years_remaining": self._calculate_remaining_years(current_dasha["end"])
            },
            "weak_planets": weak_planets,
            "doshas": doshas,
            "goal_analysis": goal_analysis,
            "remedies": remedies,
            "daily_routine": daily_routine,
            "lucky_items": lucky_items
        }

    def _detect_doshas(self, jathagam: Dict, language: str = "ta") -> List[Dict]:
        """Detect doshas in the birth chart"""
        doshas = []
        planets = {p["planet"]: p for p in jathagam["planets"]}

        # Check Mangal Dosha (simplified)
        mars = planets.get("Mars", {})
        mars_rasi = mars.get("rasi_tamil", "")
        # For simplicity, just check if Mars is weak or retrograde
        if mars.get("strength", 100) < 40 or mars.get("is_retrograde", False):
            doshas.append({
                **DOSHAS["mangal_dosha"],
                "severity": "moderate" if mars.get("strength", 100) > 30 else "high"
            })

        # Check Shani Dosha
        saturn = planets.get("Saturn", {})
        if saturn.get("strength", 100) < 40:
            doshas.append({
                **DOSHAS["shani_dosha"],
                "severity": "moderate" if saturn.get("strength", 100) > 30 else "high"
            })

        # Check for Rahu-Ketu issues (simplified Kaal Sarp)
        rahu = planets.get("Rahu", {})
        ketu = planets.get("Ketu", {})
        if rahu.get("strength", 100) < 40 and ketu.get("strength", 100) < 40:
            doshas.append({
                **DOSHAS["kaal_sarp"],
                "severity": "moderate"
            })

        return doshas

    def _analyze_goal(self, jathagam: Dict, goal: str, language: str = "ta") -> Dict:
        """Analyze chart for specific goal"""
        goal_info = GOAL_REMEDIES.get(goal, GOAL_REMEDIES["peace"])
        planets = {p["planet"]: p for p in jathagam["planets"]}

        # Calculate goal-related planet strengths
        relevant_strengths = []
        for planet_name in goal_info["planets"]:
            planet = planets.get(planet_name, {})
            relevant_strengths.append({
                "planet": planet_name,
                "planet_tamil": planet.get("tamil_name", PLANET_REMEDIES.get(planet_name, {}).get("tamil", planet_name)),
                "strength": planet.get("strength", 50),
                "status": "strong" if planet.get("strength", 50) >= 60 else "weak"
            })

        # Calculate overall goal favorability
        avg_strength = sum(p["strength"] for p in relevant_strengths) / len(relevant_strengths)

        return {
            "goal": goal,
            "favorability": round(avg_strength, 1),
            "status": "favorable" if avg_strength >= 60 else "needs attention",
            "relevant_planets": relevant_strengths,
            "deities": goal_info["deities_tamil"],
            "recommended_rituals": goal_info["rituals_tamil"][:3]
        }

    def _generate_remedies(
        self,
        current_dasha: Dict,
        weak_planets: List[Dict],
        doshas: List[Dict],
        goal: Optional[str],
        language: str = "ta"
    ) -> List[Dict]:
        """Generate prioritized list of remedies"""
        remedies = []
        priority = 1

        # 1. Dasha lord remedies (highest priority) - NOW PRACTICAL
        dasha_lord = current_dasha["lord"]
        dasha_remedies = PLANET_REMEDIES.get(dasha_lord, {})
        if dasha_remedies:
            simple_actions = dasha_remedies.get("simple_actions", [])
            weekly_action = dasha_remedies.get("weekly_action", {})

            remedies.append({
                "id": f"dasha_{dasha_lord.lower()}",
                "type": "dasha_remedy",
                "priority": priority,
                "planet": dasha_lord,
                "planet_tamil": dasha_remedies.get("tamil", dasha_lord),
                "title": f"Strengthen {dasha_lord} (Current Dasha Lord)",
                "title_tamil": f"{dasha_remedies.get('tamil', dasha_lord)} பலப்படுத்துங்கள்",
                "simple_actions": simple_actions,  # NEW: Easy daily actions
                "weekly_action": weekly_action,     # NEW: Weekly special
                "remedies": [
                    {
                        "icon": simple_actions[0].get("icon", "🙏") if simple_actions else "🙏",
                        "action": simple_actions[0].get("action", "") if simple_actions else f"Pray to {dasha_remedies.get('deity', '')}",
                        "action_tamil": simple_actions[0].get("action_tamil", "") if simple_actions else f"{dasha_remedies.get('deity_tamil', '')} வழிபடுங்கள்",
                        "difficulty": "easy",
                        "timing": "Daily"
                    },
                    {
                        "icon": "👕",
                        "action": f"Wear {dasha_remedies.get('color', '')} on {dasha_remedies.get('day', '')}",
                        "action_tamil": f"{dasha_remedies.get('day_tamil', '')} - {dasha_remedies.get('color_tamil', '')} ஆடை",
                        "difficulty": "easy",
                        "timing": dasha_remedies.get("day", "Weekly")
                    },
                    {
                        "icon": weekly_action.get("icon", "🎁"),
                        "action": weekly_action.get("action", f"Donate {', '.join(dasha_remedies.get('donation', [])[:1])}"),
                        "action_tamil": weekly_action.get("action_tamil", f"{', '.join(dasha_remedies.get('donation_tamil', [])[:1])} தானம்"),
                        "difficulty": "easy",
                        "timing": f"On {dasha_remedies.get('day', '')}"
                    }
                ],
                "effectiveness": 85
            })
            priority += 1

        # 2. Weak planet remedies - NOW PRACTICAL & GAMIFIED
        for wp in weak_planets[:3]:  # Top 3 weak planets
            planet_name = wp["planet"]
            planet_remedies = PLANET_REMEDIES.get(planet_name, {})
            if planet_remedies:
                simple_actions = planet_remedies.get("simple_actions", [])
                weekly_action = planet_remedies.get("weekly_action", {})

                # Build practical remedies list
                practical_remedies = []
                for action in simple_actions[:2]:  # Take first 2 simple actions
                    practical_remedies.append({
                        "icon": action.get("icon", "🙏"),
                        "action": action.get("action", ""),
                        "action_tamil": action.get("action_tamil", ""),
                        "difficulty": action.get("difficulty", "easy"),
                        "timing": "Daily"
                    })

                # Add weekly action
                practical_remedies.append({
                    "icon": weekly_action.get("icon", "🎁"),
                    "action": weekly_action.get("action", ""),
                    "action_tamil": weekly_action.get("action_tamil", ""),
                    "difficulty": "easy",
                    "timing": planet_remedies.get("day", "Weekly")
                })

                remedies.append({
                    "id": f"weak_{planet_name.lower()}",
                    "type": "weak_planet_remedy",
                    "priority": priority,
                    "planet": planet_name,
                    "planet_tamil": planet_remedies.get("tamil", planet_name),
                    "title": f"Strengthen {planet_name}",
                    "title_tamil": f"{planet_remedies.get('tamil', planet_name)} பலப்படுத்துங்கள்",
                    "strength": wp["strength"],
                    "simple_actions": simple_actions,
                    "weekly_action": weekly_action,
                    "remedies": practical_remedies,
                    "effectiveness": 75
                })
                priority += 1

        # 3. Dosha remedies
        for dosha in doshas[:2]:  # Top 2 doshas
            remedies.append({
                "id": f"dosha_{dosha['name'].lower().replace(' ', '_')}",
                "type": "dosha_remedy",
                "priority": priority,
                "title": f"Remedy for {dosha['name']}",
                "title_tamil": f"{dosha['tamil']} பரிகாரம்",
                "description": dosha["description_tamil"],
                "severity": dosha.get("severity", "moderate"),
                "remedies": [
                    {"action": r, "action_tamil": rt}
                    for r, rt in zip(dosha["remedies"][:3], dosha["remedies_tamil"][:3])
                ],
                "effectiveness": 80 if dosha.get("severity") == "high" else 70
            })
            priority += 1

        # 4. Goal-specific remedies
        if goal and goal in GOAL_REMEDIES:
            goal_info = GOAL_REMEDIES[goal]
            remedies.append({
                "id": f"goal_{goal}",
                "type": "goal_remedy",
                "priority": priority,
                "goal": goal,
                "title": f"Achieve {goal.title()}",
                "title_tamil": self._get_goal_tamil(goal),
                "deities": goal_info["deities_tamil"],
                "remedies": [
                    {"action": r, "action_tamil": rt}
                    for r, rt in zip(goal_info["rituals"][:4], goal_info["rituals_tamil"][:4])
                ],
                "effectiveness": 80
            })

        return remedies

    def _generate_daily_routine(self, current_dasha: Dict, weak_planets: List[Dict], language: str = "ta") -> Dict:
        """Generate recommended daily spiritual routine"""
        dasha_lord = current_dasha["lord"]
        dasha_info = PLANET_REMEDIES.get(dasha_lord, {})

        if language == "en":
            morning_routines = [
                {"time": "5:00 - 6:00", "activity": "Wake up in Brahma Muhurta"},
                {"time": "6:00 - 6:30", "activity": "Offer water to Sun"},
                {"time": "6:30 - 7:00", "activity": f"Chant {dasha_info.get('mantra', 'planet mantra')}"},
            ]
            evening_routines = [
                {"time": "18:00 - 18:30", "activity": "Light ghee lamp"},
                {"time": "18:30 - 19:00", "activity": "Meditation"},
                {"time": "19:00 - 19:30", "activity": f"Worship {dasha_info.get('deity', 'deity')}"},
            ]
            weekly_special = {
                "day": dasha_info.get("day", ""),
                "activities": [
                    "Observe fasting",
                    f"Visit {dasha_info.get('temple', 'planet temple')}",
                    f"Donate {', '.join(dasha_info.get('donation', ['items'])[:2])}"
                ]
            }
        else:
            morning_routines = [
                {"time": "5:00 - 6:00", "activity": "பிரம்ம முகூர்த்தத்தில் எழுங்கள்"},
                {"time": "6:00 - 6:30", "activity": "சூரியனுக்கு அர்க்கியம்"},
                {"time": "6:30 - 7:00", "activity": f"{dasha_info.get('mantra_tamil', 'கிரக மந்திரம்')} ஜபம்"},
            ]
            evening_routines = [
                {"time": "18:00 - 18:30", "activity": "நெய் விளக்கு ஏற்றுங்கள்"},
                {"time": "18:30 - 19:00", "activity": "தியானம்"},
                {"time": "19:00 - 19:30", "activity": f"{dasha_info.get('deity_tamil', 'இஷ்ட தெய்வ')} வழிபாடு"},
            ]
            weekly_special = {
                "day": dasha_info.get("day_tamil", ""),
                "activities": [
                    "விரதம் இருங்கள்",
                    f"{dasha_info.get('temple_tamil', 'கிரக கோவில்')} செல்லுங்கள்",
                    f"{', '.join(dasha_info.get('donation_tamil', ['தானம்'])[:2])} தானம் செய்யுங்கள்"
                ]
            }

        return {
            "morning": morning_routines,
            "evening": evening_routines,
            "weekly_special": weekly_special
        }

    def _generate_lucky_items(self, jathagam: Dict, language: str = "ta") -> Dict:
        """Generate lucky items based on chart"""
        moon_sign = jathagam.get("moon_sign", {})
        lagna = jathagam.get("lagna", {})

        # Get strongest planet
        planets_sorted = sorted(jathagam["planets"], key=lambda x: x["strength"], reverse=True)
        strongest_planet = planets_sorted[0] if planets_sorted else None
        strongest_info = PLANET_REMEDIES.get(strongest_planet["planet"], {}) if strongest_planet else {}

        if language == "en":
            return {
                "color": strongest_info.get("color", "yellow"),
                "number": random.randint(1, 9),
                "day": strongest_info.get("day", "Thursday"),
                "direction": strongest_info.get("direction", "North-East"),
                "gemstone": strongest_info.get("gemstone", "Yellow Sapphire")
            }
        else:
            return {
                "color": strongest_info.get("color_tamil", "மஞ்சள்"),
                "number": random.randint(1, 9),
                "day": strongest_info.get("day_tamil", "வியாழன்"),
                "direction": strongest_info.get("direction_tamil", "வடகிழக்கு"),
                "gemstone": strongest_info.get("gemstone_tamil", "புஷ்பராகம்")
            }

    def _calculate_remaining_years(self, end_date_str: str) -> float:
        """Calculate remaining years from end date"""
        try:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            remaining_days = (end_date - datetime.now()).days
            return round(max(0, remaining_days / 365.25), 1)
        except:
            return 0.0

    def _get_goal_tamil(self, goal: str) -> str:
        """Get Tamil translation for goal"""
        goal_tamil = {
            "love": "காதல் / திருமணம் வெற்றி",
            "job": "வேலை / தொழில் வெற்றி",
            "wealth": "செல்வம் / பணம் வளர்ச்சி",
            "peace": "மன அமைதி",
            "health": "உடல் நலம்",
            "education": "கல்வி வெற்றி"
        }
        return goal_tamil.get(goal, goal)

    def get_planet_remedies(self, planet: str, language: str = "ta") -> Dict:
        """Get remedies for a specific planet"""
        planet_info = PLANET_REMEDIES.get(planet, PLANET_REMEDIES.get("Sun"))

        return {
            "planet": planet,
            "planet_tamil": planet_info.get("tamil"),
            "day": planet_info.get("day_tamil") if language == "ta" else planet_info.get("day"),
            "color": planet_info.get("color_tamil") if language == "ta" else planet_info.get("color"),
            "gemstone": planet_info.get("gemstone_tamil") if language == "ta" else planet_info.get("gemstone"),
            "mantra": planet_info.get("mantra_tamil") if language == "ta" else planet_info.get("mantra"),
            "deity": planet_info.get("deity_tamil") if language == "ta" else planet_info.get("deity"),
            "temple": planet_info.get("temple_tamil") if language == "ta" else planet_info.get("temple"),
            "donation": planet_info.get("donation_tamil") if language == "ta" else planet_info.get("donation"),
            "direction": planet_info.get("direction_tamil") if language == "ta" else planet_info.get("direction")
        }

    def get_dosha_remedies(self, dosha: str, language: str = "ta") -> Dict:
        """Get remedies for a specific dosha"""
        dosha_key = dosha.lower().replace(" ", "_")
        dosha_info = DOSHAS.get(dosha_key, list(DOSHAS.values())[0])

        return {
            "name": dosha_info.get("tamil") if language == "ta" else dosha_info.get("name"),
            "description": dosha_info.get("description_tamil") if language == "ta" else dosha_info.get("description"),
            "affects": dosha_info.get("affects"),
            "remedies": dosha_info.get("remedies_tamil") if language == "ta" else dosha_info.get("remedies")
        }

    def get_daily_remedies(self, rasi: str, nakshatra: str, language: str = "ta") -> Dict:
        """Get simple daily remedies based on day of week - PRACTICAL & GAMIFIED"""
        today = datetime.now()
        day_of_week = today.weekday()

        # Day planets
        day_planets = ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Sun"]
        today_planet = day_planets[day_of_week]
        planet_info = PLANET_REMEDIES.get(today_planet, {})
        simple_actions = planet_info.get("simple_actions", [])
        weekly_action = planet_info.get("weekly_action", {})

        # Build gamified remedies with icons
        gamified_remedies = []
        for action in simple_actions:
            if language == "ta":
                gamified_remedies.append({
                    "icon": action.get("icon", "✨"),
                    "text": action.get("action_tamil", action.get("action", "")),
                    "difficulty": action.get("difficulty", "easy")
                })
            else:
                gamified_remedies.append({
                    "icon": action.get("icon", "✨"),
                    "text": action.get("action", ""),
                    "difficulty": action.get("difficulty", "easy")
                })

        return {
            "date": today.strftime("%Y-%m-%d"),
            "day": planet_info.get("day_tamil") if language == "ta" else planet_info.get("day"),
            "ruling_planet": planet_info.get("tamil") if language == "ta" else today_planet,
            "recommended_color": planet_info.get("color_tamil") if language == "ta" else planet_info.get("color"),
            "deity_to_worship": planet_info.get("deity_tamil") if language == "ta" else planet_info.get("deity"),
            "direction": planet_info.get("direction_tamil") if language == "ta" else planet_info.get("direction"),
            "gamified_remedies": gamified_remedies,  # NEW: Gamified with icons
            "weekly_action": {
                "icon": weekly_action.get("icon", "🎁"),
                "text": weekly_action.get("action_tamil" if language == "ta" else "action", "")
            },
            # Keep simple_remedies for backward compatibility
            "simple_remedies": [
                f"இன்று {planet_info.get('color_tamil', '')} நிற ஆடை அணியுங்கள்" if language == "ta" else f"Wear {planet_info.get('color', '')} color today",
                f"{planet_info.get('deity_tamil', '')} வழிபடுங்கள்" if language == "ta" else f"Worship {planet_info.get('deity', '')}",
                f"{weekly_action.get('action_tamil', '')}" if language == "ta" else weekly_action.get("action", "")
            ]
        }

    def get_goal_remedies(self, goal: str, rasi: str, language: str = "ta") -> Dict:
        """Get remedies for achieving a specific goal"""
        goal_info = GOAL_REMEDIES.get(goal, GOAL_REMEDIES.get("peace"))

        return {
            "goal": self._get_goal_tamil(goal) if language == "ta" else goal.title(),
            "relevant_planets": [PLANET_REMEDIES.get(p, {}).get("tamil" if language == "ta" else "name", p) for p in goal_info["planets"]],
            "deities": goal_info.get("deities_tamil") if language == "ta" else goal_info.get("deities"),
            "rituals": goal_info.get("rituals_tamil") if language == "ta" else goal_info.get("rituals"),
            "recommended_days": [PLANET_REMEDIES.get(p, {}).get("day_tamil" if language == "ta" else "day", "") for p in goal_info["planets"][:2]]
        }
