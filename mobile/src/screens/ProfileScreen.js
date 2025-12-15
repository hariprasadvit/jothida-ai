import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
  Dimensions,
  Platform,
  Animated,
  Easing,
  Modal,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import * as Print from 'expo-print';
import * as Sharing from 'expo-sharing';
import { useAuth } from '../context/AuthContext';
import { useLanguage, languageOptions } from '../context/LanguageContext';
import { mobileAPI, reportAPI } from '../services/api';
import { generateComprehensivePDFHTML } from '../services/reportGenerator';
import * as FileSystem from 'expo-file-system';

// Tamil to translation key mappings for ProfileScreen
const TAMIL_PLANET_MAP = {
  'சூரியன்': 'sun_planet', 'சந்திரன்': 'moon_planet', 'செவ்வாய்': 'mars',
  'புதன்': 'mercury', 'குரு': 'jupiter', 'சுக்கிரன்': 'venus',
  'சனி': 'saturn', 'ராகு': 'rahu', 'கேது': 'ketu',
};

const ENGLISH_PLANET_MAP = {
  'Sun': 'sun_planet', 'Moon': 'moon_planet', 'Mars': 'mars',
  'Mercury': 'mercury', 'Jupiter': 'jupiter', 'Venus': 'venus',
  'Saturn': 'saturn', 'Rahu': 'rahu', 'Ketu': 'ketu',
};

const TAMIL_RASI_MAP = {
  'மேஷம்': 'aries', 'ரிஷபம்': 'taurus', 'மிதுனம்': 'gemini',
  'கடகம்': 'cancer', 'சிம்மம்': 'leo', 'கன்னி': 'virgo',
  'துலாம்': 'libra', 'விருச்சிகம்': 'scorpio', 'தனுசு': 'sagittarius',
  'மகரம்': 'capricorn', 'கும்பம்': 'aquarius', 'மீனம்': 'pisces',
};

const ENGLISH_RASI_MAP = {
  'Aries': 'aries', 'Taurus': 'taurus', 'Gemini': 'gemini',
  'Cancer': 'cancer', 'Leo': 'leo', 'Virgo': 'virgo',
  'Libra': 'libra', 'Scorpio': 'scorpio', 'Sagittarius': 'sagittarius',
  'Capricorn': 'capricorn', 'Aquarius': 'aquarius', 'Pisces': 'pisces',
};

const TAMIL_NAKSHATRA_MAP = {
  'அஸ்வினி': 'ashwini', 'பரணி': 'bharani', 'கார்த்திகை': 'krittika',
  'ரோகிணி': 'rohini', 'மிருகசீரிடம்': 'mrigashira', 'திருவாதிரை': 'ardra',
  'புனர்பூசம்': 'punarvasu', 'பூசம்': 'pushya', 'ஆயில்யம்': 'ashlesha',
  'மகம்': 'magha', 'பூரம்': 'purvaPhalguni', 'உத்திரம்': 'uttaraPhalguni',
  'ஹஸ்தம்': 'hasta', 'சித்திரை': 'chitra', 'சுவாதி': 'swati',
  'விசாகம்': 'vishakha', 'அனுஷம்': 'anuradha', 'கேட்டை': 'jyeshtha',
  'மூலம்': 'moola', 'பூராடம்': 'purvaAshadha', 'உத்திராடம்': 'uttaraAshadha',
  'திருவோணம்': 'shravana', 'அவிட்டம்': 'dhanishta', 'சதயம்': 'shatabhisha',
  'பூரட்டாதி': 'purvaBhadrapada', 'உத்திரட்டாதி': 'uttaraBhadrapada', 'ரேவதி': 'revati',
};

// Yoga effect translations (Tamil to English)
const YOGA_EFFECT_ENGLISH = {
  'புகழ், செல்வம், நல்ல பேச்சு திறன்': 'Fame, wealth, and good speaking skills',
  'நல்ல புத்திசாலித்தனம், தொழிலில் வெற்றி': 'Good intelligence, success in business',
  'செல்வம், துணிச்சல், தொழில் வெற்றி': 'Wealth, courage, and business success',
  'ஆன்மீக சிந்தனை, கல்வி, நல்ல குணம்': 'Spiritual thinking, education, good character',
  'செல்வம், அழகு, இல்லற சுகம்': 'Wealth, beauty, and domestic happiness',
  'சராசரி வாழ்க்கை': 'Average life',
  'குரு சந்திரனிலிருந்து கேந்திரத்தில் உள்ளார்': 'Jupiter is in kendra from Moon',
  'சூரியனும் புதனும் ஒரே ராசியில்': 'Sun and Mercury are in the same sign',
  'சந்திரனும் செவ்வாயும் சேர்க்கை': 'Moon and Mars conjunction',
  'குரு கேந்திரத்தில் பலமாக உள்ளார்': 'Jupiter is strong in kendra',
  'சுக்கிரன் சுபஸ்தானத்தில் பலமாக': 'Venus is strong in auspicious house',
  'பெரிய யோகங்கள் இல்லை': 'No major yogas present',
};

// Yoga effect translations (Tamil to Kannada)
const YOGA_EFFECT_KANNADA = {
  'புகழ், செல்வம், நல்ல பேச்சு திறன்': 'ಖ್ಯಾತಿ, ಸಂಪತ್ತು ಮತ್ತು ಉತ್ತಮ ಮಾತನಾಡುವ ಕೌಶಲ್ಯ',
  'நல்ல புத்திசாலித்தனம், தொழிலில் வெற்றி': 'ಉತ್ತಮ ಬುದ್ಧಿವಂತಿಕೆ, ವ್ಯಾಪಾರದಲ್ಲಿ ಯಶಸ್ಸು',
  'செல்வம், துணிச்சல், தொழில் வெற்றி': 'ಸಂಪತ್ತು, ಧೈರ್ಯ ಮತ್ತು ವ್ಯಾಪಾರ ಯಶಸ್ಸು',
  'ஆன்மீக சிந்தனை, கல்வி, நல்ல குணம்': 'ಆಧ್ಯಾತ್ಮಿಕ ಚಿಂತನೆ, ಶಿಕ್ಷಣ, ಉತ್ತಮ ಗುಣ',
  'செல்வம், அழகு, இல்லற சுகம்': 'ಸಂಪತ್ತು, ಸೌಂದರ್ಯ ಮತ್ತು ಗೃಹ ಸುಖ',
  'சராசரி வாழ்க்கை': 'ಸರಾಸರಿ ಜೀವನ',
  'குரு சந்திரனிலிருந்து கேந்திரத்தில் உள்ளார்': 'ಗುರು ಚಂದ್ರನಿಂದ ಕೇಂದ್ರದಲ್ಲಿದ್ದಾರೆ',
  'சூரியனும் புதனும் ஒரே ராசியில்': 'ಸೂರ್ಯ ಮತ್ತು ಬುಧ ಒಂದೇ ರಾಶಿಯಲ್ಲಿದ್ದಾರೆ',
  'சந்திரனும் செவ்வாயும் சேர்க்கை': 'ಚಂದ್ರ ಮತ್ತು ಮಂಗಳ ಸಂಯೋಗ',
  'குரு கேந்திரத்தில் பலமாக உள்ளார்': 'ಗುರು ಕೇಂದ್ರದಲ್ಲಿ ಬಲಶಾಲಿಯಾಗಿದ್ದಾರೆ',
  'சுக்கிரன் சுபஸ்தானத்தில் பலமாக': 'ಶುಕ್ರ ಶುಭ ಸ್ಥಾನದಲ್ಲಿ ಬಲಶಾಲಿ',
  'பெரிய யோகங்கள் இல்லை': 'ಯಾವುದೇ ಪ್ರಮುಖ ಯೋಗಗಳಿಲ್ಲ',
};

// Tithi (lunar day) translations - Tamil to English/Kannada
const TITHI_TRANSLATIONS = {
  // Shukla Paksha (Waxing Moon)
  'பிரதமை': { en: 'Pratipada', kn: 'ಪ್ರತಿಪದ' },
  'துவிதியை': { en: 'Dwitiya', kn: 'ದ್ವಿತೀಯ' },
  'திருதியை': { en: 'Tritiya', kn: 'ತೃತೀಯ' },
  'சதுர்த்தி': { en: 'Chaturthi', kn: 'ಚತುರ್ಥಿ' },
  'பஞ்சமி': { en: 'Panchami', kn: 'ಪಂಚಮಿ' },
  'சஷ்டி': { en: 'Shashti', kn: 'ಷಷ್ಠಿ' },
  'சப்தமி': { en: 'Saptami', kn: 'ಸಪ್ತಮಿ' },
  'அஷ்டமி': { en: 'Ashtami', kn: 'ಅಷ್ಟಮಿ' },
  'நவமி': { en: 'Navami', kn: 'ನವಮಿ' },
  'தசமி': { en: 'Dashami', kn: 'ದಶಮಿ' },
  'ஏகாதசி': { en: 'Ekadashi', kn: 'ಏಕಾದಶಿ' },
  'துவாதசி': { en: 'Dwadashi', kn: 'ದ್ವಾದಶಿ' },
  'திரயோதசி': { en: 'Trayodashi', kn: 'ತ್ರಯೋದಶಿ' },
  'சதுர்தசி': { en: 'Chaturdashi', kn: 'ಚತುರ್ದಶಿ' },
  'பௌர்ணமி': { en: 'Pournami (Full Moon)', kn: 'ಪೌರ್ಣಮಿ' },
  'அமாவாசை': { en: 'Amavasya (New Moon)', kn: 'ಅಮಾವಾಸ್ಯೆ' },
};

// Vaaram (weekday) translations - Tamil to English/Kannada
const VAARAM_TRANSLATIONS = {
  'ஞாயிறு': { en: 'Sunday', kn: 'ಭಾನುವಾರ' },
  'திங்கள்': { en: 'Monday', kn: 'ಸೋಮವಾರ' },
  'செவ்வாய்': { en: 'Tuesday', kn: 'ಮಂಗಳವಾರ' },
  'புதன்': { en: 'Wednesday', kn: 'ಬುಧವಾರ' },
  'வியாழன்': { en: 'Thursday', kn: 'ಗುರುವಾರ' },
  'வெள்ளி': { en: 'Friday', kn: 'ಶುಕ್ರವಾರ' },
  'சனி': { en: 'Saturday', kn: 'ಶನಿವಾರ' },
};

// Yoga (panchang yoga) translations - Tamil to English/Kannada
const PANCHANG_YOGA_TRANSLATIONS = {
  'விஷ்கம்பம்': { en: 'Vishkambha', kn: 'ವಿಷ್ಕಂಭ' },
  'பிரீதி': { en: 'Priti', kn: 'ಪ್ರೀತಿ' },
  'ஆயுஷ்மான்': { en: 'Ayushman', kn: 'ಆಯುಷ್ಮಾನ್' },
  'சௌபாக்கியம்': { en: 'Saubhagya', kn: 'ಸೌಭಾಗ್ಯ' },
  'சோபனம்': { en: 'Shobhana', kn: 'ಶೋಭನ' },
  'அதிகண்டம்': { en: 'Atiganda', kn: 'ಅತಿಗಂಡ' },
  'சுகர்மம்': { en: 'Sukarma', kn: 'ಸುಕರ್ಮ' },
  'திருதி': { en: 'Dhriti', kn: 'ಧೃತಿ' },
  'சூலம்': { en: 'Shula', kn: 'ಶೂಲ' },
  'கண்டம்': { en: 'Ganda', kn: 'ಗಂಡ' },
  'விருத்தி': { en: 'Vriddhi', kn: 'ವೃದ್ಧಿ' },
  'துருவம்': { en: 'Dhruva', kn: 'ಧ್ರುವ' },
  'வியாகாதம்': { en: 'Vyaghata', kn: 'ವ್ಯಾಘಾತ' },
  'ஹர்ஷணம்': { en: 'Harshana', kn: 'ಹರ್ಷಣ' },
  'வஜ்ரம்': { en: 'Vajra', kn: 'ವಜ್ರ' },
  'சித்தி': { en: 'Siddhi', kn: 'ಸಿದ್ಧಿ' },
  'வியதீபாதம்': { en: 'Vyatipata', kn: 'ವ್ಯತೀಪಾತ' },
  'வரியான்': { en: 'Variyan', kn: 'ವರೀಯಾನ್' },
  'பரிகம்': { en: 'Parigha', kn: 'ಪರಿಘ' },
  'சிவம்': { en: 'Shiva', kn: 'ಶಿವ' },
  'சித்தம்': { en: 'Siddha', kn: 'ಸಿದ್ಧ' },
  'சாத்தியம்': { en: 'Sadhya', kn: 'ಸಾಧ್ಯ' },
  'சுபம்': { en: 'Shubha', kn: 'ಶುಭ' },
  'சுக்லம்': { en: 'Shukla', kn: 'ಶುಕ್ಲ' },
  'பிரம்மம்': { en: 'Brahma', kn: 'ಬ್ರಹ್ಮ' },
  'ஐந்திரம்': { en: 'Indra', kn: 'ಐಂದ್ರ' },
  'வைதிருதி': { en: 'Vaidhriti', kn: 'ವೈಧೃತಿ' },
};

// Karana translations - Tamil to English/Kannada
const KARANA_TRANSLATIONS = {
  'பவம்': { en: 'Bava', kn: 'ಬವ' },
  'பாலவம்': { en: 'Balava', kn: 'ಬಾಲವ' },
  'கௌலவம்': { en: 'Kaulava', kn: 'ಕೌಲವ' },
  'தைதுலம்': { en: 'Taitila', kn: 'ತೈತಿಲ' },
  'கரஜம்': { en: 'Garaja', kn: 'ಗರಜ' },
  'வணிஜம்': { en: 'Vanija', kn: 'ವಣಿಜ' },
  'விஷ்டி': { en: 'Vishti (Bhadra)', kn: 'ವಿಷ್ಟಿ' },
  'சகுனி': { en: 'Shakuni', kn: 'ಶಕುನಿ' },
  'சதுஷ்பாதம்': { en: 'Chatushpada', kn: 'ಚತುಷ್ಪಾದ' },
  'நாகவம்': { en: 'Nagava', kn: 'ನಾಗವ' },
  'கிம்ஸ்துக்னம்': { en: 'Kimstughna', kn: 'ಕಿಂಸ್ತುಘ್ನ' },
};

// Helper function to translate yoga effect
const translateYogaEffect = (effect, language) => {
  if (!effect) return effect;
  if (language === 'ta') return effect;
  if (language === 'kn') {
    return YOGA_EFFECT_KANNADA[effect] || effect;
  }
  return YOGA_EFFECT_ENGLISH[effect] || effect;
};

// Helper function to translate tithi
const translateTithi = (tithi, language) => {
  if (!tithi) return tithi;
  if (language === 'ta') return tithi;
  const translation = TITHI_TRANSLATIONS[tithi];
  if (translation) {
    return language === 'kn' ? translation.kn : translation.en;
  }
  return tithi;
};

// Helper function to translate vaaram (weekday)
const translateVaaram = (vaaram, language) => {
  if (!vaaram) return vaaram;
  if (language === 'ta') return vaaram;
  const translation = VAARAM_TRANSLATIONS[vaaram];
  if (translation) {
    return language === 'kn' ? translation.kn : translation.en;
  }
  return vaaram;
};

// Helper function to translate panchang yoga
const translatePanchangYoga = (yoga, language) => {
  if (!yoga) return yoga;
  if (language === 'ta') return yoga;
  const translation = PANCHANG_YOGA_TRANSLATIONS[yoga];
  if (translation) {
    return language === 'kn' ? translation.kn : translation.en;
  }
  return yoga;
};

// Helper function to translate karana
const translateKarana = (karana, language) => {
  if (!karana) return karana;
  if (language === 'ta') return karana;
  const translation = KARANA_TRANSLATIONS[karana];
  if (translation) {
    return language === 'kn' ? translation.kn : translation.en;
  }
  return karana;
};

// Helper functions for translation
const translatePlanetName = (planetName, language, t) => {
  if (!planetName) return planetName;
  if (language === 'ta') return planetName;
  const tamilKey = TAMIL_PLANET_MAP[planetName];
  if (tamilKey) return t(tamilKey);
  const englishKey = ENGLISH_PLANET_MAP[planetName];
  if (englishKey) return t(englishKey);
  return planetName;
};

const translateRasiName = (rasiName, language, t) => {
  if (!rasiName) return rasiName;
  if (language === 'ta') return rasiName;
  const tamilKey = TAMIL_RASI_MAP[rasiName];
  if (tamilKey) return t(tamilKey);
  const englishKey = ENGLISH_RASI_MAP[rasiName];
  if (englishKey) return t(englishKey);
  return rasiName;
};

const translateNakshatraName = (nakshatraName, language, t) => {
  if (!nakshatraName) return nakshatraName;
  if (language === 'ta') return nakshatraName;
  const key = TAMIL_NAKSHATRA_MAP[nakshatraName];
  if (key) return t(key);
  return nakshatraName;
};

// Animated Card Component
const AnimatedCard = ({ children, delay = 0, style }) => {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const translateY = useRef(new Animated.Value(30)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 500,
        delay,
        useNativeDriver: true,
        easing: Easing.out(Easing.ease),
      }),
      Animated.timing(translateY, {
        toValue: 0,
        duration: 500,
        delay,
        useNativeDriver: true,
        easing: Easing.out(Easing.back(1.2)),
      }),
    ]).start();
  }, []);

  return (
    <Animated.View style={[style, { opacity: fadeAnim, transform: [{ translateY }] }]}>
      {children}
    </Animated.View>
  );
};

// Animated Avatar
const AnimatedAvatar = ({ initial }) => {
  const scaleAnim = useRef(new Animated.Value(0)).current;
  const rotateAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.spring(scaleAnim, {
        toValue: 1,
        friction: 5,
        tension: 80,
        useNativeDriver: true,
      }),
      Animated.timing(rotateAnim, {
        toValue: 1,
        duration: 600,
        useNativeDriver: true,
        easing: Easing.out(Easing.ease),
      }),
    ]).start();
  }, []);

  const rotate = rotateAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  return (
    <Animated.View style={[styles.avatar, { transform: [{ scale: scaleAnim }, { rotate }] }]}>
      <Text style={styles.avatarText}>{initial}</Text>
    </Animated.View>
  );
};

// Animated Planet Row
const AnimatedPlanetRow = ({ planet, index, language, t }) => {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(20)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 400,
        delay: index * 50,
        useNativeDriver: true,
      }),
      Animated.timing(slideAnim, {
        toValue: 0,
        duration: 400,
        delay: index * 50,
        useNativeDriver: true,
        easing: Easing.out(Easing.ease),
      }),
    ]).start();
  }, []);

  const retrogradeLabel = language === 'ta' ? 'வ' : language === 'kn' ? 'ವ' : 'R';

  return (
    <Animated.View style={[styles.tableRow, { opacity: fadeAnim, transform: [{ translateX: slideAnim }] }]}>
      <View style={[styles.planetNameCell, { flex: 1.5 }]}>
        <Text style={styles.planetSymbol}>{planet.symbol}</Text>
        <Text style={[styles.planetName, planet.is_retrograde && styles.retrogradeText]}>
          {translatePlanetName(planet.tamil_name || planet.planet, language, t)}{planet.is_retrograde && ` (${retrogradeLabel})`}
        </Text>
      </View>
      <Text style={styles.tableCell}>{translateRasiName(planet.rasi_tamil || planet.rasi, language, t)}</Text>
      <Text style={styles.tableCell}>{translateNakshatraName(planet.nakshatra, language, t)}</Text>
      <Text style={[styles.tableCell, { flex: 0.5 }]}>{planet.nakshatra_pada}</Text>
    </Animated.View>
  );
};

// Animated Yoga Item
const AnimatedYogaItem = ({ yoga, index, language }) => {
  const scaleAnim = useRef(new Animated.Value(0)).current;
  const fadeAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.spring(scaleAnim, {
        toValue: 1,
        friction: 6,
        tension: 80,
        delay: index * 100,
        useNativeDriver: true,
      }),
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 400,
        delay: index * 100,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  // Use English version if available and language is not Tamil
  const yogaName = language === 'ta' ? (yoga.tamil_name || yoga.name) : (yoga.name || yoga.tamil_name);
  const yogaEffect = translateYogaEffect(yoga.effect || yoga.description, language);

  return (
    <Animated.View style={[styles.yogaItem, { opacity: fadeAnim, transform: [{ scale: scaleAnim }] }]}>
      <View style={styles.yogaHeader}>
        <Text style={styles.yogaName}>{yogaName}</Text>
        <View style={styles.yogaStrength}>
          <Text style={styles.yogaStrengthText}>{yoga.strength}%</Text>
        </View>
      </View>
      <Text style={styles.yogaEffect}>{yogaEffect}</Text>
    </Animated.View>
  );
};

// Animated Dasha Period
const AnimatedDashaPeriod = ({ period, index, isCurrent, language, t }) => {
  const scaleAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.spring(scaleAnim, {
      toValue: 1,
      friction: 6,
      tension: 80,
      delay: index * 60,
      useNativeDriver: true,
    }).start();
  }, []);

  return (
    <Animated.View style={{ transform: [{ scale: scaleAnim }] }}>
      <View style={[styles.dashaPeriod, isCurrent && styles.dashaPeriodCurrent]}>
        <Text style={[styles.dashaPeriodLord, isCurrent && styles.dashaPeriodCurrentText]}>
          {translatePlanetName(period.tamil_lord || period.lord, language, t)}
        </Text>
        <Text style={[styles.dashaPeriodYears, isCurrent && styles.dashaPeriodCurrentText]}>
          {period.years}y
        </Text>
      </View>
    </Animated.View>
  );
};

// Animated Download Button
const AnimatedDownloadButton = ({ onPress, loading, t }) => {
  const pulseAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, { toValue: 1.03, duration: 1000, useNativeDriver: true }),
        Animated.timing(pulseAnim, { toValue: 1, duration: 1000, useNativeDriver: true }),
      ])
    ).start();
  }, []);

  const handlePressIn = () => {
    Animated.spring(pulseAnim, { toValue: 0.95, useNativeDriver: true }).start();
  };

  const handlePressOut = () => {
    Animated.spring(pulseAnim, { toValue: 1, friction: 3, useNativeDriver: true }).start();
  };

  return (
    <Animated.View style={{ transform: [{ scale: pulseAnim }] }}>
      <TouchableOpacity
        style={styles.downloadBtn}
        onPress={onPress}
        disabled={loading}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        activeOpacity={0.9}
      >
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <>
            <Ionicons name="download" size={20} color="#fff" />
            <Text style={styles.downloadBtnText}>{t('downloadPDF')}</Text>
          </>
        )}
      </TouchableOpacity>
    </Animated.View>
  );
};

const { width } = Dimensions.get('window');
const CHART_SIZE = (width - 64) / 2; // Two charts side by side

const rasiSymbols = {
  'மேஷம்': '♈', 'ரிஷபம்': '♉', 'மிதுனம்': '♊', 'கடகம்': '♋',
  'சிம்மம்': '♌', 'கன்னி': '♍', 'துலாம்': '♎', 'விருச்சிகம்': '♏',
  'தனுசு': '♐', 'மகரம்': '♑', 'கும்பம்': '♒', 'மீனம்': '♓'
};

// Planet abbreviations - language specific
const PLANET_ABBR_TAMIL = {
  'சூரியன்': 'சூ', 'சந்திரன்': 'சந்', 'செவ்வாய்': 'செ',
  'புதன்': 'பு', 'குரு': 'கு', 'சுக்கிரன்': 'சு',
  'சனி': 'ச', 'ராகு': 'ரா', 'கேது': 'கே',
  'Sun': 'சூ', 'Moon': 'சந்', 'Mars': 'செ',
  'Mercury': 'பு', 'Jupiter': 'கு', 'Venus': 'சு',
  'Saturn': 'ச', 'Rahu': 'ரா', 'Ketu': 'கே'
};

const PLANET_ABBR_ENGLISH = {
  'சூரியன்': 'Su', 'சந்திரன்': 'Mo', 'செவ்வாய்': 'Ma',
  'புதன்': 'Me', 'குரு': 'Ju', 'சுக்கிரன்': 'Ve',
  'சனி': 'Sa', 'ராகு': 'Ra', 'கேது': 'Ke',
  'Sun': 'Su', 'Moon': 'Mo', 'Mars': 'Ma',
  'Mercury': 'Me', 'Jupiter': 'Ju', 'Venus': 'Ve',
  'Saturn': 'Sa', 'Rahu': 'Ra', 'Ketu': 'Ke'
};

const PLANET_ABBR_KANNADA = {
  'சூரியன்': 'ಸೂ', 'சந்திரன்': 'ಚಂ', 'செவ்வாய்': 'ಮಂ',
  'புதன்': 'ಬು', 'குரு': 'ಗು', 'சுக்கிரன்': 'ಶು',
  'சனி': 'ಶ', 'ராகு': 'ರಾ', 'கேது': 'ಕೇ',
  'Sun': 'ಸೂ', 'Moon': 'ಚಂ', 'Mars': 'ಮಂ',
  'Mercury': 'ಬು', 'Jupiter': 'ಗು', 'Venus': 'ಶು',
  'Saturn': 'ಶ', 'Rahu': 'ರಾ', 'Ketu': 'ಕೇ'
};

// Helper to get planet abbreviation based on language
const getPlanetAbbr = (planetName, language) => {
  if (language === 'kn') {
    return PLANET_ABBR_KANNADA[planetName] || planetName?.substring(0, 2);
  } else if (language === 'en') {
    return PLANET_ABBR_ENGLISH[planetName] || planetName?.substring(0, 2);
  }
  return PLANET_ABBR_TAMIL[planetName] || planetName?.substring(0, 2);
};

// Lagna abbreviation based on language
const getLagnaAbbr = (language) => {
  if (language === 'kn') return 'ಲ';
  if (language === 'en') return 'As';
  return 'லக்';
};

const rasiNames = ['மீனம்', 'மேஷம்', 'ரிஷபம்', 'மிதுனம்', 'கும்பம்', '', 'மகரம்', 'சிம்மம்', 'தனுசு', 'விருச்சிகம்', 'துலாம்', 'கன்னி'];
const rasiNamesEnglish = ['Pisces', 'Aries', 'Taurus', 'Gemini', 'Aquarius', '', 'Capricorn', 'Leo', 'Sagittarius', 'Scorpio', 'Libra', 'Virgo'];

// South Indian Chart positions (4x4 grid with center 2x2 empty)
const chartPositions = [
  { row: 0, col: 0 }, { row: 0, col: 1 }, { row: 0, col: 2 }, { row: 0, col: 3 },
  { row: 1, col: 0 }, null,              null,              { row: 1, col: 3 },
  { row: 2, col: 0 }, null,              null,              { row: 2, col: 3 },
  { row: 3, col: 0 }, { row: 3, col: 1 }, { row: 3, col: 2 }, { row: 3, col: 3 },
];

// Map house index to rasi
const houseToRasiIndex = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11];
const rasiOrder = ['Pisces', 'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Capricorn', 'Aquarius', 'Sagittarius', 'Scorpio', 'Libra', 'Virgo'];

// South Indian Chart Component - Styled like the reference image
function SouthIndianChart({ chartData, title, planets, lagna, isNavamsa = false, language, t }) {
  const cellSize = (CHART_SIZE - 4) / 4;

  // Build house data from planets
  const houses = Array(12).fill(null).map(() => []);

  const rasiToHouse = {
    'Pisces': 0, 'Aries': 1, 'Taurus': 2, 'Gemini': 3,
    'Aquarius': 4, 'Cancer': 5, 'Capricorn': 6, 'Leo': 7,
    'Sagittarius': 8, 'Scorpio': 9, 'Libra': 10, 'Virgo': 11
  };

  // Rasi names array mapped to translation keys for chart display
  const rasiKeysForChart = ['pisces', 'aries', 'taurus', 'gemini', 'aquarius', 'cancer', 'capricorn', 'leo', 'sagittarius', 'scorpio', 'libra', 'virgo'];

  if (planets) {
    planets.forEach(planet => {
      const houseIdx = rasiToHouse[planet.rasi];
      if (houseIdx !== undefined) {
        houses[houseIdx].push({
          abbr: getPlanetAbbr(planet.planet, language) || getPlanetAbbr(planet.tamil_name, language) || planet.planet.substring(0, 2),
          retrograde: planet.is_retrograde
        });
      }
    });
  }

  // Add Lagna marker
  const lagnaAbbr = getLagnaAbbr(language);
  if (lagna) {
    const lagnaHouse = rasiToHouse[lagna.rasi];
    if (lagnaHouse !== undefined && !houses[lagnaHouse].find(p => p.isLagna)) {
      houses[lagnaHouse].unshift({ abbr: lagnaAbbr, isLagna: true });
    }
  }

  const renderCell = (houseIndex, row, col) => {
    if (houseIndex === null) return null;

    const planetList = houses[houseIndex] || [];
    const rasiKey = rasiKeysForChart[houseIndex];
    const rasiName = t ? t(rasiKey) : rasiNames[houseIndex];
    const isCenter = (row === 1 || row === 2) && (col === 1 || col === 2);

    if (isCenter) return null;

    return (
      <View
        key={`${row}-${col}`}
        style={[
          styles.chartCell,
          { width: cellSize, height: cellSize },
          houseIndex === 4 && styles.leftCell,
          houseIndex === 7 && styles.rightCell,
        ]}
      >
        <Text style={styles.cellRasiName}>{rasiName}</Text>
        <View style={styles.cellPlanets}>
          {planetList.map((p, i) => (
            <Text
              key={i}
              style={[
                styles.cellPlanetText,
                p.retrograde && styles.retrogradeText,
                p.isLagna && styles.lagnaText
              ]}
            >
              {p.abbr}{planetList.length > 1 && i < planetList.length - 1 ? ',' : ''}
            </Text>
          ))}
        </View>
      </View>
    );
  };

  return (
    <View style={styles.chartWrapper}>
      <Text style={styles.chartTitle}>{title}</Text>
      <View style={[styles.chartContainer, { width: CHART_SIZE, height: CHART_SIZE }]}>
        {/* Row 0 */}
        <View style={styles.chartRow}>
          {renderCell(0, 0, 0)}
          {renderCell(1, 0, 1)}
          {renderCell(2, 0, 2)}
          {renderCell(3, 0, 3)}
        </View>
        {/* Row 1 */}
        <View style={styles.chartRow}>
          {renderCell(4, 1, 0)}
          <View style={[styles.centerCell, { width: cellSize * 2, height: cellSize }]}>
            <Text style={styles.centerText}>{isNavamsa ? (t ? t('navamsam') : 'அம்சம்') : (t ? t('rasiLabel') : 'ராசி')}</Text>
          </View>
          {renderCell(5, 1, 3)}
        </View>
        {/* Row 2 */}
        <View style={styles.chartRow}>
          {renderCell(6, 2, 0)}
          <View style={[styles.centerCellBottom, { width: cellSize * 2, height: cellSize }]} />
          {renderCell(7, 2, 3)}
        </View>
        {/* Row 3 */}
        <View style={styles.chartRow}>
          {renderCell(8, 3, 0)}
          {renderCell(9, 3, 1)}
          {renderCell(10, 3, 2)}
          {renderCell(11, 3, 3)}
        </View>
      </View>
    </View>
  );
}

// Panchagam Component
function PanchagamCard({ chartData }) {
  const panchagam = [
    { label: 'திதி', value: chartData?.panchagam?.tithi || 'சுக்ல பஞ்சமி' },
    { label: 'வாரம்', value: chartData?.panchagam?.vaaram || 'செவ்வாய்' },
    { label: 'நட்சத்திரம்', value: chartData?.moon_sign?.nakshatra || '-' },
    { label: 'யோகம்', value: chartData?.panchagam?.yogam || 'சித்த யோகம்' },
    { label: 'கரணம்', value: chartData?.panchagam?.karanam || 'பவ கரணம்' },
  ];

  return (
    <View style={styles.panchagamCard}>
      <View style={styles.cardHeader}>
        <Ionicons name="calendar" size={16} color="#ea580c" />
        <Text style={styles.cardTitle}>பஞ்சாங்கம்</Text>
      </View>
      <View style={styles.panchagamGrid}>
        {panchagam.map((item, i) => (
          <View key={i} style={styles.panchagamItem}>
            <Text style={styles.panchagamLabel}>{item.label}</Text>
            <Text style={styles.panchagamValue}>{item.value}</Text>
          </View>
        ))}
      </View>
    </View>
  );
}

export default function ProfileScreen({ navigation }) {
  const { userProfile, logout } = useAuth();
  const { language, changeLanguage, t } = useLanguage();
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [pdfLoading, setPdfLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('chart');
  const [showLanguageModal, setShowLanguageModal] = useState(false);
  const insets = useSafeAreaInsets();
  const bottomPadding = Platform.OS === 'android' ? Math.max(insets.bottom, 80) : insets.bottom + 80;

  // Animation refs
  const headerFadeAnim = useRef(new Animated.Value(0)).current;
  const headerSlideAnim = useRef(new Animated.Value(-20)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(headerFadeAnim, { toValue: 1, duration: 500, useNativeDriver: true }),
      Animated.timing(headerSlideAnim, { toValue: 0, duration: 500, useNativeDriver: true, easing: Easing.out(Easing.ease) }),
    ]).start();
  }, []);

  useEffect(() => {
    if (userProfile?.birthDate && userProfile?.birthTime && userProfile?.birthPlace) {
      fetchChartData();
    }
  }, [userProfile]);

  const fetchChartData = async () => {
    setLoading(true);
    try {
      const data = await mobileAPI.getJathagam({
        name: userProfile.name,
        birthDate: userProfile.birthDate,
        birthTime: userProfile.birthTime,
        birthPlace: userProfile.birthPlace,
      });
      setChartData(data);
    } catch (err) {
      console.error('Failed to fetch chart data:', err);
    } finally {
      setLoading(false);
    }
  };

  const generatePDF = async () => {
    if (!userProfile) {
      Alert.alert(t('error'), t('noChartData'));
      return;
    }

    setPdfLoading(true);
    try {
      // Use backend API for comprehensive 60+ page report with Chakra analysis
      const pdfResult = await reportAPI.generateReport({
        name: userProfile.name,
        birthDate: userProfile.birthDate,
        birthTime: userProfile.birthTime,
        birthPlace: userProfile.birthPlace,
      });

      const fileName = `Jathagam_Report_${userProfile.name.replace(/\s+/g, '_')}.pdf`;

      // For web platform, create download link
      if (Platform.OS === 'web') {
        const url = URL.createObjectURL(pdfResult);
        const link = document.createElement('a');
        link.href = url;
        link.download = fileName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        Alert.alert(t('pdfSuccess'), t('pdfCreated'));
      } else {
        // For mobile (React Native), handle arraybuffer response
        const fileUri = FileSystem.documentDirectory + fileName;

        // Check if response is arraybuffer (mobile) or blob (web)
        if (pdfResult.isArrayBuffer && pdfResult.data) {
          // Convert ArrayBuffer to base64
          const uint8Array = new Uint8Array(pdfResult.data);
          let binary = '';
          for (let i = 0; i < uint8Array.byteLength; i++) {
            binary += String.fromCharCode(uint8Array[i]);
          }
          const base64data = btoa(binary);

          await FileSystem.writeAsStringAsync(fileUri, base64data, {
            encoding: FileSystem.EncodingType.Base64,
          });

          if (await Sharing.isAvailableAsync()) {
            await Sharing.shareAsync(fileUri, {
              mimeType: 'application/pdf',
              dialogTitle: t('downloadPDF'),
              UTI: 'com.adobe.pdf'
            });
          } else {
            Alert.alert(t('pdfSuccess'), t('pdfCreated') + ': ' + fileUri);
          }
        } else {
          // Fallback: try blob approach
          const reader = new FileReader();
          reader.readAsDataURL(pdfResult);
          reader.onloadend = async () => {
            const base64data = reader.result.split(',')[1];
            await FileSystem.writeAsStringAsync(fileUri, base64data, {
              encoding: FileSystem.EncodingType.Base64,
            });

            if (await Sharing.isAvailableAsync()) {
              await Sharing.shareAsync(fileUri, {
                mimeType: 'application/pdf',
                dialogTitle: t('downloadPDF'),
                UTI: 'com.adobe.pdf'
              });
            } else {
              Alert.alert(t('pdfSuccess'), t('pdfCreated') + ': ' + fileUri);
            }
          };
        }
      }
    } catch (err) {
      console.error('PDF generation error:', err);
      // Fallback to local HTML generation if backend fails
      try {
        const html = generateComprehensivePDFHTML(userProfile, chartData);
        const { uri } = await Print.printToFileAsync({
          html,
          base64: false,
        });

        if (await Sharing.isAvailableAsync()) {
          await Sharing.shareAsync(uri, {
            mimeType: 'application/pdf',
            dialogTitle: t('downloadPDF'),
            UTI: 'com.adobe.pdf'
          });
        }
      } catch (fallbackErr) {
        console.error('Fallback PDF error:', fallbackErr);
        Alert.alert(t('error'), t('pdfError'));
      }
    } finally {
      setPdfLoading(false);
    }
  };

  const generatePDFHTML = () => {
    const planets = chartData?.planets || [];
    const dasha = chartData?.dasha;
    const yogas = chartData?.yogas || [];

    // Generate chart HTML for Rasi
    const generateChartHTML = (title, isAmsam = false) => {
      const rasiOrder = ['Pisces', 'Aries', 'Taurus', 'Gemini', 'Aquarius', 'Cancer', 'Capricorn', 'Leo', 'Sagittarius', 'Scorpio', 'Libra', 'Virgo'];
      const rasiTamil = ['மீனம்', 'மேஷம்', 'ரிஷபம்', 'மிதுனம்', 'கும்பம்', 'கடகம்', 'மகரம்', 'சிம்மம்', 'தனுசு', 'விருச்சிகம்', 'துலாம்', 'கன்னி'];

      const houses = Array(12).fill('');
      planets.forEach(p => {
        const idx = rasiOrder.indexOf(p.rasi);
        if (idx !== -1) {
          const abbr = PLANET_ABBR[p.planet] || p.planet.substring(0, 2);
          houses[idx] = houses[idx] ? houses[idx] + ',' + abbr : abbr;
        }
      });

      // Add Lagna
      if (chartData?.lagna) {
        const lagnaIdx = rasiOrder.indexOf(chartData.lagna.rasi);
        if (lagnaIdx !== -1) {
          houses[lagnaIdx] = 'லக்' + (houses[lagnaIdx] ? ',' + houses[lagnaIdx] : '');
        }
      }

      return `
        <div style="text-align:center;margin:10px;">
          <div style="font-weight:bold;font-size:14px;margin-bottom:5px;">${title}</div>
          <table style="border-collapse:collapse;margin:auto;background:#fffbeb;">
            <tr>
              <td style="border:1px solid #92400e;width:60px;height:45px;text-align:center;font-size:10px;vertical-align:top;padding:2px;">
                <div style="font-size:8px;color:#888;">${rasiTamil[0]}</div>${houses[0]}
              </td>
              <td style="border:1px solid #92400e;width:60px;height:45px;text-align:center;font-size:10px;vertical-align:top;padding:2px;">
                <div style="font-size:8px;color:#888;">${rasiTamil[1]}</div>${houses[1]}
              </td>
              <td style="border:1px solid #92400e;width:60px;height:45px;text-align:center;font-size:10px;vertical-align:top;padding:2px;">
                <div style="font-size:8px;color:#888;">${rasiTamil[2]}</div>${houses[2]}
              </td>
              <td style="border:1px solid #92400e;width:60px;height:45px;text-align:center;font-size:10px;vertical-align:top;padding:2px;">
                <div style="font-size:8px;color:#888;">${rasiTamil[3]}</div>${houses[3]}
              </td>
            </tr>
            <tr>
              <td style="border:1px solid #92400e;width:60px;height:45px;text-align:center;font-size:10px;vertical-align:top;padding:2px;">
                <div style="font-size:8px;color:#888;">${rasiTamil[4]}</div>${houses[4]}
              </td>
              <td colspan="2" rowspan="2" style="border:1px solid #92400e;text-align:center;background:#fef3c7;font-weight:bold;color:#92400e;">
                ${isAmsam ? 'அம்சம்' : 'ராசி'}
              </td>
              <td style="border:1px solid #92400e;width:60px;height:45px;text-align:center;font-size:10px;vertical-align:top;padding:2px;">
                <div style="font-size:8px;color:#888;">${rasiTamil[5]}</div>${houses[5]}
              </td>
            </tr>
            <tr>
              <td style="border:1px solid #92400e;width:60px;height:45px;text-align:center;font-size:10px;vertical-align:top;padding:2px;">
                <div style="font-size:8px;color:#888;">${rasiTamil[6]}</div>${houses[6]}
              </td>
              <td style="border:1px solid #92400e;width:60px;height:45px;text-align:center;font-size:10px;vertical-align:top;padding:2px;">
                <div style="font-size:8px;color:#888;">${rasiTamil[7]}</div>${houses[7]}
              </td>
            </tr>
            <tr>
              <td style="border:1px solid #92400e;width:60px;height:45px;text-align:center;font-size:10px;vertical-align:top;padding:2px;">
                <div style="font-size:8px;color:#888;">${rasiTamil[8]}</div>${houses[8]}
              </td>
              <td style="border:1px solid #92400e;width:60px;height:45px;text-align:center;font-size:10px;vertical-align:top;padding:2px;">
                <div style="font-size:8px;color:#888;">${rasiTamil[9]}</div>${houses[9]}
              </td>
              <td style="border:1px solid #92400e;width:60px;height:45px;text-align:center;font-size:10px;vertical-align:top;padding:2px;">
                <div style="font-size:8px;color:#888;">${rasiTamil[10]}</div>${houses[10]}
              </td>
              <td style="border:1px solid #92400e;width:60px;height:45px;text-align:center;font-size:10px;vertical-align:top;padding:2px;">
                <div style="font-size:8px;color:#888;">${rasiTamil[11]}</div>${houses[11]}
              </td>
            </tr>
          </table>
        </div>
      `;
    };

    return `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <style>
          body { font-family: Arial, sans-serif; padding: 20px; background: #fffbeb; }
          .header { text-align: center; border: 2px solid #f97316; border-radius: 10px; padding: 15px; background: #fff; margin-bottom: 20px; }
          .header h1 { color: #9a3412; margin: 0; font-size: 24px; }
          .section { background: #fff; border: 1px solid #fed7aa; border-radius: 10px; padding: 15px; margin-bottom: 15px; }
          .section-title { color: #9a3412; font-weight: bold; border-bottom: 2px solid #fed7aa; padding-bottom: 5px; margin-bottom: 10px; }
          .info-grid { display: flex; flex-wrap: wrap; gap: 10px; }
          .info-item { flex: 1; min-width: 45%; background: #fff7ed; padding: 10px; border-radius: 8px; }
          .info-label { font-size: 11px; color: #6b7280; }
          .info-value { font-size: 14px; font-weight: bold; color: #1f2937; }
          .charts-container { display: flex; justify-content: space-around; flex-wrap: wrap; }
          table.planets { width: 100%; border-collapse: collapse; font-size: 12px; }
          table.planets th { background: #fff7ed; color: #9a3412; padding: 8px; text-align: left; }
          table.planets td { padding: 8px; border-bottom: 1px solid #fed7aa; }
          .dasha-item { display: inline-block; background: #faf5ff; padding: 8px 15px; border-radius: 20px; margin: 5px; }
          .yoga-item { background: #ecfdf5; padding: 10px; border-radius: 8px; margin: 5px 0; }
          .footer { text-align: center; margin-top: 20px; color: #9ca3af; font-size: 10px; }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>ஜாதக கட்டம்</h1>
          <p style="color:#6b7280;margin:5px 0;">${userProfile?.name || ''} - ஜாதக அறிக்கை</p>
        </div>

        <div class="section">
          <div class="section-title">பிறப்பு விவரங்கள்</div>
          <div class="info-grid">
            <div class="info-item">
              <div class="info-label">பெயர்</div>
              <div class="info-value">${userProfile?.name || '-'}</div>
            </div>
            <div class="info-item">
              <div class="info-label">பிறந்த தேதி</div>
              <div class="info-value">${userProfile?.birthDate || '-'}</div>
            </div>
            <div class="info-item">
              <div class="info-label">பிறந்த நேரம்</div>
              <div class="info-value">${userProfile?.birthTime || '-'}</div>
            </div>
            <div class="info-item">
              <div class="info-label">பிறந்த இடம்</div>
              <div class="info-value">${userProfile?.birthPlace || '-'}</div>
            </div>
            <div class="info-item">
              <div class="info-label">ராசி</div>
              <div class="info-value">${chartData?.moon_sign?.rasi_tamil || userProfile?.rasi || '-'}</div>
            </div>
            <div class="info-item">
              <div class="info-label">நட்சத்திரம்</div>
              <div class="info-value">${chartData?.moon_sign?.nakshatra || userProfile?.nakshatra || '-'} - பாதம் ${chartData?.moon_sign?.nakshatra_pada || ''}</div>
            </div>
            <div class="info-item">
              <div class="info-label">லக்னம்</div>
              <div class="info-value">${chartData?.lagna?.rasi_tamil || '-'}</div>
            </div>
          </div>
        </div>

        <div class="section">
          <div class="section-title">ஜாதக கட்டங்கள்</div>
          <div class="charts-container">
            ${generateChartHTML('ராசி கட்டம்', false)}
            ${generateChartHTML('அம்சம் கட்டம்', true)}
          </div>
        </div>

        <div class="section">
          <div class="section-title">கிரக நிலை</div>
          <table class="planets">
            <tr>
              <th>கிரகம்</th>
              <th>ராசி</th>
              <th>நட்சத்திரம்</th>
              <th>பாதம்</th>
              <th>டிகிரி</th>
            </tr>
            ${planets.map(p => `
              <tr>
                <td>${p.symbol} ${p.tamil_name}${p.is_retrograde ? ' (வ)' : ''}</td>
                <td>${p.rasi_tamil}</td>
                <td>${p.nakshatra}</td>
                <td>${p.nakshatra_pada}</td>
                <td>${p.degree?.toFixed(2)}°</td>
              </tr>
            `).join('')}
          </table>
        </div>

        ${dasha ? `
        <div class="section">
          <div class="section-title">தசா புக்தி</div>
          <div style="margin-bottom:10px;">
            <strong>தற்போதைய மகா தசை:</strong> ${dasha.current_mahadasha?.tamil_lord || dasha.mahadasha_tamil || '-'}
            (${dasha.current_mahadasha?.start || ''} - ${dasha.current_mahadasha?.end || ''})
          </div>
          <div>
            <strong>அனைத்து தசைகள்:</strong><br/>
            ${(dasha.all_periods || []).map(p => `
              <span class="dasha-item" style="${p.is_current ? 'background:#fef3c7;border:1px solid #f97316;' : ''}">
                ${p.tamil_lord} (${p.years} வருடம்)
              </span>
            `).join('')}
          </div>
        </div>
        ` : ''}

        ${yogas.length > 0 ? `
        <div class="section">
          <div class="section-title">யோகங்கள்</div>
          ${yogas.map(y => `
            <div class="yoga-item">
              <strong>${y.tamil_name || y.name}</strong> (${y.strength}%)
              <br/><span style="font-size:12px;color:#6b7280;">${y.effect || y.description}</span>
            </div>
          `).join('')}
        </div>
        ` : ''}

        <div class="footer">
          ஜோதிட AI - உங்கள் ஜோதிட துணைவர் | ${new Date().toLocaleDateString('ta-IN')}
        </div>
      </body>
      </html>
    `;
  };

  const handleLogout = () => {
    Alert.alert(
      t('logoutConfirm'),
      t('logoutMessage'),
      [
        { text: t('cancel'), style: 'cancel' },
        {
          text: t('yes'),
          onPress: () => {
            // Use setTimeout to ensure the alert closes first
            setTimeout(async () => {
              try {
                console.log('Logging out...');
                await logout();
                console.log('Logout completed');
              } catch (error) {
                console.error('Logout error:', error);
                Alert.alert('Error', 'Failed to logout. Please try again.');
              }
            }, 100);
          },
          style: 'destructive'
        },
      ]
    );
  };

  const rasiSymbol = userProfile?.rasi ? rasiSymbols[userProfile.rasi] : '☉';

  if (!userProfile) {
    return (
      <View style={styles.container}>
        <LinearGradient colors={['#fff7ed', '#ffffff', '#fff7ed']} style={styles.gradient}>
          <LinearGradient
            colors={['#f97316', '#ef4444', '#f97316']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.headerBar}
          />
          <View style={styles.header}>
            <Text style={styles.headerTitle}>{t('profileTitle')}</Text>
            <Text style={styles.headerSubtitle}>{t('profileSubtitle')}</Text>
          </View>
          <View style={styles.emptyCard}>
            <Ionicons name="person-circle-outline" size={80} color="#fed7aa" />
            <Text style={styles.emptyTitle}>{t('newRegRequired')}</Text>
            <Text style={styles.emptyText}>{t('pleaseLogin')}</Text>
          </View>
        </LinearGradient>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <LinearGradient colors={['#fff7ed', '#ffffff', '#fff7ed']} style={styles.gradient}>
        <ScrollView contentContainerStyle={[styles.scrollContent, { paddingBottom: bottomPadding }]}>
          <LinearGradient
            colors={['#f97316', '#ef4444', '#f97316']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.headerBar}
          />

          {/* Header */}
          <Animated.View style={[styles.header, { opacity: headerFadeAnim, transform: [{ translateY: headerSlideAnim }] }]}>
            <View>
              <Text style={styles.headerTitle}>{t('profileTitle')}</Text>
              <Text style={styles.headerSubtitle}>{t('profileSubtitle')}</Text>
            </View>
          </Animated.View>

          {/* User Info Card */}
          <AnimatedCard delay={0} style={styles.card}>
            <View style={styles.userInfoRow}>
              <AnimatedAvatar initial={userProfile.name?.charAt(0) || 'அ'} />
              <View style={styles.userDetails}>
                <Text style={styles.userName}>{userProfile.name}</Text>
                <Text style={styles.userPhone}>{userProfile.phone}</Text>
                <View style={styles.rasiRow}>
                  {userProfile.rasi && (
                    <View style={styles.rasiBadge}>
                      <Text style={styles.rasiSymbolText}>{rasiSymbol}</Text>
                      <Text style={styles.rasiText}>{userProfile.rasi}</Text>
                    </View>
                  )}
                  {userProfile.nakshatra && (
                    <Text style={styles.nakshatraText}>• {userProfile.nakshatra}</Text>
                  )}
                </View>
              </View>
            </View>
          </AnimatedCard>

          {/* Birth Details */}
          <AnimatedCard delay={100} style={styles.card}>
            <View style={styles.cardHeader}>
              <Ionicons name="sunny" size={16} color="#ea580c" />
              <Text style={styles.cardTitle}>{t('birthDetails')}</Text>
            </View>
            <View style={styles.birthDetailsGrid}>
              <View style={styles.birthDetailItem}>
                <Ionicons name="calendar" size={20} color="#ea580c" />
                <View>
                  <Text style={styles.birthDetailLabel}>{t('birthDate')}</Text>
                  <Text style={styles.birthDetailValue}>{userProfile.birthDate || '-'}</Text>
                </View>
              </View>
              <View style={styles.birthDetailItem}>
                <Ionicons name="time" size={20} color="#ea580c" />
                <View>
                  <Text style={styles.birthDetailLabel}>{t('birthTime')}</Text>
                  <Text style={styles.birthDetailValue}>{userProfile.birthTime || '-'}</Text>
                </View>
              </View>
              <View style={[styles.birthDetailItem, styles.birthDetailFull]}>
                <Ionicons name="location" size={20} color="#ea580c" />
                <View>
                  <Text style={styles.birthDetailLabel}>{t('birthPlace')}</Text>
                  <Text style={styles.birthDetailValue}>{userProfile.birthPlace || '-'}</Text>
                </View>
              </View>
            </View>
          </AnimatedCard>

          {/* Panchagam */}
          {chartData && (
            <AnimatedCard delay={200} style={styles.panchagamCard}>
              <View style={styles.cardHeader}>
                <Ionicons name="calendar" size={16} color="#ea580c" />
                <Text style={styles.cardTitle}>{t('panchagam')}</Text>
              </View>
              <View style={styles.panchagamGrid}>
                {[
                  { label: t('tithi'), value: translateTithi(chartData?.panchagam?.tithi, language) || '-' },
                  { label: t('vaaram'), value: translateVaaram(chartData?.panchagam?.vaaram, language) || '-' },
                  { label: t('nakshatram'), value: translateNakshatraName(chartData?.moon_sign?.nakshatra, language, t) || '-' },
                  { label: t('yogam'), value: translatePanchangYoga(chartData?.panchagam?.yogam, language) || '-' },
                  { label: t('karanam'), value: translateKarana(chartData?.panchagam?.karanam, language) || '-' },
                ].map((item, i) => (
                  <View key={i} style={styles.panchagamItem}>
                    <Text style={styles.panchagamLabel}>{item.label}</Text>
                    <Text style={styles.panchagamValue}>{item.value}</Text>
                  </View>
                ))}
              </View>
            </AnimatedCard>
          )}

          {/* Birth Charts - Side by Side */}
          <AnimatedCard delay={300} style={styles.card}>
            <View style={styles.cardHeader}>
              <Ionicons name="grid" size={16} color="#ea580c" />
              <Text style={styles.cardTitle}>{t('jathagamChart')}</Text>
            </View>

            {loading ? (
              <View style={styles.loadingContainer}>
                <ActivityIndicator size="large" color="#f97316" />
              </View>
            ) : chartData?.planets ? (
              <View style={styles.chartsRow}>
                <SouthIndianChart
                  title={t('rasiChart')}
                  planets={chartData.planets}
                  lagna={chartData.lagna}
                  language={language}
                  t={t}
                />
                <SouthIndianChart
                  title={t('navamsaChart')}
                  planets={chartData.planets}
                  lagna={chartData.lagna}
                  isNavamsa={true}
                  language={language}
                  t={t}
                />
              </View>
            ) : (
              <View style={styles.noDataContainer}>
                <Text style={styles.noDataSymbol}>{rasiSymbol}</Text>
                <Text style={styles.noDataText}>{t('fillBirthDetails')}</Text>
              </View>
            )}
          </AnimatedCard>

          {/* Planet Positions Tab */}
          {chartData?.planets && (
            <AnimatedCard delay={400} style={styles.card}>
              <View style={styles.cardHeader}>
                <Ionicons name="planet" size={16} color="#ea580c" />
                <Text style={styles.cardTitle}>{t('planetPositions')}</Text>
              </View>
              <View style={styles.planetTable}>
                <View style={styles.tableHeader}>
                  <Text style={[styles.tableHeaderText, { flex: 1.5 }]}>{t('planet')}</Text>
                  <Text style={styles.tableHeaderText}>{t('rasi')}</Text>
                  <Text style={styles.tableHeaderText}>{t('nakshatra')}</Text>
                  <Text style={[styles.tableHeaderText, { flex: 0.5 }]}>{t('pada')}</Text>
                </View>
                {chartData.planets.map((planet, i) => (
                  <AnimatedPlanetRow key={i} planet={planet} index={i} language={language} t={t} />
                ))}
              </View>
            </AnimatedCard>
          )}

          {/* Dasha Info */}
          {chartData?.dasha && (
            <AnimatedCard delay={500} style={styles.card}>
              <View style={styles.cardHeader}>
                <Ionicons name="moon" size={16} color="#7c3aed" />
                <Text style={[styles.cardTitle, { color: '#6b21a8' }]}>{t('dashaTitle')}</Text>
              </View>
              <View style={styles.dashaGrid}>
                <View style={styles.dashaItem}>
                  <Text style={styles.dashaLabel}>{t('mahaDasha')}</Text>
                  <Text style={styles.dashaValue}>
                    {translatePlanetName(chartData.dasha.current_mahadasha?.tamil_lord || chartData.dasha.mahadasha_tamil, language, t) || '-'}
                  </Text>
                </View>
                <View style={styles.dashaItem}>
                  <Text style={styles.dashaLabel}>{t('period')}</Text>
                  <Text style={styles.dashaValue}>
                    {chartData.dasha.current_mahadasha?.years || 18} {t('years')}
                  </Text>
                </View>
              </View>
              {/* Dasha Timeline */}
              {chartData.dasha.all_periods && (
                <View style={styles.dashaTimeline}>
                  <Text style={styles.dashaTimelineTitle}>{t('dashaSequence')}</Text>
                  <ScrollView horizontal showsHorizontalScrollIndicator={false}>
                    <View style={styles.dashaTimelineRow}>
                      {chartData.dasha.all_periods.map((period, i) => (
                        <AnimatedDashaPeriod
                          key={i}
                          period={period}
                          index={i}
                          isCurrent={period.is_current}
                          language={language}
                          t={t}
                        />
                      ))}
                    </View>
                  </ScrollView>
                </View>
              )}
            </AnimatedCard>
          )}

          {/* Yogas */}
          {chartData?.yogas && chartData.yogas.length > 0 && (
            <AnimatedCard delay={600} style={styles.card}>
              <View style={styles.cardHeader}>
                <Ionicons name="star" size={16} color="#16a34a" />
                <Text style={[styles.cardTitle, { color: '#166534' }]}>{t('yogasTitle')}</Text>
              </View>
              {chartData.yogas.map((yoga, i) => (
                <AnimatedYogaItem key={i} yoga={yoga} index={i} language={language} />
              ))}
            </AnimatedCard>
          )}

          {/* Download PDF Button */}
          {chartData && (
            <AnimatedCard delay={700}>
              <AnimatedDownloadButton onPress={generatePDF} loading={pdfLoading} t={t} />
            </AnimatedCard>
          )}

          {/* Language Selector */}
          <AnimatedCard delay={750} style={styles.card}>
            <View style={styles.cardHeader}>
              <Ionicons name="language" size={16} color="#3b82f6" />
              <Text style={[styles.cardTitle, { color: '#1d4ed8' }]}>{t('language')}</Text>
            </View>
            <TouchableOpacity
              style={styles.languageSelector}
              onPress={() => setShowLanguageModal(true)}
              activeOpacity={0.7}
            >
              <View style={styles.languageInfo}>
                <Text style={styles.languageLabel}>{t('selectLanguage')}</Text>
                <Text style={styles.languageValue}>
                  {languageOptions.find(l => l.code === language)?.name || 'தமிழ்'}
                </Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color="#6b7280" />
            </TouchableOpacity>
          </AnimatedCard>

          {/* Logout Button */}
          <AnimatedCard delay={800}>
            <TouchableOpacity style={styles.logoutBtn} onPress={handleLogout} activeOpacity={0.7}>
              <Ionicons name="log-out" size={20} color="#dc2626" />
              <Text style={styles.logoutText}>{t('logout')}</Text>
            </TouchableOpacity>
          </AnimatedCard>

        </ScrollView>
      </LinearGradient>

      {/* Language Selection Modal */}
      <Modal
        transparent
        visible={showLanguageModal}
        animationType="slide"
        onRequestClose={() => setShowLanguageModal(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.languageModalContent}>
            <View style={styles.languageModalHeader}>
              <Ionicons name="language" size={24} color="#3b82f6" />
              <Text style={styles.languageModalTitle}>{t('selectLanguage')}</Text>
              <TouchableOpacity onPress={() => setShowLanguageModal(false)}>
                <Ionicons name="close" size={24} color="#6b7280" />
              </TouchableOpacity>
            </View>

            {languageOptions.map((lang) => (
              <TouchableOpacity
                key={lang.code}
                style={[
                  styles.languageOption,
                  language === lang.code && styles.languageOptionActive
                ]}
                onPress={() => {
                  changeLanguage(lang.code);
                  setShowLanguageModal(false);
                }}
              >
                <View>
                  <Text style={[
                    styles.languageOptionName,
                    language === lang.code && styles.languageOptionNameActive
                  ]}>
                    {lang.name}
                  </Text>
                  <Text style={styles.languageOptionNameEn}>{lang.nameEn}</Text>
                </View>
                {language === lang.code && (
                  <Ionicons name="checkmark-circle" size={24} color="#3b82f6" />
                )}
              </TouchableOpacity>
            ))}
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  gradient: {
    flex: 1,
  },
  scrollContent: {
    paddingBottom: 100,
  },
  headerBar: {
    height: 4,
  },
  header: {
    padding: 16,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#fed7aa',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#9a3412',
  },
  headerSubtitle: {
    fontSize: 12,
    color: '#6b7280',
    marginTop: 2,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 16,
    marginHorizontal: 16,
    marginTop: 16,
    borderWidth: 1,
    borderColor: '#fed7aa',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 12,
  },
  cardTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#374151',
  },
  userInfoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
  },
  avatar: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: '#f97316',
    justifyContent: 'center',
    alignItems: 'center',
  },
  avatarText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  userDetails: {
    flex: 1,
  },
  userName: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1f2937',
  },
  userPhone: {
    fontSize: 12,
    color: '#6b7280',
    marginTop: 2,
  },
  rasiRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginTop: 8,
  },
  rasiBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff7ed',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#fed7aa',
    gap: 4,
  },
  rasiSymbolText: {
    fontSize: 14,
  },
  rasiText: {
    fontSize: 12,
    color: '#ea580c',
  },
  nakshatraText: {
    fontSize: 12,
    color: '#6b7280',
  },
  birthDetailsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  birthDetailItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    backgroundColor: '#fff7ed',
    borderRadius: 12,
    padding: 12,
    width: '47%',
  },
  birthDetailFull: {
    width: '100%',
  },
  birthDetailLabel: {
    fontSize: 10,
    color: '#6b7280',
  },
  birthDetailValue: {
    fontSize: 13,
    fontWeight: '600',
    color: '#1f2937',
  },
  // Panchagam styles
  panchagamCard: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 16,
    marginHorizontal: 16,
    marginTop: 16,
    borderWidth: 1,
    borderColor: '#fed7aa',
  },
  panchagamGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  panchagamItem: {
    backgroundColor: '#fef3c7',
    borderRadius: 8,
    padding: 10,
    minWidth: '30%',
    flex: 1,
  },
  panchagamLabel: {
    fontSize: 10,
    color: '#92400e',
  },
  panchagamValue: {
    fontSize: 12,
    fontWeight: '600',
    color: '#78350f',
    marginTop: 2,
  },
  // Chart styles
  chartsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  chartWrapper: {
    alignItems: 'center',
  },
  chartTitle: {
    fontSize: 12,
    fontWeight: '600',
    color: '#92400e',
    marginBottom: 8,
  },
  chartContainer: {
    borderWidth: 2,
    borderColor: '#92400e',
    backgroundColor: '#fffbeb',
  },
  chartRow: {
    flexDirection: 'row',
  },
  chartCell: {
    borderWidth: 0.5,
    borderColor: '#d97706',
    backgroundColor: '#fff',
    padding: 2,
    justifyContent: 'flex-start',
  },
  leftCell: {
    borderRightWidth: 0,
  },
  rightCell: {
    borderLeftWidth: 0,
  },
  cellRasiName: {
    fontSize: 7,
    color: '#9ca3af',
  },
  cellPlanets: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginTop: 2,
  },
  cellPlanetText: {
    fontSize: 9,
    fontWeight: '600',
    color: '#374151',
  },
  retrogradeText: {
    color: '#dc2626',
  },
  lagnaText: {
    color: '#7c3aed',
    fontWeight: 'bold',
  },
  centerCell: {
    borderWidth: 0.5,
    borderColor: '#d97706',
    backgroundColor: '#fef3c7',
    justifyContent: 'center',
    alignItems: 'center',
    borderBottomWidth: 0,
  },
  centerCellBottom: {
    borderWidth: 0.5,
    borderColor: '#d97706',
    backgroundColor: '#fef3c7',
    borderTopWidth: 0,
  },
  centerText: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#92400e',
  },
  loadingContainer: {
    padding: 40,
    alignItems: 'center',
  },
  noDataContainer: {
    alignItems: 'center',
    padding: 24,
    backgroundColor: '#fff7ed',
    borderRadius: 12,
  },
  noDataSymbol: {
    fontSize: 48,
    marginBottom: 8,
  },
  noDataText: {
    fontSize: 14,
    color: '#6b7280',
    textAlign: 'center',
  },
  // Planet table styles
  planetTable: {
    marginTop: 8,
  },
  tableHeader: {
    flexDirection: 'row',
    backgroundColor: '#fff7ed',
    paddingVertical: 8,
    paddingHorizontal: 4,
    borderRadius: 8,
  },
  tableHeaderText: {
    flex: 1,
    fontSize: 11,
    fontWeight: '600',
    color: '#9a3412',
    textAlign: 'center',
  },
  tableRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#fed7aa',
  },
  planetNameCell: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    paddingLeft: 4,
  },
  planetSymbol: {
    fontSize: 12,
  },
  planetName: {
    fontSize: 11,
    color: '#374151',
  },
  tableCell: {
    flex: 1,
    fontSize: 11,
    color: '#374151',
    textAlign: 'center',
  },
  // Dasha styles
  dashaGrid: {
    flexDirection: 'row',
    gap: 12,
  },
  dashaItem: {
    flex: 1,
    backgroundColor: '#faf5ff',
    borderRadius: 12,
    padding: 12,
  },
  dashaLabel: {
    fontSize: 11,
    color: '#6b7280',
  },
  dashaValue: {
    fontSize: 14,
    fontWeight: '600',
    color: '#7c3aed',
    marginTop: 4,
  },
  dashaTimeline: {
    marginTop: 12,
  },
  dashaTimelineTitle: {
    fontSize: 11,
    color: '#6b7280',
    marginBottom: 8,
  },
  dashaTimelineRow: {
    flexDirection: 'row',
    gap: 8,
  },
  dashaPeriod: {
    backgroundColor: '#f3e8ff',
    borderRadius: 8,
    padding: 8,
    alignItems: 'center',
    minWidth: 50,
  },
  dashaPeriodCurrent: {
    backgroundColor: '#7c3aed',
  },
  dashaPeriodLord: {
    fontSize: 11,
    fontWeight: '600',
    color: '#7c3aed',
  },
  dashaPeriodYears: {
    fontSize: 9,
    color: '#9ca3af',
    marginTop: 2,
  },
  dashaPeriodCurrentText: {
    color: '#fff',
  },
  // Yoga styles
  yogaItem: {
    backgroundColor: '#ecfdf5',
    borderRadius: 12,
    padding: 12,
    marginBottom: 8,
  },
  yogaHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  yogaName: {
    fontSize: 13,
    fontWeight: '600',
    color: '#166534',
  },
  yogaStrength: {
    backgroundColor: '#16a34a',
    borderRadius: 12,
    paddingHorizontal: 8,
    paddingVertical: 2,
  },
  yogaStrengthText: {
    fontSize: 10,
    color: '#fff',
    fontWeight: '600',
  },
  yogaEffect: {
    fontSize: 11,
    color: '#6b7280',
    marginTop: 4,
  },
  // Download button
  downloadBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    marginHorizontal: 16,
    marginTop: 16,
    padding: 16,
    backgroundColor: '#16a34a',
    borderRadius: 12,
  },
  downloadBtnText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#fff',
  },
  // Logout
  logoutBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    marginHorizontal: 16,
    marginTop: 16,
    padding: 16,
    backgroundColor: '#fef2f2',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#fecaca',
  },
  logoutText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#dc2626',
  },
  emptyCard: {
    alignItems: 'center',
    padding: 32,
    margin: 16,
    backgroundColor: '#fff',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#fed7aa',
  },
  emptyTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#374151',
    marginTop: 16,
  },
  emptyText: {
    fontSize: 13,
    color: '#9ca3af',
    marginTop: 8,
  },
  // Language selector styles
  languageSelector: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#eff6ff',
    borderRadius: 12,
    padding: 14,
    borderWidth: 1,
    borderColor: '#bfdbfe',
  },
  languageInfo: {
    flex: 1,
  },
  languageLabel: {
    fontSize: 11,
    color: '#6b7280',
  },
  languageValue: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1d4ed8',
    marginTop: 2,
  },
  // Language modal styles
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'flex-end',
  },
  languageModalContent: {
    backgroundColor: '#fff',
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    padding: 20,
    paddingBottom: 40,
  },
  languageModalHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  languageModalTitle: {
    flex: 1,
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1f2937',
    marginLeft: 12,
  },
  languageOption: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
    borderRadius: 12,
    marginBottom: 8,
    backgroundColor: '#f9fafb',
    borderWidth: 1,
    borderColor: '#e5e7eb',
  },
  languageOptionActive: {
    backgroundColor: '#eff6ff',
    borderColor: '#3b82f6',
  },
  languageOptionName: {
    fontSize: 18,
    fontWeight: '600',
    color: '#374151',
  },
  languageOptionNameActive: {
    color: '#1d4ed8',
  },
  languageOptionNameEn: {
    fontSize: 12,
    color: '#9ca3af',
    marginTop: 2,
  },
});
