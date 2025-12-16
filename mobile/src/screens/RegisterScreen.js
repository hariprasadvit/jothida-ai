import React, { useState, useEffect, useRef, useCallback } from 'react';
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
import { searchCities, POPULAR_CITIES, getLocationLabel } from '../data/cities';

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
// Location Picker Modal with comprehensive city database
const LocationPickerModal = ({ visible, onClose, onSelect, selectedPlace }) => {
  const [searchText, setSearchText] = useState('');
  const [filteredPlaces, setFilteredPlaces] = useState(POPULAR_CITIES);
  const [showManualEntry, setShowManualEntry] = useState(false);
  const [manualPlace, setManualPlace] = useState({ name: '', lat: '', lng: '' });
  const [isSearching, setIsSearching] = useState(false);

  // Debounced search
  useEffect(() => {
    if (searchText.trim() === '') {
      setFilteredPlaces(POPULAR_CITIES);
      setIsSearching(false);
      return;
    }

    setIsSearching(true);
    const timer = setTimeout(() => {
      const results = searchCities(searchText, 50);
      setFilteredPlaces(results);
      setIsSearching(false);
    }, 300);

    return () => clearTimeout(timer);
  }, [searchText]);

  const handleManualSubmit = () => {
    if (!manualPlace.name || !manualPlace.lat || !manualPlace.lng) {
      return;
    }
    const lat = parseFloat(manualPlace.lat);
    const lng = parseFloat(manualPlace.lng);
    if (isNaN(lat) || isNaN(lng)) {
      return;
    }
    onSelect({
      name: manualPlace.name,
      nameEn: manualPlace.name,
      lat: lat,
      lng: lng,
      isManual: true,
    });
    setShowManualEntry(false);
    setManualPlace({ name: '', lat: '', lng: '' });
    onClose();
  };

  const renderPlace = ({ item }) => {
    const locationLabel = getLocationLabel(item);
    const isSelected = selectedPlace?.nameEn === item.nameEn && selectedPlace?.lat === item.lat;

    return (
      <TouchableOpacity
        style={[styles.placeItem, isSelected && styles.placeItemSelected]}
        onPress={() => {
          onSelect(item);
          onClose();
        }}
      >
        <Ionicons
          name={item.country ? 'globe-outline' : 'location'}
          size={20}
          color={isSelected ? '#f97316' : '#6b7280'}
        />
        <View style={styles.placeTextContainer}>
          <Text style={[styles.placeName, isSelected && styles.placeNameSelected]}>
            {item.name}
          </Text>
          <Text style={styles.placeNameEn}>{locationLabel}</Text>
        </View>
        {isSelected && (
          <Ionicons name="checkmark-circle" size={20} color="#f97316" />
        )}
      </TouchableOpacity>
    );
  };

  if (showManualEntry) {
    return (
      <Modal visible={visible} animationType="slide" transparent>
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <TouchableOpacity onPress={() => setShowManualEntry(false)} style={styles.backBtn}>
                <Ionicons name="arrow-back" size={24} color="#6b7280" />
              </TouchableOpacity>
              <Text style={styles.modalTitle}>இடத்தை உள்ளிடுக</Text>
              <TouchableOpacity onPress={onClose} style={styles.modalCloseBtn}>
                <Ionicons name="close" size={24} color="#6b7280" />
              </TouchableOpacity>
            </View>

            <View style={styles.manualFormContainer}>
              <Text style={styles.manualHint}>
                உங்கள் கிராமம்/நகரம் பட்டியலில் இல்லையா? கீழே நேரடியாக உள்ளிடுங்கள்
              </Text>

              <View style={styles.manualInputGroup}>
                <Text style={styles.manualLabel}>இடத்தின் பெயர் *</Text>
                <TextInput
                  style={styles.manualInput}
                  value={manualPlace.name}
                  onChangeText={(text) => setManualPlace({ ...manualPlace, name: text })}
                  placeholder="உதா: என் கிராமம்"
                  placeholderTextColor="#9ca3af"
                />
              </View>

              <View style={styles.coordsRow}>
                <View style={[styles.manualInputGroup, { flex: 1, marginRight: 8 }]}>
                  <Text style={styles.manualLabel}>அட்சரேகை (Latitude) *</Text>
                  <TextInput
                    style={styles.manualInput}
                    value={manualPlace.lat}
                    onChangeText={(text) => setManualPlace({ ...manualPlace, lat: text })}
                    placeholder="உதா: 10.7905"
                    placeholderTextColor="#9ca3af"
                    keyboardType="decimal-pad"
                  />
                </View>
                <View style={[styles.manualInputGroup, { flex: 1, marginLeft: 8 }]}>
                  <Text style={styles.manualLabel}>தீர்க்கரேகை (Longitude) *</Text>
                  <TextInput
                    style={styles.manualInput}
                    value={manualPlace.lng}
                    onChangeText={(text) => setManualPlace({ ...manualPlace, lng: text })}
                    placeholder="உதா: 78.7047"
                    placeholderTextColor="#9ca3af"
                    keyboardType="decimal-pad"
                  />
                </View>
              </View>

              <Text style={styles.coordsHint}>
                Google Maps-ல் உங்கள் இடத்தை தேடி, coordinates-ஐ பெறலாம்
              </Text>

              <TouchableOpacity
                style={[
                  styles.manualSubmitBtn,
                  (!manualPlace.name || !manualPlace.lat || !manualPlace.lng) && styles.manualSubmitBtnDisabled
                ]}
                onPress={handleManualSubmit}
                disabled={!manualPlace.name || !manualPlace.lat || !manualPlace.lng}
              >
                <Text style={styles.manualSubmitText}>இடத்தை தேர்வு செய்</Text>
                <Ionicons name="checkmark-circle" size={20} color="#fff" />
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    );
  }

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
              placeholder="நகரம், மாநிலம், நாடு தேடுங்கள்..."
              placeholderTextColor="#9ca3af"
              autoCapitalize="none"
            />
            {isSearching ? (
              <ActivityIndicator size="small" color="#f97316" />
            ) : (
              searchText.length > 0 && (
                <TouchableOpacity onPress={() => setSearchText('')} activeOpacity={0.7}>
                  <Ionicons name="close-circle" size={20} color="#9ca3af" />
                </TouchableOpacity>
              )
            )}
          </View>

          {/* Results Count */}
          <View style={styles.sectionHeader}>
            <Ionicons name="star" size={16} color="#fbbf24" />
            <Ionicons name={searchText ? 'search' : 'star'} size={14} color="#f97316" />
            <Text style={styles.sectionTitle}>
              {searchText
                ? `${filteredPlaces.length} இடங்கள் கிடைத்தன`
                : 'பிரபலமான இடங்கள்'}
            </Text>
          </View>

          {/* Places List */}
          <FlatList
            data={filteredPlaces}
            keyExtractor={(item, index) => `${item.nameEn}-${item.lat}-${index}`}
            renderItem={renderPlace}
            style={styles.placesList}
            showsVerticalScrollIndicator={false}
            initialNumToRender={15}
            maxToRenderPerBatch={20}
            windowSize={10}
            ListEmptyComponent={
              <View style={styles.emptyContainer}>
                <Ionicons name="location-outline" size={56} color="#d1d5db" />
                <Text style={styles.emptyText}>இடம் கிடைக்கவில்லை</Text>
                <Text style={styles.emptySubText}>கீழே உள்ள "வேறு இடம்" பொத்தானை அழுத்தவும்</Text>
              </View>
            }
          />

          {/* Manual Entry Option */}
          <TouchableOpacity
            style={styles.manualEntryBtn}
            onPress={() => setShowManualEntry(true)}
          >
            <Ionicons name="create-outline" size={18} color="#f97316" />
            <Text style={styles.manualEntryText}>வேறு இடம் / கிராமம் உள்ளிட</Text>
            <Ionicons name="chevron-forward" size={18} color="#f97316" />
          </TouchableOpacity>
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
        latitude: formData.birthPlace.lat,
        longitude: formData.birthPlace.lng,
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
                    <Ionicons
                      name="man"
                      size={40}
                      color={formData.gender === 'male' ? '#fff' : '#6b7280'}
                      style={styles.genderIcon}
                    />
                    <Text style={[styles.genderText, formData.gender === 'male' && styles.genderTextActive]}>
                      ஆண்
                    </Text>
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
                      colors={['#f97316', '#ea580c']}
                      style={styles.genderGradient}
                    />
                  )}
                  <View style={styles.genderContent}>
                    <Ionicons
                      name="woman"
                      size={40}
                      color={formData.gender === 'female' ? '#fff' : '#6b7280'}
                      style={styles.genderIcon}
                    />
                    <Text style={[styles.genderText, formData.gender === 'female' && styles.genderTextActive]}>
                      பெண்
                    </Text>
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
                <View style={styles.webInputWrapper}>
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
                      boxSizing: 'border-box',
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
                </View>
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
                <View style={styles.webInputWrapper}>
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
                      boxSizing: 'border-box',
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
                </View>
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
    top: 2,
    right: 2,
  },
  webInputWrapper: {
    width: '100%',
    overflow: 'hidden',
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
    marginTop: 12,
  },
  emptySubText: {
    fontSize: 12,
    color: '#d1d5db',
    marginTop: 4,
    textAlign: 'center',
  },
  manualEntryBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 16,
    borderTopWidth: 1,
    borderTopColor: '#f3f4f6',
    backgroundColor: '#fff7ed',
  },
  manualEntryText: {
    fontSize: 14,
    color: '#f97316',
    fontWeight: '500',
  },
  // Manual Entry Form styles
  backBtn: {
    padding: 4,
  },
  manualFormContainer: {
    padding: 20,
  },
  manualHint: {
    fontSize: 13,
    color: '#6b7280',
    marginBottom: 20,
    textAlign: 'center',
    lineHeight: 20,
  },
  manualInputGroup: {
    marginBottom: 16,
  },
  manualLabel: {
    fontSize: 13,
    fontWeight: '600',
    color: '#374151',
    marginBottom: 6,
  },
  manualInput: {
    borderWidth: 2,
    borderColor: '#fed7aa',
    borderRadius: 10,
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 15,
    color: '#1f2937',
    backgroundColor: '#fff',
  },
  coordsRow: {
    flexDirection: 'row',
  },
  coordsHint: {
    fontSize: 11,
    color: '#9ca3af',
    marginBottom: 20,
    textAlign: 'center',
  },
  manualSubmitBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f97316',
    paddingVertical: 14,
    borderRadius: 12,
    gap: 8,
  },
  manualSubmitBtnDisabled: {
    opacity: 0.5,
  },
  manualSubmitText: {
    color: '#fff',
    fontSize: 15,
    fontWeight: '600',
  },
});
