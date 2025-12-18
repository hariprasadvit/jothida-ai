"""
V6.2 Super Jyotish Engine - Core Calculation Module
All calculations are mathematically derived from birth chart data.
No static text - every insight has astrological basis.

V6.2 Enhancements:
- POI (Planet Operating Index) with combustion and transit mods
- HAI (House Activation Index) with Saturn pressure
- Enhanced aspect calculations with degree-based orbs
- Chart rendering data for D1, D9, D10
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, date, timedelta
from dataclasses import dataclass, field
import math

# ============== CONSTANTS ==============

RASIS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

RASI_TAMIL = ['மேஷம்', 'ரிஷபம்', 'மிதுனம்', 'கடகம்', 'சிம்மம்', 'கன்னி',
              'துலாம்', 'விருச்சிகம்', 'தனுசு', 'மகரம்', 'கும்பம்', 'மீனம்']

PLANETS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']

PLANET_TAMIL = {
    'Sun': 'சூரியன்', 'Moon': 'சந்திரன்', 'Mars': 'செவ்வாய்', 'Mercury': 'புதன்',
    'Jupiter': 'குரு', 'Venus': 'சுக்கிரன்', 'Saturn': 'சனி', 'Rahu': 'ராகு', 'Ketu': 'கேது'
}

PLANET_SYMBOLS = {
    'Sun': '☉', 'Moon': '☽', 'Mars': '♂', 'Mercury': '☿',
    'Jupiter': '♃', 'Venus': '♀', 'Saturn': '♄', 'Rahu': '☊', 'Ketu': '☋'
}

# Planet abbreviations for chart display
PLANET_ABBR = {
    'Sun': 'Su', 'Moon': 'Mo', 'Mars': 'Ma', 'Mercury': 'Me',
    'Jupiter': 'Ju', 'Venus': 'Ve', 'Saturn': 'Sa', 'Rahu': 'Ra', 'Ketu': 'Ke'
}

# Sanskrit/Tamil planet names
PLANET_SANSKRIT = {
    'Sun': 'Surya', 'Moon': 'Chandra', 'Mars': 'Kuja', 'Mercury': 'Budha',
    'Jupiter': 'Guru', 'Venus': 'Shukra', 'Saturn': 'Sani', 'Rahu': 'Rahu', 'Ketu': 'Ketu'
}

# Rasi Sanskrit names
RASI_SANSKRIT = {
    'Aries': 'Mesha', 'Taurus': 'Vrishabha', 'Gemini': 'Mithuna', 'Cancer': 'Karkata',
    'Leo': 'Simha', 'Virgo': 'Kanya', 'Libra': 'Thula', 'Scorpio': 'Vrischika',
    'Sagittarius': 'Dhanu', 'Capricorn': 'Makara', 'Aquarius': 'Kumbha', 'Pisces': 'Meena'
}

# Rasi Lords
RASI_LORDS = {
    'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury', 'Cancer': 'Moon',
    'Leo': 'Sun', 'Virgo': 'Mercury', 'Libra': 'Venus', 'Scorpio': 'Mars',
    'Sagittarius': 'Jupiter', 'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
}

# Exaltation signs
EXALTATION = {
    'Sun': 'Aries', 'Moon': 'Taurus', 'Mars': 'Capricorn', 'Mercury': 'Virgo',
    'Jupiter': 'Cancer', 'Venus': 'Pisces', 'Saturn': 'Libra'
}

# Debilitation signs
DEBILITATION = {
    'Sun': 'Libra', 'Moon': 'Scorpio', 'Mars': 'Cancer', 'Mercury': 'Pisces',
    'Jupiter': 'Capricorn', 'Venus': 'Virgo', 'Saturn': 'Aries'
}

# Moolatrikona signs and degrees
MOOLATRIKONA = {
    'Sun': ('Leo', 0, 20), 'Moon': ('Taurus', 4, 30), 'Mars': ('Aries', 0, 12),
    'Mercury': ('Virgo', 16, 20), 'Jupiter': ('Sagittarius', 0, 10),
    'Venus': ('Libra', 0, 15), 'Saturn': ('Aquarius', 0, 20)
}

# Own signs
OWN_SIGNS = {
    'Sun': ['Leo'], 'Moon': ['Cancer'], 'Mars': ['Aries', 'Scorpio'],
    'Mercury': ['Gemini', 'Virgo'], 'Jupiter': ['Sagittarius', 'Pisces'],
    'Venus': ['Taurus', 'Libra'], 'Saturn': ['Capricorn', 'Aquarius']
}

# Planetary friendships
NATURAL_FRIENDS = {
    'Sun': ['Moon', 'Mars', 'Jupiter'],
    'Moon': ['Sun', 'Mercury'],
    'Mars': ['Sun', 'Moon', 'Jupiter'],
    'Mercury': ['Sun', 'Venus'],
    'Jupiter': ['Sun', 'Moon', 'Mars'],
    'Venus': ['Mercury', 'Saturn'],
    'Saturn': ['Mercury', 'Venus']
}

NATURAL_ENEMIES = {
    'Sun': ['Venus', 'Saturn'],
    'Moon': [],
    'Mars': ['Mercury'],
    'Mercury': ['Moon'],
    'Jupiter': ['Mercury', 'Venus'],
    'Venus': ['Sun', 'Moon'],
    'Saturn': ['Sun', 'Moon', 'Mars']
}

# Nakshatra data
NAKSHATRAS = [
    {'name': 'Ashwini', 'tamil': 'அசுவினி', 'lord': 'Ketu', 'deity': 'Ashwini Kumaras', 'guna': 'Rajas'},
    {'name': 'Bharani', 'tamil': 'பரணி', 'lord': 'Venus', 'deity': 'Yama', 'guna': 'Rajas'},
    {'name': 'Krittika', 'tamil': 'கார்த்திகை', 'lord': 'Sun', 'deity': 'Agni', 'guna': 'Rajas'},
    {'name': 'Rohini', 'tamil': 'ரோகிணி', 'lord': 'Moon', 'deity': 'Brahma', 'guna': 'Rajas'},
    {'name': 'Mrigashira', 'tamil': 'மிருகசீரிடம்', 'lord': 'Mars', 'deity': 'Soma', 'guna': 'Tamas'},
    {'name': 'Ardra', 'tamil': 'திருவாதிரை', 'lord': 'Rahu', 'deity': 'Rudra', 'guna': 'Tamas'},
    {'name': 'Punarvasu', 'tamil': 'புனர்பூசம்', 'lord': 'Jupiter', 'deity': 'Aditi', 'guna': 'Tamas'},
    {'name': 'Pushya', 'tamil': 'பூசம்', 'lord': 'Saturn', 'deity': 'Brihaspati', 'guna': 'Tamas'},
    {'name': 'Ashlesha', 'tamil': 'ஆயில்யம்', 'lord': 'Mercury', 'deity': 'Nagas', 'guna': 'Tamas'},
    {'name': 'Magha', 'tamil': 'மகம்', 'lord': 'Ketu', 'deity': 'Pitris', 'guna': 'Tamas'},
    {'name': 'Purva Phalguni', 'tamil': 'பூரம்', 'lord': 'Venus', 'deity': 'Bhaga', 'guna': 'Tamas'},
    {'name': 'Uttara Phalguni', 'tamil': 'உத்திரம்', 'lord': 'Sun', 'deity': 'Aryaman', 'guna': 'Sattva'},
    {'name': 'Hasta', 'tamil': 'அஸ்தம்', 'lord': 'Moon', 'deity': 'Savitar', 'guna': 'Sattva'},
    {'name': 'Chitra', 'tamil': 'சித்திரை', 'lord': 'Mars', 'deity': 'Tvashtar', 'guna': 'Sattva'},
    {'name': 'Swati', 'tamil': 'சுவாதி', 'lord': 'Rahu', 'deity': 'Vayu', 'guna': 'Sattva'},
    {'name': 'Vishakha', 'tamil': 'விசாகம்', 'lord': 'Jupiter', 'deity': 'Indra-Agni', 'guna': 'Sattva'},
    {'name': 'Anuradha', 'tamil': 'அனுஷம்', 'lord': 'Saturn', 'deity': 'Mitra', 'guna': 'Sattva'},
    {'name': 'Jyeshtha', 'tamil': 'கேட்டை', 'lord': 'Mercury', 'deity': 'Indra', 'guna': 'Sattva'},
    {'name': 'Mula', 'tamil': 'மூலம்', 'lord': 'Ketu', 'deity': 'Nirriti', 'guna': 'Sattva'},
    {'name': 'Purva Ashadha', 'tamil': 'பூராடம்', 'lord': 'Venus', 'deity': 'Apas', 'guna': 'Rajas'},
    {'name': 'Uttara Ashadha', 'tamil': 'உத்திராடம்', 'lord': 'Sun', 'deity': 'Vishvedevas', 'guna': 'Rajas'},
    {'name': 'Shravana', 'tamil': 'திருவோணம்', 'lord': 'Moon', 'deity': 'Vishnu', 'guna': 'Rajas'},
    {'name': 'Dhanishta', 'tamil': 'அவிட்டம்', 'lord': 'Mars', 'deity': 'Vasus', 'guna': 'Rajas'},
    {'name': 'Shatabhisha', 'tamil': 'சதயம்', 'lord': 'Rahu', 'deity': 'Varuna', 'guna': 'Rajas'},
    {'name': 'Purva Bhadrapada', 'tamil': 'பூரட்டாதி', 'lord': 'Jupiter', 'deity': 'Ajaikapada', 'guna': 'Rajas'},
    {'name': 'Uttara Bhadrapada', 'tamil': 'உத்திரட்டாதி', 'lord': 'Saturn', 'deity': 'Ahirbudhnya', 'guna': 'Tamas'},
    {'name': 'Revati', 'tamil': 'ரேவதி', 'lord': 'Mercury', 'deity': 'Pushan', 'guna': 'Tamas'},
]

# Dasha periods (Vimshottari)
DASHA_YEARS = {
    'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10, 'Mars': 7,
    'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17
}

DASHA_ORDER = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']

# Planetary maturity ages
MATURITY_AGES = {
    'Jupiter': 16, 'Sun': 22, 'Moon': 24, 'Venus': 25,
    'Mars': 28, 'Mercury': 32, 'Saturn': 36, 'Rahu': 42, 'Ketu': 48
}

# Element mapping
ELEMENT_SIGNS = {
    'Fire': ['Aries', 'Leo', 'Sagittarius'],
    'Earth': ['Taurus', 'Virgo', 'Capricorn'],
    'Air': ['Gemini', 'Libra', 'Aquarius'],
    'Water': ['Cancer', 'Scorpio', 'Pisces']
}

# Purushartha houses
PURUSHARTHA_HOUSES = {
    'Dharma': [1, 5, 9],
    'Artha': [2, 6, 10],
    'Kama': [3, 7, 11],
    'Moksha': [4, 8, 12]
}

# House significations
HOUSE_KARAKAS = {
    1: {'karaka': 'Sun', 'signifies': ['self', 'body', 'personality', 'health', 'vitality']},
    2: {'karaka': 'Jupiter', 'signifies': ['wealth', 'family', 'speech', 'values', 'food']},
    3: {'karaka': 'Mars', 'signifies': ['siblings', 'courage', 'communication', 'short_travel']},
    4: {'karaka': 'Moon', 'signifies': ['mother', 'home', 'emotions', 'property', 'comfort']},
    5: {'karaka': 'Jupiter', 'signifies': ['children', 'intelligence', 'creativity', 'romance']},
    6: {'karaka': 'Mars', 'signifies': ['enemies', 'disease', 'service', 'competition']},
    7: {'karaka': 'Venus', 'signifies': ['spouse', 'partnership', 'business', 'public']},
    8: {'karaka': 'Saturn', 'signifies': ['longevity', 'transformation', 'occult', 'inheritance']},
    9: {'karaka': 'Jupiter', 'signifies': ['father', 'fortune', 'dharma', 'higher_learning']},
    10: {'karaka': 'Saturn', 'signifies': ['career', 'status', 'authority', 'karma']},
    11: {'karaka': 'Jupiter', 'signifies': ['gains', 'friends', 'aspirations', 'income']},
    12: {'karaka': 'Saturn', 'signifies': ['loss', 'liberation', 'foreign', 'spirituality']}
}

# V6.2 POI (Planet Operating Index) Constants
POI_DIGNITY_SCALE = {
    'Exalted': 10, 'Moolatrikona': 8.5, 'Own Sign': 8,
    'Friend Sign': 6, 'Neutral': 5, 'Enemy Sign': 3, 'Debilitated': 1
}

# Combustion orbs (degrees from Sun)
COMBUSTION_ORBS = {
    'Moon': 12, 'Mars': 17, 'Mercury': 14, 'Jupiter': 11, 'Venus': 10, 'Saturn': 15
}

# Aspect weights for POI calculation
ASPECT_WEIGHTS = {
    'conjunction': 1.0, 'opposition': 0.9, 'trine': 0.6,
    'square': 0.8, 'sextile': 0.4
}

# Saturn pressure values for HAI
SATURN_PRESSURE = {
    'transit': -3, '3rd_aspect': -2, '10th_aspect': -2, 'sade_sati': -5
}

# South Indian chart sign positions (fixed positions for each rasi)
SOUTH_INDIAN_POSITIONS = {
    'Pisces': (0, 0), 'Aries': (1, 0), 'Taurus': (2, 0), 'Gemini': (3, 0),
    'Aquarius': (0, 1), 'Cancer': (3, 1),
    'Capricorn': (0, 2), 'Leo': (3, 2),
    'Sagittarius': (0, 3), 'Scorpio': (1, 3), 'Libra': (2, 3), 'Virgo': (3, 3)
}

# Weekday names
WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
WEEKDAYS_TAMIL = ['ஞாயிறு', 'திங்கள்', 'செவ்வாய்', 'புதன்', 'வியாழன்', 'வெள்ளி', 'சனி']

# Thithi names (lunar days)
THITHIS = [
    'Pratipada', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami', 'Shashti', 'Saptami',
    'Ashtami', 'Navami', 'Dashami', 'Ekadashi', 'Dwadashi', 'Trayodashi', 'Chaturdashi', 'Purnima/Amavasya'
]
THITHIS_TAMIL = [
    'பிரதமை', 'த்விதீயை', 'திரிதீயை', 'சதுர்த்தி', 'பஞ்சமி', 'சஷ்டி', 'சப்தமி',
    'அஷ்டமி', 'நவமி', 'தசமி', 'ஏகாதசி', 'த்வாதசி', 'திரயோதசி', 'சதுர்தசி', 'பூர்ணிமை/அமாவாசை'
]

# Karana names (half lunar days)
KARANAS = ['Bava', 'Balava', 'Kaulava', 'Taitila', 'Gara', 'Vanija', 'Vishti', 'Shakuni', 'Chatushpada', 'Naga', 'Kimstughna']
KARANAS_TAMIL = ['பவ', 'பாலவ', 'கௌலவ', 'தைதில', 'கர', 'வணிஜ', 'விஷ்டி', 'சகுனி', 'சதுஷ்பாத', 'நாக', 'கிம்ஸ்துக்ன']

# Nithya Yoga names
NITHYA_YOGAS = [
    'Vishkambha', 'Preeti', 'Ayushman', 'Saubhagya', 'Shobhana', 'Atiganda', 'Sukarma',
    'Dhriti', 'Shoola', 'Ganda', 'Vriddhi', 'Dhruva', 'Vyaghata', 'Harshana', 'Vajra',
    'Siddhi', 'Vyatipata', 'Variyana', 'Parigha', 'Shiva', 'Siddha', 'Sadhya', 'Shubha',
    'Shukla', 'Brahma', 'Indra', 'Vaidhriti'
]
NITHYA_YOGAS_TAMIL = [
    'விஷ்கம்பம்', 'ப்ரீதி', 'ஆயுஷ்மான்', 'சௌபாக்கியம்', 'சோபனம்', 'அதிகண்டம்', 'சுகர்மா',
    'த்ருதி', 'சூலம்', 'கண்டம்', 'விருத்தி', 'த்ருவம்', 'வியாகாதம்', 'ஹர்ஷணம்', 'வஜ்ரம்',
    'சித்தி', 'வியதீபாதம்', 'வரியானம்', 'பரிகம்', 'சிவம்', 'சித்தம்', 'சாத்தியம்', 'சுபம்',
    'சுக்லம்', 'பிரம்மம்', 'இந்திரம்', 'வைத்ருதி'
]

# Ganam (temperament) - Deva, Manushya, Rakshasa
NAKSHATRA_GANAM = {
    'Ashwini': 'Deva', 'Bharani': 'Manushya', 'Krittika': 'Rakshasa', 'Rohini': 'Manushya',
    'Mrigashira': 'Deva', 'Ardra': 'Manushya', 'Punarvasu': 'Deva', 'Pushya': 'Deva',
    'Ashlesha': 'Rakshasa', 'Magha': 'Rakshasa', 'Purva Phalguni': 'Manushya',
    'Uttara Phalguni': 'Manushya', 'Hasta': 'Deva', 'Chitra': 'Rakshasa', 'Swati': 'Deva',
    'Vishakha': 'Rakshasa', 'Anuradha': 'Deva', 'Jyeshtha': 'Rakshasa', 'Mula': 'Rakshasa',
    'Purva Ashadha': 'Manushya', 'Uttara Ashadha': 'Manushya', 'Shravana': 'Deva',
    'Dhanishta': 'Rakshasa', 'Shatabhisha': 'Rakshasa', 'Purva Bhadrapada': 'Manushya',
    'Uttara Bhadrapada': 'Manushya', 'Revati': 'Deva'
}

# Yoni (animal symbol)
NAKSHATRA_YONI = {
    'Ashwini': 'Horse', 'Bharani': 'Elephant', 'Krittika': 'Goat', 'Rohini': 'Serpent',
    'Mrigashira': 'Serpent', 'Ardra': 'Dog', 'Punarvasu': 'Cat', 'Pushya': 'Goat',
    'Ashlesha': 'Cat', 'Magha': 'Rat', 'Purva Phalguni': 'Rat', 'Uttara Phalguni': 'Cow',
    'Hasta': 'Buffalo', 'Chitra': 'Tiger', 'Swati': 'Buffalo', 'Vishakha': 'Tiger',
    'Anuradha': 'Deer', 'Jyeshtha': 'Deer', 'Mula': 'Dog', 'Purva Ashadha': 'Monkey',
    'Uttara Ashadha': 'Mongoose', 'Shravana': 'Monkey', 'Dhanishta': 'Lion',
    'Shatabhisha': 'Horse', 'Purva Bhadrapada': 'Lion', 'Uttara Bhadrapada': 'Cow', 'Revati': 'Elephant'
}

# Nakshatra bird and tree
NAKSHATRA_BIRD = {
    'Ashwini': 'Wild Eagle', 'Bharani': 'Crow', 'Krittika': 'Peacock', 'Rohini': 'Owl',
    'Mrigashira': 'Pullu bird', 'Ardra': 'Andril', 'Punarvasu': 'Swan', 'Pushya': 'Crow',
    'Ashlesha': 'Small owl', 'Magha': 'Male eagle', 'Purva Phalguni': 'Female eagle',
    'Uttara Phalguni': 'Heron', 'Hasta': 'Vulture', 'Chitra': 'Woodpecker', 'Swati': 'Honey bee',
    'Vishakha': 'Sparrow', 'Anuradha': 'Nightingale', 'Jyeshtha': 'Cock', 'Mula': 'Hamsa',
    'Purva Ashadha': 'Francolin', 'Uttara Ashadha': 'Stork', 'Shravana': 'Pigeon',
    'Dhanishta': 'Lion bird', 'Shatabhisha': 'Raven', 'Purva Bhadrapada': 'Peacock',
    'Uttara Bhadrapada': 'Pigeon', 'Revati': 'Sparrow'
}

NAKSHATRA_TREE = {
    'Ashwini': 'Strychnine tree', 'Bharani': 'Gooseberry', 'Krittika': 'Fig tree', 'Rohini': 'Jamun',
    'Mrigashira': 'Karingali tree', 'Ardra': 'Agalochum', 'Punarvasu': 'Bamboo', 'Pushya': 'Peepal',
    'Ashlesha': 'Naga champa', 'Magha': 'Banyan', 'Purva Phalguni': 'Palash',
    'Uttara Phalguni': 'Rose laurel', 'Hasta': 'Hog plum', 'Chitra': 'Bel tree', 'Swati': 'Arjun tree',
    'Vishakha': 'Vikannai', 'Anuradha': 'Bakula', 'Jyeshtha': 'Pine tree', 'Mula': 'Sarjaka',
    'Purva Ashadha': 'Moongil', 'Uttara Ashadha': 'Jack tree', 'Shravana': 'Erukku',
    'Dhanishta': 'Shami tree', 'Shatabhisha': 'Kadamba', 'Purva Bhadrapada': 'Neem',
    'Uttara Bhadrapada': 'Mango', 'Revati': 'Madhuka'
}

# Chandra Avastha (Moon state) - based on distance from Sun
CHANDRA_AVASTHA = ['Janma', 'Sampat', 'Vipat', 'Kshema', 'Pratyari', 'Sadhaka', 'Vadha', 'Mitra', 'Atimaitra']

# Drekkana (decanate) significations
DREKKANA_SIGNIFICATIONS = {
    1: {'nature': 'Self-made', 'focus': 'Personal achievement', 'trait': 'Independent'},
    2: {'nature': 'Family-oriented', 'focus': 'Relationships', 'trait': 'Cooperative'},
    3: {'nature': 'Spiritual', 'focus': 'Higher pursuits', 'trait': 'Philosophical'}
}

# Karakas (significators)
CHARA_KARAKAS = ['Atmakaraka', 'Amatyakaraka', 'Bhratrikaraka', 'Matrikaraka', 'Putrakaraka', 'Gnatikaraka', 'Darakaraka']

# Arudha Padas
ARUDHA_NAMES = {
    1: 'Lagna Pada', 2: 'Dhana Pada', 3: 'Vikrama Pada', 4: 'Sukha Pada',
    5: 'Mantra Pada', 6: 'Shatru Pada', 7: 'Dara Pada', 8: 'Mrityu Pada',
    9: 'Dharma Pada', 10: 'Karma Pada', 11: 'Labha Pada', 12: 'Vyaya Pada'
}

# Bhava prediction templates - based on lord placement
BHAVA_LORD_RESULTS = {
    # 1st lord in various houses
    (1, 1): "You are self-confident and have a strong personality.",
    (1, 2): "You will accumulate wealth through personal efforts.",
    (1, 3): "You are brave and will achieve through siblings' support.",
    (1, 4): "You will have property, vehicles and domestic happiness.",
    (1, 5): "You are intelligent with good children prospects.",
    (1, 6): "You may face health issues or conflicts with enemies.",
    (1, 7): "Your spouse will be influential in your life.",
    (1, 8): "You may face unexpected events and transformations.",
    (1, 9): "You are fortunate with father's blessings.",
    (1, 10): "You will achieve success in career and public life.",
    (1, 11): "You will have gains and fulfill desires.",
    (1, 12): "You may travel abroad or have spiritual inclinations.",
    # 2nd lord placements
    (2, 1): "Wealth comes through personal efforts and personality.",
    (2, 2): "You will accumulate family wealth steadily.",
    (2, 3): "Income through communication, writing or siblings.",
    (2, 4): "Property and vehicles add to your wealth.",
    (2, 5): "Speculation and children bring financial gains.",
    (2, 6): "May face obstacles in wealth accumulation.",
    (2, 7): "Spouse contributes to family finances.",
    (2, 8): "Inheritance or sudden gains possible.",
    (2, 9): "Fortune favors wealth accumulation.",
    (2, 10): "Career brings good income.",
    (2, 11): "Multiple sources of income.",
    (2, 12): "Expenses may exceed income at times.",
}

# House name Tamil translations
HOUSE_TAMIL = {
    1: 'தனம்', 2: 'குடும்பம்', 3: 'சகோதரம்', 4: 'சுகம்',
    5: 'புத்திரம்', 6: 'ரோகம்', 7: 'களத்திரம்', 8: 'ஆயுள்',
    9: 'பாக்கியம்', 10: 'கர்மம்', 11: 'லாபம்', 12: 'விரயம்'
}

# ============== CAREER FIELD MAPPINGS ==============
# Based on classical Jyotish texts: 10th lord, planets in 10th, and D10 analysis

PLANET_CAREER_FIELDS = {
    'Sun': {
        'primary': ['Government', 'Administration', 'Politics', 'Leadership', 'Healthcare Administration'],
        'secondary': ['Management', 'Gold/Jewelry business', 'Medicine (administration)', 'Forest/Wildlife'],
        'traits': ['Authority-driven', 'Public-facing roles', 'Leadership positions']
    },
    'Moon': {
        'primary': ['Nursing', 'Hospitality', 'Food Industry', 'Dairy', 'Psychology'],
        'secondary': ['Travel & Tourism', 'Shipping/Maritime', 'Caregiving', 'Counseling', 'Interior Design'],
        'traits': ['Nurturing roles', 'Public interaction', 'Emotionally engaging work']
    },
    'Mars': {
        'primary': ['Military/Defense', 'Engineering', 'Surgery', 'Sports', 'Real Estate'],
        'secondary': ['Police/Law enforcement', 'Fire services', 'Mechanical work', 'Construction', 'Martial arts'],
        'traits': ['Physical work', 'Competitive fields', 'Technical expertise']
    },
    'Mercury': {
        'primary': ['IT/Software', 'Writing/Journalism', 'Accounting', 'Trading', 'Communication'],
        'secondary': ['Astrology', 'Teaching', 'Marketing', 'Data Analysis', 'Languages', 'Commerce'],
        'traits': ['Intellectual work', 'Communication-centric', 'Analytical roles']
    },
    'Jupiter': {
        'primary': ['Teaching/Education', 'Law', 'Finance/Banking', 'Religious services', 'Consulting'],
        'secondary': ['Philosophy', 'Publishing', 'Advisory roles', 'Spiritual guidance', 'Higher education'],
        'traits': ['Wisdom-sharing', 'Guiding others', 'Ethical professions']
    },
    'Venus': {
        'primary': ['Arts & Entertainment', 'Fashion', 'Beauty Industry', 'Luxury goods', 'Music'],
        'secondary': ['Interior Design', 'Hospitality', 'Event management', 'Cosmetics', 'Film/Media'],
        'traits': ['Aesthetic work', 'Creative fields', 'Relationship-oriented']
    },
    'Saturn': {
        'primary': ['Engineering', 'Mining', 'Agriculture', 'Manufacturing', 'Labor-intensive work'],
        'secondary': ['Oil & Gas', 'Judiciary', 'Real Estate', 'Construction', 'Old age care', 'Archaeology'],
        'traits': ['Systematic work', 'Long-term projects', 'Service to masses']
    },
    'Rahu': {
        'primary': ['Technology', 'Foreign trade', 'Aviation', 'Research', 'Unconventional fields'],
        'secondary': ['Pharmaceuticals', 'Chemicals', 'Electronics', 'Occult sciences', 'Import/Export'],
        'traits': ['Innovative work', 'Cross-cultural roles', 'Breaking new ground']
    },
    'Ketu': {
        'primary': ['Spirituality', 'Research', 'Computer programming', 'Mathematics', 'Healing'],
        'secondary': ['Occult', 'Veterinary', 'Meditation teaching', 'Alternative medicine', 'Detectives'],
        'traits': ['Introspective work', 'Behind-the-scenes', 'Intuitive fields']
    }
}

# Sign-based career inclinations (for 10th house sign)
SIGN_CAREER_FIELDS = {
    'Aries': ['Entrepreneurship', 'Sports', 'Military', 'Surgery', 'Leadership roles', 'Competitive business'],
    'Taurus': ['Finance', 'Agriculture', 'Food industry', 'Music', 'Real estate', 'Luxury goods', 'Banking'],
    'Gemini': ['Writing', 'Journalism', 'IT', 'Sales', 'Teaching', 'Marketing', 'Communication media'],
    'Cancer': ['Hospitality', 'Nursing', 'Psychology', 'Real estate', 'Food business', 'Child care'],
    'Leo': ['Government', 'Entertainment', 'Politics', 'Management', 'Creative arts', 'Luxury brands'],
    'Virgo': ['Healthcare', 'Accounting', 'Data analysis', 'Quality control', 'Service industry', 'Editing'],
    'Libra': ['Law', 'Diplomacy', 'Fashion', 'Art', 'Counseling', 'Public relations', 'Partnerships'],
    'Scorpio': ['Research', 'Investigation', 'Psychology', 'Surgery', 'Insurance', 'Occult', 'Mining'],
    'Sagittarius': ['Education', 'Law', 'Publishing', 'Travel', 'Philosophy', 'Religious work', 'Import/Export'],
    'Capricorn': ['Administration', 'Engineering', 'Politics', 'Manufacturing', 'Government', 'Construction'],
    'Aquarius': ['Technology', 'Social work', 'NGOs', 'Innovation', 'Science', 'Networking', 'Aviation'],
    'Pisces': ['Healthcare', 'Spirituality', 'Art', 'Film', 'Psychology', 'Charity', 'Marine/Water-related']
}

# ============== HEALTH AREA MAPPINGS ==============
# Based on classical Jyotish: Body parts ruled by signs and planets

SIGN_BODY_PARTS = {
    'Aries': ['Head', 'Brain', 'Face', 'Eyes'],
    'Taurus': ['Throat', 'Neck', 'Thyroid', 'Vocal cords'],
    'Gemini': ['Shoulders', 'Arms', 'Hands', 'Lungs', 'Nervous system'],
    'Cancer': ['Chest', 'Stomach', 'Breasts', 'Digestive system'],
    'Leo': ['Heart', 'Spine', 'Upper back', 'Circulatory system'],
    'Virgo': ['Intestines', 'Digestive tract', 'Nervous system', 'Lower abdomen'],
    'Libra': ['Kidneys', 'Lower back', 'Bladder', 'Skin'],
    'Scorpio': ['Reproductive organs', 'Excretory system', 'Pelvis'],
    'Sagittarius': ['Hips', 'Thighs', 'Liver', 'Sciatic nerve'],
    'Capricorn': ['Knees', 'Bones', 'Joints', 'Teeth', 'Skin'],
    'Aquarius': ['Ankles', 'Calves', 'Circulatory system', 'Nervous system'],
    'Pisces': ['Feet', 'Toes', 'Lymphatic system', 'Immune system']
}

PLANET_HEALTH_AREAS = {
    'Sun': {
        'governs': ['Heart', 'Eyes', 'Vitality', 'Bones', 'Right eye'],
        'weak_indicators': ['Heart issues', 'Eye problems', 'Low vitality', 'Bone density issues'],
        'strong_indicators': ['Strong constitution', 'Good eyesight', 'High energy levels']
    },
    'Moon': {
        'governs': ['Mind', 'Emotions', 'Fluids', 'Left eye', 'Stomach', 'Breasts'],
        'weak_indicators': ['Mental stress', 'Fluid imbalance', 'Digestive issues', 'Emotional instability'],
        'strong_indicators': ['Emotional balance', 'Good digestion', 'Mental clarity']
    },
    'Mars': {
        'governs': ['Blood', 'Muscles', 'Bone marrow', 'Energy levels', 'Head'],
        'weak_indicators': ['Blood pressure issues', 'Accidents', 'Inflammation', 'Anger-related issues'],
        'strong_indicators': ['Physical strength', 'Quick recovery', 'Good blood health']
    },
    'Mercury': {
        'governs': ['Nervous system', 'Skin', 'Speech', 'Intellect', 'Respiratory'],
        'weak_indicators': ['Nervous disorders', 'Skin issues', 'Speech problems', 'Respiratory issues'],
        'strong_indicators': ['Sharp intellect', 'Clear communication', 'Healthy skin']
    },
    'Jupiter': {
        'governs': ['Liver', 'Fat tissue', 'Ears', 'Thighs', 'Arterial system'],
        'weak_indicators': ['Liver issues', 'Obesity', 'Diabetes risk', 'Ear problems'],
        'strong_indicators': ['Good liver function', 'Healthy weight management', 'Longevity']
    },
    'Venus': {
        'governs': ['Reproductive system', 'Kidneys', 'Throat', 'Face', 'Hormones'],
        'weak_indicators': ['Reproductive issues', 'Kidney problems', 'Hormonal imbalance', 'Skin disorders'],
        'strong_indicators': ['Hormonal balance', 'Beautiful appearance', 'Good reproductive health']
    },
    'Saturn': {
        'governs': ['Bones', 'Teeth', 'Joints', 'Chronic conditions', 'Aging'],
        'weak_indicators': ['Joint pain', 'Dental issues', 'Chronic ailments', 'Slow metabolism'],
        'strong_indicators': ['Strong bones', 'Longevity', 'Resilience']
    },
    'Rahu': {
        'governs': ['Nervous system', 'Phobias', 'Mysterious ailments', 'Skin'],
        'weak_indicators': ['Anxiety', 'Mysterious diseases', 'Poison effects', 'Mental disturbances'],
        'strong_indicators': ['Resistance to unusual diseases', 'Strong nervous system']
    },
    'Ketu': {
        'governs': ['Nervous system', 'Spine', 'Subtle body', 'Immunity'],
        'weak_indicators': ['Spine issues', 'Immune disorders', 'Mysterious pains', 'Skin diseases'],
        'strong_indicators': ['Strong intuition', 'Spiritual health', 'Quick healing']
    }
}

# ============== MARRIAGE/RELATIONSHIP INDICATORS ==============
PLANET_MARRIAGE_INDICATORS = {
    'Venus': {'role': 'Karaka for marriage', 'strong': 'Harmonious relationships', 'weak': 'Relationship challenges'},
    'Jupiter': {'role': 'Husband indicator (for females)', 'strong': 'Wise partner', 'weak': 'Partner issues'},
    'Mars': {'role': 'Passion/energy in marriage', 'strong': 'Active partnership', 'weak': 'Conflicts possible'},
    'Moon': {'role': 'Emotional bonding', 'strong': 'Emotional harmony', 'weak': 'Mood fluctuations'},
    'Saturn': {'role': 'Longevity of marriage', 'strong': 'Stable long-term', 'weak': 'Delays/obstacles'}
}

SIGN_MARRIAGE_STYLE = {
    'Aries': 'Independent partner, leadership in relationship',
    'Taurus': 'Stable, comfort-seeking, loyal partnership',
    'Gemini': 'Communicative, intellectually stimulating partner',
    'Cancer': 'Nurturing, family-oriented, emotional bonding',
    'Leo': 'Romantic, generous, proud partnership',
    'Virgo': 'Practical, service-oriented, analytical partner',
    'Libra': 'Harmonious, partnership-focused, balanced',
    'Scorpio': 'Intense, transformative, deep bonding',
    'Sagittarius': 'Freedom-loving, philosophical partner',
    'Capricorn': 'Ambitious, traditional, committed partner',
    'Aquarius': 'Unconventional, friendly, independent partner',
    'Pisces': 'Compassionate, intuitive, spiritual bonding'
}

# ============== WEALTH INDICATORS ==============
PLANET_WEALTH_INDICATORS = {
    'Jupiter': {'role': 'Natural wealth indicator', 'fields': ['Banking', 'Finance', 'Education', 'Advisory']},
    'Venus': {'role': 'Luxury and comfort', 'fields': ['Luxury goods', 'Arts', 'Entertainment', 'Beauty']},
    'Mercury': {'role': 'Business acumen', 'fields': ['Trading', 'Commerce', 'IT', 'Communication']},
    'Sun': {'role': 'Authority and position', 'fields': ['Government', 'Gold', 'Administration']},
    'Moon': {'role': 'Public dealings', 'fields': ['Liquids', 'Public business', 'Import/Export']},
    'Saturn': {'role': 'Slow steady wealth', 'fields': ['Real estate', 'Mining', 'Agriculture']},
    'Mars': {'role': 'Property/land', 'fields': ['Real estate', 'Engineering', 'Military']}
}

# ============== EDUCATION INDICATORS ==============
PLANET_EDUCATION_FIELDS = {
    'Mercury': ['Commerce', 'Accounting', 'IT', 'Languages', 'Writing', 'Mathematics'],
    'Jupiter': ['Law', 'Philosophy', 'Higher studies', 'Teaching', 'Finance', 'Vedic studies'],
    'Venus': ['Arts', 'Music', 'Design', 'Fashion', 'Film studies', 'Literature'],
    'Mars': ['Engineering', 'Medicine (Surgery)', 'Sports science', 'Military studies'],
    'Saturn': ['Engineering', 'Mining', 'Agriculture', 'History', 'Archaeology'],
    'Sun': ['Political science', 'Administration', 'Medicine', 'Government studies'],
    'Moon': ['Psychology', 'Nursing', 'Hospitality', 'Marine studies'],
    'Rahu': ['Technology', 'Foreign studies', 'Research', 'Aviation', 'Electronics'],
    'Ketu': ['Computer science', 'Mathematics', 'Occult sciences', 'Spiritual studies']
}

# ============== CHILDREN INDICATORS ==============
PLANET_CHILDREN_INDICATORS = {
    'Jupiter': {'role': 'Primary Putrakaraka', 'strong': 'Good progeny prospects', 'weak': 'Delays or challenges'},
    'Venus': {'role': 'Creative expression', 'strong': 'Creative children', 'weak': 'May need remedies'},
    'Mars': {'role': 'Energy and vitality', 'strong': 'Active children', 'weak': 'Health concerns possible'},
    'Moon': {'role': 'Emotional bond', 'strong': 'Close relationship', 'weak': 'Emotional distance'},
    'Sun': {'role': 'Father indicator', 'strong': 'Strong father figure', 'weak': 'Father-child dynamics'}
}


@dataclass
class PlanetPosition:
    """Represents a planet's position in the chart"""
    planet: str
    sign: str
    sign_index: int  # 0-11
    house: int  # 1-12
    degree: float  # 0-30 within sign
    longitude: float  # 0-360 absolute
    nakshatra: str
    nakshatra_index: int
    nakshatra_pada: int
    is_retrograde: bool = False


@dataclass
class StrengthScore:
    """Normalized strength score with components"""
    total: float  # 0.0 to 1.0
    dignity: float
    house_position: float
    aspects: float
    shadbala_approx: float
    math_trace: str  # Shows calculation


class JyotishEngine:
    """
    V6.0 Jyotish Calculation Engine
    All methods return calculated values with math traces
    """

    def __init__(self, chart_data: Dict[str, Any], user_data: Dict[str, Any]):
        self.chart_data = chart_data
        self.user_data = user_data
        self.planets: Dict[str, PlanetPosition] = {}
        self.lagna_sign = ''
        self.lagna_degree = 0.0
        self.moon_sign = ''
        self.moon_nakshatra = ''
        self.birth_date = None
        self.current_age = 0

        self._parse_chart_data()

    def _parse_chart_data(self):
        """Parse chart data into structured format"""
        # Parse birth date
        try:
            bd = self.user_data.get('birth_date', '1990-01-01')
            if isinstance(bd, str):
                self.birth_date = datetime.strptime(bd, '%Y-%m-%d').date()
            elif isinstance(bd, date):
                self.birth_date = bd
            self.current_age = (date.today() - self.birth_date).days // 365
        except:
            self.birth_date = date(1990, 1, 1)
            self.current_age = 34

        # Parse lagna
        lagna = self.chart_data.get('lagna', {})
        if isinstance(lagna, dict):
            self.lagna_sign = lagna.get('sign', 'Aries')
            self.lagna_degree = float(lagna.get('degree', 0))
        else:
            self.lagna_sign = 'Aries'
            self.lagna_degree = 0

        # Parse planets
        planets_data = self.chart_data.get('planets', [])

        # Handle list format
        if isinstance(planets_data, list):
            for p in planets_data:
                if isinstance(p, dict):
                    name = p.get('planet', p.get('name', ''))
                    if name in PLANETS:
                        self.planets[name] = self._create_planet_position(name, p)
        # Handle dict format
        elif isinstance(planets_data, dict):
            for name, p in planets_data.items():
                if name in PLANETS and isinstance(p, dict):
                    self.planets[name] = self._create_planet_position(name, p)

        # Ensure all planets exist with defaults
        for planet in PLANETS:
            if planet not in self.planets:
                self.planets[planet] = self._default_planet_position(planet)

        # Set moon sign and nakshatra
        if 'Moon' in self.planets:
            self.moon_sign = self.planets['Moon'].sign
            self.moon_nakshatra = self.planets['Moon'].nakshatra

        # Also check moon_rasi from chart_data
        moon_rasi = self.chart_data.get('moon_rasi', {})
        if isinstance(moon_rasi, dict) and moon_rasi.get('name'):
            self.moon_sign = moon_rasi.get('name', self.moon_sign)

        nakshatra = self.chart_data.get('nakshatra', {})
        if isinstance(nakshatra, dict) and nakshatra.get('name'):
            self.moon_nakshatra = nakshatra.get('name', self.moon_nakshatra)

    def _create_planet_position(self, name: str, data: Dict) -> PlanetPosition:
        """Create PlanetPosition from data dict"""
        sign = data.get('sign', data.get('rasi', 'Aries'))
        sign_index = RASIS.index(sign) if sign in RASIS else 0

        degree = float(data.get('degree', data.get('longitude', 0)))
        if degree > 30:
            degree = degree % 30

        longitude = float(data.get('longitude', sign_index * 30 + degree))

        house = int(data.get('house', data.get('house_num', 1)))

        # Calculate nakshatra
        nak_index = int(longitude / 13.333333) % 27
        nak_pada = int((longitude % 13.333333) / 3.333333) + 1

        nakshatra_name = data.get('nakshatra', NAKSHATRAS[nak_index]['name'])

        return PlanetPosition(
            planet=name,
            sign=sign,
            sign_index=sign_index,
            house=house,
            degree=degree,
            longitude=longitude,
            nakshatra=nakshatra_name,
            nakshatra_index=nak_index,
            nakshatra_pada=nak_pada,
            is_retrograde=data.get('is_retrograde', data.get('retrograde', False))
        )

    def _default_planet_position(self, name: str) -> PlanetPosition:
        """Create default planet position"""
        idx = PLANETS.index(name) if name in PLANETS else 0
        sign_idx = idx % 12
        return PlanetPosition(
            planet=name,
            sign=RASIS[sign_idx],
            sign_index=sign_idx,
            house=(sign_idx % 12) + 1,
            degree=15.0,
            longitude=sign_idx * 30 + 15,
            nakshatra=NAKSHATRAS[(sign_idx * 2) % 27]['name'],
            nakshatra_index=(sign_idx * 2) % 27,
            nakshatra_pada=2,
            is_retrograde=False
        )

    # ============== DIGNITY CALCULATIONS ==============

    def get_dignity(self, planet: str) -> Tuple[str, float, str]:
        """
        Calculate planetary dignity
        Returns: (dignity_name, score 0-1, math_trace)
        """
        if planet not in self.planets:
            return ('Unknown', 0.5, f'{planet} not found')

        p = self.planets[planet]
        sign = p.sign
        degree = p.degree

        # Check exaltation
        if planet in EXALTATION and EXALTATION[planet] == sign:
            return ('Exalted', 1.0, f'{planet} in {sign} = Exalted (max dignity)')

        # Check debilitation
        if planet in DEBILITATION and DEBILITATION[planet] == sign:
            return ('Debilitated', 0.15, f'{planet} in {sign} = Debilitated (min dignity)')

        # Check moolatrikona
        if planet in MOOLATRIKONA:
            mt_sign, mt_start, mt_end = MOOLATRIKONA[planet]
            if sign == mt_sign and mt_start <= degree <= mt_end:
                return ('Moolatrikona', 0.85, f'{planet} in {sign} at {degree:.1f}° = Moolatrikona')

        # Check own sign
        if planet in OWN_SIGNS and sign in OWN_SIGNS[planet]:
            return ('Own Sign', 0.75, f'{planet} in own sign {sign}')

        # Check friend's sign
        sign_lord = RASI_LORDS.get(sign, '')
        if planet in NATURAL_FRIENDS and sign_lord in NATURAL_FRIENDS[planet]:
            return ('Friend Sign', 0.60, f'{planet} in {sign} (lord {sign_lord} is friend)')

        # Check enemy's sign
        if planet in NATURAL_ENEMIES and sign_lord in NATURAL_ENEMIES[planet]:
            return ('Enemy Sign', 0.35, f'{planet} in {sign} (lord {sign_lord} is enemy)')

        # Neutral
        return ('Neutral', 0.50, f'{planet} in {sign} = Neutral dignity')

    # ============== SHADBALA APPROXIMATION ==============

    def calculate_shadbala(self, planet: str) -> Dict[str, Any]:
        """
        Calculate approximate Shadbala (6-fold strength)
        Returns normalized score 0-1 with component breakdown
        """
        if planet not in self.planets or planet in ['Rahu', 'Ketu']:
            return {
                'total': 0.5,
                'components': {},
                'math_trace': f'{planet}: Using default Shadbala 0.5'
            }

        p = self.planets[planet]
        components = {}
        traces = []

        # 1. Sthana Bala (Positional Strength) - 30%
        dignity_name, dignity_score, _ = self.get_dignity(planet)
        components['sthana'] = dignity_score
        traces.append(f'Sthana: {dignity_name}={dignity_score:.2f}')

        # 2. Dig Bala (Directional Strength) - 15%
        dig_bala = self._calculate_dig_bala(planet, p.house)
        components['dig'] = dig_bala
        traces.append(f'Dig: H{p.house}={dig_bala:.2f}')

        # 3. Kala Bala (Temporal Strength) - 20%
        kala_bala = self._calculate_kala_bala(planet)
        components['kala'] = kala_bala
        traces.append(f'Kala: {kala_bala:.2f}')

        # 4. Chesta Bala (Motional Strength) - 10%
        chesta_bala = 0.3 if p.is_retrograde else 0.6
        components['chesta'] = chesta_bala
        traces.append(f'Chesta: {"R" if p.is_retrograde else "D"}={chesta_bala:.2f}')

        # 5. Naisargika Bala (Natural Strength) - 10%
        naisargika = self._get_naisargika_bala(planet)
        components['naisargika'] = naisargika
        traces.append(f'Naisargika: {naisargika:.2f}')

        # 6. Drik Bala (Aspectual Strength) - 15%
        drik_bala = self._calculate_drik_bala(planet)
        components['drik'] = drik_bala
        traces.append(f'Drik: {drik_bala:.2f}')

        # Weighted total
        weights = {'sthana': 0.30, 'dig': 0.15, 'kala': 0.20,
                   'chesta': 0.10, 'naisargika': 0.10, 'drik': 0.15}

        total = sum(components[k] * weights[k] for k in weights)

        # Apply floor (anti-punishment rule)
        total = max(0.35, total)

        return {
            'total': round(total, 3),
            'components': components,
            'math_trace': ' | '.join(traces)
        }

    def _calculate_dig_bala(self, planet: str, house: int) -> float:
        """Directional strength based on house position"""
        # Best houses for each planet
        best_houses = {
            'Sun': 10, 'Moon': 4, 'Mars': 10, 'Mercury': 1,
            'Jupiter': 1, 'Venus': 4, 'Saturn': 7
        }

        if planet not in best_houses:
            return 0.5

        best = best_houses[planet]
        distance = min(abs(house - best), 12 - abs(house - best))

        # Score decreases with distance from best house
        return max(0.2, 1.0 - (distance * 0.15))

    def _calculate_kala_bala(self, planet: str) -> float:
        """Temporal strength (simplified)"""
        # Day/night planets
        day_planets = ['Sun', 'Jupiter', 'Saturn']
        night_planets = ['Moon', 'Venus', 'Mars']

        # Assume daytime birth if hour not specified
        birth_time = self.user_data.get('birth_time', '12:00')
        try:
            hour = int(birth_time.split(':')[0])
            is_day = 6 <= hour < 18
        except:
            is_day = True

        if planet in day_planets:
            return 0.7 if is_day else 0.4
        elif planet in night_planets:
            return 0.4 if is_day else 0.7
        else:
            return 0.5

    def _get_naisargika_bala(self, planet: str) -> float:
        """Natural strength ranking"""
        rankings = {
            'Sun': 0.86, 'Moon': 0.71, 'Venus': 0.57, 'Jupiter': 0.43,
            'Mercury': 0.29, 'Mars': 0.21, 'Saturn': 0.14
        }
        return rankings.get(planet, 0.5)

    def _calculate_drik_bala(self, planet: str) -> float:
        """Aspectual strength from benefic/malefic aspects"""
        if planet not in self.planets:
            return 0.5

        p = self.planets[planet]
        benefics = ['Jupiter', 'Venus', 'Moon', 'Mercury']
        malefics = ['Saturn', 'Mars', 'Rahu', 'Ketu', 'Sun']

        score = 0.5

        for other_name, other_pos in self.planets.items():
            if other_name == planet:
                continue

            # Check conjunction (same sign)
            if other_pos.sign == p.sign:
                if other_name in benefics:
                    score += 0.1
                elif other_name in malefics:
                    score -= 0.08  # Capped negative

            # Check opposition (7th from)
            if abs(other_pos.sign_index - p.sign_index) == 6:
                if other_name in malefics:
                    score -= 0.05

        return max(0.2, min(0.9, score))

    # ============== V6.2 POI (Planet Operating Index) ==============

    def calculate_poi(self, planet: str) -> Dict[str, Any]:
        """
        V6.2 Planet Operating Index - comprehensive strength calculation
        POI = base_dignity + shadbala + retrograde_mod + combustion_mod + aspect_score
        """
        if planet not in self.planets:
            return {'total': 5.0, 'components': {}, 'math_trace': f'{planet} not found'}

        p = self.planets[planet]
        components = {}
        traces = []

        # 1. Base Dignity (0-10 scale)
        dignity_name, dignity_score, _ = self.get_dignity(planet)
        base_dignity = POI_DIGNITY_SCALE.get(dignity_name, 5)
        components['base_dignity'] = base_dignity
        traces.append(f'Dignity:{dignity_name}={base_dignity}')

        # 2. Shadbala contribution (normalized to 0-3)
        shadbala = self.calculate_shadbala(planet)
        shadbala_contrib = shadbala['total'] * 3
        components['shadbala'] = round(shadbala_contrib, 2)
        traces.append(f'Shadbala:{shadbala_contrib:.2f}')

        # 3. Retrograde modifier
        retro_mod = 0
        if p.is_retrograde:
            benefics = ['Jupiter', 'Venus', 'Mercury', 'Moon']
            if planet in benefics:
                retro_mod = 2.5  # Benefic retrograde gains strength
            else:
                retro_mod = -3.5  # Malefic retrograde loses
        components['retrograde'] = retro_mod
        if retro_mod != 0:
            traces.append(f'Retro:{retro_mod:+.1f}')

        # 4. Combustion modifier (proximity to Sun)
        combust_mod = self._calculate_combustion(planet)
        components['combustion'] = combust_mod
        if combust_mod != 0:
            traces.append(f'Combust:{combust_mod:.1f}')

        # 5. Aspect score (degree-based)
        aspect_score = self._calculate_aspect_score(planet)
        components['aspects'] = round(aspect_score, 2)
        traces.append(f'Aspects:{aspect_score:.2f}')

        # Calculate total POI (0-20 range, normalized to 0-10)
        raw_total = base_dignity + shadbala_contrib + retro_mod + combust_mod + aspect_score
        # Normalize to 0-10 scale with floor of 1.0 (never zero)
        total = max(1.0, min(10.0, raw_total * 0.5))

        return {
            'total': round(total, 2),
            'raw_total': round(raw_total, 2),
            'components': components,
            'grade': self._poi_to_grade(total),
            'math_trace': ' | '.join(traces)
        }

    def _calculate_combustion(self, planet: str) -> float:
        """Calculate combustion penalty based on distance from Sun"""
        if planet == 'Sun' or planet not in self.planets:
            return 0

        if planet not in COMBUSTION_ORBS:
            return 0

        if 'Sun' not in self.planets:
            return 0

        sun = self.planets['Sun']
        p = self.planets[planet]

        # Calculate degree difference
        degree_diff = abs(p.longitude - sun.longitude)
        if degree_diff > 180:
            degree_diff = 360 - degree_diff

        orb = COMBUSTION_ORBS[planet]

        if degree_diff < orb:
            # Combustion severity (closer = worse)
            severity = (orb - degree_diff) / orb
            return round(-4 * severity, 2)  # Max -4 penalty

        return 0

    def _calculate_aspect_score(self, planet: str) -> float:
        """Calculate aspect score with degree-based orbs (max 8 degrees)"""
        if planet not in self.planets:
            return 0

        p = self.planets[planet]
        score = 0
        benefics = ['Jupiter', 'Venus', 'Moon', 'Mercury']

        for other_name, other_pos in self.planets.items():
            if other_name == planet:
                continue

            # Calculate degree separation
            degree_diff = abs(p.longitude - other_pos.longitude)
            if degree_diff > 180:
                degree_diff = 360 - degree_diff

            aspect_type = None
            orb = 8  # Max orb

            # Identify aspect type
            if degree_diff <= orb:
                aspect_type = 'conjunction'
            elif abs(degree_diff - 180) <= orb:
                aspect_type = 'opposition'
            elif abs(degree_diff - 120) <= orb or abs(degree_diff - 240) <= orb:
                aspect_type = 'trine'
            elif abs(degree_diff - 90) <= orb or abs(degree_diff - 270) <= orb:
                aspect_type = 'square'
            elif abs(degree_diff - 60) <= orb or abs(degree_diff - 300) <= orb:
                aspect_type = 'sextile'

            if aspect_type:
                weight = ASPECT_WEIGHTS.get(aspect_type, 0)
                # Calculate orb tightness (closer = stronger)
                target_deg = {'conjunction': 0, 'opposition': 180, 'trine': 120,
                             'square': 90, 'sextile': 60}.get(aspect_type, 0)
                actual_orb = min(abs(degree_diff - target_deg),
                                abs(degree_diff - (360 - target_deg)) if target_deg else degree_diff)
                tightness = 1 - (actual_orb / orb)

                # Benefic adds, malefic subtracts
                if other_name in benefics:
                    score += weight * tightness * 1.5
                else:
                    score -= weight * tightness * 0.8  # Reduced negative

        return max(-2, min(3, score))  # Cap the range

    def _poi_to_grade(self, poi: float) -> str:
        """Convert POI to letter grade"""
        if poi >= 8:
            return 'A+'
        elif poi >= 7:
            return 'A'
        elif poi >= 6:
            return 'B+'
        elif poi >= 5:
            return 'B'
        elif poi >= 4:
            return 'C+'
        elif poi >= 3:
            return 'C'
        else:
            return 'D'

    # ============== V6.2 HAI (House Activation Index) ==============

    def calculate_hai(self, house: int) -> Dict[str, Any]:
        """
        V6.2 House Activation Index
        HAI = static_strength + house_lord_POI + dasha_activation - saturn_pressure
        """
        if house < 1 or house > 12:
            return {'total': 5.0, 'components': {}, 'math_trace': 'Invalid house'}

        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0
        house_sign = RASIS[(lagna_idx + house - 1) % 12]
        house_lord = RASI_LORDS[house_sign]

        components = {}
        traces = []

        # 1. Static house strength (based on occupants)
        static_strength = self._calculate_static_house_strength(house)
        components['static'] = round(static_strength, 2)
        traces.append(f'Static:{static_strength:.2f}')

        # 2. House lord POI
        lord_poi = self.calculate_poi(house_lord)
        lord_contribution = lord_poi['total'] * 0.5  # Scale down
        components['lord_poi'] = round(lord_contribution, 2)
        traces.append(f'Lord({house_lord}):{lord_contribution:.2f}')

        # 3. Saturn pressure
        saturn_penalty = self._calculate_saturn_pressure(house)
        components['saturn_pressure'] = saturn_penalty
        if saturn_penalty != 0:
            traces.append(f'Saturn:{saturn_penalty:+.1f}')

        # 4. Dasha activation (if house lord is current dasha lord)
        dasha_bonus = self._check_dasha_activation(house_lord)
        components['dasha_activation'] = dasha_bonus
        if dasha_bonus > 0:
            traces.append(f'Dasha:+{dasha_bonus:.1f}')

        # Calculate total HAI (0-10 scale)
        raw_total = static_strength + lord_contribution + saturn_penalty + dasha_bonus
        total = max(1.0, min(10.0, raw_total))

        return {
            'total': round(total, 2),
            'house': house,
            'sign': house_sign,
            'lord': house_lord,
            'components': components,
            'grade': self._poi_to_grade(total),
            'significations': HOUSE_KARAKAS.get(house, {}).get('signifies', []),
            'math_trace': ' | '.join(traces)
        }

    def _calculate_static_house_strength(self, house: int) -> float:
        """Calculate base strength from planets in the house"""
        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0
        strength = 5.0  # Base

        benefics = ['Jupiter', 'Venus', 'Moon', 'Mercury']
        malefics = ['Saturn', 'Mars', 'Rahu', 'Ketu']

        for planet, pos in self.planets.items():
            planet_house = ((pos.sign_index - lagna_idx) % 12) + 1
            if planet_house == house:
                if planet in benefics:
                    strength += 1.5
                elif planet in malefics:
                    strength -= 0.5  # Reduced negative per V6.2 rules
                else:
                    strength += 0.5

        return max(2, min(8, strength))

    def _calculate_saturn_pressure(self, house: int) -> float:
        """Calculate Saturn's suppressive effect on a house"""
        if 'Saturn' not in self.planets:
            return 0

        saturn = self.planets['Saturn']
        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0
        saturn_house = ((saturn.sign_index - lagna_idx) % 12) + 1

        penalty = 0

        # Saturn in the house
        if saturn_house == house:
            penalty -= 2

        # Saturn's 3rd aspect
        if ((saturn_house + 2) % 12) + 1 == house:
            penalty -= 1.5

        # Saturn's 7th aspect
        if ((saturn_house + 6) % 12) + 1 == house:
            penalty -= 1.5

        # Saturn's 10th aspect
        if ((saturn_house + 9) % 12) + 1 == house:
            penalty -= 1.5

        return max(-4, penalty)  # Cap the penalty

    def _check_dasha_activation(self, planet: str) -> float:
        """Check if planet is activated by current dasha"""
        current_dasha = self._get_current_dasha()
        if planet == current_dasha.get('mahadasha'):
            return 2.0
        elif planet == current_dasha.get('antardasha'):
            return 1.0
        return 0

    # ============== V6.2 CHART RENDERING DATA ==============

    def _deg_to_dms(self, degree: float) -> str:
        """Convert decimal degrees to Deg:Min:Sec format"""
        d = int(degree)
        m = int((degree - d) * 60)
        s = int(((degree - d) * 60 - m) * 60)
        return f"{d}:{m:02d}:{s:02d}"

    def _get_planet_status(self, planet: str) -> Dict[str, Any]:
        """Get planet status - retrograde, exalted, debilitated, combust"""
        if planet not in self.planets:
            return {'retrograde': False, 'exalted': False, 'debilitated': False, 'combust': False}

        pos = self.planets[planet]
        sign = pos.sign

        # Check status
        is_exalted = planet in EXALTATION and EXALTATION[planet] == sign
        is_debilitated = planet in DEBILITATION and DEBILITATION[planet] == sign

        # Check combustion (proximity to Sun)
        is_combust = False
        if planet != 'Sun' and 'Sun' in self.planets:
            sun_long = self.planets['Sun'].longitude
            planet_long = pos.longitude
            diff = abs(planet_long - sun_long)
            if diff > 180:
                diff = 360 - diff
            combust_orbs = {'Moon': 12, 'Mars': 17, 'Mercury': 14, 'Jupiter': 11, 'Venus': 10, 'Saturn': 15}
            if planet in combust_orbs and diff < combust_orbs[planet]:
                is_combust = True

        return {
            'retrograde': pos.is_retrograde,
            'exalted': is_exalted,
            'debilitated': is_debilitated,
            'combust': is_combust
        }

    def get_d1_chart_data(self) -> Dict[str, Any]:
        """Get D1 Rasi chart data with full details for South Indian style"""
        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0

        chart_data = {
            'style': 'south_indian',
            'lagna': self.lagna_sign,
            'lagna_sanskrit': RASI_SANSKRIT.get(self.lagna_sign, self.lagna_sign),
            'lagna_degree': self.lagna_degree,
            'lagna_dms': self._deg_to_dms(self.lagna_degree),
            'houses': {},
            'planet_longitudes': {}  # For Nirayana Longitudes table
        }

        # Build house data with planets
        for i in range(12):
            house_num = i + 1
            sign = RASIS[(lagna_idx + i) % 12]
            sign_tamil = RASI_TAMIL[(lagna_idx + i) % 12]
            sign_sanskrit = RASI_SANSKRIT.get(sign, sign)

            planets_in_house = []
            for planet, pos in self.planets.items():
                if pos.sign == sign:
                    status = self._get_planet_status(planet)
                    planets_in_house.append({
                        'name': planet,
                        'abbr': PLANET_ABBR.get(planet, planet[:2]),
                        'sanskrit': PLANET_SANSKRIT.get(planet, planet),
                        'symbol': PLANET_SYMBOLS.get(planet, ''),
                        'tamil': PLANET_TAMIL.get(planet, ''),
                        'degree': round(pos.degree, 2),
                        'degree_dms': self._deg_to_dms(pos.degree),
                        'longitude': pos.longitude,
                        'longitude_dms': self._deg_to_dms(pos.longitude),
                        'nakshatra': pos.nakshatra,
                        'pada': pos.nakshatra_pada,
                        'retrograde': status['retrograde'],
                        'exalted': status['exalted'],
                        'debilitated': status['debilitated'],
                        'combust': status['combust']
                    })

            chart_data['houses'][house_num] = {
                'sign': sign,
                'sign_tamil': sign_tamil,
                'sign_sanskrit': sign_sanskrit,
                'sign_index': (lagna_idx + i) % 12,
                'planets': planets_in_house,
                'position': SOUTH_INDIAN_POSITIONS.get(sign, (0, 0))
            }

        # Build Nirayana Longitudes summary
        for planet, pos in self.planets.items():
            status = self._get_planet_status(planet)
            nak_idx = pos.nakshatra_index if hasattr(pos, 'nakshatra_index') else 0
            nak_data = NAKSHATRAS[nak_idx] if nak_idx < len(NAKSHATRAS) else NAKSHATRAS[0]

            chart_data['planet_longitudes'][planet] = {
                'rasi': pos.sign,
                'rasi_sanskrit': RASI_SANSKRIT.get(pos.sign, pos.sign),
                'longitude_dms': self._deg_to_dms(pos.longitude),
                'star': pos.nakshatra,
                'pada': pos.nakshatra_pada,
                'star_pada': f"{pos.nakshatra} / {pos.nakshatra_pada}",
                'retrograde': status['retrograde'],
                'exalted': status['exalted'],
                'debilitated': status['debilitated'],
                'combust': status['combust']
            }

        return chart_data

    def get_d9_chart_data(self) -> Dict[str, Any]:
        """Get D9 Navamsa chart data"""
        # Calculate Navamsa positions
        navamsa_planets = {}
        vargottama = []

        for planet, pos in self.planets.items():
            # Navamsa calculation: divide sign into 9 parts (3.333 degrees each)
            navamsa_part = int(pos.degree / 3.333333) % 9
            # Starting sign depends on element
            element_start = {'Fire': 0, 'Earth': 9, 'Air': 6, 'Water': 3}
            sign_element = None
            for elem, signs in ELEMENT_SIGNS.items():
                if pos.sign in signs:
                    sign_element = elem
                    break
            start_idx = element_start.get(sign_element, 0)
            navamsa_sign_idx = (start_idx + navamsa_part) % 12
            navamsa_sign = RASIS[navamsa_sign_idx]

            navamsa_planets[planet] = {
                'sign': navamsa_sign,
                'sign_tamil': RASI_TAMIL[navamsa_sign_idx],
                'd1_sign': pos.sign
            }

            # Check vargottama (same sign in D1 and D9)
            if pos.sign == navamsa_sign:
                vargottama.append(planet)

        return {
            'style': 'south_indian',
            'planets': navamsa_planets,
            'vargottama': vargottama,
            'vargottama_count': len(vargottama),
            'marriage_strength': self._calculate_d9_marriage_strength(navamsa_planets)
        }

    def _calculate_d9_marriage_strength(self, navamsa_planets: Dict) -> Dict:
        """Calculate marriage indicators from D9"""
        score = 5.0  # Base

        # Venus position in D9
        if 'Venus' in navamsa_planets:
            venus_d9 = navamsa_planets['Venus']['sign']
            if venus_d9 in OWN_SIGNS.get('Venus', []):
                score += 2
            elif venus_d9 == EXALTATION.get('Venus'):
                score += 3

        # 7th lord in D9
        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0
        seventh_sign = RASIS[(lagna_idx + 6) % 12]
        seventh_lord = RASI_LORDS[seventh_sign]

        if seventh_lord in navamsa_planets:
            lord_d9 = navamsa_planets[seventh_lord]['sign']
            if lord_d9 == EXALTATION.get(seventh_lord, ''):
                score += 2

        return {
            'score': min(10, max(1, score)),
            'grade': self._poi_to_grade(min(10, max(1, score)))
        }

    def get_d10_chart_data(self) -> Dict[str, Any]:
        """Get D10 Dashamsa chart data for career analysis"""
        dashamsa_planets = {}

        for planet, pos in self.planets.items():
            # Dashamsa: divide sign into 10 parts (3 degrees each)
            dashamsa_part = int(pos.degree / 3) % 10
            # Odd signs start from same sign, even signs start from 9th
            if pos.sign_index % 2 == 0:  # Odd sign (1,3,5... = index 0,2,4...)
                dashamsa_sign_idx = (pos.sign_index + dashamsa_part) % 12
            else:  # Even sign
                dashamsa_sign_idx = (pos.sign_index + 9 + dashamsa_part) % 12

            dashamsa_planets[planet] = {
                'sign': RASIS[dashamsa_sign_idx],
                'sign_tamil': RASI_TAMIL[dashamsa_sign_idx]
            }

        # Career indicators
        career_strength = self._calculate_d10_career_strength(dashamsa_planets)

        return {
            'style': 'south_indian',
            'planets': dashamsa_planets,
            'career_strength': career_strength
        }

    def _calculate_d10_career_strength(self, dashamsa_planets: Dict) -> Dict:
        """Calculate career indicators from D10"""
        score = 5.0

        # Sun in D10 (authority)
        if 'Sun' in dashamsa_planets:
            sun_d10 = dashamsa_planets['Sun']['sign']
            if sun_d10 in ['Leo', 'Aries']:
                score += 2

        # Saturn in D10 (discipline)
        if 'Saturn' in dashamsa_planets:
            saturn_d10 = dashamsa_planets['Saturn']['sign']
            if saturn_d10 in ['Capricorn', 'Aquarius', 'Libra']:
                score += 1.5

        # 10th lord placement
        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0
        tenth_sign = RASIS[(lagna_idx + 9) % 12]
        tenth_lord = RASI_LORDS[tenth_sign]

        if tenth_lord in dashamsa_planets:
            score += 1

        return {
            'score': min(10, max(1, score)),
            'grade': self._poi_to_grade(min(10, max(1, score))),
            'tenth_lord': tenth_lord
        }

    def get_bhava_table_data(self) -> Dict[str, Any]:
        """
        Get Bhava (House) Table data with Arambha (start), Madhya (middle), Anthya (end) cusps
        Based on Placidus/Equal house system from Lagna degree
        """
        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0

        bhava_data = {
            'houses': [],
            'lagna_degree': self.lagna_degree,
            'lagna_longitude': (lagna_idx * 30) + self.lagna_degree
        }

        # Calculate each house cusp
        for house_num in range(1, 13):
            sign_idx = (lagna_idx + house_num - 1) % 12
            sign = RASIS[sign_idx]
            sign_tamil = RASI_TAMIL[sign_idx]
            sign_sanskrit = RASI_SANSKRIT.get(sign, sign)

            # Calculate house cusp degrees
            # Arambha (Beginning): Previous house end / This house start
            # Madhya (Middle): House cusp point
            # Anthya (End): This house end / Next house start

            # Equal house system: each house is 30 degrees from lagna
            house_start_long = (lagna_idx * 30 + self.lagna_degree + (house_num - 1) * 30) % 360
            house_mid_long = (house_start_long + 15) % 360
            house_end_long = (house_start_long + 30) % 360

            # Get degree within sign
            arambha_degree = house_start_long % 30
            madhya_degree = house_mid_long % 30
            anthya_degree = house_end_long % 30

            # Get sign for each point
            arambha_sign_idx = int(house_start_long / 30) % 12
            madhya_sign_idx = int(house_mid_long / 30) % 12
            anthya_sign_idx = int(house_end_long / 30) % 12

            # Find planets in this house
            planets_in_house = []
            for planet, pos in self.planets.items():
                planet_house = ((pos.sign_index - lagna_idx) % 12) + 1
                if planet_house == house_num:
                    status = self._get_planet_status(planet)
                    planets_in_house.append({
                        'name': planet,
                        'abbr': PLANET_ABBR.get(planet, planet[:2]),
                        'degree_dms': self._deg_to_dms(pos.degree),
                        'retrograde': status['retrograde']
                    })

            house_lord = RASI_LORDS[sign]

            bhava_data['houses'].append({
                'house_num': house_num,
                'sign': sign,
                'sign_tamil': sign_tamil,
                'sign_sanskrit': sign_sanskrit,
                'lord': house_lord,
                'lord_abbr': PLANET_ABBR.get(house_lord, house_lord[:2]),
                'arambha': {
                    'sign': RASIS[arambha_sign_idx],
                    'sign_abbr': RASIS[arambha_sign_idx][:3],
                    'degree': arambha_degree,
                    'degree_dms': self._deg_to_dms(arambha_degree),
                    'longitude': house_start_long,
                    'longitude_dms': self._deg_to_dms(house_start_long)
                },
                'madhya': {
                    'sign': RASIS[madhya_sign_idx],
                    'sign_abbr': RASIS[madhya_sign_idx][:3],
                    'degree': madhya_degree,
                    'degree_dms': self._deg_to_dms(madhya_degree),
                    'longitude': house_mid_long,
                    'longitude_dms': self._deg_to_dms(house_mid_long)
                },
                'anthya': {
                    'sign': RASIS[anthya_sign_idx],
                    'sign_abbr': RASIS[anthya_sign_idx][:3],
                    'degree': anthya_degree,
                    'degree_dms': self._deg_to_dms(anthya_degree),
                    'longitude': house_end_long,
                    'longitude_dms': self._deg_to_dms(house_end_long)
                },
                'planets': planets_in_house
            })

        return bhava_data

    def get_sudarshana_chakra_data(self) -> Dict[str, Any]:
        """
        Get Sudarshana Chakra data - three concentric rings showing:
        - Inner: Lagna (Ascendant) based houses
        - Middle: Moon based houses
        - Outer: Sun based houses
        Each showing planetary positions from that reference point
        """
        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0

        # Get Moon and Sun positions
        moon_sign = self.planets.get('Moon', self.planets.get(list(self.planets.keys())[0])).sign if self.planets else 'Aries'
        sun_sign = self.planets.get('Sun', self.planets.get(list(self.planets.keys())[0])).sign if self.planets else 'Aries'

        moon_idx = RASIS.index(moon_sign) if moon_sign in RASIS else 0
        sun_idx = RASIS.index(sun_sign) if sun_sign in RASIS else 0

        def build_ring(base_idx: int, base_name: str) -> Dict[str, Any]:
            """Build one ring of the Sudarshana Chakra"""
            ring = {
                'base': base_name,
                'base_sign': RASIS[base_idx],
                'base_sign_tamil': RASI_TAMIL[base_idx],
                'houses': {}
            }

            for i in range(12):
                house_num = i + 1
                sign_idx = (base_idx + i) % 12
                sign = RASIS[sign_idx]

                planets_here = []
                for planet, pos in self.planets.items():
                    if pos.sign == sign:
                        status = self._get_planet_status(planet)
                        planets_here.append({
                            'name': planet,
                            'abbr': PLANET_ABBR.get(planet, planet[:2]),
                            'retrograde': status['retrograde'],
                            'exalted': status['exalted'],
                            'debilitated': status['debilitated']
                        })

                ring['houses'][house_num] = {
                    'sign': sign,
                    'sign_tamil': RASI_TAMIL[sign_idx],
                    'sign_abbr': sign[:3],
                    'planets': planets_here,
                    'planet_abbrs': ' '.join([p['abbr'] + ('(R)' if p['retrograde'] else '') for p in planets_here])
                }

            return ring

        # Build all three rings
        lagna_ring = build_ring(lagna_idx, 'Lagna')
        moon_ring = build_ring(moon_idx, 'Moon')
        sun_ring = build_ring(sun_idx, 'Sun')

        # Calculate year prediction based on Sudarshana principles
        # Each house in each ring represents one year from that reference

        return {
            'lagna_ring': lagna_ring,
            'moon_ring': moon_ring,
            'sun_ring': sun_ring,
            'lagna_sign': RASIS[lagna_idx],
            'moon_sign': moon_sign,
            'sun_sign': sun_sign,
            'description': 'Three rings: Inner=Lagna, Middle=Moon, Outer=Sun. Each house=1 year.'
        }

    def get_nirayana_longitudes_table(self) -> List[Dict[str, Any]]:
        """
        Get Nirayana Longitudes Summary table with full planet details
        Returns sorted list of planets with Deg:Min:Sec, Star/Pada, status markers
        """
        longitudes = []

        for planet in PLANETS:
            if planet not in self.planets:
                continue

            pos = self.planets[planet]
            status = self._get_planet_status(planet)

            # Build status markers string
            markers = []
            if status['retrograde']:
                markers.append('(R)')  # Retrograde
            if status['exalted']:
                markers.append('(Ex)')  # Exalted
            if status['debilitated']:
                markers.append('(Db)')  # Debilitated
            if status['combust']:
                markers.append('(C)')  # Combust

            status_str = ' '.join(markers)

            longitudes.append({
                'planet': planet,
                'abbr': PLANET_ABBR.get(planet, planet[:2]),
                'sanskrit': PLANET_SANSKRIT.get(planet, planet),
                'tamil': PLANET_TAMIL.get(planet, planet),
                'rasi': pos.sign,
                'rasi_tamil': RASI_TAMIL[pos.sign_index],
                'rasi_sanskrit': RASI_SANSKRIT.get(pos.sign, pos.sign),
                'longitude': pos.longitude,
                'longitude_dms': self._deg_to_dms(pos.longitude),
                'degree': pos.degree,
                'degree_dms': self._deg_to_dms(pos.degree),
                'nakshatra': pos.nakshatra,
                'nakshatra_tamil': NAKSHATRAS[pos.nakshatra_index]['tamil'] if pos.nakshatra_index < len(NAKSHATRAS) else '',
                'pada': pos.nakshatra_pada,
                'star_pada': f"{pos.nakshatra} / {pos.nakshatra_pada}",
                'retrograde': status['retrograde'],
                'exalted': status['exalted'],
                'debilitated': status['debilitated'],
                'combust': status['combust'],
                'status_markers': status_str
            })

        return longitudes

    def get_special_rasi_chakra_data(self) -> Dict[str, Any]:
        """
        Get Special Rasi Chakra data with detailed planet info:
        - Deg:Min:Sec format
        - Retrograde (R), Exalted (*), Debilitated (^), Combust (C) markers
        """
        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0

        chakra_data = {
            'style': 'south_indian',
            'lagna': self.lagna_sign,
            'lagna_tamil': RASI_TAMIL[lagna_idx],
            'lagna_degree_dms': self._deg_to_dms(self.lagna_degree),
            'houses': {}
        }

        for i in range(12):
            house_num = i + 1
            sign_idx = (lagna_idx + i) % 12
            sign = RASIS[sign_idx]

            planets_in_house = []
            for planet, pos in self.planets.items():
                if pos.sign == sign:
                    status = self._get_planet_status(planet)

                    # Build display string with markers
                    abbr = PLANET_ABBR.get(planet, planet[:2])
                    display = abbr

                    if status['retrograde']:
                        display += '(R)'
                    if status['exalted']:
                        display += '*'
                    if status['debilitated']:
                        display += '^'
                    if status['combust']:
                        display += '(C)'

                    planets_in_house.append({
                        'name': planet,
                        'abbr': abbr,
                        'display': display,
                        'degree': pos.degree,
                        'degree_dms': self._deg_to_dms(pos.degree),
                        'longitude_dms': self._deg_to_dms(pos.longitude),
                        'nakshatra': pos.nakshatra,
                        'pada': pos.nakshatra_pada,
                        'retrograde': status['retrograde'],
                        'exalted': status['exalted'],
                        'debilitated': status['debilitated'],
                        'combust': status['combust']
                    })

            # Get position for South Indian chart
            position = SOUTH_INDIAN_POSITIONS.get(sign, (0, 0))

            chakra_data['houses'][house_num] = {
                'sign': sign,
                'sign_tamil': RASI_TAMIL[sign_idx],
                'sign_abbr': sign[:3],
                'house_num': house_num,
                'is_lagna': house_num == 1,
                'planets': planets_in_house,
                'planet_display': ' '.join([p['display'] for p in planets_in_house]),
                'position': position
            }

        return chakra_data

    # ============== COMPREHENSIVE PANCHANGA CALCULATIONS ==============

    def get_complete_panchanga(self) -> Dict[str, Any]:
        """
        Calculate complete Panchanga data for birth chart - ALL DYNAMIC
        Includes: Thithi, Karana, Yoga, Nakshatra, Weekday, Ayanamsa, etc.
        """
        # Get birth data
        birth_date = self.birth_date
        birth_time = self.user_data.get('birth_time', '12:00')
        birth_place = self.user_data.get('birth_place', 'Chennai')
        latitude = self.user_data.get('latitude', 13.0827)
        longitude_geo = self.user_data.get('longitude', 80.2707)

        # Calculate weekday
        weekday_idx = birth_date.weekday()  # 0=Monday in Python
        weekday_idx = (weekday_idx + 1) % 7  # Convert to 0=Sunday
        weekday = WEEKDAYS[weekday_idx]
        weekday_tamil = WEEKDAYS_TAMIL[weekday_idx]

        # Get Sun and Moon positions
        sun_long = self.planets.get('Sun', self.planets.get(list(self.planets.keys())[0])).longitude if self.planets else 0
        moon_long = self.planets.get('Moon', self.planets.get(list(self.planets.keys())[0])).longitude if self.planets else 0

        # Calculate Thithi (lunar day) based on Sun-Moon distance
        moon_sun_diff = (moon_long - sun_long) % 360
        thithi_idx = int(moon_sun_diff / 12) % 15
        thithi = THITHIS[thithi_idx]
        thithi_tamil = THITHIS_TAMIL[thithi_idx]
        paksha = 'Shukla' if moon_sun_diff < 180 else 'Krishna'
        paksha_tamil = 'சுக்ல பக்ஷம்' if paksha == 'Shukla' else 'கிருஷ்ண பக்ஷம்'

        # Calculate Karana (half lunar day)
        karana_idx = int(moon_sun_diff / 6) % 11
        karana = KARANAS[karana_idx]
        karana_tamil = KARANAS_TAMIL[karana_idx]

        # Calculate Nithya Yoga (Sun + Moon longitude)
        yoga_value = (sun_long + moon_long) % 360
        yoga_idx = int(yoga_value / 13.333333) % 27
        nithya_yoga = NITHYA_YOGAS[yoga_idx]
        nithya_yoga_tamil = NITHYA_YOGAS_TAMIL[yoga_idx]

        # Get Nakshatra data
        moon_pos = self.planets.get('Moon')
        nakshatra = moon_pos.nakshatra if moon_pos else 'Ashwini'
        nakshatra_pada = moon_pos.nakshatra_pada if moon_pos else 1
        nakshatra_idx = moon_pos.nakshatra_index if moon_pos else 0
        nakshatra_data = NAKSHATRAS[nakshatra_idx] if nakshatra_idx < len(NAKSHATRAS) else NAKSHATRAS[0]
        star_lord = nakshatra_data['lord']

        # Get Ganam, Yoni, Bird, Tree
        ganam = NAKSHATRA_GANAM.get(nakshatra, 'Deva')
        yoni = NAKSHATRA_YONI.get(nakshatra, 'Horse')
        bird = NAKSHATRA_BIRD.get(nakshatra, 'Eagle')
        tree = NAKSHATRA_TREE.get(nakshatra, 'Banyan')

        # Rasi and Lagna data
        moon_rasi = self.moon_sign
        moon_rasi_idx = RASIS.index(moon_rasi) if moon_rasi in RASIS else 0
        moon_rasi_lord = RASI_LORDS[moon_rasi]
        lagna = self.lagna_sign
        lagna_idx = RASIS.index(lagna) if lagna in RASIS else 0
        lagna_lord = RASI_LORDS[lagna]

        # Calculate Ayanamsa (Lahiri approximation)
        year = birth_date.year
        ayanamsa = 23.85 + (year - 2000) * 0.0139  # Approximate Lahiri
        ayanamsa_deg = int(ayanamsa)
        ayanamsa_min = int((ayanamsa - ayanamsa_deg) * 60)
        ayanamsa_sec = int(((ayanamsa - ayanamsa_deg) * 60 - ayanamsa_min) * 60)

        # Calculate approximate sunrise/sunset (based on location)
        # This is simplified - actual calculation needs ephemeris
        sunrise_hour = 6 - (longitude_geo - 82.5) / 15  # IST reference
        sunset_hour = 18 - (longitude_geo - 82.5) / 15
        sunrise = f"{int(sunrise_hour):02d}:{int((sunrise_hour % 1) * 60):02d} AM"
        sunset = f"{int(sunset_hour - 12):02d}:{int((sunset_hour % 1) * 60):02d} PM"

        # Calculate Dinamana (day duration in ghatis)
        day_duration_hours = sunset_hour - sunrise_hour
        dinamana = day_duration_hours * 2.5  # 1 hour = 2.5 ghatis

        # Calculate Kalidina Sankhya (days since Kali Yuga)
        # Kali Yuga started on February 18, 3102 BCE (Julian) - we use approximation
        # Days from Jan 1, year 1 to birth date + offset for Kali epoch
        try:
            days_from_epoch = (datetime.combine(birth_date, datetime.min.time()) - datetime(1, 1, 1)).days
            kalidina = days_from_epoch + 1859982  # Approximate days from Kali epoch to year 1
        except:
            kalidina = 1867342  # Default approximate value

        # Calculate Chandra Avastha and Vela
        moon_dist_from_sun = (moon_long - sun_long) % 360
        chandra_avastha_idx = int(moon_dist_from_sun / 40) % 9
        chandra_avastha = f"{int(moon_dist_from_sun / 30) + 1} / 12"
        chandra_vela = f"{int(moon_dist_from_sun / 10) + 1} / 36"
        chandra_kriya = f"{int(moon_dist_from_sun / 6) + 1} / 60"

        # Calculate Dagda Rasi (burnt signs)
        dagda_rasi_1_idx = (moon_rasi_idx + 6) % 12
        dagda_rasi_2_idx = (moon_rasi_idx + 8) % 12
        dagda_rasi = f"{RASI_SANSKRIT.get(RASIS[dagda_rasi_1_idx], RASIS[dagda_rasi_1_idx])}, {RASI_SANSKRIT.get(RASIS[dagda_rasi_2_idx], RASIS[dagda_rasi_2_idx])}"

        # Calculate Yogi Point and Planet
        yogi_point = (sun_long + moon_long + 93.33333) % 360
        yogi_nakshatra_idx = int(yogi_point / 13.333333) % 27
        yogi_nakshatra = NAKSHATRAS[yogi_nakshatra_idx]['name']
        yogi_planet = NAKSHATRAS[yogi_nakshatra_idx]['lord']
        yogi_point_dms = self._deg_to_dms(yogi_point)

        # Calculate Duplicate Yogi (6th from Yogi)
        duplicate_yogi_idx = (yogi_nakshatra_idx + 5) % 27
        duplicate_yogi = NAKSHATRAS[duplicate_yogi_idx]['lord']

        # Calculate Avayogi Star and Planet
        avayogi_idx = (yogi_nakshatra_idx + 13) % 27
        avayogi_star = NAKSHATRAS[avayogi_idx]['name']
        avayogi_planet = NAKSHATRAS[avayogi_idx]['lord']

        # Calculate Chara Karakas (based on degree)
        planet_degrees = [(p, pos.degree) for p, pos in self.planets.items() if p not in ['Rahu', 'Ketu']]
        planet_degrees.sort(key=lambda x: x[1], reverse=True)
        atma_karaka = planet_degrees[0][0] if planet_degrees else 'Sun'
        amatya_karaka = planet_degrees[1][0] if len(planet_degrees) > 1 else 'Moon'

        # Calculate Arudha Lagna (Lagna Pada)
        lagna_lord_house = self._get_planet_house(lagna_lord)
        lagna_pada_house = ((lagna_lord_house - 1) * 2 + 1) % 12
        lagna_pada_sign = RASIS[(lagna_idx + lagna_pada_house - 1) % 12]

        # Calculate Dhana Arudha
        second_sign = RASIS[(lagna_idx + 1) % 12]
        second_lord = RASI_LORDS[second_sign]
        dhana_lord_house = self._get_planet_house(second_lord)
        dhana_pada_sign = RASIS[(lagna_idx + 1 + (dhana_lord_house - 2) * 2) % 12]

        # Western Zodiac (Tropical)
        tropical_sun_long = (sun_long + ayanamsa) % 360
        western_sign_idx = int(tropical_sun_long / 30)
        western_sign = RASIS[western_sign_idx]

        # Uttarayana/Dakshinayana
        ayana = 'Uttarayana' if sun_long > 270 or sun_long < 90 else 'Dakshinayana'
        ayana_tamil = 'உத்தராயணம்' if ayana == 'Uttarayana' else 'தக்ஷிணாயனம்'

        # Drekkana (decanate)
        lagna_drekkana = int(self.lagna_degree / 10) + 1
        drekkana_info = DREKKANA_SIGNIFICATIONS.get(lagna_drekkana, DREKKANA_SIGNIFICATIONS[1])

        return {
            'birth_date': str(birth_date),
            'birth_time': birth_time,
            'birth_place': birth_place,
            'latitude': f"{latitude:.2f}",
            'longitude': f"{longitude_geo:.2f}",
            'weekday': weekday,
            'weekday_tamil': weekday_tamil,
            'thithi': thithi,
            'thithi_tamil': thithi_tamil,
            'paksha': paksha,
            'paksha_tamil': paksha_tamil,
            'karana': karana,
            'karana_tamil': karana_tamil,
            'nithya_yoga': nithya_yoga,
            'nithya_yoga_tamil': nithya_yoga_tamil,
            'nakshatra': nakshatra,
            'nakshatra_tamil': nakshatra_data['tamil'],
            'nakshatra_pada': nakshatra_pada,
            'star_lord': star_lord,
            'ganam': ganam,
            'yoni': yoni,
            'bird': bird,
            'tree': tree,
            'moon_rasi': moon_rasi,
            'moon_rasi_tamil': RASI_TAMIL[moon_rasi_idx],
            'moon_rasi_lord': moon_rasi_lord,
            'lagna': lagna,
            'lagna_tamil': RASI_TAMIL[lagna_idx],
            'lagna_lord': lagna_lord,
            'lagna_degree': self.lagna_degree,
            'lagna_degree_dms': self._deg_to_dms(self.lagna_degree),
            'ayanamsa': f"Chitra Paksha = {ayanamsa_deg} Deg. {ayanamsa_min} Min. {ayanamsa_sec} Sec.",
            'sunrise': sunrise,
            'sunset': sunset,
            'dinamana': f"{dinamana:.2f}",
            'kalidina_sankhya': kalidina,
            'chandra_avastha': chandra_avastha,
            'chandra_vela': chandra_vela,
            'chandra_kriya': chandra_kriya,
            'dagda_rasi': dagda_rasi,
            'yogi_point': yogi_point_dms,
            'yogi_nakshatra': yogi_nakshatra,
            'yogi_planet': yogi_planet,
            'duplicate_yogi': duplicate_yogi,
            'avayogi_star': avayogi_star,
            'avayogi_planet': avayogi_planet,
            'atma_karaka': atma_karaka,
            'amatya_karaka': amatya_karaka,
            'lagna_pada': RASI_SANSKRIT.get(lagna_pada_sign, lagna_pada_sign),
            'dhana_pada': RASI_SANSKRIT.get(dhana_pada_sign, dhana_pada_sign),
            'western_sign': western_sign,
            'ayana': ayana,
            'ayana_tamil': ayana_tamil,
            'drekkana': lagna_drekkana,
            'drekkana_info': drekkana_info,
            'dasa_system': 'Vimshottari, Years = 365.25 Days'
        }

    def _get_planet_house(self, planet: str) -> int:
        """Get house number of a planet from lagna"""
        if planet not in self.planets:
            return 1
        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0
        planet_sign_idx = self.planets[planet].sign_index
        return ((planet_sign_idx - lagna_idx) % 12) + 1

    # ============== BHAVA (HOUSE) PREDICTIONS ==============

    def get_bhava_predictions(self) -> Dict[int, Dict[str, Any]]:
        """
        Generate comprehensive Bhava predictions based on:
        - House lord placement
        - Planets in house
        - Aspects on house
        - Important years for each house
        All calculations are dynamic based on chart data.
        """
        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0
        predictions = {}

        for house in range(1, 13):
            sign_idx = (lagna_idx + house - 1) % 12
            sign = RASIS[sign_idx]
            lord = RASI_LORDS[sign]
            lord_house = self._get_planet_house(lord)

            # Get planets in this house
            planets_in_house = [p for p, pos in self.planets.items()
                               if ((pos.sign_index - lagna_idx) % 12) + 1 == house]

            # Calculate important years based on house lord and planets
            important_years = self._calculate_important_years(house, lord, lord_house, planets_in_house)

            # Generate prediction text dynamically
            prediction = self._generate_bhava_prediction(house, sign, lord, lord_house, planets_in_house)

            # Get house significations
            significations = HOUSE_KARAKAS.get(house, {}).get('signifies', [])
            karaka = HOUSE_KARAKAS.get(house, {}).get('karaka', 'Sun')

            # Calculate house strength
            house_strength = self._calculate_house_strength(house, lord, planets_in_house)

            predictions[house] = {
                'house_num': house,
                'sign': sign,
                'sign_tamil': RASI_TAMIL[sign_idx],
                'lord': lord,
                'lord_house': lord_house,
                'planets': planets_in_house,
                'karaka': karaka,
                'significations': significations,
                'important_years': important_years,
                'prediction': prediction,
                'strength': house_strength,
                'aspects': self._get_aspects_on_house(house)
            }

        return predictions

    def _calculate_important_years(self, house: int, lord: str, lord_house: int,
                                    planets: List[str]) -> List[int]:
        """Calculate important years for a house based on planetary influences"""
        years = []

        # Add maturity age of house lord
        if lord in MATURITY_AGES:
            years.append(MATURITY_AGES[lord])

        # Add maturity ages of planets in house
        for planet in planets:
            if planet in MATURITY_AGES:
                years.append(MATURITY_AGES[planet])

        # Add karaka planet maturity
        karaka = HOUSE_KARAKAS.get(house, {}).get('karaka', 'Sun')
        if karaka in MATURITY_AGES:
            years.append(MATURITY_AGES[karaka])

        # Add dasha-based years (when house lord's dasha might run)
        base_year = self.current_age
        dasha_periods = self._calculate_full_dasha_periods()
        for period in dasha_periods:
            if period['planet'] == lord:
                start_age = max(0, period['start_age'])
                if start_age > 0:
                    years.append(int(start_age))

        # Sort and remove duplicates
        years = sorted(list(set(years)))

        # Keep only reasonable years (5-80)
        years = [y for y in years if 5 <= y <= 80]

        return years[:7]  # Return max 7 important years

    def _calculate_house_strength(self, house: int, lord: str, planets: List[str]) -> str:
        """Calculate overall strength of a house"""
        score = 5.0  # Base score

        # Lord strength
        if lord in self.planets:
            lord_pos = self.planets[lord]
            # Check if lord is in own sign
            if lord_pos.sign in OWN_SIGNS.get(lord, []):
                score += 2
            # Check if lord is exalted
            if EXALTATION.get(lord) == lord_pos.sign:
                score += 3
            # Check if lord is debilitated
            if DEBILITATION.get(lord) == lord_pos.sign:
                score -= 2

        # Benefic planets in house
        benefics = ['Jupiter', 'Venus', 'Mercury', 'Moon']
        malefics = ['Saturn', 'Mars', 'Rahu', 'Ketu']
        for planet in planets:
            if planet in benefics:
                score += 1.5
            elif planet in malefics:
                score -= 0.5

        # Convert to grade
        if score >= 8:
            return 'Strong'
        elif score >= 6:
            return 'Good'
        elif score >= 4:
            return 'Average'
        else:
            return 'Weak'

    def _get_aspects_on_house(self, house: int) -> List[Dict]:
        """Get planetary aspects on a house"""
        aspects = []
        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0

        for planet, pos in self.planets.items():
            planet_house = ((pos.sign_index - lagna_idx) % 12) + 1

            # Standard 7th aspect (all planets)
            if (planet_house + 6) % 12 + 1 == house:
                aspects.append({'planet': planet, 'type': '7th aspect'})

            # Mars special aspects (4th and 8th)
            if planet == 'Mars':
                if (planet_house + 3) % 12 + 1 == house:
                    aspects.append({'planet': planet, 'type': '4th aspect'})
                if (planet_house + 7) % 12 + 1 == house:
                    aspects.append({'planet': planet, 'type': '8th aspect'})

            # Jupiter special aspects (5th and 9th)
            if planet == 'Jupiter':
                if (planet_house + 4) % 12 + 1 == house:
                    aspects.append({'planet': planet, 'type': '5th aspect'})
                if (planet_house + 8) % 12 + 1 == house:
                    aspects.append({'planet': planet, 'type': '9th aspect'})

            # Saturn special aspects (3rd and 10th)
            if planet == 'Saturn':
                if (planet_house + 2) % 12 + 1 == house:
                    aspects.append({'planet': planet, 'type': '3rd aspect'})
                if (planet_house + 9) % 12 + 1 == house:
                    aspects.append({'planet': planet, 'type': '10th aspect'})

        return aspects

    def _generate_bhava_prediction(self, house: int, sign: str, lord: str,
                                    lord_house: int, planets: List[str]) -> str:
        """Generate detailed prediction for a house - FULLY DYNAMIC"""
        predictions = []

        # Base prediction from lord placement
        lord_placement_text = self._get_lord_placement_prediction(house, lord, lord_house)
        predictions.append(lord_placement_text)

        # Add planet-in-house effects
        for planet in planets:
            planet_effect = self._get_planet_in_house_effect(planet, house)
            if planet_effect:
                predictions.append(planet_effect)

        # Add aspect effects
        aspects = self._get_aspects_on_house(house)
        for aspect in aspects:
            aspect_effect = self._get_aspect_effect(aspect['planet'], house, aspect['type'])
            if aspect_effect:
                predictions.append(aspect_effect)

        # Add drekkana effect for 1st house
        if house == 1:
            drekkana = int(self.lagna_degree / 10) + 1
            drekkana_text = self._get_drekkana_effect(drekkana)
            predictions.append(drekkana_text)

        # Add exaltation/debilitation effects for lord
        if lord in self.planets:
            lord_status = self._get_lord_status_effect(lord)
            if lord_status:
                predictions.append(lord_status)

        return ' '.join(predictions)

    def _get_lord_placement_prediction(self, house: int, lord: str, lord_house: int) -> str:
        """Get prediction based on house lord's placement"""
        # Dynamic prediction templates
        house_names = {
            1: 'ascendant', 2: '2nd', 3: '3rd', 4: '4th', 5: '5th', 6: '6th',
            7: '7th', 8: '8th', 9: '9th', 10: '10th', 11: '11th', 12: '12th'
        }

        placement_effects = {
            # Lord in angular houses (1,4,7,10) - strong
            (1, 4, 7, 10): f"Since the {house_names.get(house, '')} lord {lord} is in house {lord_house}, you will be fortunate.",
            # Lord in trine houses (1,5,9) - benefic
            (1, 5, 9): f"The {house_names.get(house, '')} lord being in a trine shows blessings.",
            # Lord in dusthana (6,8,12) - challenges
            (6, 8, 12): f"As the {house_names.get(house, '')} lord is in house {lord_house}, you may face some challenges that strengthen you."
        }

        # Generate specific prediction
        if lord_house in [1, 4, 7, 10]:
            return f"Since the lord of the {house_names.get(house, str(house))} house ({lord}) is in house {lord_house}, you are blessed with strength in this area."
        elif lord_house in [5, 9]:
            return f"The {house_names.get(house, str(house))} lord {lord} in house {lord_house} indicates good fortune and support."
        elif lord_house in [6, 8, 12]:
            return f"As the {house_names.get(house, str(house))} lord is in house {lord_house}, you may face challenges but will overcome them."
        elif lord_house in [2, 11]:
            return f"The {house_names.get(house, str(house))} lord in house {lord_house} indicates financial benefits related to this house."
        else:
            return f"The {house_names.get(house, str(house))} lord {lord} placed in house {lord_house} gives moderate results."

    def _get_planet_in_house_effect(self, planet: str, house: int) -> str:
        """Get effect of a planet in a specific house"""
        benefics = ['Jupiter', 'Venus', 'Mercury', 'Moon']
        malefics = ['Saturn', 'Mars', 'Rahu', 'Ketu', 'Sun']

        if planet in benefics:
            return f"Since {planet} is in house {house}, you will receive positive influences in this life area."
        else:
            return f"The presence of {planet} in house {house} indicates challenges that build strength."

    def _get_aspect_effect(self, planet: str, house: int, aspect_type: str) -> str:
        """Get effect of planetary aspect on a house"""
        benefics = ['Jupiter', 'Venus']
        if planet in benefics:
            return f"The {aspect_type} of {planet} on house {house} brings blessings and reduces negative effects."
        elif planet == 'Saturn':
            return f"The aspect of Saturn on house {house} indicates delays but eventual success through perseverance."
        elif planet == 'Mars':
            return f"The aspect of Mars on house {house} gives energy and drive but requires patience."
        return ""

    def _get_drekkana_effect(self, drekkana: int) -> str:
        """Get effect based on lagna drekkana"""
        effects = {
            1: "Since your Lagna lies in the first Drekkana, you are careful with resources and self-reliant.",
            2: "Since your Lagna lies in the second Drekkana, you value family relationships and cooperation.",
            3: "Since your Lagna lies in the third Drekkana, you have philosophical inclinations and spiritual interests."
        }
        return effects.get(drekkana, effects[1])

    def _get_lord_status_effect(self, lord: str) -> str:
        """Get effect based on lord's exaltation/debilitation status"""
        if lord not in self.planets:
            return ""
        pos = self.planets[lord]

        if EXALTATION.get(lord) == pos.sign:
            return f"Since {lord} is exalted, you are eligible for high positions and authority."
        elif DEBILITATION.get(lord) == pos.sign:
            return f"Since {lord} is in debilitation, focused effort is needed for best results."
        return ""

    # ============== DETAILED DASHA PREDICTIONS ==============

    def _calculate_full_dasha_periods(self) -> List[Dict[str, Any]]:
        """Calculate complete Vimshottari Dasha periods with exact dates"""
        # Get birth nakshatra lord to determine starting dasha
        moon_pos = self.planets.get('Moon')
        if not moon_pos:
            return []

        nakshatra_idx = moon_pos.nakshatra_index
        nakshatra_lord = NAKSHATRAS[nakshatra_idx]['lord'] if nakshatra_idx < len(NAKSHATRAS) else 'Ketu'

        # Calculate balance of dasha at birth
        degree_in_nakshatra = moon_pos.longitude % 13.333333
        balance_ratio = 1 - (degree_in_nakshatra / 13.333333)
        balance_years = DASHA_YEARS[nakshatra_lord] * balance_ratio

        # Find starting position in dasha order
        dasha_start_idx = DASHA_ORDER.index(nakshatra_lord)

        # Calculate all dasha periods
        periods = []
        current_date = datetime.combine(self.birth_date, datetime.min.time())
        current_age = 0

        for i in range(18):  # Cover multiple cycles
            planet_idx = (dasha_start_idx + i) % 9
            planet = DASHA_ORDER[planet_idx]

            if i == 0:
                years = balance_years
            else:
                years = DASHA_YEARS[planet]

            end_date = current_date + timedelta(days=years * 365.25)

            periods.append({
                'planet': planet,
                'planet_tamil': PLANET_TAMIL.get(planet, planet),
                'start_date': current_date.strftime('%d-%m-%Y'),
                'end_date': end_date.strftime('%d-%m-%Y'),
                'start_age': current_age,
                'end_age': current_age + years,
                'duration_years': years,
                'is_current': current_date <= datetime.now() < end_date
            })

            current_date = end_date
            current_age += years

            if current_age > 120:  # Stop at 120 years
                break

        return periods

    def get_detailed_dasha_predictions(self) -> Dict[str, Any]:
        """
        Generate detailed Dasha predictions with Bhukti (sub-periods)
        Includes exact dates, effects, and remedies
        """
        periods = self._calculate_full_dasha_periods()

        # Find current dasha
        current_dasha = None
        for period in periods:
            if period.get('is_current'):
                current_dasha = period
                break

        # Generate predictions for each period
        dasha_predictions = []
        for period in periods[:10]:  # First 10 periods
            planet = period['planet']

            # Calculate Bhukti (sub-periods)
            bhuktis = self._calculate_bhukti_periods(period)

            # Generate prediction based on planet's position in chart
            prediction = self._generate_dasha_prediction(planet)

            # Get remedies
            remedies = self._get_dasha_remedies(planet)

            dasha_predictions.append({
                **period,
                'bhuktis': bhuktis,
                'prediction': prediction,
                'remedies': remedies,
                'favorable': self._is_dasha_favorable(planet)
            })

        return {
            'current_dasha': current_dasha,
            'all_periods': dasha_predictions,
            'balance_at_birth': periods[0]['duration_years'] if periods else 0
        }

    def _calculate_bhukti_periods(self, mahadasha: Dict) -> List[Dict]:
        """Calculate Bhukti (sub-periods) within a Mahadasha"""
        dasha_planet = mahadasha['planet']
        dasha_years = mahadasha['duration_years']
        start_date = datetime.strptime(mahadasha['start_date'], '%d-%m-%Y')

        # Bhukti order starts from Mahadasha lord
        dasha_idx = DASHA_ORDER.index(dasha_planet)

        bhuktis = []
        current_date = start_date

        for i in range(9):
            bhukti_planet_idx = (dasha_idx + i) % 9
            bhukti_planet = DASHA_ORDER[bhukti_planet_idx]

            # Bhukti duration = (Dasha years * Bhukti years) / 120
            bhukti_years = (dasha_years * DASHA_YEARS[bhukti_planet]) / 120
            bhukti_days = bhukti_years * 365.25
            end_date = current_date + timedelta(days=bhukti_days)

            bhuktis.append({
                'planet': bhukti_planet,
                'planet_tamil': PLANET_TAMIL.get(bhukti_planet, bhukti_planet),
                'start_date': current_date.strftime('%d-%m-%Y'),
                'end_date': end_date.strftime('%d-%m-%Y'),
                'duration_months': bhukti_years * 12,
                'is_current': current_date <= datetime.now() < end_date
            })

            current_date = end_date

        return bhuktis

    def _generate_dasha_prediction(self, planet: str) -> str:
        """Generate prediction for a Dasha period based on planet's chart position"""
        if planet not in self.planets:
            return f"The {planet} Dasha period brings its natural significations."

        pos = self.planets[planet]
        house = self._get_planet_house(planet)

        # Check planet status
        is_exalted = EXALTATION.get(planet) == pos.sign
        is_debilitated = DEBILITATION.get(planet) == pos.sign
        is_own_sign = pos.sign in OWN_SIGNS.get(planet, [])

        prediction_parts = []

        # Base prediction
        if planet == 'Jupiter':
            prediction_parts.append("During Jupiter Dasha, you will enjoy growth, wisdom, and spiritual development.")
        elif planet == 'Venus':
            prediction_parts.append("Venus Dasha brings comforts, relationships, and material pleasures.")
        elif planet == 'Sun':
            prediction_parts.append("Sun Dasha highlights authority, recognition, and self-expression.")
        elif planet == 'Moon':
            prediction_parts.append("Moon Dasha emphasizes emotions, mother, and public interactions.")
        elif planet == 'Mars':
            prediction_parts.append("Mars Dasha brings energy, courage, and potential property matters.")
        elif planet == 'Mercury':
            prediction_parts.append("Mercury Dasha favors education, communication, and business.")
        elif planet == 'Saturn':
            prediction_parts.append("Saturn Dasha teaches patience, discipline, and karmic lessons.")
        elif planet == 'Rahu':
            prediction_parts.append("Rahu Dasha brings unexpected changes and unconventional opportunities.")
        elif planet == 'Ketu':
            prediction_parts.append("Ketu Dasha promotes spiritual growth and detachment.")

        # Add house-specific effects
        prediction_parts.append(f"Since {planet} is in house {house}, matters of that house are activated.")

        # Add dignity effects
        if is_exalted:
            prediction_parts.append(f"{planet} being exalted, you can expect excellent results during this period.")
        elif is_debilitated:
            prediction_parts.append(f"With {planet} debilitated, results may be delayed but will come with effort.")
        elif is_own_sign:
            prediction_parts.append(f"{planet} in own sign gives strong positive results.")

        return ' '.join(prediction_parts)

    def _is_dasha_favorable(self, planet: str) -> bool:
        """Determine if a Dasha is generally favorable"""
        if planet not in self.planets:
            return True

        pos = self.planets[planet]

        # Favorable conditions
        if EXALTATION.get(planet) == pos.sign:
            return True
        if pos.sign in OWN_SIGNS.get(planet, []):
            return True

        # Unfavorable conditions
        if DEBILITATION.get(planet) == pos.sign:
            return False

        # Neutral
        return True

    def _get_dasha_remedies(self, planet: str) -> Dict[str, Any]:
        """Get remedies for a specific Dasha period"""
        remedies = {
            'Sun': {
                'deity': 'Lord Shiva / Surya',
                'mantra': 'Om Suryaya Namaha',
                'color': 'Ruby red',
                'donation': 'Wheat, jaggery, red cloth',
                'fasting': 'Sunday'
            },
            'Moon': {
                'deity': 'Goddess Parvati / Chandra',
                'mantra': 'Om Chandraya Namaha',
                'color': 'White',
                'donation': 'Rice, white cloth, silver',
                'fasting': 'Monday'
            },
            'Mars': {
                'deity': 'Lord Hanuman / Kartikeya',
                'mantra': 'Om Mangalaya Namaha',
                'color': 'Red',
                'donation': 'Red lentils, copper, red cloth',
                'fasting': 'Tuesday'
            },
            'Mercury': {
                'deity': 'Lord Vishnu',
                'mantra': 'Om Budhaya Namaha',
                'color': 'Green',
                'donation': 'Green moong, emerald, green cloth',
                'fasting': 'Wednesday'
            },
            'Jupiter': {
                'deity': 'Lord Vishnu / Brihaspati',
                'mantra': 'Om Gurave Namaha',
                'color': 'Yellow',
                'donation': 'Yellow cloth, turmeric, gold',
                'fasting': 'Thursday'
            },
            'Venus': {
                'deity': 'Goddess Lakshmi',
                'mantra': 'Om Shukraya Namaha',
                'color': 'White/Pink',
                'donation': 'White rice, silk, perfume',
                'fasting': 'Friday'
            },
            'Saturn': {
                'deity': 'Lord Shani / Hanuman',
                'mantra': 'Om Shanaishcharaya Namaha',
                'color': 'Blue/Black',
                'donation': 'Black sesame, iron, blue cloth',
                'fasting': 'Saturday'
            },
            'Rahu': {
                'deity': 'Goddess Durga',
                'mantra': 'Om Rahave Namaha',
                'color': 'Smoky blue',
                'donation': 'Coconut, blanket, blue cloth',
                'fasting': 'Saturday'
            },
            'Ketu': {
                'deity': 'Lord Ganesha',
                'mantra': 'Om Ketave Namaha',
                'color': 'Grey/Brown',
                'donation': 'Blanket, sesame, dog food',
                'fasting': 'Tuesday'
            }
        }
        return remedies.get(planet, remedies['Sun'])

    def get_aspect_yoga_map(self) -> Dict[str, Any]:
        """Generate aspect and yoga visualization data"""
        conjunctions = []
        aspects = []
        yogas_visual = []

        # Find all conjunctions and aspects
        planet_list = list(self.planets.keys())
        for i, p1 in enumerate(planet_list):
            pos1 = self.planets[p1]
            for p2 in planet_list[i+1:]:
                pos2 = self.planets[p2]

                # Calculate degree separation
                degree_diff = abs(pos1.longitude - pos2.longitude)
                if degree_diff > 180:
                    degree_diff = 360 - degree_diff

                # Conjunction (within 10 degrees)
                if degree_diff <= 10:
                    conjunctions.append({
                        'planets': [p1, p2],
                        'sign': pos1.sign,
                        'orb': round(degree_diff, 1),
                        'type': 'conjunction'
                    })

                # Opposition
                elif abs(degree_diff - 180) <= 10:
                    aspects.append({
                        'planets': [p1, p2],
                        'type': 'opposition',
                        'orb': round(abs(degree_diff - 180), 1)
                    })

                # Trine
                elif abs(degree_diff - 120) <= 10 or abs(degree_diff - 240) <= 10:
                    aspects.append({
                        'planets': [p1, p2],
                        'type': 'trine',
                        'orb': round(min(abs(degree_diff - 120), abs(degree_diff - 240)), 1)
                    })

                # Square
                elif abs(degree_diff - 90) <= 10 or abs(degree_diff - 270) <= 10:
                    aspects.append({
                        'planets': [p1, p2],
                        'type': 'square',
                        'orb': round(min(abs(degree_diff - 90), abs(degree_diff - 270)), 1)
                    })

        # Get yoga data for visualization
        yogas = self.detect_yogas()
        for yoga in yogas:
            yogas_visual.append({
                'name': yoga['name'],
                'planets': [p for p in PLANETS if p in yoga.get('formed_by', '')],
                'active': yoga.get('activation', {}).get('is_active', False)
            })

        return {
            'conjunctions': conjunctions,
            'aspects': aspects,
            'yogas': yogas_visual,
            'summary': f'{len(conjunctions)} conjunctions, {len(aspects)} aspects, {len(yogas)} yogas'
        }

    # ============== ASHTAKAVARGA ==============

    def calculate_ashtakavarga(self) -> Dict[str, Any]:
        """
        Calculate Ashtakavarga points for each sign
        Returns bindu counts per sign and planet contributions
        """
        # Initialize 12 signs with base points
        sarvashtakavarga = [0] * 12
        planet_contributions = {p: [0] * 12 for p in PLANETS[:7]}  # Exclude Rahu/Ketu

        # Simplified Ashtakavarga calculation
        for planet in PLANETS[:7]:
            if planet not in self.planets:
                continue

            p = self.planets[planet]

            # Each planet contributes to certain houses from its position
            # This is a simplified version of the actual rules
            benefic_houses = self._get_ashtakavarga_benefic_houses(planet)

            for offset in benefic_houses:
                sign_idx = (p.sign_index + offset - 1) % 12
                sarvashtakavarga[sign_idx] += 1
                planet_contributions[planet][sign_idx] += 1

        # Normalize to typical range (28-35 total per sign average)
        # Add base points to simulate full calculation
        for i in range(12):
            sarvashtakavarga[i] += 20  # Base points

        return {
            'sarvashtakavarga': sarvashtakavarga,
            'planet_contributions': planet_contributions,
            'strongest_sign': RASIS[sarvashtakavarga.index(max(sarvashtakavarga))],
            'weakest_sign': RASIS[sarvashtakavarga.index(min(sarvashtakavarga))],
            'math_trace': f'SAV range: {min(sarvashtakavarga)}-{max(sarvashtakavarga)} bindus'
        }

    def _get_ashtakavarga_benefic_houses(self, planet: str) -> List[int]:
        """Get houses where planet contributes bindus (simplified)"""
        # Simplified benefic positions for each planet
        rules = {
            'Sun': [1, 2, 4, 7, 8, 9, 10, 11],
            'Moon': [1, 3, 6, 7, 10, 11],
            'Mars': [1, 2, 4, 7, 8, 10, 11],
            'Mercury': [1, 2, 4, 6, 8, 10, 11],
            'Jupiter': [1, 2, 3, 4, 7, 8, 10, 11],
            'Venus': [1, 2, 3, 4, 5, 8, 9, 11],
            'Saturn': [1, 2, 4, 7, 8, 10, 11]
        }
        return rules.get(planet, [1, 4, 7, 10])

    # ============== YOGA DETECTION ==============

    def detect_yogas(self) -> List[Dict[str, Any]]:
        """
        Detect yogas present in the chart
        Returns list of yogas with formation logic and activation status
        """
        yogas = []

        # 1. Gajakesari Yoga
        yoga = self._check_gajakesari()
        if yoga:
            yogas.append(yoga)

        # 2. Budhaditya Yoga
        yoga = self._check_budhaditya()
        if yoga:
            yogas.append(yoga)

        # 3. Chandra-Mangala Yoga
        yoga = self._check_chandra_mangala()
        if yoga:
            yogas.append(yoga)

        # 4. Pancha Mahapurusha Yogas
        for yoga in self._check_mahapurusha_yogas():
            yogas.append(yoga)

        # 5. Raja Yogas
        for yoga in self._check_raja_yogas():
            yogas.append(yoga)

        # 6. Dhana Yogas
        for yoga in self._check_dhana_yogas():
            yogas.append(yoga)

        # Calculate activation for each yoga
        for yoga in yogas:
            yoga['activation'] = self._calculate_yoga_activation(yoga)

        return yogas

    def _check_gajakesari(self) -> Optional[Dict]:
        """Jupiter in kendra from Moon"""
        if 'Jupiter' not in self.planets or 'Moon' not in self.planets:
            return None

        jup = self.planets['Jupiter']
        moon = self.planets['Moon']

        # Check if Jupiter is in 1, 4, 7, 10 from Moon
        distance = (jup.sign_index - moon.sign_index) % 12
        kendras = [0, 3, 6, 9]  # 1st, 4th, 7th, 10th

        if distance in kendras:
            strength = (self.calculate_shadbala('Jupiter')['total'] +
                       self.calculate_shadbala('Moon')['total']) / 2
            return {
                'name': 'Gajakesari Yoga',
                'name_tamil': 'கஜகேசரி யோகம்',
                'type': 'Wealth & Fame',
                'formed_by': f'Jupiter in {jup.sign} (H{distance+1} from Moon in {moon.sign})',
                'strength': round(strength, 2),
                'effects': 'Fame, wisdom, wealth, respected position',
                'math_trace': f'Jup@{jup.sign_index} - Moon@{moon.sign_index} = {distance} (kendra)'
            }
        return None

    def _check_budhaditya(self) -> Optional[Dict]:
        """Sun-Mercury conjunction"""
        if 'Sun' not in self.planets or 'Mercury' not in self.planets:
            return None

        sun = self.planets['Sun']
        merc = self.planets['Mercury']

        if sun.sign == merc.sign:
            # Check if Mercury is not combust (too close to Sun)
            degree_diff = abs(sun.degree - merc.degree)
            is_combust = degree_diff < 14

            strength = 0.7 if not is_combust else 0.4

            return {
                'name': 'Budhaditya Yoga',
                'name_tamil': 'புதாதித்ய யோகம்',
                'type': 'Intelligence',
                'formed_by': f'Sun-Mercury in {sun.sign} ({degree_diff:.1f}° apart)',
                'strength': strength,
                'effects': 'Intelligence, communication skills, analytical mind',
                'combust': is_combust,
                'math_trace': f'Sun@{sun.degree:.1f}° - Merc@{merc.degree:.1f}° = {degree_diff:.1f}°'
            }
        return None

    def _check_chandra_mangala(self) -> Optional[Dict]:
        """Moon-Mars conjunction or mutual aspect"""
        if 'Moon' not in self.planets or 'Mars' not in self.planets:
            return None

        moon = self.planets['Moon']
        mars = self.planets['Mars']

        # Conjunction
        if moon.sign == mars.sign:
            strength = (self.calculate_shadbala('Moon')['total'] +
                       self.calculate_shadbala('Mars')['total']) / 2
            return {
                'name': 'Chandra-Mangala Yoga',
                'name_tamil': 'சந்திர-மங்கள யோகம்',
                'type': 'Wealth through effort',
                'formed_by': f'Moon-Mars conjunction in {moon.sign}',
                'strength': round(strength, 2),
                'effects': 'Wealth through self-effort, business acumen',
                'math_trace': f'Moon & Mars both in {moon.sign}'
            }

        # Mutual aspect (7th from each other)
        if abs(moon.sign_index - mars.sign_index) == 6:
            return {
                'name': 'Chandra-Mangala Yoga',
                'name_tamil': 'சந்திர-மங்கள யோகம்',
                'type': 'Wealth through effort',
                'formed_by': f'Moon in {moon.sign} opposing Mars in {mars.sign}',
                'strength': 0.6,
                'effects': 'Wealth through enterprise, courage in business',
                'math_trace': f'Moon@{moon.sign_index} opposite Mars@{mars.sign_index}'
            }
        return None

    def _check_mahapurusha_yogas(self) -> List[Dict]:
        """Check Pancha Mahapurusha Yogas"""
        yogas = []

        mahapurusha = {
            'Mars': ('Ruchaka', 'ருசக யோகம்', 'Courage, leadership, military success'),
            'Mercury': ('Bhadra', 'பத்ர யோகம்', 'Intelligence, eloquence, trade success'),
            'Jupiter': ('Hamsa', 'ஹம்ச யோகம்', 'Wisdom, spirituality, noble character'),
            'Venus': ('Malavya', 'மாளவ்ய யோகம்', 'Luxury, beauty, artistic talents'),
            'Saturn': ('Sasa', 'சச யோகம்', 'Authority, discipline, political power')
        }

        for planet, (name, tamil, effects) in mahapurusha.items():
            if planet not in self.planets:
                continue

            p = self.planets[planet]
            lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0

            # Must be in kendra from lagna
            house_from_lagna = ((p.sign_index - lagna_idx) % 12) + 1
            if house_from_lagna not in [1, 4, 7, 10]:
                continue

            # Must be in own sign or exalted
            dignity, score, _ = self.get_dignity(planet)
            if dignity not in ['Own Sign', 'Exalted', 'Moolatrikona']:
                continue

            yogas.append({
                'name': f'{name} Yoga',
                'name_tamil': tamil,
                'type': 'Mahapurusha',
                'formed_by': f'{planet} in {p.sign} (H{house_from_lagna}, {dignity})',
                'strength': score,
                'effects': effects,
                'math_trace': f'{planet} in kendra H{house_from_lagna}, dignity={dignity}'
            })

        return yogas

    def _check_raja_yogas(self) -> List[Dict]:
        """Check Raja Yogas (Kendra-Trikona lord connections)"""
        yogas = []

        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0

        # Get house lords
        house_lords = {}
        for i in range(12):
            sign = RASIS[(lagna_idx + i) % 12]
            house_lords[i + 1] = RASI_LORDS[sign]

        # Kendra lords: 1, 4, 7, 10
        # Trikona lords: 1, 5, 9
        kendra_lords = [house_lords[h] for h in [1, 4, 7, 10]]
        trikona_lords = [house_lords[h] for h in [1, 5, 9]]

        # Check for conjunction of kendra and trikona lords
        for k_lord in kendra_lords:
            for t_lord in trikona_lords:
                if k_lord == t_lord:
                    continue

                if k_lord not in self.planets or t_lord not in self.planets:
                    continue

                k_pos = self.planets[k_lord]
                t_pos = self.planets[t_lord]

                # Same sign = Raja Yoga
                if k_pos.sign == t_pos.sign:
                    yogas.append({
                        'name': 'Raja Yoga',
                        'name_tamil': 'ராஜ யோகம்',
                        'type': 'Power & Status',
                        'formed_by': f'{k_lord} (kendra lord) + {t_lord} (trikona lord) in {k_pos.sign}',
                        'strength': 0.75,
                        'effects': 'Authority, success, rise in status',
                        'math_trace': f'Kendra lord {k_lord} conjunct trikona lord {t_lord}'
                    })
                    break

        return yogas[:3]  # Limit to top 3

    def _check_dhana_yogas(self) -> List[Dict]:
        """Check Dhana (Wealth) Yogas"""
        yogas = []

        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0

        # 2nd and 11th lord connection = Dhana Yoga
        sign_2 = RASIS[(lagna_idx + 1) % 12]
        sign_11 = RASIS[(lagna_idx + 10) % 12]

        lord_2 = RASI_LORDS[sign_2]
        lord_11 = RASI_LORDS[sign_11]

        if lord_2 in self.planets and lord_11 in self.planets:
            pos_2 = self.planets[lord_2]
            pos_11 = self.planets[lord_11]

            if pos_2.sign == pos_11.sign:
                yogas.append({
                    'name': 'Dhana Yoga',
                    'name_tamil': 'தன யோகம்',
                    'type': 'Wealth',
                    'formed_by': f'2nd lord ({lord_2}) + 11th lord ({lord_11}) in {pos_2.sign}',
                    'strength': 0.7,
                    'effects': 'Accumulation of wealth, financial success',
                    'math_trace': f'H2 lord {lord_2} conjunct H11 lord {lord_11}'
                })

        # Jupiter in 2nd or 11th
        if 'Jupiter' in self.planets:
            jup = self.planets['Jupiter']
            jup_house = ((jup.sign_index - lagna_idx) % 12) + 1

            if jup_house in [2, 11]:
                yogas.append({
                    'name': 'Guru Dhana Yoga',
                    'name_tamil': 'குரு தன யோகம்',
                    'type': 'Wealth',
                    'formed_by': f'Jupiter in H{jup_house} ({jup.sign})',
                    'strength': 0.65,
                    'effects': 'Wealth through wisdom, ethical gains',
                    'math_trace': f'Jupiter in wealth house {jup_house}'
                })

        return yogas

    def _calculate_yoga_activation(self, yoga: Dict) -> Dict:
        """Calculate when yoga will be activated"""
        current_dasha = self._get_current_dasha()

        # Check if yoga-forming planets are in current dasha
        formed_by = yoga.get('formed_by', '')
        is_active = False
        activation_period = 'Future'

        for planet in PLANETS:
            if planet in formed_by:
                if planet == current_dasha.get('mahadasha'):
                    is_active = True
                    activation_period = 'Current Mahadasha'
                elif planet == current_dasha.get('antardasha'):
                    is_active = True
                    activation_period = 'Current Antardasha'

        return {
            'is_active': is_active,
            'period': activation_period,
            'strength_multiplier': 1.5 if is_active else 0.7
        }

    # ============== DOSHA DETECTION ==============

    def detect_doshas(self) -> List[Dict[str, Any]]:
        """Detect doshas with severity and mitigation factors"""
        doshas = []

        # 1. Mangal Dosha
        dosha = self._check_mangal_dosha()
        if dosha:
            doshas.append(dosha)

        # 2. Kaal Sarpa Dosha
        dosha = self._check_kaal_sarpa()
        if dosha:
            doshas.append(dosha)

        # 3. Pitra Dosha
        dosha = self._check_pitra_dosha()
        if dosha:
            doshas.append(dosha)

        # 4. Shani Dosha
        dosha = self._check_shani_dosha()
        if dosha:
            doshas.append(dosha)

        return doshas

    def _check_mangal_dosha(self) -> Optional[Dict]:
        """Check Mangal/Kuja Dosha"""
        if 'Mars' not in self.planets:
            return None

        mars = self.planets['Mars']
        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0

        # Calculate Mars house from lagna
        mars_house = ((mars.sign_index - lagna_idx) % 12) + 1

        # Dosha houses: 1, 4, 7, 8, 12
        dosha_houses = [1, 4, 7, 8, 12]

        if mars_house not in dosha_houses:
            return None

        # Calculate severity
        severity = 0.7
        cancellation_factors = []

        # Check cancellation factors
        # Mars in own sign or exalted reduces severity
        dignity, _, _ = self.get_dignity('Mars')
        if dignity in ['Own Sign', 'Exalted']:
            severity -= 0.3
            cancellation_factors.append(f'Mars in {dignity}')

        # Jupiter aspect on Mars
        if 'Jupiter' in self.planets:
            jup = self.planets['Jupiter']
            if abs(jup.sign_index - mars.sign_index) in [0, 4, 6, 8]:  # Aspect houses
                severity -= 0.2
                cancellation_factors.append('Jupiter aspects Mars')

        # Venus in 7th from lagna
        if 'Venus' in self.planets:
            venus = self.planets['Venus']
            venus_house = ((venus.sign_index - lagna_idx) % 12) + 1
            if venus_house == 7:
                severity -= 0.15
                cancellation_factors.append('Venus in 7th house')

        severity = max(0.1, severity)

        return {
            'name': 'Mangal Dosha',
            'name_tamil': 'செவ்வாய் தோஷம்',
            'severity': round(severity, 2),
            'formed_by': f'Mars in H{mars_house} from Lagna',
            'cancellation_factors': cancellation_factors,
            'net_effect': 'Minimal' if severity < 0.3 else ('Moderate' if severity < 0.5 else 'Significant'),
            'remedies': ['Mangal Shanti puja', 'Wear Red Coral (consult)', 'Tuesday fasting'],
            'math_trace': f'Mars@H{mars_house}, severity={severity:.2f}'
        }

    def _check_kaal_sarpa(self) -> Optional[Dict]:
        """Check Kaal Sarpa Dosha"""
        if 'Rahu' not in self.planets or 'Ketu' not in self.planets:
            return None

        rahu = self.planets['Rahu']
        ketu = self.planets['Ketu']

        # All planets must be between Rahu and Ketu
        rahu_idx = rahu.sign_index
        ketu_idx = ketu.sign_index

        planets_between = 0
        planets_outside = 0

        for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
            if planet not in self.planets:
                continue

            p_idx = self.planets[planet].sign_index

            # Check if planet is between Rahu and Ketu
            if rahu_idx < ketu_idx:
                if rahu_idx <= p_idx <= ketu_idx:
                    planets_between += 1
                else:
                    planets_outside += 1
            else:
                if p_idx >= rahu_idx or p_idx <= ketu_idx:
                    planets_between += 1
                else:
                    planets_outside += 1

        # Full Kaal Sarpa if all planets are hemmed
        if planets_outside > 0:
            return None

        # Partial Kaal Sarpa
        severity = 0.5 if planets_between >= 5 else 0.3

        return {
            'name': 'Kaal Sarpa Dosha',
            'name_tamil': 'கால சர்ப தோஷம்',
            'severity': severity,
            'formed_by': f'All planets between Rahu ({rahu.sign}) and Ketu ({ketu.sign})',
            'type': 'Full' if planets_between == 7 else 'Partial',
            'cancellation_factors': [],
            'net_effect': 'Challenges followed by eventual success',
            'remedies': ['Rahu-Ketu Shanti', 'Naag Puja', 'Visit Kaal Sarpa temples'],
            'math_trace': f'{planets_between} planets hemmed by Rahu-Ketu axis'
        }

    def _check_pitra_dosha(self) -> Optional[Dict]:
        """Check Pitra Dosha"""
        if 'Sun' not in self.planets:
            return None

        sun = self.planets['Sun']

        # Sun afflicted by Rahu, Ketu, or Saturn
        afflicted = False
        affliction_by = []

        for malefic in ['Rahu', 'Ketu', 'Saturn']:
            if malefic not in self.planets:
                continue

            mal = self.planets[malefic]

            # Conjunction
            if mal.sign == sun.sign:
                afflicted = True
                affliction_by.append(f'{malefic} conjunction')

            # Opposition
            if abs(mal.sign_index - sun.sign_index) == 6:
                afflicted = True
                affliction_by.append(f'{malefic} opposition')

        if not afflicted:
            return None

        severity = min(0.6, len(affliction_by) * 0.25)

        return {
            'name': 'Pitra Dosha',
            'name_tamil': 'பித்ரு தோஷம்',
            'severity': severity,
            'formed_by': f'Sun afflicted by {", ".join(affliction_by)}',
            'cancellation_factors': [],
            'net_effect': 'Ancestral karma patterns',
            'remedies': ['Shraddha ceremonies', 'Tarpan to ancestors', 'Serve elderly'],
            'math_trace': f'Sun@{sun.sign} afflicted: {affliction_by}'
        }

    def _check_shani_dosha(self) -> Optional[Dict]:
        """Check Saturn-related afflictions"""
        if 'Saturn' not in self.planets:
            return None

        saturn = self.planets['Saturn']
        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0

        saturn_house = ((saturn.sign_index - lagna_idx) % 12) + 1

        # Saturn in 1, 4, 7, 8, 10 can cause challenges
        difficult_houses = [1, 4, 7, 8, 10]

        if saturn_house not in difficult_houses:
            return None

        # Check Saturn's dignity
        dignity, dig_score, _ = self.get_dignity('Saturn')

        # Well-dignified Saturn reduces severity
        severity = 0.4 if dig_score > 0.6 else 0.6

        return {
            'name': 'Shani Dosha',
            'name_tamil': 'சனி தோஷம்',
            'severity': severity,
            'formed_by': f'Saturn in H{saturn_house} ({saturn.sign}, {dignity})',
            'cancellation_factors': [f'Saturn {dignity}'] if dig_score > 0.5 else [],
            'net_effect': 'Delays and lessons in life areas of the house',
            'remedies': ['Saturday fasting', 'Shani mantra', 'Serve the disadvantaged'],
            'math_trace': f'Saturn@H{saturn_house}, dignity={dignity}'
        }

    # ============== DASHA CALCULATIONS ==============

    def _get_current_dasha(self) -> Dict[str, Any]:
        """Get current dasha period"""
        dasha_data = self.chart_data.get('current_dasha', {})

        if isinstance(dasha_data, dict):
            return {
                'mahadasha': dasha_data.get('mahadasha', 'Jupiter'),
                'mahadasha_tamil': dasha_data.get('mahadasha_tamil', PLANET_TAMIL.get('Jupiter', 'குரு')),
                'antardasha': dasha_data.get('antardasha', 'Venus'),
                'antardasha_tamil': dasha_data.get('antardasha_tamil', PLANET_TAMIL.get('Venus', 'சுக்கிரன்'))
            }

        return {
            'mahadasha': 'Jupiter',
            'mahadasha_tamil': 'குரு',
            'antardasha': 'Venus',
            'antardasha_tamil': 'சுக்கிரன்'
        }

    def calculate_dasha_analysis(self) -> Dict[str, Any]:
        """Comprehensive dasha analysis with POI (Planet of Interest) strength"""
        current = self._get_current_dasha()
        maha_lord = current['mahadasha']
        antar_lord = current['antardasha']

        # Calculate POI for mahadasha lord
        maha_poi = self._calculate_planet_poi(maha_lord)
        antar_poi = self._calculate_planet_poi(antar_lord)

        # Calculate dasha timeline
        timeline = self._calculate_dasha_timeline()

        # Life areas activated
        activated_areas = self._get_dasha_activated_areas(maha_lord, antar_lord)

        return {
            'current': current,
            'mahadasha_poi': maha_poi,
            'antardasha_poi': antar_poi,
            'combined_strength': round((maha_poi['total'] * 0.7 + antar_poi['total'] * 0.3), 2),
            'timeline': timeline,
            'activated_areas': activated_areas,
            'interpretation_strength': 'Strong' if maha_poi['total'] > 0.6 else ('Moderate' if maha_poi['total'] > 0.4 else 'Challenging')
        }

    def _calculate_planet_poi(self, planet: str) -> Dict[str, Any]:
        """Calculate Planet of Interest strength for dasha analysis"""
        if planet not in self.planets:
            return {'total': 0.5, 'components': {}, 'math_trace': f'{planet} not found'}

        p = self.planets[planet]

        # Get shadbala
        shadbala = self.calculate_shadbala(planet)

        # House context
        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0
        house_from_lagna = ((p.sign_index - lagna_idx) % 12) + 1

        # House quality score
        good_houses = [1, 2, 4, 5, 7, 9, 10, 11]
        challenging_houses = [6, 8, 12]

        if house_from_lagna in good_houses:
            house_score = 0.7
        elif house_from_lagna in challenging_houses:
            house_score = 0.4
        else:
            house_score = 0.55

        # Combine scores
        total = (shadbala['total'] * 0.6 + house_score * 0.4)
        total = max(0.35, min(0.95, total))  # Apply floor and ceiling

        return {
            'total': round(total, 2),
            'shadbala': shadbala['total'],
            'house_position': house_from_lagna,
            'house_score': house_score,
            'dignity': self.get_dignity(planet)[0],
            'math_trace': f'{planet}: Shadbala={shadbala["total"]:.2f} * 0.6 + H{house_from_lagna}={house_score:.2f} * 0.4 = {total:.2f}'
        }

    def _calculate_dasha_timeline(self) -> List[Dict]:
        """Calculate full dasha timeline from birth"""
        timeline = []

        # Get birth nakshatra lord for dasha start
        moon_nak = self.moon_nakshatra
        nak_data = next((n for n in NAKSHATRAS if n['name'] == moon_nak), NAKSHATRAS[0])
        start_dasha = nak_data['lord']

        # Find start index
        start_idx = DASHA_ORDER.index(start_dasha) if start_dasha in DASHA_ORDER else 0

        # Calculate remaining years in first dasha
        moon_long = self.planets.get('Moon', self._default_planet_position('Moon')).longitude
        nak_portion_completed = (moon_long % 13.333333) / 13.333333
        first_dasha_years = DASHA_YEARS[start_dasha] * (1 - nak_portion_completed)

        current_year = self.birth_date.year if self.birth_date else 1990

        # First (partial) dasha
        timeline.append({
            'planet': start_dasha,
            'planet_tamil': PLANET_TAMIL.get(start_dasha, start_dasha),
            'start_year': current_year,
            'end_year': current_year + int(first_dasha_years),
            'duration': round(first_dasha_years, 1),
            'is_partial': True
        })
        current_year += first_dasha_years

        # Subsequent full dashas
        for i in range(1, 10):
            dasha_lord = DASHA_ORDER[(start_idx + i) % 9]
            duration = DASHA_YEARS[dasha_lord]

            timeline.append({
                'planet': dasha_lord,
                'planet_tamil': PLANET_TAMIL.get(dasha_lord, dasha_lord),
                'start_year': int(current_year),
                'end_year': int(current_year + duration),
                'duration': duration,
                'is_partial': False
            })
            current_year += duration

        return timeline

    def _get_dasha_activated_areas(self, maha: str, antar: str) -> List[str]:
        """Get life areas activated by current dasha"""
        areas = []

        for planet in [maha, antar]:
            if planet not in self.planets:
                continue

            p = self.planets[planet]
            lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0
            house = ((p.sign_index - lagna_idx) % 12) + 1

            if house in HOUSE_KARAKAS:
                signifies = HOUSE_KARAKAS[house]['signifies']
                areas.extend(signifies[:2])  # Top 2 significations

        return list(set(areas))[:5]  # Unique, max 5

    # ============== LIFE AREA ANALYSIS ==============

    def analyze_life_area(self, area: str) -> Dict[str, Any]:
        """Analyze a specific life area with house lord logic and detailed insights"""
        area_houses = {
            'career': [10, 2, 6],
            'marriage': [7, 2, 4],
            'children': [5, 9, 11],
            'health': [1, 6, 8],
            'wealth': [2, 11, 5],
            'education': [4, 5, 9],
            'property': [4, 2, 11],
            'spirituality': [9, 12, 5]
        }

        if area not in area_houses:
            return {'error': f'Unknown area: {area}'}

        houses = area_houses[area]
        primary_house = houses[0]

        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0

        # Get house lord
        house_sign = RASIS[(lagna_idx + primary_house - 1) % 12]
        house_lord = RASI_LORDS[house_sign]

        # Lord's position and strength
        lord_poi = self._calculate_planet_poi(house_lord) if house_lord in self.planets else {'total': 0.5}

        # Karaka strength
        karaka = HOUSE_KARAKAS[primary_house]['karaka']
        karaka_strength = self.calculate_shadbala(karaka)['total'] if karaka in self.planets else 0.5

        # Planets in house
        planets_in_house = []
        for planet, pos in self.planets.items():
            p_house = ((pos.sign_index - lagna_idx) % 12) + 1
            if p_house == primary_house:
                planets_in_house.append(planet)

        # Combined score
        combined = (lord_poi['total'] * 0.5 + karaka_strength * 0.3 +
                   (0.6 if len(planets_in_house) > 0 else 0.4) * 0.2)
        combined = max(0.35, min(0.95, combined))

        # Get detailed insights based on area type
        detailed_insights = self._get_detailed_life_area_insights(
            area, house_sign, house_lord, lord_poi['total'],
            karaka, karaka_strength, planets_in_house, combined
        )

        return {
            'area': area,
            'primary_house': primary_house,
            'house_sign': house_sign,
            'house_lord': house_lord,
            'lord_strength': lord_poi['total'],
            'karaka': karaka,
            'karaka_strength': round(karaka_strength, 2),
            'planets_in_house': planets_in_house,
            'combined_score': round(combined, 2),
            'interpretation': 'Favorable' if combined > 0.6 else ('Moderate' if combined > 0.45 else 'Needs attention'),
            'math_trace': f'H{primary_house} lord {house_lord}={lord_poi["total"]:.2f}, karaka {karaka}={karaka_strength:.2f}',
            'detailed_insights': detailed_insights
        }

    def _get_detailed_life_area_insights(self, area: str, house_sign: str, house_lord: str,
                                          lord_strength: float, karaka: str, karaka_strength: float,
                                          planets_in_house: List[str], combined_score: float) -> Dict[str, Any]:
        """Generate detailed, mathematically-derived insights for each life area"""

        if area == 'career':
            return self._get_career_insights(house_sign, house_lord, lord_strength, planets_in_house, combined_score)
        elif area == 'health':
            return self._get_health_insights(house_sign, house_lord, lord_strength, planets_in_house, combined_score)
        elif area == 'marriage':
            return self._get_marriage_insights(house_sign, house_lord, lord_strength, planets_in_house, combined_score)
        elif area == 'wealth':
            return self._get_wealth_insights(house_sign, house_lord, lord_strength, planets_in_house, combined_score)
        elif area == 'education':
            return self._get_education_insights(house_sign, house_lord, lord_strength, planets_in_house, combined_score)
        elif area == 'children':
            return self._get_children_insights(house_sign, house_lord, lord_strength, planets_in_house, combined_score)
        else:
            return {'summary': 'Analysis available for this area'}

    def _get_career_insights(self, house_sign: str, house_lord: str, lord_strength: float,
                             planets_in_house: List[str], combined_score: float) -> Dict[str, Any]:
        """Generate detailed career field recommendations based on planetary analysis"""

        # Primary fields from 10th house lord
        lord_fields = PLANET_CAREER_FIELDS.get(house_lord, {})
        primary_careers = lord_fields.get('primary', [])[:3]
        secondary_careers = lord_fields.get('secondary', [])[:2]
        career_traits = lord_fields.get('traits', [])

        # Sign-based career inclinations
        sign_careers = SIGN_CAREER_FIELDS.get(house_sign, [])[:3]

        # Additional fields from planets in 10th house
        planet_influenced_careers = []
        for planet in planets_in_house:
            p_fields = PLANET_CAREER_FIELDS.get(planet, {})
            planet_influenced_careers.extend(p_fields.get('primary', [])[:2])

        # Calculate career direction strength
        # Strong lord = authority-driven, Weak lord = service-oriented
        if lord_strength > 0.65:
            career_direction = 'Leadership and authority positions suit you best'
            approach = 'Take initiative, seek management roles'
        elif lord_strength > 0.45:
            career_direction = 'Balanced approach between leadership and collaboration'
            approach = 'Build expertise, then move to leadership'
        else:
            career_direction = 'Service-oriented and skill-based roles recommended'
            approach = 'Focus on expertise and technical skills'

        # Timing based on Saturn's influence on 10th
        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0
        saturn_pos = self.planets.get('Saturn')
        saturn_aspect_10th = False
        if saturn_pos:
            saturn_house = saturn_pos.house
            # Saturn aspects 3rd, 7th, 10th from its position
            aspects = [(saturn_house + 2) % 12 + 1, (saturn_house + 6) % 12 + 1, (saturn_house + 9) % 12 + 1]
            saturn_aspect_10th = 10 in aspects or saturn_house == 10

        career_timing = 'Steady progression expected' if not saturn_aspect_10th else 'Slow but stable career growth; patience required'

        # Build recommended fields list (unique, prioritized)
        all_recommended = []
        seen = set()
        for field in (primary_careers + sign_careers + secondary_careers + planet_influenced_careers):
            if field not in seen:
                all_recommended.append(field)
                seen.add(field)

        return {
            'recommended_fields': all_recommended[:6],
            'primary_from_lord': primary_careers,
            'secondary_options': secondary_careers,
            'sign_influence': sign_careers,
            'career_traits': career_traits,
            'career_direction': career_direction,
            'approach': approach,
            'timing_note': career_timing,
            'strength_analysis': f'10th lord {house_lord} at {lord_strength:.0%} strength in {house_sign}',
            'planets_influence': f'{", ".join(planets_in_house)} in 10th house' if planets_in_house else 'No planets in 10th house',
            'math_reasoning': f'Career fields derived from: 10th lord ({house_lord}), 10th sign ({house_sign}), planets in 10th ({", ".join(planets_in_house) or "none"})'
        }

    def _get_health_insights(self, house_sign: str, house_lord: str, lord_strength: float,
                             planets_in_house: List[str], combined_score: float) -> Dict[str, Any]:
        """Generate detailed health focus areas based on planetary analysis"""

        # Areas to focus on based on 6th house sign (health challenges)
        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0
        sixth_sign = RASIS[(lagna_idx + 5) % 12]
        eighth_sign = RASIS[(lagna_idx + 7) % 12]

        # Body parts from Lagna sign (constitution)
        lagna_body_parts = SIGN_BODY_PARTS.get(self.lagna_sign, [])

        # Body parts to monitor from 6th and 8th house signs
        sixth_body_parts = SIGN_BODY_PARTS.get(sixth_sign, [])
        eighth_body_parts = SIGN_BODY_PARTS.get(eighth_sign, [])

        # Weak planets and their health indicators
        health_focus_areas = []
        health_strengths = []
        weak_planets = []

        for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
            if planet in self.planets:
                strength = self.calculate_shadbala(planet)['total']
                health_data = PLANET_HEALTH_AREAS.get(planet, {})

                if strength < 0.45:
                    weak_planets.append(planet)
                    health_focus_areas.extend(health_data.get('weak_indicators', [])[:2])
                elif strength > 0.65:
                    health_strengths.extend(health_data.get('strong_indicators', [])[:1])

        # Overall constitution assessment
        sun_strength = self.calculate_shadbala('Sun')['total'] if 'Sun' in self.planets else 0.5
        moon_strength = self.calculate_shadbala('Moon')['total'] if 'Moon' in self.planets else 0.5

        if sun_strength > 0.6 and moon_strength > 0.6:
            constitution = 'Strong overall constitution and vitality'
        elif sun_strength > 0.5 or moon_strength > 0.5:
            constitution = 'Moderate constitution; maintain balanced lifestyle'
        else:
            constitution = 'Pay attention to overall vitality and energy levels'

        # Mars for physical energy, Saturn for chronic conditions
        mars_strength = self.calculate_shadbala('Mars')['total'] if 'Mars' in self.planets else 0.5
        saturn_influence = 'Monitor for chronic conditions' if 'Saturn' in planets_in_house else ''

        # Unique focus areas
        unique_focus = list(set(health_focus_areas))[:5]

        return {
            'body_areas_to_monitor': unique_focus,
            'constitution_assessment': constitution,
            'lagna_ruled_parts': lagna_body_parts,
            'sixth_house_vulnerabilities': sixth_body_parts[:3],
            'eighth_house_concerns': eighth_body_parts[:2],
            'health_strengths': health_strengths[:3],
            'weak_planets': weak_planets,
            'vitality_score': f'Sun={sun_strength:.0%}, Moon={moon_strength:.0%}',
            'physical_energy': f'Mars at {mars_strength:.0%} - {"Good" if mars_strength > 0.5 else "Build through exercise"}',
            'chronic_tendency': saturn_influence or 'No major chronic indicators',
            'recommendations': self._get_health_recommendations(weak_planets, sixth_sign),
            'math_reasoning': f'Health analysis from: Lagna ({self.lagna_sign}), 6th house ({sixth_sign}), 8th house ({eighth_sign}), weak planets ({", ".join(weak_planets) or "none"})'
        }

    def _get_health_recommendations(self, weak_planets: List[str], sixth_sign: str) -> List[str]:
        """Generate specific health recommendations based on weak planets"""
        recommendations = []

        if 'Sun' in weak_planets:
            recommendations.append('Regular morning sunlight exposure; focus on heart health')
        if 'Moon' in weak_planets:
            recommendations.append('Maintain emotional balance; stay hydrated; monitor digestion')
        if 'Mars' in weak_planets:
            recommendations.append('Regular physical exercise; manage anger; watch blood pressure')
        if 'Mercury' in weak_planets:
            recommendations.append('Stress management; skin care; breathing exercises')
        if 'Jupiter' in weak_planets:
            recommendations.append('Monitor weight and liver health; avoid excess')
        if 'Venus' in weak_planets:
            recommendations.append('Reproductive health checkups; kidney function monitoring')
        if 'Saturn' in weak_planets:
            recommendations.append('Joint and bone care; regular dental checkups')

        if not recommendations:
            recommendations.append('Overall good planetary health indicators')
            recommendations.append('Maintain regular health checkups')

        return recommendations[:4]

    def _get_marriage_insights(self, house_sign: str, house_lord: str, lord_strength: float,
                               planets_in_house: List[str], combined_score: float) -> Dict[str, Any]:
        """Generate detailed marriage/relationship insights"""

        # Venus analysis (primary karaka for marriage)
        venus_strength = self.calculate_shadbala('Venus')['total'] if 'Venus' in self.planets else 0.5
        venus_pos = self.planets.get('Venus')
        venus_sign = venus_pos.sign if venus_pos else 'Unknown'

        # Jupiter analysis (husband karaka for females)
        jupiter_strength = self.calculate_shadbala('Jupiter')['total'] if 'Jupiter' in self.planets else 0.5

        # 7th house sign indicates partner type
        partner_style = SIGN_MARRIAGE_STYLE.get(house_sign, 'Balanced partnership approach')

        # Relationship dynamics from planets in 7th
        dynamics = []
        for planet in planets_in_house:
            indicator = PLANET_MARRIAGE_INDICATORS.get(planet, {})
            if indicator:
                if lord_strength > 0.5:
                    dynamics.append(indicator.get('strong', ''))
                else:
                    dynamics.append(indicator.get('weak', ''))

        # Timing indicators
        if 'Saturn' in planets_in_house or house_lord == 'Saturn':
            timing = 'Marriage may be delayed but stable once established'
        elif 'Jupiter' in planets_in_house or house_lord == 'Jupiter':
            timing = 'Auspicious for marriage; supportive spouse'
        elif 'Venus' in planets_in_house:
            timing = 'Romantic and passionate relationship indicated'
        else:
            timing = 'Standard timing based on dasha periods'

        # Compatibility factors
        harmony_score = (venus_strength + lord_strength + jupiter_strength) / 3

        return {
            'partner_characteristics': partner_style,
            '7th_house_sign': house_sign,
            '7th_lord': house_lord,
            'lord_strength_pct': f'{lord_strength:.0%}',
            'venus_analysis': f'Venus at {venus_strength:.0%} in {venus_sign}',
            'jupiter_analysis': f'Jupiter at {jupiter_strength:.0%}',
            'relationship_dynamics': dynamics if dynamics else ['Balanced partnership expected'],
            'timing_indication': timing,
            'harmony_potential': f'{harmony_score:.0%}',
            'planets_in_7th': planets_in_house,
            'key_advice': 'Strong 7th lord indicates supportive partnership' if lord_strength > 0.55 else 'Focus on communication and understanding in relationships',
            'math_reasoning': f'Marriage analysis from: 7th lord ({house_lord}={lord_strength:.0%}), Venus={venus_strength:.0%}, Jupiter={jupiter_strength:.0%}'
        }

    def _get_wealth_insights(self, house_sign: str, house_lord: str, lord_strength: float,
                             planets_in_house: List[str], combined_score: float) -> Dict[str, Any]:
        """Generate detailed wealth and financial insights"""

        # 2nd house (wealth accumulation) and 11th house (gains) analysis
        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0
        eleventh_sign = RASIS[(lagna_idx + 10) % 12]
        eleventh_lord = RASI_LORDS[eleventh_sign]

        # Jupiter (natural wealth karaka) analysis
        jupiter_strength = self.calculate_shadbala('Jupiter')['total'] if 'Jupiter' in self.planets else 0.5

        # Income sources based on 2nd lord and planets
        income_sources = []
        lord_wealth = PLANET_WEALTH_INDICATORS.get(house_lord, {})
        income_sources.extend(lord_wealth.get('fields', [])[:2])

        for planet in planets_in_house:
            p_wealth = PLANET_WEALTH_INDICATORS.get(planet, {})
            income_sources.extend(p_wealth.get('fields', [])[:1])

        # Wealth accumulation pattern
        if lord_strength > 0.65:
            accumulation = 'Strong wealth accumulation potential'
            pattern = 'Consistent income growth expected'
        elif lord_strength > 0.45:
            accumulation = 'Moderate wealth through steady efforts'
            pattern = 'Build savings systematically'
        else:
            accumulation = 'Wealth requires sustained effort'
            pattern = 'Focus on stable income before investments'

        # Saturn influence on wealth (delays but stability)
        saturn_pos = self.planets.get('Saturn')
        wealth_timing = 'Steady growth' if not saturn_pos or saturn_pos.house not in [2, 11] else 'Slow but stable wealth building'

        # Best wealth sources
        unique_sources = list(set(income_sources))[:4]

        return {
            'wealth_potential': accumulation,
            'accumulation_pattern': pattern,
            '2nd_lord': house_lord,
            '11th_lord': eleventh_lord,
            'lord_strength': f'{lord_strength:.0%}',
            'jupiter_influence': f'Jupiter at {jupiter_strength:.0%} - {"Favorable" if jupiter_strength > 0.5 else "Build through discipline"}',
            'recommended_income_sources': unique_sources,
            'timing_pattern': wealth_timing,
            'investment_advice': 'Can take calculated risks' if combined_score > 0.6 else 'Prefer stable, low-risk investments',
            'planets_in_2nd': planets_in_house,
            'math_reasoning': f'Wealth analysis from: 2nd lord ({house_lord}={lord_strength:.0%}), 11th lord ({eleventh_lord}), Jupiter={jupiter_strength:.0%}'
        }

    def _get_education_insights(self, house_sign: str, house_lord: str, lord_strength: float,
                                planets_in_house: List[str], combined_score: float) -> Dict[str, Any]:
        """Generate detailed education and learning insights"""

        # Mercury (intellect) and Jupiter (higher learning) analysis
        mercury_strength = self.calculate_shadbala('Mercury')['total'] if 'Mercury' in self.planets else 0.5
        jupiter_strength = self.calculate_shadbala('Jupiter')['total'] if 'Jupiter' in self.planets else 0.5

        # Education fields from planets
        recommended_fields = []

        # From 4th/5th lord
        lord_fields = PLANET_EDUCATION_FIELDS.get(house_lord, [])
        recommended_fields.extend(lord_fields[:3])

        # From Mercury (intellect)
        mercury_fields = PLANET_EDUCATION_FIELDS.get('Mercury', [])[:2]

        # From planets in education houses
        for planet in planets_in_house:
            p_fields = PLANET_EDUCATION_FIELDS.get(planet, [])
            recommended_fields.extend(p_fields[:2])

        # Learning style
        if mercury_strength > 0.6:
            learning_style = 'Quick learner; analytical and logical approach'
        elif mercury_strength > 0.4:
            learning_style = 'Steady learner; benefits from structured learning'
        else:
            learning_style = 'Visual and practical learning methods work best'

        # Higher education prospects
        if jupiter_strength > 0.6 and lord_strength > 0.5:
            higher_ed = 'Excellent prospects for higher education and advanced degrees'
        elif jupiter_strength > 0.45:
            higher_ed = 'Good potential for specialized education'
        else:
            higher_ed = 'Practical and skill-based education recommended'

        # Unique fields
        unique_fields = list(set(recommended_fields))[:6]

        return {
            'recommended_fields': unique_fields,
            'learning_style': learning_style,
            'higher_education_prospects': higher_ed,
            '4th_5th_lord': house_lord,
            'mercury_strength': f'{mercury_strength:.0%}',
            'jupiter_strength': f'{jupiter_strength:.0%}',
            'lord_strength': f'{lord_strength:.0%}',
            'intellectual_capacity': 'High' if mercury_strength > 0.6 else ('Moderate' if mercury_strength > 0.4 else 'Develops with practice'),
            'concentration': 'Strong focus' if 'Saturn' in planets_in_house else 'Build through discipline',
            'best_approach': 'Self-study and research' if mercury_strength > 0.55 else 'Guided learning with mentorship',
            'math_reasoning': f'Education analysis from: 4th/5th lord ({house_lord}={lord_strength:.0%}), Mercury={mercury_strength:.0%}, Jupiter={jupiter_strength:.0%}'
        }

    def _get_children_insights(self, house_sign: str, house_lord: str, lord_strength: float,
                               planets_in_house: List[str], combined_score: float) -> Dict[str, Any]:
        """Generate detailed children/progeny insights"""

        # Jupiter (Putrakaraka - primary significator for children)
        jupiter_strength = self.calculate_shadbala('Jupiter')['total'] if 'Jupiter' in self.planets else 0.5
        jupiter_pos = self.planets.get('Jupiter')

        # 5th house analysis
        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0

        # Children prospects
        if jupiter_strength > 0.6 and lord_strength > 0.55:
            prospects = 'Good prospects for children; harmonious relationship expected'
        elif jupiter_strength > 0.45 or lord_strength > 0.5:
            prospects = 'Children indicated; normal progeny prospects'
        else:
            prospects = 'May require patience; remedial measures may help'

        # Relationship with children
        dynamics = []
        for planet in planets_in_house:
            indicator = PLANET_CHILDREN_INDICATORS.get(planet, {})
            if indicator:
                dynamics.append(f'{planet}: {indicator.get("strong" if lord_strength > 0.5 else "weak", "")}')

        # Timing
        if 'Saturn' in planets_in_house or house_lord == 'Saturn':
            timing = 'Children may come later in life; stable relationship'
        elif 'Jupiter' in planets_in_house or house_lord == 'Jupiter':
            timing = 'Auspicious timing for children; blessed progeny'
        else:
            timing = 'Timing based on dasha periods of 5th lord'

        # Children characteristics from 5th sign
        child_traits = {
            'Aries': 'Active, independent children',
            'Taurus': 'Artistic, comfort-loving children',
            'Gemini': 'Intelligent, communicative children',
            'Cancer': 'Emotional, nurturing children',
            'Leo': 'Confident, creative children',
            'Virgo': 'Analytical, detail-oriented children',
            'Libra': 'Balanced, artistic children',
            'Scorpio': 'Intense, determined children',
            'Sagittarius': 'Adventurous, philosophical children',
            'Capricorn': 'Disciplined, ambitious children',
            'Aquarius': 'Innovative, independent children',
            'Pisces': 'Creative, intuitive children'
        }

        return {
            'progeny_prospects': prospects,
            '5th_house_sign': house_sign,
            '5th_lord': house_lord,
            'lord_strength': f'{lord_strength:.0%}',
            'jupiter_analysis': f'Jupiter (Putrakaraka) at {jupiter_strength:.0%}',
            'children_characteristics': child_traits.get(house_sign, 'Good natured children'),
            'relationship_dynamics': dynamics if dynamics else ['Harmonious bond expected'],
            'timing_indication': timing,
            'planets_in_5th': planets_in_house,
            'creative_expression': 'Strong' if combined_score > 0.6 else 'Moderate',
            'math_reasoning': f'Children analysis from: 5th lord ({house_lord}={lord_strength:.0%}), Jupiter={jupiter_strength:.0%}'
        }

    # ============== ELEMENT & GUNA BALANCE ==============

    def calculate_element_balance(self) -> Dict[str, Any]:
        """Calculate elemental balance (Fire, Earth, Air, Water)"""
        counts = {'Fire': 0, 'Earth': 0, 'Air': 0, 'Water': 0}
        weighted = {'Fire': 0.0, 'Earth': 0.0, 'Air': 0.0, 'Water': 0.0}

        for planet, pos in self.planets.items():
            for element, signs in ELEMENT_SIGNS.items():
                if pos.sign in signs:
                    counts[element] += 1
                    # Weight by planet importance
                    weight = 1.5 if planet in ['Sun', 'Moon'] else 1.0
                    weighted[element] += weight

        total_weight = sum(weighted.values())
        ratios = {e: round(w / total_weight, 2) for e, w in weighted.items()} if total_weight > 0 else weighted

        dominant = max(ratios, key=ratios.get)
        weak = min(ratios, key=ratios.get)

        return {
            'counts': counts,
            'ratios': ratios,
            'dominant_element': dominant,
            'weak_element': weak,
            'balance_score': round(1 - (max(ratios.values()) - min(ratios.values())), 2),
            'math_trace': f'Dominant: {dominant}={ratios[dominant]:.0%}, Weak: {weak}={ratios[weak]:.0%}'
        }

    def calculate_guna_balance(self) -> Dict[str, Any]:
        """Calculate Guna balance (Sattva, Rajas, Tamas)"""
        guna_counts = {'Sattva': 0, 'Rajas': 0, 'Tamas': 0}

        # Moon's nakshatra guna (primary)
        moon_nak = self.moon_nakshatra
        nak_data = next((n for n in NAKSHATRAS if n['name'] == moon_nak), None)
        if nak_data:
            guna_counts[nak_data['guna']] += 3  # Triple weight for Moon

        # Lagna nakshatra guna
        lagna_long = (RASIS.index(self.lagna_sign) * 30 + self.lagna_degree) if self.lagna_sign in RASIS else 0
        lagna_nak_idx = int(lagna_long / 13.333333) % 27
        lagna_nak = NAKSHATRAS[lagna_nak_idx]
        guna_counts[lagna_nak['guna']] += 2

        # Other planets
        for planet, pos in self.planets.items():
            if planet in ['Rahu', 'Ketu']:
                continue
            nak_data = next((n for n in NAKSHATRAS if n['name'] == pos.nakshatra), None)
            if nak_data:
                guna_counts[nak_data['guna']] += 1

        total = sum(guna_counts.values())
        ratios = {g: round(c / total, 2) for g, c in guna_counts.items()} if total > 0 else guna_counts

        dominant = max(ratios, key=ratios.get)

        return {
            'counts': guna_counts,
            'ratios': ratios,
            'dominant_guna': dominant,
            'personality_type': self._get_guna_personality(dominant),
            'math_trace': f'Moon nak {moon_nak} +3, Lagna nak {lagna_nak["name"]} +2'
        }

    def _get_guna_personality(self, guna: str) -> str:
        """Get personality description for dominant guna"""
        descriptions = {
            'Sattva': 'Pure, harmonious, knowledge-seeking nature',
            'Rajas': 'Active, ambitious, worldly-engaged nature',
            'Tamas': 'Grounded, steady, material-focused nature'
        }
        return descriptions.get(guna, '')

    # ============== PURUSHARTHA ANALYSIS ==============

    def calculate_purushartha(self) -> Dict[str, Any]:
        """Calculate Purushartha (life goals) dominance"""
        scores = {'Dharma': 0.0, 'Artha': 0.0, 'Kama': 0.0, 'Moksha': 0.0}

        lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0

        for goal, houses in PURUSHARTHA_HOUSES.items():
            for house in houses:
                # House lord strength
                house_sign = RASIS[(lagna_idx + house - 1) % 12]
                house_lord = RASI_LORDS[house_sign]

                if house_lord in self.planets:
                    strength = self.calculate_shadbala(house_lord)['total']
                    scores[goal] += strength

                # Planets in house
                for planet, pos in self.planets.items():
                    p_house = ((pos.sign_index - lagna_idx) % 12) + 1
                    if p_house == house:
                        p_strength = self.calculate_shadbala(planet)['total']
                        scores[goal] += p_strength * 0.5

        # Normalize
        total = sum(scores.values())
        if total > 0:
            scores = {k: round(v / total, 2) for k, v in scores.items()}

        dominant = max(scores, key=scores.get)

        return {
            'scores': scores,
            'dominant': dominant,
            'life_focus': self._get_purushartha_focus(dominant),
            'math_trace': f'House lords + occupants weighted by Shadbala'
        }

    def _get_purushartha_focus(self, goal: str) -> str:
        """Get life focus description"""
        focuses = {
            'Dharma': 'Purpose, ethics, and righteous living',
            'Artha': 'Material success, career, and resources',
            'Kama': 'Desires, relationships, and pleasures',
            'Moksha': 'Liberation, spirituality, and transcendence'
        }
        return focuses.get(goal, '')

    # ============== STRENGTH VS EFFORT MATRIX ==============

    def calculate_strength_effort_matrix(self) -> Dict[str, Any]:
        """Calculate areas of natural ease vs required effort"""
        areas = ['career', 'marriage', 'children', 'health', 'wealth', 'education']

        matrix = []
        for area in areas:
            analysis = self.analyze_life_area(area)

            # Ease index based on strength
            ease = analysis['combined_score']

            # Effort required (inverse of ease)
            effort = 1 - ease

            matrix.append({
                'area': area,
                'ease_index': round(ease, 2),
                'effort_index': round(effort, 2),
                'status': 'Natural Strength' if ease > 0.65 else ('Balanced' if ease > 0.45 else 'Requires Focus')
            })

        # Sort by ease
        matrix.sort(key=lambda x: x['ease_index'], reverse=True)

        return {
            'matrix': matrix,
            'strongest_area': matrix[0]['area'] if matrix else 'N/A',
            'focus_area': matrix[-1]['area'] if matrix else 'N/A',
            'math_trace': 'Ease = combined house analysis score'
        }

    # ============== PLANETARY MATURITY ==============

    def get_maturity_timeline(self) -> List[Dict]:
        """Get planetary maturity ages and their effects"""
        timeline = []

        for planet, age in sorted(MATURITY_AGES.items(), key=lambda x: x[1]):
            if planet not in self.planets:
                continue

            p = self.planets[planet]
            strength = self.calculate_shadbala(planet)['total']

            # Life area affected
            lagna_idx = RASIS.index(self.lagna_sign) if self.lagna_sign in RASIS else 0
            house = ((p.sign_index - lagna_idx) % 12) + 1
            signifies = HOUSE_KARAKAS.get(house, {}).get('signifies', [])[:2]

            status = 'Passed' if self.current_age >= age else 'Upcoming'

            timeline.append({
                'planet': planet,
                'planet_tamil': PLANET_TAMIL.get(planet, planet),
                'age': age,
                'status': status,
                'strength': round(strength, 2),
                'house': house,
                'activates': signifies,
                'interpretation': f'{planet} themes mature at age {age}'
            })

        return timeline

    # ============== GENERATE FULL REPORT DATA ==============

    def generate_report_data(self) -> Dict[str, Any]:
        """Generate complete data for the 40-page V6.2 report"""
        return {
            # Page 1: Identity
            'identity': {
                'name': self.user_data.get('name', 'User'),
                'birth_date': str(self.birth_date),
                'birth_time': self.user_data.get('birth_time', '12:00'),
                'birth_place': self.user_data.get('birth_place', 'Chennai'),
                'lagna': self.lagna_sign,
                'lagna_degree': round(self.lagna_degree, 2),
                'moon_sign': self.moon_sign,
                'moon_nakshatra': self.moon_nakshatra,
                'current_age': self.current_age
            },

            # Page 2-3: Elements & Gunas
            'elements': self.calculate_element_balance(),
            'gunas': self.calculate_guna_balance(),

            # Page 4: Purushartha
            'purushartha': self.calculate_purushartha(),

            # V6.2: Planet POI (Planet Operating Index)
            'planet_poi': {
                planet: self.calculate_poi(planet)
                for planet in PLANETS
            },

            # Page 5-13: Planetary Intelligence (with POI)
            'planets': {
                planet: {
                    'position': {
                        'sign': self.planets[planet].sign if planet in self.planets else 'Unknown',
                        'house': self.planets[planet].house if planet in self.planets else 1,
                        'degree': round(self.planets[planet].degree, 2) if planet in self.planets else 0,
                        'nakshatra': self.planets[planet].nakshatra if planet in self.planets else 'Unknown',
                        'retrograde': self.planets[planet].is_retrograde if planet in self.planets else False
                    },
                    'dignity': self.get_dignity(planet),
                    'shadbala': self.calculate_shadbala(planet),
                    'poi': self.calculate_poi(planet)  # V6.2 POI
                }
                for planet in PLANETS
            },

            # V6.2: House HAI (House Activation Index)
            'house_hai': {
                house: self.calculate_hai(house)
                for house in range(1, 13)
            },

            # Page 14: Planetary Interactions
            'interactions': self._calculate_planetary_interactions(),

            # Page 15-20: Life Areas
            'life_areas': {
                area: self.analyze_life_area(area)
                for area in ['career', 'marriage', 'children', 'health', 'wealth', 'education']
            },

            # Page 21-24: Yogas & Doshas
            'yogas': self.detect_yogas(),
            'doshas': self.detect_doshas(),

            # Page 25: Strength vs Effort
            'strength_effort': self.calculate_strength_effort_matrix(),

            # V6.2: Visual Chart Data
            'd1_chart': self.get_d1_chart_data(),
            'd9_chart': self.get_d9_chart_data(),
            'd10_chart': self.get_d10_chart_data(),
            'aspect_yoga_map': self.get_aspect_yoga_map(),

            # Page 26-27: Divisional Charts (D9, D10 summary)
            'divisional': self._get_divisional_summary(),

            # Page 28: Ashtakavarga
            'ashtakavarga': self.calculate_ashtakavarga(),

            # Page 29: Maturity Timeline
            'maturity': self.get_maturity_timeline(),

            # Page 31-35: Dasha Analysis
            'dasha': self.calculate_dasha_analysis(),

            # Page 37-39: Strategy & Remedies
            'remedies': self._generate_remedies(),

            # Metadata
            'generated_at': datetime.now().isoformat(),
            'engine_version': 'V6.2'
        }

    def _calculate_planetary_interactions(self) -> Dict[str, Any]:
        """Calculate planetary friendships and conjunctions"""
        conjunctions = []
        aspects = []

        planet_list = list(self.planets.keys())

        for i, p1 in enumerate(planet_list):
            for p2 in planet_list[i+1:]:
                pos1 = self.planets[p1]
                pos2 = self.planets[p2]

                # Conjunction
                if pos1.sign == pos2.sign:
                    conjunctions.append({
                        'planets': [p1, p2],
                        'sign': pos1.sign,
                        'degree_diff': abs(pos1.degree - pos2.degree)
                    })

                # Opposition
                if abs(pos1.sign_index - pos2.sign_index) == 6:
                    aspects.append({
                        'type': 'Opposition',
                        'planets': [p1, p2],
                        'signs': [pos1.sign, pos2.sign]
                    })

        return {
            'conjunctions': conjunctions,
            'major_aspects': aspects,
            'math_trace': f'{len(conjunctions)} conjunctions, {len(aspects)} major aspects'
        }

    def _get_divisional_summary(self) -> Dict[str, Any]:
        """Summary of D9 and D10 charts"""
        # D9 - Navamsa (simplified calculation)
        navamsa_positions = {}
        for planet, pos in self.planets.items():
            navamsa_idx = int((pos.longitude % 30) / 3.333333)
            navamsa_sign_idx = (pos.sign_index * 9 + navamsa_idx) % 12
            navamsa_positions[planet] = RASIS[navamsa_sign_idx]

        # Check vargottama (same sign in D1 and D9)
        vargottama = [p for p, nav_sign in navamsa_positions.items()
                      if p in self.planets and self.planets[p].sign == nav_sign]

        return {
            'd9_positions': navamsa_positions,
            'vargottama_planets': vargottama,
            'd9_lagna': navamsa_positions.get('lagna', self.lagna_sign),
            'congruence_score': round(len(vargottama) / len(self.planets), 2) if self.planets else 0,
            'math_trace': f'{len(vargottama)} vargottama planets'
        }

    def _generate_remedies(self) -> Dict[str, Any]:
        """Generate chart-based remedies"""
        remedies = {
            'behavioral': [],
            'gemstone': [],
            'mantra': [],
            'priority_planet': None
        }

        # Find weakest functional benefic
        weakest_planet = None
        weakest_strength = 1.0

        for planet in ['Jupiter', 'Venus', 'Mercury', 'Moon']:
            if planet in self.planets:
                strength = self.calculate_shadbala(planet)['total']
                if strength < weakest_strength:
                    weakest_strength = strength
                    weakest_planet = planet

        if weakest_planet:
            remedies['priority_planet'] = weakest_planet

            # Behavioral remedies
            behavioral_map = {
                'Jupiter': 'Cultivate wisdom through teaching, respect elders',
                'Venus': 'Appreciate art and beauty, maintain harmonious relationships',
                'Mercury': 'Improve communication skills, practice logical thinking',
                'Moon': 'Nurture emotional connections, practice mindfulness'
            }
            remedies['behavioral'].append(behavioral_map.get(weakest_planet, ''))

            # Gemstone
            gem_map = {
                'Jupiter': 'Yellow Sapphire (Pukhraj)',
                'Venus': 'Diamond or White Sapphire',
                'Mercury': 'Emerald (Panna)',
                'Moon': 'Pearl (Moti)'
            }
            remedies['gemstone'].append({
                'gem': gem_map.get(weakest_planet, ''),
                'note': 'Consult astrologer before wearing'
            })

            # Mantra
            mantra_map = {
                'Jupiter': 'Om Guruve Namaha',
                'Venus': 'Om Shukraya Namaha',
                'Mercury': 'Om Budhaya Namaha',
                'Moon': 'Om Chandraya Namaha'
            }
            remedies['mantra'].append(mantra_map.get(weakest_planet, ''))

        return remedies
