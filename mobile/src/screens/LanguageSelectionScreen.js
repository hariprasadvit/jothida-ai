import React, { useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Animated,
  Dimensions,
  Easing,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import Svg, { Path, Circle, Defs, RadialGradient, Stop, Ellipse, G } from 'react-native-svg';
import { useLanguage, languageOptions } from '../context/LanguageContext';

const { width, height } = Dimensions.get('window');

// Marigold Flower Component - More petals for realistic look
const MarigoldFlower = ({ cx, cy, size = 20, color = '#f97316' }) => (
  <G>
    {/* Outer layer - 16 petals */}
    {[...Array(16)].map((_, i) => (
      <Ellipse
        key={`outer-${i}`}
        cx={cx + (size * 0.45) * Math.cos((i * 22.5 * Math.PI) / 180)}
        cy={cy + (size * 0.45) * Math.sin((i * 22.5 * Math.PI) / 180)}
        rx={size * 0.22}
        ry={size * 0.12}
        fill={color}
        transform={`rotate(${i * 22.5 + 90}, ${cx + (size * 0.45) * Math.cos((i * 22.5 * Math.PI) / 180)}, ${cy + (size * 0.45) * Math.sin((i * 22.5 * Math.PI) / 180)})`}
      />
    ))}
    {/* Middle layer - 12 petals */}
    {[...Array(12)].map((_, i) => (
      <Ellipse
        key={`middle-${i}`}
        cx={cx + (size * 0.28) * Math.cos((i * 30 * Math.PI) / 180)}
        cy={cy + (size * 0.28) * Math.sin((i * 30 * Math.PI) / 180)}
        rx={size * 0.18}
        ry={size * 0.1}
        fill={color === '#f97316' ? '#fb923c' : '#fde047'}
        transform={`rotate(${i * 30 + 90}, ${cx + (size * 0.28) * Math.cos((i * 30 * Math.PI) / 180)}, ${cy + (size * 0.28) * Math.sin((i * 30 * Math.PI) / 180)})`}
      />
    ))}
    {/* Inner layer - 8 petals */}
    {[...Array(8)].map((_, i) => (
      <Ellipse
        key={`inner-${i}`}
        cx={cx + (size * 0.12) * Math.cos((i * 45 * Math.PI) / 180)}
        cy={cy + (size * 0.12) * Math.sin((i * 45 * Math.PI) / 180)}
        rx={size * 0.12}
        ry={size * 0.08}
        fill={color === '#f97316' ? '#fdba74' : '#fef08a'}
        transform={`rotate(${i * 45 + 90}, ${cx + (size * 0.12) * Math.cos((i * 45 * Math.PI) / 180)}, ${cy + (size * 0.12) * Math.sin((i * 45 * Math.PI) / 180)})`}
      />
    ))}
    <Circle cx={cx} cy={cy} r={size * 0.08} fill="#fbbf24" />
  </G>
);

// Rose/Red Flower Component
const RoseFlower = ({ cx, cy, size = 16 }) => (
  <G>
    {[...Array(10)].map((_, i) => (
      <Ellipse
        key={`rose-${i}`}
        cx={cx + (size * 0.35) * Math.cos((i * 36 * Math.PI) / 180)}
        cy={cy + (size * 0.35) * Math.sin((i * 36 * Math.PI) / 180)}
        rx={size * 0.25}
        ry={size * 0.15}
        fill="#dc2626"
        transform={`rotate(${i * 36 + 90}, ${cx + (size * 0.35) * Math.cos((i * 36 * Math.PI) / 180)}, ${cy + (size * 0.35) * Math.sin((i * 36 * Math.PI) / 180)})`}
      />
    ))}
    {[...Array(6)].map((_, i) => (
      <Ellipse
        key={`rose-inner-${i}`}
        cx={cx + (size * 0.15) * Math.cos((i * 60 * Math.PI) / 180)}
        cy={cy + (size * 0.15) * Math.sin((i * 60 * Math.PI) / 180)}
        rx={size * 0.15}
        ry={size * 0.1}
        fill="#ef4444"
        transform={`rotate(${i * 60 + 90}, ${cx + (size * 0.15) * Math.cos((i * 60 * Math.PI) / 180)}, ${cy + (size * 0.15) * Math.sin((i * 60 * Math.PI) / 180)})`}
      />
    ))}
    <Circle cx={cx} cy={cy} r={size * 0.08} fill="#fbbf24" />
  </G>
);

// Toran (Flower Decoration) - Multiple rows of flowers
const Toran = ({ toranWidth }) => {
  const flowerCount = Math.floor(toranWidth / 25); // Flowers instead of leaves
  const smallFlowerCount = Math.floor(toranWidth / 30);
  return (
    <Svg width={toranWidth} height={85} viewBox={`0 0 ${toranWidth} 85`}>
      {/* Rope/String */}
      <Path
        d={`M0 10 Q${toranWidth / 4} 18 ${toranWidth / 2} 12 Q${toranWidth * 3 / 4} 6 ${toranWidth} 12`}
        stroke="#92400e"
        strokeWidth="4"
        fill="none"
      />
      <Path
        d={`M0 10 Q${toranWidth / 4} 18 ${toranWidth / 2} 12 Q${toranWidth * 3 / 4} 6 ${toranWidth} 12`}
        stroke="#b45309"
        strokeWidth="2"
        fill="none"
      />

      {/* Back row of small flowers */}
      {[...Array(smallFlowerCount)].map((_, i) => {
        const x = (i / smallFlowerCount) * toranWidth + 15;
        const curveY = 12 + Math.sin((i / smallFlowerCount) * Math.PI) * 5;
        return (
          <MarigoldFlower
            key={`small-${i}`}
            cx={x}
            cy={curveY + 25}
            size={10}
            color={i % 2 === 0 ? '#fbbf24' : '#fde047'}
          />
        );
      })}

      {/* Main row of marigold flowers */}
      {[...Array(flowerCount)].map((_, i) => {
        const x = (i / flowerCount) * toranWidth + 12;
        const curveY = 12 + Math.sin((i / flowerCount) * Math.PI) * 6;
        return (
          <MarigoldFlower
            key={`main-${i}`}
            cx={x}
            cy={curveY + 40}
            size={18}
            color={i % 3 === 0 ? '#f97316' : i % 3 === 1 ? '#fb923c' : '#fbbf24'}
          />
        );
      })}

      {/* Front row alternating with roses */}
      {[...Array(Math.floor(flowerCount * 0.7))].map((_, i) => {
        const x = (i / (flowerCount * 0.7)) * toranWidth + 20;
        const curveY = 12 + Math.sin((i / (flowerCount * 0.7)) * Math.PI) * 6;
        if (i % 3 === 0) {
          return (
            <RoseFlower
              key={`front-${i}`}
              cx={x}
              cy={curveY + 55}
              size={14}
            />
          );
        }
        return (
          <MarigoldFlower
            key={`front-${i}`}
            cx={x}
            cy={curveY + 55}
            size={15}
            color={i % 2 === 0 ? '#f97316' : '#fdba74'}
          />
        );
      })}

      {/* Top accent flowers */}
      {[...Array(6)].map((_, i) => {
        const x = 30 + (i * (toranWidth - 60) / 5);
        return (
          <MarigoldFlower
            key={`toran-flower-${i}`}
            cx={x}
            cy={15}
            size={13}
            color={i % 2 === 0 ? '#f97316' : '#fbbf24'}
          />
        );
      })}
    </Svg>
  );
};

// Hanging Marigold String - Dense flower garland
const HangingMarigold = ({ length }) => {
  const flowerCount = Math.floor(length / 16); // More flowers, closer together
  return (
    <Svg width={50} height={length} viewBox={`0 0 50 ${length}`}>
      {/* Dual strings for realistic look */}
      <Path d={`M20 0 L20 ${length}`} stroke="#84cc16" strokeWidth="2.5" />
      <Path d={`M30 0 L30 ${length}`} stroke="#84cc16" strokeWidth="2.5" />
      <Path d={`M25 0 L25 ${length}`} stroke="#65a30d" strokeWidth="1.5" />

      {/* Small decorative petals between flowers */}
      {[...Array(Math.floor(flowerCount * 2))].map((_, i) => (
        <G key={`petal-${i}`}>
          <Ellipse
            cx={18}
            cy={5 + i * 8}
            rx={3}
            ry={5}
            fill="#fbbf24"
            opacity="0.6"
          />
          <Ellipse
            cx={32}
            cy={5 + i * 8}
            rx={3}
            ry={5}
            fill="#fb923c"
            opacity="0.6"
          />
        </G>
      ))}

      {/* Dense alternating marigold and rose flowers */}
      {[...Array(flowerCount)].map((_, i) => {
        const yPos = 8 + i * 16;
        if (i % 4 === 3) {
          return (
            <RoseFlower
              key={`flower-${i}`}
              cx={25}
              cy={yPos}
              size={15}
            />
          );
        }
        return (
          <MarigoldFlower
            key={`flower-${i}`}
            cx={25}
            cy={yPos}
            size={17}
            color={i % 3 === 0 ? '#f97316' : i % 3 === 1 ? '#fbbf24' : '#fb923c'}
          />
        );
      })}
    </Svg>
  );
};

// Diya Glow Component - for auspicious lighting effect
const DiyaGlow = () => (
  <Svg width={140} height={140} viewBox="0 0 140 140">
    <Defs>
      <RadialGradient id="diyaGlow" cx="50%" cy="50%" r="50%">
        <Stop offset="0%" stopColor="#fbbf24" stopOpacity="0.8" />
        <Stop offset="30%" stopColor="#f97316" stopOpacity="0.5" />
        <Stop offset="60%" stopColor="#ea580c" stopOpacity="0.3" />
        <Stop offset="100%" stopColor="#ea580c" stopOpacity="0" />
      </RadialGradient>
      <RadialGradient id="innerGlow" cx="50%" cy="50%" r="50%">
        <Stop offset="0%" stopColor="#fef3c7" stopOpacity="1" />
        <Stop offset="50%" stopColor="#fbbf24" stopOpacity="0.6" />
        <Stop offset="100%" stopColor="#f97316" stopOpacity="0" />
      </RadialGradient>
    </Defs>
    {/* Outer glow */}
    <Circle cx="70" cy="70" r="70" fill="url(#diyaGlow)" />
    {/* Middle glow */}
    <Circle cx="70" cy="70" r="50" fill="url(#innerGlow)" />
    {/* Light rays */}
    {[...Array(12)].map((_, i) => (
      <Path
        key={`ray-${i}`}
        d={`M70 70 L${70 + 60 * Math.cos((i * 30 * Math.PI) / 180)} ${70 + 60 * Math.sin((i * 30 * Math.PI) / 180)}`}
        stroke="#fbbf24"
        strokeWidth="1"
        opacity="0.3"
      />
    ))}
  </Svg>
);

export default function LanguageSelectionScreen({ onLanguageSelected }) {
  const { changeLanguage, language } = useLanguage();
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(50)).current;
  const buttonAnims = useRef(languageOptions.map(() => new Animated.Value(0))).current;
  const garlandAnim = useRef(new Animated.Value(-50)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 600,
        useNativeDriver: true,
      }),
      Animated.timing(slideAnim, {
        toValue: 0,
        duration: 600,
        easing: Easing.out(Easing.ease),
        useNativeDriver: true,
      }),
      Animated.spring(garlandAnim, {
        toValue: 0,
        friction: 8,
        tension: 40,
        useNativeDriver: true,
      }),
    ]).start();

    buttonAnims.forEach((anim, index) => {
      Animated.timing(anim, {
        toValue: 1,
        duration: 400,
        delay: 400 + index * 150,
        easing: Easing.out(Easing.ease),
        useNativeDriver: true,
      }).start();
    });
  }, []);

  const handleLanguageSelect = async (langCode) => {
    await changeLanguage(langCode);
    onLanguageSelected?.();
  };

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={['#fef3c7', '#fed7aa', '#fdba74', '#fb923c']}
        style={styles.gradient}
        start={{ x: 0.5, y: 0 }}
        end={{ x: 0.5, y: 1 }}
        locations={[0, 0.3, 0.6, 1]}
      >
        {/* Top Mango Toran */}
        <Animated.View
          style={[
            styles.toranContainer,
            {
              opacity: fadeAnim,
              transform: [{ translateY: garlandAnim }]
            }
          ]}
        >
          <Toran toranWidth={width} />
        </Animated.View>

        {/* Left hanging garlands */}
        <Animated.View
          style={[
            styles.leftGarland,
            {
              opacity: fadeAnim,
              transform: [{ translateY: garlandAnim }]
            }
          ]}
        >
          <HangingMarigold length={height * 0.25} />
        </Animated.View>

        {/* Right hanging garlands */}
        <Animated.View
          style={[
            styles.rightGarland,
            {
              opacity: fadeAnim,
              transform: [{ translateY: garlandAnim }]
            }
          ]}
        >
          <HangingMarigold length={height * 0.25} />
        </Animated.View>

        {/* Main Content */}
        <Animated.View
          style={[
            styles.content,
            {
              opacity: fadeAnim,
              transform: [{ translateY: slideAnim }],
            },
          ]}
        >
          {/* Logo with Diya Glow */}
          <View style={styles.logoWrapper}>
            {/* Diya glow behind logo */}
            <View style={styles.diyaGlowContainer}>
              <DiyaGlow />
            </View>
            {/* Logo */}
            <View style={styles.logoContainer}>
              <LinearGradient
                colors={['#f97316', '#ea580c']}
                style={styles.logoGradient}
              >
                <Svg width={48} height={48} viewBox="0 0 100 100">
                  <Path
                    d="M50 5 L55 40 L90 30 L60 50 L90 70 L55 60 L50 95 L45 60 L10 70 L40 50 L10 30 L45 40 Z"
                    fill="#fff"
                  />
                  <Circle cx="50" cy="50" r="10" fill="#f97316" />
                </Svg>
              </LinearGradient>
            </View>
          </View>

          <Text style={styles.brandName}>jothida.ai</Text>

          {/* Welcome text */}
          <View style={styles.welcomeContainer}>
            <Text style={styles.welcomeText}>Welcome</Text>
            <Text style={styles.welcomeTextTamil}>வரவேற்கிறோம்</Text>
            <Text style={styles.welcomeTextKannada}>ಸ್ವಾಗತ</Text>
          </View>

          <Text style={styles.selectLanguageText}>Select your language</Text>
          <Text style={styles.selectLanguageSubtext}>மொழியைத் தேர்வு செய்யவும்</Text>

          {/* Language Options */}
          <View style={styles.languageOptions}>
            {languageOptions.map((lang, index) => (
              <Animated.View
                key={lang.code}
                style={{
                  opacity: buttonAnims[index],
                  transform: [
                    {
                      translateY: buttonAnims[index].interpolate({
                        inputRange: [0, 1],
                        outputRange: [30, 0],
                      }),
                    },
                  ],
                }}
              >
                <TouchableOpacity
                  style={[
                    styles.languageButton,
                    language === lang.code && styles.languageButtonSelected,
                  ]}
                  onPress={() => handleLanguageSelect(lang.code)}
                  activeOpacity={0.8}
                >
                  <LinearGradient
                    colors={
                      language === lang.code
                        ? ['#f97316', '#ea580c']
                        : ['#fff', '#fef3c7']
                    }
                    style={styles.languageButtonGradient}
                  >
                    <View style={styles.languageTextContainer}>
                      <Text
                        style={[
                          styles.languageName,
                          language === lang.code && styles.languageNameSelected,
                        ]}
                      >
                        {lang.name}
                      </Text>
                      {lang.name !== lang.nameEn && (
                        <Text
                          style={[
                            styles.languageNameEn,
                            language === lang.code && styles.languageNameEnSelected,
                          ]}
                        >
                          {lang.nameEn}
                        </Text>
                      )}
                    </View>
                    {language === lang.code && (
                      <Ionicons
                        name="checkmark-circle"
                        size={24}
                        color="#fff"
                        style={styles.checkIcon}
                      />
                    )}
                  </LinearGradient>
                </TouchableOpacity>
              </Animated.View>
            ))}
          </View>

          {/* Continue Button */}
          <Animated.View
            style={{
              opacity: buttonAnims[buttonAnims.length - 1],
              marginTop: 30,
            }}
          >
            <TouchableOpacity
              style={styles.continueButton}
              onPress={() => onLanguageSelected?.()}
              activeOpacity={0.8}
            >
              <LinearGradient
                colors={['#7c2d12', '#9a3412']}
                style={styles.continueGradient}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 0 }}
              >
                <Text style={styles.continueText}>Continue</Text>
                <Ionicons name="arrow-forward" size={20} color="#fff" />
              </LinearGradient>
            </TouchableOpacity>
          </Animated.View>
        </Animated.View>
      </LinearGradient>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  gradient: {
    flex: 1,
    alignItems: 'center',
  },
  toranContainer: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    zIndex: 10,
  },
  leftGarland: {
    position: 'absolute',
    top: 55,
    left: 15,
    zIndex: 5,
  },
  rightGarland: {
    position: 'absolute',
    top: 55,
    right: 15,
    zIndex: 5,
  },
  content: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 30,
    paddingTop: 60,
  },
  logoWrapper: {
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 5,
  },
  diyaGlowContainer: {
    position: 'absolute',
    top: -25,
    left: -25,
  },
  logoContainer: {
    shadowColor: '#f97316',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.8,
    shadowRadius: 20,
    elevation: 15,
  },
  logoGradient: {
    width: 90,
    height: 90,
    borderRadius: 45,
    alignItems: 'center',
    justifyContent: 'center',
  },
  brandName: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#7c2d12',
    marginBottom: 20,
    letterSpacing: 1,
  },
  welcomeContainer: {
    alignItems: 'center',
    marginBottom: 20,
  },
  welcomeText: {
    fontSize: 24,
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: 4,
  },
  welcomeTextTamil: {
    fontSize: 20,
    color: '#9a3412',
    marginBottom: 2,
  },
  welcomeTextKannada: {
    fontSize: 18,
    color: '#b45309',
  },
  selectLanguageText: {
    fontSize: 16,
    color: '#4b5563',
    marginBottom: 4,
  },
  selectLanguageSubtext: {
    fontSize: 14,
    color: '#6b7280',
    marginBottom: 25,
  },
  languageOptions: {
    width: '100%',
    maxWidth: 500,
    gap: 14,
  },
  languageButton: {
    borderRadius: 16,
    overflow: 'hidden',
    borderWidth: 2,
    borderColor: '#fed7aa',
    minWidth: '100%',
  },
  languageButtonSelected: {
    borderColor: '#f97316',
  },
  languageButtonGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: 18,
    paddingHorizontal: 28,
  },
  languageTextContainer: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  languageName: {
    fontSize: 22,
    fontWeight: '600',
    color: '#1f2937',
  },
  languageNameSelected: {
    color: '#fff',
  },
  languageNameEn: {
    fontSize: 14,
    color: '#6b7280',
  },
  languageNameEnSelected: {
    color: '#fef3c7',
  },
  checkIcon: {
    marginLeft: 10,
  },
  continueButton: {
    borderRadius: 16,
    overflow: 'hidden',
    shadowColor: '#7c2d12',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 5,
  },
  continueGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 16,
    paddingHorizontal: 50,
    gap: 10,
  },
  continueText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
  },
});
