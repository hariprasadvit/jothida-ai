# Jothida AI - React Native Mobile App

Tamil Astrology (Jothidam) mobile application built with Expo and React Native.

## Prerequisites

1. **Node.js** (v18 or higher)
2. **npm** or **yarn**
3. **Expo CLI**: `npm install -g expo-cli`
4. **EAS CLI** (for building APK): `npm install -g eas-cli`
5. **Expo Go app** on your phone (for development testing)

## Project Structure

```
mobile/
├── App.js                    # Main entry point
├── app.json                  # Expo configuration
├── eas.json                  # EAS Build configuration
├── package.json              # Dependencies
├── babel.config.js           # Babel configuration
├── assets/                   # App icons and splash
└── src/
    ├── context/
    │   └── AuthContext.js    # Authentication state
    ├── navigation/
    │   ├── RootNavigator.js  # Root navigator
    │   ├── AuthNavigator.js  # Auth stack (Login/Register)
    │   └── MainNavigator.js  # Main tabs
    ├── screens/
    │   ├── LoginScreen.js    # OTP Login
    │   ├── RegisterScreen.js # New user registration
    │   ├── DashboardScreen.js
    │   ├── ProfileScreen.js  # With Rasi chart
    │   ├── MatchingScreen.js # 10 Porutham matching
    │   ├── ChatScreen.js     # AI chat
    │   └── MuhurthamScreen.js
    └── services/
        └── api.js            # API services
```

## Setup & Installation

### 1. Install dependencies

```bash
cd mobile
npm install
```

### 2. Configure API URL

Edit `src/services/api.js` and update the `API_BASE_URL`:

```javascript
// For Android Emulator:
const API_BASE_URL = 'http://10.0.2.2:8000';

// For iOS Simulator:
const API_BASE_URL = 'http://localhost:8000';

// For Physical Device (use your computer's IP):
const API_BASE_URL = 'http://192.168.x.x:8000';
```

To find your computer's IP:
- **Mac**: `ifconfig | grep "inet " | grep -v 127.0.0.1`
- **Windows**: `ipconfig`
- **Linux**: `ip addr show`

### 3. Start the backend server

Make sure your backend is running on port 8000:

```bash
cd ../backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Running the App

### Development Mode (with Expo Go)

```bash
cd mobile
npm start
```

This will start Expo Dev Server. Then:
- **Android**: Scan QR code with Expo Go app
- **iOS**: Scan QR code with Camera app (opens Expo Go)
- **Web**: Press `w` to open in browser

### Android Emulator

```bash
npm run android
```

### iOS Simulator (Mac only)

```bash
npm run ios
```

## Building APK for Android

### Option 1: EAS Build (Recommended - Cloud Build)

1. **Login to Expo**:
```bash
eas login
```

2. **Configure EAS project**:
```bash
eas build:configure
```

3. **Build Preview APK** (for testing):
```bash
npm run build:android
# or
eas build -p android --profile preview
```

4. **Build Production APK**:
```bash
npm run build:apk
# or
eas build -p android --profile production
```

The build will be uploaded to Expo's servers. You'll get a download link when complete.

### Option 2: Local Build (Requires Android SDK)

1. **Install Java JDK 17**
2. **Install Android SDK**
3. **Run**:
```bash
npx expo prebuild
cd android
./gradlew assembleRelease
```

APK will be at: `android/app/build/outputs/apk/release/app-release.apk`

## App Features

### 1. OTP Login (LoginScreen)
- Phone number authentication with OTP
- Demo mode shows OTP in response

### 2. Dashboard (DashboardScreen)
- Today's Panchangam (Tamil calendar)
- Overall score and AI insights
- Life areas (Love, Career, Education, Family)
- Quick actions

### 3. Profile (ProfileScreen)
- User details with birth info
- South Indian style Rasi chart (4x4 grid)
- Planet positions table
- Dasha/Bukti information
- Logout functionality

### 4. Matching (MatchingScreen)
- 10 Porutham marriage compatibility
- Detailed breakdown of each Porutham
- AI verdict and remedies

### 5. Chat (ChatScreen)
- AI-powered Tamil astrology assistant
- Quick questions
- Time slots and forecast data

### 6. Muhurtham (MuhurthamScreen)
- Auspicious time finder
- Calendar view with good/bad days
- Event type selection
- Detailed time slots

## Troubleshooting

### "Network Error" or API not connecting
1. Make sure backend is running
2. Check `API_BASE_URL` in `src/services/api.js`
3. For physical device, use your computer's local IP
4. Ensure phone and computer are on same WiFi network

### "Module not found" errors
```bash
rm -rf node_modules
npm install
```

### Expo cache issues
```bash
npx expo start -c
```

### Build failures
```bash
eas build --clear-cache -p android --profile preview
```

## Environment Variables

Create `.env` file for environment-specific config:

```env
API_URL=http://192.168.1.100:8000
```

## Icons and Splash Screen

Place your assets in `/assets`:
- `icon.png` - 1024x1024px app icon
- `splash.png` - 1284x2778px splash screen
- `adaptive-icon.png` - 1024x1024px Android adaptive icon

## Publishing to Play Store

1. Create keystore:
```bash
keytool -genkeypair -v -storetype PKCS12 -keystore jothida-ai.keystore -alias jothida-ai -keyalg RSA -keysize 2048 -validity 10000
```

2. Configure in `eas.json` under production profile

3. Build AAB:
```bash
eas build -p android --profile production
```

4. Upload to Google Play Console

## License

Private - Jothida AI
