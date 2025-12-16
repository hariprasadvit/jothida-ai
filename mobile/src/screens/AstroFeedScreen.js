import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  ActivityIndicator,
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Animated,
  Dimensions,
  FlatList,
  Share,
  Platform,
  StatusBar,
  Image,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useRoute } from '@react-navigation/native';
import Svg, { Path, Circle } from 'react-native-svg';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { fetchUnifiedScores, calculateFallbackScore } from '../services/scoringService';

const { width: screenWidth, height: screenHeight } = Dimensions.get('window');
const width = screenWidth;
const height = Platform.OS === 'web' ? window.innerHeight : screenHeight;

// Story types for different content
const STORY_TYPES = {
  PLANET_INFLUENCE: 'planet_influence',
  MOON_TRANSIT: 'moon_transit',
  DAILY_INSIGHT: 'daily_insight',
  NAKSHATRA_EFFECT: 'nakshatra_effect',
  REMEDY: 'remedy',
  LUCKY_TIME: 'lucky_time',
};

// Planet data
const planetData = {
  Sun: { tamil: 'சூரியன்', kannada: 'ಸೂರ್ಯ', color: '#f59e0b', icon: 'sunny' },
  Moon: { tamil: 'சந்திரன்', kannada: 'ಚಂದ್ರ', color: '#e5e7eb', icon: 'moon' },
  Mars: { tamil: 'செவ்வாய்', kannada: 'ಮಂಗಳ', color: '#ef4444', icon: 'flame' },
  Mercury: { tamil: 'புதன்', kannada: 'ಬುಧ', color: '#22c55e', icon: 'leaf' },
  Jupiter: { tamil: 'குரு', kannada: 'ಗುರು', color: '#f97316', icon: 'planet' },
  Venus: { tamil: 'சுக்கிரன்', kannada: 'ಶುಕ್ರ', color: '#ec4899', icon: 'heart' },
  Saturn: { tamil: 'சனி', kannada: 'ಶನಿ', color: '#3b82f6', icon: 'cube' },
  Rahu: { tamil: 'ராகு', kannada: 'ರಾಹು', color: '#6366f1', icon: 'cloudy-night' },
  Ketu: { tamil: 'கேது', kannada: 'ಕೇತು', color: '#8b5cf6', icon: 'flash' },
};

// Rasi data
const rasiData = {
  'மேஷம்': { english: 'Aries', kannada: 'ಮೇಷ', symbol: '♈', element: 'fire' },
  'ரிஷபம்': { english: 'Taurus', kannada: 'ವೃಷಭ', symbol: '♉', element: 'earth' },
  'மிதுனம்': { english: 'Gemini', kannada: 'ಮಿಥುನ', symbol: '♊', element: 'air' },
  'கடகம்': { english: 'Cancer', kannada: 'ಕರ್ಕಾಟಕ', symbol: '♋', element: 'water' },
  'சிம்மம்': { english: 'Leo', kannada: 'ಸಿಂಹ', symbol: '♌', element: 'fire' },
  'கன்னி': { english: 'Virgo', kannada: 'ಕನ್ಯಾ', symbol: '♍', element: 'earth' },
  'துலாம்': { english: 'Libra', kannada: 'ತುಲಾ', symbol: '♎', element: 'air' },
  'விருச்சிகம்': { english: 'Scorpio', kannada: 'ವೃಶ್ಚಿಕ', symbol: '♏', element: 'water' },
  'தனுசு': { english: 'Sagittarius', kannada: 'ಧನು', symbol: '♐', element: 'fire' },
  'மகரம்': { english: 'Capricorn', kannada: 'ಮಕರ', symbol: '♑', element: 'earth' },
  'கும்பம்': { english: 'Aquarius', kannada: 'ಕುಂಭ', symbol: '♒', element: 'air' },
  'மீனம்': { english: 'Pisces', kannada: 'ಮೀನ', symbol: '♓', element: 'water' },
};

// Gradient backgrounds for stories (warm theme to match Home)
const storyGradients = {
  [STORY_TYPES.PLANET_INFLUENCE]: ['#fff7ed', '#ffedd5', '#fff8f0'],
  [STORY_TYPES.MOON_TRANSIT]: ['#f5f3ff', '#ede9fe', '#fff8f0'],
  [STORY_TYPES.DAILY_INSIGHT]: ['#fefce8', '#fef9c3', '#fff8f0'],
  [STORY_TYPES.NAKSHATRA_EFFECT]: ['#ecfeff', '#cffafe', '#fff8f0'],
  [STORY_TYPES.REMEDY]: ['#f0fdf4', '#dcfce7', '#fff8f0'],
  [STORY_TYPES.LUCKY_TIME]: ['#fffbeb', '#fef3c7', '#fff8f0'],
};

// Progress bar component for story timer
const ProgressBar = ({ index, activeIndex, duration }) => {
  const progress = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    if (index === activeIndex) {
      progress.setValue(0);
      Animated.timing(progress, {
        toValue: 1,
        duration: duration,
        useNativeDriver: false,
      }).start();
    } else if (index < activeIndex) {
      progress.setValue(1);
    } else {
      progress.setValue(0);
    }
  }, [activeIndex]);

  return (
    <View style={styles.progressBarContainer}>
      <Animated.View
        style={[
          styles.progressBarFill,
          {
            width: progress.interpolate({
              inputRange: [0, 1],
              outputRange: ['0%', '100%'],
            }),
          },
        ]}
      />
    </View>
  );
};

// Individual Story Card Component
const StoryCard = ({ story, isActive, onShare, language, userRasi }) => {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(50)).current;
  const scaleAnim = useRef(new Animated.Value(0.9)).current;

  useEffect(() => {
    if (isActive) {
      Animated.parallel([
        Animated.timing(fadeAnim, {
          toValue: 1,
          duration: 400,
          useNativeDriver: true,
        }),
        Animated.spring(slideAnim, {
          toValue: 0,
          friction: 8,
          useNativeDriver: true,
        }),
        Animated.spring(scaleAnim, {
          toValue: 1,
          friction: 8,
          useNativeDriver: true,
        }),
      ]).start();
    } else {
      fadeAnim.setValue(0);
      slideAnim.setValue(50);
      scaleAnim.setValue(0.9);
    }
  }, [isActive]);

  const getPlanetName = (planet) => {
    if (language === 'kn') return planetData[planet]?.kannada || planet;
    if (language === 'en') return planet;
    return planetData[planet]?.tamil || planet;
  };

  const renderStoryContent = () => {
    switch (story.type) {
      case STORY_TYPES.PLANET_INFLUENCE:
        return (
          <View style={styles.storyContent}>
            <View style={[styles.planetIconContainer, { backgroundColor: story.planetColor + '30' }]}>
              <Ionicons name={story.planetIcon} size={48} color={story.planetColor} />
            </View>
            <Text style={styles.storyLabel}>{story.label}</Text>
            <Text style={styles.storyTitle}>{story.title}</Text>
            <Text style={styles.storyDescription}>{story.description}</Text>
            {story.effect && (
              <View style={[styles.effectBadge, { backgroundColor: story.isPositive ? '#22c55e30' : '#ef444430' }]}>
                <Ionicons
                  name={story.isPositive ? 'trending-up' : 'trending-down'}
                  size={18}
                  color={story.isPositive ? '#22c55e' : '#ef4444'}
                />
                <Text style={[styles.effectText, { color: story.isPositive ? '#22c55e' : '#ef4444' }]}>
                  {story.effect}
                </Text>
              </View>
            )}
          </View>
        );

      case STORY_TYPES.MOON_TRANSIT:
        return (
          <View style={styles.storyContent}>
            <View style={styles.moonContainer}>
              <Text style={styles.moonEmoji}>🌙</Text>
              <View style={styles.moonGlow} />
            </View>
            <Text style={styles.storyLabel}>{story.label}</Text>
            <Text style={styles.storyTitle}>{story.title}</Text>
            <View style={styles.rasiSymbolContainer}>
              <Text style={styles.rasiSymbol}>{story.rasiSymbol}</Text>
              <Text style={styles.rasiName}>{story.rasiName}</Text>
            </View>
            <Text style={styles.storyDescription}>{story.description}</Text>
            {story.personalMessage && (
              <View style={styles.personalMessageBox}>
                <Ionicons name="person" size={16} color="#f97316" />
                <Text style={styles.personalMessage}>{story.personalMessage}</Text>
              </View>
            )}
          </View>
        );

      case STORY_TYPES.DAILY_INSIGHT:
        return (
          <View style={styles.storyContent}>
            <View style={styles.sparkleContainer}>
              <Text style={styles.sparkleEmoji}>✨</Text>
            </View>
            <Text style={styles.storyLabel}>{story.label}</Text>
            <Text style={styles.storyTitle}>{story.title}</Text>
            <View style={styles.scoreCircle}>
              <Text style={styles.scoreValue}>{story.score}</Text>
              <Text style={styles.scoreLabel}>{story.scoreLabel}</Text>
            </View>
            <Text style={styles.storyDescription}>{story.description}</Text>
            {story.tip && (
              <View style={styles.tipBox}>
                <Ionicons name="bulb" size={18} color="#f59e0b" />
                <Text style={styles.tipText}>{story.tip}</Text>
              </View>
            )}
          </View>
        );

      case STORY_TYPES.NAKSHATRA_EFFECT:
        return (
          <View style={styles.storyContent}>
            <View style={styles.nakshatraIconContainer}>
              <Text style={styles.starEmoji}>⭐</Text>
            </View>
            <Text style={styles.storyLabel}>{story.label}</Text>
            <Text style={styles.storyTitle}>{story.title}</Text>
            <Text style={styles.nakshatraName}>{story.nakshatraName}</Text>
            <Text style={styles.storyDescription}>{story.description}</Text>
            {story.luckyItems && (
              <View style={styles.luckyItemsContainer}>
                {story.luckyItems.map((item, idx) => (
                  <View key={idx} style={styles.luckyItem}>
                    <Ionicons name={item.icon} size={20} color="#f97316" />
                    <Text style={styles.luckyItemText}>{item.label}</Text>
                  </View>
                ))}
              </View>
            )}
          </View>
        );

      case STORY_TYPES.REMEDY:
        return (
          <View style={styles.storyContent}>
            <View style={styles.remedyIconContainer}>
              <Ionicons name="leaf" size={48} color="#22c55e" />
            </View>
            <Text style={styles.storyLabel}>{story.label}</Text>
            <Text style={styles.storyTitle}>{story.title}</Text>
            <Text style={styles.storyDescription}>{story.description}</Text>
            {story.steps && (
              <View style={styles.stepsContainer}>
                {story.steps.map((step, idx) => (
                  <View key={idx} style={styles.stepItem}>
                    <View style={styles.stepNumber}>
                      <Text style={styles.stepNumberText}>{idx + 1}</Text>
                    </View>
                    <Text style={styles.stepText}>{step}</Text>
                  </View>
                ))}
              </View>
            )}
          </View>
        );

      case STORY_TYPES.LUCKY_TIME:
        return (
          <View style={styles.storyContent}>
            <View style={styles.clockIconContainer}>
              <Ionicons name="time" size={48} color="#f59e0b" />
            </View>
            <Text style={styles.storyLabel}>{story.label}</Text>
            <Text style={styles.storyTitle}>{story.title}</Text>
            <View style={styles.timeSlotContainer}>
              {story.timeSlots?.map((slot, idx) => (
                <View key={idx} style={[styles.timeSlot, { backgroundColor: slot.color + '30' }]}>
                  <Ionicons name={slot.icon} size={24} color={slot.color} />
                  <Text style={styles.timeSlotTime}>{slot.time}</Text>
                  <Text style={styles.timeSlotLabel}>{slot.label}</Text>
                </View>
              ))}
            </View>
            <Text style={styles.storyDescription}>{story.description}</Text>
          </View>
        );

      default:
        return null;
    }
  };

  return (
    <Animated.View
      style={[
        styles.storyCard,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }, { scale: scaleAnim }],
        },
      ]}
    >
      <View style={styles.storyCardInner}>{renderStoryContent()}</View>
    </Animated.View>
  );
};

export default function AstroFeedScreen({ navigation }) {
  const route = useRoute();
  const { userProfile } = useAuth();
  const { t, language } = useLanguage();
  const insets = useSafeAreaInsets();
  const [stories, setStories] = useState([]);

  // Get initial story index from route params
  const initialStoryParam = route.params?.initialStory;
  const storyMap = {
    'planet': 0,    // PLANET_INFLUENCE
    'moon': 1,      // MOON_TRANSIT
    'insight': 2,   // DAILY_INSIGHT
    'star': 3,      // NAKSHATRA_EFFECT
  };
  const targetStoryIndex = initialStoryParam ? (storyMap[initialStoryParam] ?? 0) : 0;

  const [currentIndex, setCurrentIndex] = useState(0);
  const [initialNavigationDone, setInitialNavigationDone] = useState(false);
  const [loading, setLoading] = useState(true);
  const [dailyScore, setDailyScore] = useState(null);
  const [scoreLoaded, setScoreLoaded] = useState(false);
  const timerRef = useRef(null);
  const flatListRef = useRef(null);

  const STORY_DURATION = 8000; // 8 seconds per story

  // Fetch scores using unified scoring service (same as Dashboard)
  useEffect(() => {
    const fetchDailyScore = async () => {
      try {
        if (userProfile?.birthDate) {
          // Use unified scoring service - SAME as Dashboard
          const unifiedData = await fetchUnifiedScores(userProfile, language);

          if (unifiedData?.overallScore) {
            console.log('[AstroFeed] Using unified score:', unifiedData.overallScore);
            setDailyScore(unifiedData.overallScore);
            setScoreLoaded(true);
            return;
          }
        }
        // Fallback: use deterministic hash-based score
        const fallbackScore = calculateFallbackScore(userProfile);
        console.log('[AstroFeed] Using fallback score:', fallbackScore);
        setDailyScore(fallbackScore);
        setScoreLoaded(true);
      } catch (error) {
        console.error('[AstroFeed] Failed to fetch daily score:', error);
        const fallbackScore = calculateFallbackScore(userProfile);
        setDailyScore(fallbackScore);
        setScoreLoaded(true);
      }
    };

    fetchDailyScore();
  }, [userProfile, language]);

  // Generate personalized stories based on user profile
  const generateStories = useCallback((apiScore) => {
    const userRasi = userProfile?.rasi || 'மேஷம்';
    const userNakshatra = userProfile?.nakshatra || 'அசுவினி';
    const today = new Date();
    const dayOfWeek = today.getDay();

    // Planet ruling each day
    const dayPlanets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'];
    const todayPlanet = dayPlanets[dayOfWeek];

    const generatedStories = [];

    // Story 1: Today's Planet Influence
    const planetInfo = planetData[todayPlanet];
    generatedStories.push({
      id: '1',
      type: STORY_TYPES.PLANET_INFLUENCE,
      label: language === 'en' ? "TODAY'S RULING PLANET" : language === 'kn' ? 'ಇಂದಿನ ಆಡಳಿತ ಗ್ರಹ' : 'இன்றைய ஆட்சி கிரகம்',
      title: language === 'en' ? todayPlanet : language === 'kn' ? planetInfo.kannada : planetInfo.tamil,
      description: getPlanetDescription(todayPlanet, language),
      planetColor: planetInfo.color,
      planetIcon: planetInfo.icon,
      isPositive: ['Jupiter', 'Venus', 'Mercury'].includes(todayPlanet),
      effect: getPlanetEffect(todayPlanet, userRasi, language),
    });

    // Story 2: Moon Transit
    const moonRasi = getMoonRasi(today);
    generatedStories.push({
      id: '2',
      type: STORY_TYPES.MOON_TRANSIT,
      label: language === 'en' ? "MOON TRANSIT" : language === 'kn' ? 'ಚಂದ್ರ ಸಂಚಾರ' : 'சந்திர சஞ்சாரம்',
      title: language === 'en' ? `Moon in ${rasiData[moonRasi]?.english}` :
             language === 'kn' ? `ಚಂದ್ರ ${rasiData[moonRasi]?.kannada}ದಲ್ಲಿ` :
             `சந்திரன் ${moonRasi}ல்`,
      rasiSymbol: rasiData[moonRasi]?.symbol || '♈',
      rasiName: language === 'en' ? rasiData[moonRasi]?.english :
                language === 'kn' ? rasiData[moonRasi]?.kannada : moonRasi,
      description: getMoonTransitDescription(moonRasi, language),
      personalMessage: getMoonPersonalMessage(moonRasi, userRasi, language),
    });

    // Story 3: Daily Insight for User
    // Use API score if available (same as Dashboard), otherwise use passed fallback
    let scoreToUse = apiScore;
    if (scoreToUse === null || scoreToUse === undefined) {
      // This should rarely happen as fetchDailyScore already calculates fallback
      scoreToUse = calculateFallbackScore(userProfile);
    }
    generatedStories.push({
      id: '3',
      type: STORY_TYPES.DAILY_INSIGHT,
      label: language === 'en' ? "YOUR DAILY INSIGHT" : language === 'kn' ? 'ನಿಮ್ಮ ದಿನದ ಒಳನೋಟ' : 'உங்கள் இன்றைய பலன்',
      title: language === 'en' ? `Hey ${userProfile?.name || 'Friend'}!` :
             language === 'kn' ? `ಹೇ ${userProfile?.name || 'ಸ್ನೇಹಿತ'}!` :
             `வணக்கம் ${userProfile?.name || 'நண்பரே'}!`,
      score: scoreToUse,
      scoreLabel: language === 'en' ? 'Today\'s Score' : language === 'kn' ? 'ಇಂದಿನ ಸ್ಕೋರ್' : 'இன்றைய மதிப்பெண்',
      description: getDailyInsightDescription(scoreToUse, userRasi, language),
      tip: getDailyTip(todayPlanet, language),
    });

    // Story 4: Nakshatra Effect
    generatedStories.push({
      id: '4',
      type: STORY_TYPES.NAKSHATRA_EFFECT,
      label: language === 'en' ? "NAKSHATRA INFLUENCE" : language === 'kn' ? 'ನಕ್ಷತ್ರ ಪ್ರಭಾವ' : 'நட்சத்திர பலன்',
      title: language === 'en' ? "Your Star's Message" : language === 'kn' ? 'ನಿಮ್ಮ ನಕ್ಷತ್ರದ ಸಂದೇಶ' : 'உங்கள் நட்சத்திர செய்தி',
      nakshatraName: userNakshatra,
      description: getNakshatraDescription(userNakshatra, language),
      luckyItems: getLuckyItems(userNakshatra, language),
    });

    // Story 5: Today's Remedy
    generatedStories.push({
      id: '5',
      type: STORY_TYPES.REMEDY,
      label: language === 'en' ? "TODAY'S REMEDY" : language === 'kn' ? 'ಇಂದಿನ ಪರಿಹಾರ' : 'இன்றைய பரிகாரம்',
      title: language === 'en' ? 'Enhance Your Day' : language === 'kn' ? 'ನಿಮ್ಮ ದಿನವನ್ನು ಉತ್ತಮಗೊಳಿಸಿ' : 'உங்கள் நாளை மேம்படுத்துங்கள்',
      description: getRemedyDescription(todayPlanet, language),
      steps: getRemedySteps(todayPlanet, language),
    });

    // Story 6: Lucky Times
    generatedStories.push({
      id: '6',
      type: STORY_TYPES.LUCKY_TIME,
      label: language === 'en' ? "LUCKY TIMES TODAY" : language === 'kn' ? 'ಇಂದಿನ ಶುಭ ಸಮಯ' : 'இன்றைய நல்ல நேரம்',
      title: language === 'en' ? 'Best Times for You' : language === 'kn' ? 'ನಿಮಗೆ ಉತ್ತಮ ಸಮಯ' : 'உங்களுக்கான சிறந்த நேரங்கள்',
      timeSlots: getLuckyTimeSlots(language),
      description: getLuckyTimeDescription(language),
    });

    return generatedStories;
  }, [userProfile, language]);

  // Only generate stories after score is loaded from API
  useEffect(() => {
    if (scoreLoaded) {
      const loadedStories = generateStories(dailyScore);
      setStories(loadedStories);
      setLoading(false);
    }
  }, [generateStories, dailyScore, scoreLoaded]);

  // Handle initial navigation to specific story
  useEffect(() => {
    if (stories.length > 0 && !initialNavigationDone && targetStoryIndex > 0) {
      console.log('[AstroFeed] Navigating to story index:', targetStoryIndex);
      setCurrentIndex(targetStoryIndex);

      setTimeout(() => {
        flatListRef.current?.scrollToIndex({
          index: targetStoryIndex,
          animated: false,
        });
        setInitialNavigationDone(true);
      }, 300);
    } else if (stories.length > 0 && !initialNavigationDone) {
      setInitialNavigationDone(true);
    }
  }, [stories.length, targetStoryIndex, initialNavigationDone]);

  // Auto-advance timer
  useEffect(() => {
    if (stories.length > 0 && currentIndex < stories.length) {
      timerRef.current = setTimeout(() => {
        if (currentIndex < stories.length - 1) {
          goToNext();
        }
      }, STORY_DURATION);
    }

    return () => {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
      }
    };
  }, [currentIndex, stories.length]);

  const goToNext = () => {
    if (currentIndex < stories.length - 1) {
      setCurrentIndex(currentIndex + 1);
      flatListRef.current?.scrollToIndex({ index: currentIndex + 1, animated: true });
    }
  };

  const goToPrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
      flatListRef.current?.scrollToIndex({ index: currentIndex - 1, animated: true });
    }
  };


  const handleShare = async () => {
    const story = stories[currentIndex];
    try {
      const shareMessage = language === 'en'
        ? `🌟 Today's Astro Insight from Jothida AI:\n\n${story.title}\n${story.description}\n\nDownload Jothida AI for personalized astrology!`
        : language === 'kn'
        ? `🌟 ಜ್ಯೋತಿಷ AI ಯಿಂದ ಇಂದಿನ ಜ್ಯೋತಿಷ್ಯ ಒಳನೋಟ:\n\n${story.title}\n${story.description}\n\nವೈಯಕ್ತಿಕ ಜ್ಯೋತಿಷ್ಯಕ್ಕಾಗಿ ಜ್ಯೋತಿಷ AI ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ!`
        : `🌟 ஜோதிட AI இன் இன்றைய ஜோதிட பலன்:\n\n${story.title}\n${story.description}\n\nதனிப்பயனாக்கப்பட்ட ஜோதிடத்திற்கு ஜோதிட AI பதிவிறக்கவும்!`;

      await Share.share({
        message: shareMessage,
      });
    } catch (error) {
      console.error('Share error:', error);
    }
  };

  const renderStory = ({ item, index }) => {
    // Calculate content height accounting for tab bar on web
    const contentHeight = height;

    return (
      <View style={[styles.storyContainer, { width, height: contentHeight }]}>
        <LinearGradient
          colors={storyGradients[item.type] || storyGradients[STORY_TYPES.DAILY_INSIGHT]}
          style={[styles.storyGradient, { height: contentHeight }]}
        >
          <StoryCard
            story={item}
            isActive={index === currentIndex}
            onShare={handleShare}
            language={language}
            userRasi={userProfile?.rasi}
          />
        </LinearGradient>
      </View>
    );
  };

  const handleScrollBeginDrag = () => {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
    }
  };

  const handleMomentumScrollEnd = (event) => {
    const nextIndex = Math.round(event.nativeEvent.contentOffset.x / width);
    if (!Number.isNaN(nextIndex) && nextIndex !== currentIndex) {
      setCurrentIndex(nextIndex);
    }
  };

  if (loading) {
    return (
      <View style={styles.container}>
        <LinearGradient colors={['#faf7f2', '#f5ede5', '#fff8f0']} style={styles.fullScreen}>
          <View style={[styles.loadingContainer, { paddingTop: insets.top }]}>
            <ActivityIndicator size="large" color="#f97316" />
            <Text style={styles.loadingText}>{t('loading')}</Text>
          </View>
        </LinearGradient>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <StatusBar barStyle="dark-content" />

      <FlatList
        ref={flatListRef}
        data={stories}
        renderItem={renderStory}
        keyExtractor={(item) => item.id}
        horizontal
        pagingEnabled
        showsHorizontalScrollIndicator={false}
        scrollEnabled
        onScrollBeginDrag={handleScrollBeginDrag}
        onMomentumScrollEnd={handleMomentumScrollEnd}
        getItemLayout={(data, index) => ({
          length: width,
          offset: width * index,
          index,
        })}
      />

      {/* Progress Bars */}
      <View style={[styles.progressContainer, { top: insets.top + 10 }]}>
        {stories.map((_, index) => (
          <ProgressBar key={index} index={index} activeIndex={currentIndex} duration={STORY_DURATION} />
        ))}
      </View>

      {/* Top Bar */}
      <View style={[styles.topBar, { top: insets.top + 20 }]}>
        <TouchableOpacity style={styles.topIconButton} onPress={() => navigation.goBack()} activeOpacity={0.8}>
          <Ionicons name="close" size={24} color="#6b5644" />
        </TouchableOpacity>

        <View style={styles.topTitleWrap}>
          <Text style={styles.topTitle}>{t('appName')}</Text>
          <Text style={styles.topSubtitle}>
            {language === 'en' ? 'Daily Stories' : language === 'kn' ? 'ದೈನಿಕ ಕಥೆಗಳು' : 'தினசரி கதைகள்'}
          </Text>
        </View>

        <TouchableOpacity style={styles.topIconButton} onPress={handleShare} activeOpacity={0.8}>
          <Ionicons name="share-outline" size={20} color="#6b5644" />
        </TouchableOpacity>
      </View>

      {/* Side Navigation */}
      <View style={styles.sideNav} pointerEvents="box-none">
        <TouchableOpacity
          style={[styles.navButton, currentIndex === 0 && styles.navButtonDisabled]}
          onPress={goToPrevious}
          disabled={currentIndex === 0}
          activeOpacity={0.8}
        >
          <Ionicons name="chevron-back" size={22} color={currentIndex === 0 ? '#cbd5e1' : '#6b5644'} />
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.navButton, currentIndex === stories.length - 1 && styles.navButtonDisabled]}
          onPress={goToNext}
          disabled={currentIndex === stories.length - 1}
          activeOpacity={0.8}
        >
          <Ionicons name="chevron-forward" size={22} color={currentIndex === stories.length - 1 ? '#cbd5e1' : '#6b5644'} />
        </TouchableOpacity>
      </View>

      {/* Bottom Actions */}
      <View style={[styles.bottomBar, { bottom: insets.bottom + 18 }]}>
        <Text style={styles.swipeHint}>
          {language === 'en' ? 'Swipe left/right' : language === 'kn' ? 'ಎಡ/ಬಲಕ್ಕೆ ಸ್ವೈಪ್ ಮಾಡಿ' : 'இடது/வலது ஸ்வைப் செய்யுங்கள்'}
        </Text>
        <TouchableOpacity style={styles.primaryAction} onPress={() => navigation.navigate('Chat')} activeOpacity={0.9}>
          <Ionicons name="chatbubble-ellipses" size={18} color="#fff" />
          <Text style={styles.primaryActionText}>{language === 'en' ? 'Ask AI' : language === 'kn' ? 'AI ಕೇಳಿ' : 'AI கேள்'}</Text>
        </TouchableOpacity>
      </View>

      {/* Story Counter */}
      <View style={[styles.counterContainer, { bottom: insets.bottom + 96 }]}>
        <Text style={styles.counterText}>
          {currentIndex + 1} / {stories.length}
        </Text>
      </View>
    </View>
  );
}

// Helper functions for generating content
function getPlanetDescription(planet, language) {
  const descriptions = {
    Sun: {
      en: 'The Sun brings leadership energy and vitality. Focus on career goals and self-expression today.',
      kn: 'ಸೂರ್ಯ ನಾಯಕತ್ವ ಶಕ್ತಿ ಮತ್ತು ಚೈತನ್ಯವನ್ನು ತರುತ್ತಾನೆ. ಇಂದು ವೃತ್ತಿ ಗುರಿಗಳು ಮತ್ತು ಸ್ವಯಂ-ಅಭಿವ್ಯಕ್ತಿ ಮೇಲೆ ಗಮನ ಹರಿಸಿ.',
      ta: 'சூரியன் தலைமைத்துவ சக்தியையும் உயிர்ச்சக்தியையும் தருகிறார். இன்று தொழில் இலக்குகள் மற்றும் சுய வெளிப்பாட்டில் கவனம் செலுத்துங்கள்.',
    },
    Moon: {
      en: 'The Moon enhances emotions and intuition. Trust your feelings and nurture close relationships.',
      kn: 'ಚಂದ್ರ ಭಾವನೆಗಳು ಮತ್ತು ಅಂತಃಪ್ರಜ್ಞೆಯನ್ನು ಹೆಚ್ಚಿಸುತ್ತಾನೆ. ನಿಮ್ಮ ಭಾವನೆಗಳನ್ನು ನಂಬಿ ಮತ್ತು ಆತ್ಮೀಯ ಸಂಬಂಧಗಳನ್ನು ಪೋಷಿಸಿ.',
      ta: 'சந்திரன் உணர்வுகளையும் உள்ளுணர்வையும் மேம்படுத்துகிறார். உங்கள் உணர்வுகளை நம்புங்கள், நெருங்கிய உறவுகளை பேணுங்கள்.',
    },
    Mars: {
      en: 'Mars brings courage and determination. Channel this energy into physical activities and bold decisions.',
      kn: 'ಮಂಗಳ ಧೈರ್ಯ ಮತ್ತು ನಿರ್ಧಾರವನ್ನು ತರುತ್ತಾನೆ. ಈ ಶಕ್ತಿಯನ್ನು ದೈಹಿಕ ಚಟುವಟಿಕೆಗಳು ಮತ್ತು ದಿಟ್ಟ ನಿರ್ಧಾರಗಳಿಗೆ ಬಳಸಿ.',
      ta: 'செவ்வாய் தைரியமும் உறுதியும் தருகிறார். இந்த சக்தியை உடல் செயல்பாடுகள் மற்றும் தைரியமான முடிவுகளுக்கு பயன்படுத்துங்கள்.',
    },
    Mercury: {
      en: 'Mercury enhances communication and intellect. Perfect day for learning, writing, and business deals.',
      kn: 'ಬುಧ ಸಂವಹನ ಮತ್ತು ಬುದ್ಧಿವಂತಿಕೆಯನ್ನು ಹೆಚ್ಚಿಸುತ್ತಾನೆ. ಕಲಿಕೆ, ಬರವಣಿಗೆ ಮತ್ತು ವ್ಯಾಪಾರ ಒಪ್ಪಂದಗಳಿಗೆ ಉತ್ತಮ ದಿನ.',
      ta: 'புதன் தொடர்பு மற்றும் அறிவை மேம்படுத்துகிறார். கற்றல், எழுத்து மற்றும் வணிக ஒப்பந்தங்களுக்கு சிறந்த நாள்.',
    },
    Jupiter: {
      en: 'Jupiter brings wisdom and expansion. Excellent for spiritual practices, education, and new opportunities.',
      kn: 'ಗುರು ಜ್ಞಾನ ಮತ್ತು ವಿಸ್ತರಣೆಯನ್ನು ತರುತ್ತಾನೆ. ಆಧ್ಯಾತ್ಮಿಕ ಅಭ್ಯಾಸಗಳು, ಶಿಕ್ಷಣ ಮತ್ತು ಹೊಸ ಅವಕಾಶಗಳಿಗೆ ಅತ್ಯುತ್ತಮ.',
      ta: 'குரு ஞானமும் வளர்ச்சியும் தருகிறார். ஆன்மீக நடைமுறைகள், கல்வி மற்றும் புதிய வாய்ப்புகளுக்கு சிறந்தது.',
    },
    Venus: {
      en: 'Venus enhances love and beauty. Perfect for relationships, arts, and enjoying life\'s pleasures.',
      kn: 'ಶುಕ್ರ ಪ್ರೀತಿ ಮತ್ತು ಸೌಂದರ್ಯವನ್ನು ಹೆಚ್ಚಿಸುತ್ತಾನೆ. ಸಂಬಂಧಗಳು, ಕಲೆಗಳು ಮತ್ತು ಜೀವನದ ಸುಖಗಳನ್ನು ಆನಂದಿಸಲು ಉತ್ತಮ.',
      ta: 'சுக்கிரன் காதலையும் அழகையும் மேம்படுத்துகிறார். உறவுகள், கலைகள் மற்றும் வாழ்க்கை இன்பங்களுக்கு சிறந்தது.',
    },
    Saturn: {
      en: 'Saturn brings discipline and responsibility. Focus on long-term goals and complete pending tasks.',
      kn: 'ಶನಿ ಶಿಸ್ತು ಮತ್ತು ಜವಾಬ್ದಾರಿಯನ್ನು ತರುತ್ತಾನೆ. ದೀರ್ಘಕಾಲೀನ ಗುರಿಗಳ ಮೇಲೆ ಗಮನ ಹರಿಸಿ ಮತ್ತು ಬಾಕಿ ಕೆಲಸಗಳನ್ನು ಪೂರ್ಣಗೊಳಿಸಿ.',
      ta: 'சனி ஒழுக்கமும் பொறுப்பும் தருகிறார். நீண்ட கால இலக்குகளில் கவனம் செலுத்தி, நிலுவையில் உள்ள பணிகளை முடியுங்கள்.',
    },
  };
  const key = language === 'en' ? 'en' : language === 'kn' ? 'kn' : 'ta';
  return descriptions[planet]?.[key] || descriptions.Sun[key];
}

function getPlanetEffect(planet, userRasi, language) {
  const effects = {
    en: ['Career boost', 'Financial gains', 'Relationship harmony', 'Health improvement', 'Mental clarity'],
    kn: ['ವೃತ್ತಿ ಏಳಿಗೆ', 'ಆರ್ಥಿಕ ಲಾಭ', 'ಸಂಬಂಧ ಸಾಮರಸ್ಯ', 'ಆರೋಗ್ಯ ಸುಧಾರಣೆ', 'ಮಾನಸಿಕ ಸ್ಪಷ್ಟತೆ'],
    ta: ['தொழில் உயர்வு', 'நிதி லாபம்', 'உறவு நல்லிணக்கம்', 'உடல்நலம் மேம்பாடு', 'மன தெளிவு'],
  };
  const key = language === 'en' ? 'en' : language === 'kn' ? 'kn' : 'ta';
  return effects[key][Math.floor(Math.random() * effects[key].length)];
}

function getMoonRasi(date) {
  const rasis = Object.keys(rasiData);
  const dayOfYear = Math.floor((date - new Date(date.getFullYear(), 0, 0)) / (1000 * 60 * 60 * 24));
  return rasis[Math.floor(dayOfYear / 2.5) % 12];
}

function getMoonTransitDescription(moonRasi, language) {
  const element = rasiData[moonRasi]?.element;
  const descriptions = {
    fire: {
      en: 'Fiery energy dominates today. Great for taking initiative and pursuing passions.',
      kn: 'ಇಂದು ಅಗ್ನಿ ಶಕ್ತಿ ಪ್ರಧಾನ. ಉಪಕ್ರಮ ತೆಗೆದುಕೊಳ್ಳಲು ಮತ್ತು ಹವ್ಯಾಸಗಳನ್ನು ಅನುಸರಿಸಲು ಉತ್ತಮ.',
      ta: 'இன்று அக்னி சக்தி ஆதிக்கம். முன்முயற்சி எடுக்கவும், ஆர்வங்களை தொடரவும் சிறந்தது.',
    },
    earth: {
      en: 'Grounded energy prevails. Focus on practical matters and building stability.',
      kn: 'ಭೂಮಿಯ ಶಕ್ತಿ ಪ್ರಧಾನ. ಪ್ರಾಯೋಗಿಕ ವಿಷಯಗಳು ಮತ್ತು ಸ್ಥಿರತೆ ನಿರ್ಮಾಣದ ಮೇಲೆ ಗಮನ ಹರಿಸಿ.',
      ta: 'பூமி சக்தி நிலவுகிறது. நடைமுறை விஷயங்கள் மற்றும் நிலைத்தன்மையை உருவாக்குவதில் கவனம் செலுத்துங்கள்.',
    },
    air: {
      en: 'Intellectual energy is high. Perfect for communication, networking, and learning.',
      kn: 'ಬೌದ್ಧಿಕ ಶಕ್ತಿ ಹೆಚ್ಚಿದೆ. ಸಂವಹನ, ನೆಟ್‌ವರ್ಕಿಂಗ್ ಮತ್ತು ಕಲಿಕೆಗೆ ಉತ್ತಮ.',
      ta: 'அறிவுசார் சக்தி அதிகம். தொடர்பு, நெட்வொர்க்கிங் மற்றும் கற்றலுக்கு சிறந்தது.',
    },
    water: {
      en: 'Emotional energy flows today. Trust your intuition and nurture relationships.',
      kn: 'ಇಂದು ಭಾವನಾತ್ಮಕ ಶಕ್ತಿ ಹರಿಯುತ್ತದೆ. ನಿಮ್ಮ ಅಂತಃಪ್ರಜ್ಞೆಯನ್ನು ನಂಬಿ ಮತ್ತು ಸಂಬಂಧಗಳನ್ನು ಪೋಷಿಸಿ.',
      ta: 'இன்று உணர்வுபூர்வ சக்தி பாய்கிறது. உங்கள் உள்ளுணர்வை நம்புங்கள், உறவுகளை பேணுங்கள்.',
    },
  };
  const key = language === 'en' ? 'en' : language === 'kn' ? 'kn' : 'ta';
  return descriptions[element]?.[key] || descriptions.fire[key];
}

function getMoonPersonalMessage(moonRasi, userRasi, language) {
  const messages = {
    en: `As a ${userRasi} native, this Moon transit brings ${Math.random() > 0.5 ? 'positive' : 'transformative'} energy to your ${Math.random() > 0.5 ? 'relationships' : 'career'}.`,
    kn: `${userRasi} ರಾಶಿಯವರಾಗಿ, ಈ ಚಂದ್ರ ಸಂಚಾರ ನಿಮ್ಮ ${Math.random() > 0.5 ? 'ಸಂಬಂಧಗಳಿಗೆ' : 'ವೃತ್ತಿಗೆ'} ${Math.random() > 0.5 ? 'ಸಕಾರಾತ್ಮಕ' : 'ಪರಿವರ್ತಕ'} ಶಕ್ತಿಯನ್ನು ತರುತ್ತದೆ.`,
    ta: `${userRasi} ராசிக்காரராக, இந்த சந்திர சஞ்சாரம் உங்கள் ${Math.random() > 0.5 ? 'உறவுகளுக்கு' : 'தொழிலுக்கு'} ${Math.random() > 0.5 ? 'நேர்மறை' : 'மாற்றும்'} சக்தியை தருகிறது.`,
  };
  const key = language === 'en' ? 'en' : language === 'kn' ? 'kn' : 'ta';
  return messages[key];
}

function getDailyInsightDescription(score, userRasi, language) {
  const level = score >= 80 ? 'excellent' : score >= 65 ? 'good' : 'moderate';
  const descriptions = {
    excellent: {
      en: 'Today is exceptionally favorable! The stars align for success. Take bold actions and trust your instincts.',
      kn: 'ಇಂದು ಅತ್ಯಂತ ಅನುಕೂಲಕರ! ನಕ್ಷತ್ರಗಳು ಯಶಸ್ಸಿಗೆ ಹೊಂದಿಕೊಳ್ಳುತ್ತವೆ. ದಿಟ್ಟ ಕ್ರಮಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳಿ ಮತ್ತು ನಿಮ್ಮ ಪ್ರವೃತ್ತಿಗಳನ್ನು ನಂಬಿ.',
      ta: 'இன்று மிகவும் சாதகமானது! நட்சத்திரங்கள் வெற்றிக்கு ஒத்துவருகின்றன. தைரியமான நடவடிக்கைகள் எடுங்கள், உங்கள் உள்ளுணர்வை நம்புங்கள்.',
    },
    good: {
      en: 'A promising day awaits! Focus on your goals and maintain positive energy throughout.',
      kn: 'ಭರವಸೆಯ ದಿನ ಕಾಯುತ್ತಿದೆ! ನಿಮ್ಮ ಗುರಿಗಳ ಮೇಲೆ ಗಮನ ಹರಿಸಿ ಮತ್ತು ಉದ್ದಕ್ಕೂ ಸಕಾರಾತ್ಮಕ ಶಕ್ತಿಯನ್ನು ಕಾಪಾಡಿ.',
      ta: 'நம்பிக்கையான நாள் காத்திருக்கிறது! உங்கள் இலக்குகளில் கவனம் செலுத்தி, நேர்மறை ஆற்றலை பராமரியுங்கள்.',
    },
    moderate: {
      en: 'A balanced day ahead. Stay patient and avoid major decisions. Good for planning and preparation.',
      kn: 'ಸಮತೋಲಿತ ದಿನ ಮುಂದಿದೆ. ತಾಳ್ಮೆಯಿಂದಿರಿ ಮತ್ತು ಪ್ರಮುಖ ನಿರ್ಧಾರಗಳನ್ನು ತಪ್ಪಿಸಿ. ಯೋಜನೆ ಮತ್ತು ತಯಾರಿಗೆ ಉತ್ತಮ.',
      ta: 'சமநிலையான நாள் வரப்போகிறது. பொறுமையாக இருங்கள், பெரிய முடிவுகளை தவிர்க்கவும். திட்டமிடல் மற்றும் தயாரிப்புக்கு நல்லது.',
    },
  };
  const key = language === 'en' ? 'en' : language === 'kn' ? 'kn' : 'ta';
  return descriptions[level][key];
}

function getDailyTip(planet, language) {
  const tips = {
    Sun: {
      en: 'Offer water to the rising sun for positive energy',
      kn: 'ಧನಾತ್ಮಕ ಶಕ್ತಿಗಾಗಿ ಉದಯಿಸುವ ಸೂರ್ಯನಿಗೆ ನೀರು ಅರ್ಪಿಸಿ',
      ta: 'நேர்மறை சக்திக்கு உதயமாகும் சூரியனுக்கு நீர் அர்ப்பணியுங்கள்',
    },
    Moon: {
      en: 'Wear white clothes and meditate tonight',
      kn: 'ಬಿಳಿ ಬಟ್ಟೆ ಧರಿಸಿ ಮತ್ತು ಇಂದು ರಾತ್ರಿ ಧ್ಯಾನ ಮಾಡಿ',
      ta: 'வெள்ளை ஆடை அணிந்து இன்று இரவு தியானம் செய்யுங்கள்',
    },
    Mars: {
      en: 'Exercise in the morning and visit Hanuman temple',
      kn: 'ಬೆಳಿಗ್ಗೆ ವ್ಯಾಯಾಮ ಮಾಡಿ ಮತ್ತು ಹನುಮಾನ್ ದೇವಾಲಯಕ್ಕೆ ಭೇಟಿ ನೀಡಿ',
      ta: 'காலையில் உடற்பயிற்சி செய்து ஹனுமான் கோவிலுக்கு செல்லுங்கள்',
    },
    Mercury: {
      en: 'Chant Vishnu mantra and wear green',
      kn: 'ವಿಷ್ಣು ಮಂತ್ರ ಪಠಿಸಿ ಮತ್ತು ಹಸಿರು ಧರಿಸಿ',
      ta: 'விஷ்ணு மந்திரம் சொல்லி பச்சை நிற ஆடை அணியுங்கள்',
    },
    Jupiter: {
      en: 'Feed bananas to cows and help a teacher',
      kn: 'ಹಸುಗಳಿಗೆ ಬಾಳೆಹಣ್ಣು ತಿನ್ನಿಸಿ ಮತ್ತು ಶಿಕ್ಷಕರಿಗೆ ಸಹಾಯ ಮಾಡಿ',
      ta: 'பசுக்களுக்கு வாழைப்பழம் கொடுத்து ஆசிரியருக்கு உதவுங்கள்',
    },
    Venus: {
      en: 'Offer white flowers to Lakshmi and wear perfume',
      kn: 'ಲಕ್ಷ್ಮಿಗೆ ಬಿಳಿ ಹೂವುಗಳನ್ನು ಅರ್ಪಿಸಿ ಮತ್ತು ಸುಗಂಧ ಧರಿಸಿ',
      ta: 'லட்சுமிக்கு வெள்ளை பூக்கள் சாற்றி வாசனை திரவியம் பூசுங்கள்',
    },
    Saturn: {
      en: 'Help the elderly and donate oil',
      kn: 'ವಯಸ್ಕರಿಗೆ ಸಹಾಯ ಮಾಡಿ ಮತ್ತು ಎಣ್ಣೆ ದಾನ ಮಾಡಿ',
      ta: 'முதியவர்களுக்கு உதவி எண்ணெய் தானம் செய்யுங்கள்',
    },
  };
  const key = language === 'en' ? 'en' : language === 'kn' ? 'kn' : 'ta';
  return tips[planet]?.[key] || tips.Sun[key];
}

function getNakshatraDescription(nakshatra, language) {
  const descriptions = {
    en: `Your birth star ${nakshatra} is receiving positive vibrations today. The cosmic energy supports your natural talents and brings opportunities for growth.`,
    kn: `ನಿಮ್ಮ ಜನ್ಮ ನಕ್ಷತ್ರ ${nakshatra} ಇಂದು ಧನಾತ್ಮಕ ಕಂಪನಗಳನ್ನು ಪಡೆಯುತ್ತಿದೆ. ಕಾಸ್ಮಿಕ್ ಶಕ್ತಿ ನಿಮ್ಮ ಸ್ವಾಭಾವಿಕ ಪ್ರತಿಭೆಗಳನ್ನು ಬೆಂಬಲಿಸುತ್ತದೆ ಮತ್ತು ಬೆಳವಣಿಗೆಗೆ ಅವಕಾಶಗಳನ್ನು ತರುತ್ತದೆ.`,
    ta: `உங்கள் பிறந்த நட்சத்திரம் ${nakshatra} இன்று நேர்மறை அதிர்வுகளை பெறுகிறது. காஸ்மிக் சக்தி உங்கள் இயல்பான திறமைகளை ஆதரித்து வளர்ச்சிக்கான வாய்ப்புகளை தருகிறது.`,
  };
  const key = language === 'en' ? 'en' : language === 'kn' ? 'kn' : 'ta';
  return descriptions[key];
}

function getLuckyItems(nakshatra, language) {
  return [
    {
      icon: 'color-palette',
      label: language === 'en' ? 'Color: Orange' : language === 'kn' ? 'ಬಣ್ಣ: ಕಿತ್ತಳೆ' : 'நிறம்: ஆரஞ்சு',
    },
    {
      icon: 'diamond',
      label: language === 'en' ? 'Stone: Ruby' : language === 'kn' ? 'ಕಲ್ಲು: ಮಾಣಿಕ್ಯ' : 'கல்: மாணிக்கம்',
    },
    {
      icon: 'compass',
      label: language === 'en' ? 'Direction: East' : language === 'kn' ? 'ದಿಕ್ಕು: ಪೂರ್ವ' : 'திசை: கிழக்கு',
    },
  ];
}

function getRemedyDescription(planet, language) {
  const descriptions = {
    en: `Based on today's planetary alignment, here are simple remedies to enhance positive energy and minimize challenges.`,
    kn: `ಇಂದಿನ ಗ್ರಹ ಜೋಡಣೆಯ ಆಧಾರದ ಮೇಲೆ, ಧನಾತ್ಮಕ ಶಕ್ತಿಯನ್ನು ಹೆಚ್ಚಿಸಲು ಮತ್ತು ಸವಾಲುಗಳನ್ನು ಕಡಿಮೆ ಮಾಡಲು ಸರಳ ಪರಿಹಾರಗಳು.`,
    ta: `இன்றைய கிரக நிலைப்படி, நேர்மறை சக்தியை அதிகரிக்கவும், சவால்களை குறைக்கவும் எளிய பரிகாரங்கள்.`,
  };
  const key = language === 'en' ? 'en' : language === 'kn' ? 'kn' : 'ta';
  return descriptions[key];
}

function getRemedySteps(planet, language) {
  const steps = {
    en: [
      'Light a diya with ghee in the morning',
      'Chant the planet mantra 11 times',
      'Donate items associated with the planet',
    ],
    kn: [
      'ಬೆಳಿಗ್ಗೆ ತುಪ್ಪದಿಂದ ದೀಪ ಹಚ್ಚಿ',
      'ಗ್ರಹ ಮಂತ್ರವನ್ನು 11 ಬಾರಿ ಪಠಿಸಿ',
      'ಗ್ರಹಕ್ಕೆ ಸಂಬಂಧಿಸಿದ ವಸ್ತುಗಳನ್ನು ದಾನ ಮಾಡಿ',
    ],
    ta: [
      'காலையில் நெய் விளக்கு ஏற்றுங்கள்',
      'கிரக மந்திரத்தை 11 முறை சொல்லுங்கள்',
      'கிரகத்துடன் தொடர்புடைய பொருட்களை தானம் செய்யுங்கள்',
    ],
  };
  const key = language === 'en' ? 'en' : language === 'kn' ? 'kn' : 'ta';
  return steps[key];
}

function getLuckyTimeSlots(language) {
  return [
    {
      time: '6:00 - 7:30',
      label: language === 'en' ? 'Brahma Muhurta' : language === 'kn' ? 'ಬ್ರಹ್ಮ ಮುಹೂರ್ತ' : 'பிரம்ம முகூர்த்தம்',
      icon: 'sunny',
      color: '#f59e0b',
    },
    {
      time: '10:00 - 11:30',
      label: language === 'en' ? 'Abhijit Muhurta' : language === 'kn' ? 'ಅಭಿಜಿತ್ ಮುಹೂರ್ತ' : 'அபிஜித் முகூர்த்தம்',
      icon: 'star',
      color: '#22c55e',
    },
    {
      time: '17:00 - 18:30',
      label: language === 'en' ? 'Evening Auspicious' : language === 'kn' ? 'ಸಂಜೆ ಶುಭ' : 'மாலை சுபம்',
      icon: 'moon',
      color: '#8b5cf6',
    },
  ];
}

function getLuckyTimeDescription(language) {
  const descriptions = {
    en: 'These time slots are especially auspicious for starting new ventures, important meetings, and spiritual practices.',
    kn: 'ಈ ಸಮಯದ ಸ್ಲಾಟ್‌ಗಳು ಹೊಸ ಉದ್ಯಮಗಳನ್ನು ಪ್ರಾರಂಭಿಸಲು, ಪ್ರಮುಖ ಸಭೆಗಳು ಮತ್ತು ಆಧ್ಯಾತ್ಮಿಕ ಅಭ್ಯಾಸಗಳಿಗೆ ವಿಶೇಷವಾಗಿ ಶುಭ.',
    ta: 'இந்த நேர இடைவெளிகள் புதிய முயற்சிகளை தொடங்க, முக்கிய சந்திப்புகள் மற்றும் ஆன்மீக நடைமுறைகளுக்கு குறிப்பாக சுபமானவை.',
  };
  const key = language === 'en' ? 'en' : language === 'kn' ? 'kn' : 'ta';
  return descriptions[key];
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
    ...(Platform.OS === 'web' && { height: '100vh', maxHeight: '100vh', overflow: 'hidden' }),
  },
  fullScreen: {
    flex: 1,
    ...(Platform.OS === 'web' && { height: '100vh' }),
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    color: '#6b5644',
    fontSize: 13,
    marginTop: 14,
    fontWeight: '800',
  },
  touchContainer: {
    flex: 1,
    ...(Platform.OS === 'web' && { height: '100vh' }),
  },
  storyContainer: {
    flex: 1,
    height: height,
    ...(Platform.OS === 'web' && { height: '100vh' }),
  },
  storyGradient: {
    flex: 1,
    justifyContent: 'center',
    height: height,
    ...(Platform.OS === 'web' && { height: '100vh' }),
    alignItems: 'center',
    paddingHorizontal: 24,
  },
  storyCard: {
    width: '100%',
    alignItems: 'center',
  },
  storyCardInner: {
    width: '100%',
    backgroundColor: '#fff8f0',
    borderRadius: 22,
    borderWidth: 1,
    borderColor: '#e8d5c4',
    paddingHorizontal: 18,
    paddingVertical: 22,
    shadowColor: '#d4a574',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.08,
    shadowRadius: 12,
    elevation: 3,
  },
  storyContent: {
    alignItems: 'center',
    width: '100%',
  },
  storyLabel: {
    color: '#8b6f47',
    fontSize: 11,
    fontWeight: '900',
    letterSpacing: 1.2,
    marginBottom: 8,
    marginTop: 6,
    textTransform: 'uppercase',
  },
  storyTitle: {
    color: '#6b5644',
    fontSize: 26,
    fontWeight: '900',
    textAlign: 'center',
    marginBottom: 14,
    letterSpacing: -0.3,
  },
  storyDescription: {
    color: '#6b5644',
    fontSize: 15,
    textAlign: 'center',
    lineHeight: 24,
    marginTop: 12,
    fontWeight: '600',
  },

  // Planet Influence styles
  planetIconContainer: {
    width: 100,
    height: 100,
    borderRadius: 50,
    justifyContent: 'center',
    alignItems: 'center',
  },
  effectBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 20,
    marginTop: 20,
    gap: 8,
  },
  effectText: {
    fontSize: 16,
    fontWeight: '600',
  },

  // Moon Transit styles
  moonContainer: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  moonEmoji: {
    fontSize: 80,
  },
  moonGlow: {
    position: 'absolute',
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
  },
  rasiSymbolContainer: {
    alignItems: 'center',
    marginVertical: 16,
  },
  rasiSymbol: {
    fontSize: 48,
    color: '#6b5644',
  },
  rasiName: {
    color: '#8b6f47',
    fontSize: 14,
    marginTop: 4,
    fontWeight: '800',
  },
  personalMessageBox: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(249, 115, 22, 0.2)',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 12,
    marginTop: 20,
    gap: 10,
  },
  personalMessage: {
    color: '#f97316',
    fontSize: 14,
    flex: 1,
  },

  // Daily Insight styles
  sparkleContainer: {
    marginBottom: 8,
  },
  sparkleEmoji: {
    fontSize: 60,
  },
  scoreCircle: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: '#fff7ed',
    borderWidth: 4,
    borderColor: '#f97316',
    justifyContent: 'center',
    alignItems: 'center',
    marginVertical: 18,
  },
  scoreValue: {
    color: '#f97316',
    fontSize: 36,
    fontWeight: 'bold',
  },
  scoreLabel: {
    color: '#8b6f47',
    fontSize: 11,
    marginTop: 4,
    fontWeight: '800',
  },
  tipBox: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(245, 158, 11, 0.2)',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 12,
    marginTop: 20,
    gap: 10,
  },
  tipText: {
    color: '#f59e0b',
    fontSize: 14,
    flex: 1,
  },

  // Nakshatra styles
  nakshatraIconContainer: {
    marginBottom: 8,
  },
  starEmoji: {
    fontSize: 60,
  },
  nakshatraName: {
    color: '#f97316',
    fontSize: 20,
    fontWeight: '600',
    marginBottom: 8,
  },
  luckyItemsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    gap: 12,
    marginTop: 20,
  },
  luckyItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(249, 115, 22, 0.2)',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 20,
    gap: 6,
  },
  luckyItemText: {
    color: '#f97316',
    fontSize: 12,
  },

  // Remedy styles
  remedyIconContainer: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: 'rgba(34, 197, 94, 0.2)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  stepsContainer: {
    width: '100%',
    marginTop: 20,
  },
  stepItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
    gap: 12,
  },
  stepNumber: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: '#22c55e',
    justifyContent: 'center',
    alignItems: 'center',
  },
  stepNumberText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  stepText: {
    color: '#6b5644',
    fontSize: 14,
    flex: 1,
    fontWeight: '700',
  },

  // Lucky Time styles
  clockIconContainer: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: 'rgba(245, 158, 11, 0.2)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  timeSlotContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    flexWrap: 'wrap',
    gap: 12,
    marginVertical: 20,
  },
  timeSlot: {
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 12,
    minWidth: 100,
  },
  timeSlotTime: {
    color: '#6b5644',
    fontSize: 14,
    fontWeight: '900',
    marginTop: 8,
  },
  timeSlotLabel: {
    color: '#8b6f47',
    fontSize: 10,
    marginTop: 4,
    fontWeight: '800',
  },

  // Progress bar styles
  progressContainer: {
    position: 'absolute',
    left: 12,
    right: 12,
    flexDirection: 'row',
    gap: 4,
    zIndex: 10,
  },
  progressBarContainer: {
    flex: 1,
    height: 3,
    backgroundColor: '#e8d5c4',
    borderRadius: 2,
    overflow: 'hidden',
  },
  progressBarFill: {
    height: '100%',
    backgroundColor: '#f97316',
    borderRadius: 2,
  },

  // Header styles
  header: {
    position: 'absolute',
    left: 16,
    right: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    zIndex: 10,
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  logoContainer: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: 'rgba(249, 115, 22, 0.3)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  appName: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  storyTime: {
    color: '#9ca3af',
    fontSize: 12,
  },
  closeButton: {
    width: 40,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },

  // Bottom actions
  bottomActions: {
    position: 'absolute',
    left: 0,
    right: 0,
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 40,
    zIndex: 10,
  },
  actionButton: {
    alignItems: 'center',
    gap: 4,
  },
  actionLabel: {
    color: '#fff',
    fontSize: 12,
  },

  // Counter
  counterContainer: {
    position: 'absolute',
    left: 0,
    right: 0,
    alignItems: 'center',
    zIndex: 10,
  },
  counterText: {
    color: '#6b5644',
    fontSize: 12,
    fontWeight: '800',
  },

  topBar: {
    position: 'absolute',
    left: 16,
    right: 16,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    zIndex: 20,
  },
  topIconButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#fff8f0',
    borderWidth: 1,
    borderColor: '#e8d5c4',
    justifyContent: 'center',
    alignItems: 'center',
  },
  topTitleWrap: {
    alignItems: 'center',
    flex: 1,
    paddingHorizontal: 10,
  },
  topTitle: {
    fontSize: 14,
    fontWeight: '900',
    color: '#6b5644',
    letterSpacing: 0.2,
  },
  topSubtitle: {
    fontSize: 11,
    fontWeight: '700',
    color: '#8b6f47',
    marginTop: 2,
  },

  sideNav: {
    position: 'absolute',
    left: 12,
    right: 12,
    top: '50%',
    transform: [{ translateY: -24 }],
    flexDirection: 'row',
    justifyContent: 'space-between',
    zIndex: 20,
  },
  navButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: '#fff8f0',
    borderWidth: 1,
    borderColor: '#e8d5c4',
    justifyContent: 'center',
    alignItems: 'center',
  },
  navButtonDisabled: {
    opacity: 0.55,
  },

  bottomBar: {
    position: 'absolute',
    left: 0,
    right: 0,
    alignItems: 'center',
    zIndex: 20,
  },
  swipeHint: {
    color: '#8b6f47',
    fontSize: 11,
    fontWeight: '800',
    marginBottom: 10,
  },
  primaryAction: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: '#f97316',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#ea580c',
  },
  primaryActionText: {
    color: '#fff',
    fontWeight: '900',
    letterSpacing: 0.3,
  },
});
