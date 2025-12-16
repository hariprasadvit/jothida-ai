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
            <TouchableOpacity onPress={onClose} style={styles.modalCloseBtn}>
              <Ionicons name="close" size={24} color="#6b7280" />
            </TouchableOpacity>
          </View>

          {/* Search Input */}
          <View style={styles.searchContainer}>
            <Ionicons name="search" size={20} color="#9ca3af" />
            <TextInput
              style={styles.searchInput}
              value={searchText}
              onChangeText={setSearchText}
              placeholder="நகரம், மாநிலம், நாடு தேடுங்கள்..."
              placeholderTextColor="#9ca3af"
              autoCapitalize="none"
            />
            {isSearching && <ActivityIndicator size="small" color="#f97316" />}
            {searchText.length > 0 && !isSearching && (
              <TouchableOpacity onPress={() => setSearchText('')}>
                <Ionicons name="close-circle" size={20} color="#9ca3af" />
              </TouchableOpacity>
            )}
          </View>

          {/* Results Count */}
          <View style={styles.sectionHeader}>
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
                <Ionicons name="location-outline" size={48} color="#d1d5db" />
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

  // Animation refs
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(30)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, { toValue: 1, duration: 500, useNativeDriver: true }),
      Animated.timing(slideAnim, { toValue: 0, duration: 500, useNativeDriver: true, easing: Easing.out(Easing.ease) }),
    ]).start();
  }, []);

  const handleDateChange = (event, selectedDate) => {
    setShowDatePicker(Platform.OS === 'ios');
    if (selectedDate) {
      setFormData({ ...formData, birthDate: selectedDate });
    }
  };

  const handleTimeChange = (event, selectedTime) => {
    setShowTimePicker(Platform.OS === 'ios');
    if (selectedTime) {
      setFormData({ ...formData, birthTime: selectedTime });
    }
  };

  const handleRegister = async () => {
    if (!formData.name || !formData.gender || !formData.birthDate || !formData.birthPlace) {
      setError('அனைத்து தேவையான விவரங்களையும் நிரப்பவும்');
      return;
    }

    setLoading(true);
    setError('');

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
        colors={['#fff7ed', '#ffffff', '#fff7ed']}
        style={styles.gradient}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          keyboardShouldPersistTaps="handled"
        >
          <LinearGradient
            colors={['#f97316', '#ef4444', '#f97316']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.headerBar}
          />

          <Animated.View
            style={[
              styles.header,
              { opacity: fadeAnim, transform: [{ translateY: slideAnim }] }
            ]}
          >
            <Text style={styles.headerTitle}>புதிய பதிவு</Text>
            <Text style={styles.headerSubtitle}>உங்கள் ஜாதக விவரங்களை நிரப்பவும்</Text>
          </Animated.View>

          <Animated.View
            style={[
              styles.card,
              { opacity: fadeAnim, transform: [{ translateY: slideAnim }] }
            ]}
          >
            {/* Name */}
            <View style={styles.inputGroup}>
              <Text style={styles.label}>
                <Ionicons name="person" size={14} color="#f97316" /> பெயர் *
              </Text>
              <TextInput
                style={styles.input}
                value={formData.name}
                onChangeText={(text) => setFormData({ ...formData, name: text })}
                placeholder="உங்கள் பெயர்"
                placeholderTextColor="#9ca3af"
              />
            </View>

            {/* Gender */}
            <View style={styles.inputGroup}>
              <Text style={styles.label}>
                <Ionicons name="male-female" size={14} color="#f97316" /> பாலினம் *
              </Text>
              <View style={styles.genderContainer}>
                <TouchableOpacity
                  style={[
                    styles.genderBtn,
                    formData.gender === 'male' && styles.genderBtnActive,
                  ]}
                  onPress={() => setFormData({ ...formData, gender: 'male' })}
                >
                  <Text style={styles.genderIcon}>👨</Text>
                  <Text style={[styles.genderText, formData.gender === 'male' && styles.genderTextActive]}>ஆண்</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={[
                    styles.genderBtn,
                    formData.gender === 'female' && styles.genderBtnActive,
                  ]}
                  onPress={() => setFormData({ ...formData, gender: 'female' })}
                >
                  <Text style={styles.genderIcon}>👩</Text>
                  <Text style={[styles.genderText, formData.gender === 'female' && styles.genderTextActive]}>பெண்</Text>
                </TouchableOpacity>
              </View>
            </View>

            {/* Birth Date */}
            <View style={styles.inputGroup}>
              <Text style={styles.label}>
                <Ionicons name="calendar" size={14} color="#f97316" /> பிறந்த தேதி *
              </Text>
              {Platform.OS === 'web' ? (
                <input
                  type="date"
                  style={{
                    width: '100%',
                    padding: 14,
                    fontSize: 16,
                    border: '2px solid #fed7aa',
                    borderRadius: 12,
                    backgroundColor: '#fff',
                    color: '#1f2937',
                  }}
                  max={new Date().toISOString().split('T')[0]}
                  min="1920-01-01"
                  onChange={(e) => {
                    if (e.target.value) {
                      setFormData({ ...formData, birthDate: new Date(e.target.value) });
                    }
                  }}
                />
              ) : (
                <>
                  <TouchableOpacity
                    style={styles.pickerButton}
                    onPress={() => setShowDatePicker(true)}
                  >
                    <Ionicons name="calendar-outline" size={20} color="#6b7280" />
                    <Text style={[styles.pickerButtonText, !formData.birthDate && styles.placeholderText]}>
                      {formData.birthDate ? formatDate(formData.birthDate) : 'தேதியை தேர்வு செய்யவும்'}
                    </Text>
                    <Ionicons name="chevron-down" size={20} color="#6b7280" />
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
                <Ionicons name="time" size={14} color="#f97316" /> பிறந்த நேரம்
              </Text>
              {Platform.OS === 'web' ? (
                <input
                  type="time"
                  style={{
                    width: '100%',
                    padding: 14,
                    fontSize: 16,
                    border: '2px solid #fed7aa',
                    borderRadius: 12,
                    backgroundColor: '#fff',
                    color: '#1f2937',
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
                    style={styles.pickerButton}
                    onPress={() => setShowTimePicker(true)}
                  >
                    <Ionicons name="time-outline" size={20} color="#6b7280" />
                    <Text style={[styles.pickerButtonText, !formData.birthTime && styles.placeholderText]}>
                      {formData.birthTime ? formatTime(formData.birthTime) : 'நேரத்தை தேர்வு செய்யவும்'}
                    </Text>
                    <Ionicons name="chevron-down" size={20} color="#6b7280" />
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
                சரியான நேரம் தெரியவில்லை என்றால் காலி விடலாம்
              </Text>
            </View>

            {/* Birth Place */}
            <View style={styles.inputGroup}>
              <Text style={styles.label}>
                <Ionicons name="location" size={14} color="#f97316" /> பிறந்த இடம் *
              </Text>
              <TouchableOpacity
                style={styles.pickerButton}
                onPress={() => setShowLocationPicker(true)}
              >
                <Ionicons name="location-outline" size={20} color="#6b7280" />
                <Text style={[styles.pickerButtonText, !formData.birthPlace && styles.placeholderText]}>
                  {formData.birthPlace ? formData.birthPlace.name : 'இடத்தை தேர்வு செய்யவும்'}
                </Text>
                <Ionicons name="chevron-down" size={20} color="#6b7280" />
              </TouchableOpacity>
              {formData.birthPlace && (
                <View style={styles.selectedLocation}>
                  <Ionicons name="checkmark-circle" size={14} color="#16a34a" />
                  <Text style={styles.selectedLocationText}>
                    {formData.birthPlace.name} ({formData.birthPlace.nameEn})
                  </Text>
                </View>
              )}
            </View>

            {error ? (
              <View style={styles.errorContainer}>
                <Ionicons name="alert-circle" size={16} color="#dc2626" />
                <Text style={styles.errorText}>{error}</Text>
              </View>
            ) : null}

            <TouchableOpacity
              style={[styles.button, loading && styles.buttonDisabled]}
              onPress={handleRegister}
              disabled={loading}
            >
              {loading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <>
                  <Text style={styles.buttonText}>பதிவு செய்க</Text>
                  <Ionicons name="checkmark-circle" size={20} color="#fff" />
                </>
              )}
            </TouchableOpacity>
          </Animated.View>
        </ScrollView>
      </LinearGradient>

      {/* Location Picker Modal */}
      <LocationPickerModal
        visible={showLocationPicker}
        onClose={() => setShowLocationPicker(false)}
        onSelect={(place) => setFormData({ ...formData, birthPlace: place })}
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
    height: 8,
  },
  header: {
    alignItems: 'center',
    paddingVertical: 24,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#9a3412',
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#6b7280',
    marginTop: 4,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 20,
    padding: 24,
    marginHorizontal: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
    borderWidth: 1,
    borderColor: '#fed7aa',
  },
  inputGroup: {
    marginBottom: 20,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    color: '#374151',
    marginBottom: 8,
  },
  input: {
    borderWidth: 2,
    borderColor: '#fed7aa',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 14,
    fontSize: 16,
    color: '#1f2937',
    backgroundColor: '#fff',
  },
  genderContainer: {
    flexDirection: 'row',
    gap: 12,
  },
  genderBtn: {
    flex: 1,
    alignItems: 'center',
    padding: 16,
    borderWidth: 2,
    borderColor: '#fed7aa',
    borderRadius: 12,
    backgroundColor: '#fff',
  },
  genderBtnActive: {
    borderColor: '#f97316',
    backgroundColor: '#fff7ed',
  },
  genderIcon: {
    fontSize: 32,
  },
  genderText: {
    marginTop: 4,
    fontSize: 14,
    color: '#6b7280',
  },
  genderTextActive: {
    color: '#f97316',
    fontWeight: '600',
  },
  pickerButton: {
    flexDirection: 'row',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#fed7aa',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 14,
    backgroundColor: '#fff',
    gap: 10,
  },
  pickerButtonText: {
    flex: 1,
    fontSize: 16,
    color: '#1f2937',
  },
  placeholderText: {
    color: '#9ca3af',
  },
  hintText: {
    fontSize: 11,
    color: '#9ca3af',
    marginTop: 6,
    marginLeft: 4,
  },
  selectedLocation: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginTop: 8,
    paddingHorizontal: 4,
  },
  selectedLocationText: {
    fontSize: 12,
    color: '#16a34a',
  },
  errorContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fef2f2',
    padding: 12,
    borderRadius: 12,
    marginTop: 8,
    gap: 8,
  },
  errorText: {
    color: '#dc2626',
    fontSize: 14,
    flex: 1,
  },
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f97316',
    paddingVertical: 16,
    borderRadius: 12,
    marginTop: 20,
    gap: 8,
  },
  buttonDisabled: {
    opacity: 0.7,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },

  // Modal styles
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    paddingTop: 20,
    maxHeight: '80%',
  },
  modalHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    marginBottom: 16,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1f2937',
  },
  modalCloseBtn: {
    padding: 4,
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f3f4f6',
    marginHorizontal: 20,
    borderRadius: 12,
    paddingHorizontal: 14,
    paddingVertical: 10,
    gap: 10,
  },
  searchInput: {
    flex: 1,
    fontSize: 15,
    color: '#1f2937',
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 20,
    marginTop: 16,
    marginBottom: 10,
  },
  sectionTitle: {
    fontSize: 12,
    fontWeight: '600',
    color: '#6b7280',
  },
  placesList: {
    maxHeight: 350,
  },
  placeItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 14,
    paddingHorizontal: 20,
    gap: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f3f4f6',
  },
  placeItemSelected: {
    backgroundColor: '#fff7ed',
  },
  placeTextContainer: {
    flex: 1,
  },
  placeName: {
    fontSize: 15,
    color: '#1f2937',
    fontWeight: '500',
  },
  placeNameSelected: {
    color: '#f97316',
  },
  placeNameEn: {
    fontSize: 12,
    color: '#9ca3af',
    marginTop: 2,
  },
  emptyContainer: {
    alignItems: 'center',
    paddingVertical: 40,
  },
  emptyText: {
    fontSize: 14,
    color: '#9ca3af',
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
