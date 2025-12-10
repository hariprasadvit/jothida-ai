import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { mobileAuthAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function LoginScreen({ navigation }) {
  const { login } = useAuth();
  const [step, setStep] = useState('phone'); // phone, otp
  const [phoneNumber, setPhoneNumber] = useState('');
  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const [demoOtp, setDemoOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const otpRefs = useRef([]);

  const handlePhoneChange = (text) => {
    const cleaned = text.replace(/\D/g, '');
    if (cleaned.length <= 10) {
      setPhoneNumber(cleaned);
    }
  };

  const handleSendOTP = async () => {
    if (phoneNumber.length !== 10) {
      setError('10 இலக்க மொபைல் எண்ணை உள்ளிடவும்');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const fullPhone = `+91${phoneNumber}`;
      const result = await mobileAuthAPI.sendOTP(fullPhone);

      if (result.demo_otp) {
        setDemoOtp(result.demo_otp);
      }

      setStep('otp');
    } catch (err) {
      console.error('OTP Send Error:', err);
      console.error('Error response:', err.response?.data);
      console.error('Error message:', err.message);

      if (err.message === 'Network Error') {
        setError('சேவையகத்தை அணுக முடியவில்லை. இணைய இணைப்பை சரிபார்க்கவும்.');
      } else if (err.code === 'ECONNABORTED') {
        setError('நேரம் முடிந்தது. மீண்டும் முயற்சிக்கவும்.');
      } else {
        setError(err.response?.data?.detail || 'OTP அனுப்புவதில் பிழை');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleOtpChange = (index, value) => {
    if (value.length > 1) value = value[0];
    if (!/^\d*$/.test(value)) return;

    const newOtp = [...otp];
    newOtp[index] = value;
    setOtp(newOtp);

    if (value && index < 5) {
      otpRefs.current[index + 1]?.focus();
    }
  };

  const handleOtpKeyPress = (index, key) => {
    if (key === 'Backspace' && !otp[index] && index > 0) {
      otpRefs.current[index - 1]?.focus();
    }
  };

  const handleVerifyOTP = async () => {
    const otpCode = otp.join('');
    if (otpCode.length !== 6) {
      setError('6 இலக்க OTP ஐ உள்ளிடவும்');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const fullPhone = `+91${phoneNumber}`;
      const result = await mobileAuthAPI.verifyOTP(fullPhone, otpCode);

      if (result.is_new_user) {
        navigation.navigate('Register', {
          phoneNumber: fullPhone,
          otpCode: otpCode,
        });
      } else {
        const profile = {
          name: result.user.name,
          phone: result.user.phone,
          rasi: result.user.rasi,
          nakshatra: result.user.nakshatra,
          birthDate: result.user.birth_date,
          birthTime: result.user.birth_time,
          birthPlace: result.user.birth_place,
          latitude: result.user.latitude,
          longitude: result.user.longitude,
        };
        await login(result.token, profile);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'OTP சரிபார்ப்பில் பிழை');
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
          {/* Header Bar */}
          <LinearGradient
            colors={['#f97316', '#ef4444', '#f97316']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.headerBar}
          />

          {/* Om Symbol */}
          <View style={styles.omContainer}>
            <Text style={styles.omSymbol}>ॐ</Text>
            <Text style={styles.appTitle}>ஜோதிட AI</Text>
            <Text style={styles.appSubtitle}>மொபைல் உள்நுழைவு</Text>
          </View>

          {/* Phone Step */}
          {step === 'phone' && (
            <View style={styles.card}>
              <View style={styles.iconContainer}>
                <Ionicons name="phone-portrait-outline" size={32} color="#f97316" />
              </View>
              <Text style={styles.cardTitle}>மொபைல் எண்</Text>
              <Text style={styles.cardSubtitle}>உங்கள் மொபைல் எண்ணை உள்ளிடவும்</Text>

              <View style={styles.phoneInputContainer}>
                <View style={styles.countryCode}>
                  <Text style={styles.countryCodeText}>+91</Text>
                </View>
                <TextInput
                  style={styles.phoneInput}
                  value={phoneNumber}
                  onChangeText={handlePhoneChange}
                  placeholder="9876543210"
                  keyboardType="phone-pad"
                  maxLength={10}
                />
              </View>

              {error ? (
                <View style={styles.errorContainer}>
                  <Ionicons name="alert-circle" size={16} color="#dc2626" />
                  <Text style={styles.errorText}>{error}</Text>
                </View>
              ) : null}

              <TouchableOpacity
                style={[
                  styles.button,
                  phoneNumber.length !== 10 && styles.buttonDisabled,
                ]}
                onPress={handleSendOTP}
                disabled={loading || phoneNumber.length !== 10}
              >
                {loading ? (
                  <ActivityIndicator color="#fff" />
                ) : (
                  <>
                    <Text style={styles.buttonText}>OTP பெறுக</Text>
                    <Ionicons name="arrow-forward" size={20} color="#fff" />
                  </>
                )}
              </TouchableOpacity>

              <Text style={styles.demoNote}>Demo: OTP console-ல் print ஆகும்</Text>
            </View>
          )}

          {/* OTP Step */}
          {step === 'otp' && (
            <View style={styles.card}>
              <Text style={styles.cardTitle}>OTP உள்ளிடவும்</Text>
              <Text style={styles.cardSubtitle}>+91 {phoneNumber} க்கு OTP அனுப்பப்பட்டது</Text>

              {demoOtp ? (
                <View style={styles.demoOtpContainer}>
                  <Text style={styles.demoOtpLabel}>Demo OTP:</Text>
                  <Text style={styles.demoOtpValue}>{demoOtp}</Text>
                </View>
              ) : null}

              <View style={styles.otpContainer}>
                {otp.map((digit, index) => (
                  <TextInput
                    key={index}
                    ref={(ref) => (otpRefs.current[index] = ref)}
                    style={styles.otpInput}
                    value={digit}
                    onChangeText={(value) => handleOtpChange(index, value)}
                    onKeyPress={({ nativeEvent }) =>
                      handleOtpKeyPress(index, nativeEvent.key)
                    }
                    keyboardType="number-pad"
                    maxLength={1}
                  />
                ))}
              </View>

              {error ? (
                <View style={styles.errorContainer}>
                  <Ionicons name="alert-circle" size={16} color="#dc2626" />
                  <Text style={styles.errorText}>{error}</Text>
                </View>
              ) : null}

              <TouchableOpacity
                style={[
                  styles.button,
                  otp.join('').length !== 6 && styles.buttonDisabled,
                ]}
                onPress={handleVerifyOTP}
                disabled={loading || otp.join('').length !== 6}
              >
                {loading ? (
                  <ActivityIndicator color="#fff" />
                ) : (
                  <>
                    <Text style={styles.buttonText}>சரிபார்க்க</Text>
                    <Ionicons name="checkmark-circle" size={20} color="#fff" />
                  </>
                )}
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.changeNumberBtn}
                onPress={() => {
                  setStep('phone');
                  setOtp(['', '', '', '', '', '']);
                  setError('');
                }}
              >
                <Text style={styles.changeNumberText}>எண்ணை மாற்று</Text>
              </TouchableOpacity>
            </View>
          )}
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
  },
  headerBar: {
    height: 8,
  },
  omContainer: {
    alignItems: 'center',
    paddingTop: 40,
    paddingBottom: 20,
  },
  omSymbol: {
    fontSize: 64,
    color: '#f97316',
  },
  appTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#9a3412',
    marginTop: 8,
  },
  appSubtitle: {
    fontSize: 14,
    color: '#f97316',
    marginTop: 4,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 20,
    padding: 24,
    marginHorizontal: 24,
    marginTop: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
    borderWidth: 1,
    borderColor: '#fed7aa',
  },
  iconContainer: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: '#fff7ed',
    alignItems: 'center',
    justifyContent: 'center',
    alignSelf: 'center',
    marginBottom: 16,
  },
  cardTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#1f2937',
    textAlign: 'center',
  },
  cardSubtitle: {
    fontSize: 14,
    color: '#6b7280',
    textAlign: 'center',
    marginTop: 4,
    marginBottom: 20,
  },
  phoneInputContainer: {
    flexDirection: 'row',
    borderWidth: 2,
    borderColor: '#fed7aa',
    borderRadius: 12,
    overflow: 'hidden',
  },
  countryCode: {
    backgroundColor: '#fff7ed',
    paddingHorizontal: 16,
    justifyContent: 'center',
  },
  countryCodeText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#9a3412',
  },
  phoneInput: {
    flex: 1,
    paddingHorizontal: 16,
    paddingVertical: 14,
    fontSize: 18,
  },
  errorContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fef2f2',
    padding: 12,
    borderRadius: 12,
    marginTop: 16,
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
  buttonDisabled: {
    backgroundColor: '#d1d5db',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  demoNote: {
    textAlign: 'center',
    fontSize: 12,
    color: '#9ca3af',
    marginTop: 16,
  },
  demoOtpContainer: {
    backgroundColor: '#dcfce7',
    borderWidth: 1,
    borderColor: '#86efac',
    borderRadius: 12,
    padding: 12,
    marginBottom: 16,
    alignItems: 'center',
  },
  demoOtpLabel: {
    fontSize: 12,
    color: '#16a34a',
  },
  demoOtpValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#16a34a',
  },
  otpContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 8,
    marginBottom: 16,
  },
  otpInput: {
    width: 48,
    height: 56,
    borderWidth: 2,
    borderColor: '#fed7aa',
    borderRadius: 12,
    textAlign: 'center',
    fontSize: 20,
    fontWeight: '600',
  },
  changeNumberBtn: {
    marginTop: 12,
    alignItems: 'center',
  },
  changeNumberText: {
    color: '#f97316',
    fontSize: 14,
  },
});
