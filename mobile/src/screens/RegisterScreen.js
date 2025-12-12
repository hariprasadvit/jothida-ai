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
    >
      <Ionicons
        name="location"
        size={20}
        color={selectedPlace?.nameEn === item.nameEn ? '#f97316' : '#6b7280'}
      />
      <View style={styles.placeTextContainer}>
        <Text style={[styles.placeName, selectedPlace?.nameEn === item.nameEn && styles.placeNameSelected]}>
          {item.name}
        </Text>
        <Text style={styles.placeNameEn}>{item.nameEn}</Text>
      </View>
      {selectedPlace?.nameEn === item.nameEn && (
        <Ionicons name="checkmark-circle" size={20} color="#f97316" />
      )}
    </TouchableOpacity>
  );

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
              placeholder="இடத்தை தேடுங்கள்..."
              placeholderTextColor="#9ca3af"
            />
            {searchText.length > 0 && (
              <TouchableOpacity onPress={() => setSearchText('')}>
                <Ionicons name="close-circle" size={20} color="#9ca3af" />
              </TouchableOpacity>
            )}
          </View>

          {/* Popular Label */}
          <View style={styles.sectionHeader}>
            <Ionicons name="star" size={14} color="#f97316" />
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
                <Ionicons name="location-outline" size={48} color="#d1d5db" />
                <Text style={styles.emptyText}>இடம் கிடைக்கவில்லை</Text>
              </View>
            }
          />

          {/* Manual Entry Option */}
          <TouchableOpacity style={styles.manualEntryBtn}>
            <Ionicons name="create-outline" size={18} color="#6b7280" />
            <Text style={styles.manualEntryText}>வேறு இடம் தட்டச்சு செய்ய</Text>
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
  manualEntryBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 16,
    borderTopWidth: 1,
    borderTopColor: '#f3f4f6',
  },
  manualEntryText: {
    fontSize: 13,
    color: '#6b7280',
  },
});
