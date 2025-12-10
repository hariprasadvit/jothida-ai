/**
 * API Service for Jothida AI
 * Connects frontend to Python backend
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// City coordinates for location lookup (English and Tamil names)
const CITY_COORDS = {
  // English names
  'Chennai': { lat: 13.0827, lon: 80.2707 },
  'Coimbatore': { lat: 11.0168, lon: 76.9558 },
  'Madurai': { lat: 9.9252, lon: 78.1198 },
  'Tiruchirappalli': { lat: 10.7905, lon: 78.7047 },
  'Salem': { lat: 11.6643, lon: 78.1460 },
  'Tirunelveli': { lat: 8.7139, lon: 77.7567 },
  'Tiruppur': { lat: 11.1085, lon: 77.3411 },
  'Erode': { lat: 11.3410, lon: 77.7172 },
  'Vellore': { lat: 12.9165, lon: 79.1325 },
  'Thoothukudi': { lat: 8.7642, lon: 78.1348 },
  'Dindigul': { lat: 10.3624, lon: 77.9695 },
  'Thanjavur': { lat: 10.7870, lon: 79.1378 },
  'Ranipet': { lat: 12.9224, lon: 79.3209 },
  'Sivakasi': { lat: 9.4533, lon: 77.8025 },
  'Karur': { lat: 10.9601, lon: 78.0766 },
  'Udhagamandalam': { lat: 11.4064, lon: 76.6932 },
  'Hosur': { lat: 12.7409, lon: 77.8253 },
  'Nagercoil': { lat: 8.1833, lon: 77.4119 },
  'Kanchipuram': { lat: 12.8342, lon: 79.7036 },
  'Kumbakonam': { lat: 10.9617, lon: 79.3881 },
  // Tamil names
  'சென்னை': { lat: 13.0827, lon: 80.2707 },
  'மதுரை': { lat: 9.9252, lon: 78.1198 },
  'கோயம்புத்தூர்': { lat: 11.0168, lon: 76.9558 },
  'திருச்சி': { lat: 10.7905, lon: 78.7047 },
  'சேலம்': { lat: 11.6643, lon: 78.1460 },
  'திருநெல்வேலி': { lat: 8.7139, lon: 77.7567 },
  'ஈரோடு': { lat: 11.3410, lon: 77.7172 },
  'வேலூர்': { lat: 12.9165, lon: 79.1325 },
  'தஞ்சாவூர்': { lat: 10.7870, lon: 79.1378 },
  'திண்டுக்கல்': { lat: 10.3624, lon: 77.9695 },
};

/**
 * Get coordinates for a city
 */
export const getCityCoordinates = (cityName) => {
  return CITY_COORDS[cityName] || { lat: 13.0827, lon: 80.2707 }; // Default Chennai
};

/**
 * Panchangam API
 */
export const panchangamAPI = {
  // Get today's panchangam
  getToday: async (lat = 13.0827, lon = 80.2707) => {
    try {
      const response = await api.get('/api/panchangam/today', {
        params: { lat, lon }
      });
      return response.data;
    } catch (error) {
      console.error('Panchangam API error:', error);
      throw error;
    }
  },

  // Get panchangam for specific date
  getByDate: async (date, lat = 13.0827, lon = 80.2707) => {
    try {
      const response = await api.get(`/api/panchangam/date/${date}`, {
        params: { lat, lon }
      });
      return response.data;
    } catch (error) {
      console.error('Panchangam API error:', error);
      throw error;
    }
  },

  // Get hourly energy data for visualization
  getTimeEnergy: async (date = null, lat = 13.0827, lon = 80.2707) => {
    try {
      const params = { lat, lon };
      if (date) params.target_date = date;

      const response = await api.get('/api/panchangam/time-energy', { params });
      return response.data;
    } catch (error) {
      console.error('Time energy API error:', error);
      throw error;
    }
  },

  // Get 7-day forecast
  getWeekForecast: async (lat = 13.0827, lon = 80.2707) => {
    try {
      const response = await api.get('/api/panchangam/week-forecast', {
        params: { lat, lon }
      });
      return response.data;
    } catch (error) {
      console.error('Week forecast API error:', error);
      throw error;
    }
  },

  // Get score breakdown with all contributing factors
  getScoreBreakdown: async (date = null, lat = 13.0827, lon = 80.2707) => {
    try {
      const params = { lat, lon };
      if (date) params.target_date = date;

      const response = await api.get('/api/panchangam/score-breakdown', { params });
      return response.data;
    } catch (error) {
      console.error('Score breakdown API error:', error);
      throw error;
    }
  }
};

/**
 * Jathagam (Birth Chart) API
 */
export const jathagamAPI = {
  // Generate birth chart
  generate: async (birthDetails) => {
    try {
      const coords = getCityCoordinates(birthDetails.birthPlace);
      const payload = {
        name: birthDetails.name,
        date: birthDetails.birthDate,
        time: birthDetails.birthTime,
        place: birthDetails.birthPlace,
        latitude: coords.lat,
        longitude: coords.lon,
        timezone: 'Asia/Kolkata'
      };

      const response = await api.post('/api/jathagam/generate', payload);
      return response.data;
    } catch (error) {
      console.error('Jathagam API error:', error);
      throw error;
    }
  },

  // Get life areas scores
  getLifeAreas: async (birthDetails) => {
    try {
      const coords = getCityCoordinates(birthDetails.birthPlace);
      const payload = {
        name: birthDetails.name,
        date: birthDetails.birthDate,
        time: birthDetails.birthTime,
        place: birthDetails.birthPlace,
        latitude: coords.lat,
        longitude: coords.lon,
      };

      const response = await api.post('/api/jathagam/life-areas', payload);
      return response.data;
    } catch (error) {
      console.error('Life areas API error:', error);
      throw error;
    }
  }
};

/**
 * Matching API
 */
export const matchingAPI = {
  // Calculate matching (main method used by frontend)
  calculate: async (data) => {
    try {
      const payload = {
        bride: {
          name: data.bride.name,
          date: data.bride.birth_date,
          time: data.bride.birth_time,
          place: data.bride.birth_place,
          latitude: data.bride.latitude,
          longitude: data.bride.longitude,
          gender: 'female'
        },
        groom: {
          name: data.groom.name,
          date: data.groom.birth_date,
          time: data.groom.birth_time,
          place: data.groom.birth_place,
          latitude: data.groom.latitude,
          longitude: data.groom.longitude,
          gender: 'male'
        }
      };

      const response = await api.post('/api/matching/check', payload);
      return response.data;
    } catch (error) {
      console.error('Matching API error:', error);
      throw error;
    }
  },

  // Full matching with birth details
  checkFull: async (brideDetails, groomDetails) => {
    try {
      const brideCoords = getCityCoordinates(brideDetails.birthPlace);
      const groomCoords = getCityCoordinates(groomDetails.birthPlace);

      const payload = {
        bride: {
          name: brideDetails.name,
          date: brideDetails.birthDate,
          time: brideDetails.birthTime,
          place: brideDetails.birthPlace,
          latitude: brideCoords.lat,
          longitude: brideCoords.lon,
          gender: 'female'
        },
        groom: {
          name: groomDetails.name,
          date: groomDetails.birthDate,
          time: groomDetails.birthTime,
          place: groomDetails.birthPlace,
          latitude: groomCoords.lat,
          longitude: groomCoords.lon,
          gender: 'male'
        }
      };

      const response = await api.post('/api/matching/check', payload);
      return response.data;
    } catch (error) {
      console.error('Matching API error:', error);
      throw error;
    }
  },

  // Quick check with just nakshatra and rasi
  quickCheck: async (brideNakshatra, brideRasi, groomNakshatra, groomRasi) => {
    try {
      const response = await api.post('/api/matching/quick-check', null, {
        params: {
          bride_nakshatra: brideNakshatra,
          bride_rasi: brideRasi,
          groom_nakshatra: groomNakshatra,
          groom_rasi: groomRasi
        }
      });
      return response.data;
    } catch (error) {
      console.error('Quick matching API error:', error);
      throw error;
    }
  },

  // Get porutham details
  getPoruthamInfo: async (name) => {
    try {
      const response = await api.get(`/api/matching/porutham-details/${name}`);
      return response.data;
    } catch (error) {
      console.error('Porutham info API error:', error);
      throw error;
    }
  }
};

/**
 * Muhurtham API
 */
export const muhurthamAPI = {
  // Find good dates for an event
  findDates: async (eventType, startDate, endDate, lat = 13.0827, lon = 80.2707) => {
    try {
      const response = await api.get('/api/muhurtham/find', {
        params: { event_type: eventType, start_date: startDate, end_date: endDate, lat, lon }
      });
      return response.data;
    } catch (error) {
      console.error('Muhurtham API error:', error);
      throw error;
    }
  },

  // Get calendar view for a month
  getCalendar: async (month, year, lat = 13.0827, lon = 80.2707) => {
    try {
      const response = await api.get('/api/muhurtham/calendar', {
        params: { month, year, lat, lon }
      });
      return response.data;
    } catch (error) {
      console.error('Muhurtham calendar API error:', error);
      throw error;
    }
  },

  // Get detailed info for a specific date
  getDayDetails: async (date, lat = 13.0827, lon = 80.2707) => {
    try {
      const response = await api.get(`/api/muhurtham/day-details/${date}`, {
        params: { lat, lon }
      });
      return response.data;
    } catch (error) {
      console.error('Muhurtham day details API error:', error);
      throw error;
    }
  },

  // Get good times for a specific date (legacy)
  getTimes: async (date, eventType, lat = 13.0827, lon = 80.2707) => {
    try {
      const response = await api.get(`/api/muhurtham/day-details/${date}`, {
        params: { lat, lon }
      });
      return response.data;
    } catch (error) {
      console.error('Muhurtham times API error:', error);
      throw error;
    }
  }
};

/**
 * Chat API
 */
export const chatAPI = {
  // Send a message
  sendMessage: async (message, userProfile = null) => {
    try {
      // Generate a simple user ID from profile or random
      const userId = userProfile?.name
        ? `user_${userProfile.name.replace(/\s+/g, '_').toLowerCase()}`
        : `user_${Date.now()}`;

      const response = await api.post('/api/chat/message', {
        message,
        user_id: userId,
        context: userProfile ? {
          name: userProfile.name,
          rasi: userProfile.rasi,
          nakshatra: userProfile.nakshatra,
          birthDate: userProfile.birthDate,
          birthTime: userProfile.birthTime,
          birthPlace: userProfile.birthPlace
        } : null
      });
      return response.data;
    } catch (error) {
      console.error('Chat API error:', error);
      throw error;
    }
  },

  // Get quick questions
  getQuickQuestions: async () => {
    try {
      const response = await api.get('/api/chat/quick-questions');
      return response.data;
    } catch (error) {
      console.error('Quick questions API error:', error);
      throw error;
    }
  }
};

/**
 * Forecast API
 */
export const forecastAPI = {
  // Get complete forecast (daily, weekly, monthly, yearly, 3-year)
  getUserForecast: async (rasi, nakshatra, birthDate = null, lat = 13.0827, lon = 80.2707) => {
    try {
      const response = await api.post('/api/forecast/user', {
        rasi,
        nakshatra,
        birth_date: birthDate,
        latitude: lat,
        longitude: lon
      });
      return response.data;
    } catch (error) {
      console.error('Forecast API error:', error);
      throw error;
    }
  },

  // Get daily forecast
  getDaily: async (rasi, nakshatra = '', lat = 13.0827, lon = 80.2707) => {
    try {
      const response = await api.get('/api/forecast/daily', {
        params: { rasi, nakshatra, lat, lon }
      });
      return response.data;
    } catch (error) {
      console.error('Daily forecast API error:', error);
      throw error;
    }
  },

  // Get weekly forecast
  getWeekly: async (rasi, nakshatra = '') => {
    try {
      const response = await api.get('/api/forecast/weekly', {
        params: { rasi, nakshatra }
      });
      return response.data;
    } catch (error) {
      console.error('Weekly forecast API error:', error);
      throw error;
    }
  },

  // Get monthly forecast
  getMonthly: async (rasi, nakshatra = '', month = null, year = null) => {
    try {
      const params = { rasi, nakshatra };
      if (month) params.month = month;
      if (year) params.year = year;

      const response = await api.get('/api/forecast/monthly', { params });
      return response.data;
    } catch (error) {
      console.error('Monthly forecast API error:', error);
      throw error;
    }
  },

  // Get yearly forecast
  getYearly: async (rasi, nakshatra = '', year = null) => {
    try {
      const params = { rasi, nakshatra };
      if (year) params.year = year;

      const response = await api.get('/api/forecast/yearly', { params });
      return response.data;
    } catch (error) {
      console.error('Yearly forecast API error:', error);
      throw error;
    }
  },

  // Get 3-year forecast
  getThreeYears: async (rasi, nakshatra = '') => {
    try {
      const response = await api.get('/api/forecast/three-years', {
        params: { rasi, nakshatra }
      });
      return response.data;
    } catch (error) {
      console.error('Three year forecast API error:', error);
      throw error;
    }
  }
};

/**
 * User Profile API
 */
export const userAPI = {
  // Get user profile summary (rasi, nakshatra, dasha)
  getProfileSummary: async (birthDetails) => {
    try {
      const coords = getCityCoordinates(birthDetails.birthPlace || birthDetails.place);
      const payload = {
        name: birthDetails.name,
        date: birthDetails.birthDate || birthDetails.date,
        time: birthDetails.birthTime || birthDetails.time,
        place: birthDetails.birthPlace || birthDetails.place,
        latitude: coords.lat,
        longitude: coords.lon
      };

      const response = await api.post('/api/user/profile-summary', payload);
      return response.data;
    } catch (error) {
      console.error('User profile API error:', error);
      throw error;
    }
  },

  // Register a new user from onboarding
  register: async (userData) => {
    try {
      const coords = getCityCoordinates(userData.birthPlace);
      const response = await api.post('/api/user/register', {
        name: userData.name,
        gender: userData.gender,
        birth_date: userData.birthDate,
        birth_time: userData.birthTime || null,
        birth_place: userData.birthPlace,
        latitude: coords.lat,
        longitude: coords.lon
      });
      return response.data;
    } catch (error) {
      console.error('User registration error:', error);
      throw error;
    }
  },

  // Get all users (admin)
  list: async () => {
    try {
      const response = await api.get('/api/user/list');
      return response.data;
    } catch (error) {
      console.error('User list error:', error);
      throw error;
    }
  }
};

/**
 * Auth API
 */
export const authAPI = {
  // Get Google login URL
  getGoogleLoginUrl: async () => {
    try {
      const response = await api.get('/api/auth/google/login');
      return response.data;
    } catch (error) {
      console.error('Auth API error:', error);
      throw error;
    }
  },

  // Get current user info
  getCurrentUser: async () => {
    try {
      const token = localStorage.getItem('authToken');
      if (!token) return null;

      const response = await api.get('/api/auth/me', {
        headers: { Authorization: `Bearer ${token}` }
      });
      return response.data;
    } catch (error) {
      console.error('Get user API error:', error);
      // Clear invalid token
      if (error.response?.status === 401) {
        localStorage.removeItem('authToken');
      }
      return null;
    }
  },

  // Check auth status
  checkAuth: async () => {
    try {
      const token = localStorage.getItem('authToken');
      if (!token) return { authenticated: false };

      const response = await api.get('/api/auth/check', {
        headers: { Authorization: `Bearer ${token}` }
      });
      return response.data;
    } catch (error) {
      return { authenticated: false };
    }
  },

  // Create/update astro profile
  createAstroProfile: async (profileData) => {
    try {
      const token = localStorage.getItem('authToken');
      if (!token) throw new Error('Not authenticated');

      const response = await api.post('/api/auth/profile/astro', profileData, {
        headers: { Authorization: `Bearer ${token}` }
      });
      return response.data;
    } catch (error) {
      console.error('Create profile API error:', error);
      throw error;
    }
  },

  // Logout
  logout: async () => {
    try {
      const token = localStorage.getItem('authToken');
      if (token) {
        await api.post('/api/auth/logout', {}, {
          headers: { Authorization: `Bearer ${token}` }
        });
      }
    } catch (error) {
      console.error('Logout API error:', error);
    } finally {
      localStorage.removeItem('authToken');
    }
  }
};

/**
 * Mobile Auth API (OTP-based login)
 */
export const mobileAuthAPI = {
  // Send OTP to phone number
  sendOTP: async (phoneNumber) => {
    try {
      const response = await api.post('/api/mobile/send-otp', {
        phone_number: phoneNumber
      });
      return response.data;
    } catch (error) {
      console.error('Send OTP error:', error);
      throw error;
    }
  },

  // Verify OTP
  verifyOTP: async (phoneNumber, otpCode) => {
    try {
      const response = await api.post('/api/mobile/verify-otp', {
        phone_number: phoneNumber,
        otp_code: otpCode
      });
      return response.data;
    } catch (error) {
      console.error('Verify OTP error:', error);
      throw error;
    }
  },

  // Register with phone (after OTP verification)
  register: async (data) => {
    try {
      const coords = getCityCoordinates(data.birthPlace);
      const response = await api.post('/api/mobile/register', {
        phone_number: data.phoneNumber,
        otp_code: data.otpCode,
        name: data.name,
        gender: data.gender,
        birth_date: data.birthDate,
        birth_time: data.birthTime || null,
        birth_place: data.birthPlace,
        latitude: coords.lat,
        longitude: coords.lon
      });
      return response.data;
    } catch (error) {
      console.error('Mobile registration error:', error);
      throw error;
    }
  },

  // Get current user from token
  getCurrentUser: async () => {
    try {
      const token = localStorage.getItem('authToken');
      if (!token) return null;

      const response = await api.get('/api/mobile/me', {
        headers: { Authorization: `Bearer ${token}` }
      });
      return response.data;
    } catch (error) {
      console.error('Get mobile user error:', error);
      if (error.response?.status === 401) {
        localStorage.removeItem('authToken');
      }
      return null;
    }
  }
};

/**
 * PDF Report API
 */
export const reportAPI = {
  // Generate and download PDF report
  generateReport: async (birthDetails) => {
    try {
      const coords = getCityCoordinates(birthDetails.birthPlace);
      const response = await api.post('/api/report/generate', {
        name: birthDetails.name,
        birth_date: birthDetails.birthDate,
        birth_time: birthDetails.birthTime,
        birth_place: birthDetails.birthPlace,
        latitude: coords.lat,
        longitude: coords.lon
      }, {
        responseType: 'blob'
      });

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Jathagam_Report_${birthDetails.name.replace(/\s+/g, '_')}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      return { success: true };
    } catch (error) {
      console.error('Report generation error:', error);
      throw error;
    }
  },

  // Download report for registered user
  downloadUserReport: async (userId) => {
    try {
      const response = await api.get(`/api/report/download/${userId}`, {
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Jathagam_Report.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      return { success: true };
    } catch (error) {
      console.error('Report download error:', error);
      throw error;
    }
  },

  // Get report preview info
  getReportInfo: async () => {
    try {
      const response = await api.get('/api/report/preview');
      return response.data;
    } catch (error) {
      console.error('Report info error:', error);
      throw error;
    }
  }
};

/**
 * Health check
 */
export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    return { status: 'offline' };
  }
};

export default api;
