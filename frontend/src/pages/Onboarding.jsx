import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronRight, ChevronLeft, Sparkles, Sun, Moon, Star, Loader2, Grid, Heart, Users, Calendar, Clock, MessageCircle, Rocket, CheckCircle } from 'lucide-react';
import { userAPI } from '../services/api';

// Get onboarding intro data by language
const getOnboardingIntro = (language) => {
  if (language === 'en') {
    return [
      {
        id: '1',
        Icon: Sun,
        IconSecondary: Moon,
        title: 'Jothida AI',
        subtitle: 'Your Life Guide',
        description: 'We combine the ancient wisdom of Tamil astrology with modern AI technology to provide you accurate predictions.',
        gradient: ['#f97316', '#ef4444'],
        features: ['Accurate Rasi Predictions', 'AI Analysis', 'Full English Support'],
      },
      {
        id: '2',
        Icon: Grid,
        IconSecondary: Star,
        title: 'Rasi & Navamsa Chart',
        subtitle: 'Detailed Horoscope Analysis',
        description: 'We calculate accurate Rasi chart, Navamsa chart, and planetary positions based on your birth time and place.',
        gradient: ['#8b5cf6', '#6366f1'],
        features: ['Rasi Chart', 'Navamsa Chart', 'Planet Positions'],
      },
      {
        id: '3',
        Icon: Heart,
        IconSecondary: Users,
        title: 'Marriage Matching',
        subtitle: '10 Porutham Analysis',
        description: 'We analyze all 10 poruthams including Dinam, Ganam, Mahendram, Stree Deergham, Yoni, Rasi, Rasi Athipathi, Vasiyam, Rajju, and Vedai.',
        gradient: ['#ec4899', '#f43f5e'],
        features: ['10 Porutham', 'AI Recommendation', 'Remedies'],
      },
      {
        id: '4',
        Icon: Calendar,
        IconSecondary: Clock,
        title: 'Muhurtham Finder',
        subtitle: 'Auspicious Time Selection',
        description: 'Find the right muhurtham time for important events like marriage, housewarming, business start, and travel.',
        gradient: ['#10b981', '#14b8a6'],
        features: ['Auspicious Time', 'Rahu Kalam', 'Panchang'],
      },
      {
        id: '5',
        Icon: MessageCircle,
        IconSecondary: Sparkles,
        title: 'AI Astrology Assistant',
        subtitle: 'Ask in Your Language',
        description: 'Ask any question about your horoscope. Our AI will provide detailed answers in your preferred language.',
        gradient: ['#f97316', '#fbbf24'],
        features: ['24/7 Support', 'Multi-language', 'Personalized Advice'],
      },
    ];
  } else {
    // Tamil (default)
    return [
      {
        id: '1',
        Icon: Sun,
        IconSecondary: Moon,
        title: 'ஜோதிட AI',
        subtitle: 'உங்கள் வாழ்க்கை வழிகாட்டி',
        description: 'தமிழ் ஜோதிடத்தின் பண்டைய ஞானத்தை நவீன AI தொழில்நுட்பத்துடன் இணைத்து உங்களுக்கு துல்லியமான பலன்களை வழங்குகிறோம்.',
        gradient: ['#f97316', '#ef4444'],
        features: ['துல்லியமான ராசி பலன்', 'AI பகுப்பாய்வு', 'தமிழில் முழு ஆதரவு'],
      },
      {
        id: '2',
        Icon: Grid,
        IconSecondary: Star,
        title: 'ராசி & நவாம்ச கட்டம்',
        subtitle: 'விரிவான ஜாதக பகுப்பாய்வு',
        description: 'உங்கள் பிறந்த நேரம் மற்றும் இடத்தின் அடிப்படையில் துல்லியமான ராசி கட்டம், நவாம்ச கட்டம், மற்றும் கிரக நிலைகளை கணக்கிடுகிறோம்.',
        gradient: ['#8b5cf6', '#6366f1'],
        features: ['ராசி கட்டம்', 'நவாம்ச கட்டம்', 'கிரக நிலைகள்'],
      },
      {
        id: '3',
        Icon: Heart,
        IconSecondary: Users,
        title: 'திருமண பொருத்தம்',
        subtitle: '10 பொருத்த பகுப்பாய்வு',
        description: 'தினம், கணம், மகேந்திரம், ஸ்திரி தீர்க்கம், யோனி, ராசி, ராசி அதிபதி, வசியம், ரஜ்ஜூ, வேதை ஆகிய 10 பொருத்தங்களை பகுப்பாய்வு செய்கிறோம்.',
        gradient: ['#ec4899', '#f43f5e'],
        features: ['10 பொருத்தம்', 'AI பரிந்துரை', 'பரிகாரங்கள்'],
      },
      {
        id: '4',
        Icon: Calendar,
        IconSecondary: Clock,
        title: 'முகூர்த்தம் கண்டறிதல்',
        subtitle: 'சுப நேரம் தேர்வு',
        description: 'திருமணம், கிரக பிரவேசம், தொழில் ஆரம்பம், பயணம் போன்ற முக்கிய நிகழ்வுகளுக்கு சரியான முகூர்த்த நேரத்தை கண்டறியுங்கள்.',
        gradient: ['#10b981', '#14b8a6'],
        features: ['சுப நேரம்', 'ராகு காலம்', 'பஞ்சாங்கம்'],
      },
      {
        id: '5',
        Icon: MessageCircle,
        IconSecondary: Sparkles,
        title: 'AI ஜோதிட உதவியாளர்',
        subtitle: 'தமிழில் கேளுங்கள்',
        description: 'உங்கள் ஜாதகம் பற்றிய எந்த கேள்வியையும் தமிழில் கேளுங்கள். எங்கள் AI உங்களுக்கு விரிவான பதில்களை தரும்.',
        gradient: ['#f97316', '#fbbf24'],
        features: ['24/7 ஆதரவு', 'தமிழில் பதில்', 'தனிப்பயன் ஆலோசனை'],
      },
    ];
  }
};

// Translations
const translations = {
  ta: {
    skip: 'தவிர்',
    next: 'அடுத்து',
    getStarted: 'தொடங்கு',
    basicDetails: 'அடிப்படை விவரங்கள்',
    nameAndGender: 'உங்கள் பெயர் மற்றும் பாலினம்',
    birthDetails: 'பிறந்த தகவல்கள்',
    birthInfo: 'பிறந்த தேதி, நேரம் மற்றும் இடம்',
    astroDetails: 'ஜாதக விவரங்கள்',
    nakshatraRasi: 'நட்சத்திரம் மற்றும் ராசி (தெரிந்தால்)',
    yourName: 'உங்கள் பெயர்',
    enterName: 'பெயரை உள்ளிடவும்',
    gender: 'பாலினம்',
    male: 'ஆண்',
    female: 'பெண்',
    birthDate: 'பிறந்த தேதி',
    birthTime: 'பிறந்த நேரம்',
    timeHint: 'சரியான நேரம் தெரியவில்லை என்றால் தோராயமாக உள்ளிடவும்',
    birthPlace: 'பிறந்த இடம்',
    selectPlace: 'இடத்தை தேர்வு செய்யவும்',
    optionalInfo: 'இந்த தகவல்கள் விருப்பமானவை. தெரியவில்லை என்றால் காலியாக விடலாம் - AI கணக்கிடும்',
    nakshatra: 'நட்சத்திரம்',
    selectNakshatra: 'நட்சத்திரத்தை தேர்வு செய்யவும்',
    rasi: 'ராசி',
    selectRasi: 'ராசியை தேர்வு செய்யவும்',
    yourDetails: 'உங்கள் விவரங்கள்',
    name: 'பெயர்',
    continue: 'தொடரவும்',
    createJathagam: 'ஜாதகம் உருவாக்கு',
    registering: 'பதிவு செய்கிறது...',
    registrationError: 'பதிவு செய்வதில் பிழை. மீண்டும் முயற்சிக்கவும்.',
  },
  en: {
    skip: 'Skip',
    next: 'Next',
    getStarted: 'Get Started',
    basicDetails: 'Basic Details',
    nameAndGender: 'Your name and gender',
    birthDetails: 'Birth Details',
    birthInfo: 'Date, time and place of birth',
    astroDetails: 'Astrology Details',
    nakshatraRasi: 'Nakshatra and Rasi (if known)',
    yourName: 'Your Name',
    enterName: 'Enter your name',
    gender: 'Gender',
    male: 'Male',
    female: 'Female',
    birthDate: 'Birth Date',
    birthTime: 'Birth Time',
    timeHint: 'Enter approximate time if exact time is not known',
    birthPlace: 'Birth Place',
    selectPlace: 'Select a place',
    optionalInfo: 'This information is optional. Leave empty if not known - AI will calculate',
    nakshatra: 'Nakshatra',
    selectNakshatra: 'Select Nakshatra',
    rasi: 'Rasi',
    selectRasi: 'Select Rasi',
    yourDetails: 'Your Details',
    name: 'Name',
    continue: 'Continue',
    createJathagam: 'Create Jathagam',
    registering: 'Registering...',
    registrationError: 'Registration failed. Please try again.',
  },
};

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

// Intro Slide Component
const IntroSlide = ({ item, isActive }) => {
  const { Icon, IconSecondary } = item;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9, y: 50 }}
      animate={isActive ? { opacity: 1, scale: 1, y: 0 } : { opacity: 0.4, scale: 0.8, y: 50 }}
      transition={{ duration: 0.4 }}
      className="flex flex-col items-center px-6 py-8"
    >
      {/* Icon Container */}
      <div className="relative mb-8">
        <div
          className="w-28 h-28 rounded-full flex items-center justify-center shadow-xl"
          style={{ background: `linear-gradient(135deg, ${item.gradient[0]}, ${item.gradient[1]})` }}
        >
          <Icon size={56} className="text-white" />
        </div>
        <div className="absolute -bottom-1 -right-1 w-11 h-11 rounded-full bg-white shadow-lg flex items-center justify-center">
          <IconSecondary size={22} style={{ color: item.gradient[0] }} />
        </div>
      </div>

      {/* Text Content */}
      <h2 className="text-2xl font-bold text-gray-800 text-center mb-2">{item.title}</h2>
      <p className="text-base font-semibold text-orange-500 text-center mb-4">{item.subtitle}</p>
      <p className="text-gray-600 text-center leading-relaxed mb-6 max-w-sm">{item.description}</p>

      {/* Features */}
      <div className="flex flex-wrap justify-center gap-2">
        {item.features.map((feature, i) => (
          <div
            key={i}
            className="flex items-center gap-1.5 px-3 py-2 rounded-full bg-white border shadow-sm"
            style={{ borderColor: item.gradient[0] }}
          >
            <CheckCircle size={14} style={{ color: item.gradient[0] }} />
            <span className="text-xs font-medium" style={{ color: item.gradient[0] }}>{feature}</span>
          </div>
        ))}
      </div>
    </motion.div>
  );
};

// Paginator Component
const Paginator = ({ data, currentIndex }) => {
  return (
    <div className="flex justify-center gap-2">
      {data.map((item, index) => (
        <div
          key={index}
          className="h-2 rounded-full transition-all duration-300"
          style={{
            width: index === currentIndex ? 24 : 8,
            backgroundColor: item.gradient[0],
            opacity: index === currentIndex ? 1 : 0.3,
          }}
        />
      ))}
    </div>
  );
};

export default function Onboarding() {
  const navigate = useNavigate();
  const [phase, setPhase] = useState('intro'); // 'intro' or 'form'
  const [introIndex, setIntroIndex] = useState(0);
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState('ta');
  const [formData, setFormData] = useState({
    name: '',
    gender: '',
    birthDate: '',
    birthTime: '',
    birthPlace: '',
    nakshatra: '',
    rasi: '',
    language: 'ta',
  });

  const introData = getOnboardingIntro(language);
  const t = translations[language];

  const formSteps = [
    { title: t.basicDetails, subtitle: t.nameAndGender },
    { title: t.birthDetails, subtitle: t.birthInfo },
    { title: t.astroDetails, subtitle: t.nakshatraRasi },
  ];

  // Handle intro navigation
  const handleIntroNext = () => {
    if (introIndex < introData.length - 1) {
      setIntroIndex(introIndex + 1);
    } else {
      setPhase('form');
    }
  };

  const handleIntroSkip = () => {
    setPhase('form');
  };

  // Handle form navigation
  const handleFormNext = async () => {
    if (step < formSteps.length - 1) {
      setStep(step + 1);
    } else {
      setLoading(true);

      try {
        const result = await userAPI.register({ ...formData, language });
        console.log('User registered:', result);

        const profileWithAstro = {
          ...formData,
          language,
          rasi: result.rasi || formData.rasi,
          nakshatra: result.nakshatra || formData.nakshatra,
        };
        localStorage.setItem('userProfile', JSON.stringify(profileWithAstro));
        localStorage.setItem('onboardingComplete', 'true');

        navigate('/dashboard');
      } catch (err) {
        console.error('Registration failed:', err);

        localStorage.setItem('userProfile', JSON.stringify({ ...formData, language }));
        localStorage.setItem('onboardingComplete', 'true');
        navigate('/dashboard');
      } finally {
        setLoading(false);
      }
    }
  };

  const handleFormBack = () => {
    if (step > 0) {
      setStep(step - 1);
    } else {
      setPhase('intro');
      setIntroIndex(introData.length - 1);
    }
  };

  const isStepValid = () => {
    switch (step) {
      case 0: return formData.name && formData.gender;
      case 1: return formData.birthDate && formData.birthTime && formData.birthPlace;
      case 2: return true;
      default: return true;
    }
  };

  const currentIntro = introData[introIndex];
  const isLastIntro = introIndex === introData.length - 1;

  // Intro Phase
  if (phase === 'intro') {
    return (
      <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-orange-50 flex flex-col">
        {/* Header */}
        <div className="flex justify-between items-center px-5 pt-6 pb-2">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6">
              <svg viewBox="0 0 100 100" className="w-full h-full">
                <path
                  d="M50 5 L55 40 L90 30 L60 50 L90 70 L55 60 L50 95 L45 60 L10 70 L40 50 L10 30 L45 40 Z"
                  fill="#f97316"
                />
                <circle cx="50" cy="50" r="10" fill="#fff7ed" />
              </svg>
            </div>
            <span className="text-lg font-bold text-orange-800">jothida.ai</span>
          </div>
          {!isLastIntro && (
            <button
              onClick={handleIntroSkip}
              className="flex items-center gap-1 px-3 py-2 rounded-full bg-gray-100 text-gray-600 text-sm"
            >
              {t.skip}
              <ChevronRight size={16} />
            </button>
          )}
        </div>

        {/* Language Selector */}
        <div className="flex justify-center gap-2 px-5 py-2">
          <button
            onClick={() => setLanguage('ta')}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${
              language === 'ta' ? 'bg-orange-500 text-white' : 'bg-gray-100 text-gray-600'
            }`}
          >
            தமிழ்
          </button>
          <button
            onClick={() => setLanguage('en')}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${
              language === 'en' ? 'bg-orange-500 text-white' : 'bg-gray-100 text-gray-600'
            }`}
          >
            English
          </button>
        </div>

        {/* Slides */}
        <div className="flex-1 flex items-center justify-center overflow-hidden">
          <AnimatePresence mode="wait">
            <IntroSlide key={introIndex} item={currentIntro} isActive={true} />
          </AnimatePresence>
        </div>

        {/* Footer */}
        <div className="px-5 pb-8 space-y-6">
          <Paginator data={introData} currentIndex={introIndex} />

          <button
            onClick={handleIntroNext}
            className="w-full py-4 rounded-full font-semibold text-white flex items-center justify-center gap-2 shadow-lg transition-all"
            style={{ background: `linear-gradient(90deg, ${currentIntro.gradient[0]}, ${currentIntro.gradient[1]})` }}
          >
            {isLastIntro ? t.getStarted : t.next}
            {isLastIntro ? <Rocket size={20} /> : <ChevronRight size={20} />}
          </button>
        </div>
      </div>
    );
  }

  // Form Phase
  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-orange-50">
      {/* Decorative Header */}
      <div className="bg-gradient-to-r from-orange-600 via-red-600 to-orange-600 h-2" />

      {/* Om Symbol Header */}
      <div className="text-center pt-6 pb-3">
        <div className="inline-block">
          <span className="text-5xl text-orange-600 font-serif">ॐ</span>
        </div>
        <h1 className="text-xl font-bold text-orange-800 mt-1 tracking-wide">
          {language === 'en' ? 'Jothida AI' : 'ஜோதிட AI'}
        </h1>
      </div>

      {/* Progress Indicator */}
      <div className="flex justify-center gap-2 px-8 mb-6">
        {formSteps.map((_, i) => (
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
            <div className="text-center mb-6">
              <h2 className="text-xl font-bold text-gray-800">{formSteps[step].title}</h2>
              <p className="text-gray-600 mt-1 text-sm">{formSteps[step].subtitle}</p>
            </div>

            {/* Step 0: Basic Info */}
            {step === 0 && (
              <div className="space-y-5">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {t.yourName}
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    placeholder={t.enterName}
                    className="w-full px-4 py-3 rounded-xl border-2 border-orange-200 focus:border-orange-500 focus:ring-0 outline-none transition-colors bg-white"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {t.gender}
                  </label>
                  <div className="grid grid-cols-2 gap-4">
                    {[
                      { value: 'male', label: t.male, icon: '👨' },
                      { value: 'female', label: t.female, icon: '👩' },
                    ].map((g) => (
                      <button
                        key={g.value}
                        onClick={() => setFormData({ ...formData, gender: g.value })}
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

            {/* Step 1: Birth Details */}
            {step === 1 && (
              <div className="space-y-5">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {t.birthDate}
                  </label>
                  <input
                    type="date"
                    value={formData.birthDate}
                    onChange={(e) => setFormData({ ...formData, birthDate: e.target.value })}
                    className="w-full px-4 py-3 rounded-xl border-2 border-orange-200 focus:border-orange-500 focus:ring-0 outline-none transition-colors bg-white"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {t.birthTime}
                  </label>
                  <input
                    type="time"
                    value={formData.birthTime}
                    onChange={(e) => setFormData({ ...formData, birthTime: e.target.value })}
                    className="w-full px-4 py-3 rounded-xl border-2 border-orange-200 focus:border-orange-500 focus:ring-0 outline-none transition-colors bg-white"
                  />
                  <p className="text-xs text-gray-500 mt-1">{t.timeHint}</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {t.birthPlace}
                  </label>
                  <select
                    value={formData.birthPlace}
                    onChange={(e) => setFormData({ ...formData, birthPlace: e.target.value })}
                    className="w-full px-4 py-3 rounded-xl border-2 border-orange-200 focus:border-orange-500 focus:ring-0 outline-none transition-colors bg-white"
                  >
                    <option value="">{t.selectPlace}</option>
                    {places.map((p) => (
                      <option key={p} value={p}>{p}</option>
                    ))}
                  </select>
                </div>
              </div>
            )}

            {/* Step 2: Astro Details */}
            {step === 2 && (
              <div className="space-y-5">
                <div className="bg-orange-50 rounded-xl p-4 border border-orange-200">
                  <p className="text-sm text-orange-700">
                    <Sparkles className="w-4 h-4 inline mr-1" />
                    {t.optionalInfo}
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {t.nakshatra}
                  </label>
                  <select
                    value={formData.nakshatra}
                    onChange={(e) => setFormData({ ...formData, nakshatra: e.target.value })}
                    className="w-full px-4 py-3 rounded-xl border-2 border-orange-200 focus:border-orange-500 focus:ring-0 outline-none transition-colors bg-white"
                  >
                    <option value="">{t.selectNakshatra}</option>
                    {nakshatras.map((n) => (
                      <option key={n} value={n}>{n}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {t.rasi}
                  </label>
                  <select
                    value={formData.rasi}
                    onChange={(e) => setFormData({ ...formData, rasi: e.target.value })}
                    className="w-full px-4 py-3 rounded-xl border-2 border-orange-200 focus:border-orange-500 focus:ring-0 outline-none transition-colors bg-white"
                  >
                    <option value="">{t.selectRasi}</option>
                    {rasiList.map((r) => (
                      <option key={r} value={r}>{r}</option>
                    ))}
                  </select>
                </div>

                {/* Summary */}
                <div className="bg-white rounded-xl p-4 border border-orange-200 mt-4">
                  <h3 className="font-medium text-gray-800 mb-3">{t.yourDetails}</h3>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-500">{t.name}</span>
                      <span className="text-gray-800">{formData.name || '-'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">{t.birthDate}</span>
                      <span className="text-gray-800">{formData.birthDate || '-'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">{t.birthTime}</span>
                      <span className="text-gray-800">{formData.birthTime || '-'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">{t.birthPlace}</span>
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
          <button
            onClick={handleFormBack}
            className="px-6 py-3 rounded-xl border-2 border-orange-300 text-orange-600 font-medium"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
          <button
            onClick={handleFormNext}
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
                {t.registering}
              </>
            ) : step === formSteps.length - 1 ? (
              <>
                <Sparkles className="w-5 h-5" />
                {t.createJathagam}
              </>
            ) : (
              <>
                {t.continue}
                <ChevronRight className="w-5 h-5" />
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
