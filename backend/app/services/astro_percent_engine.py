"""
Astro-Percent Engine v3.0 - South Indian Style Prediction Scoring
==================================================================
A strictly mathematical astrology scoring engine (0-100) using
monthly ephemeris data, verified yogas with longitude checks,
nakshatra/pada traits, eclipse penalties, and weighted scoring.

v3.0 Enhancements (Monthly Ephemeris Engine):
- Monthly ephemeris data for all planets with degree-level precision
- Eclipse detection and scoring penalties (solar: -1.0, lunar: -1.5)
- Detailed Jupiter transit table (1/5/9: +8, kendra: +7, 2/11: +6, etc.)
- Detailed Saturn transit rules (sade_sati: -3, kantaka: -2, ashtama: -3)
- Enhanced retrograde penalties (Mercury: -0.5, Venus: -0.7, Mars: -0.8, etc.)
- Peak month detection (3 consecutive good months: 1.03-1.08 boost)
- Worst month detection (2-3 consecutive bad months: 0.92-0.97 penalty)
- Validated yoga detection with actual longitude checks (no assumed yogas)
- Enhanced navamsa cross-validation with boost/penalty modifiers
- Rahu/Ketu axis scoring with 1/7 axis penalty
- Provenance v3.0 with full calculation trace

v2.3 Features (Retained):
- Dynamic planetary movement with monthly transit calculation
- Nakshatra element traits (Agni, Prithvi, Vayu, Jala) with modifiers
- Pada element modifiers affecting transit/dasha scoring

v2.2 Features (Retained):
- Updated weight allocation for better accuracy
- Nakshatra-specific meta multipliers
- Post-Jupiter transit boost logic
- Explicit planet dignity numeric mapping (0-10 scale)

v2.1 Features (Retained):
- Non-linear smoothing (power 0.92)
- Enhanced Dasha interaction formula
- Sigmoid smoothing for transits
- Yoga rarity multiplier & diminishing returns
- Domain-specific weight overrides
- Monte Carlo uncertainty estimation
- Meta-rules for contradiction resolution
- Confidence scoring & provenance tracking

Weight Allocation:
- Dasha/Bhukti strength: 25%
- House + Karaka strength: 18%
- Planetary dignity & Shadbala: 12%
- Transits (Gocharam): 20%
- Yogas / Doshas: 12%
- Navamsa support: 13%

Final Formula:
final_score = (dasha*0.25 + house*0.18 + planet*0.12 + transit*0.20 + yoga*0.12 + navamsa*0.13) * 100 * meta_multiplier
"""

from datetime import datetime, date
from typing import Dict, List, Any, Optional
import math
import hashlib
import random
from statistics import mean, median, stdev


class AstroPercentEngine:
    """South Indian Style Astrology Scoring Engine v3.0"""

    # ==================== CONFIGURATION v3.0 ====================

    ENGINE_VERSION = "3.0"

    # Default weights for final score calculation (v3.0)
    WEIGHTS = {
        'dasha': 0.25,
        'house': 0.18,
        'planet_strength': 0.12,
        'transit': 0.20,
        'yoga': 0.12,
        'navamsa': 0.13
    }

    # Domain-specific weight overrides
    DOMAIN_WEIGHTS = {
        'career': {'dasha': 0.22, 'house': 0.28, 'planet_strength': 0.15, 'transit': 0.25, 'yoga': 0.05, 'navamsa': 0.05},
        'finance': {'dasha': 0.22, 'house': 0.25, 'planet_strength': 0.15, 'transit': 0.20, 'yoga': 0.10, 'navamsa': 0.08},
        'health': {'dasha': 0.18, 'house': 0.30, 'planet_strength': 0.20, 'transit': 0.22, 'yoga': 0.05, 'navamsa': 0.05},
        'relationships': {'dasha': 0.18, 'house': 0.25, 'planet_strength': 0.12, 'transit': 0.10, 'yoga': 0.10, 'navamsa': 0.25},
        'love': {'dasha': 0.18, 'house': 0.25, 'planet_strength': 0.12, 'transit': 0.10, 'yoga': 0.10, 'navamsa': 0.25},
    }

    # Non-linear adjustments
    NON_LINEAR_CONFIG = {
        'final_smoothing_power': 0.92,
        'apply_smoothing': True
    }

    # Component scale: each component outputs 0-10, then normalized to 0-1
    COMPONENT_SCALE = {
        'min': 0,
        'max': 10
    }

    # Normalization ranges for each component (raw score to 0-10)
    NORMALIZATION = {
        'dasha': {'min': -5, 'max': 32},
        'house': {'min': -5, 'max': 25},
        'planet_strength': {'min': 0, 'max': 1},  # Already 0-1 scale
        'transit': {'min': -10, 'max': 20},
        'yoga': {'min': -6, 'max': 10},
        'navamsa': {'min': 0, 'max': 10}
    }

    # ==================== V3.0 DIGNITY TABLE ====================
    # Updated dignity scores per v3.0 spec (0-10 scale)
    DIGNITY_TABLE_V3 = {
        'exalted': 10,
        'own': 9,
        'friendly': 7,
        'neutral': 5,
        'enemy': 3,
        'debilitated': 1
    }

    # ==================== V3.0 JUPITER TRANSIT TABLE ====================
    # Jupiter transit scoring based on house from Moon/Lagna
    JUPITER_TRANSIT_TABLE_V3 = {
        'trikona': {'houses': [1, 5, 9], 'score': 8, 'label': '1/5/9 சிறப்பு'},
        'kendra': {'houses': [4, 7, 10], 'score': 7, 'label': 'கேந்திரம் நல்லது'},
        'dhana': {'houses': [2, 11], 'score': 6, 'label': '2/11 சரி'},
        'mixed': {'houses': [3, 12], 'score': 4, 'label': '3/12 கலப்பு'},
        'bad': {'houses': [6, 8], 'score': 2, 'label': '6/8 சவால்'}
    }

    # ==================== V3.0 SATURN TRANSIT RULES ====================
    SATURN_TRANSIT_RULES_V3 = {
        'sade_sati': {
            'houses': [12, 1, 2],  # 12th, 1st, 2nd from Moon
            'penalty': -3,
            'phases': {
                12: {'name': 'rising', 'tamil': 'ஆரம்பம்', 'penalty': -2.5},
                1: {'name': 'peak', 'tamil': 'உச்சம்', 'penalty': -3.0},
                2: {'name': 'setting', 'tamil': 'முடிவு', 'penalty': -2.0}
            }
        },
        'kantaka': {
            'houses': [4, 7, 10],  # Kendra positions
            'penalty': -2,
            'label': 'கண்டக சனி'
        },
        'ashtama': {
            'houses': [8],
            'penalty': -3,
            'label': 'அஷ்டம சனி'
        },
        'favorable': {
            'houses': [3, 6, 11],
            'bonus': +2,
            'label': 'சாதகமான சனி'
        }
    }

    # ==================== V3.0 RETROGRADE PENALTIES ====================
    # Per spec: specific penalties for each planet during retrograde
    RETROGRADE_PENALTIES_V3 = {
        'Mercury': -0.5,
        'Venus': -0.7,
        'Mars': -0.8,
        'Jupiter': -1.0,
        'Saturn': -1.0
    }

    # ==================== V3.0 ECLIPSE PENALTIES ====================
    ECLIPSE_PENALTIES_V3 = {
        'solar': -1.0,
        'lunar': -1.5
    }

    # Sensitive houses for eclipse impact (kendras and Moon's house)
    ECLIPSE_SENSITIVE_HOUSES = [1, 4, 7, 10]

    # ==================== V3.0 YOGA VALUES ====================
    YOGA_VALUES_V3 = {
        'strong': 4,
        'medium': 2,
        'weak': 1
    }

    # ==================== V3.0 NAVAMSA MODIFIERS ====================
    NAVAMSA_MODIFIERS_V3 = {
        'boost': +2,   # Weak natal but strong D9
        'penalty': -2  # Strong natal but weak D9
    }

    # ==================== V3.0 META MULTIPLIERS ====================
    META_MULTIPLIERS_V3 = {
        'nakshatra_range': {'min': 0.97, 'max': 1.05},
        'pada_range': {'min': 0.98, 'max': 1.06},
        'peak_month': {
            'condition': '3 consecutive strong months',
            'range': {'min': 1.03, 'max': 1.08}
        },
        'worst_month': {
            'condition': '2-3 consecutive bad months',
            'range': {'min': 0.92, 'max': 0.97}
        }
    }

    # Peak/Worst month thresholds
    PEAK_MONTH_THRESHOLD = 65  # Score above this is "strong"
    WORST_MONTH_THRESHOLD = 40  # Score below this is "bad"

    # ==================== META MULTIPLIERS (v3.0 Enhanced) ====================

    # Nakshatra element traits with specific modifiers (v3.0)
    # Each nakshatra has: element, lord, traits, base_multiplier, and transit_modifiers
    NAKSHATRA_TRAITS = {
        'Ashwini': {
            'element': 'Agni', 'lord': 'Ketu', 'base_multiplier': 1.0,
            'traits': 'speed, healing, beginnings',
            'transit_boost': {'Mars': 0.05, 'Sun': 0.03, 'Ketu': 0.04}
        },
        'Bharani': {
            'element': 'Prithvi', 'lord': 'Venus', 'base_multiplier': 1.0,
            'traits': 'restraint, transformation',
            'transit_boost': {'Venus': 0.06, 'Saturn': 0.02}
        },
        'Krittika': {
            'element': 'Agni', 'lord': 'Sun', 'base_multiplier': 1.02,
            'traits': 'purification, cutting',
            'transit_boost': {'Sun': 0.07, 'Mars': 0.04}
        },
        'Rohini': {
            'element': 'Prithvi', 'lord': 'Moon', 'base_multiplier': 1.03,
            'traits': 'growth, fertility, beauty',
            'transit_boost': {'Moon': 0.07, 'Venus': 0.05}
        },
        'Mrigashira': {
            'element': 'Prithvi', 'lord': 'Mars', 'base_multiplier': 1.0,
            'traits': 'seeking, curiosity',
            'transit_boost': {'Mars': 0.04, 'Mercury': 0.03}
        },
        'Ardra': {
            'element': 'Vayu', 'lord': 'Rahu', 'base_multiplier': 0.98,
            'traits': 'storm, transformation, effort',
            'transit_boost': {'Rahu': 0.03}, 'transit_penalty': {'Saturn': -0.03}
        },
        'Punarvasu': {
            'element': 'Vayu', 'lord': 'Jupiter', 'base_multiplier': 1.02,
            'traits': 'renewal, return, abundance',
            'transit_boost': {'Jupiter': 0.06}
        },
        'Pushya': {
            'element': 'Jala', 'lord': 'Saturn', 'base_multiplier': 1.05,
            'traits': 'nourishment, peak, auspicious',
            'transit_boost': {'Saturn': 0.04, 'Jupiter': 0.04, 'Moon': 0.03}
        },
        'Ashlesha': {
            'element': 'Jala', 'lord': 'Mercury', 'base_multiplier': 0.97,
            'traits': 'embracing, mystical, cunning',
            'transit_boost': {'Mercury': 0.03, 'Rahu': 0.02}, 'transit_penalty': {'Jupiter': -0.02}
        },
        'Magha': {
            'element': 'Agni', 'lord': 'Ketu', 'base_multiplier': 1.02,
            'traits': 'royalty, ancestors, authority',
            'transit_boost': {'Sun': 0.05, 'Ketu': 0.04}
        },
        'Purva Phalguni': {
            'element': 'Agni', 'lord': 'Venus', 'base_multiplier': 1.0,
            'traits': 'enjoyment, relaxation, creativity',
            'transit_boost': {'Venus': 0.06, 'Sun': 0.03}
        },
        'Uttara Phalguni': {
            'element': 'Prithvi', 'lord': 'Sun', 'base_multiplier': 1.02,
            'traits': 'patronage, contracts, friendships',
            'transit_boost': {'Sun': 0.05, 'Jupiter': 0.03}
        },
        'Hasta': {
            'element': 'Prithvi', 'lord': 'Moon', 'base_multiplier': 1.03,
            'traits': 'skill, craftsmanship, dexterity',
            'transit_boost': {'Moon': 0.05, 'Mercury': 0.05}
        },
        'Chitra': {
            'element': 'Agni', 'lord': 'Mars', 'base_multiplier': 1.0,
            'traits': 'brilliance, architecture, creation',
            'transit_boost': {'Mars': 0.05, 'Venus': 0.03}
        },
        'Swathi': {
            'element': 'Vayu', 'lord': 'Rahu', 'base_multiplier': 1.02,
            'traits': 'independence, intelligence, movement',
            'transit_boost': {'Mercury': 0.05, 'Venus': 0.05, 'Rahu': 0.03}
        },
        'Vishakha': {
            'element': 'Agni', 'lord': 'Jupiter', 'base_multiplier': 1.0,
            'traits': 'determination, focus, achievement',
            'transit_boost': {'Jupiter': 0.05, 'Mars': 0.03}
        },
        'Anuradha': {
            'element': 'Jala', 'lord': 'Saturn', 'base_multiplier': 1.02,
            'traits': 'devotion, friendship, success',
            'transit_boost': {'Saturn': 0.04, 'Venus': 0.03}
        },
        'Jyeshtha': {
            'element': 'Vayu', 'lord': 'Mercury', 'base_multiplier': 0.98,
            'traits': 'eldest, chief, protective',
            'transit_boost': {'Mercury': 0.04}, 'transit_penalty': {'Mars': -0.02}
        },
        'Mula': {
            'element': 'Agni', 'lord': 'Ketu', 'base_multiplier': 0.97,
            'traits': 'root, destruction, foundation',
            'transit_boost': {'Ketu': 0.04}, 'transit_penalty': {'Jupiter': -0.03}
        },
        'Purva Ashadha': {
            'element': 'Jala', 'lord': 'Venus', 'base_multiplier': 1.0,
            'traits': 'invincibility, declaration',
            'transit_boost': {'Venus': 0.06, 'Jupiter': 0.03}
        },
        'Uttara Ashadha': {
            'element': 'Prithvi', 'lord': 'Sun', 'base_multiplier': 1.02,
            'traits': 'final victory, universal',
            'transit_boost': {'Sun': 0.05, 'Saturn': 0.03}
        },
        'Shravana': {
            'element': 'Vayu', 'lord': 'Moon', 'base_multiplier': 1.03,
            'traits': 'listening, learning, connection',
            'transit_boost': {'Moon': 0.05, 'Mercury': 0.04, 'Jupiter': 0.03}
        },
        'Dhanishta': {
            'element': 'Prithvi', 'lord': 'Mars', 'base_multiplier': 1.0,
            'traits': 'wealth, music, fame',
            'transit_boost': {'Mars': 0.05, 'Saturn': 0.03}
        },
        'Shatabhisha': {
            'element': 'Vayu', 'lord': 'Rahu', 'base_multiplier': 0.98,
            'traits': 'healing, veiling, 100 physicians',
            'transit_boost': {'Rahu': 0.04, 'Saturn': 0.02}, 'transit_penalty': {'Sun': -0.02}
        },
        'Purva Bhadrapada': {
            'element': 'Agni', 'lord': 'Jupiter', 'base_multiplier': 0.98,
            'traits': 'fire, purification, transformation',
            'transit_boost': {'Jupiter': 0.04}, 'transit_penalty': {'Saturn': -0.02}
        },
        'Uttara Bhadrapada': {
            'element': 'Jala', 'lord': 'Saturn', 'base_multiplier': 1.02,
            'traits': 'depth, wisdom, cosmic serpent',
            'transit_boost': {'Saturn': 0.05, 'Jupiter': 0.04}
        },
        'Revati': {
            'element': 'Prithvi', 'lord': 'Mercury', 'base_multiplier': 1.03,
            'traits': 'nourishment, wealth, journeys',
            'transit_boost': {'Mercury': 0.05, 'Jupiter': 0.04, 'Venus': 0.03}
        }
    }

    # Simple multiplier lookup (backward compatibility)
    NAKSHATRA_MULTIPLIERS = {k: v['base_multiplier'] for k, v in NAKSHATRA_TRAITS.items()}

    # Pada element modifiers (v2.3) - each pada corresponds to an element
    # Pada 1: Agni (Aries navamsa), Pada 2: Prithvi (Taurus navamsa)
    # Pada 3: Vayu (Gemini navamsa), Pada 4: Jala (Cancer navamsa)
    PADA_ELEMENT_MODIFIERS = {
        1: {  # Agni (Fire) pada
            'element': 'Agni',
            'base_adjustment': 1.0,
            'transit_boost': {'Mars': 0.03, 'Sun': 0.03},
            'dasha_boost': {'Mars': 0.03, 'Sun': 0.02, 'Ketu': 0.02},
            'description': 'Adds +3% for Mars or Sun favourable transits'
        },
        2: {  # Prithvi (Earth) pada
            'element': 'Prithvi',
            'base_adjustment': 1.01,
            'score_smoothing': 0.85,  # Stabilizes score variation
            'transit_boost': {'Venus': 0.03, 'Mercury': 0.02},
            'description': 'Stabilizes score variation; smooths extremes'
        },
        3: {  # Vayu (Air) pada
            'element': 'Vayu',
            'base_adjustment': 1.0,
            'score_amplification': 1.05,  # Amplify swings ±5%
            'transit_boost': {'Mercury': 0.04, 'Rahu': 0.03},
            'description': 'Amplifies swings (±5%) depending on Mercury/Rahu'
        },
        4: {  # Jala (Water) pada - Moksha pada
            'element': 'Jala',
            'base_adjustment': 1.02,
            'transit_boost': {'Venus': 0.05, 'Moon': 0.04, 'Jupiter': 0.03},
            'saturn_reduction': 0.03,  # Reduce Saturn harshness by 3%
            'description': 'Boosts Venus periods by +5%, reduces Saturn harshness by -3%'
        }
    }

    # Simple pada adjustments (backward compatibility)
    PADA_ADJUSTMENTS = {k: v['base_adjustment'] for k, v in PADA_ELEMENT_MODIFIERS.items()}

    # Jupiter transit boost (when Jupiter is in favorable houses from Moon)
    JUPITER_TRANSIT_BOOST = {
        'favorable_houses': [2, 5, 7, 9, 11],  # Houses from Moon
        'boost_multiplier': 1.08
    }

    # Saturn transit penalty (when Saturn is in challenging houses)
    SATURN_TRANSIT_PENALTY = {
        'challenging_houses': [1, 4, 8, 12],  # Ashtama Shani, etc.
        'penalty_multiplier': 0.95
    }

    # ==================== V2.3 TRANSIT ENHANCEMENTS ====================

    # Detailed transit scoring by house (v2.3)
    # Score ranges: positive (8-10), mixed (4-7), negative (0-3)
    TRANSIT_HOUSE_SCORES = {
        'Jupiter': {
            'excellent': [1, 2, 4, 5, 7, 9, 10, 11],  # Score 8-10
            'good': [3],  # Score 6-7
            'negative': [6, 8, 12]  # Score 0-4
        },
        'Saturn': {
            'favorable': [3, 6, 11],  # Score 6-8
            'neutral': [2, 5, 10],  # Score 4-6
            'challenging': [1, 4, 7, 8, 12]  # Score 0-4 (Sade-Sati, Ashtama)
        },
        'Rahu': {
            'favorable': [3, 6, 10, 11],  # Score 6-8
            'neutral': [1, 2, 5, 9],  # Score 4-6
            'unfavorable': [4, 7, 8, 12]  # Score 0-4
        },
        'Ketu': {
            'favorable': [3, 6, 10, 11],  # Score 6-8
            'neutral': [1, 2, 5, 9],  # Score 4-6
            'unfavorable': [4, 7, 8, 12]  # Score 0-4
        },
        'Mars': {
            'favorable': [1, 2, 3, 6, 10, 11],
            'neutral': [4, 5, 9],
            'unfavorable': [7, 8, 12]
        }
    }

    # Retrograde penalty configuration (v2.3)
    # Retrograde reduces strength by -10% to -25%
    RETROGRADE_PENALTIES = {
        'Mercury': {'base_penalty': 0.90, 'heavy_penalty': 0.85},  # -10% to -15%
        'Venus': {'base_penalty': 0.92, 'heavy_penalty': 0.88},    # -8% to -12%
        'Mars': {'base_penalty': 0.88, 'heavy_penalty': 0.80},     # -12% to -20%
        'Jupiter': {'base_penalty': 0.90, 'heavy_penalty': 0.85},  # -10% to -15%
        'Saturn': {'base_penalty': 0.85, 'heavy_penalty': 0.75},   # -15% to -25%
        'default': {'base_penalty': 0.90, 'heavy_penalty': 0.85}
    }

    # Peak month multiplier detection (v2.3)
    # When Jupiter ingress or dasha peak month is detected
    PEAK_MONTH_CONFIG = {
        'jupiter_ingress_boost': 1.05,  # 5% boost during Jupiter sign change month
        'dasha_change_boost': 1.03,     # 3% boost during favorable dasha change
        'peak_transit_boost': 1.08,     # 8% boost when best 3 months detected
        'max_peak_multiplier': 1.10     # Cap peak boost at 10%
    }

    # Sade-Sati phase multipliers
    SADE_SATI_PHASES = {
        'rising': 0.95,    # Saturn 12th from Moon - beginning phase
        'peak': 0.88,      # Saturn conjunct Moon - peak phase
        'setting': 0.92,   # Saturn 2nd from Moon - ending phase
        'none': 1.0
    }

    # ==================== DASHA CONFIG (Enhanced v2.1) ====================

    # Dasha formula: Dasha_total = (Base*0.45) + (Dignity*0.30) + (HouseEffect*0.15) + (AspectImpact*0.10) + InteractionBonus
    DASHA_FORMULA_WEIGHTS = {
        'base': 0.45,
        'dignity': 0.30,
        'house_effect': 0.15,
        'aspect_impact': 0.10
    }

    DASHA_BASE_SCORES = {
        'Jupiter': 5.0,
        'Venus': 4.8,
        'Mercury': 4.2,
        'Moon': 4.0,
        'Sun': 3.8,
        'Rahu': 3.5,
        'Mars': 3.2,
        'Saturn': 3.0,
        'Ketu': 3.0
    }
    DASHA_BASE_SCALE = 2.4

    # Planet dignity numeric mapping (v2.2 - 0-10 scale)
    DIGNITY_POINTS = {
        'exalted': 9,
        'own': 8,          # own_house
        'friendly': 7,
        'neutral': 5,
        'enemy': 3,
        'debilitated': 1
    }

    # Alternative names mapping for flexibility
    DIGNITY_ALIASES = {
        'own_house': 'own',
        'moolatrikona': 'own',
        'great_friend': 'friendly',
        'great_enemy': 'enemy'
    }

    HOUSE_POINTS = {
        'trikona': 5,      # 1, 5, 9
        'kendra': 4,       # 4, 7, 10
        'dhana': 3,        # 2, 11
        'upachaya': 2,     # 3, 6, 10, 11
        'dusthana': -3,    # 6, 8, 12
        'default': 0
    }

    # Enhanced bhukti interaction config
    BHUKTI_CONFIG = {
        'presence_factor': 0.75,
        'base_weight': 0.4,
        'dignity_weight': 0.4,
        'placement_weight': 0.2,
        'missing_scale': 0.5  # When bhukti missing, scale interaction to 0.5
    }

    # Interaction formula: min(4, (dasha_dignity * bhukti_dignity) / 5)
    INTERACTION_CONFIG = {
        'max_bonus': 4.0,
        'divisor': 5.0
    }

    # Mixed factor penalty when both positive and negative factors present
    MIXED_FACTOR_PENALTY = 0.88

    KARAKA_CONFIG = {
        'dignity_scale': 0.5,
        'same_as_dasha_bonus': 2.0,
        'max': 4.5
    }

    # ==================== HOUSE CONFIG (Enhanced v2.1) ====================

    LIFE_AREA_HOUSES = {
        'career': [10, 6, 2],
        'love': [7, 5, 1],
        'relationships': [7, 4, 11],
        'finance': [2, 11, 5],
        'health': [1, 6, 8],
        'education': [5, 4, 9],
        'family': [4, 2, 7],
        'marriage': [7, 2, 4],
        'children': [5, 9, 7],
        'spirituality': [9, 12, 5],
        'general': [1, 10, 9]
    }

    # Dynamic house weights by life area (v2.1 spec)
    DYNAMIC_HOUSE_WEIGHTS = {
        'default': {1: 0.40, 5: 0.30, 9: 0.30},
        'career': {10: 0.50, 6: 0.30, 2: 0.20},
        'love': {7: 0.40, 5: 0.30, 1: 0.30},
        'finance': {2: 0.40, 11: 0.40, 5: 0.20},
        'health': {1: 0.50, 6: 0.30, 8: 0.20},
        'relationships': {7: 0.40, 4: 0.30, 11: 0.30},
        'general': {1: 0.40, 10: 0.30, 9: 0.30}
    }

    HOUSE_LORD_DIGNITY_SCALE = 1.2

    OCCUPANCY_CONFIG = {
        'base': 2.5,
        'benefic': 1.5,
        'malefic': -0.5,
        'min': -3,
        'max': 8
    }

    HOUSE_KARAKAS = {
        1: 'Sun',
        2: 'Jupiter',
        3: 'Mars',
        4: 'Moon',
        5: 'Jupiter',
        6: 'Mars',
        7: 'Venus',
        8: 'Saturn',
        9: 'Jupiter',
        10: 'Saturn',
        11: 'Jupiter',
        12: 'Saturn'
    }

    ASPECT_CONFIG = {
        'base': 2,
        'jupiter_bonus': 2,
        'saturn_penalty': -0.5,
        'min': -2,
        'max': 4,
        'continuous_strength_required': True  # v2.1 spec
    }

    # ==================== PLANET STRENGTH CONFIG (Enhanced v2.1) ====================

    # Formula: dignity = sign_dignity + (shadbala_percent * 2.5/100) + retro_adj + combustion_penalty + aspect_mod
    # Final: planet_strength = (avg_dignity^1.1) * (1 + aspect_strength/10)
    PLANET_STRENGTH_CONFIG = {
        'dignity_range': [0, 5],
        'retrograde_malefic_bonus': 0.5,
        'retrograde_benefic_penalty': -0.3,
        'combustion_penalty': -1.0,
        'combustion_orb_deg': 10,
        'final_scale': 15,
        'dignity_power': 1.1,  # v2.1: Apply power to avg dignity
        'aspect_strength_divisor': 10  # v2.1: aspect contribution factor
    }

    # ==================== TRANSIT CONFIG (Enhanced v2.1) ====================

    TRANSIT_CONFIG = {
        'base': 8,
        'jupiter_weight': 1.2,
        'sigmoid_smoothing': {
            'enabled': True,
            'divisor': 3  # Formula: 1 / (1 + exp(-net_transit_vector/3))
        }
    }

    TRANSIT_FROM_MOON = {
        11: 5,   # Labha - best, gains
        9: 4,    # Dharma - excellent
        3: 3,    # Sahaja - courage, success
        10: 3,   # Karma - career success
        5: 2,    # Putra - moderate gains
        2: 1,    # Dhana - some gains
        4: -1,   # Sukha - mental disturbance
        7: -1,   # Kalatra - partnership issues
        1: -2,   # Janma - health challenges
        6: -2,   # Ari - health issues
        12: -3,  # Vyaya - losses
        8: -4,   # Ayu - worst, obstacles
    }

    TRANSIT_CONDITIONS = {
        'sadesati': -3,
        'ashtama_shani': -2,
        'kantaka_shani': -1,
        'rahu_ketu_1_or_8': -2
    }

    TRANSIT_MOTION = {
        'Jupiter': 0.0831,   # ~12 years per cycle, ~30 deg/year
        'Saturn': 0.0335,    # ~29.5 years per cycle, ~12 deg/year
        'Rahu': -0.053,      # ~18 years per cycle (retrograde)
        'Ketu': -0.053,
        'Sun': 0.9856,       # ~365 days per cycle
        'Moon': 13.176,      # ~27.3 days per cycle
        'Mars': 0.524,       # ~2 years per cycle
        'Mercury': 1.383,    # ~88 days per cycle
        'Venus': 1.2         # ~225 days per cycle
    }

    # Monthly transit modifiers based on fast-moving planets
    MONTHLY_TRANSIT_MODIFIERS = {
        1: {'sun_effect': 1.0, 'mars_effect': 0.8, 'mercury_effect': 0.5},   # Jan
        2: {'sun_effect': 0.9, 'mars_effect': 0.7, 'mercury_effect': 0.6},   # Feb
        3: {'sun_effect': 1.1, 'mars_effect': 1.0, 'mercury_effect': 0.8},   # Mar
        4: {'sun_effect': 1.2, 'mars_effect': 1.1, 'mercury_effect': 1.0},   # Apr
        5: {'sun_effect': 1.0, 'mars_effect': 0.9, 'mercury_effect': 0.7},   # May
        6: {'sun_effect': 0.8, 'mars_effect': 0.6, 'mercury_effect': 0.5},   # Jun
        7: {'sun_effect': 0.7, 'mars_effect': 0.8, 'mercury_effect': 0.9},   # Jul
        8: {'sun_effect': 0.9, 'mars_effect': 1.0, 'mercury_effect': 1.1},   # Aug
        9: {'sun_effect': 1.0, 'mars_effect': 0.9, 'mercury_effect': 0.8},   # Sep
        10: {'sun_effect': 1.1, 'mars_effect': 0.7, 'mercury_effect': 0.6},  # Oct
        11: {'sun_effect': 0.8, 'mars_effect': 0.5, 'mercury_effect': 0.7},  # Nov
        12: {'sun_effect': 0.9, 'mars_effect': 0.6, 'mercury_effect': 0.8},  # Dec
    }

    # ==================== YOGA CONFIG (Enhanced v2.1) ====================

    YOGA_CONFIG = {
        'base': 6,
        'min': -6,
        'max': 10,
        'diminishing_returns_power': 0.85  # v2.1: Apply power for diminishing returns
    }

    YOGA_POSITIVE = {
        'gajakesari': 3,
        'budha_aditya': 2,
        'chandra_mangala': 1.5,
        'raja_yoga': 2.5,
        'neechabhanga': 2
    }

    YOGA_NEGATIVE = {
        'kala_sarpa': -4,
        'kemadruma': -2
    }

    # v2.1: Yoga rarity multipliers
    YOGA_RARITY = {
        'rare': {
            'multiplier': 1.3,
            'yogas': ['raja_yoga', 'neechabhanga']
        },
        'uncommon': {
            'multiplier': 1.0,
            'yogas': ['gajakesari', 'budha_aditya']
        },
        'common': {
            'multiplier': 0.7,
            'yogas': ['chandra_mangala']
        }
    }

    # ==================== NAVAMSA CONFIG (Enhanced v2.1) ====================

    # Formula: navamsa_score = 5 + improvement_bonus + vargottama_bonus + ((planet_strength_d9 / 5) * 2)
    NAVAMSA_CONFIG = {
        'base': 5,
        'improvement_points': 1.5,
        'vargottama_bonus': 0.5,
        'max': 10,
        'scale_factor': 2,  # v2.1: For planet strength scaling
        'strength_divisor': 5  # v2.1: planet_strength_d9 / 5
    }

    NAVAMSA_SIGN_OFFSET = {
        'fire': 0,    # 1, 5, 9
        'earth': 9,   # 2, 6, 10
        'air': 5,     # 3, 7, 11
        'water': 1    # 4, 8, 12
    }

    # ==================== OUTPUT CONFIG ====================

    QUALITY_RANGES = {
        'excellent': (75, 100),
        'good': (60, 74),
        'average': (45, 59),
        'challenging': (30, 44),
        'difficult': (0, 29)
    }

    QUALITY_TAMIL = {
        'excellent': 'மிகச்சிறந்தது',
        'good': 'நல்லது',
        'average': 'சராசரி',
        'challenging': 'சவாலானது',
        'difficult': 'கடினமானது'
    }

    # ==================== META-RULES CONFIG ====================

    # v2.1 Meta-rules updated multipliers per spec
    META_RULES = [
        {
            'id': 'contradiction_d1_d9',
            'description': 'Strong D1 but weak D9 - reduce confidence',
            'condition': lambda s: s.get('house', 0) >= 0.7 and s.get('navamsa', 0) <= 0.35,
            'multiplier': 0.87,  # v2.1 spec
            'reason': 'வலுவான ராசி ஆனால் நவாம்ச பலவீனம் - நம்பகத்தன்மை குறைவு'
        },
        {
            'id': 'dasha_transit_reconciliation',
            'description': 'Strong Dasha should not be fully overturned by weak transit',
            'condition': lambda s: s.get('dasha', 0) >= 0.7 and s.get('transit', 0) <= 0.4,
            'multiplier': 1.0,  # v2.1: limit negative impact instead
            'max_negative_impact': -0.10,
            'reason': 'வலுவான தசை கோசார பாதிப்பை குறைக்கிறது'
        },
        {
            'id': 'dominant_house_boost',
            'description': 'One dominant house should drive the topic',
            'condition': lambda s: max(s.get('house', 0), s.get('dasha', 0)) >= 0.75 and median(list(s.values())) <= 0.40,
            'multiplier': 1.20,  # v2.1: increase dominant house weight by 0.20
            'reason': 'ஒரு வலுவான அம்சம் ஆதிக்கம் செலுத்துகிறது'
        },
        {
            'id': 'diminishing_returns',
            'description': 'Apply nonlinear dampening for high scores',
            'condition': lambda s: sum(s.values()) / len(s) > 0.85,
            'multiplier': None,  # Uses tanh function
            'apply_tanh': True,
            'reason': 'அதிக மதிப்பெண்களுக்கு நிதான சரிசெய்தல்'
        },
        {
            'id': 'yoga_dosha_balance',
            'description': 'Strong yoga should buffer weak components',
            'condition': lambda s: s.get('yoga', 0) >= 0.8 and (s.get('transit', 0) <= 0.4 or s.get('house', 0) <= 0.4),
            'multiplier': 1.03,
            'reason': 'யோகம் பலவீனங்களை சமன் செய்கிறது'
        }
    ]

    # ==================== MONTE CARLO CONFIG ====================

    MONTE_CARLO_CONFIG = {
        'enabled': True,
        'iterations': 30,  # Reduced for performance
        'degree_jitter': 0.25,  # +/- 0.25 degrees
        'birth_time_jitter_minutes': 3,  # +/- 3 minutes
        'seed_policy': 'deterministic',  # Use input hash for reproducibility
    }

    # ==================== CONFIDENCE CONFIG ====================

    CONFIDENCE_WEIGHTS = {
        'completeness': 0.35,  # Data completeness
        'variance': 0.25,      # Low variance = high confidence
        'transit_stability': 0.20,  # Transit volatility
        'monte_carlo_spread': 0.20  # MC interval spread
    }

    # ==================== STATIC DATA ====================

    NATURAL_BENEFICS = ['Jupiter', 'Venus', 'Mercury', 'Moon']
    NATURAL_MALEFICS = ['Saturn', 'Mars', 'Rahu', 'Ketu', 'Sun']

    EXALTATION = {
        'Sun': 1, 'Moon': 2, 'Mars': 10, 'Mercury': 6,
        'Jupiter': 4, 'Venus': 12, 'Saturn': 7, 'Rahu': 3, 'Ketu': 9
    }

    DEBILITATION = {
        'Sun': 7, 'Moon': 8, 'Mars': 4, 'Mercury': 12,
        'Jupiter': 10, 'Venus': 6, 'Saturn': 1, 'Rahu': 9, 'Ketu': 3
    }

    OWN_SIGNS = {
        'Sun': [5], 'Moon': [4], 'Mars': [1, 8], 'Mercury': [3, 6],
        'Jupiter': [9, 12], 'Venus': [2, 7], 'Saturn': [10, 11],
        'Rahu': [11], 'Ketu': [8]
    }

    FRIENDLY_SIGNS = {
        'Sun': [1, 4, 5, 8, 9, 12],
        'Moon': [2, 3, 4, 5, 6, 7],
        'Mars': [1, 4, 5, 9, 10, 12],
        'Mercury': [2, 3, 5, 6, 7],
        'Jupiter': [1, 4, 5, 8, 9, 12],
        'Venus': [2, 3, 6, 7, 10, 11],
        'Saturn': [2, 3, 6, 7, 12],
        'Rahu': [3, 6, 7, 10, 11],
        'Ketu': [1, 5, 8, 9, 12]
    }

    ENEMY_SIGNS = {
        'Sun': [2, 7, 10, 11],
        'Moon': [8, 10, 11],
        'Mars': [2, 3, 6, 7],
        'Mercury': [4, 8, 9, 12],
        'Jupiter': [2, 3, 6, 7],
        'Venus': [1, 4, 5, 8, 9],
        'Saturn': [1, 4, 5, 8, 9],
        'Rahu': [1, 4, 5, 8, 9],
        'Ketu': [2, 3, 6, 7, 10, 11]
    }

    SIGNS = {
        1: {'name': 'Mesha', 'tamil': 'மேஷம்', 'element': 'fire'},
        2: {'name': 'Vrishabha', 'tamil': 'ரிஷபம்', 'element': 'earth'},
        3: {'name': 'Mithuna', 'tamil': 'மிதுனம்', 'element': 'air'},
        4: {'name': 'Kataka', 'tamil': 'கடகம்', 'element': 'water'},
        5: {'name': 'Simha', 'tamil': 'சிம்மம்', 'element': 'fire'},
        6: {'name': 'Kanya', 'tamil': 'கன்னி', 'element': 'earth'},
        7: {'name': 'Tula', 'tamil': 'துலாம்', 'element': 'air'},
        8: {'name': 'Vrischika', 'tamil': 'விருச்சிகம்', 'element': 'water'},
        9: {'name': 'Dhanus', 'tamil': 'தனுசு', 'element': 'fire'},
        10: {'name': 'Makara', 'tamil': 'மகரம்', 'element': 'earth'},
        11: {'name': 'Kumbha', 'tamil': 'கும்பம்', 'element': 'air'},
        12: {'name': 'Meena', 'tamil': 'மீனம்', 'element': 'water'},
    }

    PLANET_TAMIL = {
        'Sun': 'சூரியன்', 'Moon': 'சந்திரன்', 'Mars': 'செவ்வாய்',
        'Mercury': 'புதன்', 'Jupiter': 'குரு', 'Venus': 'சுக்கிரன்',
        'Saturn': 'சனி', 'Rahu': 'ராகு', 'Ketu': 'கேது',
    }

    # ==================== INITIALIZATION ====================

    def __init__(self, jathagam: Dict = None):
        """Initialize with birth chart data"""
        self.jathagam = jathagam or {}
        self.planets = self._extract_planets()
        self.lagna = self._get_lagna()
        self.moon_sign = self._get_moon_sign()
        self.houses = self._extract_houses()

    def _extract_planets(self) -> Dict[str, Dict]:
        """Extract planet positions from jathagam"""
        planets = {}
        planet_list = self.jathagam.get('planets', [])

        if isinstance(planet_list, list):
            for p in planet_list:
                if isinstance(p, dict):
                    name = p.get('planet', '')
                    planets[name] = {
                        'sign': self._sign_to_number(p.get('sign', '')),
                        'house': p.get('house', 1),
                        'degree': p.get('degree', 0),
                        'nakshatra': p.get('nakshatra', ''),
                        'retrograde': p.get('retrograde', False),
                        'strength': p.get('strength', 50),
                    }
        return planets

    def _extract_houses(self) -> Dict[int, Dict]:
        """Extract house information"""
        houses = {}
        for i in range(1, 13):
            houses[i] = {
                'sign': ((self.lagna - 1 + i - 1) % 12) + 1,
                'planets': [],
                'lord': self._get_house_lord(((self.lagna - 1 + i - 1) % 12) + 1),
            }

        for planet, data in self.planets.items():
            house = data.get('house', 1)
            if house in houses:
                houses[house]['planets'].append(planet)

        return houses

    def _get_lagna(self) -> int:
        """Get lagna (ascendant) sign number"""
        lagna_info = self.jathagam.get('lagna', {})
        if isinstance(lagna_info, dict):
            return self._sign_to_number(lagna_info.get('sign', 'Mesha'))
        return 1

    def _get_moon_sign(self) -> int:
        """Get Moon sign (Rasi)"""
        moon = self.planets.get('Moon', {})
        return moon.get('sign', 1)

    def _sign_to_number(self, sign_name: str) -> int:
        """Convert sign name to number"""
        sign_map = {
            'Mesha': 1, 'Aries': 1, 'மேஷம்': 1,
            'Vrishabha': 2, 'Taurus': 2, 'ரிஷபம்': 2,
            'Mithuna': 3, 'Gemini': 3, 'மிதுனம்': 3,
            'Kataka': 4, 'Cancer': 4, 'கடகம்': 4,
            'Simha': 5, 'Leo': 5, 'சிம்மம்': 5,
            'Kanya': 6, 'Virgo': 6, 'கன்னி': 6,
            'Tula': 7, 'Libra': 7, 'துலாம்': 7,
            'Vrischika': 8, 'Scorpio': 8, 'விருச்சிகம்': 8,
            'Dhanus': 9, 'Sagittarius': 9, 'தனுசு': 9,
            'Makara': 10, 'Capricorn': 10, 'மகரம்': 10,
            'Kumbha': 11, 'Aquarius': 11, 'கும்பம்': 11,
            'Meena': 12, 'Pisces': 12, 'மீனம்': 12,
        }
        if isinstance(sign_name, int):
            return sign_name
        return sign_map.get(sign_name, 1)

    def _get_house_lord(self, sign: int) -> str:
        """Get the lord of a sign"""
        lords = {
            1: 'Mars', 2: 'Venus', 3: 'Mercury', 4: 'Moon',
            5: 'Sun', 6: 'Mercury', 7: 'Venus', 8: 'Mars',
            9: 'Jupiter', 10: 'Saturn', 11: 'Saturn', 12: 'Jupiter',
        }
        return lords.get(sign, 'Sun')

    def _normalize(self, value: float, min_val: float, max_val: float) -> float:
        """Normalize value to 0-1 range"""
        if max_val == min_val:
            return 0.5
        normalized = (value - min_val) / (max_val - min_val)
        return max(0, min(1, normalized))

    # ==================== DIGNITY CALCULATION ====================

    def get_planet_dignity(self, planet: str, sign: int = None) -> Dict:
        """Calculate planet dignity with v2.0 point system"""
        if sign is None:
            sign = self.planets.get(planet, {}).get('sign', 1)

        if self.EXALTATION.get(planet) == sign:
            return {
                'score': self.DIGNITY_POINTS['exalted'],
                'status': 'exalted',
                'status_tamil': 'உச்சம்'
            }
        elif self.DEBILITATION.get(planet) == sign:
            return {
                'score': self.DIGNITY_POINTS['debilitated'],
                'status': 'debilitated',
                'status_tamil': 'நீசம்'
            }
        elif sign in self.OWN_SIGNS.get(planet, []):
            return {
                'score': self.DIGNITY_POINTS['own'],
                'status': 'own_sign',
                'status_tamil': 'சொந்த வீடு'
            }
        elif sign in self.FRIENDLY_SIGNS.get(planet, []):
            return {
                'score': self.DIGNITY_POINTS['friendly'],
                'status': 'friendly',
                'status_tamil': 'நட்பு'
            }
        elif sign in self.ENEMY_SIGNS.get(planet, []):
            return {
                'score': self.DIGNITY_POINTS['enemy'],
                'status': 'enemy',
                'status_tamil': 'பகை'
            }
        else:
            return {
                'score': self.DIGNITY_POINTS['neutral'],
                'status': 'neutral',
                'status_tamil': 'சமம்'
            }

    def _get_house_type(self, house: int) -> str:
        """Get house type for scoring"""
        if house in [1, 5, 9]:
            return 'trikona'
        elif house in [4, 7, 10]:
            return 'kendra'
        elif house in [2, 11]:
            return 'dhana'
        elif house == 3:
            return 'upachaya'
        elif house in [6, 8, 12]:
            return 'dusthana'
        return 'default'

    # ==================== DASHA SCORE (30%) ====================

    def calculate_dasha_score(self, dasha_lord: str, bhukti_lord: str = None,
                              life_area: str = 'general') -> Dict:
        """
        Calculate Dasha/Bhukti strength score (raw score, will be normalized)

        v2.1 Formula: Dasha_total = (Base*0.45) + (Dignity*0.30) + (HouseEffect*0.15) + (AspectImpact*0.10) + InteractionBonus
        Interaction: min(4, (dasha_dignity * bhukti_dignity) / 5)
        """
        factors = []
        has_positive = False
        has_negative = False

        # 1. Base Dasha score (weight: 0.45)
        dasha_base = self.DASHA_BASE_SCORES.get(dasha_lord, 3.5)
        base_component = dasha_base * self.DASHA_BASE_SCALE * self.DASHA_FORMULA_WEIGHTS['base']

        # 2. Dasha lord dignity (weight: 0.30)
        dasha_dignity = self.get_planet_dignity(dasha_lord)
        dignity_component = dasha_dignity['score'] * self.DASHA_FORMULA_WEIGHTS['dignity']

        factors.append({
            'name': f"{self.PLANET_TAMIL.get(dasha_lord, dasha_lord)} தசை",
            'value': round(base_component + dignity_component, 1),
            'positive': dasha_base >= 3.5,
            'detail': dasha_dignity['status_tamil']
        })
        if dasha_base >= 3.5:
            has_positive = True
        else:
            has_negative = True

        # 3. Dasha lord house placement (weight: 0.15)
        dasha_planet = self.planets.get(dasha_lord, {})
        dasha_house = dasha_planet.get('house', 1)
        house_type = self._get_house_type(dasha_house)
        house_points = self.HOUSE_POINTS.get(house_type, 0)
        house_component = house_points * self.DASHA_FORMULA_WEIGHTS['house_effect']

        if house_points != 0:
            factors.append({
                'name': self._get_house_type_tamil(house_type),
                'value': round(house_component, 1),
                'positive': house_points > 0
            })
            if house_points > 0:
                has_positive = True
            else:
                has_negative = True

        # 4. Aspect impact (weight: 0.10) - Jupiter/Saturn aspects on dasha lord
        aspect_score = 0
        jupiter_data = self.planets.get('Jupiter', {})
        jupiter_house = jupiter_data.get('house', 0)
        jupiter_aspects = [
            (jupiter_house + 4) % 12 + 1,
            (jupiter_house + 6) % 12 + 1,
            (jupiter_house + 8) % 12 + 1
        ]
        if dasha_house in jupiter_aspects or jupiter_house == dasha_house:
            aspect_score += 2
            has_positive = True

        saturn_data = self.planets.get('Saturn', {})
        saturn_house = saturn_data.get('house', 0)
        saturn_aspects = [
            (saturn_house + 2) % 12 + 1,
            (saturn_house + 6) % 12 + 1,
            (saturn_house + 9) % 12 + 1
        ]
        if dasha_house in saturn_aspects:
            aspect_score -= 0.5
            has_negative = True

        aspect_component = aspect_score * self.DASHA_FORMULA_WEIGHTS['aspect_impact']

        # Calculate total before interaction bonus
        score = base_component + dignity_component + house_component + aspect_component

        # 5. Bhukti lord effect with v2.1 interaction formula
        interaction_bonus = 0
        if bhukti_lord:
            bhukti_base = self.DASHA_BASE_SCORES.get(bhukti_lord, 3.5)
            bhukti_dignity = self.get_planet_dignity(bhukti_lord)
            bhukti_planet = self.planets.get(bhukti_lord, {})
            bhukti_house = bhukti_planet.get('house', 1)
            bhukti_house_type = self._get_house_type(bhukti_house)
            bhukti_house_score = self.HOUSE_POINTS.get(bhukti_house_type, 0)

            bhukti_score = (
                bhukti_base * self.BHUKTI_CONFIG['base_weight'] +
                bhukti_dignity['score'] * self.BHUKTI_CONFIG['dignity_weight'] +
                bhukti_house_score * self.BHUKTI_CONFIG['placement_weight']
            ) * self.BHUKTI_CONFIG['presence_factor']

            # v2.1 Interaction formula: min(4, (dasha_dignity * bhukti_dignity) / 5)
            interaction_bonus = min(
                self.INTERACTION_CONFIG['max_bonus'],
                (dasha_dignity['score'] * bhukti_dignity['score']) / self.INTERACTION_CONFIG['divisor']
            )

            score += bhukti_score + interaction_bonus
            factors.append({
                'name': f"{self.PLANET_TAMIL.get(bhukti_lord, bhukti_lord)} புக்தி",
                'value': round(bhukti_score, 1),
                'positive': bhukti_base >= 3.5,
                'detail': f"{bhukti_dignity['status_tamil']} | ஊடாட்டம்: +{round(interaction_bonus, 1)}"
            })
            if bhukti_base >= 3.5:
                has_positive = True
            else:
                has_negative = True
        else:
            # v2.1: When bhukti missing, scale interaction to 0.5
            interaction_bonus = dasha_dignity['score'] * self.BHUKTI_CONFIG['missing_scale'] * 0.5
            score += interaction_bonus

        # 6. Karaka relevance
        relevant_houses = self.LIFE_AREA_HOUSES.get(life_area, [10])
        karaka = self.HOUSE_KARAKAS.get(relevant_houses[0], 'Sun')
        karaka_dignity = self.get_planet_dignity(karaka)
        karaka_score = min(
            karaka_dignity['score'] * self.KARAKA_CONFIG['dignity_scale'],
            self.KARAKA_CONFIG['max']
        )
        score += karaka_score

        factors.append({
            'name': f"காரகன் {self.PLANET_TAMIL.get(karaka, karaka)}",
            'value': round(karaka_score, 1),
            'positive': karaka_dignity['score'] >= 3
        })

        if dasha_lord == karaka:
            score += self.KARAKA_CONFIG['same_as_dasha_bonus']
            factors.append({
                'name': 'தசை = காரகம்',
                'value': self.KARAKA_CONFIG['same_as_dasha_bonus'],
                'positive': True
            })
            has_positive = True

        # v2.1: Apply mixed factor penalty if both positive and negative factors present
        if has_positive and has_negative:
            score *= self.MIXED_FACTOR_PENALTY

        return {
            'raw_score': round(score, 2),
            'normalized': self._normalize(
                score,
                self.NORMALIZATION['dasha']['min'],
                self.NORMALIZATION['dasha']['max']
            ),
            'factors': factors[:5],
            'dasha_lord': dasha_lord,
            'bhukti_lord': bhukti_lord,
            'interaction_bonus': round(interaction_bonus, 2),
            'mixed_factor_penalty_applied': has_positive and has_negative
        }

    def _get_house_type_tamil(self, house_type: str) -> str:
        """Get Tamil name for house type"""
        tamil_names = {
            'trikona': 'திரிகோண வீடு',
            'kendra': 'கேந்திர வீடு',
            'dhana': 'தன வீடு',
            'upachaya': 'உபச்சய வீடு',
            'dusthana': 'துஷ்டான வீடு'
        }
        return tamil_names.get(house_type, '')

    # ==================== HOUSE SCORE (20%) ====================

    def calculate_house_score(self, life_area: str = 'career') -> Dict:
        """Calculate House + Karaka strength score"""
        score = 0
        factors = []

        relevant_houses = self.LIFE_AREA_HOUSES.get(life_area, [10])
        primary_house = relevant_houses[0]
        karaka = self.HOUSE_KARAKAS.get(primary_house, 'Sun')

        # 1. House lord dignity
        house_info = self.houses.get(primary_house, {})
        house_lord = house_info.get('lord', 'Sun')
        lord_dignity = self.get_planet_dignity(house_lord)
        lord_score = lord_dignity['score'] * self.HOUSE_LORD_DIGNITY_SCALE
        score += lord_score

        factors.append({
            'name': f"{primary_house}ஆம் வீட்டதிபதி {self.PLANET_TAMIL.get(house_lord, house_lord)}",
            'value': round(lord_score, 1),
            'positive': lord_dignity['score'] >= 3,
            'detail': lord_dignity['status_tamil']
        })

        # 2. House occupancy
        house_planets = house_info.get('planets', [])
        occupancy_score = self.OCCUPANCY_CONFIG['base']

        benefics_in_house = [p for p in house_planets if p in self.NATURAL_BENEFICS]
        malefics_in_house = [p for p in house_planets if p in self.NATURAL_MALEFICS]

        occupancy_score += len(benefics_in_house) * self.OCCUPANCY_CONFIG['benefic']
        occupancy_score += len(malefics_in_house) * self.OCCUPANCY_CONFIG['malefic']
        occupancy_score = max(
            self.OCCUPANCY_CONFIG['min'],
            min(self.OCCUPANCY_CONFIG['max'], occupancy_score)
        )
        score += occupancy_score

        if house_planets:
            planets_tamil = [self.PLANET_TAMIL.get(p, p) for p in house_planets[:2]]
            factors.append({
                'name': f"வீட்டில் {', '.join(planets_tamil)}",
                'value': round(occupancy_score, 1),
                'positive': occupancy_score >= self.OCCUPANCY_CONFIG['base'],
            })

        # 3. Karaka strength
        karaka_dignity = self.get_planet_dignity(karaka)
        karaka_score = karaka_dignity['score']
        score += karaka_score

        factors.append({
            'name': f"காரகன் {self.PLANET_TAMIL.get(karaka, karaka)}",
            'value': karaka_score,
            'positive': karaka_score >= 3,
            'detail': karaka_dignity['status_tamil']
        })

        # 4. Aspects
        aspect_score = self.ASPECT_CONFIG['base']

        jupiter_data = self.planets.get('Jupiter', {})
        jupiter_house = jupiter_data.get('house', 0)
        jupiter_aspects = [
            (jupiter_house + 4) % 12 + 1,
            (jupiter_house + 6) % 12 + 1,
            (jupiter_house + 8) % 12 + 1
        ]

        if primary_house in jupiter_aspects or jupiter_house == primary_house:
            aspect_score += self.ASPECT_CONFIG['jupiter_bonus']
            factors.append({
                'name': 'குரு பார்வை',
                'value': self.ASPECT_CONFIG['jupiter_bonus'],
                'positive': True
            })

        saturn_data = self.planets.get('Saturn', {})
        saturn_house = saturn_data.get('house', 0)
        saturn_aspects = [
            (saturn_house + 2) % 12 + 1,
            (saturn_house + 6) % 12 + 1,
            (saturn_house + 9) % 12 + 1
        ]

        if primary_house in saturn_aspects:
            aspect_score += self.ASPECT_CONFIG['saturn_penalty']
            factors.append({
                'name': 'சனி பார்வை',
                'value': self.ASPECT_CONFIG['saturn_penalty'],
                'positive': False
            })

        aspect_score = max(
            self.ASPECT_CONFIG['min'],
            min(self.ASPECT_CONFIG['max'], aspect_score)
        )
        score += aspect_score

        return {
            'raw_score': round(score, 2),
            'normalized': self._normalize(
                score,
                self.NORMALIZATION['house']['min'],
                self.NORMALIZATION['house']['max']
            ),
            'factors': factors[:4],
            'house': primary_house,
            'karaka': karaka,
        }

    # ==================== PLANET STRENGTH SCORE (15%) ====================

    def calculate_planet_strength_score(self, life_area: str = 'general') -> Dict:
        """Calculate Planetary Dignity & Shadbala score (0-1 normalized)"""
        factors = []

        relevant_houses = self.LIFE_AREA_HOUSES.get(life_area, [10, 1])
        relevant_planets = set()

        for house in relevant_houses[:2]:
            karaka = self.HOUSE_KARAKAS.get(house, 'Sun')
            relevant_planets.add(karaka)
            house_lord = self._get_house_lord(((self.lagna - 1 + house - 1) % 12) + 1)
            relevant_planets.add(house_lord)

        lagna_lord = self._get_house_lord(self.lagna)
        relevant_planets.add(lagna_lord)
        relevant_planets.add('Moon')

        total_dignity = 0
        planet_count = 0
        max_dignity = self.PLANET_STRENGTH_CONFIG['dignity_range'][1]

        for planet in relevant_planets:
            if planet in self.planets:
                planet_data = self.planets[planet]
                dignity = self.get_planet_dignity(planet)
                dignity_value = dignity['score'] / max_dignity  # Normalize to 0-1

                # Retrograde adjustment
                if planet_data.get('retrograde'):
                    if planet in self.NATURAL_MALEFICS:
                        dignity_value += self.PLANET_STRENGTH_CONFIG['retrograde_malefic_bonus'] / max_dignity
                    else:
                        dignity_value += self.PLANET_STRENGTH_CONFIG['retrograde_benefic_penalty'] / max_dignity

                # Combustion check
                sun_data = self.planets.get('Sun', {})
                if planet != 'Sun' and planet_data.get('sign') == sun_data.get('sign'):
                    deg_diff = abs(planet_data.get('degree', 0) - sun_data.get('degree', 0))
                    if deg_diff < self.PLANET_STRENGTH_CONFIG['combustion_orb_deg']:
                        dignity_value += self.PLANET_STRENGTH_CONFIG['combustion_penalty'] / max_dignity

                dignity_value = max(0, min(1, dignity_value))
                total_dignity += dignity_value
                planet_count += 1

                if dignity['score'] >= 4 or dignity['score'] <= 1:
                    factors.append({
                        'name': self.PLANET_TAMIL.get(planet, planet),
                        'value': round(dignity['score'], 1),
                        'positive': dignity['score'] >= 3,
                        'detail': dignity['status_tamil']
                    })

        avg_strength = total_dignity / max(1, planet_count)

        return {
            'raw_score': round(avg_strength, 3),
            'normalized': avg_strength,  # Already 0-1
            'factors': factors[:3],
        }

    # ==================== TRANSIT SCORE (15%) ====================

    def calculate_transit_score(self, target_date: date, life_area: str = 'general') -> Dict:
        """Calculate Transit (Gocharam) score with monthly variation"""
        score = self.TRANSIT_CONFIG['base']
        factors = []

        transit_positions = self._calculate_transits(target_date)
        month = target_date.month

        # Jupiter transit effect (weighted higher)
        jupiter_transit = transit_positions.get('Jupiter', 1)
        jupiter_from_moon = ((jupiter_transit - self.moon_sign) % 12) + 1
        jupiter_effect = self.TRANSIT_FROM_MOON.get(jupiter_from_moon, 0) * self.TRANSIT_CONFIG['jupiter_weight']

        score += jupiter_effect
        jupiter_sign_tamil = self.SIGNS.get(jupiter_transit, {}).get('tamil', '')
        factors.append({
            'name': f"குரு {jupiter_sign_tamil}இல் - {jupiter_from_moon}ஆம் வீடு",
            'value': round(jupiter_effect, 1),
            'positive': jupiter_effect > 0,
            'detail': self._get_transit_house_meaning(jupiter_from_moon)
        })

        # Saturn transit effect
        saturn_transit = transit_positions.get('Saturn', 1)
        saturn_from_moon = ((saturn_transit - self.moon_sign) % 12) + 1
        saturn_effect = self.TRANSIT_FROM_MOON.get(saturn_from_moon, 0)

        # Special Saturn conditions
        if saturn_from_moon in [12, 1, 2]:
            saturn_effect += self.TRANSIT_CONDITIONS['sadesati']
            phase = 'ஆரம்பம்' if saturn_from_moon == 12 else ('நடுப்பகுதி' if saturn_from_moon == 1 else 'முடிவு')
            factors.append({
                'name': f'சடேசதி ({phase})',
                'value': self.TRANSIT_CONDITIONS['sadesati'],
                'positive': False,
                'detail': 'பொறுமை தேவை, கடின உழைப்பு வெற்றி தரும்'
            })
        elif saturn_from_moon == 8:
            saturn_effect += self.TRANSIT_CONDITIONS['ashtama_shani']
            factors.append({
                'name': 'அஷ்டம சனி',
                'value': self.TRANSIT_CONDITIONS['ashtama_shani'],
                'positive': False,
                'detail': 'ஆரோக்கியம் கவனிக்க, பெரிய முடிவுகள் தவிர்க்க'
            })
        elif saturn_from_moon in [4, 7, 10]:
            saturn_effect += self.TRANSIT_CONDITIONS['kantaka_shani']
            factors.append({
                'name': 'கண்டக சனி',
                'value': self.TRANSIT_CONDITIONS['kantaka_shani'],
                'positive': False,
                'detail': 'தொழில்/குடும்பத்தில் சவால், திட்டமிட்டு செயல்படுக'
            })

        score += saturn_effect

        if saturn_from_moon not in [12, 1, 2, 8, 4, 7, 10]:
            saturn_sign_tamil = self.SIGNS.get(saturn_transit, {}).get('tamil', '')
            factors.append({
                'name': f"சனி {saturn_sign_tamil}இல் - {saturn_from_moon}ஆம் வீடு",
                'value': round(saturn_effect, 1),
                'positive': saturn_effect > 0,
                'detail': self._get_transit_house_meaning(saturn_from_moon)
            })

        # Rahu/Ketu effect
        rahu_transit = transit_positions.get('Rahu', 1)
        rahu_from_moon = ((rahu_transit - self.moon_sign) % 12) + 1

        if rahu_from_moon in [1, 8]:
            score += self.TRANSIT_CONDITIONS['rahu_ketu_1_or_8']
            factors.append({
                'name': f'ராகு {rahu_from_moon}ஆம் வீட்டில்',
                'value': self.TRANSIT_CONDITIONS['rahu_ketu_1_or_8'],
                'positive': False,
                'detail': 'குழப்பம் வரலாம், தெளிவாக சிந்திக்க'
            })

        # Add fast-moving planet effects for monthly variation
        monthly_mod = self.MONTHLY_TRANSIT_MODIFIERS.get(month, {})

        # Sun transit from moon (changes every month)
        sun_transit = transit_positions.get('Sun', 1)
        sun_from_moon = ((sun_transit - self.moon_sign) % 12) + 1
        sun_base_effect = self.TRANSIT_FROM_MOON.get(sun_from_moon, 0) * 0.5  # Sun weighted 0.5x
        sun_effect = sun_base_effect * monthly_mod.get('sun_effect', 1.0)
        score += sun_effect

        # Mars transit (changes every ~2 months)
        mars_transit = transit_positions.get('Mars', 1)
        mars_from_moon = ((mars_transit - self.moon_sign) % 12) + 1
        mars_base_effect = self.TRANSIT_FROM_MOON.get(mars_from_moon, 0) * 0.6  # Mars weighted 0.6x
        mars_effect = mars_base_effect * monthly_mod.get('mars_effect', 1.0)
        score += mars_effect

        if abs(mars_effect) > 1:
            mars_sign_tamil = self.SIGNS.get(mars_transit, {}).get('tamil', '')
            factors.append({
                'name': f"செவ்வாய் {mars_sign_tamil}இல்",
                'value': round(mars_effect, 1),
                'positive': mars_effect > 0,
                'detail': 'சக்தி மற்றும் துணிவு' if mars_effect > 0 else 'பொறுமை தேவை'
            })

        # Mercury transit for communication/business
        mercury_transit = transit_positions.get('Mercury', 1)
        mercury_from_moon = ((mercury_transit - self.moon_sign) % 12) + 1
        mercury_effect = self.TRANSIT_FROM_MOON.get(mercury_from_moon, 0) * 0.3 * monthly_mod.get('mercury_effect', 1.0)
        score += mercury_effect

        # v2.1: Apply sigmoid smoothing if enabled
        # Formula: transit_score = 1 / (1 + exp(-net_transit_vector/divisor))
        raw_score = score
        sigmoid_applied = False
        sigmoid_config = self.TRANSIT_CONFIG.get('sigmoid_smoothing', {})

        if sigmoid_config.get('enabled', False):
            divisor = sigmoid_config.get('divisor', 3)
            # Normalize score to sigmoid-friendly range
            net_vector = (score - self.TRANSIT_CONFIG['base']) / 5  # Normalize around base
            sigmoid_score = 1 / (1 + math.exp(-net_vector / divisor))
            # Map sigmoid (0-1) back to transit range
            min_transit = self.NORMALIZATION['transit']['min']
            max_transit = self.NORMALIZATION['transit']['max']
            score = min_transit + sigmoid_score * (max_transit - min_transit)
            sigmoid_applied = True

        return {
            'raw_score': round(raw_score, 2),
            'normalized': self._normalize(
                score,
                self.NORMALIZATION['transit']['min'],
                self.NORMALIZATION['transit']['max']
            ),
            'factors': factors[:4],
            'transits': {
                'jupiter': jupiter_transit,
                'saturn': saturn_transit,
                'sun': sun_transit,
                'mars': mars_transit,
                'jupiter_from_moon': jupiter_from_moon,
                'saturn_from_moon': saturn_from_moon,
                'sun_from_moon': sun_from_moon,
                'mars_from_moon': mars_from_moon,
            },
            'sigmoid_applied': sigmoid_applied
        }

    def _get_transit_house_meaning(self, house: int) -> str:
        """Get Tamil meaning for transit house position"""
        meanings = {
            1: 'உடல் ஆரோக்கியம் கவனிக்க',
            2: 'நிதி நிலை சீராகும்',
            3: 'தைரியமும் வெற்றியும்',
            4: 'மன அமைதி குறையும்',
            5: 'புத்தி தெளிவு, நல்ல முடிவுகள்',
            6: 'எதிரிகள் மீது வெற்றி',
            7: 'உறவுகளில் சிக்கல் வரலாம்',
            8: 'தடைகள், பொறுமை தேவை',
            9: 'அதிர்ஷ்டம், தர்மம் வளரும்',
            10: 'தொழில் வெற்றி',
            11: 'லாபம், ஆதாயம்',
            12: 'செலவுகள் அதிகரிக்கும்'
        }
        return meanings.get(house, '')

    def _calculate_transits(self, target_date: date) -> Dict[str, int]:
        """Calculate approximate planetary positions for a date"""
        base_date = date(2024, 1, 1)
        days_diff = (target_date - base_date).days

        base_positions = {
            'Sun': 260, 'Moon': 120, 'Mars': 270,
            'Mercury': 250, 'Jupiter': 15, 'Venus': 230,
            'Saturn': 325, 'Rahu': 25, 'Ketu': 205,
        }

        positions = {}
        for planet, base_pos in base_positions.items():
            motion = self.TRANSIT_MOTION.get(planet, 0)
            current_deg = (base_pos + motion * days_diff) % 360
            positions[planet] = int(current_deg // 30) + 1

        return positions

    # ==================== V3.0 TRANSIT SCORING ====================

    def calculate_transit_score_v3(
        self,
        target_date: date,
        life_area: str = 'general',
        ephemeris_data: Dict = None,
        retrograde_status: Dict = None,
        eclipse_data: Dict = None
    ) -> Dict:
        """
        v3.0 Enhanced Transit Scoring with:
        - Jupiter transit table (1/5/9: +8, kendra: +7, 2/11: +6, etc.)
        - Saturn transit rules (sade_sati: -3, kantaka: -2, ashtama: -3)
        - Retrograde penalties per planet
        - Eclipse penalties (solar: -1.0, lunar: -1.5)
        - Rahu/Ketu axis scoring
        """
        score = self.TRANSIT_CONFIG['base']
        factors = []
        retrograde_planets = []

        # Get transit positions (use ephemeris if provided, else calculate)
        if ephemeris_data:
            transit_positions = self._parse_ephemeris_positions(ephemeris_data)
        else:
            transit_positions = self._calculate_transits(target_date)

        month = target_date.month

        # ===== JUPITER TRANSIT (v3.0 Table) =====
        jupiter_transit = transit_positions.get('Jupiter', 1)
        jupiter_from_moon = ((jupiter_transit - self.moon_sign) % 12) + 1

        # Use v3.0 Jupiter transit table
        jupiter_score = 5  # Default neutral
        jupiter_label = ''
        for category, config in self.JUPITER_TRANSIT_TABLE_V3.items():
            if jupiter_from_moon in config['houses']:
                jupiter_score = config['score']
                jupiter_label = config['label']
                break

        # Convert to score adjustment (table gives 0-10, we need adjustment)
        jupiter_effect = (jupiter_score - 5) * 0.6  # Scale to effect
        score += jupiter_effect

        jupiter_sign_tamil = self.SIGNS.get(jupiter_transit, {}).get('tamil', '')
        factors.append({
            'name': f"குரு {jupiter_sign_tamil}இல் - {jupiter_from_moon}ஆம் வீடு",
            'value': round(jupiter_effect, 1),
            'positive': jupiter_effect > 0,
            'detail': jupiter_label or self._get_transit_house_meaning(jupiter_from_moon),
            'v3_score': jupiter_score
        })

        # ===== SATURN TRANSIT (v3.0 Rules) =====
        saturn_transit = transit_positions.get('Saturn', 1)
        saturn_from_moon = ((saturn_transit - self.moon_sign) % 12) + 1
        saturn_effect = 0
        saturn_condition = None

        # Check Sade-Sati (priority)
        sade_sati_config = self.SATURN_TRANSIT_RULES_V3['sade_sati']
        if saturn_from_moon in sade_sati_config['houses']:
            phase_config = sade_sati_config['phases'].get(saturn_from_moon, {})
            saturn_effect = phase_config.get('penalty', sade_sati_config['penalty'])
            saturn_condition = 'sade_sati'
            factors.append({
                'name': f"சடேசதி ({phase_config.get('tamil', '')})",
                'value': saturn_effect,
                'positive': False,
                'detail': 'பொறுமை தேவை, கடின உழைப்பு வெற்றி தரும்',
                'phase': phase_config.get('name', '')
            })

        # Check Ashtama Shani
        elif saturn_from_moon in self.SATURN_TRANSIT_RULES_V3['ashtama']['houses']:
            saturn_effect = self.SATURN_TRANSIT_RULES_V3['ashtama']['penalty']
            saturn_condition = 'ashtama'
            factors.append({
                'name': self.SATURN_TRANSIT_RULES_V3['ashtama']['label'],
                'value': saturn_effect,
                'positive': False,
                'detail': 'ஆரோக்கியம் கவனிக்க, பெரிய முடிவுகள் தவிர்க்க'
            })

        # Check Kantaka Shani
        elif saturn_from_moon in self.SATURN_TRANSIT_RULES_V3['kantaka']['houses']:
            saturn_effect = self.SATURN_TRANSIT_RULES_V3['kantaka']['penalty']
            saturn_condition = 'kantaka'
            factors.append({
                'name': self.SATURN_TRANSIT_RULES_V3['kantaka']['label'],
                'value': saturn_effect,
                'positive': False,
                'detail': 'தொழில்/குடும்பத்தில் சவால், திட்டமிட்டு செயல்படுக'
            })

        # Check Favorable Saturn
        elif saturn_from_moon in self.SATURN_TRANSIT_RULES_V3['favorable']['houses']:
            saturn_effect = self.SATURN_TRANSIT_RULES_V3['favorable']['bonus']
            saturn_condition = 'favorable'
            factors.append({
                'name': self.SATURN_TRANSIT_RULES_V3['favorable']['label'],
                'value': saturn_effect,
                'positive': True,
                'detail': 'கடின உழைப்புக்கு பலன் கிடைக்கும்'
            })

        score += saturn_effect

        # ===== RAHU/KETU TRANSIT =====
        rahu_transit = transit_positions.get('Rahu', 1)
        rahu_from_moon = ((rahu_transit - self.moon_sign) % 12) + 1
        ketu_from_moon = ((rahu_from_moon + 5) % 12) + 1  # Ketu is always 7th from Rahu

        # Check 1/7 axis (sensitive)
        if rahu_from_moon in [1, 7]:
            rahu_effect = self.TRANSIT_CONDITIONS['rahu_ketu_1_or_8']
            score += rahu_effect
            factors.append({
                'name': f'ராகு-கேது 1/7 அச்சு',
                'value': rahu_effect,
                'positive': False,
                'detail': 'மன குழப்பம், முக்கிய முடிவுகள் தாமதிக்க'
            })
        elif rahu_from_moon in [8]:
            score += self.TRANSIT_CONDITIONS['rahu_ketu_1_or_8']
            factors.append({
                'name': f'ராகு 8ஆம் வீட்டில்',
                'value': self.TRANSIT_CONDITIONS['rahu_ketu_1_or_8'],
                'positive': False,
                'detail': 'திடீர் மாற்றங்கள், எச்சரிக்கையாக இருக்க'
            })

        # ===== RETROGRADE PENALTIES (v3.0) =====
        if retrograde_status:
            for planet, is_retro in retrograde_status.items():
                if is_retro:
                    planet_cap = planet.capitalize()
                    penalty = self.RETROGRADE_PENALTIES_V3.get(planet_cap, 0)
                    if penalty != 0:
                        score += penalty
                        retrograde_planets.append(planet_cap)
                        factors.append({
                            'name': f'{self.PLANET_TAMIL.get(planet_cap, planet_cap)} வக்கிரம்',
                            'value': penalty,
                            'positive': False,
                            'detail': 'வக்கிர கால பாதிப்பு'
                        })

        # ===== ECLIPSE PENALTIES (v3.0) =====
        if eclipse_data:
            # Solar eclipse
            if eclipse_data.get('solar'):
                # Check if eclipse affects sensitive houses
                sun_transit = transit_positions.get('Sun', 1)
                sun_from_lagna = ((sun_transit - self.lagna) % 12) + 1
                if sun_from_lagna in self.ECLIPSE_SENSITIVE_HOUSES:
                    eclipse_penalty = self.ECLIPSE_PENALTIES_V3['solar']
                    score += eclipse_penalty
                    factors.append({
                        'name': 'சூரிய கிரகணம்',
                        'value': eclipse_penalty,
                        'positive': False,
                        'detail': 'கிரகண கால பாதிப்பு - புதிய தொடக்கங்கள் தவிர்க்க'
                    })

            # Lunar eclipse
            if eclipse_data.get('lunar'):
                moon_from_lagna = ((self.moon_sign - self.lagna) % 12) + 1
                if moon_from_lagna in self.ECLIPSE_SENSITIVE_HOUSES or True:  # Lunar always affects Moon
                    eclipse_penalty = self.ECLIPSE_PENALTIES_V3['lunar']
                    score += eclipse_penalty
                    factors.append({
                        'name': 'சந்திர கிரகணம்',
                        'value': eclipse_penalty,
                        'positive': False,
                        'detail': 'மன அமைதி பாதிப்பு - முக்கிய முடிவுகள் தள்ளிவைக்க'
                    })

        # ===== FAST-MOVING PLANETS =====
        monthly_mod = self.MONTHLY_TRANSIT_MODIFIERS.get(month, {})

        # Sun transit
        sun_transit = transit_positions.get('Sun', 1)
        sun_from_moon = ((sun_transit - self.moon_sign) % 12) + 1
        sun_effect = self.TRANSIT_FROM_MOON.get(sun_from_moon, 0) * 0.4 * monthly_mod.get('sun_effect', 1.0)
        score += sun_effect

        # Mars transit
        mars_transit = transit_positions.get('Mars', 1)
        mars_from_moon = ((mars_transit - self.moon_sign) % 12) + 1
        mars_effect = self.TRANSIT_FROM_MOON.get(mars_from_moon, 0) * 0.5 * monthly_mod.get('mars_effect', 1.0)
        score += mars_effect

        if abs(mars_effect) > 0.8:
            mars_sign_tamil = self.SIGNS.get(mars_transit, {}).get('tamil', '')
            factors.append({
                'name': f"செவ்வாய் {mars_sign_tamil}இல்",
                'value': round(mars_effect, 1),
                'positive': mars_effect > 0,
                'detail': 'சக்தி மற்றும் துணிவு' if mars_effect > 0 else 'பொறுமை தேவை'
            })

        # Mercury transit
        mercury_transit = transit_positions.get('Mercury', 1)
        mercury_from_moon = ((mercury_transit - self.moon_sign) % 12) + 1
        mercury_effect = self.TRANSIT_FROM_MOON.get(mercury_from_moon, 0) * 0.3 * monthly_mod.get('mercury_effect', 1.0)
        score += mercury_effect

        # Apply sigmoid smoothing
        raw_score = score
        sigmoid_applied = False
        sigmoid_config = self.TRANSIT_CONFIG.get('sigmoid_smoothing', {})

        if sigmoid_config.get('enabled', False):
            divisor = sigmoid_config.get('divisor', 3)
            net_vector = (score - self.TRANSIT_CONFIG['base']) / 5
            sigmoid_score = 1 / (1 + math.exp(-net_vector / divisor))
            min_transit = self.NORMALIZATION['transit']['min']
            max_transit = self.NORMALIZATION['transit']['max']
            score = min_transit + sigmoid_score * (max_transit - min_transit)
            sigmoid_applied = True

        return {
            'raw_score': round(raw_score, 2),
            'normalized': self._normalize(
                score,
                self.NORMALIZATION['transit']['min'],
                self.NORMALIZATION['transit']['max']
            ),
            'factors': factors[:6],
            'transits': {
                'jupiter': jupiter_transit,
                'saturn': saturn_transit,
                'rahu': rahu_transit,
                'sun': sun_transit,
                'mars': mars_transit,
                'mercury': mercury_transit,
                'jupiter_from_moon': jupiter_from_moon,
                'saturn_from_moon': saturn_from_moon,
                'rahu_from_moon': rahu_from_moon,
            },
            'v3_details': {
                'jupiter_table_score': jupiter_score,
                'saturn_condition': saturn_condition,
                'retrograde_planets': retrograde_planets,
                'eclipse_applied': bool(eclipse_data and (eclipse_data.get('solar') or eclipse_data.get('lunar')))
            },
            'sigmoid_applied': sigmoid_applied,
            'version': '3.0'
        }

    def _parse_ephemeris_positions(self, ephemeris_data: Dict) -> Dict[str, int]:
        """Parse ephemeris data to get sign positions"""
        positions = {}
        planet_map = {
            'sun': 'Sun', 'moon': 'Moon', 'mars': 'Mars',
            'mercury': 'Mercury', 'jupiter': 'Jupiter', 'venus': 'Venus',
            'saturn': 'Saturn', 'rahu': 'Rahu', 'ketu': 'Ketu'
        }

        for key, planet_name in planet_map.items():
            deg = ephemeris_data.get(key, 0)
            if isinstance(deg, (int, float)):
                positions[planet_name] = int(deg // 30) + 1
            else:
                positions[planet_name] = 1

        return positions

    # ==================== YOGA SCORE (10%) ====================

    def _get_yoga_rarity_multiplier(self, yoga_name: str) -> float:
        """Get rarity multiplier for a yoga (v2.1)"""
        for rarity_level, config in self.YOGA_RARITY.items():
            if yoga_name in config.get('yogas', []):
                return config.get('multiplier', 1.0)
        return 1.0  # Default multiplier

    def calculate_yoga_score(self) -> Dict:
        """
        Calculate Yoga/Dosha effect score

        v2.1 Enhancements:
        - Rarity multipliers (rare: 1.3, uncommon: 1.0, common: 0.7)
        - Diminishing returns (power: 0.85)
        """
        score = self.YOGA_CONFIG['base']
        factors = []
        yogas_found = []
        doshas_found = []
        yoga_contributions = []  # Track individual contributions for diminishing returns

        # Gajakesari Yoga
        jupiter_data = self.planets.get('Jupiter', {})
        jupiter_house = jupiter_data.get('house', 0)
        moon_house = self.planets.get('Moon', {}).get('house', 1)

        jupiter_from_moon_house = ((jupiter_house - moon_house) % 12) + 1
        if jupiter_from_moon_house in [1, 4, 7, 10]:
            base_value = self.YOGA_POSITIVE['gajakesari']
            rarity_mult = self._get_yoga_rarity_multiplier('gajakesari')
            adjusted_value = base_value * rarity_mult
            yoga_contributions.append(adjusted_value)
            yogas_found.append('gajakesari')
            factors.append({
                'name': 'கஜகேசரி யோகம்',
                'value': round(adjusted_value, 1),
                'positive': True,
                'rarity': 'uncommon'
            })

        # Budha Aditya Yoga
        sun_sign = self.planets.get('Sun', {}).get('sign', 0)
        mercury_sign = self.planets.get('Mercury', {}).get('sign', 0)
        if sun_sign == mercury_sign and sun_sign != 0:
            base_value = self.YOGA_POSITIVE['budha_aditya']
            rarity_mult = self._get_yoga_rarity_multiplier('budha_aditya')
            adjusted_value = base_value * rarity_mult
            yoga_contributions.append(adjusted_value)
            yogas_found.append('budha_aditya')
            factors.append({
                'name': 'புத ஆதித்ய யோகம்',
                'value': round(adjusted_value, 1),
                'positive': True,
                'rarity': 'uncommon'
            })

        # Chandra Mangala Yoga
        moon_sign = self.planets.get('Moon', {}).get('sign', 0)
        mars_sign = self.planets.get('Mars', {}).get('sign', 0)
        if moon_sign == mars_sign and moon_sign != 0:
            base_value = self.YOGA_POSITIVE['chandra_mangala']
            rarity_mult = self._get_yoga_rarity_multiplier('chandra_mangala')
            adjusted_value = base_value * rarity_mult
            yoga_contributions.append(adjusted_value)
            yogas_found.append('chandra_mangala')
            factors.append({
                'name': 'சந்திர மங்கள யோகம்',
                'value': round(adjusted_value, 1),
                'positive': True,
                'rarity': 'common'
            })

        # Raja Yoga check (simplified)
        kendra_lords = set()
        trikona_lords = set()
        for house in [1, 4, 7, 10]:
            house_info = self.houses.get(house, {})
            kendra_lords.add(house_info.get('lord'))
        for house in [1, 5, 9]:
            house_info = self.houses.get(house, {})
            trikona_lords.add(house_info.get('lord'))

        for planet, data in self.planets.items():
            planet_sign = data.get('sign', 0)
            for other_planet, other_data in self.planets.items():
                if planet != other_planet:
                    if planet_sign == other_data.get('sign', -1):
                        if planet in kendra_lords and other_planet in trikona_lords:
                            if 'raja_yoga' not in yogas_found:
                                base_value = self.YOGA_POSITIVE['raja_yoga']
                                rarity_mult = self._get_yoga_rarity_multiplier('raja_yoga')
                                adjusted_value = base_value * rarity_mult
                                yoga_contributions.append(adjusted_value)
                                yogas_found.append('raja_yoga')
                                factors.append({
                                    'name': 'ராஜ யோகம்',
                                    'value': round(adjusted_value, 1),
                                    'positive': True,
                                    'rarity': 'rare'
                                })
                            break

        # Kala Sarpa Dosha check
        rahu_house = self.planets.get('Rahu', {}).get('house', 0)
        ketu_house = self.planets.get('Ketu', {}).get('house', 0)

        if rahu_house and ketu_house:
            planets_between = True
            for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
                p_house = self.planets.get(planet, {}).get('house', 0)
                if p_house:
                    if rahu_house < ketu_house:
                        if not (rahu_house <= p_house <= ketu_house):
                            planets_between = False
                            break
                    else:
                        if not (p_house >= rahu_house or p_house <= ketu_house):
                            planets_between = False
                            break

            if planets_between:
                yoga_contributions.append(self.YOGA_NEGATIVE['kala_sarpa'])
                doshas_found.append('kala_sarpa')
                factors.append({
                    'name': 'கால சர்ப்ப தோஷம்',
                    'value': self.YOGA_NEGATIVE['kala_sarpa'],
                    'positive': False,
                })

        # Kemadruma Dosha check
        moon_house_num = self.planets.get('Moon', {}).get('house', 1)
        house_before = (moon_house_num - 2) % 12 + 1
        house_after = moon_house_num % 12 + 1

        planets_around_moon = False
        for planet in ['Sun', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
            p_house = self.planets.get(planet, {}).get('house', 0)
            if p_house in [house_before, house_after]:
                planets_around_moon = True
                break

        if not planets_around_moon:
            yoga_contributions.append(self.YOGA_NEGATIVE['kemadruma'])
            doshas_found.append('kemadruma')
            factors.append({
                'name': 'கேமத்ருமா தோஷம்',
                'value': self.YOGA_NEGATIVE['kemadruma'],
                'positive': False,
            })

        # Neechabhanga Raja Yoga
        for planet, debil_sign in self.DEBILITATION.items():
            data = self.planets.get(planet, {})
            if data.get('sign') == debil_sign:
                debil_lord = self._get_house_lord(debil_sign)
                lord_dignity = self.get_planet_dignity(debil_lord)

                if lord_dignity['score'] >= 4:
                    base_value = self.YOGA_POSITIVE['neechabhanga']
                    rarity_mult = self._get_yoga_rarity_multiplier('neechabhanga')
                    adjusted_value = base_value * rarity_mult
                    yoga_contributions.append(adjusted_value)
                    yogas_found.append('neechabhanga')
                    factors.append({
                        'name': f"{self.PLANET_TAMIL.get(planet, planet)} நீச பங்கம்",
                        'value': round(adjusted_value, 1),
                        'positive': True,
                        'rarity': 'rare'
                    })
                    break

        # v2.1: Apply diminishing returns to yoga contributions
        if yoga_contributions:
            diminishing_power = self.YOGA_CONFIG.get('diminishing_returns_power', 0.85)
            total_contribution = sum(yoga_contributions)
            # Apply diminishing returns: (total)^0.85
            if total_contribution > 0:
                adjusted_total = math.pow(total_contribution, diminishing_power)
            else:
                # For negative values (doshas), don't apply diminishing returns
                adjusted_total = total_contribution
            score += adjusted_total
        else:
            score += sum(yoga_contributions)

        # Apply caps
        score = max(self.YOGA_CONFIG['min'], min(self.YOGA_CONFIG['max'], score))

        return {
            'raw_score': round(score, 2),
            'normalized': self._normalize(
                score,
                self.NORMALIZATION['yoga']['min'],
                self.NORMALIZATION['yoga']['max']
            ),
            'factors': factors[:4],
            'yogas': yogas_found,
            'doshas': doshas_found,
            'diminishing_returns_applied': len(yoga_contributions) > 1
        }

    def calculate_yoga_score_v3(self, natal_longitudes: Dict = None) -> Dict:
        """
        v3.0 Enhanced Yoga scoring with actual longitude-based validation.
        - Validates each yoga based on actual planetary longitudes
        - Does not assume yoga if conditions are not met
        - Uses YOGA_VALUES_V3 (strong: 4, medium: 2, weak: 1)
        """
        score = self.YOGA_CONFIG['base']
        factors = []
        yogas_found = []
        doshas_found = []
        yoga_contributions = []
        validation_details = []

        # Helper: Get longitude (use provided or calculate from sign/degree)
        def get_longitude(planet: str) -> float:
            if natal_longitudes and planet.lower() in natal_longitudes:
                return natal_longitudes[planet.lower()]
            data = self.planets.get(planet, {})
            sign = data.get('sign', 1)
            degree = data.get('degree', 15)
            return (sign - 1) * 30 + degree

        # Helper: Check if planets are conjunct (within orb)
        def are_conjunct(p1: str, p2: str, orb: float = 10.0) -> bool:
            long1 = get_longitude(p1)
            long2 = get_longitude(p2)
            diff = abs(long1 - long2)
            if diff > 180:
                diff = 360 - diff
            return diff <= orb

        # Helper: Check if planets are in same sign
        def same_sign(p1: str, p2: str) -> bool:
            long1 = get_longitude(p1)
            long2 = get_longitude(p2)
            return int(long1 // 30) == int(long2 // 30)

        # Helper: Get house from moon for a planet
        def house_from_moon(planet: str) -> int:
            moon_long = get_longitude('Moon')
            planet_long = get_longitude(planet)
            moon_sign = int(moon_long // 30) + 1
            planet_sign = int(planet_long // 30) + 1
            return ((planet_sign - moon_sign) % 12) + 1

        # ===== GAJAKESARI YOGA =====
        # Jupiter in kendra from Moon (actual longitude check)
        jupiter_from_moon = house_from_moon('Jupiter')
        if jupiter_from_moon in [1, 4, 7, 10]:
            # Validate: Jupiter should not be debilitated
            jupiter_long = get_longitude('Jupiter')
            jupiter_sign = int(jupiter_long // 30) + 1
            is_debilitated = (jupiter_sign == 10)  # Capricorn

            if not is_debilitated:
                strength = 'strong' if jupiter_from_moon in [1, 5, 9] else 'medium'
                yoga_value = self.YOGA_VALUES_V3[strength]
                yoga_contributions.append(yoga_value)
                yogas_found.append('gajakesari')
                factors.append({
                    'name': 'கஜகேசரி யோகம்',
                    'value': yoga_value,
                    'positive': True,
                    'strength': strength,
                    'validation': f'குரு சந்திரனிலிருந்து {jupiter_from_moon}ஆம் வீடு'
                })
                validation_details.append({
                    'yoga': 'gajakesari',
                    'validated': True,
                    'jupiter_house_from_moon': jupiter_from_moon,
                    'jupiter_longitude': round(jupiter_long, 2)
                })
            else:
                validation_details.append({
                    'yoga': 'gajakesari',
                    'validated': False,
                    'reason': 'Jupiter debilitated'
                })

        # ===== BUDHA ADITYA YOGA =====
        # Sun and Mercury conjunct (within 10 degrees)
        if same_sign('Sun', 'Mercury'):
            sun_long = get_longitude('Sun')
            mercury_long = get_longitude('Mercury')
            orb = abs(sun_long - mercury_long)

            # Validate: Mercury should not be combust (too close to Sun)
            is_combust = orb < 3  # Within 3 degrees = combust

            if not is_combust and orb <= 15:
                strength = 'strong' if orb <= 8 else 'medium'
                yoga_value = self.YOGA_VALUES_V3[strength]
                yoga_contributions.append(yoga_value)
                yogas_found.append('budha_aditya')
                factors.append({
                    'name': 'புத ஆதித்ய யோகம்',
                    'value': yoga_value,
                    'positive': True,
                    'strength': strength,
                    'validation': f'சூரியன்-புதன் இடைவெளி: {round(orb, 1)}°'
                })
                validation_details.append({
                    'yoga': 'budha_aditya',
                    'validated': True,
                    'orb': round(orb, 2),
                    'sun_longitude': round(sun_long, 2),
                    'mercury_longitude': round(mercury_long, 2)
                })
            else:
                validation_details.append({
                    'yoga': 'budha_aditya',
                    'validated': False,
                    'reason': 'Mercury combust' if is_combust else 'Orb too wide'
                })

        # ===== CHANDRA MANGALA YOGA =====
        # Moon and Mars conjunct
        if same_sign('Moon', 'Mars'):
            moon_long = get_longitude('Moon')
            mars_long = get_longitude('Mars')
            orb = abs(moon_long - mars_long)

            if orb <= 12:
                strength = 'medium' if orb <= 6 else 'weak'
                yoga_value = self.YOGA_VALUES_V3[strength]
                yoga_contributions.append(yoga_value)
                yogas_found.append('chandra_mangala')
                factors.append({
                    'name': 'சந்திர மங்கள யோகம்',
                    'value': yoga_value,
                    'positive': True,
                    'strength': strength,
                    'validation': f'சந்திரன்-செவ்வாய் இடைவெளி: {round(orb, 1)}°'
                })
                validation_details.append({
                    'yoga': 'chandra_mangala',
                    'validated': True,
                    'orb': round(orb, 2)
                })

        # ===== RAJA YOGA (Kendra-Trikona lords conjunct) =====
        kendra_lords = set()
        trikona_lords = set()
        for house in [1, 4, 7, 10]:
            house_info = self.houses.get(house, {})
            kendra_lords.add(house_info.get('lord'))
        for house in [1, 5, 9]:
            house_info = self.houses.get(house, {})
            trikona_lords.add(house_info.get('lord'))

        raja_yoga_found = False
        for kendra_lord in kendra_lords:
            if raja_yoga_found:
                break
            for trikona_lord in trikona_lords:
                if kendra_lord and trikona_lord and kendra_lord != trikona_lord:
                    if are_conjunct(kendra_lord, trikona_lord, orb=12):
                        yoga_value = self.YOGA_VALUES_V3['strong']
                        yoga_contributions.append(yoga_value)
                        yogas_found.append('raja_yoga')
                        factors.append({
                            'name': 'ராஜ யோகம்',
                            'value': yoga_value,
                            'positive': True,
                            'strength': 'strong',
                            'validation': f'{kendra_lord} + {trikona_lord} சேர்க்கை'
                        })
                        raja_yoga_found = True
                        validation_details.append({
                            'yoga': 'raja_yoga',
                            'validated': True,
                            'planets': [kendra_lord, trikona_lord]
                        })
                        break

        # ===== KALA SARPA DOSHA =====
        rahu_long = get_longitude('Rahu')
        ketu_long = get_longitude('Ketu')
        rahu_sign = int(rahu_long // 30) + 1
        ketu_sign = int(ketu_long // 30) + 1

        planets_hemmed = True
        for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
            p_long = get_longitude(planet)
            # Check if planet is between Rahu and Ketu (on one side of axis)
            if rahu_long < ketu_long:
                if not (rahu_long <= p_long <= ketu_long):
                    planets_hemmed = False
                    break
            else:
                if not (p_long >= rahu_long or p_long <= ketu_long):
                    planets_hemmed = False
                    break

        if planets_hemmed:
            dosha_value = self.YOGA_NEGATIVE['kala_sarpa']
            yoga_contributions.append(dosha_value)
            doshas_found.append('kala_sarpa')
            factors.append({
                'name': 'கால சர்ப்ப தோஷம்',
                'value': dosha_value,
                'positive': False,
                'validation': 'அனைத்து கிரகங்களும் ராகு-கேது அச்சில்'
            })

        # ===== KEMADRUMA DOSHA =====
        moon_long = get_longitude('Moon')
        moon_sign = int(moon_long // 30) + 1
        adjacent_signs = [(moon_sign - 2) % 12 + 1, moon_sign % 12 + 1]

        planets_around_moon = False
        for planet in ['Sun', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
            p_long = get_longitude(planet)
            p_sign = int(p_long // 30) + 1
            if p_sign in adjacent_signs:
                planets_around_moon = True
                break

        if not planets_around_moon:
            dosha_value = self.YOGA_NEGATIVE['kemadruma']
            yoga_contributions.append(dosha_value)
            doshas_found.append('kemadruma')
            factors.append({
                'name': 'கேமத்ருமா தோஷம்',
                'value': dosha_value,
                'positive': False,
                'validation': 'சந்திரனுக்கு அருகில் கிரகம் இல்லை'
            })

        # Apply diminishing returns
        if yoga_contributions:
            diminishing_power = self.YOGA_CONFIG.get('diminishing_returns_power', 0.85)
            total_contribution = sum(yoga_contributions)
            if total_contribution > 0:
                adjusted_total = math.pow(total_contribution, diminishing_power)
            else:
                adjusted_total = total_contribution
            score += adjusted_total
        else:
            score += sum(yoga_contributions)

        score = max(self.YOGA_CONFIG['min'], min(self.YOGA_CONFIG['max'], score))

        return {
            'raw_score': round(score, 2),
            'normalized': self._normalize(
                score,
                self.NORMALIZATION['yoga']['min'],
                self.NORMALIZATION['yoga']['max']
            ),
            'factors': factors[:5],
            'yogas': yogas_found,
            'doshas': doshas_found,
            'validation_details': validation_details,
            'longitude_based': True,
            'version': '3.0'
        }

    # ==================== NAVAMSA SCORE (10%) ====================

    def calculate_navamsa_score(self, life_area: str = 'general') -> Dict:
        """Calculate Navamsa (D9) support score"""
        score = self.NAVAMSA_CONFIG['base']
        factors = []

        relevant_houses = self.LIFE_AREA_HOUSES.get(life_area, [10])
        primary_house = relevant_houses[0]

        for planet, data in self.planets.items():
            degree = data.get('degree', 15)
            sign = data.get('sign', 1)

            # Calculate navamsa pada (1-9)
            navamsa_pada = min(9, int(degree / 3.333) + 1)

            # Get element of sign
            element = self.SIGNS.get(sign, {}).get('element', 'fire')
            offset = self.NAVAMSA_SIGN_OFFSET.get(element, 0)

            # Calculate navamsa sign
            navamsa_sign = ((navamsa_pada - 1 + offset) % 12) + 1

            # Check if planet improves in navamsa
            rasi_dignity = self.get_planet_dignity(planet, sign)
            navamsa_dignity = self.get_planet_dignity(planet, navamsa_sign)

            if navamsa_dignity['score'] > rasi_dignity['score']:
                karaka = self.HOUSE_KARAKAS.get(primary_house)
                house_lord = self._get_house_lord(((self.lagna - 1 + primary_house - 1) % 12) + 1)

                if planet in [karaka, house_lord]:
                    score += self.NAVAMSA_CONFIG['improvement_points']
                    factors.append({
                        'name': f"{self.PLANET_TAMIL.get(planet, planet)} D9 உயர்வு",
                        'value': self.NAVAMSA_CONFIG['improvement_points'],
                        'positive': True,
                    })

            # Vargottama check (same sign in D1 and D9)
            if sign == navamsa_sign:
                score += self.NAVAMSA_CONFIG['vargottama_bonus']
                factors.append({
                    'name': f"{self.PLANET_TAMIL.get(planet, planet)} வர்கோத்தமம்",
                    'value': self.NAVAMSA_CONFIG['vargottama_bonus'],
                    'positive': True,
                })

        score = min(self.NAVAMSA_CONFIG['max'], score)

        return {
            'raw_score': round(score, 2),
            'normalized': self._normalize(
                score,
                self.NORMALIZATION['navamsa']['min'],
                self.NORMALIZATION['navamsa']['max']
            ),
            'factors': factors[:3],
        }

    def calculate_navamsa_score_v3(
        self,
        life_area: str = 'general',
        navamsa_positions: Dict = None
    ) -> Dict:
        """
        v3.0 Enhanced Navamsa (D9) scoring with:
        - If natal planet is weak but strong in D9 → boost score (+2)
        - If strong in natal but weak in D9 → reduce score (-2)
        - Check D9 Lagna lord strength
        """
        score = self.NAVAMSA_CONFIG['base']
        factors = []
        boost_count = 0
        penalty_count = 0

        relevant_houses = self.LIFE_AREA_HOUSES.get(life_area, [10])
        primary_house = relevant_houses[0]
        karaka = self.HOUSE_KARAKAS.get(primary_house)
        house_lord = self._get_house_lord(((self.lagna - 1 + primary_house - 1) % 12) + 1)

        # Key planets to check
        key_planets = list(set([karaka, house_lord, 'Moon', self._get_house_lord(self.lagna)]))

        for planet in key_planets:
            if planet not in self.planets:
                continue

            data = self.planets[planet]
            degree = data.get('degree', 15)
            sign = data.get('sign', 1)

            # Calculate navamsa sign
            navamsa_pada = min(9, int(degree / 3.333) + 1)
            element = self.SIGNS.get(sign, {}).get('element', 'fire')
            offset = self.NAVAMSA_SIGN_OFFSET.get(element, 0)
            navamsa_sign = ((navamsa_pada - 1 + offset) % 12) + 1

            # If navamsa_positions provided, use those
            if navamsa_positions and planet.lower() in navamsa_positions:
                navamsa_deg = navamsa_positions.get(planet.lower(), 0)
                navamsa_sign = int(navamsa_deg // 30) + 1

            # Get dignities
            rasi_dignity = self.get_planet_dignity(planet, sign)
            navamsa_dignity = self.get_planet_dignity(planet, navamsa_sign)

            rasi_score = rasi_dignity['score']
            d9_score = navamsa_dignity['score']

            # v3.0 Logic: Boost if weak natal but strong D9
            if rasi_score <= 4 and d9_score >= 7:  # Weak in D1, Strong in D9
                boost = self.NAVAMSA_MODIFIERS_V3['boost']
                score += boost
                boost_count += 1
                factors.append({
                    'name': f"{self.PLANET_TAMIL.get(planet, planet)} D9 பலம்",
                    'value': boost,
                    'positive': True,
                    'detail': f'ராசி: {rasi_dignity["status_tamil"]} → நவாம்ச: {navamsa_dignity["status_tamil"]}'
                })

            # v3.0 Logic: Penalty if strong natal but weak D9
            elif rasi_score >= 7 and d9_score <= 4:  # Strong in D1, Weak in D9
                penalty = self.NAVAMSA_MODIFIERS_V3['penalty']
                score += penalty
                penalty_count += 1
                factors.append({
                    'name': f"{self.PLANET_TAMIL.get(planet, planet)} D9 பலவீனம்",
                    'value': penalty,
                    'positive': False,
                    'detail': f'ராசி: {rasi_dignity["status_tamil"]} → நவாம்ச: {navamsa_dignity["status_tamil"]}'
                })

            # Vargottama check (same sign in D1 and D9) - always good
            if sign == navamsa_sign:
                vargottama_bonus = self.NAVAMSA_CONFIG['vargottama_bonus']
                score += vargottama_bonus
                factors.append({
                    'name': f"{self.PLANET_TAMIL.get(planet, planet)} வர்கோத்தமம்",
                    'value': vargottama_bonus,
                    'positive': True,
                    'detail': 'D1 = D9 ராசி'
                })

        # Check D9 Lagna lord strength
        d9_lagna_lord = self._get_house_lord(self.lagna)  # Simplified - use same lord
        if d9_lagna_lord in self.planets:
            d9_lord_dignity = self.get_planet_dignity(d9_lagna_lord)
            if d9_lord_dignity['score'] >= 7:
                lagna_bonus = 1.0
                score += lagna_bonus
                factors.append({
                    'name': 'D9 லக்ன அதிபதி பலம்',
                    'value': lagna_bonus,
                    'positive': True,
                    'detail': f'{self.PLANET_TAMIL.get(d9_lagna_lord, d9_lagna_lord)} {d9_lord_dignity["status_tamil"]}'
                })

        # Cap score
        score = max(0, min(self.NAVAMSA_CONFIG['max'], score))

        return {
            'raw_score': round(score, 2),
            'normalized': self._normalize(
                score,
                self.NORMALIZATION['navamsa']['min'],
                self.NORMALIZATION['navamsa']['max']
            ),
            'factors': factors[:4],
            'v3_details': {
                'boost_count': boost_count,
                'penalty_count': penalty_count,
                'modifiers_used': self.NAVAMSA_MODIFIERS_V3
            },
            'version': '3.0'
        }

    # ==================== META-RULES ENGINE ====================

    def apply_meta_rules(self, normalized_scores: Dict[str, float], raw_score: float) -> Dict:
        """
        Apply meta-rules for contradiction resolution and conditional modifiers.
        Returns adjusted score and list of applied rules.
        """
        applied_rules = []
        adjusted_score = raw_score
        total_multiplier = 1.0

        for rule in self.META_RULES:
            try:
                if rule['condition'](normalized_scores):
                    if rule.get('apply_tanh'):
                        # Apply tanh dampening for high scores
                        adjusted_score = math.tanh(adjusted_score / 100 * 1.2) * 100
                        applied_rules.append({
                            'id': rule['id'],
                            'description': rule['description'],
                            'effect': 'tanh_dampening',
                            'reason': rule['reason']
                        })
                    elif rule.get('multiplier'):
                        total_multiplier *= rule['multiplier']
                        applied_rules.append({
                            'id': rule['id'],
                            'description': rule['description'],
                            'multiplier': rule['multiplier'],
                            'reason': rule['reason']
                        })
            except Exception:
                continue  # Skip invalid rules

        adjusted_score *= total_multiplier

        return {
            'adjusted_score': round(adjusted_score, 2),
            'applied_rules': applied_rules,
            'total_multiplier': round(total_multiplier, 4)
        }

    # ==================== MONTE CARLO SIMULATION ====================

    def run_monte_carlo(
        self,
        target_date: date,
        life_area: str,
        dasha_lord: str,
        bhukti_lord: str,
        iterations: int = None
    ) -> Dict:
        """
        Run Monte Carlo simulation with degree jittering for uncertainty estimation.
        Returns mean, median, and confidence interval.
        """
        if not self.MONTE_CARLO_CONFIG.get('enabled', False):
            return {'enabled': False}

        iterations = iterations or self.MONTE_CARLO_CONFIG.get('iterations', 30)
        jitter_deg = self.MONTE_CARLO_CONFIG.get('degree_jitter', 0.25)

        # Generate deterministic seed from input
        input_hash = hashlib.md5(
            f"{self.jathagam}{target_date}{life_area}".encode()
        ).hexdigest()
        seed = int(input_hash[:8], 16)
        random.seed(seed)

        scores = []
        original_planets = self.planets.copy()

        for i in range(iterations):
            # Jitter planet degrees
            jittered_planets = {}
            for planet, data in original_planets.items():
                jittered_data = data.copy()
                if 'degree' in jittered_data:
                    jitter = random.uniform(-jitter_deg, jitter_deg)
                    jittered_data['degree'] = (jittered_data['degree'] + jitter) % 30
                jittered_planets[planet] = jittered_data

            # Temporarily set jittered planets
            self.planets = jittered_planets

            # Calculate score
            try:
                dasha_result = self.calculate_dasha_score(dasha_lord, bhukti_lord, life_area)
                house_result = self.calculate_house_score(life_area)
                planet_result = self.calculate_planet_strength_score(life_area)
                transit_result = self.calculate_transit_score(target_date, life_area)
                yoga_result = self.calculate_yoga_score()
                navamsa_result = self.calculate_navamsa_score(life_area)

                score = (
                    dasha_result['normalized'] * self.WEIGHTS['dasha'] +
                    house_result['normalized'] * self.WEIGHTS['house'] +
                    planet_result['normalized'] * self.WEIGHTS['planet_strength'] +
                    transit_result['normalized'] * self.WEIGHTS['transit'] +
                    yoga_result['normalized'] * self.WEIGHTS['yoga'] +
                    navamsa_result['normalized'] * self.WEIGHTS['navamsa']
                ) * 100
                scores.append(score)
            except Exception:
                continue

        # Restore original planets
        self.planets = original_planets

        if not scores:
            return {'enabled': False, 'error': 'No valid iterations'}

        scores.sort()
        n = len(scores)
        percentile_5 = scores[max(0, int(n * 0.05))]
        percentile_95 = scores[min(n - 1, int(n * 0.95))]

        return {
            'enabled': True,
            'iterations': iterations,
            'mean': round(mean(scores), 2),
            'median': round(median(scores), 2),
            'std_dev': round(stdev(scores), 2) if n > 1 else 0,
            'percentile_5': round(percentile_5, 2),
            'percentile_95': round(percentile_95, 2),
            'interval_spread': round(percentile_95 - percentile_5, 2),
            'seed': input_hash[:8]
        }

    # ==================== META MULTIPLIER CALCULATION (v2.3 Enhanced) ====================

    def calculate_meta_multiplier(
        self,
        target_date: date = None,
        transit_result: Dict = None,
        dasha_lord: str = None,
        retrograde_planets: List[str] = None
    ) -> Dict:
        """
        v2.3 Enhanced meta multiplier calculation based on:
        - Nakshatra element traits with transit-specific boosts
        - Pada element modifiers (Agni, Prithvi, Vayu, Jala)
        - Jupiter transit boost (if favorable)
        - Saturn transit penalty / Sade-Sati detection
        - Retrograde penalties (-10% to -25%)
        - Peak month detection

        Returns dict with multiplier value, breakdown, and element info.
        """
        multiplier = 1.0
        breakdown = []
        element_info = {}

        # 1. Get nakshatra from jathagam
        moon_data = self.jathagam.get('moon_sign', {})
        nakshatra = moon_data.get('nakshatra', '')
        pada = moon_data.get('pada', 1)

        # If not in moon_sign, check planets
        if not nakshatra:
            moon_planet = self.planets.get('Moon', {})
            nakshatra = moon_planet.get('nakshatra', '')
            pada = moon_planet.get('pada', 1)

        # 2. Apply nakshatra element traits (v2.3)
        nakshatra_traits = self.NAKSHATRA_TRAITS.get(nakshatra, {})
        nakshatra_mult = nakshatra_traits.get('base_multiplier', 1.0)
        nakshatra_element = nakshatra_traits.get('element', 'Prithvi')
        nakshatra_lord = nakshatra_traits.get('lord', '')

        element_info['nakshatra_element'] = nakshatra_element
        element_info['nakshatra_lord'] = nakshatra_lord

        if nakshatra_mult != 1.0:
            multiplier *= nakshatra_mult
            breakdown.append({
                'factor': 'nakshatra',
                'name': nakshatra,
                'element': nakshatra_element,
                'multiplier': nakshatra_mult,
                'reason': f'{nakshatra} ({nakshatra_element}) நட்சத்திர பலன்'
            })

        # 2b. Apply nakshatra-specific transit boosts (v2.3)
        if transit_result and nakshatra_traits:
            transit_boosts = nakshatra_traits.get('transit_boost', {})
            transit_penalties = nakshatra_traits.get('transit_penalty', {})
            transits = transit_result.get('transits', {})

            # Check each planet's transit for boosts
            for planet, boost_pct in transit_boosts.items():
                planet_house = transits.get(f'{planet.lower()}_from_moon', 0)
                # Apply boost if planet is in favorable position
                if planet_house in [1, 2, 5, 7, 9, 10, 11]:
                    boost = 1.0 + boost_pct
                    multiplier *= boost
                    breakdown.append({
                        'factor': 'nakshatra_transit_boost',
                        'name': f'{planet} {nakshatra} சிறப்பு',
                        'multiplier': boost,
                        'reason': f'{nakshatra} நட்சத்திரத்தில் {planet} கோச்சார சிறப்பு'
                    })

            # Apply nakshatra-specific transit penalties
            for planet, penalty_pct in transit_penalties.items():
                planet_house = transits.get(f'{planet.lower()}_from_moon', 0)
                if planet_house in [6, 8, 12]:
                    penalty = 1.0 + penalty_pct  # penalty_pct is negative
                    multiplier *= penalty
                    breakdown.append({
                        'factor': 'nakshatra_transit_penalty',
                        'name': f'{planet} {nakshatra} சவால்',
                        'multiplier': penalty,
                        'reason': f'{nakshatra} நட்சத்திரத்தில் {planet} பாதிப்பு'
                    })

        # 3. Apply pada element modifiers (v2.3)
        pada_config = self.PADA_ELEMENT_MODIFIERS.get(pada, {})
        pada_adj = pada_config.get('base_adjustment', 1.0)
        pada_element = pada_config.get('element', 'Prithvi')

        element_info['pada_element'] = pada_element

        if pada_adj != 1.0:
            multiplier *= pada_adj
            breakdown.append({
                'factor': 'pada',
                'name': f'பாதம் {pada}',
                'element': pada_element,
                'multiplier': pada_adj,
                'reason': f'பாதம் {pada} ({pada_element}) சரிசெய்தல்'
            })

        # 3b. Apply pada-specific transit boosts (v2.3)
        if transit_result and pada_config:
            pada_transit_boosts = pada_config.get('transit_boost', {})
            transits = transit_result.get('transits', {})

            for planet, boost_pct in pada_transit_boosts.items():
                planet_house = transits.get(f'{planet.lower()}_from_moon', 0)
                if planet_house in [1, 2, 5, 7, 9, 10, 11]:
                    boost = 1.0 + boost_pct
                    multiplier *= boost
                    breakdown.append({
                        'factor': 'pada_transit_boost',
                        'name': f'{pada_element} பாத {planet} சிறப்பு',
                        'multiplier': boost,
                        'reason': f'{pada_element} பாதத்தில் {planet} சாதகம்'
                    })

            # Check for Saturn reduction in Jala (water) pada
            if pada == 4 and 'saturn_reduction' in pada_config:
                saturn_house = transits.get('saturn_from_moon', 0)
                if saturn_house in [1, 4, 7, 8, 12]:
                    reduction = pada_config['saturn_reduction']
                    multiplier *= (1.0 + reduction)  # Reduces harshness
                    breakdown.append({
                        'factor': 'pada_saturn_reduction',
                        'name': 'ஜல பாத சனி தணிப்பு',
                        'multiplier': 1.0 + reduction,
                        'reason': 'மோட்ச பாதம் சனி கடுமையை குறைக்கிறது'
                    })

        # 4. Check Jupiter transit boost
        if transit_result:
            jupiter_from_moon = transit_result.get('transits', {}).get('jupiter_from_moon', 0)
            if jupiter_from_moon in self.JUPITER_TRANSIT_BOOST['favorable_houses']:
                boost = self.JUPITER_TRANSIT_BOOST['boost_multiplier']
                multiplier *= boost
                breakdown.append({
                    'factor': 'jupiter_transit',
                    'name': f'குரு {jupiter_from_moon}ம் வீட்டில்',
                    'multiplier': boost,
                    'reason': 'சாதகமான குரு கோச்சாரம்'
                })

        # 5. Check Saturn transit penalty / Sade-Sati (v2.3 enhanced)
        if transit_result:
            saturn_from_moon = transit_result.get('transits', {}).get('saturn_from_moon', 0)

            # Detect Sade-Sati phase
            sade_sati_phase = 'none'
            if saturn_from_moon == 12:
                sade_sati_phase = 'rising'
            elif saturn_from_moon == 1:
                sade_sati_phase = 'peak'
            elif saturn_from_moon == 2:
                sade_sati_phase = 'setting'

            if sade_sati_phase != 'none':
                penalty = self.SADE_SATI_PHASES[sade_sati_phase]
                multiplier *= penalty
                phase_names = {'rising': 'ஆரம்பம்', 'peak': 'உச்சம்', 'setting': 'முடிவு'}
                breakdown.append({
                    'factor': 'sade_sati',
                    'name': f'சடேசதி ({phase_names[sade_sati_phase]})',
                    'phase': sade_sati_phase,
                    'multiplier': penalty,
                    'reason': f'சடேசதி {phase_names[sade_sati_phase]} காலம்'
                })
            elif saturn_from_moon in self.SATURN_TRANSIT_PENALTY['challenging_houses']:
                penalty = self.SATURN_TRANSIT_PENALTY['penalty_multiplier']
                multiplier *= penalty
                breakdown.append({
                    'factor': 'saturn_transit',
                    'name': f'சனி {saturn_from_moon}ம் வீட்டில்',
                    'multiplier': penalty,
                    'reason': 'சவாலான சனி கோச்சாரம்'
                })

        # 6. Apply retrograde penalties (v2.3)
        if retrograde_planets:
            for planet in retrograde_planets:
                retro_config = self.RETROGRADE_PENALTIES.get(planet, self.RETROGRADE_PENALTIES['default'])
                # Use base penalty; heavy penalty if planet is dasha lord
                if dasha_lord and planet == dasha_lord:
                    penalty = retro_config['heavy_penalty']
                    reason = f'{planet} வக்கிரம் (தசை நாதன்)'
                else:
                    penalty = retro_config['base_penalty']
                    reason = f'{planet} வக்கிரம்'

                multiplier *= penalty
                breakdown.append({
                    'factor': 'retrograde',
                    'name': f'{planet} வக்கிரம்',
                    'multiplier': penalty,
                    'reason': reason
                })

        return {
            'multiplier': round(multiplier, 4),
            'breakdown': breakdown,
            'nakshatra': nakshatra,
            'pada': pada,
            'element_info': element_info,
            'version': '2.3'
        }

    # ==================== CONFIDENCE CALCULATION ====================

    def calculate_confidence(
        self,
        normalized_scores: Dict[str, float],
        monte_carlo_result: Dict = None
    ) -> Dict:
        """
        Calculate confidence score (0-100) based on:
        - Data completeness
        - Score variance
        - Transit stability
        - Monte Carlo spread
        """
        # Data completeness (based on available jathagam fields)
        required_fields = ['planets', 'lagna', 'dasha']
        available = sum(1 for f in required_fields if self.jathagam.get(f))
        completeness = available / len(required_fields)

        # Score variance (lower variance = higher confidence)
        score_values = list(normalized_scores.values())
        if len(score_values) > 1:
            try:
                variance = stdev(score_values)
            except Exception:
                variance = 0.5
        else:
            variance = 0.5
        variance_factor = max(0, 1 - variance)

        # Transit stability (higher transit score = more stable)
        transit_stability = normalized_scores.get('transit', 0.5)

        # Monte Carlo spread (narrower spread = higher confidence)
        mc_spread_factor = 0.5  # default
        if monte_carlo_result and monte_carlo_result.get('enabled'):
            spread = monte_carlo_result.get('interval_spread', 50)
            mc_spread_factor = max(0, 1 - (spread / 100))

        # Calculate weighted confidence
        confidence = (
            completeness * self.CONFIDENCE_WEIGHTS['completeness'] +
            variance_factor * self.CONFIDENCE_WEIGHTS['variance'] +
            transit_stability * self.CONFIDENCE_WEIGHTS['transit_stability'] +
            mc_spread_factor * self.CONFIDENCE_WEIGHTS['monte_carlo_spread']
        ) * 100

        return {
            'score': round(confidence, 1),
            'breakdown': {
                'completeness': round(completeness * 100, 1),
                'variance_factor': round(variance_factor * 100, 1),
                'transit_stability': round(transit_stability * 100, 1),
                'mc_spread_factor': round(mc_spread_factor * 100, 1)
            },
            'interpretation': 'அதிக நம்பகத்தன்மை' if confidence >= 70 else 'நடுத்தர நம்பகத்தன்மை' if confidence >= 50 else 'குறைந்த நம்பகத்தன்மை'
        }

    # ==================== V3.0 MONTHLY SCORE CALCULATION ====================

    def calculate_monthly_scores_v3(
        self,
        year: int,
        life_area: str = 'general',
        dasha_lord: str = None,
        bhukti_lord: str = None,
        ephemeris_data: List[Dict] = None,
        natal_longitudes: Dict = None,
        navamsa_positions: Dict = None
    ) -> Dict:
        """
        v3.0 Monthly score calculation for a full year.
        Returns monthly_scores array and annual_summary per spec.
        """
        monthly_scores = []
        all_scores = []

        # Get dasha from jathagam if not provided
        if not dasha_lord:
            dasha_info = self.jathagam.get('dasha', {})
            current = dasha_info.get('current', {})
            dasha_lord = current.get('lord', 'Jupiter')
            if not bhukti_lord and 'antardasha' in dasha_info:
                bhukti_lord = dasha_info.get('antardasha')

        # Get domain-specific weights
        weights = self.DOMAIN_WEIGHTS.get(life_area, self.WEIGHTS)

        for month_num in range(1, 13):
            target_date = date(year, month_num, 15)  # Mid-month
            month_str = f"{year}-{month_num:02d}"

            # Get ephemeris for this month if provided
            month_ephemeris = None
            retrograde_status = None
            eclipse_data = None

            if ephemeris_data:
                for eph in ephemeris_data:
                    if eph.get('month') == month_str:
                        month_ephemeris = eph
                        retrograde_status = eph.get('retrograde', {})
                        eclipse_data = eph.get('eclipse', {})
                        break

            # Calculate all components using v3.0 methods
            dasha_result = self.calculate_dasha_score(
                dasha_lord, bhukti_lord, life_area
            )
            house_result = self.calculate_house_score(life_area)
            planet_result = self.calculate_planet_strength_score(life_area)

            # Use v3.0 transit scoring
            transit_result = self.calculate_transit_score_v3(
                target_date,
                life_area,
                ephemeris_data=month_ephemeris,
                retrograde_status=retrograde_status,
                eclipse_data=eclipse_data
            )

            # Use v3.0 yoga scoring with longitude validation
            yoga_result = self.calculate_yoga_score_v3(natal_longitudes)

            # Use v3.0 navamsa scoring
            navamsa_result = self.calculate_navamsa_score_v3(
                life_area, navamsa_positions
            )

            # Calculate weighted score (0-10 scale for components)
            dasha_10 = dasha_result['normalized'] * 10
            house_10 = house_result['normalized'] * 10
            planet_10 = planet_result['normalized'] * 10
            transit_10 = transit_result['normalized'] * 10
            yoga_10 = yoga_result['normalized'] * 10
            navamsa_10 = navamsa_result['normalized'] * 10

            # Calculate final month score (0-100)
            final_month_score = (
                dasha_result['normalized'] * weights.get('dasha', 0.25) +
                house_result['normalized'] * weights.get('house', 0.18) +
                planet_result['normalized'] * weights.get('planet_strength', 0.12) +
                transit_result['normalized'] * weights.get('transit', 0.20) +
                yoga_result['normalized'] * weights.get('yoga', 0.12) +
                navamsa_result['normalized'] * weights.get('navamsa', 0.13)
            ) * 100

            # Apply smoothing
            if self.NON_LINEAR_CONFIG.get('apply_smoothing', False):
                power = self.NON_LINEAR_CONFIG.get('final_smoothing_power', 0.92)
                final_month_score = math.pow(final_month_score / 100, power) * 100

            final_month_score = max(0, min(100, final_month_score))
            all_scores.append(final_month_score)

            monthly_scores.append({
                'month': month_str,
                'dasha': round(dasha_10, 1),
                'house': round(house_10, 1),
                'planet': round(planet_10, 1),
                'transit': round(transit_10, 1),
                'yoga': round(yoga_10, 1),
                'navamsa': round(navamsa_10, 1),
                'final_month_score': round(final_month_score, 1),
                'transit_details': transit_result.get('v3_details', {}),
                'yoga_details': {
                    'yogas': yoga_result.get('yogas', []),
                    'doshas': yoga_result.get('doshas', [])
                }
            })

        # Calculate annual summary
        annual_average = sum(all_scores) / len(all_scores) if all_scores else 0
        peak_month_score = max(all_scores) if all_scores else 0
        worst_month_score = min(all_scores) if all_scores else 0
        peak_month_idx = all_scores.index(peak_month_score) if all_scores else 0
        worst_month_idx = all_scores.index(worst_month_score) if all_scores else 0

        # Calculate meta multipliers
        nakshatra_mult = self._get_nakshatra_multiplier()
        pada_mult = self._get_pada_multiplier()

        # Peak month multiplier (3 consecutive strong months)
        peak_mult = 1.0
        for i in range(len(all_scores) - 2):
            if all(s >= self.PEAK_MONTH_THRESHOLD for s in all_scores[i:i+3]):
                avg_peak = sum(all_scores[i:i+3]) / 3
                peak_mult = 1.03 + (avg_peak - 65) / 100 * 0.05
                peak_mult = min(1.08, max(1.03, peak_mult))
                break

        # Worst month multiplier (2-3 consecutive bad months)
        worst_mult = 1.0
        for i in range(len(all_scores) - 1):
            bad_count = sum(1 for s in all_scores[i:i+3] if s < self.WORST_MONTH_THRESHOLD)
            if bad_count >= 2:
                avg_bad = sum(s for s in all_scores[i:i+3] if s < 40) / max(1, bad_count)
                worst_mult = 0.97 - (40 - avg_bad) / 100 * 0.05
                worst_mult = max(0.92, min(0.97, worst_mult))
                break

        # Apply meta multipliers to annual score
        final_annual_score = annual_average * nakshatra_mult * pada_mult
        if peak_mult > 1.0:
            final_annual_score *= peak_mult
        if worst_mult < 1.0:
            final_annual_score *= worst_mult

        final_annual_score = max(0, min(100, final_annual_score))

        return {
            'monthly_scores': monthly_scores,
            'annual_summary': {
                'annual_average_score': round(annual_average, 1),
                'peak_month': {
                    'month': f"{year}-{peak_month_idx + 1:02d}",
                    'score': round(peak_month_score, 1)
                },
                'worst_month': {
                    'month': f"{year}-{worst_month_idx + 1:02d}",
                    'score': round(worst_month_score, 1)
                },
                'meta_multipliers_applied': {
                    'nakshatra': round(nakshatra_mult, 4),
                    'pada': round(pada_mult, 4),
                    'peak': round(peak_mult, 4),
                    'worst': round(worst_mult, 4)
                },
                'final_annual_score': round(final_annual_score, 1)
            },
            'version': '3.0',
            'life_area': life_area,
            'year': year
        }

    def _get_nakshatra_multiplier(self) -> float:
        """Get nakshatra multiplier from jathagam"""
        moon_data = self.jathagam.get('moon_sign', {})
        nakshatra = moon_data.get('nakshatra', '')
        if not nakshatra:
            moon_planet = self.planets.get('Moon', {})
            nakshatra = moon_planet.get('nakshatra', '')
        traits = self.NAKSHATRA_TRAITS.get(nakshatra, {})
        return traits.get('base_multiplier', 1.0)

    def _get_pada_multiplier(self) -> float:
        """Get pada multiplier from jathagam"""
        moon_data = self.jathagam.get('moon_sign', {})
        pada = moon_data.get('pada', 1)
        if not pada:
            moon_planet = self.planets.get('Moon', {})
            pada = moon_planet.get('pada', 1)
        config = self.PADA_ELEMENT_MODIFIERS.get(pada, {})
        return config.get('base_adjustment', 1.0)

    # ==================== PROVENANCE/AUDIT TRAIL ====================

    def generate_provenance(self, target_date: date) -> Dict:
        """Generate provenance information for audit trail (v3.0)"""
        input_str = f"{self.jathagam}{target_date}"
        input_hash = hashlib.sha256(input_str.encode()).hexdigest()[:16]

        return {
            'engine_version': self.ENGINE_VERSION,
            'calculation_timestamp_utc': datetime.utcnow().isoformat(),
            'input_hash': input_hash,
            'lagna_used': self.lagna,
            'moon_sign_used': self.moon_sign,
            'planets_count': len(self.planets),
            'target_date': target_date.isoformat(),
            'weights_used': self.WEIGHTS,
            'normalization_bounds': self.NORMALIZATION,
            # v3.0 feature flags
            'v3_features': {
                'jupiter_transit_table': True,
                'saturn_transit_rules': True,
                'retrograde_penalties_v3': True,
                'eclipse_penalties': True,
                'longitude_based_yoga_validation': True,
                'navamsa_boost_penalty': True,
                'peak_worst_month_detection': True,
                'monthly_ephemeris_support': True
            },
            # Legacy v2.3 flags (retained)
            'nakshatra_element_traits_enabled': True,
            'pada_element_modifiers_enabled': True,
            'sade_sati_detection_enabled': True
        }

    # ==================== MAIN PREDICTION SCORE ====================

    def calculate_prediction_score(
        self,
        target_date: date,
        life_area: str = 'general',
        dasha_lord: str = None,
        bhukti_lord: str = None,
    ) -> Dict:
        """
        Calculate final prediction percentage (0-100%)
        using weighted normalized scores with meta-rules,
        Monte Carlo uncertainty estimation, and confidence scoring.

        v2.2 Enhancements:
        - Updated weight allocation (dasha:25%, house:18%, planet:12%, transit:20%, yoga:12%, navamsa:13%)
        - Nakshatra-specific meta multipliers
        - Post-Jupiter transit boost
        - Domain-specific weight overrides
        - Non-linear smoothing (power 0.92)
        - Enhanced interaction formula
        """
        # Get dasha from jathagam if not provided
        if not dasha_lord:
            dasha_info = self.jathagam.get('dasha', {})
            current = dasha_info.get('current', {})
            dasha_lord = current.get('lord', 'Jupiter')
            if not bhukti_lord and 'antardasha' in dasha_info:
                bhukti_lord = dasha_info.get('antardasha')

        # Calculate all components
        dasha_result = self.calculate_dasha_score(dasha_lord, bhukti_lord, life_area)
        house_result = self.calculate_house_score(life_area)
        planet_result = self.calculate_planet_strength_score(life_area)
        transit_result = self.calculate_transit_score(target_date, life_area)
        yoga_result = self.calculate_yoga_score()
        navamsa_result = self.calculate_navamsa_score(life_area)

        # v2.2: Get domain-specific weights or use defaults
        weights = self.DOMAIN_WEIGHTS.get(life_area, self.WEIGHTS)
        weights_used = life_area if life_area in self.DOMAIN_WEIGHTS else 'default'

        # Calculate weighted final score (0-100) using v2.2 weights
        # Formula: final_score = (dasha*0.25 + house*0.18 + planet*0.12 + transit*0.20 + yoga*0.12 + navamsa*0.13) * 10 * meta_multiplier
        raw_final_score = (
            dasha_result['normalized'] * weights.get('dasha', self.WEIGHTS['dasha']) +
            house_result['normalized'] * weights.get('house', self.WEIGHTS['house']) +
            planet_result['normalized'] * weights.get('planet_strength', self.WEIGHTS['planet_strength']) +
            transit_result['normalized'] * weights.get('transit', self.WEIGHTS['transit']) +
            yoga_result['normalized'] * weights.get('yoga', self.WEIGHTS['yoga']) +
            navamsa_result['normalized'] * weights.get('navamsa', self.WEIGHTS['navamsa'])
        ) * 100

        # v2.1: Apply non-linear smoothing (power 0.92)
        if self.NON_LINEAR_CONFIG.get('apply_smoothing', False):
            smoothing_power = self.NON_LINEAR_CONFIG.get('final_smoothing_power', 0.92)
            # Apply smoothing: score^0.92 normalized to 0-100 range
            raw_final_score = math.pow(raw_final_score / 100, smoothing_power) * 100

        # Collect normalized scores for meta-rules
        normalized_scores = {
            'dasha': dasha_result['normalized'],
            'house': house_result['normalized'],
            'planet_strength': planet_result['normalized'],
            'transit': transit_result['normalized'],
            'yoga': yoga_result['normalized'],
            'navamsa': navamsa_result['normalized']
        }

        # Apply meta-rules for contradiction resolution
        meta_result = self.apply_meta_rules(normalized_scores, raw_final_score)

        # v2.3: Calculate and apply enhanced meta multiplier (nakshatra/pada/element/retrograde)
        # Get retrograde planets from transit result if available
        retrograde_planets = transit_result.get('retrograde_planets', []) if transit_result else []

        v23_meta = self.calculate_meta_multiplier(
            target_date=target_date,
            transit_result=transit_result,
            dasha_lord=dasha_lord,
            retrograde_planets=retrograde_planets
        )
        final_score = meta_result['adjusted_score'] * v23_meta['multiplier']

        # Ensure score is within 0-100 range
        final_score = max(0, min(100, final_score))

        # Run Monte Carlo simulation for uncertainty estimation
        monte_carlo_result = self.run_monte_carlo(
            target_date, life_area, dasha_lord, bhukti_lord
        )

        # Calculate confidence score
        confidence_result = self.calculate_confidence(normalized_scores, monte_carlo_result)

        # Generate provenance/audit trail
        provenance = self.generate_provenance(target_date)

        # Collect all significant factors
        all_factors = []
        for result in [dasha_result, house_result, planet_result, transit_result, yoga_result, navamsa_result]:
            all_factors.extend(result.get('factors', []))

        # Sort by absolute value
        all_factors.sort(key=lambda x: abs(x.get('value', 0)), reverse=True)

        # Determine quality (use adjusted score)
        quality = 'average'
        for q_name, (q_min, q_max) in self.QUALITY_RANGES.items():
            if q_min <= final_score <= q_max:
                quality = q_name
                break

        # Build detailed calculation trace (v2.2 weights)
        calculation_trace = {
            'formula': 'final_score = (dasha×25% + house×18% + planet×12% + transit×20% + yoga×12% + navamsa×13%) × 100 × meta_multiplier',
            'version': '2.2',
            'step_by_step': [
                {
                    'component': 'dasha',
                    'component_tamil': 'தசை/புக்தி வலிமை',
                    'weight': '25%',
                    'raw_score': dasha_result['raw_score'],
                    'normalization_range': f"{self.NORMALIZATION['dasha']['min']} to {self.NORMALIZATION['dasha']['max']}",
                    'normalized': round(dasha_result['normalized'], 4),
                    'contribution': round(dasha_result['normalized'] * 25, 2),
                    'calculation': f"({dasha_result['raw_score']} - {self.NORMALIZATION['dasha']['min']}) / ({self.NORMALIZATION['dasha']['max']} - {self.NORMALIZATION['dasha']['min']}) = {round(dasha_result['normalized'], 4)}",
                    'factors_detail': dasha_result['factors']
                },
                {
                    'component': 'house',
                    'component_tamil': 'வீடு + காரகன்',
                    'weight': '18%',
                    'raw_score': house_result['raw_score'],
                    'normalization_range': f"{self.NORMALIZATION['house']['min']} to {self.NORMALIZATION['house']['max']}",
                    'normalized': round(house_result['normalized'], 4),
                    'contribution': round(house_result['normalized'] * 18, 2),
                    'calculation': f"({house_result['raw_score']} - {self.NORMALIZATION['house']['min']}) / ({self.NORMALIZATION['house']['max']} - {self.NORMALIZATION['house']['min']}) = {round(house_result['normalized'], 4)}",
                    'factors_detail': house_result['factors']
                },
                {
                    'component': 'planet_strength',
                    'component_tamil': 'கிரக பலம்',
                    'weight': '12%',
                    'raw_score': planet_result['raw_score'],
                    'normalization_range': '0 to 1 (already normalized)',
                    'normalized': round(planet_result['normalized'], 4),
                    'contribution': round(planet_result['normalized'] * 12, 2),
                    'factors_detail': planet_result['factors']
                },
                {
                    'component': 'transit',
                    'component_tamil': 'கோசாரம்',
                    'weight': '20%',
                    'raw_score': transit_result['raw_score'],
                    'normalization_range': f"{self.NORMALIZATION['transit']['min']} to {self.NORMALIZATION['transit']['max']}",
                    'normalized': round(transit_result['normalized'], 4),
                    'contribution': round(transit_result['normalized'] * 20, 2),
                    'calculation': f"({transit_result['raw_score']} - {self.NORMALIZATION['transit']['min']}) / ({self.NORMALIZATION['transit']['max']} - {self.NORMALIZATION['transit']['min']}) = {round(transit_result['normalized'], 4)}",
                    'factors_detail': transit_result['factors'],
                    'transit_positions': transit_result.get('transits', {})
                },
                {
                    'component': 'yoga',
                    'component_tamil': 'யோகம்/தோஷம்',
                    'weight': '12%',
                    'raw_score': yoga_result['raw_score'],
                    'normalization_range': f"{self.NORMALIZATION['yoga']['min']} to {self.NORMALIZATION['yoga']['max']}",
                    'normalized': round(yoga_result['normalized'], 4),
                    'contribution': round(yoga_result['normalized'] * 12, 2),
                    'yogas_found': yoga_result.get('yogas', []),
                    'doshas_found': yoga_result.get('doshas', []),
                    'factors_detail': yoga_result['factors']
                },
                {
                    'component': 'navamsa',
                    'component_tamil': 'நவாம்ச ஆதரவு',
                    'weight': '13%',
                    'raw_score': navamsa_result['raw_score'],
                    'normalization_range': f"{self.NORMALIZATION['navamsa']['min']} to {self.NORMALIZATION['navamsa']['max']}",
                    'normalized': round(navamsa_result['normalized'], 4),
                    'contribution': round(navamsa_result['normalized'] * 13, 2),
                    'factors_detail': navamsa_result['factors']
                }
            ],
            'final_calculation': {
                'sum_of_contributions': f"{round(dasha_result['normalized'] * 25, 2)} + {round(house_result['normalized'] * 18, 2)} + {round(planet_result['normalized'] * 12, 2)} + {round(transit_result['normalized'] * 20, 2)} + {round(yoga_result['normalized'] * 12, 2)} + {round(navamsa_result['normalized'] * 13, 2)}",
                'raw_total': round(raw_final_score, 2),
                'meta_multiplier': meta_result['total_multiplier'],
                'v23_meta_multiplier': v23_meta['multiplier'],
                'adjusted_total': round(final_score, 2)
            },
            'meta_rules_applied': meta_result['applied_rules'],
            'v23_meta_breakdown': v23_meta['breakdown']
        }

        # Build Monte Carlo interval for display
        monte_carlo_interval = None
        if monte_carlo_result.get('enabled'):
            monte_carlo_interval = {
                'low': monte_carlo_result['percentile_5'],
                'high': monte_carlo_result['percentile_95'],
                'spread': monte_carlo_result['interval_spread'],
                'interpretation': 'குறுகிய இடைவெளி - அதிக நிச்சயம்' if monte_carlo_result['interval_spread'] < 10 else 'நடுத்தர இடைவெளி' if monte_carlo_result['interval_spread'] < 20 else 'பரந்த இடைவெளி - சில நிச்சயமின்மை'
            }

        return {
            'score': round(final_score, 1),
            'raw_score': round(raw_final_score, 1),
            'quality': quality,
            'quality_tamil': self.QUALITY_TAMIL.get(quality, 'சராசரி'),
            'confidence': confidence_result,
            'monte_carlo_interval': monte_carlo_interval,
            'breakdown': {
                'dasha': {
                    'score': round(dasha_result['normalized'] * 25, 1),
                    'raw': dasha_result['raw_score'],
                    'normalized': round(dasha_result['normalized'], 4),
                    'weight': '25%',
                    'factors': dasha_result['factors']
                },
                'house': {
                    'score': round(house_result['normalized'] * 18, 1),
                    'raw': house_result['raw_score'],
                    'normalized': round(house_result['normalized'], 4),
                    'weight': '18%',
                    'factors': house_result['factors']
                },
                'planet_strength': {
                    'score': round(planet_result['normalized'] * 12, 1),
                    'normalized': round(planet_result['normalized'], 4),
                    'weight': '12%',
                    'factors': planet_result['factors']
                },
                'transit': {
                    'score': round(transit_result['normalized'] * 20, 1),
                    'raw': transit_result['raw_score'],
                    'normalized': round(transit_result['normalized'], 4),
                    'weight': '20%',
                    'factors': transit_result['factors']
                },
                'yoga': {
                    'score': round(yoga_result['normalized'] * 12, 1),
                    'raw': yoga_result['raw_score'],
                    'normalized': round(yoga_result['normalized'], 4),
                    'weight': '12%',
                    'factors': yoga_result['factors'],
                    'yogas': yoga_result.get('yogas', []),
                    'doshas': yoga_result.get('doshas', [])
                },
                'navamsa': {
                    'score': round(navamsa_result['normalized'] * 13, 1),
                    'raw': navamsa_result['raw_score'],
                    'normalized': round(navamsa_result['normalized'], 4),
                    'weight': '13%',
                    'factors': navamsa_result['factors']
                },
            },
            'meta_adjustments': {
                'rules_applied': meta_result['applied_rules'],
                'total_multiplier': meta_result['total_multiplier'],
                'adjustment_reason': meta_result['applied_rules'][0]['reason'] if meta_result['applied_rules'] else None,
                'v23_meta': {
                    'version': v23_meta.get('version', '2.3'),
                    'multiplier': v23_meta['multiplier'],
                    'nakshatra': v23_meta['nakshatra'],
                    'pada': v23_meta['pada'],
                    'element_info': v23_meta.get('element_info', {}),
                    'breakdown': v23_meta['breakdown']
                }
            },
            'calculation_trace': calculation_trace,
            'top_factors': all_factors[:5],
            'positive_factors': [f for f in all_factors if f.get('positive', False)][:3],
            'negative_factors': [f for f in all_factors if not f.get('positive', True)][:3],
            'life_area': life_area,
            'target_date': target_date.isoformat(),
            'dasha_lord': dasha_lord,
            'bhukti_lord': bhukti_lord,
            'provenance': provenance
        }


# Convenience function for quick predictions
def get_prediction_score(
    jathagam: Dict,
    target_date: date = None,
    life_area: str = 'general',
    dasha_lord: str = None,
) -> Dict:
    """Quick prediction score calculation"""
    if target_date is None:
        target_date = date.today()

    engine = AstroPercentEngine(jathagam)
    return engine.calculate_prediction_score(
        target_date=target_date,
        life_area=life_area,
        dasha_lord=dasha_lord
    )
