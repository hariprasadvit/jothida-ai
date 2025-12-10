/**
 * Complete Profile Page
 * Collects birth location after Google OAuth login
 * Google provides DOB and gender, we need birth place/time
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { motion } from 'framer-motion';
import { MapPin, Clock, Sparkles, Loader2, ChevronRight } from 'lucide-react';
import { getCityCoordinates } from '../services/api';

const places = [
  { name: 'சென்னை', english: 'Chennai' },
  { name: 'மதுரை', english: 'Madurai' },
  { name: 'கோயம்புத்தூர்', english: 'Coimbatore' },
  { name: 'திருச்சி', english: 'Tiruchirappalli' },
  { name: 'சேலம்', english: 'Salem' },
  { name: 'திருநெல்வேலி', english: 'Tirunelveli' },
  { name: 'ஈரோடு', english: 'Erode' },
  { name: 'வேலூர்', english: 'Vellore' },
  { name: 'தஞ்சாவூர்', english: 'Thanjavur' },
  { name: 'திண்டுக்கல்', english: 'Dindigul' },
];

export default function CompleteProfile() {
  const navigate = useNavigate();
  const { user, updateAstroProfile, loading: authLoading } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    birthDate: '',
    birthTime: '',
    birthPlace: ''
  });

  // Pre-fill birth date from Google if available
  useEffect(() => {
    if (user?.google_birthday) {
      setFormData(prev => ({
        ...prev,
        birthDate: user.google_birthday
      }));
    }
  }, [user]);

  // Redirect if not authenticated
  useEffect(() => {
    if (!authLoading && !user) {
      navigate('/onboarding');
    }
  }, [user, authLoading, navigate]);

  const handleSubmit = async () => {
    if (!formData.birthDate || !formData.birthPlace) {
      setError('பிறந்த தேதி மற்றும் இடம் அவசியம்');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const coords = getCityCoordinates(formData.birthPlace);

      await updateAstroProfile({
        birth_date: formData.birthDate,
        birth_time: formData.birthTime || null,
        birth_place: formData.birthPlace,
        latitude: coords.lat,
        longitude: coords.lon
      });

      // Also save to localStorage for immediate use
      localStorage.setItem('userProfile', JSON.stringify({
        name: user?.name,
        gender: user?.gender,
        birthDate: formData.birthDate,
        birthTime: formData.birthTime,
        birthPlace: formData.birthPlace
      }));
      localStorage.setItem('onboardingComplete', 'true');

      navigate('/');
    } catch (err) {
      console.error('Profile creation failed:', err);
      setError('சேமிப்பதில் பிழை. மீண்டும் முயற்சிக்கவும்.');
    } finally {
      setLoading(false);
    }
  };

  const isValid = formData.birthDate && formData.birthPlace;

  if (authLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-orange-50 flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-orange-500" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-orange-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-600 via-red-600 to-orange-600 h-2" />

      <div className="text-center pt-8 pb-4">
        <span className="text-5xl text-orange-600 font-serif">ॐ</span>
        <h1 className="text-xl font-bold text-orange-800 mt-2">ஜோதிட AI</h1>
      </div>

      {/* User Info Card */}
      {user && (
        <div className="mx-4 mb-6 bg-white rounded-xl p-4 border border-orange-200 shadow-sm">
          <div className="flex items-center gap-3">
            {user.picture && (
              <img
                src={user.picture}
                alt={user.name}
                className="w-12 h-12 rounded-full border-2 border-orange-200"
              />
            )}
            <div>
              <p className="font-medium text-gray-800">{user.name}</p>
              <p className="text-sm text-gray-500">{user.email}</p>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="px-4 pb-32"
      >
        <div className="text-center mb-6">
          <h2 className="text-xl font-bold text-gray-800">பிறந்த விவரங்கள்</h2>
          <p className="text-gray-600 text-sm mt-1">
            உங்கள் ஜாதகம் கணிக்க பிறந்த இடம் தேவை
          </p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-xl text-red-600 text-sm">
            {error}
          </div>
        )}

        <div className="space-y-5">
          {/* Birth Date */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-orange-500" />
              பிறந்த தேதி
              {user?.google_birthday && (
                <span className="text-xs text-green-600 bg-green-50 px-2 py-0.5 rounded-full">
                  Google இலிருந்து
                </span>
              )}
            </label>
            <input
              type="date"
              value={formData.birthDate}
              onChange={(e) => setFormData({ ...formData, birthDate: e.target.value })}
              className="w-full px-4 py-3 rounded-xl border-2 border-orange-200 focus:border-orange-500 focus:ring-0 outline-none transition-colors bg-white"
            />
          </div>

          {/* Birth Time */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
              <Clock className="w-4 h-4 text-orange-500" />
              பிறந்த நேரம்
              <span className="text-xs text-gray-500">(விருப்பம்)</span>
            </label>
            <input
              type="time"
              value={formData.birthTime}
              onChange={(e) => setFormData({ ...formData, birthTime: e.target.value })}
              className="w-full px-4 py-3 rounded-xl border-2 border-orange-200 focus:border-orange-500 focus:ring-0 outline-none transition-colors bg-white"
            />
            <p className="text-xs text-gray-500 mt-1">
              தெரியவில்லை என்றால் காலியாக விடலாம்
            </p>
          </div>

          {/* Birth Place */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
              <MapPin className="w-4 h-4 text-orange-500" />
              பிறந்த இடம்
            </label>
            <select
              value={formData.birthPlace}
              onChange={(e) => setFormData({ ...formData, birthPlace: e.target.value })}
              className="w-full px-4 py-3 rounded-xl border-2 border-orange-200 focus:border-orange-500 focus:ring-0 outline-none transition-colors bg-white"
            >
              <option value="">இடத்தை தேர்வு செய்யவும்</option>
              {places.map((p) => (
                <option key={p.english} value={p.name}>
                  {p.name} ({p.english})
                </option>
              ))}
            </select>
          </div>

          {/* Gender Display (from Google) */}
          {user?.gender && (
            <div className="bg-orange-50 rounded-xl p-4 border border-orange-200">
              <p className="text-sm text-gray-600">
                <span className="font-medium">பாலினம்:</span>{' '}
                {user.gender === 'male' ? 'ஆண்' : user.gender === 'female' ? 'பெண்' : user.gender}
                <span className="text-xs text-gray-500 ml-2">(Google இலிருந்து)</span>
              </p>
            </div>
          )}
        </div>
      </motion.div>

      {/* Bottom Button */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-orange-100 p-4 safe-bottom">
        <button
          onClick={handleSubmit}
          disabled={!isValid || loading}
          className={`w-full py-3 rounded-xl font-medium flex items-center justify-center gap-2 transition-all ${
            isValid && !loading
              ? 'bg-gradient-to-r from-orange-500 to-red-500 text-white shadow-lg shadow-orange-500/30'
              : 'bg-gray-200 text-gray-400'
          }`}
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              சேமிக்கிறது...
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              ஜாதகம் உருவாக்கு
              <ChevronRight className="w-5 h-5" />
            </>
          )}
        </button>
      </div>
    </div>
  );
}
