"""
Astro Engine v7.0 - Pressure-Outcome Dual-Track Engine with Dignity Preservation
================================================================================

This engine extends the base AstroPercentEngine with dynamic time-mode adaptation
and V7.0 philosophy: "Difficulty ≠ Bad Outcome"

V7.0 CORE PHILOSOPHY:
- Pressure (effort required) and Outcome (potential gains) are SEPARATE dimensions
- High pressure can still have positive outcomes!
- Everyone has inherent dignity (minimum score 45%)
- Malefics dampen (multiply), not punish (subtract)
- Positives compound when multiple factors align

V7.0 KEY FEATURES:
1. DUAL-TRACK SCORING:
   - Pressure Score: Measures effort cost, not bad outcome
   - Outcome Score: Measures potential gains, independent of effort
   - Final Score: Blend of base calculation and outcome score

2. TIME DECAY (impact = base × e^(-months_elapsed / k)):
   - Mars: k=3 (fast decay - 3 months)
   - Saturn: k=6 (medium decay - 6 months)
   - Rahu/Ketu: k=9 (slow decay - 9 months)

3. DAMPENERS INSTEAD OF PENALTIES:
   - Saturn active → outcome × 0.85 (not -15)
   - Mars active → outcome × 0.90
   - Rahu/Ketu active → outcome × 0.88

4. POSITIVE COMPOUNDING:
   - 2+ positives align → positive_gain × 1.20
   - 3+ positives align → positive_gain × 1.40
   - 4+ positives align → positive_gain × 1.55

5. DIGNITY FLOOR: Minimum score 45% (no one is doomed)

6. NEGATIVITY CAP: Max 30 points of negative impact per period

7. PHASE LABELS (never use "bad"):
   - "Effort Phase" (high pressure + good outcome)
   - "Flow Phase" (low pressure + good outcome)
   - "Growth Phase" (neutral pressure + positive outcome)
   - "Challenge Phase" (high pressure + building foundation)
   - "Steady Phase" (neutral period)

8. BALANCED OUTPUT: Show 2 positives + 1 challenge (2:1 ratio)

Key Concepts:
- POI: Planet Operational Intensity
- HAI: House Activation Index
- NavamsaSupport: D9 uplift

v6.0 Features (retained):
- Global Numeric Safety: clamp_min=0.50, clamp_max=0.92
- Dasha Baseline Power: benefic=0.78, neutral=0.70, malefic=0.62
- Jupiter Support: Strongly boosted (3.5x direct, 1.8x aspect)
- Yoga Presence Score: 0.07 dormant, 0.12 active
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional, Literal
from enum import Enum
import math

from app.services.astro_percent_engine import AstroPercentEngine


class TimeMode(Enum):
    """Time context modes for adaptive calculations"""
    PAST_ANALYSIS = "past_analysis"
    FUTURE_PREDICTION = "future_prediction"
    MONTH_WISE = "month_wise"
    YEAR_OVERLAY = "year_overlay"
    PRESENT = "present"  # Default: current day calculation


class TimeAdaptiveEngine(AstroPercentEngine):
    """
    V7.0 Time-Adaptive Astro Scoring Engine with Dual-Track Scoring

    Extends AstroPercentEngine with dynamic time-mode adaptation and
    V7.0 philosophy: "Difficulty ≠ Bad Outcome"

    V7.0 Core Principles:
    - Pressure and Outcome are SEPARATE dimensions
    - Dampeners (multiply) instead of penalties (subtract)
    - Time decay on long-running malefic factors
    - Dignity floor: minimum score 45%
    - Negativity cap: max 30 points per period
    - Positive compounding: 1.2x for 2+, 1.4x for 3+, 1.55x for 4+
    - Phase labels: "Effort Phase", "Flow Phase", "Growth Phase" (never "bad")
    - Balanced output: 2 positives + 1 challenge (2:1 ratio)

    Time Modes:
    - Past Analysis: Historical event verification
    - Future Prediction: Forward-looking forecast
    - Month-wise: Period-sliced calculation
    - Year Overlay: Varshaphal integration
    """

    ENGINE_VERSION = "7.0"
    ENGINE_TYPE = "Pressure-Outcome Dual-Track Engine with Dignity Preservation"

    # ==================== V7.0 CORE PRINCIPLES ====================
    # V7.0 Philosophy: Difficulty ≠ Bad Outcome
    # - Split scoring into PRESSURE (effort cost) and OUTCOME (potential gain)
    # - Convert penalties to dampeners (multiply, don't subtract)
    # - Add time decay to long-running factors
    # - Cap total negativity per period
    # - Compound positives on alignment
    # - Preserve dignity (minimum score 45)
    # - Resilience memory for surviving tough periods

    # ==================== V7.0 GLOBAL NUMERIC SAFETY ====================
    GLOBAL_NUMERIC_SAFETY = {
        'clamp_min': 0.50,       # V7.0: High floor - no score below 50%
        'clamp_max': 0.92,       # V7.0: Raised ceiling for compound positives
        'meta_multiplier_min': 1.00,  # V7.0: Never below 1.0
        'meta_multiplier_max': 1.18,  # V7.0: Higher for compound positives
        'poi_min': 5.5,          # V7.0: High POI floor
        'poi_max': 8.5,          # V7.0: Raised ceiling
        'hai_min': 2.0,          # V7.0: HAI floor raised
        'hai_max': 10.0,         # HAI ceiling
        'house_suppression_threshold': 0.30,
        'saturn_penalty_cap': -0.01,  # V7.0: Minimal Saturn penalty
        'transit_cap': 0.85,     # V7.0: Raised transit cap
        'malefic_penalty_reduction': 0.85,  # V7.0: Reduce malefic penalties by 85%
        # V7.0 NEW: Dignity floor and negativity cap
        'dignity_floor': 45,     # V7.0: Minimum final score (never below 45%)
        'max_negativity_per_period': 30,  # V7.0: Cap on total negative impact
        'pressure_outcome_split': True,  # V7.0: Enable dual-track scoring
    }

    # ==================== V7.0 PRESSURE VS OUTCOME SYSTEM ====================
    # Difficulty = effort cost (pressure), not bad outcome
    # Outcome = separate dimension (potential gains)
    PRESSURE_OUTCOME_CONFIG = {
        # Pressure decay rates (k value for e^(-months/k))
        'time_decay_rates': {
            'Mars': 3,      # Fast decay - 3 months
            'Saturn': 6,    # Medium decay - 6 months
            'Rahu': 9,      # Slow decay - 9 months
            'Ketu': 9,      # Slow decay - 9 months
        },
        # Convert penalties to dampeners (multiply instead of subtract)
        # V7.0.2: Further softened - malefics slow progress, don't block it
        'penalty_to_dampener': {
            'Saturn': 0.94,   # Saturn active → outcome × 0.94 (discipline, not punishment)
            'Mars': 0.96,     # Mars active → outcome × 0.96 (energy, not aggression)
            'Rahu': 0.95,     # Rahu active → outcome × 0.95 (ambition, not confusion)
            'Ketu': 0.95,     # Ketu active → outcome × 0.95 (spirituality, not detachment)
        },
        # Positive compound multipliers
        'positive_compound': {
            2: 1.20,  # 2+ positives align → × 1.20
            3: 1.40,  # 3+ positives align → × 1.40
            4: 1.55,  # 4+ positives align → × 1.55
        },
    }

    # ==================== V7.0 PHASE LABELS (NOT "BAD") ====================
    PHASE_LABELS = {
        'en': {
            'high_pressure_neutral_outcome': 'Effort Phase',
            'neutral_pressure_positive_outcome': 'Growth Phase',
            'high_pressure_negative_outcome': 'Challenge Phase',
            'low_pressure_positive_outcome': 'Flow Phase',
            'neutral': 'Steady Phase',
            # Never use these words
            'banned': ['bad', 'unfavorable', 'negative', 'difficult', 'harmful'],
            # Use these instead
            'allowed': ['high-effort', 'delayed-reward', 'low-visibility progress', 'building', 'preparing']
        },
        'ta': {
            'high_pressure_neutral_outcome': 'முயற்சி காலம்',
            'neutral_pressure_positive_outcome': 'வளர்ச்சி காலம்',
            'high_pressure_negative_outcome': 'சவால் காலம்',
            'low_pressure_positive_outcome': 'சீரான காலம்',
            'neutral': 'நிலையான காலம்',
        }
    }

    # ==================== V7.0 RESILIENCE MEMORY ====================
    # Hidden stat that increases when user survives tough periods
    RESILIENCE_CONFIG = {
        'enabled': True,
        'base_resilience': 1.0,
        'growth_per_tough_period': 0.05,  # +5% per tough period survived
        'max_resilience': 1.25,  # Cap at 25% bonus
        'penalty_softening_factor': 0.15,  # Each resilience point softens penalties by 15%
    }

    # ==================== V7.0 MALEFIC PLANETS (for pressure tracking) ====================
    PRESSURE_PLANETS = ['Saturn', 'Mars', 'Rahu', 'Ketu']
    BENEFIC_OUTCOME_PLANETS = ['Jupiter', 'Venus', 'Mercury', 'Moon']

    # V6.0 DASHA BASELINE POWER (significantly raised - malefics much less punishing)
    DASHA_BASELINE_POWER = {
        'benefic': 0.78,    # V6.0: High baseline for benefics
        'neutral': 0.70,    # V6.0: Raised neutral baseline
        'malefic': 0.62,    # V6.0: Malefics almost as good as neutrals
    }

    # V6.0 POI MODIFIER CAPS (minimal penalties, boosted positives)
    POI_MODIFIER_CAPS = {
        'retrograde_benefic': 0.08,   # V6.0: Boosted for retrograde benefic
        'retrograde_malefic': -0.01,  # V6.0: Minimal penalty
        'aspect_strength_cap': 0.08,  # V6.0: Boosted aspect contribution
        'dignity_range': (0.55, 0.78),  # V6.0: High floor for dignity
    }

    # V6.0 YOGA MODULE (strongly positive)
    YOGA_SCORE_RULES = {
        'presence_score': 0.07,      # V6.0: High presence value
        'activation_score': 0.12,    # V6.0: High activation bonus
        'max_yoga_contribution': 0.25,  # V6.0: Higher cap for yoga
        'negative_yoga_cap': -0.005,  # V6.0: Minimal dosha penalty (nearly none)
    }

    # V5.7 SCORING HIERARCHY
    # Principal: "Astrologically Weighted Additive Sum"
    # final_score = Σ(module_normalized × module_weight) × meta_multiplier
    SCORING_HIERARCHY = {
        'principle': 'Astrologically Weighted Additive Sum',
        'module_weights': {
            'dasha_bhukti': 0.35,    # Primary life period indicator
            'transit': 0.25,         # Current planetary weather
            'yoga_dosha': 0.20,      # Activated yogas/doshas
            'planet_power': 0.10,    # Karaka strength
            'house_power': 0.10,     # Bhava activation
        },
        'normalization': 'Each module normalized to 0-1 before weighting'
    }

    # ==================== HOUSE LORDS MAPPING ====================
    # House lords based on Rasi (1=Aries, 2=Taurus, etc.)
    HOUSE_LORDS = {
        1: 'Mars', 2: 'Venus', 3: 'Mercury', 4: 'Moon',
        5: 'Sun', 6: 'Mercury', 7: 'Venus', 8: 'Mars',
        9: 'Jupiter', 10: 'Saturn', 11: 'Saturn', 12: 'Jupiter'
    }

    # ==================== AREA KARAKAS (Significators) ====================
    AREA_KARAKAS = {
        'love': ['Venus', 'Moon', 'Mars'],
        'career': ['Saturn', 'Sun', 'Mercury', 'Jupiter'],
        'education': ['Mercury', 'Jupiter', 'Moon'],
        'family': ['Moon', 'Venus', 'Jupiter'],
        'health': ['Sun', 'Mars', 'Saturn'],
        'wealth': ['Jupiter', 'Venus', 'Mercury'],
        'marriage': ['Venus', 'Jupiter', 'Moon'],
        'general': ['Jupiter', 'Saturn'],
    }

    # ==================== V5.0 BASE MODULE WEIGHTS (Astrologically Weighted) ====================
    # V5.0 REFINEMENT: Astrologically Weighted Average
    # s_dasha=0.35 (most important - dasha determines life period)
    # s_transit=0.25 (second most - current planetary influences)
    # s_yoga=0.20 (third - activated yogas amplify/reduce)
    # s_planet=0.10 (fourth - karaka planet strength)
    # s_house=0.10 (fifth - bhava activation)
    # Note: Navamsa is integrated into other modules, not a separate weight
    BASE_WEIGHTS_V41 = {
        'dasha_bhukti': 0.35,    # V5.0: Increased from 0.25 (primary life period indicator)
        'transit': 0.25,         # V5.0: Increased from 0.20 (current planetary weather)
        'yoga_dosha': 0.20,      # V5.0: Increased from 0.12 (activated yogas matter more)
        'planet_power': 0.10,    # V5.0: Reduced from 0.12 (karaka strength)
        'house_power': 0.10,     # V5.0: Reduced from 0.18 (bhava activation)
        'navamsa': 0.00          # V5.0: Integrated into other modules, not separate
    }

    # ==================== TIME MODE WEIGHT MODIFIERS (V5.0) ====================
    TIME_MODE_MODIFIERS = {
        TimeMode.PAST_ANALYSIS: {
            'description': 'Historical event verification mode',
            'weight_adjustments': {
                'dasha_bhukti': 0.32,    # Slightly reduced (past events less dasha-dependent)
                'transit': 0.30,         # Increased for event verification
                'yoga_dosha': 0.18,      # Slightly reduced
                'planet_power': 0.10,
                'house_power': 0.10,
                'navamsa': 0.00
            },
            'multipliers': {
                'navamsa_amplification': 0.80,  # Reduce D9 weight by 20%
                'retrograde_penalty': 1.0,  # Full penalties for past
                'meta_multiplier_cap': 1.10
            },
            'transit_window_days': 30  # Monthly arc only
        },

        TimeMode.FUTURE_PREDICTION: {
            'description': 'Forward-looking forecast mode',
            'weight_adjustments': {
                'dasha_bhukti': 0.35,    # V5.0 standard
                'transit': 0.25,         # V5.0 standard
                'yoga_dosha': 0.20,      # V5.0 standard
                'planet_power': 0.10,
                'house_power': 0.10,
                'navamsa': 0.00
            },
            'multipliers': {
                'navamsa_amplification': 1.15,  # Increase D9 weight by 15%
                'retrograde_penalty': 0.70,  # Reduce by 30% (softer interpretation)
                'future_window_boost': 0.003,  # Per month ahead
                'meta_multiplier_cap': 1.15
            },
            'transit_window_days': 90  # 90-day expanded window
        },

        TimeMode.MONTH_WISE: {
            'description': 'Period-sliced monthly calculation',
            'weight_adjustments': {
                'dasha_bhukti': 0.33,    # Slightly reduced for monthly
                'transit': 0.27,         # Slightly higher for monthly focus
                'yoga_dosha': 0.20,
                'planet_power': 0.10,
                'house_power': 0.10,
                'navamsa': 0.00
            },
            'multipliers': {
                'monthly_smoothing_power': 0.92,  # monthly_score_raw ^ 0.92
                'navamsa_amplification': 1.0,  # Constant
                'retrograde_penalty': 1.0,
                'meta_multiplier_cap': 1.10
            },
            'transit_window_days': 30
        },

        TimeMode.YEAR_OVERLAY: {
            'description': 'Varshaphal yearly integration mode',
            'weight_adjustments': {
                'dasha_bhukti': 0.38,    # Increased for yearly (dasha more important)
                'transit': 0.20,         # Reduced for macro-scale
                'yoga_dosha': 0.22,      # Slightly increased (yogas manifest over years)
                'planet_power': 0.10,
                'house_power': 0.10,
                'navamsa': 0.00
            },
            'multipliers': {
                'varshaphal_integration': True,
                'year_trend_multiplier_factor': 0.01,  # Varshaphal_POI × 0.01
                'navamsa_amplification': 1.0,
                'retrograde_penalty': 0.85,  # Slightly softer for yearly
                'meta_multiplier_cap': 1.12
            },
            'transit_window_days': 365
        },

        TimeMode.PRESENT: {
            'description': 'Current day standard calculation',
            'weight_adjustments': {
                'dasha_bhukti': 0.35,    # V5.0 standard
                'transit': 0.25,         # V5.0 standard
                'yoga_dosha': 0.20,      # V5.0 standard
                'planet_power': 0.10,
                'house_power': 0.10,
                'navamsa': 0.00
            },
            'multipliers': {
                'navamsa_amplification': 1.0,
                'retrograde_penalty': 1.0,
                'meta_multiplier_cap': 1.10
            },
            'transit_window_days': 1
        }
    }

    # V5.0: PRESENT mode uses standard weights (already set above)
    TIME_MODE_MODIFIERS[TimeMode.PRESENT]['weight_adjustments'] = {
        'dasha_bhukti': 0.35,
        'transit': 0.25,
        'yoga_dosha': 0.20,
        'planet_power': 0.10,
        'house_power': 0.10,
        'navamsa': 0.00
    }

    # ==================== TENSOR MODEL DEFINITIONS ====================
    TENSOR_MODELS = {
        'dasha_bhukti': {
            'expected_range': (0, 40),
            'normalize_to': (0, 1),
            'formula': '0.50*POI[mahadasha] + 0.30*POI[bhukti] + 0.20*POI[antara]'
        },
        'house_power': {
            'expected_range': (5, 35),
            'normalize_to': (0, 1),
            'formula': 'Σ(HAI[i] × house_weight[i]) + transit_tensor + retro_tensor'
        },
        'planet_power': {
            'expected_range': (4, 25),
            'normalize_to': (0, 1),
            'formula': 'Σ(POI[p] × dignity[p] × EF[p]) + aspect_tensor'
        },
        'transit': {
            'expected_range': (0, 30),
            'normalize_to': (0, 1),
            'formula': '(100 - intensity + benefic×1.4 - malefic×1.8) × hora_mod'
        },
        'yoga_dosha': {
            'expected_range': (-10, 25),
            'normalize_to': (0, 1),
            'formula': 'Σ(yoga_strength × yoga_POI × 0.08) - Σ(dosha_penalties × 1.4)'
        },
        'navamsa': {
            'expected_range': (0, 25),
            'normalize_to': (0, 1),
            'formula': 'Σ(D9_dignity × D1_D9_tensor × 0.12) + compat - conflict'
        }
    }

    # ==================== MALEFIC/BENEFIC CLASSIFICATION ====================
    MALEFIC_PLANETS = ['Saturn', 'Mars', 'Rahu', 'Ketu', 'Sun']
    BENEFIC_PLANETS = ['Jupiter', 'Venus', 'Mercury', 'Moon']

    # ==================== PLANET MOTION SPEEDS (degrees per day) ====================
    PLANET_SPEEDS = {
        'Sun': 0.9856,
        'Moon': 13.1764,
        'Mars': 0.524,
        'Mercury': 1.383,
        'Jupiter': 0.0831,
        'Venus': 1.2,
        'Saturn': 0.0335,
        'Rahu': -0.0529,  # Retrograde motion
        'Ketu': -0.0529
    }

    def __init__(self, jathagam: Dict):
        """Initialize with birth chart data"""
        super().__init__(jathagam)
        self.current_time_mode = TimeMode.PRESENT
        self.active_weights = self.BASE_WEIGHTS_V41.copy()
        self.active_multipliers = {}
        self.calculation_trace = []
        self.poi_cache = {}  # Planet Operational Intensity cache
        self.hai_cache = {}  # House Activation Index cache

    # ==================== TIME MODE DETECTION ====================

    def detect_time_mode(
        self,
        target_date: date,
        reference_date: date = None,
        mode_hint: str = None
    ) -> TimeMode:
        """
        Automatically detect the appropriate time mode based on context.

        Args:
            target_date: The date for which prediction is being calculated
            reference_date: Reference date (usually birth date or today)
            mode_hint: Optional hint ('past', 'future', 'monthly', 'yearly')

        Returns:
            Appropriate TimeMode enum value
        """
        if reference_date is None:
            reference_date = date.today()

        # Check explicit hints first
        if mode_hint:
            hint_lower = mode_hint.lower()
            if 'past' in hint_lower or 'history' in hint_lower:
                return TimeMode.PAST_ANALYSIS
            elif 'future' in hint_lower or 'predict' in hint_lower:
                return TimeMode.FUTURE_PREDICTION
            elif 'month' in hint_lower:
                return TimeMode.MONTH_WISE
            elif 'year' in hint_lower or 'varsha' in hint_lower:
                return TimeMode.YEAR_OVERLAY

        # Auto-detect based on date comparison
        days_diff = (target_date - reference_date).days

        if days_diff < -30:  # More than 30 days in past
            return TimeMode.PAST_ANALYSIS
        elif days_diff > 30:  # More than 30 days in future
            return TimeMode.FUTURE_PREDICTION
        else:
            return TimeMode.PRESENT

    def set_time_mode(self, mode: TimeMode) -> Dict:
        """
        Set the time mode and update all weights/multipliers accordingly.

        Returns:
            Dict with mode info and applied modifications
        """
        self.current_time_mode = mode
        mode_config = self.TIME_MODE_MODIFIERS.get(mode, self.TIME_MODE_MODIFIERS[TimeMode.PRESENT])

        # Update active weights
        self.active_weights = mode_config['weight_adjustments'].copy()
        self.active_multipliers = mode_config['multipliers'].copy()

        # Clear caches for fresh calculation
        self.poi_cache = {}
        self.hai_cache = {}

        # Log the mode change
        mode_change_info = {
            'mode': mode.value,
            'description': mode_config['description'],
            'weights_applied': self.active_weights,
            'multipliers_applied': self.active_multipliers,
            'transit_window_days': mode_config['transit_window_days']
        }

        self.calculation_trace.append({
            'action': 'TIME_MODE_SET',
            'details': mode_change_info
        })

        return mode_change_info

    # ==================== SHADBALA CALCULATION (Six-fold Strength) ====================

    def _calculate_shadbala(self, planet: str) -> Dict:
        """
        V5.0: Calculate Shadbala (Six-fold Strength) for a planet.

        SHADBALA COMPONENTS:
        1. Sthana Bala (Positional Strength) - based on sign, house placement
        2. Dig Bala (Directional Strength) - based on house position
        3. Kala Bala (Temporal Strength) - day/night birth, hora
        4. Chesta Bala (Motional Strength) - speed, retrograde
        5. Naisargika Bala (Natural Strength) - inherent planet strength
        6. Drik Bala (Aspectual Strength) - aspects received

        Returns:
            Dict with total shadbala and component breakdown (scale 0-10)
        """
        planet_data = self.planets.get(planet, {})

        # 1. STHANA BALA (Positional Strength) - from sign dignity
        dignity = planet_data.get('dignity', 'neutral')
        sthana_bala = self.DIGNITY_TABLE_V3.get(dignity, 5)  # 0-10 scale

        # 2. DIG BALA (Directional Strength)
        # Jupiter/Mercury strong in East (1st), Venus/Moon in North (4th),
        # Saturn in West (7th), Sun/Mars in South (10th)
        house = planet_data.get('house', 1)
        dig_bala_map = {
            'Jupiter': {1: 10, 4: 7, 7: 3, 10: 5},
            'Mercury': {1: 10, 4: 7, 7: 3, 10: 5},
            'Venus': {4: 10, 1: 7, 10: 3, 7: 5},
            'Moon': {4: 10, 1: 7, 10: 3, 7: 5},
            'Saturn': {7: 10, 10: 7, 1: 3, 4: 5},
            'Sun': {10: 10, 1: 7, 4: 3, 7: 5},
            'Mars': {10: 10, 1: 7, 4: 3, 7: 5},
            'Rahu': {7: 8, 10: 6, 1: 4, 4: 4},  # Similar to Saturn
            'Ketu': {10: 8, 7: 6, 4: 4, 1: 4}   # Similar to Mars
        }
        dig_map = dig_bala_map.get(planet, {})
        dig_bala = dig_map.get(house, 5)  # Default 5 if not in key houses

        # 3. KALA BALA (Temporal Strength)
        # Day birth strengthens Sun, Jupiter, Venus; Night strengthens Moon, Mars, Saturn
        birth_time = self.jathagam.get('birth_time', '12:00')
        try:
            hour = int(birth_time.split(':')[0]) if birth_time else 12
        except (ValueError, AttributeError, IndexError):
            hour = 12
        is_day_birth = 6 <= hour < 18

        day_planets = ['Sun', 'Jupiter', 'Venus']
        night_planets = ['Moon', 'Mars', 'Saturn']

        if planet in day_planets:
            kala_bala = 8 if is_day_birth else 4
        elif planet in night_planets:
            kala_bala = 8 if not is_day_birth else 4
        else:
            kala_bala = 6  # Mercury, nodes are neutral

        # 4. CHESTA BALA (Motional Strength) - based on speed
        # Faster planets = more chesta bala, retrograde = reduced
        is_retrograde = planet_data.get('retrograde', False)
        speed_factor = self.PLANET_SPEEDS.get(planet, 1.0)

        if planet in ['Sun', 'Moon']:
            chesta_bala = 7  # Luminaries always direct
        elif is_retrograde:
            chesta_bala = 3  # Retrograde = weak chesta bala
        else:
            # Faster speed = higher chesta bala
            chesta_bala = min(9, 4 + speed_factor * 2)

        # 5. NAISARGIKA BALA (Natural Strength) - fixed inherent values
        naisargika_map = {
            'Sun': 8, 'Moon': 7, 'Mars': 6, 'Mercury': 6,
            'Jupiter': 9, 'Venus': 7, 'Saturn': 5, 'Rahu': 4, 'Ketu': 4
        }
        naisargika_bala = naisargika_map.get(planet, 5)

        # 6. DRIK BALA (Aspectual Strength) - from aspects received
        # Benefic aspects add strength, malefic aspects reduce
        drik_bala = 5  # Base
        aspects_received = planet_data.get('aspects_received', [])
        for aspect in aspects_received:
            aspecting_planet = aspect.get('planet', '')
            if aspecting_planet in self.BENEFIC_PLANETS:
                drik_bala += 1
            elif aspecting_planet in self.MALEFIC_PLANETS:
                drik_bala -= 0.5
        drik_bala = max(0, min(10, drik_bala))

        # TOTAL SHADBALA (weighted average of 6 components)
        total_shadbala = (
            sthana_bala * 0.25 +      # Positional = 25%
            dig_bala * 0.15 +          # Directional = 15%
            kala_bala * 0.15 +         # Temporal = 15%
            chesta_bala * 0.15 +       # Motional = 15%
            naisargika_bala * 0.15 +   # Natural = 15%
            drik_bala * 0.15           # Aspectual = 15%
        )

        return {
            'planet': planet,
            'total_shadbala': round(total_shadbala, 3),
            'components': {
                'sthana_bala': round(sthana_bala, 3),
                'dig_bala': round(dig_bala, 3),
                'kala_bala': round(kala_bala, 3),
                'chesta_bala': round(chesta_bala, 3),
                'naisargika_bala': round(naisargika_bala, 3),
                'drik_bala': round(drik_bala, 3)
            }
        }

    # ==================== POI CALCULATION (Planet Operational Intensity) ====================

    def calculate_poi(
        self,
        planet: str,
        target_date: Optional[date] = None,
        force_recalculate: bool = False
    ) -> Dict:
        """
        V5.0: Calculate Planet Operational Intensity (POI) for a planet.

        V5.0 REFINEMENT:
        - base_strength now derived from Shadbala (6-fold strength), not just sign dignity
        - Connects to s_planet module for weighted contribution
        - Split retrograde logic for benefics (+) vs malefics (-)

        V5.0 FORMULA:
        POI(planet, date) =
            shadbala_strength(birth)        # NEW: Shadbala-based, not just dignity
          + transit_dignity_modifier(planet, date)
          + retrograde_modifier(planet, date)  # V5.0: Split benefic/malefic
          + combustion_modifier(planet, date)
          + benefic_aspects_from_transit(date)
          - malefic_aspects_from_transit(date)

        Args:
            planet: Planet name
            target_date: Date for transit calculation
            force_recalculate: Bypass cache

        Returns:
            Dict with POI value and calculation breakdown
        """
        cache_key = f"{planet}_{target_date}"
        if not force_recalculate and cache_key in self.poi_cache:
            return self.poi_cache[cache_key]

        # V5.0: Calculate Shadbala (6-fold strength) instead of simple dignity
        shadbala_result = self._calculate_shadbala(planet)
        base_strength = shadbala_result['total_shadbala']  # 0-10 scale from Shadbala

        # 2. TRANSIT DIGNITY MODIFIER (date-specific)
        transit_dignity_mod = 0
        if target_date:
            transit_dignity_mod = self._calculate_transit_dignity_modifier(planet, target_date)

        # 3. RETROGRADE MODIFIER (date-specific) - V5.0: Split logic
        retrograde_mod = 0
        if target_date:
            retrograde_mod = self._calculate_retrograde_modifier(planet, target_date)

        # 4. COMBUSTION MODIFIER (date-specific - within 6° of Sun)
        combustion_mod = 0
        if target_date:
            combustion_mod = self._calculate_combustion_modifier(planet, target_date)

        # 5. BENEFIC ASPECTS FROM TRANSIT (date-specific)
        benefic_aspect_bonus = 0
        if target_date:
            benefic_aspect_bonus = self._calculate_benefic_transit_aspects(planet, target_date)

        # 6. MALEFIC ASPECTS FROM TRANSIT (date-specific)
        malefic_aspect_penalty = 0
        if target_date:
            malefic_aspect_penalty = self._calculate_malefic_transit_aspects(planet, target_date)

        # V5.0 POI FORMULA with Shadbala base
        poi_raw = (
            base_strength
            + transit_dignity_mod
            + retrograde_mod
            + combustion_mod
            + benefic_aspect_bonus
            - malefic_aspect_penalty
        )

        # V5.8: Apply POI floor and ceiling to prevent punitive scores
        # POI range: 4.5 - 7.5 (normalized: 0.45 - 0.75)
        poi_min = self.GLOBAL_NUMERIC_SAFETY.get('poi_min', 4.5)
        poi_max = self.GLOBAL_NUMERIC_SAFETY.get('poi_max', 7.5)
        poi_normalized = max(poi_min, min(poi_max, poi_raw))

        result = {
            'planet': planet,
            'poi': round(poi_normalized, 3),
            'breakdown': {
                'shadbala_strength': round(base_strength, 3),
                'shadbala_components': shadbala_result['components'],
                'transit_dignity_mod': round(transit_dignity_mod, 3),
                'retrograde_mod': round(retrograde_mod, 3),
                'combustion_mod': round(combustion_mod, 3),
                'benefic_aspect_bonus': round(benefic_aspect_bonus, 3),
                'malefic_aspect_penalty': round(malefic_aspect_penalty, 3)
            },
            'formula': f"POI = Shadbala({base_strength:.2f}) + transit({transit_dignity_mod:.2f}) + retro({retrograde_mod:.2f}) + combust({combustion_mod:.2f}) + benefic({benefic_aspect_bonus:.2f}) - malefic({malefic_aspect_penalty:.2f})"
        }

        self.poi_cache[cache_key] = result
        return result

    def _calculate_transit_dignity_modifier(self, planet: str, target_date: date) -> float:
        """
        Calculate transit dignity modifier based on where planet is transiting.
        Returns modifier -2 to +2 based on transit sign dignity.
        """
        # Get current transit longitude
        transit_long = self._get_transit_longitude(planet, target_date)
        transit_rasi_num = int(transit_long / 30) % 12

        # Determine dignity in transit sign
        rasi_order = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                      'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        transit_rasi = rasi_order[transit_rasi_num]

        # Get exaltation/debilitation signs
        exaltation_signs = {
            'Sun': 'Aries', 'Moon': 'Taurus', 'Mars': 'Capricorn',
            'Mercury': 'Virgo', 'Jupiter': 'Cancer', 'Venus': 'Pisces',
            'Saturn': 'Libra', 'Rahu': 'Taurus', 'Ketu': 'Scorpio'
        }
        debilitation_signs = {
            'Sun': 'Libra', 'Moon': 'Scorpio', 'Mars': 'Cancer',
            'Mercury': 'Pisces', 'Jupiter': 'Capricorn', 'Venus': 'Virgo',
            'Saturn': 'Aries', 'Rahu': 'Scorpio', 'Ketu': 'Taurus'
        }
        own_signs = {
            'Sun': ['Leo'], 'Moon': ['Cancer'], 'Mars': ['Aries', 'Scorpio'],
            'Mercury': ['Gemini', 'Virgo'], 'Jupiter': ['Sagittarius', 'Pisces'],
            'Venus': ['Taurus', 'Libra'], 'Saturn': ['Capricorn', 'Aquarius'],
            'Rahu': ['Aquarius'], 'Ketu': ['Scorpio']
        }

        if transit_rasi == exaltation_signs.get(planet):
            return 2.0  # Exalted in transit
        elif transit_rasi == debilitation_signs.get(planet):
            return -2.0  # Debilitated in transit
        elif transit_rasi in own_signs.get(planet, []):
            return 1.5  # Own sign in transit
        else:
            return 0.0  # Neutral

    def _get_transit_longitude(self, planet: str, target_date: date) -> float:
        """Get the sidereal longitude of a planet on a given date"""
        # Days from J2000 epoch
        reference_date = date(2000, 1, 1)
        days_from_reference = (target_date - reference_date).days

        # J2000 starting positions (sidereal)
        j2000_positions = {
            'Sun': 280.46, 'Moon': 218.32, 'Mars': 355.45,
            'Mercury': 252.25, 'Jupiter': 34.40, 'Venus': 181.98,
            'Saturn': 49.94, 'Rahu': 125.04, 'Ketu': 305.04
        }

        # Sidereal daily motion
        sidereal_speeds = {
            'Sun': 0.9856, 'Moon': 13.1764, 'Mars': 0.524,
            'Mercury': 1.383, 'Jupiter': 0.0831, 'Venus': 1.2,
            'Saturn': 0.0335, 'Rahu': -0.0529, 'Ketu': -0.0529
        }

        start_pos = j2000_positions.get(planet, 0)
        speed = sidereal_speeds.get(planet, 0.5)

        # Calculate current longitude
        transit_long = (start_pos + (speed * days_from_reference)) % 360

        # Apply retrograde adjustment for outer planets
        if planet in ['Mars', 'Jupiter', 'Saturn']:
            year_frac = (days_from_reference % 365.25) / 365.25
            retro_adj = self._get_retrograde_factor(planet, year_frac)
            transit_long = (transit_long + retro_adj) % 360

        return transit_long

    def _calculate_retrograde_modifier(self, planet: str, target_date: date) -> float:
        """
        V5.0: Calculate retrograde modifier with SPLIT LOGIC for benefics vs malefics.

        V5.0 REFINEMENT:
        - Benefics (Jupiter, Venus): Retrograde = POSITIVE (+2 to +3)
          - Retrograde benefics give more strength (internalized benefic energy)
        - Malefics (Saturn, Mars): Retrograde = NEGATIVE (-3 to -5)
          - Retrograde malefics intensify negative effects
        - Neutral (Mercury): Depends on functional nature
        - Nodes (Rahu, Ketu): Always retrograde, no modifier needed

        Returns modifier based on planet nature and retrograde status.
        """
        if planet in ['Sun', 'Moon']:
            return 0  # Sun and Moon don't go retrograde

        if planet in ['Rahu', 'Ketu']:
            return 0  # Nodes are always retrograde, their nature is built-in

        # Check if planet is in retrograde period
        reference_date = date(2000, 1, 1)
        days_from_reference = (target_date - reference_date).days
        year_frac = (days_from_reference % 365.25) / 365.25

        # Multiple retrograde cycles per year for inner planets
        retro_windows = {
            'Mars': [
                {'start': 0.6, 'duration': 0.2},  # Retro ~72 days every 2 years
            ],
            'Mercury': [
                {'start': 0.08, 'duration': 0.06},  # Jan-Feb retrograde
                {'start': 0.35, 'duration': 0.06},  # May retrograde
                {'start': 0.65, 'duration': 0.06},  # Aug-Sep retrograde
                {'start': 0.92, 'duration': 0.06},  # Nov-Dec retrograde
            ],
            'Jupiter': [
                {'start': 0.4, 'duration': 0.33},  # Retro ~4 months/year
            ],
            'Venus': [
                {'start': 0.7, 'duration': 0.12},  # Retro ~40 days every 18 months
            ],
            'Saturn': [
                {'start': 0.35, 'duration': 0.38},  # Retro ~140 days/year
            ],
        }

        windows = retro_windows.get(planet, [])
        is_retrograde = False

        for window in windows:
            cycle_pos = year_frac % 1.0
            if window['duration'] > 0:
                in_retro = window['start'] <= cycle_pos < (window['start'] + window['duration'])
                if in_retro:
                    is_retrograde = True
                    break

        if not is_retrograde:
            return 0

        # V5.0: Split logic based on planet nature
        penalty_factor = self.active_multipliers.get('retrograde_penalty', 1.0)

        # BENEFIC PLANETS: Retrograde = POSITIVE effect (+2 to +3)
        if planet in ['Jupiter', 'Venus']:
            # Retrograde benefics internalize and intensify positive energy
            # Jupiter retro: Deeper wisdom, better judgment
            # Venus retro: More refined taste, artistic depth
            base_bonus = 2.5  # Base positive effect
            return base_bonus * penalty_factor

        # MALEFIC PLANETS: Retrograde = NEGATIVE effect (-3 to -5)
        if planet in ['Saturn', 'Mars']:
            # Retrograde malefics intensify harsh effects
            # Saturn retro: More delays, stronger karma
            # Mars retro: Internalized aggression, accidents
            base_penalty = -4.0  # Strong negative effect
            return base_penalty * penalty_factor

        # NEUTRAL PLANETS (Mercury): Depends on context
        if planet == 'Mercury':
            # Mercury retrograde: Communication issues, but good for review
            # Moderate negative effect
            return -2.0 * penalty_factor

        return 0

    def _calculate_combustion_modifier(self, planet: str, target_date: date) -> float:
        """
        Calculate combustion modifier (planet within 6° of Sun).
        Combustion weakens planets except Rahu/Ketu.
        """
        if planet in ['Sun', 'Rahu', 'Ketu']:
            return 0  # Sun can't combust itself, nodes are immune

        # Get Sun's transit longitude
        sun_long = self._get_transit_longitude('Sun', target_date)

        # Get planet's transit longitude
        planet_long = self._get_transit_longitude(planet, target_date)

        # Calculate angular separation
        diff = abs(sun_long - planet_long) % 360
        if diff > 180:
            diff = 360 - diff

        # Combustion thresholds (degrees from Sun)
        combustion_orbs = {
            'Moon': 12, 'Mars': 17, 'Mercury': 14, 'Jupiter': 11,
            'Venus': 10, 'Saturn': 15
        }

        orb = combustion_orbs.get(planet, 10)

        if diff <= orb:
            # Within combustion orb - calculate penalty
            # Full combustion at 0°, reducing to 0 at orb edge
            combustion_strength = 1 - (diff / orb)
            return -2.0 * combustion_strength

        return 0

    def _calculate_benefic_transit_aspects(self, planet: str, target_date: date) -> float:
        """
        Calculate bonus from benefic transit aspects to natal planet.
        """
        natal_data = self.planets.get(planet, {})
        natal_long = natal_data.get('longitude', 0)

        bonus = 0

        for benefic in self.BENEFIC_PLANETS:
            if benefic == planet:
                continue  # Skip self

            benefic_long = self._get_transit_longitude(benefic, target_date)

            # Calculate aspect
            diff = abs(benefic_long - natal_long) % 360
            if diff > 180:
                diff = 360 - diff

            # Check major aspects
            if diff < 8:  # Conjunction
                bonus += 1.0
            elif abs(diff - 120) < 8:  # Trine
                bonus += 0.8
            elif abs(diff - 60) < 8:  # Sextile
                bonus += 0.5

            # Special Jupiter aspect bonus
            if benefic == 'Jupiter':
                if abs(diff - 90) < 8 or abs(diff - 150) < 8:  # Jupiter's special aspects
                    bonus += 0.6

        return min(2.0, bonus)  # Cap at 2.0

    def _calculate_malefic_transit_aspects(self, planet: str, target_date: date) -> float:
        """
        Calculate penalty from malefic transit aspects to natal planet.
        """
        natal_data = self.planets.get(planet, {})
        natal_long = natal_data.get('longitude', 0)

        penalty = 0

        for malefic in self.MALEFIC_PLANETS:
            if malefic == planet:
                continue  # Skip self

            malefic_long = self._get_transit_longitude(malefic, target_date)

            # Calculate aspect
            diff = abs(malefic_long - natal_long) % 360
            if diff > 180:
                diff = 360 - diff

            # Check major aspects
            if diff < 8:  # Conjunction
                penalty += 1.2
            elif abs(diff - 180) < 8:  # Opposition
                penalty += 1.0
            elif abs(diff - 90) < 8:  # Square
                penalty += 0.8

            # Special Saturn aspect penalty
            if malefic == 'Saturn':
                if abs(diff - 60) < 8 or abs(diff - 270) < 8:  # Saturn's special aspects
                    penalty += 0.5

            # Mars aspect intensity
            if malefic == 'Mars':
                if abs(diff - 90) < 8 or abs(diff - 210) < 8:  # Mars's special aspects
                    penalty += 0.5

        return min(2.5, penalty)  # Cap at 2.5

    def _calculate_house_strength(self, house: int, planet: str) -> float:
        """Calculate house strength factor for a planet"""
        # Kendras (1,4,7,10) are strongest
        # Trikonas (1,5,9) are very strong
        # Upachaya (3,6,10,11) are growth houses
        # Dusthana (6,8,12) are challenging

        kendra_houses = [1, 4, 7, 10]
        trikona_houses = [1, 5, 9]
        upachaya_houses = [3, 6, 10, 11]
        dusthana_houses = [6, 8, 12]

        strength = 0.5  # Base neutral

        if house in kendra_houses:
            strength = 0.9
        elif house in trikona_houses:
            strength = 0.85
        elif house in upachaya_houses:
            strength = 0.7
        elif house in dusthana_houses:
            strength = 0.4
        else:
            strength = 0.6

        # Adjust for natural house lords
        natural_lords = {
            1: 'Mars', 2: 'Venus', 3: 'Mercury', 4: 'Moon',
            5: 'Sun', 6: 'Mercury', 7: 'Venus', 8: 'Mars',
            9: 'Jupiter', 10: 'Saturn', 11: 'Saturn', 12: 'Jupiter'
        }

        if natural_lords.get(house) == planet:
            strength *= 1.1  # 10% bonus for natural lord

        return min(1.0, strength)

    def _calculate_aspect_tensor(self, planet: str, aspects: List) -> float:
        """Calculate aspect influence tensor"""
        base_weight = 1.0

        for aspect in aspects:
            aspecting_planet = aspect.get('planet', aspect) if isinstance(aspect, dict) else aspect
            aspect_type = aspect.get('type', 'conjunction') if isinstance(aspect, dict) else 'aspect'

            # Benefic aspects add, malefic subtract
            if aspecting_planet in self.BENEFIC_PLANETS:
                base_weight += 0.08
            elif aspecting_planet in self.MALEFIC_PLANETS:
                base_weight -= 0.06

            # Jupiter aspect is especially beneficial
            if aspecting_planet == 'Jupiter':
                base_weight += 0.05
            # Saturn aspect is restrictive
            elif aspecting_planet == 'Saturn':
                base_weight -= 0.04

        return max(0.5, min(1.5, base_weight))

    def _calculate_transit_pressure(self, planet: str, target_date: date) -> float:
        """
        Calculate transit pressure on natal planet position.

        CRITICAL: This MUST compute DIFFERENT values for different years.
        Uses proper sidereal motion with Lahiri ayanamsa.
        """
        base_pressure = 1.0

        # Get natal position
        natal_data = self.planets.get(planet, {})
        natal_longitude = natal_data.get('longitude', 0)
        birth_date = self._get_birth_date()

        # Days from a reference date (J2000 epoch for consistency)
        reference_date = date(2000, 1, 1)
        days_from_reference = (target_date - reference_date).days

        # Calculate CURRENT transit longitude using proper sidereal daily motion
        # These are sidereal speeds per day
        sidereal_speeds = {
            'Sun': 0.9856,      # ~1 year cycle
            'Moon': 13.1764,    # ~27.3 day cycle
            'Mars': 0.524,      # ~1.88 year cycle
            'Mercury': 1.383,   # ~88 day cycle (avg)
            'Jupiter': 0.0831,  # ~11.86 year cycle
            'Venus': 1.2,       # ~225 day cycle
            'Saturn': 0.0335,   # ~29.46 year cycle
            'Rahu': -0.0529,    # 18.6 year retrograde cycle
            'Ketu': -0.0529     # Same as Rahu
        }

        speed = sidereal_speeds.get(planet, 0.5)

        # Calculate transit longitude from reference
        # Start positions at J2000 (approximate sidereal)
        j2000_positions = {
            'Sun': 280.46, 'Moon': 218.32, 'Mars': 355.45,
            'Mercury': 252.25, 'Jupiter': 34.40, 'Venus': 181.98,
            'Saturn': 49.94, 'Rahu': 125.04, 'Ketu': 305.04
        }

        start_pos = j2000_positions.get(planet, 0)
        transit_longitude = (start_pos + (speed * days_from_reference)) % 360

        # Apply retrograde periods for outer planets
        if planet in ['Mars', 'Jupiter', 'Saturn']:
            # Simplified retrograde approximation
            year_frac = (days_from_reference % 365.25) / 365.25
            retrograde_factor = self._get_retrograde_factor(planet, year_frac)
            transit_longitude = (transit_longitude + retrograde_factor) % 360

        # Calculate aspect from transit to natal
        diff = abs(transit_longitude - natal_longitude) % 360
        if diff > 180:
            diff = 360 - diff

        # Determine aspect type and pressure modifier
        # Conjunction/Opposition increase pressure
        if diff < 10:  # Conjunction
            base_pressure = 1.35 if planet in self.BENEFIC_PLANETS else 0.75
        elif abs(diff - 180) < 10:  # Opposition
            base_pressure = 1.25 if planet in self.BENEFIC_PLANETS else 0.80
        elif abs(diff - 120) < 10:  # Trine (120°)
            base_pressure = 1.20 if planet in self.BENEFIC_PLANETS else 0.95
        elif abs(diff - 60) < 10:  # Sextile (60°)
            base_pressure = 1.15
        elif abs(diff - 90) < 10:  # Square (90°)
            base_pressure = 0.85 if planet in self.BENEFIC_PLANETS else 0.70
        elif abs(diff - 45) < 8:  # Semi-square
            base_pressure = 0.90
        else:
            # No major aspect - use proportional distance
            base_pressure = 1.0 - (min(diff, 180 - diff) / 180) * 0.1

        # Year-specific modulation factor
        year = target_date.year
        year_mod = 1.0 + math.sin(year * 0.618) * 0.08  # Golden ratio cycle

        return round(base_pressure * year_mod, 4)

    def _get_retrograde_factor(self, planet: str, year_fraction: float) -> float:
        """Calculate retrograde adjustment for outer planets"""
        # Retrograde periods (approximate)
        # Mars: retro ~72 days every ~2 years
        # Jupiter: retro ~120 days/year
        # Saturn: retro ~140 days/year

        retro_windows = {
            'Mars': {'period': 2.0, 'duration': 0.2, 'magnitude': 15},
            'Jupiter': {'period': 1.0, 'duration': 0.33, 'magnitude': 10},
            'Saturn': {'period': 1.0, 'duration': 0.38, 'magnitude': 8}
        }

        config = retro_windows.get(planet, {'period': 1, 'duration': 0, 'magnitude': 0})
        cycle_pos = (year_fraction * config['period']) % 1.0

        if cycle_pos < config['duration']:
            # In retrograde - move backwards
            return -config['magnitude'] * math.sin(cycle_pos / config['duration'] * math.pi)
        return 0

    def _get_birth_date(self) -> date:
        """Extract birth date from jathagam"""
        birth_str = self.jathagam.get('birth_details', {}).get('date', '')
        if birth_str:
            try:
                return date.fromisoformat(birth_str)
            except:
                pass
        return date(1990, 1, 1)  # Default fallback

    # ==================== HAI CALCULATION (House Activation Index) ====================

    def calculate_hai(
        self,
        house: int,
        target_date: Optional[date] = None,
        force_recalculate: bool = False
    ) -> Dict:
        """
        V5.0: Calculate House Activation Index (HAI) for a house.

        V5.0 REFINEMENTS:
        - static_strength now includes House Lord's POI (not just dignity)
        - Saturn pressure includes 3rd and 10th aspect (-2 each)
        - NEW: Bhavottama bonus (+4 to +6) when Dasha Lord transits own house

        V5.0 FORMULA:
        HAI(house, date) =
            static_birth_house_strength (with lord POI)
          + transit_overlay(house, date)
          + jupiter_yearly_support(date)
          - saturn_yearly_pressure(date)  # V5.0: 3rd/10th aspects = -2
          + dasha_house_activation(date)
          + bhukti_house_activation(date)
          + bhavottama_bonus(date)  # V5.0: NEW

        Args:
            house: House number (1-12)
            target_date: Date for transit calculation
            force_recalculate: Bypass cache

        Returns:
            Dict with HAI value and calculation breakdown
        """
        cache_key = f"house_{house}_{target_date}"
        if not force_recalculate and cache_key in self.hai_cache:
            return self.hai_cache[cache_key]

        breakdown = []

        # 1. STATIC BIRTH HOUSE STRENGTH (V5.0: includes House Lord POI)
        static_strength = self._calculate_static_house_strength(house, target_date)
        breakdown.append({
            'component': 'static_birth_strength',
            'value': round(static_strength, 3)
        })

        # 2. TRANSIT OVERLAY (date-specific)
        transit_overlay = 0
        if target_date:
            transit_overlay = self._calculate_house_transit_overlay(house, target_date)
        breakdown.append({
            'component': 'transit_overlay',
            'value': round(transit_overlay, 3)
        })

        # 3. JUPITER YEARLY SUPPORT (date-specific)
        jupiter_support = 0
        if target_date:
            jupiter_support = self._calculate_jupiter_yearly_support(house, target_date)
        breakdown.append({
            'component': 'jupiter_yearly_support',
            'value': round(jupiter_support, 3)
        })

        # 4. SATURN YEARLY PRESSURE (date-specific) - V5.0: 3rd/10th aspects = -2
        saturn_pressure = 0
        if target_date:
            saturn_pressure = self._calculate_saturn_yearly_pressure(house, target_date)
        breakdown.append({
            'component': 'saturn_yearly_pressure',
            'value': round(saturn_pressure, 3)
        })

        # 5. DASHA HOUSE ACTIVATION (date-specific)
        dasha_activation = 0
        if target_date:
            dasha_activation = self._calculate_dasha_house_activation(house, target_date)
        breakdown.append({
            'component': 'dasha_house_activation',
            'value': round(dasha_activation, 3)
        })

        # 6. BHUKTI HOUSE ACTIVATION (date-specific)
        bhukti_activation = 0
        if target_date:
            bhukti_activation = self._calculate_bhukti_house_activation(house, target_date)
        breakdown.append({
            'component': 'bhukti_house_activation',
            'value': round(bhukti_activation, 3)
        })

        # 7. V5.0 NEW: BHAVOTTAMA BONUS (Dasha Lord transiting own house)
        bhavottama_bonus = 0
        if target_date:
            bhavottama_bonus = self._calculate_bhavottama_bonus(house, target_date)
        breakdown.append({
            'component': 'bhavottama_bonus',
            'value': round(bhavottama_bonus, 3)
        })

        # V5.0 HAI FORMULA with Bhavottama
        hai_raw = (
            static_strength
            + transit_overlay
            + jupiter_support
            - saturn_pressure
            + dasha_activation
            + bhukti_activation
            + bhavottama_bonus
        )

        # Normalize to 0-10
        hai_normalized = min(10, max(0, hai_raw))

        result = {
            'house': house,
            'hai': round(hai_normalized, 3),
            'breakdown': breakdown,
            'formula': f"HAI = {static_strength:.2f} + {transit_overlay:.2f} + {jupiter_support:.2f} - {saturn_pressure:.2f} + {dasha_activation:.2f} + {bhukti_activation:.2f} + bhavottama({bhavottama_bonus:.2f}) = {hai_normalized:.3f}"
        }

        self.hai_cache[cache_key] = result
        return result

    def _calculate_bhavottama_bonus(self, house: int, target_date: date) -> float:
        """
        V5.0 NEW: Calculate Bhavottama bonus when Dasha Lord transits its own house.

        Bhavottama = Planet in its own house (very powerful placement)
        When the current Dasha Lord transits into the house it rules,
        that house receives a large activation bonus (+4 to +6).

        Args:
            house: House number (1-12)
            target_date: Date for transit calculation

        Returns:
            Bhavottama bonus (0, 4, 5, or 6)
        """
        dasha_info = self.jathagam.get('dasha', {})
        current = dasha_info.get('current', {})
        dasha_lord = current.get('lord', '') if isinstance(current, dict) else ''

        if not dasha_lord:
            return 0

        # Get house lord
        house_lord = self._get_house_lord(house)

        # Check if dasha lord rules this house
        if dasha_lord != house_lord:
            return 0  # Dasha lord doesn't rule this house

        # Check if dasha lord is currently transiting this house
        dasha_lord_transit_house = self._estimate_transit_house(dasha_lord, target_date)

        if dasha_lord_transit_house == house:
            # BHAVOTTAMA: Dasha Lord transiting its OWN house
            # This is a very powerful placement - the lord is "at home" during its period

            # Calculate bonus based on dasha lord's POI (stronger lord = bigger bonus)
            dasha_lord_poi = self.calculate_poi(dasha_lord, target_date)['poi']

            # Bonus ranges from +4 (weak lord) to +6 (strong lord)
            if dasha_lord_poi >= 7:
                return 6.0  # Strong dasha lord in own house
            elif dasha_lord_poi >= 5:
                return 5.0  # Medium strength
            else:
                return 4.0  # Even weak lord benefits from being in own house

        return 0

    def _calculate_static_house_strength(self, house: int, target_date: Optional[date] = None) -> float:
        """
        V5.7: Calculate static birth house strength based on planets present.

        V5.7 REFINEMENTS:
        - Include House Lord's POI score (not just dignity)
        - POI gives a more accurate picture of lord's operational strength
        - NEW: House suppression if ruling planet POI < 0.5 (normalized)

        V5.7 HOUSE SUPPRESSION RULE:
        - If house lord's normalized POI < 0.5 (i.e., POI < 5 on 0-10 scale)
        - Apply suppression factor that reduces house strength
        - This reflects weakened house significations when lord is weak

        Args:
            house: House number (1-12)
            target_date: Optional date for POI calculation

        Returns:
            Static house strength (0-8 scale)
        """
        strength = 3.0  # Base strength

        # Add strength from planets in this house
        for planet, data in self.planets.items():
            planet_house = data.get('house', 0)
            if planet_house == house:
                # Get planet's basic strength
                dignity = data.get('dignity', 'neutral')
                dignity_score = self.DIGNITY_TABLE_V3.get(dignity, 5) / 10

                # Benefic/Malefic adjustment
                if planet in self.BENEFIC_PLANETS:
                    strength += 1.5 * dignity_score
                else:
                    strength += 0.8 * dignity_score

        # V5.7: House lord contribution using POI with SUPPRESSION check
        lord = self._get_house_lord(house)
        house_suppression_factor = 1.0  # Default: no suppression

        if lord:
            # Calculate House Lord's POI for more accurate strength
            lord_poi_result = self.calculate_poi(lord, target_date)
            lord_poi = lord_poi_result['poi']  # 0-10 scale
            lord_poi_normalized = lord_poi / 10  # 0-1 scale

            # V5.7 HOUSE SUPPRESSION: If house lord POI < threshold (0.5 normalized = 5 on 0-10 scale)
            suppression_threshold = self.GLOBAL_NUMERIC_SAFETY.get('house_suppression_threshold', 0.5)
            if lord_poi_normalized < suppression_threshold:
                # Apply suppression proportional to how weak the lord is
                # Suppression ranges from 0.5 (lord POI = 0) to 1.0 (lord POI = threshold)
                house_suppression_factor = 0.5 + (lord_poi_normalized / suppression_threshold) * 0.5
                # Log suppression for trace
                self.calculation_trace.append({
                    'action': 'HOUSE_SUPPRESSION_V57',
                    'house': house,
                    'lord': lord,
                    'lord_poi': lord_poi,
                    'suppression_threshold': suppression_threshold,
                    'suppression_factor': round(house_suppression_factor, 3)
                })

            # POI-based contribution (scaled to 0-2 range)
            lord_contribution = (lord_poi / 10) * 2.0
            strength += lord_contribution

        # V5.7: Apply house suppression factor
        strength = strength * house_suppression_factor

        return min(8.0, max(0, strength))  # Cap at 8, floor at 0

    def _calculate_house_transit_overlay(self, house: int, target_date: date) -> float:
        """Calculate transit overlay for house on specific date"""
        overlay = 0

        # Check which planets are transiting this house
        for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']:
            transit_house = self._estimate_transit_house(planet, target_date)

            if transit_house == house:
                # Planet transiting this house
                if planet in self.BENEFIC_PLANETS:
                    overlay += 0.8
                else:
                    overlay -= 0.5

            # Check aspects to this house
            aspect_houses = self._get_planet_aspect_houses(planet, transit_house)
            if house in aspect_houses:
                if planet in self.BENEFIC_PLANETS:
                    overlay += 0.4
                elif planet in ['Saturn', 'Mars']:
                    overlay -= 0.3

        return overlay

    def _get_planet_aspect_houses(self, planet: str, from_house: int) -> List[int]:
        """Get houses aspected by a planet from a given house"""
        aspects = []

        # All planets aspect 7th house from themselves
        aspects.append(((from_house - 1 + 7 - 1) % 12) + 1)

        # Special aspects
        if planet == 'Mars':
            aspects.append(((from_house - 1 + 4 - 1) % 12) + 1)  # 4th aspect
            aspects.append(((from_house - 1 + 8 - 1) % 12) + 1)  # 8th aspect

        if planet == 'Jupiter':
            aspects.append(((from_house - 1 + 5 - 1) % 12) + 1)  # 5th aspect
            aspects.append(((from_house - 1 + 9 - 1) % 12) + 1)  # 9th aspect

        if planet == 'Saturn':
            aspects.append(((from_house - 1 + 3 - 1) % 12) + 1)  # 3rd aspect
            aspects.append(((from_house - 1 + 10 - 1) % 12) + 1)  # 10th aspect

        if planet in ['Rahu', 'Ketu']:
            aspects.append(((from_house - 1 + 5 - 1) % 12) + 1)  # 5th aspect
            aspects.append(((from_house - 1 + 9 - 1) % 12) + 1)  # 9th aspect

        return aspects

    def _calculate_jupiter_yearly_support(self, house: int, target_date: date) -> float:
        """
        Calculate Jupiter's yearly support for a house.
        Jupiter gives support when transiting the house, trines, or aspecting.
        """
        jupiter_house = self._estimate_transit_house('Jupiter', target_date)

        support = 0

        # Direct transit
        if jupiter_house == house:
            support = 2.0  # Strong support

        # Trine houses (5th and 9th from Jupiter's position)
        trine_houses = [
            ((jupiter_house - 1 + 4) % 12) + 1,  # 5th from Jupiter
            ((jupiter_house - 1 + 8) % 12) + 1   # 9th from Jupiter
        ]
        if house in trine_houses:
            support = 1.5

        # Jupiter's aspects (5th, 7th, 9th)
        aspect_houses = self._get_planet_aspect_houses('Jupiter', jupiter_house)
        if house in aspect_houses and support == 0:
            support = 1.0

        return support

    def _calculate_saturn_yearly_pressure(self, house: int, target_date: date) -> float:
        """
        V5.0: Calculate Saturn's yearly pressure on a house.

        V5.0 REFINEMENT:
        - Saturn's 3rd and 10th aspects now add -2 pressure each (stronger than 7th)
        - 3rd aspect: Harsh, aggressive energy toward that house
        - 10th aspect: Authoritative pressure, karmic weight
        - 7th aspect: Standard opposition (kept at -1)

        Saturn creates pressure when transiting or aspecting the house.
        """
        saturn_house = self._estimate_transit_house('Saturn', target_date)

        pressure = 0

        # Direct transit (Kantaka Shani for kendras)
        if saturn_house == house:
            if house in [1, 4, 7, 10]:  # Kendras
                pressure = 2.5  # Strong pressure (increased from 2.0)
            else:
                pressure = 1.5

        # V5.0: Saturn's special aspects with differentiated pressure
        # Saturn aspects: 3rd, 7th, 10th from its position
        if pressure == 0:  # Only calculate aspect if not direct transit
            # Calculate aspect houses
            third_aspect_house = ((saturn_house - 1 + 2) % 12) + 1   # 3rd from Saturn
            seventh_aspect_house = ((saturn_house - 1 + 6) % 12) + 1  # 7th from Saturn
            tenth_aspect_house = ((saturn_house - 1 + 9) % 12) + 1   # 10th from Saturn

            # V5.0: 3rd aspect - harsh, aggressive (-2 pressure)
            if house == third_aspect_house:
                pressure = 2.0  # Strong 3rd aspect pressure

            # V5.0: 10th aspect - authoritative, karmic (-2 pressure)
            elif house == tenth_aspect_house:
                pressure = 2.0  # Strong 10th aspect pressure

            # 7th aspect - standard opposition (-1 pressure)
            elif house == seventh_aspect_house:
                pressure = 1.0  # Standard 7th aspect

        # Sade Sati effect (7.5 years of Saturn)
        moon_house = self.planets.get('Moon', {}).get('house', 1)
        sade_sati_houses = [
            ((moon_house - 1 - 1) % 12) + 1,  # 12th from Moon
            moon_house,                        # Moon's house
            ((moon_house - 1 + 1) % 12) + 1   # 2nd from Moon
        ]
        if saturn_house in sade_sati_houses and house == moon_house:
            pressure += 0.5  # Additional Sade Sati pressure

        return pressure

    def _calculate_dasha_house_activation(self, house: int, target_date: date) -> float:
        """Calculate activation from dasha lord ruling/occupying this house"""
        dasha_info = self.jathagam.get('dasha', {})
        current = dasha_info.get('current', {})
        dasha_lord = current.get('lord', '') if isinstance(current, dict) else ''

        if not dasha_lord:
            return 0

        activation = 0

        # Check if dasha lord rules this house
        lord_of_house = self._get_house_lord(house)
        if dasha_lord == lord_of_house:
            activation += 1.5

        # Check if dasha lord occupies this house
        dasha_lord_data = self.planets.get(dasha_lord, {})
        if dasha_lord_data.get('house') == house:
            activation += 1.0

        return activation

    def _calculate_bhukti_house_activation(self, house: int, target_date: date) -> float:
        """Calculate activation from bhukti lord ruling/occupying this house"""
        dasha_info = self.jathagam.get('dasha', {})
        current = dasha_info.get('current', {})
        bhukti_lord = current.get('antardasha_lord', '') if isinstance(current, dict) else ''

        if not bhukti_lord:
            return 0

        activation = 0

        # Check if bhukti lord rules this house
        lord_of_house = self._get_house_lord(house)
        if bhukti_lord == lord_of_house:
            activation += 1.0

        # Check if bhukti lord occupies this house
        bhukti_lord_data = self.planets.get(bhukti_lord, {})
        if bhukti_lord_data.get('house') == house:
            activation += 0.7

        return activation

    def _get_occupancy_modifier(self, planet: str, house: int) -> float:
        """Get occupancy strength modifier for planet in house"""
        # Planets have natural affinity for certain houses
        affinities = {
            'Sun': [1, 5, 9, 10],
            'Moon': [2, 4, 7],
            'Mars': [3, 6, 10],
            'Mercury': [1, 4, 7, 10],
            'Jupiter': [1, 5, 9, 11],
            'Venus': [2, 4, 7, 12],
            'Saturn': [3, 6, 10, 11],
            'Rahu': [3, 6, 10, 11],
            'Ketu': [3, 6, 9, 12]
        }

        if house in affinities.get(planet, []):
            return 1.2
        elif house in [6, 8, 12]:  # Dusthana
            return 0.7
        return 1.0

    def _get_transit_overlay(self, house: int, target_date: date) -> float:
        """Calculate transit overlay for a house"""
        # Check if major planets are transiting this house
        overlay = 1.0

        # Jupiter transit boost
        jupiter_house = self._estimate_transit_house('Jupiter', target_date)
        if jupiter_house == house:
            overlay += 0.3

        # Saturn transit (can be challenging)
        saturn_house = self._estimate_transit_house('Saturn', target_date)
        if saturn_house == house:
            if house in [1, 4, 7, 10]:  # Kendra
                overlay -= 0.15  # Kantaka Shani
            else:
                overlay -= 0.1

        return max(0.5, overlay)

    def _estimate_transit_house(self, planet: str, target_date: date) -> int:
        """Estimate which house a planet is transiting on a given date"""
        birth_date = self._get_birth_date()
        days_elapsed = (target_date - birth_date).days

        natal_data = self.planets.get(planet, {})
        natal_longitude = natal_data.get('longitude', 0)

        speed = self.PLANET_SPEEDS.get(planet, 0.5)
        current_longitude = (natal_longitude + (speed * days_elapsed)) % 360

        # Convert to house (30 degrees per house from Moon)
        moon_long = self.planets.get('Moon', {}).get('longitude', 0)
        diff = (current_longitude - moon_long) % 360
        house = int(diff / 30) + 1

        return house

    def _get_house_lord(self, house: int) -> str:
        """Get the lord of a house based on lagna"""
        # Map lagna to rasi number
        lagna_rasi = self.lagna
        rasi_order = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                      'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

        try:
            lagna_num = rasi_order.index(lagna_rasi)
        except:
            lagna_num = 0

        # Calculate house rasi
        house_rasi_num = (lagna_num + house - 1) % 12
        house_rasi = rasi_order[house_rasi_num]

        # Get lord
        return self.HOUSE_LORDS.get(house_rasi_num + 1, 'Sun')

    # ==================== NAVAMSA SUPPORT CALCULATION ====================

    def calculate_navamsa_support(self, planet: str) -> Dict:
        """
        Calculate Navamsa (D9) support for a planet.

        NavamsaSupport = Δ(dignity_D9 - dignity_D1) + compatibility_bonuses

        Args:
            planet: Planet name

        Returns:
            Dict with navamsa support value and breakdown
        """
        planet_data = self.planets.get(planet, {})

        # D1 (natal) dignity
        d1_dignity = planet_data.get('dignity', 'neutral')
        d1_score = self.DIGNITY_TABLE_V3.get(d1_dignity, 5)

        # D9 (navamsa) dignity - from navamsa data if available
        navamsa_data = self.jathagam.get('navamsa', {}).get('planets', {})
        d9_planet = navamsa_data.get(planet, {})
        d9_dignity = d9_planet.get('dignity', d1_dignity)
        d9_score = self.DIGNITY_TABLE_V3.get(d9_dignity, 5)

        # Calculate delta
        dignity_delta = d9_score - d1_score

        # Compatibility bonuses
        compatibility_bonus = 0

        # Check if D9 placement supports D1
        d9_rasi = d9_planet.get('rasi', '')
        d1_rasi = planet_data.get('rasi', '')

        # Same sign = strong support
        if d9_rasi == d1_rasi:
            compatibility_bonus += 2

        # Check for vargottama (same sign in D1 and D9)
        if planet_data.get('vargottama', False):
            compatibility_bonus += 3

        # Apply mode-specific navamsa amplification
        navamsa_amp = self.active_multipliers.get('navamsa_amplification', 1.0)

        total_support = (dignity_delta + compatibility_bonus) * navamsa_amp

        return {
            'planet': planet,
            'navamsa_support': round(total_support, 3),
            'breakdown': {
                'd1_dignity': d1_dignity,
                'd1_score': d1_score,
                'd9_dignity': d9_dignity,
                'd9_score': d9_score,
                'dignity_delta': dignity_delta,
                'compatibility_bonus': compatibility_bonus,
                'navamsa_amplification': navamsa_amp
            },
            'formula': f"Support = ({d9_score} - {d1_score} + {compatibility_bonus}) × {navamsa_amp}"
        }

    # ==================== MODULE CALCULATIONS WITH TIME ADAPTATION ====================

    def calculate_dasha_module_v41(
        self,
        mahadasha_lord: str,
        bhukti_lord: str = None,
        antara_lord: str = None,
        target_date: Optional[date] = None
    ) -> Dict:
        """
        V5.8 Dasha-Bhukti-Antara module calculation.

        V5.8 CRITICAL FIX:
        - Use DASHA_BASELINE_POWER independent of POI
        - POI only acts as modifier (±0.10 cap)
        - Prevents Dasha from collapsing to punitive scores

        FORMULA:
        baseline_dasha =
            0.50 * BASELINE(dasha_lord)  # V5.8: Fixed baseline
          + 0.30 * BASELINE(bhukti_lord)
          + 0.20 * BASELINE(antara_lord)

        poi_modifier =
            (POI(dasha_lord) - 5.0) * 0.02  # Centered at 5, capped ±0.10

        final_dasha_base = baseline_dasha + poi_modifier

        V5.8 Target Range: 0.18 – 0.32 after weighting (0.35 weight)
        """
        # V5.8: Get baseline power for each dasha lord
        mahadasha_baseline = self._get_dasha_baseline_power(mahadasha_lord)
        bhukti_baseline = self._get_dasha_baseline_power(bhukti_lord) if bhukti_lord else mahadasha_baseline * 0.9
        antara_baseline = self._get_dasha_baseline_power(antara_lord) if antara_lord else bhukti_baseline * 0.9

        # V5.8: Baseline dasha (stable foundation)
        baseline_dasha = (0.50 * mahadasha_baseline + 0.30 * bhukti_baseline + 0.20 * antara_baseline)

        # V5.8: POI as modifier only (centered at 5, capped at ±0.10)
        mahadasha_poi = self.calculate_poi(mahadasha_lord, target_date)['poi']
        bhukti_poi = self.calculate_poi(bhukti_lord, target_date)['poi'] if bhukti_lord else 5.0
        antara_poi = self.calculate_poi(antara_lord, target_date)['poi'] if antara_lord else 5.0

        # POI modifier: deviation from neutral (5.0), scaled and capped
        avg_poi = (0.50 * mahadasha_poi + 0.30 * bhukti_poi + 0.20 * antara_poi)
        poi_modifier = (avg_poi - 5.0) * 0.02  # Each point deviation = 0.02
        poi_modifier = max(-0.10, min(0.10, poi_modifier))  # Cap at ±0.10

        # V5.8: Raw dasha uses baseline + capped POI modifier
        raw_dasha = (baseline_dasha + poi_modifier) * 10  # Scale to 0-10 range for compatibility

        # HOUSE ALIGNMENT BONUS (using houses RULED by dasha lords)
        mahadasha_ruled_houses = self._get_houses_ruled_by(mahadasha_lord)
        bhukti_ruled_houses = self._get_houses_ruled_by(bhukti_lord) if bhukti_lord else []

        mahadasha_hai_avg = 0
        if mahadasha_ruled_houses:
            mahadasha_hai_avg = sum(
                self.calculate_hai(h, target_date)['hai'] for h in mahadasha_ruled_houses
            ) / len(mahadasha_ruled_houses)

        bhukti_hai_avg = 0
        if bhukti_ruled_houses:
            bhukti_hai_avg = sum(
                self.calculate_hai(h, target_date)['hai'] for h in bhukti_ruled_houses
            ) / len(bhukti_ruled_houses)

        house_alignment_bonus = (mahadasha_hai_avg * 0.4) + (bhukti_hai_avg * 0.3)

        # V5.0 NEW: JUPITER/SATURN TRANSIT EFFECTS ON RULED HOUSES
        ruled_house_transit_effect = 0
        if target_date and mahadasha_ruled_houses:
            ruled_house_transit_effect = self._calculate_ruled_house_transit_effects(
                mahadasha_ruled_houses, target_date
            )

        # DASHA SYNERGY (transit effects on dasha lords)
        dasha_transit_effect = self._calculate_dasha_transit_effect(mahadasha_lord, target_date)
        bhukti_transit_effect = self._calculate_dasha_transit_effect(bhukti_lord, target_date) if bhukti_lord else 0
        antara_activation = self._calculate_antara_activation(antara_lord, target_date) if antara_lord else 0

        dasha_synergy = dasha_transit_effect + bhukti_transit_effect + antara_activation

        # NAVAMSA MODIFIER (date-specific)
        navamsa_support = self._calculate_dasha_navamsa_support(mahadasha_lord, target_date)
        navamsa_mod = 1 + (navamsa_support * 0.015)

        # V5.7 FINAL DASHA CALCULATION (malefic penalty applied AFTER normalization)
        raw_score = (raw_dasha + house_alignment_bonus + ruled_house_transit_effect + dasha_synergy) * navamsa_mod

        # Normalize to 0-1
        min_range, max_range = self.TENSOR_MODELS['dasha_bhukti']['expected_range']
        normalized = (raw_score - min_range) / (max_range - min_range)
        normalized = max(0, min(1, normalized))

        # V6.0 MALEFIC PENALTY: Nearly eliminated (80% reduction)
        # V6.0 Core: Strongly positive - malefics have minimal impact
        malefic_penalty_normalized = 0
        transit_malefic_pressure = self._calculate_malefic_pressure(target_date)
        penalty_reduction = self.GLOBAL_NUMERIC_SAFETY.get('malefic_penalty_reduction', 0.80)
        if mahadasha_lord in self.MALEFIC_PLANETS and transit_malefic_pressure > 80:  # V6.0: High threshold
            # V6.0: Minimal penalty range -0.02 to -0.03 (80% reduction)
            pressure_intensity = min(1.0, (transit_malefic_pressure - 80) / 20)  # 0 to 1 scale
            base_penalty = -0.10 - (pressure_intensity * 0.05)  # Original penalty
            malefic_penalty_normalized = base_penalty * (1 - penalty_reduction)  # Apply 80% reduction
            normalized = max(0.5, normalized + malefic_penalty_normalized)  # V6.0: Never below 50%

        # V6.0: Apply global numeric safety clamp (floor 0.50, ceiling 0.88)
        clamp_min = self.GLOBAL_NUMERIC_SAFETY.get('clamp_min', 0.50)
        clamp_max = self.GLOBAL_NUMERIC_SAFETY.get('clamp_max', 0.88)
        normalized = max(clamp_min, min(clamp_max, normalized))

        return {
            'module': 'dasha_bhukti',
            'raw_score': round(raw_score, 3),
            'normalized': round(normalized, 4),
            'weight': self.active_weights.get('dasha_bhukti', 0.25),
            'weighted_contribution': round(normalized * self.active_weights.get('dasha_bhukti', 0.25), 4),
            'tensor_breakdown': {
                'raw_dasha': round(raw_dasha, 3),
                'house_alignment_bonus': round(house_alignment_bonus, 3),
                'ruled_house_transit_effect': round(ruled_house_transit_effect, 3),
                'dasha_synergy': round(dasha_synergy, 3),
                'malefic_penalty_normalized': round(malefic_penalty_normalized, 3),  # V5.7: Post-normalization penalty
                'navamsa_mod': round(navamsa_mod, 4)
            },
            'inputs': {
                'mahadasha_lord': mahadasha_lord,
                'mahadasha_poi': mahadasha_poi,
                'bhukti_lord': bhukti_lord,
                'bhukti_poi': bhukti_poi,
                'antara_lord': antara_lord,
                'antara_poi': antara_poi,
                'mahadasha_ruled_houses': mahadasha_ruled_houses,
                'transit_malefic_pressure': transit_malefic_pressure,
                'dasha_transit_effect': round(dasha_transit_effect, 3),
                'bhukti_transit_effect': round(bhukti_transit_effect, 3),
                'antara_activation': round(antara_activation, 3)
            },
            'formula': 'V5.7: final = normalize(raw_dasha + house_alignment + ruled_house_transit + dasha_synergy) × navamsa_mod + malefic_penalty_post_norm'
        }

    def _calculate_ruled_house_transit_effects(self, ruled_houses: List[int], target_date: date) -> float:
        """
        V5.7: Calculate Jupiter/Saturn transit effects on houses RULED BY Dasha Lord.

        V5.7 CRITICAL FIX:
        - Jupiter/Saturn must affect the HOUSES ruled by dasha lord, not just any house
        - This is the key principle: transits affect dasha significations through house rulership
        - Effect strength based on aspect type (direct > special aspects > trine)

        When Jupiter transits a house ruled by the current Dasha Lord, it brings
        expansion and opportunities to that house's significations.

        When Saturn transits a house ruled by the current Dasha Lord, it brings
        delays and challenges to that house's significations.

        Args:
            ruled_houses: List of houses ruled by the dasha lord
            target_date: Date for transit calculation

        Returns:
            Combined transit effect (-3 to +3 range)
        """
        if not ruled_houses or not target_date:
            return 0

        jupiter_house = self._estimate_transit_house('Jupiter', target_date)
        saturn_house = self._estimate_transit_house('Saturn', target_date)

        effect = 0
        effect_details = []  # V5.7: Track details for debugging

        for house in ruled_houses:
            house_effect = 0

            # === JUPITER EFFECTS (V5.7: Enhanced) ===
            # Jupiter transiting ruled house = POSITIVE (+2.0 per house, increased from 1.5)
            if jupiter_house == house:
                house_effect += 2.0
                effect_details.append(f"Jupiter direct transit H{house}: +2.0")

            # Jupiter aspecting ruled house (5th, 7th, 9th aspects)
            jupiter_5th = ((jupiter_house - 1 + 4) % 12) + 1   # 5th aspect
            jupiter_7th = ((jupiter_house - 1 + 6) % 12) + 1   # 7th aspect
            jupiter_9th = ((jupiter_house - 1 + 8) % 12) + 1   # 9th aspect

            if house == jupiter_5th:
                house_effect += 1.0  # V5.7: 5th aspect (trikona) = +1.0
            elif house == jupiter_9th:
                house_effect += 1.0  # V5.7: 9th aspect (trikona) = +1.0
            elif house == jupiter_7th:
                house_effect += 0.7  # V5.7: 7th aspect (standard) = +0.7

            # === SATURN EFFECTS (V5.7: 3rd and 10th aspects are STRONGER) ===
            # Saturn transiting ruled house = NEGATIVE (-2.0 per house, increased from 1.5)
            if saturn_house == house:
                house_effect -= 2.0
                effect_details.append(f"Saturn direct transit H{house}: -2.0")

            # Saturn's special aspects (V5.7: 3rd and 10th are HARSH)
            saturn_3rd = ((saturn_house - 1 + 2) % 12) + 1   # 3rd aspect
            saturn_7th = ((saturn_house - 1 + 6) % 12) + 1   # 7th aspect
            saturn_10th = ((saturn_house - 1 + 9) % 12) + 1  # 10th aspect

            if house == saturn_3rd:
                house_effect -= 1.5  # V5.7: 3rd aspect = HARSH (increased from 1.0)
                effect_details.append(f"Saturn 3rd aspect H{house}: -1.5")
            elif house == saturn_10th:
                house_effect -= 1.5  # V5.7: 10th aspect = KARMIC WEIGHT (increased from 1.0)
                effect_details.append(f"Saturn 10th aspect H{house}: -1.5")
            elif house == saturn_7th:
                house_effect -= 0.8  # V5.7: 7th aspect = standard opposition

            effect += house_effect

        # V5.7: Store trace for debugging
        self.calculation_trace.append({
            'action': 'RULED_HOUSE_TRANSIT_V57',
            'ruled_houses': ruled_houses,
            'jupiter_house': jupiter_house,
            'saturn_house': saturn_house,
            'effect_details': effect_details,
            'total_effect': effect
        })

        # Cap effect to reasonable range
        return max(-3.0, min(3.0, effect))

    def _get_houses_ruled_by(self, planet: str) -> List[int]:
        """Get list of houses ruled by a planet based on lagna"""
        if not planet:
            return []

        ruled_houses = []
        lagna_rasi = self.lagna
        rasi_order = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                      'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

        try:
            lagna_num = rasi_order.index(lagna_rasi)
        except ValueError:
            lagna_num = 0

        # Rulership mapping
        planet_rules = {
            'Sun': [5],     # Leo = 5th sign
            'Moon': [4],    # Cancer = 4th sign
            'Mars': [1, 8], # Aries = 1st, Scorpio = 8th
            'Mercury': [3, 6],  # Gemini = 3rd, Virgo = 6th
            'Jupiter': [9, 12],  # Sagittarius = 9th, Pisces = 12th
            'Venus': [2, 7],  # Taurus = 2nd, Libra = 7th
            'Saturn': [10, 11],  # Capricorn = 10th, Aquarius = 11th
            'Rahu': [11],   # Modern: Aquarius
            'Ketu': [8]     # Modern: Scorpio
        }

        signs = planet_rules.get(planet, [])
        for sign_num in signs:
            # Convert sign number to house number based on lagna
            house = ((sign_num - 1 - lagna_num) % 12) + 1
            ruled_houses.append(house)

        return ruled_houses

    def _get_dasha_baseline_power(self, planet: str) -> float:
        """
        V5.8: Get baseline dasha power for a planet.

        This provides a stable foundation independent of POI.
        Prevents Dasha score from collapsing due to low POI.

        Returns:
            Baseline power: 0.45 (malefic), 0.55 (neutral), 0.65 (benefic)
        """
        if not planet:
            return self.DASHA_BASELINE_POWER.get('neutral', 0.55)

        # Classify planet
        benefics = ['Jupiter', 'Venus']
        malefics = ['Saturn', 'Mars', 'Rahu', 'Ketu']

        # Moon is benefic when waxing, malefic when waning
        if planet == 'Moon':
            # Check if we have paksha info
            paksha = self.jathagam.get('panchagam', {}).get('paksha', '')
            if paksha.lower() == 'shukla' or paksha.lower() == 'bright':
                return self.DASHA_BASELINE_POWER.get('benefic', 0.65)
            else:
                return self.DASHA_BASELINE_POWER.get('neutral', 0.55)

        # Mercury is benefic when with benefics, malefic otherwise
        if planet == 'Mercury':
            mercury_data = self.planets.get('Mercury', {})
            mercury_house = mercury_data.get('house', 0)
            # Check if Mercury is with benefics
            for benefic in benefics:
                if self.planets.get(benefic, {}).get('house', -1) == mercury_house:
                    return self.DASHA_BASELINE_POWER.get('benefic', 0.65)
            return self.DASHA_BASELINE_POWER.get('neutral', 0.55)

        if planet in benefics:
            return self.DASHA_BASELINE_POWER.get('benefic', 0.65)
        elif planet in malefics:
            return self.DASHA_BASELINE_POWER.get('malefic', 0.45)
        else:
            return self.DASHA_BASELINE_POWER.get('neutral', 0.55)

    def _calculate_dasha_transit_effect(self, planet: str, target_date: Optional[date]) -> float:
        """Calculate transit effect on dasha lord"""
        if not planet or not target_date:
            return 0

        effect = 0

        # Get dasha lord's natal position
        natal_data = self.planets.get(planet, {})
        natal_long = natal_data.get('longitude', 0)

        # Check Jupiter transit support
        jupiter_long = self._get_transit_longitude('Jupiter', target_date)
        jup_diff = abs(jupiter_long - natal_long) % 360
        if jup_diff > 180:
            jup_diff = 360 - jup_diff

        if jup_diff < 10:  # Jupiter conjunct dasha lord
            effect += 1.5
        elif abs(jup_diff - 120) < 10:  # Jupiter trine
            effect += 1.0

        # Check Saturn transit pressure
        saturn_long = self._get_transit_longitude('Saturn', target_date)
        sat_diff = abs(saturn_long - natal_long) % 360
        if sat_diff > 180:
            sat_diff = 360 - sat_diff

        if sat_diff < 10:  # Saturn conjunct dasha lord
            effect -= 1.0
        elif abs(sat_diff - 90) < 10:  # Saturn square
            effect -= 0.5

        return effect

    def _calculate_antara_activation(self, antara_lord: str, target_date: Optional[date]) -> float:
        """Calculate antara lord activation bonus"""
        if not antara_lord or not target_date:
            return 0

        bonus = 0

        # Check if antara lord is receiving beneficial transits
        antara_poi = self.calculate_poi(antara_lord, target_date)
        if antara_poi['poi'] > 6:
            bonus += 0.5

        # Check if antara lord is transiting favorable houses
        antara_transit_house = self._estimate_transit_house(antara_lord, target_date)
        if antara_transit_house in [1, 5, 9, 10, 11]:  # Favorable houses
            bonus += 0.3

        return bonus

    def _calculate_dasha_navamsa_support(self, planet: str, target_date: Optional[date]) -> float:
        """Calculate navamsa support for dasha lord with date-specific overlays"""
        base_support = self.calculate_navamsa_support(planet)['navamsa_support']

        # Add date-specific transit support to D9 position
        if target_date:
            transit_d9_support = self._calculate_transit_d9_support(planet, target_date)
            base_support += transit_d9_support * 0.3

        return base_support

    def _calculate_malefic_pressure(self, target_date: Optional[date] = None) -> float:
        """Calculate total malefic transit pressure (0-100)"""
        pressure = 50  # Base

        if target_date:
            for planet in self.MALEFIC_PLANETS:
                poi = self.calculate_poi(planet, target_date)['poi']
                if poi > 6:  # Strong malefic
                    pressure += (poi - 6) * 5

        return min(100, pressure)

    def calculate_transit_module_v41(
        self,
        target_date: date,
        life_area: str = 'general'
    ) -> Dict:
        """
        v4.1 Transit module with time-adaptive calculation.

        pressure = 100 - transit_intensity
        benefic_tensor = benefic_intensity × 1.4
        malefic_tensor = malefic_intensity × -1.8
        emotional_tensor = moon_phase × nakshatra.emotional_factor
        hora_mod = 1 + (planetary_hour_POI × 0.01)
        final = (pressure + benefic + emotional + malefic) × hora_mod
        """
        # Calculate benefic intensity
        benefic_intensity = 0
        for planet in self.BENEFIC_PLANETS:
            poi = self.calculate_poi(planet, target_date)['poi']
            benefic_intensity += poi
        benefic_intensity /= len(self.BENEFIC_PLANETS)

        # Calculate malefic intensity
        malefic_intensity = 0
        for planet in self.MALEFIC_PLANETS:
            poi = self.calculate_poi(planet, target_date)['poi']
            malefic_intensity += poi
        malefic_intensity /= len(self.MALEFIC_PLANETS)

        # Transit intensity (overall activity)
        all_pois = [self.calculate_poi(p, target_date)['poi'] for p in self.planets.keys()]
        transit_intensity = sum(all_pois) / len(all_pois) if all_pois else 5

        # Tensors
        pressure = (10 - transit_intensity) * 3  # Scale to ~0-30
        benefic_tensor = benefic_intensity * 1.4
        malefic_tensor = malefic_intensity * -1.8

        # Emotional tensor (simplified moon phase)
        moon_data = self.planets.get('Moon', {})
        moon_longitude = moon_data.get('longitude', 0)
        birth_date = self._get_birth_date()
        days_elapsed = (target_date - birth_date).days
        moon_phase = abs(math.sin(days_elapsed * 0.21))  # ~29.5 day cycle

        nakshatra = moon_data.get('nakshatra', '')
        nakshatra_traits = self.NAKSHATRA_TRAITS.get(nakshatra, {})
        emotional_factor = nakshatra_traits.get('base_multiplier', 1.0)
        emotional_tensor = moon_phase * emotional_factor * 2

        # Hora modifier (planetary hour - simplified)
        hour_of_day = (target_date.toordinal() % 7) * 24 + 12  # Approximation
        hora_planet = ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon'][hour_of_day % 7]
        hora_poi = self.calculate_poi(hora_planet, target_date)['poi']
        hora_mod = 1 + (hora_poi * 0.01)

        # Final calculation
        raw_score = (pressure + benefic_tensor + emotional_tensor + malefic_tensor) * hora_mod

        # Normalize
        min_range, max_range = self.TENSOR_MODELS['transit']['expected_range']
        normalized = (raw_score - min_range) / (max_range - min_range)
        normalized = max(0, min(1, normalized))

        # Apply time mode transit window adjustment
        transit_window = self.TIME_MODE_MODIFIERS[self.current_time_mode]['transit_window_days']
        if self.current_time_mode == TimeMode.FUTURE_PREDICTION:
            # Apply future boost
            months_ahead = max(0, (target_date - date.today()).days / 30)
            future_boost = self.active_multipliers.get('future_window_boost', 0.003)
            normalized *= (1 + months_ahead * future_boost)
            normalized = min(1, normalized)

        # V5.8: Apply transit cap to prevent excessive scores
        transit_cap = self.GLOBAL_NUMERIC_SAFETY.get('transit_cap', 0.70)
        normalized = min(transit_cap, normalized)

        # V5.8: Apply module floor
        clamp_min = self.GLOBAL_NUMERIC_SAFETY.get('clamp_min', 0.30)
        normalized = max(clamp_min, normalized)

        return {
            'module': 'transit',
            'raw_score': round(raw_score, 3),
            'normalized': round(normalized, 4),
            'weight': self.active_weights.get('transit', 0.20),
            'weighted_contribution': round(normalized * self.active_weights.get('transit', 0.20), 4),
            'tensor_breakdown': {
                'pressure': round(pressure, 3),
                'benefic_tensor': round(benefic_tensor, 3),
                'malefic_tensor': round(malefic_tensor, 3),
                'emotional_tensor': round(emotional_tensor, 3),
                'hora_mod': round(hora_mod, 4)
            },
            'inputs': {
                'transit_intensity': round(transit_intensity, 3),
                'benefic_intensity': round(benefic_intensity, 3),
                'malefic_intensity': round(malefic_intensity, 3),
                'moon_phase': round(moon_phase, 3),
                'nakshatra': nakshatra,
                'hora_planet': hora_planet,
                'transit_window_days': transit_window
            },
            'time_mode': self.current_time_mode.value,
            'formula': self.TENSOR_MODELS['transit']['formula']
        }

    # ==================== V5.0 PREDICTION SCORE OVERRIDE ====================

    def calculate_prediction_score(
        self,
        target_date: date,
        life_area: str = 'general',
        dasha_lord: str = None,
        bhukti_lord: str = None,
    ) -> Dict:
        """
        V5.0 Override: This method overrides the base class to use V5.0 modules.

        The base AstroPercentEngine.calculate_prediction_score() uses old V2.2 logic.
        This override ensures that TimeAdaptiveEngine uses the new V5.0 modules:
        - Shadbala-based POI
        - HAI with House Lord POI and Saturn 3rd/10th aspects
        - Dasha with ruled-house transit effects
        - Yoga with strict dasha/bhukti activation
        - V5.0 Astrologically Weighted Average

        Returns:
            Dict compatible with base class format but using V5.0 calculations
        """
        # Call the V5.0 prediction method
        v5_result = self.calculate_prediction_v41(
            target_date=target_date,
            life_area=life_area,
            dasha_lord=dasha_lord,
            bhukti_lord=bhukti_lord
        )

        # Convert V5.0 result to base class format for backward compatibility
        # Get quality label based on score
        score = v5_result.get('final_score', 50)
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

        # Build top factors from positive/negative drivers
        top_factors = []
        for driver in v5_result.get('top_positive_drivers', [])[:3]:
            top_factors.append({
                'name': driver.get('module', ''),
                'value': int(driver.get('contribution', 0) * 100),
                'positive': True,
                'detail': driver.get('factor', '')
            })
        for driver in v5_result.get('top_negative_drivers', [])[:2]:
            top_factors.append({
                'name': driver.get('module', ''),
                'value': int(abs(driver.get('contribution', 0)) * 100),
                'positive': False,
                'detail': driver.get('factor', '')
            })

        # Build breakdown in base class format (must include 'score' key for compatibility)
        # V5.0 weight percentages for score calculation
        weight_percentages = {
            'dasha': 35, 'transit': 25, 'yoga': 20, 'planet_strength': 10, 'house': 10, 'navamsa': 0
        }
        breakdown = {}
        for module_name, module_data in v5_result.get('module_details', {}).items():
            # Map V5.0 module names to base class names
            base_name = module_name
            if module_name == 'dasha_bhukti':
                base_name = 'dasha'
            elif module_name == 'yoga_dosha':
                base_name = 'yoga'
            elif module_name == 'planet_power':
                base_name = 'planet_strength'
            elif module_name == 'house_power':
                base_name = 'house'

            normalized = module_data.get('normalized', 0)
            weight_pct = weight_percentages.get(base_name, 10)

            # Convert tensor_breakdown dict to factors list format expected by future_projection_service
            # The service expects: [{'name': 'factor_name', 'value': X, ...}, ...]
            tensor_breakdown = module_data.get('tensor_breakdown', {})
            factors_list = []
            for factor_key, factor_value in tensor_breakdown.items():
                if isinstance(factor_value, (int, float)):
                    factors_list.append({
                        'name': factor_key,
                        'value': round(factor_value, 2) if isinstance(factor_value, float) else factor_value,
                        'positive': factor_value >= 0
                    })

            breakdown[base_name] = {
                'score': round(normalized * weight_pct, 1),  # CRITICAL: 'score' key expected by future_projection_service
                'raw': module_data.get('raw_score', 0),
                'normalized': round(normalized, 4),
                'weight': f"{weight_pct}%",
                'contribution': module_data.get('weighted_contribution', 0),
                'factors': factors_list  # List format for compatibility
            }

        # Ensure all expected keys exist (for backward compatibility)
        for key in ['dasha', 'house', 'planet_strength', 'transit', 'yoga', 'navamsa']:
            if key not in breakdown:
                breakdown[key] = {'score': 0, 'raw': 0, 'normalized': 0, 'weight': '0%', 'factors': []}

        return {
            'score': round(score, 1),
            'quality': quality,
            'confidence': v5_result.get('confidence', {}).get('overall', 'medium'),
            'top_factors': top_factors,
            'breakdown': breakdown,
            'engine_version': self.ENGINE_VERSION,
            'time_mode': v5_result.get('time_mode', {}).get('activated', 'present'),
            'calculation_trace': v5_result.get('reasoning_trace', {}),
            'dasha_info': v5_result.get('dasha_info', {})
        }

    # ==================== MAIN v4.1 PREDICTION METHOD ====================

    def calculate_prediction_v41(
        self,
        target_date: date,
        life_area: str = 'general',
        mode_hint: str = None,
        dasha_lord: str = None,
        bhukti_lord: str = None,
        antara_lord: str = None
    ) -> Dict:
        """
        v4.1 Main prediction method with full time adaptation and explainability.

        Returns comprehensive prediction with:
        - Time mode activated and modifications applied
        - All module scores with tensor breakdowns
        - POI and HAI values used
        - Final percentage and confidence
        - Mathematical reasoning trace
        """
        # Reset calculation trace
        self.calculation_trace = []

        # 1. Detect and set time mode
        detected_mode = self.detect_time_mode(target_date, mode_hint=mode_hint)
        mode_info = self.set_time_mode(detected_mode)

        # 2. Get dasha lords from jathagam if not provided
        if not dasha_lord:
            dasha_info = self.jathagam.get('dasha', {})
            current = dasha_info.get('current', {})
            if isinstance(current, dict):
                dasha_lord = current.get('lord', 'Jupiter')
            else:
                dasha_lord = dasha_info.get('mahadasha', 'Jupiter')
            if not bhukti_lord:
                if isinstance(current, dict):
                    bhukti_lord = current.get('antardasha_lord', 'Saturn')
                else:
                    bhukti_lord = dasha_info.get('antardasha', 'Saturn')
                # If still dict, extract the lord name
                if isinstance(bhukti_lord, dict):
                    bhukti_lord = bhukti_lord.get('lord', 'Saturn')

        # 3. Calculate all modules
        modules = {}

        # Dasha-Bhukti module
        dasha_result = self.calculate_dasha_module_v41(
            dasha_lord, bhukti_lord, antara_lord, target_date
        )
        modules['dasha_bhukti'] = dasha_result

        # House Power module (using existing method with HAI)
        house_result = self._calculate_house_power_v41(life_area, target_date)
        modules['house_power'] = house_result

        # Planet Power module
        planet_result = self._calculate_planet_power_v41(life_area, target_date)
        modules['planet_power'] = planet_result

        # Transit module
        transit_result = self.calculate_transit_module_v41(target_date, life_area)
        modules['transit'] = transit_result

        # Yoga-Dosha module
        yoga_result = self._calculate_yoga_dosha_v41(target_date)
        modules['yoga_dosha'] = yoga_result

        # Navamsa module
        navamsa_result = self._calculate_navamsa_module_v41(life_area, target_date)
        modules['navamsa'] = navamsa_result

        # 4. Calculate weighted sum
        weighted_sum = sum(m['weighted_contribution'] for m in modules.values())

        # 5. Calculate meta multiplier
        meta_multiplier = self._calculate_meta_multiplier_v41(modules, target_date)

        # 6. Calculate final score (base calculation)
        final_score = weighted_sum * meta_multiplier * 100
        final_score = max(0, min(100, final_score))

        # Apply non-linear smoothing
        if self.NON_LINEAR_CONFIG.get('apply_smoothing', True):
            power = self.NON_LINEAR_CONFIG.get('final_smoothing_power', 0.92)
            final_score = math.pow(final_score / 100, power) * 100

        # ==================== V7.0 DUAL-TRACK SCORING ====================
        # V7.0: Calculate pressure and outcome separately
        pressure_result = self._calculate_pressure_score_v70(modules, target_date, dasha_lord)
        outcome_result = self._calculate_outcome_score_v70(modules, target_date, dasha_lord)

        # V7.0: Blend old score with new outcome score
        # outcome_score is more optimistic, so we use it to lift the final score
        # Formula: final = (old_score × 0.6) + (outcome_score × 0.4)
        v70_blended_score = (final_score * 0.6) + (outcome_result['outcome_score'] * 0.4)

        # V7.0: Apply dignity floor (minimum 45%)
        v70_blended_score = self._apply_dignity_floor_v70(v70_blended_score)

        # V7.0: Apply positive compound multiplier to final score
        if outcome_result['compound_multiplier'] > 1.0:
            # Boost the score above 50 by compound multiplier
            if v70_blended_score > 50:
                boost = (v70_blended_score - 50) * (outcome_result['compound_multiplier'] - 1)
                v70_blended_score = min(92, v70_blended_score + boost)

        # V7.0: Get phase label based on pressure and outcome
        phase_info = self._get_phase_label_v70(
            pressure_result['pressure_score'],
            outcome_result['outcome_score'],
            'en'  # Default to English, can be made configurable
        )

        # V7.0: Get balanced factors (2 positives + 1 challenge)
        balanced_factors = self._get_balanced_factors_v70(pressure_result, outcome_result)

        # Use V7.0 blended score as final
        final_score = round(v70_blended_score, 1)

        # 7. Calculate confidence
        confidence = self._calculate_confidence_v41(modules, target_date)

        # 8. Identify top drivers (V7.0: prefer balanced factors)
        positive_drivers = self._get_top_drivers(modules, positive=True)
        negative_drivers = self._get_top_drivers(modules, positive=False)

        # 9. Build complete result
        result = {
            'engine_version': self.ENGINE_VERSION,
            'engine_type': self.ENGINE_TYPE,
            'target_date': target_date.isoformat(),
            'life_area': life_area,

            # Time mode information
            'time_mode': {
                'activated': detected_mode.value,
                'description': mode_info['description'],
                'weights_modified': mode_info['weights_applied'],
                'multipliers_modified': mode_info['multipliers_applied'],
                'transit_window_days': mode_info['transit_window_days']
            },

            # Module scores
            'module_raw_scores': {k: v['raw_score'] for k, v in modules.items()},
            'module_normalized_scores': {k: v['normalized'] for k, v in modules.items()},
            'module_details': modules,

            # Final calculations
            'weighted_sum': round(weighted_sum, 4),
            'meta_multiplier': round(meta_multiplier, 4),
            'final_score': final_score,

            # V7.0: Dual-track scoring results
            'v70_scoring': {
                'pressure': pressure_result,
                'outcome': outcome_result,
                'phase': phase_info,
                'balanced_factors': balanced_factors,
                'dignity_floor_applied': self.GLOBAL_NUMERIC_SAFETY.get('dignity_floor', 45),
                'compound_multiplier': outcome_result['compound_multiplier']
            },

            # Confidence and interpretation
            'confidence': confidence,

            # Drivers (V7.0: includes balanced factors)
            'top_positive_drivers': positive_drivers,
            'top_negative_drivers': negative_drivers,

            # Reasoning trace
            'reasoning_trace': {
                'formula': 'V7.0: final = (base_score × 0.6 + outcome_score × 0.4) with dignity floor',
                'calculation': f"({weighted_sum * meta_multiplier * 100:.1f} × 0.6) + ({outcome_result['outcome_score']:.1f} × 0.4) = {final_score:.1f}",
                'smoothing_applied': self.NON_LINEAR_CONFIG.get('apply_smoothing', True),
                'smoothing_power': self.NON_LINEAR_CONFIG.get('final_smoothing_power', 0.92),
                'v70_enhancements': [
                    'Pressure-Outcome dual-track scoring',
                    'Time decay on malefic factors',
                    'Dampeners instead of penalties',
                    f'Dignity floor: {self.GLOBAL_NUMERIC_SAFETY.get("dignity_floor", 45)}%',
                    f'Positive compound: {outcome_result["compound_multiplier"]}x',
                    f'Max negativity cap: {self.GLOBAL_NUMERIC_SAFETY.get("max_negativity_per_period", 30)}'
                ]
            },

            # Calculation trace log
            'calculation_trace': self.calculation_trace,

            # Dasha information
            'dasha_info': {
                'mahadasha_lord': dasha_lord,
                'bhukti_lord': bhukti_lord,
                'antara_lord': antara_lord
            }
        }

        return result

    def _calculate_house_power_v41(self, life_area: str, target_date: date) -> Dict:
        """
        V5.0 House Power module calculation.

        FORMULA:
        HousePower(date) =
            Σ (HAI[h, date] * house_weight[h])
          + transit_house_overlay(date)
          + saturn_jupiter_pressure_index(date)
        """
        # Get relevant houses for life area
        area_houses = self.LIFE_AREA_HOUSES.get(life_area, [1, 2, 3])

        # House weights (primary house gets more weight)
        house_weights = [0.5, 0.3, 0.2]

        weighted_hai_sum = 0
        hai_breakdown = []

        for i, house in enumerate(area_houses[:3]):  # Top 3 relevant houses
            hai_result = self.calculate_hai(house, target_date)
            weight = house_weights[i] if i < len(house_weights) else 0.1

            weighted_hai_sum += hai_result['hai'] * weight

            hai_breakdown.append({
                'house': house,
                'hai': hai_result['hai'],
                'weight': weight,
                'weighted_contribution': round(hai_result['hai'] * weight, 3),
                'breakdown': hai_result['breakdown']
            })

        # TRANSIT HOUSE OVERLAY (date-specific)
        transit_house_overlay = 0
        if target_date:
            transit_house_overlay = self._calculate_transit_house_overlay_v50(area_houses[:3], target_date)

        # SATURN/JUPITER PRESSURE INDEX (date-specific)
        sat_jup_pressure_index = 0
        if target_date:
            sat_jup_pressure_index = self._calculate_saturn_jupiter_pressure_index(area_houses[:3], target_date)

        # V5.0 House Power Formula
        raw_score = (weighted_hai_sum * 3) + transit_house_overlay + sat_jup_pressure_index

        min_range, max_range = self.TENSOR_MODELS['house_power']['expected_range']
        normalized = (raw_score - min_range) / (max_range - min_range)
        normalized = max(0, min(1, normalized))

        # V5.8: Apply module floor and ceiling
        clamp_min = self.GLOBAL_NUMERIC_SAFETY.get('clamp_min', 0.30)
        clamp_max = self.GLOBAL_NUMERIC_SAFETY.get('clamp_max', 0.85)
        normalized = max(clamp_min, min(clamp_max, normalized))

        return {
            'module': 'house_power',
            'raw_score': round(raw_score, 3),
            'normalized': round(normalized, 4),
            'weight': self.active_weights.get('house_power', 0.18),
            'weighted_contribution': round(normalized * self.active_weights.get('house_power', 0.18), 4),
            'tensor_breakdown': {
                'weighted_hai_sum': round(weighted_hai_sum, 3),
                'transit_house_overlay': round(transit_house_overlay, 3),
                'sat_jup_pressure_index': round(sat_jup_pressure_index, 3)
            },
            'hai_details': hai_breakdown,
            'formula': 'Σ(HAI × weight) × 3 + transit_overlay + sat_jup_pressure'
        }

    def _calculate_transit_house_overlay_v50(self, houses: List[int], target_date: date) -> float:
        """Calculate transit house overlay for V6.0 - strongly positive"""
        overlay = 0

        for house in houses:
            # Check benefic transits through house (V6.0: significantly boosted)
            for benefic in self.BENEFIC_PLANETS:
                benefic_house = self._estimate_transit_house(benefic, target_date)
                if benefic_house == house:
                    overlay += 2.5  # V6.0: Strongly boosted
                # Check benefic aspects to house
                aspect_houses = self._get_planet_aspect_houses(benefic, benefic_house)
                if house in aspect_houses:
                    overlay += 1.0  # V6.0: Boosted

            # Check malefic transits through house (V6.0: minimal penalties)
            for malefic in self.MALEFIC_PLANETS:
                malefic_house = self._estimate_transit_house(malefic, target_date)
                if malefic_house == house:
                    overlay -= 0.2  # V6.0: Minimal penalty (was -0.6)
                # Check malefic aspects to house
                aspect_houses = self._get_planet_aspect_houses(malefic, malefic_house)
                if house in aspect_houses:
                    overlay -= 0.05  # V6.0: Nearly no penalty (was -0.2)

        return overlay / len(houses) if houses else 0

    def _calculate_saturn_jupiter_pressure_index(self, houses: List[int], target_date: date) -> float:
        """
        Calculate Saturn/Jupiter pressure index for houses.
        Positive = Jupiter support, Negative = Saturn pressure

        V6.0 FIX: Saturn penalties nearly eliminated, Jupiter strongly boosted
        """
        jupiter_house = self._estimate_transit_house('Jupiter', target_date)
        saturn_house = self._estimate_transit_house('Saturn', target_date)

        jupiter_index = 0
        saturn_index = 0

        for house in houses:
            # Jupiter support (V6.0: significantly boosted)
            if jupiter_house == house:
                jupiter_index += 3.5  # V6.0: Strongly boosted
            elif house in self._get_planet_aspect_houses('Jupiter', jupiter_house):
                jupiter_index += 1.8  # V6.0: Boosted
            elif self._is_trine_house(jupiter_house, house):
                jupiter_index += 1.2  # V6.0: Boosted

            # Saturn pressure (V6.0: minimal - 80% reduction)
            if saturn_house == house:
                saturn_index -= 0.2  # V6.0: Minimal (was -0.75)
            elif house in self._get_planet_aspect_houses('Saturn', saturn_house):
                saturn_index -= 0.1  # V6.0: Minimal (was -0.4)

        # V6.0: Very strict Saturn penalty cap (-0.01 max)
        saturn_penalty_cap = self.GLOBAL_NUMERIC_SAFETY.get('saturn_penalty_cap', -0.01)
        # Convert to comparable scale
        saturn_index = max(saturn_index, saturn_penalty_cap * 10)

        index = jupiter_index + saturn_index
        return index / len(houses) if houses else 0

    def _is_trine_house(self, from_house: int, to_house: int) -> bool:
        """Check if two houses are in trine relationship"""
        diff = (to_house - from_house) % 12
        return diff in [4, 8]  # 5th and 9th from

    def _calculate_planet_power_v41(self, life_area: str, target_date: date) -> Dict:
        """
        V5.0 Planet Power module calculation.

        FORMULA:
        PlanetPower(date) =
          Σ over planets p:
                POI(p, date)
              + transit_aspect_bonus(p, date)
              - transit_aspect_penalty(p, date)
              + retrograde_effect(p, date)
              - combustion_penalty(p, date)
              + varshaphal_overlay(p, date)
        """
        # Get karaka planets for life area
        karakas = self.AREA_KARAKAS.get(life_area, ['Jupiter', 'Saturn'])

        total_strength = 0
        poi_details = []

        for planet in karakas:
            # 1. POI already includes base dignity + transit modifiers
            poi_result = self.calculate_poi(planet, target_date)
            base_poi = poi_result['poi']

            # 2. TRANSIT ASPECT BONUS (date-specific)
            transit_aspect_bonus = self._calculate_benefic_transit_aspects(planet, target_date) if target_date else 0

            # 3. TRANSIT ASPECT PENALTY (date-specific)
            transit_aspect_penalty = self._calculate_malefic_transit_aspects(planet, target_date) if target_date else 0

            # 4. RETROGRADE EFFECT (date-specific)
            retrograde_effect = self._calculate_retrograde_modifier(planet, target_date) if target_date else 0

            # 5. COMBUSTION PENALTY (date-specific)
            combustion_penalty = abs(self._calculate_combustion_modifier(planet, target_date)) if target_date else 0

            # 6. VARSHAPHAL OVERLAY (year-specific)
            varshaphal_overlay = 0
            if target_date and self.current_time_mode == TimeMode.YEAR_OVERLAY:
                varshaphal_overlay = self._calculate_varshaphal_planet_overlay(planet, target_date)

            # V5.0 Planet Power Formula
            planet_power = (
                base_poi
                + transit_aspect_bonus
                - transit_aspect_penalty
                + retrograde_effect
                - combustion_penalty
                + varshaphal_overlay
            )

            # Enemy/Friend factor
            ef_factor = self._get_enemy_friend_factor(planet)
            planet_power *= ef_factor

            total_strength += planet_power

            poi_details.append({
                'planet': planet,
                'base_poi': round(base_poi, 3),
                'transit_aspect_bonus': round(transit_aspect_bonus, 3),
                'transit_aspect_penalty': round(transit_aspect_penalty, 3),
                'retrograde_effect': round(retrograde_effect, 3),
                'combustion_penalty': round(combustion_penalty, 3),
                'varshaphal_overlay': round(varshaphal_overlay, 3),
                'ef_factor': round(ef_factor, 3),
                'final_power': round(planet_power, 3)
            })

        avg_strength = total_strength / len(karakas) if karakas else 5

        # Normalize
        min_range, max_range = self.TENSOR_MODELS['planet_power']['expected_range']
        normalized = (avg_strength - min_range) / (max_range - min_range)
        normalized = max(0, min(1, normalized))

        # V5.8: Apply module floor and ceiling
        clamp_min = self.GLOBAL_NUMERIC_SAFETY.get('clamp_min', 0.30)
        clamp_max = self.GLOBAL_NUMERIC_SAFETY.get('clamp_max', 0.85)
        normalized = max(clamp_min, min(clamp_max, normalized))

        return {
            'module': 'planet_power',
            'raw_score': round(avg_strength, 3),
            'normalized': round(normalized, 4),
            'weight': self.active_weights.get('planet_power', 0.12),
            'weighted_contribution': round(normalized * self.active_weights.get('planet_power', 0.12), 4),
            'poi_details': poi_details,
            'formula': 'Σ(POI + transit_bonus - transit_penalty + retro_effect - combustion + varshaphal) × EF'
        }

    def _calculate_varshaphal_planet_overlay(self, planet: str, target_date: date) -> float:
        """Calculate Varshaphal (Solar Return) overlay for a planet"""
        birth_date = self._get_birth_date()
        age = target_date.year - birth_date.year

        # Get muntha position
        muntha_sign_num = (self.lagna_num + age) % 12

        # Check if planet is in muntha sign or aspects it
        planet_data = self.planets.get(planet, {})
        planet_house = planet_data.get('house', 1)

        # Calculate muntha house from lagna
        muntha_house = muntha_sign_num + 1

        overlay = 0

        # Planet in muntha sign
        if planet_house == muntha_house:
            overlay = 1.0

        # Planet aspects muntha
        aspect_houses = self._get_planet_aspect_houses(planet, planet_house)
        if muntha_house in aspect_houses:
            overlay = 0.5

        # Year lord bonus
        solar_return_date = date(target_date.year, birth_date.month, birth_date.day)
        try:
            weekday = solar_return_date.weekday()
            year_lords = ['Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Sun']
            year_lord = year_lords[weekday]
            if planet == year_lord:
                overlay += 0.8
        except:
            pass

        return overlay

    def _get_enemy_friend_factor(self, planet: str) -> float:
        """Get enemy/friend relationship factor for planet"""
        planet_data = self.planets.get(planet, {})
        dispositor = planet_data.get('dispositor', '')

        # Natural friendships
        friends = {
            'Sun': ['Moon', 'Mars', 'Jupiter'],
            'Moon': ['Sun', 'Mercury'],
            'Mars': ['Sun', 'Moon', 'Jupiter'],
            'Mercury': ['Sun', 'Venus'],
            'Jupiter': ['Sun', 'Moon', 'Mars'],
            'Venus': ['Mercury', 'Saturn'],
            'Saturn': ['Mercury', 'Venus']
        }

        enemies = {
            'Sun': ['Venus', 'Saturn'],
            'Moon': ['Rahu', 'Ketu'],
            'Mars': ['Mercury'],
            'Mercury': ['Moon'],
            'Jupiter': ['Mercury', 'Venus'],
            'Venus': ['Sun', 'Moon'],
            'Saturn': ['Sun', 'Moon', 'Mars']
        }

        if dispositor in friends.get(planet, []):
            return 1.2
        elif dispositor in enemies.get(planet, []):
            return 0.8
        return 1.0

    def _calculate_yoga_dosha_v41(self, target_date: date) -> Dict:
        """
        V5.7 Yoga-Dosha module calculation with STRICT TIME-DEPENDENT activation.

        V5.7 CRITICAL RULE:
        - Yoga activation: ONLY if yoga planet = dasha OR bhukti lord
        - Transit activation REMOVED - transits alone cannot activate yogas
        - This is stricter than V5.0 which allowed 0.5 transit activation

        V5.7 REFINEMENTS:
        - YogaPresence = 1 or 0 (birth chart)
        - YogaActivation = 1.0 ONLY IF dasha/bhukti lord forms the yoga
        - YogaActivation = 0 otherwise (NO transit fallback)
        - OrbStrength = degree-based angular separation factor (0.5-1.0)
        - FinalYogaScore = Σ(YogaPresence × YogaActivation × YogaStrength × OrbStrength × TransitSupport)
        """
        # Use base class yoga calculation for PRESENCE
        yoga_result = self.calculate_yoga_score()

        yoga_score = yoga_result.get('raw_score', 0)
        yogas = yoga_result.get('yogas', [])  # Yoga names present in birth chart
        doshas = yoga_result.get('doshas', [])
        factors = yoga_result.get('factors', [])

        # Get current dasha/bhukti lords for activation check
        dasha_info = self.jathagam.get('dasha', {})
        current = dasha_info.get('current', {})
        dasha_lord = current.get('lord', '') if isinstance(current, dict) else ''
        bhukti_lord = current.get('antardasha_lord', '') if isinstance(current, dict) else ''

        # Yoga karakas mapping
        yoga_karakas = {
            'gajakesari': ['Jupiter', 'Moon'],
            'budha_aditya': ['Mercury', 'Sun'],
            'chandra_mangala': ['Moon', 'Mars'],
            'dhana': ['Jupiter', 'Venus'],
            'raja': ['Sun', 'Jupiter'],
            'raja_yoga': ['Sun', 'Jupiter'],
            'hamsa': ['Jupiter'],
            'malavya': ['Venus'],
            'bhadra': ['Mercury'],
            'ruchaka': ['Mars'],
            'shasha': ['Saturn'],
            'neechabhanga': ['Saturn', 'Mars'],  # Debilitation cancellation
        }

        # Calculate yoga tensor with V5.0 STRICT ACTIVATION
        yoga_tensor = 0
        activated_yogas = []
        dormant_yogas = []

        for yoga in yogas:
            yoga_key = yoga.lower().replace(' ', '_')
            planets = yoga_karakas.get(yoga_key, ['Jupiter'])

            # --- V5.7: STRICT YOGA ACTIVATION CHECK ---
            # V5.7 CRITICAL: ONLY dasha/bhukti lord participation activates yoga
            # Transit activation REMOVED (was 0.5 in V5.0)
            yoga_activation = 0
            activation_reason = 'dormant'

            # V5.7 ONLY ACTIVATION: Dasha/Bhukti lord MUST be a yoga-forming planet
            # This is the ONLY way to activate a yoga - NO transit fallback
            if dasha_lord in planets:
                yoga_activation = 1.0
                activation_reason = f'dasha_lord_{dasha_lord}'
            elif bhukti_lord in planets:
                yoga_activation = 1.0
                activation_reason = f'bhukti_lord_{bhukti_lord}'
            # V5.7: NO transit activation fallback - yoga stays dormant if not dasha/bhukti activated

            # --- V5.7: DEGREE-BASED ORB STRENGTH ---
            orb_strength = self._calculate_yoga_orb_strength(planets)

            # --- YOGA STRENGTH (rarity) ---
            yoga_factor = next((f for f in factors if yoga.lower() in str(f).lower()), None)
            if isinstance(yoga_factor, dict):
                yoga_rarity = yoga_factor.get('rarity', 'medium')
                strength_map = {'rare': 4, 'uncommon': 2, 'common': 1}
                yoga_strength = strength_map.get(yoga_rarity, 2)
            else:
                yoga_strength = 2

            # --- TRANSIT SUPPORT for yoga planets ---
            transit_support = sum(
                self.calculate_poi(p, target_date)['poi'] for p in planets
            ) / len(planets) if planets else 5

            # --- V5.8 YOGA SCORE FORMULA ---
            # V5.8 FIX: Presence score even without activation
            # presence_score = 0.04 (just having yoga gives points)
            # activation_score = 0.08 (dasha activation bonus)
            presence_score = self.YOGA_SCORE_RULES.get('presence_score', 0.04)
            activation_bonus = self.YOGA_SCORE_RULES.get('activation_score', 0.08)

            # V5.8: Presence contribution (always given if yoga exists)
            presence_contribution = presence_score * yoga_strength * orb_strength

            # V5.8: Activation contribution (only if dasha/bhukti activates)
            activation_contribution = 0
            if yoga_activation > 0:
                activation_contribution = activation_bonus * yoga_strength * orb_strength * (transit_support / 5)

            yoga_contribution = presence_contribution + activation_contribution

            # V5.8: All yogas get at least presence score
            yoga_tensor += yoga_contribution

            if yoga_activation > 0:
                activated_yogas.append({
                    'name': yoga,
                    'activation': round(yoga_activation, 2),
                    'activation_reason': activation_reason,
                    'strength': yoga_strength,
                    'orb_strength': round(orb_strength, 2),
                    'transit_support': round(transit_support, 2),
                    'presence_contribution': round(presence_contribution, 3),
                    'activation_contribution': round(activation_contribution, 3),
                    'contribution': round(yoga_contribution, 3)
                })
            else:
                dormant_yogas.append({
                    'name': yoga,
                    'presence_contribution': round(presence_contribution, 3),
                    'note': 'V5.8: Presence score given even when dormant'
                })

        # Dosha penalties (also time-dependent)
        dosha_tensor = 0
        active_doshas = []

        for dosha in doshas:
            dosha_name = dosha if isinstance(dosha, str) else dosha.get('name', str(dosha))
            dosha_key = dosha_name.lower()

            # V6.0: Minimal base penalties (80% reduction from original)
            dosha_penalties = {
                'manglik': -0.5,    # V6.0: Minimal (was -3)
                'kala_sarpa': -0.6, # V6.0: Minimal (was -4)
                'pitru': -0.3,      # V6.0: Minimal (was -2)
                'nadi': -0.3,       # V6.0: Minimal (was -2)
                'kemadruma': -0.3,  # V6.0: Minimal (was -2)
            }
            base_penalty = dosha_penalties.get(dosha_key, -0.3)

            # V6.0: Very low dosha activation (doshas rarely activate)
            dosha_activation = 0.15  # V6.0: Very low baseline

            # Kala Sarpa activates when Rahu/Ketu transit sensitive points
            if 'kala' in dosha_key or 'sarpa' in dosha_key:
                rahu_house = self._estimate_transit_house('Rahu', target_date)
                if rahu_house in [1, 4, 7, 10]:  # Kendra transit
                    dosha_activation = 0.3  # V6.0: Still low activation

            # Manglik activates during Mars transits to 1,4,7,8,12
            if 'manglik' in dosha_key:
                mars_house = self._estimate_transit_house('Mars', target_date)
                if mars_house in [1, 4, 7, 8, 12]:
                    dosha_activation = 0.3  # V6.0: Still low activation

            # V6.0: Minimal Saturn amplification
            if dasha_lord == 'Saturn' or bhukti_lord == 'Saturn':
                dosha_activation = min(0.4, dosha_activation + 0.05)  # V6.0: Minimal boost

            penalty = base_penalty * dosha_activation
            dosha_tensor += penalty * 0.3  # V6.0: Much reduced multiplier (was 0.7)

            if dosha_activation > 0.2:
                active_doshas.append({
                    'name': dosha_name,
                    'activation': round(dosha_activation, 2),
                    'penalty': round(penalty * 0.3, 2)
                })

        # V5.8: Cap negative dosha impact
        negative_yoga_cap = self.YOGA_SCORE_RULES.get('negative_yoga_cap', -0.05)
        # Scale to raw score range (approx -0.5 for -0.05 normalized)
        dosha_tensor = max(dosha_tensor, negative_yoga_cap * 10)

        # V5.8: Cap total yoga contribution
        max_yoga_contribution = self.YOGA_SCORE_RULES.get('max_yoga_contribution', 0.15)
        yoga_tensor = min(yoga_tensor, max_yoga_contribution * 10)

        raw_score = yoga_tensor + dosha_tensor

        min_range, max_range = self.TENSOR_MODELS['yoga_dosha']['expected_range']
        normalized = (raw_score - min_range) / (max_range - min_range)
        normalized = max(0, min(1, normalized))

        # V5.8: Apply module floor and ceiling
        clamp_min = self.GLOBAL_NUMERIC_SAFETY.get('clamp_min', 0.30)
        clamp_max = self.GLOBAL_NUMERIC_SAFETY.get('clamp_max', 0.85)
        normalized = max(clamp_min, min(clamp_max, normalized))

        return {
            'module': 'yoga_dosha',
            'raw_score': round(raw_score, 3),
            'normalized': round(normalized, 4),
            'weight': self.active_weights.get('yoga_dosha', 0.12),
            'weighted_contribution': round(normalized * self.active_weights.get('yoga_dosha', 0.12), 4),
            'tensor_breakdown': {
                'yoga_tensor': round(yoga_tensor, 3),
                'dosha_tensor': round(dosha_tensor, 3),
                'activated_count': len(activated_yogas),
                'dormant_count': len(dormant_yogas)
            },
            'yogas': yogas,
            'activated_yogas': activated_yogas,
            'dormant_yogas': dormant_yogas,
            'doshas': doshas,
            'active_doshas': active_doshas,
            'formula': 'V5.8: Σ(presence_score + activation_bonus) - Σ(DoshaPenalty) with caps',
            'activation_note': 'V5.8: Presence score given even when dormant. Yogas activate ONLY if dasha/bhukti lord is yoga-forming planet.'
        }

    def _calculate_yoga_orb_strength(self, planets: List[str]) -> float:
        """
        V5.0 NEW: Calculate degree-based orb strength for yoga planets.

        Yogas are stronger when the participating planets are in tighter
        angular relationships (closer degrees within the same sign/aspect).

        Orb calculation:
        - Planets in same sign within 5°: 1.0 (tight conjunction)
        - Planets in same sign within 10°: 0.9
        - Planets in same sign within 15°: 0.8
        - Planets in same sign within 20°: 0.7
        - Planets in same sign beyond 20°: 0.6
        - Planets in different signs (aspect-based): 0.5-0.8

        Args:
            planets: List of planets forming the yoga

        Returns:
            Orb strength multiplier (0.5 to 1.0)
        """
        if len(planets) < 2:
            return 1.0  # Single planet yogas have full strength

        # Get longitudes for first two planets (primary yoga-formers)
        planet1_data = self.planets.get(planets[0], {})
        planet2_data = self.planets.get(planets[1], {})

        long1 = planet1_data.get('longitude', 0)
        long2 = planet2_data.get('longitude', 0)

        # Calculate angular separation
        separation = abs(long1 - long2)
        if separation > 180:
            separation = 360 - separation

        # Check if same sign (conjunction-type yoga)
        sign1 = int(long1 / 30)
        sign2 = int(long2 / 30)

        if sign1 == sign2:
            # Same sign - degree separation matters
            degree_diff = abs((long1 % 30) - (long2 % 30))
            if degree_diff <= 5:
                return 1.0   # Tight conjunction
            elif degree_diff <= 10:
                return 0.9
            elif degree_diff <= 15:
                return 0.8
            elif degree_diff <= 20:
                return 0.7
            else:
                return 0.6
        else:
            # Different signs - check aspect-based yoga
            # Kendra (1, 4, 7, 10) - strong
            house_diff = abs(sign1 - sign2)
            if house_diff in [0, 3, 6, 9]:  # Kendra (square/opposite)
                return 0.8
            elif house_diff in [4, 8]:  # Trikona (trine)
                return 0.75
            else:
                return 0.5  # Weaker aspect

    def _calculate_navamsa_module_v41(self, life_area: str, target_date: Optional[date] = None) -> Dict:
        """
        v4.1 Navamsa module calculation with YEAR-SPECIFIC activation.

        CRITICAL: D9 chart is static, but ACTIVATION changes yearly based on:
        - Transit support to D9 planets
        - Dasha lord support in D9
        - Enemy sign conflicts (year-dependent transits)
        """
        karakas = self.AREA_KARAKAS.get(life_area, ['Jupiter', 'Saturn'])
        if target_date is None:
            target_date = date.today()

        total_support = 0
        navamsa_details = []

        # Get dasha lord for activation check
        dasha_info = self.jathagam.get('dasha', {})
        current = dasha_info.get('current', {})
        dasha_lord = current.get('lord', 'Jupiter') if isinstance(current, dict) else 'Jupiter'

        for planet in karakas:
            support_result = self.calculate_navamsa_support(planet)
            base_support = support_result['navamsa_support']

            # --- YEAR-SPECIFIC TRANSIT SUPPORT TO D9 ---
            # Check transit planets aspecting D9 position of this planet
            transit_d9_support = self._calculate_transit_d9_support(planet, target_date)

            # --- DASHA LORD SUPPORT IN D9 ---
            dasha_d9_support = 0
            if dasha_lord == planet:
                dasha_d9_support = 1.5  # Dasha lord in D9 gets boost
            elif self._are_friendly(dasha_lord, planet):
                dasha_d9_support = 0.5

            # --- ENEMY SIGN CONFLICT (year-dependent) ---
            enemy_conflict = self._calculate_d9_enemy_conflict(planet, target_date)

            # FINAL year-adjusted support
            year_adjusted_support = base_support + transit_d9_support + dasha_d9_support - enemy_conflict

            total_support += year_adjusted_support
            navamsa_details.append({
                'planet': planet,
                'navamsa_support': round(year_adjusted_support, 3),
                'breakdown': {
                    'd1_dignity': support_result.get('breakdown', {}).get('d1_dignity', 'neutral'),
                    'd9_dignity': support_result.get('breakdown', {}).get('d9_dignity', 'neutral'),
                    'base_support': round(base_support, 3),
                    'transit_d9_support': round(transit_d9_support, 3),
                    'dasha_d9_support': round(dasha_d9_support, 3),
                    'enemy_conflict': round(enemy_conflict, 3),
                    'navamsa_amplification': self.active_multipliers.get('navamsa_amplification', 1.0)
                },
                'formula': f'Support = ({base_support:.2f} + {transit_d9_support:.2f} + {dasha_d9_support:.2f} - {enemy_conflict:.2f}) × amplification'
            })

        avg_support = total_support / len(karakas) if karakas else 0

        # Check D9 compatibility
        compat_bonus = 0
        conflict_penalty = 0

        # Compatibility check based on D9 positions
        navamsa_data = self.jathagam.get('navamsa', {})
        if navamsa_data:
            # Year-dependent: Check if transits support D9 lagna
            d9_lagna = navamsa_data.get('lagna', {}).get('rasi', '')
            jupiter_transit_rasi = self._get_transit_rasi('Jupiter', target_date)

            if jupiter_transit_rasi == d9_lagna:
                compat_bonus = 3  # Jupiter transiting D9 lagna
            elif self._is_trine_sign(jupiter_transit_rasi, d9_lagna):
                compat_bonus = 2
            else:
                compat_bonus = 0.5

            # Saturn transit check for conflict
            saturn_transit_rasi = self._get_transit_rasi('Saturn', target_date)
            if saturn_transit_rasi == d9_lagna:
                conflict_penalty = 1.5

        raw_score = (avg_support * 0.12) + compat_bonus - conflict_penalty

        # Scale to expected range
        raw_score = raw_score * 5 + 10  # Shift to 0-25 range

        min_range, max_range = self.TENSOR_MODELS['navamsa']['expected_range']
        normalized = (raw_score - min_range) / (max_range - min_range)
        normalized = max(0, min(1, normalized))

        # Apply navamsa amplification from time mode
        amplification = self.active_multipliers.get('navamsa_amplification', 1.0)
        normalized = min(1.0, normalized * amplification)

        return {
            'module': 'navamsa',
            'raw_score': round(raw_score, 3),
            'normalized': round(normalized, 4),
            'weight': self.active_weights.get('navamsa', 0.13),
            'weighted_contribution': round(normalized * self.active_weights.get('navamsa', 0.13), 4),
            'tensor_breakdown': {
                'avg_support': round(avg_support, 3),
                'compat_bonus': round(compat_bonus, 3),
                'conflict_penalty': round(conflict_penalty, 3),
                'amplification': amplification
            },
            'navamsa_details': navamsa_details,
            'target_year': target_date.year,
            'formula': 'Σ(D9_dignity × D1_D9_tensor × 0.12 + transit_support + dasha_support - conflict) × amplification'
        }

    def _calculate_transit_d9_support(self, planet: str, target_date: date) -> float:
        """Calculate transit support to D9 position of a planet"""
        navamsa_data = self.jathagam.get('navamsa', {}).get('planets', {})
        d9_planet = navamsa_data.get(planet, {})
        d9_rasi = d9_planet.get('rasi', '')

        if not d9_rasi:
            return 0

        support = 0

        # Check if Jupiter is transiting the D9 rasi or its trines
        jupiter_transit_rasi = self._get_transit_rasi('Jupiter', target_date)
        if jupiter_transit_rasi == d9_rasi:
            support += 1.0
        elif self._is_trine_sign(jupiter_transit_rasi, d9_rasi):
            support += 0.5

        # Check if benefics are aspecting the D9 position
        for benefic in ['Jupiter', 'Venus', 'Mercury']:
            benefic_transit_rasi = self._get_transit_rasi(benefic, target_date)
            if self._is_aspecting(benefic_transit_rasi, d9_rasi):
                support += 0.3

        return support

    def _calculate_d9_enemy_conflict(self, planet: str, target_date: date) -> float:
        """Calculate D9 enemy sign conflict based on transits"""
        navamsa_data = self.jathagam.get('navamsa', {}).get('planets', {})
        d9_planet = navamsa_data.get(planet, {})
        d9_rasi = d9_planet.get('rasi', '')

        conflict = 0

        # Check if malefics are transiting the D9 position
        for malefic in ['Saturn', 'Mars', 'Rahu']:
            malefic_transit_rasi = self._get_transit_rasi(malefic, target_date)
            if malefic_transit_rasi == d9_rasi:
                conflict += 0.8
            elif self._is_aspecting(malefic_transit_rasi, d9_rasi):
                conflict += 0.3

        return conflict

    def _get_transit_rasi(self, planet: str, target_date: date) -> str:
        """Get the rasi a planet is transiting on a given date"""
        transit_house = self._estimate_transit_house(planet, target_date)
        # Convert house to rasi based on moon position
        moon_rasi = self.jathagam.get('moon_sign', {}).get('rasi', 'Aries')
        rasi_order = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                      'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

        try:
            moon_idx = rasi_order.index(moon_rasi)
        except ValueError:
            moon_idx = 0

        transit_rasi_idx = (moon_idx + transit_house - 1) % 12
        return rasi_order[transit_rasi_idx]

    def _is_trine_sign(self, rasi1: str, rasi2: str) -> bool:
        """Check if two rasis are in trine (same element)"""
        rasi_order = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                      'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        try:
            idx1 = rasi_order.index(rasi1)
            idx2 = rasi_order.index(rasi2)
            diff = abs(idx1 - idx2) % 12
            return diff in [0, 4, 8]  # Same element (fire, earth, air, water)
        except ValueError:
            return False

    def _is_aspecting(self, from_rasi: str, to_rasi: str) -> bool:
        """Check if from_rasi aspects to_rasi (simplified)"""
        rasi_order = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                      'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        try:
            idx1 = rasi_order.index(from_rasi)
            idx2 = rasi_order.index(to_rasi)
            diff = (idx2 - idx1) % 12
            # Major aspects: opposition(7), trine(5,9), square(4,10), sextile(3,11)
            return diff in [3, 5, 7, 9, 11]
        except ValueError:
            return False

    def _are_friendly(self, planet1: str, planet2: str) -> bool:
        """Check if two planets are natural friends"""
        friendships = {
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
        return planet2 in friendships.get(planet1, [])

    def _calculate_meta_multiplier_v57(self, modules: Dict, target_date: date) -> float:
        """
        V5.7: Calculate meta multiplier with stricter bounds.

        V5.7 Meta Multiplier Logic:
        - Base: 1.0
        - Nakshatra Effect: nes × 0.01 (capped contribution)
        - Overall POI: poi_avg × 0.003 (reduced from 0.005)
        - STRICT RANGE: 0.90 to 1.10 (no exceptions)
        - Future/Year modes: small adjustments within range

        Formula: meta = clamp(1.0 + nes_contrib + poi_contrib + mode_adj, 0.90, 1.10)
        """
        # V5.7: Get strict bounds from global safety config
        meta_min = self.GLOBAL_NUMERIC_SAFETY.get('meta_multiplier_min', 0.90)
        meta_max = self.GLOBAL_NUMERIC_SAFETY.get('meta_multiplier_max', 1.10)

        # Nakshatra effect score (NES)
        nakshatra_mult = self._get_nakshatra_multiplier()
        nes = (nakshatra_mult - 1.0) * 100  # Convert to percentage
        nes_contribution = nes * 0.01  # Cap at +/- 0.05 effective
        nes_contribution = max(-0.05, min(0.05, nes_contribution))

        # Overall POI average (V5.7: reduced coefficient)
        all_pois = [self.calculate_poi(p, target_date)['poi'] for p in self.planets.keys()]
        overall_poi = sum(all_pois) / len(all_pois) if all_pois else 5
        poi_contribution = (overall_poi - 5) * 0.003  # Centered at 5, reduced from 0.005
        poi_contribution = max(-0.03, min(0.03, poi_contribution))

        # Base calculation
        meta = 1.0 + nes_contribution + poi_contribution

        # Mode-specific adjustments (small, within bounds)
        mode_adjustment = 0.0

        if self.current_time_mode == TimeMode.FUTURE_PREDICTION:
            # V5.7: Very small future adjustment
            months_ahead = max(0, (target_date - date.today()).days / 30)
            mode_adjustment = min(0.02, months_ahead * 0.002)  # Max +0.02

        elif self.current_time_mode == TimeMode.YEAR_OVERLAY:
            # V5.7: Varshaphal factor (small)
            varshaphal_poi = self._calculate_varshaphal_poi(target_date)
            mode_adjustment = (varshaphal_poi - 5) * 0.005  # Centered at 5
            mode_adjustment = max(-0.02, min(0.02, mode_adjustment))

        meta += mode_adjustment

        # V5.7: STRICT CLAMPING - no exceptions
        meta = max(meta_min, min(meta_max, meta))

        return round(meta, 4)

    def _calculate_meta_multiplier_v41(self, modules: Dict, target_date: date) -> float:
        """Backward compatible wrapper - calls V5.7 implementation"""
        return self._calculate_meta_multiplier_v57(modules, target_date)

    def _calculate_varshaphal_poi(self, target_date: date) -> float:
        """Calculate Varshaphal (Solar Return) POI for yearly mode"""
        # Simplified Varshaphal calculation
        # In full implementation, this would calculate the solar return chart
        birth_date = self._get_birth_date()
        age = target_date.year - birth_date.year

        # Get solar return ascendant (simplified)
        sun_data = self.planets.get('Sun', {})
        natal_sun_long = sun_data.get('longitude', 0)

        # Varshaphal POI is based on muntha (progressed ascendant)
        muntha_sign = (self.lagna_num + age) % 12

        # Base Varshaphal POI
        varshaphal_poi = 5.0  # Neutral

        # Adjust based on muntha position
        if muntha_sign in [1, 5, 9]:  # Trines
            varshaphal_poi = 7.0
        elif muntha_sign in [4, 7, 10]:  # Kendras
            varshaphal_poi = 6.5
        elif muntha_sign in [6, 8, 12]:  # Dusthanas
            varshaphal_poi = 4.0

        return varshaphal_poi

    def _calculate_confidence_v41(self, modules: Dict, target_date: date) -> Dict:
        """Calculate v4.1 confidence score"""
        # Data completeness
        total_fields = 0
        filled_fields = 0

        for planet in self.planets.values():
            total_fields += 5
            if planet.get('longitude'): filled_fields += 1
            if planet.get('rasi'): filled_fields += 1
            if planet.get('house'): filled_fields += 1
            if planet.get('nakshatra'): filled_fields += 1
            if planet.get('dignity'): filled_fields += 1

        completeness = filled_fields / total_fields if total_fields > 0 else 0.5

        # Module variance
        normalized_scores = [m['normalized'] for m in modules.values()]
        if len(normalized_scores) > 1:
            variance = sum((s - sum(normalized_scores)/len(normalized_scores))**2 for s in normalized_scores) / len(normalized_scores)
            variance_factor = max(0, 1 - variance * 2)
        else:
            variance_factor = 0.8

        # Time mode confidence adjustment
        mode_confidence = {
            TimeMode.PRESENT: 0.95,
            TimeMode.PAST_ANALYSIS: 0.90,
            TimeMode.FUTURE_PREDICTION: 0.75,
            TimeMode.MONTH_WISE: 0.85,
            TimeMode.YEAR_OVERLAY: 0.70
        }

        time_factor = mode_confidence.get(self.current_time_mode, 0.80)

        # Days from today factor (confidence decreases with distance)
        days_diff = abs((target_date - date.today()).days)
        distance_factor = max(0.5, 1 - (days_diff / 3650) * 0.3)  # Degrades over 10 years

        # Calculate final confidence
        confidence = (
            completeness * 0.25 +
            variance_factor * 0.25 +
            time_factor * 0.30 +
            distance_factor * 0.20
        ) * 100

        interpretation = 'அதிக நம்பகத்தன்மை' if confidence >= 70 else 'நடுத்தர நம்பகத்தன்மை' if confidence >= 50 else 'குறைந்த நம்பகத்தன்மை'

        return {
            'score': round(confidence, 1),
            'breakdown': {
                'data_completeness': round(completeness * 100, 1),
                'module_variance': round(variance_factor * 100, 1),
                'time_mode_factor': round(time_factor * 100, 1),
                'temporal_distance': round(distance_factor * 100, 1)
            },
            'interpretation': interpretation,
            'interpretation_en': 'High confidence' if confidence >= 70 else 'Medium confidence' if confidence >= 50 else 'Low confidence'
        }

    def _get_top_drivers(self, modules: Dict, positive: bool = True, top_n: int = 3) -> List[Dict]:
        """Get top positive or negative score drivers"""
        drivers = []

        for module_name, module_data in modules.items():
            weighted = module_data['weighted_contribution']
            normalized = module_data['normalized']

            # Determine if this is positive or negative
            is_positive = normalized > 0.5

            if (positive and is_positive) or (not positive and not is_positive):
                drivers.append({
                    'module': module_name,
                    'contribution': round(weighted * 100, 2),
                    'normalized_score': round(normalized, 3),
                    'weight': module_data['weight'],
                    'impact': 'positive' if is_positive else 'negative'
                })

        # Sort by absolute contribution
        drivers.sort(key=lambda x: abs(x['contribution']), reverse=True)

        return drivers[:top_n]

    # ==================== V7.0 DUAL-TRACK SCORING METHODS ====================

    def _calculate_pressure_score_v70(self, modules: Dict, target_date: date, dasha_lord: str = None) -> Dict:
        """
        V7.0: Calculate PRESSURE score (effort required, not bad outcome)

        Pressure = effort cost, strain, challenge level
        High pressure does NOT mean bad outcome - it means more effort required

        Returns:
            Dict with pressure_score (0-100), pressure_factors list, and phase_label
        """
        pressure_score = 0
        pressure_factors = []

        # 1. Check dasha lord - malefics add pressure
        if dasha_lord in self.PRESSURE_PLANETS:
            # Apply time decay based on how long the dasha has been running
            decay_k = self.PRESSURE_OUTCOME_CONFIG['time_decay_rates'].get(dasha_lord, 6)
            # Estimate months into dasha (simplified - use start of current year as reference)
            months_elapsed = max(0, (target_date.month - 1))  # Simplified decay
            decay_factor = math.exp(-months_elapsed / decay_k)

            base_pressure = 20 if dasha_lord == 'Saturn' else 15
            pressure_contribution = base_pressure * decay_factor

            pressure_score += pressure_contribution
            pressure_factors.append({
                'factor': f'{dasha_lord} Dasha',
                'contribution': round(pressure_contribution, 1),
                'type': 'effort_phase',
                'description_en': f'{dasha_lord} period requires sustained effort',
                'description_ta': f'{dasha_lord} காலம் தொடர்ச்சியான முயற்சி தேவை'
            })

        # 2. Check Saturn transit influence
        saturn_module = modules.get('transit', {})
        transit_details = saturn_module.get('tensor_breakdown', {})

        # Saturn pressure from transit
        saturn_transit_pressure = abs(transit_details.get('saturn_pressure', 0)) * 10
        if saturn_transit_pressure > 0:
            decay_k = self.PRESSURE_OUTCOME_CONFIG['time_decay_rates']['Saturn']
            saturn_transit_pressure *= math.exp(-target_date.month / decay_k)  # Time decay

            pressure_score += min(saturn_transit_pressure, 15)  # Cap individual factor
            if saturn_transit_pressure > 3:
                pressure_factors.append({
                    'factor': 'Saturn Transit',
                    'contribution': round(min(saturn_transit_pressure, 15), 1),
                    'type': 'delayed_reward',
                    'description_en': 'Saturn transit brings delayed rewards',
                    'description_ta': 'சனி கோச்சாரம் தாமதமான பலன்கள்'
                })

        # 3. Check Mars influence (short-term pressure)
        mars_data = self.planets.get('Mars', {})
        if mars_data.get('house') in [1, 4, 7, 8, 12]:  # Mars in challenging houses
            decay_k = self.PRESSURE_OUTCOME_CONFIG['time_decay_rates']['Mars']
            mars_pressure = 10 * math.exp(-target_date.month / decay_k)

            pressure_score += mars_pressure
            pressure_factors.append({
                'factor': 'Mars Energy',
                'contribution': round(mars_pressure, 1),
                'type': 'action_required',
                'description_en': 'Mars energy requires channeled action',
                'description_ta': 'செவ்வாய் ஆற்றல் செயல்பாடு தேவை'
            })

        # 4. Cap total pressure at max_negativity_per_period
        max_negativity = self.GLOBAL_NUMERIC_SAFETY.get('max_negativity_per_period', 30)
        pressure_score = min(pressure_score, max_negativity)

        # Determine phase label based on pressure level
        if pressure_score >= 20:
            phase = 'high_pressure_neutral_outcome'
        elif pressure_score >= 10:
            phase = 'neutral'
        else:
            phase = 'low_pressure_positive_outcome'

        return {
            'pressure_score': round(pressure_score, 1),
            'pressure_factors': pressure_factors[:3],  # Top 3 factors
            'phase_key': phase,
            'max_capped': max_negativity
        }

    def _calculate_outcome_score_v70(self, modules: Dict, target_date: date, dasha_lord: str = None) -> Dict:
        """
        V7.0.2: Calculate OUTCOME score (potential gains)

        Outcome = what you actually achieve, independent of effort
        High pressure can still have positive outcome!
        V7.0.2: Enhanced positive detection for more optimistic scores

        Returns:
            Dict with outcome_score, outcome_factors, and compound_multiplier
        """
        outcome_score = 55  # V7.0.2: Start at slightly positive baseline
        outcome_factors = []
        positive_count = 0

        # 1. Jupiter influence (always positive)
        jupiter_data = self.planets.get('Jupiter', {})
        jupiter_dignity = jupiter_data.get('dignity', 'neutral')
        jupiter_house = jupiter_data.get('house', 1)

        if jupiter_dignity in ['exalted', 'own', 'mooltrikona']:
            outcome_score += 12
            positive_count += 1
            outcome_factors.append({
                'factor': 'Jupiter Strength',
                'contribution': 12,
                'type': 'blessing',
                'description_en': 'Strong Jupiter brings expansion and wisdom',
                'description_ta': 'வலுவான குரு விரிவாக்கம் தருகிறது'
            })
        elif jupiter_house in [1, 4, 5, 7, 9, 10, 11]:  # Kendras and trikonas
            outcome_score += 8
            positive_count += 1
            outcome_factors.append({
                'factor': 'Jupiter Position',
                'contribution': 8,
                'type': 'opportunity',
                'description_en': 'Jupiter placement supports growth',
                'description_ta': 'குரு நிலை வளர்ச்சிக்கு உதவுகிறது'
            })

        # 2. Venus influence (harmony and comfort)
        venus_data = self.planets.get('Venus', {})
        venus_dignity = venus_data.get('dignity', 'neutral')
        venus_house = venus_data.get('house', 1)

        if venus_dignity in ['exalted', 'own', 'mooltrikona']:
            outcome_score += 10
            positive_count += 1
            outcome_factors.append({
                'factor': 'Venus Strength',
                'contribution': 10,
                'type': 'harmony',
                'description_en': 'Strong Venus brings comfort and harmony',
                'description_ta': 'வலுவான சுக்கிரன் ஆறுதல் தருகிறது'
            })
        elif venus_house in [1, 2, 4, 5, 7, 9, 11]:  # Good houses for Venus
            outcome_score += 5
            positive_count += 1
            outcome_factors.append({
                'factor': 'Venus Position',
                'contribution': 5,
                'type': 'comfort',
                'description_en': 'Venus placement brings material comfort',
                'description_ta': 'சுக்கிரன் நிலை வசதி தருகிறது'
            })

        # 3. Saturn strength (V7.0.2: Saturn own/exalted is positive!)
        saturn_data = self.planets.get('Saturn', {})
        saturn_dignity = saturn_data.get('dignity', 'neutral')

        if saturn_dignity in ['exalted', 'own', 'mooltrikona']:
            outcome_score += 8
            positive_count += 1
            outcome_factors.append({
                'factor': 'Saturn Discipline',
                'contribution': 8,
                'type': 'stability',
                'description_en': 'Strong Saturn brings discipline and stability',
                'description_ta': 'வலுவான சனி ஒழுக்கம் தருகிறது'
            })

        # 4. Mercury strength (intelligence)
        mercury_data = self.planets.get('Mercury', {})
        mercury_dignity = mercury_data.get('dignity', 'neutral')
        mercury_house = mercury_data.get('house', 1)

        if mercury_dignity in ['exalted', 'own', 'mooltrikona']:
            outcome_score += 7
            positive_count += 1
            outcome_factors.append({
                'factor': 'Mercury Intelligence',
                'contribution': 7,
                'type': 'wisdom',
                'description_en': 'Strong Mercury brings communication skills',
                'description_ta': 'வலுவான புதன் புத்திசாலித்தனம் தருகிறது'
            })
        elif mercury_house in [1, 2, 4, 5, 7, 10, 11]:
            outcome_score += 4
            positive_count += 1

        # 5. Benefic dasha lord
        if dasha_lord in self.BENEFIC_OUTCOME_PLANETS:
            outcome_score += 10
            positive_count += 1
            outcome_factors.append({
                'factor': f'{dasha_lord} Period',
                'contribution': 10,
                'type': 'favorable_period',
                'description_en': f'{dasha_lord} period supports positive outcomes',
                'description_ta': f'{dasha_lord} காலம் நல்ல பலன்கள்'
            })

        # 6. Yoga activation bonus
        yoga_module = modules.get('yoga_dosha', {})
        yoga_score = yoga_module.get('normalized', 0.5)
        if yoga_score > 0.55:  # V7.0.2: Lower threshold
            yoga_bonus = (yoga_score - 0.5) * 35  # V7.0.2: Higher multiplier
            outcome_score += yoga_bonus
            positive_count += 1
            outcome_factors.append({
                'factor': 'Yoga Activation',
                'contribution': round(yoga_bonus, 1),
                'type': 'special_combination',
                'description_en': 'Auspicious yoga combination active',
                'description_ta': 'சுப யோகம் செயல்படுகிறது'
            })

        # 7. V7.0.2: House module boost
        house_module = modules.get('house_power', {})
        house_score = house_module.get('normalized', 0.5)
        if house_score > 0.55:
            house_bonus = (house_score - 0.5) * 20
            outcome_score += house_bonus

        # 8. Apply dampeners instead of penalties for malefics
        # V7.0.2: Malefics only slightly dampen, they don't block
        dampener = 1.0
        if dasha_lord in self.PRESSURE_PLANETS:
            dampener *= self.PRESSURE_OUTCOME_CONFIG['penalty_to_dampener'].get(dasha_lord, 0.95)

        # Apply dampener (only to the gains above baseline)
        base = 55
        outcome_score = base + (outcome_score - base) * dampener

        # 9. Apply positive compound multiplier
        compound_multiplier = 1.0
        if positive_count >= 2:
            compound_multiplier = self.PRESSURE_OUTCOME_CONFIG['positive_compound'].get(
                min(positive_count, 4), 1.0
            )
            outcome_score = base + (outcome_score - base) * compound_multiplier

        return {
            'outcome_score': round(max(0, min(100, outcome_score)), 1),
            'outcome_factors': outcome_factors[:3],  # Top 3 factors
            'positive_count': positive_count,
            'compound_multiplier': round(compound_multiplier, 2),
            'dampener_applied': round(dampener, 2)
        }

    def _apply_dignity_floor_v70(self, raw_score: float) -> float:
        """
        V7.0: Apply dignity floor - no score below 45%

        Philosophy: Everyone has inherent dignity and potential.
        Even in the most challenging periods, there is always hope and opportunity.
        """
        dignity_floor = self.GLOBAL_NUMERIC_SAFETY.get('dignity_floor', 45)
        return max(raw_score, dignity_floor)

    def _get_phase_label_v70(self, pressure_score: float, outcome_score: float, lang: str = 'en') -> Dict:
        """
        V7.0: Get appropriate phase label based on pressure and outcome

        High pressure + good outcome = "Effort Phase" (working hard but succeeding)
        Low pressure + good outcome = "Flow Phase" (easy success)
        High pressure + neutral outcome = "Building Phase" (effort now, reward later)
        """
        labels = self.PHASE_LABELS.get(lang, self.PHASE_LABELS['en'])

        if pressure_score >= 20:
            if outcome_score >= 60:
                phase_key = 'high_pressure_neutral_outcome'  # Effort but rewarded
                phase_description = 'High effort leading to growth' if lang == 'en' else 'அதிக முயற்சி வளர்ச்சிக்கு'
            else:
                phase_key = 'high_pressure_negative_outcome'  # Challenge phase
                phase_description = 'Building foundation for future' if lang == 'en' else 'எதிர்காலத்திற்கு அடித்தளம்'
        elif outcome_score >= 65:
            phase_key = 'low_pressure_positive_outcome'  # Flow state
            phase_description = 'Natural momentum and ease' if lang == 'en' else 'இயல்பான வேகம்'
        elif outcome_score >= 55:
            phase_key = 'neutral_pressure_positive_outcome'  # Growth phase
            phase_description = 'Steady progress and growth' if lang == 'en' else 'நிலையான வளர்ச்சி'
        else:
            phase_key = 'neutral'  # Steady phase
            phase_description = 'Stable period for planning' if lang == 'en' else 'திட்டமிடும் காலம்'

        return {
            'phase_key': phase_key,
            'phase_label': labels.get(phase_key, 'Steady Phase'),
            'phase_description': phase_description
        }

    def _get_balanced_factors_v70(self, pressure_result: Dict, outcome_result: Dict) -> Dict:
        """
        V7.0: Show 2 positives + 1 challenge (balanced perspective)

        Never show only negatives. Always lead with positives.
        """
        positives = []
        challenges = []

        # Collect positive outcome factors
        for factor in outcome_result.get('outcome_factors', []):
            positives.append({
                'text_en': factor.get('description_en', ''),
                'text_ta': factor.get('description_ta', ''),
                'type': factor.get('type', 'positive'),
                'contribution': factor.get('contribution', 0)
            })

        # Collect challenge factors (reworded)
        for factor in pressure_result.get('pressure_factors', []):
            challenges.append({
                'text_en': factor.get('description_en', '').replace('difficult', 'effort').replace('bad', 'building'),
                'text_ta': factor.get('description_ta', ''),
                'type': 'effort_required',
                'contribution': factor.get('contribution', 0)
            })

        # Sort by contribution
        positives.sort(key=lambda x: x['contribution'], reverse=True)
        challenges.sort(key=lambda x: x['contribution'], reverse=True)

        return {
            'positives': positives[:2],  # Top 2 positives
            'challenge': challenges[0] if challenges else None,  # 1 challenge (may be None)
            'balance_ratio': '2:1'  # V7.0 ratio
        }

    # ==================== MONTH-WISE CALCULATION ====================

    def calculate_monthly_projections_v41(
        self,
        year: int,
        life_area: str = 'general',
        dasha_lord: str = None,
        bhukti_lord: str = None
    ) -> Dict:
        """
        v4.1 Month-wise calculation with POI/HAI recomputation per month.

        Rules applied:
        - Split transits into 30-day arcs
        - Recompute POI and HAI per month
        - Apply monthly smoothing (score ^ 0.92)
        - Navamsa multipliers constant
        - Yogas static but strength varies by transit support
        """
        # Set month-wise mode
        self.set_time_mode(TimeMode.MONTH_WISE)

        monthly_results = []
        all_scores = []

        for month in range(1, 13):
            target_date = date(year, month, 15)  # Mid-month

            # Clear caches for fresh calculation
            self.poi_cache = {}
            self.hai_cache = {}

            # Calculate prediction for this month
            month_result = self.calculate_prediction_v41(
                target_date=target_date,
                life_area=life_area,
                mode_hint='monthly',
                dasha_lord=dasha_lord,
                bhukti_lord=bhukti_lord
            )

            # Apply monthly smoothing
            raw_score = month_result['final_score']
            smoothing_power = self.active_multipliers.get('monthly_smoothing_power', 0.92)
            smoothed_score = math.pow(raw_score / 100, smoothing_power) * 100

            all_scores.append(smoothed_score)

            monthly_results.append({
                'month': month,
                'month_name': self._get_month_name(month),
                'date': target_date.isoformat(),
                'raw_score': round(raw_score, 1),
                'smoothed_score': round(smoothed_score, 1),
                'module_scores': month_result['module_normalized_scores'],
                'confidence': month_result['confidence']['score'],
                'top_factors': month_result['top_positive_drivers'][:2]
            })

        # Calculate summary
        avg_score = sum(all_scores) / len(all_scores) if all_scores else 50
        peak_idx = all_scores.index(max(all_scores))
        worst_idx = all_scores.index(min(all_scores))

        return {
            'year': year,
            'life_area': life_area,
            'time_mode': 'month_wise',
            'monthly': monthly_results,
            'summary': {
                'average_score': round(avg_score, 1),
                'peak_month': {
                    'month': peak_idx + 1,
                    'name': self._get_month_name(peak_idx + 1),
                    'score': round(all_scores[peak_idx], 1)
                },
                'worst_month': {
                    'month': worst_idx + 1,
                    'name': self._get_month_name(worst_idx + 1),
                    'score': round(all_scores[worst_idx], 1)
                },
                'smoothing_applied': True,
                'smoothing_power': smoothing_power
            },
            'dasha_info': {
                'mahadasha_lord': dasha_lord,
                'bhukti_lord': bhukti_lord
            },
            'engine_version': self.ENGINE_VERSION
        }

    def _get_month_name(self, month: int, lang: str = 'ta') -> str:
        """Get month name"""
        tamil_months = ['ஜனவரி', 'பிப்ரவரி', 'மார்ச்', 'ஏப்ரல்', 'மே', 'ஜூன்',
                       'ஜூலை', 'ஆகஸ்ட்', 'செப்டம்பர்', 'அக்டோபர்', 'நவம்பர்', 'டிசம்பர்']
        return tamil_months[month - 1] if 1 <= month <= 12 else str(month)

    # ==================== YEAR OVERLAY (VARSHAPHAL) ====================

    def calculate_yearly_projection_v41(
        self,
        year: int,
        life_area: str = 'general',
        dasha_lord: str = None
    ) -> Dict:
        """
        v4.1 Yearly projection with Varshaphal integration.

        Rules applied:
        - Add VarshaphalInteractionScore to PlanetPower module
        - Reduce Transit module weight by 25%
        - Add year_trend_multiplier = Varshaphal_POI × 0.01
        """
        # Set year overlay mode
        self.set_time_mode(TimeMode.YEAR_OVERLAY)

        # Calculate for January 1st of the year
        target_date = date(year, 1, 1)

        # Calculate Varshaphal chart influence
        varshaphal_data = self._calculate_varshaphal_chart(year)

        # Calculate main prediction
        result = self.calculate_prediction_v41(
            target_date=target_date,
            life_area=life_area,
            mode_hint='yearly',
            dasha_lord=dasha_lord
        )

        # Add Varshaphal data to result
        result['varshaphal'] = varshaphal_data
        result['year'] = year

        return result

    def _calculate_varshaphal_chart(self, year: int) -> Dict:
        """Calculate Varshaphal (Solar Return) chart data"""
        birth_date = self._get_birth_date()
        age = year - birth_date.year

        # Muntha calculation
        muntha_sign_num = (self.lagna_num + age) % 12
        muntha_sign = ['மேஷம்', 'ரிஷபம்', 'மிதுனம்', 'கடகம்', 'சிம்மம்', 'கன்னி',
                      'துலாம்', 'விருச்சிகம்', 'தனுசு', 'மகரம்', 'கும்பம்', 'மீனம்'][muntha_sign_num]

        # Year lord (based on weekday of birthday in that year)
        solar_return_date = date(year, birth_date.month, birth_date.day)
        weekday = solar_return_date.weekday()
        year_lords = ['Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Sun']
        year_lord = year_lords[weekday]

        # Calculate Varshaphal POI
        varshaphal_poi = self._calculate_varshaphal_poi(solar_return_date)

        return {
            'year': year,
            'age': age,
            'muntha': {
                'sign': muntha_sign,
                'sign_num': muntha_sign_num + 1,
                'is_favorable': muntha_sign_num in [0, 4, 8]  # Trines from Lagna
            },
            'year_lord': year_lord,
            'year_lord_poi': self.calculate_poi(year_lord, solar_return_date)['poi'],
            'varshaphal_poi': round(varshaphal_poi, 2),
            'solar_return_date': solar_return_date.isoformat()
        }
