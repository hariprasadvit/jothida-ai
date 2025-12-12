import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Share2, MessageCircle, Sun, Moon, Flame, Leaf, Heart, Zap, Cloud, TrendingUp, TrendingDown, User, Lightbulb, Clock, Star, Palette, Diamond, Compass } from 'lucide-react';

// Story types
const STORY_TYPES = {
  PLANET_INFLUENCE: 'planet_influence',
  MOON_TRANSIT: 'moon_transit',
  DAILY_INSIGHT: 'daily_insight',
  NAKSHATRA_EFFECT: 'nakshatra_effect',
  REMEDY: 'remedy',
  LUCKY_TIME: 'lucky_time',
};

// Planet data
const planetData = {
  Sun: { tamil: 'சூரியன்', color: '#f59e0b', Icon: Sun },
  Moon: { tamil: 'சந்திரன்', color: '#e5e7eb', Icon: Moon },
  Mars: { tamil: 'செவ்வாய்', color: '#ef4444', Icon: Flame },
  Mercury: { tamil: 'புதன்', color: '#22c55e', Icon: Leaf },
  Jupiter: { tamil: 'குரு', color: '#f97316', Icon: Star },
  Venus: { tamil: 'சுக்கிரன்', color: '#ec4899', Icon: Heart },
  Saturn: { tamil: 'சனி', color: '#3b82f6', Icon: Cloud },
  Rahu: { tamil: 'ராகு', color: '#6366f1', Icon: Zap },
  Ketu: { tamil: 'கேது', color: '#8b5cf6', Icon: Zap },
};

// Rasi data
const rasiData = {
  'மேஷம்': { english: 'Aries', symbol: '♈', element: 'fire' },
  'ரிஷபம்': { english: 'Taurus', symbol: '♉', element: 'earth' },
  'மிதுனம்': { english: 'Gemini', symbol: '♊', element: 'air' },
  'கடகம்': { english: 'Cancer', symbol: '♋', element: 'water' },
  'சிம்மம்': { english: 'Leo', symbol: '♌', element: 'fire' },
  'கன்னி': { english: 'Virgo', symbol: '♍', element: 'earth' },
  'துலாம்': { english: 'Libra', symbol: '♎', element: 'air' },
  'விருச்சிகம்': { english: 'Scorpio', symbol: '♏', element: 'water' },
  'தனுசு': { english: 'Sagittarius', symbol: '♐', element: 'fire' },
  'மகரம்': { english: 'Capricorn', symbol: '♑', element: 'earth' },
  'கும்பம்': { english: 'Aquarius', symbol: '♒', element: 'air' },
  'மீனம்': { english: 'Pisces', symbol: '♓', element: 'water' },
};

// Gradient backgrounds for stories
const storyGradients = {
  [STORY_TYPES.PLANET_INFLUENCE]: 'from-[#1a1a2e] via-[#16213e] to-[#0f3460]',
  [STORY_TYPES.MOON_TRANSIT]: 'from-[#0f0f23] via-[#1a1a3a] to-[#2d2d5a]',
  [STORY_TYPES.DAILY_INSIGHT]: 'from-[#1a0a2e] via-[#2d1b4e] to-[#4a2c7a]',
  [STORY_TYPES.NAKSHATRA_EFFECT]: 'from-[#0a1628] via-[#162d50] to-[#234b7a]',
  [STORY_TYPES.REMEDY]: 'from-[#1a2e1a] via-[#2e4a2e] to-[#3d6b3d]',
  [STORY_TYPES.LUCKY_TIME]: 'from-[#2e1a1a] via-[#4a2e2e] to-[#6b3d3d]',
};

// Translations
const translations = {
  ta: {
    loading: 'ஏற்றுகிறது...',
    appName: 'ஜோதிடா AI',
    dailyStories: 'தினசரி கதைகள்',
    share: 'பகிர்',
    askAI: 'AI கேள்',
    todayRulingPlanet: 'இன்றைய ஆட்சி கிரகம்',
    moonTransit: 'சந்திர சஞ்சாரம்',
    moonIn: 'சந்திரன்',
    yourDailyInsight: 'உங்கள் இன்றைய பலன்',
    hey: 'வணக்கம்',
    todayScore: 'இன்றைய மதிப்பெண்',
    nakshatraInfluence: 'நட்சத்திர பலன்',
    yourStarMessage: 'உங்கள் நட்சத்திர செய்தி',
    todayRemedy: 'இன்றைய பரிகாரம்',
    enhanceYourDay: 'உங்கள் நாளை மேம்படுத்துங்கள்',
    luckyTimesToday: 'இன்றைய நல்ல நேரம்',
    bestTimesForYou: 'உங்களுக்கான சிறந்த நேரங்கள்',
    color: 'நிறம்',
    stone: 'கல்',
    direction: 'திசை',
    orange: 'ஆரஞ்சு',
    ruby: 'மாணிக்கம்',
    east: 'கிழக்கு',
    brahmaKala: 'பிரம்ம முகூர்த்தம்',
    abhijit: 'அபிஜித் முகூர்த்தம்',
    eveningAuspicious: 'மாலை சுபம்',
  },
  en: {
    loading: 'Loading...',
    appName: 'Jothida AI',
    dailyStories: 'Daily Stories',
    share: 'Share',
    askAI: 'Ask AI',
    todayRulingPlanet: "TODAY'S RULING PLANET",
    moonTransit: 'MOON TRANSIT',
    moonIn: 'Moon in',
    yourDailyInsight: 'YOUR DAILY INSIGHT',
    hey: 'Hey',
    todayScore: "Today's Score",
    nakshatraInfluence: 'NAKSHATRA INFLUENCE',
    yourStarMessage: "Your Star's Message",
    todayRemedy: "TODAY'S REMEDY",
    enhanceYourDay: 'Enhance Your Day',
    luckyTimesToday: 'LUCKY TIMES TODAY',
    bestTimesForYou: 'Best Times for You',
    color: 'Color',
    stone: 'Stone',
    direction: 'Direction',
    orange: 'Orange',
    ruby: 'Ruby',
    east: 'East',
    brahmaKala: 'Brahma Muhurta',
    abhijit: 'Abhijit Muhurta',
    eveningAuspicious: 'Evening Auspicious',
  },
};

// Progress bar component
const ProgressBar = ({ index, activeIndex, duration }) => {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (index === activeIndex) {
      setProgress(0);
      const interval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 100) {
            clearInterval(interval);
            return 100;
          }
          return prev + (100 / (duration / 50));
        });
      }, 50);
      return () => clearInterval(interval);
    } else if (index < activeIndex) {
      setProgress(100);
    } else {
      setProgress(0);
    }
  }, [activeIndex, duration, index]);

  return (
    <div className="flex-1 h-1 bg-white/30 rounded-full overflow-hidden">
      <div
        className="h-full bg-white rounded-full transition-all duration-50"
        style={{ width: `${progress}%` }}
      />
    </div>
  );
};

// Story Card Component
const StoryCard = ({ story, isActive, t, userProfile }) => {
  const renderContent = () => {
    switch (story.type) {
      case STORY_TYPES.PLANET_INFLUENCE:
        const PlanetIcon = story.Icon;
        return (
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={isActive ? { opacity: 1, y: 0, scale: 1 } : {}}
            transition={{ duration: 0.4 }}
            className="flex flex-col items-center text-center px-6"
          >
            <div
              className="w-24 h-24 rounded-full flex items-center justify-center mb-4"
              style={{ backgroundColor: `${story.planetColor}30` }}
            >
              <PlanetIcon size={48} color={story.planetColor} />
            </div>
            <p className="text-gray-400 text-xs tracking-widest mb-2">{story.label}</p>
            <h2 className="text-white text-3xl font-bold mb-4">{story.title}</h2>
            <p className="text-gray-300 text-base leading-relaxed mb-5">{story.description}</p>
            {story.effect && (
              <div
                className={`flex items-center gap-2 px-4 py-2.5 rounded-full ${
                  story.isPositive ? 'bg-green-500/20' : 'bg-red-500/20'
                }`}
              >
                {story.isPositive ? (
                  <TrendingUp size={18} className="text-green-500" />
                ) : (
                  <TrendingDown size={18} className="text-red-500" />
                )}
                <span className={story.isPositive ? 'text-green-500' : 'text-red-500'}>
                  {story.effect}
                </span>
              </div>
            )}
          </motion.div>
        );

      case STORY_TYPES.MOON_TRANSIT:
        return (
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={isActive ? { opacity: 1, y: 0, scale: 1 } : {}}
            transition={{ duration: 0.4 }}
            className="flex flex-col items-center text-center px-6"
          >
            <div className="relative mb-4">
              <span className="text-7xl">🌙</span>
              <div className="absolute inset-0 w-28 h-28 -m-4 rounded-full bg-white/10" />
            </div>
            <p className="text-gray-400 text-xs tracking-widest mb-2">{story.label}</p>
            <h2 className="text-white text-3xl font-bold mb-4">{story.title}</h2>
            <div className="mb-4">
              <span className="text-5xl text-white">{story.rasiSymbol}</span>
              <p className="text-gray-400 text-sm mt-2">{story.rasiName}</p>
            </div>
            <p className="text-gray-300 text-base leading-relaxed mb-5">{story.description}</p>
            {story.personalMessage && (
              <div className="flex items-center gap-2 bg-orange-500/20 px-4 py-3 rounded-xl">
                <User size={16} className="text-orange-500" />
                <span className="text-orange-500 text-sm">{story.personalMessage}</span>
              </div>
            )}
          </motion.div>
        );

      case STORY_TYPES.DAILY_INSIGHT:
        return (
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={isActive ? { opacity: 1, y: 0, scale: 1 } : {}}
            transition={{ duration: 0.4 }}
            className="flex flex-col items-center text-center px-6"
          >
            <span className="text-6xl mb-2">✨</span>
            <p className="text-gray-400 text-xs tracking-widest mb-2">{story.label}</p>
            <h2 className="text-white text-3xl font-bold mb-4">{story.title}</h2>
            <div className="w-28 h-28 rounded-full bg-orange-500/20 border-4 border-orange-500 flex flex-col items-center justify-center mb-5">
              <span className="text-orange-500 text-4xl font-bold">{story.score}</span>
              <span className="text-gray-400 text-xs mt-1">{story.scoreLabel}</span>
            </div>
            <p className="text-gray-300 text-base leading-relaxed mb-5">{story.description}</p>
            {story.tip && (
              <div className="flex items-center gap-2 bg-amber-500/20 px-4 py-3 rounded-xl">
                <Lightbulb size={18} className="text-amber-500" />
                <span className="text-amber-500 text-sm">{story.tip}</span>
              </div>
            )}
          </motion.div>
        );

      case STORY_TYPES.NAKSHATRA_EFFECT:
        return (
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={isActive ? { opacity: 1, y: 0, scale: 1 } : {}}
            transition={{ duration: 0.4 }}
            className="flex flex-col items-center text-center px-6"
          >
            <span className="text-6xl mb-2">⭐</span>
            <p className="text-gray-400 text-xs tracking-widest mb-2">{story.label}</p>
            <h2 className="text-white text-3xl font-bold mb-2">{story.title}</h2>
            <p className="text-orange-500 text-xl font-semibold mb-4">{story.nakshatraName}</p>
            <p className="text-gray-300 text-base leading-relaxed mb-5">{story.description}</p>
            {story.luckyItems && (
              <div className="flex flex-wrap justify-center gap-3">
                {story.luckyItems.map((item, idx) => (
                  <div
                    key={idx}
                    className="flex items-center gap-2 bg-orange-500/20 px-3 py-2 rounded-full"
                  >
                    {idx === 0 && <Palette size={18} className="text-orange-500" />}
                    {idx === 1 && <Diamond size={18} className="text-orange-500" />}
                    {idx === 2 && <Compass size={18} className="text-orange-500" />}
                    <span className="text-orange-500 text-xs">{item.label}</span>
                  </div>
                ))}
              </div>
            )}
          </motion.div>
        );

      case STORY_TYPES.REMEDY:
        return (
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={isActive ? { opacity: 1, y: 0, scale: 1 } : {}}
            transition={{ duration: 0.4 }}
            className="flex flex-col items-center text-center px-6"
          >
            <div className="w-24 h-24 rounded-full bg-green-500/20 flex items-center justify-center mb-4">
              <Leaf size={48} className="text-green-500" />
            </div>
            <p className="text-gray-400 text-xs tracking-widest mb-2">{story.label}</p>
            <h2 className="text-white text-3xl font-bold mb-4">{story.title}</h2>
            <p className="text-gray-300 text-base leading-relaxed mb-5">{story.description}</p>
            {story.steps && (
              <div className="w-full space-y-3">
                {story.steps.map((step, idx) => (
                  <div key={idx} className="flex items-center gap-3">
                    <div className="w-7 h-7 rounded-full bg-green-500 flex items-center justify-center">
                      <span className="text-white text-sm font-bold">{idx + 1}</span>
                    </div>
                    <span className="text-gray-300 text-sm text-left flex-1">{step}</span>
                  </div>
                ))}
              </div>
            )}
          </motion.div>
        );

      case STORY_TYPES.LUCKY_TIME:
        return (
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={isActive ? { opacity: 1, y: 0, scale: 1 } : {}}
            transition={{ duration: 0.4 }}
            className="flex flex-col items-center text-center px-6"
          >
            <div className="w-24 h-24 rounded-full bg-amber-500/20 flex items-center justify-center mb-4">
              <Clock size={48} className="text-amber-500" />
            </div>
            <p className="text-gray-400 text-xs tracking-widest mb-2">{story.label}</p>
            <h2 className="text-white text-3xl font-bold mb-4">{story.title}</h2>
            <div className="flex flex-wrap justify-center gap-3 mb-5">
              {story.timeSlots?.map((slot, idx) => (
                <div
                  key={idx}
                  className="flex flex-col items-center px-4 py-3 rounded-xl"
                  style={{ backgroundColor: `${slot.color}30` }}
                >
                  {idx === 0 && <Sun size={24} style={{ color: slot.color }} />}
                  {idx === 1 && <Star size={24} style={{ color: slot.color }} />}
                  {idx === 2 && <Moon size={24} style={{ color: slot.color }} />}
                  <span className="text-white text-sm font-bold mt-2">{slot.time}</span>
                  <span className="text-gray-400 text-xs mt-1">{slot.label}</span>
                </div>
              ))}
            </div>
            <p className="text-gray-300 text-base leading-relaxed">{story.description}</p>
          </motion.div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="flex items-center justify-center min-h-full py-24">
      {renderContent()}
    </div>
  );
};

// Helper functions
function getPlanetDescription(planet, language) {
  const descriptions = {
    Sun: {
      en: 'The Sun brings leadership energy and vitality. Focus on career goals and self-expression today.',
      ta: 'சூரியன் தலைமைத்துவ சக்தியையும் உயிர்ச்சக்தியையும் தருகிறார். இன்று தொழில் இலக்குகள் மற்றும் சுய வெளிப்பாட்டில் கவனம் செலுத்துங்கள்.',
    },
    Moon: {
      en: 'The Moon enhances emotions and intuition. Trust your feelings and nurture close relationships.',
      ta: 'சந்திரன் உணர்வுகளையும் உள்ளுணர்வையும் மேம்படுத்துகிறார். உங்கள் உணர்வுகளை நம்புங்கள், நெருங்கிய உறவுகளை பேணுங்கள்.',
    },
    Mars: {
      en: 'Mars brings courage and determination. Channel this energy into physical activities and bold decisions.',
      ta: 'செவ்வாய் தைரியமும் உறுதியும் தருகிறார். இந்த சக்தியை உடல் செயல்பாடுகள் மற்றும் தைரியமான முடிவுகளுக்கு பயன்படுத்துங்கள்.',
    },
    Mercury: {
      en: 'Mercury enhances communication and intellect. Perfect day for learning, writing, and business deals.',
      ta: 'புதன் தொடர்பு மற்றும் அறிவை மேம்படுத்துகிறார். கற்றல், எழுத்து மற்றும் வணிக ஒப்பந்தங்களுக்கு சிறந்த நாள்.',
    },
    Jupiter: {
      en: 'Jupiter brings wisdom and expansion. Excellent for spiritual practices, education, and new opportunities.',
      ta: 'குரு ஞானமும் வளர்ச்சியும் தருகிறார். ஆன்மீக நடைமுறைகள், கல்வி மற்றும் புதிய வாய்ப்புகளுக்கு சிறந்தது.',
    },
    Venus: {
      en: 'Venus enhances love and beauty. Perfect for relationships, arts, and enjoying life\'s pleasures.',
      ta: 'சுக்கிரன் காதலையும் அழகையும் மேம்படுத்துகிறார். உறவுகள், கலைகள் மற்றும் வாழ்க்கை இன்பங்களுக்கு சிறந்தது.',
    },
    Saturn: {
      en: 'Saturn brings discipline and responsibility. Focus on long-term goals and complete pending tasks.',
      ta: 'சனி ஒழுக்கமும் பொறுப்பும் தருகிறார். நீண்ட கால இலக்குகளில் கவனம் செலுத்தி, நிலுவையில் உள்ள பணிகளை முடியுங்கள்.',
    },
  };
  return descriptions[planet]?.[language] || descriptions.Sun[language];
}

function getPlanetEffect(planet, userRasi, language) {
  const effects = {
    en: ['Career boost', 'Financial gains', 'Relationship harmony', 'Health improvement', 'Mental clarity'],
    ta: ['தொழில் உயர்வு', 'நிதி லாபம்', 'உறவு நல்லிணக்கம்', 'உடல்நலம் மேம்பாடு', 'மன தெளிவு'],
  };
  const seed = (userRasi || 'மேஷம்').charCodeAt(0) % effects[language].length;
  return effects[language][seed];
}

function getMoonRasi(date) {
  const rasis = Object.keys(rasiData);
  const dayOfYear = Math.floor((date - new Date(date.getFullYear(), 0, 0)) / (1000 * 60 * 60 * 24));
  return rasis[Math.floor(dayOfYear / 2.5) % 12];
}

function getMoonTransitDescription(moonRasi, language) {
  const element = rasiData[moonRasi]?.element;
  const descriptions = {
    fire: {
      en: 'Fiery energy dominates today. Great for taking initiative and pursuing passions.',
      ta: 'இன்று அக்னி சக்தி ஆதிக்கம். முன்முயற்சி எடுக்கவும், ஆர்வங்களை தொடரவும் சிறந்தது.',
    },
    earth: {
      en: 'Grounded energy prevails. Focus on practical matters and building stability.',
      ta: 'பூமி சக்தி நிலவுகிறது. நடைமுறை விஷயங்கள் மற்றும் நிலைத்தன்மையை உருவாக்குவதில் கவனம் செலுத்துங்கள்.',
    },
    air: {
      en: 'Intellectual energy is high. Perfect for communication, networking, and learning.',
      ta: 'அறிவுசார் சக்தி அதிகம். தொடர்பு, நெட்வொர்க்கிங் மற்றும் கற்றலுக்கு சிறந்தது.',
    },
    water: {
      en: 'Emotional energy flows today. Trust your intuition and nurture relationships.',
      ta: 'இன்று உணர்வுபூர்வ சக்தி பாய்கிறது. உங்கள் உள்ளுணர்வை நம்புங்கள், உறவுகளை பேணுங்கள்.',
    },
  };
  return descriptions[element]?.[language] || descriptions.fire[language];
}

function getMoonPersonalMessage(moonRasi, userRasi, language) {
  const messages = {
    en: `As a ${userRasi} native, this Moon transit brings positive energy to your relationships.`,
    ta: `${userRasi} ராசிக்காரராக, இந்த சந்திர சஞ்சாரம் உங்கள் உறவுகளுக்கு நேர்மறை சக்தியை தருகிறது.`,
  };
  return messages[language];
}

function getDailyInsightDescription(score, userRasi, language) {
  const level = score >= 80 ? 'excellent' : score >= 65 ? 'good' : 'moderate';
  const descriptions = {
    excellent: {
      en: 'Today is exceptionally favorable! The stars align for success. Take bold actions and trust your instincts.',
      ta: 'இன்று மிகவும் சாதகமானது! நட்சத்திரங்கள் வெற்றிக்கு ஒத்துவருகின்றன. தைரியமான நடவடிக்கைகள் எடுங்கள், உங்கள் உள்ளுணர்வை நம்புங்கள்.',
    },
    good: {
      en: 'A promising day awaits! Focus on your goals and maintain positive energy throughout.',
      ta: 'நம்பிக்கையான நாள் காத்திருக்கிறது! உங்கள் இலக்குகளில் கவனம் செலுத்தி, நேர்மறை ஆற்றலை பராமரியுங்கள்.',
    },
    moderate: {
      en: 'A balanced day ahead. Stay patient and avoid major decisions. Good for planning and preparation.',
      ta: 'சமநிலையான நாள் வரப்போகிறது. பொறுமையாக இருங்கள், பெரிய முடிவுகளை தவிர்க்கவும். திட்டமிடல் மற்றும் தயாரிப்புக்கு நல்லது.',
    },
  };
  return descriptions[level][language];
}

function getDailyTip(planet, language) {
  const tips = {
    Sun: {
      en: 'Offer water to the rising sun for positive energy',
      ta: 'நேர்மறை சக்திக்கு உதயமாகும் சூரியனுக்கு நீர் அர்ப்பணியுங்கள்',
    },
    Moon: {
      en: 'Wear white clothes and meditate tonight',
      ta: 'வெள்ளை ஆடை அணிந்து இன்று இரவு தியானம் செய்யுங்கள்',
    },
    Mars: {
      en: 'Exercise in the morning and visit Hanuman temple',
      ta: 'காலையில் உடற்பயிற்சி செய்து ஹனுமான் கோவிலுக்கு செல்லுங்கள்',
    },
    Mercury: {
      en: 'Chant Vishnu mantra and wear green',
      ta: 'விஷ்ணு மந்திரம் சொல்லி பச்சை நிற ஆடை அணியுங்கள்',
    },
    Jupiter: {
      en: 'Feed bananas to cows and help a teacher',
      ta: 'பசுக்களுக்கு வாழைப்பழம் கொடுத்து ஆசிரியருக்கு உதவுங்கள்',
    },
    Venus: {
      en: 'Offer white flowers to Lakshmi and wear perfume',
      ta: 'லட்சுமிக்கு வெள்ளை பூக்கள் சாற்றி வாசனை திரவியம் பூசுங்கள்',
    },
    Saturn: {
      en: 'Help the elderly and donate oil',
      ta: 'முதியவர்களுக்கு உதவி எண்ணெய் தானம் செய்யுங்கள்',
    },
  };
  return tips[planet]?.[language] || tips.Sun[language];
}

function getNakshatraDescription(nakshatra, language) {
  const descriptions = {
    en: `Your birth star ${nakshatra} is receiving positive vibrations today. The cosmic energy supports your natural talents and brings opportunities for growth.`,
    ta: `உங்கள் பிறந்த நட்சத்திரம் ${nakshatra} இன்று நேர்மறை அதிர்வுகளை பெறுகிறது. காஸ்மிக் சக்தி உங்கள் இயல்பான திறமைகளை ஆதரித்து வளர்ச்சிக்கான வாய்ப்புகளை தருகிறது.`,
  };
  return descriptions[language];
}

function getLuckyItems(nakshatra, language, t) {
  return [
    { label: `${t.color}: ${t.orange}` },
    { label: `${t.stone}: ${t.ruby}` },
    { label: `${t.direction}: ${t.east}` },
  ];
}

function getRemedyDescription(planet, language) {
  const descriptions = {
    en: 'Based on today\'s planetary alignment, here are simple remedies to enhance positive energy and minimize challenges.',
    ta: 'இன்றைய கிரக நிலைப்படி, நேர்மறை சக்தியை அதிகரிக்கவும், சவால்களை குறைக்கவும் எளிய பரிகாரங்கள்.',
  };
  return descriptions[language];
}

function getRemedySteps(planet, language) {
  const steps = {
    en: [
      'Light a diya with ghee in the morning',
      'Chant the planet mantra 11 times',
      'Donate items associated with the planet',
    ],
    ta: [
      'காலையில் நெய் விளக்கு ஏற்றுங்கள்',
      'கிரக மந்திரத்தை 11 முறை சொல்லுங்கள்',
      'கிரகத்துடன் தொடர்புடைய பொருட்களை தானம் செய்யுங்கள்',
    ],
  };
  return steps[language];
}

function getLuckyTimeSlots(language, t) {
  return [
    { time: '6:00 - 7:30', label: t.brahmaKala, color: '#f59e0b' },
    { time: '10:00 - 11:30', label: t.abhijit, color: '#22c55e' },
    { time: '17:00 - 18:30', label: t.eveningAuspicious, color: '#8b5cf6' },
  ];
}

function getLuckyTimeDescription(language) {
  const descriptions = {
    en: 'These time slots are especially auspicious for starting new ventures, important meetings, and spiritual practices.',
    ta: 'இந்த நேர இடைவெளிகள் புதிய முயற்சிகளை தொடங்க, முக்கிய சந்திப்புகள் மற்றும் ஆன்மீக நடைமுறைகளுக்கு குறிப்பாக சுபமானவை.',
  };
  return descriptions[language];
}

function calculateFallbackScore(userProfile) {
  const today = new Date();
  const seed = today.getDate() + today.getMonth() * 31;
  const nameSeed = (userProfile?.name || 'User').charCodeAt(0);
  return 60 + ((seed + nameSeed) % 35);
}

export default function Stories() {
  const navigate = useNavigate();
  const [stories, setStories] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [userProfile, setUserProfile] = useState(null);
  const [language, setLanguage] = useState('ta');
  const timerRef = useRef(null);

  const STORY_DURATION = 8000;
  const t = translations[language];

  // Load user profile
  useEffect(() => {
    const stored = localStorage.getItem('userProfile');
    if (stored) {
      const profile = JSON.parse(stored);
      setUserProfile(profile);
      setLanguage(profile.language || 'ta');
    }
  }, []);

  // Generate stories
  const generateStories = useCallback(() => {
    const userRasi = userProfile?.rasi || 'மேஷம்';
    const userNakshatra = userProfile?.nakshatra || 'அசுவினி';
    const today = new Date();
    const dayOfWeek = today.getDay();
    const dayPlanets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'];
    const todayPlanet = dayPlanets[dayOfWeek];
    const planetInfo = planetData[todayPlanet];
    const moonRasi = getMoonRasi(today);
    const score = calculateFallbackScore(userProfile);

    const generatedStories = [
      // Story 1: Planet Influence
      {
        id: '1',
        type: STORY_TYPES.PLANET_INFLUENCE,
        label: t.todayRulingPlanet,
        title: language === 'en' ? todayPlanet : planetInfo.tamil,
        description: getPlanetDescription(todayPlanet, language),
        planetColor: planetInfo.color,
        Icon: planetInfo.Icon,
        isPositive: ['Jupiter', 'Venus', 'Mercury'].includes(todayPlanet),
        effect: getPlanetEffect(todayPlanet, userRasi, language),
      },
      // Story 2: Moon Transit
      {
        id: '2',
        type: STORY_TYPES.MOON_TRANSIT,
        label: t.moonTransit,
        title: language === 'en'
          ? `${t.moonIn} ${rasiData[moonRasi]?.english}`
          : `${t.moonIn} ${moonRasi}ல்`,
        rasiSymbol: rasiData[moonRasi]?.symbol || '♈',
        rasiName: language === 'en' ? rasiData[moonRasi]?.english : moonRasi,
        description: getMoonTransitDescription(moonRasi, language),
        personalMessage: getMoonPersonalMessage(moonRasi, userRasi, language),
      },
      // Story 3: Daily Insight
      {
        id: '3',
        type: STORY_TYPES.DAILY_INSIGHT,
        label: t.yourDailyInsight,
        title: `${t.hey} ${userProfile?.name || 'நண்பரே'}!`,
        score: score,
        scoreLabel: t.todayScore,
        description: getDailyInsightDescription(score, userRasi, language),
        tip: getDailyTip(todayPlanet, language),
      },
      // Story 4: Nakshatra Effect
      {
        id: '4',
        type: STORY_TYPES.NAKSHATRA_EFFECT,
        label: t.nakshatraInfluence,
        title: t.yourStarMessage,
        nakshatraName: userNakshatra,
        description: getNakshatraDescription(userNakshatra, language),
        luckyItems: getLuckyItems(userNakshatra, language, t),
      },
      // Story 5: Remedy
      {
        id: '5',
        type: STORY_TYPES.REMEDY,
        label: t.todayRemedy,
        title: t.enhanceYourDay,
        description: getRemedyDescription(todayPlanet, language),
        steps: getRemedySteps(todayPlanet, language),
      },
      // Story 6: Lucky Time
      {
        id: '6',
        type: STORY_TYPES.LUCKY_TIME,
        label: t.luckyTimesToday,
        title: t.bestTimesForYou,
        timeSlots: getLuckyTimeSlots(language, t),
        description: getLuckyTimeDescription(language),
      },
    ];

    return generatedStories;
  }, [userProfile, language, t]);

  // Load stories
  useEffect(() => {
    if (userProfile !== null || localStorage.getItem('userProfile') === null) {
      const loadedStories = generateStories();
      setStories(loadedStories);
      setLoading(false);
    }
  }, [generateStories, userProfile]);

  // Auto-advance timer
  useEffect(() => {
    if (stories.length > 0 && currentIndex < stories.length) {
      timerRef.current = setTimeout(() => {
        if (currentIndex < stories.length - 1) {
          setCurrentIndex(currentIndex + 1);
        }
      }, STORY_DURATION);
    }

    return () => {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
      }
    };
  }, [currentIndex, stories.length]);

  const goToNext = () => {
    if (currentIndex < stories.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const goToPrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const handleClick = (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const width = rect.width;

    if (clickX < width / 3) {
      goToPrevious();
    } else if (clickX > (width * 2) / 3) {
      goToNext();
    }
  };

  const handleShare = async () => {
    const story = stories[currentIndex];
    const shareText = language === 'en'
      ? `🌟 Today's Astro Insight from Jothida AI:\n\n${story.title}\n${story.description}\n\nDownload Jothida AI for personalized astrology!`
      : `🌟 ஜோதிட AI இன் இன்றைய ஜோதிட பலன்:\n\n${story.title}\n${story.description}\n\nதனிப்பயனாக்கப்பட்ட ஜோதிடத்திற்கு ஜோதிட AI பதிவிறக்கவும்!`;

    if (navigator.share) {
      try {
        await navigator.share({ text: shareText });
      } catch (err) {
        console.log('Share cancelled');
      }
    } else {
      // Fallback: copy to clipboard
      await navigator.clipboard.writeText(shareText);
      alert(language === 'en' ? 'Copied to clipboard!' : 'கிளிப்போர்டுக்கு நகலெடுக்கப்பட்டது!');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-[#1a1a2e] via-[#16213e] to-[#0f3460] flex items-center justify-center">
        <p className="text-white text-lg">{t.loading}</p>
      </div>
    );
  }

  const currentStory = stories[currentIndex];
  const gradientClass = storyGradients[currentStory?.type] || storyGradients[STORY_TYPES.DAILY_INSIGHT];

  return (
    <div
      className={`min-h-screen bg-gradient-to-b ${gradientClass} pb-20 overflow-hidden`}
      onClick={handleClick}
    >
      {/* Progress Bars */}
      <div className="fixed top-4 left-3 right-3 flex gap-1 z-20">
        {stories.map((_, index) => (
          <ProgressBar
            key={index}
            index={index}
            activeIndex={currentIndex}
            duration={STORY_DURATION}
          />
        ))}
      </div>

      {/* Header */}
      <div className="fixed top-8 left-4 right-4 flex justify-between items-center z-20">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-orange-500/30 flex items-center justify-center">
            <svg width={24} height={24} viewBox="0 0 100 100">
              <path
                d="M50 5 L55 40 L90 30 L60 50 L90 70 L55 60 L50 95 L45 60 L10 70 L40 50 L10 30 L45 40 Z"
                fill="#fff"
              />
            </svg>
          </div>
          <div>
            <p className="text-white font-bold">{t.appName}</p>
            <p className="text-gray-400 text-xs">{t.dailyStories}</p>
          </div>
        </div>
        <button
          onClick={(e) => {
            e.stopPropagation();
            navigate('/dashboard');
          }}
          className="w-10 h-10 flex items-center justify-center"
        >
          <X size={28} className="text-white" />
        </button>
      </div>

      {/* Story Content */}
      <AnimatePresence mode="wait">
        <StoryCard
          key={currentIndex}
          story={currentStory}
          isActive={true}
          t={t}
          userProfile={userProfile}
        />
      </AnimatePresence>

      {/* Story Counter */}
      <div className="fixed bottom-28 left-0 right-0 flex justify-center z-20">
        <span className="text-gray-400 text-sm">
          {currentIndex + 1} / {stories.length}
        </span>
      </div>

      {/* Bottom Actions */}
      <div className="fixed bottom-20 left-0 right-0 flex justify-center gap-12 z-20">
        <button
          onClick={(e) => {
            e.stopPropagation();
            handleShare();
          }}
          className="flex flex-col items-center gap-1"
        >
          <Share2 size={28} className="text-white" />
          <span className="text-white text-xs">{t.share}</span>
        </button>
        <button
          onClick={(e) => {
            e.stopPropagation();
            navigate('/chat');
          }}
          className="flex flex-col items-center gap-1"
        >
          <MessageCircle size={28} className="text-white" />
          <span className="text-white text-xs">{t.askAI}</span>
        </button>
      </div>
    </div>
  );
}
