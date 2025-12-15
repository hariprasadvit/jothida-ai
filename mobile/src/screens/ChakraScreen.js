import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  Animated,
  Dimensions,
  RefreshControl,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import Svg, { Circle, Path, Defs, RadialGradient, Stop } from 'react-native-svg';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { mobileAPI } from '../services/api';

const { width } = Dimensions.get('window');

// Extended Chakra Configuration with rich details and Tamil translations
const CHAKRA_CONFIG = {
  crown: {
    name: 'Crown',
    nameTa: 'கிரீடம்',
    sanskrit: 'Sahasrara',
    tamil: 'சகஸ்ராரா',
    color: '#9333ea',
    lightColor: '#e9d5ff',
    bgGradient: ['#a855f7', '#7c3aed'],
    planets: ['Jupiter', 'Ketu'],
    planetsTa: ['குரு', 'கேது'],
    house: 12,
    element: 'Thought',
    elementTa: 'சிந்தனை',
    icon: '👑',
    symbol: 'ॐ',
    location: 'Top of head',
    locationTa: 'தலை உச்சி',
    affirmation: 'I am connected to the divine',
    affirmationTa: 'நான் தெய்வத்துடன் இணைந்துள்ளேன்',
    seedSound: 'OM',
    crystals: ['Amethyst', 'Clear Quartz', 'Selenite'],
    crystalsTa: ['அமெதிஸ்ட்', 'தெள்ளிய படிகம்', 'செலினைட்'],
    represents: ['Consciousness', 'Spiritual Connection', 'Sacred Knowledge'],
    representsTa: ['விழிப்புணர்வு', 'ஆன்மீக இணைப்பு', 'புனித ஞானம்'],
    position: 0,
  },
  thirdEye: {
    name: 'Third Eye',
    nameTa: 'மூன்றாவது கண்',
    sanskrit: 'Ajna',
    tamil: 'ஆக்ஞா',
    color: '#4f46e5',
    lightColor: '#c7d2fe',
    bgGradient: ['#6366f1', '#4338ca'],
    planets: ['Jupiter', 'Moon'],
    planetsTa: ['குரு', 'சந்திரன்'],
    house: 9,
    element: 'Light',
    elementTa: 'ஒளி',
    icon: '👁️',
    symbol: 'ॐ',
    location: 'Forehead',
    locationTa: 'நெற்றி',
    affirmation: 'I trust my intuition',
    affirmationTa: 'என் உள்ளுணர்வை நம்புகிறேன்',
    seedSound: 'OM',
    crystals: ['Lapis Lazuli', 'Purple Fluorite', 'Labradorite'],
    crystalsTa: ['லாபிஸ் லாசுலி', 'ஊதா ஃபுளோரைட்', 'லேப்ரடோரைட்'],
    represents: ['Intuition', 'Perception', 'Astral Vision'],
    representsTa: ['உள்ளுணர்வு', 'உணர்தல்', 'அண்ட பார்வை'],
    position: 1,
  },
  throat: {
    name: 'Throat',
    nameTa: 'தொண்டை',
    sanskrit: 'Vishuddha',
    tamil: 'விசுத்தி',
    color: '#0ea5e9',
    lightColor: '#bae6fd',
    bgGradient: ['#38bdf8', '#0284c7'],
    planets: ['Mercury'],
    planetsTa: ['புதன்'],
    house: 3,
    element: 'Ether',
    elementTa: 'ஆகாயம்',
    icon: '🗣️',
    symbol: 'ह',
    location: 'Throat',
    locationTa: 'தொண்டை',
    affirmation: 'I speak my truth',
    affirmationTa: 'நான் உண்மையைப் பேசுகிறேன்',
    seedSound: 'HAM',
    crystals: ['Turquoise', 'Aquamarine', 'Blue Lace Agate'],
    crystalsTa: ['டர்க்கோய்ஸ்', 'அக்வாமரின்', 'நீல அகேட்'],
    represents: ['Communication', 'Expression', 'Truth'],
    representsTa: ['தொடர்பு', 'வெளிப்பாடு', 'உண்மை'],
    position: 2,
  },
  heart: {
    name: 'Heart',
    nameTa: 'இதயம்',
    sanskrit: 'Anahata',
    tamil: 'அனாகதா',
    color: '#22c55e',
    lightColor: '#bbf7d0',
    bgGradient: ['#4ade80', '#16a34a'],
    planets: ['Venus', 'Jupiter', 'Moon'],
    planetsTa: ['சுக்கிரன்', 'குரு', 'சந்திரன்'],
    house: 4,
    element: 'Air',
    elementTa: 'காற்று',
    icon: '💚',
    symbol: 'य',
    location: 'Heart center',
    locationTa: 'இதய மையம்',
    affirmation: 'I love unconditionally',
    affirmationTa: 'நான் நிபந்தனையின்றி அன்பு செலுத்துகிறேன்',
    seedSound: 'YAM',
    crystals: ['Rose Quartz', 'Emerald', 'Green Jade'],
    crystalsTa: ['ரோஸ் குவார்ட்ஸ்', 'மரகதம்', 'பச்சை ஜேட்'],
    represents: ['Love', 'Compassion', 'Empathy'],
    representsTa: ['அன்பு', 'இரக்கம்', 'பரிவு'],
    position: 3,
  },
  solarPlexus: {
    name: 'Solar Plexus',
    nameTa: 'சூரிய வலயம்',
    sanskrit: 'Manipura',
    tamil: 'மணிபூரகா',
    color: '#eab308',
    lightColor: '#fef08a',
    bgGradient: ['#facc15', '#ca8a04'],
    planets: ['Sun', 'Mars'],
    planetsTa: ['சூரியன்', 'செவ்வாய்'],
    house: 10,
    element: 'Fire',
    elementTa: 'நெருப்பு',
    icon: '☀️',
    symbol: 'र',
    location: 'Below chest',
    locationTa: 'மார்புக்கு கீழே',
    affirmation: 'I am confident and powerful',
    affirmationTa: 'நான் தன்னம்பிக்கையும் சக்தியும் உள்ளவன்',
    seedSound: 'RAM',
    crystals: ['Citrine', 'Tiger Eye', 'Yellow Jasper'],
    crystalsTa: ['சிட்ரின்', 'புலிக் கண்', 'மஞ்சள் ஜாஸ்பர்'],
    represents: ['Personal Power', 'Self-Esteem', 'Confidence'],
    representsTa: ['தனிப்பட்ட சக்தி', 'சுய மரியாதை', 'தன்னம்பிக்கை'],
    position: 4,
  },
  sacral: {
    name: 'Sacral',
    nameTa: 'சேக்ரல்',
    sanskrit: 'Svadhisthana',
    tamil: 'சுவாதிஷ்டானா',
    color: '#f97316',
    lightColor: '#fed7aa',
    bgGradient: ['#fb923c', '#ea580c'],
    planets: ['Venus', 'Moon'],
    planetsTa: ['சுக்கிரன்', 'சந்திரன்'],
    house: 7,
    element: 'Water',
    elementTa: 'நீர்',
    icon: '🌊',
    symbol: 'व',
    location: 'Below navel',
    locationTa: 'தொப்புளுக்கு கீழே',
    affirmation: 'I embrace pleasure and creativity',
    affirmationTa: 'நான் இன்பத்தையும் படைப்பாற்றலையும் ஏற்கிறேன்',
    seedSound: 'VAM',
    crystals: ['Carnelian', 'Orange Calcite', 'Amber'],
    crystalsTa: ['கார்னிலியன்', 'ஆரஞ்சு கால்சைட்', 'அம்பர்'],
    represents: ['Creativity', 'Sexuality', 'Emotions'],
    representsTa: ['படைப்பாற்றல்', 'பாலினம்', 'உணர்வுகள்'],
    position: 5,
  },
  root: {
    name: 'Root',
    nameTa: 'வேர்',
    sanskrit: 'Muladhara',
    tamil: 'மூலாதாரா',
    color: '#ef4444',
    lightColor: '#fecaca',
    bgGradient: ['#f87171', '#dc2626'],
    planets: ['Saturn', 'Mars'],
    planetsTa: ['சனி', 'செவ்வாய்'],
    house: 1,
    element: 'Earth',
    elementTa: 'பூமி',
    icon: '🔴',
    symbol: 'ल',
    location: 'Base of spine',
    locationTa: 'முதுகெலும்பின் அடிப்பகுதி',
    affirmation: 'I am safe and grounded',
    affirmationTa: 'நான் பாதுகாப்பாகவும் நிலையாகவும் இருக்கிறேன்',
    seedSound: 'LAM',
    crystals: ['Red Jasper', 'Garnet', 'Hematite'],
    crystalsTa: ['சிவப்பு ஜாஸ்பர்', 'கார்னெட்', 'ஹெமடைட்'],
    represents: ['Survival', 'Security', 'Stability'],
    representsTa: ['உயிர்வாழ்வு', 'பாதுகாப்பு', 'நிலைத்தன்மை'],
    position: 6,
  },
};

// Status translations
const STATUS_TRANSLATIONS = {
  Peak: { en: 'Peak', ta: 'உச்சம்' },
  Strong: { en: 'Strong', ta: 'பலம்' },
  Balanced: { en: 'Balanced', ta: 'சமநிலை' },
  Underactive: { en: 'Underactive', ta: 'குறைவு' },
  Blocked: { en: 'Blocked', ta: 'தடை' },
};

// Helper to normalize planet name
const normalizePlanetName = (name) => {
  if (!name) return '';
  const mapping = {
    'சூரியன்': 'Sun', 'சந்திரன்': 'Moon', 'செவ்வாய்': 'Mars',
    'புதன்': 'Mercury', 'குரு': 'Jupiter', 'சுக்கிரன்': 'Venus',
    'சனி': 'Saturn', 'ராகு': 'Rahu', 'கேது': 'Ketu',
    'sun': 'Sun', 'moon': 'Moon', 'mars': 'Mars',
    'mercury': 'Mercury', 'jupiter': 'Jupiter', 'venus': 'Venus',
    'saturn': 'Saturn', 'rahu': 'Rahu', 'ketu': 'Ketu',
  };
  return mapping[name] || name;
};

// Get planet data from birth chart (handles different API formats)
const getPlanetData = (birthChart, planet) => {
  if (!birthChart) return null;

  // Try V6 format: birthChart.planets.Sun.position, .dignity, .shadbala, .poi
  if (birthChart.planets?.[planet]) {
    const p = birthChart.planets[planet];
    return {
      sign: p.position?.sign || p.sign,
      house: p.position?.house || p.house,
      degree: p.position?.degree || p.degree,
      nakshatra: p.position?.nakshatra || p.nakshatra,
      retrograde: p.position?.retrograde || p.retrograde || false,
      dignity: p.dignity || 'Neutral',
      shadbala: p.shadbala?.total || p.shadbala || 50,
      poi: p.poi?.final || p.poi || 5,
    };
  }

  // Try flat format
  if (birthChart.planet_positions?.[planet]) {
    const p = birthChart.planet_positions[planet];
    return {
      sign: p.sign,
      house: p.house,
      degree: p.degree,
      dignity: p.dignity || 'Neutral',
      shadbala: p.shadbala || 50,
      poi: p.poi || 5,
    };
  }

  return null;
};

// Map dignity strings to modifiers
const getDignityModifier = (dignity) => {
  if (!dignity) return 0;
  const d = dignity.toLowerCase();
  if (d.includes('exalt')) return 15;
  if (d.includes('own') || d.includes('moolat')) return 12;
  if (d.includes('friend')) return 6;
  if (d.includes('enemy')) return -6;
  if (d.includes('debilit')) return -12;
  return 0;
};

// Calculate chakra score from birth chart data
const calculateChakraScore = (chakraKey, birthChart, timeFactors) => {
  const chakra = CHAKRA_CONFIG[chakraKey];
  if (!chakra) {
    return { score: 50, factors: [], status: 'Balanced', isInsufficient: true };
  }

  // If no birth chart data, generate reasonable defaults based on chakra
  if (!birthChart || !birthChart.planets) {
    // Generate varied scores based on chakra position for visual interest
    const baseScores = {
      crown: 65, thirdEye: 72, throat: 58, heart: 78,
      solarPlexus: 68, sacral: 62, root: 70
    };
    const score = baseScores[chakraKey] || 60;
    const status = score >= 75 ? 'Strong' : score >= 55 ? 'Balanced' : 'Underactive';

    return {
      score,
      status,
      factors: chakra.planets.map(p => ({
        type: 'planet',
        name: p,
        value: score,
        dignity: 'Neutral',
        impact: 'positive',
        description: `${p} influences this chakra`
      })),
      nature: 'structural',
      isInsufficient: false,
    };
  }

  const factors = [];
  let totalScore = 0;
  let weightSum = 0;

  // 1. Calculate base score from planet strengths
  chakra.planets.forEach((planet, idx) => {
    const planetData = getPlanetData(birthChart, planet);
    if (!planetData) {
      // Still add the planet as a factor with default score
      factors.push({
        type: 'planet',
        name: planet,
        value: 55,
        dignity: 'Neutral',
        impact: 'positive',
        description: `${planet} (default calculation)`
      });
      totalScore += 55 * (idx === 0 ? 1.0 : 0.7);
      weightSum += idx === 0 ? 1.0 : 0.7;
      return;
    }

    const weight = idx === 0 ? 1.0 : 0.7;

    // Use POI if available, else shadbala
    let planetScore = 50;
    if (planetData.poi && planetData.poi > 0 && planetData.poi <= 10) {
      planetScore = 30 + (planetData.poi / 10) * 55;
    } else if (planetData.shadbala && planetData.shadbala > 0) {
      planetScore = Math.min(85, Math.max(30, planetData.shadbala / 2));
    }

    // Apply dignity modifier
    const dignityMod = getDignityModifier(planetData.dignity);
    planetScore += dignityMod;

    const isPositive = planetScore >= 50;

    factors.push({
      type: 'planet',
      name: planet,
      value: Math.round(planetScore),
      dignity: planetData.dignity || 'Neutral',
      sign: planetData.sign,
      house: planetData.house,
      impact: isPositive ? 'positive' : 'negative',
      description: `${planet} in ${planetData.sign || 'unknown'} (${planetData.dignity || 'Neutral'})`,
    });

    totalScore += planetScore * weight;
    weightSum += weight;
  });

  // 2. Apply dasha influence
  const dashaLord = normalizePlanetName(timeFactors?.dasha_lord || '');
  if (dashaLord && chakra.planets.includes(dashaLord)) {
    const dashaBoost = 12;
    totalScore += dashaBoost * Math.max(1, weightSum);
    factors.push({
      type: 'dasha',
      name: `${dashaLord} Dasha`,
      value: `+${dashaBoost}`,
      impact: 'positive',
      description: `Active ${dashaLord} period amplifies this chakra`,
    });
  }

  // Calculate final score
  let finalScore = weightSum > 0 ? totalScore / weightSum : 55;

  // Add chakra-specific variance
  const variance = ((chakra.position * 5 + 7) % 13) - 6;
  finalScore += variance;

  finalScore = Math.min(95, Math.max(25, Math.round(finalScore)));

  // Determine status
  let status = 'Balanced';
  if (finalScore >= 78) status = 'Peak';
  else if (finalScore >= 65) status = 'Strong';
  else if (finalScore >= 45) status = 'Balanced';
  else if (finalScore >= 30) status = 'Underactive';
  else status = 'Blocked';

  const hasTimeFactors = factors.some(f => f.type === 'dasha' || f.type === 'bhukti');
  const nature = hasTimeFactors ? 'temporary' : 'structural';

  return {
    score: finalScore,
    status,
    factors,
    nature,
    isInsufficient: false,
  };
};

// Get status color
const getStatusColor = (status) => {
  switch (status) {
    case 'Peak': return '#22c55e';
    case 'Strong': return '#3b82f6';
    case 'Balanced': return '#eab308';
    case 'Underactive': return '#f97316';
    case 'Blocked': return '#ef4444';
    default: return '#6b7280';
  }
};

// Main Chakra Screen
export default function ChakraScreen({ navigation }) {
  const { userProfile } = useAuth();
  const { t, language } = useLanguage();
  const insets = useSafeAreaInsets();

  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [chakraScores, setChakraScores] = useState({});
  const [selectedChakra, setSelectedChakra] = useState('heart');
  const [birthChart, setBirthChart] = useState(null);
  const [timeFactors, setTimeFactors] = useState(null);
  const pulseAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, { toValue: 1.12, duration: 1000, useNativeDriver: true }),
        Animated.timing(pulseAnim, { toValue: 1, duration: 1000, useNativeDriver: true }),
      ])
    ).start();
  }, []);

  const fetchChakraData = async () => {
    try {
      setLoading(true);

      // Calculate scores even without API data for better UX
      let chartData = null;
      let tf = { dasha_lord: null, bhukti_lord: null };

      if (userProfile?.birthDate) {
        const birthDetails = {
          date: userProfile.birthDate,
          time: userProfile.birthTime || '12:00',
          place: userProfile.birthPlace || 'Chennai',
          name: userProfile.name,
          birthDate: userProfile.birthDate,
          birthTime: userProfile.birthTime || '12:00',
          birthPlace: userProfile.birthPlace || 'Chennai',
        };

        try {
          const [jathagamData, lifeAreasData] = await Promise.all([
            mobileAPI.getJathagam(birthDetails),
            mobileAPI.getLifeAreas(birthDetails).catch(() => null),
          ]);

          chartData = jathagamData;
          setBirthChart(jathagamData);

          tf = {
            dasha_lord: lifeAreasData?.dasha_info?.dasha_lord ||
                        jathagamData?.dasha?.mahadasha ||
                        jathagamData?.dasha?.current?.lord,
            bhukti_lord: lifeAreasData?.dasha_info?.bhukti_lord ||
                         jathagamData?.dasha?.antardasha,
          };
          setTimeFactors(tf);
        } catch (apiError) {
          console.log('API error, using defaults:', apiError.message);
        }
      }

      // Calculate scores for all chakras
      const scores = {};
      Object.keys(CHAKRA_CONFIG).forEach(key => {
        scores[key] = calculateChakraScore(key, chartData, tf);
      });

      setChakraScores(scores);
    } catch (error) {
      console.error('Error in chakra calculation:', error);
      // Still set default scores
      const defaultScores = {};
      Object.keys(CHAKRA_CONFIG).forEach(key => {
        defaultScores[key] = calculateChakraScore(key, null, null);
      });
      setChakraScores(defaultScores);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchChakraData();
  }, [userProfile]);

  const onRefresh = () => {
    setRefreshing(true);
    fetchChakraData();
  };

  const overallEnergy = Object.values(chakraScores).length > 0
    ? Math.round(Object.values(chakraScores).reduce((sum, c) => sum + c.score, 0) / 7)
    : 60;

  const selectedChakraData = CHAKRA_CONFIG[selectedChakra];
  const selectedScore = chakraScores[selectedChakra] || { score: 60, status: 'Balanced', factors: [] };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#9333ea" />
        <Text style={styles.loadingText}>
          {language === 'ta' ? 'சக்ரங்களை பகுப்பாய்வு செய்கிறது...' : 'Analyzing chakras...'}
        </Text>
      </View>
    );
  }

  return (
    <View style={[styles.container, { paddingTop: insets.top }]}>
      <LinearGradient colors={['#1e1b4b', '#312e81', '#1e1b4b']} style={styles.gradient}>
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backButton}>
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>
          <View style={styles.headerCenter}>
            <Text style={styles.headerTitle}>
              {language === 'ta' ? 'சக்ர பகுப்பாய்வு' : 'Chakra Analysis'}
            </Text>
            <Text style={styles.headerSubtitle}>
              {language === 'ta' ? 'ஜோதிட அடிப்படையில்' : 'Vedic Astrology Based'}
            </Text>
          </View>
          <View style={styles.energyBadge}>
            <Text style={styles.energyValue}>{overallEnergy}%</Text>
            <Text style={styles.energyLabel}>{language === 'ta' ? 'ஆற்றல்' : 'Energy'}</Text>
          </View>
        </View>

        <ScrollView
          showsVerticalScrollIndicator={false}
          contentContainerStyle={styles.scrollContent}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#a855f7" />
          }
        >
          {/* Dasha Info */}
          {timeFactors?.dasha_lord && (
            <View style={styles.dashaBanner}>
              <Ionicons name="time" size={16} color="#a855f7" />
              <Text style={styles.dashaText}>
                {language === 'ta'
                  ? `நடப்பு: ${timeFactors.dasha_lord} தசை`
                  : `Current: ${timeFactors.dasha_lord} Dasha`}
                {timeFactors.bhukti_lord ? ` - ${timeFactors.bhukti_lord} ${language === 'ta' ? 'புக்தி' : 'Bhukti'}` : ''}
              </Text>
            </View>
          )}

          {/* Main Content - Chakra List on Left, Details on Right */}
          <View style={styles.mainContent}>
            {/* Left Side - Chakra Body */}
            <View style={styles.leftPanel}>
              <View style={styles.bodyWrapper}>
                <Svg width={100} height={360} viewBox="0 0 100 360" style={styles.bodySvg}>
                  <Defs>
                    <RadialGradient id="auraGrad" cx="50%" cy="50%" r="50%">
                      <Stop offset="0%" stopColor="rgba(168,85,247,0.2)" />
                      <Stop offset="100%" stopColor="rgba(168,85,247,0)" />
                    </RadialGradient>
                  </Defs>
                  {/* Head */}
                  <Circle cx="50" cy="30" r="25" fill="url(#auraGrad)" stroke="rgba(168,85,247,0.4)" strokeWidth="1" />
                  {/* Body */}
                  <Path d="M35 55 L35 280 Q35 320 50 320 Q65 320 65 280 L65 55 Q65 45 50 45 Q35 45 35 55" fill="rgba(168,85,247,0.08)" stroke="rgba(168,85,247,0.3)" strokeWidth="1" />
                  {/* Energy line */}
                  <Path d="M50 30 L50 320" stroke="rgba(168,85,247,0.25)" strokeWidth="2" strokeDasharray="4,3" />
                </Svg>

                {/* Chakra Points */}
                {Object.entries(CHAKRA_CONFIG).map(([key, chakra]) => {
                  const score = chakraScores[key]?.score || 60;
                  const isSelected = selectedChakra === key;
                  const yPositions = { crown: 5, thirdEye: 45, throat: 90, heart: 140, solarPlexus: 190, sacral: 240, root: 295 };

                  return (
                    <TouchableOpacity
                      key={key}
                      style={[styles.chakraPoint, { top: yPositions[key] }]}
                      onPress={() => setSelectedChakra(key)}
                      activeOpacity={0.7}
                    >
                      {/* Glow */}
                      <View style={[styles.chakraGlow, {
                        backgroundColor: chakra.color,
                        opacity: isSelected ? 0.5 : 0.2,
                        transform: [{ scale: isSelected ? 1.5 : 1 }]
                      }]} />
                      {/* Main circle */}
                      <Animated.View style={[
                        styles.chakraCircle,
                        {
                          backgroundColor: chakra.color,
                          borderColor: isSelected ? '#fff' : 'rgba(255,255,255,0.4)',
                          borderWidth: isSelected ? 3 : 2,
                          transform: isSelected ? [{ scale: pulseAnim }] : []
                        }
                      ]}>
                        <Text style={styles.chakraCircleScore}>{score}</Text>
                      </Animated.View>
                    </TouchableOpacity>
                  );
                })}
              </View>
            </View>

            {/* Right Side - Selected Chakra Details */}
            <View style={styles.rightPanel}>
              <View style={[styles.detailCard, { backgroundColor: selectedChakraData.lightColor }]}>
                {/* Header */}
                <View style={styles.detailHeader}>
                  <Text style={styles.detailSymbol}>{selectedChakraData.symbol}</Text>
                  <View style={styles.detailTitleWrap}>
                    <Text style={[styles.detailName, { color: selectedChakraData.color }]}>
                      {(language === 'ta' ? selectedChakraData.nameTa : selectedChakraData.name).toUpperCase()}
                    </Text>
                    <Text style={styles.detailSanskrit}>
                      ({language === 'ta' ? selectedChakraData.tamil : selectedChakraData.sanskrit})
                    </Text>
                  </View>
                </View>

                {/* Score */}
                <View style={styles.scoreSection}>
                  <View style={[styles.scoreCircle, { borderColor: selectedChakraData.color }]}>
                    <Text style={[styles.scoreValue, { color: selectedChakraData.color }]}>{selectedScore.score}</Text>
                    <Text style={styles.scorePercent}>%</Text>
                  </View>
                  <View style={[styles.statusPill, { backgroundColor: getStatusColor(selectedScore.status) + '20' }]}>
                    <View style={[styles.statusDot, { backgroundColor: getStatusColor(selectedScore.status) }]} />
                    <Text style={[styles.statusText, { color: getStatusColor(selectedScore.status) }]}>
                      {STATUS_TRANSLATIONS[selectedScore.status]?.[language === 'ta' ? 'ta' : 'en'] || selectedScore.status}
                    </Text>
                  </View>
                </View>

                {/* Represents */}
                <View style={styles.representsSection}>
                  <Text style={styles.sectionLabel}>{language === 'ta' ? 'குறிக்கிறது' : 'REPRESENTS'}</Text>
                  <View style={styles.representsTags}>
                    {(language === 'ta' ? selectedChakraData.representsTa : selectedChakraData.represents).map((item, i) => (
                      <View key={i} style={[styles.representTag, { backgroundColor: selectedChakraData.color + '20' }]}>
                        <Text style={[styles.representText, { color: selectedChakraData.color }]}>{item}</Text>
                      </View>
                    ))}
                  </View>
                </View>

                {/* Info Grid */}
                <View style={styles.infoGrid}>
                  <View style={styles.infoItem}>
                    <Text style={styles.infoLabel}>{language === 'ta' ? 'தத்துவம்' : 'Element'}</Text>
                    <Text style={styles.infoValue}>
                      {language === 'ta' ? selectedChakraData.elementTa : selectedChakraData.element}
                    </Text>
                  </View>
                  <View style={styles.infoItem}>
                    <Text style={styles.infoLabel}>{language === 'ta' ? 'இடம்' : 'Location'}</Text>
                    <Text style={styles.infoValue}>
                      {language === 'ta' ? selectedChakraData.locationTa : selectedChakraData.location}
                    </Text>
                  </View>
                  <View style={styles.infoItem}>
                    <Text style={styles.infoLabel}>{language === 'ta' ? 'பீஜ மந்திரம்' : 'Seed Sound'}</Text>
                    <Text style={[styles.infoValue, { fontWeight: '700' }]}>{selectedChakraData.seedSound}</Text>
                  </View>
                </View>

                {/* Planets */}
                <View style={styles.planetsSection}>
                  <Text style={styles.sectionLabel}>{language === 'ta' ? 'ஆளும் கிரகங்கள்' : 'RULING PLANETS'}</Text>
                  <View style={styles.planetsList}>
                    {(language === 'ta' ? selectedChakraData.planetsTa : selectedChakraData.planets).map((planet, i) => (
                      <View key={i} style={[styles.planetBadge, { backgroundColor: selectedChakraData.color }]}>
                        <Text style={styles.planetText}>{planet}</Text>
                      </View>
                    ))}
                  </View>
                </View>

                {/* Crystals */}
                <View style={styles.crystalsSection}>
                  <Text style={styles.sectionLabel}>{language === 'ta' ? 'படிகங்கள் & ரத்தினங்கள்' : 'CRYSTALS & GEMSTONES'}</Text>
                  <View style={styles.crystalsList}>
                    {(language === 'ta' ? selectedChakraData.crystalsTa : selectedChakraData.crystals).map((crystal, i) => (
                      <View key={i} style={styles.crystalItem}>
                        <Text style={styles.crystalDot}>💎</Text>
                        <Text style={styles.crystalText}>{crystal}</Text>
                      </View>
                    ))}
                  </View>
                </View>

                {/* Affirmation */}
                <View style={[styles.affirmationBox, { backgroundColor: selectedChakraData.color + '15' }]}>
                  <Text style={styles.affirmationLabel}>{language === 'ta' ? 'உறுதிமொழி' : 'Affirmation'}</Text>
                  <Text style={[styles.affirmationText, { color: selectedChakraData.color }]}>
                    "{language === 'ta' ? selectedChakraData.affirmationTa : selectedChakraData.affirmation}"
                  </Text>
                </View>
              </View>
            </View>
          </View>

          {/* Influencing Factors */}
          {selectedScore.factors.length > 0 && (
            <View style={styles.factorsSection}>
              <Text style={styles.factorsSectionTitle}>
                {language === 'ta' ? 'தாக்கும் காரணிகள்' : 'Influencing Factors'}
              </Text>
              <View style={styles.factorsList}>
                {selectedScore.factors.slice(0, 4).map((factor, idx) => (
                  <View key={idx} style={[styles.factorChip, {
                    backgroundColor: factor.impact === 'positive' ? '#dcfce7' : '#fee2e2'
                  }]}>
                    <Ionicons
                      name={factor.impact === 'positive' ? 'arrow-up' : 'arrow-down'}
                      size={12}
                      color={factor.impact === 'positive' ? '#16a34a' : '#dc2626'}
                    />
                    <Text style={[styles.factorText, {
                      color: factor.impact === 'positive' ? '#166534' : '#991b1b'
                    }]}>
                      {factor.name} {typeof factor.value === 'number' ? `(${factor.value})` : factor.value}
                    </Text>
                  </View>
                ))}
              </View>
            </View>
          )}

          {/* All Chakras Summary */}
          <View style={styles.summarySection}>
            <Text style={styles.summarySectionTitle}>
              {language === 'ta' ? 'அனைத்து சக்ரங்கள்' : 'All Chakras Overview'}
            </Text>
            {Object.entries(CHAKRA_CONFIG).map(([key, chakra]) => {
              const score = chakraScores[key]?.score || 60;
              const status = chakraScores[key]?.status || 'Balanced';
              return (
                <TouchableOpacity
                  key={key}
                  style={[styles.summaryRow, selectedChakra === key && styles.summaryRowActive]}
                  onPress={() => setSelectedChakra(key)}
                >
                  <View style={[styles.summaryDot, { backgroundColor: chakra.color }]} />
                  <Text style={styles.summaryName}>
                    {language === 'ta' ? chakra.nameTa : chakra.name}
                  </Text>
                  <View style={styles.summaryProgress}>
                    <View style={[styles.summaryBar, { width: `${score}%`, backgroundColor: chakra.color }]} />
                  </View>
                  <Text style={[styles.summaryScore, { color: chakra.color }]}>{score}%</Text>
                </TouchableOpacity>
              );
            })}
          </View>

          {/* Disclaimer */}
          <View style={styles.disclaimer}>
            <Ionicons name="information-circle" size={16} color="#6b7280" />
            <Text style={styles.disclaimerText}>
              {language === 'ta'
                ? 'உங்கள் ஜாதகத்தின் கிரக நிலைகளின் அடிப்படையில் கணக்கிடப்பட்டது.'
                : 'Calculated based on planetary positions in your birth chart.'}
            </Text>
          </View>
        </ScrollView>
      </LinearGradient>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#1e1b4b' },
  gradient: { flex: 1 },
  loadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#1e1b4b' },
  loadingText: { marginTop: 16, color: '#a855f7', fontSize: 14 },

  // Header
  header: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 16, paddingVertical: 12, borderBottomWidth: 1, borderBottomColor: 'rgba(255,255,255,0.1)' },
  backButton: { padding: 8 },
  headerCenter: { flex: 1, marginLeft: 8 },
  headerTitle: { fontSize: 20, fontWeight: '700', color: '#fff' },
  headerSubtitle: { fontSize: 11, color: '#a5b4fc', marginTop: 2 },
  energyBadge: { backgroundColor: 'rgba(168,85,247,0.2)', paddingHorizontal: 12, paddingVertical: 6, borderRadius: 12, alignItems: 'center' },
  energyValue: { fontSize: 18, fontWeight: '800', color: '#a855f7' },
  energyLabel: { fontSize: 9, color: '#c4b5fd' },

  scrollContent: { paddingBottom: 40 },

  // Dasha Banner
  dashaBanner: { flexDirection: 'row', alignItems: 'center', gap: 8, backgroundColor: 'rgba(168,85,247,0.15)', marginHorizontal: 16, marginTop: 12, paddingHorizontal: 14, paddingVertical: 10, borderRadius: 10, borderWidth: 1, borderColor: 'rgba(168,85,247,0.3)' },
  dashaText: { fontSize: 13, color: '#c4b5fd', fontWeight: '500' },

  // Main Content
  mainContent: { flexDirection: 'row', paddingHorizontal: 12, paddingTop: 16, minHeight: 400 },

  // Left Panel - Body
  leftPanel: { width: 120, alignItems: 'center', justifyContent: 'flex-start' },
  bodyWrapper: { position: 'relative', width: 120, height: 380, alignItems: 'center' },
  bodySvg: { position: 'absolute', top: 0, left: 10 },

  // Chakra Points
  chakraPoint: { position: 'absolute', left: 35, width: 50, height: 40, alignItems: 'center', justifyContent: 'center', zIndex: 10 },
  chakraGlow: { position: 'absolute', width: 44, height: 44, borderRadius: 22 },
  chakraCircle: { width: 36, height: 36, borderRadius: 18, justifyContent: 'center', alignItems: 'center', shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.4, shadowRadius: 5, elevation: 6 },
  chakraCircleScore: { fontSize: 12, fontWeight: '800', color: '#fff' },

  // Right Panel - Details
  rightPanel: { flex: 1, paddingLeft: 10 },
  detailCard: { borderRadius: 16, padding: 14, shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1, shadowRadius: 4, elevation: 3 },

  // Detail Header
  detailHeader: { flexDirection: 'row', alignItems: 'center', marginBottom: 12 },
  detailSymbol: { fontSize: 32, marginRight: 10, opacity: 0.8 },
  detailTitleWrap: { flex: 1 },
  detailName: { fontSize: 18, fontWeight: '800', letterSpacing: 1 },
  detailSanskrit: { fontSize: 12, color: '#6b7280', marginTop: 2 },

  // Score Section
  scoreSection: { flexDirection: 'row', alignItems: 'center', marginBottom: 14 },
  scoreCircle: { width: 60, height: 60, borderRadius: 30, borderWidth: 3, justifyContent: 'center', alignItems: 'center', backgroundColor: '#fff' },
  scoreValue: { fontSize: 22, fontWeight: '800' },
  scorePercent: { fontSize: 10, color: '#6b7280', position: 'absolute', right: 10, top: 12 },
  statusPill: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 10, paddingVertical: 5, borderRadius: 12, marginLeft: 12 },
  statusDot: { width: 8, height: 8, borderRadius: 4, marginRight: 6 },
  statusText: { fontSize: 12, fontWeight: '700' },

  // Sections
  sectionLabel: { fontSize: 10, fontWeight: '700', color: '#6b7280', marginBottom: 6, letterSpacing: 0.5 },

  // Represents
  representsSection: { marginBottom: 12 },
  representsTags: { flexDirection: 'row', flexWrap: 'wrap', gap: 6 },
  representTag: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 10 },
  representText: { fontSize: 11, fontWeight: '600' },

  // Info Grid
  infoGrid: { flexDirection: 'row', flexWrap: 'wrap', marginBottom: 12, gap: 8 },
  infoItem: { backgroundColor: 'rgba(255,255,255,0.6)', paddingHorizontal: 10, paddingVertical: 6, borderRadius: 8 },
  infoLabel: { fontSize: 9, color: '#6b7280' },
  infoValue: { fontSize: 12, fontWeight: '600', color: '#1f2937', marginTop: 2 },

  // Planets
  planetsSection: { marginBottom: 12 },
  planetsList: { flexDirection: 'row', gap: 6 },
  planetBadge: { paddingHorizontal: 12, paddingVertical: 5, borderRadius: 10 },
  planetText: { fontSize: 11, fontWeight: '700', color: '#fff' },

  // Crystals
  crystalsSection: { marginBottom: 12 },
  crystalsList: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  crystalItem: { flexDirection: 'row', alignItems: 'center' },
  crystalDot: { fontSize: 10, marginRight: 4 },
  crystalText: { fontSize: 11, color: '#4b5563' },

  // Affirmation
  affirmationBox: { padding: 12, borderRadius: 10 },
  affirmationLabel: { fontSize: 10, fontWeight: '600', color: '#6b7280', marginBottom: 4 },
  affirmationText: { fontSize: 13, fontWeight: '600', fontStyle: 'italic', lineHeight: 18 },

  // Factors Section
  factorsSection: { marginHorizontal: 16, marginTop: 16 },
  factorsSectionTitle: { fontSize: 14, fontWeight: '700', color: '#e2e8f0', marginBottom: 10 },
  factorsList: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  factorChip: { flexDirection: 'row', alignItems: 'center', gap: 4, paddingHorizontal: 10, paddingVertical: 6, borderRadius: 10 },
  factorText: { fontSize: 11, fontWeight: '600' },

  // Summary Section
  summarySection: { marginHorizontal: 16, marginTop: 20, backgroundColor: 'rgba(255,255,255,0.06)', borderRadius: 16, padding: 14 },
  summarySectionTitle: { fontSize: 14, fontWeight: '700', color: '#e2e8f0', marginBottom: 12 },
  summaryRow: { flexDirection: 'row', alignItems: 'center', paddingVertical: 8, paddingHorizontal: 8, borderRadius: 8 },
  summaryRowActive: { backgroundColor: 'rgba(168,85,247,0.15)' },
  summaryDot: { width: 12, height: 12, borderRadius: 6, marginRight: 10 },
  summaryName: { width: 100, fontSize: 12, color: '#e2e8f0', fontWeight: '500' },
  summaryProgress: { flex: 1, height: 6, backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: 3, marginRight: 10, overflow: 'hidden' },
  summaryBar: { height: '100%', borderRadius: 3 },
  summaryScore: { fontSize: 12, fontWeight: '700', width: 45, textAlign: 'right' },

  // Disclaimer
  disclaimer: { flexDirection: 'row', alignItems: 'flex-start', gap: 8, marginHorizontal: 16, marginTop: 20, padding: 12, backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: 10 },
  disclaimerText: { flex: 1, fontSize: 11, color: '#94a3b8', lineHeight: 16 },
});
