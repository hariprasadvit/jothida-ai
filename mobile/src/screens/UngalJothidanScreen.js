import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Animated,
  PanResponder,
  Dimensions,
  TouchableOpacity,
  ActivityIndicator,
  Platform,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import Svg, {
  Circle,
  Defs,
  LinearGradient as SvgLinearGradient,
  RadialGradient,
  Stop,
  Path,
  G,
  Text as SvgText,
  Line,
} from 'react-native-svg';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { fetchUnifiedScores } from '../services/scoringService';
import { calculateDeepScores, generateFallbackScores, getRahuKalam } from '../services/astroScoringEngine';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');
const SWIPE_THRESHOLD = 120;
const SWIPE_OUT_DURATION = 250;

// Planet symbols in Tamil/English tradition
const PLANET_SYMBOLS = {
  Sun: { symbol: '☉', english: 'Sun', tamil: 'சூரியன்', kannada: 'ಸೂರ್ಯ', color: '#f59e0b' },
  Moon: { symbol: '☽', english: 'Moon', tamil: 'சந்திரன்', kannada: 'ಚಂದ್ರ', color: '#94a3b8' },
  Mars: { symbol: '♂', english: 'Mars', tamil: 'செவ்வாய்', kannada: 'ಮಂಗಳ', color: '#ef4444' },
  Mercury: { symbol: '☿', english: 'Mercury', tamil: 'புதன்', kannada: 'ಬುಧ', color: '#22c55e' },
  Jupiter: { symbol: '♃', english: 'Jupiter', tamil: 'குரு', kannada: 'ಗುರು', color: '#eab308' },
  Venus: { symbol: '♀', english: 'Venus', tamil: 'சுக்கிரன்', kannada: 'ಶುಕ್ರ', color: '#ec4899' },
  Saturn: { symbol: '♄', english: 'Saturn', tamil: 'சனி', kannada: 'ಶನಿ', color: '#6366f1' },
  Rahu: { symbol: '☊', english: 'Rahu', tamil: 'ராகு', kannada: 'ರಾಹು', color: '#8b5cf6' },
  Ketu: { symbol: '☋', english: 'Ketu', tamil: 'கேது', kannada: 'ಕೇತು', color: '#f97316' },
};

// Card configurations with spiritual themes and ruling planets
const CARD_CONFIGS = {
  dasha_mood: {
    planet: 'Moon',
    gradients: ['#1e1b4b', '#312e81', '#4338ca'],
    borderColor: '#818cf8',
    nakshatraIndex: 0,
  },
  transit_pressure: {
    planet: 'Saturn',
    gradients: ['#1c1917', '#292524', '#44403c'],
    borderColor: '#78716c',
    nakshatraIndex: 1,
  },
  finance_outlook: {
    planet: 'Jupiter',
    gradients: ['#422006', '#713f12', '#a16207'],
    borderColor: '#eab308',
    nakshatraIndex: 2,
  },
  work_career: {
    planet: 'Sun',
    gradients: ['#7c2d12', '#c2410c', '#ea580c'],
    borderColor: '#fb923c',
    nakshatraIndex: 3,
  },
  relationship_energy: {
    planet: 'Venus',
    gradients: ['#500724', '#831843', '#be185d'],
    borderColor: '#f472b6',
    nakshatraIndex: 4,
  },
  health_vibration: {
    planet: 'Mars',
    gradients: ['#14532d', '#166534', '#15803d'],
    borderColor: '#4ade80',
    nakshatraIndex: 5,
  },
  lucky_window: {
    planet: 'Jupiter',
    gradients: ['#451a03', '#78350f', '#b45309'],
    borderColor: '#fbbf24',
    nakshatraIndex: 6,
  },
  avoid_window: {
    planet: 'Rahu',
    gradients: ['#450a0a', '#7f1d1d', '#991b1b'],
    borderColor: '#f87171',
    nakshatraIndex: 7,
  },
  opportunity_indicator: {
    planet: 'Mercury',
    gradients: ['#042f2e', '#115e59', '#0f766e'],
    borderColor: '#2dd4bf',
    nakshatraIndex: 8,
  },
  risk_indicator: {
    planet: 'Ketu',
    gradients: ['#3b0764', '#581c87', '#7e22ce'],
    borderColor: '#c084fc',
    nakshatraIndex: 9,
  },
  color_direction: {
    planet: 'Sun',
    gradients: ['#172554', '#1e3a8a', '#1d4ed8'],
    borderColor: '#60a5fa',
    nakshatraIndex: 10,
  },
  personal_note: {
    planet: 'Moon',
    gradients: ['#1e1b4b', '#3730a3', '#4f46e5'],
    borderColor: '#a5b4fc',
    nakshatraIndex: 11,
  },
};

// Mandala Pattern Component - SVG geometric sacred pattern
const MandalaPattern = ({ size = 200, color = '#fff', opacity = 0.08 }) => {
  const center = size / 2;
  const layers = 4;
  const petalsPerLayer = [8, 12, 16, 24];

  return (
    <Svg width={size} height={size} style={styles.mandalaOverlay}>
      <Defs>
        <RadialGradient id="mandalaGrad" cx="50%" cy="50%" r="50%">
          <Stop offset="0%" stopColor={color} stopOpacity={opacity * 1.5} />
          <Stop offset="100%" stopColor={color} stopOpacity={0} />
        </RadialGradient>
      </Defs>

      {/* Center lotus */}
      <Circle cx={center} cy={center} r={12} fill={color} fillOpacity={opacity * 2} />
      <Circle cx={center} cy={center} r={8} fill="none" stroke={color} strokeOpacity={opacity * 3} strokeWidth={1} />

      {/* Concentric circles */}
      {[30, 50, 70, 90].map((r, i) => (
        <Circle
          key={`circle-${i}`}
          cx={center}
          cy={center}
          r={r}
          fill="none"
          stroke={color}
          strokeOpacity={opacity * (1 - i * 0.2)}
          strokeWidth={0.5}
          strokeDasharray={i % 2 === 0 ? "4,4" : "2,6"}
        />
      ))}

      {/* Petal patterns */}
      {petalsPerLayer.map((petals, layerIndex) => {
        const radius = 25 + layerIndex * 20;
        return Array.from({ length: petals }).map((_, i) => {
          const angle = (i * 360 / petals) * (Math.PI / 180);
          const x1 = center + Math.cos(angle) * (radius - 10);
          const y1 = center + Math.sin(angle) * (radius - 10);
          const x2 = center + Math.cos(angle) * (radius + 10);
          const y2 = center + Math.sin(angle) * (radius + 10);

          return (
            <Line
              key={`petal-${layerIndex}-${i}`}
              x1={x1}
              y1={y1}
              x2={x2}
              y2={y2}
              stroke={color}
              strokeOpacity={opacity * (1 - layerIndex * 0.15)}
              strokeWidth={0.5}
            />
          );
        });
      })}
    </Svg>
  );
};

// Nakshatra Constellation Component
const NakshatraConstellation = ({ index, size = 120, color = '#fff' }) => {
  // Simplified constellation patterns for each nakshatra group
  const constellationPatterns = [
    // Ashwini - horse head pattern
    [[0.3, 0.2], [0.5, 0.3], [0.7, 0.2], [0.5, 0.5], [0.3, 0.7], [0.7, 0.7]],
    // Bharani - triangle pattern
    [[0.5, 0.2], [0.2, 0.8], [0.8, 0.8], [0.5, 0.5]],
    // Krittika - flame/Pleiades pattern
    [[0.5, 0.15], [0.3, 0.35], [0.7, 0.35], [0.4, 0.55], [0.6, 0.55], [0.5, 0.75]],
    // Rohini - cart pattern
    [[0.2, 0.3], [0.8, 0.3], [0.8, 0.7], [0.2, 0.7], [0.5, 0.5]],
    // Mrigashira - deer head pattern
    [[0.5, 0.2], [0.3, 0.4], [0.7, 0.4], [0.4, 0.6], [0.6, 0.6], [0.5, 0.8]],
    // Ardra - teardrop pattern
    [[0.5, 0.2], [0.35, 0.4], [0.65, 0.4], [0.3, 0.6], [0.7, 0.6], [0.5, 0.85]],
    // Punarvasu - bow pattern
    [[0.2, 0.5], [0.4, 0.3], [0.6, 0.3], [0.8, 0.5], [0.6, 0.7], [0.4, 0.7]],
    // Pushya - flower pattern
    [[0.5, 0.2], [0.25, 0.4], [0.75, 0.4], [0.5, 0.5], [0.25, 0.7], [0.75, 0.7], [0.5, 0.85]],
    // Ashlesha - serpent pattern
    [[0.2, 0.3], [0.35, 0.45], [0.5, 0.35], [0.65, 0.5], [0.8, 0.4], [0.7, 0.7]],
    // Magha - throne pattern
    [[0.3, 0.2], [0.7, 0.2], [0.8, 0.5], [0.2, 0.5], [0.5, 0.8]],
    // Purva Phalguni - hammock pattern
    [[0.2, 0.4], [0.4, 0.3], [0.6, 0.3], [0.8, 0.4], [0.5, 0.7]],
    // Uttara Phalguni - bed pattern
    [[0.2, 0.3], [0.8, 0.3], [0.8, 0.6], [0.2, 0.6], [0.35, 0.45], [0.65, 0.45]],
  ];

  const pattern = constellationPatterns[index % 12];
  const center = size / 2;

  return (
    <Svg width={size} height={size} style={styles.constellationOverlay}>
      {/* Stars */}
      {pattern.map((point, i) => (
        <G key={`star-${i}`}>
          <Circle
            cx={point[0] * size}
            cy={point[1] * size}
            r={3}
            fill={color}
            fillOpacity={0.6 + (i * 0.05)}
          />
          {/* Star glow */}
          <Circle
            cx={point[0] * size}
            cy={point[1] * size}
            r={6}
            fill={color}
            fillOpacity={0.15}
          />
        </G>
      ))}

      {/* Connection lines */}
      {pattern.slice(0, -1).map((point, i) => (
        <Line
          key={`line-${i}`}
          x1={point[0] * size}
          y1={point[1] * size}
          x2={pattern[i + 1][0] * size}
          y2={pattern[i + 1][1] * size}
          stroke={color}
          strokeOpacity={0.2}
          strokeWidth={0.5}
          strokeDasharray="2,2"
        />
      ))}
    </Svg>
  );
};

// Planet Symbol Component
const PlanetSymbol = ({ planet, size = 60 }) => {
  const planetData = PLANET_SYMBOLS[planet] || PLANET_SYMBOLS.Sun;

  return (
    <View style={[styles.planetSymbolContainer, { width: size, height: size }]}>
      {/* Outer glow ring */}
      <View style={[styles.planetGlowOuter, {
        width: size,
        height: size,
        borderRadius: size / 2,
        borderColor: planetData.color + '40',
      }]} />

      {/* Inner ring */}
      <View style={[styles.planetGlowInner, {
        width: size * 0.85,
        height: size * 0.85,
        borderRadius: size * 0.425,
        borderColor: planetData.color + '60',
      }]} />

      {/* Symbol */}
      <Text style={[styles.planetSymbolText, {
        fontSize: size * 0.45,
        color: planetData.color,
      }]}>
        {planetData.symbol}
      </Text>
    </View>
  );
};

// Sacred Score Ring with Om symbol
const SacredScoreRing = ({ percentage, size = 140, strokeWidth = 8, color, planet }) => {
  const animatedValue = useRef(new Animated.Value(0)).current;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const planetData = PLANET_SYMBOLS[planet] || PLANET_SYMBOLS.Sun;

  useEffect(() => {
    Animated.timing(animatedValue, {
      toValue: percentage,
      duration: 1500,
      useNativeDriver: false,
    }).start();
  }, [percentage]);

  const strokeDashoffset = animatedValue.interpolate({
    inputRange: [0, 100],
    outputRange: [circumference, 0],
  });

  const AnimatedCircle = Animated.createAnimatedComponent(Circle);

  return (
    <View style={{ width: size, height: size, alignItems: 'center', justifyContent: 'center' }}>
      <Svg width={size} height={size} style={{ position: 'absolute' }}>
        <Defs>
          <SvgLinearGradient id={`scoreGrad-${planet}`} x1="0%" y1="0%" x2="100%" y2="100%">
            <Stop offset="0%" stopColor={planetData.color} stopOpacity="1" />
            <Stop offset="50%" stopColor="#fff" stopOpacity="0.8" />
            <Stop offset="100%" stopColor={planetData.color} stopOpacity="0.6" />
          </SvgLinearGradient>
        </Defs>

        {/* Background decorative ring */}
        <Circle
          cx={size / 2}
          cy={size / 2}
          r={radius + 8}
          fill="none"
          stroke="rgba(255,255,255,0.05)"
          strokeWidth={1}
        />

        {/* Track ring */}
        <Circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="rgba(255,255,255,0.1)"
          strokeWidth={strokeWidth}
          fill="none"
        />

        {/* Progress ring */}
        <AnimatedCircle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={`url(#scoreGrad-${planet})`}
          strokeWidth={strokeWidth}
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
        />

        {/* Inner decorative circle */}
        <Circle
          cx={size / 2}
          cy={size / 2}
          r={radius - 15}
          fill="none"
          stroke="rgba(255,255,255,0.08)"
          strokeWidth={0.5}
          strokeDasharray="4,8"
        />
      </Svg>

      {/* Score text */}
      <View style={styles.scoreCenter}>
        <Text style={[styles.scorePercentage, { color: planetData.color }]}>{percentage}</Text>
        <Text style={styles.scorePercent}>%</Text>
      </View>
    </View>
  );
};

// Decorative Border Component
const DecorativeBorder = ({ color }) => (
  <View style={styles.decorativeBorderContainer}>
    {/* Top border pattern */}
    <View style={[styles.borderPattern, styles.borderTop]}>
      <View style={[styles.borderDot, { backgroundColor: color }]} />
      <View style={[styles.borderLine, { backgroundColor: color }]} />
      <View style={[styles.borderDiamond, { borderColor: color }]} />
      <View style={[styles.borderLine, { backgroundColor: color }]} />
      <View style={[styles.borderDot, { backgroundColor: color }]} />
    </View>

    {/* Bottom border pattern */}
    <View style={[styles.borderPattern, styles.borderBottom]}>
      <View style={[styles.borderDot, { backgroundColor: color }]} />
      <View style={[styles.borderLine, { backgroundColor: color }]} />
      <View style={[styles.borderDiamond, { borderColor: color }]} />
      <View style={[styles.borderLine, { backgroundColor: color }]} />
      <View style={[styles.borderDot, { backgroundColor: color }]} />
    </View>
  </View>
);

// Single Swipeable Card with Hindu spiritual design
const SwipeableCard = ({ card, config, isFirst, onSwipeComplete, cardIndex, totalCards, t, language }) => {
  const position = useRef(new Animated.ValueXY()).current;
  const rotation = position.x.interpolate({
    inputRange: [-SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2],
    outputRange: ['-12deg', '0deg', '12deg'],
  });
  const scaleAnim = useRef(new Animated.Value(isFirst ? 1 : 0.95)).current;
  const planetData = PLANET_SYMBOLS[config?.planet] || PLANET_SYMBOLS.Sun;

  useEffect(() => {
    Animated.spring(scaleAnim, {
      toValue: isFirst ? 1 : 0.95,
      friction: 5,
      useNativeDriver: true,
    }).start();
  }, [isFirst]);

  const panResponder = useRef(
    PanResponder.create({
      onStartShouldSetPanResponder: () => isFirst,
      onPanResponderMove: (_, gesture) => {
        position.setValue({ x: gesture.dx, y: gesture.dy * 0.5 });
      },
      onPanResponderRelease: (_, gesture) => {
        if (gesture.dx > SWIPE_THRESHOLD) {
          swipeRight();
        } else if (gesture.dx < -SWIPE_THRESHOLD) {
          swipeLeft();
        } else {
          resetPosition();
        }
      },
    })
  ).current;

  const swipeRight = () => {
    Animated.timing(position, {
      toValue: { x: SCREEN_WIDTH + 100, y: 0 },
      duration: SWIPE_OUT_DURATION,
      useNativeDriver: true,
    }).start(() => onSwipeComplete());
  };

  const swipeLeft = () => {
    Animated.timing(position, {
      toValue: { x: -SCREEN_WIDTH - 100, y: 0 },
      duration: SWIPE_OUT_DURATION,
      useNativeDriver: true,
    }).start(() => onSwipeComplete());
  };

  const resetPosition = () => {
    Animated.spring(position, {
      toValue: { x: 0, y: 0 },
      friction: 5,
      useNativeDriver: true,
    }).start();
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return { text: t('excellent') || 'சிறப்பு', color: '#22c55e' };
    if (score >= 65) return { text: t('good') || 'நல்லது', color: '#eab308' };
    if (score >= 50) return { text: t('average') || 'சராசரி', color: '#3b82f6' };
    return { text: t('caution') || 'கவனம்', color: '#ef4444' };
  };

  const scoreInfo = getScoreLabel(card.score);
  const gradients = config?.gradients || ['#1a1a2e', '#16213e', '#0f3460'];
  const langCode = language === 'tamil' ? 'ta' : language === 'kannada' ? 'kn' : 'en';

  return (
    <Animated.View
      {...(isFirst ? panResponder.panHandlers : {})}
      style={[
        styles.card,
        {
          transform: [
            { translateX: position.x },
            { translateY: position.y },
            { rotate: isFirst ? rotation : '0deg' },
            { scale: scaleAnim },
          ],
          zIndex: isFirst ? 10 : 5,
        },
      ]}
    >
      <LinearGradient colors={gradients} style={styles.cardGradient}>
        {/* Mandala background pattern */}
        <MandalaPattern size={SCREEN_WIDTH - 40} color={config?.borderColor || '#fff'} opacity={0.06} />

        {/* Constellation pattern */}
        <View style={styles.constellationWrapper}>
          <NakshatraConstellation
            index={config?.nakshatraIndex || 0}
            size={100}
            color={config?.borderColor || '#fff'}
          />
        </View>

        {/* Decorative border */}
        <DecorativeBorder color={config?.borderColor || '#fff'} />

        {/* Card Counter with Om symbol */}
        <View style={styles.cardCounter}>
          <Text style={styles.omSymbol}>ॐ</Text>
          <Text style={styles.cardCounterText}>{cardIndex + 1} / {totalCards}</Text>
        </View>

        {/* Planet Symbol */}
        <PlanetSymbol planet={config?.planet || 'Sun'} size={70} />

        {/* Planet Name */}
        <Text style={[styles.planetName, { color: planetData.color }]}>
          {langCode === 'ta' ? planetData.tamil : langCode === 'kn' ? planetData.kannada : planetData.english}
        </Text>

        {/* Title */}
        <Text style={styles.cardTitle}>{card.title}</Text>

        {/* Sacred Score Ring */}
        <SacredScoreRing
          percentage={card.score}
          size={150}
          strokeWidth={10}
          color={scoreInfo.color}
          planet={config?.planet || 'Sun'}
        />

        {/* Score Label Badge */}
        <View style={[styles.scoreBadge, {
          backgroundColor: scoreInfo.color + '25',
          borderColor: scoreInfo.color + '40',
        }]}>
          <Text style={[styles.scoreBadgeText, { color: scoreInfo.color }]}>
            {scoreInfo.text}
          </Text>
        </View>

        {/* Description */}
        <Text style={styles.cardDescription}>{card.text}</Text>

        {/* Confidence with traditional styling */}
        <View style={styles.confidenceContainer}>
          <Text style={styles.confidenceLabel}>
            {langCode === 'ta' ? 'நம்பகத்தன்மை' : langCode === 'kn' ? 'ವಿಶ್ವಾಸಾರ್ಹತೆ' : 'Confidence'}
          </Text>
          <View style={styles.confidenceBarBg}>
            <View style={[styles.confidenceBarFill, {
              width: `${card.confidence}%`,
              backgroundColor: config?.borderColor || '#8b5cf6',
            }]} />
          </View>
          <Text style={styles.confidenceValue}>{card.confidence}%</Text>
        </View>

        {/* Swipe Hints */}
        {isFirst && (
          <View style={styles.swipeHints}>
            <View style={styles.swipeHint}>
              <Ionicons name="chevron-back" size={18} color="rgba(255,255,255,0.3)" />
            </View>
            <Text style={styles.swipeHintText}>
              {langCode === 'ta' ? 'ஸ்வைப் செய்யவும்' : 'Swipe'}
            </Text>
            <View style={styles.swipeHint}>
              <Ionicons name="chevron-forward" size={18} color="rgba(255,255,255,0.3)" />
            </View>
          </View>
        )}
      </LinearGradient>
    </Animated.View>
  );
};

// Main Screen
export default function UngalJothidanScreen() {
  const insets = useSafeAreaInsets();
  const { userProfile } = useAuth();
  const { t, language } = useLanguage();
  const [cards, setCards] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [overallConfidence, setOverallConfidence] = useState(0);
  const [summary, setSummary] = useState('');

  // Fetch insights using UNIFIED scoring service (SAME as Dashboard & AstroFeed)
  const fetchInsights = useCallback(async () => {
    try {
      setLoading(true);
      const langCode = language === 'tamil' ? 'ta' : language === 'kannada' ? 'kn' : 'en';

      if (!userProfile?.birthDate) {
        setLoading(false);
        return;
      }

      // Use unified scoring service - SAME data source as Dashboard & AstroFeed
      console.log('[UngalJothidan] Fetching unified scores...');
      const unifiedData = await fetchUnifiedScores(userProfile, language);

      let generatedCards;
      if (unifiedData) {
        console.log('[UngalJothidan] Using unified data, overall score:', unifiedData.overallScore);
        // Generate cards from unified data
        generatedCards = generateCardsFromUnifiedData(
          unifiedData,
          userProfile,
          langCode,
          t
        );
      } else {
        console.log('[UngalJothidan] Using fallback cards');
        generatedCards = generateFallbackCardsLocal(userProfile, language, t);
      }

      setCards(generatedCards);

      if (generatedCards.length > 0) {
        const avgConfidence = Math.round(
          generatedCards.reduce((sum, c) => sum + c.confidence, 0) / generatedCards.length
        );
        setOverallConfidence(avgConfidence);

        const sortedCards = [...generatedCards].sort((a, b) => b.score - a.score);
        const topCard = sortedCards[0];
        const bottomCard = sortedCards[sortedCards.length - 1];

        if (langCode === 'ta') {
          setSummary(`${topCard.title} சிறப்பாக உள்ளது; ${bottomCard.title} கவனம் தேவை.`);
        } else if (langCode === 'kn') {
          setSummary(`${topCard.title} ಉತ್ತಮವಾಗಿದೆ; ${bottomCard.title} ಗಮನ ಬೇಕು.`);
        } else {
          setSummary(`${topCard.title} is favorable; ${bottomCard.title} needs attention.`);
        }
      }

    } catch (error) {
      console.error('[UngalJothidan] Failed to fetch insights:', error);
      const fallbackCards = generateFallbackCardsLocal(userProfile, language, t);
      setCards(fallbackCards);
      setOverallConfidence(70);
    } finally {
      setLoading(false);
    }
  }, [userProfile, language, t]);

  useEffect(() => {
    fetchInsights();
  }, [fetchInsights]);

  const handleSwipeComplete = () => {
    setCurrentIndex((prev) => (prev + 1) % cards.length);
  };

  const goToCard = (index) => {
    setCurrentIndex(index);
  };

  const langCode = language === 'tamil' ? 'ta' : language === 'kannada' ? 'kn' : 'en';

  if (loading) {
    return (
      <View style={[styles.container, styles.loadingContainer]}>
        <LinearGradient colors={['#0c0a1d', '#1a1528', '#0f0a1e']} style={StyleSheet.absoluteFill} />
        <View style={styles.loadingMandala}>
          <MandalaPattern size={150} color="#8b5cf6" opacity={0.15} />
        </View>
        <Text style={styles.omLoading}>ॐ</Text>
        <ActivityIndicator size="large" color="#8b5cf6" style={{ marginTop: 20 }} />
        <Text style={styles.loadingText}>
          {langCode === 'ta' ? 'உங்கள் ஜோதிடம் ஏற்றுகிறது...' : 'Loading your insights...'}
        </Text>
      </View>
    );
  }

  if (cards.length === 0) {
    return (
      <View style={[styles.container, styles.loadingContainer]}>
        <LinearGradient colors={['#0c0a1d', '#1a1528', '#0f0a1e']} style={StyleSheet.absoluteFill} />
        <Text style={styles.omLoading}>ॐ</Text>
        <Text style={styles.errorText}>
          {langCode === 'ta' ? 'உங்கள் சுயவிவரத்தை நிரப்பவும்' : 'Complete your profile to see insights'}
        </Text>
      </View>
    );
  }

  const visibleCards = [];
  for (let i = 0; i < Math.min(2, cards.length); i++) {
    const cardIndex = (currentIndex + i) % cards.length;
    visibleCards.push({ ...cards[cardIndex], renderIndex: i, actualIndex: cardIndex });
  }

  return (
    <View style={[styles.container, { paddingTop: insets.top }]}>
      <LinearGradient colors={['#0c0a1d', '#1a1528', '#0f0a1e']} style={StyleSheet.absoluteFill} />

      {/* Header with spiritual styling */}
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <View style={styles.headerTitleRow}>
            <Text style={styles.headerOm}>ॐ</Text>
            <Text style={styles.headerTitle}>{t('ungalJothidan') || 'உங்கள் ஜோதிடர்'}</Text>
          </View>
          <Text style={styles.headerSubtitle}>
            {langCode === 'ta' ? 'இன்றைய ஜோதிட பலன்கள்' : 'Daily Astrological Insights'}
          </Text>
        </View>
        <View style={styles.confidenceBadge}>
          <Text style={styles.confidenceBadgeLabel}>
            {langCode === 'ta' ? 'துல்லியம்' : 'Accuracy'}
          </Text>
          <Text style={styles.confidenceBadgeText}>{overallConfidence}%</Text>
        </View>
      </View>

      {/* Summary */}
      {summary && (
        <View style={styles.summaryContainer}>
          <View style={styles.summaryDeco}>
            <View style={styles.summaryLine} />
            <Text style={styles.summaryIcon}>✦</Text>
            <View style={styles.summaryLine} />
          </View>
          <Text style={styles.summaryText}>{summary}</Text>
        </View>
      )}

      {/* Card Stack */}
      <View style={styles.cardContainer}>
        {visibleCards.reverse().map((card) => (
          <SwipeableCard
            key={`${card.id}-${card.actualIndex}`}
            card={card}
            config={CARD_CONFIGS[card.id]}
            isFirst={card.renderIndex === 0}
            onSwipeComplete={handleSwipeComplete}
            cardIndex={card.actualIndex}
            totalCards={cards.length}
            t={t}
            language={language}
          />
        ))}
      </View>

      {/* Card Navigation Dots */}
      <View style={styles.dotsContainer}>
        {cards.map((_, index) => (
          <TouchableOpacity
            key={index}
            onPress={() => goToCard(index)}
            style={[
              styles.dot,
              currentIndex === index && styles.dotActive,
            ]}
          />
        ))}
      </View>

      {/* Bottom Spacer */}
      <View style={{ height: Platform.OS === 'web' ? 60 : 80 + insets.bottom }} />
    </View>
  );
}

// ============================================================================
// CARD GENERATION - Uses Deep Astrology Scoring Engine
// ============================================================================

function generateCardsFromUnifiedData(unifiedData, userProfile, langCode, t) {
  const cards = [];

  // Use deep astrology scoring engine for sophisticated calculations
  const { scores, metadata } = calculateDeepScores(userProfile, unifiedData);
  const confidence = metadata.confidence;

  // 1. Dasha Mood
  const dashaLord = metadata.dashaLord;
  cards.push({
    id: 'dasha_mood',
    title: langCode === 'ta' ? 'தசா மனநிலை' : langCode === 'kn' ? 'ದಶಾ ಮನಸ್ಥಿತಿ' : 'Dasha Mood',
    score: scores.dasha_mood,
    confidence: Math.min(95, confidence + 5),
    text: getDashaMoodText(dashaLord, scores.dasha_mood, langCode),
  });

  // 2. Transit Pressure
  cards.push({
    id: 'transit_pressure',
    title: langCode === 'ta' ? 'கிரக அழுத்தம்' : langCode === 'kn' ? 'ಗ್ರಹ ಒತ್ತಡ' : 'Transit Pressure',
    score: scores.transit_pressure,
    confidence: confidence,
    text: getTransitPressureText(scores.transit_pressure, langCode),
  });

  // 3. Finance Outlook
  cards.push({
    id: 'finance_outlook',
    title: langCode === 'ta' ? 'நிதி நிலை' : langCode === 'kn' ? 'ಹಣಕಾಸು ದೃಷ್ಟಿಕೋನ' : 'Finance Outlook',
    score: scores.finance_outlook,
    confidence: confidence,
    text: getFinanceText(scores.finance_outlook, langCode),
  });

  // 4. Work/Career
  cards.push({
    id: 'work_career',
    title: langCode === 'ta' ? 'தொழில் கவனம்' : langCode === 'kn' ? 'ಕೆಲಸ / ವೃತ್ತಿ' : 'Work / Career',
    score: scores.work_career,
    confidence: confidence,
    text: getCareerText(scores.work_career, langCode),
  });

  // 5. Relationship Energy
  cards.push({
    id: 'relationship_energy',
    title: langCode === 'ta' ? 'உறவு சக்தி' : langCode === 'kn' ? 'ಸಂಬಂಧ ಶಕ್ತಿ' : 'Relationship Energy',
    score: scores.relationship_energy,
    confidence: confidence,
    text: getRelationshipText(scores.relationship_energy, langCode),
  });

  // 6. Health Vibration
  cards.push({
    id: 'health_vibration',
    title: langCode === 'ta' ? 'உடல்நலம்' : langCode === 'kn' ? 'ಆರೋಗ್ಯ ಕಂಪನ' : 'Health Vibration',
    score: scores.health_vibration,
    confidence: Math.min(90, confidence),
    text: getHealthText(scores.health_vibration, langCode),
  });

  // 7. Lucky Window - with hora-based timing
  const luckyWindow = metadata.luckyWindow;
  cards.push({
    id: 'lucky_window',
    title: langCode === 'ta' ? 'அதிர்ஷ்ட நேரம்' : langCode === 'kn' ? 'ಅದೃಷ್ಟದ ಸಮಯ' : 'Lucky Window',
    score: scores.lucky_window,
    confidence: 85,
    text: langCode === 'ta'
      ? `அதிர்ஷ்ட நேரம்: ${luckyWindow.start} - ${luckyWindow.end} (${getPlanetNameLocal(luckyWindow.planet, 'ta')} ஹோரை)`
      : langCode === 'kn'
      ? `ಅದೃಷ್ಟದ ಸಮಯ: ${luckyWindow.start} - ${luckyWindow.end} (${getPlanetNameLocal(luckyWindow.planet, 'kn')} ಹೋರಾ)`
      : `Lucky window: ${luckyWindow.start} - ${luckyWindow.end} (${luckyWindow.planet} Hora)`,
  });

  // 8. Avoid Window - Rahu Kalam and Yama Kandam
  const avoidWindow = metadata.avoidWindow;
  cards.push({
    id: 'avoid_window',
    title: langCode === 'ta' ? 'தவிர்க்க வேண்டிய நேரம்' : langCode === 'kn' ? 'ತಪ್ಪಿಸಬೇಕಾದ ಸಮಯ' : 'Avoid Window',
    score: scores.avoid_window,
    confidence: 92,
    text: langCode === 'ta'
      ? `ராகு காலம்: ${avoidWindow.rahuKalam.start} - ${avoidWindow.rahuKalam.end}\nயம கண்டம்: ${avoidWindow.yamaKandam.start} - ${avoidWindow.yamaKandam.end}`
      : langCode === 'kn'
      ? `ರಾಹು ಕಾಲ: ${avoidWindow.rahuKalam.start} - ${avoidWindow.rahuKalam.end}\nಯಮ ಗಂಡ: ${avoidWindow.yamaKandam.start} - ${avoidWindow.yamaKandam.end}`
      : `Rahu Kalam: ${avoidWindow.rahuKalam.start} - ${avoidWindow.rahuKalam.end}\nYama Kandam: ${avoidWindow.yamaKandam.start} - ${avoidWindow.yamaKandam.end}`,
  });

  // 9. Opportunity Indicator
  const opportunity = metadata.opportunity;
  cards.push({
    id: 'opportunity_indicator',
    title: langCode === 'ta' ? 'வாய்ப்பு குறிகாட்டி' : langCode === 'kn' ? 'ಅವಕಾಶ' : 'Opportunity',
    score: scores.opportunity_indicator,
    confidence: confidence,
    text: getOpportunityText(scores.opportunity_indicator, opportunity.area, langCode),
  });

  // 10. Risk Alert
  const risk = metadata.risk;
  cards.push({
    id: 'risk_indicator',
    title: langCode === 'ta' ? 'அபாய குறிகாட்டி' : langCode === 'kn' ? 'ಅಪಾಯ ಎಚ್ಚರಿಕೆ' : 'Risk Alert',
    score: scores.risk_indicator,
    confidence: confidence,
    text: getRiskText(risk.intensity, risk.area, langCode),
  });

  // 11. Color/Direction - using deep engine calculations
  const colorSuggestion = metadata.colorSuggestion;
  const directionSuggestion = metadata.directionSuggestion;
  cards.push({
    id: 'color_direction',
    title: langCode === 'ta' ? 'நிறம் / திசை' : langCode === 'kn' ? 'ಬಣ್ಣ / ದಿಕ್ಕು' : 'Color / Direction',
    score: scores.color_direction,
    confidence: 88,
    text: getColorDirectionText(colorSuggestion, directionSuggestion, langCode),
  });

  // 12. Personal Note
  const personalNote = metadata.personalNote;
  cards.push({
    id: 'personal_note',
    title: langCode === 'ta' ? 'தனிப்பட்ட குறிப்பு' : langCode === 'kn' ? 'ವೈಯಕ್ತಿಕ ಟಿಪ್ಪಣಿ' : 'Personal Note',
    score: scores.personal_note,
    confidence: confidence,
    text: getPersonalNoteTextDeep(personalNote, langCode),
  });

  return cards;
}

// Helper to get planet name in local language
function getPlanetNameLocal(planet, langCode) {
  const names = {
    Sun: { ta: 'சூரியன்', kn: 'ಸೂರ್ಯ', en: 'Sun' },
    Moon: { ta: 'சந்திரன்', kn: 'ಚಂದ್ರ', en: 'Moon' },
    Mars: { ta: 'செவ்வாய்', kn: 'ಮಂಗಳ', en: 'Mars' },
    Mercury: { ta: 'புதன்', kn: 'ಬುಧ', en: 'Mercury' },
    Jupiter: { ta: 'குரு', kn: 'ಗುರು', en: 'Jupiter' },
    Venus: { ta: 'சுக்கிரன்', kn: 'ಶುಕ್ರ', en: 'Venus' },
    Saturn: { ta: 'சனி', kn: 'ಶನಿ', en: 'Saturn' },
  };
  return names[planet]?.[langCode] || planet;
}

// Helper to get color/direction text
function getColorDirectionText(colorSuggestion, directionSuggestion, langCode) {
  const colorTranslations = {
    Orange: { ta: 'ஆரஞ்சு', kn: 'ಕಿತ್ತಳೆ' },
    Red: { ta: 'சிவப்பு', kn: 'ಕೆಂಪು' },
    Gold: { ta: 'தங்கம்', kn: 'ಚಿನ್ನ' },
    White: { ta: 'வெள்ளை', kn: 'ಬಿಳಿ' },
    Silver: { ta: 'வெள்ளி', kn: 'ಬೆಳ್ಳಿ' },
    Green: { ta: 'பச்சை', kn: 'ಹಸಿರು' },
    Yellow: { ta: 'மஞ்சள்', kn: 'ಹಳದಿ' },
    Blue: { ta: 'நீலம்', kn: 'ನೀಲಿ' },
    Pink: { ta: 'இளஞ்சிவப்பு', kn: 'ಗುಲಾಬಿ' },
  };

  const directionTranslations = {
    East: { ta: 'கிழக்கு', kn: 'ಪೂರ್ವ' },
    West: { ta: 'மேற்கு', kn: 'ಪಶ್ಚಿಮ' },
    North: { ta: 'வடக்கு', kn: 'ಉತ್ತರ' },
    South: { ta: 'தெற்கு', kn: 'ದಕ್ಷಿಣ' },
    Northeast: { ta: 'வடகிழக்கு', kn: 'ಈಶಾನ್ಯ' },
    Northwest: { ta: 'வடமேற்கு', kn: 'ವಾಯುವ್ಯ' },
    Southeast: { ta: 'தென்கிழக்கு', kn: 'ಆಗ್ನೇಯ' },
    Southwest: { ta: 'தென்மேற்கு', kn: 'ನೈರುತ್ಯ' },
  };

  const color = colorSuggestion.primary;
  const direction = directionSuggestion.primary;

  const colorName = langCode === 'ta' ? (colorTranslations[color]?.ta || color) :
                    langCode === 'kn' ? (colorTranslations[color]?.kn || color) : color;
  const dirName = langCode === 'ta' ? (directionTranslations[direction]?.ta || direction) :
                  langCode === 'kn' ? (directionTranslations[direction]?.kn || direction) : direction;

  if (langCode === 'ta') return `நிறம்: ${colorName} | திசை: ${dirName}`;
  if (langCode === 'kn') return `ಬಣ್ಣ: ${colorName} | ದಿಕ್ಕು: ${dirName}`;
  return `Color: ${colorName} | Direction: ${dirName}`;
}

// Helper to get personal note text with deep engine data
function getPersonalNoteTextDeep(personalNote, langCode) {
  const { score, strengths, weakness, emotionalTone, dashaInfluence } = personalNote;

  const areaNames = {
    finance: { ta: 'நிதி', kn: 'ಹಣಕಾಸು', en: 'Finance' },
    career: { ta: 'தொழில்', kn: 'ವೃತ್ತಿ', en: 'Career' },
    relationship: { ta: 'உறவுகள்', kn: 'ಸಂಬಂಧಗಳು', en: 'Relationships' },
    health: { ta: 'உடல்நலம்', kn: 'ಆರೋಗ್ಯ', en: 'Health' },
  };

  const toneText = {
    positive: { ta: 'நேர்மறை', kn: 'ಧನಾತ್ಮಕ', en: 'positive' },
    neutral: { ta: 'நடுநிலை', kn: 'ತಟಸ್ಥ', en: 'neutral' },
    introspective: { ta: 'சிந்தனை', kn: 'ಆತ್ಮಾವಲೋಕನ', en: 'introspective' },
  };

  const strength1 = areaNames[strengths[0]]?.[langCode === 'ta' ? 'ta' : langCode === 'kn' ? 'kn' : 'en'] || strengths[0];
  const strength2 = areaNames[strengths[1]]?.[langCode === 'ta' ? 'ta' : langCode === 'kn' ? 'kn' : 'en'] || strengths[1];
  const tone = toneText[emotionalTone]?.[langCode === 'ta' ? 'ta' : langCode === 'kn' ? 'kn' : 'en'] || emotionalTone;

  if (score >= 75) {
    if (langCode === 'ta') {
      return `சிறந்த நாள்! ${strength1}, ${strength2} துறைகளில் வலிமை. உணர்வு: ${tone}. தைரியமாக செயல்படுங்கள்.`;
    }
    if (langCode === 'kn') {
      return `ಅದ್ಭುತ ದಿನ! ${strength1}, ${strength2} ಕ್ಷೇತ್ರಗಳಲ್ಲಿ ಬಲ. ಭಾವನೆ: ${tone}. ಧೈರ್ಯದಿಂದ ಮುಂದುವರಿಯಿರಿ.`;
    }
    return `Excellent day! Strength in ${strength1}, ${strength2}. Mood: ${tone}. Proceed with confidence.`;
  }

  if (score >= 60) {
    if (langCode === 'ta') {
      return `நல்ல நாள். ${strength1} சிறப்பாக உள்ளது. உணர்வு: ${tone}. வழக்கமான பணிகளில் கவனம் செலுத்துங்கள்.`;
    }
    if (langCode === 'kn') {
      return `ಒಳ್ಳೆಯ ದಿನ. ${strength1} ಉತ್ತಮವಾಗಿದೆ. ಭಾವನೆ: ${tone}. ದಿನಚರಿ ಕಾರ್ಯಗಳ ಮೇಲೆ ಗಮನ ಹರಿಸಿ.`;
    }
    return `Good day. ${strength1} is favorable. Mood: ${tone}. Focus on routine tasks.`;
  }

  if (langCode === 'ta') {
    return `ஓய்வு எடுங்கள். உணர்வு: ${tone}. முக்கிய முடிவுகளை தள்ளிவையுங்கள்.`;
  }
  if (langCode === 'kn') {
    return `ವಿಶ್ರಾಂತಿ ತೆಗೆದುಕೊಳ್ಳಿ. ಭಾವನೆ: ${tone}. ಪ್ರಮುಖ ನಿರ್ಧಾರಗಳನ್ನು ಮುಂದೂಡಿ.`;
  }
  return `Take rest. Mood: ${tone}. Postpone major decisions.`;
}

// Fallback: Uses deep astrology engine's deterministic fallback logic
function generateFallbackCardsLocal(userProfile, language, t) {
  const langCode = language === 'tamil' ? 'ta' : language === 'kannada' ? 'kn' : 'en';
  const dayOfWeek = new Date().getDay();

  // Use the engine's fallback scores
  const fallbackScores = generateFallbackScores(userProfile);
  const rahuKalam = getRahuKalam(dayOfWeek);

  // Generate cards with fallback scores
  const cards = [
    {
      id: 'dasha_mood',
      title: getCardTitle('dasha_mood', langCode),
      score: fallbackScores.dasha_mood,
      confidence: 65,
      text: getDashaMoodText('Venus', fallbackScores.dasha_mood, langCode),
    },
    {
      id: 'transit_pressure',
      title: getCardTitle('transit_pressure', langCode),
      score: fallbackScores.transit_pressure,
      confidence: 65,
      text: getTransitPressureText(fallbackScores.transit_pressure, langCode),
    },
    {
      id: 'finance_outlook',
      title: getCardTitle('finance_outlook', langCode),
      score: fallbackScores.finance_outlook,
      confidence: 65,
      text: getFinanceText(fallbackScores.finance_outlook, langCode),
    },
    {
      id: 'work_career',
      title: getCardTitle('work_career', langCode),
      score: fallbackScores.work_career,
      confidence: 65,
      text: getCareerText(fallbackScores.work_career, langCode),
    },
    {
      id: 'relationship_energy',
      title: getCardTitle('relationship_energy', langCode),
      score: fallbackScores.relationship_energy,
      confidence: 65,
      text: getRelationshipText(fallbackScores.relationship_energy, langCode),
    },
    {
      id: 'health_vibration',
      title: getCardTitle('health_vibration', langCode),
      score: fallbackScores.health_vibration,
      confidence: 65,
      text: getHealthText(fallbackScores.health_vibration, langCode),
    },
    {
      id: 'lucky_window',
      title: getCardTitle('lucky_window', langCode),
      score: fallbackScores.lucky_window,
      confidence: 70,
      text: langCode === 'ta'
        ? `அதிர்ஷ்ட நேரம்: ${8 + (dayOfWeek % 4)}:00 - ${10 + (dayOfWeek % 4)}:00`
        : langCode === 'kn'
        ? `ಅದೃಷ್ಟದ ಸಮಯ: ${8 + (dayOfWeek % 4)}:00 - ${10 + (dayOfWeek % 4)}:00`
        : `Lucky window: ${8 + (dayOfWeek % 4)}:00 - ${10 + (dayOfWeek % 4)}:00`,
    },
    {
      id: 'avoid_window',
      title: getCardTitle('avoid_window', langCode),
      score: fallbackScores.avoid_window,
      confidence: 90,
      text: langCode === 'ta'
        ? `ராகு காலம்: ${rahuKalam.start} - ${rahuKalam.end}`
        : langCode === 'kn'
        ? `ರಾಹು ಕಾಲ: ${rahuKalam.start} - ${rahuKalam.end}`
        : `Rahu Kalam: ${rahuKalam.start} - ${rahuKalam.end}`,
    },
    {
      id: 'opportunity_indicator',
      title: getCardTitle('opportunity_indicator', langCode),
      score: fallbackScores.opportunity_indicator,
      confidence: 65,
      text: getOpportunityText(fallbackScores.opportunity_indicator, 'career', langCode),
    },
    {
      id: 'risk_indicator',
      title: getCardTitle('risk_indicator', langCode),
      score: fallbackScores.risk_indicator,
      confidence: 65,
      text: getRiskText(100 - fallbackScores.risk_indicator, 'health', langCode),
    },
    {
      id: 'color_direction',
      title: getCardTitle('color_direction', langCode),
      score: fallbackScores.color_direction,
      confidence: 85,
      text: getColorDirection(userProfile?.nakshatra, dayOfWeek, langCode),
    },
    {
      id: 'personal_note',
      title: getCardTitle('personal_note', langCode),
      score: fallbackScores.personal_note,
      confidence: 65,
      text: getPersonalNoteText(fallbackScores.personal_note, langCode),
    },
  ];

  return cards;
}

// Helper functions
function getCardTitle(id, langCode) {
  const titles = {
    dasha_mood: { ta: 'தசா மனநிலை', kn: 'ದಶಾ ಮನಸ್ಥಿತಿ', en: 'Dasha Mood' },
    transit_pressure: { ta: 'கிரக அழுத்தம்', kn: 'ಗ್ರಹ ಒತ್ತಡ', en: 'Transit Pressure' },
    finance_outlook: { ta: 'நிதி நிலை', kn: 'ಹಣಕಾಸು ದೃಷ್ಟಿಕೋನ', en: 'Finance Outlook' },
    work_career: { ta: 'தொழில் கவனம்', kn: 'ಕೆಲಸ / ವೃತ್ತಿ', en: 'Work / Career' },
    relationship_energy: { ta: 'உறவு சக்தி', kn: 'ಸಂಬಂಧ ಶಕ್ತಿ', en: 'Relationship Energy' },
    health_vibration: { ta: 'உடல்நலம்', kn: 'ಆರೋಗ್ಯ ಕಂಪನ', en: 'Health Vibration' },
    lucky_window: { ta: 'அதிர்ஷ்ட நேரம்', kn: 'ಅದೃಷ್ಟದ ಸಮಯ', en: 'Lucky Window' },
    avoid_window: { ta: 'தவிர்க்க வேண்டிய நேரம்', kn: 'ತಪ್ಪಿಸಬೇಕಾದ ಸಮಯ', en: 'Avoid Window' },
    opportunity_indicator: { ta: 'வாய்ப்பு குறிகாட்டி', kn: 'ಅವಕಾಶ', en: 'Opportunity' },
    risk_indicator: { ta: 'அபாய குறிகாட்டி', kn: 'ಅಪಾಯ ಎಚ್ಚರಿಕೆ', en: 'Risk Alert' },
    color_direction: { ta: 'நிறம் / திசை', kn: 'ಬಣ್ಣ / ದಿಕ್ಕು', en: 'Color / Direction' },
    personal_note: { ta: 'தனிப்பட்ட குறிப்பு', kn: 'ವೈಯಕ್ತಿಕ ಟಿಪ್ಪಣಿ', en: 'Personal Note' },
  };
  return titles[id]?.[langCode] || titles[id]?.en || id;
}

function getDashaFromNakshatra(nakshatra) {
  const nakshatraLords = {
    'அஸ்வினி': 'Ketu', 'பரணி': 'Venus', 'கார்த்திகை': 'Sun',
    'ரோகிணி': 'Moon', 'மிருகசீரிடம்': 'Mars', 'திருவாதிரை': 'Rahu',
    'புனர்பூசம்': 'Jupiter', 'பூசம்': 'Saturn', 'ஆயில்யம்': 'Mercury',
  };
  return nakshatraLords[nakshatra] || 'Venus';
}

function calculateDashaScore(dashaLord, dayOfWeek) {
  // Each planet has base strength; bonus if day matches planet's day
  const lordStrengths = {
    Sun: 75, Moon: 70, Mars: 65, Mercury: 80,
    Jupiter: 85, Venus: 82, Saturn: 55, Rahu: 50, Ketu: 48,
  };
  const dayLords = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'];
  const base = lordStrengths[dashaLord] || 70;
  const bonus = dayLords[dayOfWeek] === dashaLord ? 10 : 0;
  return Math.min(95, base + bonus);
}

function calculateLuckyTime(nakshatra, dayOfWeek) {
  const baseHour = 8 + (dayOfWeek % 4);
  return {
    start: `${String(baseHour).padStart(2, '0')}:00`,
    end: `${String(baseHour + 2).padStart(2, '0')}:00`,
  };
}

// NOTE: getRahuKalam is imported from astroScoringEngine

function getColorDirection(nakshatra, dayOfWeek, langCode) {
  // Traditional Vedic colors and directions for each day
  const colors = {
    ta: ['ஆரஞ்சு', 'வெள்ளை', 'சிவப்பு', 'பச்சை', 'மஞ்சள்', 'வெள்ளை', 'நீலம்'],
    kn: ['ಕಿತ್ತಳೆ', 'ಬಿಳಿ', 'ಕೆಂಪು', 'ಹಸಿರು', 'ಹಳದಿ', 'ಬಿಳಿ', 'ನೀಲಿ'],
    en: ['Orange', 'White', 'Red', 'Green', 'Yellow', 'White', 'Blue'],
  };
  const directions = {
    ta: ['கிழக்கு', 'வடமேற்கு', 'தெற்கு', 'வடக்கு', 'வடகிழக்கு', 'தென்கிழக்கு', 'மேற்கு'],
    kn: ['ಪೂರ್ವ', 'ವಾಯುವ್ಯ', 'ದಕ್ಷಿಣ', 'ಉತ್ತರ', 'ಈಶಾನ್ಯ', 'ಆಗ್ನೇಯ', 'ಪಶ್ಚಿಮ'],
    en: ['East', 'Northwest', 'South', 'North', 'Northeast', 'Southeast', 'West'],
  };
  const color = colors[langCode]?.[dayOfWeek] || colors.en[dayOfWeek];
  const direction = directions[langCode]?.[dayOfWeek] || directions.en[dayOfWeek];

  if (langCode === 'ta') return `நிறம்: ${color} | திசை: ${direction}`;
  if (langCode === 'kn') return `ಬಣ್ಣ: ${color} | ದಿಕ್ಕು: ${direction}`;
  return `Color: ${color} | Direction: ${direction}`;
}

// Text generation helpers
function getDashaMoodText(lord, score, langCode) {
  if (score >= 75) {
    return langCode === 'ta' ? `${lord} தசை சாதகமாக உள்ளது; நல்ல முடிவுகள் எடுக்கலாம்.`
      : langCode === 'kn' ? `${lord} ದಶೆ ಅನುಕೂಲಕರ; ಒಳ್ಳೆಯ ನಿರ್ಧಾರಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳಬಹುದು.`
      : `${lord} dasha is favorable; good for making decisions.`;
  }
  return langCode === 'ta' ? `${lord} தசை: பொறுமையாக இருங்கள்.`
    : langCode === 'kn' ? `${lord} ದಶೆ: ತಾಳ್ಮೆಯಿಂದಿರಿ.`
    : `${lord} dasha: Be patient.`;
}

function getTransitPressureText(score, langCode) {
  if (score >= 70) {
    return langCode === 'ta' ? 'கிரக அழுத்தம் குறைவு — சுமுகமான நாள்.'
      : langCode === 'kn' ? 'ಗ್ರಹ ಒತ್ತಡ ಕಡಿಮೆ — ಸುಗಮ ದಿನ.'
      : 'Low planetary pressure — smooth day.';
  }
  return langCode === 'ta' ? 'கிரக அழுத்தம் அதிகம் — கவனமாக செயல்படுங்கள்.'
    : langCode === 'kn' ? 'ಹೆಚ್ಚಿನ ಗ್ರಹ ಒತ್ತಡ — ಜಾಗರೂಕರಾಗಿರಿ.'
    : 'High planetary pressure — proceed with caution.';
}

function getFinanceText(score, langCode) {
  if (score >= 75) {
    return langCode === 'ta' ? 'நிதி நிலை சிறப்பு — முதலீடுகளுக்கு நல்ல நாள்.'
      : langCode === 'kn' ? 'ಆರ್ಥಿಕ ಪರಿಸ್ಥಿತಿ ಉತ್ತಮ — ಹೂಡಿಕೆಗೆ ಒಳ್ಳೆಯ ದಿನ.'
      : 'Excellent finance day — good for investments.';
  }
  return langCode === 'ta' ? 'நிதி விஷயங்களில் கவனம் தேவை.'
    : langCode === 'kn' ? 'ಆರ್ಥಿಕ ವಿಷಯಗಳಲ್ಲಿ ಗಮನ ಬೇಕು.'
    : 'Be cautious with financial matters.';
}

function getCareerText(score, langCode) {
  if (score >= 75) {
    return langCode === 'ta' ? 'தொழில் வளர்ச்சிக்கு சிறந்த நாள் — முன்னெடுங்கள்.'
      : langCode === 'kn' ? 'ವೃತ್ತಿ ಬೆಳವಣಿಗೆಗೆ ಅತ್ಯುತ್ತಮ ದಿನ — ಮುಂದುವರಿಯಿರಿ.'
      : 'Excellent day for career growth — take initiative.';
  }
  return langCode === 'ta' ? 'வழக்கமான பணிகளை முடிக்க நல்லது.'
    : langCode === 'kn' ? 'ದಿನಚರಿ ಕಾರ್ಯಗಳನ್ನು ಮುಗಿಸಲು ಒಳ್ಳೆಯದು.'
    : 'Good for completing routine tasks.';
}

function getRelationshipText(score, langCode) {
  if (score >= 70) {
    return langCode === 'ta' ? 'உறவுகளுக்கு நல்ல நாள் — அன்பை பகிரவும்.'
      : langCode === 'kn' ? 'ಸಂಬಂಧಗಳಿಗೆ ಒಳ್ಳೆಯ ದಿನ — ಪ್ರೀತಿಯನ್ನು ಹಂಚಿಕೊಳ್ಳಿ.'
      : 'Good day for relationships — share love.';
  }
  return langCode === 'ta' ? 'பொறுமை அவசியம் — வாதங்களை தவிர்க்கவும்.'
    : langCode === 'kn' ? 'ತಾಳ್ಮೆ ಅಗತ್ಯ — ವಾದಗಳನ್ನು ತಪ್ಪಿಸಿ.'
    : 'Patience needed — avoid arguments.';
}

function getHealthText(score, langCode) {
  if (score >= 70) {
    return langCode === 'ta' ? 'ஆரோக்கிய சக்தி நல்லது — உடற்பயிற்சி செய்யவும்.'
      : langCode === 'kn' ? 'ಆರೋಗ್ಯ ಶಕ್ತಿ ಒಳ್ಳೆಯದು — ವ್ಯಾಯಾಮ ಶಿಫಾರಸು.'
      : 'Good health energy — exercise recommended.';
  }
  return langCode === 'ta' ? 'ஓய்வு எடுங்கள் — அதிக உழைப்பு வேண்டாம்.'
    : langCode === 'kn' ? 'ವಿಶ್ರಾಂತಿ ತೆಗೆದುಕೊಳ್ಳಿ — ಅತಿಯಾದ ಶ್ರಮ ತಪ್ಪಿಸಿ.'
    : 'Take rest — avoid overexertion.';
}

function getOpportunityText(score, area, langCode) {
  const areaNames = {
    love: { ta: 'காதல்', kn: 'ಪ್ರೀತಿ', en: 'Love' },
    career: { ta: 'தொழில்', kn: 'ವೃತ್ತಿ', en: 'Career' },
    education: { ta: 'கல்வி', kn: 'ಶಿಕ್ಷಣ', en: 'Education' },
    family: { ta: 'குடும்பம்', kn: 'ಕುಟುಂಬ', en: 'Family' },
  };
  const areaName = areaNames[area]?.[langCode] || area;

  if (score >= 75) {
    return langCode === 'ta' ? `${areaName} துறையில் வலுவான வாய்ப்புகள்.`
      : langCode === 'kn' ? `${areaName} ಕ್ಷೇತ್ರದಲ್ಲಿ ಬಲವಾದ ಅವಕಾಶಗಳು.`
      : `Strong opportunities in ${areaName}.`;
  }
  return langCode === 'ta' ? 'மிதமான வாய்ப்புகள் — திட்டமிட்டு செயல்படுங்கள்.'
    : langCode === 'kn' ? 'ಮಧ್ಯಮ ಅವಕಾಶಗಳು — ಯೋಜನೆಯೊಂದಿಗೆ ಮುಂದುವರಿಯಿರಿ.'
    : 'Moderate opportunities — proceed with planning.';
}

function getRiskText(riskScore, area, langCode) {
  if (riskScore <= 30) {
    return langCode === 'ta' ? 'குறைவான அபாயம் — நிம்மதியாக இருங்கள்.'
      : langCode === 'kn' ? 'ಕಡಿಮೆ ಅಪಾಯ — ನಿಶ್ಚಿಂತೆಯಾಗಿರಿ.'
      : 'Low risk — stay relaxed.';
  }
  return langCode === 'ta' ? 'கவனம் தேவை — முக்கிய முடிவுகளை தவிர்க்கவும்.'
    : langCode === 'kn' ? 'ಗಮನ ಬೇಕು — ಪ್ರಮುಖ ನಿರ್ಧಾರಗಳನ್ನು ತಪ್ಪಿಸಿ.'
    : 'Attention needed — avoid major decisions.';
}

function getPersonalNoteText(avgScore, langCode) {
  if (avgScore >= 75) {
    return langCode === 'ta' ? 'சிறந்த நாள்! உங்கள் திட்டங்களை தைரியமாக செயல்படுத்துங்கள்.'
      : langCode === 'kn' ? 'ಅದ್ಭುತ ದಿನ! ನಿಮ್ಮ ಯೋಜನೆಗಳನ್ನು ಧೈರ್ಯದಿಂದ ಕಾರ್ಯಗತಗೊಳಿಸಿ.'
      : 'Great day! Execute your plans with confidence.';
  }
  if (avgScore >= 60) {
    return langCode === 'ta' ? 'நல்ல நாள். வழக்கமான பணிகளை முடிப்பதில் கவனம் செலுத்துங்கள்.'
      : langCode === 'kn' ? 'ಒಳ್ಳೆಯ ದಿನ. ದಿನಚರಿ ಕಾರ್ಯಗಳ ಮೇಲೆ ಕೇಂದ್ರೀಕರಿಸಿ.'
      : 'Good day. Focus on completing routine tasks.';
  }
  return langCode === 'ta' ? 'ஓய்வு எடுங்கள். முக்கிய முடிவுகளை நாளைக்கு தள்ளிவையுங்கள்.'
    : langCode === 'kn' ? 'ವಿಶ್ರಾಂತಿ ತೆಗೆದುಕೊಳ್ಳಿ. ಪ್ರಮುಖ ನಿರ್ಧಾರಗಳನ್ನು ನಾಳೆಗೆ ಮುಂದೂಡಿ.'
    : 'Take rest. Postpone major decisions to tomorrow.';
}

function getGenericCardText(id, score, langCode) {
  const level = score >= 75 ? 'high' : score >= 55 ? 'medium' : 'low';
  const texts = {
    high: {
      ta: 'சிறப்பான நிலை — முன்னேறுங்கள்.',
      kn: 'ಅತ್ಯುತ್ತಮ ಸ್ಥಿತಿ — ಮುಂದುವರಿಯಿರಿ.',
      en: 'Excellent condition — proceed ahead.',
    },
    medium: {
      ta: 'சராசரி நிலை — கவனமாக இருங்கள்.',
      kn: 'ಸಾಮಾನ್ಯ ಸ್ಥಿತಿ — ಜಾಗರೂಕರಾಗಿರಿ.',
      en: 'Average condition — stay cautious.',
    },
    low: {
      ta: 'கவனம் தேவை — பொறுமையாக இருங்கள்.',
      kn: 'ಗಮನ ಬೇಕು — ತಾಳ್ಮೆಯಿಂದಿರಿ.',
      en: 'Attention needed — be patient.',
    },
  };
  return texts[level][langCode] || texts[level].en;
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0c0a1d',
  },
  loadingContainer: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingMandala: {
    position: 'absolute',
  },
  omLoading: {
    fontSize: 48,
    color: '#8b5cf6',
    fontWeight: '300',
  },
  loadingText: {
    color: '#94a3b8',
    marginTop: 16,
    fontSize: 14,
  },
  errorText: {
    color: '#f59e0b',
    marginTop: 16,
    fontSize: 16,
    textAlign: 'center',
    paddingHorizontal: 40,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 12,
  },
  headerLeft: {
    flex: 1,
  },
  headerTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  headerOm: {
    fontSize: 24,
    color: '#f59e0b',
    marginRight: 8,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: '#fff',
  },
  headerSubtitle: {
    fontSize: 12,
    color: '#94a3b8',
    marginTop: 2,
    marginLeft: 32,
  },
  confidenceBadge: {
    alignItems: 'center',
    backgroundColor: 'rgba(139,92,246,0.15)',
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: 'rgba(139,92,246,0.3)',
  },
  confidenceBadgeLabel: {
    color: '#94a3b8',
    fontSize: 10,
    marginBottom: 2,
  },
  confidenceBadgeText: {
    color: '#8b5cf6',
    fontWeight: '700',
    fontSize: 16,
  },
  summaryContainer: {
    marginHorizontal: 20,
    marginBottom: 10,
    padding: 14,
    backgroundColor: 'rgba(255,255,255,0.03)',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.05)',
  },
  summaryDeco: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 8,
  },
  summaryLine: {
    height: 1,
    width: 40,
    backgroundColor: 'rgba(255,255,255,0.2)',
  },
  summaryIcon: {
    color: '#f59e0b',
    marginHorizontal: 10,
    fontSize: 12,
  },
  summaryText: {
    color: '#e2e8f0',
    fontSize: 13,
    lineHeight: 20,
    textAlign: 'center',
  },
  cardContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  card: {
    position: 'absolute',
    width: SCREEN_WIDTH - 40,
    height: SCREEN_HEIGHT * 0.56,
    borderRadius: 20,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.4,
    shadowRadius: 20,
    elevation: 12,
  },
  cardGradient: {
    flex: 1,
    padding: 20,
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  mandalaOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
  },
  constellationWrapper: {
    position: 'absolute',
    top: 20,
    left: 20,
    opacity: 0.4,
  },
  constellationOverlay: {
    position: 'absolute',
  },
  decorativeBorderContainer: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'space-between',
    paddingVertical: 8,
  },
  borderPattern: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 20,
  },
  borderTop: {},
  borderBottom: {},
  borderDot: {
    width: 4,
    height: 4,
    borderRadius: 2,
    opacity: 0.5,
  },
  borderLine: {
    height: 1,
    width: 50,
    marginHorizontal: 8,
    opacity: 0.3,
  },
  borderDiamond: {
    width: 8,
    height: 8,
    borderWidth: 1,
    transform: [{ rotate: '45deg' }],
    opacity: 0.5,
  },
  cardCounter: {
    position: 'absolute',
    top: 14,
    right: 14,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.3)',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 10,
  },
  omSymbol: {
    color: '#f59e0b',
    fontSize: 14,
    marginRight: 6,
  },
  cardCounterText: {
    color: 'rgba(255,255,255,0.7)',
    fontSize: 11,
    fontWeight: '600',
  },
  planetSymbolContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 15,
  },
  planetGlowOuter: {
    position: 'absolute',
    borderWidth: 1,
  },
  planetGlowInner: {
    position: 'absolute',
    borderWidth: 1,
  },
  planetSymbolText: {
    fontWeight: '300',
  },
  planetName: {
    fontSize: 12,
    fontWeight: '600',
    marginTop: 4,
    opacity: 0.8,
  },
  cardTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: '#fff',
    textAlign: 'center',
    marginTop: 4,
  },
  scoreCenter: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  scorePercentage: {
    fontSize: 38,
    fontWeight: '700',
  },
  scorePercent: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.6)',
    marginTop: -6,
  },
  scoreBadge: {
    paddingHorizontal: 18,
    paddingVertical: 6,
    borderRadius: 16,
    borderWidth: 1,
    marginTop: 4,
  },
  scoreBadgeText: {
    fontSize: 13,
    fontWeight: '700',
  },
  cardDescription: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.85)',
    textAlign: 'center',
    lineHeight: 20,
    paddingHorizontal: 8,
  },
  confidenceContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 4,
  },
  confidenceLabel: {
    color: 'rgba(255,255,255,0.5)',
    fontSize: 11,
    marginRight: 8,
  },
  confidenceBarBg: {
    width: 60,
    height: 4,
    backgroundColor: 'rgba(255,255,255,0.1)',
    borderRadius: 2,
    overflow: 'hidden',
  },
  confidenceBarFill: {
    height: '100%',
    borderRadius: 2,
  },
  confidenceValue: {
    color: 'rgba(255,255,255,0.6)',
    fontSize: 11,
    marginLeft: 8,
  },
  swipeHints: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 6,
  },
  swipeHint: {
    padding: 4,
  },
  swipeHintText: {
    color: 'rgba(255,255,255,0.3)',
    fontSize: 11,
    marginHorizontal: 8,
  },
  dotsContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    paddingVertical: 12,
  },
  dot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: 'rgba(255,255,255,0.25)',
    marginHorizontal: 3,
  },
  dotActive: {
    backgroundColor: '#f59e0b',
    width: 20,
  },
});
