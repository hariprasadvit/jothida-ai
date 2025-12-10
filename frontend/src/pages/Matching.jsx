import { useState, useEffect } from 'react';
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer } from 'recharts';
import { Heart, AlertTriangle, CheckCircle, XCircle, Sparkles, Users, ChevronDown, ChevronUp, Loader2, User, Calendar, Clock, MapPin, RefreshCw } from 'lucide-react';
import { matchingAPI, getCityCoordinates } from '../services/api';

// Tamil city options
const cities = [
  'Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem',
  'Tirunelveli', 'Tiruppur', 'Erode', 'Vellore', 'Thoothukudi',
  'Dindigul', 'Thanjavur', 'Ranipet', 'Sivakasi', 'Karur',
  'Udhagamandalam', 'Hosur', 'Nagercoil', 'Kanchipuram', 'Kumbakonam'
];

// Nakshatra options
const nakshatras = [
  'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
  'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
  'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
  'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
  'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
];

// Rasi options
const rasis = [
  { english: 'Mesha', tamil: 'மேஷம்' },
  { english: 'Vrishabha', tamil: 'ரிஷபம்' },
  { english: 'Mithuna', tamil: 'மிதுனம்' },
  { english: 'Kataka', tamil: 'கடகம்' },
  { english: 'Simha', tamil: 'சிம்மம்' },
  { english: 'Kanya', tamil: 'கன்னி' },
  { english: 'Tula', tamil: 'துலாம்' },
  { english: 'Vrischika', tamil: 'விருச்சிகம்' },
  { english: 'Dhanus', tamil: 'தனுசு' },
  { english: 'Makara', tamil: 'மகரம்' },
  { english: 'Kumbha', tamil: 'கும்பம்' },
  { english: 'Meena', tamil: 'மீனம்' },
];

export default function Matching() {
  const [step, setStep] = useState('input'); // 'input' | 'loading' | 'result'
  const [groomData, setGroomData] = useState({
    name: '',
    birthDate: '',
    birthTime: '',
    birthPlace: 'Chennai',
    nakshatra: '',
    rasi: '',
  });
  const [brideData, setBrideData] = useState({
    name: '',
    birthDate: '',
    birthTime: '',
    birthPlace: 'Chennai',
    nakshatra: '',
    rasi: '',
  });

  const [matchResult, setMatchResult] = useState(null);
  const [overallMatch, setOverallMatch] = useState(0);
  const [animationComplete, setAnimationComplete] = useState(false);
  const [expandedPorutham, setExpandedPorutham] = useState(null);
  const [error, setError] = useState(null);

  // Load user profile as groom/bride default
  useEffect(() => {
    const profile = localStorage.getItem('userProfile');
    if (profile) {
      const userData = JSON.parse(profile);
      // Set as groom by default
      setGroomData({
        name: userData.name || '',
        birthDate: userData.birthDate || '',
        birthTime: userData.birthTime || '',
        birthPlace: userData.birthPlace || 'Chennai',
        nakshatra: userData.nakshatra || '',
        rasi: userData.rasi || '',
      });
    }
  }, []);

  const handleCalculateMatching = async () => {
    setStep('loading');
    setError(null);

    try {
      const groomCoords = getCityCoordinates(groomData.birthPlace);
      const brideCoords = getCityCoordinates(brideData.birthPlace);

      const payload = {
        groom: {
          name: groomData.name,
          birth_date: groomData.birthDate,
          birth_time: groomData.birthTime,
          birth_place: groomData.birthPlace,
          latitude: groomCoords.lat,
          longitude: groomCoords.lon,
          nakshatra: groomData.nakshatra || null,
          rasi: groomData.rasi || null,
        },
        bride: {
          name: brideData.name,
          birth_date: brideData.birthDate,
          birth_time: brideData.birthTime,
          birth_place: brideData.birthPlace,
          latitude: brideCoords.lat,
          longitude: brideCoords.lon,
          nakshatra: brideData.nakshatra || null,
          rasi: brideData.rasi || null,
        }
      };

      const result = await matchingAPI.calculate(payload);
      setMatchResult(result);
      setStep('result');

      // Animate score
      let current = 0;
      const target = result.overall_score || 0;
      const timer = setInterval(() => {
        current += 2;
        if (current >= target) {
          setOverallMatch(target);
          setAnimationComplete(true);
          clearInterval(timer);
        } else {
          setOverallMatch(current);
        }
      }, 30);
    } catch (err) {
      console.error('Matching calculation error:', err);
      setError('பொருத்தம் கணக்கிடுவதில் பிழை. மீண்டும் முயற்சிக்கவும்.');
      setStep('input');
    }
  };

  const getStatusStyle = (status) => {
    switch (status) {
      case 'excellent': return { bg: 'bg-green-50', border: 'border-green-200', text: 'text-green-700', bar: 'bg-green-500' };
      case 'good': return { bg: 'bg-blue-50', border: 'border-blue-200', text: 'text-blue-700', bar: 'bg-blue-500' };
      case 'warning': return { bg: 'bg-yellow-50', border: 'border-yellow-200', text: 'text-yellow-700', bar: 'bg-yellow-500' };
      case 'critical': return { bg: 'bg-red-50', border: 'border-red-200', text: 'text-red-700', bar: 'bg-red-500' };
      default: return { bg: 'bg-gray-50', border: 'border-gray-200', text: 'text-gray-700', bar: 'bg-gray-500' };
    }
  };

  const resetForm = () => {
    setStep('input');
    setMatchResult(null);
    setOverallMatch(0);
    setAnimationComplete(false);
    setExpandedPorutham(null);
  };

  // Input Form
  if (step === 'input') {
    return (
      <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-orange-50 pb-24">
        <div className="bg-gradient-to-r from-red-500 via-pink-500 to-red-500 h-1" />

        <div className="bg-white border-b border-orange-100 px-4 py-4">
          <h1 className="text-xl font-bold text-red-800 flex items-center gap-2">
            <Heart className="w-5 h-5 text-red-500" />
            திருமண பொருத்தம்
          </h1>
          <p className="text-gray-500 text-sm">10 பொருத்த பகுப்பாய்வு</p>
        </div>

        {error && (
          <div className="mx-4 mt-4 p-3 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm">
            {error}
          </div>
        )}

        {/* Groom Details */}
        <div className="mx-4 mt-4 bg-white rounded-2xl border border-blue-200 p-4 shadow-sm">
          <h2 className="font-semibold text-blue-800 mb-4 flex items-center gap-2">
            <User className="w-4 h-4" />
            மணமகன் விவரங்கள்
          </h2>

          <div className="space-y-3">
            <div>
              <label className="text-xs text-gray-500 mb-1 block">பெயர் *</label>
              <input
                type="text"
                value={groomData.name}
                onChange={(e) => setGroomData({ ...groomData, name: e.target.value })}
                className="w-full p-3 border border-gray-200 rounded-xl focus:border-blue-400 focus:ring-2 focus:ring-blue-100"
                placeholder="பெயர் உள்ளிடவும்"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs text-gray-500 mb-1 block flex items-center gap-1">
                  <Calendar className="w-3 h-3" /> பிறந்த தேதி *
                </label>
                <input
                  type="date"
                  value={groomData.birthDate}
                  onChange={(e) => setGroomData({ ...groomData, birthDate: e.target.value })}
                  className="w-full p-3 border border-gray-200 rounded-xl focus:border-blue-400 focus:ring-2 focus:ring-blue-100"
                />
              </div>
              <div>
                <label className="text-xs text-gray-500 mb-1 block flex items-center gap-1">
                  <Clock className="w-3 h-3" /> பிறந்த நேரம் *
                </label>
                <input
                  type="time"
                  value={groomData.birthTime}
                  onChange={(e) => setGroomData({ ...groomData, birthTime: e.target.value })}
                  className="w-full p-3 border border-gray-200 rounded-xl focus:border-blue-400 focus:ring-2 focus:ring-blue-100"
                />
              </div>
            </div>

            <div>
              <label className="text-xs text-gray-500 mb-1 block flex items-center gap-1">
                <MapPin className="w-3 h-3" /> பிறந்த இடம் *
              </label>
              <select
                value={groomData.birthPlace}
                onChange={(e) => setGroomData({ ...groomData, birthPlace: e.target.value })}
                className="w-full p-3 border border-gray-200 rounded-xl focus:border-blue-400 focus:ring-2 focus:ring-blue-100"
              >
                {cities.map(city => (
                  <option key={city} value={city}>{city}</option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs text-gray-500 mb-1 block">நட்சத்திரம் (விரும்பினால்)</label>
                <select
                  value={groomData.nakshatra}
                  onChange={(e) => setGroomData({ ...groomData, nakshatra: e.target.value })}
                  className="w-full p-3 border border-gray-200 rounded-xl focus:border-blue-400 focus:ring-2 focus:ring-blue-100 text-sm"
                >
                  <option value="">தானாக கணக்கிடு</option>
                  {nakshatras.map(nak => (
                    <option key={nak} value={nak}>{nak}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-xs text-gray-500 mb-1 block">ராசி (விரும்பினால்)</label>
                <select
                  value={groomData.rasi}
                  onChange={(e) => setGroomData({ ...groomData, rasi: e.target.value })}
                  className="w-full p-3 border border-gray-200 rounded-xl focus:border-blue-400 focus:ring-2 focus:ring-blue-100 text-sm"
                >
                  <option value="">தானாக கணக்கிடு</option>
                  {rasis.map(r => (
                    <option key={r.english} value={r.english}>{r.tamil}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Bride Details */}
        <div className="mx-4 mt-4 bg-white rounded-2xl border border-pink-200 p-4 shadow-sm">
          <h2 className="font-semibold text-pink-800 mb-4 flex items-center gap-2">
            <User className="w-4 h-4" />
            மணமகள் விவரங்கள்
          </h2>

          <div className="space-y-3">
            <div>
              <label className="text-xs text-gray-500 mb-1 block">பெயர் *</label>
              <input
                type="text"
                value={brideData.name}
                onChange={(e) => setBrideData({ ...brideData, name: e.target.value })}
                className="w-full p-3 border border-gray-200 rounded-xl focus:border-pink-400 focus:ring-2 focus:ring-pink-100"
                placeholder="பெயர் உள்ளிடவும்"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs text-gray-500 mb-1 block flex items-center gap-1">
                  <Calendar className="w-3 h-3" /> பிறந்த தேதி *
                </label>
                <input
                  type="date"
                  value={brideData.birthDate}
                  onChange={(e) => setBrideData({ ...brideData, birthDate: e.target.value })}
                  className="w-full p-3 border border-gray-200 rounded-xl focus:border-pink-400 focus:ring-2 focus:ring-pink-100"
                />
              </div>
              <div>
                <label className="text-xs text-gray-500 mb-1 block flex items-center gap-1">
                  <Clock className="w-3 h-3" /> பிறந்த நேரம் *
                </label>
                <input
                  type="time"
                  value={brideData.birthTime}
                  onChange={(e) => setBrideData({ ...brideData, birthTime: e.target.value })}
                  className="w-full p-3 border border-gray-200 rounded-xl focus:border-pink-400 focus:ring-2 focus:ring-pink-100"
                />
              </div>
            </div>

            <div>
              <label className="text-xs text-gray-500 mb-1 block flex items-center gap-1">
                <MapPin className="w-3 h-3" /> பிறந்த இடம் *
              </label>
              <select
                value={brideData.birthPlace}
                onChange={(e) => setBrideData({ ...brideData, birthPlace: e.target.value })}
                className="w-full p-3 border border-gray-200 rounded-xl focus:border-pink-400 focus:ring-2 focus:ring-pink-100"
              >
                {cities.map(city => (
                  <option key={city} value={city}>{city}</option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs text-gray-500 mb-1 block">நட்சத்திரம் (விரும்பினால்)</label>
                <select
                  value={brideData.nakshatra}
                  onChange={(e) => setBrideData({ ...brideData, nakshatra: e.target.value })}
                  className="w-full p-3 border border-gray-200 rounded-xl focus:border-pink-400 focus:ring-2 focus:ring-pink-100 text-sm"
                >
                  <option value="">தானாக கணக்கிடு</option>
                  {nakshatras.map(nak => (
                    <option key={nak} value={nak}>{nak}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-xs text-gray-500 mb-1 block">ராசி (விரும்பினால்)</label>
                <select
                  value={brideData.rasi}
                  onChange={(e) => setBrideData({ ...brideData, rasi: e.target.value })}
                  className="w-full p-3 border border-gray-200 rounded-xl focus:border-pink-400 focus:ring-2 focus:ring-pink-100 text-sm"
                >
                  <option value="">தானாக கணக்கிடு</option>
                  {rasis.map(r => (
                    <option key={r.english} value={r.english}>{r.tamil}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Calculate Button */}
        <div className="mx-4 mt-6">
          <button
            onClick={handleCalculateMatching}
            disabled={!groomData.name || !groomData.birthDate || !groomData.birthTime || !brideData.name || !brideData.birthDate || !brideData.birthTime}
            className="w-full bg-gradient-to-r from-red-500 to-pink-500 text-white p-4 rounded-xl flex items-center justify-center gap-2 font-medium shadow-lg shadow-red-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Heart className="w-5 h-5" />
            பொருத்தம் கணக்கிடு
          </button>
        </div>
      </div>
    );
  }

  // Loading State
  if (step === 'loading') {
    return (
      <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-orange-50 flex items-center justify-center">
        <div className="text-center">
          <div className="relative">
            <Heart className="w-16 h-16 text-red-500 animate-pulse mx-auto" />
            <Loader2 className="w-8 h-8 text-pink-500 animate-spin absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
          </div>
          <p className="text-gray-600 mt-4">10 பொருத்தங்களை கணக்கிடுகிறது...</p>
          <p className="text-gray-400 text-sm mt-2">Swiss Ephemeris பயன்படுத்தி துல்லியமாக கணக்கிடப்படுகிறது</p>
        </div>
      </div>
    );
  }

  // Results Display
  if (!matchResult) return null;

  const poruthams = matchResult.poruthams || [];
  const doshaStatus = matchResult.doshas || [];
  const compatibilityAreas = matchResult.compatibility_radar || [];
  const matchedCount = poruthams.filter(p => p.matched).length;
  const criticalCount = poruthams.filter(p => p.status === 'critical').length;

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-orange-50 pb-24">
      {/* Decorative Header */}
      <div className="bg-gradient-to-r from-red-500 via-pink-500 to-red-500 h-1" />

      {/* Header */}
      <div className="bg-white border-b border-orange-100 px-4 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-red-800 flex items-center gap-2">
              <Heart className="w-5 h-5 text-red-500" />
              திருமண பொருத்தம்
            </h1>
            <p className="text-gray-500 text-sm">10 பொருத்த பகுப்பாய்வு</p>
          </div>
          <button
            onClick={resetForm}
            className="p-2 bg-orange-50 rounded-lg border border-orange-200 hover:bg-orange-100"
          >
            <RefreshCw className="w-5 h-5 text-orange-600" />
          </button>
        </div>
      </div>

      {/* Couple Names */}
      <div className="mx-4 mt-4 bg-white rounded-2xl border border-orange-200 p-4 shadow-sm">
        <div className="flex items-center justify-center gap-4">
          <div className="text-center">
            <div className="w-12 h-12 rounded-full bg-gradient-to-r from-blue-400 to-blue-500 flex items-center justify-center text-white text-lg font-bold mx-auto shadow">
              {groomData.name?.charAt(0) || 'அ'}
            </div>
            <p className="text-sm font-medium text-gray-800 mt-2">{groomData.name}</p>
            <p className="text-xs text-gray-500">{matchResult.groom_nakshatra || groomData.nakshatra}</p>
          </div>
          <Heart className="w-8 h-8 text-red-500" />
          <div className="text-center">
            <div className="w-12 h-12 rounded-full bg-gradient-to-r from-pink-400 to-pink-500 flex items-center justify-center text-white text-lg font-bold mx-auto shadow">
              {brideData.name?.charAt(0) || 'ப'}
            </div>
            <p className="text-sm font-medium text-gray-800 mt-2">{brideData.name}</p>
            <p className="text-xs text-gray-500">{matchResult.bride_nakshatra || brideData.nakshatra}</p>
          </div>
        </div>
      </div>

      {/* Main Score Card */}
      <div className="mx-4 mt-4 bg-white rounded-2xl border border-red-200 p-4 shadow-sm">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-gray-500 text-sm mb-1">ஒட்டுமொத்த பொருத்தம்</p>
            <div className="flex items-baseline gap-2">
              <span className="text-5xl font-bold text-red-600">{overallMatch.toFixed(1)}</span>
              <span className="text-gray-400 text-xl">/100</span>
            </div>
            <div className="flex items-center gap-3 mt-2">
              <span className="flex items-center gap-1 text-green-600 text-sm">
                <CheckCircle className="w-4 h-4" />
                {matchedCount}/10 பொருந்தும்
              </span>
              {criticalCount > 0 && (
                <span className="flex items-center gap-1 text-red-600 text-sm">
                  <AlertTriangle className="w-4 h-4" />
                  {criticalCount} கவனம்
                </span>
              )}
            </div>
          </div>

          {/* Radar Chart */}
          {compatibilityAreas.length > 0 && (
            <div className="w-32 h-32">
              <ResponsiveContainer>
                <RadarChart data={compatibilityAreas}>
                  <PolarGrid stroke="#fecaca" />
                  <PolarAngleAxis dataKey="subject" tick={{ fill: '#6b7280', fontSize: 8 }} />
                  <Radar name="Match" dataKey="A" stroke="#dc2626" fill="#dc2626" fillOpacity={0.2} strokeWidth={2} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>

        {/* AI Verdict */}
        <div className={`mt-4 p-3 rounded-xl ${overallMatch >= 70 ? 'bg-green-50 border border-green-200' : overallMatch >= 50 ? 'bg-yellow-50 border border-yellow-200' : 'bg-red-50 border border-red-200'}`}>
          <div className="flex items-start gap-2">
            <Sparkles className={`w-5 h-5 mt-0.5 ${overallMatch >= 70 ? 'text-green-600' : overallMatch >= 50 ? 'text-yellow-600' : 'text-red-600'}`} />
            <div>
              <span className={`font-medium ${overallMatch >= 70 ? 'text-green-700' : overallMatch >= 50 ? 'text-yellow-700' : 'text-red-700'}`}>
                AI தீர்ப்பு: {matchResult.ai_verdict?.verdict || (overallMatch >= 70 ? 'நல்ல பொருத்தம்' : 'கவனிக்க வேண்டும்')}
              </span>
              <p className="text-gray-600 text-sm mt-1">
                {matchResult.ai_verdict?.explanation || 'விரிவான பகுப்பாய்வு கீழே உள்ளது.'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* 10 Poruthams */}
      <div className="mx-4 mt-4 bg-white rounded-2xl border border-orange-200 p-4 shadow-sm">
        <h2 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
          <span className="text-orange-600">॥</span>
          10 பொருத்தங்கள்
          <span className="text-orange-600">॥</span>
        </h2>

        <div className="space-y-2">
          {poruthams.map((p, i) => {
            const style = getStatusStyle(p.status);
            const isExpanded = expandedPorutham === i;
            return (
              <div
                key={i}
                className={`rounded-xl border ${style.border} overflow-hidden transition-all`}
              >
                <button
                  onClick={() => setExpandedPorutham(isExpanded ? null : i)}
                  className={`w-full p-3 ${style.bg} flex items-center justify-between`}
                >
                  <div className="flex items-center gap-2">
                    {p.matched ? <CheckCircle className="w-4 h-4 text-green-600" /> : <XCircle className="w-4 h-4 text-red-600" />}
                    <span className="font-medium text-gray-800 text-sm">{p.name}</span>
                    <span className="text-gray-400 text-xs">({p.english})</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`font-bold ${style.text}`}>{p.score}%</span>
                    {isExpanded ? <ChevronUp className="w-4 h-4 text-gray-400" /> : <ChevronDown className="w-4 h-4 text-gray-400" />}
                  </div>
                </button>

                {/* Progress bar */}
                <div className="px-3 pb-2 pt-1 bg-white">
                  <div className="w-full bg-gray-100 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all duration-1000 ${style.bar}`}
                      style={{ width: animationComplete ? `${p.score}%` : '0%' }}
                    />
                  </div>
                </div>

                {isExpanded && (
                  <div className="px-3 pb-3 bg-white border-t border-gray-100">
                    <p className="text-gray-600 text-sm py-2">{p.description}</p>
                    {p.remedy && (
                      <div className="p-2 bg-orange-50 rounded-lg border border-orange-200">
                        <p className="text-orange-700 text-xs flex items-start gap-1">
                          <Sparkles className="w-3 h-3 mt-0.5" />
                          பரிகாரம்: {p.remedy}
                        </p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Dosha Analysis */}
      {doshaStatus.length > 0 && (
        <div className="mx-4 mt-4 bg-white rounded-2xl border border-orange-200 p-4 shadow-sm">
          <h2 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-orange-600" />
            தோஷ பகுப்பாய்வு
          </h2>

          <div className="space-y-3">
            {doshaStatus.map((d, i) => (
              <div key={i} className="p-3 bg-gray-50 rounded-xl border border-gray-200">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-800">{d.name}</span>
                  <span className={`text-xs px-2 py-1 rounded-full ${d.compatible ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                    {d.compatible ? 'பொருந்தும்' : 'கவனிக்கவும்'}
                  </span>
                </div>
                <div className="flex items-center gap-6 text-sm">
                  <div className="flex items-center gap-2">
                    <span className="text-gray-500">மணமகன்:</span>
                    <span className={`px-2 py-0.5 rounded ${d.groom ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
                      {d.groom ? 'உள்ளது' : 'இல்லை'}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-gray-500">மணமகள்:</span>
                    <span className={`px-2 py-0.5 rounded ${d.bride ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
                      {d.bride ? 'உள்ளது' : 'இல்லை'}
                    </span>
                  </div>
                </div>
                {d.remedy && !d.compatible && (
                  <p className="text-xs text-orange-600 mt-2 flex items-center gap-1">
                    <Sparkles className="w-3 h-3" />
                    பரிகாரம்: {d.remedy}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="mx-4 mt-4 grid grid-cols-2 gap-3">
        <button className="bg-gradient-to-r from-red-500 to-pink-500 text-white p-4 rounded-xl flex items-center justify-center gap-2 font-medium shadow-lg shadow-red-500/20">
          <Sparkles className="w-5 h-5" />
          முழு அறிக்கை
        </button>
        <button
          onClick={resetForm}
          className="bg-white border border-orange-200 text-gray-700 p-4 rounded-xl flex items-center justify-center gap-2 font-medium"
        >
          <Users className="w-5 h-5 text-orange-600" />
          புதிய பொருத்தம்
        </button>
      </div>
    </div>
  );
}
