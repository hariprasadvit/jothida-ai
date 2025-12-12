/**
 * Deep Astrology Scoring Engine for Ungal Jothidan
 * Version 2.0
 *
 * This engine provides sophisticated astrological calculations using:
 * - HAI: House Activation Index (12 houses)
 * - POI: Planet Operating Intensity (Sun through Ketu)
 * - NES: Nakshatra Emotional Score
 * - DashaComposite: Weighted blend of Maha, Bhukti, Antara with transit and dignity
 */

// ============================================================================
// CONSTANTS AND MAPPINGS
// ============================================================================

// Planet indices for consistent referencing
const PLANETS = {
  Sun: 0, Moon: 1, Mars: 2, Mercury: 3, Jupiter: 4,
  Venus: 5, Saturn: 6, Rahu: 7, Ketu: 8
};

// Planet dignities (base strength 0-100)
const PLANET_DIGNITIES = {
  Sun: { exalted: 'மேஷம்', debilitated: 'துலாம்', ownSigns: ['சிம்மம்'] },
  Moon: { exalted: 'ரிஷபம்', debilitated: 'விருச்சிகம்', ownSigns: ['கடகம்'] },
  Mars: { exalted: 'மகரம்', debilitated: 'கடகம்', ownSigns: ['மேஷம்', 'விருச்சிகம்'] },
  Mercury: { exalted: 'கன்னி', debilitated: 'மீனம்', ownSigns: ['மிதுனம்', 'கன்னி'] },
  Jupiter: { exalted: 'கடகம்', debilitated: 'மகரம்', ownSigns: ['தனுசு', 'மீனம்'] },
  Venus: { exalted: 'மீனம்', debilitated: 'கன்னி', ownSigns: ['ரிஷபம்', 'துலாம்'] },
  Saturn: { exalted: 'துலாம்', debilitated: 'மேஷம்', ownSigns: ['மகரம்', 'கும்பம்'] },
  Rahu: { exalted: 'மிதுனம்', debilitated: 'தனுசு', ownSigns: [] },
  Ketu: { exalted: 'தனுசு', debilitated: 'மிதுனம்', ownSigns: [] },
};

// House rulers by rasi (Moon sign)
const HOUSE_RULERS = {
  'மேஷம்': ['Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter'],
  'ரிஷபம்': ['Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter', 'Mars'],
  'மிதுனம்': ['Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter', 'Mars', 'Venus'],
  'கடகம்': ['Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter', 'Mars', 'Venus', 'Mercury'],
  'சிம்மம்': ['Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter', 'Mars', 'Venus', 'Mercury', 'Moon'],
  'கன்னி': ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter', 'Mars', 'Venus', 'Mercury', 'Moon', 'Sun'],
  'துலாம்': ['Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter', 'Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury'],
  'விருச்சிகம்': ['Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter', 'Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus'],
  'தனுசு': ['Jupiter', 'Saturn', 'Saturn', 'Jupiter', 'Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars'],
  'மகரம்': ['Saturn', 'Saturn', 'Jupiter', 'Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter'],
  'கும்பம்': ['Saturn', 'Jupiter', 'Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn'],
  'மீனம்': ['Jupiter', 'Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn'],
};

// Nakshatra data with element, guna, and deity
const NAKSHATRA_DATA = {
  'அஸ்வினி': { lord: 'Ketu', element: 'fire', guna: 'rajas', deity: 'Ashwini Kumaras', emotionalBase: 75 },
  'பரணி': { lord: 'Venus', element: 'earth', guna: 'rajas', deity: 'Yama', emotionalBase: 65 },
  'கார்த்திகை': { lord: 'Sun', element: 'fire', guna: 'rajas', deity: 'Agni', emotionalBase: 70 },
  'ரோகிணி': { lord: 'Moon', element: 'earth', guna: 'rajas', deity: 'Brahma', emotionalBase: 85 },
  'மிருகசீரிடம்': { lord: 'Mars', element: 'earth', guna: 'tamas', deity: 'Soma', emotionalBase: 72 },
  'திருவாதிரை': { lord: 'Rahu', element: 'water', guna: 'tamas', deity: 'Rudra', emotionalBase: 58 },
  'புனர்பூசம்': { lord: 'Jupiter', element: 'water', guna: 'sattva', deity: 'Aditi', emotionalBase: 80 },
  'பூசம்': { lord: 'Saturn', element: 'water', guna: 'tamas', deity: 'Brihaspati', emotionalBase: 78 },
  'ஆயில்யம்': { lord: 'Mercury', element: 'water', guna: 'sattva', deity: 'Sarpa', emotionalBase: 62 },
  'மகம்': { lord: 'Ketu', element: 'fire', guna: 'tamas', deity: 'Pitris', emotionalBase: 70 },
  'பூரம்': { lord: 'Venus', element: 'fire', guna: 'rajas', deity: 'Bhaga', emotionalBase: 82 },
  'உத்திரம்': { lord: 'Sun', element: 'fire', guna: 'rajas', deity: 'Aryaman', emotionalBase: 76 },
  'ஹஸ்தம்': { lord: 'Moon', element: 'earth', guna: 'rajas', deity: 'Savitar', emotionalBase: 74 },
  'சித்திரை': { lord: 'Mars', element: 'fire', guna: 'tamas', deity: 'Tvashtar', emotionalBase: 68 },
  'சுவாதி': { lord: 'Rahu', element: 'air', guna: 'tamas', deity: 'Vayu', emotionalBase: 72 },
  'விசாகம்': { lord: 'Jupiter', element: 'fire', guna: 'sattva', deity: 'Indra-Agni', emotionalBase: 75 },
  'அனுஷம்': { lord: 'Saturn', element: 'fire', guna: 'tamas', deity: 'Mitra', emotionalBase: 70 },
  'கேட்டை': { lord: 'Mercury', element: 'air', guna: 'sattva', deity: 'Indra', emotionalBase: 65 },
  'மூலம்': { lord: 'Ketu', element: 'air', guna: 'tamas', deity: 'Nirriti', emotionalBase: 55 },
  'பூராடம்': { lord: 'Venus', element: 'water', guna: 'rajas', deity: 'Apas', emotionalBase: 78 },
  'உத்திராடம்': { lord: 'Sun', element: 'earth', guna: 'rajas', deity: 'Vishvadevas', emotionalBase: 80 },
  'திருவோணம்': { lord: 'Moon', element: 'air', guna: 'rajas', deity: 'Vishnu', emotionalBase: 85 },
  'அவிட்டம்': { lord: 'Mars', element: 'earth', guna: 'tamas', deity: 'Vasus', emotionalBase: 72 },
  'சதயம்': { lord: 'Rahu', element: 'air', guna: 'tamas', deity: 'Varuna', emotionalBase: 68 },
  'பூரட்டாதி': { lord: 'Jupiter', element: 'air', guna: 'sattva', deity: 'Aja Ekapada', emotionalBase: 70 },
  'உத்திரட்டாதி': { lord: 'Saturn', element: 'water', guna: 'tamas', deity: 'Ahir Budhnya', emotionalBase: 75 },
  'ரேவதி': { lord: 'Mercury', element: 'water', guna: 'sattva', deity: 'Pushan', emotionalBase: 82 },
};

// Rasi index mapping
const RASI_INDEX = {
  'மேஷம்': 0, 'ரிஷபம்': 1, 'மிதுனம்': 2, 'கடகம்': 3,
  'சிம்மம்': 4, 'கன்னி': 5, 'துலாம்': 6, 'விருச்சிகம்': 7,
  'தனுசு': 8, 'மகரம்': 9, 'கும்பம்': 10, 'மீனம்': 11,
};

// Nakshatra index for hash calculation
const NAKSHATRA_INDEX = {
  'அஸ்வினி': 0, 'பரணி': 1, 'கார்த்திகை': 2, 'ரோகிணி': 3,
  'மிருகசீரிடம்': 4, 'திருவாதிரை': 5, 'புனர்பூசம்': 6, 'பூசம்': 7,
  'ஆயில்யம்': 8, 'மகம்': 9, 'பூரம்': 10, 'உத்திரம்': 11,
  'ஹஸ்தம்': 12, 'சித்திரை': 13, 'சுவாதி': 14, 'விசாகம்': 15,
  'அனுஷம்': 16, 'கேட்டை': 17, 'மூலம்': 18, 'பூராடம்': 19,
  'உத்திராடம்': 20, 'திருவோணம்': 21, 'அவிட்டம்': 22, 'சதயம்': 23,
  'பூரட்டாதி': 24, 'உத்திரட்டாதி': 25, 'ரேவதி': 26,
};

// Day of week to planet ruler
const DAY_PLANET = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'];

// Hora table (planetary hours)
const HORA_SEQUENCE = ['Sun', 'Venus', 'Mercury', 'Moon', 'Saturn', 'Jupiter', 'Mars'];

// Planet colors for color suggestion
const PLANET_COLORS = {
  Sun: ['Orange', 'Red', 'Gold'],
  Moon: ['White', 'Silver', 'Cream'],
  Mars: ['Red', 'Maroon', 'Coral'],
  Mercury: ['Green', 'Light Green', 'Emerald'],
  Jupiter: ['Yellow', 'Gold', 'Saffron'],
  Venus: ['White', 'Pink', 'Light Blue'],
  Saturn: ['Blue', 'Black', 'Dark Blue'],
  Rahu: ['Blue', 'Grey', 'Smoky'],
  Ketu: ['Grey', 'Brown', 'Orange'],
};

// Planet directions
const PLANET_DIRECTIONS = {
  Sun: 'East',
  Moon: 'Northwest',
  Mars: 'South',
  Mercury: 'North',
  Jupiter: 'Northeast',
  Venus: 'Southeast',
  Saturn: 'West',
  Rahu: 'Southwest',
  Ketu: 'Southwest',
};

// ============================================================================
// CORE ENGINE FUNCTIONS
// ============================================================================

/**
 * Calculate House Activation Index (HAI) for all 12 houses
 * @param {Object} userProfile - User profile with rasi, nakshatra
 * @param {Object} transits - Transit data from API
 * @param {number} dayOfWeek - Day of week (0-6)
 * @returns {Array} HAI values for houses 1-12
 */
export function calculateHAI(userProfile, transits, dayOfWeek) {
  const rasi = userProfile?.rasi || 'மேஷம்';
  const hai = new Array(12).fill(50); // Base activation

  // Get house rulers for this rasi
  const rulers = HOUSE_RULERS[rasi] || HOUSE_RULERS['மேஷம்'];

  // Day planet bonus (ruler of the day activates related houses)
  const dayPlanet = DAY_PLANET[dayOfWeek];
  rulers.forEach((ruler, houseIndex) => {
    if (ruler === dayPlanet) {
      hai[houseIndex] += 15;
    }
  });

  // Transit influence on houses
  if (transits?.planet_positions) {
    Object.entries(transits.planet_positions).forEach(([planet, position]) => {
      const houseNum = position?.house;
      if (houseNum >= 1 && houseNum <= 12) {
        const isBenefic = ['Jupiter', 'Venus', 'Mercury', 'Moon'].includes(planet);
        hai[houseNum - 1] += isBenefic ? 12 : -8;
      }
    });
  }

  // Benefic/malefic intensity modulation
  if (transits?.benefic_index) {
    hai[1] += transits.benefic_index * 0.15; // 2nd house (wealth)
    hai[10] += transits.benefic_index * 0.15; // 11th house (gains)
  }

  // Clamp values to 0-100
  return hai.map(v => Math.max(0, Math.min(100, Math.round(v))));
}

/**
 * Calculate Planet Operating Intensity (POI) for all planets
 * @param {Object} userProfile - User profile
 * @param {Object} transits - Transit data
 * @param {Object} projections - Projections data with dasha info
 * @param {number} dayOfWeek - Day of week
 * @returns {Object} POI values for each planet
 */
export function calculatePOI(userProfile, transits, projections, dayOfWeek) {
  const poi = {};
  const dayPlanet = DAY_PLANET[dayOfWeek];
  const rasi = userProfile?.rasi || 'மேஷம்';

  Object.keys(PLANETS).forEach(planet => {
    let intensity = 50; // Base intensity

    // Day ruler bonus
    if (planet === dayPlanet) {
      intensity += 20;
    }

    // Dignity calculation
    const dignity = PLANET_DIGNITIES[planet];
    if (dignity) {
      if (dignity.exalted === rasi) {
        intensity += 25;
      } else if (dignity.debilitated === rasi) {
        intensity -= 20;
      } else if (dignity.ownSigns.includes(rasi)) {
        intensity += 15;
      }
    }

    // Current dasha lord bonus
    const dashaLord = projections?.current_dasha?.lord;
    if (dashaLord === planet) {
      intensity += 18;
    }

    // Transit influence
    if (transits?.overall_intensity) {
      const isBenefic = ['Jupiter', 'Venus', 'Mercury'].includes(planet);
      if (isBenefic) {
        intensity += (transits.benefic_index || 50) * 0.1;
      } else if (['Mars', 'Saturn', 'Rahu', 'Ketu'].includes(planet)) {
        intensity += (transits.malefic_intensity || 30) * 0.08;
      }
    }

    poi[planet] = Math.max(0, Math.min(100, Math.round(intensity)));
  });

  return poi;
}

/**
 * Calculate Nakshatra Emotional Score (NES)
 * @param {Object} userProfile - User profile with nakshatra
 * @param {number} dayOfWeek - Day of week
 * @returns {number} NES value 0-100
 */
export function calculateNES(userProfile, dayOfWeek) {
  const nakshatra = userProfile?.nakshatra || 'அஸ்வினி';
  const nakshatraInfo = NAKSHATRA_DATA[nakshatra] || NAKSHATRA_DATA['அஸ்வினி'];

  let nes = nakshatraInfo.emotionalBase;

  // Day lord compatibility
  const dayPlanet = DAY_PLANET[dayOfWeek];
  if (nakshatraInfo.lord === dayPlanet) {
    nes += 15;
  }

  // Guna influence
  if (nakshatraInfo.guna === 'sattva') {
    nes += 8;
  } else if (nakshatraInfo.guna === 'tamas') {
    nes -= 5;
  }

  // Element cycle bonus (fire->air->water->earth)
  const elementBonus = {
    fire: [0, 3, 6], // Sunday, Wednesday, Saturday
    air: [1, 4], // Monday, Thursday
    water: [2, 5], // Tuesday, Friday
    earth: [0, 2, 4, 6], // Multiple days
  };
  if (elementBonus[nakshatraInfo.element]?.includes(dayOfWeek)) {
    nes += 10;
  }

  return Math.max(0, Math.min(100, Math.round(nes)));
}

/**
 * Calculate Dasha Composite Score
 * @param {Object} projections - Projections data with dasha info
 * @param {Object} poi - Planet Operating Intensity
 * @param {number} dayOfWeek - Day of week
 * @returns {Object} Dasha composite scores
 */
export function calculateDashaComposite(projections, poi, dayOfWeek) {
  const dashaLord = projections?.current_dasha?.lord || 'Venus';
  const dashaStrength = projections?.current_dasha?.strength || 70;

  // Base composite from dasha strength
  let composite = dashaStrength * 0.6;

  // POI of dasha lord
  composite += (poi[dashaLord] || 50) * 0.25;

  // Day compatibility
  const dayPlanet = DAY_PLANET[dayOfWeek];
  if (dashaLord === dayPlanet) {
    composite += 15;
  }

  // Sub-period influence (simplified)
  composite = Math.max(30, Math.min(95, composite));

  return {
    overall: Math.round(composite),
    finance: Math.round(composite * (dashaLord === 'Jupiter' || dashaLord === 'Venus' ? 1.15 : 0.95)),
    career: Math.round(composite * (dashaLord === 'Sun' || dashaLord === 'Mercury' ? 1.15 : 0.95)),
    relationship: Math.round(composite * (dashaLord === 'Venus' || dashaLord === 'Moon' ? 1.15 : 0.95)),
    health: Math.round(composite * (dashaLord === 'Mars' || dashaLord === 'Saturn' ? 0.9 : 1.05)),
    tension: Math.round(100 - composite), // Inverse for risk calculation
  };
}

/**
 * Calculate Moon Phase Stability
 * @param {number} dayOfMonth - Day of month (1-30)
 * @returns {number} Stability score 0-100
 */
export function calculateMoonPhaseStability(dayOfMonth) {
  // Full moon (15) and new moon (30/1) are most intense
  // Waxing (1-14) generally positive, waning (16-29) more introspective
  const lunarDay = dayOfMonth % 30 || 30;

  if (lunarDay === 15) {
    return 60; // Full moon - high energy but less stable
  } else if (lunarDay === 30 || lunarDay === 1) {
    return 55; // New moon - low energy
  } else if (lunarDay >= 7 && lunarDay <= 13) {
    return 85; // Waxing phase - stable growth
  } else if (lunarDay >= 2 && lunarDay <= 6) {
    return 75; // Early waxing
  } else if (lunarDay >= 16 && lunarDay <= 22) {
    return 70; // Early waning
  } else {
    return 65; // Late waning
  }
}

/**
 * Get current Hora (planetary hour)
 * @param {number} hour - Current hour (0-23)
 * @param {number} dayOfWeek - Day of week
 * @returns {Object} Current hora info
 */
export function getCurrentHora(hour, dayOfWeek) {
  const dayPlanet = DAY_PLANET[dayOfWeek];
  const startIndex = HORA_SEQUENCE.indexOf(dayPlanet);

  // Each hora is approximately 1 hour (simplified)
  // Sunrise assumed at 6 AM
  const horaIndex = (hour - 6 + 24) % 24;
  const planetIndex = (startIndex + horaIndex) % 7;
  const horaPlanet = HORA_SEQUENCE[planetIndex];

  const isBenefic = ['Jupiter', 'Venus', 'Mercury', 'Moon'].includes(horaPlanet);

  return {
    planet: horaPlanet,
    isBenefic,
    intensity: isBenefic ? 75 : 55,
  };
}

/**
 * Get Rahu Kalam timings
 * @param {number} dayOfWeek - Day of week (0-6)
 * @returns {Object} Rahu Kalam start and end times
 */
export function getRahuKalam(dayOfWeek) {
  const times = [
    { start: '16:30', end: '18:00' }, // Sunday
    { start: '07:30', end: '09:00' }, // Monday
    { start: '15:00', end: '16:30' }, // Tuesday
    { start: '12:00', end: '13:30' }, // Wednesday
    { start: '13:30', end: '15:00' }, // Thursday
    { start: '10:30', end: '12:00' }, // Friday
    { start: '09:00', end: '10:30' }, // Saturday
  ];
  return times[dayOfWeek] || times[0];
}

/**
 * Get Yama Kandam timings
 * @param {number} dayOfWeek - Day of week (0-6)
 * @returns {Object} Yama Kandam start and end times
 */
export function getYamaKandam(dayOfWeek) {
  const times = [
    { start: '12:00', end: '13:30' }, // Sunday
    { start: '10:30', end: '12:00' }, // Monday
    { start: '09:00', end: '10:30' }, // Tuesday
    { start: '07:30', end: '09:00' }, // Wednesday
    { start: '06:00', end: '07:30' }, // Thursday
    { start: '15:00', end: '16:30' }, // Friday
    { start: '13:30', end: '15:00' }, // Saturday
  ];
  return times[dayOfWeek] || times[0];
}

// ============================================================================
// CARD SCORE CALCULATORS
// ============================================================================

/**
 * Calculate Dasha Mood Score
 * Formula: 0.45 * DashaComposite + 0.25 * POI[dashaLord] + 0.15 * HAI[house] + 0.15 * NES
 */
export function calculateDashaMoodScore(dashaComposite, poi, hai, nes, dashaLord, rasi) {
  const rulers = HOUSE_RULERS[rasi] || HOUSE_RULERS['மேஷம்'];
  const dashaHouse = rulers.indexOf(dashaLord);
  const houseScore = dashaHouse >= 0 ? hai[dashaHouse] : 50;

  const score = (
    0.45 * dashaComposite.overall +
    0.25 * (poi[dashaLord] || 50) +
    0.15 * houseScore +
    0.15 * nes
  );

  return Math.round(Math.max(30, Math.min(95, score)));
}

/**
 * Calculate Transit Pressure Score
 * Formula: 0.40 * (100 - overall_intensity) + 0.30 * benefic_index + 0.20 * NES + 0.10 * moon_phase
 */
export function calculateTransitPressureScore(transits, nes, moonPhaseStability) {
  const overallIntensity = transits?.overall_intensity || 50;
  const beneficIndex = transits?.benefic_index || 50;

  const score = (
    0.40 * (100 - overallIntensity) +
    0.30 * beneficIndex +
    0.20 * nes +
    0.10 * moonPhaseStability
  );

  return Math.round(Math.max(30, Math.min(90, score)));
}

/**
 * Calculate Finance Score
 * Formula: 0.35 * HAI[2] + 0.25 * HAI[11] + 0.15 * POI[Jupiter] + 0.10 * POI[Venus] + 0.15 * DashaComposite_finance
 */
export function calculateFinanceScore(hai, poi, dashaComposite, lifeAreasScore) {
  // Blend API score with engine calculation
  const engineScore = (
    0.35 * hai[1] + // 2nd house (0-indexed)
    0.25 * hai[10] + // 11th house (0-indexed)
    0.15 * (poi.Jupiter || 50) +
    0.10 * (poi.Venus || 50) +
    0.15 * dashaComposite.finance
  );

  // Blend with API score if available
  const finalScore = lifeAreasScore
    ? (engineScore * 0.6 + lifeAreasScore * 0.4)
    : engineScore;

  return Math.round(Math.max(35, Math.min(92, finalScore)));
}

/**
 * Calculate Career Score
 * Formula: 0.40 * HAI[10] + 0.25 * POI[Mercury] + 0.15 * POI[Sun] + 0.10 * transit + 0.10 * DashaComposite_career
 */
export function calculateCareerScore(hai, poi, dashaComposite, transits, lifeAreasScore) {
  const transitTo10th = transits?.house_transits?.[10]?.score || 50;

  const engineScore = (
    0.40 * hai[9] + // 10th house (0-indexed)
    0.25 * (poi.Mercury || 50) +
    0.15 * (poi.Sun || 50) +
    0.10 * transitTo10th +
    0.10 * dashaComposite.career
  );

  const finalScore = lifeAreasScore
    ? (engineScore * 0.6 + lifeAreasScore * 0.4)
    : engineScore;

  return Math.round(Math.max(35, Math.min(92, finalScore)));
}

/**
 * Calculate Relationship Score
 * Formula: 0.35 * HAI[7] + 0.25 * HAI[5] + 0.20 * POI[Venus] + 0.10 * POI[Moon] + 0.10 * NES
 */
export function calculateRelationshipScore(hai, poi, nes, lifeAreasScore) {
  const engineScore = (
    0.35 * hai[6] + // 7th house (0-indexed)
    0.25 * hai[4] + // 5th house (0-indexed)
    0.20 * (poi.Venus || 50) +
    0.10 * (poi.Moon || 50) +
    0.10 * nes
  );

  const finalScore = lifeAreasScore
    ? (engineScore * 0.6 + lifeAreasScore * 0.4)
    : engineScore;

  return Math.round(Math.max(35, Math.min(92, finalScore)));
}

/**
 * Calculate Health Score
 * Formula: 0.30 * HAI[1] + 0.25 * HAI[6] + 0.20 * POI[Saturn] + 0.15 * POI[Mars] + 0.10 * moon_phase
 */
export function calculateHealthScore(hai, poi, moonPhaseStability, lifeAreasScore) {
  // Invert Saturn and Mars influence (lower malefic = better health)
  const saturnHealth = 100 - (poi.Saturn || 50);
  const marsHealth = 100 - (poi.Mars || 50);

  const engineScore = (
    0.30 * hai[0] + // 1st house (0-indexed) - body
    0.25 * hai[5] + // 6th house (0-indexed) - health/disease
    0.20 * saturnHealth * 0.5 + 25 + // Normalize
    0.15 * marsHealth * 0.5 + 25 + // Normalize
    0.10 * moonPhaseStability
  );

  const finalScore = lifeAreasScore
    ? (engineScore * 0.5 + lifeAreasScore * 0.5)
    : engineScore;

  return Math.round(Math.max(40, Math.min(90, finalScore)));
}

/**
 * Calculate Lucky Window
 * Returns best time slots based on benefic hora and nakshatra flow
 */
export function calculateLuckyWindow(userProfile, poi, dayOfWeek) {
  const hora8 = getCurrentHora(8, dayOfWeek);
  const hora10 = getCurrentHora(10, dayOfWeek);
  const hora14 = getCurrentHora(14, dayOfWeek);
  const hora17 = getCurrentHora(17, dayOfWeek);

  // Find best benefic hora
  const horas = [
    { time: '08:00 - 10:00', hora: hora8, score: hora8.isBenefic ? 85 : 55 },
    { time: '10:00 - 12:00', hora: hora10, score: hora10.isBenefic ? 85 : 55 },
    { time: '14:00 - 16:00', hora: hora14, score: hora14.isBenefic ? 80 : 50 },
    { time: '17:00 - 19:00', hora: hora17, score: hora17.isBenefic ? 75 : 45 },
  ];

  // Boost if hora planet matches user's nakshatra lord
  const nakshatraInfo = NAKSHATRA_DATA[userProfile?.nakshatra] || NAKSHATRA_DATA['அஸ்வினி'];
  horas.forEach(h => {
    if (h.hora.planet === nakshatraInfo.lord) {
      h.score += 10;
    }
    // Add POI influence
    h.score += (poi[h.hora.planet] || 50) * 0.1;
  });

  // Sort and get best
  horas.sort((a, b) => b.score - a.score);
  const bestSlot = horas[0];

  return {
    start: bestSlot.time.split(' - ')[0],
    end: bestSlot.time.split(' - ')[1],
    score: Math.round(Math.min(92, bestSlot.score)),
    planet: bestSlot.hora.planet,
  };
}

/**
 * Calculate Avoid Window
 * Returns worst time slots (Rahu Kalam, Yama Kandam)
 */
export function calculateAvoidWindow(dayOfWeek) {
  const rahuKalam = getRahuKalam(dayOfWeek);
  const yamaKandam = getYamaKandam(dayOfWeek);

  return {
    rahuKalam,
    yamaKandam,
    score: 40, // Low score indicating caution
  };
}

/**
 * Calculate Opportunity Indicator
 * Based on highest positive delta from life areas
 */
export function calculateOpportunityScore(scores) {
  const { finance, career, relationship, health } = scores;
  const allScores = [
    { area: 'finance', score: finance },
    { area: 'career', score: career },
    { area: 'relationship', score: relationship },
    { area: 'health', score: health },
  ];

  const best = allScores.sort((a, b) => b.score - a.score)[0];

  return {
    area: best.area,
    score: Math.round(Math.min(95, best.score + 5)), // Slight boost for opportunity
  };
}

/**
 * Calculate Risk Alert Score
 * Based on lowest area score and malefic intensity
 */
export function calculateRiskScore(scores, transits, poi, dashaComposite) {
  const { finance, career, relationship, health } = scores;
  const allScores = [
    { area: 'finance', score: finance },
    { area: 'career', score: career },
    { area: 'relationship', score: relationship },
    { area: 'health', score: health },
  ];

  const worst = allScores.sort((a, b) => a.score - b.score)[0];

  // Malefic influence
  const maleficFactor = (
    (poi.Mars || 50) +
    (poi.Saturn || 50) +
    (poi.Rahu || 50)
  ) / 300;

  const riskIntensity = (
    (100 - worst.score) * 0.5 +
    (transits?.malefic_intensity || 30) * 0.3 +
    dashaComposite.tension * 0.2
  ) * maleficFactor;

  return {
    area: worst.area,
    score: Math.round(Math.max(35, 100 - riskIntensity)),
    intensity: Math.round(riskIntensity),
  };
}

/**
 * Calculate Color Suggestion
 */
export function calculateColorSuggestion(poi, dayOfWeek, userProfile) {
  const dayPlanet = DAY_PLANET[dayOfWeek];
  const nakshatraInfo = NAKSHATRA_DATA[userProfile?.nakshatra] || NAKSHATRA_DATA['அஸ்வினி'];

  // Element to color mapping
  const elementColors = {
    fire: ['Orange', 'Red', 'Gold'],
    earth: ['Green', 'Brown', 'Yellow'],
    air: ['White', 'Light Blue', 'Grey'],
    water: ['Blue', 'Silver', 'White'],
  };

  // Find dominant planet by POI
  let maxPOI = 0;
  let dominantPlanet = dayPlanet;
  Object.entries(poi).forEach(([planet, intensity]) => {
    if (intensity > maxPOI) {
      maxPOI = intensity;
      dominantPlanet = planet;
    }
  });

  // Color selection weights
  const dayColor = PLANET_COLORS[dayPlanet]?.[0] || 'White';
  const nakshatraColor = elementColors[nakshatraInfo.element]?.[0] || 'White';
  const transitColor = PLANET_COLORS[dominantPlanet]?.[0] || 'White';

  // Return primary color (day planet has highest weight)
  return {
    primary: dayColor,
    secondary: nakshatraColor,
    tertiary: transitColor,
    score: 78,
  };
}

/**
 * Calculate Direction Suggestion
 */
export function calculateDirectionSuggestion(poi, hai, userProfile) {
  const nakshatraInfo = NAKSHATRA_DATA[userProfile?.nakshatra] || NAKSHATRA_DATA['அஸ்வினி'];

  // Find dominant planet
  let maxPOI = 0;
  let dominantPlanet = 'Sun';
  Object.entries(poi).forEach(([planet, intensity]) => {
    if (intensity > maxPOI) {
      maxPOI = intensity;
      dominantPlanet = planet;
    }
  });

  // Find strongest house
  let maxHAI = 0;
  let strongestHouse = 1;
  hai.forEach((val, idx) => {
    if (val > maxHAI) {
      maxHAI = val;
      strongestHouse = idx + 1;
    }
  });

  // House to direction mapping
  const houseDirections = {
    1: 'East', 2: 'Northeast', 3: 'East',
    4: 'North', 5: 'Northeast', 6: 'South',
    7: 'West', 8: 'Southwest', 9: 'Southeast',
    10: 'South', 11: 'Northwest', 12: 'Southwest',
  };

  // Nakshatra element direction
  const elementDirections = {
    fire: 'East',
    earth: 'South',
    air: 'West',
    water: 'North',
  };

  return {
    primary: PLANET_DIRECTIONS[dominantPlanet] || 'East',
    houseDirection: houseDirections[strongestHouse] || 'East',
    nakshatraDirection: elementDirections[nakshatraInfo.element] || 'East',
    score: 80,
  };
}

/**
 * Calculate Personal Note Score and generate summary
 */
export function calculatePersonalNote(allScores, nes, dashaComposite) {
  const avgScore = Object.values(allScores).reduce((sum, s) => sum + (s.score || s), 0) / Object.values(allScores).length;

  // Find top 2 strengths
  const sorted = Object.entries(allScores)
    .filter(([key]) => ['finance', 'career', 'relationship', 'health'].includes(key))
    .map(([area, data]) => ({ area, score: data.score || data }))
    .sort((a, b) => b.score - a.score);

  const strengths = sorted.slice(0, 2).map(s => s.area);
  const weakness = sorted[sorted.length - 1]?.area;

  return {
    score: Math.round(avgScore),
    strengths,
    weakness,
    emotionalTone: nes >= 75 ? 'positive' : nes >= 55 ? 'neutral' : 'introspective',
    dashaInfluence: dashaComposite.overall >= 70 ? 'supportive' : 'challenging',
  };
}

// ============================================================================
// CONFIDENCE CALCULATION
// ============================================================================

/**
 * Calculate overall confidence score
 */
export function calculateConfidence(hasLifeAreas, hasTransits, hasProjections, signalAgreement) {
  const dataCompleteness = (
    (hasLifeAreas ? 30 : 0) +
    (hasTransits ? 30 : 0) +
    (hasProjections ? 40 : 0)
  );

  const signalAgreementIndex = signalAgreement || 70;
  const transitClarityFactor = hasTransits ? 80 : 50;
  const dashaPredictability = hasProjections ? 75 : 55;

  const confidence = (
    0.30 * dataCompleteness +
    0.25 * signalAgreementIndex +
    0.25 * transitClarityFactor +
    0.20 * dashaPredictability
  );

  return Math.round(Math.max(50, Math.min(95, confidence)));
}

// ============================================================================
// FALLBACK LOGIC
// ============================================================================

/**
 * Deterministic fallback scoring when API is unavailable
 * Formula: base = 40 + (nakshatraID * 2) + (rasiID * 3)
 *          variation = (dateHash % 15) - 7
 *          final = clamp(base + variation, 45, 92)
 */
export function calculateFallbackScore(userProfile) {
  const today = new Date();
  const dateStr = today.toISOString().split('T')[0];

  const nakshatraId = NAKSHATRA_INDEX[userProfile?.nakshatra] || 0;
  const rasiId = RASI_INDEX[userProfile?.rasi] || 0;

  // Create deterministic hash from date
  let dateHash = 0;
  for (let i = 0; i < dateStr.length; i++) {
    dateHash = ((dateHash << 5) - dateHash) + dateStr.charCodeAt(i);
    dateHash = dateHash & dateHash;
  }
  dateHash = Math.abs(dateHash);

  const base = 40 + (nakshatraId * 2) + (rasiId * 3);
  const variation = (dateHash % 15) - 7;
  const final = Math.max(45, Math.min(92, base + variation));

  return final;
}

/**
 * Generate all card scores using fallback logic
 */
export function generateFallbackScores(userProfile) {
  const baseScore = calculateFallbackScore(userProfile);
  const dayOfWeek = new Date().getDay();
  const dayOfMonth = new Date().getDate();

  // Create variations for each card
  const nakshatraId = NAKSHATRA_INDEX[userProfile?.nakshatra] || 0;
  const rasiId = RASI_INDEX[userProfile?.rasi] || 0;

  const variations = [
    (nakshatraId % 7) - 3, // dasha_mood
    (rasiId % 5) - 2, // transit_pressure
    (dayOfWeek % 4) + 1, // finance
    ((nakshatraId + rasiId) % 6) - 2, // career
    (dayOfMonth % 5) - 2, // relationship
    ((dayOfWeek + nakshatraId) % 5) - 2, // health
    5, // lucky_window (generally positive)
    -5, // avoid_window (generally cautionary)
    Math.max(0, (baseScore - 65) / 2), // opportunity
    Math.min(0, (65 - baseScore) / 2), // risk
    0, // color (neutral)
    0, // direction (neutral)
    0, // personal_note (average)
  ];

  return {
    dasha_mood: Math.max(45, Math.min(92, baseScore + variations[0])),
    transit_pressure: Math.max(45, Math.min(92, baseScore + variations[1])),
    finance_outlook: Math.max(45, Math.min(92, baseScore + variations[2])),
    work_career: Math.max(45, Math.min(92, baseScore + variations[3])),
    relationship_energy: Math.max(45, Math.min(92, baseScore + variations[4])),
    health_vibration: Math.max(45, Math.min(92, baseScore + variations[5])),
    lucky_window: Math.max(60, Math.min(88, baseScore + variations[6])),
    avoid_window: Math.max(35, Math.min(65, 50 + variations[7])),
    opportunity_indicator: Math.max(50, Math.min(92, baseScore + variations[8])),
    risk_indicator: Math.max(40, Math.min(85, baseScore + variations[9])),
    color_direction: 78,
    personal_note: baseScore,
  };
}

// ============================================================================
// MAIN ENGINE FUNCTION
// ============================================================================

/**
 * Main function to calculate all scores using the deep astrology engine
 * @param {Object} userProfile - User profile with rasi, nakshatra
 * @param {Object} unifiedData - Data from unified scoring service
 * @returns {Object} All calculated scores and metadata
 */
export function calculateDeepScores(userProfile, unifiedData) {
  const today = new Date();
  const dayOfWeek = today.getDay();
  const dayOfMonth = today.getDate();
  const currentHour = today.getHours();

  // Extract data from unified data
  const lifeAreas = unifiedData?.lifeAreas?.life_areas || {};
  const transits = unifiedData?.transits || {};
  const projections = unifiedData?.projections || {};

  // Calculate core engine values
  const hai = calculateHAI(userProfile, transits, dayOfWeek);
  const poi = calculatePOI(userProfile, transits, projections, dayOfWeek);
  const nes = calculateNES(userProfile, dayOfWeek);
  const dashaComposite = calculateDashaComposite(projections, poi, dayOfWeek);
  const moonPhaseStability = calculateMoonPhaseStability(dayOfMonth);
  const dashaLord = projections?.current_dasha?.lord || 'Venus';
  const rasi = userProfile?.rasi || 'மேஷம்';

  // Calculate individual card scores
  const dasha_mood = calculateDashaMoodScore(dashaComposite, poi, hai, nes, dashaLord, rasi);
  const transit_pressure = calculateTransitPressureScore(transits, nes, moonPhaseStability);
  const finance_outlook = calculateFinanceScore(hai, poi, dashaComposite, lifeAreas.career?.score);
  const work_career = calculateCareerScore(hai, poi, dashaComposite, transits, lifeAreas.career?.score);
  const relationship_energy = calculateRelationshipScore(hai, poi, nes, lifeAreas.love?.score);
  const health_vibration = calculateHealthScore(hai, poi, moonPhaseStability, lifeAreas.family?.score);

  // Calculate time windows
  const luckyWindow = calculateLuckyWindow(userProfile, poi, dayOfWeek);
  const avoidWindow = calculateAvoidWindow(dayOfWeek);

  // Calculate opportunity and risk
  const scores = { finance: finance_outlook, career: work_career, relationship: relationship_energy, health: health_vibration };
  const opportunity = calculateOpportunityScore(scores);
  const risk = calculateRiskScore(scores, transits, poi, dashaComposite);

  // Calculate color and direction
  const colorSuggestion = calculateColorSuggestion(poi, dayOfWeek, userProfile);
  const directionSuggestion = calculateDirectionSuggestion(poi, hai, userProfile);

  // Calculate personal note
  const personalNote = calculatePersonalNote(scores, nes, dashaComposite);

  // Calculate confidence
  const hasLifeAreas = Object.keys(lifeAreas).length > 0;
  const hasTransits = Object.keys(transits).length > 0;
  const hasProjections = Object.keys(projections).length > 0;

  // Signal agreement: how well do the scores align
  const scoreValues = [dasha_mood, transit_pressure, finance_outlook, work_career, relationship_energy, health_vibration];
  const avgScore = scoreValues.reduce((a, b) => a + b, 0) / scoreValues.length;
  const variance = scoreValues.reduce((sum, s) => sum + Math.pow(s - avgScore, 2), 0) / scoreValues.length;
  const signalAgreement = Math.max(50, 100 - Math.sqrt(variance));

  const confidence = calculateConfidence(hasLifeAreas, hasTransits, hasProjections, signalAgreement);

  return {
    scores: {
      dasha_mood,
      transit_pressure,
      finance_outlook,
      work_career,
      relationship_energy,
      health_vibration,
      lucky_window: luckyWindow.score,
      avoid_window: avoidWindow.score,
      opportunity_indicator: opportunity.score,
      risk_indicator: risk.score,
      color_direction: colorSuggestion.score,
      personal_note: personalNote.score,
    },
    metadata: {
      dashaLord,
      nes,
      moonPhaseStability,
      luckyWindow,
      avoidWindow,
      opportunity,
      risk,
      colorSuggestion,
      directionSuggestion,
      personalNote,
      confidence,
      hai,
      poi,
      dashaComposite,
    },
  };
}

export default {
  calculateDeepScores,
  calculateFallbackScore,
  generateFallbackScores,
  calculateHAI,
  calculatePOI,
  calculateNES,
  calculateDashaComposite,
  getRahuKalam,
  getYamaKandam,
  getCurrentHora,
};
