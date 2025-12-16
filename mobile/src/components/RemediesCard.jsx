import React, { useRef, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Animated, Easing } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';

// Planet symbols mapping
const PLANET_SYMBOLS = {
  Sun: '☉', Moon: '☽', Mars: '♂', Mercury: '☿',
  Jupiter: '♃', Venus: '♀', Saturn: '♄', Rahu: '☊', Ketu: '☋',
  சூரியன்: '☉', சந்திரன்: '☽', செவ்வாய்: '♂', புதன்: '☿',
  குரு: '♃', சுக்கிரன்: '♀', சனி: '♄', ராகு: '☊', கேது: '☋'
};

// Animated Card Wrapper
const AnimatedCard = ({ children, delay = 0 }) => {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const scaleAnim = useRef(new Animated.Value(0.95)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 400,
        delay,
        useNativeDriver: true,
        easing: Easing.out(Easing.ease),
      }),
      Animated.spring(scaleAnim, {
        toValue: 1,
        friction: 8,
        tension: 40,
        delay,
        useNativeDriver: true,
      }),
    ]).start();
  }, [delay]);

  return (
    <Animated.View style={{ opacity: fadeAnim, transform: [{ scale: scaleAnim }] }}>
      {children}
    </Animated.View>
  );
};

export default function RemediesCard({ planets = [], onPress, language = 'en', t }) {
  const getPlanetSymbol = (planet) => {
    return PLANET_SYMBOLS[planet.name] || PLANET_SYMBOLS[planet.tamil] || '⭐';
  };

  return (
    <AnimatedCard delay={400}>
      <TouchableOpacity activeOpacity={0.9} onPress={onPress}>
        <View style={styles.card}>
          {/* Decorative accent border */}
          <LinearGradient
            colors={['#f97316', '#ea580c']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.accentBorder}
          />

          <View style={styles.header}>
            <View style={styles.iconContainer}>
              <LinearGradient
                colors={['#fed7aa', '#fdba74']}
                style={styles.iconGradient}
              >
                <Ionicons name="leaf-outline" size={28} color="#9a3412" />
              </LinearGradient>
            </View>

            <View style={styles.titleSection}>
              <Text style={styles.title}>
                {language === 'ta' ? 'இன்றைய பரிகாரங்கள்' : 'Today\'s Remedies'}
              </Text>
              <Text style={styles.subtitle}>
                {language === 'ta' ? 'பரிகாரங்களுக்கு தட்டவும்' : 'Tap for remedies'}
              </Text>
            </View>

            <View style={styles.arrowContainer}>
              <Ionicons name="chevron-forward-circle" size={28} color="#f97316" />
            </View>
          </View>

          {/* Planet badges with better contrast */}
          {planets.length > 0 && (
            <View style={styles.planetsSection}>
              <Text style={styles.planetsLabel}>
                {language === 'ta' ? 'கவனிக்க வேண்டிய கிரகங்கள்' : 'Planets Needing Attention'}
              </Text>
              <View style={styles.planetsRow}>
                {planets.slice(0, 3).map((planet, i) => (
                  <LinearGradient
                    key={i}
                    colors={['#fff7ed', '#ffedd5']}
                    style={styles.planetBadge}
                  >
                    <Text style={styles.planetSymbol}>{getPlanetSymbol(planet)}</Text>
                    <Text style={styles.planetName}>
                      {t ? t(planet.translationKey) : (planet.name || planet.tamil)}
                    </Text>
                  </LinearGradient>
                ))}
              </View>
            </View>
          )}

          {/* Quick remedy icons with better labels */}
          <View style={styles.remedySection}>
            <View style={styles.remedyRow}>
              <View style={styles.remedyItem}>
                <View style={[styles.remedyIconBg, { backgroundColor: '#fef3c7' }]}>
                  <Ionicons name="flower" size={20} color="#d97706" />
                </View>
                <Text style={styles.remedyLabel}>
                  {language === 'ta' ? 'பூஜை' : 'Puja'}
                </Text>
              </View>

              <View style={styles.remedyItem}>
                <View style={[styles.remedyIconBg, { backgroundColor: '#dbeafe' }]}>
                  <Ionicons name="water" size={20} color="#1d4ed8" />
                </View>
                <Text style={styles.remedyLabel}>
                  {language === 'ta' ? 'தானம்' : 'Charity'}
                </Text>
              </View>

              <View style={styles.remedyItem}>
                <View style={[styles.remedyIconBg, { backgroundColor: '#fce7f3' }]}>
                  <Ionicons name="musical-notes" size={20} color="#be185d" />
                </View>
                <Text style={styles.remedyLabel}>
                  {language === 'ta' ? 'மந்திரம்' : 'Mantra'}
                </Text>
              </View>
            </View>
          </View>
        </View>
      </TouchableOpacity>
    </AnimatedCard>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 20,
    padding: 20,
    marginHorizontal: 16,
    marginTop: 16,
    borderWidth: 1.5,
    borderColor: '#fed7aa',
    shadowColor: '#ea580c',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.12,
    shadowRadius: 12,
    elevation: 4,
    overflow: 'hidden',
  },
  accentBorder: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: 4,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 14,
    marginBottom: 18,
  },
  iconContainer: {
    width: 60,
    height: 60,
    borderRadius: 30,
    overflow: 'hidden',
    shadowColor: '#ea580c',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 4,
    elevation: 3,
  },
  iconGradient: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  titleSection: {
    flex: 1,
  },
  title: {
    fontSize: 19,
    fontWeight: '700',
    color: '#7c2d12',
    letterSpacing: 0.3,
  },
  subtitle: {
    fontSize: 13,
    color: '#9a3412',
    marginTop: 3,
    fontWeight: '500',
  },
  arrowContainer: {
    padding: 4,
  },
  planetsSection: {
    marginBottom: 16,
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: '#fed7aa',
  },
  planetsLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: '#92400e',
    marginBottom: 10,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  planetsRow: {
    flexDirection: 'row',
    gap: 10,
  },
  planetBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderRadius: 16,
    gap: 8,
    borderWidth: 1,
    borderColor: '#fdba74',
    shadowColor: '#ea580c',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 1,
  },
  planetSymbol: {
    fontSize: 20,
    color: '#9a3412',
  },
  planetName: {
    fontSize: 14,
    fontWeight: '700',
    color: '#7c2d12',
    letterSpacing: 0.2,
  },
  remedySection: {
    backgroundColor: '#fef3c7',
    borderRadius: 14,
    padding: 14,
    borderWidth: 1,
    borderColor: '#fde68a',
  },
  remedyRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  remedyItem: {
    alignItems: 'center',
    gap: 8,
  },
  remedyIconBg: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: 'rgba(0,0,0,0.05)',
  },
  remedyLabel: {
    fontSize: 12,
    color: '#78350f',
    fontWeight: '600',
    letterSpacing: 0.2,
  },
});
