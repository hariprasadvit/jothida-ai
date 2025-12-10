import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, Calendar, MapPin, Clock, ChevronRight, Edit3, LogOut, Sun, Moon, Loader2, Download, FileText } from 'lucide-react';
import { jathagamAPI, reportAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

const rasiSymbols = {
  'மேஷம்': '♈', 'ரிஷபம்': '♉', 'மிதுனம்': '♊', 'கடகம்': '♋',
  'சிம்மம்': '♌', 'கன்னி': '♍', 'துலாம்': '♎', 'விருச்சிகம்': '♏',
  'தனுசு': '♐', 'மகரம்': '♑', 'கும்பம்': '♒', 'மீனம்': '♓'
};

// Planet abbreviations
const PLANET_ABBR = {
  'Sun': 'சூ',
  'Moon': 'ச',
  'Mars': 'செ',
  'Mercury': 'பு',
  'Jupiter': 'கு',
  'Venus': 'சு',
  'Saturn': 'ச',
  'Rahu': 'ரா',
  'Ketu': 'கே'
};

// Compact South Indian Birth Chart Component
function SouthIndianChart({ planets, lagna }) {
  // Initialize 12 houses with planet lists
  const houses = {};
  const rasiToHouse = {
    'Pisces': 0, 'Aries': 1, 'Taurus': 2, 'Gemini': 3,
    'Aquarius': 4, 'Cancer': 5, 'Capricorn': 6, 'Leo': 7,
    'Sagittarius': 8, 'Scorpio': 9, 'Libra': 10, 'Virgo': 11
  };

  // Place planets in houses
  if (planets) {
    planets.forEach(planet => {
      const houseIdx = rasiToHouse[planet.rasi];
      if (houseIdx !== undefined) {
        if (!houses[houseIdx]) houses[houseIdx] = [];
        houses[houseIdx].push({
          abbr: PLANET_ABBR[planet.planet] || planet.planet.substring(0, 2),
          retrograde: planet.is_retrograde
        });
      }
    });
  }

  const rasiNames = ['மீனம்', 'மேஷம்', 'ரிஷபம்', 'மிதுனம்', 'கும்பம்', 'கடகம்', 'மகரம்', 'சிம்மம்', 'தனுசு', 'விருச்சிகம்', 'துலாம்', 'கன்னி'];

  // Render a house cell
  const HouseCell = ({ index, className = '' }) => {
    const planetList = houses[index] || [];
    const rasiName = rasiNames[index];
    const isLagna = lagna && rasiName === lagna;

    return (
      <div className={`border border-orange-300 bg-white p-1 relative ${isLagna ? 'bg-orange-50' : ''} ${className}`}>
        <span className="text-[7px] text-gray-400 leading-none">{rasiName}</span>
        {isLagna && <span className="text-[7px] text-orange-600 font-bold absolute top-0.5 right-1">L</span>}
        <div className="flex flex-wrap gap-0.5 mt-0.5 min-h-[16px]">
          {planetList.map((p, i) => (
            <span key={i} className={`text-[9px] font-semibold ${p.retrograde ? 'text-red-600' : 'text-gray-700'}`}>
              {p.abbr}
            </span>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="w-full max-w-[280px] mx-auto">
      {/* 4x4 Grid - South Indian Style */}
      <div className="grid grid-cols-4 border-2 border-orange-400 rounded-lg overflow-hidden bg-orange-100">
        {/* Row 1 */}
        <HouseCell index={0} />
        <HouseCell index={1} />
        <HouseCell index={2} />
        <HouseCell index={3} />

        {/* Row 2 */}
        <HouseCell index={4} />
        <div className="col-span-2 row-span-2 border border-orange-300 bg-gradient-to-br from-orange-50 to-amber-50 flex flex-col items-center justify-center">
          <span className="text-orange-600 font-bold text-sm">ராசி</span>
          <span className="text-orange-500 text-xs">சக்கரம்</span>
        </div>
        <HouseCell index={5} />

        {/* Row 3 */}
        <HouseCell index={6} />
        <HouseCell index={7} />

        {/* Row 4 */}
        <HouseCell index={8} />
        <HouseCell index={9} />
        <HouseCell index={10} />
        <HouseCell index={11} />
      </div>
    </div>
  );
}

// Planet Details Table Component
function PlanetTable({ planets }) {
  if (!planets || planets.length === 0) return null;

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-xs">
        <thead>
          <tr className="bg-orange-50 text-orange-800">
            <th className="p-2 text-left">கிரகம்</th>
            <th className="p-2 text-left">ராசி</th>
            <th className="p-2 text-left">நட்சத்திரம்</th>
            <th className="p-2 text-center">பாதம்</th>
          </tr>
        </thead>
        <tbody>
          {planets.map((planet, i) => (
            <tr key={i} className="border-b border-orange-100">
              <td className="p-2">
                <div className="flex items-center gap-1">
                  <span>{planet.symbol}</span>
                  <span className={planet.is_retrograde ? 'text-red-600' : ''}>
                    {planet.tamil_name}
                    {planet.is_retrograde && ' (வ)'}
                  </span>
                </div>
              </td>
              <td className="p-2">{planet.rasi_tamil}</td>
              <td className="p-2">{planet.nakshatra}</td>
              <td className="p-2 text-center">{planet.nakshatra_pada}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function Profile() {
  const navigate = useNavigate();
  const { user, isAuthenticated, logout, getUserProfile } = useAuth();
  const [userProfile, setUserProfile] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('chart'); // 'chart' or 'planets'
  const [downloadingReport, setDownloadingReport] = useState(false);

  useEffect(() => {
    // Try to get profile from auth context first, then localStorage
    const authProfile = getUserProfile();
    if (authProfile) {
      setUserProfile(authProfile);
    } else {
      const profile = localStorage.getItem('userProfile');
      if (profile) {
        setUserProfile(JSON.parse(profile));
      }
    }
  }, [getUserProfile, user]);

  // Fetch chart data when profile is available
  useEffect(() => {
    const fetchChartData = async () => {
      if (!userProfile?.birthDate || !userProfile?.birthTime || !userProfile?.birthPlace) {
        return;
      }

      setLoading(true);
      try {
        const data = await jathagamAPI.generate({
          name: userProfile.name,
          birthDate: userProfile.birthDate,
          birthTime: userProfile.birthTime,
          birthPlace: userProfile.birthPlace
        });
        setChartData(data);
      } catch (err) {
        console.error('Failed to fetch chart data:', err);
      } finally {
        setLoading(false);
      }
    };

    if (userProfile) {
      fetchChartData();
    }
  }, [userProfile]);

  const handleLogout = async () => {
    await logout(); // This clears auth token and localStorage
    navigate('/onboarding');
  };

  const handleEditProfile = () => {
    localStorage.removeItem('onboardingComplete');
    navigate('/onboarding');
  };

  const handleDownloadReport = async () => {
    if (!userProfile?.birthDate || !userProfile?.birthTime || !userProfile?.birthPlace) {
      alert('பிறப்பு விவரங்களை முழுமையாக நிரப்பவும் (Please complete birth details)');
      return;
    }

    setDownloadingReport(true);
    try {
      await reportAPI.generateReport({
        name: userProfile.name || user?.name || 'User',
        birthDate: userProfile.birthDate,
        birthTime: userProfile.birthTime,
        birthPlace: userProfile.birthPlace,
        latitude: userProfile.latitude,
        longitude: userProfile.longitude
      });
    } catch (err) {
      console.error('Failed to download report:', err);
      alert('அறிக்கை பதிவிறக்கம் தோல்வியடைந்தது (Report download failed)');
    } finally {
      setDownloadingReport(false);
    }
  };

  if (!userProfile) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-orange-50 pb-24">
        {/* Decorative Header */}
        <div className="bg-gradient-to-r from-orange-500 via-red-500 to-orange-500 h-1" />

        {/* Header */}
        <div className="bg-white border-b border-orange-100 px-4 py-4">
          <h1 className="text-xl font-bold text-orange-800">சுயவிவரம்</h1>
          <p className="text-gray-500 text-sm">உங்கள் ஜாதக விவரங்கள்</p>
        </div>

        <div className="mx-4 mt-4 bg-white rounded-2xl border border-orange-200 p-6 text-center shadow-sm">
          <div className="w-20 h-20 rounded-full bg-orange-100 flex items-center justify-center mx-auto mb-4">
            <User className="w-10 h-10 text-orange-400" />
          </div>
          <h2 className="text-xl font-semibold text-gray-800 mb-2">ஜாதகம் சேர்க்கவும்</h2>
          <p className="text-gray-500 text-sm mb-6">
            உங்கள் பிறந்த தேதி, நேரம், இடம் சேர்த்து தனிப்பயனாக்கப்பட்ட
            கணிப்புகளைப் பெறுங்கள்
          </p>

          <button
            onClick={() => navigate('/onboarding')}
            className="bg-gradient-to-r from-orange-500 to-red-500 text-white px-6 py-3 rounded-xl font-medium shadow-lg shadow-orange-500/20"
          >
            + பிறப்பு விவரங்களை சேர்க்கவும்
          </button>
        </div>

        {/* Settings */}
        <div className="mx-4 mt-4 bg-white rounded-2xl border border-orange-200 overflow-hidden shadow-sm">
          <h3 className="p-4 text-sm font-medium text-gray-800 border-b border-orange-100">அமைப்புகள்</h3>
          {[
            { icon: '🌐', label: 'மொழி', value: 'தமிழ்' },
            { icon: '📍', label: 'இடம்', value: 'சென்னை' },
            { icon: '🔔', label: 'அறிவிப்புகள்', value: 'On' },
          ].map((item, i) => (
            <button
              key={i}
              className="w-full p-4 flex items-center justify-between border-b border-orange-50 last:border-0 hover:bg-orange-50"
            >
              <div className="flex items-center gap-3">
                <span className="text-xl">{item.icon}</span>
                <span className="text-gray-700">{item.label}</span>
              </div>
              <div className="flex items-center gap-2 text-gray-400">
                <span className="text-sm">{item.value}</span>
                <ChevronRight className="w-4 h-4" />
              </div>
            </button>
          ))}
        </div>
      </div>
    );
  }

  // Profile with data
  const rasiSymbol = userProfile.rasi ? rasiSymbols[userProfile.rasi] : '☉';

  // Find Moon's rasi from chart data for lagna
  const moonPlanet = chartData?.planets?.find(p => p.planet === 'Moon');
  const lagnaRasi = moonPlanet?.rasi_tamil;

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-orange-50 pb-24">
      {/* Decorative Header */}
      <div className="bg-gradient-to-r from-orange-500 via-red-500 to-orange-500 h-1" />

      {/* Header */}
      <div className="bg-white border-b border-orange-100 px-4 py-4 flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold text-orange-800">சுயவிவரம்</h1>
          <p className="text-gray-500 text-sm">உங்கள் ஜாதக விவரங்கள்</p>
        </div>
        <button
          onClick={handleEditProfile}
          className="p-2 bg-orange-50 rounded-lg border border-orange-200 hover:bg-orange-100"
        >
          <Edit3 className="w-5 h-5 text-orange-600" />
        </button>
      </div>

      {/* User Info Card */}
      <div className="mx-4 mt-4 bg-white rounded-2xl border border-orange-200 p-4 shadow-sm">
        <div className="flex items-center gap-4">
          {/* Profile picture - from Google or fallback */}
          {isAuthenticated && user?.picture ? (
            <img
              src={user.picture}
              alt={user.name}
              className="w-16 h-16 rounded-full border-2 border-orange-200 shadow-lg"
            />
          ) : (
            <div className="w-16 h-16 rounded-full bg-gradient-to-r from-orange-400 to-red-400 flex items-center justify-center text-2xl font-bold text-white shadow-lg">
              {userProfile.name?.charAt(0) || 'அ'}
            </div>
          )}
          <div className="flex-1">
            <h2 className="text-xl font-semibold text-gray-800">{userProfile.name || user?.name || 'பெயர் இல்லை'}</h2>
            {isAuthenticated && user?.email && (
              <p className="text-xs text-gray-500">{user.email}</p>
            )}
            <div className="flex items-center gap-2 mt-1">
              {userProfile.rasi && (
                <span className="text-sm text-orange-600 bg-orange-50 px-2 py-0.5 rounded-full border border-orange-200">
                  {rasiSymbol} {userProfile.rasi}
                </span>
              )}
              {userProfile.nakshatra && (
                <span className="text-sm text-gray-500">• {userProfile.nakshatra}</span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Birth Details */}
      <div className="mx-4 mt-4 bg-white rounded-2xl border border-orange-200 p-4 shadow-sm">
        <h3 className="text-sm font-medium text-gray-800 mb-4 flex items-center gap-2">
          <Sun className="w-4 h-4 text-orange-500" />
          பிறப்பு விவரங்கள்
        </h3>
        <div className="grid grid-cols-2 gap-4">
          <div className="flex items-center gap-3 p-3 bg-orange-50 rounded-xl">
            <Calendar className="w-5 h-5 text-orange-500" />
            <div>
              <p className="text-xs text-gray-500">பிறந்த தேதி</p>
              <p className="text-sm font-medium text-gray-800">
                {userProfile.birthDate || '-'}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3 p-3 bg-orange-50 rounded-xl">
            <Clock className="w-5 h-5 text-orange-500" />
            <div>
              <p className="text-xs text-gray-500">பிறந்த நேரம்</p>
              <p className="text-sm font-medium text-gray-800">
                {userProfile.birthTime || '-'}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3 p-3 bg-orange-50 rounded-xl col-span-2">
            <MapPin className="w-5 h-5 text-orange-500" />
            <div>
              <p className="text-xs text-gray-500">பிறந்த இடம்</p>
              <p className="text-sm font-medium text-gray-800">
                {userProfile.birthPlace || '-'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Birth Chart Section */}
      <div className="mx-4 mt-4 bg-white rounded-2xl border border-orange-200 p-4 shadow-sm">
        {/* Tab Switcher */}
        <div className="flex gap-2 mb-4">
          <button
            onClick={() => setActiveTab('chart')}
            className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all ${
              activeTab === 'chart'
                ? 'bg-orange-500 text-white'
                : 'bg-orange-50 text-orange-700 hover:bg-orange-100'
            }`}
          >
            ராசி சக்கரம்
          </button>
          <button
            onClick={() => setActiveTab('planets')}
            className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all ${
              activeTab === 'planets'
                ? 'bg-orange-500 text-white'
                : 'bg-orange-50 text-orange-700 hover:bg-orange-100'
            }`}
          >
            கிரக நிலை
          </button>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="w-8 h-8 text-orange-500 animate-spin" />
          </div>
        ) : chartData?.planets ? (
          <>
            {activeTab === 'chart' ? (
              <div>
                <SouthIndianChart planets={chartData.planets} lagna={lagnaRasi} />
                <div className="mt-2 flex flex-wrap justify-center gap-x-3 gap-y-0.5 text-[9px] text-gray-500">
                  <span>சூ-சூரியன்</span>
                  <span>ச-சந்திரன்</span>
                  <span>செ-செவ்வாய்</span>
                  <span>பு-புதன்</span>
                  <span>கு-குரு</span>
                  <span>சு-சுக்கிரன்</span>
                  <span>ச-சனி</span>
                  <span>ரா-ராகு</span>
                  <span>கே-கேது</span>
                  <span className="text-red-500">சிவப்பு=வக்கிரம்</span>
                </div>
              </div>
            ) : (
              <PlanetTable planets={chartData.planets} />
            )}
          </>
        ) : (
          <div className="aspect-square bg-gradient-to-br from-orange-50 to-yellow-50 rounded-xl border border-orange-200 flex items-center justify-center">
            <div className="text-center">
              <div className="text-6xl mb-2">{rasiSymbol}</div>
              <p className="text-gray-600">{userProfile.rasi || 'ராசி'}</p>
              <p className="text-sm text-gray-400 mt-2">பிறப்பு விவரங்களை முழுமையாக நிரப்பவும்</p>
            </div>
          </div>
        )}
      </div>

      {/* Dasha Info (if available) */}
      {chartData?.dasha && (
        <div className="mx-4 mt-4 bg-white rounded-2xl border border-orange-200 p-4 shadow-sm">
          <h3 className="text-sm font-medium text-gray-800 mb-3 flex items-center gap-2">
            <Moon className="w-4 h-4 text-purple-500" />
            தசா புக்தி
          </h3>
          <div className="space-y-2">
            <div className="flex justify-between items-center p-3 bg-purple-50 rounded-xl">
              <span className="text-sm text-gray-600">மகா தசா</span>
              <span className="font-medium text-purple-700">{chartData.dasha.mahadasha_tamil || chartData.dasha.mahadasha}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-purple-50 rounded-xl">
              <span className="text-sm text-gray-600">அந்தர தசா</span>
              <span className="font-medium text-purple-700">{chartData.dasha.antardasha_tamil || chartData.dasha.antardasha}</span>
            </div>
          </div>
        </div>
      )}

      {/* Download Report Section */}
      <div className="mx-4 mt-4 bg-gradient-to-r from-orange-500 to-red-500 rounded-2xl p-4 shadow-lg">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
            <FileText className="w-6 h-6 text-white" />
          </div>
          <div className="flex-1">
            <h3 className="text-white font-semibold text-lg">முழு ஜாதக அறிக்கை</h3>
            <p className="text-white/80 text-sm mt-1">
              60+ பக்க விரிவான PDF அறிக்கை - ராசி, நவாம்சம், தசா புக்தி, யோகங்கள், தோஷங்கள், பரிகாரங்கள் மற்றும் பல
            </p>
            <div className="flex flex-wrap gap-2 mt-3">
              <span className="text-xs bg-white/20 text-white px-2 py-1 rounded-full">ராசி சக்கரம்</span>
              <span className="text-xs bg-white/20 text-white px-2 py-1 rounded-full">நவாம்சம்</span>
              <span className="text-xs bg-white/20 text-white px-2 py-1 rounded-full">தசா புக்தி</span>
              <span className="text-xs bg-white/20 text-white px-2 py-1 rounded-full">பரிகாரங்கள்</span>
            </div>
          </div>
        </div>
        <button
          onClick={handleDownloadReport}
          disabled={downloadingReport || !userProfile?.birthDate}
          className="w-full mt-4 bg-white text-orange-600 font-semibold py-3 rounded-xl flex items-center justify-center gap-2 hover:bg-orange-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {downloadingReport ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              அறிக்கை உருவாக்கப்படுகிறது...
            </>
          ) : (
            <>
              <Download className="w-5 h-5" />
              PDF அறிக்கை பதிவிறக்கம்
            </>
          )}
        </button>
      </div>

      {/* Settings */}
      <div className="mx-4 mt-4 bg-white rounded-2xl border border-orange-200 overflow-hidden shadow-sm">
        <h3 className="p-4 text-sm font-medium text-gray-800 border-b border-orange-100">அமைப்புகள்</h3>
        {[
          { icon: '🌐', label: 'மொழி', value: 'தமிழ்' },
          { icon: '📍', label: 'இடம்', value: userProfile.birthPlace || 'சென்னை' },
          { icon: '🔔', label: 'அறிவிப்புகள்', value: 'On' },
        ].map((item, i) => (
          <button
            key={i}
            className="w-full p-4 flex items-center justify-between border-b border-orange-50 last:border-0 hover:bg-orange-50"
          >
            <div className="flex items-center gap-3">
              <span className="text-xl">{item.icon}</span>
              <span className="text-gray-700">{item.label}</span>
            </div>
            <div className="flex items-center gap-2 text-gray-400">
              <span className="text-sm">{item.value}</span>
              <ChevronRight className="w-4 h-4" />
            </div>
          </button>
        ))}
      </div>

      {/* Logout Button */}
      <div className="mx-4 mt-4">
        <button
          onClick={handleLogout}
          className="w-full p-4 bg-red-50 border border-red-200 rounded-xl text-red-600 font-medium flex items-center justify-center gap-2 hover:bg-red-100"
        >
          <LogOut className="w-5 h-5" />
          வெளியேறு
        </button>
      </div>
    </div>
  );
}
