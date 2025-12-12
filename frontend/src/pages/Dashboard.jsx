import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  TrendingUp, Moon, Star, Sparkles, Heart, Briefcase,
  GraduationCap, Home, Calendar, ChevronRight, X,
  Flame, Activity
} from 'lucide-react';
import { panchangamAPI, jathagamAPI } from '../services/api';
import axios from 'axios';

// Translation mappings
const translations = {
  ta: {
    greeting: 'வணக்கம்',
    todayScore: 'இன்றைய பலன்',
    tapForDetails: 'விவரங்களுக்கு தட்டவும்',
    panchangam: 'இன்றைய பஞ்சாங்கம்',
    month: 'மாதம்',
    tithi: 'திதி',
    nakshatra: 'நட்சத்திரம்',
    yoga: 'யோகம்',
    lifeAreas: 'வாழ்க்கை பகுதிகள்',
    futureProjections: 'எதிர்கால பலன்கள்',
    monthly: 'மாதம்',
    yearly: 'வருடம்',
    dasha: 'தசை',
    bhukti: 'புக்தி',
    good: 'நல்லது',
    average: 'சாதாரணம்',
    caution: 'எச்சரிக்கை',
    currentYear: 'நடப்பு ஆண்டு',
    nextYear: 'அடுத்த ஆண்டு',
    thirdYear: 'மூன்றாம் ஆண்டு',
    planetAura: 'கிரக ஒளி',
    strongAura: 'வலிமை',
    weakAura: 'பலவீனம்',
    love: 'காதல்',
    career: 'தொழில்',
    education: 'கல்வி',
    family: 'குடும்பம்',
    health: 'உடல்நலம்',
    scoreBreakdown: 'மதிப்பெண் விவரம்',
    close: 'மூடு',
    rahuKalam: 'ராகு காலம்',
    goodTime: 'நல்ல நேரம்',
    normalTime: 'சாதாரண நேரம்',
  },
  en: {
    greeting: 'Hello',
    todayScore: "Today's Score",
    tapForDetails: 'Tap for details',
    panchangam: "Today's Panchangam",
    month: 'Month',
    tithi: 'Tithi',
    nakshatra: 'Nakshatra',
    yoga: 'Yoga',
    lifeAreas: 'Life Areas',
    futureProjections: 'Future Projections',
    monthly: 'Monthly',
    yearly: 'Yearly',
    dasha: 'Dasha',
    bhukti: 'Bhukti',
    good: 'Good',
    average: 'Average',
    caution: 'Caution',
    currentYear: 'Current Year',
    nextYear: 'Next Year',
    thirdYear: 'Third Year',
    planetAura: 'Planet Aura',
    strongAura: 'Strong',
    weakAura: 'Weak',
    love: 'Love',
    career: 'Career',
    education: 'Education',
    family: 'Family',
    health: 'Health',
    scoreBreakdown: 'Score Breakdown',
    close: 'Close',
    rahuKalam: 'Rahu Kalam',
    goodTime: 'Good Time',
    normalTime: 'Normal Time',
  }
};

// Diya (Oil Lamp) SVG Component
const DiyaIcon = ({ size = 40 }) => (
  <svg width={size} height={size} viewBox="0 0 100 100">
    <defs>
      <radialGradient id="flameGlow" cx="50%" cy="20%" r="60%">
        <stop offset="0%" stopColor="#fbbf24" stopOpacity="1" />
        <stop offset="50%" stopColor="#f97316" stopOpacity="0.6" />
        <stop offset="100%" stopColor="#f97316" stopOpacity="0" />
      </radialGradient>
    </defs>
    <ellipse cx="50" cy="22" rx="18" ry="22" fill="url(#flameGlow)" />
    <path d="M50 5 Q58 18 55 30 Q52 38 50 42 Q48 38 45 30 Q42 18 50 5" fill="#f97316" />
    <path d="M50 12 Q54 20 52 28 Q51 34 50 38 Q49 34 48 28 Q46 20 50 12" fill="#fbbf24" />
    <path d="M50 18 Q52 24 51 30 Q50 34 50 36 Q50 34 49 30 Q48 24 50 18" fill="#fff" opacity="0.8" />
    <ellipse cx="50" cy="52" rx="28" ry="10" fill="#d97706" />
    <path d="M22 52 Q22 68 32 78 L68 78 Q78 68 78 52" fill="#d97706" />
    <ellipse cx="50" cy="60" rx="20" ry="6" fill="#b45309" opacity="0.5" />
    <ellipse cx="50" cy="82" rx="22" ry="6" fill="#d97706" />
    <ellipse cx="50" cy="88" rx="18" ry="4" fill="#92400e" />
  </svg>
);

// Decorative Border
const DecorativeBorder = () => (
  <div className="flex items-center w-full py-2">
    <div className="flex-1 h-px bg-gradient-to-r from-transparent via-amber-400 to-transparent" />
    <div className="w-2 h-2 rounded-full bg-orange-500 mx-3" />
    <div className="flex-1 h-px bg-gradient-to-r from-transparent via-amber-400 to-transparent" />
  </div>
);

// Animated Score Circle
const AnimatedScoreCircle = ({ score, onClick, tapText }) => (
  <motion.div
    initial={{ scale: 0, rotate: -180 }}
    animate={{ scale: 1, rotate: 0 }}
    transition={{ type: 'spring', stiffness: 100, damping: 15 }}
    onClick={onClick}
    className="cursor-pointer"
  >
    <div className="relative w-32 h-32 mx-auto">
      <svg className="w-full h-full transform -rotate-90" viewBox="0 0 128 128">
        <circle cx="64" cy="64" r="56" fill="none" stroke="#fed7aa" strokeWidth="8" />
        <motion.circle
          cx="64" cy="64" r="56"
          fill="none"
          stroke="url(#scoreGradient)"
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={`${score * 3.52} 352`}
          initial={{ strokeDasharray: '0 352' }}
          animate={{ strokeDasharray: `${score * 3.52} 352` }}
          transition={{ duration: 1.5, ease: 'easeOut' }}
        />
        <defs>
          <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#f97316" />
            <stop offset="100%" stopColor="#ea580c" />
          </linearGradient>
        </defs>
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-3xl font-bold text-orange-800">{score}%</span>
        <span className="text-xs text-orange-600">{tapText}</span>
      </div>
    </div>
  </motion.div>
);

// Life Area Card
const LifeAreaCard = ({ area, index, onClick, t }) => {
  const icons = {
    love: Heart,
    career: Briefcase,
    education: GraduationCap,
    family: Home,
    health: Activity,
  };
  const Icon = icons[area.key] || Star;

  const getScoreColor = (score) => {
    if (score >= 75) return { bg: 'bg-green-100', text: 'text-green-600', border: 'border-green-200' };
    if (score >= 50) return { bg: 'bg-amber-100', text: 'text-amber-600', border: 'border-amber-200' };
    return { bg: 'bg-red-100', text: 'text-red-600', border: 'border-red-200' };
  };

  const colors = getScoreColor(area.score);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: index * 0.1 }}
      onClick={() => onClick(area)}
      className={`bg-white rounded-xl p-4 shadow-sm border ${colors.border} cursor-pointer hover:shadow-md transition-shadow`}
    >
      <div className="flex items-center justify-between mb-2">
        <div className={`p-2 rounded-lg ${colors.bg}`}>
          <Icon className={`w-5 h-5 ${colors.text}`} />
        </div>
        <span className={`text-xs px-2 py-1 rounded-full ${colors.bg} ${colors.text}`}>
          {area.score >= 75 ? t('good') : area.score >= 50 ? t('average') : t('caution')}
        </span>
      </div>
      <h3 className="font-medium text-gray-800">{area.name}</h3>
      <div className="flex items-center gap-1 mt-1">
        <span className={`text-xl font-bold ${colors.text}`}>{area.score}</span>
        <span className="text-gray-400 text-sm">/100</span>
        <ChevronRight className="w-4 h-4 text-gray-300 ml-auto" />
      </div>
      <div className="mt-2 h-1.5 bg-gray-100 rounded-full overflow-hidden">
        <motion.div
          className={`h-full rounded-full ${area.score >= 75 ? 'bg-green-500' : area.score >= 50 ? 'bg-amber-500' : 'bg-red-500'}`}
          initial={{ width: 0 }}
          animate={{ width: `${area.score}%` }}
          transition={{ delay: index * 0.1 + 0.3, duration: 0.8 }}
        />
      </div>
    </motion.div>
  );
};

// Month Projection Card
const MonthCard = ({ month, index, onClick }) => {
  const getScoreColor = (score) => {
    if (score >= 75) return 'text-green-600 bg-green-50';
    if (score >= 50) return 'text-amber-600 bg-amber-50';
    return 'text-red-600 bg-red-50';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
      onClick={() => onClick(month)}
      className="flex-shrink-0 w-20 bg-white rounded-xl p-3 shadow-sm cursor-pointer hover:shadow-md transition-shadow"
    >
      <p className="text-xs text-gray-500 text-center truncate">{month.name}</p>
      <div className={`text-center mt-1 py-1 px-2 rounded-lg ${getScoreColor(month.score)}`}>
        <span className="font-bold">{month.score}</span>
      </div>
      <div className="mt-2 h-1 bg-gray-100 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full ${month.score >= 75 ? 'bg-green-500' : month.score >= 50 ? 'bg-amber-500' : 'bg-red-500'}`}
          style={{ width: `${month.score}%` }}
        />
      </div>
    </motion.div>
  );
};

// Year Projection Card
const YearCard = ({ year, onClick }) => {
  const getScoreColor = (score) => {
    if (score >= 75) return { main: '#16a34a', light: '#dcfce7' };
    if (score >= 50) return { main: '#d97706', light: '#fef3c7' };
    return { main: '#dc2626', light: '#fee2e2' };
  };

  const colors = getScoreColor(year.score);

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      onClick={() => onClick(year)}
      className="bg-white rounded-xl p-4 shadow-sm cursor-pointer hover:shadow-md transition-shadow flex items-center gap-4"
      style={{ borderLeft: `4px solid ${colors.main}` }}
    >
      <div className="p-2 rounded-lg" style={{ backgroundColor: colors.light }}>
        <Calendar className="w-5 h-5" style={{ color: colors.main }} />
      </div>
      <div className="flex-1">
        <p className="font-medium text-gray-800">{year.year}</p>
        <p className="text-xs text-gray-500">{year.label}</p>
      </div>
      <div className="text-right">
        <span className="text-xl font-bold" style={{ color: colors.main }}>{year.score}%</span>
        <div className="w-16 h-1.5 bg-gray-100 rounded-full mt-1 overflow-hidden">
          <div className="h-full rounded-full" style={{ width: `${year.score}%`, backgroundColor: colors.main }} />
        </div>
      </div>
      <ChevronRight className="w-5 h-5 text-gray-300" />
    </motion.div>
  );
};

// Score Detail Modal
const ScoreModal = ({ data, onClose, t }) => {
  if (!data) return null;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/50 z-50 flex items-end justify-center"
      onClick={onClose}
    >
      <motion.div
        initial={{ y: '100%' }}
        animate={{ y: 0 }}
        exit={{ y: '100%' }}
        transition={{ type: 'spring', damping: 25 }}
        onClick={(e) => e.stopPropagation()}
        className="bg-white rounded-t-3xl w-full max-w-lg max-h-[80vh] overflow-y-auto"
      >
        <div className="sticky top-0 bg-white p-4 border-b flex items-center justify-between">
          <h2 className="text-lg font-bold text-gray-800">{data.title || data.name}</h2>
          <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-full">
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>

        <div className="p-6">
          <div className="text-center mb-6">
            <span className="text-5xl font-bold text-orange-600">{data.score}</span>
            <span className="text-2xl text-gray-400">/100</span>
          </div>

          {data.breakdown && (
            <div className="space-y-3">
              <h3 className="font-medium text-gray-700">{t('scoreBreakdown')}</h3>
              {Object.entries(data.breakdown).map(([key, value]) => (
                <div key={key} className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 capitalize">{key}</span>
                  <div className="flex items-center gap-2">
                    <div className="w-24 h-2 bg-gray-100 rounded-full overflow-hidden">
                      <div className="h-full bg-orange-500 rounded-full" style={{ width: `${Math.min(100, value * 3)}%` }} />
                    </div>
                    <span className="text-sm font-medium w-8 text-right">{value}</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {data.suggestion && (
            <div className="mt-6 p-4 bg-orange-50 rounded-xl">
              <div className="flex items-start gap-3">
                <Sparkles className="w-5 h-5 text-orange-500 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-orange-800">{data.suggestion}</p>
              </div>
            </div>
          )}
        </div>

        <div className="p-4 border-t">
          <button
            onClick={onClose}
            className="w-full py-3 bg-orange-500 text-white rounded-xl font-medium hover:bg-orange-600 transition-colors"
          >
            {t('close')}
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default function Dashboard() {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [userProfile, setUserProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [panchangam, setPanchangam] = useState(null);
  const [jathagam, setJathagam] = useState(null);
  const [lifeAreas, setLifeAreas] = useState(null);
  const [projections, setProjections] = useState(null);
  const [projectionView, setProjectionView] = useState('month');
  const [selectedScore, setSelectedScore] = useState(null);
  const [language] = useState('ta');

  const t = (key) => translations[language]?.[key] || translations['en'][key] || key;

  useEffect(() => {
    const profile = localStorage.getItem('userProfile');
    if (profile) {
      setUserProfile(JSON.parse(profile));
    }

    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    if (userProfile) {
      fetchData();
    } else {
      setLoading(false);
    }
  }, [userProfile, language]);

  const fetchData = async () => {
    try {
      setLoading(true);

      // Fetch panchangam
      const panchangamData = await panchangamAPI.getToday().catch(() => null);
      setPanchangam(panchangamData);

      // For jathagamAPI (uses camelCase)
      const jathagamDetails = {
        name: userProfile?.name || 'User',
        birthDate: userProfile?.birthDate,
        birthTime: userProfile?.birthTime || '12:00',
        birthPlace: userProfile?.birthPlace || 'Chennai',
      };

      // For forecast APIs (uses snake_case)
      const forecastDetails = {
        name: userProfile?.name || 'User',
        birth_date: userProfile?.birthDate,
        birth_time: userProfile?.birthTime || '12:00',
        birth_place: userProfile?.birthPlace || 'Chennai',
        latitude: 13.0827,
        longitude: 80.2707,
        language: language,
      };

      // Fetch all data in parallel (use relative URLs for vite proxy)
      const [jathagamData, lifeAreasData, projectionsData] = await Promise.all([
        jathagamAPI.generate(jathagamDetails).catch(() => null),
        axios.post('/api/forecast/life-areas', forecastDetails).then(r => r.data).catch(() => null),
        axios.post('/api/forecast/future-projections', forecastDetails).then(r => r.data).catch(() => null),
      ]);

      setJathagam(jathagamData);
      setLifeAreas(lifeAreasData);
      setProjections(projectionsData);

    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCurrentPeriod = () => {
    const hour = currentTime.getHours();
    if (hour >= 15 && hour < 17) return { label: t('rahuKalam'), color: 'text-red-600', bg: 'bg-red-50' };
    if (hour >= 9 && hour < 11) return { label: t('goodTime'), color: 'text-green-600', bg: 'bg-green-50' };
    return { label: t('normalTime'), color: 'text-orange-600', bg: 'bg-orange-50' };
  };

  const period = getCurrentPeriod();

  // Get overall score
  const getOverallScore = () => {
    if (lifeAreas?.life_areas) {
      const areas = Object.values(lifeAreas.life_areas);
      const sum = areas.reduce((acc, area) => acc + (area.score || 0), 0);
      return Math.round(sum / areas.length);
    }
    return jathagam?.overall_score || 55;
  };

  // Format life areas for display
  const getLifeAreasForDisplay = () => {
    if (!lifeAreas?.life_areas) return [];

    const areaConfig = {
      love: { key: 'love', name: t('love'), color: '#ec4899' },
      career: { key: 'career', name: t('career'), color: '#3b82f6' },
      education: { key: 'education', name: t('education'), color: '#8b5cf6' },
      family: { key: 'family', name: t('family'), color: '#10b981' },
      health: { key: 'health', name: t('health'), color: '#f59e0b' },
    };

    return Object.entries(lifeAreas.life_areas).map(([key, data]) => ({
      key,
      name: areaConfig[key]?.name || key,
      score: data.score || 50,
      color: areaConfig[key]?.color || '#6b7280',
      suggestion: data.suggestion,
      factors: data.factors,
      breakdown: data.breakdown,
    }));
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-orange-50 to-white flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
          >
            <DiyaIcon size={60} />
          </motion.div>
          <p className="text-orange-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-orange-50 pb-24">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-orange-500 to-orange-600 text-white p-4 pt-6"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
              <span className="text-xl">ॐ</span>
            </div>
            <div>
              <h1 className="text-lg font-bold">ஜோதிட AI</h1>
              <p className="text-orange-100 text-sm">
                {t('greeting')}, {userProfile?.name || 'User'}
              </p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-2xl font-bold">
              {currentTime.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', hour12: true })}
            </p>
            <span className={`text-xs px-2 py-0.5 rounded-full ${period.bg} ${period.color}`}>
              {period.label}
            </span>
          </div>
        </div>

        {/* User Info Card */}
        {jathagam && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="mt-4 bg-white/10 backdrop-blur rounded-xl p-3"
          >
            <div className="flex items-center gap-4 text-sm">
              <div className="flex items-center gap-1">
                <Moon className="w-4 h-4" />
                <span>{jathagam.rasi || jathagam.moon_sign?.rasi}</span>
              </div>
              <div className="flex items-center gap-1">
                <Star className="w-4 h-4" />
                <span>{jathagam.nakshatra || jathagam.moon_sign?.nakshatra}</span>
              </div>
              <div className="flex items-center gap-1 ml-auto">
                <Sparkles className="w-4 h-4" />
                <span>{jathagam.dasha?.current?.lord || 'Saturn'} {t('dasha')}</span>
              </div>
            </div>
          </motion.div>
        )}
      </motion.div>

      <div className="p-4 space-y-6">
        {/* Today's Score */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl p-6 shadow-sm"
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-gray-800 flex items-center gap-2">
              <Flame className="w-5 h-5 text-orange-500" />
              {t('todayScore')}
            </h2>
            <DiyaIcon size={32} />
          </div>

          <AnimatedScoreCircle
            score={getOverallScore()}
            onClick={() => setSelectedScore({
              title: t('todayScore'),
              score: getOverallScore(),
              breakdown: jathagam?.breakdown,
            })}
            tapText={t('tapForDetails')}
          />

          {jathagam?.dasha?.current && (
            <div className="mt-4 text-center">
              <p className="text-sm text-gray-500">
                {jathagam.dasha.current.lord} {t('dasha')} / {jathagam.dasha.current.antardasha_lord || 'Jupiter'} {t('bhukti')}
              </p>
            </div>
          )}
        </motion.div>

        <DecorativeBorder />

        {/* Panchangam */}
        {panchangam && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl p-4 shadow-sm"
          >
            <h2 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
              <Calendar className="w-5 h-5 text-orange-500" />
              {t('panchangam')}
            </h2>
            <div className="grid grid-cols-4 gap-2">
              {[
                { label: t('month'), value: panchangam.tamil_month || panchangam.month },
                { label: t('tithi'), value: panchangam.tithi?.tamil || panchangam.tithi?.name || panchangam.tithi },
                { label: t('nakshatra'), value: panchangam.nakshatra?.tamil || panchangam.nakshatra?.name || panchangam.nakshatra },
                { label: t('yoga'), value: panchangam.yoga?.tamil || panchangam.yoga?.name || panchangam.yoga },
              ].map((item, i) => (
                <div key={i} className="text-center p-2 bg-orange-50 rounded-lg">
                  <p className="text-xs text-gray-500">{item.label}</p>
                  <p className="text-sm font-medium text-orange-800 truncate">{typeof item.value === 'object' ? '-' : (item.value || '-')}</p>
                </div>
              ))}
            </div>
          </motion.div>
        )}

        {/* Life Areas */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h2 className="text-lg font-bold text-gray-800 mb-3 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-orange-500" />
            {t('lifeAreas')}
          </h2>
          <div className="grid grid-cols-2 gap-3">
            {getLifeAreasForDisplay().slice(0, 4).map((area, index) => (
              <LifeAreaCard
                key={area.key}
                area={area}
                index={index}
                onClick={setSelectedScore}
                t={t}
              />
            ))}
          </div>
        </motion.div>

        <DecorativeBorder />

        {/* Future Projections */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-lg font-bold text-gray-800 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-orange-500" />
              {t('futureProjections')}
            </h2>
            <div className="flex gap-1 bg-gray-100 rounded-lg p-1">
              <button
                onClick={() => setProjectionView('month')}
                className={`px-3 py-1 text-sm rounded-md transition-colors ${
                  projectionView === 'month' ? 'bg-white shadow text-orange-600' : 'text-gray-500'
                }`}
              >
                {t('monthly')}
              </button>
              <button
                onClick={() => setProjectionView('year')}
                className={`px-3 py-1 text-sm rounded-md transition-colors ${
                  projectionView === 'year' ? 'bg-white shadow text-orange-600' : 'text-gray-500'
                }`}
              >
                {t('yearly')}
              </button>
            </div>
          </div>

          {projectionView === 'month' && projections?.projections?.monthly && (
            <div className="flex gap-3 overflow-x-auto pb-2 -mx-4 px-4 scrollbar-hide">
              {projections.projections.monthly.map((month, index) => (
                <MonthCard key={index} month={month} index={index} onClick={setSelectedScore} />
              ))}
            </div>
          )}

          {projectionView === 'year' && projections?.projections?.yearly && (
            <div className="space-y-3">
              {projections.projections.yearly.map((year, index) => (
                <YearCard key={index} year={year} onClick={setSelectedScore} />
              ))}
            </div>
          )}
        </motion.div>
      </div>

      {/* Score Modal */}
      <AnimatePresence>
        {selectedScore && (
          <ScoreModal
            data={selectedScore}
            onClose={() => setSelectedScore(null)}
            t={t}
          />
        )}
      </AnimatePresence>
    </div>
  );
}
