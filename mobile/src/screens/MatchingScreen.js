import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  TextInput,
  ActivityIndicator,
  Platform,
  Animated,
  Easing,
  Modal,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { Picker } from '@react-native-picker/picker';
import DateTimePicker from '@react-native-community/datetimepicker';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { mobileAPI, CITY_COORDINATES } from '../services/api';
import AppHeader from '../components/AppHeader';

const rasis = [
  { english: 'Mesha', tamil: 'மேஷம்' },
  { english: 'Vrishabha', tamil: 'ரிஷபம்' },
  { english: 'Mithuna', tamil: 'மிதுனம்' },
  { english: 'Kataka', tamil: 'கடகம்' },
  { english: 'Simha', tamil: 'சிம்மம்' },
  { english: 'Kanya', tamil: 'கன்னி' },
  { english: 'Tula', tamil: 'துலாம்' },
  { english: 'Vrischika', tamil: 'விருச்சிகம்' },
  { english: 'Dhanus', tamil: 'தனுசு' },
  { english: 'Makara', tamil: 'மகரம்' },
  { english: 'Kumbha', tamil: 'கும்பம்' },
  { english: 'Meena', tamil: 'மீனம்' },
];

const WEB_DATE_TIME_INPUT_STYLE = {
  padding: 12,
  borderRadius: 12,
  border: '1px solid #e8d5c4',
  fontSize: 14,
  width: '100%',
  backgroundColor: '#fef6ed',
  color: '#6b5644',
  outline: 'none',
  boxSizing: 'border-box',
  height: 48,
  lineHeight: '20px',
  display: 'block',
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

// Animated Heart for Loading
const AnimatedHeart = () => {
  const scaleAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(scaleAnim, { toValue: 1.2, duration: 500, useNativeDriver: true }),
        Animated.timing(scaleAnim, { toValue: 1, duration: 500, useNativeDriver: true }),
      ])
    ).start();
  }, []);

  return (
    <Animated.View style={{ transform: [{ scale: scaleAnim }] }}>
      <Ionicons name="heart" size={64} color="#ef4444" />
    </Animated.View>
  );
};

// Animated Progress Bar
const AnimatedProgressBar = ({ score, color, delay = 0 }) => {
  const widthAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(widthAnim, {
      toValue: score,
      duration: 800,
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
        friction: 5,
        tension: 80,
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
    <Animated.View style={[styles.scoreCircle, { transform: [{ scale: scaleAnim }, { rotate }] }]}>
      <Text style={styles.scoreCircleText}>{Math.round(score)}%</Text>
    </Animated.View>
  );
};

// Animated Button with pulse
const AnimatedButton = ({ onPress, disabled, children }) => {
  const scaleAnim = useRef(new Animated.Value(1)).current;
  const glowAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    if (!disabled) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(glowAnim, { toValue: 1, duration: 1000, useNativeDriver: true }),
          Animated.timing(glowAnim, { toValue: 0, duration: 1000, useNativeDriver: true }),
        ])
      ).start();
    }
  }, [disabled]);

  const handlePressIn = () => {
    Animated.spring(scaleAnim, { toValue: 0.95, useNativeDriver: true }).start();
  };

  const handlePressOut = () => {
    Animated.spring(scaleAnim, { toValue: 1, friction: 3, useNativeDriver: true }).start();
  };

  return (
    <Animated.View style={{ transform: [{ scale: scaleAnim }], opacity: glowAnim.interpolate({ inputRange: [0, 1], outputRange: [0.9, 1] }) }}>
      <TouchableOpacity
        style={[styles.calculateBtn, disabled && styles.disabledBtn]}
        onPress={onPress}
        disabled={disabled}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        activeOpacity={0.9}
      >
        {children}
      </TouchableOpacity>
    </Animated.View>
  );
};

// Floating Hearts Animation
const FloatingHearts = () => {
  const hearts = [0, 1, 2, 3, 4];
  const animations = hearts.map(() => ({
    translateY: useRef(new Animated.Value(0)).current,
    opacity: useRef(new Animated.Value(0)).current,
    translateX: useRef(new Animated.Value(0)).current,
  }));

  useEffect(() => {
    hearts.forEach((_, i) => {
      const startAnimation = () => {
        animations[i].translateY.setValue(0);
        animations[i].opacity.setValue(1);
        animations[i].translateX.setValue((Math.random() - 0.5) * 40);

        Animated.parallel([
          Animated.timing(animations[i].translateY, {
            toValue: -100,
            duration: 2000 + Math.random() * 1000,
            useNativeDriver: true,
            easing: Easing.out(Easing.ease),
          }),
          Animated.timing(animations[i].opacity, {
            toValue: 0,
            duration: 2000 + Math.random() * 1000,
            useNativeDriver: true,
          }),
        ]).start(() => {
          setTimeout(startAnimation, Math.random() * 2000);
        });
      };
      setTimeout(startAnimation, i * 400);
    });
  }, []);

  return (
    <View style={styles.floatingHeartsContainer}>
      {hearts.map((_, i) => (
        <Animated.View
          key={i}
          style={{
            position: 'absolute',
            transform: [{ translateY: animations[i].translateY }, { translateX: animations[i].translateX }],
            opacity: animations[i].opacity,
          }}
        >
          <Ionicons name="heart" size={16 + Math.random() * 8} color={`rgba(239, 68, 68, ${0.3 + Math.random() * 0.4})`} />
        </Animated.View>
      ))}
    </View>
  );
};

// Porutham Item with Animation
const AnimatedPoruthamItem = ({ porutham, index, isExpanded, onPress, statusStyle, language, t }) => {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(30)).current;
  const expandAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 400,
        delay: index * 80,
        useNativeDriver: true,
      }),
      Animated.timing(slideAnim, {
        toValue: 0,
        duration: 400,
        delay: index * 80,
        useNativeDriver: true,
        easing: Easing.out(Easing.back(1.1)),
      }),
    ]).start();
  }, []);

  useEffect(() => {
    Animated.timing(expandAnim, {
      toValue: isExpanded ? 1 : 0,
      duration: 200,
      useNativeDriver: false,
    }).start();
  }, [isExpanded]);

  return (
    <Animated.View style={{ opacity: fadeAnim, transform: [{ translateY: slideAnim }] }}>
      <TouchableOpacity
        style={[styles.poruthamItem, { backgroundColor: statusStyle.bg, borderColor: statusStyle.border }]}
        onPress={onPress}
        activeOpacity={0.7}
      >
        <View style={styles.poruthamHeader}>
          <View style={styles.poruthamLeft}>
            <Ionicons
              name={porutham.matched ? 'checkmark-circle' : 'close-circle'}
              size={18}
              color={porutham.matched ? '#16a34a' : '#dc2626'}
            />
            <Text style={styles.poruthamName}>{language === 'ta' ? porutham.name : (porutham.english || porutham.name)}</Text>
            {language !== 'ta' && porutham.name && <Text style={styles.poruthamEnglish}>({porutham.name})</Text>}
          </View>
          <View style={styles.poruthamRight}>
            <Text style={[styles.poruthamScore, { color: statusStyle.text }]}>{porutham.score}%</Text>
            <Ionicons name={isExpanded ? 'chevron-up' : 'chevron-down'} size={16} color="#9ca3af" />
          </View>
        </View>

        <AnimatedProgressBar score={porutham.score} color={statusStyle.text} delay={index * 80 + 200} />

        {isExpanded && (
          <View style={styles.poruthamExpanded}>
            <Text style={styles.poruthamDesc}>{language === 'ta' ? porutham.description : (porutham.description_en || porutham.description)}</Text>
            {porutham.remedy && (
              <View style={styles.remedyBox}>
                <Ionicons name="sparkles" size={12} color="#ea580c" />
                <Text style={styles.remedyText}>{t('remedy')}: {language === 'ta' ? porutham.remedy : (porutham.remedy_en || porutham.remedy)}</Text>
              </View>
            )}
          </View>
        )}
      </TouchableOpacity>
    </Animated.View>
  );
};

export default function MatchingScreen() {
  const { userProfile } = useAuth();
  const { t, language } = useLanguage();
  const insets = useSafeAreaInsets();
  const bottomPadding = Platform.OS === 'android' ? Math.max(insets.bottom, 80) : insets.bottom + 80;

  const [step, setStep] = useState('input'); // 'input' | 'loading' | 'result'
  const [groomData, setGroomData] = useState({
    name: '',
    birthDate: '',
    birthTime: '',
    birthPlace: '',
    rasi: '',
  });
  const [brideData, setBrideData] = useState({
    name: '',
    birthDate: '',
    birthTime: '',
    birthPlace: '',
    rasi: '',
  });
  const [matchResult, setMatchResult] = useState(null);
  const [error, setError] = useState(null);
  const [expandedPorutham, setExpandedPorutham] = useState(null);

  // Date picker states
  const [showGroomDatePicker, setShowGroomDatePicker] = useState(false);
  const [showBrideDatePicker, setShowBrideDatePicker] = useState(false);
  const [groomDate, setGroomDate] = useState(new Date(1990, 0, 1));
  const [brideDate, setBrideDate] = useState(new Date(1990, 0, 1));

  // Time picker states
  const [showGroomTimePicker, setShowGroomTimePicker] = useState(false);
  const [showBrideTimePicker, setShowBrideTimePicker] = useState(false);
  const [groomTime, setGroomTime] = useState(new Date(2000, 0, 1, 6, 0));
  const [brideTime, setBrideTime] = useState(new Date(2000, 0, 1, 6, 0));

  const formatDate = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  const formatTime = (date) => {
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}`;
  };

  const handleGroomDateChange = (event, selectedDate) => {
    setShowGroomDatePicker(false);
    if (selectedDate) {
      setGroomDate(selectedDate);
      setGroomData({ ...groomData, birthDate: formatDate(selectedDate) });
    }
  };

  const handleBrideDateChange = (event, selectedDate) => {
    setShowBrideDatePicker(false);
    if (selectedDate) {
      setBrideDate(selectedDate);
      setBrideData({ ...brideData, birthDate: formatDate(selectedDate) });
    }
  };

  const handleGroomTimeChange = (event, selectedTime) => {
    setShowGroomTimePicker(false);
    if (selectedTime) {
      setGroomTime(selectedTime);
      setGroomData({ ...groomData, birthTime: formatTime(selectedTime) });
    }
  };

  const handleBrideTimeChange = (event, selectedTime) => {
    setShowBrideTimePicker(false);
    if (selectedTime) {
      setBrideTime(selectedTime);
      setBrideData({ ...brideData, birthTime: formatTime(selectedTime) });
    }
  };

  useEffect(() => {
    if (userProfile) {
      setGroomData({
        name: userProfile.name || '',
        birthDate: userProfile.birthDate || '',
        birthTime: userProfile.birthTime || '',
        birthPlace: userProfile.birthPlace || 'Chennai',
        rasi: '',
      });
    }
  }, [userProfile]);

  const handleCalculate = async () => {
    setStep('loading');
    setError(null);

    try {
      const groomCoords = CITY_COORDINATES[groomData.birthPlace] || CITY_COORDINATES['Chennai'];
      const brideCoords = CITY_COORDINATES[brideData.birthPlace] || CITY_COORDINATES['Chennai'];

      const payload = {
        groom: {
          name: groomData.name,
          birth_date: groomData.birthDate,
          birth_time: groomData.birthTime,
          birth_place: groomData.birthPlace,
          latitude: groomCoords.lat,
          longitude: groomCoords.lon,
          rasi: groomData.rasi || null,
        },
        bride: {
          name: brideData.name,
          birth_date: brideData.birthDate,
          birth_time: brideData.birthTime,
          birth_place: brideData.birthPlace,
          latitude: brideCoords.lat,
          longitude: brideCoords.lon,
          rasi: brideData.rasi || null,
        }
      };

      const result = await mobileAPI.calculateMatching(payload);
      setMatchResult(result);
      setStep('result');
    } catch (err) {
      console.error('Matching error:', err);
      setError(t('matchingError'));
      setStep('input');
    }
  };

  const resetForm = () => {
    setStep('input');
    setMatchResult(null);
    setExpandedPorutham(null);
  };

  const getStatusStyle = (status) => {
    switch (status) {
      case 'excellent': return { bg: '#f0fdf4', border: '#bbf7d0', text: '#15803d' };
      case 'good': return { bg: '#eff6ff', border: '#bfdbfe', text: '#1d4ed8' };
      case 'warning': return { bg: '#fefce8', border: '#fef08a', text: '#a16207' };
      case 'critical': return { bg: '#fef2f2', border: '#fecaca', text: '#dc2626' };
      default: return { bg: '#f9fafb', border: '#e5e7eb', text: '#6b7280' };
    }
  };

  // Input Form
  if (step === 'input') {
    return (
      <View style={styles.container}>
        <LinearGradient colors={['#faf7f2', '#f5ede5', '#fff8f0']} style={styles.gradient}>
          <ScrollView contentContainerStyle={[styles.scrollContent, { paddingBottom: bottomPadding }]} showsVerticalScrollIndicator={false}>
            <AppHeader t={t} userProfile={userProfile} />

            <AnimatedCard delay={40} style={styles.sectionCard}>
              <View style={styles.sectionRow}>
                <View style={styles.sectionIcon}>
                  <Ionicons name="heart" size={18} color="#f97316" />
                </View>
                <View style={styles.sectionText}>
                  <Text style={styles.sectionTitle}>{t('marriageMatching')}</Text>
                  <Text style={styles.sectionSubtitle}>{t('tenPoruthamAnalysis')}</Text>
                </View>
              </View>
            </AnimatedCard>

            {error && (
              <View style={styles.errorBox}>
                <Ionicons name="alert-circle" size={16} color="#dc2626" />
                <Text style={styles.errorText}>{error}</Text>
              </View>
            )}

            {/* Groom Details */}
            <AnimatedCard delay={100} style={[styles.card, styles.groomCard]}>
              <View style={styles.cardHeader}>
                <Ionicons name="person" size={16} color="#2563eb" />
                <Text style={[styles.cardTitle, { color: '#1e40af' }]}>{t('groomDetails')}</Text>
              </View>

              <View style={styles.inputGroup}>
                <Text style={styles.label}>{t('name')} *</Text>
                <TextInput
                  style={styles.input}
                  value={groomData.name}
                  onChangeText={(text) => setGroomData({ ...groomData, name: text })}
                  placeholder={t('enterName')}
                />
              </View>

              <View style={styles.row}>
                <View style={styles.halfInput}>
                  <Text style={styles.label}>{t('birthDate')} *</Text>
                  {Platform.OS === 'web' ? (
                    <input
                      type="date"
                      style={WEB_DATE_TIME_INPUT_STYLE}
                      value={groomData.birthDate}
                      max={new Date().toISOString().split('T')[0]}
                      min="1920-01-01"
                      onChange={(e) => setGroomData({ ...groomData, birthDate: e.target.value })}
                    />
                  ) : (
                    <TouchableOpacity
                      style={styles.datePickerButton}
                      onPress={() => setShowGroomDatePicker(true)}
                    >
                      <Text style={groomData.birthDate ? styles.datePickerText : styles.datePickerPlaceholder}>
                        {groomData.birthDate || t('selectDatePlaceholder')}
                      </Text>
                      <Ionicons name="calendar" size={18} color="#6b7280" />
                    </TouchableOpacity>
                  )}
                </View>
                <View style={styles.halfInput}>
                  <Text style={styles.label}>{t('birthTime')} *</Text>
                  {Platform.OS === 'web' ? (
                    <input
                      type="time"
                      style={WEB_DATE_TIME_INPUT_STYLE}
                      value={groomData.birthTime}
                      onChange={(e) => setGroomData({ ...groomData, birthTime: e.target.value })}
                    />
                  ) : (
                    <TouchableOpacity
                      style={styles.datePickerButton}
                      onPress={() => setShowGroomTimePicker(true)}
                    >
                      <Text style={groomData.birthTime ? styles.datePickerText : styles.datePickerPlaceholder}>
                        {groomData.birthTime || t('selectTimePlaceholder')}
                      </Text>
                      <Ionicons name="time" size={18} color="#6b7280" />
                    </TouchableOpacity>
                  )}
                </View>
              </View>

              {showGroomDatePicker && Platform.OS === 'android' && (
                <DateTimePicker
                  value={groomDate}
                  mode="date"
                  display="default"
                  onChange={handleGroomDateChange}
                  maximumDate={new Date()}
                  minimumDate={new Date(1920, 0, 1)}
                />
              )}

              {showGroomTimePicker && Platform.OS === 'android' && (
                <DateTimePicker
                  value={groomTime}
                  mode="time"
                  display="default"
                  onChange={handleGroomTimeChange}
                  is24Hour={true}
                />
              )}

              <View style={styles.inputGroup}>
                <Text style={styles.label}>{t('birthPlace')} *</Text>
                <TextInput
                  style={styles.input}
                  value={groomData.birthPlace}
                  onChangeText={(text) => setGroomData({ ...groomData, birthPlace: text })}
                  placeholder={t('enterBirthPlace') || 'Enter birth place'}
                />
              </View>

              <View style={styles.inputGroup}>
                <Text style={styles.label}>{t('rasiOptional')}</Text>
                <View style={styles.pickerContainer}>
                  <Picker
                    selectedValue={groomData.rasi}
                    onValueChange={(value) => setGroomData({ ...groomData, rasi: value })}
                    style={styles.picker}
                  >
                    <Picker.Item label={t('autoCalculate')} value="" />
                    {rasis.map((r) => (
                      <Picker.Item key={r.english} label={language === 'ta' ? r.tamil : r.english} value={r.english} />
                    ))}
                  </Picker>
                </View>
              </View>
            </AnimatedCard>

            {/* Bride Details */}
            <AnimatedCard delay={200} style={[styles.card, styles.brideCard]}>
              <View style={styles.cardHeader}>
                <Ionicons name="person" size={16} color="#db2777" />
                <Text style={[styles.cardTitle, { color: '#be185d' }]}>{t('brideDetails')}</Text>
              </View>

              <View style={styles.inputGroup}>
                <Text style={styles.label}>{t('name')} *</Text>
                <TextInput
                  style={[styles.input, styles.brideInput]}
                  value={brideData.name}
                  onChangeText={(text) => setBrideData({ ...brideData, name: text })}
                  placeholder={t('enterName')}
                />
              </View>

              <View style={styles.row}>
                <View style={styles.halfInput}>
                  <Text style={styles.label}>{t('birthDate')} *</Text>
                  {Platform.OS === 'web' ? (
                    <input
                      type="date"
                      style={WEB_DATE_TIME_INPUT_STYLE}
                      value={brideData.birthDate}
                      max={new Date().toISOString().split('T')[0]}
                      min="1920-01-01"
                      onChange={(e) => setBrideData({ ...brideData, birthDate: e.target.value })}
                    />
                  ) : (
                    <TouchableOpacity
                      style={[styles.datePickerButton, styles.brideDatePicker]}
                      onPress={() => setShowBrideDatePicker(true)}
                    >
                      <Text style={brideData.birthDate ? styles.datePickerText : styles.datePickerPlaceholder}>
                        {brideData.birthDate || t('selectDatePlaceholder')}
                      </Text>
                      <Ionicons name="calendar" size={18} color="#db2777" />
                    </TouchableOpacity>
                  )}
                </View>
                <View style={styles.halfInput}>
                  <Text style={styles.label}>{t('birthTime')} *</Text>
                  {Platform.OS === 'web' ? (
                    <input
                      type="time"
                      style={WEB_DATE_TIME_INPUT_STYLE}
                      value={brideData.birthTime}
                      onChange={(e) => setBrideData({ ...brideData, birthTime: e.target.value })}
                    />
                  ) : (
                    <TouchableOpacity
                      style={[styles.datePickerButton, styles.brideDatePicker]}
                      onPress={() => setShowBrideTimePicker(true)}
                    >
                      <Text style={brideData.birthTime ? styles.datePickerText : styles.datePickerPlaceholder}>
                        {brideData.birthTime || t('selectTimePlaceholder')}
                      </Text>
                      <Ionicons name="time" size={18} color="#db2777" />
                    </TouchableOpacity>
                  )}
                </View>
              </View>

              {showBrideDatePicker && Platform.OS === 'android' && (
                <DateTimePicker
                  value={brideDate}
                  mode="date"
                  display="default"
                  onChange={handleBrideDateChange}
                  maximumDate={new Date()}
                  minimumDate={new Date(1920, 0, 1)}
                />
              )}

              {showBrideTimePicker && Platform.OS === 'android' && (
                <DateTimePicker
                  value={brideTime}
                  mode="time"
                  display="default"
                  onChange={handleBrideTimeChange}
                  is24Hour={true}
                />
              )}

              <View style={styles.inputGroup}>
                <Text style={styles.label}>{t('birthPlace')} *</Text>
                <TextInput
                  style={[styles.input, styles.brideInput]}
                  value={brideData.birthPlace}
                  onChangeText={(text) => setBrideData({ ...brideData, birthPlace: text })}
                  placeholder={t('enterBirthPlace') || 'Enter birth place'}
                />
              </View>

              <View style={styles.inputGroup}>
                <Text style={styles.label}>{t('rasiOptional')}</Text>
                <View style={[styles.pickerContainer, styles.bridePicker]}>
                  <Picker
                    selectedValue={brideData.rasi}
                    onValueChange={(value) => setBrideData({ ...brideData, rasi: value })}
                    style={styles.picker}
                  >
                    <Picker.Item label={t('autoCalculate')} value="" />
                    {rasis.map((r) => (
                      <Picker.Item key={r.english} label={language === 'ta' ? r.tamil : r.english} value={r.english} />
                    ))}
                  </Picker>
                </View>
              </View>
            </AnimatedCard>

            {/* Calculate Button */}
            <AnimatedCard delay={300}>
              <AnimatedButton
                onPress={handleCalculate}
                disabled={!groomData.name || !groomData.birthDate || !groomData.birthTime || !groomData.birthPlace ||
                         !brideData.name || !brideData.birthDate || !brideData.birthTime || !brideData.birthPlace}
              >
                <LinearGradient
                  colors={['#ef4444', '#ec4899']}
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 0 }}
                  style={styles.calculateBtnGradient}
                >
                  <Ionicons name="heart" size={20} color="#fff" />
                  <Text style={styles.calculateBtnText}>{t('calculateCompatibility')}</Text>
                </LinearGradient>
              </AnimatedButton>
            </AnimatedCard>
          </ScrollView>

          {/* iOS Date/Time Picker Modals */}
          {Platform.OS === 'ios' && (
            <>
              <Modal
                visible={showGroomDatePicker}
                transparent={true}
                animationType="slide"
              >
                <View style={styles.modalOverlay}>
                  <View style={styles.modalContent}>
                    <View style={styles.modalHeader}>
                      <Text style={styles.modalTitle}>{t('birthDate')} - {t('groomDetails')}</Text>
                      <TouchableOpacity onPress={() => setShowGroomDatePicker(false)}>
                        <Text style={styles.modalDone}>Done</Text>
                      </TouchableOpacity>
                    </View>
                    <DateTimePicker
                      value={groomDate}
                      mode="date"
                      display="spinner"
                      onChange={(event, date) => {
                        if (date) {
                          setGroomDate(date);
                          setGroomData({ ...groomData, birthDate: formatDate(date) });
                        }
                      }}
                      maximumDate={new Date()}
                      minimumDate={new Date(1920, 0, 1)}
                      style={{ height: 200 }}
                    />
                  </View>
                </View>
              </Modal>

              <Modal
                visible={showGroomTimePicker}
                transparent={true}
                animationType="slide"
              >
                <View style={styles.modalOverlay}>
                  <View style={styles.modalContent}>
                    <View style={styles.modalHeader}>
                      <Text style={styles.modalTitle}>{t('birthTime')} - {t('groomDetails')}</Text>
                      <TouchableOpacity onPress={() => setShowGroomTimePicker(false)}>
                        <Text style={styles.modalDone}>Done</Text>
                      </TouchableOpacity>
                    </View>
                    <DateTimePicker
                      value={groomTime}
                      mode="time"
                      display="spinner"
                      onChange={(event, time) => {
                        if (time) {
                          setGroomTime(time);
                          setGroomData({ ...groomData, birthTime: formatTime(time) });
                        }
                      }}
                      is24Hour={true}
                      style={{ height: 200 }}
                    />
                  </View>
                </View>
              </Modal>

              <Modal
                visible={showBrideDatePicker}
                transparent={true}
                animationType="slide"
              >
                <View style={styles.modalOverlay}>
                  <View style={styles.modalContent}>
                    <View style={styles.modalHeader}>
                      <Text style={styles.modalTitle}>{t('birthDate')} - {t('brideDetails')}</Text>
                      <TouchableOpacity onPress={() => setShowBrideDatePicker(false)}>
                        <Text style={styles.modalDone}>Done</Text>
                      </TouchableOpacity>
                    </View>
                    <DateTimePicker
                      value={brideDate}
                      mode="date"
                      display="spinner"
                      onChange={(event, date) => {
                        if (date) {
                          setBrideDate(date);
                          setBrideData({ ...brideData, birthDate: formatDate(date) });
                        }
                      }}
                      maximumDate={new Date()}
                      minimumDate={new Date(1920, 0, 1)}
                      style={{ height: 200 }}
                    />
                  </View>
                </View>
              </Modal>

              <Modal
                visible={showBrideTimePicker}
                transparent={true}
                animationType="slide"
              >
                <View style={styles.modalOverlay}>
                  <View style={styles.modalContent}>
                    <View style={styles.modalHeader}>
                      <Text style={styles.modalTitle}>{t('birthTime')} - {t('brideDetails')}</Text>
                      <TouchableOpacity onPress={() => setShowBrideTimePicker(false)}>
                        <Text style={styles.modalDone}>Done</Text>
                      </TouchableOpacity>
                    </View>
                    <DateTimePicker
                      value={brideTime}
                      mode="time"
                      display="spinner"
                      onChange={(event, time) => {
                        if (time) {
                          setBrideTime(time);
                          setBrideData({ ...brideData, birthTime: formatTime(time) });
                        }
                      }}
                      is24Hour={true}
                      style={{ height: 200 }}
                    />
                  </View>
                </View>
              </Modal>
            </>
          )}
        </LinearGradient>
      </View>
    );
  }

  // Loading
  if (step === 'loading') {
    return (
      <View style={styles.container}>
        <LinearGradient colors={['#faf7f2', '#f5ede5', '#fff8f0']} style={styles.gradient}>
          <View style={styles.loadingContainer}>
            <FloatingHearts />
            <AnimatedHeart />
            <ActivityIndicator size="large" color="#ec4899" style={{ marginTop: 16 }} />
            <Text style={styles.loadingText}>{t('calculatingPoruthams')}</Text>
            <Text style={styles.loadingSubtext}>{t('analyzingCompatibility')}</Text>
          </View>
        </LinearGradient>
      </View>
    );
  }

  // Results
  if (!matchResult) return null;

  const poruthams = matchResult.poruthams || [];
  const overallScore = matchResult.overall_score || 0;
  const matchedCount = poruthams.filter(p => p.matched).length;

  return (
    <View style={styles.container}>
      <LinearGradient colors={['#faf7f2', '#f5ede5', '#fff8f0']} style={styles.gradient}>
        <ScrollView contentContainerStyle={[styles.scrollContent, { paddingBottom: bottomPadding }]} showsVerticalScrollIndicator={false}>
          <AppHeader t={t} userProfile={userProfile} />

          <AnimatedCard delay={40} style={styles.sectionCard}>
            <View style={styles.sectionRow}>
              <View style={styles.sectionIcon}>
                <Ionicons name="heart" size={18} color="#f97316" />
              </View>
              <View style={styles.sectionText}>
                <Text style={styles.sectionTitle}>{t('marriageMatching')}</Text>
                <Text style={styles.sectionSubtitle}>{t('tenPoruthamAnalysis')}</Text>
              </View>
              <TouchableOpacity onPress={resetForm} style={styles.sectionActionBtn} activeOpacity={0.8}>
                <Ionicons name="refresh" size={18} color="#ea580c" />
              </TouchableOpacity>
            </View>
          </AnimatedCard>

          {/* Couple Names */}
          <AnimatedCard delay={0} style={styles.card}>
            <View style={styles.coupleRow}>
              <View style={styles.personBox}>
                <View style={[styles.personAvatar, { backgroundColor: '#3b82f6' }]}>
                  <Text style={styles.personAvatarText}>{groomData.name?.charAt(0) || 'அ'}</Text>
                </View>
                <Text style={styles.personName}>{groomData.name}</Text>
              </View>
              <AnimatedHeart />
              <View style={styles.personBox}>
                <View style={[styles.personAvatar, { backgroundColor: '#ec4899' }]}>
                  <Text style={styles.personAvatarText}>{brideData.name?.charAt(0) || 'ப'}</Text>
                </View>
                <Text style={styles.personName}>{brideData.name}</Text>
              </View>
            </View>
          </AnimatedCard>

          {/* Overall Score */}
          <AnimatedCard delay={100} style={styles.card}>
            <View style={styles.scoreRow}>
              <View>
                <Text style={styles.scoreLabel}>{t('overallCompatibility')}</Text>
                <View style={styles.scoreValueRow}>
                  <Text style={styles.scoreNumber}>{overallScore.toFixed(1)}</Text>
                  <Text style={styles.scoreMax}>/100</Text>
                </View>
                <View style={styles.matchInfo}>
                  <View style={styles.matchBadge}>
                    <Ionicons name="checkmark-circle" size={14} color="#16a34a" />
                    <Text style={styles.matchBadgeText}>{matchedCount}/10 {t('matchesOutOf10')}</Text>
                  </View>
                </View>
              </View>
              <AnimatedScoreCircle score={overallScore} />
            </View>

            {/* AI Verdict */}
            <View style={[styles.verdictBox, { backgroundColor: overallScore >= 70 ? '#f0fdf4' : '#fef3c7' }]}>
              <Ionicons name="sparkles" size={16} color={overallScore >= 70 ? '#16a34a' : '#d97706'} />
              <View style={{ flex: 1 }}>
                <Text style={[styles.verdictTitle, { color: overallScore >= 70 ? '#15803d' : '#a16207' }]}>
                  {t('aiVerdict')}: {overallScore >= 70 ? t('goodMatch') : t('needsAttention')}
                </Text>
                <Text style={styles.verdictText}>{matchResult.ai_verdict?.explanation || t('detailedAnalysisBelow')}</Text>
              </View>
            </View>
          </AnimatedCard>

          {/* 10 Poruthams */}
          <AnimatedCard delay={200} style={styles.card}>
            <View style={styles.cardHeader}>
              <Text style={styles.poruthamTitle}>{t('tenPoruthams')}</Text>
            </View>

            {poruthams.map((p, i) => {
              const statusStyle = getStatusStyle(p.status);
              const isExpanded = expandedPorutham === i;

              return (
                <AnimatedPoruthamItem
                  key={i}
                  porutham={p}
                  index={i}
                  isExpanded={isExpanded}
                  onPress={() => setExpandedPorutham(isExpanded ? null : i)}
                  statusStyle={statusStyle}
                  language={language}
                  t={t}
                />
              );
            })}
          </AnimatedCard>

          {/* Action Buttons */}
          <AnimatedCard delay={300} style={styles.actionRow}>
            <TouchableOpacity style={styles.newMatchBtn} onPress={resetForm} activeOpacity={0.7}>
              <Ionicons name="people" size={20} color="#ea580c" />
              <Text style={styles.newMatchBtnText}>{t('newMatching')}</Text>
            </TouchableOpacity>
          </AnimatedCard>
        </ScrollView>
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
  scrollContent: {
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 16,
    color: '#6b7280',
    fontSize: 14,
  },
  loadingSubtext: {
    marginTop: 8,
    color: '#9ca3af',
    fontSize: 12,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    paddingBottom: 40,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#e5e7eb',
  },
  modalTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#374151',
  },
  modalDone: {
    fontSize: 16,
    fontWeight: '600',
    color: '#ef4444',
  },
  floatingHeartsContainer: {
    position: 'absolute',
    width: 100,
    height: 100,
    alignItems: 'center',
    justifyContent: 'center',
  },
  sectionCard: {
    backgroundColor: '#fff8f0',
    borderRadius: 20,
    padding: 18,
    marginHorizontal: 16,
    marginTop: 16,
    borderWidth: 1,
    borderColor: '#e8d5c4',
    shadowColor: '#d4a574',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 10,
    elevation: 2,
  },
  sectionRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  sectionIcon: {
    width: 38,
    height: 38,
    borderRadius: 19,
    backgroundColor: '#f4e4d7',
    borderWidth: 1,
    borderColor: '#e8d5c4',
    justifyContent: 'center',
    alignItems: 'center',
  },
  sectionText: {
    flex: 1,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '800',
    color: '#6b5644',
    letterSpacing: 0.2,
  },
  sectionSubtitle: {
    fontSize: 12,
    color: '#8b6f47',
    marginTop: 2,
    fontWeight: '600',
  },
  sectionActionBtn: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#fef6ed',
    borderWidth: 1,
    borderColor: '#e8d5c4',
    justifyContent: 'center',
    alignItems: 'center',
  },
  headerBar: {
    height: 4,
  },
  header: {
    padding: 16,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#fed7aa',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  headerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#be123c',
  },
  headerSubtitle: {
    fontSize: 12,
    color: '#6b7280',
    marginTop: 2,
  },
  resetBtn: {
    padding: 8,
    backgroundColor: '#fff7ed',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#fed7aa',
  },
  errorBox: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginHorizontal: 16,
    marginTop: 16,
    padding: 12,
    backgroundColor: '#fef2f2',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#fecaca',
  },
  errorText: {
    flex: 1,
    color: '#dc2626',
    fontSize: 13,
  },
  card: {
    backgroundColor: '#fff8f0',
    borderRadius: 20,
    padding: 20,
    marginHorizontal: 16,
    marginTop: 20,
    borderWidth: 1,
    borderColor: '#e8d5c4',
    shadowColor: '#d4a574',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.06,
    shadowRadius: 10,
    elevation: 2,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    marginBottom: 12,
  },
  cardTitle: {
    fontSize: 14,
    fontWeight: '600',
  },
  groomCard: {
    borderColor: '#e8d5c4',
    borderLeftWidth: 4,
    borderLeftColor: '#3b82f6',
  },
  brideCard: {
    borderColor: '#e8d5c4',
    borderLeftWidth: 4,
    borderLeftColor: '#ec4899',
  },
  inputGroup: {
    marginBottom: 12,
  },
  label: {
    fontSize: 12,
    color: '#8b6f47',
    marginBottom: 6,
    fontWeight: '600',
  },
  input: {
    borderWidth: 1,
    borderColor: '#e8d5c4',
    borderRadius: 12,
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 14,
    backgroundColor: '#fef6ed',
    color: '#6b5644',
  },
  brideInput: {
    borderColor: '#e8d5c4',
  },
  datePickerButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    borderWidth: 1,
    borderColor: '#e8d5c4',
    borderRadius: 12,
    paddingHorizontal: 14,
    paddingVertical: 12,
    backgroundColor: '#fef6ed',
  },
  brideDatePicker: {
    borderColor: '#e8d5c4',
  },
  datePickerText: {
    fontSize: 14,
    color: '#6b5644',
    fontWeight: '600',
  },
  datePickerPlaceholder: {
    fontSize: 14,
    color: '#b8997a',
    fontWeight: '600',
  },
  row: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 12,
    marginBottom: 12,
  },
  halfInput: {
    flex: 1,
    minWidth: 0,
  },
  pickerContainer: {
    borderWidth: 1,
    borderColor: '#e8d5c4',
    borderRadius: 12,
    overflow: 'hidden',
    backgroundColor: '#fef6ed',
  },
  bridePicker: {
    borderColor: '#e8d5c4',
  },
  picker: {
    height: 50,
  },
  calculateBtn: {
    marginHorizontal: 16,
    marginTop: 24,
    borderRadius: 12,
    overflow: 'hidden',
  },
  calculateBtnGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 16,
  },
  calculateBtnText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  disabledBtn: {
    opacity: 0.5,
  },
  coupleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 16,
  },
  personBox: {
    alignItems: 'center',
  },
  personAvatar: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
  },
  personAvatarText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  personName: {
    fontSize: 13,
    fontWeight: '500',
    color: '#374151',
    marginTop: 8,
  },
  scoreRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  scoreLabel: {
    fontSize: 12,
    color: '#6b7280',
  },
  scoreValueRow: {
    flexDirection: 'row',
    alignItems: 'baseline',
    marginTop: 4,
  },
  scoreNumber: {
    fontSize: 42,
    fontWeight: 'bold',
    color: '#ef4444',
  },
  scoreMax: {
    fontSize: 18,
    color: '#9ca3af',
    marginLeft: 4,
  },
  matchInfo: {
    marginTop: 8,
  },
  matchBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  matchBadgeText: {
    fontSize: 12,
    color: '#16a34a',
  },
  scoreCircle: {
    width: 72,
    height: 72,
    borderRadius: 36,
    backgroundColor: '#fef2f2',
    borderWidth: 4,
    borderColor: '#ef4444',
    justifyContent: 'center',
    alignItems: 'center',
  },
  scoreCircleText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ef4444',
  },
  verdictBox: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 8,
    marginTop: 16,
    padding: 12,
    borderRadius: 12,
  },
  verdictTitle: {
    fontSize: 13,
    fontWeight: '600',
  },
  verdictText: {
    fontSize: 12,
    color: '#6b7280',
    marginTop: 4,
    lineHeight: 18,
  },
  poruthamTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#374151',
    textAlign: 'center',
  },
  poruthamItem: {
    borderRadius: 12,
    borderWidth: 1,
    padding: 12,
    marginTop: 8,
  },
  poruthamHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  poruthamLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  poruthamName: {
    fontSize: 13,
    fontWeight: '500',
    color: '#374151',
  },
  poruthamEnglish: {
    fontSize: 11,
    color: '#9ca3af',
  },
  poruthamRight: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  poruthamScore: {
    fontSize: 14,
    fontWeight: '600',
  },
  progressBar: {
    height: 6,
    backgroundColor: '#f4e4d7',
    borderRadius: 3,
    marginTop: 10,
  },
  progressFill: {
    height: 6,
    borderRadius: 3,
  },
  poruthamExpanded: {
    marginTop: 12,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#e5e7eb',
  },
  poruthamDesc: {
    fontSize: 12,
    color: '#6b7280',
    lineHeight: 18,
  },
  remedyBox: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 6,
    marginTop: 10,
    padding: 10,
    backgroundColor: '#fef6ed',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#e8d5c4',
  },
  remedyText: {
    flex: 1,
    fontSize: 11,
    color: '#9a3412',
  },
  actionRow: {
    marginHorizontal: 16,
    marginTop: 16,
  },
  newMatchBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    padding: 16,
    backgroundColor: '#fff8f0',
    borderRadius: 18,
    borderWidth: 1,
    borderColor: '#e8d5c4',
    shadowColor: '#d4a574',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 10,
    elevation: 2,
  },
  newMatchBtnText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#374151',
  },
});
