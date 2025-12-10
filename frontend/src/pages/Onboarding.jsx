import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronRight, ChevronLeft, Sparkles, Sun, Moon, Star, Loader2 } from 'lucide-react';
import { userAPI } from '../services/api';

const nakshatras = [
  'அசுவினி', 'பரணி', 'கார்த்திகை', 'ரோகிணி', 'மிருகசீரிடம்', 'திருவாதிரை',
  'புனர்பூசம்', 'பூசம்', 'ஆயில்யம்', 'மகம்', 'பூரம்', 'உத்திரம்',
  'அஸ்தம்', 'சித்திரை', 'சுவாதி', 'விசாகம்', 'அனுஷம்', 'கேட்டை',
  'மூலம்', 'பூராடம்', 'உத்திராடம்', 'திருவோணம்', 'அவிட்டம்', 'சதயம்',
  'பூரட்டாதி', 'உத்திரட்டாதி', 'ரேவதி'
];

const rasiList = [
  'மேஷம்', 'ரிஷபம்', 'மிதுனம்', 'கடகம்', 'சிம்மம்', 'கன்னி',
  'துலாம்', 'விருச்சிகம்', 'தனுசு', 'மகரம்', 'கும்பம்', 'மீனம்'
];

const places = [
  'சென்னை', 'மதுரை', 'கோயம்புத்தூர்', 'திருச்சி', 'சேலம்',
  'திருநெல்வேலி', 'ஈரோடு', 'வேலூர்', 'தஞ்சாவூர்', 'திண்டுக்கல்'
];

export default function Onboarding() {
  const navigate = useNavigate();
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    gender: '',
    birthDate: '',
    birthTime: '',
    birthPlace: '',
    nakshatra: '',
    rasi: ''
  });

  const steps = [
    {
      title: 'வணக்கம்',
      subtitle: 'ஜோதிட AI உங்களை வரவேற்கிறது',
      description: 'பாரம்பரிய வேத ஜோதிடத்தை நவீன AI தொழில்நுட்பத்துடன் இணைத்து உங்கள் வாழ்க்கை பயணத்தை வழிநடத்துகிறோம்'
    },
    {
      title: 'அடிப்படை விவரங்கள்',
      subtitle: 'உங்கள் பெயர் மற்றும் பாலினம்'
    },
    {
      title: 'பிறந்த தகவல்கள்',
      subtitle: 'பிறந்த தேதி, நேரம் மற்றும் இடம்'
    },
    {
      title: 'ஜாதக விவரங்கள்',
      subtitle: 'நட்சத்திரம் மற்றும் ராசி (தெரிந்தால்)'
    }
  ];

  const handleNext = async () => {
    if (step < steps.length - 1) {
      setStep(step + 1);
    } else {
      // Register user in database and save to localStorage
      setLoading(true);
      setError('');

      try {
        // Call API to register user
        const result = await userAPI.register(formData);
        console.log('User registered:', result);

        // Save to localStorage for immediate use
        const profileWithAstro = {
          ...formData,
          rasi: result.rasi || formData.rasi,
          nakshatra: result.nakshatra || formData.nakshatra
        };
        localStorage.setItem('userProfile', JSON.stringify(profileWithAstro));
        localStorage.setItem('onboardingComplete', 'true');

        navigate('/dashboard');
      } catch (err) {
        console.error('Registration failed:', err);
        setError('பதிவு செய்வதில் பிழை. மீண்டும் முயற்சிக்கவும்.');

        // Still save to localStorage as fallback
        localStorage.setItem('userProfile', JSON.stringify(formData));
        localStorage.setItem('onboardingComplete', 'true');
        navigate('/dashboard');
      } finally {
        setLoading(false);
      }
    }
  };

  const handleBack = () => {
    if (step > 0) setStep(step - 1);
  };

  const isStepValid = () => {
    switch (step) {
      case 0: return true;
      case 1: return formData.name && formData.gender;
      case 2: return formData.birthDate && formData.birthTime && formData.birthPlace;
      case 3: return true; // Optional step
      default: return true;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-orange-50">
      {/* Decorative Header */}
      <div className="bg-gradient-to-r from-orange-600 via-red-600 to-orange-600 h-2" />

      {/* Om Symbol Header */}
      <div className="text-center pt-8 pb-4">
        <div className="inline-block">
          <span className="text-6xl text-orange-600 font-serif">ॐ</span>
        </div>
        <h1 className="text-2xl font-bold text-orange-800 mt-2 tracking-wide">
          ஜோதிட AI
        </h1>
        <p className="text-orange-600 text-sm">வேத ஜோதிடம் • AI துணை</p>
      </div>

      {/* Progress Indicator */}
      <div className="flex justify-center gap-2 px-8 mb-8">
        {steps.map((_, i) => (
          <div
            key={i}
            className={`h-1.5 rounded-full transition-all duration-300 ${
              i <= step ? 'bg-orange-500 flex-grow' : 'bg-orange-200 w-8'
            }`}
          />
        ))}
      </div>

      {/* Main Content */}
      <div className="px-6 pb-32">
        <AnimatePresence mode="wait">
          <motion.div
            key={step}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            {/* Step Title */}
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-gray-800">{steps[step].title}</h2>
              <p className="text-gray-600 mt-1">{steps[step].subtitle}</p>
            </div>

            {/* Step 0: Welcome */}
            {step === 0 && (
              <div className="text-center space-y-6">
                {/* Kolam Pattern */}
                <div className="relative w-48 h-48 mx-auto">
                  <div className="absolute inset-0 border-4 border-orange-300 rounded-full animate-spin-slow" style={{animationDuration: '20s'}} />
                  <div className="absolute inset-4 border-4 border-red-300 rounded-full animate-spin-slow" style={{animationDuration: '15s', animationDirection: 'reverse'}} />
                  <div className="absolute inset-8 border-4 border-orange-400 rounded-full animate-spin-slow" style={{animationDuration: '10s'}} />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="text-center">
                      <Sun className="w-12 h-12 text-orange-500 mx-auto" />
                      <Moon className="w-8 h-8 text-orange-400 mx-auto -mt-2" />
                    </div>
                  </div>
                </div>

                <p className="text-gray-600 leading-relaxed max-w-sm mx-auto">
                  {steps[step].description}
                </p>

                {/* Features */}
                <div className="grid grid-cols-3 gap-4 mt-8">
                  {[
                    { icon: '🪔', label: 'ஜாதகம்' },
                    { icon: '💑', label: 'பொருத்தம்' },
                    { icon: '📅', label: 'முகூர்த்தம்' }
                  ].map((f, i) => (
                    <div key={i} className="bg-white rounded-xl p-4 shadow-sm border border-orange-100">
                      <span className="text-2xl">{f.icon}</span>
                      <p className="text-sm text-gray-600 mt-1">{f.label}</p>
                    </div>
                  ))}
                </div>

              </div>
            )}

            {/* Step 1: Basic Info */}
            {step === 1 && (
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    உங்கள் பெயர்
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    placeholder="பெயரை உள்ளிடவும்"
                    className="w-full px-4 py-3 rounded-xl border-2 border-orange-200 focus:border-orange-500 focus:ring-0 outline-none transition-colors bg-white"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    பாலினம்
                  </label>
                  <div className="grid grid-cols-2 gap-4">
                    {[
                      { value: 'male', label: 'ஆண்', icon: '👨' },
                      { value: 'female', label: 'பெண்', icon: '👩' }
                    ].map((g) => (
                      <button
                        key={g.value}
                        onClick={() => setFormData({...formData, gender: g.value})}
                        className={`p-4 rounded-xl border-2 transition-all ${
                          formData.gender === g.value
                            ? 'border-orange-500 bg-orange-50'
                            : 'border-orange-200 bg-white hover:border-orange-300'
                        }`}
                      >
                        <span className="text-3xl">{g.icon}</span>
                        <p className="mt-2 font-medium text-gray-700">{g.label}</p>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Step 2: Birth Details */}
            {step === 2 && (
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    பிறந்த தேதி
                  </label>
                  <input
                    type="date"
                    value={formData.birthDate}
                    onChange={(e) => setFormData({...formData, birthDate: e.target.value})}
                    className="w-full px-4 py-3 rounded-xl border-2 border-orange-200 focus:border-orange-500 focus:ring-0 outline-none transition-colors bg-white"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    பிறந்த நேரம்
                  </label>
                  <input
                    type="time"
                    value={formData.birthTime}
                    onChange={(e) => setFormData({...formData, birthTime: e.target.value})}
                    className="w-full px-4 py-3 rounded-xl border-2 border-orange-200 focus:border-orange-500 focus:ring-0 outline-none transition-colors bg-white"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    சரியான நேரம் தெரியவில்லை என்றால் தோராயமாக உள்ளிடவும்
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    பிறந்த இடம்
                  </label>
                  <select
                    value={formData.birthPlace}
                    onChange={(e) => setFormData({...formData, birthPlace: e.target.value})}
                    className="w-full px-4 py-3 rounded-xl border-2 border-orange-200 focus:border-orange-500 focus:ring-0 outline-none transition-colors bg-white"
                  >
                    <option value="">இடத்தை தேர்வு செய்யவும்</option>
                    {places.map((p) => (
                      <option key={p} value={p}>{p}</option>
                    ))}
                  </select>
                </div>
              </div>
            )}

            {/* Step 3: Astro Details */}
            {step === 3 && (
              <div className="space-y-6">
                <div className="bg-orange-50 rounded-xl p-4 border border-orange-200">
                  <p className="text-sm text-orange-700">
                    <Sparkles className="w-4 h-4 inline mr-1" />
                    இந்த தகவல்கள் விருப்பமானவை. தெரியவில்லை என்றால் காலியாக விடலாம் - AI கணக்கிடும்
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    நட்சத்திரம்
                  </label>
                  <select
                    value={formData.nakshatra}
                    onChange={(e) => setFormData({...formData, nakshatra: e.target.value})}
                    className="w-full px-4 py-3 rounded-xl border-2 border-orange-200 focus:border-orange-500 focus:ring-0 outline-none transition-colors bg-white"
                  >
                    <option value="">நட்சத்திரத்தை தேர்வு செய்யவும்</option>
                    {nakshatras.map((n) => (
                      <option key={n} value={n}>{n}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    ராசி
                  </label>
                  <select
                    value={formData.rasi}
                    onChange={(e) => setFormData({...formData, rasi: e.target.value})}
                    className="w-full px-4 py-3 rounded-xl border-2 border-orange-200 focus:border-orange-500 focus:ring-0 outline-none transition-colors bg-white"
                  >
                    <option value="">ராசியை தேர்வு செய்யவும்</option>
                    {rasiList.map((r) => (
                      <option key={r} value={r}>{r}</option>
                    ))}
                  </select>
                </div>

                {/* Summary */}
                <div className="bg-white rounded-xl p-4 border border-orange-200 mt-6">
                  <h3 className="font-medium text-gray-800 mb-3">உங்கள் விவரங்கள்</h3>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-500">பெயர்</span>
                      <span className="text-gray-800">{formData.name || '-'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">பிறந்த தேதி</span>
                      <span className="text-gray-800">{formData.birthDate || '-'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">பிறந்த நேரம்</span>
                      <span className="text-gray-800">{formData.birthTime || '-'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">பிறந்த இடம்</span>
                      <span className="text-gray-800">{formData.birthPlace || '-'}</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Bottom Navigation */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-orange-100 p-4 safe-bottom">
        <div className="flex gap-3">
          {step > 0 && (
            <button
              onClick={handleBack}
              className="px-6 py-3 rounded-xl border-2 border-orange-300 text-orange-600 font-medium"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
          )}
          <button
            onClick={handleNext}
            disabled={!isStepValid() || loading}
            className={`flex-1 py-3 rounded-xl font-medium flex items-center justify-center gap-2 transition-all ${
              isStepValid() && !loading
                ? 'bg-gradient-to-r from-orange-500 to-red-500 text-white shadow-lg shadow-orange-500/30'
                : 'bg-gray-200 text-gray-400'
            }`}
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                பதிவு செய்கிறது...
              </>
            ) : step === steps.length - 1 ? (
              <>
                <Sparkles className="w-5 h-5" />
                ஜாதகம் உருவாக்கு
              </>
            ) : (
              <>
                தொடரவும்
                <ChevronRight className="w-5 h-5" />
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
