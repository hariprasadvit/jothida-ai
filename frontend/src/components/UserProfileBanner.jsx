import { useState, useEffect } from 'react';
import { Moon, Star, Sparkles, Loader2, ChevronRight } from 'lucide-react';
import { userAPI } from '../services/api';

export default function UserProfileBanner({ userProfile, onNavigateToProfile }) {
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      if (!userProfile) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const data = await userAPI.getProfileSummary(userProfile);
        setProfileData(data);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch profile summary:', err);
        setError('தரவு ஏற்ற முடியவில்லை');
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [userProfile]);

  if (!userProfile) {
    return null;
  }

  if (loading) {
    return (
      <div className="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-2xl border border-purple-200 p-4 shadow-sm">
        <div className="flex items-center justify-center gap-2 py-2">
          <Loader2 className="w-4 h-4 text-purple-500 animate-spin" />
          <span className="text-purple-600 text-sm">சுருக்கம் ஏற்றுகிறது...</span>
        </div>
      </div>
    );
  }

  if (error || !profileData) {
    return null;
  }

  const { moon_rasi, nakshatra, current_dasha } = profileData;

  return (
    <button
      onClick={onNavigateToProfile}
      className="w-full bg-gradient-to-r from-purple-50 via-indigo-50 to-purple-50 rounded-2xl border border-purple-200 p-4 shadow-sm hover:border-purple-300 transition-all text-left"
    >
      {/* Main Profile Line */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3 flex-wrap">
          {/* Moon Rasi */}
          <div className="flex items-center gap-1.5">
            <Moon className="w-4 h-4 text-purple-600" />
            <span className="text-sm font-semibold text-purple-800">
              {moon_rasi.tamil}
            </span>
          </div>

          <span className="text-purple-300">|</span>

          {/* Nakshatra with Pada */}
          <div className="flex items-center gap-1.5">
            <Star className="w-4 h-4 text-indigo-500" />
            <span className="text-sm text-indigo-700">
              {nakshatra.tamil}
              <span className="text-xs text-indigo-500 ml-1">
                {nakshatra.pada}ம் பாதம்
              </span>
            </span>
          </div>

          <span className="text-purple-300">|</span>

          {/* Current Dasha */}
          <div className="flex items-center gap-1.5">
            <Sparkles className="w-4 h-4 text-orange-500" />
            <span className="text-sm text-gray-700">
              <span className="font-medium text-orange-700">
                {current_dasha.mahadasha_tamil}
              </span>
              <span className="text-gray-500 mx-1">தசை</span>
              <span className="text-xs text-gray-500">
                / {current_dasha.antardasha_tamil} புக்தி
              </span>
            </span>
          </div>
        </div>

        <ChevronRight className="w-4 h-4 text-purple-400 flex-shrink-0" />
      </div>

      {/* Dasha Details Row */}
      <div className="mt-3 pt-3 border-t border-purple-100 flex flex-wrap gap-4 text-xs">
        <div className="flex items-center gap-2">
          <span className="text-gray-500">மகா தசை முடிவு:</span>
          <span className="text-purple-700 font-medium">
            {new Date(current_dasha.mahadasha_end).toLocaleDateString('ta-IN')}
          </span>
          <span className="text-gray-400">
            ({current_dasha.mahadasha_remaining_years} ஆண்டுகள்)
          </span>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-gray-500">அந்தர தசை முடிவு:</span>
          <span className="text-indigo-700 font-medium">
            {new Date(current_dasha.antardasha_end).toLocaleDateString('ta-IN')}
          </span>
          <span className="text-gray-400">
            ({current_dasha.antardasha_remaining_months} மாதங்கள்)
          </span>
        </div>
      </div>
    </button>
  );
}
