import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  RefreshControl,
  Platform,
  Animated,
  Easing,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useAuth } from '../context/AuthContext';
import { mobileAPI } from '../services/api';

// Planet Tamil names
const planetTamilNames = {
  'Sun': 'சூரியன்',
  'Moon': 'சந்திரன்',
  'Mars': 'செவ்வாய்',
  'Mercury': 'புதன்',
  'Jupiter': 'குரு',
  'Venus': 'சுக்கிரன்',
  'Saturn': 'சனி',
  'Rahu': 'ராகு',
  'Ketu': 'கேது',
};

const getTamilDay = (dayIndex) => {
  const days = ['ஞாயிறு', 'திங்கள்', 'செவ்வாய்', 'புதன்', 'வியாழன்', 'வெள்ளி', 'சனி'];
  return days[dayIndex];
};

// Animated Card Component
const AnimatedCard = ({ children, delay = 0, style }) => {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const translateY = useRef(new Animated.Value(30)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 500,
        delay,
        useNativeDriver: true,
        easing: Easing.out(Easing.ease),
      }),
      Animated.timing(translateY, {
        toValue: 0,
        duration: 500,
        delay,
        useNativeDriver: true,
        easing: Easing.out(Easing.back(1.2)),
      }),
    ]).start();
  }, []);

  return (
    <Animated.View style={[style, { opacity: fadeAnim, transform: [{ translateY }] }]}>
      {children}
    </Animated.View>
  );
};

// Animated Progress Bar
const AnimatedProgressBar = ({ score, color, delay = 0 }) => {
  const widthAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(widthAnim, {
      toValue: score,
      duration: 1000,
      delay,
      useNativeDriver: false,
      easing: Easing.out(Easing.ease),
    }).start();
  }, [score]);

  return (
    <View style={styles.progressBar}>
      <Animated.View
        style={[
          styles.progressFill,
          {
            backgroundColor: color,
            width: widthAnim.interpolate({
              inputRange: [0, 100],
              outputRange: ['0%', '100%'],
            }),
          },
        ]}
      />
    </View>
  );
};

// Animated Score Circle
const AnimatedScoreCircle = ({ score }) => {
  const scaleAnim = useRef(new Animated.Value(0)).current;
  const rotateAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.spring(scaleAnim, {
        toValue: 1,
        friction: 4,
        tension: 50,
        useNativeDriver: true,
      }),
      Animated.timing(rotateAnim, {
        toValue: 1,
        duration: 800,
        useNativeDriver: true,
        easing: Easing.out(Easing.ease),
      }),
    ]).start();
  }, []);

  const rotate = rotateAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  return (
    <Animated.View
      style={[
        styles.scoreCircle,
        { transform: [{ scale: scaleAnim }, { rotate }] },
      ]}
    >
      <Text style={styles.scoreCircleText}>{score}%</Text>
    </Animated.View>
  );
};

// Animated Quick Action Button
const AnimatedQuickAction = ({ action, index, onPress }) => {
  const scaleAnim = useRef(new Animated.Value(1)).current;
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const translateY = useRef(new Animated.Value(20)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 400,
        delay: 300 + index * 100,
        useNativeDriver: true,
      }),
      Animated.spring(translateY, {
        toValue: 0,
        friction: 6,
        delay: 300 + index * 100,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  const handlePressIn = () => {
    Animated.spring(scaleAnim, {
      toValue: 0.92,
      useNativeDriver: true,
    }).start();
  };

  const handlePressOut = () => {
    Animated.spring(scaleAnim, {
      toValue: 1,
      friction: 3,
      useNativeDriver: true,
    }).start();
  };

  return (
    <Animated.View
      style={{
        flex: 1,
        opacity: fadeAnim,
        transform: [{ translateY }, { scale: scaleAnim }],
      }}
    >
      <TouchableOpacity
        style={styles.quickActionBtn}
        onPress={onPress}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        activeOpacity={1}
      >
        <Ionicons name={action.icon} size={24} color={action.color} />
        <Text style={styles.quickActionLabel}>{action.label}</Text>
      </TouchableOpacity>
    </Animated.View>
  );
};

// Animated Life Area Card
const AnimatedLifeAreaCard = ({ area, index }) => {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const scaleAnim = useRef(new Animated.Value(0.8)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 400,
        delay: 200 + index * 100,
        useNativeDriver: true,
      }),
      Animated.spring(scaleAnim, {
        toValue: 1,
        friction: 6,
        delay: 200 + index * 100,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  return (
    <Animated.View
      style={[
        styles.lifeAreaCard,
        { opacity: fadeAnim, transform: [{ scale: scaleAnim }] },
      ]}
    >
      <View style={styles.lifeAreaHeader}>
        <Ionicons name={area.icon} size={20} color={area.color} />
        <View style={[styles.lifeAreaBadge, { backgroundColor: area.score > 75 ? '#dcfce7' : '#fef3c7' }]}>
          <Text style={[styles.lifeAreaBadgeText, { color: area.score > 75 ? '#16a34a' : '#d97706' }]}>
            {area.score > 75 ? 'நல்லது' : 'சாதாரணம்'}
          </Text>
        </View>
      </View>
      <Text style={styles.lifeAreaName}>{area.name}</Text>
      <View style={styles.lifeAreaScoreRow}>
        <Text style={[styles.lifeAreaScore, { color: area.color }]}>{area.score}</Text>
        <Text style={styles.lifeAreaMax}>/100</Text>
      </View>
      <AnimatedProgressBar score={area.score} color={area.color} delay={400 + index * 100} />
    </Animated.View>
  );
};

// Pulsing Sparkle Icon
const PulsingSparkle = () => {
  const pulseAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.3,
          duration: 800,
          useNativeDriver: true,
          easing: Easing.inOut(Easing.ease),
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 800,
          useNativeDriver: true,
          easing: Easing.inOut(Easing.ease),
        }),
      ])
    ).start();
  }, []);

  return (
    <Animated.View style={{ transform: [{ scale: pulseAnim }] }}>
      <Ionicons name="sparkles" size={16} color="#ea580c" />
    </Animated.View>
  );
};

export default function DashboardScreen({ navigation }) {
  const { userProfile } = useAuth();
  const [currentTime, setCurrentTime] = useState(new Date());
  const [panchangam, setPanchangam] = useState(null);
  const [jathagam, setJathagam] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const insets = useSafeAreaInsets();
  const bottomPadding = Platform.OS === 'android' ? Math.max(insets.bottom, 80) : insets.bottom + 80;

  // Header animation
  const headerFadeAnim = useRef(new Animated.Value(0)).current;
  const headerSlideAnim = useRef(new Animated.Value(-20)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(headerFadeAnim, {
        toValue: 1,
        duration: 600,
        useNativeDriver: true,
      }),
      Animated.timing(headerSlideAnim, {
        toValue: 0,
        duration: 600,
        useNativeDriver: true,
        easing: Easing.out(Easing.ease),
      }),
    ]).start();
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    fetchData();
  }, [userProfile]);

  const fetchData = async () => {
    try {
      const panchangamData = await mobileAPI.getPanchangam();
      setPanchangam(panchangamData);

      if (userProfile?.birthDate && userProfile?.birthTime && userProfile?.birthPlace) {
        const jathagamData = await mobileAPI.getJathagam({
          name: userProfile.name,
          birthDate: userProfile.birthDate,
          birthTime: userProfile.birthTime,
          birthPlace: userProfile.birthPlace,
        });
        setJathagam(jathagamData);
      }
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    fetchData();
  };

  const getCurrentPeriod = () => {
    const hour = currentTime.getHours();
    if (hour >= 15 && hour < 17) {
      return { label: 'ராகு காலம்', color: '#dc2626', bg: '#fef2f2' };
    }
    if (hour >= 9 && hour < 11) {
      return { label: 'நல்ல நேரம்', color: '#16a34a', bg: '#f0fdf4' };
    }
    return { label: 'சாதாரண நேரம்', color: '#ea580c', bg: '#fff7ed' };
  };

  const period = getCurrentPeriod();
  const overallScore = 72;

  const lifeAreas = [
    { name: 'காதல்', icon: 'heart', score: 78, color: '#ec4899' },
    { name: 'தொழில்', icon: 'briefcase', score: 72, color: '#3b82f6' },
    { name: 'கல்வி', icon: 'school', score: 85, color: '#8b5cf6' },
    { name: 'குடும்பம்', icon: 'home', score: 80, color: '#10b981' },
  ];

  const quickActions = [
    { icon: 'chatbubbles', label: 'AI கேள்வி', screen: 'Chat', color: '#ea580c' },
    { icon: 'heart', label: 'பொருத்தம்', screen: 'Matching', color: '#ef4444' },
    { icon: 'calendar', label: 'முகூர்த்தம்', screen: 'Muhurtham', color: '#16a34a' },
  ];

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Animated.View style={{ transform: [{ rotate: '0deg' }] }}>
          <ActivityIndicator size="large" color="#f97316" />
        </Animated.View>
        <Text style={styles.loadingText}>ஜாதக தரவுகளை ஏற்றுகிறது...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <LinearGradient colors={['#fff7ed', '#ffffff', '#fff7ed']} style={styles.gradient}>
        <ScrollView
          contentContainerStyle={[styles.scrollContent, { paddingBottom: bottomPadding }]}
          refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={['#f97316']} />}
        >
          <LinearGradient
            colors={['#f97316', '#ef4444', '#f97316']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.headerBar}
          />

          {/* Header */}
          <Animated.View
            style={[
              styles.header,
              {
                opacity: headerFadeAnim,
                transform: [{ translateY: headerSlideAnim }],
              },
            ]}
          >
            <View>
              <View style={styles.logoRow}>
                <Text style={styles.omSymbol}>ॐ</Text>
                <Text style={styles.appTitle}>ஜோதிட AI</Text>
              </View>
              {userProfile && (
                <View style={styles.userInfo}>
                  <Text style={styles.greeting}>வணக்கம், {userProfile.name}</Text>
                  {userProfile.rasi && (
                    <Text style={styles.rasiInfo}>{userProfile.rasi} • {userProfile.nakshatra}</Text>
                  )}
                </View>
              )}
            </View>
            <View style={styles.timeContainer}>
              <Text style={styles.currentTime}>
                {currentTime.toLocaleTimeString('ta-IN', { hour: '2-digit', minute: '2-digit' })}
              </Text>
              <View style={[styles.periodBadge, { backgroundColor: period.bg }]}>
                <Text style={[styles.periodText, { color: period.color }]}>{period.label}</Text>
              </View>
            </View>
          </Animated.View>

          {/* Tamil Calendar */}
          <AnimatedCard delay={100} style={styles.card}>
            <View style={styles.cardHeader}>
              <Ionicons name="calendar" size={16} color="#ea580c" />
              <Text style={styles.cardTitle}>இன்றைய பஞ்சாங்கம்</Text>
              <Text style={styles.dayText}>{getTamilDay(currentTime.getDay())}</Text>
            </View>
            <View style={styles.panchangamGrid}>
              <View style={styles.panchangamItem}>
                <Text style={styles.panchangamLabel}>மாதம்</Text>
                <Text style={styles.panchangamValue}>{panchangam?.tamil_month || 'மார்கழி'}</Text>
              </View>
              <View style={styles.panchangamItem}>
                <Text style={styles.panchangamLabel}>திதி</Text>
                <Text style={styles.panchangamValue}>{panchangam?.tithi?.name || 'சப்தமி'}</Text>
              </View>
              <View style={styles.panchangamItem}>
                <Text style={styles.panchangamLabel}>நட்சத்திரம்</Text>
                <Text style={styles.panchangamValue}>{panchangam?.nakshatra?.tamil || 'உத்திரம்'}</Text>
              </View>
              <View style={styles.panchangamItem}>
                <Text style={styles.panchangamLabel}>யோகம்</Text>
                <Text style={styles.panchangamValue}>{panchangam?.yoga?.name || 'சித்த யோகம்'}</Text>
              </View>
            </View>
          </AnimatedCard>

          {/* Today's Score */}
          <AnimatedCard delay={200} style={styles.card}>
            <View style={styles.scoreRow}>
              <View>
                <Text style={styles.scoreLabel}>இன்றைய ஒட்டுமொத்த பலன்</Text>
                <View style={styles.scoreValue}>
                  <Text style={styles.scoreNumber}>{overallScore}</Text>
                  <Text style={styles.scoreMax}>/100</Text>
                  <View style={[styles.scoreBadge, { backgroundColor: overallScore >= 70 ? '#dcfce7' : '#fef3c7' }]}>
                    <Ionicons name="trending-up" size={14} color={overallScore >= 70 ? '#16a34a' : '#d97706'} />
                    <Text style={[styles.scoreBadgeText, { color: overallScore >= 70 ? '#16a34a' : '#d97706' }]}>
                      {overallScore >= 70 ? 'நல்லது' : 'சாதாரணம்'}
                    </Text>
                  </View>
                </View>
              </View>
              <AnimatedScoreCircle score={overallScore} />
            </View>

            <LinearGradient colors={['#fff7ed', '#fef3c7']} style={styles.insightBox}>
              <PulsingSparkle />
              <Text style={styles.insightText}>
                {jathagam?.dasha
                  ? `${planetTamilNames[jathagam.dasha.mahadasha] || jathagam.dasha.mahadasha} மகா தசை நடைபெறுகிறது.`
                  : 'குரு உங்கள் 9ம் வீட்டில் இருப்பதால் இன்று புதிய கற்றல் சிறப்பாக அமையும்.'
                }
              </Text>
            </LinearGradient>
          </AnimatedCard>

          {/* Life Areas */}
          <AnimatedCard delay={300} style={styles.card}>
            <View style={styles.cardHeader}>
              <Ionicons name="star" size={16} color="#ea580c" />
              <Text style={styles.cardTitle}>வாழ்க்கை துறைகள்</Text>
            </View>
            <View style={styles.lifeAreasGrid}>
              {lifeAreas.map((area, i) => (
                <AnimatedLifeAreaCard key={i} area={area} index={i} />
              ))}
            </View>
          </AnimatedCard>

          {/* Quick Actions */}
          <AnimatedCard delay={400} style={styles.card}>
            <Text style={styles.cardTitle}>விரைவு செயல்கள்</Text>
            <View style={styles.quickActionsGrid}>
              {quickActions.map((action, i) => (
                <AnimatedQuickAction
                  key={i}
                  action={action}
                  index={i}
                  onPress={() => navigation.navigate(action.screen)}
                />
              ))}
            </View>
          </AnimatedCard>

          {/* Current Dasha */}
          {jathagam?.dasha && (
            <AnimatedCard delay={500}>
              <LinearGradient colors={['#faf5ff', '#eef2ff']} style={[styles.card, styles.dashaCard, { marginHorizontal: 0 }]}>
                <View style={styles.cardHeader}>
                  <Ionicons name="sparkles" size={16} color="#7c3aed" />
                  <Text style={[styles.cardTitle, { color: '#6b21a8' }]}>நடப்பு தசா</Text>
                </View>
                <View style={styles.dashaGrid}>
                  <View style={styles.dashaItem}>
                    <Text style={styles.dashaLabel}>மகா தசை</Text>
                    <Text style={styles.dashaValue}>
                      {planetTamilNames[jathagam.dasha.mahadasha] || jathagam.dasha.mahadasha}
                    </Text>
                  </View>
                  <View style={styles.dashaItem}>
                    <Text style={styles.dashaLabel}>அந்தர தசை</Text>
                    <Text style={styles.dashaValue}>
                      {planetTamilNames[jathagam.dasha.antardasha] || jathagam.dasha.antardasha}
                    </Text>
                  </View>
                </View>
              </LinearGradient>
            </AnimatedCard>
          )}
        </ScrollView>
      </LinearGradient>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  gradient: { flex: 1 },
  scrollContent: { },
  loadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#fff7ed' },
  loadingText: { marginTop: 16, color: '#6b7280' },
  headerBar: { height: 4 },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start', padding: 16, backgroundColor: '#fff', borderBottomWidth: 1, borderBottomColor: '#fed7aa' },
  logoRow: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  omSymbol: { fontSize: 24, color: '#ea580c' },
  appTitle: { fontSize: 20, fontWeight: 'bold', color: '#9a3412' },
  userInfo: { marginTop: 4 },
  greeting: { fontSize: 14, color: '#6b7280' },
  rasiInfo: { fontSize: 12, color: '#ea580c' },
  timeContainer: { alignItems: 'flex-end' },
  currentTime: { fontSize: 18, fontFamily: 'monospace', color: '#1f2937' },
  periodBadge: { paddingHorizontal: 8, paddingVertical: 4, borderRadius: 12, marginTop: 4 },
  periodText: { fontSize: 10, fontWeight: '600' },
  card: { backgroundColor: '#fff', borderRadius: 16, padding: 16, marginHorizontal: 16, marginTop: 16, borderWidth: 1, borderColor: '#fed7aa' },
  cardHeader: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 12 },
  cardTitle: { fontSize: 14, fontWeight: '600', color: '#1f2937', flex: 1 },
  dayText: { fontSize: 12, color: '#6b7280' },
  panchangamGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  panchangamItem: { flex: 1, minWidth: '45%', backgroundColor: '#fff7ed', borderRadius: 12, padding: 12 },
  panchangamLabel: { fontSize: 10, color: '#6b7280', marginBottom: 4 },
  panchangamValue: { fontSize: 12, fontWeight: '600', color: '#1f2937' },
  scoreRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  scoreLabel: { fontSize: 12, color: '#6b7280' },
  scoreValue: { flexDirection: 'row', alignItems: 'baseline', gap: 4, marginTop: 4 },
  scoreNumber: { fontSize: 36, fontWeight: 'bold', color: '#ea580c' },
  scoreMax: { fontSize: 14, color: '#9ca3af' },
  scoreBadge: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 8, paddingVertical: 4, borderRadius: 12, marginLeft: 8, gap: 4 },
  scoreBadgeText: { fontSize: 12, fontWeight: '500' },
  scoreCircle: { width: 64, height: 64, borderRadius: 32, backgroundColor: '#fff7ed', borderWidth: 4, borderColor: '#ea580c', justifyContent: 'center', alignItems: 'center' },
  scoreCircleText: { fontSize: 16, fontWeight: 'bold', color: '#ea580c' },
  insightBox: { flexDirection: 'row', alignItems: 'flex-start', gap: 8, padding: 12, borderRadius: 12, marginTop: 16, borderWidth: 1, borderColor: '#fed7aa' },
  insightText: { flex: 1, fontSize: 13, color: '#374151', lineHeight: 20 },
  lifeAreasGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 12 },
  lifeAreaCard: { width: '47%', backgroundColor: '#fff', borderRadius: 12, padding: 12, borderWidth: 1, borderColor: '#fed7aa' },
  lifeAreaHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 },
  lifeAreaBadge: { paddingHorizontal: 8, paddingVertical: 2, borderRadius: 12 },
  lifeAreaBadgeText: { fontSize: 10 },
  lifeAreaName: { fontSize: 13, color: '#374151', fontWeight: '500' },
  lifeAreaScoreRow: { flexDirection: 'row', alignItems: 'baseline', marginTop: 4 },
  lifeAreaScore: { fontSize: 24, fontWeight: 'bold' },
  lifeAreaMax: { fontSize: 12, color: '#9ca3af', marginLeft: 2 },
  progressBar: { height: 6, backgroundColor: '#f3f4f6', borderRadius: 3, marginTop: 8, overflow: 'hidden' },
  progressFill: { height: 6, borderRadius: 3 },
  quickActionsGrid: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 12 },
  quickActionBtn: { flex: 1, alignItems: 'center', backgroundColor: '#fff', borderRadius: 12, padding: 16, marginHorizontal: 4, borderWidth: 1, borderColor: '#fed7aa' },
  quickActionLabel: { fontSize: 11, color: '#6b7280', marginTop: 8 },
  dashaCard: { borderColor: '#ddd6fe', marginHorizontal: 16 },
  dashaGrid: { flexDirection: 'row', gap: 12 },
  dashaItem: { flex: 1, backgroundColor: 'rgba(255,255,255,0.5)', borderRadius: 12, padding: 12 },
  dashaLabel: { fontSize: 11, color: '#6b7280' },
  dashaValue: { fontSize: 14, fontWeight: '600', color: '#7c3aed', marginTop: 4 },
});
