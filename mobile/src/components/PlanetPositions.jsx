import React, { useRef, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, Animated, Easing } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';

// Planet symbols
const PLANET_SYMBOLS = {
  Sun: '☉', Moon: '☽', Mars: '♂', Mercury: '☿',
  Jupiter: '♃', Venus: '♀', Saturn: '♄', Rahu: '☊', Ketu: '☋',
};

// Planet colors - lighter pastels for backgrounds, darker for text
const PLANET_THEMES = {
  Sun: { bg: ['#fff7ed', '#ffedd5'], border: '#fb923c', text: '#9a3412', icon: '#ea580c' },
  Moon: { bg: ['#f5f3ff', '#ede9fe'], border: '#c4b5fd', text: '#5b21b6', icon: '#7c3aed' },
  Mars: { bg: ['#fee2e2', '#fecaca'], border: '#fca5a5', text: '#991b1b', icon: '#dc2626' },
  Mercury: { bg: ['#dcfce7', '#bbf7d0'], border: '#86efac', text: '#166534', icon: '#16a34a' },
  Jupiter: { bg: ['#fef9c3', '#fef08a'], border: '#fde047', text: '#854d0e', icon: '#ca8a04' },
  Venus: { bg: ['#fce7f3', '#fbcfe8'], border: '#f9a8d4', text: '#831843', icon: '#be185d' },
  Saturn: { bg: ['#e0e7ff', '#c7d2fe'], border: '#a5b4fc', text: '#3730a3', icon: '#4f46e5' },
  Rahu: { bg: ['#fef3c7', '#fde68a'], border: '#fcd34d', text: '#78350f', icon: '#b45309' },
  Ketu: { bg: ['#dbeafe', '#bfdbfe'], border: '#93c5fd', text: '#1e40af', icon: '#2563eb' },
};

// Animated planet card
const PlanetCard = ({ planet, index, language, t }) => {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(30)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 400,
        delay: index * 80,
        useNativeDriver: true,
        easing: Easing.out(Easing.ease),
      }),
      Animated.spring(slideAnim, {
        toValue: 0,
        friction: 8,
        tension: 40,
        delay: index * 80,
        useNativeDriver: true,
      }),
    ]).start();
  }, [index]);

  const theme = PLANET_THEMES[planet.name] || PLANET_THEMES.Sun;
  const symbol = PLANET_SYMBOLS[planet.name] || '⭐';
  const isRetrograde = planet.is_retrograde || planet.retrograde;

  return (
    <Animated.View
      style={[
        styles.cardWrapper,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      <LinearGradient colors={theme.bg} style={[styles.card, { borderColor: theme.border }]}>
        {/* Planet symbol and name */}
        <View style={[styles.iconContainer, { backgroundColor: theme.icon + '15' }]}>
          <Text style={[styles.symbol, { color: theme.icon }]}>{symbol}</Text>
        </View>

        <Text style={[styles.planetName, { color: theme.text }]}>
          {t ? t(planet.translationKey) : planet.name}
        </Text>

        {/* Sign information with better contrast */}
        <View style={styles.signRow}>
          <View style={[styles.signBadge, { backgroundColor: theme.icon + '10', borderColor: theme.border }]}>
            <Text style={[styles.signSymbol, { color: theme.icon }]}>
              {planet.sign_symbol || planet.rasi_symbol || '♈'}
            </Text>
            <Text style={[styles.signName, { color: theme.text }]}>
              {t ? t(planet.sign_translation_key) : (planet.sign_name || planet.rasi)}
            </Text>
          </View>
        </View>

        {/* Degree with improved readability */}
        <View style={styles.degreeRow}>
          <Ionicons name="navigate" size={14} color={theme.icon} />
          <Text style={[styles.degreeText, { color: theme.text }]}>
            {planet.degree_display || `${Math.round(planet.degree || 0)}°`}
          </Text>
        </View>

        {/* Nakshatra info - clearer */}
        {planet.nakshatra && (
          <View style={styles.nakshatraRow}>
            <Ionicons name="star" size={12} color={theme.icon} />
            <Text style={[styles.nakshatraText, { color: theme.text }]}>
              {t ? t(planet.nakshatra_key) : planet.nakshatra}
            </Text>
          </View>
        )}

        {/* Retrograde indicator - more visible */}
        {isRetrograde && (
          <View style={[styles.retroBadge, { backgroundColor: '#dc2626' }]}>
            <Text style={styles.retroText}>
              ℞ {language === 'ta' ? 'வ' : 'R'}
            </Text>
          </View>
        )}
      </LinearGradient>
    </Animated.View>
  );
};

// Retrograde Alert Component - improved visibility
const RetrogradeAlert = ({ retrograde, language, t }) => {
  const theme = PLANET_THEMES[retrograde.name] || PLANET_THEMES.Sun;
  const symbol = PLANET_SYMBOLS[retrograde.name] || '⭐';

  return (
    <View style={styles.retroAlert}>
      <LinearGradient
        colors={['#fee2e2', '#fecaca']}
        style={styles.retroAlertGradient}
      >
        <View style={styles.retroAlertHeader}>
          <View style={[styles.retroIconBg, { backgroundColor: '#dc2626' }]}>
            <Text style={styles.retroSymbol}>{symbol}</Text>
          </View>
          <View style={styles.retroInfo}>
            <Text style={styles.retroName}>
              {t ? t(retrograde.translationKey) : retrograde.name}
            </Text>
            <View style={styles.retroStatusPill}>
              <Ionicons name="refresh" size={14} color="#991b1b" />
              <Text style={styles.retroStatus}>
                {language === 'ta' ? 'வக்ர நிலை' : 'Retrograde'}
              </Text>
            </View>
          </View>
          {retrograde.days_remaining && (
            <View style={styles.retroDaysBox}>
              <Text style={styles.retroDaysNumber}>{retrograde.days_remaining}</Text>
              <Text style={styles.retroDaysLabel}>
                {language === 'ta' ? 'நாட்கள்' : 'days'}
              </Text>
            </View>
          )}
        </View>
        <Text style={styles.retroMessage}>
          {retrograde.message || 
           `${language === 'ta' ? 'வக்ர கிரக காலம் - கவனமாக இருங்கள்' : 'Retrograde period - exercise caution'}`}
        </Text>
      </LinearGradient>
    </View>
  );
};

// Transit Preview Component
const TransitPreview = ({ transit, language, t }) => {
  const theme = PLANET_THEMES[transit.name] || PLANET_THEMES.Sun;
  const symbol = PLANET_SYMBOLS[transit.name] || '⭐';

  return (
    <View style={styles.transitCard}>
      <View style={[styles.transitIconBox, { backgroundColor: theme.icon + '15' }]}>
        <Text style={[styles.transitSymbol, { color: theme.icon }]}>{symbol}</Text>
      </View>
      
      <View style={styles.transitInfo}>
        <Text style={styles.transitPlanet}>
          {t ? t(transit.translationKey) : transit.name}
        </Text>
        <View style={styles.transitArrowRow}>
          <Text style={styles.transitSign}>
            {transit.from_sign_symbol} {t ? t(transit.from_sign_key) : transit.from_sign}
          </Text>
          <Ionicons name="arrow-forward" size={14} color={theme.icon} />
          <Text style={[styles.transitSign, { color: theme.icon, fontWeight: '700' }]}>
            {transit.to_sign_symbol} {t ? t(transit.to_sign_key) : transit.to_sign}
          </Text>
        </View>
      </View>

      <View style={styles.transitTimeBox}>
        <Text style={styles.transitTimeValue}>
          {Math.round(transit.hours_remaining || 0)}
        </Text>
        <Text style={styles.transitTimeLabel}>
          {language === 'ta' ? 'மணி' : 'HRS'}
        </Text>
      </View>
    </View>
  );
};

export default function PlanetPositions({ 
  planets = [], 
  retrogrades = [],
  upcomingTransits = [],
  language = 'en', 
  t 
}) {
  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Ionicons name="location" size={20} color="#6b5644" />
        <Text style={styles.title}>
          {language === 'ta' ? 'கிரக நிலைகள்' : 'PLANET POSITIONS'}
        </Text>
      </View>

      {/* Planet cards - horizontal scroll */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {planets.map((planet, index) => (
          <PlanetCard
            key={index}
            planet={planet}
            index={index}
            language={language}
            t={t}
          />
        ))}
      </ScrollView>

      {/* Retrograde alerts */}
      {retrogrades.length > 0 && (
        <View style={styles.retroSection}>
          <View style={styles.retroSectionHeader}>
            <Ionicons name="alert-circle" size={18} color="#dc2626" />
            <Text style={styles.retroSectionTitle}>
              {language === 'ta' ? 'வக்ர எச்சரிக்கை' : 'Retrograde Alert'}
            </Text>
          </View>
          {retrogrades.map((retro, index) => (
            <RetrogradeAlert
              key={index}
              retrograde={retro}
              language={language}
              t={t}
            />
          ))}
        </View>
      )}

      {/* Upcoming transits */}
      {upcomingTransits.length > 0 && (
        <View style={styles.transitSection}>
          <View style={styles.transitSectionHeader}>
            <Ionicons name="calendar" size={18} color="#6b5644" />
            <Text style={styles.transitSectionTitle}>
              {language === 'ta' ? 'வரவிருக்கும் மாற்றங்கள்' : 'Coming Up'}
            </Text>
          </View>
          {upcomingTransits.slice(0, 3).map((transit, index) => (
            <TransitPreview
              key={index}
              transit={transit}
              language={language}
              t={t}
            />
          ))}
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginTop: 16,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    paddingHorizontal: 16,
    marginBottom: 16,
  },
  title: {
    fontSize: 18,
    fontWeight: '700',
    color: '#6b5644',
    letterSpacing: 0.8,
  },
  scrollContent: {
    paddingHorizontal: 16,
    gap: 12,
  },
  cardWrapper: {
    width: 140,
  },
  card: {
    padding: 16,
    borderRadius: 20,
    borderWidth: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.12,
    shadowRadius: 8,
    elevation: 4,
    minHeight: 200,
    position: 'relative',
  },
  iconContainer: {
    width: 56,
    height: 56,
    borderRadius: 28,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
    borderWidth: 2,
    borderColor: 'rgba(0,0,0,0.05)',
  },
  symbol: {
    fontSize: 28,
    fontWeight: '600',
    color: '#1f2937',
  },
  planetName: {
    fontSize: 14,
    fontWeight: '800',
    letterSpacing: 0.5,
    marginBottom: 8,
    textTransform: 'uppercase',
    color: '#6b5644',
  },
  signRow: {
    marginBottom: 10,
  },
  signBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 12,
    borderWidth: 1.5,
  },
  signSymbol: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1f2937',
  },
  signName: {
    fontSize: 12,
    fontWeight: '700',
    letterSpacing: 0.3,
    color: '#6b5644',
  },
  degreeRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginBottom: 6,
  },
  degreeText: {
    fontSize: 14,
    fontWeight: '800',
    letterSpacing: 0.3,
    color: '#6b5644',
  },
  nakshatraRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  nakshatraText: {
    fontSize: 12,
    fontWeight: '700',
    color: '#1f2937',
  },
  retroBadge: {
    position: 'absolute',
    top: 12,
    right: 12,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 10,
  },
  retroText: {
    fontSize: 12,
    fontWeight: '900',
    color: '#ffffff',
    letterSpacing: 0.5,
  },
  retroSection: {
    paddingHorizontal: 16,
    marginTop: 24,
  },
  retroSectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 12,
  },
  retroSectionTitle: {
    fontSize: 17,
    fontWeight: '800',
    color: '#7c2d12',
    letterSpacing: 0.5,
  },
  retroAlert: {
    marginBottom: 12,
  },
  retroAlertGradient: {
    borderRadius: 16,
    padding: 16,
    borderWidth: 1.5,
    borderColor: '#fca5a5',
  },
  retroAlertHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    marginBottom: 10,
  },
  retroIconBg: {
    width: 44,
    height: 44,
    borderRadius: 22,
    justifyContent: 'center',
    alignItems: 'center',
  },
  retroSymbol: {
    fontSize: 22,
    color: '#ffffff',
    fontWeight: '600',
  },
  retroInfo: {
    flex: 1,
    gap: 4,
  },
  retroName: {
    fontSize: 17,
    fontWeight: '900',
    color: '#5a2d0c',
    letterSpacing: 0.4,
  },
  retroStatusPill: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    alignSelf: 'flex-start',
    paddingHorizontal: 8,
    paddingVertical: 3,
    backgroundColor: '#ffffff',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#fca5a5',
  },
  retroStatus: {
    fontSize: 12,
    fontWeight: '800',
    color: '#7c2d12',
  },
  retroDaysBox: {
    alignItems: 'center',
    backgroundColor: '#ffffff',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 12,
    borderWidth: 1.5,
    borderColor: '#fca5a5',
  },
  retroDaysNumber: {
    fontSize: 20,
    fontWeight: '900',
    color: '#dc2626',
    lineHeight: 22,
  },
  retroDaysLabel: {
    fontSize: 11,
    color: '#7c2d12',
    fontWeight: '700',
  },
  retroMessage: {
    fontSize: 14,
    color: '#5a2d0c',
    lineHeight: 22,
    fontWeight: '700',
  },
  transitSection: {
    paddingHorizontal: 16,
    marginTop: 24,
  },
  transitSectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 12,
  },
  transitSectionTitle: {
    fontSize: 17,
    fontWeight: '800',
    color: '#5a4838',
    letterSpacing: 0.5,
  },
  transitCard: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    backgroundColor: '#ffffff',
    borderRadius: 16,
    padding: 14,
    marginBottom: 10,
    borderWidth: 1.5,
    borderColor: '#e8d5c4',
    shadowColor: '#d4a574',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 4,
    elevation: 2,
  },
  transitIconBox: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'rgba(0,0,0,0.05)',
  },
  transitSymbol: {
    fontSize: 22,
    fontWeight: '600',
    color: '#1f2937',
  },
  transitInfo: {
    flex: 1,
    gap: 4,
  },
  transitPlanet: {
    fontSize: 15,
    fontWeight: '900',
    color: '#6b5644',
    letterSpacing: 0.4,
  },
  transitArrowRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    color: '#0f172a',
  },
  transitSign: {
    fontSize: 13,
    fontWeight: '700',
    color: '#6b5644',
  },
  transitTimeBox: {
    alignItems: 'center',
    backgroundColor: '#f3f4f6',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#e5e7eb',
  },
  transitTimeValue: {
    fontSize: 20,
    fontWeight: '900',
    color: '#6b5644',
    lineHeight: 22,
  },
  transitTimeLabel: {
    fontSize: 10,
    color: '#0f172a',
    fontWeight: '800',
  },
});
