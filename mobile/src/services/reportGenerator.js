/**
 * Comprehensive Jathagam Report Generator
 * Generates detailed 20-30 page PDF reports with AI analysis
 * Supports multiple languages: Tamil, Kannada, English
 */

// Language-specific data
const LANG_DATA = {
  ta: {
    months: ['சித்திரை', 'வைகாசி', 'ஆனி', 'ஆடி', 'ஆவணி', 'புரட்டாசி', 'ஐப்பசி', 'கார்த்திகை', 'மார்கழி', 'தை', 'மாசி', 'பங்குனி'],
    tithis: ['பிரதமை', 'துவிதியை', 'திருதியை', 'சதுர்த்தி', 'பஞ்சமி', 'சஷ்டி', 'சப்தமி', 'அஷ்டமி', 'நவமி', 'தசமி', 'ஏகாதசி', 'துவாதசி', 'திரயோதசி', 'சதுர்த்தசி', 'பூர்ணிமை', 'அமாவாசை'],
    rasiNames: ['மேஷம்', 'ரிஷபம்', 'மிதுனம்', 'கடகம்', 'சிம்மம்', 'கன்னி', 'துலாம்', 'விருச்சிகம்', 'தனுசு', 'மகரம்', 'கும்பம்', 'மீனம்'],
    chartRasiOrder: ['மீனம்', 'மேஷம்', 'ரிஷபம்', 'மிதுனம்', 'கும்பம்', 'கடகம்', 'மகரம்', 'சிம்மம்', 'தனுசு', 'விருச்சிகம்', 'துலாம்', 'கன்னி'],
    lagnaAbbr: 'லக்',
    rasiLabel: 'ராசி',
    amsamLabel: 'அம்சம்',
    planetAbbr: { 'Sun': 'சூ', 'Moon': 'சந்', 'Mars': 'செ', 'Mercury': 'பு', 'Jupiter': 'கு', 'Venus': 'சு', 'Saturn': 'ச', 'Rahu': 'ரா', 'Ketu': 'கே' },
    ui: {
      reportTitle: 'ஜாதக அறிக்கை',
      detailedAnalysis: 'விரிவான ஜோதிட பகுப்பாய்வு',
      birthDetails: 'பிறப்பு விவரங்கள்',
      name: 'பெயர்',
      birthDate: 'பிறந்த தேதி',
      birthTime: 'பிறந்த நேரம்',
      birthPlace: 'பிறந்த இடம்',
      rasi: 'ராசி',
      nakshatra: 'நட்சத்திரம்',
      lagna: 'லக்னம்',
      lagnaNakshatra: 'லக்ன நட்சத்திரம்',
      pada: 'பாதம்',
      panchagamDetails: 'பஞ்சாங்கம் விவரங்கள்',
      tithi: 'திதி',
      vaaram: 'வாரம்',
      yogam: 'யோகம்',
      karanam: 'கரணம்',
      sunrise: 'சூரிய உதயம்',
      sunset: 'சூரிய அஸ்தமனம்',
      chartTitle: 'ஜாதக கட்டங்கள்',
      rasiChart: 'ராசி கட்டம்',
      navamsaChart: 'நவாம்ச கட்டம்',
      planetPositions: 'கிரக நிலை விவரங்கள்',
      planet: 'கிரகம்',
      degree: 'டிகிரி',
      strength: 'பலம்',
      status: 'நிலை',
      retrograde: 'வக்கிரம்',
      goodStatus: '↑ நல்லது',
      cautionStatus: '↓ கவனம்',
      normalStatus: '→ சாதாரணம்',
      aiAnalysisSummary: 'AI ஜோதிட பகுப்பாய்வு சுருக்கம்',
      chartIntro: 'ஜாதக அறிமுகம்',
      rasiTraits: 'ராசி பண்புகள்',
      nakshatraTraits: 'நட்சத்திர பண்புகள்',
      planetStrengthAnalysis: 'கிரக பலம் பகுப்பாய்வு',
      strongPlanets: 'பலமான கிரகங்கள்',
      weakPlanets: 'பலவீனமான கிரகங்கள்',
      currentDashaStatus: 'தற்போதைய தசா நிலை',
      yogaBenefits: 'யோக பலன்கள்',
      luckyAspects: 'அதிர்ஷ்ட அம்சங்கள்',
      luckyColor: 'அதிர்ஷ்ட நிறம்',
      luckyNumber: 'அதிர்ஷ்ட எண்',
      luckyGem: 'அதிர்ஷ்ட கல்',
      detailedYogaAnalysis: 'விரிவான யோக பகுப்பாய்வு',
      yogaFormation: 'யோக உருவாக்கம்',
      expectedBenefits: 'எதிர்பார்க்கும் பலன்கள்',
      activationPeriod: 'செயல்படும் காலம்',
      detailedDashaAnalysis: 'விரிவான தசா புக்தி பலன்கள்',
      mahaDasha: 'மகா தசை',
      currentlyRunning: 'தற்போது நடப்பில்',
      years: 'வருடம்',
      positiveBenefits: 'சாதகமான பலன்கள்',
      thingsToWatch: 'கவனிக்க வேண்டியவை',
      remedies: 'பரிகாரங்கள்',
      lifeAreaPredictions: 'வாழ்க்கை துறை பலன்கள் (12 வீடுகள்)',
      house: 'வீடு',
      areas: 'துறைகள்',
      planets: 'கிரகங்கள்',
      noPlanetsInHouse: 'இந்த வீட்டில் கிரகங்கள் இல்லை',
      benefits: 'பலன்',
      reportDate: 'அறிக்கை தேதி',
      trustedAstrologer: 'உங்கள் நம்பகமான ஜோதிட துணைவர்',
      aiGeneratedReport: 'இந்த அறிக்கை AI உதவியுடன் உருவாக்கப்பட்டது',
      allRightsReserved: 'அனைத்து உரிமைகளும் பாதுகாக்கப்பட்டவை',
      element: 'தத்துவம்',
      ruler: 'அதிபதி',
      mainQualities: 'முக்கிய பண்புகள்',
      suitableCareers: 'பொருத்தமான தொழில்கள்',
      deity: 'அதிதேவதை',
      specialTrait: 'சிறப்பு பண்பு',
      suitableCareer: 'பொருத்தமான தொழில்',
      noYogasFound: 'குறிப்பிட்ட யோகங்கள் கணக்கிடப்படவில்லை',
      yogasFoundMsg: 'இந்த ஜாதகத்தில் சிறப்பு யோகங்கள் உள்ளன',
      yogasWillBenefit: 'இவை வாழ்வில் சிறப்பான பலன்களை தரும்',
      theseWillGiveBenefits: 'இவை நல்ல பலன்களை தரும்',
      needsRemedies: 'இவற்றிற்கு பரிகாரம் தேவை',
      inRelatedPlanetDasha: 'சம்பந்தப்பட்ட கிரக தசையில்',
    }
  },
  kn: {
    months: ['ಚೈತ್ರ', 'ವೈಶಾಖ', 'ಜ್ಯೇಷ್ಠ', 'ಆಷಾಢ', 'ಶ್ರಾವಣ', 'ಭಾದ್ರಪದ', 'ಆಶ್ವಯುಜ', 'ಕಾರ್ತೀಕ', 'ಮಾರ್ಗಶಿರ', 'ಪುಷ್ಯ', 'ಮಾಘ', 'ಫಾಲ್ಗುಣ'],
    tithis: ['ಪ್ರತಿಪದ', 'ದ್ವಿತೀಯ', 'ತೃತೀಯ', 'ಚತುರ್ಥಿ', 'ಪಂಚಮಿ', 'ಷಷ್ಠಿ', 'ಸಪ್ತಮಿ', 'ಅಷ್ಟಮಿ', 'ನವಮಿ', 'ದಶಮಿ', 'ಏಕಾದಶಿ', 'ದ್ವಾದಶಿ', 'ತ್ರಯೋದಶಿ', 'ಚತುರ್ದಶಿ', 'ಪೂರ್ಣಿಮ', 'ಅಮಾವಾಸ್ಯೆ'],
    rasiNames: ['ಮೇಷ', 'ವೃಷಭ', 'ಮಿಥುನ', 'ಕರ್ಕಾಟಕ', 'ಸಿಂಹ', 'ಕನ್ಯಾ', 'ತುಲಾ', 'ವೃಶ್ಚಿಕ', 'ಧನು', 'ಮಕರ', 'ಕುಂಭ', 'ಮೀನ'],
    chartRasiOrder: ['ಮೀನ', 'ಮೇಷ', 'ವೃಷಭ', 'ಮಿಥುನ', 'ಕುಂಭ', 'ಕರ್ಕಾಟಕ', 'ಮಕರ', 'ಸಿಂಹ', 'ಧನು', 'ವೃಶ್ಚಿಕ', 'ತುಲಾ', 'ಕನ್ಯಾ'],
    lagnaAbbr: 'ಲಗ್ನ',
    rasiLabel: 'ರಾಶಿ',
    amsamLabel: 'ನವಾಂಶ',
    planetAbbr: { 'Sun': 'ಸೂ', 'Moon': 'ಚಂ', 'Mars': 'ಕು', 'Mercury': 'ಬು', 'Jupiter': 'ಗು', 'Venus': 'ಶು', 'Saturn': 'ಶ', 'Rahu': 'ರಾ', 'Ketu': 'ಕೇ' },
    ui: {
      reportTitle: 'ಜಾತಕ ವರದಿ',
      detailedAnalysis: 'ವಿಸ್ತೃತ ಜ್ಯೋತಿಷ ವಿಶ್ಲೇಷಣೆ',
      birthDetails: 'ಜನ್ಮ ವಿವರಗಳು',
      name: 'ಹೆಸರು',
      birthDate: 'ಜನ್ಮ ದಿನಾಂಕ',
      birthTime: 'ಜನ್ಮ ಸಮಯ',
      birthPlace: 'ಜನ್ಮ ಸ್ಥಳ',
      rasi: 'ರಾಶಿ',
      nakshatra: 'ನಕ್ಷತ್ರ',
      lagna: 'ಲಗ್ನ',
      lagnaNakshatra: 'ಲಗ್ನ ನಕ್ಷತ್ರ',
      pada: 'ಪಾದ',
      panchagamDetails: 'ಪಂಚಾಂಗ ವಿವರಗಳು',
      tithi: 'ತಿಥಿ',
      vaaram: 'ವಾರ',
      yogam: 'ಯೋಗ',
      karanam: 'ಕರಣ',
      sunrise: 'ಸೂರ್ಯೋದಯ',
      sunset: 'ಸೂರ್ಯಾಸ್ತ',
      chartTitle: 'ಜಾತಕ ಚಾರ್ಟ್‌ಗಳು',
      rasiChart: 'ರಾಶಿ ಚಾರ್ಟ್',
      navamsaChart: 'ನವಾಂಶ ಚಾರ್ಟ್',
      planetPositions: 'ಗ್ರಹ ಸ್ಥಾನ ವಿವರಗಳು',
      planet: 'ಗ್ರಹ',
      degree: 'ಡಿಗ್ರಿ',
      strength: 'ಬಲ',
      status: 'ಸ್ಥಿತಿ',
      retrograde: 'ವಕ್ರ',
      goodStatus: '↑ ಒಳ್ಳೆಯದು',
      cautionStatus: '↓ ಎಚ್ಚರಿಕೆ',
      normalStatus: '→ ಸಾಮಾನ್ಯ',
      aiAnalysisSummary: 'AI ಜ್ಯೋತಿಷ ವಿಶ್ಲೇಷಣೆ ಸಾರಾಂಶ',
      chartIntro: 'ಜಾತಕ ಪರಿಚಯ',
      rasiTraits: 'ರಾಶಿ ಗುಣಲಕ್ಷಣಗಳು',
      nakshatraTraits: 'ನಕ್ಷತ್ರ ಗುಣಲಕ್ಷಣಗಳು',
      planetStrengthAnalysis: 'ಗ್ರಹ ಬಲ ವಿಶ್ಲೇಷಣೆ',
      strongPlanets: 'ಬಲಿಷ್ಠ ಗ್ರಹಗಳು',
      weakPlanets: 'ದುರ್ಬಲ ಗ್ರಹಗಳು',
      currentDashaStatus: 'ಪ್ರಸ್ತುತ ದಶಾ ಸ್ಥಿತಿ',
      yogaBenefits: 'ಯೋಗ ಫಲಗಳು',
      luckyAspects: 'ಅದೃಷ್ಟ ಅಂಶಗಳು',
      luckyColor: 'ಅದೃಷ್ಟ ಬಣ್ಣ',
      luckyNumber: 'ಅದೃಷ್ಟ ಸಂಖ್ಯೆ',
      luckyGem: 'ಅದೃಷ್ಟ ರತ್ನ',
      detailedYogaAnalysis: 'ವಿಸ್ತೃತ ಯೋಗ ವಿಶ್ಲೇಷಣೆ',
      yogaFormation: 'ಯೋಗ ರಚನೆ',
      expectedBenefits: 'ನಿರೀಕ್ಷಿತ ಫಲಗಳು',
      activationPeriod: 'ಸಕ್ರಿಯಗೊಳ್ಳುವ ಅವಧಿ',
      detailedDashaAnalysis: 'ವಿಸ್ತೃತ ದಶಾ ಭುಕ್ತಿ ಫಲಗಳು',
      mahaDasha: 'ಮಹಾ ದಶಾ',
      currentlyRunning: 'ಪ್ರಸ್ತುತ ನಡೆಯುತ್ತಿದೆ',
      years: 'ವರ್ಷ',
      positiveBenefits: 'ಸಕಾರಾತ್ಮಕ ಫಲಗಳು',
      thingsToWatch: 'ಗಮನಿಸಬೇಕಾದ ಅಂಶಗಳು',
      remedies: 'ಪರಿಹಾರಗಳು',
      lifeAreaPredictions: 'ಜೀವನ ಕ್ಷೇತ್ರ ಫಲಗಳು (12 ಮನೆಗಳು)',
      house: 'ಮನೆ',
      areas: 'ಕ್ಷೇತ್ರಗಳು',
      planets: 'ಗ್ರಹಗಳು',
      noPlanetsInHouse: 'ಈ ಮನೆಯಲ್ಲಿ ಗ್ರಹಗಳಿಲ್ಲ',
      benefits: 'ಫಲ',
      reportDate: 'ವರದಿ ದಿನಾಂಕ',
      trustedAstrologer: 'ನಿಮ್ಮ ನಂಬಿಕಸ್ಥ ಜ್ಯೋತಿಷ ಸಹಚರ',
      aiGeneratedReport: 'ಈ ವರದಿ AI ಸಹಾಯದಿಂದ ರಚಿಸಲಾಗಿದೆ',
      allRightsReserved: 'ಎಲ್ಲಾ ಹಕ್ಕುಗಳು ಕಾಯ್ದಿರಿಸಲಾಗಿದೆ',
      element: 'ತತ್ವ',
      ruler: 'ಅಧಿಪತಿ',
      mainQualities: 'ಮುಖ್ಯ ಗುಣಗಳು',
      suitableCareers: 'ಸೂಕ್ತ ವೃತ್ತಿಗಳು',
      deity: 'ಅಧಿದೇವತೆ',
      specialTrait: 'ವಿಶೇಷ ಗುಣ',
      suitableCareer: 'ಸೂಕ್ತ ವೃತ್ತಿ',
      noYogasFound: 'ನಿರ್ದಿಷ್ಟ ಯೋಗಗಳು ಲೆಕ್ಕಾಚಾರ ಮಾಡಿಲ್ಲ',
      yogasFoundMsg: 'ಈ ಜಾತಕದಲ್ಲಿ ವಿಶೇಷ ಯೋಗಗಳಿವೆ',
      yogasWillBenefit: 'ಇವು ಜೀವನದಲ್ಲಿ ವಿಶೇಷ ಫಲಗಳನ್ನು ನೀಡುತ್ತವೆ',
      theseWillGiveBenefits: 'ಇವು ಒಳ್ಳೆಯ ಫಲಗಳನ್ನು ನೀಡುತ್ತವೆ',
      needsRemedies: 'ಇವುಗಳಿಗೆ ಪರಿಹಾರ ಅಗತ್ಯ',
      inRelatedPlanetDasha: 'ಸಂಬಂಧಿತ ಗ್ರಹ ದಶೆಯಲ್ಲಿ',
    }
  },
  en: {
    months: ['Chaitra', 'Vaishakha', 'Jyeshtha', 'Ashadha', 'Shravana', 'Bhadrapada', 'Ashwayuja', 'Kartika', 'Margashira', 'Pushya', 'Magha', 'Phalguna'],
    tithis: ['Pratipada', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami', 'Shashthi', 'Saptami', 'Ashtami', 'Navami', 'Dashami', 'Ekadashi', 'Dwadashi', 'Trayodashi', 'Chaturdashi', 'Purnima', 'Amavasya'],
    rasiNames: ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'],
    chartRasiOrder: ['Pisces', 'Aries', 'Taurus', 'Gemini', 'Aquarius', 'Cancer', 'Capricorn', 'Leo', 'Sagittarius', 'Scorpio', 'Libra', 'Virgo'],
    lagnaAbbr: 'Asc',
    rasiLabel: 'Rasi',
    amsamLabel: 'Navamsa',
    planetAbbr: { 'Sun': 'Su', 'Moon': 'Mo', 'Mars': 'Ma', 'Mercury': 'Me', 'Jupiter': 'Ju', 'Venus': 'Ve', 'Saturn': 'Sa', 'Rahu': 'Ra', 'Ketu': 'Ke' },
    ui: {
      reportTitle: 'Birth Chart Report',
      detailedAnalysis: 'Detailed Astrological Analysis',
      birthDetails: 'Birth Details',
      name: 'Name',
      birthDate: 'Date of Birth',
      birthTime: 'Time of Birth',
      birthPlace: 'Place of Birth',
      rasi: 'Moon Sign',
      nakshatra: 'Nakshatra',
      lagna: 'Ascendant',
      lagnaNakshatra: 'Ascendant Nakshatra',
      pada: 'Pada',
      panchagamDetails: 'Panchagam Details',
      tithi: 'Tithi',
      vaaram: 'Weekday',
      yogam: 'Yoga',
      karanam: 'Karana',
      sunrise: 'Sunrise',
      sunset: 'Sunset',
      chartTitle: 'Birth Charts',
      rasiChart: 'Rasi Chart',
      navamsaChart: 'Navamsa Chart',
      planetPositions: 'Planet Position Details',
      planet: 'Planet',
      degree: 'Degree',
      strength: 'Strength',
      status: 'Status',
      retrograde: 'Retrograde',
      goodStatus: '↑ Good',
      cautionStatus: '↓ Caution',
      normalStatus: '→ Normal',
      aiAnalysisSummary: 'AI Astrological Analysis Summary',
      chartIntro: 'Chart Introduction',
      rasiTraits: 'Rasi Characteristics',
      nakshatraTraits: 'Nakshatra Characteristics',
      planetStrengthAnalysis: 'Planet Strength Analysis',
      strongPlanets: 'Strong Planets',
      weakPlanets: 'Weak Planets',
      currentDashaStatus: 'Current Dasha Status',
      yogaBenefits: 'Yoga Benefits',
      luckyAspects: 'Lucky Aspects',
      luckyColor: 'Lucky Color',
      luckyNumber: 'Lucky Number',
      luckyGem: 'Lucky Gem',
      detailedYogaAnalysis: 'Detailed Yoga Analysis',
      yogaFormation: 'Yoga Formation',
      expectedBenefits: 'Expected Benefits',
      activationPeriod: 'Activation Period',
      detailedDashaAnalysis: 'Detailed Dasha Bhukti Analysis',
      mahaDasha: 'Maha Dasha',
      currentlyRunning: 'Currently Running',
      years: 'years',
      positiveBenefits: 'Positive Benefits',
      thingsToWatch: 'Things to Watch',
      remedies: 'Remedies',
      lifeAreaPredictions: 'Life Area Predictions (12 Houses)',
      house: 'House',
      areas: 'Areas',
      planets: 'Planets',
      noPlanetsInHouse: 'No planets in this house',
      benefits: 'Benefits',
      reportDate: 'Report Date',
      trustedAstrologer: 'Your Trusted Astrology Companion',
      aiGeneratedReport: 'This report was generated with AI assistance',
      allRightsReserved: 'All rights reserved',
      element: 'Element',
      ruler: 'Ruler',
      mainQualities: 'Main Qualities',
      suitableCareers: 'Suitable Careers',
      deity: 'Deity',
      specialTrait: 'Special Trait',
      suitableCareer: 'Suitable Career',
      noYogasFound: 'No specific yogas calculated',
      yogasFoundMsg: 'This chart has special yogas',
      yogasWillBenefit: 'These will provide special benefits in life',
      theseWillGiveBenefits: 'These will give good benefits',
      needsRemedies: 'These need remedies',
      inRelatedPlanetDasha: 'in the related planet dasha',
    }
  }
};

// Legacy constants for backward compatibility
const TAMIL_MONTHS = LANG_DATA.ta.months;
const TITHIS = LANG_DATA.ta.tithis;

// Multi-language Nakshatra details
const NAKSHATRA_DETAILS_ML = {
  ta: {
    'அஸ்வினி': { deity: 'அஸ்வினி குமாரர்கள்', symbol: 'குதிரை தலை', quality: 'சுறுசுறுப்பு, வேகம்', career: 'மருத்துவம், போக்குவரத்து', lucky_gems: 'வைடூர்யம்' },
    'பரணி': { deity: 'யமன்', symbol: 'யோனி', quality: 'சுய கட்டுப்பாடு', career: 'நீதி, சட்டம்', lucky_gems: 'வைரம்' },
    'கார்த்திகை': { deity: 'அக்னி', symbol: 'தீ', quality: 'தீவிரம், உறுதி', career: 'ராணுவம், காவல்துறை', lucky_gems: 'மாணிக்கம்' },
    'ரோகிணி': { deity: 'பிரம்மா', symbol: 'மாட்டு வண்டி', quality: 'அழகு, கலை', career: 'கலை, திரைப்படம்', lucky_gems: 'முத்து' },
    'மிருகசீரிடம்': { deity: 'சந்திரன்', symbol: 'மான் தலை', quality: 'ஆராய்ச்சி', career: 'ஆராய்ச்சி, அறிவியல்', lucky_gems: 'முத்து' },
    'திருவாதிரை': { deity: 'ருத்ரன்', symbol: 'கண்ணீர் துளி', quality: 'ஆன்மீகம்', career: 'ஆன்மீகம், யோகா', lucky_gems: 'கோமேதகம்' },
    'புனர்பூசம்': { deity: 'அதிதி', symbol: 'அம்பு கூடு', quality: 'புத்துணர்வு', career: 'ஆசிரியர், எழுத்தாளர்', lucky_gems: 'புஷ்பராகம்' },
    'பூசம்': { deity: 'பிரஹஸ்பதி', symbol: 'பசு மடி', quality: 'அன்பு, கருணை', career: 'சமூக சேவை', lucky_gems: 'நீலம்' },
    'ஆயில்யம்': { deity: 'சர்ப்பம்', symbol: 'பாம்பு', quality: 'புத்திசாலித்தனம்', career: 'மருந்து, ஆராய்ச்சி', lucky_gems: 'வைடூர்யம்' },
    'மகம்': { deity: 'பிதுர்கள்', symbol: 'அரியணை', quality: 'தலைமை', career: 'அரசியல், நிர்வாகம்', lucky_gems: 'மாணிக்கம்' },
    'பூரம்': { deity: 'பகன்', symbol: 'கட்டில்', quality: 'சுகம்', career: 'கலை, பொழுதுபோக்கு', lucky_gems: 'வைரம்' },
    'உத்திரம்': { deity: 'சூரியன்', symbol: 'படுக்கை', quality: 'நிலைத்தன்மை', career: 'அரசு வேலை', lucky_gems: 'மாணிக்கம்' },
    'அஸ்தம்': { deity: 'சூரியன்', symbol: 'கை', quality: 'திறமை', career: 'கைவினை, தொழில்நுட்பம்', lucky_gems: 'மரகதம்' },
    'சித்திரை': { deity: 'விஸ்வகர்மா', symbol: 'முத்து', quality: 'படைப்பாற்றல்', career: 'கட்டிடக்கலை, வடிவமைப்பு', lucky_gems: 'வைடூர்யம்' },
    'சுவாதி': { deity: 'வாயு', symbol: 'பவளம்', quality: 'சுதந்திரம்', career: 'வணிகம், வர்த்தகம்', lucky_gems: 'கோமேதகம்' },
    'விசாகம்': { deity: 'இந்திராக்னி', symbol: 'தோரணம்', quality: 'லட்சியம்', career: 'ஆராய்ச்சி, அரசியல்', lucky_gems: 'புஷ்பராகம்' },
    'அனுஷம்': { deity: 'மித்ரன்', symbol: 'குடை', quality: 'நட்பு', career: 'வெளியுறவு, பேச்சுவார்த்தை', lucky_gems: 'நீலம்' },
    'கேட்டை': { deity: 'இந்திரன்', symbol: 'குண்டலம்', quality: 'அதிகாரம்', career: 'நிர்வாகம், தலைமை', lucky_gems: 'வைடூர்யம்' },
    'மூலம்': { deity: 'நிர்ருதி', symbol: 'வேர்', quality: 'ஆராய்ச்சி', career: 'மருத்துவம், ஆராய்ச்சி', lucky_gems: 'வைடூர்யம்' },
    'பூராடம்': { deity: 'அபஹ்', symbol: 'யானை தந்தம்', quality: 'வெற்றி', career: 'கலை, ஊடகம்', lucky_gems: 'வைரம்' },
    'உத்திராடம்': { deity: 'விஸ்வதேவர்', symbol: 'யானை தந்தம்', quality: 'நேர்மை', career: 'சட்டம், நீதி', lucky_gems: 'மாணிக்கம்' },
    'திருவோணம்': { deity: 'விஷ்ணு', symbol: 'காதுகள்', quality: 'கேட்டறிதல்', career: 'ஊடகம், தொலைத்தொடர்பு', lucky_gems: 'முத்து' },
    'அவிட்டம்': { deity: 'வசுக்கள்', symbol: 'முரசு', quality: 'செல்வம்', career: 'வணிகம், நிதி', lucky_gems: 'நீலம்' },
    'சதயம்': { deity: 'வருணன்', symbol: 'வட்டம்', quality: 'குணப்படுத்துதல்', career: 'மருத்துவம்', lucky_gems: 'நீலம்' },
    'பூரட்டாதி': { deity: 'அஜைகபாத்', symbol: 'கட்டில் கால்கள்', quality: 'துறவு', career: 'ஆன்மீகம், தத்துவம்', lucky_gems: 'புஷ்பராகம்' },
    'உத்திரட்டாதி': { deity: 'அஹிர்புத்னியா', symbol: 'இரட்டை முகம்', quality: 'ஞானம்', career: 'ஆசிரியர், ஆலோசகர்', lucky_gems: 'நீலம்' },
    'ரேவதி': { deity: 'பூஷன்', symbol: 'மீன்', quality: 'இரக்கம்', career: 'சமூக சேவை, மருத்துவம்', lucky_gems: 'வைடூர்யம்' },
  },
  kn: {
    'ಅಶ್ವಿನಿ': { deity: 'ಅಶ್ವಿನಿ ಕುಮಾರರು', symbol: 'ಕುದುರೆ ತಲೆ', quality: 'ಚುರುಕುತನ, ವೇಗ', career: 'ವೈದ್ಯಕೀಯ, ಸಾರಿಗೆ', lucky_gems: 'ವೈಡೂರ್ಯ' },
    'ಭರಣಿ': { deity: 'ಯಮ', symbol: 'ಯೋನಿ', quality: 'ಸ್ವಯಂ ನಿಯಂತ್ರಣ', career: 'ನ್ಯಾಯ, ಕಾನೂನು', lucky_gems: 'ವಜ್ರ' },
    'ಕೃತ್ತಿಕಾ': { deity: 'ಅಗ್ನಿ', symbol: 'ಬೆಂಕಿ', quality: 'ತೀವ್ರತೆ, ದೃಢತೆ', career: 'ಸೈನ್ಯ, ಪೊಲೀಸ್', lucky_gems: 'ಮಾಣಿಕ್ಯ' },
    'ರೋಹಿಣಿ': { deity: 'ಬ್ರಹ್ಮ', symbol: 'ಎತ್ತಿನ ಬಂಡಿ', quality: 'ಸೌಂದರ್ಯ, ಕಲೆ', career: 'ಕಲೆ, ಚಲನಚಿತ್ರ', lucky_gems: 'ಮುತ್ತು' },
    'ಮೃಗಶಿರ': { deity: 'ಚಂದ್ರ', symbol: 'ಜಿಂಕೆ ತಲೆ', quality: 'ಸಂಶೋಧನೆ', career: 'ಸಂಶೋಧನೆ, ವಿಜ್ಞಾನ', lucky_gems: 'ಮುತ್ತು' },
    'ಆರ್ದ್ರಾ': { deity: 'ರುದ್ರ', symbol: 'ಕಣ್ಣೀರ ಹನಿ', quality: 'ಆಧ್ಯಾತ್ಮಿಕತೆ', career: 'ಆಧ್ಯಾತ್ಮಿಕ, ಯೋಗ', lucky_gems: 'ಗೋಮೇದಕ' },
    'ಪುನರ್ವಸು': { deity: 'ಅದಿತಿ', symbol: 'ಬಾಣದ ಕೋಶ', quality: 'ಪುನರುಜ್ಜೀವನ', career: 'ಶಿಕ್ಷಕ, ಬರಹಗಾರ', lucky_gems: 'ಪುಷ್ಯರಾಗ' },
    'ಪುಷ್ಯ': { deity: 'ಬೃಹಸ್ಪತಿ', symbol: 'ಹಸುವಿನ ಕೆಚ್ಚಲು', quality: 'ಪ್ರೀತಿ, ಕರುಣೆ', career: 'ಸಮಾಜ ಸೇವೆ', lucky_gems: 'ನೀಲ' },
    'ಆಶ್ಲೇಷಾ': { deity: 'ಸರ್ಪ', symbol: 'ಹಾವು', quality: 'ಬುದ್ಧಿವಂತಿಕೆ', career: 'ಔಷಧ, ಸಂಶೋಧನೆ', lucky_gems: 'ವೈಡೂರ್ಯ' },
    'ಮಘಾ': { deity: 'ಪಿತೃಗಳು', symbol: 'ಸಿಂಹಾಸನ', quality: 'ನಾಯಕತ್ವ', career: 'ರಾಜಕೀಯ, ಆಡಳಿತ', lucky_gems: 'ಮಾಣಿಕ್ಯ' },
    'ಪೂರ್ವಫಾಲ್ಗುಣಿ': { deity: 'ಭಗ', symbol: 'ಮಂಚ', quality: 'ಸುಖ', career: 'ಕಲೆ, ಮನೋರಂಜನೆ', lucky_gems: 'ವಜ್ರ' },
    'ಉತ್ತರಫಾಲ್ಗುಣಿ': { deity: 'ಸೂರ್ಯ', symbol: 'ಹಾಸಿಗೆ', quality: 'ಸ್ಥಿರತೆ', career: 'ಸರ್ಕಾರಿ ಕೆಲಸ', lucky_gems: 'ಮಾಣಿಕ್ಯ' },
    'ಹಸ್ತ': { deity: 'ಸೂರ್ಯ', symbol: 'ಕೈ', quality: 'ಕೌಶಲ್ಯ', career: 'ಕರಕುಶಲ, ತಂತ್ರಜ್ಞಾನ', lucky_gems: 'ಪಚ್ಚೆ' },
    'ಚಿತ್ರಾ': { deity: 'ವಿಶ್ವಕರ್ಮ', symbol: 'ಮುತ್ತು', quality: 'ಸೃಜನಶೀಲತೆ', career: 'ವಾಸ್ತುಶಿಲ್ಪ, ವಿನ್ಯಾಸ', lucky_gems: 'ವೈಡೂರ್ಯ' },
    'ಸ್ವಾತಿ': { deity: 'ವಾಯು', symbol: 'ಹವಳ', quality: 'ಸ್ವಾತಂತ್ರ್ಯ', career: 'ವ್ಯಾಪಾರ, ವಾಣಿಜ್ಯ', lucky_gems: 'ಗೋಮೇದಕ' },
    'ವಿಶಾಖ': { deity: 'ಇಂದ್ರಾಗ್ನಿ', symbol: 'ತೋರಣ', quality: 'ಮಹತ್ವಾಕಾಂಕ್ಷೆ', career: 'ಸಂಶೋಧನೆ, ರಾಜಕೀಯ', lucky_gems: 'ಪುಷ್ಯರಾಗ' },
    'ಅನುರಾಧಾ': { deity: 'ಮಿತ್ರ', symbol: 'ಛತ್ರಿ', quality: 'ಸ್ನೇಹ', career: 'ರಾಜತಾಂತ್ರಿಕ, ಮಾತುಕತೆ', lucky_gems: 'ನೀಲ' },
    'ಜ್ಯೇಷ್ಠಾ': { deity: 'ಇಂದ್ರ', symbol: 'ಕುಂಡಲ', quality: 'ಅಧಿಕಾರ', career: 'ಆಡಳಿತ, ನಾಯಕತ್ವ', lucky_gems: 'ವೈಡೂರ್ಯ' },
    'ಮೂಲ': { deity: 'ನಿರೃತಿ', symbol: 'ಬೇರು', quality: 'ಸಂಶೋಧನೆ', career: 'ವೈದ್ಯಕೀಯ, ಸಂಶೋಧನೆ', lucky_gems: 'ವೈಡೂರ್ಯ' },
    'ಪೂರ್ವಾಷಾಢ': { deity: 'ಅಪಹ್', symbol: 'ಆನೆ ದಂತ', quality: 'ವಿಜಯ', career: 'ಕಲೆ, ಮಾಧ್ಯಮ', lucky_gems: 'ವಜ್ರ' },
    'ಉತ್ತರಾಷಾಢ': { deity: 'ವಿಶ್ವದೇವರು', symbol: 'ಆನೆ ದಂತ', quality: 'ಪ್ರಾಮಾಣಿಕತೆ', career: 'ಕಾನೂನು, ನ್ಯಾಯ', lucky_gems: 'ಮಾಣಿಕ್ಯ' },
    'ಶ್ರವಣ': { deity: 'ವಿಷ್ಣು', symbol: 'ಕಿವಿಗಳು', quality: 'ಕೇಳುವಿಕೆ', career: 'ಮಾಧ್ಯಮ, ದೂರಸಂಪರ್ಕ', lucky_gems: 'ಮುತ್ತು' },
    'ಧನಿಷ್ಠಾ': { deity: 'ವಸುಗಳು', symbol: 'ಮೃದಂಗ', quality: 'ಸಂಪತ್ತು', career: 'ವ್ಯಾಪಾರ, ಹಣಕಾಸು', lucky_gems: 'ನೀಲ' },
    'ಶತಭಿಷಾ': { deity: 'ವರುಣ', symbol: 'ವೃತ್ತ', quality: 'ಗುಣಪಡಿಸುವಿಕೆ', career: 'ವೈದ್ಯಕೀಯ', lucky_gems: 'ನೀಲ' },
    'ಪೂರ್ವಾಭಾದ್ರ': { deity: 'ಅಜೈಕಪಾದ', symbol: 'ಮಂಚದ ಕಾಲುಗಳು', quality: 'ತ್ಯಾಗ', career: 'ಆಧ್ಯಾತ್ಮಿಕ, ತತ್ವಶಾಸ್ತ್ರ', lucky_gems: 'ಪುಷ್ಯರಾಗ' },
    'ಉತ್ತರಾಭಾದ್ರ': { deity: 'ಅಹಿರ್ಬುಧ್ನ್ಯ', symbol: 'ಎರಡು ಮುಖ', quality: 'ಜ್ಞಾನ', career: 'ಶಿಕ್ಷಕ, ಸಲಹೆಗಾರ', lucky_gems: 'ನೀಲ' },
    'ರೇವತಿ': { deity: 'ಪೂಷನ್', symbol: 'ಮೀನು', quality: 'ಕರುಣೆ', career: 'ಸಮಾಜ ಸೇವೆ, ವೈದ್ಯಕೀಯ', lucky_gems: 'ವೈಡೂರ್ಯ' },
  },
  en: {
    'Ashwini': { deity: 'Ashwini Kumaras', symbol: 'Horse Head', quality: 'Speed, Agility', career: 'Medicine, Transport', lucky_gems: 'Cat\'s Eye' },
    'Bharani': { deity: 'Yama', symbol: 'Yoni', quality: 'Self-control', career: 'Justice, Law', lucky_gems: 'Diamond' },
    'Krittika': { deity: 'Agni', symbol: 'Fire', quality: 'Intensity, Determination', career: 'Military, Police', lucky_gems: 'Ruby' },
    'Rohini': { deity: 'Brahma', symbol: 'Ox Cart', quality: 'Beauty, Art', career: 'Arts, Cinema', lucky_gems: 'Pearl' },
    'Mrigashira': { deity: 'Moon', symbol: 'Deer Head', quality: 'Research', career: 'Research, Science', lucky_gems: 'Pearl' },
    'Ardra': { deity: 'Rudra', symbol: 'Teardrop', quality: 'Spirituality', career: 'Spirituality, Yoga', lucky_gems: 'Hessonite' },
    'Punarvasu': { deity: 'Aditi', symbol: 'Quiver', quality: 'Renewal', career: 'Teaching, Writing', lucky_gems: 'Yellow Sapphire' },
    'Pushya': { deity: 'Brihaspati', symbol: 'Cow Udder', quality: 'Love, Compassion', career: 'Social Service', lucky_gems: 'Blue Sapphire' },
    'Ashlesha': { deity: 'Serpent', symbol: 'Snake', quality: 'Intelligence', career: 'Medicine, Research', lucky_gems: 'Cat\'s Eye' },
    'Magha': { deity: 'Pitrus', symbol: 'Throne', quality: 'Leadership', career: 'Politics, Administration', lucky_gems: 'Ruby' },
    'Purva Phalguni': { deity: 'Bhaga', symbol: 'Bed', quality: 'Comfort', career: 'Arts, Entertainment', lucky_gems: 'Diamond' },
    'Uttara Phalguni': { deity: 'Sun', symbol: 'Bed', quality: 'Stability', career: 'Government Jobs', lucky_gems: 'Ruby' },
    'Hasta': { deity: 'Sun', symbol: 'Hand', quality: 'Skill', career: 'Crafts, Technology', lucky_gems: 'Emerald' },
    'Chitra': { deity: 'Vishwakarma', symbol: 'Pearl', quality: 'Creativity', career: 'Architecture, Design', lucky_gems: 'Cat\'s Eye' },
    'Swati': { deity: 'Vayu', symbol: 'Coral', quality: 'Freedom', career: 'Business, Commerce', lucky_gems: 'Hessonite' },
    'Vishakha': { deity: 'Indragni', symbol: 'Archway', quality: 'Ambition', career: 'Research, Politics', lucky_gems: 'Yellow Sapphire' },
    'Anuradha': { deity: 'Mitra', symbol: 'Umbrella', quality: 'Friendship', career: 'Diplomacy, Negotiation', lucky_gems: 'Blue Sapphire' },
    'Jyeshtha': { deity: 'Indra', symbol: 'Earring', quality: 'Authority', career: 'Administration, Leadership', lucky_gems: 'Cat\'s Eye' },
    'Mula': { deity: 'Nirriti', symbol: 'Root', quality: 'Research', career: 'Medicine, Research', lucky_gems: 'Cat\'s Eye' },
    'Purva Ashadha': { deity: 'Apah', symbol: 'Elephant Tusk', quality: 'Victory', career: 'Arts, Media', lucky_gems: 'Diamond' },
    'Uttara Ashadha': { deity: 'Vishwadevas', symbol: 'Elephant Tusk', quality: 'Honesty', career: 'Law, Justice', lucky_gems: 'Ruby' },
    'Shravana': { deity: 'Vishnu', symbol: 'Ears', quality: 'Listening', career: 'Media, Telecom', lucky_gems: 'Pearl' },
    'Dhanishta': { deity: 'Vasus', symbol: 'Drum', quality: 'Wealth', career: 'Business, Finance', lucky_gems: 'Blue Sapphire' },
    'Shatabhisha': { deity: 'Varuna', symbol: 'Circle', quality: 'Healing', career: 'Medicine', lucky_gems: 'Blue Sapphire' },
    'Purva Bhadrapada': { deity: 'Ajaikapada', symbol: 'Bed Legs', quality: 'Renunciation', career: 'Spirituality, Philosophy', lucky_gems: 'Yellow Sapphire' },
    'Uttara Bhadrapada': { deity: 'Ahirbudhnya', symbol: 'Two Faces', quality: 'Wisdom', career: 'Teaching, Counseling', lucky_gems: 'Blue Sapphire' },
    'Revati': { deity: 'Pushan', symbol: 'Fish', quality: 'Compassion', career: 'Social Service, Medicine', lucky_gems: 'Cat\'s Eye' },
  }
};

// Legacy Tamil constant for backward compatibility
const NAKSHATRA_DETAILS = NAKSHATRA_DETAILS_ML.ta;

// Multi-language Rasi details
const RASI_DETAILS_ML = {
  ta: {
    'மேஷம்': { element: 'நெருப்பு', ruler: 'செவ்வாய்', quality: 'தலைமை, துணிச்சல்', lucky_color: 'சிவப்பு', lucky_number: '9', career: 'ராணுவம், விளையாட்டு, தொழில்முனைவு' },
    'ரிஷபம்': { element: 'பூமி', ruler: 'சுக்கிரன்', quality: 'நிலைத்தன்மை, அழகு', lucky_color: 'வெள்ளை', lucky_number: '6', career: 'கலை, நிதி, வேளாண்மை' },
    'மிதுனம்': { element: 'காற்று', ruler: 'புதன்', quality: 'புத்திசாலித்தனம், தொடர்பு', lucky_color: 'பச்சை', lucky_number: '5', career: 'எழுத்து, ஊடகம், வணிகம்' },
    'கடகம்': { element: 'நீர்', ruler: 'சந்திரன்', quality: 'அன்பு, பாதுகாப்பு', lucky_color: 'வெள்ளை', lucky_number: '2', career: 'வீடு, உணவு, மருத்துவம்' },
    'சிம்மம்': { element: 'நெருப்பு', ruler: 'சூரியன்', quality: 'தலைமை, கம்பீரம்', lucky_color: 'தங்கம்', lucky_number: '1', career: 'அரசியல், நிர்வாகம், கலை' },
    'கன்னி': { element: 'பூமி', ruler: 'புதன்', quality: 'பகுப்பாய்வு, சேவை', lucky_color: 'பச்சை', lucky_number: '5', career: 'மருத்துவம், கணக்கியல், ஆராய்ச்சி' },
    'துலாம்': { element: 'காற்று', ruler: 'சுக்கிரன்', quality: 'சமநிலை, அழகு', lucky_color: 'நீலம்', lucky_number: '6', career: 'சட்டம், கலை, வெளியுறவு' },
    'விருச்சிகம்': { element: 'நீர்', ruler: 'செவ்வாய்', quality: 'ஆழ்ந்த சிந்தனை, மாற்றம்', lucky_color: 'சிவப்பு', lucky_number: '9', career: 'ஆராய்ச்சி, மருத்துவம், உளவியல்' },
    'தனுசு': { element: 'நெருப்பு', ruler: 'குரு', quality: 'ஞானம், பயணம்', lucky_color: 'மஞ்சள்', lucky_number: '3', career: 'கல்வி, சட்டம், பயணம்' },
    'மகரம்': { element: 'பூமி', ruler: 'சனி', quality: 'உழைப்பு, பொறுப்பு', lucky_color: 'கருப்பு', lucky_number: '8', career: 'அரசு, நிர்வாகம், கட்டுமானம்' },
    'கும்பம்': { element: 'காற்று', ruler: 'சனி', quality: 'புதுமை, சமூக சேவை', lucky_color: 'நீலம்', lucky_number: '8', career: 'தொழில்நுட்பம், சமூக சேவை, அறிவியல்' },
    'மீனம்': { element: 'நீர்', ruler: 'குரு', quality: 'இரக்கம், கற்பனை', lucky_color: 'மஞ்சள்', lucky_number: '3', career: 'கலை, ஆன்மீகம், மருத்துவம்' },
  },
  kn: {
    'ಮೇಷ': { element: 'ಅಗ್ನಿ', ruler: 'ಕುಜ', quality: 'ನಾಯಕತ್ವ, ಧೈರ್ಯ', lucky_color: 'ಕೆಂಪು', lucky_number: '9', career: 'ಸೈನ್ಯ, ಕ್ರೀಡೆ, ಉದ್ಯಮ' },
    'ವೃಷಭ': { element: 'ಭೂಮಿ', ruler: 'ಶುಕ್ರ', quality: 'ಸ್ಥಿರತೆ, ಸೌಂದರ್ಯ', lucky_color: 'ಬಿಳಿ', lucky_number: '6', career: 'ಕಲೆ, ಹಣಕಾಸು, ಕೃಷಿ' },
    'ಮಿಥುನ': { element: 'ವಾಯು', ruler: 'ಬುಧ', quality: 'ಬುದ್ಧಿವಂತಿಕೆ, ಸಂವಹನ', lucky_color: 'ಹಸಿರು', lucky_number: '5', career: 'ಬರವಣಿಗೆ, ಮಾಧ್ಯಮ, ವ್ಯಾಪಾರ' },
    'ಕರ್ಕಾಟಕ': { element: 'ನೀರು', ruler: 'ಚಂದ್ರ', quality: 'ಪ್ರೀತಿ, ರಕ್ಷಣೆ', lucky_color: 'ಬಿಳಿ', lucky_number: '2', career: 'ಮನೆ, ಆಹಾರ, ವೈದ್ಯಕೀಯ' },
    'ಸಿಂಹ': { element: 'ಅಗ್ನಿ', ruler: 'ಸೂರ್ಯ', quality: 'ನಾಯಕತ್ವ, ಗಾಂಭೀರ್ಯ', lucky_color: 'ಚಿನ್ನ', lucky_number: '1', career: 'ರಾಜಕೀಯ, ಆಡಳಿತ, ಕಲೆ' },
    'ಕನ್ಯಾ': { element: 'ಭೂಮಿ', ruler: 'ಬುಧ', quality: 'ವಿಶ್ಲೇಷಣೆ, ಸೇವೆ', lucky_color: 'ಹಸಿರು', lucky_number: '5', career: 'ವೈದ್ಯಕೀಯ, ಲೆಕ್ಕಪತ್ರ, ಸಂಶೋಧನೆ' },
    'ತುಲಾ': { element: 'ವಾಯು', ruler: 'ಶುಕ್ರ', quality: 'ಸಮತೋಲನ, ಸೌಂದರ್ಯ', lucky_color: 'ನೀಲಿ', lucky_number: '6', career: 'ಕಾನೂನು, ಕಲೆ, ರಾಜತಾಂತ್ರಿಕ' },
    'ವೃಶ್ಚಿಕ': { element: 'ನೀರು', ruler: 'ಕುಜ', quality: 'ಆಳವಾದ ಚಿಂತನೆ, ಬದಲಾವಣೆ', lucky_color: 'ಕೆಂಪು', lucky_number: '9', career: 'ಸಂಶೋಧನೆ, ವೈದ್ಯಕೀಯ, ಮನೋವಿಜ್ಞಾನ' },
    'ಧನು': { element: 'ಅಗ್ನಿ', ruler: 'ಗುರು', quality: 'ಜ್ಞಾನ, ಪ್ರಯಾಣ', lucky_color: 'ಹಳದಿ', lucky_number: '3', career: 'ಶಿಕ್ಷಣ, ಕಾನೂನು, ಪ್ರಯಾಣ' },
    'ಮಕರ': { element: 'ಭೂಮಿ', ruler: 'ಶನಿ', quality: 'ಪರಿಶ್ರಮ, ಜವಾಬ್ದಾರಿ', lucky_color: 'ಕಪ್ಪು', lucky_number: '8', career: 'ಸರ್ಕಾರ, ಆಡಳಿತ, ನಿರ್ಮಾಣ' },
    'ಕುಂಭ': { element: 'ವಾಯು', ruler: 'ಶನಿ', quality: 'ಹೊಸತನ, ಸಮಾಜ ಸೇವೆ', lucky_color: 'ನೀಲಿ', lucky_number: '8', career: 'ತಂತ್ರಜ್ಞಾನ, ಸಮಾಜ ಸೇವೆ, ವಿಜ್ಞಾನ' },
    'ಮೀನ': { element: 'ನೀರು', ruler: 'ಗುರು', quality: 'ಕರುಣೆ, ಕಲ್ಪನೆ', lucky_color: 'ಹಳದಿ', lucky_number: '3', career: 'ಕಲೆ, ಆಧ್ಯಾತ್ಮಿಕ, ವೈದ್ಯಕೀಯ' },
  },
  en: {
    'Aries': { element: 'Fire', ruler: 'Mars', quality: 'Leadership, Courage', lucky_color: 'Red', lucky_number: '9', career: 'Military, Sports, Entrepreneurship' },
    'Taurus': { element: 'Earth', ruler: 'Venus', quality: 'Stability, Beauty', lucky_color: 'White', lucky_number: '6', career: 'Arts, Finance, Agriculture' },
    'Gemini': { element: 'Air', ruler: 'Mercury', quality: 'Intelligence, Communication', lucky_color: 'Green', lucky_number: '5', career: 'Writing, Media, Business' },
    'Cancer': { element: 'Water', ruler: 'Moon', quality: 'Love, Protection', lucky_color: 'White', lucky_number: '2', career: 'Home, Food, Medicine' },
    'Leo': { element: 'Fire', ruler: 'Sun', quality: 'Leadership, Majesty', lucky_color: 'Gold', lucky_number: '1', career: 'Politics, Administration, Arts' },
    'Virgo': { element: 'Earth', ruler: 'Mercury', quality: 'Analysis, Service', lucky_color: 'Green', lucky_number: '5', career: 'Medicine, Accounting, Research' },
    'Libra': { element: 'Air', ruler: 'Venus', quality: 'Balance, Beauty', lucky_color: 'Blue', lucky_number: '6', career: 'Law, Arts, Diplomacy' },
    'Scorpio': { element: 'Water', ruler: 'Mars', quality: 'Deep Thinking, Transformation', lucky_color: 'Red', lucky_number: '9', career: 'Research, Medicine, Psychology' },
    'Sagittarius': { element: 'Fire', ruler: 'Jupiter', quality: 'Wisdom, Travel', lucky_color: 'Yellow', lucky_number: '3', career: 'Education, Law, Travel' },
    'Capricorn': { element: 'Earth', ruler: 'Saturn', quality: 'Hard Work, Responsibility', lucky_color: 'Black', lucky_number: '8', career: 'Government, Administration, Construction' },
    'Aquarius': { element: 'Air', ruler: 'Saturn', quality: 'Innovation, Social Service', lucky_color: 'Blue', lucky_number: '8', career: 'Technology, Social Service, Science' },
    'Pisces': { element: 'Water', ruler: 'Jupiter', quality: 'Compassion, Imagination', lucky_color: 'Yellow', lucky_number: '3', career: 'Arts, Spirituality, Medicine' },
  }
};

// Legacy Tamil constant for backward compatibility
const RASI_DETAILS = RASI_DETAILS_ML.ta;

// Yoga definitions with effects and timing
const YOGA_DEFINITIONS = {
  'Gajakesari Yoga': {
    tamil: 'கஜகேசரி யோகம்',
    formation: 'குரு சந்திரனிலிருந்து கேந்திரத்தில் இருக்கும்போது',
    effects: ['புகழ் மற்றும் அங்கீகாரம்', 'நல்ல சொத்துக்கள்', 'அறிவு மற்றும் ஞானம்', 'சமூகத்தில் மரியாதை'],
    activation: 'குரு அல்லது சந்திர தசையில் செயல்படும்',
    strength_factors: ['குரு பலம்', 'சந்திர பலம்', 'கேந்திர அதிபதித்துவம்'],
  },
  'Lakshmi Yoga': {
    tamil: 'லக்ஷ்மி யோகம்',
    formation: 'சுக்கிரன் சுபஸ்தானத்தில் பலமாக இருக்கும்போது',
    effects: ['செல்வம் மற்றும் வளம்', 'அழகு மற்றும் கவர்ச்சி', 'இல்ல சுகம்', 'கலை திறமை'],
    activation: 'சுக்கிர தசையில் முழுமையாக செயல்படும்',
    strength_factors: ['சுக்கிர பலம்', '2ம், 7ம் வீட்டு தொடர்பு'],
  },
  'Raja Yoga': {
    tamil: 'ராஜ யோகம்',
    formation: 'கேந்திர-திரிகோண அதிபதிகள் இணையும்போது',
    effects: ['அதிகாரம் மற்றும் பதவி', 'சமூக அந்தஸ்து', 'தலைமைத் திறன்', 'வெற்றி'],
    activation: 'சம்பந்தப்பட்ட கிரக தசையில் செயல்படும்',
    strength_factors: ['கேந்திர அதிபதித்துவம்', 'திரிகோண அதிபதித்துவம்'],
  },
  'Dhana Yoga': {
    tamil: 'தன யோகம்',
    formation: '2ம், 11ம் வீட்டு அதிபதிகள் இணையும்போது',
    effects: ['நிதி வளர்ச்சி', 'சொத்து சேர்க்கை', 'வருமான அதிகரிப்பு', 'வணிக வெற்றி'],
    activation: '2ம் அல்லது 11ம் அதிபதி தசையில் செயல்படும்',
    strength_factors: ['2ம் வீட்டு பலம்', '11ம் வீட்டு பலம்'],
  },
  'Budhaditya Yoga': {
    tamil: 'புதாதித்ய யோகம்',
    formation: 'சூரியன் மற்றும் புதன் ஒரே வீட்டில்',
    effects: ['அறிவு மற்றும் புத்திசாலித்தனம்', 'பேச்சு திறமை', 'கணித திறன்', 'வணிக புத்தி'],
    activation: 'சூரிய அல்லது புத மதசையில் செயல்படும்',
    strength_factors: ['சூரிய பலம்', 'புத பலம்', 'வீட்டு நிலை'],
  },
  'Hamsa Yoga': {
    tamil: 'ஹம்ச யோகம்',
    formation: 'குரு லக்னம், 4ம், 7ம், 10ம் வீட்டில் சொந்த அல்லது உச்ச நிலையில்',
    effects: ['ஆன்மீக வளர்ச்சி', 'கல்வியில் சிறப்பு', 'நற்பண்புகள்', 'மரியாதை'],
    activation: 'குரு தசையில் முழுமையாக செயல்படும்',
    strength_factors: ['குரு பலம்', 'கேந்திர நிலை'],
  },
  'Malavya Yoga': {
    tamil: 'மாளவ்ய யோகம்',
    formation: 'சுக்கிரன் கேந்திரத்தில் சொந்த அல்லது உச்ச நிலையில்',
    effects: ['அழகு மற்றும் கவர்ச்சி', 'சுக வாழ்க்கை', 'கலை திறமை', 'வாகன யோகம்'],
    activation: 'சுக்கிர தசையில் முழுமையாக செயல்படும்',
    strength_factors: ['சுக்கிர பலம்', 'கேந்திர நிலை'],
  },
  'Ruchaka Yoga': {
    tamil: 'ருசக யோகம்',
    formation: 'செவ்வாய் கேந்திரத்தில் சொந்த அல்லது உச்ச நிலையில்',
    effects: ['துணிச்சல் மற்றும் வீரம்', 'தலைமைத் திறன்', 'நிலம் சேர்க்கை', 'அதிகாரம்'],
    activation: 'செவ்வாய் தசையில் முழுமையாக செயல்படும்',
    strength_factors: ['செவ்வாய் பலம்', 'கேந்திர நிலை'],
  },
  'Shasha Yoga': {
    tamil: 'சச யோகம்',
    formation: 'சனி கேந்திரத்தில் சொந்த அல்லது உச்ச நிலையில்',
    effects: ['அதிகாரம் மற்றும் பதவி', 'பொறுமை', 'நீண்ட ஆயுள்', 'செல்வம்'],
    activation: 'சனி தசையில் முழுமையாக செயல்படும்',
    strength_factors: ['சனி பலம்', 'கேந்திர நிலை'],
  },
  'Bhadra Yoga': {
    tamil: 'பத்ர யோகம்',
    formation: 'புதன் கேந்திரத்தில் சொந்த அல்லது உச்ச நிலையில்',
    effects: ['புத்திசாலித்தனம்', 'பேச்சு திறமை', 'வணிக வெற்றி', 'நல்ல ஆரோக்கியம்'],
    activation: 'புத தசையில் முழுமையாக செயல்படும்',
    strength_factors: ['புத பலம்', 'கேந்திர நிலை'],
  },
};

// Multi-language House significations
const HOUSE_MEANINGS_ML = {
  ta: {
    1: { name: 'லக்னம்', areas: ['உடல் ஆரோக்கியம்', 'தன்னம்பிக்கை', 'தோற்றம்', 'ஆளுமை'] },
    2: { name: 'தன ஸ்தானம்', areas: ['குடும்பம்', 'செல்வம்', 'பேச்சு', 'உணவு'] },
    3: { name: 'சகோதர ஸ்தானம்', areas: ['சகோதரர்கள்', 'துணிச்சல்', 'குறுகிய பயணம்', 'தொடர்பு'] },
    4: { name: 'சுக ஸ்தானம்', areas: ['தாய்', 'வீடு', 'வாகனம்', 'நிம்மதி'] },
    5: { name: 'புத்திர ஸ்தானம்', areas: ['குழந்தைகள்', 'கல்வி', 'படைப்பாற்றல்', 'காதல்'] },
    6: { name: 'சத்ரு ஸ்தானம்', areas: ['எதிரிகள்', 'நோய்', 'கடன்', 'வேலை'] },
    7: { name: 'களத்திர ஸ்தானம்', areas: ['திருமணம்', 'வாழ்க்கைத் துணை', 'வணிக பங்காளி', 'பொது உறவுகள்'] },
    8: { name: 'ஆயுள் ஸ்தானம்', areas: ['ஆயுள்', 'மறைவான விஷயங்கள்', 'மரபு சொத்து', 'மாற்றம்'] },
    9: { name: 'பாக்கிய ஸ்தானம்', areas: ['அதிர்ஷ்டம்', 'தந்தை', 'ஆன்மீகம்', 'நீண்ட பயணம்'] },
    10: { name: 'கர்ம ஸ்தானம்', areas: ['தொழில்', 'அந்தஸ்து', 'அரசு', 'புகழ்'] },
    11: { name: 'லாப ஸ்தானம்', areas: ['வருமானம்', 'நண்பர்கள்', 'ஆசைகள்', 'மூத்த சகோதரர்'] },
    12: { name: 'விரய ஸ்தானம்', areas: ['செலவு', 'வெளிநாடு', 'ஆன்மீகம்', 'படுக்கை சுகம்'] },
  },
  kn: {
    1: { name: 'ಲಗ್ನ', areas: ['ದೇಹ ಆರೋಗ್ಯ', 'ಆತ್ಮವಿಶ್ವಾಸ', 'ನೋಟ', 'ವ್ಯಕ್ತಿತ್ವ'] },
    2: { name: 'ಧನ ಸ್ಥಾನ', areas: ['ಕುಟುಂಬ', 'ಸಂಪತ್ತು', 'ಮಾತು', 'ಆಹಾರ'] },
    3: { name: 'ಸಹೋದರ ಸ್ಥಾನ', areas: ['ಸಹೋದರರು', 'ಧೈರ್ಯ', 'ಕಿರು ಪ್ರಯಾಣ', 'ಸಂವಹನ'] },
    4: { name: 'ಸುಖ ಸ್ಥಾನ', areas: ['ತಾಯಿ', 'ಮನೆ', 'ವಾಹನ', 'ನೆಮ್ಮದಿ'] },
    5: { name: 'ಪುತ್ರ ಸ್ಥಾನ', areas: ['ಮಕ್ಕಳು', 'ಶಿಕ್ಷಣ', 'ಸೃಜನಶೀಲತೆ', 'ಪ್ರೇಮ'] },
    6: { name: 'ಶತ್ರು ಸ್ಥಾನ', areas: ['ಶತ್ರುಗಳು', 'ರೋಗ', 'ಸಾಲ', 'ಕೆಲಸ'] },
    7: { name: 'ಕಳತ್ರ ಸ್ಥಾನ', areas: ['ವಿವಾಹ', 'ಜೀವನ ಸಂಗಾತಿ', 'ವ್ಯಾಪಾರ ಪಾಲುದಾರ', 'ಸಾರ್ವಜನಿಕ ಸಂಬಂಧ'] },
    8: { name: 'ಆಯುಷ್ಯ ಸ್ಥಾನ', areas: ['ಆಯುಷ್ಯ', 'ಗುಪ್ತ ವಿಷಯಗಳು', 'ಪಿತ್ರಾರ್ಜಿತ ಆಸ್ತಿ', 'ಪರಿವರ್ತನೆ'] },
    9: { name: 'ಭಾಗ್ಯ ಸ್ಥಾನ', areas: ['ಅದೃಷ್ಟ', 'ತಂದೆ', 'ಆಧ್ಯಾತ್ಮಿಕ', 'ದೂರ ಪ್ರಯಾಣ'] },
    10: { name: 'ಕರ್ಮ ಸ್ಥಾನ', areas: ['ವೃತ್ತಿ', 'ಸ್ಥಾನಮಾನ', 'ಸರ್ಕಾರ', 'ಕೀರ್ತಿ'] },
    11: { name: 'ಲಾಭ ಸ್ಥಾನ', areas: ['ಆದಾಯ', 'ಸ್ನೇಹಿತರು', 'ಆಸೆಗಳು', 'ಹಿರಿಯ ಸಹೋದರ'] },
    12: { name: 'ವ್ಯಯ ಸ್ಥಾನ', areas: ['ವೆಚ್ಚ', 'ವಿದೇಶ', 'ಆಧ್ಯಾತ್ಮಿಕ', 'ಹಾಸಿಗೆ ಸುಖ'] },
  },
  en: {
    1: { name: 'Ascendant', areas: ['Physical Health', 'Self-confidence', 'Appearance', 'Personality'] },
    2: { name: 'Wealth House', areas: ['Family', 'Wealth', 'Speech', 'Food'] },
    3: { name: 'Sibling House', areas: ['Siblings', 'Courage', 'Short Travel', 'Communication'] },
    4: { name: 'Happiness House', areas: ['Mother', 'Home', 'Vehicle', 'Peace'] },
    5: { name: 'Children House', areas: ['Children', 'Education', 'Creativity', 'Romance'] },
    6: { name: 'Enemy House', areas: ['Enemies', 'Disease', 'Debt', 'Work'] },
    7: { name: 'Marriage House', areas: ['Marriage', 'Life Partner', 'Business Partner', 'Public Relations'] },
    8: { name: 'Longevity House', areas: ['Longevity', 'Hidden Matters', 'Inheritance', 'Transformation'] },
    9: { name: 'Fortune House', areas: ['Luck', 'Father', 'Spirituality', 'Long Travel'] },
    10: { name: 'Career House', areas: ['Profession', 'Status', 'Government', 'Fame'] },
    11: { name: 'Gains House', areas: ['Income', 'Friends', 'Desires', 'Elder Siblings'] },
    12: { name: 'Expense House', areas: ['Expenses', 'Foreign Lands', 'Spirituality', 'Bed Pleasures'] },
  }
};

// Legacy Tamil constant for backward compatibility
const HOUSE_MEANINGS = HOUSE_MEANINGS_ML.ta;

// Multi-language Dasha predictions by planet
const DASHA_PREDICTIONS_ML = {
  ta: {
    'சூரியன்': {
      positive: ['அரசு வேலை', 'தந்தையின் ஆசி', 'புகழ்', 'தலைமை பதவி', 'ஆரோக்கியம்'],
      challenges: ['அகந்தை', 'அதிகாரிகளுடன் மோதல்', 'கண் பிரச்சனை'],
      remedies: ['சூரிய வழிபாடு', 'ஆதித்ய ஹ்ருதயம்', 'சிவப்பு உடை ஞாயிறு'],
    },
    'சந்திரன்': {
      positive: ['மன நிம்மதி', 'தாயின் ஆசி', 'புதிய வீடு', 'நல்ல உறவுகள்', 'கற்பனை திறன்'],
      challenges: ['மன அழுத்தம்', 'நிலையின்மை', 'குளிர் சம்பந்த நோய்'],
      remedies: ['சந்திர வழிபாடு', 'சிவ வழிபாடு திங்கள்', 'வெள்ளை உடை'],
    },
    'செவ்வாய்': {
      positive: ['துணிச்சல்', 'நிலம் சேர்க்கை', 'சகோதர உதவி', 'விளையாட்டு வெற்றி', 'தொழில்நுட்பம்'],
      challenges: ['எடுத்தெறிந்த குணம்', 'விபத்து', 'ரத்த சம்பந்த நோய்'],
      remedies: ['முருகன் வழிபாடு', 'அங்காரக ஸ்தோத்திரம்', 'சிவப்பு உடை செவ்வாய்'],
    },
    'புதன்': {
      positive: ['கல்வி வெற்றி', 'வணிக லாபம்', 'பேச்சு திறமை', 'புதிய தொடர்புகள்', 'எழுத்து'],
      challenges: ['நரம்பு பிரச்சனை', 'தோல் நோய்', 'மன குழப்பம்'],
      remedies: ['விஷ்ணு வழிபாடு', 'புத ஸ்தோத்திரம்', 'பச்சை உடை புதன்'],
    },
    'குரு': {
      positive: ['ஆன்மீக வளர்ச்சி', 'குழந்தை பாக்கியம்', 'கல்வி', 'குரு ஆசி', 'வெளிநாடு'],
      challenges: ['உடல் பருமன்', 'கல்லீரல் பிரச்சனை', 'அதிக நம்பிக்கை'],
      remedies: ['குரு வழிபாடு', 'விஷ்ணு சஹஸ்ரநாமம்', 'மஞ்சள் உடை வியாழன்'],
    },
    'சுக்கிரன்': {
      positive: ['திருமணம்', 'சொகுசு', 'கலை வெற்றி', 'வாகனம்', 'அழகு'],
      challenges: ['சர்க்கரை நோய்', 'சிறுநீரக பிரச்சனை', 'உறவு சிக்கல்'],
      remedies: ['லக்ஷ்மி வழிபாடு', 'சுக்கிர ஸ்தோத்திரம்', 'வெள்ளை உடை வெள்ளி'],
    },
    'சனி': {
      positive: ['அரசு உதவி', 'நீண்டகால லாபம்', 'நிலம்', 'கட்டிடம்', 'பொறுமை'],
      challenges: ['தாமதம்', 'உடல் வலி', 'மன சோர்வு', 'தடைகள்'],
      remedies: ['ஹனுமான் வழிபாடு', 'சனி ஸ்தோத்திரம்', 'கருப்பு/நீலம் உடை சனி'],
    },
    'ராகு': {
      positive: ['திடீர் வெற்றி', 'வெளிநாடு', 'தொழில்நுட்பம்', 'புதுமை', 'ஆராய்ச்சி'],
      challenges: ['குழப்பம்', 'மோசடி', 'தோல் நோய்', 'நஞ்சு பயம்'],
      remedies: ['துர்கா வழிபாடு', 'ராகு ஸ்தோத்திரம்', 'நீலம் உடை சனி'],
    },
    'கேது': {
      positive: ['ஆன்மீகம்', 'மோட்சம்', 'ஆராய்ச்சி', 'மறைவான ஞானம்', 'வைராக்கியம்'],
      challenges: ['திடீர் நஷ்டம்', 'விபத்து', 'மர்மமான நோய்'],
      remedies: ['கணபதி வழிபாடு', 'கேது ஸ்தோத்திரம்', 'சாம்பல் நிற உடை'],
    },
  },
  kn: {
    'ಸೂರ್ಯ': {
      positive: ['ಸರ್ಕಾರಿ ಕೆಲಸ', 'ತಂದೆಯ ಆಶೀರ್ವಾದ', 'ಕೀರ್ತಿ', 'ನಾಯಕತ್ವ ಹುದ್ದೆ', 'ಆರೋಗ್ಯ'],
      challenges: ['ಅಹಂಕಾರ', 'ಅಧಿಕಾರಿಗಳೊಂದಿಗೆ ಘರ್ಷಣೆ', 'ಕಣ್ಣು ಸಮಸ್ಯೆ'],
      remedies: ['ಸೂರ್ಯ ಆರಾಧನೆ', 'ಆದಿತ್ಯ ಹೃದಯಂ', 'ಕೆಂಪು ಬಟ್ಟೆ ಭಾನುವಾರ'],
    },
    'ಚಂದ್ರ': {
      positive: ['ಮಾನಸಿಕ ಶಾಂತಿ', 'ತಾಯಿಯ ಆಶೀರ್ವಾದ', 'ಹೊಸ ಮನೆ', 'ಒಳ್ಳೆಯ ಸಂಬಂಧಗಳು', 'ಕಲ್ಪನಾ ಶಕ್ತಿ'],
      challenges: ['ಮಾನಸಿಕ ಒತ್ತಡ', 'ಅಸ್ಥಿರತೆ', 'ಶೀತ ಸಂಬಂಧಿ ರೋಗ'],
      remedies: ['ಚಂದ್ರ ಆರಾಧನೆ', 'ಶಿವ ಪೂಜೆ ಸೋಮವಾರ', 'ಬಿಳಿ ಬಟ್ಟೆ'],
    },
    'ಕುಜ': {
      positive: ['ಧೈರ್ಯ', 'ಭೂಮಿ ಸಂಪಾದನೆ', 'ಸಹೋದರ ಸಹಾಯ', 'ಕ್ರೀಡೆ ಗೆಲುವು', 'ತಂತ್ರಜ್ಞಾನ'],
      challenges: ['ಕೋಪ', 'ಅಪಘಾತ', 'ರಕ್ತ ಸಂಬಂಧಿ ರೋಗ'],
      remedies: ['ಸುಬ್ರಹ್ಮಣ್ಯ ಆರಾಧನೆ', 'ಅಂಗಾರಕ ಸ್ತೋತ್ರ', 'ಕೆಂಪು ಬಟ್ಟೆ ಮಂಗಳವಾರ'],
    },
    'ಬುಧ': {
      positive: ['ಶಿಕ್ಷಣ ಯಶಸ್ಸು', 'ವ್ಯಾಪಾರ ಲಾಭ', 'ಮಾತಿನ ಕೌಶಲ್ಯ', 'ಹೊಸ ಸಂಪರ್ಕಗಳು', 'ಬರವಣಿಗೆ'],
      challenges: ['ನರ ಸಮಸ್ಯೆ', 'ಚರ್ಮ ರೋಗ', 'ಮಾನಸಿಕ ಗೊಂದಲ'],
      remedies: ['ವಿಷ್ಣು ಆರಾಧನೆ', 'ಬುಧ ಸ್ತೋತ್ರ', 'ಹಸಿರು ಬಟ್ಟೆ ಬುಧವಾರ'],
    },
    'ಗುರು': {
      positive: ['ಆಧ್ಯಾತ್ಮಿಕ ಬೆಳವಣಿಗೆ', 'ಮಕ್ಕಳ ಭಾಗ್ಯ', 'ಶಿಕ್ಷಣ', 'ಗುರು ಆಶೀರ್ವಾದ', 'ವಿದೇಶ'],
      challenges: ['ದೇಹ ಬೊಜ್ಜು', 'ಯಕೃತ್ ಸಮಸ್ಯೆ', 'ಅತಿ ನಂಬಿಕೆ'],
      remedies: ['ಗುರು ಆರಾಧನೆ', 'ವಿಷ್ಣು ಸಹಸ್ರನಾಮ', 'ಹಳದಿ ಬಟ್ಟೆ ಗುರುವಾರ'],
    },
    'ಶುಕ್ರ': {
      positive: ['ವಿವಾಹ', 'ಐಷಾರಾಮ', 'ಕಲೆ ಯಶಸ್ಸು', 'ವಾಹನ', 'ಸೌಂದರ್ಯ'],
      challenges: ['ಮಧುಮೇಹ', 'ಮೂತ್ರಪಿಂಡ ಸಮಸ್ಯೆ', 'ಸಂಬಂಧ ತೊಂದರೆ'],
      remedies: ['ಲಕ್ಷ್ಮಿ ಆರಾಧನೆ', 'ಶುಕ್ರ ಸ್ತೋತ್ರ', 'ಬಿಳಿ ಬಟ್ಟೆ ಶುಕ್ರವಾರ'],
    },
    'ಶನಿ': {
      positive: ['ಸರ್ಕಾರಿ ಸಹಾಯ', 'ದೀರ್ಘಕಾಲಿಕ ಲಾಭ', 'ಭೂಮಿ', 'ಕಟ್ಟಡ', 'ತಾಳ್ಮೆ'],
      challenges: ['ವಿಳಂಬ', 'ದೇಹ ನೋವು', 'ಮಾನಸಿಕ ಆಯಾಸ', 'ಅಡೆತಡೆಗಳು'],
      remedies: ['ಹನುಮಾನ್ ಆರಾಧನೆ', 'ಶನಿ ಸ್ತೋತ್ರ', 'ಕಪ್ಪು/ನೀಲಿ ಬಟ್ಟೆ ಶನಿವಾರ'],
    },
    'ರಾಹು': {
      positive: ['ಆಕಸ್ಮಿಕ ಯಶಸ್ಸು', 'ವಿದೇಶ', 'ತಂತ್ರಜ್ಞಾನ', 'ನಾವೀನ್ಯತೆ', 'ಸಂಶೋಧನೆ'],
      challenges: ['ಗೊಂದಲ', 'ವಂಚನೆ', 'ಚರ್ಮ ರೋಗ', 'ವಿಷ ಭಯ'],
      remedies: ['ದುರ್ಗಾ ಆರಾಧನೆ', 'ರಾಹು ಸ್ತೋತ್ರ', 'ನೀಲಿ ಬಟ್ಟೆ ಶನಿವಾರ'],
    },
    'ಕೇತು': {
      positive: ['ಆಧ್ಯಾತ್ಮಿಕತೆ', 'ಮೋಕ್ಷ', 'ಸಂಶೋಧನೆ', 'ಗುಪ್ತ ಜ್ಞಾನ', 'ವೈರಾಗ್ಯ'],
      challenges: ['ಆಕಸ್ಮಿಕ ನಷ್ಟ', 'ಅಪಘಾತ', 'ರಹಸ್ಯ ರೋಗ'],
      remedies: ['ಗಣಪತಿ ಆರಾಧನೆ', 'ಕೇತು ಸ್ತೋತ್ರ', 'ಬೂದು ಬಣ್ಣ ಬಟ್ಟೆ'],
    },
  },
  en: {
    'Sun': {
      positive: ['Government Job', 'Father\'s Blessing', 'Fame', 'Leadership Position', 'Health'],
      challenges: ['Ego', 'Conflict with Authority', 'Eye Problems'],
      remedies: ['Sun Worship', 'Aditya Hridayam', 'Red Clothes on Sunday'],
    },
    'Moon': {
      positive: ['Mental Peace', 'Mother\'s Blessing', 'New Home', 'Good Relationships', 'Imagination'],
      challenges: ['Mental Stress', 'Instability', 'Cold-related Illness'],
      remedies: ['Moon Worship', 'Shiva Worship on Monday', 'White Clothes'],
    },
    'Mars': {
      positive: ['Courage', 'Land Acquisition', 'Sibling Help', 'Sports Victory', 'Technology'],
      challenges: ['Aggression', 'Accidents', 'Blood-related Disease'],
      remedies: ['Murugan Worship', 'Angaaraka Stotra', 'Red Clothes on Tuesday'],
    },
    'Mercury': {
      positive: ['Education Success', 'Business Profit', 'Speaking Skills', 'New Contacts', 'Writing'],
      challenges: ['Nerve Problems', 'Skin Disease', 'Mental Confusion'],
      remedies: ['Vishnu Worship', 'Budha Stotra', 'Green Clothes on Wednesday'],
    },
    'Jupiter': {
      positive: ['Spiritual Growth', 'Children Blessing', 'Education', 'Guru\'s Grace', 'Foreign Travel'],
      challenges: ['Obesity', 'Liver Problems', 'Over-confidence'],
      remedies: ['Guru Worship', 'Vishnu Sahasranama', 'Yellow Clothes on Thursday'],
    },
    'Venus': {
      positive: ['Marriage', 'Luxury', 'Art Success', 'Vehicle', 'Beauty'],
      challenges: ['Diabetes', 'Kidney Problems', 'Relationship Issues'],
      remedies: ['Lakshmi Worship', 'Shukra Stotra', 'White Clothes on Friday'],
    },
    'Saturn': {
      positive: ['Government Help', 'Long-term Gains', 'Land', 'Building', 'Patience'],
      challenges: ['Delays', 'Body Pain', 'Mental Depression', 'Obstacles'],
      remedies: ['Hanuman Worship', 'Shani Stotra', 'Black/Blue Clothes on Saturday'],
    },
    'Rahu': {
      positive: ['Sudden Success', 'Foreign Travel', 'Technology', 'Innovation', 'Research'],
      challenges: ['Confusion', 'Fraud', 'Skin Disease', 'Fear of Poison'],
      remedies: ['Durga Worship', 'Rahu Stotra', 'Blue Clothes on Saturday'],
    },
    'Ketu': {
      positive: ['Spirituality', 'Liberation', 'Research', 'Hidden Knowledge', 'Detachment'],
      challenges: ['Sudden Loss', 'Accidents', 'Mysterious Illness'],
      remedies: ['Ganapati Worship', 'Ketu Stotra', 'Grey Clothes'],
    },
  }
};

// Legacy Tamil constant for backward compatibility
const DASHA_PREDICTIONS = DASHA_PREDICTIONS_ML.ta;

/**
 * Generate comprehensive PDF HTML
 * @param {Object} userProfile - User profile data
 * @param {Object} chartData - Chart calculation data
 * @param {string} language - Language code ('ta', 'kn', 'en') - defaults to 'ta'
 */
export function generateComprehensivePDFHTML(userProfile, chartData, language = 'ta') {
  // Get language-specific data
  const lang = LANG_DATA[language] || LANG_DATA.ta;
  const ui = lang.ui;

  const planets = chartData?.planets || [];
  const dasha = chartData?.dasha;
  const yogas = chartData?.yogas || [];
  const lagna = chartData?.lagna;
  const moonSign = chartData?.moon_sign;

  // Date locale based on language
  const dateLocale = language === 'en' ? 'en-IN' : language === 'kn' ? 'kn-IN' : 'ta-IN';
  const currentDate = new Date().toLocaleDateString(dateLocale);
  const rasiDetails = RASI_DETAILS[moonSign?.rasi_tamil] || {};
  const nakshatraDetails = NAKSHATRA_DETAILS[moonSign?.nakshatra] || {};

  // Generate chart HTML using language-specific labels
  const generateChartHTML = (title, isAmsam = false) => {
    const rasiOrder = ['Pisces', 'Aries', 'Taurus', 'Gemini', 'Aquarius', 'Cancer', 'Capricorn', 'Leo', 'Sagittarius', 'Scorpio', 'Libra', 'Virgo'];
    const rasiDisplay = lang.chartRasiOrder;
    const PLANET_ABBR = lang.planetAbbr;

    const houses = Array(12).fill('');
    planets.forEach(p => {
      const idx = rasiOrder.indexOf(p.rasi);
      if (idx !== -1) {
        const abbr = PLANET_ABBR[p.planet] || p.planet.substring(0, 2);
        houses[idx] = houses[idx] ? houses[idx] + ',' + abbr : abbr;
      }
    });

    if (lagna) {
      const lagnaIdx = rasiOrder.indexOf(lagna.rasi);
      if (lagnaIdx !== -1) {
        houses[lagnaIdx] = lang.lagnaAbbr + (houses[lagnaIdx] ? ',' + houses[lagnaIdx] : '');
      }
    }

    return `
      <div style="text-align:center;margin:15px 0;">
        <div style="font-weight:bold;font-size:14px;margin-bottom:8px;color:#92400e;">${title}</div>
        <table style="border-collapse:collapse;margin:auto;background:#fffbeb;border:2px solid #92400e;">
          <tr>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiDisplay[0]}</div><b>${houses[0]}</b>
            </td>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiDisplay[1]}</div><b>${houses[1]}</b>
            </td>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiDisplay[2]}</div><b>${houses[2]}</b>
            </td>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiDisplay[3]}</div><b>${houses[3]}</b>
            </td>
          </tr>
          <tr>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiDisplay[4]}</div><b>${houses[4]}</b>
            </td>
            <td colspan="2" rowspan="2" style="border:1px solid #d97706;text-align:center;background:#fef3c7;font-weight:bold;font-size:16px;color:#92400e;">
              ${isAmsam ? lang.amsamLabel : lang.rasiLabel}
            </td>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiDisplay[5]}</div><b>${houses[5]}</b>
            </td>
          </tr>
          <tr>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiDisplay[6]}</div><b>${houses[6]}</b>
            </td>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiDisplay[7]}</div><b>${houses[7]}</b>
            </td>
          </tr>
          <tr>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiDisplay[8]}</div><b>${houses[8]}</b>
            </td>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiDisplay[9]}</div><b>${houses[9]}</b>
            </td>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiDisplay[10]}</div><b>${houses[10]}</b>
            </td>
            <td style="border:1px solid #d97706;width:70px;height:55px;text-align:center;font-size:11px;vertical-align:top;padding:3px;background:#fff;">
              <div style="font-size:9px;color:#888;">${rasiDisplay[11]}</div><b>${houses[11]}</b>
            </td>
          </tr>
        </table>
      </div>
    `;
  };

  // Generate life area predictions
  const generateLifeAreaPredictions = () => {
    const houseMeanings = HOUSE_MEANINGS_ML[language] || HOUSE_MEANINGS_ML.ta;
    const dashaPredictions = DASHA_PREDICTIONS_ML[language] || DASHA_PREDICTIONS_ML.ta;
    const retrogradeSymbol = language === 'ta' ? ' (வ)' : language === 'kn' ? ' (ವ)' : ' (R)';
    const houseLabel = language === 'ta' ? 'ம் வீடு' : language === 'kn' ? 'ನೇ ಮನೆ' : ' House';

    let html = '';
    Object.entries(houseMeanings).forEach(([house, info]) => {
      const housePlanets = planets.filter(p => {
        const rasiOrder = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
        const lagnaIndex = lagna ? rasiOrder.indexOf(lagna.rasi) : 0;
        const planetIndex = rasiOrder.indexOf(p.rasi);
        const houseNum = ((planetIndex - lagnaIndex + 12) % 12) + 1;
        return houseNum === parseInt(house);
      });

      // Get planet name based on language
      const getPlanetName = (p) => {
        if (language === 'en') return p.planet;
        if (language === 'kn') {
          const knNames = { 'Sun': 'ಸೂರ್ಯ', 'Moon': 'ಚಂದ್ರ', 'Mars': 'ಕುಜ', 'Mercury': 'ಬುಧ', 'Jupiter': 'ಗುರು', 'Venus': 'ಶುಕ್ರ', 'Saturn': 'ಶನಿ', 'Rahu': 'ರಾಹು', 'Ketu': 'ಕೇತು' };
          return knNames[p.planet] || p.planet;
        }
        return p.tamil_name || p.planet;
      };

      // Get dasha prediction key based on language
      const getDashaPredKey = (p) => {
        if (language === 'en') return p.planet;
        if (language === 'kn') {
          const knNames = { 'Sun': 'ಸೂರ್ಯ', 'Moon': 'ಚಂದ್ರ', 'Mars': 'ಕುಜ', 'Mercury': 'ಬುಧ', 'Jupiter': 'ಗುರು', 'Venus': 'ಶುಕ್ರ', 'Saturn': 'ಶನಿ', 'Rahu': 'ರಾಹು', 'Ketu': 'ಕೇತು' };
          return knNames[p.planet] || p.planet;
        }
        return p.tamil_name || p.planet;
      };

      html += `
        <div style="margin:10px 0;padding:12px;background:#fff;border:1px solid #fed7aa;border-radius:8px;">
          <div style="font-weight:bold;color:#9a3412;margin-bottom:5px;">${house}${houseLabel} - ${info.name}</div>
          <div style="font-size:11px;color:#6b7280;margin-bottom:5px;">${ui.areas}: ${info.areas.join(', ')}</div>
          ${housePlanets.length > 0 ? `
            <div style="font-size:11px;color:#374151;">
              <b>${ui.planets}:</b> ${housePlanets.map(p => getPlanetName(p) + (p.is_retrograde ? retrogradeSymbol : '')).join(', ')}
            </div>
            <div style="font-size:11px;color:#16a34a;margin-top:5px;">
              <b>${ui.benefits}:</b> ${housePlanets.map(p => {
                const pred = dashaPredictions[getDashaPredKey(p)];
                return pred ? pred.positive[0] : '';
              }).filter(Boolean).join(', ')}
            </div>
          ` : `<div style="font-size:11px;color:#9ca3af;">${ui.noPlanetsInHouse}</div>`}
        </div>
      `;
    });
    return html;
  };

  // Generate detailed yoga analysis
  const generateYogaAnalysis = () => {
    const strengthLabel = language === 'ta' ? 'பலம்' : language === 'kn' ? 'ಬಲ' : 'Strength';
    let html = '';
    yogas.forEach((yoga, idx) => {
      const yogaInfo = YOGA_DEFINITIONS[yoga.name] || {};
      // Use English name for English, else use tamil name
      const yogaDisplayName = language === 'en' ? yoga.name : (yogaInfo.tamil || yoga.tamil_name || yoga.name);

      html += `
        <div style="page-break-inside:avoid;margin:15px 0;padding:15px;background:linear-gradient(135deg, #ecfdf5, #d1fae5);border:2px solid #10b981;border-radius:12px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <span style="font-size:16px;font-weight:bold;color:#166534;">${idx + 1}. ${yogaDisplayName}</span>
            <span style="background:#16a34a;color:#fff;padding:4px 12px;border-radius:20px;font-size:12px;">${yoga.strength}% ${strengthLabel}</span>
          </div>

          <div style="margin:10px 0;padding:10px;background:#fff;border-radius:8px;">
            <div style="font-size:12px;font-weight:bold;color:#374151;margin-bottom:5px;">${ui.yogaFormation}:</div>
            <div style="font-size:11px;color:#6b7280;">${yogaInfo.formation || yoga.description || '-'}</div>
          </div>

          ${yogaInfo.effects ? `
          <div style="margin:10px 0;">
            <div style="font-size:12px;font-weight:bold;color:#374151;margin-bottom:5px;">${ui.expectedBenefits}:</div>
            <ul style="margin:0;padding-left:20px;font-size:11px;color:#374151;">
              ${yogaInfo.effects.map(e => `<li>${e}</li>`).join('')}
            </ul>
          </div>
          ` : ''}

          <div style="margin-top:10px;padding:10px;background:#fef3c7;border-radius:8px;">
            <div style="font-size:11px;color:#92400e;">
              <b>${ui.activationPeriod}:</b> ${yogaInfo.activation || ui.inRelatedPlanetDasha}
            </div>
          </div>
        </div>
      `;
    });
    return html;
  };

  // Generate dasha timeline analysis
  const generateDashaAnalysis = () => {
    if (!dasha?.all_periods) return '';

    const dashaPredictions = DASHA_PREDICTIONS_ML[language] || DASHA_PREDICTIONS_ML.ta;

    // Helper to get planet lord name in current language
    const getPlanetLord = (period) => {
      if (language === 'en') return period.lord || period.tamil_lord;
      if (language === 'kn') {
        const knNames = { 'சூரியன்': 'ಸೂರ್ಯ', 'சந்திரன்': 'ಚಂದ್ರ', 'செவ்வாய்': 'ಕುಜ', 'புதன்': 'ಬುಧ', 'குரு': 'ಗುರು', 'சுக்கிரன்': 'ಶುಕ್ರ', 'சனி': 'ಶನಿ', 'ராகு': 'ರಾಹು', 'கேது': 'ಕೇತು' };
        return knNames[period.tamil_lord] || period.tamil_lord;
      }
      return period.tamil_lord;
    };

    // Helper to get dasha prediction key
    const getDashaPredKey = (period) => {
      if (language === 'en') {
        const enNames = { 'சூரியன்': 'Sun', 'சந்திரன்': 'Moon', 'செவ்வாய்': 'Mars', 'புதன்': 'Mercury', 'குரு': 'Jupiter', 'சுக்கிரன்': 'Venus', 'சனி': 'Saturn', 'ராகு': 'Rahu', 'கேது': 'Ketu' };
        return enNames[period.tamil_lord] || period.lord || period.tamil_lord;
      }
      if (language === 'kn') {
        const knNames = { 'சூரியன்': 'ಸೂರ್ಯ', 'சந்திரன்': 'ಚಂದ್ರ', 'செவ்வாய்': 'ಕುಜ', 'புதன்': 'ಬುಧ', 'குரு': 'ಗுರು', 'சுக்கிரன்': 'ಶುಕ್ರ', 'சனி': 'ಶನಿ', 'ராகு': 'ರಾಹು', 'கேது': 'ಕೇತು' };
        return knNames[period.tamil_lord] || period.tamil_lord;
      }
      return period.tamil_lord;
    };

    let html = `<div style="page-break-before:always;"></div><h2 style="color:#6b21a8;border-bottom:2px solid #c4b5fd;padding-bottom:5px;">${ui.detailedDashaAnalysis}</h2>`;

    dasha.all_periods.forEach((period) => {
      const predKey = getDashaPredKey(period);
      const pred = dashaPredictions[predKey] || {};
      const isCurrent = period.is_current;
      const planetLord = getPlanetLord(period);

      html += `
        <div style="page-break-inside:avoid;margin:15px 0;padding:15px;background:${isCurrent ? 'linear-gradient(135deg, #fef3c7, #fde68a)' : '#fff'};border:2px solid ${isCurrent ? '#f59e0b' : '#e5e7eb'};border-radius:12px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <span style="font-size:16px;font-weight:bold;color:${isCurrent ? '#92400e' : '#374151'};">
              ${planetLord} ${ui.mahaDasha} ${isCurrent ? `(${ui.currentlyRunning})` : ''}
            </span>
            <span style="font-size:12px;color:#6b7280;">${period.start} - ${period.end} (${period.years} ${ui.years})</span>
          </div>

          ${pred.positive ? `
          <div style="margin:10px 0;padding:10px;background:#ecfdf5;border-radius:8px;">
            <div style="font-size:12px;font-weight:bold;color:#166534;margin-bottom:5px;">${ui.positiveBenefits}:</div>
            <ul style="margin:0;padding-left:20px;font-size:11px;color:#374151;">
              ${pred.positive.map(p => `<li>${p}</li>`).join('')}
            </ul>
          </div>
          ` : ''}

          ${pred.challenges ? `
          <div style="margin:10px 0;padding:10px;background:#fef2f2;border-radius:8px;">
            <div style="font-size:12px;font-weight:bold;color:#dc2626;margin-bottom:5px;">${ui.thingsToWatch}:</div>
            <ul style="margin:0;padding-left:20px;font-size:11px;color:#374151;">
              ${pred.challenges.map(c => `<li>${c}</li>`).join('')}
            </ul>
          </div>
          ` : ''}

          ${pred.remedies ? `
          <div style="margin:10px 0;padding:10px;background:#eff6ff;border-radius:8px;">
            <div style="font-size:12px;font-weight:bold;color:#1d4ed8;margin-bottom:5px;">${ui.remedies}:</div>
            <ul style="margin:0;padding-left:20px;font-size:11px;color:#374151;">
              ${pred.remedies.map(r => `<li>${r}</li>`).join('')}
            </ul>
          </div>
          ` : ''}
        </div>
      `;
    });

    return html;
  };

  // Generate AI summary
  const generateAISummary = () => {
    const strongPlanets = planets.filter(p => (p.strength || 50) >= 60);
    const weakPlanets = planets.filter(p => (p.strength || 50) < 40);
    const currentDashaTamil = dasha?.current_mahadasha?.tamil_lord || dasha?.all_periods?.find(p => p.is_current)?.tamil_lord || '-';

    // Get language-specific rasi and nakshatra details
    const rasiDetailsLang = RASI_DETAILS_ML[language] || RASI_DETAILS_ML.ta;
    const nakshatraDetailsLang = NAKSHATRA_DETAILS_ML[language] || NAKSHATRA_DETAILS_ML.ta;
    const dashaPredLang = DASHA_PREDICTIONS_ML[language] || DASHA_PREDICTIONS_ML.ta;

    // Get rasi/nakshatra name based on language
    const getRasiName = () => {
      if (language === 'en') return moonSign?.rasi || moonSign?.rasi_tamil;
      if (language === 'kn') {
        const knRasiMap = { 'மேஷம்': 'ಮೇಷ', 'ரிஷபம்': 'ವೃಷಭ', 'மிதுனம்': 'ಮಿಥುನ', 'கடகம்': 'ಕರ್ಕಾಟಕ', 'சிம்மம்': 'ಸಿಂಹ', 'கன்னி': 'ಕನ್ಯಾ', 'துலாம்': 'ತುಲಾ', 'விருச்சிகம்': 'ವೃಶ್ಚಿಕ', 'தனுசு': 'ಧನು', 'மகரம்': 'ಮಕರ', 'கும்பம்': 'ಕುಂಭ', 'மீனம்': 'ಮೀನ' };
        return knRasiMap[moonSign?.rasi_tamil] || moonSign?.rasi_tamil;
      }
      return moonSign?.rasi_tamil;
    };

    const getLagnaName = () => {
      if (language === 'en') return lagna?.rasi || lagna?.rasi_tamil;
      if (language === 'kn') {
        const knRasiMap = { 'மேஷம்': 'ಮೇಷ', 'ரிஷபம்': 'ವೃಷಭ', 'மிதுனம்': 'ಮಿಥುನ', 'கடகம்': 'ಕರ್ಕಾಟಕ', 'சிம்மம்': 'ಸಿಂಹ', 'கன்னி': 'ಕನ್ಯಾ', 'துலாம்': 'ತುಲಾ', 'விருச்சிகம்': 'ವೃಶ್ಚಿಕ', 'தனுசு': 'ಧನು', 'மகரம்': 'ಮಕರ', 'கும்பம்': 'ಕುಂಭ', 'மீனம்': 'ಮೀನ' };
        return knRasiMap[lagna?.rasi_tamil] || lagna?.rasi_tamil;
      }
      return lagna?.rasi_tamil;
    };

    // Get rasi details for current language
    const getRasiDetails = () => {
      const rasiName = language === 'en' ? moonSign?.rasi : language === 'kn' ? getRasiName() : moonSign?.rasi_tamil;
      return rasiDetailsLang[rasiName] || rasiDetails || {};
    };

    // Get nakshatra details for current language
    const getNakshatraDetails = () => {
      // Map Tamil nakshatra to English/Kannada
      const nakshatraMap = {
        ta: moonSign?.nakshatra,
        en: moonSign?.nakshatra_en || moonSign?.nakshatra,
        kn: moonSign?.nakshatra_kn || moonSign?.nakshatra
      };
      const nakshatraName = nakshatraMap[language] || moonSign?.nakshatra;
      return nakshatraDetailsLang[nakshatraName] || nakshatraDetails || {};
    };

    // Get current dasha name in language
    const getCurrentDasha = () => {
      if (language === 'en') {
        const enNames = { 'சூரியன்': 'Sun', 'சந்திரன்': 'Moon', 'செவ்வாய்': 'Mars', 'புதன்': 'Mercury', 'குரு': 'Jupiter', 'சுக்கிரன்': 'Venus', 'சனி': 'Saturn', 'ராகு': 'Rahu', 'கேது': 'Ketu' };
        return enNames[currentDashaTamil] || currentDashaTamil;
      }
      if (language === 'kn') {
        const knNames = { 'சூரியன்': 'ಸೂರ್ಯ', 'சந்திரன்': 'ಚಂದ್ರ', 'செவ்வாய்': 'ಕುಜ', 'புதன்': 'ಬುಧ', 'குரு': 'ಗುರು', 'சுக்கிரன்': 'ಶುಕ್ರ', 'சனி': 'ಶನಿ', 'ராகு': 'ರಾಹು', 'கேது': 'ಕೇತು' };
        return knNames[currentDashaTamil] || currentDashaTamil;
      }
      return currentDashaTamil;
    };

    // Get planet name based on language
    const getPlanetName = (p) => {
      if (language === 'en') return p.planet;
      if (language === 'kn') {
        const knNames = { 'Sun': 'ಸೂರ್ಯ', 'Moon': 'ಚಂದ್ರ', 'Mars': 'ಕುಜ', 'Mercury': 'ಬುಧ', 'Jupiter': 'ಗುರು', 'Venus': 'ಶುಕ್ರ', 'Saturn': 'ಶನಿ', 'Rahu': 'ರಾಹು', 'Ketu': 'ಕೇತು' };
        return knNames[p.planet] || p.tamil_name;
      }
      return p.tamil_name;
    };

    const currentDasha = getCurrentDasha();
    const currentRasiDetails = getRasiDetails();
    const currentNakshatraDetails = getNakshatraDetails();
    const currentDashaPred = dashaPredLang[currentDasha] || {};

    return `
      <div style="page-break-before:always;"></div>
      <h2 style="color:#7c3aed;border-bottom:2px solid #c4b5fd;padding-bottom:5px;">${ui.aiAnalysisSummary}</h2>

      <div style="background:linear-gradient(135deg, #faf5ff, #f3e8ff);padding:20px;border-radius:12px;border:2px solid #a855f7;">
        <h3 style="color:#6b21a8;margin-top:0;">${ui.chartIntro}</h3>
        <p style="font-size:12px;line-height:1.8;color:#374151;">
          ${userProfile?.name || ''} - <b>${getRasiName() || ''}</b> ${ui.rasi},
          <b>${moonSign?.nakshatra || ''}</b> ${ui.nakshatra} ${ui.pada} ${moonSign?.nakshatra_pada || ''}.
          ${ui.lagna}: <b>${getLagnaName() || ''}</b>.
        </p>

        <h3 style="color:#6b21a8;">${ui.rasiTraits}</h3>
        <p style="font-size:12px;line-height:1.8;color:#374151;">
          ${getRasiName() || ''} - ${ui.element}: <b>${currentRasiDetails.element || ''}</b>.
          ${ui.ruler}: <b>${currentRasiDetails.ruler || ''}</b>.
          ${currentRasiDetails.quality ? `${ui.mainQualities}: ${currentRasiDetails.quality}.` : ''}
          ${currentRasiDetails.career ? `${ui.suitableCareers}: ${currentRasiDetails.career}.` : ''}
        </p>

        <h3 style="color:#6b21a8;">${ui.nakshatraTraits}</h3>
        <p style="font-size:12px;line-height:1.8;color:#374151;">
          ${moonSign?.nakshatra || ''} - ${ui.deity}: <b>${currentNakshatraDetails.deity || ''}</b>.
          ${currentNakshatraDetails.quality ? `${ui.specialTrait}: ${currentNakshatraDetails.quality}.` : ''}
          ${currentNakshatraDetails.career ? `${ui.suitableCareer}: ${currentNakshatraDetails.career}.` : ''}
          ${currentNakshatraDetails.lucky_gems ? `${ui.luckyGem}: ${currentNakshatraDetails.lucky_gems}.` : ''}
        </p>

        <h3 style="color:#6b21a8;">${ui.planetStrengthAnalysis}</h3>
        <p style="font-size:12px;line-height:1.8;color:#374151;">
          ${strongPlanets.length > 0 ? `<b>${ui.strongPlanets}:</b> ${strongPlanets.map(p => getPlanetName(p)).join(', ')} - ${ui.theseWillGiveBenefits}.` : ''}
          ${weakPlanets.length > 0 ? `<br/><b>${ui.weakPlanets}:</b> ${weakPlanets.map(p => getPlanetName(p)).join(', ')} - ${ui.needsRemedies}.` : ''}
        </p>

        <h3 style="color:#6b21a8;">${ui.currentDashaStatus}</h3>
        <p style="font-size:12px;line-height:1.8;color:#374151;">
          ${ui.currentlyRunning}: <b>${currentDasha}</b> ${ui.mahaDasha}.
          ${currentDashaPred?.positive ?
            `${currentDashaPred.positive.slice(0, 3).join(', ')}.` : ''
          }
        </p>

        <h3 style="color:#6b21a8;">${ui.yogaBenefits}</h3>
        <p style="font-size:12px;line-height:1.8;color:#374151;">
          ${yogas.length > 0 ?
            `${ui.yogasFoundMsg}: ${yogas.map(y => language === 'en' ? y.name : (y.tamil_name || y.name)).join(', ')}.
            ${ui.yogasWillBenefit}.` :
            ui.noYogasFound
          }
        </p>

        <h3 style="color:#6b21a8;">${ui.luckyAspects}</h3>
        <p style="font-size:12px;line-height:1.8;color:#374151;">
          <b>${ui.luckyColor}:</b> ${currentRasiDetails.lucky_color || '-'}<br/>
          <b>${ui.luckyNumber}:</b> ${currentRasiDetails.lucky_number || '-'}<br/>
          <b>${ui.luckyGem}:</b> ${currentNakshatraDetails.lucky_gems || '-'}
        </p>
      </div>
    `;
  };

  // Main HTML
  return `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <style>
        @page { margin: 15mm; size: A4; }
        body {
          font-family: Arial, sans-serif;
          font-size: 12px;
          line-height: 1.6;
          color: #374151;
          background: #fffbeb;
        }
        .header {
          text-align: center;
          border: 3px solid #f97316;
          border-radius: 15px;
          padding: 20px;
          background: linear-gradient(135deg, #fff, #fff7ed);
          margin-bottom: 20px;
        }
        .header h1 {
          color: #9a3412;
          margin: 0;
          font-size: 28px;
        }
        .header .subtitle {
          color: #6b7280;
          margin-top: 5px;
          font-size: 14px;
        }
        .section {
          background: #fff;
          border: 1px solid #fed7aa;
          border-radius: 12px;
          padding: 15px;
          margin-bottom: 15px;
          page-break-inside: avoid;
        }
        .section-title {
          color: #9a3412;
          font-size: 16px;
          font-weight: bold;
          border-bottom: 2px solid #fed7aa;
          padding-bottom: 8px;
          margin-bottom: 12px;
        }
        .info-grid {
          display: flex;
          flex-wrap: wrap;
          gap: 10px;
        }
        .info-item {
          flex: 1;
          min-width: 30%;
          background: #fff7ed;
          padding: 12px;
          border-radius: 8px;
          border: 1px solid #fed7aa;
        }
        .info-label {
          font-size: 10px;
          color: #6b7280;
          text-transform: uppercase;
        }
        .info-value {
          font-size: 14px;
          font-weight: bold;
          color: #1f2937;
          margin-top: 3px;
        }
        .charts-container {
          display: flex;
          justify-content: space-around;
          flex-wrap: wrap;
          margin: 15px 0;
        }
        table.planets {
          width: 100%;
          border-collapse: collapse;
          font-size: 11px;
          margin-top: 10px;
        }
        table.planets th {
          background: #fff7ed;
          color: #9a3412;
          padding: 10px;
          text-align: left;
          border: 1px solid #fed7aa;
        }
        table.planets td {
          padding: 10px;
          border: 1px solid #fed7aa;
        }
        table.planets tr:nth-child(even) {
          background: #fffbeb;
        }
        .footer {
          text-align: center;
          margin-top: 30px;
          padding: 15px;
          background: linear-gradient(135deg, #f97316, #ea580c);
          color: #fff;
          border-radius: 10px;
          font-size: 11px;
        }
        h2 {
          color: #9a3412;
          font-size: 18px;
          margin-top: 25px;
        }
        .page-break { page-break-before: always; }
      </style>
    </head>
    <body>
      <!-- Cover Page -->
      <div class="header">
        <svg width="50" height="50" viewBox="0 0 100 100" style="margin-bottom:10px;">
          <path d="M50 5 L55 40 L90 30 L60 50 L90 70 L55 60 L50 95 L45 60 L10 70 L40 50 L10 30 L45 40 Z" fill="#f97316"/>
          <circle cx="50" cy="50" r="10" fill="#fff7ed"/>
        </svg>
        <div style="font-size:24px;font-weight:bold;color:#9a3412;margin-bottom:5px;">jothida.ai</div>
        <h1>${ui.reportTitle}</h1>
        <div class="subtitle">${ui.detailedAnalysis}</div>
        <div style="margin-top:15px;font-size:16px;color:#374151;font-weight:bold;">${userProfile?.name || ''}</div>
        <div style="color:#6b7280;font-size:12px;">${ui.reportDate}: ${currentDate}</div>
      </div>

      <!-- Birth Details -->
      <div class="section">
        <div class="section-title">${ui.birthDetails}</div>
        <div class="info-grid">
          <div class="info-item">
            <div class="info-label">${ui.name}</div>
            <div class="info-value">${userProfile?.name || '-'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">${ui.birthDate}</div>
            <div class="info-value">${userProfile?.birthDate || '-'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">${ui.birthTime}</div>
            <div class="info-value">${userProfile?.birthTime || '-'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">${ui.birthPlace}</div>
            <div class="info-value">${userProfile?.birthPlace || '-'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">${ui.rasi}</div>
            <div class="info-value">${moonSign?.rasi_tamil || userProfile?.rasi || '-'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">${ui.nakshatra}</div>
            <div class="info-value">${moonSign?.nakshatra || userProfile?.nakshatra || '-'} - ${ui.pada} ${moonSign?.nakshatra_pada || ''}</div>
          </div>
          <div class="info-item">
            <div class="info-label">${ui.lagna}</div>
            <div class="info-value">${lagna?.rasi_tamil || '-'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">${ui.lagnaNakshatra}</div>
            <div class="info-value">${lagna?.nakshatra || '-'}</div>
          </div>
        </div>
      </div>

      <!-- Panchagam -->
      <div class="section">
        <div class="section-title">${ui.panchagamDetails}</div>
        <div class="info-grid">
          <div class="info-item">
            <div class="info-label">${ui.tithi}</div>
            <div class="info-value">${chartData?.panchagam?.tithi || '-'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">${ui.vaaram}</div>
            <div class="info-value">${chartData?.panchagam?.vaaram || '-'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">${ui.yogam}</div>
            <div class="info-value">${chartData?.panchagam?.yogam || '-'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">${ui.karanam}</div>
            <div class="info-value">${chartData?.panchagam?.karanam || '-'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">${ui.sunrise}</div>
            <div class="info-value">${chartData?.panchagam?.sunrise || '06:00'}</div>
          </div>
          <div class="info-item">
            <div class="info-label">${ui.sunset}</div>
            <div class="info-value">${chartData?.panchagam?.sunset || '18:00'}</div>
          </div>
        </div>
      </div>

      <!-- Charts -->
      <div class="section">
        <div class="section-title">${ui.chartTitle}</div>
        <div class="charts-container">
          ${generateChartHTML(ui.rasiChart, false)}
          ${generateChartHTML(ui.navamsaChart, true)}
        </div>
      </div>

      <!-- Planet Positions -->
      <div class="section">
        <div class="section-title">${ui.planetPositions}</div>
        <table class="planets">
          <tr>
            <th>${ui.planet}</th>
            <th>${ui.rasi}</th>
            <th>${ui.degree}</th>
            <th>${ui.nakshatra}</th>
            <th>${ui.pada}</th>
            <th>${ui.strength}</th>
            <th>${ui.status}</th>
          </tr>
          ${planets.map(p => {
            // Get planet name based on language
            const planetName = language === 'en' ? p.planet : language === 'kn' ?
              ({ 'Sun': 'ಸೂರ್ಯ', 'Moon': 'ಚಂದ್ರ', 'Mars': 'ಕುಜ', 'Mercury': 'ಬುಧ', 'Jupiter': 'ಗುರು', 'Venus': 'ಶುಕ್ರ', 'Saturn': 'ಶನಿ', 'Rahu': 'ರಾಹು', 'Ketu': 'ಕೇತು' }[p.planet] || p.tamil_name) : p.tamil_name;
            const rasiName = language === 'en' ? p.rasi : p.rasi_tamil;
            return `
            <tr>
              <td><b>${p.symbol} ${planetName}</b>${p.is_retrograde ? ` <span style="color:red;">(${ui.retrograde})</span>` : ''}</td>
              <td>${rasiName}</td>
              <td>${p.degree?.toFixed(2) || '-'}°</td>
              <td>${p.nakshatra}</td>
              <td>${p.nakshatra_pada}</td>
              <td>
                <span style="background:${(p.strength || 50) >= 60 ? '#dcfce7' : (p.strength || 50) >= 40 ? '#fef3c7' : '#fef2f2'};padding:2px 8px;border-radius:10px;">
                  ${p.strength || 50}%
                </span>
              </td>
              <td>${p.trend === 'up' ? ui.goodStatus : p.trend === 'down' ? ui.cautionStatus : ui.normalStatus}</td>
            </tr>
          `}).join('')}
        </table>
      </div>

      <!-- AI Summary -->
      ${generateAISummary()}

      <!-- Yoga Analysis -->
      <div class="page-break"></div>
      <h2 style="color:#166534;border-bottom:2px solid #86efac;padding-bottom:5px;">${ui.detailedYogaAnalysis}</h2>
      ${yogas.length > 0 ? generateYogaAnalysis() : `<p>${ui.noYogasFound}</p>`}

      <!-- Dasha Analysis -->
      ${generateDashaAnalysis()}

      <!-- Life Area Predictions -->
      <div class="page-break"></div>
      <h2 style="color:#9a3412;border-bottom:2px solid #fed7aa;padding-bottom:5px;">${ui.lifeAreaPredictions}</h2>
      ${generateLifeAreaPredictions()}

      <!-- Footer -->
      <div class="footer">
        <div style="font-size:14px;font-weight:bold;">Jothida AI</div>
        <div>${ui.trustedAstrologer}</div>
        <div style="margin-top:5px;">${ui.aiGeneratedReport}</div>
        <div style="margin-top:10px;font-size:10px;">© ${new Date().getFullYear()} Jothida AI. ${ui.allRightsReserved}.</div>
      </div>
    </body>
    </html>
  `;
}

export default { generateComprehensivePDFHTML };
