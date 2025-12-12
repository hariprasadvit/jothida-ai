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

  const scale = scrollX.interpolate({
    inputRange,
    outputRange: [0.8, 1, 0.8],
    extrapolate: 'clamp',
  });

  const opacity = scrollX.interpolate({
    inputRange,
    outputRange: [0.4, 1, 0.4],
    extrapolate: 'clamp',
  });

  const translateY = scrollX.interpolate({
    inputRange,
    outputRange: [50, 0, 50],
    extrapolate: 'clamp',
  });

  const iconRotate = scrollX.interpolate({
    inputRange,
    outputRange: ['45deg', '0deg', '-45deg'],
    extrapolate: 'clamp',
  });

  return (
    <View style={styles.slide}>
      <Animated.View style={[styles.content, { opacity, transform: [{ scale }, { translateY }] }]}>
        {/* Icon Container */}
        <Animated.View style={[styles.iconContainer, { transform: [{ rotate: iconRotate }] }]}>
          <LinearGradient colors={item.gradient} style={styles.iconGradient}>
            <Ionicons name={item.icon} size={60} color="#fff" />
          </LinearGradient>
          <View style={styles.iconSecondary}>
            <Ionicons name={item.iconSecondary} size={24} color={item.gradient[0]} />
          </View>
        </Animated.View>

        {/* Text Content */}
        <Text style={styles.title}>{item.title}</Text>
        <Text style={styles.subtitle}>{item.subtitle}</Text>
        <Text style={styles.description}>{item.description}</Text>

        {/* Features */}
        <View style={styles.featuresContainer}>
          {item.features.map((feature, i) => (
            <View key={i} style={[styles.featureBadge, { borderColor: item.gradient[0] }]}>
              <Ionicons name="checkmark-circle" size={14} color={item.gradient[0]} />
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
          outputRange: [8, 24, 8],
          extrapolate: 'clamp',
        });

        const opacity = scrollX.interpolate({
          inputRange,
          outputRange: [0.3, 1, 0.3],
          extrapolate: 'clamp',
        });

        return (
          <Animated.View
            key={index}
            style={[
              styles.dot,
              { width: dotWidth, opacity, backgroundColor: item.gradient[0] },
            ]}
          />
        );
      })}
    </View>
  );
};

export default function OnboardingScreen({ navigation }) {
  const { language, isLoading } = useLanguage();

  // Memoize the onboarding data based on language
  const onboardingData = React.useMemo(() => getOnboardingData(language), [language]);

  const [currentIndex, setCurrentIndex] = useState(0);
  const scrollX = useRef(new Animated.Value(0)).current;
  const flatListRef = useRef(null);
  const insets = useSafeAreaInsets();

  // Animated values for buttons
  const buttonScale = useRef(new Animated.Value(1)).current;
  const fadeAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 800,
      useNativeDriver: true,
    }).start();
  }, []);

  // If language is still loading, wait
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
    if (currentIndex < onboardingData.length - 1) {
      flatListRef.current?.scrollToIndex({ index: currentIndex + 1 });
    } else {
      completeOnboarding();
    }
  };

  const handleSkip = () => {
    completeOnboarding();
  };

  const completeOnboarding = async () => {
    try {
      await setStorageItem('onboardingComplete', 'true');
      navigation.replace('Login');
    } catch (error) {
      console.error('Error saving onboarding status:', error);
      navigation.replace('Login');
    }
  };

  const handlePressIn = () => {
    Animated.spring(buttonScale, {
      toValue: 0.95,
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

  // Button text based on language
  const skipText = language === 'en' ? 'Skip' : language === 'kn' ? 'ಬಿಡಿ' : 'தவிர்';
  const nextText = language === 'en' ? 'Next' : language === 'kn' ? 'ಮುಂದೆ' : 'அடுத்து';
  const startText = language === 'en' ? 'Get Started' : language === 'kn' ? 'ಪ್ರಾರಂಭಿಸಿ' : 'தொடங்கு';

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={['#fff7ed', '#ffffff', '#fff7ed']}
        style={styles.gradient}
      >
        {/* Header */}
        <Animated.View style={[styles.header, { opacity: fadeAnim, paddingTop: insets.top + 10 }]}>
          <View style={styles.logoContainer}>
            <View style={styles.logoIcon}>
              <Svg width={24} height={24} viewBox="0 0 100 100">
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
            <TouchableOpacity onPress={handleSkip} style={styles.skipBtn}>
              <Text style={styles.skipText}>{skipText}</Text>
              <Ionicons name="chevron-forward" size={16} color="#6b7280" />
            </TouchableOpacity>
          )}
        </Animated.View>

        {/* Slides */}
        <FlatList
          key={language} // Force re-render when language changes
          ref={flatListRef}
          data={onboardingData}
          extraData={language} // Re-render when language changes
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
          scrollEventThrottle={32}
        />

        {/* Footer */}
        <View style={[styles.footer, { paddingBottom: insets.bottom + 20 }]}>
          <Paginator data={onboardingData} scrollX={scrollX} />

          <Animated.View style={{ transform: [{ scale: buttonScale }] }}>
            <TouchableOpacity
              onPress={handleNext}
              onPressIn={handlePressIn}
              onPressOut={handlePressOut}
              activeOpacity={0.9}
            >
              <LinearGradient
                colors={currentItem.gradient}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 0 }}
                style={styles.nextBtn}
              >
                <Text style={styles.nextBtnText}>
                  {isLastSlide ? startText : nextText}
                </Text>
                <Ionicons
                  name={isLastSlide ? 'rocket' : 'arrow-forward'}
                  size={20}
                  color="#fff"
                />
              </LinearGradient>
            </TouchableOpacity>
          </Animated.View>
        </View>
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
    gap: 8,
  },
  logoIcon: {
    width: 24,
    height: 24,
  },
  logoText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#9a3412',
  },
  skipBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 20,
    backgroundColor: '#f3f4f6',
  },
  skipText: {
    fontSize: 14,
    color: '#6b7280',
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
  iconContainer: {
    marginBottom: 30,
    position: 'relative',
  },
  iconGradient: {
    width: 120,
    height: 120,
    borderRadius: 60,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.3,
    shadowRadius: 20,
    elevation: 15,
  },
  iconSecondary: {
    position: 'absolute',
    bottom: -5,
    right: -5,
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 5,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1f2937',
    textAlign: 'center',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#f97316',
    fontWeight: '600',
    textAlign: 'center',
    marginBottom: 16,
  },
  description: {
    fontSize: 15,
    color: '#6b7280',
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: 24,
    paddingHorizontal: 10,
  },
  featuresContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    gap: 8,
  },
  featureBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: '#fff',
    borderWidth: 1,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  featureText: {
    fontSize: 12,
    fontWeight: '600',
  },
  footer: {
    paddingHorizontal: 20,
    gap: 24,
  },
  paginatorContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 8,
  },
  dot: {
    height: 8,
    borderRadius: 4,
  },
  nextBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 16,
    paddingHorizontal: 32,
    borderRadius: 30,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 5,
  },
  nextBtnText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#fff',
  },
});
