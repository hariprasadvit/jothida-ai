import React, { useState } from 'react';
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
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { Picker } from '@react-native-picker/picker';
import { mobileAuthAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

const PLACES = [
  'சென்னை', 'மதுரை', 'கோயம்புத்தூர்', 'திருச்சி', 'சேலம்',
  'திருநெல்வேலி', 'ஈரோடு', 'வேலூர்', 'தஞ்சாவூர்', 'திண்டுக்கல்'
];

export default function RegisterScreen({ route, navigation }) {
  const { login } = useAuth();
  const { phoneNumber, otpCode } = route.params;

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    gender: '',
    birthDate: '',
    birthTime: '',
    birthPlace: '',
  });

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
        ...formData,
      });

      const profile = {
        name: result.user.name,
        phone: result.user.phone,
        rasi: result.user.rasi,
        nakshatra: result.user.nakshatra,
        birthDate: formData.birthDate,
        birthTime: formData.birthTime,
        birthPlace: formData.birthPlace,
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

          <View style={styles.header}>
            <Text style={styles.headerTitle}>புதிய பதிவு</Text>
            <Text style={styles.headerSubtitle}>உங்கள் விவரங்களை நிரப்பவும்</Text>
          </View>

          <View style={styles.card}>
            {/* Name */}
            <View style={styles.inputGroup}>
              <Text style={styles.label}>பெயர் *</Text>
              <TextInput
                style={styles.input}
                value={formData.name}
                onChangeText={(text) => setFormData({ ...formData, name: text })}
                placeholder="உங்கள் பெயர்"
              />
            </View>

            {/* Gender */}
            <View style={styles.inputGroup}>
              <Text style={styles.label}>பாலினம் *</Text>
              <View style={styles.genderContainer}>
                <TouchableOpacity
                  style={[
                    styles.genderBtn,
                    formData.gender === 'male' && styles.genderBtnActive,
                  ]}
                  onPress={() => setFormData({ ...formData, gender: 'male' })}
                >
                  <Text style={styles.genderIcon}>👨</Text>
                  <Text style={styles.genderText}>ஆண்</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={[
                    styles.genderBtn,
                    formData.gender === 'female' && styles.genderBtnActive,
                  ]}
                  onPress={() => setFormData({ ...formData, gender: 'female' })}
                >
                  <Text style={styles.genderIcon}>👩</Text>
                  <Text style={styles.genderText}>பெண்</Text>
                </TouchableOpacity>
              </View>
            </View>

            {/* Birth Date */}
            <View style={styles.inputGroup}>
              <Text style={styles.label}>பிறந்த தேதி * (YYYY-MM-DD)</Text>
              <TextInput
                style={styles.input}
                value={formData.birthDate}
                onChangeText={(text) => setFormData({ ...formData, birthDate: text })}
                placeholder="1990-01-15"
                keyboardType="numbers-and-punctuation"
              />
            </View>

            {/* Birth Time */}
            <View style={styles.inputGroup}>
              <Text style={styles.label}>பிறந்த நேரம் (HH:MM)</Text>
              <TextInput
                style={styles.input}
                value={formData.birthTime}
                onChangeText={(text) => setFormData({ ...formData, birthTime: text })}
                placeholder="08:30"
                keyboardType="numbers-and-punctuation"
              />
            </View>

            {/* Birth Place */}
            <View style={styles.inputGroup}>
              <Text style={styles.label}>பிறந்த இடம் *</Text>
              <View style={styles.pickerContainer}>
                <Picker
                  selectedValue={formData.birthPlace}
                  onValueChange={(value) => setFormData({ ...formData, birthPlace: value })}
                  style={styles.picker}
                >
                  <Picker.Item label="இடத்தை தேர்வு செய்யவும்" value="" />
                  {PLACES.map((place) => (
                    <Picker.Item key={place} label={place} value={place} />
                  ))}
                </Picker>
              </View>
            </View>

            {error ? (
              <View style={styles.errorContainer}>
                <Ionicons name="alert-circle" size={16} color="#dc2626" />
                <Text style={styles.errorText}>{error}</Text>
              </View>
            ) : null}

            <TouchableOpacity
              style={styles.button}
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
          </View>
        </ScrollView>
      </LinearGradient>
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
    marginBottom: 16,
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
    paddingVertical: 12,
    fontSize: 16,
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
    color: '#374151',
  },
  pickerContainer: {
    borderWidth: 2,
    borderColor: '#fed7aa',
    borderRadius: 12,
    overflow: 'hidden',
  },
  picker: {
    height: 50,
  },
  errorContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fef2f2',
    padding: 12,
    borderRadius: 12,
    marginTop: 8,
  },
  errorText: {
    color: '#dc2626',
    fontSize: 14,
    marginLeft: 8,
  },
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f97316',
    paddingVertical: 14,
    borderRadius: 12,
    marginTop: 20,
    gap: 8,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});
