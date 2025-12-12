# Jothida AI - Tamil Astrology App

## Feature Documentation

### Overview
Jothida AI is a comprehensive Tamil astrology mobile application built with React Native (Expo) and FastAPI backend. The app provides personalized astrological insights, predictions, and guidance based on Vedic astrology principles.

---

## 1. Authentication System

### Phone OTP Login
- **OTP-based authentication** using Indian phone numbers (+91XXXXXXXXXX)
- 6-digit OTP with 5-minute expiry
- Maximum 3 attempts per OTP
- Demo mode returns OTP in API response for testing
- JWT token-based session management (30-day expiry)

### User Registration
- Name, gender, birth details collection
- Automatic Rasi (Moon Sign) and Nakshatra calculation
- Birth place with coordinates lookup
- Profile stored with computed astrology data

---

## 2. Dashboard Screen

### Header Section
- App branding with Om symbol (ॐ)
- User greeting with name
- Current Rasi and Nakshatra display
- Real-time clock
- Current period indicator (Rahu Kalam, Good Time, Normal Time)

### Today's Panchangam Card
- Tamil month display
- Tithi (lunar day)
- Nakshatra (star)
- Yoga

### Today's Overall Score
- Animated score circle (tappable)
- Score out of 100 with progress indicator
- Good/Average/Caution badge
- Tap to see detailed score breakdown with:
  - Factor-wise analysis
  - Positive/negative influences
  - Personalized suggestions

### Life Areas Section
Four animated cards showing scores for:
1. **Love (காதல்)** - Venus-based analysis
2. **Career (தொழில்)** - Sun and 10th house analysis
3. **Education (கல்வி)** - Mercury and Jupiter analysis
4. **Family (குடும்பம்)** - Moon and 4th house analysis

Each card includes:
- Animated progress bar
- Good/Average/Caution indicator
- Tap for detailed modal with:
  - Planet-wise factor breakdown
  - Score justification
  - Remedies and suggestions

### Future Projection Section
Toggle between two views:

#### Monthly View
- Next 12 months forecast
- Horizontal scrollable cards
- Score for each month
- Tap for detailed monthly analysis

#### 3-Year Projection
- Current year, next year, and third year
- Unique comprehensive data for each year:
  - Different scores (68%, 78%, 85%)
  - Unique planetary factors
  - Year-specific opportunities (positives)
  - Year-specific remedies
  - Detailed suggestions

### Quick Actions
- AI Question - Navigate to Chat
- Matching - Navigate to Compatibility
- Muhurtham - Navigate to Auspicious Times

### Current Dasha Display
- Maha Dasha (major period)
- Antar Dasha (sub-period)
- Planet names in Tamil

---

## 3. Muhurtham Screen (Auspicious Times)

### Event Type Selector
Six categories with icons:
- திருமணம் (Marriage) 💒
- கிரக பிரவேசம் (Housewarming) 🏠
- வாகனம் (Vehicle) 🚗
- தொழில் (Business) 💼
- பயணம் (Travel) ✈️
- பொது (General) 📅

### Interactive Calendar
- Monthly calendar view
- Color-coded dates:
  - Green: Good days
  - Yellow: Normal days
  - Red: Days to avoid
- Event dot indicator for selected event type
- Navigation between months
- Animated cell interactions

### Selected Date Details
- Date display in Tamil format
- Day quality assessment
- Best time slots for selected event
- AI-powered recommendations

### Legend
- Visual guide for calendar colors

---

## 4. Matching Screen (Compatibility)

### Person Input Forms
Two forms for:
- Person 1 details
- Person 2 details

Each form collects:
- Name
- Birth Date (date picker)
- Birth Time (time picker)
- Birth Place (with coordinate lookup)

### Compatibility Analysis
- 10 Porutham (compatibility aspects) calculation
- Overall compatibility score
- Detailed breakdown of each Porutham
- Recommendations

---

## 5. Chat Screen (AI Astrology Assistant)

### Features
- Real-time AI chat interface
- Context-aware responses using user's:
  - Rasi
  - Nakshatra
  - Birth date
- Message copy functionality
- Clear chat option
- Typing indicator

### Chat Capabilities
- Answer astrology questions
- Provide personalized predictions
- Explain planetary influences
- Suggest remedies

---

## 6. Profile Screen

### User Information Display
- Name with avatar
- Phone number
- Rasi and Nakshatra badges
- Birth details

### Birth Chart (Jathagam)
- South Indian style chart
- 12 houses with planet positions
- Planet abbreviations in boxes
- Lagna (Ascendant) indicator

### Dasha Timeline
- Visual timeline of planetary periods
- Current Maha Dasha highlighted
- Antar Dasha display
- Period durations

### Planet Positions Table
- All 9 planets (Navagraha)
- House positions
- Degree positions
- Retrograde indicators

### PDF Report Generation
- Comprehensive jathagam report
- Downloadable/shareable PDF
- Includes all chart details

### Language Selector
- Tamil (தமிழ்) - Default
- Kannada (ಕನ್ನಡ)
- English

### Logout
- Secure logout with confirmation

---

## 7. Multi-Language Support

### Supported Languages
1. **Tamil (ta)** - Default language
2. **Kannada (kn)** - Full translation
3. **English (en)** - Full translation

### Translated Elements
- Navigation labels
- All UI text
- Dashboard content
- Life area names
- Panchangam labels
- Score descriptions
- Button labels
- Modal content
- Planet names
- Day and month names

### Language Persistence
- Selection saved to AsyncStorage
- Persists across app restarts
- Instant language switching

---

## 8. Backend API Features

### Endpoints

#### Authentication (`/api/mobile/`)
- `POST /send-otp` - Send OTP to phone
- `POST /verify-otp` - Verify OTP
- `POST /register` - Register new user
- `GET /me` - Get current user

#### Panchangam (`/api/panchangam/`)
- `GET /today` - Today's panchangam data

#### Jathagam (`/api/jathagam/`)
- `POST /generate` - Generate birth chart

#### Matching (`/api/matching/`)
- `POST /calculate` - Calculate compatibility

#### Chat (`/api/chat/`)
- `POST /message` - Send chat message

#### Muhurtham (`/api/muhurtham/`)
- `GET /calendar` - Monthly calendar data
- `GET /day-details/{date}` - Specific day details

#### Forecast (`/api/forecast/`)
- `GET /user` - User-specific forecast

---

## 9. Technical Features

### Frontend (React Native/Expo)
- Expo SDK 54
- React Navigation (Bottom Tabs + Stack)
- React Native Animated API
- Linear Gradient backgrounds
- Safe Area handling
- Secure token storage
- Axios for API calls

### Backend (FastAPI)
- Python FastAPI framework
- SQLite database
- Swiss Ephemeris for calculations
- JWT authentication
- Pydantic models

### Animations
- Fade-in cards with delays
- Scale animations on press
- Progress bar animations
- Pulsing sparkle effects
- Slide-up modals

### UI/UX
- Orange/saffron theme (Hindu auspicious color)
- Card-based design
- Consistent border radius (12-16px)
- Shadow effects
- Responsive layout

---

## 10. Data Models

### User
- UUID, name, phone, email
- Gender, verification status
- Last login tracking

### AstroProfile
- Birth date, time, place
- Coordinates (lat/lon)
- Rasi, Nakshatra (English + Tamil)
- Nakshatra Pada
- Current Maha/Antar Dasha

### OTPVerification
- Phone number
- OTP code
- Expiry time
- Attempt tracking
- Verification status

---

## 11. City Coordinates

Pre-configured Tamil Nadu cities:
- Chennai, Coimbatore, Madurai
- Tiruchirappalli, Salem, Tirunelveli
- Tiruppur, Erode, Vellore
- Thoothukudi, Dindigul, Thanjavur

Both English and Tamil city names supported.

---

## 12. Build & Deployment

### Mobile App
- EAS Build for Android APK
- Preview profile for testing
- Production profile for release

### Backend
- Uvicorn server
- Hot reload for development
- Render.yaml for cloud deployment

---

## Version History

### Current Version
- Multi-language support (Tamil, Kannada, English)
- Enhanced 3-year predictions with unique data
- Fixed calendar date display
- Fixed life area card layout
- Language switcher in Profile

---

## Future Enhancements (Planned)
- Push notifications for daily predictions
- Horoscope matching history
- Favorite muhurtham dates
- Voice-based queries
- More regional languages
- Premium features
