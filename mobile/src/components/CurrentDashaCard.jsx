import React, { useRef, useEffect } from 'react';
import { View, Text, StyleSheet, Animated, Easing } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';

// Animated shimmer effect
const ShimmerEffect = () => {
  const shimmerAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.loop(
      Animated.timing(shimmerAnim, {
        toValue: 1,
        duration: 2000,
        useNativeDriver: true,
        easing: Easing.linear,
      })
    ).start();
  }, []);

  const translateX = shimmerAnim.interpolate({
    inputRange: [0, 1],
    outputRange: [-100, 300],
  });

  return (
    <Animated.View
      style={[
        styles.shimmer,
        {
          transform: [{ translateX }],
        },
      ]}
    />
  );
};

// Animated card wrapper
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

export default function CurrentDashaCard({ 
  mahaDasha = 'Jupiter',
  antarDasha = null,
  yearsRemaining = null,
  language = 'en',
  t 
}) {
  return (
    <AnimatedCard delay={500}>
      <View style={styles.card}>
        {/* Decorative shimmer overlay */}
        <View style={styles.shimmerContainer}>
          <ShimmerEffect />
        </View>

        {/* Header with icon */}
        <View style={styles.header}>
          <LinearGradient
            colors={['#faf5ff', '#f3e8ff']}
            style={styles.iconBg}
          >
            <Ionicons name="sparkles" size={24} color="#7c3aed" />
          </LinearGradient>
          <Text style={styles.title}>
            {language === 'ta' ? 'நடப்பு தசா' : 'Current Dasha'}
          </Text>
        </View>

        {/* Dasha information grid */}
        <View style={styles.dashaGrid}>
          {/* Maha Dasha */}
          <View style={styles.dashaItem}>
            <Text style={styles.dashaLabel}>
              {language === 'ta' ? 'மகா தசா' : 'MAHA DASHA'}
            </Text>
            <LinearGradient
              colors={['#faf5ff', '#f3e8ff']}
              style={styles.dashaValueBg}
            >
              <Text style={styles.dashaValue}>
                {t ? t(mahaDasha.toLowerCase() + '_planet') : mahaDasha}
              </Text>
            </LinearGradient>
            {yearsRemaining && (
              <View style={styles.durationBadge}>
                <Ionicons name="time" size={12} color="#8b5cf6" />
                <Text style={styles.durationText}>
                  {yearsRemaining} {language === 'ta' ? 'ஆண்டுகள்' : 'years'}
                </Text>
              </View>
            )}
          </View>

          {/* Antar Dasha */}
          {antarDasha && (
            <View style={styles.dashaItem}>
              <Text style={styles.dashaLabel}>
                {language === 'ta' ? 'அந்தர தசா' : 'ANTAR DASHA'}
              </Text>
              <LinearGradient
                colors={['#ede9fe', '#ddd6fe']}
                style={styles.dashaValueBg}
              >
                <Text style={styles.dashaValue}>
                  {t ? t(antarDasha.toLowerCase() + '_planet') : antarDasha}
                </Text>
              </LinearGradient>
            </View>
          )}
        </View>

        {/* Info footer */}
        <View style={styles.infoFooter}>
          <Ionicons name="information-circle" size={16} color="#8b5cf6" />
          <Text style={styles.infoText}>
            {language === 'ta' 
              ? 'தசா உங்கள் வாழ்க்கை பயணத்தை வழிநடத்துகிறது'
              : 'Dasha guides your life journey'}
          </Text>
        </View>
      </View>
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
    borderColor: '#e9d5ff',
    shadowColor: '#7c3aed',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.12,
    shadowRadius: 12,
    elevation: 4,
    overflow: 'hidden',
    position: 'relative',
  },
  shimmerContainer: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    overflow: 'hidden',
  },
  shimmer: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(139, 92, 246, 0.05)',
    transform: [{ skewX: '-20deg' }],
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    marginBottom: 20,
  },
  iconBg: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#e9d5ff',
  },
  title: {
    fontSize: 18,
    fontWeight: '700',
    color: '#5b21b6',
    letterSpacing: 0.3,
  },
  dashaGrid: {
    flexDirection: 'row',
    gap: 12,
  },
  dashaItem: {
    flex: 1,
    gap: 10,
  },
  dashaLabel: {
    fontSize: 11,
    fontWeight: '800',
    color: '#7c3aed',
    letterSpacing: 0.8,
  },
  dashaValueBg: {
    paddingVertical: 14,
    paddingHorizontal: 16,
    borderRadius: 14,
    borderWidth: 1.5,
    borderColor: '#ddd6fe',
    alignItems: 'center',
    shadowColor: '#7c3aed',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 4,
    elevation: 2,
  },
  dashaValue: {
    fontSize: 16,
    fontWeight: '800',
    color: '#5b21b6',
    letterSpacing: 0.3,
  },
  durationBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    alignSelf: 'flex-start',
    backgroundColor: '#faf5ff',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#e9d5ff',
  },
  durationText: {
    fontSize: 11,
    fontWeight: '700',
    color: '#7c3aed',
  },
  infoFooter: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginTop: 16,
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: '#f3e8ff',
  },
  infoText: {
    flex: 1,
    fontSize: 12,
    color: '#6b21a8',
    fontWeight: '600',
    lineHeight: 18,
  },
});
