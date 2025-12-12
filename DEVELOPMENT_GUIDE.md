# Jothida AI - Development Guide & Logic Documentation

## Overview

This document explains the **logic, reasoning, and approach** behind each feature in the Jothida AI Tamil Astrology app. It's written in a human-readable way to help developers understand not just *what* was built, but *why* and *how*.

---

## 1. Authentication System

### The Problem
Users need a simple, secure way to sign in without remembering passwords. Most Indian users are comfortable with OTP-based phone authentication (like WhatsApp, Paytm, etc.).

### Our Solution
```
User enters phone → Backend generates 6-digit OTP → OTP sent (demo: returned in response)
→ User enters OTP → Backend verifies → If new user: Registration flow
                                      → If existing user: Return JWT token
```

### Logic Applied

#### Why Phone OTP instead of Email/Password?
1. **User familiarity** - Indian users use OTP daily (UPI, banking apps)
2. **No password to remember** - Reduces friction
3. **Phone verification** - Ensures real users
4. **Quick onboarding** - 30 seconds to sign in

#### OTP Security Logic
```python
# Generate random 6 digits
otp = ''.join(random.choices(string.digits, k=6))

# Store with expiry (5 minutes)
expires_at = datetime.utcnow() + timedelta(minutes=5)

# Limit attempts to prevent brute force
max_attempts = 3
```

#### Why 5-minute expiry?
- **Too short (1-2 min)**: User might not receive SMS in time
- **Too long (30 min)**: Security risk if phone is compromised
- **5 minutes**: Sweet spot - enough time, still secure

#### JWT Token Logic
```python
# Token valid for 30 days - balance between security and convenience
expire = datetime.utcnow() + timedelta(days=30)

# Payload contains user ID and phone for verification
payload = {"sub": user_id, "phone": phone, "exp": expire}
```

---

## 2. Dashboard - The Heart of the App

### The Problem
Users want to see "What does today look like for me?" at a glance, without navigating multiple screens.

### Our Solution
A single scrollable dashboard with:
- Today's summary at the top
- Detailed breakdowns below
- Quick actions for common tasks

### Logic Applied

#### Score Calculation Philosophy
We don't use random numbers. Each score is based on astrological factors:

```javascript
// Overall score is weighted average of life areas
overallScore = (loveScore * 0.25) + (careerScore * 0.30) +
               (educationScore * 0.20) + (familyScore * 0.25)

// Each life area score = sum of planetary factors
loveScore = venusStrength + moonAspect - saturnAspect
// Example: 25 + 15 - 12 = 78
```

#### Why These 4 Life Areas?
Based on traditional Vedic astrology houses:
1. **Love** → 7th house (partnerships, Venus)
2. **Career** → 10th house (profession, Sun)
3. **Education** → 5th house (learning, Mercury)
4. **Family** → 4th house (home, Moon)

These cover 80% of what users care about daily.

#### Time Period Logic
```javascript
const getCurrentPeriod = () => {
  const hour = currentTime.getHours();

  // Rahu Kalam varies by day, simplified to afternoon
  if (hour >= 15 && hour < 17) return 'ராகு காலம்'; // Inauspicious

  // Morning hours generally good
  if (hour >= 9 && hour < 11) return 'நல்ல நேரம்'; // Good time

  return 'சாதாரண நேரம்'; // Normal time
};
```

#### Animation Strategy
```javascript
// Cards appear with staggered delays for visual flow
<AnimatedCard delay={0}>Header</AnimatedCard>
<AnimatedCard delay={100}>Panchangam</AnimatedCard>
<AnimatedCard delay={200}>Score</AnimatedCard>
<AnimatedCard delay={300}>Life Areas</AnimatedCard>

// Each card fades in and slides up
Animated.parallel([
  Animated.timing(fadeAnim, { toValue: 1, duration: 500 }),
  Animated.timing(translateY, { toValue: 0, duration: 500 })
])
```

**Why staggered?** Creates a "cascading" effect that:
1. Draws user's eye down the page
2. Feels more polished than everything appearing at once
3. Gives time for data to load progressively

---

## 3. Three-Year Prediction System

### The Problem
Users want to know not just today, but their future. "Will next year be better?" is a common question.

### Our Solution
Comprehensive 3-year forecast with unique, detailed data for each year.

### Logic Applied

#### Year Score Progression
```javascript
// Designed to show realistic life progression
2025: 68% (Current - challenges exist)
2026: 78% (Improvement - Jupiter transit helps)
2027: 85% (Best year - multiple positive factors)
```

**Why ascending scores?**
1. **Psychological boost** - Gives hope for the future
2. **Astrologically realistic** - Jupiter's 12-year cycle brings good periods
3. **Motivational** - Encourages users to work through current challenges

#### Unique Data Per Year
Each year has completely different:

```javascript
// 2025 - Current challenges
factors: [
  { name: 'குரு மேஷத்தில்', positive: true },  // Jupiter positive
  { name: 'சனி கும்பத்தில்', positive: false }, // Saturn negative
]
positives: ['தொழில் வாய்ப்புகள்', 'கல்வி உயர்வு']
remedies: ['சனிக்கிழமை ஹனுமான் வழிபாடு']

// 2026 - Improvement year
factors: [
  { name: 'குரு ரிஷபத்தில்', positive: true },
  { name: 'சனி பெயர்ச்சி', positive: true }, // Saturn moves!
]
positives: ['பண வரவு அதிகம்', 'சொத்து வாங்கலாம்', 'வெளிநாடு வாய்ப்பு']

// 2027 - Best year
factors: [
  { name: 'குரு மிதுனத்தில்', positive: true },
  { name: 'சனி மீனத்தில்', positive: true },
  { name: 'ராகு மகரத்தில்', positive: true },
  { name: 'கேது கடகத்தில்', positive: true }, // All positive!
]
```

#### Why Include Remedies?
1. **Actionable advice** - Users can do something about it
2. **Traditional expectation** - Astrology users expect remedies
3. **Engagement** - Gives reason to return to app

---

## 4. Muhurtham Calendar

### The Problem
Users planning events (wedding, housewarming, travel) need to know which dates are auspicious.

### Our Solution
Visual calendar with color-coded dates and time slots.

### Logic Applied

#### Date Quality Calculation
```javascript
const getDateQuality = (date, eventType) => {
  // Check multiple factors
  const dayOfWeek = date.getDay();
  const tithi = calculateTithi(date);
  const nakshatra = calculateNakshatra(date);

  // Each event type has preferred days
  const eventPreferences = {
    'marriage': { goodDays: [1, 4, 5], avoidDays: [2, 6] }, // Mon, Thu, Fri good
    'travel': { goodDays: [1, 3, 5], avoidDays: [2, 6] },
    'business': { goodDays: [3, 4, 5], avoidDays: [2, 6] },
  };

  // Combine factors for final score
  let score = 50; // Base
  if (eventPreferences[eventType].goodDays.includes(dayOfWeek)) score += 30;
  if (goodTithis.includes(tithi)) score += 20;
  if (goodNakshatras.includes(nakshatra)) score += 20;

  return score >= 75 ? 'good' : score >= 50 ? 'normal' : 'avoid';
};
```

#### Calendar Color Logic
```javascript
// Green: Safe to proceed
// Yellow: Okay, but check time slots
// Red: Avoid if possible

const colors = {
  good: { bg: '#dcfce7', border: '#16a34a', text: '#15803d' },
  normal: { bg: '#fef3c7', border: '#d97706', text: '#92400e' },
  avoid: { bg: '#fef2f2', border: '#dc2626', text: '#dc2626' }
};
```

#### Why Fixed Height Cells (not aspectRatio)?
```css
/* Problem: aspectRatio: 1 caused issues on some devices */
/* Solution: Fixed height with percentage width */
calendarCellWrapper: {
  width: '14.28%',  /* 100/7 days */
  height: 44,       /* Fixed, works everywhere */
  padding: 2,
}
```

---

## 5. Life Area Cards - UI Fix

### The Problem
Text was displaying vertically ("க-ா-த-ல்") instead of horizontally ("காதல்").

### Root Cause Analysis
```javascript
// WRONG: Cards were too narrow, text wrapped character by character
lifeAreaCard: {
  width: '48%',  // Left too little space
  flexDirection: 'column',
}

// Badge had no flex direction
lifeAreaBadge: {
  // Missing flexDirection caused vertical stacking
}
```

### Our Fix
```javascript
// CORRECT: Calculate exact width accounting for gaps
lifeAreaCard: {
  width: (screenWidth - 32 - 12) / 2,
  // 32 = horizontal margins (16 * 2)
  // 12 = gap between cards
  // /2 = two cards per row
}

// Badge needs horizontal layout
lifeAreaBadge: {
  flexDirection: 'row',  // Force horizontal
  paddingHorizontal: 6,
  paddingVertical: 2,
}
```

---

## 6. Multi-Language System

### The Problem
App started in Tamil only, but users in Karnataka and other states need their language.

### Our Solution
React Context-based language system with full translations.

### Logic Applied

#### Context Structure
```javascript
// LanguageContext.js
const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState('ta'); // Default Tamil

  // Persist to storage
  useEffect(() => {
    AsyncStorage.getItem('appLanguage').then(saved => {
      if (saved) setLanguage(saved);
    });
  }, []);

  // Translation function
  const t = (key) => {
    return translations[language]?.[key]
        || translations['en']?.[key]  // Fallback to English
        || key;  // Fallback to key itself
  };

  return (
    <LanguageContext.Provider value={{ language, t, changeLanguage }}>
      {children}
    </LanguageContext.Provider>
  );
};
```

#### Translation Organization
```javascript
const translations = {
  ta: {  // Tamil
    home: 'முகப்பு',
    love: 'காதல்',
    career: 'தொழில்',
    // ... 150+ keys
  },
  kn: {  // Kannada
    home: 'ಮುಖಪುಟ',
    love: 'ಪ್ರೀತಿ',
    career: 'ವೃತ್ತಿ',
    // ... 150+ keys
  },
  en: {  // English
    home: 'Home',
    love: 'Love',
    career: 'Career',
    // ... 150+ keys
  }
};
```

#### Why Context Instead of i18n Library?
1. **Simpler** - No extra dependencies
2. **Full control** - Can add custom functions (formatDate, getMonthName)
3. **Smaller bundle** - No library overhead
4. **Sufficient** - App has ~150 strings, not thousands

#### Dynamic Content Translation
```javascript
// Static labels use t() function
<Text>{t('todayScore')}</Text>

// Dynamic content needs conditional logic
const getLifeAreas = () => [
  {
    name: t('love'),  // Uses translation
    factors: [
      {
        name: `${t('venus')} ${language === 'en' ? 'strength' : 'பலம்'}`,
        description: language === 'en'
          ? 'Venus is well placed in 7th house'
          : language === 'kn'
            ? 'ಶುಕ್ರ 7ನೇ ಮನೆಯಲ್ಲಿ ಉತ್ತಮ ಸ್ಥಿತಿಯಲ್ಲಿದ್ದಾರೆ'
            : 'சுக்கிரன் 7ம் வீட்டில் நல்ல நிலையில் உள்ளார்'
      }
    ]
  }
];
```

---

## 7. Score Modal - Detailed Breakdown

### The Problem
Users see a score (72/100) but want to know "Why this score?"

### Our Solution
Tappable scores that open detailed modal with factor breakdown.

### Logic Applied

#### Modal Content Structure
```javascript
const ScoreJustificationModal = ({ data }) => (
  <Modal>
    {/* Header with icon and title */}
    <Header icon={data.icon} title={data.title} />

    {/* Large score display */}
    <ScoreDisplay score={data.score} />

    {/* Factors - What contributed to score */}
    <Section title="மதிப்பெண் விளக்கம்">
      {data.factors.map(factor => (
        <FactorItem
          name={factor.name}
          value={factor.value}
          positive={factor.positive}
          description={factor.description}
        />
      ))}
    </Section>

    {/* Positives - Opportunities */}
    <Section title="நல்ல வாய்ப்புகள்">
      {data.positives?.map(positive => (
        <PositiveItem
          icon={positive.icon}
          title={positive.title}
          description={positive.description}
        />
      ))}
    </Section>

    {/* Remedies - Actions user can take */}
    <Section title="பரிகாரங்கள்">
      {data.remedies?.map(remedy => (
        <RemedyItem text={remedy} />
      ))}
    </Section>

    {/* Suggestion - Summary advice */}
    <SuggestionBox text={data.suggestion} />
  </Modal>
);
```

#### Factor Display Logic
```javascript
// Positive factors shown in green with + icon
// Negative factors shown in red with - icon
<Ionicons
  name={factor.positive ? 'add-circle' : 'remove-circle'}
  color={factor.positive ? '#16a34a' : '#dc2626'}
/>
<Text>{factor.positive ? '+' : ''}{factor.value}</Text>
```

---

## 8. Bottom Tab Navigation with Translations

### The Problem
Tab labels were hardcoded in Tamil. Need to change with language.

### Our Solution
Dynamic tab labels using translation context.

### Logic Applied

```javascript
// MainNavigator.js
export default function MainNavigator() {
  const { t } = useLanguage();  // Get translation function

  return (
    <Tab.Navigator>
      <Tab.Screen
        name="Dashboard"
        component={DashboardScreen}
        options={{ tabBarLabel: t('home') }}  // Dynamic!
      />
      <Tab.Screen
        name="Matching"
        options={{ tabBarLabel: t('matching') }}
      />
      {/* ... other screens */}
    </Tab.Navigator>
  );
}
```

**Key insight**: When language changes in context, the navigator re-renders and tab labels update automatically.

---

## 9. API Architecture

### The Problem
Mobile app needs to communicate with backend for:
- Authentication
- Astrology calculations
- Data persistence

### Our Solution
RESTful API with axios client and token interceptor.

### Logic Applied

#### Axios Interceptor for Auth
```javascript
api.interceptors.request.use(async (config) => {
  // Get token from secure storage
  const token = await SecureStore.getItemAsync('authToken');

  // Add to every request automatically
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});
```

**Why interceptor?**
- Don't need to add token manually to every request
- Centralized auth handling
- Easy to add refresh token logic later

#### City Coordinates Lookup
```javascript
// Pre-defined coordinates for Tamil Nadu cities
const CITY_COORDINATES = {
  'Chennai': { lat: 13.0827, lon: 80.2707 },
  'சென்னை': { lat: 13.0827, lon: 80.2707 },  // Tamil name too!
  // ... more cities
};

// Used in API calls
const coords = getCityCoordinates(birthPlace);
api.post('/api/jathagam/generate', {
  ...birthDetails,
  latitude: coords.lat,
  longitude: coords.lon
});
```

**Why hardcode coordinates?**
1. **Faster** - No geocoding API call needed
2. **Reliable** - No dependency on external service
3. **Offline** - Works without internet for coordinate lookup
4. **Sufficient** - Covers major Tamil Nadu cities

---

## 10. Animation System

### The Problem
Static UI feels lifeless and cheap. Need polish without complexity.

### Our Solution
React Native Animated API with reusable components.

### Logic Applied

#### Reusable AnimatedCard
```javascript
const AnimatedCard = ({ children, delay = 0, style }) => {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const translateY = useRef(new Animated.Value(30)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 500,
        delay,  // Staggered appearance
        useNativeDriver: true,
      }),
      Animated.timing(translateY, {
        toValue: 0,
        duration: 500,
        delay,
        easing: Easing.out(Easing.back(1.2)),  // Slight overshoot
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  return (
    <Animated.View style={[style, { opacity: fadeAnim, transform: [{ translateY }] }]}>
      {children}
    </Animated.View>
  );
};
```

#### Why `useNativeDriver: true`?
- Animations run on UI thread, not JS thread
- 60fps even on low-end devices
- No jank or stuttering

#### Press Animations
```javascript
const handlePressIn = () => {
  Animated.spring(scaleAnim, {
    toValue: 0.95,  // Slight shrink
    useNativeDriver: true
  }).start();
};

const handlePressOut = () => {
  Animated.spring(scaleAnim, {
    toValue: 1,
    friction: 3,  // Bouncy return
    useNativeDriver: true
  }).start();
};
```

---

## 11. Error Handling Strategy

### App-Level Error Boundary
```javascript
class ErrorBoundary extends React.Component {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('App Error:', error, errorInfo);
    // Could send to crash reporting service
  }

  render() {
    if (this.state.hasError) {
      return <ErrorScreen message={this.state.error?.message} />;
    }
    return this.props.children;
  }
}
```

### API Error Handling
```javascript
// Graceful degradation - show fallback data
const getPanchangam = async () => {
  try {
    const response = await api.get('/api/panchangam/today');
    return response.data;
  } catch (error) {
    console.error('Panchangam API error:', error);
    return null;  // UI shows default values
  }
};
```

---

## Summary

### Design Principles Applied

1. **User-First**: Every feature answers "What does the user want to know?"
2. **Progressive Disclosure**: Show summary first, details on tap
3. **Graceful Degradation**: App works even if API fails
4. **Performance**: Native driver animations, efficient re-renders
5. **Accessibility**: Multiple languages, clear visual hierarchy
6. **Trust**: Show reasoning behind predictions (factors, not just numbers)

### Technical Decisions

| Decision | Reason |
|----------|--------|
| React Native + Expo | Cross-platform, fast development |
| FastAPI | Python ecosystem for astro calculations |
| SQLite | Simple, no server needed for dev |
| JWT Auth | Stateless, mobile-friendly |
| Context for i18n | Simpler than libraries for our scale |
| Hardcoded coordinates | Faster, more reliable |

---

## Files Reference

```
mobile/
├── App.js                           # Entry point with providers
├── src/
│   ├── context/
│   │   ├── AuthContext.js          # Authentication state
│   │   └── LanguageContext.js      # Multi-language support
│   ├── navigation/
│   │   ├── RootNavigator.js        # Auth flow routing
│   │   ├── AuthNavigator.js        # Login/Register stack
│   │   └── MainNavigator.js        # Bottom tabs
│   ├── screens/
│   │   ├── DashboardScreen.js      # Main dashboard
│   │   ├── MuhurthamScreen.js      # Auspicious times
│   │   ├── MatchingScreen.js       # Compatibility
│   │   ├── ChatScreen.js           # AI assistant
│   │   ├── ProfileScreen.js        # User profile
│   │   ├── LoginScreen.js          # OTP login
│   │   └── RegisterScreen.js       # New user registration
│   └── services/
│       ├── api.js                  # API client
│       └── reportGenerator.js      # PDF generation

backend/
├── app/
│   ├── main.py                     # FastAPI entry
│   ├── routers/
│   │   ├── mobile_auth.py          # OTP authentication
│   │   ├── jathagam.py             # Birth chart
│   │   ├── panchangam.py           # Daily almanac
│   │   ├── matching.py             # Compatibility
│   │   └── chat.py                 # AI chat
│   ├── models/
│   │   └── user.py                 # Database models
│   └── services/
│       └── jathagam_generator.py   # Astro calculations
```
