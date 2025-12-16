import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  RefreshControl,
  Platform,
  Animated,
  Easing,
  Modal,
  Dimensions,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import Svg, { Path, Circle, Defs, RadialGradient, Stop, Ellipse, Text as SvgText } from 'react-native-svg';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { mobileAPI } from '../services/api';
import { populateScoreCache } from '../services/scoringService';
import notificationService from '../services/notificationService';

const { width } = Dimensions.get('window');

// Planet API name to translation key mapping
const planetTranslationKeys = {
  'Sun': 'sun_planet',
  'Moon': 'moon_planet',
  'Mars': 'mars',
  'Mercury': 'mercury',
  'Jupiter': 'jupiter',
  'Venus': 'venus',
  'Saturn': 'saturn',
  'Rahu': 'rahu',
  'Ketu': 'ketu',
};

// Month name mapping for translation from Tamil to translation keys
const TAMIL_MONTH_MAP = {
  'ஜனவரி': 'january', 'பிப்ரவரி': 'february', 'மார்ச்': 'march',
  'ஏப்ரல்': 'april', 'மே': 'may', 'ஜூன்': 'june',
  'ஜூலை': 'july', 'ஆகஸ்ட்': 'august', 'செப்டம்பர்': 'september',
  'அக்டோபர்': 'october', 'நவம்பர்': 'november', 'டிசம்பர்': 'december',
};

// Tamil planet name to translation key mapping
const TAMIL_PLANET_MAP = {
  'சூரியன்': 'sun_planet', 'சந்திரன்': 'moon_planet', 'செவ்வாய்': 'mars',
  'புதன்': 'mercury', 'குரு': 'jupiter', 'சுக்கிரன்': 'venus',
  'சனி': 'saturn', 'ராகு': 'rahu', 'கேது': 'ketu',
};

// Tamil Rasi (zodiac) name to translation key mapping
const TAMIL_RASI_MAP = {
  'மேஷம்': 'aries', 'ரிஷபம்': 'taurus', 'மிதுனம்': 'gemini',
  'கடகம்': 'cancer', 'சிம்மம்': 'leo', 'கன்னி': 'virgo',
  'துலாம்': 'libra', 'விருச்சிகம்': 'scorpio', 'தனுசு': 'sagittarius',
  'மகரம்': 'capricorn', 'கும்பம்': 'aquarius', 'மீனம்': 'pisces',
};

// English Rasi name to translation key mapping
const ENGLISH_RASI_MAP = {
  'Aries': 'aries', 'Taurus': 'taurus', 'Gemini': 'gemini',
  'Cancer': 'cancer', 'Leo': 'leo', 'Virgo': 'virgo',
  'Libra': 'libra', 'Scorpio': 'scorpio', 'Sagittarius': 'sagittarius',
  'Capricorn': 'capricorn', 'Aquarius': 'aquarius', 'Pisces': 'pisces',
};

// Tamil Nakshatra name to translation key mapping
const TAMIL_NAKSHATRA_MAP = {
  'அஸ்வினி': 'ashwini', 'பரணி': 'bharani', 'கார்த்திகை': 'krittika',
  'ரோகிணி': 'rohini', 'மிருகசீரிடம்': 'mrigashira', 'திருவாதிரை': 'ardra',
  'புனர்பூசம்': 'punarvasu', 'பூசம்': 'pushya', 'ஆயில்யம்': 'ashlesha',
  'மகம்': 'magha', 'பூரம்': 'purvaPhalguni', 'உத்திரம்': 'uttaraPhalguni',
  'ஹஸ்தம்': 'hasta', 'சித்திரை': 'chitra', 'சுவாதி': 'swati',
  'விசாகம்': 'vishakha', 'அனுஷம்': 'anuradha', 'கேட்டை': 'jyeshtha',
  'மூலம்': 'moola', 'பூராடம்': 'purvaAshadha', 'உத்திராடம்': 'uttaraAshadha',
  'திருவோணம்': 'shravana', 'அவிட்டம்': 'dhanishta', 'சதயம்': 'shatabhisha',
  'பூரட்டாதி': 'purvaBhadrapada', 'உத்திரட்டாதி': 'uttaraBhadrapada', 'ரேவதி': 'revati',
};

// Tamil Month (Panchangam) name to translation key mapping
const TAMIL_PANCHANGAM_MONTH_MAP = {
  'சித்திரை': 'chithirai', 'வைகாசி': 'vaikasi', 'ஆனி': 'aani',
  'ஆடி': 'aadi', 'ஆவணி': 'aavani', 'புரட்டாசி': 'purattasi',
  'ஐப்பசி': 'aippasi', 'கார்த்திகை': 'karthigai', 'மார்கழி': 'margazhi',
  'தை': 'thai', 'மாசி': 'maasi', 'பங்குனி': 'panguni',
};

// Tamil Moon phase to translation key mapping
const TAMIL_MOON_PHASE_MAP = {
  'அமாவாசை': 'newMoon', 'வளர்பிறை': 'waxingCrescent', 'பௌர்ணமி': 'fullMoon',
  'தேய்பிறை': 'waningCrescent', 'சுக்ல பட்சம்': 'waxingCrescent',
  'கிருஷ்ண பட்சம்': 'waningCrescent',
};

// Tamil Aura level to translation key mapping
const TAMIL_AURA_MAP = {
  'வலிமையான ஒளி': 'strongAura', 'மிதமான ஒளி': 'moderateAura',
  'பலவீனமான ஒளி': 'weakAura',
};

// Tamil Life Trend direction to translation key mapping
const TAMIL_DIRECTION_MAP = {
  'ஏற்றம்': 'ascending', 'இறக்கம்': 'descending', 'நிலையான நிலை': 'stable',
  'உயர்வு': 'ascending', 'தாழ்வு': 'descending', 'சமநிலை': 'stable',
};

// Tamil Dasha planet name to translation key mapping (for timeline)
const TAMIL_DASHA_MAP = {
  'சூரியன்': 'sun_planet', 'சந்திரன்': 'moon_planet', 'செவ்வாய்': 'mars',
  'புதன்': 'mercury', 'குரு': 'jupiter', 'சுக்கிரன்': 'venus',
  'சனி': 'saturn', 'ராகு': 'rahu', 'கேது': 'ketu',
  // Also short forms
  'சூரி': 'sun_planet', 'சந்': 'moon_planet', 'செவ்': 'mars',
  'புத': 'mercury', 'குரு': 'jupiter', 'சுக்': 'venus',
  'சனி': 'saturn', 'ராகு': 'rahu', 'கேது': 'ketu',
};

// English Dasha names mapping
const ENGLISH_DASHA_MAP = {
  'Sun': 'sun_planet', 'Moon': 'moon_planet', 'Mars': 'mars',
  'Mercury': 'mercury', 'Jupiter': 'jupiter', 'Venus': 'venus',
  'Saturn': 'saturn', 'Rahu': 'rahu', 'Ketu': 'ketu',
};

// Helper to translate month name from API response to user's language
const translateMonthName = (monthName, t) => {
  if (!monthName) return monthName;
  // Check if it's a Tamil month name that needs translation
  const monthKey = TAMIL_MONTH_MAP[monthName];
  if (monthKey) {
    return t(monthKey);
  }
  // Check if it matches English month names (API might return English)
  const englishMonths = ['January', 'February', 'March', 'April', 'May', 'June',
                         'July', 'August', 'September', 'October', 'November', 'December'];
  const monthIndex = englishMonths.findIndex(m => m.toLowerCase() === monthName.toLowerCase());
  if (monthIndex !== -1) {
    const keys = ['january', 'february', 'march', 'april', 'may', 'june',
                  'july', 'august', 'september', 'october', 'november', 'december'];
    return t(keys[monthIndex]);
  }
  return monthName;
};

// Helper to get planet name based on language
const getPlanetName = (planet, language, t) => {
  if (!planet) return '';
  // If language is Tamil, use the Tamil name directly from API
  if (language === 'ta') {
    return planet.tamil || planet.name;
  }
  // For other languages, use translation
  const planetKey = TAMIL_PLANET_MAP[planet.tamil] || planetTranslationKeys[planet.name];
  if (planetKey) {
    return t(planetKey);
  }
  // Fallback to English name
  return planet.name || planet.tamil;
};

// Helper to translate Rasi (zodiac sign) name
const translateRasiName = (rasiName, t) => {
  if (!rasiName) return rasiName;
  // Check Tamil rasi names
  const tamilKey = TAMIL_RASI_MAP[rasiName];
  if (tamilKey) return t(tamilKey);
  // Check English rasi names
  const englishKey = ENGLISH_RASI_MAP[rasiName];
  if (englishKey) return t(englishKey);
  return rasiName;
};

// Helper to translate Nakshatra name
const translateNakshatraName = (nakshatraName, t) => {
  if (!nakshatraName) return nakshatraName;
  const key = TAMIL_NAKSHATRA_MAP[nakshatraName];
  if (key) return t(key);
  return nakshatraName;
};

// Helper to translate Tamil month (Panchangam)
const translatePanchangamMonth = (monthName, t) => {
  if (!monthName) return monthName;
  const key = TAMIL_PANCHANGAM_MONTH_MAP[monthName];
  if (key) return t(key);
  return monthName;
};

// Helper to translate moon phase
const translateMoonPhase = (phase, t) => {
  if (!phase) return phase;
  const key = TAMIL_MOON_PHASE_MAP[phase];
  if (key) return t(key);
  return phase;
};

// Helper to translate aura level
const translateAuraLevel = (auraLabel, t) => {
  if (!auraLabel) return auraLabel;
  const key = TAMIL_AURA_MAP[auraLabel];
  if (key) return t(key);
  return auraLabel;
};

// Helper to translate planet name from string (for dominant/challenged planets)
const translatePlanetString = (planetName, language, t) => {
  if (!planetName) return planetName;
  if (language === 'ta') return planetName;
  const key = TAMIL_PLANET_MAP[planetName];
  if (key) return t(key);
  return planetName;
};

// Helper to translate life trend direction
const translateDirection = (directionTamil, t) => {
  if (!directionTamil) return directionTamil;
  const key = TAMIL_DIRECTION_MAP[directionTamil];
  if (key) return t(key);
  return directionTamil;
};

// Helper to translate Dasha planet name
const translateDashaName = (dashaName, language, t) => {
  if (!dashaName) return dashaName;
  if (language === 'ta') return dashaName;
  // Check Tamil dasha names
  const tamilKey = TAMIL_DASHA_MAP[dashaName];
  if (tamilKey) return t(tamilKey);
  // Check English dasha names
  const englishKey = ENGLISH_DASHA_MAP[dashaName];
  if (englishKey) return t(englishKey);
  // Check if it's a partial Tamil name (e.g., first 3 chars)
  for (const [tamil, key] of Object.entries(TAMIL_DASHA_MAP)) {
    if (tamil.startsWith(dashaName) || dashaName.startsWith(tamil.substring(0, 3))) {
      return t(key);
    }
  }
  return dashaName;
};

// Helper to construct retrograde message in user's language
const getRetrogradeMessage = (retro, language, t) => {
  if (!retro) return '';
  if (language === 'ta') return retro.message || '';
  // Construct message from data
  const planetName = translatePlanetString(retro.tamil, language, t);
  if (retro.days_remaining) {
    return `${planetName} ${t('retrograde')} - ${retro.days_remaining} ${t('daysRemaining')}`;
  }
  return `${planetName} ${t('retrograde')}`;
};

// Helper to translate event labels
const translateEventLabel = (event, language, t) => {
  if (!event) return '';
  if (language === 'ta') return event.label_tamil || event.label;
  return event.label || event.label_tamil;
};

// ============== RASHI PALAN DATA & COMPONENT ==============

// Zodiac Icon Component using SVG
const ZodiacIcon = ({ sign, size = 30 }) => {
  const zodiacData = {
    aries: { symbol: '♈', color1: '#f59e0b', color2: '#fb923c' },
    taurus: { symbol: '♉', color1: '#f59e0b', color2: '#fbbf24' },
    gemini: { symbol: '♊', color1: '#f97316', color2: '#fb923c' },
    cancer: { symbol: '♋', color1: '#f59e0b', color2: '#fbbf24' },
    leo: { symbol: '♌', color1: '#f97316', color2: '#fb923c' },
    virgo: { symbol: '♍', color1: '#f97316', color2: '#fbbf24' },
    libra: { symbol: '♎', color1: '#f59e0b', color2: '#fb923c' },
    scorpio: { symbol: '♏', color1: '#f59e0b', color2: '#fbbf24' },
    sagittarius: { symbol: '♐', color1: '#f59e0b', color2: '#fb923c' },
    capricorn: { symbol: '♑', color1: '#f59e0b', color2: '#fbbf24' },
    aquarius: { symbol: '♒', color1: '#f97316', color2: '#fb923c' },
    pisces: { symbol: '♓', color1: '#f59e0b', color2: '#fbbf24' },
  };

  const data = zodiacData[sign];

  return (
    <Svg width={size} height={size} viewBox="0 0 100 100">
      <Defs>
        <RadialGradient id={`grad-${sign}`} cx="50%" cy="50%" r="50%">
          <Stop offset="0%" stopColor={data.color1} stopOpacity="1" />
          <Stop offset="100%" stopColor={data.color2} stopOpacity="1" />
        </RadialGradient>
      </Defs>
      <Circle cx="50" cy="50" r="48" fill={`url(#grad-${sign})`} stroke="#fff" strokeWidth="2" />
      <SvgText
        x="50"
        y="50"
        fontSize="48"
        fontWeight="bold"
        fill="#fff"
        textAnchor="middle"
        alignmentBaseline="central"
        dy="3"
      >
        {data.symbol}
      </SvgText>
    </Svg>
  );
};

// 12 Zodiac signs data
const RASHI_DATA = [
  { key: 'aries', color: '#f59e0b', ruler: 'Mars', element: 'fire', ta: 'மேஷம்' },
  { key: 'taurus', color: '#f59e0b', ruler: 'Venus', element: 'earth', ta: 'ரிஷபம்' },
  { key: 'gemini', color: '#f97316', ruler: 'Mercury', element: 'air', ta: 'மிதுனம்' },
  { key: 'cancer', color: '#f59e0b', ruler: 'Moon', element: 'water', ta: 'கடகம்' },
  { key: 'leo', color: '#f97316', ruler: 'Sun', element: 'fire', ta: 'சிம்மம்' },
  { key: 'virgo', color: '#f97316', ruler: 'Mercury', element: 'earth', ta: 'கன்னி' },
  { key: 'libra', color: '#f59e0b', ruler: 'Venus', element: 'air', ta: 'துலாம்' },
  { key: 'scorpio', color: '#f59e0b', ruler: 'Mars', element: 'water', ta: 'விருச்சிகம்' },
  { key: 'sagittarius', color: '#f59e0b', ruler: 'Jupiter', element: 'fire', ta: 'தனுசு' },
  { key: 'capricorn', color: '#f59e0b', ruler: 'Saturn', element: 'earth', ta: 'மகரம்' },
  { key: 'aquarius', color: '#f97316', ruler: 'Saturn', element: 'air', ta: 'கும்பம்' },
  { key: 'pisces', color: '#f59e0b', ruler: 'Jupiter', element: 'water', ta: 'மீனம்' },
];

// Calculate dynamic Rashi score based on current transits and date
const calculateRashiScore = (rashiKey, transits, currentDate) => {
  // Base score varies by day of month (creates daily variation)
  const day = currentDate.getDate();
  const month = currentDate.getMonth();
  const rashiIndex = RASHI_DATA.findIndex(r => r.key === rashiKey);

  // Seed based on rashi position and date for consistent daily scores
  const seed = (rashiIndex * 7 + day * 3 + month * 11) % 100;

  // Base score between 55-85
  let score = 55 + (seed % 31);

  // Adjust based on element and current month
  const rashi = RASHI_DATA[rashiIndex];
  const monthElement = ['earth', 'earth', 'air', 'fire', 'fire', 'earth', 'air', 'water', 'fire', 'earth', 'air', 'water'][month];

  if (rashi.element === monthElement) score += 8;
  else if ((rashi.element === 'fire' && monthElement === 'air') ||
           (rashi.element === 'earth' && monthElement === 'water')) score += 5;

  // Adjust based on ruling planet transits if available
  if (transits) {
    const rulerTransit = transits[rashi.ruler.toLowerCase()] || transits[rashi.ruler];
    if (rulerTransit) {
      if (rulerTransit.is_retrograde) score -= 5;
      if (rulerTransit.dignity === 'exalted' || rulerTransit.dignity === 'own_sign') score += 7;
      if (rulerTransit.dignity === 'debilitated') score -= 5;
    }
  }

  // Ensure score is within bounds
  return Math.min(95, Math.max(45, Math.round(score)));
};

// Rashi Palan Ticker Component - News Bulletin Style Auto-Scroll
const RashiPalanTicker = ({ transits, language, t, userRashi, onRashiPress }) => {
  const scrollX = useRef(new Animated.Value(0)).current;
  const blinkAnim = useRef(new Animated.Value(1)).current;
  const [currentDate] = useState(new Date());
  const animationRef = useRef(null);
  const ITEM_WIDTH = 120; // Width of each rashi item + margin
  const TOTAL_WIDTH = ITEM_WIDTH * 12; // Total width for 12 items

  // Calculate scores for all rashis
  const rashiScores = RASHI_DATA.map(rashi => ({
    ...rashi,
    score: calculateRashiScore(rashi.key, transits, currentDate),
    name: language === 'ta' ? rashi.ta : t(rashi.key),
  }));

  // Triple the items for seamless infinite scroll
  const tickerItems = [...rashiScores, ...rashiScores, ...rashiScores];

  // Blinking LIVE dot animation
  useEffect(() => {
    const blink = Animated.loop(
      Animated.sequence([
        Animated.timing(blinkAnim, { toValue: 0.2, duration: 600, useNativeDriver: true }),
        Animated.timing(blinkAnim, { toValue: 1, duration: 600, useNativeDriver: true }),
      ])
    );
    blink.start();
    return () => blink.stop();
  }, []);

  // Auto-scroll animation - continuous loop
  useEffect(() => {
    const duration = TOTAL_WIDTH * 30; // 30ms per pixel for smooth scroll

    const animate = () => {
      scrollX.setValue(0);
      animationRef.current = Animated.timing(scrollX, {
        toValue: -TOTAL_WIDTH,
        duration: duration,
        easing: Easing.linear,
        useNativeDriver: true,
      });
      animationRef.current.start(({ finished }) => {
        if (finished) animate();
      });
    };

    animate();
    return () => animationRef.current?.stop();
  }, []);

  // Get score color
  const getScoreColor = (score) => {
    if (score >= 75) return '#22c55e';
    if (score >= 60) return '#fbbf24';
    return '#ef4444';
  };

  return (
    <View style={rashiTickerStyles.container}>
      {/* Header Bar */}
      <View style={rashiTickerStyles.header}>
        <View style={rashiTickerStyles.liveIndicator}>
          <Animated.View style={[rashiTickerStyles.liveDot, { opacity: blinkAnim }]} />
          <Text style={rashiTickerStyles.liveText}>LIVE</Text>
        </View>
        <Text style={rashiTickerStyles.title}>
          {language === 'ta' ? '⭐ இன்றைய ராசி பலன்' : '⭐ Today\'s Rashi Palan'}
        </Text>
        <Text style={rashiTickerStyles.date}>
          {currentDate.toLocaleDateString(language === 'ta' ? 'ta-IN' : 'en-IN', { weekday: 'short', day: 'numeric', month: 'short' })}
        </Text>
      </View>

      {/* Scrolling Ticker */}
      <View style={rashiTickerStyles.tickerWrapper}>
        <Animated.View
          style={[
            rashiTickerStyles.tickerContent,
            { transform: [{ translateX: scrollX }] }
          ]}
        >
          {tickerItems.map((rashi, index) => {
            const isUserRashi = userRashi && (
              userRashi.toLowerCase() === rashi.key ||
              userRashi === rashi.ta ||
              userRashi.toLowerCase().includes(rashi.key.substring(0, 4))
            );

            return (
              <View key={`${rashi.key}-${index}`} style={rashiTickerStyles.rashiItem}>
                <ZodiacIcon sign={rashi.key} size={30} />
                <Text style={[
                  rashiTickerStyles.rashiName,
                  isUserRashi && rashiTickerStyles.rashiNameHighlight
                ]}>
                  {rashi.name}
                </Text>
                <Text style={[rashiTickerStyles.scoreText, { color: getScoreColor(rashi.score) }]}>
                  {rashi.score}%
                </Text>
                {isUserRashi && <Ionicons name="star" size={14} color="#f97316" style={rashiTickerStyles.youIndicator} />}
                <Text style={rashiTickerStyles.separator}>│</Text>
              </View>
            );
          })}
        </Animated.View>
      </View>
    </View>
  );
};

// Rashi Ticker Styles - News Bulletin Style
const rashiTickerStyles = StyleSheet.create({
  container: {
    backgroundColor: '#fff',
    marginTop: 0,
    marginHorizontal: -16,
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 10,
    paddingVertical: 5,
    backgroundColor: '#ea580c',
    gap: 8,
  },
  liveIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 3,
    gap: 4,
  },
  liveDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#f97316',
  },
  liveText: {
    fontSize: 10,
    fontWeight: '900',
    color: '#f97316',
    letterSpacing: 0.5,
  },
  title: {
    flex: 1,
    fontSize: 13,
    fontWeight: '700',
    color: '#fff',
  },
  date: {
    fontSize: 11,
    color: '#fed7aa',
    fontWeight: '600',
  },
  tickerWrapper: {
    overflow: 'hidden',
    backgroundColor: '#fff',
    paddingVertical: 12,
  },
  tickerContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  rashiItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 6,
    gap: 6,
  },
  rashiName: {
    fontSize: 13,
    fontWeight: '600',
    color: '#1f2937',
    lineHeight: 18,
  },
  rashiNameHighlight: {
    color: '#f97316',
    fontWeight: '800',
  },
  scoreText: {
    fontSize: 14,
    fontWeight: '800',
    minWidth: 45,
    textAlign: 'right',
    lineHeight: 18,
  },
  youIndicator: {
    marginLeft: -2,
  },
  separator: {
    fontSize: 16,
    color: '#d1d5db',
    marginHorizontal: 8,
  },
});

// ============== DECORATIVE COMPONENTS ==============

// Simple decorative border - subtle golden line with dots
const DecorativeBorder = ({ style }) => {
  return (
    <View style={[{ width: '100%', alignItems: 'center', paddingVertical: 6 }, style]}>
      <View style={{ flexDirection: 'row', alignItems: 'center', width: '85%' }}>
        <View style={{ flex: 1, height: 1, backgroundColor: '#fcd34d' }} />
        <View style={{ width: 6, height: 6, borderRadius: 3, backgroundColor: '#f97316', marginHorizontal: 12 }} />
        <View style={{ flex: 1, height: 1, backgroundColor: '#fcd34d' }} />
      </View>
    </View>
  );
};

// Detailed Diya (Oil Lamp) Icon - Traditional style
const DiyaIcon = ({ size = 40, color = '#d97706' }) => (
  <Svg width={size} height={size} viewBox="0 0 100 100">
    <Defs>
      <RadialGradient id="flameGlow" cx="50%" cy="20%" r="60%">
        <Stop offset="0%" stopColor="#fbbf24" stopOpacity="1" />
        <Stop offset="50%" stopColor="#f97316" stopOpacity="0.6" />
        <Stop offset="100%" stopColor="#f97316" stopOpacity="0" />
      </RadialGradient>
    </Defs>
    {/* Flame glow */}
    <Ellipse cx="50" cy="22" rx="18" ry="22" fill="url(#flameGlow)" />
    {/* Outer flame */}
    <Path d="M50 5 Q58 18 55 30 Q52 38 50 42 Q48 38 45 30 Q42 18 50 5" fill="#f97316" />
    {/* Inner flame */}
    <Path d="M50 12 Q54 20 52 28 Q51 34 50 38 Q49 34 48 28 Q46 20 50 12" fill="#fbbf24" />
    {/* Flame core */}
    <Path d="M50 18 Q52 24 51 30 Q50 34 50 36 Q50 34 49 30 Q48 24 50 18" fill="#fff" opacity="0.8" />
    {/* Lamp body */}
    <Ellipse cx="50" cy="52" rx="28" ry="10" fill={color} />
    <Path d="M22 52 Q22 68 32 78 L68 78 Q78 68 78 52" fill={color} />
    {/* Lamp decorations */}
    <Ellipse cx="50" cy="60" rx="20" ry="6" fill="#b45309" opacity="0.5" />
    {/* Base */}
    <Ellipse cx="50" cy="82" rx="22" ry="6" fill={color} />
    <Ellipse cx="50" cy="88" rx="18" ry="4" fill="#92400e" />
    {/* Highlight */}
    <Ellipse cx="40" cy="52" rx="8" ry="3" fill="#fcd34d" opacity="0.4" />
  </Svg>
);



// Animated Card Component
const AnimatedCard = ({ children, delay = 0, style }) => {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const translateY = useRef(new Animated.Value(30)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 500,
        delay,
        useNativeDriver: true,
        easing: Easing.out(Easing.ease),
      }),
      Animated.timing(translateY, {
        toValue: 0,
        duration: 500,
        delay,
        useNativeDriver: true,
        easing: Easing.out(Easing.back(1.2)),
      }),
    ]).start();
  }, []);

  return (
    <Animated.View style={[style, { opacity: fadeAnim, transform: [{ translateY }] }]}>
      {children}
    </Animated.View>
  );
};

// Animated Progress Bar
const AnimatedProgressBar = ({ score, color, delay = 0 }) => {
  const widthAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(widthAnim, {
      toValue: score,
      duration: 1000,
      delay,
      useNativeDriver: false,
      easing: Easing.out(Easing.ease),
    }).start();
  }, [score]);

  return (
    <View style={styles.progressBar}>
      <Animated.View
        style={[
          styles.progressFill,
          {
            backgroundColor: color,
            width: widthAnim.interpolate({
              inputRange: [0, 100],
              outputRange: ['0%', '100%'],
            }),
          },
        ]}
      />
    </View>
  );
};

// Animated Score Circle - Tappable
const AnimatedScoreCircle = ({ score, onPress, tapText }) => {
  const scaleAnim = useRef(new Animated.Value(0)).current;
  const rotateAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.spring(scaleAnim, {
        toValue: 1,
        friction: 4,
        tension: 50,
        useNativeDriver: true,
      }),
      Animated.timing(rotateAnim, {
        toValue: 1,
        duration: 800,
        useNativeDriver: true,
        easing: Easing.out(Easing.ease),
      }),
    ]).start();
  }, []);

  const rotate = rotateAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  return (
    <TouchableOpacity onPress={onPress} activeOpacity={0.8}>
      <Animated.View
        style={[
          styles.scoreCircle,
          { transform: [{ scale: scaleAnim }, { rotate }] },
        ]}
      >
        <Text style={styles.scoreCircleText}>{score}%</Text>
        <Text style={styles.tapHint}>{tapText}</Text>
      </Animated.View>
    </TouchableOpacity>
  );
};

// Animated Quick Action Button
const AnimatedQuickAction = ({ action, index, onPress }) => {
  const scaleAnim = useRef(new Animated.Value(1)).current;
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const translateY = useRef(new Animated.Value(20)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 400,
        delay: 300 + index * 100,
        useNativeDriver: true,
      }),
      Animated.spring(translateY, {
        toValue: 0,
        friction: 6,
        delay: 300 + index * 100,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  const handlePressIn = () => {
    Animated.spring(scaleAnim, { toValue: 0.92, useNativeDriver: true }).start();
  };

  const handlePressOut = () => {
    Animated.spring(scaleAnim, { toValue: 1, friction: 3, useNativeDriver: true }).start();
  };

  return (
    <Animated.View
      style={{
        flex: 1,
        opacity: fadeAnim,
        transform: [{ translateY }, { scale: scaleAnim }],
      }}
    >
      <TouchableOpacity
        style={styles.quickActionBtn}
        onPress={onPress}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        activeOpacity={1}
      >
        <Ionicons name={action.icon} size={24} color={action.color} />
        <Text style={styles.quickActionLabel}>{action.label}</Text>
      </TouchableOpacity>
    </Animated.View>
  );
};

// Animated Life Area Card - Tappable for score details
const AnimatedLifeAreaCard = ({ area, index, onPress, t }) => {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const scaleAnim = useRef(new Animated.Value(0.8)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 400,
        delay: 200 + index * 100,
        useNativeDriver: true,
      }),
      Animated.spring(scaleAnim, {
        toValue: 1,
        friction: 6,
        delay: 200 + index * 100,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  return (
    <TouchableOpacity onPress={() => onPress(area)} activeOpacity={0.8}>
      <Animated.View
        style={[
          styles.lifeAreaCard,
          { opacity: fadeAnim, transform: [{ scale: scaleAnim }] },
        ]}
      >
        <View style={styles.lifeAreaHeader}>
          <Ionicons name={area.icon} size={20} color={area.color} />
          <View style={[styles.lifeAreaBadge, { backgroundColor: area.score > 75 ? '#dcfce7' : area.score > 50 ? '#fef3c7' : '#fef2f2' }]}>
            <Text style={[styles.lifeAreaBadgeText, { color: area.score > 75 ? '#16a34a' : area.score > 50 ? '#d97706' : '#dc2626' }]}>
              {area.score > 75 ? t('good') : area.score > 50 ? t('average') : t('caution')}
            </Text>
          </View>
        </View>
        <Text style={styles.lifeAreaName}>{area.name}</Text>
        <View style={styles.lifeAreaScoreRow}>
          <Text style={[styles.lifeAreaScore, { color: area.color }]}>{area.score}</Text>
          <Text style={styles.lifeAreaMax}>/100</Text>
          <Ionicons name="chevron-forward" size={16} color="#9ca3af" style={{ marginLeft: 'auto' }} />
        </View>
        <AnimatedProgressBar score={area.score} color={area.color} delay={400 + index * 100} />
      </Animated.View>
    </TouchableOpacity>
  );
};

// Month Projection Card
const MonthProjectionCard = ({ month, index, onPress }) => {
  const fadeAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 300,
      delay: index * 50,
      useNativeDriver: true,
    }).start();
  }, []);

  const getScoreColor = (score) => {
    if (score >= 75) return '#16a34a';
    if (score >= 50) return '#d97706';
    return '#dc2626';
  };

  return (
    <TouchableOpacity onPress={() => onPress(month)} activeOpacity={0.8}>
      <Animated.View style={[styles.monthCard, { opacity: fadeAnim }]}>
        <Text style={styles.monthName}>{month.name}</Text>
        <View style={[styles.monthScoreBadge, { backgroundColor: getScoreColor(month.score) + '20' }]}>
          <Text style={[styles.monthScore, { color: getScoreColor(month.score) }]}>{month.score}</Text>
        </View>
        <View style={styles.monthBarContainer}>
          <View style={[styles.monthBar, { width: `${month.score}%`, backgroundColor: getScoreColor(month.score) }]} />
        </View>
      </Animated.View>
    </TouchableOpacity>
  );
};

// Year Projection Card
const YearProjectionCard = ({ year, onPress }) => {
  const color = year.color || (year.score >= 75 ? '#16a34a' : year.score >= 50 ? '#d97706' : '#dc2626');

  return (
    <TouchableOpacity onPress={() => onPress(year)} activeOpacity={0.8} style={styles.yearCard}>
      <LinearGradient
        colors={[color + '10', color + '20']}
        style={styles.yearCardGradient}
      >
        <View style={[styles.yearIconBg, { backgroundColor: color + '20' }]}>
          <Ionicons name={year.icon || 'calendar'} size={20} color={color} />
        </View>
        <View style={styles.yearInfo}>
          <Text style={styles.yearName}>{year.year}</Text>
          <Text style={styles.yearLabel}>{year.label}</Text>
        </View>
        <View style={styles.yearScoreContainer}>
          <Text style={[styles.yearScore, { color }]}>{year.score}%</Text>
          <View style={[styles.yearScoreBar, { backgroundColor: color + '30' }]}>
            <View style={[styles.yearScoreFill, { width: `${year.score}%`, backgroundColor: color }]} />
          </View>
        </View>
        <Ionicons name="chevron-forward" size={18} color={color} />
      </LinearGradient>
    </TouchableOpacity>
  );
};

// Pulsing Sparkle Icon
const PulsingSparkle = () => {
  const pulseAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, { toValue: 1.3, duration: 800, useNativeDriver: true, easing: Easing.inOut(Easing.ease) }),
        Animated.timing(pulseAnim, { toValue: 1, duration: 800, useNativeDriver: true, easing: Easing.inOut(Easing.ease) }),
      ])
    ).start();
  }, []);

  return (
    <Animated.View style={{ transform: [{ scale: pulseAnim }] }}>
      <Ionicons name="sparkles" size={16} color="#ea580c" />
    </Animated.View>
  );
};

// Component name translation key mapping
const COMPONENT_KEYS = {
  dasha: { key: 'dashaBhukti', icon: 'time', color: '#8b5cf6' },
  house: { key: 'housePower', icon: 'home', color: '#3b82f6' },
  planet_strength: { key: 'planetPower', icon: 'planet', color: '#f59e0b' },
  transit: { key: 'transit', icon: 'swap-horizontal', color: '#10b981' },
  yoga: { key: 'yogaDosham', icon: 'sparkles', color: '#ec4899' },
  navamsa: { key: 'navamsam', icon: 'grid', color: '#6366f1' },
  // Life area components
  karaka: { key: 'karakaPlanet', icon: 'star', color: '#f97316' },
};

// Area name translation key mapping
const AREA_KEYS = {
  career: { key: 'careerLabel', icon: 'briefcase', color: '#3b82f6' },
  finance: { key: 'financeLabel', icon: 'wallet', color: '#10b981' },
  health: { key: 'healthLabel', icon: 'heart', color: '#ef4444' },
  relationships: { key: 'relationshipsLabel', icon: 'people', color: '#ec4899' },
};

// Generate truly dynamic AI Summary based on actual birth chart data
const generateAISummary = (data, score, t, language = 'en') => {
  const lang = language === 'ta' ? 'ta' : 'en';
  const scoreLevel = score >= 75 ? 'excellent' : score >= 60 ? 'good' : score >= 45 ? 'moderate' : 'challenging';

  // Extract actual birth chart factors
  const dashaLord = data.dasha_lord_label || data.dasha_lord || '';
  const bhuktiLord = data.bhukti_lord_label || data.bhukti_lord || '';
  const breakdown = data.breakdown || {};
  const trace = data.calculation_trace || {};
  const factors = data.factors || [];

  // Determine life area
  let area = data.area || 'general';
  const title = (data.title || data.name || '').toLowerCase();
  if (title.includes('love') || title.includes('காதல்')) area = 'love';
  else if (title.includes('career') || title.includes('தொழில்')) area = 'career';
  else if (title.includes('education') || title.includes('கல்வி')) area = 'education';
  else if (title.includes('family') || title.includes('குடும்ப')) area = 'family';
  else if (title.includes('health') || title.includes('ஆரோக்கிய')) area = 'health';

  // Build dynamic summary from actual data
  let summary = '';
  let highlights = [];
  let advice = '';

  // Area-specific house lords from Jyotish
  const areaHouses = {
    love: { house: 7, karaka: 'Venus', ta: { house: '7ஆம் வீடு', karaka: 'சுக்கிரன்' }},
    career: { house: 10, karaka: 'Saturn', ta: { house: '10ஆம் வீடு', karaka: 'சனி' }},
    education: { house: 4, karaka: 'Mercury', ta: { house: '4ஆம் வீடு', karaka: 'புதன்' }},
    family: { house: 4, karaka: 'Moon', ta: { house: '4ஆம் வீடு', karaka: 'சந்திரன்' }},
    health: { house: 1, karaka: 'Sun', ta: { house: 'லக்னம்', karaka: 'சூரியன்' }},
    general: { house: 1, karaka: 'Sun', ta: { house: 'லக்னம்', karaka: 'சூரியன்' }}
  };

  const houseInfo = areaHouses[area] || areaHouses.general;

  // Build summary based on score + dasha + area
  if (lang === 'ta') {
    if (dashaLord) {
      summary = `${dashaLord} தசையில் ${houseInfo.ta.house} ${score >= 60 ? 'பலமாக' : 'கவனம் தேவை'}. `;
      if (bhuktiLord) summary += `${bhuktiLord} புக்தி ${score >= 70 ? 'ஆதரவு தருகிறது' : 'சவால்களை கொண்டு வரலாம்'}. `;
    }
    summary += `உங்கள் மதிப்பெண் ${score}/100 - ${scoreLevel === 'excellent' ? 'மிகச்சிறந்த நிலை' : scoreLevel === 'good' ? 'நல்ல நிலை' : scoreLevel === 'moderate' ? 'சராசரி நிலை' : 'கவனம் தேவை'}.`;
  } else {
    if (dashaLord) {
      summary = `In ${dashaLord} dasha, your ${area === 'general' ? 'overall' : area} sector (House ${houseInfo.house}) is ${score >= 60 ? 'strong' : 'needing attention'}. `;
      if (bhuktiLord) summary += `${bhuktiLord} bhukti ${score >= 70 ? 'supports growth' : 'brings challenges to navigate'}. `;
    }
    summary += `Your score is ${score}/100 - ${scoreLevel === 'excellent' ? 'excellent position' : scoreLevel === 'good' ? 'favorable conditions' : scoreLevel === 'moderate' ? 'mixed influences' : 'caution advised'}.`;
  }

  // Build highlights from actual breakdown/factors
  if (factors.length > 0) {
    highlights = factors.slice(0, 3).map(f => {
      const isPositive = f.impact > 0 || f.type === 'positive';
      const icon = isPositive ? '✅' : '⚠️';
      return `${icon} ${f.description || f.factor || f.name}`;
    });
  } else if (Object.keys(breakdown).length > 0) {
    // Build from breakdown
    Object.entries(breakdown).slice(0, 3).forEach(([key, val]) => {
      const value = typeof val === 'object' ? val.value || val.score : val;
      const isGood = value >= 60;
      highlights.push(`${isGood ? '✅' : '⚠️'} ${key.replace(/_/g, ' ')}: ${value}%`);
    });
  }

  // Default highlights if none from data
  if (highlights.length === 0) {
    if (lang === 'ta') {
      if (area === 'love') {
        highlights = score >= 60
          ? [`💕 ${houseInfo.ta.karaka} பலமாக உள்ளது`, `🤝 உறவுகள் வளரும்`, `💫 புரிதல் அதிகரிக்கும்`]
          : [`⚠️ ${houseInfo.ta.karaka} பலவீனம்`, `🛡️ பொறுமை தேவை`, `🙏 தொடர்பில் கவனம்`];
      } else if (area === 'career') {
        highlights = score >= 60
          ? [`📈 ${houseInfo.ta.house} பலமாக`, `💼 வளர்ச்சி வாய்ப்புகள்`, `🏆 முயற்சி வெற்றி`]
          : [`⚠️ வேலை சுமை அதிகம்`, `🛡️ மோதல்களைத் தவிர்க்கவும்`, `⏸️ பெரிய மாற்றங்கள் வேண்டாம்`];
      } else if (area === 'education') {
        highlights = score >= 60
          ? [`📚 கற்றல் எளிது`, `🧠 நினைவாற்றல் சிறப்பு`, `🎓 தேர்வு வெற்றி`]
          : [`⚠️ கவனம் சிதறும்`, `📅 திட்டமிடல் அவசியம்`, `💪 கூடுதல் முயற்சி தேவை`];
      } else if (area === 'family') {
        highlights = score >= 60
          ? [`🏠 வீட்டில் மகிழ்ச்சி`, `👨‍👩‍👧‍👦 ஒற்றுமை`, `💝 அன்பு பெருகும்`]
          : [`⚠️ கருத்து வேறுபாடுகள்`, `🕊️ சமரசம் தேவை`, `🙏 பொறுமை முக்கியம்`];
      } else if (area === 'health') {
        highlights = score >= 60
          ? [`💪 ஆற்றல் அதிகம்`, `😊 மன அமைதி`, `🏃 உடற்பயிற்சி நல்லது`]
          : [`⚠️ ஓய்வு எடுங்கள்`, `🏥 பரிசோதனை செய்யுங்கள்`, `🧘 மன அழுத்தம் குறைக்கவும்`];
      } else {
        highlights = score >= 60
          ? [`✨ சாதகமான காலம்`, `📈 முன்னேற்றம்`, `🎯 இலக்குகள் அடையலாம்`]
          : [`⚠️ கவனமாக இருங்கள்`, `⏸️ பெரிய முடிவுகள் வேண்டாம்`, `🙏 பொறுமை தேவை`];
      }
    } else {
      if (area === 'love') {
        highlights = score >= 60
          ? [`💕 ${houseInfo.karaka} is strong in your chart`, `🤝 Relationships will flourish`, `💫 Understanding deepens`]
          : [`⚠️ ${houseInfo.karaka} needs strengthening`, `🛡️ Patience required`, `🙏 Focus on communication`];
      } else if (area === 'career') {
        highlights = score >= 60
          ? [`📈 House ${houseInfo.house} is well-placed`, `💼 Growth opportunities ahead`, `🏆 Efforts will be recognized`]
          : [`⚠️ Heavy workload expected`, `🛡️ Avoid workplace conflicts`, `⏸️ Delay major changes`];
      } else if (area === 'education') {
        highlights = score >= 60
          ? [`📚 Learning comes easy`, `🧠 Sharp memory and focus`, `🎓 Success in exams`]
          : [`⚠️ Concentration may waver`, `📅 Study plan essential`, `💪 Extra effort needed`];
      } else if (area === 'family') {
        highlights = score >= 60
          ? [`🏠 Harmony at home`, `👨‍👩‍👧‍👦 Family unity strong`, `💝 Love and bonding increase`]
          : [`⚠️ Differences may arise`, `🕊️ Compromise needed`, `🙏 Patience is key`];
      } else if (area === 'health') {
        highlights = score >= 60
          ? [`💪 Energy levels high`, `😊 Mental peace`, `🏃 Good time for fitness`]
          : [`⚠️ Take adequate rest`, `🏥 Get checkups done`, `🧘 Reduce stress`];
      } else {
        highlights = score >= 60
          ? [`✨ Favorable period`, `📈 Progress expected`, `🎯 Goals achievable`]
          : [`⚠️ Be cautious`, `⏸️ Delay major decisions`, `🙏 Patience needed`];
      }
    }
  }

  // Build advice based on dasha lord + area + score
  const dashaAdvice = {
    'Sun': { good: 'leadership', bad: 'ego', ta_good: 'தலைமை', ta_bad: 'கர்வம்' },
    'Moon': { good: 'intuition', bad: 'emotions', ta_good: 'உள்ளுணர்வு', ta_bad: 'உணர்ச்சி' },
    'Mars': { good: 'action', bad: 'aggression', ta_good: 'செயல்பாடு', ta_bad: 'கோபம்' },
    'Mercury': { good: 'communication', bad: 'overthinking', ta_good: 'தொடர்பு', ta_bad: 'அதிக சிந்தனை' },
    'Jupiter': { good: 'wisdom', bad: 'overconfidence', ta_good: 'ஞானம்', ta_bad: 'அதிக நம்பிக்கை' },
    'Venus': { good: 'harmony', bad: 'indulgence', ta_good: 'இணக்கம்', ta_bad: 'ஆடம்பரம்' },
    'Saturn': { good: 'discipline', bad: 'delays', ta_good: 'ஒழுக்கம்', ta_bad: 'தாமதம்' },
    'Rahu': { good: 'ambition', bad: 'confusion', ta_good: 'லட்சியம்', ta_bad: 'குழப்பம்' },
    'Ketu': { good: 'spirituality', bad: 'detachment', ta_good: 'ஆன்மீகம்', ta_bad: 'பற்றின்மை' },
  };

  const dInfo = dashaAdvice[dashaLord] || dashaAdvice['Jupiter'];

  if (lang === 'ta') {
    if (score >= 60) {
      advice = `${dashaLord || 'கிரக'} காலத்தில் ${dInfo.ta_good} பயன்படுத்துங்கள். `;
      if (area === 'love') advice += 'உறவுகளில் நேர்மையாக இருங்கள்.';
      else if (area === 'career') advice += 'புதிய வாய்ப்புகளை தேடுங்கள்.';
      else if (area === 'education') advice += 'கற்றலில் தொடர்ந்து கவனம் செலுத்துங்கள்.';
      else if (area === 'family') advice += 'குடும்பத்துடன் நேரம் செலவிடுங்கள்.';
      else if (area === 'health') advice += 'உடற்பயிற்சியை தொடருங்கள்.';
      else advice += 'இந்த சாதகமான நேரத்தை பயன்படுத்துங்கள்.';
    } else {
      advice = `${dInfo.ta_bad} தவிர்க்கவும். `;
      if (area === 'love') advice += 'பொறுமையாக இருங்கள், சண்டையை தவிர்க்கவும்.';
      else if (area === 'career') advice += 'வேலையில் கவனமாக இருங்கள், மாற்றங்களை தள்ளி வையுங்கள்.';
      else if (area === 'education') advice += 'திட்டமிட்டு படியுங்கள், கவனச்சிதறலை தவிர்க்கவும்.';
      else if (area === 'family') advice += 'சமரசத்துடன் இருங்கள், கோபத்தை கட்டுப்படுத்துங்கள்.';
      else if (area === 'health') advice += 'ஓய்வு எடுங்கள், கடினமான உடற்பயிற்சியை தவிர்க்கவும்.';
      else advice += 'பெரிய முடிவுகளை தள்ளி வையுங்கள்.';
    }
  } else {
    if (score >= 60) {
      advice = `Use the ${dInfo.good} energy of ${dashaLord || 'this'} period. `;
      if (area === 'love') advice += 'Be open and honest in relationships.';
      else if (area === 'career') advice += 'Explore new opportunities and take initiative.';
      else if (area === 'education') advice += 'Maintain focus and consistency in studies.';
      else if (area === 'family') advice += 'Spend quality time with loved ones.';
      else if (area === 'health') advice += 'Continue your fitness routine.';
      else advice += 'Take advantage of this favorable period.';
    } else {
      advice = `Watch out for ${dInfo.bad} tendencies. `;
      if (area === 'love') advice += 'Be patient, avoid arguments.';
      else if (area === 'career') advice += 'Be careful at work, delay major changes.';
      else if (area === 'education') advice += 'Follow a strict study schedule, avoid distractions.';
      else if (area === 'family') advice += 'Practice compromise, control temper.';
      else if (area === 'health') advice += 'Take rest, avoid strenuous activities.';
      else advice += 'Delay major decisions.';
    }
  }

  return { summary, highlights, advice, scoreLevel, area };
};

// Score Justification Modal with Tabs
const ScoreJustificationModal = ({ visible, onClose, data, t, language = 'en' }) => {
  const [activeTab, setActiveTab] = useState('summary'); // 'summary' or 'detailed'

  if (!data) return null;

  const breakdown = data.breakdown || {};
  const trace = data.calculation_trace || {};
  const stepByStep = trace.step_by_step || [];
  const aiSummary = generateAISummary(data, data.score, t, language);

  return (
    <Modal transparent visible={visible} animationType="slide">
      <View style={styles.modalOverlay}>
        <ScrollView style={styles.modalScrollView} contentContainerStyle={{ paddingBottom: 100 }}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <View style={[styles.modalIconBg, { backgroundColor: (data.color || '#f97316') + '20' }]}>
                <Ionicons name={data.icon || 'star'} size={28} color={data.color || '#f97316'} />
              </View>
              <Text style={styles.modalTitle}>{data.title || data.name}</Text>
              <TouchableOpacity style={styles.modalCloseBtn} onPress={onClose}>
                <Ionicons name="close" size={24} color="#6b7280" />
              </TouchableOpacity>
            </View>

            <View style={styles.modalScoreSection}>
              <Text style={[styles.modalScoreValue, { color: data.color || '#f97316' }]}>{data.score}</Text>
              <Text style={styles.modalScoreMax}>/100</Text>
            </View>

            {data.quality && (
              <View style={[styles.qualityBadge, { backgroundColor: data.score >= 70 ? '#dcfce7' : data.score >= 50 ? '#fef3c7' : '#fee2e2' }]}>
                <Text style={[styles.qualityText, { color: data.score >= 70 ? '#166534' : data.score >= 50 ? '#a16207' : '#dc2626' }]}>
                  {data.quality}
                </Text>
              </View>
            )}

            {/* Tab Switcher */}
            <View style={styles.modalTabContainer}>
              <TouchableOpacity
                style={[styles.modalTab, activeTab === 'summary' && styles.modalTabActive]}
                onPress={() => setActiveTab('summary')}
              >
                <Ionicons name="bulb" size={16} color={activeTab === 'summary' ? '#f97316' : '#9ca3af'} />
                <Text style={[styles.modalTabText, activeTab === 'summary' && styles.modalTabTextActive]}>
                  {t('aiSummary') || 'AI Summary'}
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.modalTab, activeTab === 'detailed' && styles.modalTabActive]}
                onPress={() => setActiveTab('detailed')}
              >
                <Ionicons name="analytics" size={16} color={activeTab === 'detailed' ? '#f97316' : '#9ca3af'} />
                <Text style={[styles.modalTabText, activeTab === 'detailed' && styles.modalTabTextActive]}>
                  {t('detailed') || 'Detailed'}
                </Text>
              </TouchableOpacity>
            </View>

            {/* AI Summary Tab Content */}
            {activeTab === 'summary' && (
              <View style={styles.aiSummaryContainer}>
                {/* Summary Card */}
                <View style={[styles.aiSummaryCard, {
                  backgroundColor: aiSummary.scoreLevel === 'excellent' ? '#f0fdf4' :
                                   aiSummary.scoreLevel === 'good' ? '#eff6ff' :
                                   aiSummary.scoreLevel === 'moderate' ? '#fffbeb' : '#fef2f2',
                  borderColor: aiSummary.scoreLevel === 'excellent' ? '#86efac' :
                               aiSummary.scoreLevel === 'good' ? '#93c5fd' :
                               aiSummary.scoreLevel === 'moderate' ? '#fde68a' : '#fecaca',
                }]}>
                  <View style={styles.aiSummaryHeader}>
                    <Ionicons name="sparkles" size={20} color="#f97316" />
                    <Text style={styles.aiSummaryTitle}>{t('whatThisMeans') || 'What This Means'}</Text>
                  </View>
                  <Text style={styles.aiSummaryText}>{aiSummary.summary}</Text>
                </View>

                {/* Highlights */}
                <View style={styles.aiHighlightsContainer}>
                  <Text style={styles.aiHighlightsTitle}>{t('keyTakeaways') || 'Key Takeaways'}</Text>
                  {aiSummary.highlights.map((highlight, i) => (
                    <View key={i} style={styles.aiHighlightItem}>
                      <Text style={styles.aiHighlightText}>{highlight}</Text>
                    </View>
                  ))}
                </View>

                {/* Advice Card */}
                <View style={styles.aiAdviceCard}>
                  <View style={styles.aiAdviceHeader}>
                    <Ionicons name="hand-right" size={18} color="#8b5cf6" />
                    <Text style={styles.aiAdviceTitle}>{t('whatToDo') || 'What You Can Do'}</Text>
                  </View>
                  <Text style={styles.aiAdviceText}>{aiSummary.advice}</Text>
                </View>

                {/* Dasha Info in simple terms */}
                {(data.dasha_lord || data.bhukti_lord) && (
                  <View style={styles.aiDashaCard}>
                    <View style={styles.aiDashaHeader}>
                      <Ionicons name="time" size={16} color="#8b5cf6" />
                      <Text style={styles.aiDashaTitle}>{t('currentPeriod') || 'Current Period'}</Text>
                    </View>
                    <Text style={styles.aiDashaText}>
                      {t('youAreIn') || "You're in"} <Text style={styles.aiDashaBold}>{data.dasha_lord_label || data.dasha_lord}</Text> {t('periodWhichInfluences') || 'period, which influences your overall energy and opportunities.'}
                    </Text>
                  </View>
                )}

                {/* Suggestion if available */}
                {(data.suggestion || data.recommendation) && (
                  <View style={styles.suggestionBox}>
                    <Ionicons name="bulb" size={18} color="#f97316" />
                    <Text style={styles.suggestionText}>{data.suggestion || data.recommendation}</Text>
                  </View>
                )}
              </View>
            )}

            {/* Detailed Tab Content */}
            {activeTab === 'detailed' && (
              <>
                {/* Dasha/Bhukti Info */}
                {(data.dasha_lord || data.bhukti_lord) && (
                  <View style={styles.dashaInfoBox}>
                    <Ionicons name="time" size={16} color="#8b5cf6" />
                    <Text style={styles.dashaInfoText}>
                      {data.dasha_lord_label || data.dasha_lord} {t('dashaLabel')} {data.bhukti_lord ? `- ${data.bhukti_lord_label || data.bhukti_lord} ${t('bhuktiLabel')}` : ''}
                    </Text>
                  </View>
                )}

                <View style={styles.modalDivider} />

                {/* Detailed Breakdown Section */}
                {stepByStep.length > 0 && (
                  <>
                    <Text style={styles.modalSectionTitle}><Ionicons name="bar-chart" size={16} color="#ea580c" /> {t('scoreCalculation')}</Text>
                    <Text style={styles.formulaText}>{trace.formula}</Text>

                    {stepByStep.map((step, i) => {
                      const compInfo = COMPONENT_KEYS[step.component] || { key: step.component, icon: 'help', color: '#6b7280' };
                      return (
                        <View key={i} style={styles.breakdownCard}>
                          <View style={styles.breakdownHeader}>
                            <View style={[styles.breakdownIconBg, { backgroundColor: compInfo.color + '20' }]}>
                              <Ionicons name={compInfo.icon} size={16} color={compInfo.color} />
                            </View>
                            <View style={styles.breakdownTitleRow}>
                              <Text style={styles.breakdownTitle}>{t(compInfo.key) || step.component_label || step.component}</Text>
                              <Text style={styles.breakdownWeight}>({step.weight})</Text>
                            </View>
                            <Text style={[styles.breakdownContribution, { color: compInfo.color }]}>
                              {step.contribution}
                            </Text>
                          </View>

                          {/* Progress bar for contribution */}
                          <View style={styles.breakdownProgressBg}>
                            <View style={[styles.breakdownProgressFill, {
                              width: `${Math.min(100, step.contribution * 3.33)}%`,
                              backgroundColor: compInfo.color
                            }]} />
                          </View>

                          {/* Factors for this component */}
                          {step.factors_detail && step.factors_detail.length > 0 && (
                            <View style={styles.breakdownFactors}>
                              {step.factors_detail.slice(0, 3).map((f, j) => (
                                <View key={j} style={styles.miniFactorRow}>
                                  <Ionicons
                                    name={f.positive !== false ? 'add-circle' : 'remove-circle'}
                                    size={12}
                                    color={f.positive !== false ? '#16a34a' : '#dc2626'}
                                  />
                                  <Text style={styles.miniFactorText} numberOfLines={1}>
                                    {f.name}{f.detail ? ` (${f.detail})` : ''}
                                  </Text>
                                  <Text style={[styles.miniFactorValue, { color: f.positive !== false ? '#16a34a' : '#dc2626' }]}>
                                    {f.positive !== false ? '+' : ''}{f.value}
                                  </Text>
                                </View>
                              ))}
                            </View>
                          )}
                        </View>
                      );
                    })}

                    {/* Final Calculation */}
                    {trace.final_calculation && (
                      <View style={styles.finalCalcBox}>
                        <Text style={styles.finalCalcLabel}>{t('total')}:</Text>
                        <Text style={styles.finalCalcFormula}>{trace.final_calculation.sum_of_contributions}</Text>
                        <Text style={styles.finalCalcResult}>= {trace.final_calculation.total}%</Text>
                      </View>
                    )}
                  </>
                )}

                {/* Simple Breakdown (if no detailed trace) */}
                {stepByStep.length === 0 && Object.keys(breakdown).length > 0 && (
                  <>
                    <Text style={styles.modalSectionTitle}><Ionicons name="bar-chart" size={16} color="#ea580c" /> {t('scoreBreakdown')}</Text>
                    {Object.entries(breakdown).map(([key, value], i) => {
                      const compInfo = COMPONENT_KEYS[key] || { key: key, icon: 'help', color: '#6b7280' };
                      return (
                        <View key={i} style={styles.simpleBreakdownRow}>
                          <View style={styles.simpleBreakdownLeft}>
                            <Ionicons name={compInfo.icon} size={14} color={compInfo.color} />
                            <Text style={styles.simpleBreakdownLabel}>{t(compInfo.key) || key}</Text>
                          </View>
                          <View style={styles.simpleBreakdownRight}>
                            <View style={[styles.simpleProgressBg]}>
                              <View style={[styles.simpleProgressFill, {
                                width: `${Math.min(100, value * 3.33)}%`,
                                backgroundColor: compInfo.color
                              }]} />
                            </View>
                            <Text style={styles.simpleBreakdownValue}>{value}</Text>
                          </View>
                        </View>
                      );
                    })}
                  </>
                )}

                {/* Factors Section (for simple factor display) */}
                {data.factors && data.factors.length > 0 && stepByStep.length === 0 && (
                  <>
                    <View style={styles.modalDivider} />
                    <Text style={styles.modalSectionTitle}><Ionicons name="trending-up" size={16} color="#ea580c" /> {t('keyFactors')}</Text>
                    {data.factors.map((factor, i) => (
                      <View key={i} style={styles.factorItem}>
                        <View style={styles.factorHeader}>
                          <Ionicons name={factor.positive ? 'add-circle' : 'remove-circle'} size={18} color={factor.positive ? '#16a34a' : '#dc2626'} />
                          <Text style={styles.factorName}>{factor.name}</Text>
                          <Text style={[styles.factorScore, { color: factor.positive ? '#16a34a' : '#dc2626' }]}>
                            {factor.positive ? '+' : ''}{factor.value}
                          </Text>
                        </View>
                        {factor.detail && <Text style={styles.factorDesc}>{factor.detail}</Text>}
                      </View>
                    ))}
                  </>
                )}

                {/* Area Scores (for yearly) */}
                {data.area_scores && Object.keys(data.area_scores).length > 0 && (
                  <>
                    <View style={styles.modalDivider} />
                    <Text style={styles.modalSectionTitle}><Ionicons name="compass" size={16} color="#ea580c" /> {t('lifeAreasLabel')}</Text>
                    <View style={styles.areaScoresGrid}>
                      {Object.entries(data.area_scores).map(([area, score], i) => {
                        const areaInfo = AREA_KEYS[area] || { key: area, icon: 'help', color: '#6b7280' };
                        return (
                          <View key={i} style={[styles.areaScoreCard, { borderColor: areaInfo.color + '40' }]}>
                            <Ionicons name={areaInfo.icon} size={16} color={areaInfo.color} />
                            <Text style={styles.areaScoreLabel}>{t(areaInfo.key) || area}</Text>
                            <Text style={[styles.areaScoreValue, { color: areaInfo.color }]}>{score}%</Text>
                          </View>
                        );
                      })}
                    </View>
                  </>
                )}

                {/* Positives Section */}
                {data.positives && data.positives.length > 0 && (
                  <>
                    <View style={styles.modalDivider} />
                    <Text style={styles.modalSectionTitle}><Ionicons name="sparkles" size={16} color="#ea580c" /> {t('goodOpportunities')}</Text>
                    {data.positives.map((positive, i) => (
                      <View key={i} style={styles.positiveItem}>
                        <View style={styles.positiveIconBg}>
                          <Ionicons name={positive.icon || 'checkmark-circle'} size={20} color="#16a34a" />
                        </View>
                        <View style={styles.positiveContent}>
                          <Text style={styles.positiveTitle}>{positive.title}</Text>
                          <Text style={styles.positiveDesc}>{positive.description}</Text>
                        </View>
                      </View>
                    ))}
                  </>
                )}

                {/* Remedies Section */}
                {data.remedies && data.remedies.length > 0 && (
                  <>
                    <View style={styles.modalDivider} />
                    <Text style={styles.modalSectionTitle}><Ionicons name="leaf" size={16} color="#ea580c" /> {t('remediesLabel')}</Text>
                    <View style={styles.remediesBox}>
                      {data.remedies.map((remedy, i) => (
                        <View key={i} style={styles.remedyItem}>
                          <Ionicons name="chevron-forward" size={14} color="#f97316" />
                          <Text style={styles.remedyText}>{remedy}</Text>
                        </View>
                      ))}
                    </View>
                  </>
                )}

                {/* Suggestion/Recommendation Section */}
                {(data.suggestion || data.recommendation) && (
                  <View style={styles.suggestionBox}>
                    <Ionicons name="bulb" size={18} color="#f97316" />
                    <Text style={styles.suggestionText}>{data.suggestion || data.recommendation}</Text>
                  </View>
                )}
              </>
            )}

            <TouchableOpacity style={styles.modalButton} onPress={onClose}>
              <Text style={styles.modalButtonText}>{t('ok')}</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </View>
    </Modal>
  );
};

// Timeline Year Detail Modal (Enhanced)
const TimelineYearModal = ({ visible, onClose, data, language, t }) => {
  if (!data) return null;

  const scores = data.scores || {};
  const trace = data.calculation_trace || {};
  const factors = data.factors || [];
  const events = data.events || [];
  const insight = data.insight || {};

  const isPeak = data.period_type === 'high';
  const isLow = data.period_type === 'low';
  const scoreColor = isPeak ? '#22c55e' : isLow ? '#ef4444' : '#3b82f6';

  const lifeAreas = [
    { key: 'career', label: t('career'), color: '#3b82f6', icon: 'briefcase' },
    { key: 'relationships', label: t('relationships'), color: '#ec4899', icon: 'heart' },
    { key: 'finances', label: t('finances'), color: '#22c55e', icon: 'cash' },
    { key: 'health', label: t('health'), color: '#f97316', icon: 'fitness' },
  ];

  return (
    <Modal transparent visible={visible} animationType="slide">
      <View style={styles.modalOverlay}>
        <ScrollView style={styles.modalScrollView}>
          <View style={styles.modalContent}>
            {/* Header */}
            <View style={styles.modalHeader}>
              <View style={[styles.modalIconBg, { backgroundColor: scoreColor + '20' }]}>
                <Text style={{ fontSize: 24, fontWeight: 'bold', color: scoreColor }}>{data.year}</Text>
              </View>
              <View style={{ flex: 1 }}>
                <Text style={styles.modalTitle}>{data.year} - {t('age')} {data.age}</Text>
                <Text style={{ fontSize: 12, color: '#8b5cf6', marginTop: 2 }}>
                  {translateDashaName(data.dasha_tamil || data.dasha, language, t)} {t('dasha')}
                </Text>
              </View>
              <TouchableOpacity style={styles.modalCloseBtn} onPress={onClose}>
                <Ionicons name="close" size={24} color="#6b7280" />
              </TouchableOpacity>
            </View>

            {/* Overall Score */}
            <View style={styles.modalScoreSection}>
              <Text style={[styles.modalScoreValue, { color: scoreColor }]}>{Math.round(data.overall_score)}</Text>
              <Text style={styles.modalScoreMax}>/100</Text>
            </View>

            <View style={[styles.qualityBadge, { backgroundColor: scoreColor + '20' }]}>
              <Text style={[styles.qualityText, { color: scoreColor }]}>
                {isPeak ? t('peakYear') :
                 isLow ? t('challenging') :
                 t('normalYear')}
              </Text>
            </View>

            <View style={styles.modalDivider} />

            {/* Life Area Breakdown */}
            <Text style={styles.modalSectionTitle}><Ionicons name="grid" size={16} color="#ea580c" /> {t('lifeAreasBreakdown')}</Text>
            <View style={styles.tlmAreaContainer}>
              {lifeAreas.map((area) => {
                const score = scores[area.key] || 0;
                return (
                  <View key={area.key} style={styles.tlmAreaRow}>
                    <View style={styles.tlmAreaInfo}>
                      <Ionicons name={area.icon} size={16} color={area.color} />
                      <Text style={styles.tlmAreaLabel}>{area.label}</Text>
                    </View>
                    <View style={styles.tlmAreaBarBg}>
                      <View style={[styles.tlmAreaBarFill, { width: `${score}%`, backgroundColor: area.color }]} />
                    </View>
                    <Text style={[styles.tlmAreaScore, { color: area.color }]}>{Math.round(score)}%</Text>
                  </View>
                );
              })}
            </View>

            {/* Calculation Trace */}
            {trace.formula && (
              <>
                <View style={styles.modalDivider} />
                <Text style={styles.modalSectionTitle}><Ionicons name="calculator" size={16} color="#ea580c" /> {t('calculation')}</Text>
                <View style={styles.tlmTraceBox}>
                  <Text style={styles.tlmTraceVersion}>v{trace.engine_version || '2.3'}</Text>
                  <Text style={styles.tlmTraceFormula}>{trace.formula}</Text>
                  {trace.meta_multiplier && trace.meta_multiplier !== 1.0 && (
                    <View style={styles.tlmTraceMeta}>
                      <Ionicons name="flash" size={12} color="#f97316" />
                      <Text style={styles.tlmTraceMetaText}>
                        Meta: ×{trace.meta_multiplier?.toFixed(3) || '1.000'}
                      </Text>
                    </View>
                  )}
                </View>
              </>
            )}

            {/* Contributing Factors */}
            {factors.length > 0 && (
              <>
                <View style={styles.modalDivider} />
                <Text style={styles.modalSectionTitle}><Ionicons name="flash" size={16} color="#ea580c" /> {t('keyFactors')}</Text>
                {factors.slice(0, 5).map((factor, i) => (
                  <View key={i} style={styles.factorItem}>
                    <Ionicons
                      name={factor.positive !== false ? 'add-circle' : 'remove-circle'}
                      size={18}
                      color={factor.positive !== false ? '#16a34a' : '#dc2626'}
                    />
                    <View style={styles.factorContent}>
                      <Text style={styles.factorTitle}>{factor.name}</Text>
                      {factor.detail && <Text style={styles.factorDesc}>{factor.detail}</Text>}
                    </View>
                    <Text style={[styles.factorValue, { color: factor.positive !== false ? '#16a34a' : '#dc2626' }]}>
                      {factor.positive !== false ? '+' : ''}{factor.value}
                    </Text>
                  </View>
                ))}
              </>
            )}

            {/* Events */}
            {events.length > 0 && (
              <>
                <View style={styles.modalDivider} />
                <Text style={styles.modalSectionTitle}><Ionicons name="flag" size={16} color="#ea580c" /> {t('events')}</Text>
                <View style={styles.tlmEventsGrid}>
                  {events.map((event, i) => (
                    <View key={i} style={[styles.tlmEventChip, { backgroundColor: event.color + '20', borderColor: event.color }]}>
                      <Ionicons name={event.icon} size={14} color={event.color} />
                      <Text style={[styles.tlmEventText, { color: event.color }]} numberOfLines={1}>
                        {translateEventLabel(event, language, t)}
                      </Text>
                    </View>
                  ))}
                </View>
              </>
            )}

            {/* Insight */}
            {insight.text && (
              <View style={[styles.suggestionBox, {
                backgroundColor: insight.mood === 'positive' ? '#dcfce720' :
                                 insight.mood === 'challenging' ? '#fee2e220' : '#fef3c720'
              }]}>
                <Ionicons name="bulb" size={18} color={
                  insight.mood === 'positive' ? '#16a34a' :
                  insight.mood === 'challenging' ? '#dc2626' : '#f97316'
                } />
                <Text style={styles.suggestionText}>{insight.text}</Text>
              </View>
            )}

            <TouchableOpacity style={styles.modalButton} onPress={onClose}>
              <Text style={styles.modalButtonText}>{t('ok')}</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </View>
    </Modal>
  );
};

export default function DashboardScreen({ navigation }) {
  const { userProfile } = useAuth();
  const { t, formatDate, language } = useLanguage();
  // language is already 'ta', 'en', or 'kn' from LanguageContext
  const apiLang = language;
  const [currentTime, setCurrentTime] = useState(new Date());
  const [panchangam, setPanchangam] = useState(null);
  const [jathagam, setJathagam] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [showScoreModal, setShowScoreModal] = useState(false);
  const [selectedScoreData, setSelectedScoreData] = useState(null);
  const [projectionView, setProjectionView] = useState('month'); // 'month' or 'year'
  const [lifeTimeline, setLifeTimeline] = useState(null);
  const [selectedTimelineYear, setSelectedTimelineYear] = useState(null);
  const [showTimelineModal, setShowTimelineModal] = useState(false);
  const [planetAura, setPlanetAura] = useState(null);
  const [selectedPlanet, setSelectedPlanet] = useState(null);
  const [transitsMap, setTransitsMap] = useState(null);
  const [dynamicLifeAreas, setDynamicLifeAreas] = useState(null);
  const [dynamicProjections, setDynamicProjections] = useState(null);
  const insets = useSafeAreaInsets();
  const bottomPadding = Platform.OS === 'android' ? Math.max(insets.bottom, 80) : insets.bottom + 80;

  // Header animation
  const headerFadeAnim = useRef(new Animated.Value(0)).current;
  const headerSlideAnim = useRef(new Animated.Value(-20)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(headerFadeAnim, { toValue: 1, duration: 600, useNativeDriver: true }),
      Animated.timing(headerSlideAnim, { toValue: 0, duration: 600, useNativeDriver: true, easing: Easing.out(Easing.ease) }),
    ]).start();
  }, []);

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    fetchData();
  }, [userProfile, language]); // Re-fetch when language changes

  const fetchData = async () => {
    try {
      const panchangamData = await mobileAPI.getPanchangam();
      setPanchangam(panchangamData);

      // Check for birth details - also check alternate property names
      const birthDate = userProfile?.birthDate || userProfile?.birth_date;
      const birthTime = userProfile?.birthTime || userProfile?.birth_time || '12:00';
      const birthPlace = userProfile?.birthPlace || userProfile?.birth_place || 'Chennai';
      const userName = userProfile?.name || 'User';

      console.log('User profile for API calls:', { birthDate, birthTime, birthPlace, userName });

      if (birthDate) {
        const birthDetails = {
          name: userName,
          birthDate: birthDate,
          birthTime: birthTime,
          birthPlace: birthPlace,
        };

        console.log('Fetching personalized data with:', birthDetails);

        // Fetch jathagam first (needed for other calls)
        const jathagamData = await mobileAPI.getJathagam(birthDetails);
        console.log('Jathagam data received:', jathagamData ? 'Yes' : 'No');
        setJathagam(jathagamData);

        // Fetch all data in parallel for better performance
        const [timelineData, auraData, transitsData, lifeAreasData, projectionsData] = await Promise.all([
          // Life Timeline
          mobileAPI.getLifeTimeline(birthDetails, 10).catch(err => {
            console.error('Life Timeline API error:', err);
            return null;
          }),
          // Planet Aura
          mobileAPI.getPlanetAura(birthDetails).catch(err => {
            console.error('Planet Aura API error:', err);
            return null;
          }),
          // Transits Map
          mobileAPI.getTransitsMap(
            birthPlace,
            jathagamData?.rasi || jathagamData?.moon_sign?.rasi || ''
          ).catch(err => {
            console.error('Transits Map API error:', err);
            return null;
          }),
          // Life Areas - pass language for translated content
          mobileAPI.getLifeAreas(birthDetails, apiLang).catch(err => {
            console.error('Life Areas API error:', err);
            return null;
          }),
          // Future Projections - pass language for translated content
          mobileAPI.getFutureProjections(birthDetails, apiLang).catch(err => {
            console.error('Future Projections API error:', err);
            return null;
          }),
        ]);

        console.log('API responses:', {
          timeline: timelineData ? 'Yes' : 'No',
          aura: auraData ? 'Yes' : 'No',
          transits: transitsData ? 'Yes' : 'No',
          lifeAreas: lifeAreasData ? 'Yes' : 'No',
          projections: projectionsData ? 'Yes' : 'No',
          projectionsMonthly: projectionsData?.projections?.monthly?.length || 0,
          projectionsYearly: projectionsData?.projections?.yearly?.length || 0,
        });

        // Set all state
        setLifeTimeline(timelineData);
        setPlanetAura(auraData);
        setTransitsMap(transitsData);
        setDynamicLifeAreas(lifeAreasData);
        setDynamicProjections(projectionsData);

        // Populate unified scoring cache so AstroFeed and UngalJothidan use the same scores
        populateScoreCache(userProfile, lifeAreasData, transitsData, projectionsData);

        // Schedule transit notifications
        if (transitsData) {
          await notificationService.initialize();
          await notificationService.updateTransitNotifications(transitsData);
        }
      } else {
        console.warn('No birth date available in userProfile:', userProfile);
      }
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    fetchData();
  };

  const getCurrentPeriod = () => {
    const hour = currentTime.getHours();
    if (hour >= 15 && hour < 17) return { label: t('rahuKalam'), color: '#dc2626', bg: '#fef2f2' };
    if (hour >= 9 && hour < 11) return { label: t('goodTime'), color: '#16a34a', bg: '#f0fdf4' };
    return { label: t('normalTime'), color: '#ea580c', bg: '#fff7ed' };
  };

  const period = getCurrentPeriod();

  // Area config for colors and icons
  const areaConfig = {
    love: { icon: 'heart', color: '#ec4899', name: t('love') },
    career: { icon: 'briefcase', color: '#3b82f6', name: t('career') },
    education: { icon: 'school', color: '#8b5cf6', name: t('education') },
    family: { icon: 'home', color: '#10b981', name: t('family') },
    health: { icon: 'fitness', color: '#f59e0b', name: t('health') },
  };

  // Get life areas - use dynamic data if available, otherwise fallback
  const getLifeAreas = () => {
    // If dynamic data is available from API, use it
    if (dynamicLifeAreas?.life_areas) {
      const apiAreas = dynamicLifeAreas.life_areas;
      return Object.keys(areaConfig).slice(0, 4).map(areaKey => {
        const area = apiAreas[areaKey];
        const config = areaConfig[areaKey];
        return {
          area: areaKey, // Add area key for AI Summary detection
          name: config.name,
          icon: config.icon,
          score: area?.score || 50,
          color: config.color,
          factors: area?.factors || [],
          suggestion: area?.suggestion || '',
          breakdown: area?.breakdown || {},
          calculation_trace: area?.calculation_trace || {},
          dasha_lord: area?.dasha_lord || dynamicLifeAreas?.dasha_info?.dasha_lord,
          dasha_lord_label: area?.dasha_lord_label || dynamicLifeAreas?.dasha_info?.dasha_lord,
          quality: area?.score >= 70 ? t('good') : area?.score >= 50 ? t('average') : t('caution')
        };
      });
    }

    // Fallback static data (should rarely be used now)
    return [
      {
        area: 'love',
        name: t('love'),
        icon: 'heart',
        score: 65,
        color: '#ec4899',
        factors: [],
        suggestion: ''
      },
      {
        area: 'career',
        name: t('career'),
        icon: 'briefcase',
        score: 60,
        color: '#3b82f6',
        factors: [],
        suggestion: ''
      },
      {
        area: 'education',
        name: t('education'),
        icon: 'school',
        score: 68,
        color: '#8b5cf6',
        factors: [],
        suggestion: ''
      },
      {
        area: 'family',
        name: t('family'),
        icon: 'home',
        score: 62,
        color: '#10b981',
        factors: [],
        suggestion: ''
      },
    ];
  };

  const lifeAreas = getLifeAreas();

  // Calculate overall score dynamically from life areas
  const overallScore = lifeAreas.length > 0
    ? Math.round(lifeAreas.reduce((sum, area) => sum + area.score, 0) / lifeAreas.length)
    : 72;

  // Month-wise projections (next 12 months) - uses dynamic API data
  const getMonthProjections = () => {
    // If dynamic projections are available from API, use them
    if (dynamicProjections?.projections?.monthly) {
      console.log('Using DYNAMIC monthly projections from API');
      return dynamicProjections.projections.monthly.map((m, i) => ({
        name: translateMonthName(m.name, t), // Translate month name to user's language
        monthIndex: m.month - 1,
        year: m.year,
        score: m.score,
        quality: m.quality,
        factors: m.factors || [],
        breakdown: m.breakdown || {},
        calculation_trace: m.calculation_trace || {},
        dasha_lord: m.dasha_lord,
        dasha_lord_label: m.dasha_lord_label,
        bhukti_lord: m.bhukti_lord,
        bhukti_lord_label: m.bhukti_lord_label,
        recommendation: m.recommendation || '',
        suggestion: m.recommendation || '',
        isPersonalized: true
      }));
    }

    console.log('Using FALLBACK monthly projections (API data not available)');
    // Fallback to static data if API not available
    const months = [];
    const currentMonth = currentTime.getMonth();
    const monthKeys = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'];
    const baseScores = [72, 68, 75, 82, 70, 78, 65, 80, 73, 85, 77, 71];

    for (let i = 0; i < 12; i++) {
      const monthIndex = (currentMonth + i) % 12;
      const year = currentTime.getFullYear() + Math.floor((currentMonth + i) / 12);
      months.push({
        name: t(monthKeys[monthIndex]),
        monthIndex,
        year,
        score: baseScores[monthIndex],
        factors: [],
        suggestion: ''
      });
    }
    return months;
  };

  // 3-year projections - uses dynamic API data
  const getYearProjections = () => {
    const currentYear = currentTime.getFullYear();
    const icons = ['time-outline', 'trending-up', 'star'];
    const colors = ['#f59e0b', '#10b981', '#8b5cf6'];

    // If dynamic projections are available from API, use them
    if (dynamicProjections?.projections?.yearly) {
      console.log('Using DYNAMIC yearly projections from API');
      // V5.0 DEBUG: Log actual scores from backend
      console.log('V5.0 Year Scores:', dynamicProjections.projections.yearly.map(y => `${y.year}: ${y.score}`).join(', '));
      return dynamicProjections.projections.yearly.map((y, i) => ({
        year: y.year,
        score: y.score,
        label: y.label,
        quality: y.quality,
        icon: icons[i] || 'star',
        color: colors[i] || '#8b5cf6',
        factors: y.factors || [],
        breakdown: y.breakdown || {},
        calculation_trace: y.calculation_trace || {},
        detailed_breakdown: y.detailed_breakdown || {},
        area_scores: y.area_scores || {},
        area_recommendations: y.area_recommendations || {},
        dasha_lord: y.dasha_lord,
        dasha_lord_label: y.dasha_lord_label,
        bhukti_lord: y.bhukti_lord,
        bhukti_lord_label: y.bhukti_lord_label,
        positives: [],
        remedies: [],
        recommendation: y.recommendation || '',
        suggestion: y.recommendation || '',
        isPersonalized: true
      }));
    }

    console.log('Using FALLBACK yearly projections (API data not available)');
    // Fallback to static data
    return [
      {
        year: currentYear,
        score: 68,
        label: t('currentYear'),
        icon: 'time-outline',
        color: '#f59e0b',
        factors: [],
        positives: [],
        remedies: [],
        suggestion: ''
      },
      {
        year: currentYear + 1,
        score: 78,
        label: t('nextYear'),
        icon: 'trending-up',
        color: '#10b981',
        factors: [],
        positives: [],
        remedies: [],
        suggestion: ''
      },
      {
        year: currentYear + 2,
        score: 85,
        label: t('thirdYear'),
        icon: 'star',
        color: '#8b5cf6',
        factors: [],
        positives: [],
        remedies: [],
        suggestion: ''
      },
    ];
  };

  const monthProjections = getMonthProjections();
  const yearProjections = getYearProjections();

  const quickActions = [
    { icon: 'medkit', label: t('remedies'), screen: 'Remedy', color: '#8b5cf6' },
    { icon: 'sparkles', label: t('astroFeed'), screen: 'AstroFeed', color: '#ea580c' },
    { icon: 'heart', label: t('matching'), screen: 'Matching', color: '#ef4444' },
    { icon: 'calendar', label: t('muhurtham'), screen: 'Muhurtham', color: '#16a34a' },
  ];

  const handleScorePress = (data) => {
    setSelectedScoreData({
      ...data,
      title: data.name || t('todayScore'),
    });
    setShowScoreModal(true);
  };

  const handleOverallScorePress = () => {
    setSelectedScoreData({
      title: t('todayScore'),
      score: overallScore,
      icon: 'star',
      color: '#f97316',
      factors: [],
      suggestion: ''
    });
    setShowScoreModal(true);
  };

  const handleMonthPress = (month) => {
    setSelectedScoreData({
      title: `${month.name} ${month.year}`,
      score: month.score,
      quality: month.quality,
      icon: 'calendar',
      color: '#3b82f6',
      factors: month.factors,
      breakdown: month.breakdown,
      calculation_trace: month.calculation_trace,
      dasha_lord: month.dasha_lord,
      dasha_lord_label: month.dasha_lord_label,
      bhukti_lord: month.bhukti_lord,
      bhukti_lord_label: month.bhukti_lord_label,
      suggestion: month.suggestion,
      recommendation: month.recommendation,
      month: month.monthNum || new Date().getMonth() + 1, // For month-specific AI content
      area: 'general' // Monthly projections are general
    });
    setShowScoreModal(true);
  };

  const handleYearPress = (year) => {
    const currentYear = new Date().getFullYear();
    const isCurrentYear = parseInt(year.year) === currentYear;
    const isNextYear = parseInt(year.year) === currentYear + 1;

    setSelectedScoreData({
      title: `${year.year}`,
      score: year.score,
      quality: year.quality,
      icon: year.icon || 'calendar-outline',
      color: year.color || '#8b5cf6',
      factors: year.factors,
      breakdown: year.breakdown,
      calculation_trace: year.calculation_trace,
      detailed_breakdown: year.detailed_breakdown,
      area_scores: year.area_scores,
      area_recommendations: year.area_recommendations,
      dasha_lord: year.dasha_lord,
      dasha_lord_label: year.dasha_lord_label,
      bhukti_lord: year.bhukti_lord,
      bhukti_lord_label: year.bhukti_lord_label,
      positives: year.positives,
      remedies: year.remedies,
      suggestion: year.suggestion,
      recommendation: year.recommendation,
      year: year.year,
      label: isCurrentYear ? 'Current Year' : isNextYear ? 'Next Year' : 'Future Year',
      area: 'general' // Yearly projections are general
    });
    setShowScoreModal(true);
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <View style={{ alignItems: 'center' }}>
          <DiyaIcon size={60} />
          <Text style={styles.loadingText}>{t('loading')}</Text>
        </View>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Warm auspicious gradient background */}
      <LinearGradient colors={['#f0f4f8', '#e5e9f2', '#dfe7f5']} style={styles.gradient}>
        <ScrollView
          contentContainerStyle={[styles.scrollContent, { paddingBottom: bottomPadding }]}
          refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={['#f97316']} tintColor="#f97316" />}
          showsVerticalScrollIndicator={false}
        >
          {/* Top accent bar */}
          <LinearGradient
            colors={['#f97316', '#ea580c', '#f97316']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.headerBar}
          />

          {/* Header */}
          <Animated.View
            style={[
              styles.header,
              { opacity: headerFadeAnim, transform: [{ translateY: headerSlideAnim }] },
            ]}
          >
            <View>
              <View style={styles.logoRow}>
                <View style={styles.logoIcon}>
                  <Svg width={28} height={28} viewBox="0 0 100 100">
                    <Path
                      d="M50 5 L55 40 L90 30 L60 50 L90 70 L55 60 L50 95 L45 60 L10 70 L40 50 L10 30 L45 40 Z"
                      fill="#f97316"
                    />
                    <Circle cx="50" cy="50" r="10" fill="#fff7ed" />
                  </Svg>
                </View>
                <Text style={styles.appTitle}>{t('appName')}</Text>
              </View>
              {userProfile && (
                <View style={styles.userInfo}>
                  <Text style={styles.greeting}>{t('greeting')}, {userProfile.name}</Text>
                  {userProfile.rasi && (
                    <Text style={styles.rasiInfo}>{translateRasiName(userProfile.rasi, t)} • {translateNakshatraName(userProfile.nakshatra, t)}</Text>
                  )}
                </View>
              )}
            </View>
            <View style={styles.timeContainer}>
              <Text style={styles.currentTime}>
                {currentTime.toLocaleTimeString('ta-IN', { hour: '2-digit', minute: '2-digit' })}
              </Text>
              <View style={[styles.periodBadge, { backgroundColor: period.bg }]}>
                <Text style={[styles.periodText, { color: period.color }]}>{period.label}</Text>
              </View>
            </View>
          </Animated.View>

          {/* Rashi Palan Ticker - Shows all 12 zodiac signs with daily scores */}
          <RashiPalanTicker
            transits={transitsMap}
            language={language}
            t={t}
            userRashi={userProfile?.rasi}
            onRashiPress={(rashi) => {
              // Show rashi detail when tapped
              setSelectedScoreData({
                title: rashi.name,
                score: rashi.score,
                icon: 'star',
                color: rashi.score >= 75 ? '#16a34a' : rashi.score >= 60 ? '#f97316' : '#dc2626',
                area: 'general',
                dasha_lord: rashi.ruler,
                dasha_lord_label: rashi.ruler,
                factors: [
                  { description: `${rashi.ruler} is the ruling planet`, type: 'info' },
                  { description: `Element: ${rashi.element}`, type: 'info' },
                ],
              });
              setShowScoreModal(true);
            }}
          />

          {/* Date Display */}
          <AnimatedCard delay={50} style={styles.dateCard}>
            <Text style={styles.dateText}>{formatDate(currentTime)}</Text>
          </AnimatedCard>

          {/* Story Preview Row */}
          <AnimatedCard delay={75}>
            <View style={styles.storyPreviewRow}>
              <View style={styles.storyCirclesContainer}>
                <TouchableOpacity
                  style={[styles.storyCircle, styles.storyCircleActive]}
                  onPress={() => navigation.navigate('AstroFeed', { initialStory: 'planet' })}
                  activeOpacity={0.7}
                >
                  <LinearGradient
                    colors={['#f97316', '#ef4444', '#ec4899']}
                    style={styles.storyGradientBorder}
                  >
                    <View style={styles.storyInner}>
                      <Ionicons name="sunny" size={20} color="#f59e0b" />
                    </View>
                  </LinearGradient>
                  <Text style={styles.storyLabel}>{t('planet')}</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={[styles.storyCircle, styles.storyCircleActive]}
                  onPress={() => navigation.navigate('AstroFeed', { initialStory: 'moon' })}
                  activeOpacity={0.7}
                >
                  <LinearGradient
                    colors={['#8b5cf6', '#6366f1', '#3b82f6']}
                    style={styles.storyGradientBorder}
                  >
                    <View style={styles.storyInner}>
                      <Ionicons name="moon" size={20} color="#a78bfa" />
                    </View>
                  </LinearGradient>
                  <Text style={styles.storyLabel}>{t('moon')}</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={[styles.storyCircle, styles.storyCircleActive]}
                  onPress={() => navigation.navigate('AstroFeed', { initialStory: 'insight' })}
                  activeOpacity={0.7}
                >
                  <LinearGradient
                    colors={['#22c55e', '#16a34a', '#15803d']}
                    style={styles.storyGradientBorder}
                  >
                    <View style={styles.storyInner}>
                      <Ionicons name="sparkles" size={20} color="#22c55e" />
                    </View>
                  </LinearGradient>
                  <Text style={styles.storyLabel}>{t('insight')}</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={[styles.storyCircle, styles.storyCircleActive]}
                  onPress={() => navigation.navigate('AstroFeed', { initialStory: 'star' })}
                  activeOpacity={0.7}
                >
                  <LinearGradient
                    colors={['#f59e0b', '#d97706', '#b45309']}
                    style={styles.storyGradientBorder}
                  >
                    <View style={styles.storyInner}>
                      <Ionicons name="star" size={20} color="#f59e0b" />
                    </View>
                  </LinearGradient>
                  <Text style={styles.storyLabel}>{t('star')}</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={styles.storyCircle}
                  onPress={() => navigation.navigate('AstroFeed')}
                  activeOpacity={0.7}
                >
                  <View style={styles.storyMoreCircle}>
                    <Ionicons name="add" size={24} color="#f97316" />
                  </View>
                  <Text style={styles.storyLabel}>{t('more')}</Text>
                </TouchableOpacity>
              </View>
            </View>
          </AnimatedCard>

          {/* Tamil Calendar */}
          <AnimatedCard delay={100} style={styles.card}>
            <View style={styles.cardHeader}>
              <DiyaIcon size={32} color="#d97706" />
              <Text style={styles.cardTitle}>{t('todayPanchangam')}</Text>
            </View>
            <View style={styles.panchangamGrid}>
              <View style={styles.panchangamItem}>
                <Text style={styles.panchangamLabel}>{t('month')}</Text>
                <Text style={styles.panchangamValue}>{translatePanchangamMonth(panchangam?.tamil_month, t) || '-'}</Text>
              </View>
              <View style={styles.panchangamItem}>
                <Text style={styles.panchangamLabel}>{t('tithi')}</Text>
                <Text style={styles.panchangamValue}>{panchangam?.tithi?.name || '-'}</Text>
              </View>
              <View style={styles.panchangamItem}>
                <Text style={styles.panchangamLabel}>{t('nakshatra')}</Text>
                <Text style={styles.panchangamValue}>{translateNakshatraName(panchangam?.nakshatra?.tamil, t) || '-'}</Text>
              </View>
              <View style={styles.panchangamItem}>
                <Text style={styles.panchangamLabel}>{t('yoga')}</Text>
                <Text style={styles.panchangamValue}>{panchangam?.yoga?.name || '-'}</Text>
              </View>
            </View>
          </AnimatedCard>

          {/* Today's Score */}
          <AnimatedCard delay={200} style={styles.card}>
            <View style={styles.scoreRow}>
              <View>
                <Text style={styles.scoreLabel}>{t('todayScore')}</Text>
                <View style={styles.scoreValue}>
                  <Text style={styles.scoreNumber}>{overallScore}</Text>
                  <Text style={styles.scoreMax}>/100</Text>
                  <View style={[styles.scoreBadge, { backgroundColor: overallScore >= 70 ? '#dcfce7' : '#fef3c7' }]}>
                    <Ionicons name="trending-up" size={14} color={overallScore >= 70 ? '#16a34a' : '#d97706'} />
                    <Text style={[styles.scoreBadgeText, { color: overallScore >= 70 ? '#16a34a' : '#d97706' }]}>
                      {overallScore >= 70 ? t('good') : t('average')}
                    </Text>
                  </View>
                </View>
              </View>
              <AnimatedScoreCircle score={overallScore} onPress={handleOverallScorePress} tapText={t('tap')} />
            </View>

            <LinearGradient colors={['#fff7ed', '#fef3c7']} style={styles.insightBox}>
              <PulsingSparkle />
              <Text style={styles.insightText}>
                {jathagam?.dasha?.mahadasha
                  ? `${t(planetTranslationKeys[jathagam.dasha.mahadasha]) || jathagam.dasha.mahadasha} ${t('dashaRunning')}`
                  : t('defaultInsight')
                }
              </Text>
            </LinearGradient>
          </AnimatedCard>

          {/* Life Areas */}
          <AnimatedCard delay={300} style={styles.card}>
            <View style={styles.cardHeader}>
              <Ionicons name="heart" size={24} color="#ec4899" />
              <Text style={styles.cardTitle}>{t('lifeAreas')}</Text>
              {dynamicLifeAreas?.life_areas ? (
                <View style={{ flexDirection: 'row', alignItems: 'center', marginLeft: 'auto', backgroundColor: '#dcfce7', paddingHorizontal: 8, paddingVertical: 2, borderRadius: 10, marginRight: 8 }}>
                  <Ionicons name="checkmark-circle" size={12} color="#16a34a" />
                  <Text style={{ fontSize: 10, color: '#16a34a', marginLeft: 4 }}>{t('personal')}</Text>
                </View>
              ) : (
                <View style={{ flexDirection: 'row', alignItems: 'center', marginLeft: 'auto', backgroundColor: '#fef3c7', paddingHorizontal: 8, paddingVertical: 2, borderRadius: 10, marginRight: 8 }}>
                  <Ionicons name="information-circle" size={12} color="#d97706" />
                  <Text style={{ fontSize: 10, color: '#d97706', marginLeft: 4 }}>{t('generic')}</Text>
                </View>
              )}
              <Text style={styles.tapHintSmall}>{t('tapForDetails')}</Text>
            </View>
            {/* Row 1 */}
            <View style={styles.lifeAreasRow}>
              {lifeAreas.slice(0, 2).map((area, i) => (
                <TouchableOpacity
                  key={i}
                  style={styles.lifeAreaCard}
                  onPress={() => handleScorePress(area)}
                  activeOpacity={0.8}
                >
                  <View style={styles.lifeAreaHeader}>
                    <View style={[styles.lifeAreaIconBg, { backgroundColor: area.color + '20' }]}>
                      <Ionicons name={area.icon} size={18} color={area.color} />
                    </View>
                    <View style={[styles.lifeAreaBadge, { backgroundColor: area.score >= 75 ? '#dcfce7' : area.score >= 50 ? '#fef3c7' : '#fef2f2' }]}>
                      <Text style={[styles.lifeAreaBadgeText, { color: area.score >= 75 ? '#16a34a' : area.score >= 50 ? '#d97706' : '#dc2626' }]}>
                        {area.score >= 75 ? t('good') : area.score >= 50 ? t('average') : t('caution')}
                      </Text>
                    </View>
                  </View>
                  <Text style={styles.lifeAreaName} numberOfLines={1}>{area.name}</Text>
                  <View style={styles.lifeAreaScoreRow}>
                    <Text style={[styles.lifeAreaScore, { color: area.color }]}>{area.score}</Text>
                    <Text style={styles.lifeAreaMax}>/100</Text>
                    <Ionicons name="chevron-forward" size={14} color="#9ca3af" style={{ marginLeft: 'auto' }} />
                  </View>
                  <View style={styles.lifeAreaProgressBar}>
                    <View style={[styles.lifeAreaProgressFill, { width: `${area.score}%`, backgroundColor: area.color }]} />
                  </View>
                </TouchableOpacity>
              ))}
            </View>
            {/* Row 2 */}
            <View style={styles.lifeAreasRow}>
              {lifeAreas.slice(2, 4).map((area, i) => (
                <TouchableOpacity
                  key={i + 2}
                  style={styles.lifeAreaCard}
                  onPress={() => handleScorePress(area)}
                  activeOpacity={0.8}
                >
                  <View style={styles.lifeAreaHeader}>
                    <View style={[styles.lifeAreaIconBg, { backgroundColor: area.color + '20' }]}>
                      <Ionicons name={area.icon} size={18} color={area.color} />
                    </View>
                    <View style={[styles.lifeAreaBadge, { backgroundColor: area.score >= 75 ? '#dcfce7' : area.score >= 50 ? '#fef3c7' : '#fef2f2' }]}>
                      <Text style={[styles.lifeAreaBadgeText, { color: area.score >= 75 ? '#16a34a' : area.score >= 50 ? '#d97706' : '#dc2626' }]}>
                        {area.score >= 75 ? t('good') : area.score >= 50 ? t('average') : t('caution')}
                      </Text>
                    </View>
                  </View>
                  <Text style={styles.lifeAreaName} numberOfLines={1}>{area.name}</Text>
                  <View style={styles.lifeAreaScoreRow}>
                    <Text style={[styles.lifeAreaScore, { color: area.color }]}>{area.score}</Text>
                    <Text style={styles.lifeAreaMax}>/100</Text>
                    <Ionicons name="chevron-forward" size={14} color="#9ca3af" style={{ marginLeft: 'auto' }} />
                  </View>
                  <View style={styles.lifeAreaProgressBar}>
                    <View style={[styles.lifeAreaProgressFill, { width: `${area.score}%`, backgroundColor: area.color }]} />
                  </View>
                </TouchableOpacity>
              ))}
            </View>
          </AnimatedCard>

          {/* Month & Year Projections */}
          <AnimatedCard delay={350} style={styles.card}>
            <View style={styles.cardHeader}>
              <Ionicons name="analytics" size={16} color="#ea580c" />
              <Text style={styles.cardTitle}>{t('futureProjection')}</Text>
              {dynamicProjections?.projections ? (
                <View style={{ flexDirection: 'row', alignItems: 'center', marginLeft: 'auto', backgroundColor: '#dcfce7', paddingHorizontal: 8, paddingVertical: 2, borderRadius: 10 }}>
                  <Ionicons name="checkmark-circle" size={12} color="#16a34a" />
                  <Text style={{ fontSize: 10, color: '#16a34a', marginLeft: 4 }}>{t('personal')}</Text>
                </View>
              ) : (
                <View style={{ flexDirection: 'row', alignItems: 'center', marginLeft: 'auto', backgroundColor: '#fef3c7', paddingHorizontal: 8, paddingVertical: 2, borderRadius: 10 }}>
                  <Ionicons name="information-circle" size={12} color="#d97706" />
                  <Text style={{ fontSize: 10, color: '#d97706', marginLeft: 4 }}>{t('generic')}</Text>
                </View>
              )}
            </View>

            {/* Toggle Buttons */}
            <View style={styles.projectionToggle}>
              <TouchableOpacity
                style={[styles.toggleBtn, projectionView === 'month' && styles.toggleBtnActive]}
                onPress={() => setProjectionView('month')}
              >
                <Text style={[styles.toggleText, projectionView === 'month' && styles.toggleTextActive]}>{t('monthly')}</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.toggleBtn, projectionView === 'year' && styles.toggleBtnActive]}
                onPress={() => setProjectionView('year')}
              >
                <Text style={[styles.toggleText, projectionView === 'year' && styles.toggleTextActive]}>{t('threeYears')}</Text>
              </TouchableOpacity>
            </View>

            {projectionView === 'month' ? (
              <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.monthsScroll}>
                {monthProjections.map((month, i) => (
                  <MonthProjectionCard key={i} month={month} index={i} onPress={handleMonthPress} />
                ))}
              </ScrollView>
            ) : (
              <View style={styles.yearsGrid}>
                {yearProjections.map((year, i) => (
                  <YearProjectionCard key={i} year={year} onPress={handleYearPress} />
                ))}
              </View>
            )}
          </AnimatedCard>

          {/* Past Years Analysis */}
          {lifeTimeline?.past_years?.length > 0 && (
            <AnimatedCard delay={375} style={styles.card}>
              <View style={styles.cardHeader}>
                <Ionicons name="time-outline" size={16} color="#6b7280" />
                <Text style={styles.cardTitle}>
                  {t('pastYears')}
                </Text>
              </View>
              <View style={styles.pastYearsGrid}>
                {lifeTimeline.past_years.map((yearData, index) => {
                  const scoreColor = yearData.overall_score >= 70 ? '#22c55e' : yearData.overall_score >= 50 ? '#f59e0b' : '#ef4444';
                  return (
                    <TouchableOpacity
                      key={yearData.year}
                      style={styles.pastYearCard}
                      onPress={() => {
                        setSelectedTimelineYear(yearData);
                        setShowTimelineModal(true);
                      }}
                    >
                      <View style={styles.pastYearHeader}>
                        <Text style={styles.pastYearLabel}>{yearData.year}</Text>
                        <View style={[styles.pastYearBadge, { backgroundColor: scoreColor + '20' }]}>
                          <Text style={[styles.pastYearScore, { color: scoreColor }]}>{Math.round(yearData.overall_score)}%</Text>
                        </View>
                      </View>
                      <Text style={styles.pastYearDasha}>
                        {translateDashaName(yearData.dasha_tamil || yearData.dasha, language, t)} {t('dasha')}
                      </Text>
                      <View style={styles.pastYearBar}>
                        <View style={[styles.pastYearBarFill, { width: `${yearData.overall_score}%`, backgroundColor: scoreColor }]} />
                      </View>
                    </TouchableOpacity>
                  );
                })}
              </View>
            </AnimatedCard>
          )}

          {/* Quick Actions */}
          <AnimatedCard delay={400} style={styles.card}>
            <View style={styles.cardHeader}>
              <Ionicons name="flash" size={24} color="#f97316" />
              <Text style={styles.cardTitle}>{t('quickActions')}</Text>
            </View>
            <View style={styles.quickActionsGrid}>
              {quickActions.map((action, i) => (
                <AnimatedQuickAction
                  key={i}
                  action={action}
                  index={i}
                  onPress={() => {
                    // Remedy screen is in root navigator, others are in tab navigator
                    if (action.screen === 'Remedy') {
                      navigation.getParent()?.navigate('Remedy');
                    } else {
                      navigation.navigate(action.screen);
                    }
                  }}
                />
              ))}
            </View>
          </AnimatedCard>

          {/* Today's Parigaram - Gamified Remedies */}
          {planetAura?.challenged_planets?.length > 0 && (
            <AnimatedCard delay={450}>
              <TouchableOpacity
                activeOpacity={0.9}
                onPress={() => navigation.getParent()?.navigate('Remedy')}
              >
                <LinearGradient
                  colors={['#fef3c7', '#fde68a', '#fcd34d']}
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 1 }}
                  style={[styles.card, styles.parigaramCard]}
                >
                  <View style={styles.parigaramHeader}>
                    <View style={styles.parigaramIconBadge}>
                      <Ionicons name="leaf" size={24} color="#92400e" />
                    </View>
                    <View style={styles.parigaramTitleSection}>
                      <Text style={styles.parigaramTitle}>{t('todayParigaram')}</Text>
                      <Text style={styles.parigaramSubtitle}>{t('tapForRemedies')}</Text>
                    </View>
                    <View style={styles.parigaramArrow}>
                      <Ionicons name="chevron-forward" size={20} color="#92400e" />
                    </View>
                  </View>

                  <View style={styles.parigaramPlanets}>
                    {planetAura.challenged_planets.slice(0, 3).map((planet, i) => (
                      <View key={i} style={styles.parigaramPlanetBadge}>
                        <Text style={styles.parigaramPlanetIcon}>
                          {planet.name === 'Saturn' ? '♄' : planet.name === 'Mars' ? '♂' :
                           planet.name === 'Rahu' ? '☊' : planet.name === 'Ketu' ? '☋' :
                           planet.name === 'Sun' ? '☉' : planet.name === 'Moon' ? '☽' : '⭐'}
                        </Text>
                        <Text style={styles.parigaramPlanetName}>
                          {translatePlanetString(planet.tamil, language, t)}
                        </Text>
                      </View>
                    ))}
                  </View>

                  <View style={styles.parigaramQuickTips}>
                    <View style={styles.parigaramTip}>
                      <Ionicons name="flower" size={16} color="#b45309" />
                      <Text style={styles.parigaramTipText}>{t('puja')}</Text>
                    </View>
                    <View style={styles.parigaramTip}>
                      <Ionicons name="water" size={16} color="#b45309" />
                      <Text style={styles.parigaramTipText}>{t('charity')}</Text>
                    </View>
                    <View style={styles.parigaramTip}>
                      <Ionicons name="musical-notes" size={16} color="#b45309" />
                      <Text style={styles.parigaramTipText}>{t('mantra')}</Text>
                    </View>
                  </View>
                </LinearGradient>
              </TouchableOpacity>
            </AnimatedCard>
          )}

          {/* Current Dasha */}
          {jathagam?.dasha?.mahadasha && (
            <AnimatedCard delay={500}>
              <LinearGradient colors={['#faf5ff', '#eef2ff']} style={[styles.card, styles.dashaCard]}>
                <View style={styles.cardHeader}>
                  <Ionicons name="sparkles" size={16} color="#7c3aed" />
                  <Text style={[styles.cardTitle, { color: '#6b21a8' }]}>{t('currentDasha')}</Text>
                </View>
                <View style={styles.dashaGrid}>
                  <View style={styles.dashaItem}>
                    <Text style={styles.dashaLabel}>{t('mahaDasha')}</Text>
                    <Text style={styles.dashaValue}>
                      {t(planetTranslationKeys[jathagam.dasha.mahadasha]) || jathagam.dasha.mahadasha}
                    </Text>
                  </View>
                  {jathagam.dasha.antardasha && (
                    <View style={styles.dashaItem}>
                      <Text style={styles.dashaLabel}>{t('antarDasha')}</Text>
                      <Text style={styles.dashaValue}>
                        {t(planetTranslationKeys[jathagam.dasha.antardasha]) || jathagam.dasha.antardasha}
                      </Text>
                    </View>
                  )}
                </View>
              </LinearGradient>
            </AnimatedCard>
          )}

          {/* Chakra Analysis Section */}
          <AnimatedCard delay={550}>
            <TouchableOpacity
              activeOpacity={0.85}
              onPress={() => navigation.navigate('Chakra')}
            >
              <LinearGradient
                colors={['#1e1b4b', '#4c1d95', '#5b21b6']}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
                style={[styles.card, styles.chakraCard]}
              >
                <View style={styles.chakraCardHeader}>
                  <View style={styles.chakraIconContainer}>
                    <Text style={styles.chakraIconLarge}>🧘</Text>
                  </View>
                  <View style={styles.chakraCardInfo}>
                    <Text style={styles.chakraCardTitle}>
                      {language === 'ta' ? 'சக்ர பகுப்பாய்வு' : 'Chakra Analysis'}
                    </Text>
                    <Text style={styles.chakraCardSubtitle}>
                      {language === 'ta' ? '7 சக்ரங்கள் • ஜோதிட அடிப்படையில்' : '7 Chakras • Jyotish Based'}
                    </Text>
                  </View>
                  <View style={styles.chakraArrowContainer}>
                    <Ionicons name="chevron-forward" size={24} color="#c4b5fd" />
                  </View>
                </View>

                {/* Chakra Mini Preview with Scores */}
                <View style={styles.chakraMiniPreview}>
                  {[
                    { color: '#9333ea', score: 72, name: 'Crown', nameTa: 'கிரீடம்' },
                    { color: '#4f46e5', score: 68, name: 'Third Eye', nameTa: '3வது கண்' },
                    { color: '#0ea5e9', score: 61, name: 'Throat', nameTa: 'தொண்டை' },
                    { color: '#22c55e', score: 78, name: 'Heart', nameTa: 'இதயம்' },
                    { color: '#eab308', score: 65, name: 'Solar', nameTa: 'சூரியன்' },
                    { color: '#f97316', score: 58, name: 'Sacral', nameTa: 'சேக்ரல்' },
                    { color: '#ef4444', score: 70, name: 'Root', nameTa: 'வேர்' },
                  ].map((chakra, idx) => (
                    <View key={idx} style={styles.chakraMiniItem}>
                      <View style={[styles.chakraMiniCircle, { backgroundColor: chakra.color }]}>
                        <Text style={styles.chakraMiniScore}>{chakra.score}</Text>
                      </View>
                      <Text style={styles.chakraMiniName}>
                        {language === 'ta' ? chakra.nameTa : chakra.name}
                      </Text>
                    </View>
                  ))}
                </View>

                {/* Overall Energy */}
                <View style={styles.chakraEnergyRow}>
                  <View style={styles.chakraEnergyInfo}>
                    <Ionicons name="flash" size={14} color="#a855f7" />
                    <Text style={styles.chakraEnergyLabel}>
                      {language === 'ta' ? 'ஒட்டுமொத்த ஆற்றல்' : 'Overall Energy'}
                    </Text>
                  </View>
                  <View style={styles.chakraEnergyBar}>
                    <View style={[styles.chakraEnergyFill, { width: '67%' }]} />
                  </View>
                  <Text style={styles.chakraEnergyPercent}>67%</Text>
                </View>

                <View style={styles.chakraCardFooter}>
                  <Text style={styles.chakraCardHint}>
                    {language === 'ta' ? 'விரிவான பகுப்பாய்வுக்கு தட்டவும்' : 'Tap for detailed analysis'}
                  </Text>
                  <View style={styles.chakraNewBadge}>
                    <Text style={styles.chakraNewText}>NEW</Text>
                  </View>
                </View>
              </LinearGradient>
            </TouchableOpacity>
          </AnimatedCard>

          {/* Aura Heatmap - Planet Strength Visualization */}
          {planetAura && (
            <AnimatedCard delay={600}>
              <LinearGradient colors={['#1e1b4b', '#312e81']} style={[styles.card, styles.auraCard]}>
                <View style={styles.cardHeader}>
                  <Ionicons name="planet" size={16} color="#a78bfa" />
                  <Text style={[styles.cardTitle, { color: '#fff' }]}>
                    {t('planetAuraMap')}
                  </Text>
                  <View style={[styles.auraBadge, { backgroundColor: planetAura.overall?.aura_color + '30' }]}>
                    <Text style={[styles.auraBadgeText, { color: planetAura.overall?.aura_color }]}>
                      {planetAura.overall?.aura_score}%
                    </Text>
                  </View>
                </View>

                {/* Overall Aura Status */}
                <View style={styles.auraOverview}>
                  <View style={[styles.auraLevelBadge, { backgroundColor: planetAura.overall?.aura_color + '20' }]}>
                    <Text style={[styles.auraLevelText, { color: planetAura.overall?.aura_color }]}>
                      {translateAuraLevel(planetAura.overall?.aura_tamil, t) || planetAura.overall?.aura_label}
                    </Text>
                  </View>
                  <View style={styles.auraStats}>
                    <View style={styles.auraStat}>
                      <Ionicons name="checkmark-circle" size={14} color="#22c55e" />
                      <Text style={styles.auraStatText}>{planetAura.overall?.favorable_count}</Text>
                    </View>
                    <View style={styles.auraStat}>
                      <Ionicons name="alert-circle" size={14} color="#ef4444" />
                      <Text style={styles.auraStatText}>{planetAura.overall?.unfavorable_count}</Text>
                    </View>
                  </View>
                </View>

                {/* Radial Heatmap - Circular Planet Layout */}
                <View style={styles.auraRadialContainer}>
                  {/* Center Circle */}
                  <View style={styles.auraCenterCircle}>
                    <Text style={styles.auraCenterScore}>{planetAura.overall?.aura_score}</Text>
                    <Text style={styles.auraCenterLabel}>{t('aura')}</Text>
                  </View>

                  {/* Planet Rings */}
                  {planetAura.planets?.map((planet, index) => {
                    const angle = (index * 40) * (Math.PI / 180);
                    const radius = 85;
                    const x = Math.cos(angle) * radius;
                    const y = Math.sin(angle) * radius;

                    return (
                      <TouchableOpacity
                        key={planet.name}
                        style={[
                          styles.auraPlanetOrb,
                          {
                            left: 110 + x - 22,
                            top: 110 + y - 22,
                            backgroundColor: planet.color + '30',
                            borderColor: planet.color,
                          },
                        ]}
                        onPress={() => setSelectedPlanet(planet)}
                      >
                        <Text style={styles.auraPlanetSymbol}>{planet.symbol}</Text>
                        <View style={[styles.auraPlanetStrength, { backgroundColor: planet.color }]}>
                          <Text style={styles.auraPlanetScore}>{planet.strength}</Text>
                        </View>
                      </TouchableOpacity>
                    );
                  })}

                  {/* Influence Lines - SVG alternative using Views */}
                  <View style={styles.auraRings}>
                    <View style={[styles.auraRing, { width: 180, height: 180 }]} />
                    <View style={[styles.auraRing, { width: 140, height: 140 }]} />
                    <View style={[styles.auraRing, { width: 100, height: 100 }]} />
                  </View>
                </View>

                {/* Planet Legend - Horizontal Scroll */}
                <ScrollView
                  horizontal
                  showsHorizontalScrollIndicator={false}
                  contentContainerStyle={styles.auraLegendScroll}
                >
                  {planetAura.planets?.map((planet) => (
                    <TouchableOpacity
                      key={planet.name}
                      style={[
                        styles.auraLegendItem,
                        selectedPlanet?.name === planet.name && styles.auraLegendItemActive,
                        { borderColor: planet.color }
                      ]}
                      onPress={() => setSelectedPlanet(selectedPlanet?.name === planet.name ? null : planet)}
                    >
                      <View style={[styles.auraLegendDot, { backgroundColor: planet.color }]} />
                      <Text style={styles.auraLegendName}>{getPlanetName(planet, language, t)}</Text>
                      <Text style={[styles.auraLegendScore, { color: planet.color }]}>{planet.strength}</Text>
                      {planet.transit_effect === 'favorable' && (
                        <Ionicons name="trending-up" size={12} color="#22c55e" />
                      )}
                      {planet.transit_effect === 'challenging' && (
                        <Ionicons name="trending-down" size={12} color="#ef4444" />
                      )}
                    </TouchableOpacity>
                  ))}
                </ScrollView>

                {/* Selected Planet Detail */}
                {selectedPlanet && (
                  <View style={[styles.auraPlanetDetail, { borderLeftColor: selectedPlanet.color }]}>
                    <View style={styles.auraPlanetDetailHeader}>
                      <Text style={styles.auraPlanetDetailSymbol}>{selectedPlanet.symbol}</Text>
                      <View>
                        <Text style={styles.auraPlanetDetailName}>{getPlanetName(selectedPlanet, language, t)}</Text>
                        <Text style={styles.auraPlanetDetailDomain}>{selectedPlanet.domain}</Text>
                      </View>
                      <View style={[styles.auraPlanetDetailScore, { backgroundColor: selectedPlanet.color }]}>
                        <Text style={styles.auraPlanetDetailScoreText}>{selectedPlanet.strength}%</Text>
                      </View>
                    </View>
                    <Text style={styles.auraPlanetDetailInsight}>{language === 'ta' ? selectedPlanet.insight : (selectedPlanet.insight_en || selectedPlanet.insight)}</Text>
                    <View style={styles.auraPlanetDetailTags}>
                      {selectedPlanet.keywords?.slice(0, 3).map((kw, i) => (
                        <View key={i} style={[styles.auraKeywordTag, { backgroundColor: selectedPlanet.color + '20' }]}>
                          <Text style={[styles.auraKeywordText, { color: selectedPlanet.color }]}>{kw}</Text>
                        </View>
                      ))}
                    </View>
                  </View>
                )}

                {/* Transit Summary */}
                {planetAura.transit_summary && (
                  <View style={styles.auraTransitSummary}>
                    <Ionicons name="pulse" size={14} color="#a78bfa" />
                    <Text style={styles.auraTransitText}>{language === 'ta' ? planetAura.transit_summary : (planetAura.transit_summary_en || planetAura.transit_summary)}</Text>
                  </View>
                )}

                {/* Dominant & Challenged Planets */}
                <View style={styles.auraDominantRow}>
                  {planetAura.dominant_planets?.length > 0 && (
                    <View style={styles.auraDominantSection}>
                      <Text style={styles.auraDominantLabel}>
                        <Ionicons name="flash" size={14} color="#16a34a" /> {t('strong')}
                      </Text>
                      <View style={styles.auraDominantList}>
                        {planetAura.dominant_planets.slice(0, 2).map((p, i) => (
                          <Text key={i} style={styles.auraDominantPlanet}>{translatePlanetString(p.tamil, language, t)}</Text>
                        ))}
                      </View>
                    </View>
                  )}
                  {planetAura.challenged_planets?.length > 0 && (
                    <View style={styles.auraDominantSection}>
                      <Text style={styles.auraDominantLabel}>
                        <Ionicons name="leaf" size={14} color="#f97316" /> {t('needsRemedy')}
                      </Text>
                      <View style={styles.auraDominantList}>
                        {planetAura.challenged_planets.slice(0, 2).map((p, i) => (
                          <Text key={i} style={[styles.auraDominantPlanet, { color: '#f97316' }]}>{translatePlanetString(p.tamil, language, t)}</Text>
                        ))}
                      </View>
                    </View>
                  )}
                </View>
              </LinearGradient>
            </AnimatedCard>
          )}

          {/* Transits Map - Live Planetary Movements - Premium Design */}
          {transitsMap && (
            <AnimatedCard delay={650}>
              <View style={styles.transitsContainer}>
                {/* Header with Glassmorphism */}
                <LinearGradient
                  colors={['#6366f1', '#8b5cf6']}
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 0 }}
                  style={styles.transitsHeader}
                >
                  <View style={styles.transitsHeaderContent}>
                    <View style={styles.transitsHeaderLeft}>
                      <Ionicons name="planet" size={24} color="#a5b4fc" />
                      <View>
                        <Text style={styles.transitsHeaderTitle}>
                          {t('liveTransits')}
                        </Text>
                        <Text style={styles.transitsHeaderSubtitle}>
                          {t('realTimePositions')}
                        </Text>
                      </View>
                    </View>
                    <View style={styles.livePulseContainer}>
                      <View style={styles.livePulseOuter}>
                        <View style={styles.livePulseInner} />
                      </View>
                      <Text style={styles.livePulseText}>{t('live')}</Text>
                    </View>
                  </View>
                </LinearGradient>

                {/* Moon Transit - Hero Section */}
                {transitsMap.moon_transit && (
                  <View style={styles.moonHeroSection}>
                    <View style={styles.moonHeroHeader}>
                      <View style={styles.moonHeroIconContainer}>
                        <Text style={styles.moonHeroIcon}>{transitsMap.moon_transit.phase_icon}</Text>
                        <View style={styles.moonHeroGlow} />
                      </View>
                      <View style={styles.moonHeroInfo}>
                        <Text style={styles.moonHeroLabel}>
                          {t('moonSign')}
                        </Text>
                        <Text style={styles.moonHeroSign}>
                          {transitsMap.moon_transit.current_sign_symbol} {translateRasiName(transitsMap.moon_transit.current_sign_name, t)}
                        </Text>
                        <Text style={styles.moonHeroPhase}>{translateMoonPhase(transitsMap.moon_transit.phase, t)}</Text>
                      </View>
                      {transitsMap.moon_transit.energy && (
                        <LinearGradient
                          colors={[transitsMap.moon_transit.energy.color + '40', transitsMap.moon_transit.energy.color + '20']}
                          style={styles.moonEnergyCard}
                        >
                          <Text style={styles.moonEnergyEmoji}>{transitsMap.moon_transit.energy.icon}</Text>
                          <Text style={[styles.moonEnergyMood, { color: transitsMap.moon_transit.energy.color }]}>
                            {language === 'ta' ? transitsMap.moon_transit.energy.mood : (transitsMap.moon_transit.energy.mood_en || transitsMap.moon_transit.energy.mood)}
                          </Text>
                        </LinearGradient>
                      )}
                    </View>

                    {/* Countdown Timer */}
                    <View style={styles.countdownContainer}>
                      <Text style={styles.countdownLabel}>
                        <Ionicons name="time" size={14} color="#a78bfa" /> {t('nextSignChange')}
                      </Text>
                      <View style={styles.countdownTimerRow}>
                        <View style={styles.countdownBox}>
                          <LinearGradient colors={['#6366f1', '#4f46e5']} style={styles.countdownBoxGradient}>
                            <Text style={styles.countdownValue}>{transitsMap.moon_transit.time_to_transit?.hours || 0}</Text>
                          </LinearGradient>
                          <Text style={styles.countdownUnit}>{t('hours')}</Text>
                        </View>
                        <Text style={styles.countdownSeparator}>:</Text>
                        <View style={styles.countdownBox}>
                          <LinearGradient colors={['#6366f1', '#4f46e5']} style={styles.countdownBoxGradient}>
                            <Text style={styles.countdownValue}>{transitsMap.moon_transit.time_to_transit?.minutes || 0}</Text>
                          </LinearGradient>
                          <Text style={styles.countdownUnit}>{t('minutes')}</Text>
                        </View>
                      </View>
                      <View style={styles.nextSignRow}>
                        <Ionicons name="arrow-forward-circle" size={18} color="#a78bfa" />
                        <Text style={styles.nextSignText}>
                          {transitsMap.moon_transit.next_sign_symbol} {translateRasiName(transitsMap.moon_transit.next_sign_name, t)}
                        </Text>
                      </View>
                    </View>

                    {/* Alert Message */}
                    {transitsMap.moon_transit.transit_message && (
                      <View style={styles.alertMessageBox}>
                        <View style={styles.alertMessageIconWrapper}>
                          <Ionicons name="notifications" size={18} color="#f59e0b" />
                        </View>
                        <Text style={styles.alertMessageText}>{language === 'ta' ? transitsMap.moon_transit.transit_message : (transitsMap.moon_transit.transit_message_en || transitsMap.moon_transit.transit_message)}</Text>
                      </View>
                    )}
                  </View>
                )}

                {/* Sky Map - Orbital View */}
                <View style={styles.orbitalSection}>
                  <Text style={styles.orbitalTitle}>
                    <Ionicons name="telescope" size={16} color="#6366f1" /> {t('celestialMap')}
                  </Text>
                  <View style={styles.orbitalContainer}>
                    {/* Outer Ring */}
                    <View style={styles.orbitalRingOuter} />
                    <View style={styles.orbitalRingMiddle} />
                    <View style={styles.orbitalRingInner} />

                    {/* Planet Positions */}
                    {transitsMap.sky_positions?.map((planet) => {
                      const angleRad = ((planet.angle - 90) * Math.PI) / 180;
                      const radius = planet.radius_factor * 75;
                      const x = Math.cos(angleRad) * radius;
                      const y = Math.sin(angleRad) * radius;

                      return (
                        <View
                          key={planet.planet}
                          style={[
                            styles.orbitalPlanet,
                            {
                              left: 85 + x - 15,
                              top: 85 + y - 15,
                              backgroundColor: planet.color + '30',
                              borderColor: planet.color,
                              shadowColor: planet.color,
                            },
                          ]}
                        >
                          <Text style={[styles.orbitalPlanetSymbol, { color: planet.color }]}>{planet.symbol}</Text>
                        </View>
                      );
                    })}

                    {/* Earth Center */}
                    <View style={styles.earthCenter}>
                      <Ionicons name="globe" size={20} color="#22c55e" />
                    </View>
                  </View>
                </View>

                {/* Planet Cards - Horizontal Scroll */}
                <View style={styles.planetCardsSection}>
                  <Text style={styles.planetCardsTitle}>
                    <Ionicons name="location" size={16} color="#6366f1" /> {t('planetPositions')}
                  </Text>
                  <ScrollView
                    horizontal
                    showsHorizontalScrollIndicator={false}
                    contentContainerStyle={styles.planetCardsScroll}
                  >
                    {Object.entries(transitsMap.planets || {}).map(([name, planet]) => (
                      <LinearGradient
                        key={name}
                        colors={[planet.color + '25', planet.color + '10']}
                        style={[styles.planetCard, { borderColor: planet.color + '60' }]}
                      >
                        <View style={[styles.planetCardIconBg, { backgroundColor: planet.color + '30' }]}>
                          <Text style={styles.planetCardSymbol}>{planet.symbol}</Text>
                        </View>
                        <Text style={styles.planetCardName}>{translatePlanetString(planet.tamil, language, t)}</Text>
                        <View style={styles.planetCardSignRow}>
                          <Text style={[styles.planetCardSign, { color: planet.color }]}>
                            {planet.sign_symbol}
                          </Text>
                          <Text style={styles.planetCardSignName}>{translateRasiName(planet.sign_name, t)}</Text>
                        </View>
                        <Text style={styles.planetCardDegree}>{planet.degree_display}</Text>
                        {planet.is_retrograde && (
                          <View style={styles.retroIndicator}>
                            <Text style={styles.retroIndicatorText}>℞ {t('retrograde')}</Text>
                          </View>
                        )}
                      </LinearGradient>
                    ))}
                  </ScrollView>
                </View>

                {/* Retrograde Alert Section */}
                {transitsMap.retrogrades?.length > 0 && (
                  <View style={styles.retroAlertSection}>
                    <View style={styles.retroAlertHeader}>
                      <Ionicons name="alert-circle" size={18} color="#fca5a5" />
                      <Text style={styles.retroAlertTitle}>
                        {t('retrogradeAlert')}
                      </Text>
                    </View>
                    {transitsMap.retrogrades.map((retro, index) => (
                      <LinearGradient
                        key={index}
                        colors={['#7f1d1d20', '#45122520']}
                        style={[styles.retroAlertCard, { borderLeftColor: retro.color }]}
                      >
                        <View style={styles.retroAlertCardHeader}>
                          <Text style={styles.retroAlertSymbol}>{retro.symbol}</Text>
                          <View style={styles.retroAlertInfo}>
                            <Text style={styles.retroAlertName}>{translatePlanetString(retro.tamil, language, t)}</Text>
                            <View style={[
                              styles.retroStatusPill,
                              { backgroundColor: retro.status === 'retrograde' ? '#ef444440' : '#f59e0b40' }
                            ]}>
                              <Text style={[
                                styles.retroStatusText,
                                { color: retro.status === 'retrograde' ? '#fca5a5' : '#fcd34d' }
                              ]}>
                                {t('retrograde')}
                              </Text>
                            </View>
                          </View>
                          {retro.days_remaining && (
                            <View style={styles.retroDaysLeft}>
                              <Text style={styles.retroDaysNumber}>{retro.days_remaining}</Text>
                              <Text style={styles.retroDaysLabel}>{t('days')}</Text>
                            </View>
                          )}
                        </View>
                        <Text style={styles.retroAlertMessage}>{getRetrogradeMessage(retro, language, t)}</Text>
                      </LinearGradient>
                    ))}
                  </View>
                )}

                {/* Upcoming Changes */}
                {transitsMap.upcoming_transits?.length > 0 && (
                  <View style={styles.upcomingSection}>
                    <Text style={styles.upcomingSectionTitle}>
                      <Ionicons name="calendar" size={16} color="#6366f1" /> {t('comingUp')}
                    </Text>
                    {transitsMap.upcoming_transits.slice(0, 3).map((transit, index) => (
                      <View key={index} style={styles.upcomingCard}>
                        <View style={[styles.upcomingIconBox, { backgroundColor: transit.color + '30' }]}>
                          <Text style={styles.upcomingIcon}>{transit.symbol}</Text>
                        </View>
                        <View style={styles.upcomingDetails}>
                          <Text style={styles.upcomingPlanet}>{translatePlanetString(transit.tamil, language, t)}</Text>
                          <View style={styles.upcomingArrowRow}>
                            <Text style={styles.upcomingFrom}>{translateRasiName(transit.from_sign_name, t)}</Text>
                            <Ionicons name="arrow-forward" size={12} color="#6366f1" />
                            <Text style={styles.upcomingTo}>{transit.to_sign_symbol} {translateRasiName(transit.to_sign_name, t)}</Text>
                          </View>
                        </View>
                        <View style={styles.upcomingTimeBox}>
                          <Text style={styles.upcomingTimeValue}>{Math.round(transit.hours_remaining)}</Text>
                          <Text style={styles.upcomingTimeUnit}>{t('hours')}</Text>
                        </View>
                      </View>
                    ))}
                  </View>
                )}

                {/* Auspicious Time Footer */}
                {transitsMap.auspicious_time && (
                  <LinearGradient
                    colors={[transitsMap.auspicious_time.color + '30', transitsMap.auspicious_time.color + '10']}
                    style={styles.auspiciousFooter}
                  >
                    <Ionicons name="sparkles" size={16} color={transitsMap.auspicious_time.color} />
                    <Text style={[styles.auspiciousText, { color: transitsMap.auspicious_time.color }]}>
                      {language === 'ta' ? transitsMap.auspicious_time.name : (transitsMap.auspicious_time.name_en || transitsMap.auspicious_time.name)}
                    </Text>
                  </LinearGradient>
                )}
              </View>
            </AnimatedCard>
          )}

          {/* Bottom decorative section */}
          <DecorativeBorder style={{ marginTop: 20, marginBottom: 10 }} />
        </ScrollView>
      </LinearGradient>

      {/* Score Justification Modal */}
      <ScoreJustificationModal
        visible={showScoreModal}
        onClose={() => setShowScoreModal(false)}
        data={selectedScoreData}
        t={t}
        language={language}
      />

      {/* Timeline Year Detail Modal */}
      <TimelineYearModal
        visible={showTimelineModal}
        onClose={() => {
          setShowTimelineModal(false);
          setSelectedTimelineYear(null);
        }}
        data={selectedTimelineYear}
        language={language}
        t={t}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  gradient: { flex: 1, backgroundColor: '#e8ecf3' },
  scrollContent: { paddingHorizontal: 0 },

  loadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#e8ecf3' },
  loadingText: { marginTop: 16, color: '#5a6c8f', fontSize: 16, fontWeight: '600' },
  headerBar: { height: 0 },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start', padding: 24, paddingBottom: 20, backgroundColor: '#e8ecf3', marginHorizontal: 16, marginTop: 16, borderRadius: 28, shadowColor: '#a3b9d9', shadowOffset: { width: -6, height: -6 }, shadowOpacity: 0.8, shadowRadius: 12, elevation: 0, borderWidth: 1, borderColor: '#f5f7fa' },
  logoRow: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  logoIcon: { width: 32, height: 32, shadowColor: '#f97316', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.2, shadowRadius: 4, elevation: 3 },
  appTitle: { fontSize: 22, fontWeight: '900', color: '#9a3412', letterSpacing: 0.5 },
  userInfo: { marginTop: 6 },
  greeting: { fontSize: 15, color: '#6b7280', fontWeight: '500' },
  rasiInfo: { fontSize: 13, color: '#ea580c', marginTop: 2, fontWeight: '600' },
  timeContainer: { alignItems: 'flex-end' },
  currentTime: { fontSize: 20, fontFamily: 'monospace', color: '#1f2937', fontWeight: '600', letterSpacing: 1 },
  periodBadge: { paddingHorizontal: 10, paddingVertical: 5, borderRadius: 14, marginTop: 6, shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1, shadowRadius: 3, elevation: 2 },
  periodText: { fontSize: 11, fontWeight: '700', letterSpacing: 0.5 },

  // Date card
  dateCard: { backgroundColor: '#fff', marginHorizontal: 16, marginTop: 16, padding: 14, borderRadius: 16, alignItems: 'center', borderWidth: 1, borderColor: '#fcd34d', shadowColor: '#f97316', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.12, shadowRadius: 8, elevation: 4 },
  dateText: { fontSize: 15, color: '#9a3412', fontWeight: '700', letterSpacing: 0.3 },

  // Story Preview Row (Instagram-style)
  storyPreviewRow: { paddingHorizontal: 16, paddingVertical: 16 },
  storyCirclesContainer: { flexDirection: 'row', justifyContent: 'space-around', alignItems: 'center' },
  storyCircle: { alignItems: 'center', width: 68 },
  storyCircleActive: {},
  storyGradientBorder: { width: 60, height: 60, borderRadius: 30, padding: 3, justifyContent: 'center', alignItems: 'center', shadowColor: '#000', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.2, shadowRadius: 6, elevation: 6 },
  storyInner: { width: 52, height: 52, borderRadius: 26, backgroundColor: '#1a1a2e', justifyContent: 'center', alignItems: 'center', borderWidth: 2, borderColor: '#2d2d5a' },
  storyMoreCircle: { width: 60, height: 60, borderRadius: 30, backgroundColor: '#fff', borderWidth: 2.5, borderColor: '#fcd34d', borderStyle: 'dashed', justifyContent: 'center', alignItems: 'center', shadowColor: '#f97316', shadowOffset: { width: 0, height: 3 }, shadowOpacity: 0.15, shadowRadius: 5, elevation: 4 },
  storyLabel: { fontSize: 11, color: '#4b5563', marginTop: 6, textAlign: 'center', fontWeight: '600' },

  card: { backgroundColor: '#fff', borderRadius: 20, padding: 20, marginTop: 16, marginHorizontal: 16, borderWidth: 1, borderColor: 'rgba(252, 211, 77, 0.4)', shadowColor: '#000', shadowOffset: { width: 0, height: 6 }, shadowOpacity: 0.1, shadowRadius: 12, elevation: 6 },
  cardHeader: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 16 },
  cardTitle: { fontSize: 17, fontWeight: '800', color: '#92400e', flex: 1, letterSpacing: 0.2 },
  tapHintSmall: { fontSize: 10, color: '#9ca3af' },
  panchangamGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 12 },
  panchangamItem: { flex: 1, minWidth: '45%', backgroundColor: '#fffbeb', borderRadius: 14, padding: 16, borderWidth: 1, borderColor: 'rgba(252, 211, 77, 0.5)', shadowColor: '#f97316', shadowOffset: { width: 0, height: 3 }, shadowOpacity: 0.08, shadowRadius: 6, elevation: 3 },
  panchangamLabel: { fontSize: 11, color: '#92400e', marginBottom: 6, fontWeight: '600', textTransform: 'uppercase', letterSpacing: 0.5 },
  panchangamValue: { fontSize: 14, fontWeight: '800', color: '#78350f', letterSpacing: 0.2 },

  scoreRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  scoreLabel: { fontSize: 13, color: '#6b7280', fontWeight: '600', textTransform: 'uppercase', letterSpacing: 0.5 },
  scoreValue: { flexDirection: 'row', alignItems: 'baseline', gap: 6, marginTop: 6 },
  scoreNumber: { fontSize: 42, fontWeight: '900', color: '#ea580c', letterSpacing: -1 },
  scoreMax: { fontSize: 16, color: '#9ca3af', fontWeight: '600' },
  scoreBadge: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 12, paddingVertical: 6, borderRadius: 14, marginLeft: 10, gap: 5, shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1, shadowRadius: 4, elevation: 3 },
  scoreBadgeText: { fontSize: 13, fontWeight: '700', letterSpacing: 0.3 },
  scoreCircle: { width: 80, height: 80, borderRadius: 40, backgroundColor: '#fffbeb', borderWidth: 5, borderColor: '#ea580c', justifyContent: 'center', alignItems: 'center', shadowColor: '#ea580c', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.25, shadowRadius: 8, elevation: 6 },
  scoreCircleText: { fontSize: 18, fontWeight: '900', color: '#ea580c' },
  tapHint: { fontSize: 8, color: '#9ca3af', marginTop: 2 },

  insightBox: { flexDirection: 'row', alignItems: 'flex-start', gap: 10, padding: 16, borderRadius: 14, marginTop: 16, borderWidth: 1, borderColor: 'rgba(254, 215, 170, 0.5)', backgroundColor: '#fffbeb', shadowColor: '#f97316', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.06, shadowRadius: 4, elevation: 2 },
  insightText: { flex: 1, fontSize: 14, color: '#374151', lineHeight: 22, fontWeight: '500' },

  lifeAreasRow: { flexDirection: 'row', gap: 12, marginBottom: 12 },
  lifeAreaCard: { flex: 1, backgroundColor: '#fff', borderRadius: 16, padding: 16, borderWidth: 1, borderColor: 'rgba(252, 211, 77, 0.3)', minHeight: 130, shadowColor: '#000', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.08, shadowRadius: 8, elevation: 4 },
  lifeAreaHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 },
  lifeAreaIconBg: { width: 36, height: 36, borderRadius: 18, justifyContent: 'center', alignItems: 'center', shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1, shadowRadius: 4, elevation: 2 },
  lifeAreaBadge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12, shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.08, shadowRadius: 2, elevation: 2 },
  lifeAreaBadgeText: { fontSize: 10, fontWeight: '700', letterSpacing: 0.3 },
  lifeAreaName: { fontSize: 14, color: '#374151', fontWeight: '700', marginBottom: 8, letterSpacing: 0.2 },
  lifeAreaScoreRow: { flexDirection: 'row', alignItems: 'baseline' },
  lifeAreaScore: { fontSize: 30, fontWeight: '900', letterSpacing: -0.5 },
  lifeAreaMax: { fontSize: 12, color: '#9ca3af', marginLeft: 3, fontWeight: '600' },
  lifeAreaProgressBar: { height: 6, backgroundColor: '#f3f4f6', borderRadius: 3, marginTop: 12, overflow: 'hidden' },
  lifeAreaProgressFill: { height: 6, borderRadius: 3 },
  progressBar: { height: 7, backgroundColor: '#f3f4f6', borderRadius: 4, marginTop: 10, overflow: 'hidden' },
  progressFill: { height: 7, borderRadius: 4, shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.1, shadowRadius: 2 },

  // Projection styles
  projectionToggle: { flexDirection: 'row', backgroundColor: '#f3f4f6', borderRadius: 10, padding: 4, marginBottom: 12 },
  toggleBtn: { flex: 1, paddingVertical: 8, borderRadius: 8, alignItems: 'center' },
  toggleBtnActive: { backgroundColor: '#fff', shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.1, shadowRadius: 2, elevation: 2 },
  toggleText: { fontSize: 12, color: '#6b7280' },
  toggleTextActive: { color: '#f97316', fontWeight: '600' },

  monthsScroll: { marginHorizontal: -4 },
  monthCard: { width: 86, backgroundColor: '#fff', borderRadius: 14, padding: 12, marginHorizontal: 5, borderWidth: 1, borderColor: 'rgba(229, 231, 235, 0.5)', alignItems: 'center', shadowColor: '#000', shadowOffset: { width: 0, height: 3 }, shadowOpacity: 0.06, shadowRadius: 6, elevation: 3 },
  monthName: { fontSize: 11, color: '#374151', fontWeight: '700', marginBottom: 8, textTransform: 'uppercase', letterSpacing: 0.5 },
  monthScoreBadge: { paddingHorizontal: 10, paddingVertical: 5, borderRadius: 12, marginBottom: 8, shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.08, shadowRadius: 2, elevation: 2 },
  monthScore: { fontSize: 15, fontWeight: '900' },
  monthBarContainer: { width: '100%', height: 5, backgroundColor: '#f3f4f6', borderRadius: 3 },
  monthBar: { height: 5, borderRadius: 3 },

  yearsGrid: { gap: 12 },

  // Past Years styles
  pastYearsGrid: { flexDirection: 'row', gap: 12 },
  pastYearCard: { flex: 1, backgroundColor: '#f9fafb', borderRadius: 12, padding: 12, borderWidth: 1, borderColor: '#e5e7eb' },
  pastYearHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 },
  pastYearLabel: { fontSize: 16, fontWeight: 'bold', color: '#374151' },
  pastYearBadge: { paddingHorizontal: 8, paddingVertical: 2, borderRadius: 10 },
  pastYearScore: { fontSize: 13, fontWeight: '600' },
  pastYearDasha: { fontSize: 11, color: '#6b7280', marginBottom: 8 },
  pastYearBar: { height: 4, backgroundColor: '#e5e7eb', borderRadius: 2, overflow: 'hidden' },
  pastYearBarFill: { height: 4, borderRadius: 2 },

  yearCard: { borderRadius: 16, overflow: 'hidden', borderWidth: 1, borderColor: 'rgba(229, 231, 235, 0.6)', shadowColor: '#000', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.08, shadowRadius: 8, elevation: 4 },
  yearCardGradient: { flexDirection: 'row', alignItems: 'center', padding: 18, gap: 14 },
  yearIconBg: { width: 48, height: 48, borderRadius: 24, justifyContent: 'center', alignItems: 'center', shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1, shadowRadius: 4, elevation: 2 },
  yearInfo: { flex: 1 },
  yearName: { fontSize: 19, fontWeight: '900', color: '#1f2937', letterSpacing: 0.3 },
  yearLabel: { fontSize: 13, color: '#6b7280', marginTop: 4, fontWeight: '600' },
  yearScoreContainer: { alignItems: 'flex-end', marginRight: 8 },
  yearScore: { fontSize: 24, fontWeight: '900', letterSpacing: -0.5 },
  yearScoreBar: { width: 60, height: 4, borderRadius: 2, marginTop: 4 },
  yearScoreFill: { height: 4, borderRadius: 2 },

  quickActionsGrid: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 14 },
  quickActionBtn: { flex: 1, alignItems: 'center', backgroundColor: '#fff', borderRadius: 14, padding: 18, marginHorizontal: 5, borderWidth: 1, borderColor: 'rgba(254, 215, 170, 0.5)', shadowColor: '#f97316', shadowOffset: { width: 0, height: 3 }, shadowOpacity: 0.08, shadowRadius: 6, elevation: 3 },
  quickActionLabel: { fontSize: 11, color: '#4b5563', marginTop: 10, fontWeight: '700', letterSpacing: 0.2 },

  dashaCard: { borderColor: 'rgba(221, 214, 254, 0.6)', shadowColor: '#8b5cf6', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.12, shadowRadius: 10, elevation: 5 },
  dashaGrid: { flexDirection: 'row', gap: 14 },
  dashaItem: { flex: 1, backgroundColor: 'rgba(255,255,255,0.6)', borderRadius: 14, padding: 14, borderWidth: 1, borderColor: 'rgba(221, 214, 254, 0.4)', shadowColor: '#8b5cf6', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.06, shadowRadius: 4, elevation: 2 },
  dashaLabel: { fontSize: 11, color: '#6b7280', fontWeight: '600', textTransform: 'uppercase', letterSpacing: 0.5 },
  dashaValue: { fontSize: 15, fontWeight: '800', color: '#7c3aed', marginTop: 6, letterSpacing: 0.2 },

  // Chakra Card Styles
  chakraCard: { borderRadius: 22, padding: 18, borderWidth: 1, borderColor: 'rgba(168, 85, 247, 0.5)', shadowColor: '#a855f7', shadowOffset: { width: 0, height: 6 }, shadowOpacity: 0.25, shadowRadius: 12, elevation: 8 },
  chakraCardHeader: { flexDirection: 'row', alignItems: 'center', gap: 14 },
  chakraIconContainer: { width: 56, height: 56, borderRadius: 28, backgroundColor: 'rgba(168, 85, 247, 0.3)', justifyContent: 'center', alignItems: 'center', borderWidth: 2, borderColor: 'rgba(255,255,255,0.2)', shadowColor: '#a855f7', shadowOffset: { width: 0, height: 3 }, shadowOpacity: 0.3, shadowRadius: 6, elevation: 4 },
  chakraIconLarge: { fontSize: 30 },
  chakraCardInfo: { flex: 1 },
  chakraCardTitle: { fontSize: 18, fontWeight: '900', color: '#fff', letterSpacing: 0.3 },
  chakraCardSubtitle: { fontSize: 13, color: '#c4b5fd', marginTop: 4, fontWeight: '600' },
  chakraArrowContainer: { padding: 4 },
  chakraMiniPreview: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 16, paddingVertical: 10, paddingHorizontal: 4, backgroundColor: 'rgba(0,0,0,0.25)', borderRadius: 12 },
  chakraMiniItem: { alignItems: 'center', flex: 1, paddingHorizontal: 2 },
  chakraMiniCircle: { width: 30, height: 30, borderRadius: 15, justifyContent: 'center', alignItems: 'center', borderWidth: 2, borderColor: 'rgba(255,255,255,0.3)' },
  chakraMiniScore: { fontSize: 9, fontWeight: '800', color: '#fff' },
  chakraMiniName: { fontSize: 7, color: '#a5b4fc', marginTop: 3, textAlign: 'center', maxWidth: 45 },
  chakraEnergyRow: { flexDirection: 'row', alignItems: 'center', marginTop: 14, paddingTop: 12, borderTopWidth: 1, borderTopColor: 'rgba(255,255,255,0.1)' },
  chakraEnergyInfo: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  chakraEnergyLabel: { fontSize: 11, color: '#c4b5fd', fontWeight: '500' },
  chakraEnergyBar: { flex: 1, height: 6, backgroundColor: 'rgba(255,255,255,0.15)', borderRadius: 3, marginHorizontal: 10, overflow: 'hidden' },
  chakraEnergyFill: { height: '100%', backgroundColor: '#a855f7', borderRadius: 3 },
  chakraEnergyPercent: { fontSize: 14, fontWeight: '800', color: '#a855f7' },
  chakraCardFooter: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginTop: 12 },
  chakraCardHint: { fontSize: 12, color: '#a5b4fc' },
  chakraNewBadge: { backgroundColor: '#22c55e', paddingHorizontal: 8, paddingVertical: 3, borderRadius: 8 },
  chakraNewText: { fontSize: 10, fontWeight: '800', color: '#fff' },

  // Parigaram Card Styles - Gamified
  parigaramCard: { borderColor: '#fbbf24', borderWidth: 2, shadowColor: '#f59e0b', shadowOffset: { width: 0, height: 6 }, shadowOpacity: 0.35, shadowRadius: 12, elevation: 8 },
  parigaramHeader: { flexDirection: 'row', alignItems: 'center', gap: 14 },
  parigaramIconBadge: { width: 52, height: 52, borderRadius: 26, backgroundColor: 'rgba(146, 64, 14, 0.2)', justifyContent: 'center', alignItems: 'center', borderWidth: 2, borderColor: 'rgba(251, 191, 36, 0.3)', shadowColor: '#f59e0b', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.2, shadowRadius: 4, elevation: 3 },
  parigaramTitleSection: { flex: 1 },
  parigaramTitle: { fontSize: 17, fontWeight: '900', color: '#92400e', letterSpacing: 0.3 },
  parigaramSubtitle: { fontSize: 12, color: '#b45309', marginTop: 3, fontWeight: '600' },
  parigaramArrow: { padding: 4 },
  parigaramPlanets: { flexDirection: 'row', gap: 12, marginTop: 16, marginBottom: 14 },
  parigaramPlanetBadge: { flexDirection: 'row', alignItems: 'center', backgroundColor: 'rgba(255,255,255,0.8)', paddingHorizontal: 14, paddingVertical: 8, borderRadius: 22, borderWidth: 1.5, borderColor: '#fbbf24', gap: 7, shadowColor: '#f59e0b', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.12, shadowRadius: 4, elevation: 3 },
  parigaramPlanetIcon: { fontSize: 17, color: '#b45309' },
  parigaramPlanetName: { fontSize: 13, fontWeight: '700', color: '#92400e', letterSpacing: 0.2 },
  parigaramQuickTips: { flexDirection: 'row', justifyContent: 'space-around', paddingTop: 10, borderTopWidth: 1, borderTopColor: 'rgba(180, 83, 9, 0.2)' },
  parigaramTip: { alignItems: 'center', gap: 4 },
  parigaramTipText: { fontSize: 10, color: '#92400e', fontWeight: '500' },

  // Modal styles
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.6)' },
  modalScrollView: { marginTop: 'auto', maxHeight: '88%' },
  modalContent: { backgroundColor: '#fff', borderTopLeftRadius: 28, borderTopRightRadius: 28, padding: 24, paddingBottom: 44, shadowColor: '#000', shadowOffset: { width: 0, height: -4 }, shadowOpacity: 0.15, shadowRadius: 16, elevation: 10 },
  modalHeader: { flexDirection: 'row', alignItems: 'center', gap: 14, marginBottom: 20 },
  modalIconBg: { width: 52, height: 52, borderRadius: 26, justifyContent: 'center', alignItems: 'center', shadowColor: '#000', shadowOffset: { width: 0, height: 3 }, shadowOpacity: 0.15, shadowRadius: 6, elevation: 4 },
  modalTitle: { flex: 1, fontSize: 20, fontWeight: '900', color: '#1f2937', letterSpacing: 0.3 },
  modalCloseBtn: { padding: 4 },
  modalScoreSection: { flexDirection: 'row', alignItems: 'baseline', justifyContent: 'center', marginBottom: 20 },
  modalScoreValue: { fontSize: 56, fontWeight: '900', letterSpacing: -2 },
  modalScoreMax: { fontSize: 20, color: '#9ca3af', marginLeft: 6, fontWeight: '700' },
  modalDivider: { height: 1, backgroundColor: '#e5e7eb', marginVertical: 20 },
  modalSectionTitle: { fontSize: 15, fontWeight: '800', color: '#374151', marginBottom: 14, textTransform: 'uppercase', letterSpacing: 0.5 },
  factorItem: { backgroundColor: '#f9fafb', borderRadius: 14, padding: 14, marginBottom: 12, borderWidth: 1, borderColor: 'rgba(229, 231, 235, 0.6)' },
  factorHeader: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  factorName: { flex: 1, fontSize: 14, fontWeight: '700', color: '#374151' },
  factorScore: { fontSize: 14, fontWeight: 'bold' },
  factorDesc: { fontSize: 12, color: '#6b7280', marginTop: 6, marginLeft: 26 },

  // Positives styles
  positiveItem: { flexDirection: 'row', alignItems: 'flex-start', gap: 12, marginBottom: 12, backgroundColor: '#f0fdf4', borderRadius: 12, padding: 12, borderWidth: 1, borderColor: '#bbf7d0' },
  positiveIconBg: { width: 36, height: 36, borderRadius: 18, backgroundColor: '#dcfce7', justifyContent: 'center', alignItems: 'center' },
  positiveContent: { flex: 1 },
  positiveTitle: { fontSize: 14, fontWeight: '600', color: '#15803d', marginBottom: 4 },
  positiveDesc: { fontSize: 12, color: '#166534', lineHeight: 18 },

  // Remedies styles
  remediesBox: { backgroundColor: '#fef3c7', borderRadius: 12, padding: 12, borderWidth: 1, borderColor: '#fde68a' },
  remedyItem: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 8 },
  remedyText: { flex: 1, fontSize: 13, color: '#92400e', lineHeight: 18 },

  suggestionBox: { flexDirection: 'row', alignItems: 'flex-start', gap: 10, backgroundColor: '#fff7ed', borderRadius: 12, padding: 14, marginTop: 16, borderWidth: 1, borderColor: '#fed7aa' },
  suggestionText: { flex: 1, fontSize: 13, color: '#9a3412', lineHeight: 20 },
  modalButton: { backgroundColor: '#f97316', borderRadius: 12, paddingVertical: 14, alignItems: 'center', marginTop: 20 },
  modalButtonText: { color: '#fff', fontSize: 16, fontWeight: '600' },

  // Score breakdown detailed styles
  qualityBadge: { alignSelf: 'center', paddingHorizontal: 16, paddingVertical: 6, borderRadius: 20, marginBottom: 12 },
  qualityText: { fontSize: 14, fontWeight: '600' },
  dashaInfoBox: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, backgroundColor: '#f3e8ff', borderRadius: 10, paddingVertical: 8, paddingHorizontal: 12, marginBottom: 8 },
  dashaInfoText: { fontSize: 13, color: '#7c3aed', fontWeight: '500' },

  // Modal Tab Styles
  modalTabContainer: { flexDirection: 'row', backgroundColor: '#f3f4f6', borderRadius: 12, padding: 4, marginBottom: 16 },
  modalTab: { flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 6, paddingVertical: 10, borderRadius: 10 },
  modalTabActive: { backgroundColor: '#fff', shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.1, shadowRadius: 2, elevation: 2 },
  modalTabText: { fontSize: 13, color: '#9ca3af', fontWeight: '500' },
  modalTabTextActive: { color: '#f97316', fontWeight: '600' },

  // AI Summary Styles
  aiSummaryContainer: { gap: 16 },
  aiSummaryCard: { borderRadius: 16, padding: 16, borderWidth: 1 },
  aiSummaryHeader: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 10 },
  aiSummaryTitle: { fontSize: 15, fontWeight: '600', color: '#374151' },
  aiSummaryText: { fontSize: 14, color: '#4b5563', lineHeight: 22 },
  aiHighlightsContainer: { backgroundColor: '#f9fafb', borderRadius: 14, padding: 14 },
  aiHighlightsTitle: { fontSize: 14, fontWeight: '600', color: '#374151', marginBottom: 10 },
  aiHighlightItem: { paddingVertical: 8, borderBottomWidth: 1, borderBottomColor: '#e5e7eb' },
  aiHighlightText: { fontSize: 14, color: '#4b5563' },
  aiAdviceCard: { backgroundColor: '#faf5ff', borderRadius: 14, padding: 14, borderWidth: 1, borderColor: '#e9d5ff' },
  aiAdviceHeader: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 8 },
  aiAdviceTitle: { fontSize: 14, fontWeight: '600', color: '#7c3aed' },
  aiAdviceText: { fontSize: 14, color: '#6b21a8', lineHeight: 22 },
  aiDashaCard: { backgroundColor: '#f5f3ff', borderRadius: 12, padding: 12, borderWidth: 1, borderColor: '#ddd6fe' },
  aiDashaHeader: { flexDirection: 'row', alignItems: 'center', gap: 6, marginBottom: 6 },
  aiDashaTitle: { fontSize: 12, fontWeight: '600', color: '#8b5cf6' },
  aiDashaText: { fontSize: 13, color: '#6b7280', lineHeight: 20 },
  aiDashaBold: { fontWeight: '600', color: '#7c3aed' },
  formulaText: { fontSize: 11, color: '#6b7280', fontFamily: 'monospace', backgroundColor: '#f3f4f6', padding: 10, borderRadius: 8, marginBottom: 12, textAlign: 'center' },

  // Breakdown card styles
  breakdownCard: { backgroundColor: '#f9fafb', borderRadius: 12, padding: 12, marginBottom: 10, borderWidth: 1, borderColor: '#e5e7eb' },
  breakdownHeader: { flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 8 },
  breakdownIconBg: { width: 32, height: 32, borderRadius: 16, justifyContent: 'center', alignItems: 'center' },
  breakdownTitleRow: { flex: 1, flexDirection: 'row', alignItems: 'center', gap: 6 },
  breakdownTitle: { fontSize: 13, fontWeight: '600', color: '#374151' },
  breakdownWeight: { fontSize: 11, color: '#9ca3af' },
  breakdownContribution: { fontSize: 16, fontWeight: 'bold' },
  breakdownProgressBg: { height: 6, backgroundColor: '#e5e7eb', borderRadius: 3, marginBottom: 8 },
  breakdownProgressFill: { height: 6, borderRadius: 3 },
  breakdownFactors: { marginTop: 4 },
  miniFactorRow: { flexDirection: 'row', alignItems: 'center', gap: 6, paddingVertical: 3 },
  miniFactorText: { flex: 1, fontSize: 11, color: '#6b7280' },
  miniFactorValue: { fontSize: 11, fontWeight: '600' },

  // Final calculation styles
  finalCalcBox: { backgroundColor: '#fef3c7', borderRadius: 10, padding: 12, marginTop: 8, alignItems: 'center' },
  finalCalcLabel: { fontSize: 12, color: '#92400e', fontWeight: '600', marginBottom: 4 },
  finalCalcFormula: { fontSize: 10, color: '#a16207', fontFamily: 'monospace', marginBottom: 4 },
  finalCalcResult: { fontSize: 18, fontWeight: 'bold', color: '#b45309' },

  // Simple breakdown styles
  simpleBreakdownRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingVertical: 8, borderBottomWidth: 1, borderBottomColor: '#f3f4f6' },
  simpleBreakdownLeft: { flexDirection: 'row', alignItems: 'center', gap: 8, flex: 1 },
  simpleBreakdownLabel: { fontSize: 13, color: '#374151' },
  simpleBreakdownRight: { flexDirection: 'row', alignItems: 'center', gap: 10, flex: 1.5 },
  simpleProgressBg: { flex: 1, height: 6, backgroundColor: '#e5e7eb', borderRadius: 3 },
  simpleProgressFill: { height: 6, borderRadius: 3 },
  simpleBreakdownValue: { fontSize: 14, fontWeight: '600', color: '#374151', minWidth: 35, textAlign: 'right' },

  // Area scores grid styles
  areaScoresGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10 },
  areaScoreCard: { flex: 1, minWidth: '45%', backgroundColor: '#fff', borderRadius: 10, padding: 12, alignItems: 'center', borderWidth: 1 },
  areaScoreLabel: { fontSize: 11, color: '#6b7280', marginTop: 4 },
  areaScoreValue: { fontSize: 18, fontWeight: 'bold', marginTop: 2 },

  // Life Timeline styles (v4 - Bar Chart Design)
  timelineCard: { borderColor: '#f97316', borderWidth: 1 },

  // Journey Header
  journeyHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 },
  journeyTitleRow: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  journeyIcon: { fontSize: 22 },
  journeyTitleInfo: { flex: 1 },
  journeyTitle: { fontSize: 16, fontWeight: '700', color: '#fff' },
  journeySubtitle: { fontSize: 11, color: '#94a3b8', marginTop: 2 },
  journeyExpandBtn: { padding: 8, backgroundColor: 'rgba(249, 115, 22, 0.15)', borderRadius: 10 },

  // Score Scale
  scoreScaleRow: { flexDirection: 'row', justifyContent: 'center', gap: 12, marginBottom: 12, flexWrap: 'wrap' },
  scoreScaleItem: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  scoreScaleDot: { width: 8, height: 8, borderRadius: 4 },
  scoreScaleText: { fontSize: 10, color: '#94a3b8' },

  // Bar Chart
  barChartContainer: { flexDirection: 'row', marginBottom: 16 },
  yAxisLabels: { width: 28, justifyContent: 'space-between', paddingVertical: 4 },
  yAxisText: { fontSize: 9, color: '#64748b', textAlign: 'right' },
  barChartArea: { flex: 1, height: 140, position: 'relative' },
  gridLine: { position: 'absolute', left: 0, right: 0, height: 1, backgroundColor: 'rgba(100, 116, 139, 0.2)' },
  gridLineHighlight: { backgroundColor: 'rgba(249, 115, 22, 0.3)', height: 2 },
  barsScrollContent: { paddingHorizontal: 4, alignItems: 'flex-end', minWidth: '100%' },
  barColumn: { alignItems: 'center', marginHorizontal: 6, width: 32 },
  barWrapper: { height: 120, justifyContent: 'flex-end' },
  bar: { width: 24, borderRadius: 4, alignItems: 'center', justifyContent: 'flex-start', paddingTop: 4, minHeight: 20 },
  barScoreText: { fontSize: 9, fontWeight: '700', color: '#fff' },
  barYearText: { fontSize: 11, color: '#94a3b8', marginTop: 4, fontWeight: '500' },
  barYearTextCurrent: { color: '#f97316', fontWeight: '700' },
  currentYearMarker: { marginTop: 2 },
  currentYearMarkerText: { fontSize: 8, color: '#f97316' },

  // Summary Cards
  summaryCardsRow: { flexDirection: 'row', justifyContent: 'space-between', gap: 8, marginBottom: 12 },
  summaryCard: { flex: 1, alignItems: 'center', padding: 10, borderRadius: 10, borderWidth: 1 },
  summaryCardEmoji: { fontSize: 18, marginBottom: 4 },
  summaryCardLabel: { fontSize: 9, color: '#94a3b8', marginBottom: 2 },
  summaryCardValue: { fontSize: 14, fontWeight: '700' },
  summaryCardScore: { fontSize: 10, color: '#64748b', marginTop: 2 },

  // Tap hint
  tapHintText: { fontSize: 11, color: '#64748b', textAlign: 'center', fontStyle: 'italic' },
  // TimelineYearModal styles
  tlmAreaContainer: { marginBottom: 8 },
  tlmAreaRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 10 },
  tlmAreaInfo: { flexDirection: 'row', alignItems: 'center', width: 90, gap: 6 },
  tlmAreaLabel: { fontSize: 12, color: '#374151' },
  tlmAreaBarBg: { flex: 1, height: 12, backgroundColor: '#e5e7eb', borderRadius: 6, overflow: 'hidden', marginHorizontal: 8 },
  tlmAreaBarFill: { height: '100%', borderRadius: 6 },
  tlmAreaScore: { fontSize: 12, fontWeight: '600', width: 40, textAlign: 'right' },
  tlmTraceBox: { backgroundColor: '#f3f4f6', borderRadius: 10, padding: 12, marginBottom: 8 },
  tlmTraceVersion: { fontSize: 10, color: '#6b7280', marginBottom: 4 },
  tlmTraceFormula: { fontSize: 11, color: '#374151', fontFamily: 'monospace' },
  tlmTraceMeta: { flexDirection: 'row', alignItems: 'center', gap: 4, marginTop: 6 },
  tlmTraceMetaText: { fontSize: 11, color: '#f97316', fontWeight: '500' },
  tlmEventsGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  tlmEventChip: { flexDirection: 'row', alignItems: 'center', gap: 6, paddingHorizontal: 10, paddingVertical: 6, borderRadius: 16, borderWidth: 1 },
  tlmEventText: { fontSize: 11, fontWeight: '500' },
  majorEventsPreview: { marginTop: 16, paddingTop: 16, borderTopWidth: 1, borderTopColor: '#334155' },
  majorEventsTitle: { fontSize: 13, fontWeight: '600', color: '#e2e8f0', marginBottom: 10 },
  majorEventsList: { gap: 8 },
  majorEventItem: { flexDirection: 'row', alignItems: 'center', gap: 10, backgroundColor: 'rgba(51, 65, 85, 0.6)', borderRadius: 10, paddingVertical: 8, paddingHorizontal: 12 },
  majorEventIcon: { fontSize: 18 },
  majorEventYear: { fontSize: 13, fontWeight: '700', color: '#a78bfa', minWidth: 40 },
  majorEventLabel: { flex: 1, fontSize: 12, color: '#cbd5e1' },
  peakLowContainer: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 12, paddingTop: 12, borderTopWidth: 1, borderTopColor: '#334155' },
  peakLowItem: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  peakLowText: { fontSize: 12, color: '#cbd5e1' },

  // Aura Heatmap styles
  auraCard: { borderColor: 'rgba(139, 92, 246, 0.6)', shadowColor: '#8b5cf6', shadowOffset: { width: 0, height: 8 }, shadowOpacity: 0.3, shadowRadius: 16, elevation: 10 },
  auraBadge: { paddingHorizontal: 12, paddingVertical: 5, borderRadius: 14, shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.15, shadowRadius: 4, elevation: 3 },
  auraBadgeText: { fontSize: 15, fontWeight: '900', letterSpacing: 0.3 },
  auraOverview: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 18 },
  auraLevelBadge: { paddingHorizontal: 16, paddingVertical: 7, borderRadius: 18, shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.12, shadowRadius: 4, elevation: 3 },
  auraLevelText: { fontSize: 14, fontWeight: '800', letterSpacing: 0.4 },
  auraStats: { flexDirection: 'row', gap: 12 },
  auraStat: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  auraStatText: { fontSize: 13, color: '#e5e7eb', fontWeight: '500' },

  // Radial container
  auraRadialContainer: { width: 230, height: 230, alignSelf: 'center', position: 'relative', marginVertical: 14 },
  auraCenterCircle: { position: 'absolute', left: 90, top: 90, width: 50, height: 50, borderRadius: 25, backgroundColor: '#4c1d95', justifyContent: 'center', alignItems: 'center', zIndex: 10, borderWidth: 3, borderColor: '#7c3aed', shadowColor: '#8b5cf6', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.4, shadowRadius: 8, elevation: 6 },
  auraCenterScore: { fontSize: 19, fontWeight: '900', color: '#fff', letterSpacing: -0.5 },
  auraCenterLabel: { fontSize: 9, color: '#c4b5fd', fontWeight: '600' },

  // Planet orbs
  auraPlanetOrb: { position: 'absolute', width: 46, height: 46, borderRadius: 23, borderWidth: 2.5, justifyContent: 'center', alignItems: 'center', zIndex: 5, shadowColor: '#000', shadowOffset: { width: 0, height: 3 }, shadowOpacity: 0.3, shadowRadius: 6, elevation: 5 },
  auraPlanetSymbol: { fontSize: 17, color: '#fff', fontWeight: '600' },
  auraPlanetStrength: { position: 'absolute', bottom: -5, right: -5, width: 22, height: 22, borderRadius: 11, justifyContent: 'center', alignItems: 'center', borderWidth: 2, borderColor: '#1e1b4b', shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.2, shadowRadius: 3, elevation: 3 },
  auraPlanetScore: { fontSize: 10, fontWeight: '900', color: '#fff' },

  // Rings
  auraRings: { position: 'absolute', left: 20, top: 20, width: 180, height: 180, justifyContent: 'center', alignItems: 'center' },
  auraRing: { position: 'absolute', borderRadius: 100, borderWidth: 1, borderColor: 'rgba(167, 139, 250, 0.2)' },

  // Legend
  auraLegendScroll: { paddingVertical: 14, paddingHorizontal: 4 },
  auraLegendItem: { flexDirection: 'row', alignItems: 'center', gap: 7, backgroundColor: 'rgba(255,255,255,0.12)', paddingHorizontal: 12, paddingVertical: 8, borderRadius: 18, marginRight: 10, borderWidth: 1, shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1, shadowRadius: 4, elevation: 2 },
  auraLegendItemActive: { backgroundColor: 'rgba(255,255,255,0.25)', borderWidth: 1.5 },
  auraLegendDot: { width: 9, height: 9, borderRadius: 5, shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.2, shadowRadius: 2 },
  auraLegendName: { fontSize: 12, color: '#e5e7eb', fontWeight: '600' },
  auraLegendScore: { fontSize: 12, fontWeight: '800' },

  // Planet detail
  auraPlanetDetail: { backgroundColor: 'rgba(255,255,255,0.12)', borderRadius: 14, padding: 14, marginTop: 10, borderLeftWidth: 4, shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.08, shadowRadius: 4, elevation: 2 },
  auraPlanetDetailHeader: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  auraPlanetDetailSymbol: { fontSize: 26, color: '#fff', fontWeight: '600' },
  auraPlanetDetailName: { fontSize: 15, fontWeight: '800', color: '#fff', letterSpacing: 0.3 },
  auraPlanetDetailDomain: { fontSize: 11, color: '#a78bfa', textTransform: 'capitalize', fontWeight: '600', marginTop: 2 },
  auraPlanetDetailScore: { marginLeft: 'auto', paddingHorizontal: 12, paddingVertical: 5, borderRadius: 12, shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.15, shadowRadius: 2 },
  auraPlanetDetailScoreText: { fontSize: 14, fontWeight: '900', color: '#fff' },
  auraPlanetDetailInsight: { fontSize: 13, color: '#c4b5fd', marginTop: 10, lineHeight: 20, fontWeight: '500' },
  auraPlanetDetailTags: { flexDirection: 'row', gap: 6, marginTop: 8, flexWrap: 'wrap' },
  auraKeywordTag: { paddingHorizontal: 8, paddingVertical: 3, borderRadius: 8 },
  auraKeywordText: { fontSize: 10, fontWeight: '500' },

  // Transit summary
  auraTransitSummary: { flexDirection: 'row', alignItems: 'center', gap: 8, backgroundColor: 'rgba(167, 139, 250, 0.15)', borderRadius: 10, padding: 10, marginTop: 12 },
  auraTransitText: { flex: 1, fontSize: 11, color: '#c4b5fd', lineHeight: 16 },

  // Dominant planets
  auraDominantRow: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 14, paddingTop: 14, borderTopWidth: 1, borderTopColor: 'rgba(167, 139, 250, 0.25)' },
  auraDominantSection: { flex: 1 },
  auraDominantLabel: { fontSize: 11, color: '#9ca3af', marginBottom: 6, fontWeight: '700', textTransform: 'uppercase', letterSpacing: 0.5 },
  auraDominantList: { flexDirection: 'row', gap: 8 },
  auraDominantPlanet: { fontSize: 13, color: '#22c55e', fontWeight: '700', letterSpacing: 0.2 },

  // Transits Map - Premium Styles
  transitsContainer: { marginTop: 16, marginHorizontal: 16, borderRadius: 24, overflow: 'hidden', backgroundColor: '#1e1b4b', shadowColor: '#000', shadowOffset: { width: 0, height: 8 }, shadowOpacity: 0.3, shadowRadius: 20, elevation: 10 },
  transitsHeader: { padding: 20, paddingBottom: 16 },
  transitsHeaderContent: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start' },
  transitsHeaderLeft: { flexDirection: 'row', alignItems: 'center', gap: 14 },
  transitsHeaderIcon: { fontSize: 28 },
  transitsHeaderTitle: { fontSize: 20, fontWeight: '800', color: '#fff', letterSpacing: 0.5 },
  transitsHeaderSubtitle: { fontSize: 12, color: '#c7d2fe', marginTop: 4, fontWeight: '500' },
  livePulseContainer: { flexDirection: 'row', alignItems: 'center', gap: 8, backgroundColor: '#fff', paddingHorizontal: 12, paddingVertical: 6, borderRadius: 16, shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1, shadowRadius: 4, elevation: 3 },
  livePulseOuter: { width: 10, height: 10, borderRadius: 5, backgroundColor: '#22c55e', justifyContent: 'center', alignItems: 'center' },
  livePulseInner: { width: 6, height: 6, borderRadius: 3, backgroundColor: '#fff' },
  livePulseText: { fontSize: 11, fontWeight: '900', color: '#1e293b', letterSpacing: 0.5 },

  // Moon Hero Section
  moonHeroSection: { padding: 24, backgroundColor: '#fff', borderTopWidth: 1, borderTopColor: 'rgba(139, 92, 246, 0.1)' },
  moonHeroHeader: { flexDirection: 'row', alignItems: 'center', gap: 16 },
  moonHeroIconContainer: { position: 'relative', backgroundColor: '#fef3c7', width: 64, height: 64, borderRadius: 32, alignItems: 'center', justifyContent: 'center' },
  moonHeroIcon: { fontSize: 36 },
  moonHeroGlow: { position: 'absolute', width: 64, height: 64, borderRadius: 32, backgroundColor: '#fbbf24', opacity: 0.2, top: 0, left: 0 },
  moonHeroInfo: { flex: 1 },
  moonHeroLabel: { fontSize: 11, color: '#6366f1', textTransform: 'uppercase', letterSpacing: 1.2, fontWeight: '700', marginBottom: 6 },
  moonHeroSign: { fontSize: 24, fontWeight: '800', color: '#1e293b', marginBottom: 4 },
  moonHeroPhase: { fontSize: 13, color: '#64748b', fontWeight: '600' },
  moonEnergyCard: { paddingHorizontal: 16, paddingVertical: 12, borderRadius: 16, alignItems: 'center', backgroundColor: '#fff', borderWidth: 2, borderColor: '#e2e8f0' },
  moonEnergyEmoji: { fontSize: 24, marginBottom: 4 },
  moonEnergyMood: { fontSize: 12, fontWeight: '800', textAlign: 'center', textTransform: 'capitalize' },

  // Countdown Timer
  countdownContainer: { alignItems: 'center', marginTop: 28, paddingTop: 28, borderTopWidth: 2, borderTopColor: '#f1f5f9', backgroundColor: '#fafafa', marginHorizontal: -24, paddingHorizontal: 24, paddingBottom: 24 },
  countdownLabel: { fontSize: 13, color: '#6366f1', marginBottom: 16, fontWeight: '700', textTransform: 'uppercase', letterSpacing: 1 },
  countdownTimerRow: { flexDirection: 'row', alignItems: 'center', gap: 16 },
  countdownBox: { alignItems: 'center' },
  countdownBoxGradient: { width: 80, height: 80, borderRadius: 20, justifyContent: 'center', alignItems: 'center', shadowColor: '#6366f1', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.3, shadowRadius: 8, elevation: 5 },
  countdownValue: { fontSize: 36, fontWeight: '900', color: '#fff' },
  countdownUnit: { fontSize: 11, color: '#64748b', marginTop: 8, textTransform: 'uppercase', letterSpacing: 1.5, fontWeight: '700' },
  countdownSeparator: { fontSize: 36, fontWeight: '800', color: '#6366f1', marginBottom: 24 },
  nextSignRow: { flexDirection: 'row', alignItems: 'center', gap: 10, marginTop: 20, backgroundColor: '#6366f1', paddingHorizontal: 20, paddingVertical: 12, borderRadius: 24, shadowColor: '#6366f1', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.3, shadowRadius: 8, elevation: 4 },
  nextSignText: { fontSize: 15, fontWeight: '700', color: '#fff', flex: 1 },

  // Alert Message
  alertMessageBox: { flexDirection: 'row', alignItems: 'flex-start', gap: 14, backgroundColor: '#fffbeb', padding: 18, paddingVertical: 20, marginTop: 24, marginHorizontal: -24, marginBottom: -24, borderLeftWidth: 4, borderLeftColor: '#f59e0b' },
  alertMessageIconWrapper: { marginTop: 2, width: 24, height: 24, alignItems: 'center', justifyContent: 'center' },
  alertMessageText: { flex: 1, fontSize: 14, color: '#92400e', lineHeight: 22, fontWeight: '600', letterSpacing: 0.2 },

  // Orbital View
  orbitalSection: { padding: 28, paddingTop: 28, backgroundColor: '#0f172a', borderTopWidth: 1, borderTopColor: 'rgba(139, 92, 246, 0.2)' },
  orbitalTitle: { fontSize: 15, fontWeight: '700', color: '#e0e7ff', marginBottom: 24, textAlign: 'center', textTransform: 'uppercase', letterSpacing: 1.5 },
  orbitalContainer: { width: 170, height: 170, alignSelf: 'center', position: 'relative' },
  orbitalRingOuter: { position: 'absolute', width: 170, height: 170, borderRadius: 85, borderWidth: 1, borderColor: 'rgba(139, 92, 246, 0.2)' },
  orbitalRingMiddle: { position: 'absolute', width: 120, height: 120, borderRadius: 60, borderWidth: 1, borderColor: 'rgba(139, 92, 246, 0.15)', left: 25, top: 25 },
  orbitalRingInner: { position: 'absolute', width: 70, height: 70, borderRadius: 35, borderWidth: 1, borderColor: 'rgba(139, 92, 246, 0.1)', left: 50, top: 50 },
  orbitalPlanet: { position: 'absolute', width: 30, height: 30, borderRadius: 15, borderWidth: 2, justifyContent: 'center', alignItems: 'center', shadowOffset: { width: 0, height: 0 }, shadowOpacity: 0.5, shadowRadius: 8, elevation: 5 },
  orbitalPlanetSymbol: { fontSize: 14, fontWeight: '600' },
  earthCenter: { position: 'absolute', left: 70, top: 70, width: 30, height: 30, borderRadius: 15, backgroundColor: 'rgba(59, 130, 246, 0.3)', justifyContent: 'center', alignItems: 'center' },
  earthEmoji: { fontSize: 16 },

  // Planet Cards
  planetCardsSection: { paddingBottom: 24, paddingTop: 24, backgroundColor: '#1e1b4b', borderTopWidth: 1, borderTopColor: 'rgba(139, 92, 246, 0.2)' },
  planetCardsTitle: { fontSize: 15, fontWeight: '700', color: '#e0e7ff', marginBottom: 16, paddingHorizontal: 20, textTransform: 'uppercase', letterSpacing: 1.5 },
  planetCardsScroll: { paddingHorizontal: 16 },
  planetCard: { alignItems: 'center', paddingHorizontal: 16, paddingVertical: 16, borderRadius: 20, marginRight: 14, borderWidth: 2, minWidth: 95, shadowColor: '#000', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.3, shadowRadius: 8, elevation: 5 },
  planetCardIconBg: { width: 48, height: 48, borderRadius: 24, justifyContent: 'center', alignItems: 'center', marginBottom: 10 },
  planetCardSymbol: { fontSize: 24 },
  planetCardName: { fontSize: 12, color: '#fff', fontWeight: '700', marginBottom: 8, textTransform: 'uppercase', letterSpacing: 0.5 },
  planetCardSignRow: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  planetCardSign: { fontSize: 16, fontWeight: '800' },
  planetCardSignName: { fontSize: 11, color: '#e0e7ff', fontWeight: '600' },
  planetCardDegree: { fontSize: 10, color: '#c7d2fe', marginTop: 6, fontWeight: '500' },
  retroIndicator: { backgroundColor: 'rgba(239, 68, 68, 0.2)', paddingHorizontal: 8, paddingVertical: 3, borderRadius: 8, marginTop: 6 },
  retroIndicatorText: { fontSize: 9, color: '#fca5a5', fontWeight: '600' },

  // Retrograde Alert
  retroAlertSection: { padding: 16, paddingTop: 0 },
  retroAlertHeader: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 12 },
  retroAlertIcon: { fontSize: 18 },
  retroAlertTitle: { fontSize: 14, fontWeight: '700', color: '#fbbf24' },
  retroAlertCard: { borderRadius: 14, padding: 14, marginBottom: 10, borderLeftWidth: 4 },
  retroAlertCardHeader: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  retroAlertSymbol: { fontSize: 22, color: '#fff' },
  retroAlertInfo: { flex: 1 },
  retroAlertName: { fontSize: 14, fontWeight: '600', color: '#fff' },
  retroStatusPill: { paddingHorizontal: 8, paddingVertical: 3, borderRadius: 10, marginTop: 4, alignSelf: 'flex-start' },
  retroStatusText: { fontSize: 10, fontWeight: '600' },
  retroDaysLeft: { alignItems: 'center', backgroundColor: 'rgba(251, 191, 36, 0.15)', paddingHorizontal: 12, paddingVertical: 6, borderRadius: 10 },
  retroDaysNumber: { fontSize: 18, fontWeight: '800', color: '#fbbf24' },
  retroDaysLabel: { fontSize: 9, color: '#94a3b8' },
  retroAlertMessage: { fontSize: 11, color: '#94a3b8', marginTop: 10, lineHeight: 16 },

  // Upcoming Section
  upcomingSection: { padding: 16, paddingTop: 0 },
  upcomingSectionTitle: { fontSize: 14, fontWeight: '600', color: '#e2e8f0', marginBottom: 12 },
  upcomingCard: { flexDirection: 'row', alignItems: 'center', gap: 12, backgroundColor: 'rgba(255,255,255,0.04)', borderRadius: 14, padding: 12, marginBottom: 10 },
  upcomingIconBox: { width: 44, height: 44, borderRadius: 22, justifyContent: 'center', alignItems: 'center' },
  upcomingIcon: { fontSize: 20 },
  upcomingDetails: { flex: 1 },
  upcomingPlanet: { fontSize: 14, fontWeight: '600', color: '#fff' },
  upcomingArrowRow: { flexDirection: 'row', alignItems: 'center', gap: 6, marginTop: 4 },
  upcomingFrom: { fontSize: 11, color: '#94a3b8' },
  upcomingTo: { fontSize: 11, color: '#a78bfa', fontWeight: '500' },
  upcomingTimeBox: { alignItems: 'center', backgroundColor: 'rgba(99, 102, 241, 0.2)', paddingHorizontal: 14, paddingVertical: 8, borderRadius: 12 },
  upcomingTimeValue: { fontSize: 18, fontWeight: '800', color: '#818cf8' },
  upcomingTimeUnit: { fontSize: 9, color: '#94a3b8', marginTop: 2 },

  // Auspicious Footer
  auspiciousFooter: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, padding: 14, borderTopWidth: 1, borderTopColor: 'rgba(139, 92, 246, 0.1)' },
  auspiciousText: { fontSize: 13, fontWeight: '600' },
});
