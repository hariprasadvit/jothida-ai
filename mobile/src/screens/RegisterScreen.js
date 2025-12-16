import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  Modal,
  FlatList,
  Animated,
  Easing,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import DateTimePicker from '@react-native-community/datetimepicker';
import Svg, { Circle, Defs, RadialGradient, Stop } from 'react-native-svg';
import { mobileAuthAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

// Popular Tamil Nadu cities with coordinates
const POPULAR_PLACES = [
  { name: 'சென்னை', nameEn: 'Chennai', lat: 13.0827, lng: 80.2707 },
  { name: 'மதுரை', nameEn: 'Madurai', lat: 9.9252, lng: 78.1198 },
  { name: 'கோயம்புத்தூர்', nameEn: 'Coimbatore', lat: 11.0168, lng: 76.9558 },
  { name: 'திருச்சி', nameEn: 'Tiruchirappalli', lat: 10.7905, lng: 78.7047 },
  { name: 'சேலம்', nameEn: 'Salem', lat: 11.6643, lng: 78.1460 },
  { name: 'திருநெல்வேலி', nameEn: 'Tirunelveli', lat: 8.7139, lng: 77.7567 },
  { name: 'ஈரோடு', nameEn: 'Erode', lat: 11.3410, lng: 77.7172 },
  { name: 'வேலூர்', nameEn: 'Vellore', lat: 12.9165, lng: 79.1325 },
  { name: 'தஞ்சாவூர்', nameEn: 'Thanjavur', lat: 10.7870, lng: 79.1378 },
  { name: 'திண்டுக்கல்', nameEn: 'Dindigul', lat: 10.3624, lng: 77.9695 },
  { name: 'நாகர்கோவில்', nameEn: 'Nagercoil', lat: 8.1833, lng: 77.4119 },
  { name: 'காஞ்சிபுரம்', nameEn: 'Kanchipuram', lat: 12.8342, lng: 79.7036 },
  { name: 'குடந்தை', nameEn: 'Kumbakonam', lat: 10.9617, lng: 79.3881 },
  { name: 'கரூர்', nameEn: 'Karur', lat: 10.9601, lng: 78.0766 },
  { name: 'தூத்துக்குடி', nameEn: 'Thoothukudi', lat: 8.7642, lng: 78.1348 },
  { name: 'நெல்லை', nameEn: 'Nellai', lat: 8.7139, lng: 77.7567 },
  { name: 'விருதுநகர்', nameEn: 'Virudhunagar', lat: 9.5680, lng: 77.9624 },
  { name: 'ராமநாதபுரம்', nameEn: 'Ramanathapuram', lat: 9.3639, lng: 78.8395 },
  { name: 'புதுக்கோட்டை', nameEn: 'Pudukkottai', lat: 10.3833, lng: 78.8001 },
  { name: 'சிவகங்கை', nameEn: 'Sivaganga', lat: 9.8433, lng: 78.4809 },
];

// Format date for display
const formatDate = (date) => {
  if (!date) return '';
  const d = new Date(date);
  const day = d.getDate();
  const month = d.getMonth() + 1;
  const year = d.getFullYear();

  const tamilMonths = [
    'ஜனவரி', 'பிப்ரவரி', 'மார்ச்', 'ஏப்ரல்', 'மே', 'ஜூன்',
    'ஜூலை', 'ஆகஸ்ட்', 'செப்டம்பர்', 'அக்டோபர்', 'நவம்பர்', 'டிசம்பர்'
  ];

  return `${day} ${tamilMonths[d.getMonth()]} ${year}`;
};

// Format time for display
const formatTime = (date) => {
  if (!date) return '';
  const d = new Date(date);
  const hours = d.getHours();
  const minutes = d.getMinutes();
  const ampm = hours >= 12 ? 'மாலை' : 'காலை';
  const displayHours = hours % 12 || 12;
  return `${displayHours}:${minutes.toString().padStart(2, '0')} ${ampm}`;
};

// Format for API (YYYY-MM-DD)
const formatDateForAPI = (date) => {
  if (!date) return '';
  const d = new Date(date);
  return `${d.getFullYear()}-${(d.getMonth() + 1).toString().padStart(2, '0')}-${d.getDate().toString().padStart(2, '0')}`;
};

// Format time for API (HH:MM)
const formatTimeForAPI = (date) => {
  if (!date) return '';
  const d = new Date(date);
  return `${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`;
};

// Glowing Circle Component
const GlowCircle = ({ size = 140, color = '#f97316' }) => (
  <Svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} style={styles.glowCircle}>
    <Defs>
      <RadialGradient id="glow" cx="50%" cy="50%" r="50%">
        <Stop offset="0%" stopColor={color} stopOpacity="0.3" />
        <Stop offset="50%" stopColor={color} stopOpacity="0.15" />
        <Stop offset="100%" stopColor={color} stopOpacity="0" />
      </RadialGradient>
    </Defs>
    <Circle cx={size / 2} cy={size / 2} r={size / 2} fill="url(#glow)" />
  </Svg>
);

// Location Picker Modal
const LocationPickerModal = ({ visible, onClose, onSelect, selectedPlace }) => {
  const [searchText, setSearchText] = useState('');
  const [filteredPlaces, setFilteredPlaces] = useState(POPULAR_PLACES);

  useEffect(() => {
    if (searchText.trim() === '') {
      setFilteredPlaces(POPULAR_PLACES);
    } else {
      const filtered = POPULAR_PLACES.filter(
        place =>
          place.name.includes(searchText) ||
          place.nameEn.toLowerCase().includes(searchText.toLowerCase())
      );
      setFilteredPlaces(filtered);
    }
  }, [searchText]);

  const renderPlace = ({ item }) => (
    <TouchableOpacity
      style={[styles.placeItem, selectedPlace?.nameEn === item.nameEn && styles.placeItemSelected]}
      onPress={() => {
        onSelect(item);
        onClose();
      }}
      activeOpacity={0.7}
    >
      <View style={[styles.placeIcon, selectedPlace?.nameEn === item.nameEn && styles.placeIconSelected]}>
        <Ionicons
          name="location"
          size={20}
          color={selectedPlace?.nameEn === item.nameEn ? '#fff' : '#f97316'}
        />
      </View>
      <View style={styles.placeTextContainer}>
        <Text style={[styles.placeName, selectedPlace?.nameEn === item.nameEn && styles.placeNameSelected]}>
          {item.name}
        </Text>
        <Text style={styles.placeNameEn}>{item.nameEn}</Text>
      </View>
      {selectedPlace?.nameEn === item.nameEn && (
        <Ionicons name="checkmark-circle" size={24} color="#f97316" />
      )}
    </TouchableOpacity>
  );

  return (
    <Modal visible={visible} animationType="slide" transparent>
      <View style={styles.modalOverlay}>
        <View style={styles.modalContent}>
          <View style={styles.modalHeader}>
            <Text style={styles.modalTitle}>பிறந்த இடம் தேர்வு</Text>
            <TouchableOpacity onPress={onClose} style={styles.modalCloseBtn} activeOpacity={0.7}>
              <Ionicons name="close-circle" size={28} color="#6b7280" />
            </TouchableOpacity>
          </View>

          {/* Search Input */}
          <View style={styles.searchContainer}>
            <Ionicons name="search" size={20} color="#f97316" />
            <TextInput
              style={styles.searchInput}
              value={searchText}
              onChangeText={setSearchText}
              placeholder="இடத்தை தேடுங்கள்..."
              placeholderTextColor="#9ca3af"
            />
            {searchText.length > 0 && (
              <TouchableOpacity onPress={() => setSearchText('')} activeOpacity={0.7}>
                <Ionicons name="close-circle" size={20} color="#9ca3af" />
              </TouchableOpacity>
            )}
          </View>

          {/* Popular Label */}
          <View style={styles.sectionHeader}>
            <Ionicons name="star" size={16} color="#fbbf24" />
            <Text style={styles.sectionTitle}>
              {searchText ? 'தேடல் முடிவுகள்' : 'பிரபலமான இடங்கள்'}
            </Text>
          </View>

          {/* Places List */}
          <FlatList
            data={filteredPlaces}
            keyExtractor={(item) => item.nameEn}
            renderItem={renderPlace}
            style={styles.placesList}
            showsVerticalScrollIndicator={false}
            ListEmptyComponent={
              <View style={styles.emptyContainer}>
                <Ionicons name="location-outline" size={56} color="#d1d5db" />
                <Text style={styles.emptyText}>இடம் கிடைக்கவில்லை</Text>
              </View>
            }
          />
        </View>
      </View>
    </Modal>
  );
};

export default function RegisterScreen({ route, navigation }) {
  const { login } = useAuth();
  const { phoneNumber, otpCode } = route.params;

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    gender: '',
    birthDate: null,
    birthTime: null,
    birthPlace: null,
  });

  const [showDatePicker, setShowDatePicker] = useState(false);
  const [showTimePicker, setShowTimePicker] = useState(false);
  const [showLocationPicker, setShowLocationPicker] = useState(false);
  const [focusedField, setFocusedField] = useState('');

  // Animation refs
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(40)).current;
  const buttonScale = useRef(new Animated.Value(1)).current;
  const errorShake = useRef(new Animated.Value(0)).current;
  const successPulse = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, { 
        toValue: 1, 
        duration: 600, 
        useNativeDriver: true,
        easing: Easing.out(Easing.ease)
      }),
      Animated.spring(slideAnim, { 
        toValue: 0, 
        friction: 8,
        tension: 40,
        useNativeDriver: true
      }),
    ]).start();
  }, []);

  // Calculate completion percentage
  const completionPercentage = () => {
    let filled = 0;
    if (formData.name) filled++;
    if (formData.gender) filled++;
    if (formData.birthDate) filled++;
    if (formData.birthPlace) filled++;
    return (filled / 4) * 100;
  };

  const handleDateChange = (event, selectedDate) => {
    setShowDatePicker(Platform.OS === 'ios');
    if (selectedDate) {
      setFormData({ ...formData, birthDate: selectedDate });
      animateSuccess();
    }
  };

  const handleTimeChange = (event, selectedTime) => {
    setShowTimePicker(Platform.OS === 'ios');
    if (selectedTime) {
      setFormData({ ...formData, birthTime: selectedTime });
    }
  };

  const animateSuccess = () => {
    Animated.sequence([
      Animated.timing(successPulse, {
        toValue: 1.05,
        duration: 150,
        useNativeDriver: true,
      }),
      Animated.timing(successPulse, {
        toValue: 1,
        duration: 150,
        useNativeDriver: true,
      }),
    ]).start();
  };

  const animateError = () => {
    Animated.sequence([
      Animated.timing(errorShake, {
        toValue: 10,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.timing(errorShake, {
        toValue: -10,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.timing(errorShake, {
        toValue: 10,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.timing(errorShake, {
        toValue: 0,
        duration: 100,
        useNativeDriver: true,
      }),
    ]).start();
  };

  const handleRegister = async () => {
    if (!formData.name || !formData.gender || !formData.birthDate || !formData.birthPlace) {
      setError('அனைத்து தேவையான விவரங்களையும் நிரப்பவும்');
      animateError();
      return;
    }

    setLoading(true);
    setError('');

    // Button press animation
    Animated.sequence([
      Animated.timing(buttonScale, {
        toValue: 0.95,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.spring(buttonScale, {
        toValue: 1,
        friction: 3,
        useNativeDriver: true,
      }),
    ]).start();

    try {
      const result = await mobileAuthAPI.register({
        phoneNumber,
        otpCode,
        name: formData.name,
        gender: formData.gender,
        birthDate: formatDateForAPI(formData.birthDate),
        birthTime: formData.birthTime ? formatTimeForAPI(formData.birthTime) : '',
        birthPlace: formData.birthPlace.nameEn,
      });

      const profile = {
        name: result.user.name,
        phone: result.user.phone,
        rasi: result.user.rasi,
        nakshatra: result.user.nakshatra,
        birthDate: formatDateForAPI(formData.birthDate),
        birthTime: formData.birthTime ? formatTimeForAPI(formData.birthTime) : '',
        birthPlace: formData.birthPlace.nameEn,
      };

      await login(result.token, profile);
    } catch (err) {
      setError(err.response?.data?.detail || 'பதிவு செய்வதில் பிழை');
      animateError();
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <LinearGradient
        colors={['#fef3c7', '#fed7aa', '#fdba74']}
        style={styles.gradient}
        start={{ x: 0.5, y: 0 }}
        end={{ x: 0.5, y: 1 }}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
        >
          {/* Decorative Top Bar */}
          <LinearGradient
            colors={['#f97316', '#ea580c', '#c2410c']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.headerBar}
          >
            <View style={styles.progressBarContainer}>
              <Animated.View 
                style={[
                  styles.progressBar,
                  { width: `${completionPercentage()}%` }
                ]}
              >
                <LinearGradient
                  colors={['#fbbf24', '#fde047']}
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 0 }}
                  style={styles.progressGradient}
                />
              </Animated.View>
            </View>
          </LinearGradient>

          <Animated.View
            style={[
              styles.header,
              { opacity: fadeAnim, transform: [{ translateY: slideAnim }] }
            ]}
          >
            <View style={styles.iconContainer}>
              <View style={styles.iconGlowWrapper}>
                <GlowCircle size={100} color="#f97316" />
              </View>
              <LinearGradient
                colors={['#f97316', '#ea580c']}
                style={styles.headerIcon}
              >
                <Ionicons name="person-add" size={32} color="#fff" />
              </LinearGradient>
            </View>
            <Text style={styles.headerTitle}>புதிய பதிவு</Text>
            <Text style={styles.headerSubtitle}>உங்கள் ஜாதக விவரங்களை நிரப்பவும்</Text>
            <View style={styles.progressTextContainer}>
              <Text style={styles.progressText}>{Math.round(completionPercentage())}% நிறைவு</Text>
            </View>
          </Animated.View>

          <Animated.View
            style={[
              styles.card,
              { 
                opacity: fadeAnim, 
                transform: [
                  { translateY: slideAnim },
                  { translateX: errorShake }
                ] 
              }
            ]}
          >
            {/* Name */}
            <View style={styles.inputGroup}>
              <Text style={styles.label}>
                <Ionicons name="person" size={16} color="#f97316" /> பெயர் *
              </Text>
              <View style={[
                styles.inputWrapper,
                focusedField === 'name' && styles.inputWrapperFocused,
                formData.name && styles.inputWrapperFilled
              ]}>
                <TextInput
                  style={styles.input}
                  value={formData.name}
                  onChangeText={(text) => {
                    setFormData({ ...formData, name: text });
                    if (text) animateSuccess();
                  }}
                  onFocus={() => setFocusedField('name')}
                  onBlur={() => setFocusedField('')}
                  placeholder="உங்கள் பெயர்"
                  placeholderTextColor="#9ca3af"
                />
                {formData.name && (
                  <Ionicons name="checkmark-circle" size={20} color="#16a34a" />
                )}
              </View>
            </View>

            {/* Gender */}
            <View style={styles.inputGroup}>
              <Text style={styles.label}>
                <Ionicons name="male-female" size={16} color="#f97316" /> பாலினம் *
              </Text>
              <View style={styles.genderContainer}>
                <TouchableOpacity
                  style={[
                    styles.genderBtn,
                    formData.gender === 'male' && styles.genderBtnActive,
                  ]}
                  onPress={() => {
                    setFormData({ ...formData, gender: 'male' });
                    animateSuccess();
                  }}
                  activeOpacity={0.8}
                >
                  {formData.gender === 'male' && (
                    <LinearGradient
                      colors={['#3b82f6', '#2563eb']}
                      style={styles.genderGradient}
                    />
                  )}
                  <View style={styles.genderContent}>
                    <Text style={styles.genderIcon}>👨</Text>
                    <Text style={[styles.genderText, formData.gender === 'male' && styles.genderTextActive]}>
                      ஆண்
                    </Text>
                    {formData.gender === 'male' && (
                      <Ionicons name="checkmark-circle" size={18} color="#fff" style={styles.genderCheck} />
                    )}
                  </View>
                </TouchableOpacity>
                <TouchableOpacity
                  style={[
                    styles.genderBtn,
                    formData.gender === 'female' && styles.genderBtnActive,
                  ]}
                  onPress={() => {
                    setFormData({ ...formData, gender: 'female' });
                    animateSuccess();
                  }}
                  activeOpacity={0.8}
                >
                  {formData.gender === 'female' && (
                    <LinearGradient
                      colors={['#ec4899', '#db2777']}
                      style={styles.genderGradient}
                    />
                  )}
                  <View style={styles.genderContent}>
                    <Text style={styles.genderIcon}>👩</Text>
                    <Text style={[styles.genderText, formData.gender === 'female' && styles.genderTextActive]}>
                      பெண்
                    </Text>
                    {formData.gender === 'female' && (
                      <Ionicons name="checkmark-circle" size={18} color="#fff" style={styles.genderCheck} />
                    )}
                  </View>
                </TouchableOpacity>
              </View>
            </View>

            {/* Birth Date */}
            <View style={styles.inputGroup}>
              <Text style={styles.label}>
                <Ionicons name="calendar" size={16} color="#f97316" /> பிறந்த தேதி *
              </Text>
              {Platform.OS === 'web' ? (
                <input
                  type="date"
                  style={{
                    width: '100%',
                    padding: 16,
                    fontSize: 16,
                    border: '2px solid #fed7aa',
                    borderRadius: 14,
                    backgroundColor: '#fff',
                    color: '#1f2937',
                    fontWeight: '500',
                  }}
                  max={new Date().toISOString().split('T')[0]}
                  min="1920-01-01"
                  onChange={(e) => {
                    if (e.target.value) {
                      setFormData({ ...formData, birthDate: new Date(e.target.value) });
                      animateSuccess();
                    }
                  }}
                />
              ) : (
                <>
                  <TouchableOpacity
                    style={[
                      styles.pickerButton,
                      formData.birthDate && styles.pickerButtonFilled
                    ]}
                    onPress={() => setShowDatePicker(true)}
                    activeOpacity={0.8}
                  >
                    <View style={styles.pickerIconWrapper}>
                      <Ionicons name="calendar-outline" size={22} color={formData.birthDate ? '#f97316' : '#6b7280'} />
                    </View>
                    <Text style={[styles.pickerButtonText, !formData.birthDate && styles.placeholderText]}>
                      {formData.birthDate ? formatDate(formData.birthDate) : 'தேதியை தேர்வு செய்யவும்'}
                    </Text>
                    {formData.birthDate ? (
                      <Ionicons name="checkmark-circle" size={22} color="#16a34a" />
                    ) : (
                      <Ionicons name="chevron-down" size={22} color="#6b7280" />
                    )}
                  </TouchableOpacity>
                  {showDatePicker && (
                    <DateTimePicker
                      value={formData.birthDate || new Date(1990, 0, 1)}
                      mode="date"
                      display={Platform.OS === 'ios' ? 'spinner' : 'default'}
                      onChange={handleDateChange}
                      maximumDate={new Date()}
                      minimumDate={new Date(1920, 0, 1)}
                    />
                  )}
                </>
              )}
            </View>

            {/* Birth Time */}
            <View style={styles.inputGroup}>
              <Text style={styles.label}>
                <Ionicons name="time" size={16} color="#f97316" /> பிறந்த நேரம்
              </Text>
              {Platform.OS === 'web' ? (
                <input
                  type="time"
                  style={{
                    width: '100%',
                    padding: 16,
                    fontSize: 16,
                    border: '2px solid #fed7aa',
                    borderRadius: 14,
                    backgroundColor: '#fff',
                    color: '#1f2937',
                    fontWeight: '500',
                  }}
                  onChange={(e) => {
                    if (e.target.value) {
                      const [hours, minutes] = e.target.value.split(':');
                      const date = new Date();
                      date.setHours(parseInt(hours), parseInt(minutes));
                      setFormData({ ...formData, birthTime: date });
                    }
                  }}
                />
              ) : (
                <>
                  <TouchableOpacity
                    style={[
                      styles.pickerButton,
                      formData.birthTime && styles.pickerButtonFilled
                    ]}
                    onPress={() => setShowTimePicker(true)}
                    activeOpacity={0.8}
                  >
                    <View style={styles.pickerIconWrapper}>
                      <Ionicons name="time-outline" size={22} color={formData.birthTime ? '#f97316' : '#6b7280'} />
                    </View>
                    <Text style={[styles.pickerButtonText, !formData.birthTime && styles.placeholderText]}>
                      {formData.birthTime ? formatTime(formData.birthTime) : 'நேரத்தை தேர்வு செய்யவும்'}
                    </Text>
                    {formData.birthTime ? (
                      <Ionicons name="checkmark-circle" size={22} color="#16a34a" />
                    ) : (
                      <Ionicons name="chevron-down" size={22} color="#6b7280" />
                    )}
                  </TouchableOpacity>
                  {showTimePicker && (
                    <DateTimePicker
                      value={formData.birthTime || new Date()}
                      mode="time"
                      display={Platform.OS === 'ios' ? 'spinner' : 'default'}
                      onChange={handleTimeChange}
                      is24Hour={false}
                    />
                  )}
                </>
              )}
              <Text style={styles.hintText}>
                💡 சரியான நேரம் தெரியவில்லை என்றால் காலி விடலாம்
              </Text>
            </View>

            {/* Birth Place */}
            <View style={styles.inputGroup}>
              <Text style={styles.label}>
                <Ionicons name="location" size={16} color="#f97316" /> பிறந்த இடம் *
              </Text>
              <TouchableOpacity
                style={[
                  styles.pickerButton,
                  formData.birthPlace && styles.pickerButtonFilled
                ]}
                onPress={() => setShowLocationPicker(true)}
                activeOpacity={0.8}
              >
                <View style={styles.pickerIconWrapper}>
                  <Ionicons name="location-outline" size={22} color={formData.birthPlace ? '#f97316' : '#6b7280'} />
                </View>
                <Text style={[styles.pickerButtonText, !formData.birthPlace && styles.placeholderText]}>
                  {formData.birthPlace ? formData.birthPlace.name : 'இடத்தை தேர்வு செய்யவும்'}
                </Text>
                {formData.birthPlace ? (
                  <Ionicons name="checkmark-circle" size={22} color="#16a34a" />
                ) : (
                  <Ionicons name="chevron-down" size={22} color="#6b7280" />
                )}
              </TouchableOpacity>
              {formData.birthPlace && (
                <View style={styles.selectedLocation}>
                  <Ionicons name="pin" size={14} color="#16a34a" />
                  <Text style={styles.selectedLocationText}>
                    {formData.birthPlace.nameEn}
                  </Text>
                </View>
              )}
            </View>

            {error ? (
              <View style={styles.errorContainer}>
                <Ionicons name="alert-circle" size={18} color="#dc2626" />
                <Text style={styles.errorText}>{error}</Text>
              </View>
            ) : null}

            <Animated.View style={{ transform: [{ scale: buttonScale }] }}>
              <TouchableOpacity
                style={[styles.button, loading && styles.buttonDisabled]}
                onPress={handleRegister}
                disabled={loading}
                activeOpacity={0.9}
              >
                <LinearGradient
                  colors={['#f97316', '#ea580c', '#c2410c']}
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 0 }}
                  style={styles.buttonGradient}
                >
                  {loading ? (
                    <ActivityIndicator color="#fff" size="small" />
                  ) : (
                    <>
                      <Ionicons name="rocket" size={22} color="#fff" />
                      <Text style={styles.buttonText}>பதிவு செய்க</Text>
                      <Ionicons name="arrow-forward" size={22} color="#fff" />
                    </>
                  )}
                </LinearGradient>
              </TouchableOpacity>
            </Animated.View>
          </Animated.View>
        </ScrollView>
      </LinearGradient>

      {/* Location Picker Modal */}
      <LocationPickerModal
        visible={showLocationPicker}
        onClose={() => setShowLocationPicker(false)}
        onSelect={(place) => {
          setFormData({ ...formData, birthPlace: place });
          animateSuccess();
        }}
        selectedPlace={formData.birthPlace}
      />
    </KeyboardAvoidingView>
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
    flexGrow: 1,
    paddingBottom: 40,
  },
  headerBar: {
    height: 6,
  },
  progressBarContainer: {
    height: 6,
    backgroundColor: 'rgba(255,255,255,0.3)',
  },
  progressBar: {
    height: 6,
    overflow: 'hidden',
  },
  progressGradient: {
    height: 6,
  },
  header: {
    alignItems: 'center',
    paddingTop: 32,
    paddingBottom: 24,
  },
  iconContainer: {
    position: 'relative',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
  },
  iconGlowWrapper: {
    position: 'absolute',
  },
  glowCircle: {
    position: 'absolute',
  },
  headerIcon: {
    width: 72,
    height: 72,
    borderRadius: 36,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#f97316',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 12,
    elevation: 8,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#7c2d12',
    marginBottom: 6,
  },
  headerSubtitle: {
    fontSize: 15,
    color: '#92400e',
    marginBottom: 12,
  },
  progressTextContainer: {
    backgroundColor: 'rgba(255,255,255,0.9)',
    paddingHorizontal: 16,
    paddingVertical: 6,
    borderRadius: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  progressText: {
    fontSize: 13,
    fontWeight: '700',
    color: '#f97316',
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 24,
    padding: 24,
    marginHorizontal: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.15,
    shadowRadius: 16,
    elevation: 8,
    borderWidth: 1,
    borderColor: 'rgba(251, 191, 36, 0.3)',
  },
  inputGroup: {
    marginBottom: 24,
  },
  label: {
    fontSize: 15,
    fontWeight: '700',
    color: '#374151',
    marginBottom: 10,
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#fed7aa',
    borderRadius: 14,
    paddingHorizontal: 16,
    paddingVertical: 4,
    backgroundColor: '#fff',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  inputWrapperFocused: {
    borderColor: '#f97316',
    shadowColor: '#f97316',
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 4,
  },
  inputWrapperFilled: {
    borderColor: '#16a34a',
    backgroundColor: '#f0fdf4',
  },
  input: {
    flex: 1,
    paddingVertical: 14,
    fontSize: 16,
    color: '#1f2937',
    fontWeight: '500',
  },
  genderContainer: {
    flexDirection: 'row',
    gap: 14,
  },
  genderBtn: {
    flex: 1,
    position: 'relative',
    alignItems: 'center',
    paddingVertical: 20,
    paddingHorizontal: 16,
    borderWidth: 2,
    borderColor: '#fed7aa',
    borderRadius: 16,
    backgroundColor: '#fff',
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.08,
    shadowRadius: 6,
    elevation: 3,
  },
  genderBtnActive: {
    borderColor: 'transparent',
    shadowColor: '#000',
    shadowOpacity: 0.2,
    shadowRadius: 10,
    elevation: 6,
  },
  genderGradient: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
  },
  genderContent: {
    alignItems: 'center',
  },
  genderIcon: {
    fontSize: 40,
    marginBottom: 8,
  },
  genderText: {
    fontSize: 15,
    color: '#6b7280',
    fontWeight: '600',
  },
  genderTextActive: {
    color: '#fff',
    fontWeight: '700',
  },
  genderCheck: {
    position: 'absolute',
    top: -28,
    right: -10,
  },
  pickerButton: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#fed7aa',
    borderRadius: 14,
    paddingHorizontal: 16,
    paddingVertical: 16,
    backgroundColor: '#fff',
    gap: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  pickerButtonFilled: {
    borderColor: '#16a34a',
    backgroundColor: '#f0fdf4',
  },
  pickerIconWrapper: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#fef3c7',
    alignItems: 'center',
    justifyContent: 'center',
  },
  pickerButtonText: {
    flex: 1,
    fontSize: 16,
    color: '#1f2937',
    fontWeight: '500',
  },
  placeholderText: {
    color: '#9ca3af',
    fontWeight: '400',
  },
  hintText: {
    fontSize: 12,
    color: '#9ca3af',
    marginTop: 8,
    marginLeft: 4,
    fontStyle: 'italic',
  },
  selectedLocation: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginTop: 10,
    paddingHorizontal: 12,
    paddingVertical: 6,
    backgroundColor: '#f0fdf4',
    borderRadius: 8,
    alignSelf: 'flex-start',
  },
  selectedLocationText: {
    fontSize: 12,
    color: '#16a34a',
    fontWeight: '600',
  },
  errorContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fef2f2',
    padding: 14,
    borderRadius: 14,
    marginBottom: 20,
    gap: 10,
    borderWidth: 1,
    borderColor: '#fecaca',
  },
  errorText: {
    color: '#dc2626',
    fontSize: 14,
    flex: 1,
    fontWeight: '600',
  },
  button: {
    borderRadius: 16,
    overflow: 'hidden',
    shadowColor: '#f97316',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.4,
    shadowRadius: 12,
    elevation: 8,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 18,
    gap: 12,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '700',
    letterSpacing: 0.5,
  },

  // Modal styles
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.6)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderTopLeftRadius: 28,
    borderTopRightRadius: 28,
    paddingTop: 24,
    maxHeight: '85%',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: -4 },
    shadowOpacity: 0.3,
    shadowRadius: 16,
    elevation: 16,
  },
  modalHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 24,
    marginBottom: 20,
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1f2937',
  },
  modalCloseBtn: {
    padding: 4,
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fef3c7',
    marginHorizontal: 24,
    borderRadius: 16,
    paddingHorizontal: 16,
    paddingVertical: 12,
    gap: 12,
    borderWidth: 2,
    borderColor: '#fde68a',
  },
  searchInput: {
    flex: 1,
    fontSize: 16,
    color: '#1f2937',
    fontWeight: '500',
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingHorizontal: 24,
    marginTop: 20,
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 13,
    fontWeight: '700',
    color: '#6b7280',
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  placesList: {
    maxHeight: 400,
  },
  placeItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 16,
    paddingHorizontal: 24,
    gap: 14,
    borderBottomWidth: 1,
    borderBottomColor: '#f3f4f6',
  },
  placeItemSelected: {
    backgroundColor: '#fff7ed',
    borderLeftWidth: 4,
    borderLeftColor: '#f97316',
  },
  placeIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#fef3c7',
    alignItems: 'center',
    justifyContent: 'center',
  },
  placeIconSelected: {
    backgroundColor: '#f97316',
  },
  placeTextContainer: {
    flex: 1,
  },
  placeName: {
    fontSize: 16,
    color: '#1f2937',
    fontWeight: '600',
    marginBottom: 2,
  },
  placeNameSelected: {
    color: '#ea580c',
    fontWeight: '700',
  },
  placeNameEn: {
    fontSize: 13,
    color: '#9ca3af',
    fontWeight: '500',
  },
  emptyContainer: {
    alignItems: 'center',
    paddingVertical: 60,
  },
  emptyText: {
    fontSize: 15,
    color: '#9ca3af',
    marginTop: 16,
    fontWeight: '500',
  },
});
