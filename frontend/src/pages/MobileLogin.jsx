import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Phone, ArrowRight, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import { mobileAuthAPI } from '../services/api';

export default function MobileLogin() {
  const navigate = useNavigate();
  const [step, setStep] = useState('phone'); // phone, otp, register
  const [phoneNumber, setPhoneNumber] = useState('');
  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const [demoOtp, setDemoOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isNewUser, setIsNewUser] = useState(false);

  // OTP input refs
  const otpRefs = useRef([]);

  // Registration form data
  const [registerData, setRegisterData] = useState({
    name: '',
    gender: '',
    birthDate: '',
    birthTime: '',
    birthPlace: ''
  });

  const places = [
    'சென்னை', 'மதுரை', 'கோயம்புத்தூர்', 'திருச்சி', 'சேலம்',
    'திருநெல்வேலி', 'ஈரோடு', 'வேலூர்', 'தஞ்சாவூர்', 'திண்டுக்கல்'
  ];

  // Handle phone number input
  const handlePhoneChange = (e) => {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length <= 10) {
      setPhoneNumber(value);
    }
  };

  // Send OTP
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

      // In demo mode, show the OTP
      if (result.demo_otp) {
        setDemoOtp(result.demo_otp);
      }

      setSuccess('OTP அனுப்பப்பட்டது!');
      setStep('otp');
    } catch (err) {
      setError(err.response?.data?.detail || 'OTP அனுப்புவதில் பிழை');
    } finally {
      setLoading(false);
    }
  };

  // Handle OTP input
  const handleOtpChange = (index, value) => {
    if (value.length > 1) value = value[0];
    if (!/^\d*$/.test(value)) return;

    const newOtp = [...otp];
    newOtp[index] = value;
    setOtp(newOtp);

    // Auto-focus next input
    if (value && index < 5) {
      otpRefs.current[index + 1]?.focus();
    }
  };

  // Handle OTP paste
  const handleOtpPaste = (e) => {
    e.preventDefault();
    const pastedData = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6);
    const newOtp = pastedData.split('');
    while (newOtp.length < 6) newOtp.push('');
    setOtp(newOtp);
    otpRefs.current[Math.min(pastedData.length, 5)]?.focus();
  };

  // Handle OTP backspace
  const handleOtpKeyDown = (index, e) => {
    if (e.key === 'Backspace' && !otp[index] && index > 0) {
      otpRefs.current[index - 1]?.focus();
    }
  };

  // Verify OTP
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
        // New user - need registration
        setIsNewUser(true);
        setStep('register');
      } else {
        // Existing user - logged in
        localStorage.setItem('authToken', result.token);
        localStorage.setItem('userProfile', JSON.stringify({
          name: result.user.name,
          phone: result.user.phone,
          rasi: result.user.rasi,
          nakshatra: result.user.nakshatra,
          birthDate: result.user.birth_date,
          birthTime: result.user.birth_time,
          birthPlace: result.user.birth_place,
          latitude: result.user.latitude,
          longitude: result.user.longitude
        }));
        localStorage.setItem('onboardingComplete', 'true');
        setSuccess('உள்நுழைவு வெற்றி!');
        setTimeout(() => navigate('/dashboard'), 1500);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'OTP சரிபார்ப்பில் பிழை');
    } finally {
      setLoading(false);
    }
  };

  // Complete registration
  const handleRegister = async () => {
    if (!registerData.name || !registerData.gender || !registerData.birthDate || !registerData.birthPlace) {
      setError('அனைத்து தேவையான விவரங்களையும் நிரப்பவும்');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const fullPhone = `+91${phoneNumber}`;
      const result = await mobileAuthAPI.register({
        phoneNumber: fullPhone,
        otpCode: otp.join(''),
        ...registerData
      });

      localStorage.setItem('authToken', result.token);
      localStorage.setItem('userProfile', JSON.stringify({
        name: result.user.name,
        phone: result.user.phone,
        rasi: result.user.rasi,
        nakshatra: result.user.nakshatra,
        birthDate: registerData.birthDate,
        birthTime: registerData.birthTime,
        birthPlace: registerData.birthPlace
      }));
      localStorage.setItem('onboardingComplete', 'true');

      setSuccess('பதிவு வெற்றி!');
      setTimeout(() => navigate('/dashboard'), 1500);
    } catch (err) {
      setError(err.response?.data?.detail || 'பதிவு செய்வதில் பிழை');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-orange-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-600 via-red-600 to-orange-600 h-2" />

      {/* Om Symbol */}
      <div className="text-center pt-8 pb-4">
        <span className="text-6xl text-orange-600 font-serif">ॐ</span>
        <h1 className="text-2xl font-bold text-orange-800 mt-2">ஜோதிட AI</h1>
        <p className="text-orange-600 text-sm">மொபைல் உள்நுழைவு</p>
      </div>

      <div className="px-6 py-8">
        <AnimatePresence mode="wait">
          {/* Phone Number Step */}
          {step === 'phone' && (
            <motion.div
              key="phone"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="max-w-sm mx-auto"
            >
              <div className="bg-white rounded-2xl p-6 shadow-lg border border-orange-100">
                <div className="text-center mb-6">
                  <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Phone className="w-8 h-8 text-orange-600" />
                  </div>
                  <h2 className="text-xl font-semibold text-gray-800">மொபைல் எண்</h2>
                  <p className="text-gray-500 text-sm mt-1">உங்கள் மொபைல் எண்ணை உள்ளிடவும்</p>
                </div>

                <div className="flex items-center border-2 border-orange-200 rounded-xl overflow-hidden focus-within:border-orange-500">
                  <span className="px-4 py-3 bg-orange-50 text-orange-700 font-medium">+91</span>
                  <input
                    type="tel"
                    value={phoneNumber}
                    onChange={handlePhoneChange}
                    placeholder="9876543210"
                    className="flex-1 px-4 py-3 outline-none text-lg"
                    maxLength={10}
                  />
                </div>

                {error && (
                  <div className="flex items-center gap-2 mt-4 p-3 bg-red-50 rounded-lg text-red-600 text-sm">
                    <AlertCircle className="w-4 h-4" />
                    {error}
                  </div>
                )}

                <button
                  onClick={handleSendOTP}
                  disabled={loading || phoneNumber.length !== 10}
                  className={`w-full mt-6 py-3 rounded-xl font-medium flex items-center justify-center gap-2 transition-all ${
                    phoneNumber.length === 10 && !loading
                      ? 'bg-gradient-to-r from-orange-500 to-red-500 text-white shadow-lg'
                      : 'bg-gray-200 text-gray-400'
                  }`}
                >
                  {loading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <>
                      OTP பெறுக
                      <ArrowRight className="w-5 h-5" />
                    </>
                  )}
                </button>

                <p className="text-center text-xs text-gray-400 mt-4">
                  Demo: OTP console-ல் print ஆகும்
                </p>
              </div>
            </motion.div>
          )}

          {/* OTP Step */}
          {step === 'otp' && (
            <motion.div
              key="otp"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="max-w-sm mx-auto"
            >
              <div className="bg-white rounded-2xl p-6 shadow-lg border border-orange-100">
                <div className="text-center mb-6">
                  <h2 className="text-xl font-semibold text-gray-800">OTP உள்ளிடவும்</h2>
                  <p className="text-gray-500 text-sm mt-1">+91 {phoneNumber} க்கு OTP அனுப்பப்பட்டது</p>
                </div>

                {/* Demo OTP display */}
                {demoOtp && (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-3 mb-4 text-center">
                    <p className="text-green-700 text-sm">Demo OTP: <span className="font-bold text-lg">{demoOtp}</span></p>
                  </div>
                )}

                {/* OTP Input */}
                <div className="flex justify-center gap-2 mb-6">
                  {otp.map((digit, index) => (
                    <input
                      key={index}
                      ref={(el) => (otpRefs.current[index] = el)}
                      type="text"
                      inputMode="numeric"
                      value={digit}
                      onChange={(e) => handleOtpChange(index, e.target.value)}
                      onKeyDown={(e) => handleOtpKeyDown(index, e)}
                      onPaste={handleOtpPaste}
                      className="w-12 h-14 text-center text-xl font-semibold border-2 border-orange-200 rounded-xl focus:border-orange-500 outline-none"
                      maxLength={1}
                    />
                  ))}
                </div>

                {error && (
                  <div className="flex items-center gap-2 mb-4 p-3 bg-red-50 rounded-lg text-red-600 text-sm">
                    <AlertCircle className="w-4 h-4" />
                    {error}
                  </div>
                )}

                {success && (
                  <div className="flex items-center gap-2 mb-4 p-3 bg-green-50 rounded-lg text-green-600 text-sm">
                    <CheckCircle className="w-4 h-4" />
                    {success}
                  </div>
                )}

                <button
                  onClick={handleVerifyOTP}
                  disabled={loading || otp.join('').length !== 6}
                  className={`w-full py-3 rounded-xl font-medium flex items-center justify-center gap-2 transition-all ${
                    otp.join('').length === 6 && !loading
                      ? 'bg-gradient-to-r from-orange-500 to-red-500 text-white shadow-lg'
                      : 'bg-gray-200 text-gray-400'
                  }`}
                >
                  {loading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <>
                      சரிபார்க்க
                      <CheckCircle className="w-5 h-5" />
                    </>
                  )}
                </button>

                <button
                  onClick={() => { setStep('phone'); setOtp(['', '', '', '', '', '']); setError(''); }}
                  className="w-full mt-3 py-2 text-orange-600 text-sm"
                >
                  எண்ணை மாற்று
                </button>
              </div>
            </motion.div>
          )}

          {/* Registration Step */}
          {step === 'register' && (
            <motion.div
              key="register"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="max-w-sm mx-auto"
            >
              <div className="bg-white rounded-2xl p-6 shadow-lg border border-orange-100">
                <div className="text-center mb-6">
                  <h2 className="text-xl font-semibold text-gray-800">புதிய பதிவு</h2>
                  <p className="text-gray-500 text-sm mt-1">உங்கள் விவரங்களை நிரப்பவும்</p>
                </div>

                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">பெயர் *</label>
                    <input
                      type="text"
                      value={registerData.name}
                      onChange={(e) => setRegisterData({...registerData, name: e.target.value})}
                      placeholder="உங்கள் பெயர்"
                      className="w-full px-4 py-3 rounded-xl border-2 border-orange-200 focus:border-orange-500 outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">பாலினம் *</label>
                    <div className="grid grid-cols-2 gap-3">
                      {[
                        { value: 'male', label: 'ஆண்', icon: '👨' },
                        { value: 'female', label: 'பெண்', icon: '👩' }
                      ].map((g) => (
                        <button
                          key={g.value}
                          onClick={() => setRegisterData({...registerData, gender: g.value})}
                          className={`p-3 rounded-xl border-2 transition-all ${
                            registerData.gender === g.value
                              ? 'border-orange-500 bg-orange-50'
                              : 'border-orange-200 bg-white'
                          }`}
                        >
                          <span className="text-2xl">{g.icon}</span>
                          <p className="text-sm mt-1">{g.label}</p>
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">பிறந்த தேதி *</label>
                    <input
                      type="date"
                      value={registerData.birthDate}
                      onChange={(e) => setRegisterData({...registerData, birthDate: e.target.value})}
                      className="w-full px-4 py-3 rounded-xl border-2 border-orange-200 focus:border-orange-500 outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">பிறந்த நேரம்</label>
                    <input
                      type="time"
                      value={registerData.birthTime}
                      onChange={(e) => setRegisterData({...registerData, birthTime: e.target.value})}
                      className="w-full px-4 py-3 rounded-xl border-2 border-orange-200 focus:border-orange-500 outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">பிறந்த இடம் *</label>
                    <select
                      value={registerData.birthPlace}
                      onChange={(e) => setRegisterData({...registerData, birthPlace: e.target.value})}
                      className="w-full px-4 py-3 rounded-xl border-2 border-orange-200 focus:border-orange-500 outline-none bg-white"
                    >
                      <option value="">இடத்தை தேர்வு செய்யவும்</option>
                      {places.map((p) => (
                        <option key={p} value={p}>{p}</option>
                      ))}
                    </select>
                  </div>
                </div>

                {error && (
                  <div className="flex items-center gap-2 mt-4 p-3 bg-red-50 rounded-lg text-red-600 text-sm">
                    <AlertCircle className="w-4 h-4" />
                    {error}
                  </div>
                )}

                {success && (
                  <div className="flex items-center gap-2 mt-4 p-3 bg-green-50 rounded-lg text-green-600 text-sm">
                    <CheckCircle className="w-4 h-4" />
                    {success}
                  </div>
                )}

                <button
                  onClick={handleRegister}
                  disabled={loading}
                  className="w-full mt-6 py-3 rounded-xl font-medium flex items-center justify-center gap-2 bg-gradient-to-r from-orange-500 to-red-500 text-white shadow-lg"
                >
                  {loading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <>
                      பதிவு செய்க
                      <CheckCircle className="w-5 h-5" />
                    </>
                  )}
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Skip to regular onboarding */}
        <div className="text-center mt-8">
          <button
            onClick={() => navigate('/onboarding')}
            className="text-orange-600 text-sm hover:underline"
          >
            மொபைல் இல்லாமல் தொடர
          </button>
        </div>
      </div>
    </div>
  );
}
