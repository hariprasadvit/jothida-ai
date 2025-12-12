/**
 * Unified Scoring Service
 *
 * This service ensures consistent scores across Dashboard, AstroFeed, and UngalJothidan.
 * All screens MUST use this service to fetch and calculate scores.
 *
 * SCORING LOGIC:
 * 1. Fetch life areas from API (career, love, family, education)
 * 2. Calculate overall score as average of all life areas
 * 3. Cache results to avoid redundant API calls within same session
 */

import { mobileAPI } from './api';

// In-memory cache for scores (reset on app restart)
let scoreCache = {
  data: null,
  timestamp: null,
  userKey: null,
};

// Cache validity: 5 minutes
const CACHE_VALIDITY_MS = 5 * 60 * 1000;

/**
 * Generate a consistent user key for caching
 */
const getUserKey = (userProfile) => {
  if (!userProfile?.birthDate) return null;
  return `${userProfile.birthDate}-${userProfile.birthTime || '06:00'}-${userProfile.birthPlace || 'Chennai'}`;
};

/**
 * Check if cache is valid
 */
const isCacheValid = (userProfile) => {
  if (!scoreCache.data || !scoreCache.timestamp) return false;

  const userKey = getUserKey(userProfile);
  if (scoreCache.userKey !== userKey) return false;

  const now = Date.now();
  return (now - scoreCache.timestamp) < CACHE_VALIDITY_MS;
};

/**
 * Prepare birth details in the format expected by mobileAPI.getLifeAreas
 * This is the SINGLE SOURCE OF TRUTH for birth details formatting
 */
export const prepareBirthDetails = (userProfile) => {
  if (!userProfile?.birthDate) return null;

  return {
    name: userProfile.name || '',
    birthDate: userProfile.birthDate,
    birthTime: userProfile.birthTime || '06:00',
    birthPlace: userProfile.birthPlace || 'Chennai',
  };
};

/**
 * Fetch unified scores from API
 * Returns: { overallScore, lifeAreas, transits, projections, confidence }
 */
export const fetchUnifiedScores = async (userProfile, language = 'ta') => {
  // Return cached data if valid
  if (isCacheValid(userProfile)) {
    console.log('[ScoringService] Using cached scores');
    return scoreCache.data;
  }

  const birthDetails = prepareBirthDetails(userProfile);
  if (!birthDetails) {
    console.log('[ScoringService] No birth details available');
    return null;
  }

  const langCode = language === 'tamil' ? 'ta' : language === 'kannada' ? 'kn' :
                   language === 'en' ? 'en' : language;

  try {
    console.log('[ScoringService] Fetching fresh scores from API');

    // Fetch all data in parallel
    const [lifeAreasData, transitsData, projectionsData] = await Promise.all([
      mobileAPI.getLifeAreas(birthDetails, langCode).catch(err => {
        console.error('[ScoringService] Life areas API error:', err);
        return null;
      }),
      mobileAPI.getTransitsMap(
        userProfile.birthPlace || 'Chennai',
        userProfile.rasi || ''
      ).catch(err => {
        console.error('[ScoringService] Transits API error:', err);
        return null;
      }),
      mobileAPI.getFutureProjections(birthDetails, langCode).catch(err => {
        console.error('[ScoringService] Projections API error:', err);
        return null;
      }),
    ]);

    // Calculate overall score from life areas (SAME as Dashboard)
    let overallScore = 70; // Default fallback
    let lifeAreasArray = [];
    let confidence = 70;

    if (lifeAreasData?.life_areas) {
      const areas = lifeAreasData.life_areas;
      const areaKeys = ['love', 'career', 'education', 'family'];
      const validScores = areaKeys
        .map(key => areas[key]?.score)
        .filter(score => score !== undefined && score !== null);

      if (validScores.length > 0) {
        overallScore = Math.round(validScores.reduce((sum, s) => sum + s, 0) / validScores.length);
        confidence = 85; // Higher confidence with API data

        // Build life areas array with all details
        lifeAreasArray = areaKeys.map(key => ({
          key,
          score: areas[key]?.score || 50,
          factors: areas[key]?.factors || [],
          suggestion: areas[key]?.suggestion || '',
          breakdown: areas[key]?.breakdown || {},
        }));
      }
    }

    // Build result object
    const result = {
      overallScore,
      lifeAreas: lifeAreasData,
      lifeAreasArray,
      transits: transitsData,
      projections: projectionsData,
      confidence,
      fetchedAt: new Date().toISOString(),
    };

    // Cache the result
    scoreCache = {
      data: result,
      timestamp: Date.now(),
      userKey: getUserKey(userProfile),
    };

    console.log('[ScoringService] Scores fetched successfully, overall:', overallScore);
    return result;

  } catch (error) {
    console.error('[ScoringService] Error fetching scores:', error);
    return null;
  }
};

/**
 * Get the cached overall score (for quick access without API call)
 * Returns null if no cached data
 */
export const getCachedOverallScore = () => {
  return scoreCache.data?.overallScore || null;
};

/**
 * Get cached life areas data
 */
export const getCachedLifeAreas = () => {
  return scoreCache.data?.lifeAreas || null;
};

/**
 * Get cached transits data
 */
export const getCachedTransits = () => {
  return scoreCache.data?.transits || null;
};

/**
 * Get cached projections data
 */
export const getCachedProjections = () => {
  return scoreCache.data?.projections || null;
};

/**
 * Clear the score cache (call on logout or profile change)
 */
export const clearScoreCache = () => {
  scoreCache = {
    data: null,
    timestamp: null,
    userKey: null,
  };
  console.log('[ScoringService] Cache cleared');
};

/**
 * Manually populate the score cache
 * Called by DashboardScreen after it fetches all data
 * This ensures AstroFeed and UngalJothidan use the same scores
 */
export const populateScoreCache = (userProfile, lifeAreasData, transitsData, projectionsData) => {
  if (!userProfile?.birthDate) return;

  // Calculate overall score from life areas (SAME logic as Dashboard)
  let overallScore = 70;
  let lifeAreasArray = [];
  let confidence = 70;

  if (lifeAreasData?.life_areas) {
    const areas = lifeAreasData.life_areas;
    const areaKeys = ['love', 'career', 'education', 'family'];
    const validScores = areaKeys
      .map(key => areas[key]?.score)
      .filter(score => score !== undefined && score !== null);

    if (validScores.length > 0) {
      overallScore = Math.round(validScores.reduce((sum, s) => sum + s, 0) / validScores.length);
      confidence = 85;

      lifeAreasArray = areaKeys.map(key => ({
        key,
        score: areas[key]?.score || 50,
        factors: areas[key]?.factors || [],
        suggestion: areas[key]?.suggestion || '',
        breakdown: areas[key]?.breakdown || {},
      }));
    }
  }

  // Build result object (same structure as fetchUnifiedScores)
  const result = {
    overallScore,
    lifeAreas: lifeAreasData,
    lifeAreasArray,
    transits: transitsData,
    projections: projectionsData,
    confidence,
    fetchedAt: new Date().toISOString(),
  };

  // Cache the result
  scoreCache = {
    data: result,
    timestamp: Date.now(),
    userKey: getUserKey(userProfile),
  };

  console.log('[ScoringService] Cache populated from Dashboard, overall score:', overallScore);
  return result;
};

/**
 * Calculate fallback score using deterministic hash
 * This ensures same user gets same score on same day even without API
 */
export const calculateFallbackScore = (userProfile) => {
  const today = new Date();
  const dateStr = today.toISOString().split('T')[0];
  const hashInput = `${dateStr}-${userProfile?.rasi || 'default'}-${userProfile?.nakshatra || 'default'}`;

  let hash = 0;
  for (let i = 0; i < hashInput.length; i++) {
    hash = ((hash << 5) - hash) + hashInput.charCodeAt(i);
    hash = hash & hash;
  }

  // Range: 55-89 (centered around 72)
  return 55 + Math.abs(hash % 35);
};

/**
 * Generate individual card scores from unified data
 * Used by UngalJothidan for 12-card display
 */
export const generateCardScores = (unifiedData, userProfile) => {
  if (!unifiedData) {
    return generateFallbackCardScores(userProfile);
  }

  const { lifeAreas, transits, projections } = unifiedData;
  const today = new Date();
  const dayOfWeek = today.getDay();

  const areas = lifeAreas?.life_areas || {};

  // Get dasha info
  const dashaLord = projections?.current_dasha?.lord || getDashaFromNakshatra(userProfile?.nakshatra);
  const dashaScore = projections?.current_dasha?.strength || calculateDashaScore(dashaLord, dayOfWeek);

  // Transit pressure (inverted: high intensity = low score)
  const transitScore = transits?.overall_intensity
    ? Math.max(30, Math.min(90, 100 - transits.overall_intensity))
    : 65;

  // Life area scores
  const careerScore = areas.career?.score || 65;
  const loveScore = areas.love?.score || 60;
  const familyScore = areas.family?.score || 65;
  const educationScore = areas.education?.score || 68;

  // Health: 60% family + 40% inverse malefic
  const healthScore = Math.round(
    (familyScore * 0.6) + (100 - (transits?.malefic_intensity || 35)) * 0.4
  );

  // Lucky/Avoid window times
  const luckyTime = calculateLuckyTime(dayOfWeek);
  const rahuKalam = getRahuKalam(dayOfWeek);

  // Best and worst areas
  const areaEntries = Object.entries(areas).filter(([k, v]) => v?.score !== undefined);
  const sortedAreas = [...areaEntries].sort((a, b) => (b[1]?.score || 0) - (a[1]?.score || 0));
  const bestArea = sortedAreas[0];
  const worstArea = sortedAreas[sortedAreas.length - 1];

  const opportunityScore = bestArea?.[1]?.score || 70;
  const riskScore = 100 - (worstArea?.[1]?.score || 70);

  // Color/Direction based on day
  const colorDirection = getColorDirectionData(dayOfWeek);

  return {
    dasha_mood: { score: dashaScore, lord: dashaLord },
    transit_pressure: { score: transitScore },
    finance_outlook: { score: careerScore },
    work_career: { score: careerScore },
    relationship_energy: { score: loveScore },
    health_vibration: { score: healthScore },
    lucky_window: { score: 70 + (dayOfWeek % 3) * 8, time: luckyTime },
    avoid_window: { score: 60, time: rahuKalam },
    opportunity_indicator: { score: opportunityScore, area: bestArea?.[0] },
    risk_indicator: { score: Math.max(30, 100 - riskScore), area: worstArea?.[0] },
    color_direction: { score: 78, ...colorDirection },
    personal_note: { score: unifiedData.overallScore },
  };
};

/**
 * Fallback card scores when API is unavailable
 */
const generateFallbackCardScores = (userProfile) => {
  const baseScore = calculateFallbackScore(userProfile);
  const dayOfWeek = new Date().getDay();

  return {
    dasha_mood: { score: baseScore + 5, lord: 'Venus' },
    transit_pressure: { score: baseScore - 5 },
    finance_outlook: { score: baseScore },
    work_career: { score: baseScore + 3 },
    relationship_energy: { score: baseScore - 3 },
    health_vibration: { score: baseScore + 2 },
    lucky_window: { score: 70 + (dayOfWeek % 3) * 8, time: calculateLuckyTime(dayOfWeek) },
    avoid_window: { score: 60, time: getRahuKalam(dayOfWeek) },
    opportunity_indicator: { score: baseScore + 5 },
    risk_indicator: { score: Math.max(40, baseScore - 10) },
    color_direction: { score: 78, ...getColorDirectionData(dayOfWeek) },
    personal_note: { score: baseScore },
  };
};

// Helper functions
function getDashaFromNakshatra(nakshatra) {
  const nakshatraLords = {
    'அஸ்வினி': 'Ketu', 'பரணி': 'Venus', 'கார்த்திகை': 'Sun',
    'ரோகிணி': 'Moon', 'மிருகசீரிடம்': 'Mars', 'திருவாதிரை': 'Rahu',
    'புனர்பூசம்': 'Jupiter', 'பூசம்': 'Saturn', 'ஆயில்யம்': 'Mercury',
  };
  return nakshatraLords[nakshatra] || 'Venus';
}

function calculateDashaScore(dashaLord, dayOfWeek) {
  const lordStrengths = {
    Sun: 75, Moon: 70, Mars: 65, Mercury: 80,
    Jupiter: 85, Venus: 82, Saturn: 55, Rahu: 50, Ketu: 48,
  };
  const dayLords = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'];
  const base = lordStrengths[dashaLord] || 70;
  const bonus = dayLords[dayOfWeek] === dashaLord ? 10 : 0;
  return Math.min(95, base + bonus);
}

function calculateLuckyTime(dayOfWeek) {
  const baseHour = 8 + (dayOfWeek % 4);
  return {
    start: `${String(baseHour).padStart(2, '0')}:00`,
    end: `${String(baseHour + 2).padStart(2, '0')}:00`,
  };
}

function getRahuKalam(dayOfWeek) {
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

function getColorDirectionData(dayOfWeek) {
  const colors = ['Orange', 'White', 'Red', 'Green', 'Yellow', 'White', 'Blue'];
  const directions = ['East', 'Northwest', 'South', 'North', 'Northeast', 'Southeast', 'West'];
  return {
    color: colors[dayOfWeek],
    direction: directions[dayOfWeek],
  };
}

export default {
  fetchUnifiedScores,
  prepareBirthDetails,
  getCachedOverallScore,
  getCachedLifeAreas,
  getCachedTransits,
  getCachedProjections,
  clearScoreCache,
  populateScoreCache,
  calculateFallbackScore,
  generateCardScores,
};
