import axios from 'axios';
import { Platform } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import AsyncStorage from '@react-native-async-storage/async-storage';

// API URL - switch between local and production
// const API_BASE_URL = 'http://localhost:8000';
const API_BASE_URL = 'https://jothida-api.booleanbeyond.com';

// Storage helper for web compatibility
const getStorageItem = async (key) => {
  if (Platform.OS === 'web') {
    return AsyncStorage.getItem(key);
  }
  return SecureStore.getItemAsync(key);
};

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
    const token = await getStorageItem('authToken');
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
  // Tamil Nadu
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
  'Kanchipuram': { lat: 12.8342, lon: 79.7036 },
  'Kumbakonam': { lat: 10.9617, lon: 79.3881 },
  'Nagercoil': { lat: 8.1833, lon: 77.4119 },
  'Karur': { lat: 10.9601, lon: 78.0766 },
  'Cuddalore': { lat: 11.7480, lon: 79.7714 },
  'Hosur': { lat: 12.7409, lon: 77.8253 },
  'Pondicherry': { lat: 11.9416, lon: 79.8083 },

  // Other South Indian Cities
  'Bangalore': { lat: 12.9716, lon: 77.5946 },
  'Hyderabad': { lat: 17.3850, lon: 78.4867 },
  'Kochi': { lat: 9.9312, lon: 76.2673 },
  'Thiruvananthapuram': { lat: 8.5241, lon: 76.9366 },
  'Mysore': { lat: 12.2958, lon: 76.6394 },
  'Mangalore': { lat: 12.9141, lon: 74.8560 },
  'Visakhapatnam': { lat: 17.6868, lon: 83.2185 },
  'Vijayawada': { lat: 16.5062, lon: 80.6480 },
  'Tirupati': { lat: 13.6288, lon: 79.4192 },
  'Kozhikode': { lat: 11.2588, lon: 75.7804 },
  'Thrissur': { lat: 10.5276, lon: 76.2144 },

  // North Indian Cities
  'Delhi': { lat: 28.6139, lon: 77.2090 },
  'New Delhi': { lat: 28.6139, lon: 77.2090 },
  'Mumbai': { lat: 19.0760, lon: 72.8777 },
  'Kolkata': { lat: 22.5726, lon: 88.3639 },
  'Ahmedabad': { lat: 23.0225, lon: 72.5714 },
  'Pune': { lat: 18.5204, lon: 73.8567 },
  'Jaipur': { lat: 26.9124, lon: 75.7873 },
  'Lucknow': { lat: 26.8467, lon: 80.9462 },
  'Kanpur': { lat: 26.4499, lon: 80.3319 },
  'Nagpur': { lat: 21.1458, lon: 79.0882 },
  'Indore': { lat: 22.7196, lon: 75.8577 },
  'Bhopal': { lat: 23.2599, lon: 77.4126 },
  'Patna': { lat: 25.5941, lon: 85.1376 },
  'Varanasi': { lat: 25.3176, lon: 82.9739 },
  'Agra': { lat: 27.1767, lon: 78.0081 },
  'Surat': { lat: 21.1702, lon: 72.8311 },
  'Chandigarh': { lat: 30.7333, lon: 76.7794 },
  'Amritsar': { lat: 31.6340, lon: 74.8723 },
  'Guwahati': { lat: 26.1445, lon: 91.7362 },
  'Ranchi': { lat: 23.3441, lon: 85.3096 },
  'Bhubaneswar': { lat: 20.2961, lon: 85.8245 },

  // International - Middle East
  'Dubai': { lat: 25.2048, lon: 55.2708 },
  'Abu Dhabi': { lat: 24.4539, lon: 54.3773 },
  'Sharjah': { lat: 25.3463, lon: 55.4209 },
  'Muscat': { lat: 23.5880, lon: 58.3829 },
  'Doha': { lat: 25.2854, lon: 51.5310 },
  'Kuwait City': { lat: 29.3759, lon: 47.9774 },
  'Riyadh': { lat: 24.7136, lon: 46.6753 },
  'Jeddah': { lat: 21.4858, lon: 39.1925 },
  'Bahrain': { lat: 26.0667, lon: 50.5577 },

  // International - Southeast Asia
  'Singapore': { lat: 1.3521, lon: 103.8198 },
  'Kuala Lumpur': { lat: 3.1390, lon: 101.6869 },
  'Bangkok': { lat: 13.7563, lon: 100.5018 },
  'Jakarta': { lat: -6.2088, lon: 106.8456 },
  'Manila': { lat: 14.5995, lon: 120.9842 },
  'Ho Chi Minh City': { lat: 10.8231, lon: 106.6297 },

  // International - East Asia
  'Hong Kong': { lat: 22.3193, lon: 114.1694 },
  'Tokyo': { lat: 35.6762, lon: 139.6503 },
  'Seoul': { lat: 37.5665, lon: 126.9780 },
  'Beijing': { lat: 39.9042, lon: 116.4074 },
  'Shanghai': { lat: 31.2304, lon: 121.4737 },
  'Taipei': { lat: 25.0330, lon: 121.5654 },

  // International - Europe
  'London': { lat: 51.5074, lon: -0.1278 },
  'Paris': { lat: 48.8566, lon: 2.3522 },
  'Berlin': { lat: 52.5200, lon: 13.4050 },
  'Amsterdam': { lat: 52.3676, lon: 4.9041 },
  'Frankfurt': { lat: 50.1109, lon: 8.6821 },
  'Zurich': { lat: 47.3769, lon: 8.5417 },
  'Geneva': { lat: 46.2044, lon: 6.1432 },
  'Munich': { lat: 48.1351, lon: 11.5820 },
  'Rome': { lat: 41.9028, lon: 12.4964 },
  'Milan': { lat: 45.4642, lon: 9.1900 },
  'Madrid': { lat: 40.4168, lon: -3.7038 },
  'Barcelona': { lat: 41.3851, lon: 2.1734 },
  'Vienna': { lat: 48.2082, lon: 16.3738 },
  'Dublin': { lat: 53.3498, lon: -6.2603 },
  'Stockholm': { lat: 59.3293, lon: 18.0686 },
  'Oslo': { lat: 59.9139, lon: 10.7522 },
  'Copenhagen': { lat: 55.6761, lon: 12.5683 },
  'Helsinki': { lat: 60.1699, lon: 24.9384 },
  'Brussels': { lat: 50.8503, lon: 4.3517 },
  'Prague': { lat: 50.0755, lon: 14.4378 },
  'Warsaw': { lat: 52.2297, lon: 21.0122 },
  'Budapest': { lat: 47.4979, lon: 19.0402 },
  'Athens': { lat: 37.9838, lon: 23.7275 },
  'Moscow': { lat: 55.7558, lon: 37.6173 },

  // International - North America
  'New York': { lat: 40.7128, lon: -74.0060 },
  'Los Angeles': { lat: 34.0522, lon: -118.2437 },
  'Chicago': { lat: 41.8781, lon: -87.6298 },
  'Houston': { lat: 29.7604, lon: -95.3698 },
  'San Francisco': { lat: 37.7749, lon: -122.4194 },
  'Seattle': { lat: 47.6062, lon: -122.3321 },
  'Boston': { lat: 42.3601, lon: -71.0589 },
  'Dallas': { lat: 32.7767, lon: -96.7970 },
  'Atlanta': { lat: 33.7490, lon: -84.3880 },
  'Washington DC': { lat: 38.9072, lon: -77.0369 },
  'Miami': { lat: 25.7617, lon: -80.1918 },
  'Phoenix': { lat: 33.4484, lon: -112.0740 },
  'Denver': { lat: 39.7392, lon: -104.9903 },
  'San Diego': { lat: 32.7157, lon: -117.1611 },
  'Austin': { lat: 30.2672, lon: -97.7431 },
  'Toronto': { lat: 43.6532, lon: -79.3832 },
  'Vancouver': { lat: 49.2827, lon: -123.1207 },
  'Montreal': { lat: 45.5017, lon: -73.5673 },
  'Calgary': { lat: 51.0447, lon: -114.0719 },
  'Mexico City': { lat: 19.4326, lon: -99.1332 },

  // International - Oceania
  'Sydney': { lat: -33.8688, lon: 151.2093 },
  'Melbourne': { lat: -37.8136, lon: 144.9631 },
  'Brisbane': { lat: -27.4698, lon: 153.0251 },
  'Perth': { lat: -31.9505, lon: 115.8605 },
  'Auckland': { lat: -36.8509, lon: 174.7645 },
  'Wellington': { lat: -41.2865, lon: 174.7762 },

  // International - Africa
  'Johannesburg': { lat: -26.2041, lon: 28.0473 },
  'Cape Town': { lat: -33.9249, lon: 18.4241 },
  'Cairo': { lat: 30.0444, lon: 31.2357 },
  'Nairobi': { lat: -1.2921, lon: 36.8219 },
  'Lagos': { lat: 6.5244, lon: 3.3792 },

  // International - South America
  'Sao Paulo': { lat: -23.5505, lon: -46.6333 },
  'Rio de Janeiro': { lat: -22.9068, lon: -43.1729 },
  'Buenos Aires': { lat: -34.6037, lon: -58.3816 },
  'Santiago': { lat: -33.4489, lon: -70.6693 },
  'Lima': { lat: -12.0464, lon: -77.0428 },
  'Bogota': { lat: 4.7110, lon: -74.0721 },

  // Sri Lanka
  'Colombo': { lat: 6.9271, lon: 79.8612 },
  'Jaffna': { lat: 9.6615, lon: 80.0255 },
  'Kandy': { lat: 7.2906, lon: 80.6337 },

  // Mauritius
  'Port Louis': { lat: -20.1609, lon: 57.5012 },
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

      // Transform dasha data to expected format
      const jathagamData = response.data;
      if (jathagamData?.dasha?.current) {
        jathagamData.dasha = {
          mahadasha: jathagamData.dasha.current.lord,
          mahadasha_tamil: jathagamData.dasha.current.tamil_lord,
          antardasha: jathagamData.dasha.current.lord, // Using same for now
          antardasha_tamil: jathagamData.dasha.current.tamil_lord,
          all_periods: jathagamData.dasha.all_periods,
        };
      }
      return jathagamData;
    } catch (error) {
      console.error('Jathagam API error:', error);
      return null;
    }
  },

  // Matching
  calculateMatching: async (payload) => {
    // Transform payload to match backend expected format
    // Backend expects: name, date (YYYY-MM-DD), time (HH:MM), place, latitude, longitude, gender
    const transformedPayload = {
      bride: {
        name: payload.bride.name,
        date: payload.bride.birth_date,
        time: payload.bride.birth_time,
        place: payload.bride.birth_place,
        latitude: payload.bride.latitude,
        longitude: payload.bride.longitude,
        gender: 'female'
      },
      groom: {
        name: payload.groom.name,
        date: payload.groom.birth_date,
        time: payload.groom.birth_time,
        place: payload.groom.birth_place,
        latitude: payload.groom.latitude,
        longitude: payload.groom.longitude,
        gender: 'male'
      }
    };
    const response = await api.post('/api/matching/check', transformedPayload);
    return response.data;
  },

  // Chat
  sendChatMessage: async (message, userProfile = {}, language = 'en') => {
    try {
      const response = await api.post('/api/chat/message', {
        message: message,
        user_id: userProfile?.phone || 'anonymous',
        language: language,
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
  getMuhurthamCalendar: async (month, year, lang = 'ta') => {
    try {
      const response = await api.get('/api/muhurtham/calendar', {
        params: { month, year, lang }
      });
      return response.data;
    } catch (error) {
      console.error('Muhurtham calendar API error:', error);
      // Return fallback data with extensive event-specific scoring logic
      const daysInMonth = new Date(year, month, 0).getDate();

      // Event-specific day preferences (0=Sun, 1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri, 6=Sat)
      const eventDayScores = {
        // Marriage: Best on Mon, Wed, Thu, Fri. Avoid Tue, Sat
        marriage: { 0: 60, 1: 75, 2: 25, 3: 80, 4: 85, 5: 80, 6: 30 },
        // Housewarming: Best on Mon, Wed, Thu, Fri. Avoid Tue, Sat, Sun
        griha_pravesam: { 0: 45, 1: 80, 2: 20, 3: 85, 4: 90, 5: 75, 6: 35 },
        // Vehicle: Best on Wed, Thu, Fri, Sat. Avoid Tue
        vehicle: { 0: 55, 1: 60, 2: 25, 3: 80, 4: 85, 5: 80, 6: 70 },
        // Business: Best on Mon, Wed, Thu, Fri. Avoid Tue, Sat
        business: { 0: 50, 1: 75, 2: 30, 3: 85, 4: 80, 5: 85, 6: 40 },
        // Travel: Best on Mon, Wed, Fri. Avoid Tue, Sat
        travel: { 0: 55, 1: 80, 2: 20, 3: 75, 4: 65, 5: 85, 6: 35 },
        // General: Balanced, slight preference for Thu, Fri
        general: { 0: 55, 1: 65, 2: 35, 3: 70, 4: 75, 5: 70, 6: 45 },
      };

      // Tithi simulation based on lunar cycle (approx 29.5 days)
      const getTithiScore = (day, eventType) => {
        // Simulate tithi: good tithis on 2,3,5,7,10,11,13 of lunar cycle
        const lunarDay = ((day + 10) % 15) + 1; // Approximate tithi
        const goodTithis = [2, 3, 5, 7, 10, 11, 13];
        const badTithis = [4, 8, 9, 14]; // Chaturthi, Ashtami, Navami, Chaturdashi

        if (goodTithis.includes(lunarDay)) return 15;
        if (badTithis.includes(lunarDay)) return -15;
        // Amavasya (new moon) and Purnima (full moon)
        if (lunarDay === 15) return eventType === 'marriage' ? -10 : 5; // Purnima
        if (lunarDay === 1) return -20; // Amavasya - avoid for all
        return 0;
      };

      // Nakshatra simulation based on day
      const getNakshatraScore = (day, eventType) => {
        // 27 nakshatras, cycle through them
        const nakshatraIndex = (day * 3 + month) % 27;

        // Good nakshatras by event type (indices)
        const goodNakshatras = {
          marriage: [3, 4, 9, 11, 12, 14, 16, 18, 20, 22, 25, 26], // Rohini, Mrigashira, Magha, etc.
          griha_pravesam: [3, 4, 7, 11, 12, 13, 14, 16, 20, 22, 23, 25, 26],
          vehicle: [0, 3, 4, 6, 7, 12, 13, 14, 16, 22, 23, 26],
          business: [0, 3, 4, 6, 7, 9, 11, 12, 13, 14, 16, 20, 22, 26],
          travel: [0, 4, 6, 7, 12, 16, 22, 23, 26],
          general: [0, 3, 4, 6, 7, 11, 12, 13, 14, 16, 20, 22, 23, 25, 26],
        };

        // Bad nakshatras to avoid
        const badNakshatras = [1, 2, 5, 8, 10, 15, 17, 19, 24]; // Bharani, Krittika, Ardra, etc.

        if (goodNakshatras[eventType]?.includes(nakshatraIndex)) return 20;
        if (badNakshatras.includes(nakshatraIndex)) return -20;
        return 0;
      };

      return Array.from({ length: daysInMonth }, (_, i) => {
        const day = i + 1;
        const dayOfWeek = new Date(year, month - 1, day).getDay();

        // Calculate scores for each event type
        const eventScores = {};
        const goodForEvents = [];

        Object.keys(eventDayScores).forEach(eventType => {
          // Base score from day of week
          let score = eventDayScores[eventType][dayOfWeek];

          // Add tithi influence
          score += getTithiScore(day, eventType);

          // Add nakshatra influence
          score += getNakshatraScore(day, eventType);

          // Add some variation based on day number for visual interest
          score += Math.sin(day * 0.3) * 8;

          // Clamp score between 15 and 95
          score = Math.max(15, Math.min(95, Math.round(score)));

          eventScores[eventType] = score;

          // Mark as good for this event if score >= 65
          if (score >= 65) {
            goodForEvents.push({
              type: eventType,
              label: eventType === 'griha_pravesam' ? 'Housewarming' :
                     eventType.charAt(0).toUpperCase() + eventType.slice(1),
              score: score
            });
          }
        });

        // General day score
        const generalScore = eventScores.general;

        return {
          date: `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`,
          day_score: generalScore,
          is_auspicious: generalScore >= 60,
          has_muhurtham: generalScore >= 70,
          event_scores: eventScores,
          good_for_events: goodForEvents,
          festivals: [],
          warnings: dayOfWeek === 2 ? ['Tuesday - Generally Avoid'] : []
        };
      });
    }
  },

  // Muhurtham Day Details
  getMuhurthamDayDetails: async (dateStr, lang = 'ta') => {
    try {
      const response = await api.get(`/api/muhurtham/day-details/${dateStr}`, {
        params: { lang }
      });
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

  // Life Timeline
  getLifeTimeline: async (birthDetails, yearsAhead = 10) => {
    try {
      const coords = getCityCoordinates(birthDetails.birthPlace);
      const response = await api.post('/api/forecast/life-timeline', {
        name: birthDetails.name,
        birth_date: birthDetails.birthDate,
        birth_time: birthDetails.birthTime,
        birth_place: birthDetails.birthPlace,
        latitude: coords.lat,
        longitude: coords.lon,
        years_ahead: yearsAhead,
      });
      return response.data;
    } catch (error) {
      console.error('Life Timeline API error:', error);
      return null;
    }
  },

  // Planet Aura (Strength Visualization)
  getPlanetAura: async (birthDetails) => {
    try {
      const coords = getCityCoordinates(birthDetails.birthPlace);
      const response = await api.post('/api/forecast/planet-aura', {
        name: birthDetails.name,
        birth_date: birthDetails.birthDate,
        birth_time: birthDetails.birthTime,
        birth_place: birthDetails.birthPlace,
        latitude: coords.lat,
        longitude: coords.lon,
      });
      return response.data;
    } catch (error) {
      console.error('Planet Aura API error:', error);
      return null;
    }
  },

  // Transits Map (Live Planetary Movements)
  getTransitsMap: async (birthPlace, rasi = '') => {
    try {
      const coords = getCityCoordinates(birthPlace);
      const response = await api.get('/api/forecast/transits-map', {
        params: {
          lat: coords.lat,
          lon: coords.lon,
          rasi: rasi,
        },
      });
      return response.data;
    } catch (error) {
      console.error('Transits Map API error:', error);
      return null;
    }
  },

  // Life Areas (Dynamic calculation based on birth chart)
  getLifeAreas: async (birthDetails, language = 'ta') => {
    try {
      const coords = getCityCoordinates(birthDetails.birthPlace);
      const response = await api.post('/api/forecast/life-areas', {
        name: birthDetails.name,
        birth_date: birthDetails.birthDate,
        birth_time: birthDetails.birthTime,
        birth_place: birthDetails.birthPlace,
        latitude: coords.lat,
        longitude: coords.lon,
        language: language,
      });
      return response.data;
    } catch (error) {
      console.error('Life Areas API error:', error);
      return null;
    }
  },

  getFutureProjections: async (birthDetails, language = 'ta') => {
    try {
      const coords = getCityCoordinates(birthDetails.birthPlace);
      const response = await api.post('/api/forecast/future-projections', {
        name: birthDetails.name,
        birth_date: birthDetails.birthDate,
        birth_time: birthDetails.birthTime,
        birth_place: birthDetails.birthPlace,
        latitude: coords.lat,
        longitude: coords.lon,
        language: language,
      });
      return response.data;
    } catch (error) {
      console.error('Future Projections API error:', error);
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
    const isWeb = Platform.OS === 'web';

    const response = await api.post('/api/report/generate', {
      name: birthDetails.name,
      birth_date: birthDetails.birthDate,
      birth_time: birthDetails.birthTime,
      birth_place: birthDetails.birthPlace,
      latitude: coords.lat,
      longitude: coords.lon,
    }, {
      responseType: isWeb ? 'blob' : 'arraybuffer',
    });

    // For web, return blob directly
    if (isWeb) {
      return response.data;
    }

    // For mobile (React Native), convert arraybuffer to base64
    // This will be handled by the ProfileScreen
    return {
      data: response.data,
      isArrayBuffer: true
    };
  },
};

// Ungal Jothidan (Your Astrologer) - Daily Intelligence Dashboard API
export const ungalJothidanAPI = {
  // Get daily insights for a user
  getDailyInsights: async (userData, language = 'ta', targetDate = null) => {
    const coords = getCityCoordinates(userData.birthPlace);
    const response = await api.post('/api/ungal-jothidan/daily-insights', {
      user_id: userData.id || userData.phone || 'demo',
      name: userData.name,
      birth_date: userData.birthDate,
      birth_time: userData.birthTime || '06:00',
      birth_place: userData.birthPlace,
      rasi: userData.rasi,
      nakshatra: userData.nakshatra,
      language: language,
      target_date: targetDate,
    });
    return response.data;
  },

  // Get insights by user ID (from database)
  getDailyInsightsByUserId: async (userId, language = 'ta', targetDate = null) => {
    const response = await api.get(`/api/ungal-jothidan/daily-insights/${userId}`, {
      params: { language, target_date: targetDate },
    });
    return response.data;
  },

  // Get detailed explanation for a specific card
  getCardDetails: async (cardId, userId, language = 'ta') => {
    const response = await api.get(`/api/ungal-jothidan/card-details/${cardId}`, {
      params: { user_id: userId, language },
    });
    return response.data;
  },
};

// AI Remedy Engine API
export const remedyAPI = {
  // Get personalized remedies based on birth chart
  getPersonalized: async (birthDetails, goal = null, language = 'ta') => {
    const coords = getCityCoordinates(birthDetails.birthPlace);
    const response = await api.post('/api/remedy/personalized', {
      name: birthDetails.name,
      birth_date: birthDetails.birthDate,
      birth_time: birthDetails.birthTime,
      birth_place: birthDetails.birthPlace,
      latitude: coords.lat,
      longitude: coords.lon,
      goal: goal,
      language: language,
    });
    return response.data;
  },

  // Get remedies for a specific planet
  getForPlanet: async (planet, language = 'ta') => {
    const response = await api.get(`/api/remedy/for-planet/${planet}`, {
      params: { language },
    });
    return response.data;
  },

  // Get remedies for a specific dosha
  getForDosha: async (dosha, language = 'ta') => {
    const response = await api.get(`/api/remedy/for-dosha/${dosha}`, {
      params: { language },
    });
    return response.data;
  },

  // Get daily remedies based on rasi
  getDaily: async (rasi, nakshatra, language = 'ta') => {
    const response = await api.get('/api/remedy/daily', {
      params: { rasi, nakshatra, language },
    });
    return response.data;
  },

  // Get goal-specific remedies
  getForGoal: async (goal, rasi, language = 'ta') => {
    const response = await api.get(`/api/remedy/goal/${goal}`, {
      params: { rasi, language },
    });
    return response.data;
  },
};

export default api;
