import React, { createContext, useContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

const LanguageContext = createContext();

// Translations for all supported languages
export const translations = {
  // Tamil (default)
  ta: {
    // Common
    appName: 'ஜோதிட AI',
    loading: 'ஏற்றுகிறது...',
    error: 'பிழை',
    ok: 'சரி',
    cancel: 'ரத்து',
    save: 'சேமி',
    close: 'மூடு',
    retry: 'மீண்டும் முயற்சி',

    // Navigation
    home: 'முகப்பு',
    astroFeed: 'கதைகள்',
    matching: 'பொருத்தம்',
    chat: 'AI',
    muhurtham: 'முகூர்த்தம்',
    profile: 'சுயவிவரம்',

    // Dashboard
    greeting: 'வணக்கம்',
    todayPanchangam: 'இன்றைய பஞ்சாங்கம்',
    month: 'மாதம்',
    tithi: 'திதி',
    nakshatra: 'நட்சத்திரம்',
    yoga: 'யோகம்',
    todayScore: 'இன்றைய ஒட்டுமொத்த பலன்',
    good: 'நல்லது',
    average: 'சாதாரணம்',
    caution: 'கவனம்',
    lifeAreas: 'வாழ்க்கை துறைகள்',
    tapForDetails: 'தட்டி விவரம் காண',
    love: 'காதல்',
    career: 'தொழில்',
    education: 'கல்வி',
    family: 'குடும்பம்',
    futureProjection: 'எதிர்கால கணிப்பு',
    monthly: 'மாதவாரி',
    threeYears: '3 ஆண்டுகள்',
    quickActions: 'விரைவு செயல்கள்',
    aiQuestion: 'AI கேள்வி',
    currentYear: 'நடப்பு ஆண்டு',
    nextYear: 'அடுத்த ஆண்டு',
    thirdYear: 'மூன்றாம் ஆண்டு',
    currentDasha: 'நடப்பு தசா',
    mahaDasha: 'மகா தசை',
    antarDasha: 'அந்தர தசை',

    // Score Modal
    scoreExplanation: 'மதிப்பெண் விளக்கம்',
    opportunities: 'நல்ல வாய்ப்புகள்',
    remedies: 'பரிகாரங்கள்',

    // Muhurtham
    muhurthamFinder: 'முகூர்த்தம் கண்டறிதல்',
    auspiciousTime: 'சுப நேரம் தேர்வு',
    eventType: 'நிகழ்வு வகை',
    marriage: 'திருமணம்',
    housewarming: 'கிரக பிரவேசம்',
    vehicle: 'வாகனம்',
    business: 'தொழில்',
    travel: 'பயணம்',
    general: 'பொது',
    goodDay: 'நல்ல நாள்',
    normalDay: 'சாதாரணம்',
    avoidDay: 'தவிர்க்கவும்',
    selectDate: 'நாளை தேர்வு செய்யவும்',
    bestTimes: 'சிறந்த நேரங்கள்',
    todayGoodFor: 'இன்று நல்ல நாள்',
    aiRecommendation: 'AI பரிந்துரை',

    // Chat
    askQuestion: 'கேள்வி கேளுங்கள்...',
    thinking: 'சிந்திக்கிறது...',
    clearChat: 'அழி',
    copied: 'நகல் எடுக்கப்பட்டது',
    messageCopied: 'செய்தி நகல் எடுக்கப்பட்டது!',

    // Matching
    compatibility: 'பொருத்தம்',
    marriageMatching: 'திருமண பொருத்தம்',
    tenPoruthamAnalysis: '10 பொருத்த பகுப்பாய்வு',
    checkCompatibility: 'பொருத்தம் பார்க்க',
    calculateCompatibility: 'பொருத்தம் கணக்கிடு',
    calculatingPoruthams: '10 பொருத்தங்களை கணக்கிடுகிறது...',
    analyzingCompatibility: 'உங்கள் ஜோதிட பொருத்தத்தை ஆராய்கிறோம்',
    groomDetails: 'மணமகன் விவரங்கள்',
    brideDetails: 'மணமகள் விவரங்கள்',
    person1: 'நபர் 1',
    person2: 'நபர் 2',
    name: 'பெயர்',
    enterName: 'பெயர் உள்ளிடவும்',
    birthDate: 'பிறந்த தேதி',
    birthTime: 'பிறந்த நேரம்',
    birthPlace: 'பிறந்த இடம்',
    rasi: 'ராசி',
    rasiOptional: 'ராசி (விரும்பினால்)',
    autoCalculate: 'தானாக கணக்கிடு',
    overallCompatibility: 'ஒட்டுமொத்த பொருத்தம்',
    matchesOutOf10: 'பொருந்தும்',
    aiVerdict: 'AI தீர்ப்பு',
    goodMatch: 'நல்ல பொருத்தம்',
    needsAttention: 'கவனிக்க வேண்டும்',
    tenPoruthams: '꯶ 10 பொருத்தங்கள் ꯶',
    newMatching: 'புதிய பொருத்தம்',
    matchingError: 'பொருத்தம் கணக்கிடுவதில் பிழை. மீண்டும் முயற்சிக்கவும்.',

    // Profile
    editProfile: 'சுயவிவரம் திருத்து',
    language: 'மொழி',
    selectLanguage: 'மொழி தேர்வு',
    logout: 'வெளியேறு',

    // Register
    register: 'பதிவு',
    createAccount: 'கணக்கு உருவாக்கு',

    // Days
    sunday: 'ஞாயிறு',
    monday: 'திங்கள்',
    tuesday: 'செவ்வாய்',
    wednesday: 'புதன்',
    thursday: 'வியாழன்',
    friday: 'வெள்ளி',
    saturday: 'சனி',

    // Short days
    sun: 'ஞா',
    mon: 'தி',
    tue: 'செ',
    wed: 'பு',
    thu: 'வி',
    fri: 'வெ',
    sat: 'ச',

    // Months
    january: 'ஜனவரி',
    february: 'பிப்ரவரி',
    march: 'மார்ச்',
    april: 'ஏப்ரல்',
    may: 'மே',
    june: 'ஜூன்',
    july: 'ஜூலை',
    august: 'ஆகஸ்ட்',
    september: 'செப்டம்பர்',
    october: 'அக்டோபர்',
    november: 'நவம்பர்',
    december: 'டிசம்பர்',

    // Planets
    sun_planet: 'சூரியன்',
    moon_planet: 'சந்திரன்',
    mars: 'செவ்வாய்',
    mercury: 'புதன்',
    jupiter: 'குரு',
    venus: 'சுக்கிரன்',
    saturn: 'சனி',
    rahu: 'ராகு',
    ketu: 'கேது',

    // Time periods
    rahuKalam: 'ராகு காலம்',
    goodTime: 'நல்ல நேரம்',
    normalTime: 'சாதாரண நேரம்',

    // Remedy
    remedy: 'பரிகாரம்',

    // Dashboard - Additional
    planet: 'கிரகம்',
    moon: 'சந்திரன்',
    insight: 'பலன்',
    star: 'நட்சத்திரம்',
    more: 'மேலும்',
    pastYears: 'கடந்த ஆண்டுகள்',
    dasha: 'தசை',
    peakYear: 'சிறந்த ஆண்டு',
    challenging: 'கவனத்துடன்',
    normalYear: 'சாதாரண ஆண்டு',
    lifeAreasBreakdown: 'வாழ்க்கை பகுதிகள்',
    calculation: 'கணக்கீடு விவரம்',
    keyFactors: 'முக்கிய காரணிகள்',
    events: 'நிகழ்வுகள்',
    relationships: 'உறவுகள்',
    finances: 'நிதி',
    health: 'ஆரோக்கியம்',
    age: 'வயது',
    lifeTimeline: 'வாழ்க்கை காலவரிசை',
    avg: 'சராசரி',
    high: 'உயர்வு',
    low: 'குறைவு',
    keyEvents: 'முக்கிய நிகழ்வுகள்',
    best: 'சிறந்த ஆண்டு',
    planetAuraMap: 'கிரக ஒளி வரைபடம்',
    aura: 'ஒளி',
    strong: 'வலிமை',
    live: 'நேரடி',
    liveTransits: 'கிரக கோச்சாரம்',
    realTimePositions: 'நேரடி நிலை',
    moonSign: 'சந்திர ராசி',
    nextSignChange: 'அடுத்த ராசி மாற்றம்',
    hours: 'மணி',
    minutes: 'நிமிடம்',
    celestialMap: 'வான வரைபடம்',
    planetPositions: 'கிரக நிலைகள்',
    retrograde: 'வக்ர',
    retrogradeAlert: 'வக்ர கிரகங்கள்',
    days: 'நாள்',
    comingUp: 'வரவிருக்கும் மாற்றங்கள்',
    personal: 'தனிப்பட்ட',
    generic: 'பொது',
    tap: 'தட்டவும்',
    dashaRunning: 'மகா தசை நடைபெறுகிறது.',
    defaultInsight: 'குரு உங்கள் 9ம் வீட்டில் இருப்பதால் இன்று புதிய கற்றல் சிறப்பாக அமையும்.',

    // Score Modal
    scoreCalculation: 'மதிப்பெண் கணக்கீடு',
    scoreBreakdown: 'மதிப்பெண் பிரிவு',
    keyFactors: 'முக்கிய காரணிகள்',
    lifeAreasLabel: 'வாழ்க்கை பகுதிகள்',
    goodOpportunities: 'நல்ல வாய்ப்புகள்',
    remediesLabel: 'பரிகாரங்கள்',
    total: 'மொத்தம்',
    dashaBhukti: 'தசா/புக்தி',
    housePower: 'வீட்டு பலம்',
    planetPower: 'கிரக பலம்',
    transit: 'கோச்சாரம்',
    yogaDosham: 'யோகம்/தோஷம்',
    navamsam: 'நவாம்சம்',
    karakaPlanet: 'காரக கிரகம்',
    dashaLabel: 'தசை',
    bhuktiLabel: 'புக்தி',
    careerLabel: 'தொழில்',
    financeLabel: 'நிதி',
    healthLabel: 'ஆரோக்கியம்',
    relationshipsLabel: 'உறவுகள்',

    // Remedy Screen
    aiRemedyEngine: 'AI பரிகார இயந்திரம்',
    personalizedRemedies: 'உங்களுக்கான தனிப்பயன் பரிகாரங்கள்',
    selectYourGoal: 'உங்கள் இலக்கைத் தேர்ந்தெடுக்கவும்',
    generatingRemedies: 'பரிகாரங்களை உருவாக்குகிறது...',
    currentDashaLabel: 'தற்போதைய தசா',
    remaining: 'மீதமுள்ள காலம்',
    years: 'வருடங்கள்',
    weakPlanets: 'பலவீனமான கிரகங்கள்',
    goalAnalysis: 'இலக்கு பகுப்பாய்வு',
    favorability: 'சாதகத்தன்மை',
    recommendedRemedies: 'பரிந்துரைக்கப்பட்ட பரிகாரங்கள்',
    priority: 'முன்னுரிமை',
    effect: 'திறன்',
    planetStrength: 'கிரக பலம்',
    dailySchedule: 'தினசரி பரிகார அட்டவணை',
    morning: 'காலை',
    evening: 'மாலை',
    special: 'சிறப்பு',
    luckyItems: 'அதிர்ஷ்ட பொருட்கள்',
    color: 'நிறம்',
    gemstone: 'கல்',
    day: 'நாள்',
    direction: 'திசை',
    number: 'எண்',
    birthDetailsRequired: 'பிறந்த விவரங்கள் தேவை',
    failedToLoadRemedies: 'பரிகாரங்களை ஏற்ற முடியவில்லை',
  },

  // Kannada
  kn: {
    // Common
    appName: 'ಜ್ಯೋತಿಷ AI',
    loading: 'ಲೋಡ್ ಆಗುತ್ತಿದೆ...',
    error: 'ದೋಷ',
    ok: 'ಸರಿ',
    cancel: 'ರದ್ದುಮಾಡು',
    save: 'ಉಳಿಸಿ',
    close: 'ಮುಚ್ಚು',
    retry: 'ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ',

    // Navigation
    home: 'ಮುಖಪುಟ',
    astroFeed: 'ಕಥೆಗಳು',
    matching: 'ಹೊಂದಾಣಿಕೆ',
    chat: 'AI',
    muhurtham: 'ಮುಹೂರ್ತ',
    profile: 'ಪ್ರೊಫೈಲ್',

    // Dashboard
    greeting: 'ನಮಸ್ಕಾರ',
    todayPanchangam: 'ಇಂದಿನ ಪಂಚಾಂಗ',
    month: 'ತಿಂಗಳು',
    tithi: 'ತಿಥಿ',
    nakshatra: 'ನಕ್ಷತ್ರ',
    yoga: 'ಯೋಗ',
    todayScore: 'ಇಂದಿನ ಒಟ್ಟಾರೆ ಫಲ',
    good: 'ಒಳ್ಳೆಯದು',
    average: 'ಸಾಮಾನ್ಯ',
    caution: 'ಎಚ್ಚರಿಕೆ',
    lifeAreas: 'ಜೀವನ ಕ್ಷೇತ್ರಗಳು',
    tapForDetails: 'ವಿವರಗಳಿಗೆ ಟ್ಯಾಪ್ ಮಾಡಿ',
    love: 'ಪ್ರೀತಿ',
    career: 'ವೃತ್ತಿ',
    education: 'ಶಿಕ್ಷಣ',
    family: 'ಕುಟುಂಬ',
    futureProjection: 'ಭವಿಷ್ಯದ ಊಹೆ',
    monthly: 'ಮಾಸಿಕ',
    threeYears: '3 ವರ್ಷಗಳು',
    quickActions: 'ತ್ವರಿತ ಕ್ರಿಯೆಗಳು',
    aiQuestion: 'AI ಪ್ರಶ್ನೆ',
    currentYear: 'ಪ್ರಸ್ತುತ ವರ್ಷ',
    nextYear: 'ಮುಂದಿನ ವರ್ಷ',
    thirdYear: 'ಮೂರನೇ ವರ್ಷ',
    currentDasha: 'ಪ್ರಸ್ತುತ ದಶೆ',
    mahaDasha: 'ಮಹಾ ದಶೆ',
    antarDasha: 'ಅಂತರ್ ದಶೆ',

    // Score Modal
    scoreExplanation: 'ಅಂಕಗಳ ವಿವರಣೆ',
    opportunities: 'ಒಳ್ಳೆಯ ಅವಕಾಶಗಳು',
    remedies: 'ಪರಿಹಾರಗಳು',

    // Muhurtham
    muhurthamFinder: 'ಮುಹೂರ್ತ ಹುಡುಕಾಟ',
    auspiciousTime: 'ಶುಭ ಸಮಯ ಆಯ್ಕೆ',
    eventType: 'ಕಾರ್ಯಕ್ರಮದ ಪ್ರಕಾರ',
    marriage: 'ವಿವಾಹ',
    housewarming: 'ಗೃಹ ಪ್ರವೇಶ',
    vehicle: 'ವಾಹನ',
    business: 'ವ್ಯಾಪಾರ',
    travel: 'ಪ್ರಯಾಣ',
    general: 'ಸಾಮಾನ್ಯ',
    goodDay: 'ಒಳ್ಳೆಯ ದಿನ',
    normalDay: 'ಸಾಮಾನ್ಯ',
    avoidDay: 'ತಪ್ಪಿಸಿ',
    selectDate: 'ದಿನಾಂಕ ಆಯ್ಕೆಮಾಡಿ',
    bestTimes: 'ಉತ್ತಮ ಸಮಯಗಳು',
    todayGoodFor: 'ಇಂದು ಒಳ್ಳೆಯ ದಿನ',
    aiRecommendation: 'AI ಶಿಫಾರಸು',

    // Chat
    askQuestion: 'ಪ್ರಶ್ನೆ ಕೇಳಿ...',
    thinking: 'ಯೋಚಿಸುತ್ತಿದೆ...',
    clearChat: 'ಅಳಿಸಿ',
    copied: 'ನಕಲು ಮಾಡಲಾಗಿದೆ',
    messageCopied: 'ಸಂದೇಶ ನಕಲು ಮಾಡಲಾಗಿದೆ!',

    // Matching
    compatibility: 'ಹೊಂದಾಣಿಕೆ',
    marriageMatching: 'ವಿವಾಹ ಹೊಂದಾಣಿಕೆ',
    tenPoruthamAnalysis: '10 ಪೊರುತಂ ವಿಶ್ಲೇಷಣೆ',
    checkCompatibility: 'ಹೊಂದಾಣಿಕೆ ಪರಿಶೀಲಿಸಿ',
    calculateCompatibility: 'ಹೊಂದಾಣಿಕೆ ಲೆಕ್ಕಹಾಕಿ',
    calculatingPoruthams: '10 ಪೊರುತಂಗಳನ್ನು ಲೆಕ್ಕಹಾಕಲಾಗುತ್ತಿದೆ...',
    analyzingCompatibility: 'ನಿಮ್ಮ ಜ್ಯೋತಿಷ ಹೊಂದಾಣಿಕೆಯನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ',
    groomDetails: 'ವರನ ವಿವರಗಳು',
    brideDetails: 'ವಧುವಿನ ವಿವರಗಳು',
    person1: 'ವ್ಯಕ್ತಿ 1',
    person2: 'ವ್ಯಕ್ತಿ 2',
    name: 'ಹೆಸರು',
    enterName: 'ಹೆಸರು ನಮೂದಿಸಿ',
    birthDate: 'ಹುಟ್ಟಿದ ದಿನಾಂಕ',
    birthTime: 'ಹುಟ್ಟಿದ ಸಮಯ',
    birthPlace: 'ಹುಟ್ಟಿದ ಸ್ಥಳ',
    rasi: 'ರಾಶಿ',
    rasiOptional: 'ರಾಶಿ (ಐಚ್ಛಿಕ)',
    autoCalculate: 'ಸ್ವಯಂ ಲೆಕ್ಕಹಾಕಿ',
    overallCompatibility: 'ಒಟ್ಟಾರೆ ಹೊಂದಾಣಿಕೆ',
    matchesOutOf10: 'ಹೊಂದುತ್ತದೆ',
    aiVerdict: 'AI ತೀರ್ಪು',
    goodMatch: 'ಒಳ್ಳೆಯ ಹೊಂದಾಣಿಕೆ',
    needsAttention: 'ಗಮನ ಬೇಕು',
    tenPoruthams: '꯶ 10 ಪೊರುತಂಗಳು ꯶',
    newMatching: 'ಹೊಸ ಹೊಂದಾಣಿಕೆ',
    matchingError: 'ಹೊಂದಾಣಿಕೆ ಲೆಕ್ಕಾಚಾರದಲ್ಲಿ ದೋಷ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.',

    // Profile
    editProfile: 'ಪ್ರೊಫೈಲ್ ಸಂಪಾದಿಸಿ',
    language: 'ಭಾಷೆ',
    selectLanguage: 'ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ',
    logout: 'ಲಾಗ್ ಔಟ್',

    // Register
    register: 'ನೋಂದಣಿ',
    createAccount: 'ಖಾತೆ ರಚಿಸಿ',

    // Days
    sunday: 'ಭಾನುವಾರ',
    monday: 'ಸೋಮವಾರ',
    tuesday: 'ಮಂಗಳವಾರ',
    wednesday: 'ಬುಧವಾರ',
    thursday: 'ಗುರುವಾರ',
    friday: 'ಶುಕ್ರವಾರ',
    saturday: 'ಶನಿವಾರ',

    // Short days
    sun: 'ಭಾ',
    mon: 'ಸೋ',
    tue: 'ಮಂ',
    wed: 'ಬು',
    thu: 'ಗು',
    fri: 'ಶು',
    sat: 'ಶ',

    // Months
    january: 'ಜನವರಿ',
    february: 'ಫೆಬ್ರವರಿ',
    march: 'ಮಾರ್ಚ್',
    april: 'ಏಪ್ರಿಲ್',
    may: 'ಮೇ',
    june: 'ಜೂನ್',
    july: 'ಜುಲೈ',
    august: 'ಆಗಸ್ಟ್',
    september: 'ಸೆಪ್ಟೆಂಬರ್',
    october: 'ಅಕ್ಟೋಬರ್',
    november: 'ನವೆಂಬರ್',
    december: 'ಡಿಸೆಂಬರ್',

    // Planets
    sun_planet: 'ಸೂರ್ಯ',
    moon_planet: 'ಚಂದ್ರ',
    mars: 'ಮಂಗಳ',
    mercury: 'ಬುಧ',
    jupiter: 'ಗುರು',
    venus: 'ಶುಕ್ರ',
    saturn: 'ಶನಿ',
    rahu: 'ರಾಹು',
    ketu: 'ಕೇತು',

    // Time periods
    rahuKalam: 'ರಾಹು ಕಾಲ',
    goodTime: 'ಒಳ್ಳೆಯ ಸಮಯ',
    normalTime: 'ಸಾಮಾನ್ಯ ಸಮಯ',

    // Remedy
    remedy: 'ಪರಿಹಾರ',

    // Dashboard - Additional
    planet: 'ಗ್ರಹ',
    moon: 'ಚಂದ್ರ',
    insight: 'ಒಳನೋಟ',
    star: 'ನಕ್ಷತ್ರ',
    more: 'ಇನ್ನಷ್ಟು',
    pastYears: 'ಹಿಂದಿನ ವರ್ಷಗಳು',
    dasha: 'ದಶೆ',
    peakYear: 'ಉತ್ತಮ ವರ್ಷ',
    challenging: 'ಸವಾಲಿನ',
    normalYear: 'ಸಾಮಾನ್ಯ ವರ್ಷ',
    lifeAreasBreakdown: 'ಜೀವನ ಕ್ಷೇತ್ರಗಳು',
    calculation: 'ಲೆಕ್ಕಾಚಾರ',
    keyFactors: 'ಪ್ರಮುಖ ಅಂಶಗಳು',
    events: 'ಘಟನೆಗಳು',
    relationships: 'ಸಂಬಂಧಗಳು',
    finances: 'ಹಣಕಾಸು',
    health: 'ಆರೋಗ್ಯ',
    age: 'ವಯಸ್ಸು',
    lifeTimeline: 'ಜೀವನ ಕಾಲರೇಖೆ',
    avg: 'ಸರಾಸರಿ',
    high: 'ಹೆಚ್ಚು',
    low: 'ಕಡಿಮೆ',
    keyEvents: 'ಪ್ರಮುಖ ಘಟನೆಗಳು',
    best: 'ಉತ್ತಮ',
    planetAuraMap: 'ಗ್ರಹ ಆಭಾ ನಕ್ಷೆ',
    aura: 'ಆಭಾ',
    strong: 'ಬಲವಾದ',
    live: 'ನೇರ',
    liveTransits: 'ಗ್ರಹ ಸಂಚಾರ',
    realTimePositions: 'ನೈಜ ಸಮಯ ಸ್ಥಾನಗಳು',
    moonSign: 'ಚಂದ್ರ ರಾಶಿ',
    nextSignChange: 'ಮುಂದಿನ ರಾಶಿ ಬದಲಾವಣೆ',
    hours: 'ಗಂಟೆ',
    minutes: 'ನಿಮಿಷ',
    celestialMap: 'ಆಕಾಶ ನಕ್ಷೆ',
    planetPositions: 'ಗ್ರಹ ಸ್ಥಾನಗಳು',
    retrograde: 'ವಕ್ರ',
    retrogradeAlert: 'ವಕ್ರ ಗ್ರಹಗಳು',
    days: 'ದಿನಗಳು',
    comingUp: 'ಮುಂಬರುವ ಬದಲಾವಣೆಗಳು',
    personal: 'ವೈಯಕ್ತಿಕ',
    generic: 'ಸಾಮಾನ್ಯ',
    tap: 'ಟ್ಯಾಪ್ ಮಾಡಿ',
    dashaRunning: 'ಮಹಾ ದಶೆ ನಡೆಯುತ್ತಿದೆ.',
    defaultInsight: 'ಗುರು ನಿಮ್ಮ 9ನೇ ಮನೆಯಲ್ಲಿ ಇರುವುದರಿಂದ ಇಂದು ಹೊಸ ಕಲಿಕೆ ಉತ್ತಮವಾಗಿರುತ್ತದೆ.',

    // Score Modal
    scoreCalculation: 'ಅಂಕ ಲೆಕ್ಕಾಚಾರ',
    scoreBreakdown: 'ಅಂಕ ವಿಭಜನೆ',
    keyFactors: 'ಪ್ರಮುಖ ಅಂಶಗಳು',
    lifeAreasLabel: 'ಜೀವನ ಕ್ಷೇತ್ರಗಳು',
    goodOpportunities: 'ಒಳ್ಳೆಯ ಅವಕಾಶಗಳು',
    remediesLabel: 'ಪರಿಹಾರಗಳು',
    total: 'ಒಟ್ಟು',
    dashaBhukti: 'ದಶೆ/ಭುಕ್ತಿ',
    housePower: 'ಮನೆ ಬಲ',
    planetPower: 'ಗ್ರಹ ಬಲ',
    transit: 'ಸಂಚಾರ',
    yogaDosham: 'ಯೋಗ/ದೋಷ',
    navamsam: 'ನವಾಂಶ',
    karakaPlanet: 'ಕಾರಕ ಗ್ರಹ',
    dashaLabel: 'ದಶೆ',
    bhuktiLabel: 'ಭುಕ್ತಿ',
    careerLabel: 'ವೃತ್ತಿ',
    financeLabel: 'ಹಣಕಾಸು',
    healthLabel: 'ಆರೋಗ್ಯ',
    relationshipsLabel: 'ಸಂಬಂಧಗಳು',

    // Remedy Screen
    aiRemedyEngine: 'AI ಪರಿಹಾರ ಎಂಜಿನ್',
    personalizedRemedies: 'ನಿಮಗಾಗಿ ವೈಯಕ್ತಿಕ ಪರಿಹಾರಗಳು',
    selectYourGoal: 'ನಿಮ್ಮ ಗುರಿಯನ್ನು ಆಯ್ಕೆಮಾಡಿ',
    generatingRemedies: 'ಪರಿಹಾರಗಳನ್ನು ರಚಿಸಲಾಗುತ್ತಿದೆ...',
    currentDashaLabel: 'ಪ್ರಸ್ತುತ ದಶೆ',
    remaining: 'ಉಳಿದಿದೆ',
    years: 'ವರ್ಷಗಳು',
    weakPlanets: 'ದುರ್ಬಲ ಗ್ರಹಗಳು',
    goalAnalysis: 'ಗುರಿ ವಿಶ್ಲೇಷಣೆ',
    favorability: 'ಅನುಕೂಲತೆ',
    recommendedRemedies: 'ಶಿಫಾರಸು ಮಾಡಿದ ಪರಿಹಾರಗಳು',
    priority: 'ಆದ್ಯತೆ',
    effect: 'ಪರಿಣಾಮ',
    planetStrength: 'ಗ್ರಹ ಶಕ್ತಿ',
    dailySchedule: 'ದೈನಿಕ ಪರಿಹಾರ ವೇಳಾಪಟ್ಟಿ',
    morning: 'ಬೆಳಿಗ್ಗೆ',
    evening: 'ಸಂಜೆ',
    special: 'ವಿಶೇಷ',
    luckyItems: 'ಅದೃಷ್ಟ ವಸ್ತುಗಳು',
    color: 'ಬಣ್ಣ',
    gemstone: 'ರತ್ನ',
    day: 'ದಿನ',
    direction: 'ದಿಕ್ಕು',
    number: 'ಸಂಖ್ಯೆ',
    birthDetailsRequired: 'ಹುಟ್ಟಿದ ವಿವರಗಳು ಅಗತ್ಯ',
    failedToLoadRemedies: 'ಪರಿಹಾರಗಳನ್ನು ಲೋಡ್ ಮಾಡಲು ವಿಫಲವಾಗಿದೆ',
  },

  // English
  en: {
    // Common
    appName: 'Jothida AI',
    loading: 'Loading...',
    error: 'Error',
    ok: 'OK',
    cancel: 'Cancel',
    save: 'Save',
    close: 'Close',
    retry: 'Retry',

    // Navigation
    home: 'Home',
    astroFeed: 'Stories',
    matching: 'Matching',
    chat: 'AI',
    muhurtham: 'Muhurtham',
    profile: 'Profile',

    // Dashboard
    greeting: 'Hello',
    todayPanchangam: "Today's Panchangam",
    month: 'Month',
    tithi: 'Tithi',
    nakshatra: 'Nakshatra',
    yoga: 'Yoga',
    todayScore: "Today's Overall Score",
    good: 'Good',
    average: 'Average',
    caution: 'Caution',
    lifeAreas: 'Life Areas',
    tapForDetails: 'Tap for details',
    love: 'Love',
    career: 'Career',
    education: 'Education',
    family: 'Family',
    futureProjection: 'Future Projection',
    monthly: 'Monthly',
    threeYears: '3 Years',
    quickActions: 'Quick Actions',
    aiQuestion: 'AI Question',
    currentYear: 'Current Year',
    nextYear: 'Next Year',
    thirdYear: 'Third Year',
    currentDasha: 'Current Dasha',
    mahaDasha: 'Maha Dasha',
    antarDasha: 'Antar Dasha',

    // Score Modal
    scoreExplanation: 'Score Explanation',
    opportunities: 'Good Opportunities',
    remedies: 'Remedies',

    // Muhurtham
    muhurthamFinder: 'Muhurtham Finder',
    auspiciousTime: 'Auspicious Time Selection',
    eventType: 'Event Type',
    marriage: 'Marriage',
    housewarming: 'Housewarming',
    vehicle: 'Vehicle',
    business: 'Business',
    travel: 'Travel',
    general: 'General',
    goodDay: 'Good Day',
    normalDay: 'Normal',
    avoidDay: 'Avoid',
    selectDate: 'Select a date',
    bestTimes: 'Best Times',
    todayGoodFor: 'Today is good for',
    aiRecommendation: 'AI Recommendation',

    // Chat
    askQuestion: 'Ask a question...',
    thinking: 'Thinking...',
    clearChat: 'Clear',
    copied: 'Copied',
    messageCopied: 'Message copied!',

    // Matching
    compatibility: 'Compatibility',
    marriageMatching: 'Marriage Matching',
    tenPoruthamAnalysis: '10 Porutham Analysis',
    checkCompatibility: 'Check Compatibility',
    calculateCompatibility: 'Calculate Compatibility',
    calculatingPoruthams: 'Calculating 10 Poruthams...',
    analyzingCompatibility: 'Analyzing your astrological compatibility',
    groomDetails: 'Groom Details',
    brideDetails: 'Bride Details',
    person1: 'Person 1',
    person2: 'Person 2',
    name: 'Name',
    enterName: 'Enter name',
    birthDate: 'Birth Date',
    birthTime: 'Birth Time',
    birthPlace: 'Birth Place',
    rasi: 'Rasi',
    rasiOptional: 'Rasi (optional)',
    autoCalculate: 'Auto calculate',
    overallCompatibility: 'Overall Compatibility',
    matchesOutOf10: 'matches',
    aiVerdict: 'AI Verdict',
    goodMatch: 'Good Match',
    needsAttention: 'Needs Attention',
    tenPoruthams: '꯶ 10 Poruthams ꯶',
    newMatching: 'New Matching',
    matchingError: 'Error calculating compatibility. Please try again.',

    // Profile
    editProfile: 'Edit Profile',
    language: 'Language',
    selectLanguage: 'Select Language',
    logout: 'Logout',

    // Register
    register: 'Register',
    createAccount: 'Create Account',

    // Days
    sunday: 'Sunday',
    monday: 'Monday',
    tuesday: 'Tuesday',
    wednesday: 'Wednesday',
    thursday: 'Thursday',
    friday: 'Friday',
    saturday: 'Saturday',

    // Short days
    sun: 'Su',
    mon: 'Mo',
    tue: 'Tu',
    wed: 'We',
    thu: 'Th',
    fri: 'Fr',
    sat: 'Sa',

    // Months
    january: 'January',
    february: 'February',
    march: 'March',
    april: 'April',
    may: 'May',
    june: 'June',
    july: 'July',
    august: 'August',
    september: 'September',
    october: 'October',
    november: 'November',
    december: 'December',

    // Planets
    sun_planet: 'Sun',
    moon_planet: 'Moon',
    mars: 'Mars',
    mercury: 'Mercury',
    jupiter: 'Jupiter',
    venus: 'Venus',
    saturn: 'Saturn',
    rahu: 'Rahu',
    ketu: 'Ketu',

    // Time periods
    rahuKalam: 'Rahu Kalam',
    goodTime: 'Good Time',
    normalTime: 'Normal Time',

    // Remedy
    remedy: 'Remedy',

    // Dashboard - Additional
    planet: 'Planet',
    moon: 'Moon',
    insight: 'Insight',
    star: 'Star',
    more: 'More',
    pastYears: 'Past Years',
    dasha: 'Dasha',
    peakYear: 'Peak Year',
    challenging: 'Challenging',
    normalYear: 'Normal Year',
    lifeAreasBreakdown: 'Life Areas',
    calculation: 'Calculation',
    keyFactors: 'Key Factors',
    events: 'Events',
    relationships: 'Relationships',
    finances: 'Finances',
    health: 'Health',
    age: 'Age',
    lifeTimeline: 'Life Timeline',
    avg: 'Avg',
    high: 'High',
    low: 'Low',
    keyEvents: 'Key Events',
    best: 'Best',
    planetAuraMap: 'Planet Aura Map',
    aura: 'Aura',
    strong: 'Strong',
    live: 'LIVE',
    liveTransits: 'Live Transits',
    realTimePositions: 'Real-time positions',
    moonSign: 'Moon Sign',
    nextSignChange: 'Next Sign Change',
    hours: 'HRS',
    minutes: 'MIN',
    celestialMap: 'Celestial Map',
    planetPositions: 'Planet Positions',
    retrograde: 'R',
    retrogradeAlert: 'Retrograde Alert',
    days: 'days',
    comingUp: 'Coming Up',
    personal: 'Personal',
    generic: 'Generic',
    tap: 'Tap',
    dashaRunning: 'Maha Dasha is running.',
    defaultInsight: 'Jupiter in your 9th house makes today excellent for new learning.',

    // Score Modal
    scoreCalculation: 'Score Calculation',
    scoreBreakdown: 'Score Breakdown',
    keyFactors: 'Key Factors',
    lifeAreasLabel: 'Life Areas',
    goodOpportunities: 'Good Opportunities',
    remediesLabel: 'Remedies',
    total: 'Total',
    dashaBhukti: 'Dasha/Bhukti',
    housePower: 'House Power',
    planetPower: 'Planet Power',
    transit: 'Transit',
    yogaDosham: 'Yoga/Dosha',
    navamsam: 'Navamsa',
    karakaPlanet: 'Karaka Planet',
    dashaLabel: 'Dasha',
    bhuktiLabel: 'Bhukti',
    careerLabel: 'Career',
    financeLabel: 'Finance',
    healthLabel: 'Health',
    relationshipsLabel: 'Relationships',

    // Remedy Screen
    aiRemedyEngine: 'AI Remedy Engine',
    personalizedRemedies: 'Personalized remedies for you',
    selectYourGoal: 'Select Your Goal',
    generatingRemedies: 'Generating remedies...',
    currentDashaLabel: 'Current Dasha',
    remaining: 'Remaining',
    years: 'years',
    weakPlanets: 'Weak Planets',
    goalAnalysis: 'Goal Analysis',
    favorability: 'Favorability',
    recommendedRemedies: 'Recommended Remedies',
    priority: 'Priority',
    effect: 'Effect',
    planetStrength: 'Planet Strength',
    dailySchedule: 'Daily Remedy Schedule',
    morning: 'Morning',
    evening: 'Evening',
    special: 'Special',
    luckyItems: 'Lucky Items',
    color: 'Color',
    gemstone: 'Gemstone',
    day: 'Day',
    direction: 'Direction',
    number: 'Number',
    birthDetailsRequired: 'Birth details required',
    failedToLoadRemedies: 'Failed to load remedies',
  },
};

// Language options for the picker
export const languageOptions = [
  { code: 'ta', name: 'தமிழ்', nameEn: 'Tamil' },
  { code: 'kn', name: 'ಕನ್ನಡ', nameEn: 'Kannada' },
  { code: 'en', name: 'English', nameEn: 'English' },
];

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState('ta'); // Default to Tamil
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadLanguage();
  }, []);

  const loadLanguage = async () => {
    try {
      const savedLanguage = await AsyncStorage.getItem('appLanguage');
      if (savedLanguage && translations[savedLanguage]) {
        setLanguage(savedLanguage);
      }
    } catch (error) {
      console.error('Error loading language:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const changeLanguage = async (langCode) => {
    if (translations[langCode]) {
      setLanguage(langCode);
      try {
        await AsyncStorage.setItem('appLanguage', langCode);
      } catch (error) {
        console.error('Error saving language:', error);
      }
    }
  };

  // Get translation by key
  const t = (key) => {
    return translations[language]?.[key] || translations['en']?.[key] || key;
  };

  // Get month name by index (0-11)
  const getMonthName = (index) => {
    const monthKeys = ['january', 'february', 'march', 'april', 'may', 'june',
                       'july', 'august', 'september', 'october', 'november', 'december'];
    return t(monthKeys[index]);
  };

  // Get day name by index (0-6, Sunday = 0)
  const getDayName = (index) => {
    const dayKeys = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
    return t(dayKeys[index]);
  };

  // Get short day name
  const getShortDayName = (index) => {
    const dayKeys = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'];
    return t(dayKeys[index]);
  };

  // Format date based on language
  const formatDate = (date) => {
    const d = new Date(date);
    const day = d.getDate();
    const monthName = getMonthName(d.getMonth());
    const year = d.getFullYear();
    const dayName = getDayName(d.getDay());
    return `${dayName}, ${day} ${monthName} ${year}`;
  };

  return (
    <LanguageContext.Provider
      value={{
        language,
        changeLanguage,
        t,
        getMonthName,
        getDayName,
        getShortDayName,
        formatDate,
        isLoading,
        translations: translations[language]
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

export default LanguageContext;
