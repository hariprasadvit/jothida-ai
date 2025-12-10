import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

// Change this to your actual server IP when testing on device
// For emulator use: http://10.0.2.2:8000 (Android) or http://localhost:8000 (iOS)
// For physical device use your computer's local IP: http://192.168.x.x:8000
const API_BASE_URL = 'http://192.168.1.40:8000'; // Update with your IP

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use(async (config) => {
  try {
    const token = await SecureStore.getItemAsync('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  } catch (error) {
    console.error('Error getting token:', error);
  }
  return config;
});

// City coordinates for birth place lookup
export const CITY_COORDINATES = {
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

export const getCityCoordinates = (city) => {
  return CITY_COORDINATES[city] || { lat: 13.0827, lon: 80.2707 };
};

// Mobile Auth API
export const mobileAuthAPI = {
  sendOTP: async (phoneNumber) => {
    const response = await api.post('/api/mobile/send-otp', {
      phone_number: phoneNumber,
    });
    return response.data;
  },

  verifyOTP: async (phoneNumber, otpCode) => {
    const response = await api.post('/api/mobile/verify-otp', {
      phone_number: phoneNumber,
      otp_code: otpCode,
    });
    return response.data;
  },

  register: async (data) => {
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
      longitude: coords.lon,
    });
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get('/api/mobile/me');
    return response.data;
  },
};

// Combined Mobile API for all screens
export const mobileAPI = {
  // Panchangam
  getPanchangam: async () => {
    try {
      const response = await api.get('/api/panchangam/today');
      return response.data;
    } catch (error) {
      console.error('Panchangam API error:', error);
      return null;
    }
  },

  // Jathagam
  getJathagam: async (data) => {
    try {
      const coords = getCityCoordinates(data.birthPlace);
      const response = await api.post('/api/jathagam/generate', {
        name: data.name,
        date: data.birthDate,
        time: data.birthTime,
        place: data.birthPlace,
        latitude: coords.lat,
        longitude: coords.lon,
      });
      return response.data;
    } catch (error) {
      console.error('Jathagam API error:', error);
      return null;
    }
  },

  // Matching
  calculateMatching: async (payload) => {
    const response = await api.post('/api/matching/calculate', payload);
    return response.data;
  },

  // Chat
  sendChatMessage: async (message, userProfile = {}) => {
    try {
      const response = await api.post('/api/chat/message', {
        message: message,
        user_id: userProfile?.phone || 'anonymous',
        context: {
          rasi: userProfile?.rasi,
          nakshatra: userProfile?.nakshatra,
          birthDate: userProfile?.birthDate,
        },
      });
      return response.data;
    } catch (error) {
      console.error('Chat API error:', error);
      throw error;
    }
  },

  // Muhurtham Calendar
  getMuhurthamCalendar: async (month, year) => {
    try {
      const response = await api.get('/api/muhurtham/calendar', {
        params: { month, year }
      });
      return response.data;
    } catch (error) {
      console.error('Muhurtham calendar API error:', error);
      return [];
    }
  },

  // Muhurtham Day Details
  getMuhurthamDayDetails: async (dateStr) => {
    try {
      const response = await api.get(`/api/muhurtham/day-details/${dateStr}`);
      return response.data;
    } catch (error) {
      console.error('Muhurtham day API error:', error);
      return null;
    }
  },

  // Forecast
  getForecast: async (rasi, nakshatra, birthDate) => {
    try {
      const response = await api.get('/api/forecast/user', {
        params: { rasi, nakshatra, birth_date: birthDate },
      });
      return response.data;
    } catch (error) {
      console.error('Forecast API error:', error);
      return null;
    }
  },
};

// Jathagam API
export const jathagamAPI = {
  generate: async (data) => {
    const coords = getCityCoordinates(data.birthPlace);
    const response = await api.post('/api/jathagam/generate', {
      name: data.name,
      date: data.birthDate,
      time: data.birthTime,
      place: data.birthPlace,
      latitude: coords.lat,
      longitude: coords.lon,
    });
    return response.data;
  },
};

// Panchangam API
export const panchangamAPI = {
  getToday: async () => {
    const response = await api.get('/api/panchangam/today');
    return response.data;
  },
};

// Forecast API
export const forecastAPI = {
  getDaily: async (rasi) => {
    const response = await api.get(`/api/forecast/daily/${encodeURIComponent(rasi)}`);
    return response.data;
  },
};

// Matching API
export const matchingAPI = {
  calculate: async (payload) => {
    const response = await api.post('/api/matching/calculate', payload);
    return response.data;
  },
};

// Chat API
export const chatAPI = {
  send: async (message, userId, context = {}) => {
    const response = await api.post('/api/chat/message', {
      message: message,
      user_id: userId || 'anonymous',
      context,
    });
    return response.data;
  },
};

// Muhurtham API
export const muhurthamAPI = {
  find: async (params) => {
    const response = await api.get('/api/muhurtham/find', { params });
    return response.data;
  },
  getCalendar: async (month, year) => {
    const response = await api.get('/api/muhurtham/calendar', {
      params: { month, year }
    });
    return response.data;
  },
  getDayDetails: async (dateStr) => {
    const response = await api.get(`/api/muhurtham/day-details/${dateStr}`);
    return response.data;
  },
};

// Report API
export const reportAPI = {
  generateReport: async (birthDetails) => {
    const coords = getCityCoordinates(birthDetails.birthPlace);
    const response = await api.post('/api/report/generate', {
      name: birthDetails.name,
      birth_date: birthDetails.birthDate,
      birth_time: birthDetails.birthTime,
      birth_place: birthDetails.birthPlace,
      latitude: coords.lat,
      longitude: coords.lon,
    }, {
      responseType: 'blob',
    });
    return response.data;
  },
};

export default api;
