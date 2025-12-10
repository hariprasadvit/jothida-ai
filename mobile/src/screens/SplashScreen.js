import React, { useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Animated,
  Dimensions,
  Easing,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';

const { width, height } = Dimensions.get('window');

export default function SplashScreen({ onFinish }) {
  // Animated values
  const logoScale = useRef(new Animated.Value(0)).current;
  const logoRotate = useRef(new Animated.Value(0)).current;
  const titleOpacity = useRef(new Animated.Value(0)).current;
  const titleTranslateY = useRef(new Animated.Value(30)).current;
  const subtitleOpacity = useRef(new Animated.Value(0)).current;
  const starScale = useRef(new Animated.Value(0)).current;
  const ringScale = useRef(new Animated.Value(0.5)).current;
  const ringOpacity = useRef(new Animated.Value(0.8)).current;
  const shimmerPosition = useRef(new Animated.Value(-width)).current;

  // Particle animations
  const particles = useRef(
    Array.from({ length: 12 }, () => ({
      translateX: new Animated.Value(0),
      translateY: new Animated.Value(0),
      opacity: new Animated.Value(0),
      scale: new Animated.Value(0),
    }))
  ).current;

  useEffect(() => {
    // Start animation sequence
    Animated.sequence([
      // Ring pulse animation
      Animated.parallel([
        Animated.timing(ringScale, {
          toValue: 1.5,
          duration: 800,
          easing: Easing.out(Easing.ease),
          useNativeDriver: true,
        }),
        Animated.timing(ringOpacity, {
          toValue: 0,
          duration: 800,
          useNativeDriver: true,
        }),
      ]),

      // Logo entrance with bounce
      Animated.parallel([
        Animated.spring(logoScale, {
          toValue: 1,
          friction: 4,
          tension: 40,
          useNativeDriver: true,
        }),
        Animated.timing(logoRotate, {
          toValue: 1,
          duration: 1000,
          easing: Easing.out(Easing.back(1.5)),
          useNativeDriver: true,
        }),
      ]),

      // Title fade in
      Animated.parallel([
        Animated.timing(titleOpacity, {
          toValue: 1,
          duration: 500,
          useNativeDriver: true,
        }),
        Animated.timing(titleTranslateY, {
          toValue: 0,
          duration: 500,
          easing: Easing.out(Easing.ease),
          useNativeDriver: true,
        }),
      ]),

      // Subtitle and stars
      Animated.parallel([
        Animated.timing(subtitleOpacity, {
          toValue: 1,
          duration: 400,
          useNativeDriver: true,
        }),
        Animated.spring(starScale, {
          toValue: 1,
          friction: 5,
          useNativeDriver: true,
        }),
      ]),
    ]).start();

    // Shimmer animation loop
    const shimmerLoop = Animated.loop(
      Animated.timing(shimmerPosition, {
        toValue: width,
        duration: 1500,
        easing: Easing.linear,
        useNativeDriver: true,
      })
    );
    shimmerLoop.start();

    // Particle animations
    particles.forEach((particle, index) => {
      const angle = (index / 12) * 2 * Math.PI;
      const delay = 500 + index * 100;
      const distance = 80 + Math.random() * 40;

      setTimeout(() => {
        Animated.parallel([
          Animated.timing(particle.opacity, {
            toValue: 1,
            duration: 300,
            useNativeDriver: true,
          }),
          Animated.spring(particle.scale, {
            toValue: 1,
            friction: 5,
            useNativeDriver: true,
          }),
          Animated.timing(particle.translateX, {
            toValue: Math.cos(angle) * distance,
            duration: 800,
            easing: Easing.out(Easing.ease),
            useNativeDriver: true,
          }),
          Animated.timing(particle.translateY, {
            toValue: Math.sin(angle) * distance,
            duration: 800,
            easing: Easing.out(Easing.ease),
            useNativeDriver: true,
          }),
        ]).start(() => {
          // Fade out particles
          Animated.timing(particle.opacity, {
            toValue: 0,
            duration: 500,
            useNativeDriver: true,
          }).start();
        });
      }, delay);
    });

    // Finish splash after animation
    const timer = setTimeout(() => {
      onFinish?.();
    }, 3000);

    return () => {
      clearTimeout(timer);
      shimmerLoop.stop();
    };
  }, []);

  const rotateInterpolate = logoRotate.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={['#fff7ed', '#fef3c7', '#fff7ed']}
        style={styles.gradient}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        {/* Background pattern */}
        <View style={styles.patternContainer}>
          {[...Array(20)].map((_, i) => (
            <View
              key={i}
              style={[
                styles.patternDot,
                {
                  top: Math.random() * height,
                  left: Math.random() * width,
                  opacity: 0.1 + Math.random() * 0.1,
                },
              ]}
            />
          ))}
        </View>

        {/* Animated ring */}
        <Animated.View
          style={[
            styles.ring,
            {
              transform: [{ scale: ringScale }],
              opacity: ringOpacity,
            },
          ]}
        />

        {/* Particles */}
        <View style={styles.particlesContainer}>
          {particles.map((particle, index) => (
            <Animated.View
              key={index}
              style={[
                styles.particle,
                {
                  transform: [
                    { translateX: particle.translateX },
                    { translateY: particle.translateY },
                    { scale: particle.scale },
                  ],
                  opacity: particle.opacity,
                },
              ]}
            >
              <Ionicons
                name={index % 3 === 0 ? 'star' : index % 3 === 1 ? 'sparkles' : 'sunny'}
                size={12}
                color="#f97316"
              />
            </Animated.View>
          ))}
        </View>

        {/* Logo */}
        <Animated.View
          style={[
            styles.logoContainer,
            {
              transform: [
                { scale: logoScale },
                { rotate: rotateInterpolate },
              ],
            },
          ]}
        >
          <LinearGradient
            colors={['#f97316', '#ef4444']}
            style={styles.logoGradient}
          >
            <View style={styles.logoInner}>
              <Text style={styles.omSymbol}>ॐ</Text>
            </View>
          </LinearGradient>

          {/* Sun rays */}
          <Animated.View style={[styles.sunRays, { transform: [{ scale: starScale }] }]}>
            {[...Array(8)].map((_, i) => (
              <View
                key={i}
                style={[
                  styles.ray,
                  { transform: [{ rotate: `${i * 45}deg` }] },
                ]}
              />
            ))}
          </Animated.View>
        </Animated.View>

        {/* Title */}
        <Animated.View
          style={[
            styles.titleContainer,
            {
              opacity: titleOpacity,
              transform: [{ translateY: titleTranslateY }],
            },
          ]}
        >
          <Text style={styles.title}>ஜோதிட AI</Text>

          {/* Shimmer effect */}
          <Animated.View
            style={[
              styles.shimmer,
              { transform: [{ translateX: shimmerPosition }] },
            ]}
          />
        </Animated.View>

        {/* Subtitle */}
        <Animated.View style={{ opacity: subtitleOpacity }}>
          <Text style={styles.subtitle}>உங்கள் வாழ்க்கை வழிகாட்டி</Text>
        </Animated.View>

        {/* Decorative stars */}
        <Animated.View style={[styles.starsContainer, { transform: [{ scale: starScale }] }]}>
          <View style={styles.starRow}>
            <Ionicons name="star" size={16} color="#fbbf24" />
            <Ionicons name="star" size={20} color="#f97316" />
            <Ionicons name="star" size={16} color="#fbbf24" />
          </View>
        </Animated.View>

        {/* Loading dots */}
        <View style={styles.loadingContainer}>
          <LoadingDots />
        </View>

        {/* Footer */}
        <View style={styles.footer}>
          <Text style={styles.footerText}>தமிழ் ஜோதிடம் • AI இயங்குகிறது</Text>
        </View>
      </LinearGradient>
    </View>
  );
}

// Animated loading dots component
const LoadingDots = () => {
  const dot1 = useRef(new Animated.Value(0)).current;
  const dot2 = useRef(new Animated.Value(0)).current;
  const dot3 = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    const animateDot = (dot, delay) => {
      return Animated.loop(
        Animated.sequence([
          Animated.delay(delay),
          Animated.timing(dot, {
            toValue: 1,
            duration: 300,
            useNativeDriver: true,
          }),
          Animated.timing(dot, {
            toValue: 0,
            duration: 300,
            useNativeDriver: true,
          }),
        ])
      );
    };

    const anim1 = animateDot(dot1, 0);
    const anim2 = animateDot(dot2, 200);
    const anim3 = animateDot(dot3, 400);

    anim1.start();
    anim2.start();
    anim3.start();

    return () => {
      anim1.stop();
      anim2.stop();
      anim3.stop();
    };
  }, []);

  const dotStyle = (animValue) => ({
    transform: [
      {
        translateY: animValue.interpolate({
          inputRange: [0, 1],
          outputRange: [0, -8],
        }),
      },
    ],
  });

  return (
    <View style={styles.dotsRow}>
      <Animated.View style={[styles.dot, dotStyle(dot1)]} />
      <Animated.View style={[styles.dot, dotStyle(dot2)]} />
      <Animated.View style={[styles.dot, dotStyle(dot3)]} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  gradient: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  patternContainer: {
    ...StyleSheet.absoluteFillObject,
  },
  patternDot: {
    position: 'absolute',
    width: 4,
    height: 4,
    borderRadius: 2,
    backgroundColor: '#f97316',
  },
  ring: {
    position: 'absolute',
    width: 150,
    height: 150,
    borderRadius: 75,
    borderWidth: 3,
    borderColor: '#f97316',
  },
  particlesContainer: {
    position: 'absolute',
    width: 200,
    height: 200,
    justifyContent: 'center',
    alignItems: 'center',
  },
  particle: {
    position: 'absolute',
  },
  logoContainer: {
    marginBottom: 30,
    alignItems: 'center',
    justifyContent: 'center',
  },
  logoGradient: {
    width: 120,
    height: 120,
    borderRadius: 60,
    padding: 4,
    shadowColor: '#f97316',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.5,
    shadowRadius: 20,
    elevation: 15,
  },
  logoInner: {
    flex: 1,
    backgroundColor: '#fff',
    borderRadius: 56,
    justifyContent: 'center',
    alignItems: 'center',
  },
  omSymbol: {
    fontSize: 56,
    color: '#f97316',
  },
  sunRays: {
    position: 'absolute',
    width: 180,
    height: 180,
  },
  ray: {
    position: 'absolute',
    width: 2,
    height: 180,
    left: 89,
    backgroundColor: '#fed7aa',
  },
  titleContainer: {
    overflow: 'hidden',
    marginBottom: 8,
  },
  title: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#9a3412',
    textShadowColor: 'rgba(249, 115, 22, 0.3)',
    textShadowOffset: { width: 0, height: 2 },
    textShadowRadius: 4,
  },
  shimmer: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    width: 50,
    backgroundColor: 'rgba(255,255,255,0.4)',
    transform: [{ skewX: '-20deg' }],
  },
  subtitle: {
    fontSize: 16,
    color: '#ea580c',
    fontWeight: '500',
    marginBottom: 20,
  },
  starsContainer: {
    marginTop: 10,
  },
  starRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  loadingContainer: {
    marginTop: 40,
  },
  dotsRow: {
    flexDirection: 'row',
    gap: 8,
  },
  dot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: '#f97316',
  },
  footer: {
    position: 'absolute',
    bottom: 50,
  },
  footerText: {
    fontSize: 12,
    color: '#9ca3af',
  },
});
