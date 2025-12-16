import React, { useRef, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Animated, Easing } from 'react';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';

// Planet symbols
const PLANET_SYMBOLS = {
  Sun: '☉', Moon: '☽', Mars: '♂', Mercury: '☿',
  Jupiter: '♃', Venus: '♀', Saturn: '♄', Rahu: '☊', Ketu: '☋',
};

// Animated pulse for center score
const PulsingCenter = ({ score, label }) => {
  const pulseAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.05,
          duration: 1500,
          useNativeDriver: true,
          easing: Easing.inOut(Easing.ease),
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 1500,
          useNativeDriver: true,
          easing: Easing.inOut(Easing.ease),
        }),
      ])
    ).start();
  }, []);

  return (
    <Animated.View style={[styles.centerCircle, { transform: [{ scale: pulseAnim }] }]}>
      <Text style={styles.centerScore}>{score}</Text>
      <Text style={styles.centerLabel}>{label}</Text>
    </Animated.View>
  );
};

// Individual planet orb
const PlanetOrb = ({ planet, index }) => {
  const scaleAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.spring(scaleAnim, {
      toValue: 1,
      friction: 6,
      tension: 40,
      delay: index * 100,
      useNativeDriver: true,
    }).start();
  }, [index]);

  // Position planets in a circle
  const angle = (index * 40) * (Math.PI / 180);
  const radius = 90;
  const x = Math.cos(angle) * radius;
  const y = Math.sin(angle) * radius;

  const symbol = PLANET_SYMBOLS[planet.name] || planet.symbol || '⭐';
  const score = planet.score || planet.strength || 50;
  
  // Determine color based on score
  let gradientColors = ['#fca5a5', '#ef4444']; // Red (low)
  let borderColor = '#dc2626';
  if (score >= 70) {
    gradientColors = ['#86efac', '#22c55e']; // Green (good)
    borderColor = '#16a34a';
  } else if (score >= 50) {
    gradientColors = ['#fde047', '#facc15']; // Yellow (average)
    borderColor = '#ca8a04';
  }

  return (
    <Animated.View
      style={[
        styles.planetOrb,
        {
          left: 115 + x - 24,
          top: 115 + y - 24,
          transform: [{ scale: scaleAnim }],
        },
      ]}
    >
      <LinearGradient
        colors={gradientColors}
        style={styles.planetOrbGradient}
      >
        <Text style={styles.planetSymbol}>{symbol}</Text>
        <View style={[styles.scoreChip, { borderColor }]}>
          <Text style={[styles.scoreChipText, { color: borderColor }]}>{score}</Text>
        </View>
      </LinearGradient>
    </Animated.View>
  );
};

export default function PlanetAuraMap({ 
  planets = [], 
  overallScore = 63, 
  auraLevel = 'Strong Aura',
  dominantPlanets = [],
  challengedPlanets = [],
  language = 'en',
  t
}) {
  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Ionicons name="planet" size={20} color="#6b5644" />
        <Text style={styles.title}>
          {language === 'ta' ? 'கிரக ஒளிநிலை வரைபடம்' : 'Planet Aura Map'}
        </Text>
        <View style={styles.overallBadge}>
          <Text style={styles.overallScore}>{overallScore}%</Text>
        </View>
      </View>

      {/* Aura level indicator with better contrast */}
      <View style={styles.levelSection}>
        <LinearGradient
          colors={overallScore >= 70 ? ['#dcfce7', '#bbf7d0'] : 
                  overallScore >= 50 ? ['#fef9c3', '#fef08a'] : 
                  ['#fee2e2', '#fecaca']}
          style={styles.levelBadge}
        >
          <Ionicons 
            name={overallScore >= 70 ? 'checkmark-circle' : 
                  overallScore >= 50 ? 'alert-circle' : 
                  'warning'} 
            size={18} 
            color={overallScore >= 70 ? '#166534' : 
                   overallScore >= 50 ? '#854d0e' : 
                   '#991b1b'} 
          />
          <Text style={[
            styles.levelText,
            { color: overallScore >= 70 ? '#166534' : 
                     overallScore >= 50 ? '#854d0e' : 
                     '#991b1b' }
          ]}>
            {auraLevel}
          </Text>
        </LinearGradient>

        <View style={styles.statsRow}>
          <View style={styles.statItem}>
            <Ionicons name="checkmark-circle" size={16} color="#16a34a" />
            <Text style={styles.statText}>{dominantPlanets.length}</Text>
            <Text style={styles.statLabel}>
              {language === 'ta' ? 'நல்ல' : 'Good'}
            </Text>
          </View>
          <View style={styles.statDivider} />
          <View style={styles.statItem}>
            <Ionicons name="alert-circle" size={16} color="#dc2626" />
            <Text style={styles.statText}>{challengedPlanets.length}</Text>
            <Text style={styles.statLabel}>
              {language === 'ta' ? 'பலவீனம்' : 'Weak'}
            </Text>
          </View>
        </View>
      </View>

      {/* Radial visualization */}
      <View style={styles.radialContainer}>
        {/* Background rings */}
        <View style={[styles.ring, { width: 200, height: 200 }]} />
        <View style={[styles.ring, { width: 160, height: 160 }]} />
        <View style={[styles.ring, { width: 120, height: 120 }]} />
        
        {/* Center score */}
        <PulsingCenter 
          score={overallScore} 
          label={language === 'ta' ? 'ஒளி' : 'Aura'} 
        />

        {/* Planet orbs */}
        {planets.map((planet, index) => (
          <PlanetOrb key={index} planet={planet} index={index} />
        ))}
      </View>

      {/* Planet legend with better readability */}
      <ScrollView 
        horizontal 
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.legendScroll}
      >
        {planets.map((planet, index) => {
          const score = planet.score || planet.strength || 50;
          const scoreColor = score >= 70 ? '#16a34a' : score >= 50 ? '#ca8a04' : '#dc2626';
          
          return (
            <View key={index} style={[styles.legendItem, { borderColor: scoreColor + '30' }]}>
              <View style={[styles.legendDot, { backgroundColor: scoreColor }]} />
              <View style={styles.legendInfo}>
                <Text style={styles.legendName}>
                  {t ? t(planet.translationKey) : planet.name}
                </Text>
                <Text style={[styles.legendScore, { color: scoreColor }]}>
                  {score}%
                </Text>
              </View>
            </View>
          );
        })}
      </ScrollView>

      {/* Summary section with improved contrast */}
      <View style={styles.summarySection}>
        {/* Strong planets */}
        {dominantPlanets.length > 0 && (
          <View style={styles.summaryRow}>
            <View style={styles.summaryHeader}>
              <Ionicons name="trending-up" size={16} color="#16a34a" />
              <Text style={styles.summaryTitle}>
                {language === 'ta' ? 'வலிமையான கிரகங்கள்' : 'STRONG'}
              </Text>
            </View>
            <Text style={styles.summaryList}>
              {dominantPlanets.map(p => t ? t(p.translationKey) : p.name).join(', ')}
            </Text>
          </View>
        )}

        {/* Challenged planets */}
        {challengedPlanets.length > 0 && (
          <View style={styles.summaryRow}>
            <View style={styles.summaryHeader}>
              <Ionicons name="medical" size={16} color="#dc2626" />
              <Text style={[styles.summaryTitle, { color: '#dc2626' }]}>
                {language === 'ta' ? 'பரிகாரம் தேவை' : 'NEEDS REMEDY'}
              </Text>
            </View>
            <Text style={[styles.summaryList, { color: '#dc2626' }]}>
              {challengedPlanets.map(p => t ? t(p.translationKey) : p.name).join(', ')}
            </Text>
          </View>
        )}
      </View>

      {/* Insight text with darker, readable color */}
      <View style={styles.insightBox}>
        <Ionicons name="bulb" size={16} color="#92400e" />
        <Text style={styles.insightText}>
          {language === 'ta' 
            ? 'அனைத்து காலங்களிலும் கிரகங்கள் இவ்வாறு நம் வாழ்க்கையை பாதிக்கின்றன'
            : 'All planets continuously influence your life energy and opportunities'}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#ffffff',
    borderRadius: 20,
    padding: 20,
    marginHorizontal: 16,
    marginTop: 16,
    borderWidth: 1.5,
    borderColor: '#e8d5c4',
    shadowColor: '#d4a574',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 12,
    elevation: 3,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    marginBottom: 16,
  },
  title: {
    flex: 1,
    fontSize: 18,
    fontWeight: '700',
    color: '#6b5644',
    letterSpacing: 0.3,
  },
  overallBadge: {
    backgroundColor: '#fef3c7',
    paddingHorizontal: 14,
    paddingVertical: 6,
    borderRadius: 14,
    borderWidth: 1.5,
    borderColor: '#fde68a',
  },
  overallScore: {
    fontSize: 16,
    fontWeight: '900',
    color: '#78350f',
    letterSpacing: 0.3,
  },
  levelSection: {
    marginBottom: 20,
  },
  levelBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 16,
    alignSelf: 'flex-start',
    borderWidth: 1.5,
    borderColor: 'rgba(0,0,0,0.08)',
    marginBottom: 12,
  },
  levelText: {
    fontSize: 15,
    fontWeight: '800',
    letterSpacing: 0.4,
  },
  statsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
  },
  statItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  statText: {
    fontSize: 16,
    fontWeight: '800',
    color: '#1f2937',
  },
  statLabel: {
    fontSize: 12,
    color: '#6b7280',
    fontWeight: '600',
  },
  statDivider: {
    width: 1,
    height: 20,
    backgroundColor: '#d1d5db',
  },
  radialContainer: {
    width: 240,
    height: 240,
    alignSelf: 'center',
    justifyContent: 'center',
    alignItems: 'center',
    marginVertical: 20,
  },
  ring: {
    position: 'absolute',
    borderRadius: 200,
    borderWidth: 1,
    borderColor: '#e8d5c4',
    opacity: 0.5,
  },
  centerCircle: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#ffffff',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 10,
    borderWidth: 3,
    borderColor: '#8b6f47',
    shadowColor: '#d4a574',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 6,
  },
  centerScore: {
    fontSize: 22,
    fontWeight: '900',
    color: '#6b5644',
    letterSpacing: -0.5,
  },
  centerLabel: {
    fontSize: 10,
    color: '#8b6f47',
    fontWeight: '700',
    marginTop: -2,
  },
  planetOrb: {
    position: 'absolute',
    width: 48,
    height: 48,
    zIndex: 5,
  },
  planetOrbGradient: {
    flex: 1,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2.5,
    borderColor: '#ffffff',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.25,
    shadowRadius: 6,
    elevation: 5,
  },
  planetSymbol: {
    fontSize: 22,
    color: '#0f172a',
    fontWeight: '900',
    textShadowColor: 'rgba(255, 255, 255, 0.5)',
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 2,
  },
  scoreChip: {
    position: 'absolute',
    bottom: -6,
    right: -6,
    backgroundColor: '#ffffff',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 10,
    borderWidth: 2,
    minWidth: 28,
    alignItems: 'center',
  },
  scoreChipText: {
    fontSize: 12,
    fontWeight: '900',
    color: '#1f2937',
    textShadowColor: 'rgba(0, 0, 0, 0.1)',
    textShadowOffset: { width: 0, height: 0.5 },
    textShadowRadius: 1,
  },
  legendScroll: {
    paddingVertical: 12,
    paddingHorizontal: 4,
    gap: 10,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    backgroundColor: '#fef6ed',
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderRadius: 16,
    marginRight: 8,
    borderWidth: 1.5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.08,
    shadowRadius: 2,
    elevation: 1,
  },
  legendDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
  },
  legendInfo: {
    gap: 2,
  },
  legendName: {
    fontSize: 14,
    fontWeight: '800',
    color: '#0f172a',
    letterSpacing: 0.3,
  },
  legendScore: {
    fontSize: 14,
    fontWeight: '900',
    letterSpacing: 0.4,
    color: '#1f2937',
  },
  summarySection: {
    gap: 12,
    marginTop: 16,
    paddingTop: 16,
    borderTopWidth: 1.5,
    borderTopColor: '#e8d5c4',
  },
  summaryRow: {
    gap: 8,
  },
  summaryHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  summaryTitle: {
    fontSize: 12,
    fontWeight: '800',
    color: '#16a34a',
    letterSpacing: 0.8,
  },
  summaryList: {
    fontSize: 15,
    fontWeight: '800',
    color: '#15803d',
    lineHeight: 24,
    paddingLeft: 24,
  },
  insightBox: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 10,
    backgroundColor: '#fef3c7',
    borderRadius: 14,
    padding: 14,
    marginTop: 16,
    borderWidth: 1,
    borderColor: '#fde68a',
  },
  insightText: {
    flex: 1,
    fontSize: 14,
    color: '#5a3a1a',
    lineHeight: 22,
    fontWeight: '700',
  },
});
