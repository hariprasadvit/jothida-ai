import React, { useState, useRef, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Dimensions,
  TouchableOpacity,
  Animated,
  FlatList,
  Platform,
  Easing,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import Svg, { Path, Circle, Ellipse, G, Defs, RadialGradient, Stop } from 'react-native-svg';
import * as SecureStore from 'expo-secure-store';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useLanguage } from '../context/LanguageContext';

// Storage helper for web compatibility
const setStorageItem = async (key, value) => {
  if (Platform.OS === 'web') {
    return AsyncStorage.setItem(key, value);
  }
  return SecureStore.setItemAsync(key, value);
};

const { width, height } = Dimensions.get('window');

// Floating Particle Component
const FloatingParticle = ({ delay = 0, duration = 3000, x, color = '#fbbf24' }) => {
  const translateY = useRef(new Animated.Value(0)).current;
  const opacity = useRef(new Animated.Value(0)).current;
  const scale = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    const animate = () => {
      Animated.loop(
        Animated.parallel([
          Animated.sequence([
            Animated.timing(opacity, {
              toValue: 1,
              duration: 800,
              delay,
              useNativeDriver: true,
            }),
            Animated.timing(opacity, {
              toValue: 0,
              duration: 800,
              delay: duration - 1600,
              useNativeDriver: true,
            }),
          ]),
          Animated.timing(translateY, {
            toValue: -height * 0.8,
            duration,
            delay,
            easing: Easing.linear,
            useNativeDriver: true,
          }),
          Animated.sequence([
            Animated.timing(scale, {
              toValue: 1,
              duration: 400,
              delay,
              useNativeDriver: true,
            }),
            Animated.timing(scale, {
              toValue: 0.5,
              duration: 400,
              delay: duration - 800,
              useNativeDriver: true,
            }),
          ]),
        ])
      ).start();
    };
    animate();
  }, []);

  return (
    <Animated.View
      style={[
        styles.particle,
        {
          left: x,
          opacity,
          transform: [{ translateY }, { scale }],
        },
      ]}
    >
      <View style={[styles.particleDot, { backgroundColor: color }]} />
    </Animated.View>
  );
};

// Shimmer Effect Component
const ShimmerEffect = ({ colors = ['transparent', 'rgba(255,255,255,0.3)', 'transparent'] }) => {
  const shimmerAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.loop(
      Animated.timing(shimmerAnim, {
        toValue: 1,
        duration: 2000,
        easing: Easing.linear,
        useNativeDriver: true,
      })
    ).start();
  }, []);

  const translateX = shimmerAnim.interpolate({
    inputRange: [0, 1],
    outputRange: [-width, width],
  });

  return (
    <Animated.View
      pointerEvents="none"
      style={[
        styles.shimmerContainer,
        { transform: [{ translateX }] },
      ]}
    >
      <LinearGradient
        colors={colors}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 0 }}
        style={styles.shimmerGradient}
      />
    </Animated.View>
  );
};

// Pulsing Glow Component
const PulsingGlow = ({ size = 140, color = '#f97316' }) => {
  const pulseAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 2000,
          easing: Easing.inOut(Easing.ease),
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 0,
          duration: 2000,
          easing: Easing.inOut(Easing.ease),
          useNativeDriver: true,
        }),
      ])
    ).start();
  }, []);

  const scale = pulseAnim.interpolate({
    inputRange: [0, 1],
    outputRange: [1, 1.15],
  });

  const opacity = pulseAnim.interpolate({
    inputRange: [0, 1],
    outputRange: [0.3, 0.6],
  });

  return (
    <Animated.View
      style={[
        styles.pulsingGlow,
        {
          width: size,
          height: size,
          opacity,
          transform: [{ scale }],
        },
      ]}
    >
      <Svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <Defs>
          <RadialGradient id="glowGradient" cx="50%" cy="50%" r="50%">
            <Stop offset="0%" stopColor={color} stopOpacity="0.8" />
            <Stop offset="50%" stopColor={color} stopOpacity="0.4" />
            <Stop offset="100%" stopColor={color} stopOpacity="0" />
          </RadialGradient>
        </Defs>
        <Circle cx={size / 2} cy={size / 2} r={size / 2} fill="url(#glowGradient)" />
      </Svg>
    </Animated.View>
  );
};

// Onboarding content by language
const getOnboardingData = (language) => {
  if (language === 'en') {
    return [
      {
        id: '1',
        icon: 'sunny',
        iconSecondary: 'moon',
        title: 'Jothida AI',
        subtitle: 'Your Life Guide',
        description: 'We combine the ancient wisdom of Tamil astrology with modern AI technology to provide you accurate predictions.',
        gradient: ['#f97316', '#ef4444'],
        features: ['Accurate Rasi Predictions', 'AI Analysis', 'Full English Support'],
      },
      {
        id: '2',
        icon: 'grid',
        iconSecondary: 'star',
        title: 'Rasi & Navamsa Chart',
        subtitle: 'Detailed Horoscope Analysis',
        description: 'We calculate accurate Rasi chart, Navamsa chart, and planetary positions based on your birth time and place.',
        gradient: ['#8b5cf6', '#6366f1'],
        features: ['Rasi Chart', 'Navamsa Chart', 'Planet Positions'],
      },
      {
        id: '3',
        icon: 'heart',
        iconSecondary: 'people',
        title: 'Marriage Matching',
        subtitle: '10 Porutham Analysis',
        description: 'We analyze all 10 poruthams including Dinam, Ganam, Mahendram, Stree Deergham, Yoni, Rasi, Rasi Athipathi, Vasiyam, Rajju, and Vedai.',
        gradient: ['#ec4899', '#f43f5e'],
        features: ['10 Porutham', 'AI Recommendation', 'Remedies'],
      },
      {
        id: '4',
        icon: 'calendar',
        iconSecondary: 'time',
        title: 'Muhurtham Finder',
        subtitle: 'Auspicious Time Selection',
        description: 'Find the right muhurtham time for important events like marriage, housewarming, business start, and travel.',
        gradient: ['#10b981', '#14b8a6'],
        features: ['Auspicious Time', 'Rahu Kalam', 'Panchang'],
      },
      {
        id: '5',
        icon: 'chatbubbles',
        iconSecondary: 'sparkles',
        title: 'AI Astrology Assistant',
        subtitle: 'Ask in Your Language',
        description: 'Ask any question about your horoscope. Our AI will provide detailed answers in your preferred language.',
        gradient: ['#f97316', '#fbbf24'],
        features: ['24/7 Support', 'Multi-language', 'Personalized Advice'],
      },
    ];
  } else if (language === 'kn') {
    return [
      {
        id: '1',
        icon: 'sunny',
        iconSecondary: 'moon',
        title: 'ಜ್ಯೋತಿಷ AI',
        subtitle: 'ನಿಮ್ಮ ಜೀವನ ಮಾರ್ಗದರ್ಶಿ',
        description: 'ತಮಿಳು ಜ್ಯೋತಿಷ್ಯದ ಪ್ರಾಚೀನ ಜ್ಞಾನವನ್ನು ಆಧುನಿಕ AI ತಂತ್ರಜ್ಞಾನದೊಂದಿಗೆ ಸಂಯೋಜಿಸಿ ನಿಖರ ಫಲಗಳನ್ನು ನೀಡುತ್ತೇವೆ.',
        gradient: ['#f97316', '#ef4444'],
        features: ['ನಿಖರ ರಾಶಿ ಫಲ', 'AI ವಿಶ್ಲೇಷಣೆ', 'ಕನ್ನಡದಲ್ಲಿ ಬೆಂಬಲ'],
      },
      {
        id: '2',
        icon: 'grid',
        iconSecondary: 'star',
        title: 'ರಾಶಿ & ನವಾಂಶ ಚಕ್ರ',
        subtitle: 'ವಿವರವಾದ ಜಾತಕ ವಿಶ್ಲೇಷಣೆ',
        description: 'ನಿಮ್ಮ ಹುಟ್ಟಿದ ಸಮಯ ಮತ್ತು ಸ್ಥಳದ ಆಧಾರದ ಮೇಲೆ ನಿಖರ ರಾಶಿ ಚಕ್ರ, ನವಾಂಶ ಚಕ್ರ, ಮತ್ತು ಗ್ರಹ ಸ್ಥಾನಗಳನ್ನು ಲೆಕ್ಕಾಚಾರ ಮಾಡುತ್ತೇವೆ.',
        gradient: ['#8b5cf6', '#6366f1'],
        features: ['ರಾಶಿ ಚಕ್ರ', 'ನವಾಂಶ ಚಕ್ರ', 'ಗ್ರಹ ಸ್ಥಾನಗಳು'],
      },
      {
        id: '3',
        icon: 'heart',
        iconSecondary: 'people',
        title: 'ವಿವಾಹ ಹೊಂದಾಣಿಕೆ',
        subtitle: '10 ಪೊರುತ್ತಂ ವಿಶ್ಲೇಷಣೆ',
        description: 'ದಿನಂ, ಗಣಂ, ಮಹೇಂದ್ರಂ, ಸ್ತ್ರೀ ದೀರ್ಘಂ, ಯೋನಿ, ರಾಶಿ, ರಾಶಿ ಅಧಿಪತಿ, ವಶ್ಯಂ, ರಜ್ಜು, ವೇದೈ ಎಲ್ಲಾ 10 ಪೊರುತ್ತಂಗಳನ್ನು ವಿಶ್ಲೇಷಿಸುತ್ತೇವೆ.',
        gradient: ['#ec4899', '#f43f5e'],
        features: ['10 ಪೊರುತ್ತಂ', 'AI ಶಿಫಾರಸು', 'ಪರಿಹಾರಗಳು'],
      },
      {
        id: '4',
        icon: 'calendar',
        iconSecondary: 'time',
        title: 'ಮುಹೂರ್ತ ಹುಡುಕುವಿಕೆ',
        subtitle: 'ಶುಭ ಸಮಯ ಆಯ್ಕೆ',
        description: 'ವಿವಾಹ, ಗೃಹಪ್ರವೇಶ, ವ್ಯಾಪಾರ ಆರಂಭ, ಪ್ರಯಾಣ ಮುಂತಾದ ಮುಖ್ಯ ಘಟನೆಗಳಿಗೆ ಸರಿಯಾದ ಮುಹೂರ್ತ ಸಮಯವನ್ನು ಕಂಡುಹಿಡಿಯಿರಿ.',
        gradient: ['#10b981', '#14b8a6'],
        features: ['ಶುಭ ಸಮಯ', 'ರಾಹು ಕಾಲ', 'ಪಂಚಾಂಗ'],
      },
      {
        id: '5',
        icon: 'chatbubbles',
        iconSecondary: 'sparkles',
        title: 'AI ಜ್ಯೋತಿಷ್ಯ ಸಹಾಯಕ',
        subtitle: 'ಕನ್ನಡದಲ್ಲಿ ಕೇಳಿ',
        description: 'ನಿಮ್ಮ ಜಾತಕದ ಬಗ್ಗೆ ಯಾವುದೇ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ. ನಮ್ಮ AI ನಿಮಗೆ ವಿವರವಾದ ಉತ್ತರಗಳನ್ನು ನೀಡುತ್ತದೆ.',
        gradient: ['#f97316', '#fbbf24'],
        features: ['24/7 ಬೆಂಬಲ', 'ಕನ್ನಡದಲ್ಲಿ ಉತ್ತರ', 'ವೈಯಕ್ತಿಕ ಸಲಹೆ'],
      },
    ];
  } else {
    // Tamil (default)
    return [
      {
        id: '1',
        icon: 'sunny',
        iconSecondary: 'moon',
        title: 'ஜோதிட AI',
        subtitle: 'உங்கள் வாழ்க்கை வழிகாட்டி',
        description: 'தமிழ் ஜோதிடத்தின் பண்டைய ஞானத்தை நவீன AI தொழில்நுட்பத்துடன் இணைத்து உங்களுக்கு துல்லியமான பலன்களை வழங்குகிறோம்.',
        gradient: ['#f97316', '#ef4444'],
        features: ['துல்லியமான ராசி பலன்', 'AI பகுப்பாய்வு', 'தமிழில் முழு ஆதரவு'],
      },
      {
        id: '2',
        icon: 'grid',
        iconSecondary: 'star',
        title: 'ராசி & நவாம்ச கட்டம்',
        subtitle: 'விரிவான ஜாதக பகுப்பாய்வு',
        description: 'உங்கள் பிறந்த நேரம் மற்றும் இடத்தின் அடிப்படையில் துல்லியமான ராசி கட்டம், நவாம்ச கட்டம், மற்றும் கிரக நிலைகளை கணக்கிடுகிறோம்.',
        gradient: ['#8b5cf6', '#6366f1'],
        features: ['ராசி கட்டம்', 'நவாம்ச கட்டம்', 'கிரக நிலைகள்'],
      },
      {
        id: '3',
        icon: 'heart',
        iconSecondary: 'people',
        title: 'திருமண பொருத்தம்',
        subtitle: '10 பொருத்த பகுப்பாய்வு',
        description: 'தினம், கணம், மகேந்திரம், ஸ்திரி தீர்க்கம், யோனி, ராசி, ராசி அதிபதி, வசியம், ரஜ்ஜூ, வேதை ஆகிய 10 பொருத்தங்களை பகுப்பாய்வு செய்கிறோம்.',
        gradient: ['#ec4899', '#f43f5e'],
        features: ['10 பொருத்தம்', 'AI பரிந்துரை', 'பரிகாரங்கள்'],
      },
      {
        id: '4',
        icon: 'calendar',
        iconSecondary: 'time',
        title: 'முகூர்த்தம் கண்டறிதல்',
        subtitle: 'சுப நேரம் தேர்வு',
        description: 'திருமணம், கிரக பிரவேசம், தொழில் ஆரம்பம், பயணம் போன்ற முக்கிய நிகழ்வுகளுக்கு சரியான முகூர்த்த நேரத்தை கண்டறியுங்கள்.',
        gradient: ['#10b981', '#14b8a6'],
        features: ['சுப நேரம்', 'ராகு காலம்', 'பஞ்சாங்கம்'],
      },
      {
        id: '5',
        icon: 'chatbubbles',
        iconSecondary: 'sparkles',
        title: 'AI ஜோதிட உதவியாளர்',
        subtitle: 'தமிழில் கேளுங்கள்',
        description: 'உங்கள் ஜாதகம் பற்றிய எந்த கேள்வியையும் தமிழில் கேளுங்கள். எங்கள் AI உங்களுக்கு விரிவான பதில்களை தரும்.',
        gradient: ['#f97316', '#fbbf24'],
        features: ['24/7 ஆதரவு', 'தமிழில் பதில்', 'தனிப்பயன் ஆலோசனை'],
      },
    ];
  }
};

const OnboardingItem = ({ item, index, scrollX }) => {
  const inputRange = [(index - 1) * width, index * width, (index + 1) * width];
  const iconPulse = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(iconPulse, {
          toValue: 1.05,
          duration: 1500,
          easing: Easing.inOut(Easing.ease),
          useNativeDriver: true,
        }),
        Animated.timing(iconPulse, {
          toValue: 1,
          duration: 1500,
          easing: Easing.inOut(Easing.ease),
          useNativeDriver: true,
        }),
      ])
    ).start();
  }, []);

  const scale = scrollX.interpolate({
    inputRange,
    outputRange: [0.85, 1, 0.85],
    extrapolate: 'clamp',
  });

  const opacity = scrollX.interpolate({
    inputRange,
    outputRange: [0.5, 1, 0.5],
    extrapolate: 'clamp',
  });

  const translateY = scrollX.interpolate({
    inputRange,
    outputRange: [60, 0, 60],
    extrapolate: 'clamp',
  });

  const iconRotate = scrollX.interpolate({
    inputRange,
    outputRange: ['30deg', '0deg', '-30deg'],
    extrapolate: 'clamp',
  });

  return (
    <View style={styles.slide}>
      <Animated.View style={[styles.content, { opacity, transform: [{ scale }, { translateY }] }]}>
        {/* Icon Container with Glow */}
        <View style={styles.iconWrapper}>
          <PulsingGlow size={180} color={item.gradient[0]} />
          <Animated.View 
            style={[
              styles.iconContainer, 
              { 
                transform: [
                  { rotate: iconRotate },
                  { scale: iconPulse }
                ] 
              }
            ]}
          >
            <LinearGradient colors={item.gradient} style={styles.iconGradient}>
              <ShimmerEffect />
              <Ionicons name={item.icon} size={70} color="#fff" />
            </LinearGradient>
            <View style={styles.iconSecondary}>
              <Ionicons name={item.iconSecondary} size={28} color={item.gradient[0]} />
            </View>
          </Animated.View>
        </View>

        {/* Text Content */}
        <Text style={styles.title}>{item.title}</Text>
        <Text style={[styles.subtitle, { color: item.gradient[0] }]}>{item.subtitle}</Text>
        <Text style={styles.description}>{item.description}</Text>

        {/* Features */}
        <View style={styles.featuresContainer}>
          {item.features.map((feature, i) => (
            <View key={i} style={[styles.featureBadge, { borderColor: item.gradient[0] }]}>
              <Ionicons name="checkmark-circle" size={16} color={item.gradient[0]} />
              <Text style={[styles.featureText, { color: item.gradient[0] }]}>{feature}</Text>
            </View>
          ))}
        </View>
      </Animated.View>
    </View>
  );
};

const Paginator = ({ data, scrollX }) => {
  return (
    <View style={styles.paginatorContainer}>
      {data.map((item, index) => {
        const inputRange = [(index - 1) * width, index * width, (index + 1) * width];

        const dotWidth = scrollX.interpolate({
          inputRange,
          outputRange: [10, 32, 10],
          extrapolate: 'clamp',
        });

        const opacity = scrollX.interpolate({
          inputRange,
          outputRange: [0.4, 1, 0.4],
          extrapolate: 'clamp',
        });

        return (
          <Animated.View
            key={index}
            style={[
              styles.dot,
              { 
                width: dotWidth, 
                opacity,
              },
            ]}
          >
            <LinearGradient
              colors={item.gradient}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 0 }}
              style={styles.dotGradient}
            />
          </Animated.View>
        );
      })}
    </View>
  );
};

export default function OnboardingScreen({ navigation }) {
  const { language, isLoading } = useLanguage();
  const onboardingData = React.useMemo(() => getOnboardingData(language), [language]);

  const [currentIndex, setCurrentIndex] = useState(0);
  const scrollX = useRef(new Animated.Value(0)).current;
  const flatListRef = useRef(null);
  const insets = useSafeAreaInsets();

  const buttonScale = useRef(new Animated.Value(1)).current;
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideUpAnim = useRef(new Animated.Value(30)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 1000,
        easing: Easing.out(Easing.ease),
        useNativeDriver: true,
      }),
      Animated.spring(slideUpAnim, {
        toValue: 0,
        friction: 8,
        tension: 40,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  if (isLoading) {
    return (
      <View style={styles.container}>
        <LinearGradient colors={['#fff7ed', '#ffffff', '#fff7ed']} style={styles.gradient}>
          <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
            <Text>Loading...</Text>
          </View>
        </LinearGradient>
      </View>
    );
  }

  const viewableItemsChanged = useRef(({ viewableItems }) => {
    if (viewableItems.length > 0) {
      setCurrentIndex(viewableItems[0].index);
    }
  }).current;

  const viewConfig = useRef({ viewAreaCoveragePercentThreshold: 50 }).current;

  const handleNext = () => {
    console.log('Next button pressed, currentIndex:', currentIndex);

    Animated.sequence([
      Animated.timing(buttonScale, {
        toValue: 0.9,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.spring(buttonScale, {
        toValue: 1,
        friction: 4,
        useNativeDriver: true,
      }),
    ]).start();

    if (currentIndex < onboardingData.length - 1) {
      try {
        // Safer scrolling with error handling
        const nextIndex = currentIndex + 1;
        console.log('Scrolling to index:', nextIndex);

        if (flatListRef.current) {
          flatListRef.current.scrollToIndex({
            index: nextIndex,
            animated: true,
            viewPosition: 0.5
          });
        }
      } catch (error) {
        console.error('Error scrolling to next slide:', error);
        // Fallback: manually update index
        setCurrentIndex(currentIndex + 1);
      }
    } else {
      console.log('Last slide, completing onboarding');
      completeOnboarding();
    }
  };

  const handleSkip = () => {
    completeOnboarding();
  };

  const completeOnboarding = async () => {
    console.log('Completing onboarding, navigation object:', navigation);
    try {
      await setStorageItem('onboardingComplete', 'true');
      console.log('Onboarding status saved');

      Animated.sequence([
        Animated.timing(fadeAnim, {
          toValue: 0,
          duration: 300,
          useNativeDriver: true,
        }),
      ]).start(() => {
        console.log('Animation complete, navigating to Login');
        if (navigation && navigation.replace) {
          navigation.replace('Login');
        } else {
          console.error('Navigation object not available or missing replace method');
        }
      });
    } catch (error) {
      console.error('Error saving onboarding status:', error);
      if (navigation && navigation.replace) {
        navigation.replace('Login');
      }
    }
  };

  const handlePressIn = () => {
    Animated.spring(buttonScale, {
      toValue: 0.96,
      friction: 4,
      useNativeDriver: true,
    }).start();
  };

  const handlePressOut = () => {
    Animated.spring(buttonScale, {
      toValue: 1,
      friction: 3,
      useNativeDriver: true,
    }).start();
  };

  const isLastSlide = currentIndex === onboardingData.length - 1;
  const currentItem = onboardingData[currentIndex];

  const skipText = language === 'en' ? 'Skip' : language === 'kn' ? 'ಬಿಡಿ' : 'தவிர்';
  const nextText = language === 'en' ? 'Next' : language === 'kn' ? 'ಮುಂದೆ' : 'அடுத்து';
  const startText = language === 'en' ? 'Get Started' : language === 'kn' ? 'ಪ್ರಾರಂಭಿಸಿ' : 'தொடங்கு';

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={['#fff7ed', '#fef3c7', '#fed7aa']}
        style={styles.gradient}
      >
        {/* Floating Particles */}
        {[...Array(8)].map((_, i) => (
          <FloatingParticle
            key={i}
            delay={i * 400}
            duration={3000 + i * 200}
            x={Math.random() * width}
            color={i % 2 === 0 ? '#fbbf24' : '#f97316'}
          />
        ))}

        {/* Header */}
        <Animated.View 
          style={[
            styles.header, 
            { 
              opacity: fadeAnim, 
              paddingTop: insets.top + 10,
              transform: [{ translateY: slideUpAnim }]
            }
          ]}
        >
          <View style={styles.logoContainer}>
            <View style={styles.logoIcon}>
              <Svg width={28} height={28} viewBox="0 0 100 100">
                <Path
                  d="M50 5 L55 40 L90 30 L60 50 L90 70 L55 60 L50 95 L45 60 L10 70 L40 50 L10 30 L45 40 Z"
                  fill="#f97316"
                />
                <Circle cx="50" cy="50" r="10" fill="#fff7ed" />
              </Svg>
            </View>
            <Text style={styles.logoText}>jothida.ai</Text>
          </View>
          {!isLastSlide && (
            <TouchableOpacity 
              onPress={handleSkip} 
              style={styles.skipBtn}
              activeOpacity={0.7}
            >
              <Text style={styles.skipText}>{skipText}</Text>
              <Ionicons name="chevron-forward" size={16} color="#6b7280" />
            </TouchableOpacity>
          )}
        </Animated.View>

        {/* Slides */}
        <FlatList
          key={language}
          ref={flatListRef}
          data={onboardingData}
          extraData={language}
          renderItem={({ item, index }) => (
            <OnboardingItem item={item} index={index} scrollX={scrollX} />
          )}
          horizontal
          showsHorizontalScrollIndicator={false}
          pagingEnabled
          bounces={false}
          keyExtractor={(item) => `${language}-${item.id}`}
          onScroll={Animated.event(
            [{ nativeEvent: { contentOffset: { x: scrollX } } }],
            { useNativeDriver: false }
          )}
          onViewableItemsChanged={viewableItemsChanged}
          viewabilityConfig={viewConfig}
          scrollEventThrottle={16}
          decelerationRate="fast"
          onScrollToIndexFailed={(info) => {
            console.warn('Scroll to index failed:', info);
            // Fallback: scroll to offset
            const wait = new Promise(resolve => setTimeout(resolve, 100));
            wait.then(() => {
              flatListRef.current?.scrollToOffset({
                offset: info.index * width,
                animated: true
              });
            });
          }}
          getItemLayout={(data, index) => ({
            length: width,
            offset: width * index,
            index,
          })}
        />

        {/* Footer */}
        <Animated.View 
          style={[
            styles.footer, 
            { 
              paddingBottom: insets.bottom + 20,
              opacity: fadeAnim,
              transform: [{ translateY: slideUpAnim }]
            }
          ]}
        >
          <Paginator data={onboardingData} scrollX={scrollX} />

          <Animated.View
            style={{
              transform: [{ scale: buttonScale }],
              zIndex: 100
            }}
          >
            <TouchableOpacity
              onPress={handleNext}
              onPressIn={handlePressIn}
              onPressOut={handlePressOut}
              activeOpacity={0.95}
              style={styles.buttonWrapper}
              disabled={false}
              hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
            >
              <LinearGradient
                colors={currentItem.gradient}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 0 }}
                style={styles.nextBtn}
              >
                <ShimmerEffect colors={['transparent', 'rgba(255,255,255,0.4)', 'transparent']} />
                <Text style={styles.nextBtnText}>
                  {isLastSlide ? startText : nextText}
                </Text>
                <Ionicons
                  name={isLastSlide ? 'rocket' : 'arrow-forward'}
                  size={22}
                  color="#fff"
                />
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
  },
  particle: {
    position: 'absolute',
    bottom: 0,
  },
  particleDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    shadowColor: '#f97316',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.8,
    shadowRadius: 4,
    elevation: 3,
  },
  shimmerContainer: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    overflow: 'hidden',
  },
  shimmerGradient: {
    width: width * 0.5,
    height: '100%',
  },
  pulsingGlow: {
    position: 'absolute',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingBottom: 10,
  },
  logoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  logoIcon: {
    width: 28,
    height: 28,
  },
  logoText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#9a3412',
    letterSpacing: 0.5,
  },
  skipBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
    paddingHorizontal: 16,
    borderRadius: 24,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  skipText: {
    fontSize: 15,
    color: '#6b7280',
    fontWeight: '600',
    marginRight: 4,
  },
  slide: {
    width,
    paddingHorizontal: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  iconWrapper: {
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 35,
  },
  iconContainer: {
    position: 'relative',
  },
  iconGradient: {
    width: 140,
    height: 140,
    borderRadius: 70,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 12 },
    shadowOpacity: 0.35,
    shadowRadius: 24,
    elevation: 18,
    overflow: 'hidden',
  },
  iconSecondary: {
    position: 'absolute',
    bottom: -8,
    right: -8,
    width: 52,
    height: 52,
    borderRadius: 26,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 10,
    elevation: 6,
    borderWidth: 3,
    borderColor: '#fef3c7',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#1f2937',
    textAlign: 'center',
    marginBottom: 10,
    letterSpacing: 0.5,
  },
  subtitle: {
    fontSize: 18,
    fontWeight: '700',
    textAlign: 'center',
    marginBottom: 18,
  },
  description: {
    fontSize: 16,
    color: '#6b7280',
    textAlign: 'center',
    lineHeight: 26,
    marginBottom: 28,
    paddingHorizontal: 5,
  },
  featuresContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    gap: 10,
  },
  featureBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 24,
    backgroundColor: '#fff',
    borderWidth: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.08,
    shadowRadius: 6,
    elevation: 4,
  },
  featureText: {
    fontSize: 13,
    fontWeight: '700',
  },
  footer: {
    paddingHorizontal: 20,
    gap: 28,
  },
  paginatorContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 10,
    height: 12,
  },
  dot: {
    height: 12,
    borderRadius: 6,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 3,
    elevation: 3,
  },
  dotGradient: {
    flex: 1,
  },
  buttonWrapper: {
    borderRadius: 32,
    overflow: 'hidden',
  },
  nextBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 12,
    paddingVertical: 18,
    paddingHorizontal: 48,
    borderRadius: 32,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.3,
    shadowRadius: 12,
    elevation: 8,
    overflow: 'hidden',
    minWidth: 200,
  },
  nextBtnText: {
    fontSize: 19,
    fontWeight: '700',
    color: '#fff',
    letterSpacing: 0.5,
  },
});
