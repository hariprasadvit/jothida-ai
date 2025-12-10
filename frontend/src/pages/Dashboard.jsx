import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ResponsiveContainer, RadialBarChart, RadialBar } from 'recharts';
import { TrendingUp, Sun, Star, Clock, Sparkles, Heart, Briefcase, GraduationCap, Home, MessageCircle, Calendar, Users, Loader2, RefreshCw } from 'lucide-react';
import { useDashboardData } from '../hooks/useAstroData';
import { forecastAPI } from '../services/api';
import ScoreBreakdown from '../components/ScoreBreakdown';
import UserProfileBanner from '../components/UserProfileBanner';

// Icon mapping for life areas
const iconMap = {
  'Heart': Heart,
  'Briefcase': Briefcase,
  'GraduationCap': GraduationCap,
  'Home': Home,
};

// Planet symbols
const planetSymbols = {
  'Sun': '☉',
  'Moon': '☽',
  'Mars': '♂',
  'Mercury': '☿',
  'Jupiter': '♃',
  'Venus': '♀',
  'Saturn': '♄',
  'Rahu': '☊',
  'Ketu': '☋',
};

// Planet names in Tamil
const planetTamilNames = {
  'Sun': 'சூரியன்',
  'Moon': 'சந்திரன்',
  'Mars': 'செவ்வாய்',
  'Mercury': 'புதன்',
  'Jupiter': 'குரு',
  'Venus': 'சுக்கிரன்',
  'Saturn': 'சனி',
  'Rahu': 'ராகு',
  'Ketu': 'கேது',
};

// Rasi names in Tamil
const rasiTamilNames = {
  'Mesha': 'மேஷம்',
  'Vrishabha': 'ரிஷபம்',
  'Mithuna': 'மிதுனம்',
  'Kataka': 'கடகம்',
  'Simha': 'சிம்மம்',
  'Kanya': 'கன்னி',
  'Tula': 'துலாம்',
  'Vrischika': 'விருச்சிகம்',
  'Dhanus': 'தனுசு',
  'Makara': 'மகரம்',
  'Kumbha': 'கும்பம்',
  'Meena': 'மீனம்',
};

export default function Dashboard() {
  const navigate = useNavigate();
  const [currentTime, setCurrentTime] = useState(new Date());
  const [userProfile, setUserProfile] = useState(null);
  const [forecast, setForecast] = useState(null);
  const [forecastLoading, setForecastLoading] = useState(false);
  const [expandedForecast, setExpandedForecast] = useState('week'); // 'week', 'month', 'year', '3year'

  useEffect(() => {
    // Check onboarding
    const onboardingComplete = localStorage.getItem('onboardingComplete');
    if (!onboardingComplete) {
      navigate('/onboarding');
      return;
    }

    const profile = localStorage.getItem('userProfile');
    if (profile) {
      setUserProfile(JSON.parse(profile));
    }

    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(timer);
  }, [navigate]);

  // Fetch real data using the hook
  const dashboardData = useDashboardData(userProfile);

  // Fetch forecast data when dashboardData.userRasi is available (comes from jathagam API)
  useEffect(() => {
    const fetchForecast = async () => {
      // Primary: use dashboardData.userRasi (from jathagam API - most accurate)
      // Fallback: use userProfile.rasi (from onboarding - may be empty)
      const rasi = dashboardData?.userRasi || (userProfile?.rasi && userProfile.rasi.trim());
      const nakshatra = dashboardData?.userNakshatra || (userProfile?.nakshatra && userProfile.nakshatra.trim()) || '';

      console.log('Forecast fetch - rasi:', rasi, 'nakshatra:', nakshatra, 'isLoading:', dashboardData?.isLoading);

      // Wait for dashboardData to finish loading before deciding there's no rasi
      if (!rasi) {
        if (dashboardData?.isLoading || dashboardData?.isJathagamLoading) {
          console.log('Still loading, waiting for rasi...');
          return;
        }
        console.log('No rasi found after loading complete');
        return;
      }

      // Don't refetch if we already have forecast data
      if (forecast) {
        console.log('Forecast already loaded');
        return;
      }

      setForecastLoading(true);
      try {
        console.log('Fetching forecast for:', rasi, nakshatra);
        const data = await forecastAPI.getUserForecast(
          rasi,
          nakshatra,
          userProfile?.birthDate,
          13.0827,
          80.2707
        );
        console.log('Forecast data received:', data);
        setForecast(data);
      } catch (error) {
        console.error('Failed to fetch forecast:', error);
      } finally {
        setForecastLoading(false);
      }
    };

    fetchForecast();
  }, [dashboardData?.userRasi, dashboardData?.userNakshatra, dashboardData?.isLoading, dashboardData?.isJathagamLoading, userProfile, forecast]);

  const getCurrentPeriod = () => {
    const hour = currentTime.getHours();
    // Check if we have real rahu kalam data
    if (dashboardData.panchangam?.rahu_kalam) {
      const rahuStart = parseInt(dashboardData.panchangam.rahu_kalam.start?.split(':')[0] || '15');
      const rahuEnd = parseInt(dashboardData.panchangam.rahu_kalam.end?.split(':')[0] || '17');
      if (hour >= rahuStart && hour < rahuEnd) {
        return { status: 'rahu', label: 'ராகு காலம்', color: 'text-red-600', bg: 'bg-red-50', border: 'border-red-200' };
      }
    }

    // Check nalla neram
    if (dashboardData.panchangam?.nalla_neram?.length > 0) {
      for (const period of dashboardData.panchangam.nalla_neram) {
        const start = parseInt(period.start?.split(':')[0] || '9');
        const end = parseInt(period.end?.split(':')[0] || '11');
        if (hour >= start && hour < end) {
          return { status: 'good', label: 'நல்ல நேரம்', color: 'text-green-600', bg: 'bg-green-50', border: 'border-green-200' };
        }
      }
    }

    // Default fallback
    if (hour >= 15 && hour < 17) return { status: 'rahu', label: 'ராகு காலம்', color: 'text-red-600', bg: 'bg-red-50', border: 'border-red-200' };
    if (hour >= 9 && hour < 11) return { status: 'good', label: 'நல்ல நேரம்', color: 'text-green-600', bg: 'bg-green-50', border: 'border-green-200' };
    return { status: 'neutral', label: 'சாதாரண நேரம்', color: 'text-orange-600', bg: 'bg-orange-50', border: 'border-orange-200' };
  };

  const period = getCurrentPeriod();
  const currentHour = currentTime.getHours();

  // Get Tamil date info from API data
  const tamilDate = {
    month: dashboardData.panchangam?.tamil_month || 'மார்கழி',
    tithi: dashboardData.panchangam?.tithi?.name || 'சப்தமி',
    nakshatra: dashboardData.panchangam?.nakshatra?.tamil || dashboardData.userNakshatra || 'உத்திரம்',
    yoga: dashboardData.panchangam?.yoga?.name || 'சித்த யோகம்',
    vaaram: dashboardData.panchangam?.vaaram || getTamilDay(currentTime.getDay()),
  };

  // Get overall score
  const overallScore = dashboardData.overallScore || 65;

  // Generate AI insight based on data
  const generateInsight = () => {
    if (dashboardData.currentDasha) {
      const dashaLord = dashboardData.currentDasha.mahadasha;
      const antarLord = dashboardData.currentDasha.antardasha;
      return `${planetTamilNames[dashaLord] || dashaLord} மகா தசை மற்றும் ${planetTamilNames[antarLord] || antarLord} அந்தர தசை நடைபெறுகிறது. இது உங்கள் வாழ்க்கையில் முக்கிய மாற்றங்களைக் கொண்டுவரும்.`;
    }
    if (dashboardData.yogas?.length > 0) {
      const yoga = dashboardData.yogas[0];
      return `உங்கள் ஜாதகத்தில் ${yoga.name} யோகம் உள்ளது. ${yoga.effect || 'இது நல்ல பலன்களை தரும்.'}`;
    }
    return `குரு உங்கள் 9ம் வீட்டில் இருப்பதால் இன்று புதிய கற்றல் மற்றும் ஆன்மீக செயல்கள் சிறப்பாக அமையும்.`;
  };

  // Loading state
  if (dashboardData.isLoading && !dashboardData.panchangam) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-orange-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-orange-500 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">ஜாதக தரவுகளை ஏற்றுகிறது...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-orange-50 pb-24">
      {/* Decorative Top Border */}
      <div className="bg-gradient-to-r from-orange-500 via-red-500 to-orange-500 h-1" />

      {/* Header */}
      <div className="bg-white border-b border-orange-100 px-4 py-4">
        <div className="flex justify-between items-start">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-2xl text-orange-600">ॐ</span>
              <h1 className="text-xl font-bold text-orange-800">ஜோதிட AI</h1>
            </div>
            {userProfile && (
              <div className="mt-1">
                <p className="text-gray-600 text-sm">வணக்கம், {userProfile.name}</p>
                {dashboardData.userRasi && (
                  <p className="text-xs text-orange-600">
                    {dashboardData.userRasi} • {dashboardData.userNakshatra}
                  </p>
                )}
              </div>
            )}
          </div>
          <div className="text-right">
            <div className="text-lg font-mono text-gray-800">
              {currentTime.toLocaleTimeString('ta-IN', { hour: '2-digit', minute: '2-digit' })}
            </div>
            <div className={`text-xs px-2 py-1 rounded-full ${period.bg} ${period.color} ${period.border} border inline-block mt-1`}>
              {period.label}
            </div>
          </div>
        </div>
      </div>

      {/* Offline indicator */}
      {dashboardData.isOffline && (
        <div className="mx-4 mt-2 bg-yellow-50 border border-yellow-200 rounded-lg p-2 text-xs text-yellow-700 flex items-center gap-2">
          <RefreshCw className="w-3 h-3" />
          ஆஃப்லைன் பயன்முறை - உள்ளூர் கணக்கீடுகள்
        </div>
      )}

      {/* User Profile Banner */}
      {userProfile && (
        <div className="mx-4 mt-4">
          <UserProfileBanner
            userProfile={userProfile}
            onNavigateToProfile={() => navigate('/profile')}
          />
        </div>
      )}

      {/* Tamil Calendar Info */}
      <div className="mx-4 mt-4 bg-white rounded-2xl border border-orange-200 p-4 shadow-sm">
        <div className="flex items-center gap-2 mb-3">
          <Calendar className="w-4 h-4 text-orange-600" />
          <span className="text-sm font-medium text-gray-800">இன்றைய பஞ்சாங்கம்</span>
          <span className="text-xs text-gray-500 ml-auto">{tamilDate.vaaram}</span>
        </div>
        <div className="grid grid-cols-4 gap-2 text-center">
          <div className="bg-orange-50 rounded-lg p-2">
            <p className="text-xs text-gray-500">மாதம்</p>
            <p className="text-sm font-medium text-gray-800">{tamilDate.month}</p>
          </div>
          <div className="bg-orange-50 rounded-lg p-2">
            <p className="text-xs text-gray-500">திதி</p>
            <p className="text-sm font-medium text-gray-800">{tamilDate.tithi}</p>
          </div>
          <div className="bg-orange-50 rounded-lg p-2">
            <p className="text-xs text-gray-500">நட்சத்திரம்</p>
            <p className="text-sm font-medium text-gray-800">{tamilDate.nakshatra}</p>
          </div>
          <div className="bg-orange-50 rounded-lg p-2">
            <p className="text-xs text-gray-500">யோகம்</p>
            <p className="text-sm font-medium text-gray-800">{tamilDate.yoga}</p>
          </div>
        </div>
      </div>

      {/* Today's Score */}
      <div className="mx-4 mt-4 bg-white rounded-2xl border border-orange-200 p-4 shadow-sm">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-gray-500 text-sm">இன்றைய ஒட்டுமொத்த பலன்</p>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-4xl font-bold text-orange-600">{overallScore}</span>
              <span className="text-sm text-gray-500">/100</span>
              <span className={`flex items-center text-sm ${
                overallScore >= 70 ? 'text-green-600' : overallScore >= 50 ? 'text-orange-600' : 'text-red-600'
              }`}>
                <TrendingUp className="w-4 h-4 mr-1" />
                {overallScore >= 70 ? 'நல்லது' : overallScore >= 50 ? 'சாதாரணம்' : 'கவனம்'}
              </span>
            </div>
          </div>
          <div className="w-20 h-20">
            <ResponsiveContainer>
              <RadialBarChart cx="50%" cy="50%" innerRadius="70%" outerRadius="100%" data={[{ value: overallScore }]} startAngle={90} endAngle={-270}>
                <RadialBar dataKey="value" cornerRadius={10} fill="#ea580c" background={{ fill: '#fed7aa' }} />
              </RadialBarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* AI Insight */}
        <div className="mt-4 bg-gradient-to-r from-orange-50 to-yellow-50 rounded-xl p-3 border border-orange-200">
          <div className="flex items-start gap-2">
            <Sparkles className="w-4 h-4 text-orange-500 mt-0.5" />
            <p className="text-sm text-gray-700 leading-relaxed">
              {generateInsight()}
            </p>
          </div>
        </div>
      </div>

      {/* Forecast Section - Right after Today's Score for visibility */}
      {userProfile && (
        <div className="mx-4 mt-4 bg-white rounded-2xl border border-orange-200 p-4 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-medium text-gray-800 flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-orange-600" />
              எதிர்கால பலன்கள்
            </h3>
            {forecastLoading && <Loader2 className="w-4 h-4 animate-spin text-orange-500" />}
          </div>

          {/* Forecast Tabs */}
          <div className="flex gap-2 mb-4 overflow-x-auto pb-2">
            {[
              { key: 'week', label: 'வாரம்' },
              { key: 'month', label: 'மாதம்' },
              { key: 'year', label: 'வருடம்' },
              { key: '3year', label: '3 வருடம்' }
            ].map(tab => (
              <button
                key={tab.key}
                onClick={() => setExpandedForecast(tab.key)}
                className={`px-4 py-2 rounded-full text-sm whitespace-nowrap transition-all ${
                  expandedForecast === tab.key
                    ? 'bg-orange-500 text-white'
                    : 'bg-orange-50 text-orange-700 border border-orange-200'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Weekly Forecast */}
          {expandedForecast === 'week' && forecast?.week && (
            <div>
              <div className="flex items-center justify-between mb-3 p-3 bg-orange-50 rounded-xl">
                <div>
                  <p className="text-xs text-gray-500">வார சராசரி</p>
                  <p className="text-2xl font-bold text-orange-600">{forecast.week.average_score}%</p>
                </div>
                <div className="text-right">
                  <p className="text-xs text-green-600">சிறந்த நாள்: {forecast.week.best_day?.day}</p>
                  <p className="text-xs text-red-600">கவனம்: {forecast.week.worst_day?.day}</p>
                </div>
              </div>
              <div className="flex gap-2 overflow-x-auto pb-2">
                {forecast.week.days?.map((day, i) => (
                  <div
                    key={i}
                    className={`flex-shrink-0 w-16 p-2 rounded-xl text-center border ${
                      day.is_good ? 'bg-green-50 border-green-200' : 'bg-gray-50 border-gray-200'
                    }`}
                  >
                    <p className="text-xs text-gray-500">{day.day}</p>
                    <p className={`text-lg font-bold ${day.is_good ? 'text-green-600' : 'text-gray-600'}`}>
                      {day.score}%
                    </p>
                  </div>
                ))}
              </div>
              {forecast.week.advice && (
                <p className="text-xs text-gray-600 mt-3 p-2 bg-gray-50 rounded-lg">{forecast.week.advice}</p>
              )}
            </div>
          )}

          {/* Monthly Forecast */}
          {expandedForecast === 'month' && forecast?.month && (
            <div>
              <div className="flex items-center justify-between mb-3 p-3 bg-orange-50 rounded-xl">
                <div>
                  <p className="text-xs text-gray-500">{forecast.month.month_name} மாதம்</p>
                  <p className="text-2xl font-bold text-orange-600">{forecast.month.average_score}%</p>
                </div>
                <div className="text-right">
                  <p className="text-xs text-green-600">நல்ல நாட்கள்: {forecast.month.good_days_count}</p>
                  <p className="text-xs text-red-600">கவனம்: {forecast.month.caution_days_count}</p>
                </div>
              </div>
              {/* Monthly calendar grid */}
              <div className="grid grid-cols-7 gap-1 text-center">
                {['ஞா', 'தி', 'செ', 'பு', 'வி', 'வெ', 'ச'].map(d => (
                  <div key={d} className="text-xs text-gray-500 py-1">{d}</div>
                ))}
                {/* Add empty cells for proper alignment */}
                {(() => {
                  const firstDay = new Date(forecast.month.year, forecast.month.month - 1, 1).getDay();
                  return Array(firstDay).fill(null).map((_, i) => (
                    <div key={`empty-${i}`} className="p-1"></div>
                  ));
                })()}
                {forecast.month.days?.map((day, i) => (
                  <div
                    key={i}
                    className={`p-1 rounded text-xs font-medium ${
                      day.type === 'good' ? 'bg-green-100 text-green-700 border border-green-200' :
                      day.type === 'caution' ? 'bg-red-100 text-red-700 border border-red-200' :
                      'bg-gray-50 text-gray-600 border border-gray-100'
                    }`}
                    title={`${day.day}: ${day.score}%`}
                  >
                    {day.day}
                  </div>
                ))}
              </div>
              {forecast.month.advice && (
                <p className="text-xs text-gray-600 mt-3 p-2 bg-gray-50 rounded-lg">{forecast.month.advice}</p>
              )}
            </div>
          )}

          {/* Yearly Forecast */}
          {expandedForecast === 'year' && forecast?.year && (
            <div>
              <div className="flex items-center justify-between mb-3 p-3 bg-orange-50 rounded-xl">
                <div>
                  <p className="text-xs text-gray-500">{forecast.year.year} வருடம்</p>
                  <p className="text-2xl font-bold text-orange-600">{forecast.year.average_score}%</p>
                </div>
                <div className="text-right text-xs">
                  <p className="text-green-600">சிறந்த: {forecast.year.best_months?.map(m => m.month).join(', ')}</p>
                </div>
              </div>
              <div className="grid grid-cols-4 gap-2">
                {forecast.year.months?.map((month, i) => (
                  <div
                    key={i}
                    className={`p-2 rounded-lg text-center border ${
                      month.type === 'excellent' ? 'bg-green-50 border-green-200' :
                      month.type === 'good' ? 'bg-orange-50 border-orange-200' :
                      'bg-gray-50 border-gray-200'
                    }`}
                  >
                    <p className="text-xs text-gray-500">{month.name}</p>
                    <p className={`text-sm font-bold ${
                      month.type === 'excellent' ? 'text-green-600' :
                      month.type === 'good' ? 'text-orange-600' :
                      'text-gray-600'
                    }`}>
                      {month.score}%
                    </p>
                  </div>
                ))}
              </div>
              {forecast.year.advice && (
                <p className="text-xs text-gray-600 mt-3 p-2 bg-gray-50 rounded-lg">{forecast.year.advice}</p>
              )}
            </div>
          )}

          {/* 3-Year Forecast */}
          {expandedForecast === '3year' && forecast?.three_years && (
            <div className="space-y-4">
              {forecast.three_years.map((yearData, yi) => (
                <div key={yi} className="border border-orange-100 rounded-xl p-3">
                  <p className="text-sm font-medium text-orange-700 mb-2">{yearData.year}</p>
                  <div className="flex gap-1 overflow-x-auto pb-1">
                    {yearData.months?.map((month, mi) => (
                      <div
                        key={mi}
                        className={`flex-shrink-0 w-12 p-1 rounded text-center ${
                          month.type === 'excellent' ? 'bg-green-100' :
                          month.type === 'good' ? 'bg-orange-100' :
                          month.type === 'caution' ? 'bg-red-100' :
                          'bg-gray-100'
                        }`}
                      >
                        <p className="text-[10px] text-gray-500">{month.name?.substring(0, 3)}</p>
                        <p className={`text-xs font-bold ${
                          month.type === 'excellent' ? 'text-green-700' :
                          month.type === 'good' ? 'text-orange-700' :
                          month.type === 'caution' ? 'text-red-700' :
                          'text-gray-600'
                        }`}>
                          {month.score}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* No forecast yet - show loading or placeholder */}
          {!forecast && (
            <div className="text-center py-6 text-gray-500">
              {(forecastLoading || dashboardData?.isJathagamLoading) ? (
                <>
                  <Loader2 className="w-8 h-8 mx-auto mb-2 animate-spin text-orange-400" />
                  <p className="text-sm">பலன்களை ஏற்றுகிறது...</p>
                </>
              ) : (
                <>
                  <Calendar className="w-8 h-8 mx-auto mb-2 opacity-50" />
                  <p className="text-sm">பலன் தரவு இல்லை</p>
                </>
              )}
            </div>
          )}
        </div>
      )}

      {/* Score Breakdown - Expandable */}
      <div className="mx-4 mt-4">
        <ScoreBreakdown />
      </div>

      {/* Time Chart */}
      <div className="mx-4 mt-4 bg-white rounded-2xl border border-orange-200 p-4 shadow-sm">
        <div className="flex justify-between items-center mb-3">
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4 text-orange-600" />
            <span className="text-sm font-medium text-gray-800">இன்றைய நேர பலன்</span>
          </div>
          <div className="flex gap-3 text-xs">
            <span className="flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-green-500"></span>
              நல்ல நேரம்
            </span>
            <span className="flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-red-500"></span>
              ராகு காலம்
            </span>
          </div>
        </div>

        {/* Time Blocks from API data */}
        <div className="flex gap-1 overflow-x-auto pb-2">
          {dashboardData.timeEnergy.map((t, i) => (
            <div
              key={i}
              className={`flex-shrink-0 w-10 h-12 rounded-lg flex flex-col items-center justify-center text-xs transition-all
                ${t.hour === currentHour ? 'ring-2 ring-orange-500 ring-offset-1' : ''}
                ${t.is_rahu_kalam ? 'bg-red-100 text-red-700 border border-red-200' :
                  t.is_nalla_neram ? 'bg-green-100 text-green-700 border border-green-200' :
                  'bg-gray-100 text-gray-600 border border-gray-200'}`}
            >
              <span className="font-medium">{t.hour}</span>
              <span className="text-[10px]">{t.is_nalla_neram ? '✓' : t.is_rahu_kalam ? '✗' : '•'}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Life Areas Grid */}
      <div className="mx-4 mt-4">
        <h3 className="text-sm font-medium text-gray-800 mb-3 flex items-center gap-2">
          <Star className="w-4 h-4 text-orange-600" />
          வாழ்க்கை துறைகள்
        </h3>
        <div className="grid grid-cols-2 gap-3">
          {dashboardData.lifeAreas.map((area, i) => {
            const IconComponent = iconMap[area.icon] || Heart;
            return (
              <div key={i} className="bg-white rounded-xl p-4 border border-orange-200 shadow-sm">
                <div className="flex items-center justify-between mb-2">
                  <IconComponent className="w-5 h-5" style={{ color: area.color }} />
                  <span className={`text-xs px-2 py-0.5 rounded-full ${
                    area.score > 75 ? 'bg-green-100 text-green-700' : 'bg-orange-100 text-orange-700'
                  }`}>
                    {area.score > 75 ? 'நல்லது' : 'சாதாரணம்'}
                  </span>
                </div>
                <p className="text-gray-700 text-sm font-medium">{area.name}</p>
                <div className="flex items-end gap-2 mt-1">
                  <span className="text-2xl font-bold" style={{ color: area.color }}>{area.score}</span>
                  <span className="text-gray-400 text-sm mb-1">/100</span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-1.5 mt-2">
                  <div
                    className="h-1.5 rounded-full transition-all duration-500"
                    style={{ width: `${area.score}%`, backgroundColor: area.color }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Planet Positions from Jathagam */}
      {dashboardData.planets.length > 0 && (
        <div className="mx-4 mt-4 bg-white rounded-2xl border border-orange-200 p-4 shadow-sm">
          <h3 className="text-sm font-medium text-gray-800 mb-3 flex items-center gap-2">
            <Sun className="w-4 h-4 text-orange-600" />
            கிரக நிலை
            {dashboardData.isJathagamLoading && (
              <Loader2 className="w-3 h-3 animate-spin text-orange-400 ml-2" />
            )}
          </h3>
          <div className="space-y-3">
            {dashboardData.planets.slice(0, 7).map((planet, i) => {
              const symbol = planetSymbols[planet.planet] || '★';
              const tamilName = planetTamilNames[planet.planet] || planet.planet;
              const rasiTamil = rasiTamilNames[planet.rasi] || planet.rasi;
              const strength = planet.strength || 50;
              const status = strength >= 70 ? 'மிக நல்லது' : strength >= 50 ? 'நல்லது' : 'கவனம்';

              return (
                <div key={i} className="flex items-center justify-between py-2 border-b border-orange-100 last:border-0">
                  <div className="flex items-center gap-3">
                    <span className="text-xl w-8 text-center">{symbol}</span>
                    <div>
                      <p className="text-sm font-medium text-gray-800">{tamilName}</p>
                      <p className="text-xs text-gray-500">
                        {rasiTamil} - {planet.degree?.toFixed(1) || '0'}°
                        {planet.retrograde && <span className="text-red-500 ml-1">(வக்ர)</span>}
                      </p>
                    </div>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded-full ${
                    status === 'மிக நல்லது' ? 'bg-green-100 text-green-700' :
                    status === 'நல்லது' ? 'bg-orange-100 text-orange-700' :
                    'bg-red-100 text-red-700'
                  }`}>
                    {status}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Current Dasha */}
      {dashboardData.currentDasha && (
        <div className="mx-4 mt-4 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-2xl border border-purple-200 p-4 shadow-sm">
          <h3 className="text-sm font-medium text-purple-800 mb-3 flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-purple-600" />
            நடப்பு தசா
          </h3>
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-white/50 rounded-lg p-3">
              <p className="text-xs text-gray-500">மகா தசை</p>
              <p className="text-sm font-semibold text-purple-700">
                {planetTamilNames[dashboardData.currentDasha.mahadasha] || dashboardData.currentDasha.mahadasha}
              </p>
            </div>
            <div className="bg-white/50 rounded-lg p-3">
              <p className="text-xs text-gray-500">அந்தர தசை</p>
              <p className="text-sm font-semibold text-purple-700">
                {planetTamilNames[dashboardData.currentDasha.antardasha] || dashboardData.currentDasha.antardasha}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="mx-4 mt-4 mb-4">
        <h3 className="text-sm font-medium text-gray-800 mb-3">விரைவு செயல்கள்</h3>
        <div className="grid grid-cols-3 gap-3">
          {[
            { icon: MessageCircle, label: 'AI கேள்வி', path: '/chat', color: 'text-orange-600' },
            { icon: Users, label: 'பொருத்தம்', path: '/matching', color: 'text-red-600' },
            { icon: Calendar, label: 'முகூர்த்தம்', path: '/muhurtham', color: 'text-green-600' },
          ].map((action, i) => (
            <button
              key={i}
              onClick={() => navigate(action.path)}
              className="bg-white rounded-xl p-4 border border-orange-200 shadow-sm hover:border-orange-400 transition-all"
            >
              <action.icon className={`w-6 h-6 mx-auto ${action.color}`} />
              <span className="text-xs text-gray-600 mt-2 block">{action.label}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

// Helper function for Tamil day
function getTamilDay(dayIndex) {
  const days = ['ஞாயிறு', 'திங்கள்', 'செவ்வாய்', 'புதன்', 'வியாழன்', 'வெள்ளி', 'சனி'];
  return days[dayIndex];
}
