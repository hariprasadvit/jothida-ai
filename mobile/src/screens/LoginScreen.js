import React, { useState, useRef, useEffect } from 'react';
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
  Animated,
  Dimensions,
  Easing,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import Svg, { Path, Circle, Defs, RadialGradient, Stop, Ellipse, G } from 'react-native-svg';
import { mobileAuthAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';

const { width, height } = Dimensions.get('window');

// Mango Leaf Component
const MangoLeaf = ({ x, y, rotation = 0, scale = 1 }) => (
  <G transform={`translate(${x}, ${y}) rotate(${rotation}) scale(${scale})`}>
    <Path
      d="M0 0 Q5 -15 0 -35 Q-5 -15 0 0"
      fill="#166534"
      stroke="#15803d"
      strokeWidth="0.5"
    />
    <Path
      d="M0 -5 L0 -30"
      stroke="#22c55e"
      strokeWidth="0.8"
    />
  </G>
);

// Marigold Flower Component
const MarigoldFlower = ({ cx, cy, size = 20, color = '#f97316' }) => (
  <G>
    {[...Array(12)].map((_, i) => (
      <Ellipse
        key={`outer-${i}`}
        cx={cx + (size * 0.4) * Math.cos((i * 30 * Math.PI) / 180)}
        cy={cy + (size * 0.4) * Math.sin((i * 30 * Math.PI) / 180)}
        rx={size * 0.25}
        ry={size * 0.15}
        fill={color}
        transform={`rotate(${i * 30 + 90}, ${cx + (size * 0.4) * Math.cos((i * 30 * Math.PI) / 180)}, ${cy + (size * 0.4) * Math.sin((i * 30 * Math.PI) / 180)})`}
      />
    ))}
    {[...Array(8)].map((_, i) => (
      <Ellipse
        key={`inner-${i}`}
        cx={cx + (size * 0.2) * Math.cos((i * 45 * Math.PI) / 180)}
        cy={cy + (size * 0.2) * Math.sin((i * 45 * Math.PI) / 180)}
        rx={size * 0.18}
        ry={size * 0.12}
        fill={color === '#f97316' ? '#fb923c' : '#fca5a5'}
        transform={`rotate(${i * 45 + 90}, ${cx + (size * 0.2) * Math.cos((i * 45 * Math.PI) / 180)}, ${cy + (size * 0.2) * Math.sin((i * 45 * Math.PI) / 180)})`}
      />
    ))}
    <Circle cx={cx} cy={cy} r={size * 0.1} fill="#fbbf24" />
  </G>
);

// Toran (Mango Leaf Decoration) Component
const Toran = ({ toranWidth }) => {
  const leafCount = Math.floor(toranWidth / 15);
  return (
    <Svg width={toranWidth} height={60} viewBox={`0 0 ${toranWidth} 60`}>
      <Path
        d={`M0 10 Q${toranWidth / 4} 18 ${toranWidth / 2} 12 Q${toranWidth * 3 / 4} 8 ${toranWidth} 12`}
        stroke="#92400e"
        strokeWidth="3"
        fill="none"
      />
      {[...Array(leafCount)].map((_, i) => {
        const x = (i / leafCount) * toranWidth + 8;
        const curveY = 12 + Math.sin((i / leafCount) * Math.PI) * 5;
        const rotation = -10 + (i % 3) * 10;
        return (
          <MangoLeaf
            key={i}
            x={x}
            y={curveY + 25}
            rotation={rotation}
            scale={0.6}
          />
        );
      })}
    </Svg>
  );
};

// Hanging Marigold String
const HangingMarigold = ({ length }) => {
  const flowerCount = Math.floor(length / 20);
  return (
    <Svg width={30} height={length} viewBox={`0 0 30 ${length}`}>
      <Path
        d={`M15 0 L15 ${length}`}
        stroke="#84cc16"
        strokeWidth="2"
      />
      {[...Array(flowerCount)].map((_, i) => (
        <MarigoldFlower
          key={i}
          cx={15}
          cy={10 + i * 20}
          size={13}
          color={i % 2 === 0 ? '#f97316' : '#fbbf24'}
        />
      ))}
    </Svg>
  );
};

export default function LoginScreen({ navigation }) {
  const { login } = useAuth();
  const { t, language } = useLanguage();
  const [step, setStep] = useState('phone');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const [demoOtp, setDemoOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const otpRefs = useRef([]);
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const garlandAnim = useRef(new Animated.Value(-40)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 600,
        useNativeDriver: true,
      }),
      Animated.spring(garlandAnim, {
        toValue: 0,
        friction: 8,
        tension: 40,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  const texts = {
    mobileNumber: language === 'en' ? 'Mobile Number' : language === 'kn' ? 'ಮೊಬೈಲ್ ಸಂಖ್ಯೆ' : 'மொபைல் எண்',
    enterMobile: language === 'en' ? 'Enter your mobile number' : language === 'kn' ? 'ನಿಮ್ಮ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ' : 'உங்கள் மொபைல் எண்ணை உள்ளிடவும்',
    getOtp: language === 'en' ? 'Get OTP' : language === 'kn' ? 'OTP ಪಡೆಯಿರಿ' : 'OTP பெறுக',
    enterOtp: language === 'en' ? 'Enter OTP' : language === 'kn' ? 'OTP ನಮೂದಿಸಿ' : 'OTP உள்ளிடவும்',
    otpSent: language === 'en' ? 'OTP sent to' : language === 'kn' ? 'OTP ಕಳುಹಿಸಲಾಗಿದೆ' : 'OTP அனுப்பப்பட்டது',
    verify: language === 'en' ? 'Verify' : language === 'kn' ? 'ಪರಿಶೀಲಿಸಿ' : 'சரிபார்க்க',
    changeNumber: language === 'en' ? 'Change Number' : language === 'kn' ? 'ಸಂಖ್ಯೆ ಬದಲಾಯಿಸಿ' : 'எண்ணை மாற்று',
    mobileLogin: language === 'en' ? 'Mobile Login' : language === 'kn' ? 'ಮೊಬೈಲ್ ಲಾಗಿನ್' : 'மொபைல் உள்நுழைவு',
    enter10Digit: language === 'en' ? 'Enter 10 digit mobile number' : language === 'kn' ? '10 ಅಂಕಿ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ' : '10 இலக்க மொபைல் எண்ணை உள்ளிடவும்',
    enter6DigitOtp: language === 'en' ? 'Enter 6 digit OTP' : language === 'kn' ? '6 ಅಂಕಿ OTP ನಮೂದಿಸಿ' : '6 இலக்க OTP ஐ உள்ளிடவும்',
  };

  const handlePhoneChange = (text) => {
    const cleaned = text.replace(/\D/g, '');
    if (cleaned.length <= 10) {
      setPhoneNumber(cleaned);
    }
  };

  const handleSendOTP = async () => {
    if (phoneNumber.length !== 10) {
      setError(texts.enter10Digit);
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
      if (err.message === 'Network Error') {
        setError(language === 'en' ? 'Cannot reach server. Check your connection.' : 'சேவையகத்தை அணுக முடியவில்லை');
      } else {
        setError(err.response?.data?.detail || 'OTP sending failed');
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
      setError(texts.enter6DigitOtp);
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
      setError(err.response?.data?.detail || 'OTP verification failed');
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
        colors={['#fef3c7', '#fed7aa', '#fdba74', '#fb923c']}
        style={styles.gradient}
        start={{ x: 0.5, y: 0 }}
        end={{ x: 0.5, y: 1 }}
        locations={[0, 0.3, 0.6, 1]}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          keyboardShouldPersistTaps="handled"
        >
          {/* Top Mango Toran */}
          <Animated.View
            style={[
              styles.toranContainer,
              {
                opacity: fadeAnim,
                transform: [{ translateY: garlandAnim }]
              }
            ]}
          >
            <Toran toranWidth={width} />
          </Animated.View>

          {/* Left hanging garland */}
          <Animated.View
            style={[
              styles.leftGarland,
              {
                opacity: fadeAnim,
                transform: [{ translateY: garlandAnim }]
              }
            ]}
          >
            <HangingMarigold length={height * 0.18} />
          </Animated.View>

          {/* Right hanging garland */}
          <Animated.View
            style={[
              styles.rightGarland,
              {
                opacity: fadeAnim,
                transform: [{ translateY: garlandAnim }]
              }
            ]}
          >
            <HangingMarigold length={height * 0.18} />
          </Animated.View>

          {/* Logo and Title */}
          <Animated.View style={[styles.headerContainer, { opacity: fadeAnim }]}>
            <View style={styles.logoContainer}>
              <LinearGradient
                colors={['#fff', '#fef3c7']}
                style={styles.logoOuter}
              >
                <LinearGradient
                  colors={['#f97316', '#ea580c']}
                  style={styles.logoGradient}
                >
                  <Svg width={40} height={40} viewBox="0 0 100 100">
                    <Path
                      d="M50 5 L55 40 L90 30 L60 50 L90 70 L55 60 L50 95 L45 60 L10 70 L40 50 L10 30 L45 40 Z"
                      fill="#fff"
                    />
                    <Circle cx="50" cy="50" r="10" fill="#f97316" />
                  </Svg>
                </LinearGradient>
              </LinearGradient>
            </View>
            <Text style={styles.appTitle}>jothida.ai</Text>
            <Text style={styles.appSubtitle}>{texts.mobileLogin}</Text>
          </Animated.View>

          {/* Phone Step */}
          {step === 'phone' && (
            <View style={styles.card}>
              <View style={styles.iconContainer}>
                <Ionicons name="phone-portrait-outline" size={32} color="#f97316" />
              </View>
              <Text style={styles.cardTitle}>{texts.mobileNumber}</Text>
              <Text style={styles.cardSubtitle}>{texts.enterMobile}</Text>

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
                <LinearGradient
                  colors={phoneNumber.length === 10 ? ['#7c2d12', '#9a3412'] : ['#d1d5db', '#d1d5db']}
                  style={styles.buttonGradient}
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 0 }}
                >
                  {loading ? (
                    <ActivityIndicator color="#fff" />
                  ) : (
                    <>
                      <Text style={styles.buttonText}>{texts.getOtp}</Text>
                      <Ionicons name="arrow-forward" size={20} color="#fff" />
                    </>
                  )}
                </LinearGradient>
              </TouchableOpacity>

              <Text style={styles.demoNote}>Demo: OTP will be shown below</Text>
            </View>
          )}

          {/* OTP Step */}
          {step === 'otp' && (
            <View style={styles.card}>
              <Text style={styles.cardTitle}>{texts.enterOtp}</Text>
              <Text style={styles.cardSubtitle}>{texts.otpSent} +91 {phoneNumber}</Text>

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
                <LinearGradient
                  colors={otp.join('').length === 6 ? ['#7c2d12', '#9a3412'] : ['#d1d5db', '#d1d5db']}
                  style={styles.buttonGradient}
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 0 }}
                >
                  {loading ? (
                    <ActivityIndicator color="#fff" />
                  ) : (
                    <>
                      <Text style={styles.buttonText}>{texts.verify}</Text>
                      <Ionicons name="checkmark-circle" size={20} color="#fff" />
                    </>
                  )}
                </LinearGradient>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.changeNumberBtn}
                onPress={() => {
                  setStep('phone');
                  setOtp(['', '', '', '', '', '']);
                  setError('');
                }}
              >
                <Text style={styles.changeNumberText}>{texts.changeNumber}</Text>
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
    paddingBottom: 30,
  },
  toranContainer: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    zIndex: 10,
  },
  leftGarland: {
    position: 'absolute',
    top: 45,
    left: 10,
    zIndex: 5,
  },
  rightGarland: {
    position: 'absolute',
    top: 45,
    right: 10,
    zIndex: 5,
  },
  headerContainer: {
    alignItems: 'center',
    paddingTop: 80,
    paddingBottom: 20,
  },
  logoContainer: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.3,
    shadowRadius: 15,
    elevation: 10,
  },
  logoOuter: {
    width: 85,
    height: 85,
    borderRadius: 18,
    padding: 5,
    alignItems: 'center',
    justifyContent: 'center',
  },
  logoGradient: {
    width: 72,
    height: 72,
    borderRadius: 36,
    alignItems: 'center',
    justifyContent: 'center',
  },
  appTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#7c2d12',
    marginTop: 12,
    letterSpacing: 1,
  },
  appSubtitle: {
    fontSize: 14,
    color: '#9a3412',
    marginTop: 4,
  },
  card: {
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: 20,
    padding: 24,
    marginHorizontal: 24,
    marginTop: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
    borderWidth: 2,
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
    backgroundColor: '#fff',
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
    backgroundColor: '#fff',
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
    borderRadius: 12,
    overflow: 'hidden',
    marginTop: 20,
  },
  buttonDisabled: {
    opacity: 0.7,
  },
  buttonGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 14,
    gap: 8,
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
    backgroundColor: '#fff',
  },
  changeNumberBtn: {
    marginTop: 12,
    alignItems: 'center',
  },
  changeNumberText: {
    color: '#9a3412',
    fontSize: 14,
  },
});
