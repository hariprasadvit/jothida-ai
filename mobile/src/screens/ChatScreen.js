import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  TextInput,
  KeyboardAvoidingView,
  Platform,
  Dimensions,
  Animated,
  Easing,
  Share,
  Alert,
  Modal,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../context/AuthContext';
import { mobileAPI } from '../services/api';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Clipboard from 'expo-clipboard';

const { width } = Dimensions.get('window');

// Expanded question categories with Tamil content
const questionCategories = [
  {
    id: 'daily',
    name: 'தினசரி',
    icon: 'sunny',
    color: '#f97316',
    questions: [
      { icon: 'time', text: 'இன்று நல்ல நேரம் எப்போது?', category: 'time' },
      { icon: 'calendar', text: 'இன்றைய ராசிபலன் என்ன?', category: 'horoscope' },
      { icon: 'star', text: 'இன்று எந்த கிரகம் பலமாக உள்ளது?', category: 'planets' },
      { icon: 'alert-circle', text: 'இன்று தவிர்க்க வேண்டியவை என்ன?', category: 'avoid' },
    ],
  },
  {
    id: 'career',
    name: 'தொழில்',
    icon: 'briefcase',
    color: '#3b82f6',
    questions: [
      { icon: 'trending-up', text: 'தொழில் முன்னேற்றம் எப்போது?', category: 'career' },
      { icon: 'cash', text: 'பணவரவு எப்படி இருக்கும்?', category: 'finance' },
      { icon: 'business', text: 'புதிய வேலை கிடைக்குமா?', category: 'job' },
      { icon: 'bulb', text: 'சொந்த தொழில் செய்யலாமா?', category: 'business' },
    ],
  },
  {
    id: 'love',
    name: 'காதல்',
    icon: 'heart',
    color: '#ec4899',
    questions: [
      { icon: 'heart', text: 'என் காதல் வாழ்க்கை எப்படி?', category: 'love' },
      { icon: 'people', text: 'திருமணம் எப்போது நடக்கும்?', category: 'marriage' },
      { icon: 'home', text: 'இல்லறவாழ்க்கை சிறப்பாக இருக்குமா?', category: 'family' },
      { icon: 'happy', text: 'உறவுகள் சீராக இருக்குமா?', category: 'relationship' },
    ],
  },
  {
    id: 'health',
    name: 'உடல்நலம்',
    icon: 'fitness',
    color: '#22c55e',
    questions: [
      { icon: 'medkit', text: 'உடல்நிலை எப்படி இருக்கும்?', category: 'health' },
      { icon: 'nutrition', text: 'என்ன உணவு சாப்பிடலாம்?', category: 'food' },
      { icon: 'fitness', text: 'உடற்பயிற்சி செய்ய நல்ல நேரம்?', category: 'exercise' },
      { icon: 'medical', text: 'ஆரோக்கிய பரிகாரங்கள் என்ன?', category: 'remedies' },
    ],
  },
  {
    id: 'education',
    name: 'கல்வி',
    icon: 'school',
    color: '#8b5cf6',
    questions: [
      { icon: 'book', text: 'படிப்பு எப்படி இருக்கும்?', category: 'study' },
      { icon: 'trophy', text: 'தேர்வில் வெற்றி கிடைக்குமா?', category: 'exam' },
      { icon: 'globe', text: 'வெளிநாடு செல்ல வாய்ப்பு உண்டா?', category: 'abroad' },
      { icon: 'ribbon', text: 'உயர்கல்வி வாய்ப்பு என்ன?', category: 'higher_education' },
    ],
  },
  {
    id: 'spiritual',
    name: 'ஆன்மீகம்',
    icon: 'flame',
    color: '#f59e0b',
    questions: [
      { icon: 'leaf', text: 'என் ஆன்மீக வளர்ச்சி எப்படி?', category: 'spiritual' },
      { icon: 'star', text: 'எந்த தெய்வத்தை வழிபடுவது?', category: 'worship' },
      { icon: 'moon', text: 'பரிகாரங்கள் என்ன செய்யலாம்?', category: 'remedies' },
      { icon: 'compass', text: 'யோகம் இருக்கிறதா?', category: 'yoga' },
    ],
  },
];

// Get all questions flat
const getAllQuestions = () => {
  const questions = [];
  questionCategories.forEach(cat => {
    cat.questions.forEach(q => questions.push({ ...q, categoryColor: cat.color }));
  });
  return questions;
};

// Follow-up suggestions based on response category
const getFollowUpSuggestions = (category) => {
  const suggestions = {
    time: ['நாளை நல்ல நேரம் என்ன?', 'இந்த வாரம் சிறந்த நாள் எது?'],
    horoscope: ['இந்த மாத பலன் என்ன?', 'அடுத்த வாரம் எப்படி?'],
    career: ['எந்த துறையில் சிறப்பு?', 'சம்பள உயர்வு கிடைக்குமா?'],
    love: ['திருமண நாள் எப்போது?', 'வாழ்க்கைத்துணை எப்படி இருப்பார்?'],
    health: ['என்ன பரிகாரம் செய்யலாம்?', 'யோகா உதவுமா?'],
    finance: ['பணம் சேமிக்க வழி என்ன?', 'முதலீடு செய்யலாமா?'],
    default: ['மேலும் கேளுங்கள்', 'வேறு கேள்வி உள்ளதா?'],
  };
  return suggestions[category] || suggestions.default;
};

const welcomeMessage = {
  type: 'ai',
  text: 'வணக்கம்! நான் உங்கள் ஜோதிட AI உதவியாளர். எந்த கேள்வியும் கேளுங்கள் - தினசரி பலன், தொழில், காதல், உடல்நலம், கல்வி, ஆன்மீகம் என அனைத்தும் பதில் தருவேன்.',
  time: new Date().toLocaleTimeString('ta-IN', { hour: '2-digit', minute: '2-digit' }),
  insight: 'கீழே உள்ள பிரிவுகளை தொடர்ந்து விரைவாக கேள்வி கேளுங்கள்!',
};

// Animated Message Bubble
const AnimatedMessageBubble = ({ msg, isNew, onLongPress, onRetry }) => {
  const fadeAnim = useRef(new Animated.Value(isNew ? 0 : 1)).current;
  const scaleAnim = useRef(new Animated.Value(isNew ? 0.8 : 1)).current;
  const translateY = useRef(new Animated.Value(isNew ? 20 : 0)).current;

  useEffect(() => {
    if (isNew) {
      Animated.parallel([
        Animated.timing(fadeAnim, {
          toValue: 1,
          duration: 300,
          useNativeDriver: true,
        }),
        Animated.spring(scaleAnim, {
          toValue: 1,
          friction: 6,
          useNativeDriver: true,
        }),
        Animated.timing(translateY, {
          toValue: 0,
          duration: 300,
          easing: Easing.out(Easing.ease),
          useNativeDriver: true,
        }),
      ]).start();
    }
  }, []);

  return (
    <Animated.View
      style={[
        styles.messageRow,
        msg.type === 'user' ? styles.userRow : styles.aiRow,
        {
          opacity: fadeAnim,
          transform: [{ scale: scaleAnim }, { translateY }],
        },
      ]}
    >
      <TouchableOpacity
        activeOpacity={0.8}
        onLongPress={() => onLongPress && onLongPress(msg)}
        delayLongPress={500}
      >
        <View style={[styles.messageBubble, msg.type === 'user' ? styles.userBubble : styles.aiBubble]}>
          <Text style={[styles.messageText, msg.type === 'user' && styles.userText]}>{msg.text}</Text>

          {msg.data && <MessageData data={msg.data} />}

          {msg.predictions && <PredictionData predictions={msg.predictions} />}

          {msg.remedies && <RemediesData remedies={msg.remedies} />}

          {msg.insight && (
            <View style={styles.insightBox}>
              <Ionicons name="sparkles" size={14} color="#ea580c" />
              <Text style={styles.insightText}>{msg.insight}</Text>
            </View>
          )}

          {msg.followUp && msg.followUp.length > 0 && (
            <View style={styles.followUpContainer}>
              <Text style={styles.followUpTitle}>தொடர்ந்து கேளுங்கள்:</Text>
              {msg.followUp.map((suggestion, i) => (
                <TouchableOpacity key={i} style={styles.followUpPill}>
                  <Ionicons name="arrow-forward" size={12} color="#ea580c" />
                  <Text style={styles.followUpText}>{suggestion}</Text>
                </TouchableOpacity>
              ))}
            </View>
          )}

          {msg.isError && onRetry && (
            <TouchableOpacity style={styles.retryBtn} onPress={onRetry}>
              <Ionicons name="refresh" size={16} color="#ef4444" />
              <Text style={styles.retryText}>மீண்டும் முயற்சி</Text>
            </TouchableOpacity>
          )}
        </View>
      </TouchableOpacity>
      <Text style={styles.messageTime}>{msg.time}</Text>
    </Animated.View>
  );
};

// Prediction Data Component
const PredictionData = ({ predictions }) => {
  if (!predictions) return null;

  return (
    <View style={styles.predictionContainer}>
      {predictions.map((pred, i) => (
        <View key={i} style={styles.predictionItem}>
          <View style={styles.predictionHeader}>
            <Ionicons name={pred.icon || 'star'} size={16} color={pred.color || '#f97316'} />
            <Text style={styles.predictionTitle}>{pred.title}</Text>
          </View>
          <View style={styles.predictionScoreBar}>
            <View style={[styles.predictionScoreFill, { width: `${pred.score}%`, backgroundColor: pred.color || '#f97316' }]} />
          </View>
          <Text style={styles.predictionDesc}>{pred.description}</Text>
        </View>
      ))}
    </View>
  );
};

// Remedies Data Component
const RemediesData = ({ remedies }) => {
  if (!remedies) return null;

  return (
    <View style={styles.remediesContainer}>
      <View style={styles.remediesHeader}>
        <Ionicons name="leaf" size={16} color="#16a34a" />
        <Text style={styles.remediesTitle}>பரிகாரங்கள்</Text>
      </View>
      {remedies.map((remedy, i) => (
        <View key={i} style={styles.remedyItem}>
          <Text style={styles.remedyNumber}>{i + 1}</Text>
          <Text style={styles.remedyText}>{remedy}</Text>
        </View>
      ))}
    </View>
  );
};

// Animated Category Tab
const AnimatedCategoryTab = ({ category, isActive, onPress, index }) => {
  const scaleAnim = useRef(new Animated.Value(1)).current;
  const fadeAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 300,
      delay: index * 50,
      useNativeDriver: true,
    }).start();
  }, []);

  const handlePressIn = () => {
    Animated.spring(scaleAnim, { toValue: 0.9, useNativeDriver: true }).start();
  };

  const handlePressOut = () => {
    Animated.spring(scaleAnim, { toValue: 1, friction: 3, useNativeDriver: true }).start();
  };

  return (
    <Animated.View style={{ opacity: fadeAnim, transform: [{ scale: scaleAnim }] }}>
      <TouchableOpacity
        style={[styles.categoryTab, isActive && { backgroundColor: category.color + '20', borderColor: category.color }]}
        onPress={onPress}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        activeOpacity={1}
      >
        <Ionicons name={category.icon} size={18} color={isActive ? category.color : '#6b7280'} />
        <Text style={[styles.categoryTabText, isActive && { color: category.color, fontWeight: '600' }]}>
          {category.name}
        </Text>
      </TouchableOpacity>
    </Animated.View>
  );
};

// Animated Quick Card
const AnimatedQuickCard = ({ question, index, onPress, categoryColor }) => {
  const scaleAnim = useRef(new Animated.Value(1)).current;
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const translateY = useRef(new Animated.Value(30)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 400,
        delay: index * 80,
        useNativeDriver: true,
      }),
      Animated.spring(translateY, {
        toValue: 0,
        friction: 6,
        delay: index * 80,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  const handlePressIn = () => {
    Animated.spring(scaleAnim, { toValue: 0.95, useNativeDriver: true }).start();
  };

  const handlePressOut = () => {
    Animated.spring(scaleAnim, { toValue: 1, friction: 3, useNativeDriver: true }).start();
  };

  return (
    <Animated.View
      style={{
        flex: 1,
        opacity: fadeAnim,
        transform: [{ translateY }, { scale: scaleAnim }],
      }}
    >
      <TouchableOpacity
        style={[styles.quickCard, { borderColor: categoryColor + '40' }]}
        onPress={onPress}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        activeOpacity={1}
      >
        <View style={[styles.quickCardIcon, { backgroundColor: categoryColor + '20' }]}>
          <Ionicons name={question.icon} size={20} color={categoryColor || '#ea580c'} />
        </View>
        <Text style={styles.quickCardText} numberOfLines={2}>{question.text}</Text>
      </TouchableOpacity>
    </Animated.View>
  );
};

// Animated Quick Pill
const AnimatedQuickPill = ({ question, onPress }) => {
  const scaleAnim = useRef(new Animated.Value(1)).current;

  const handlePressIn = () => {
    Animated.spring(scaleAnim, { toValue: 0.9, useNativeDriver: true }).start();
  };

  const handlePressOut = () => {
    Animated.spring(scaleAnim, { toValue: 1, friction: 3, useNativeDriver: true }).start();
  };

  return (
    <Animated.View style={{ transform: [{ scale: scaleAnim }] }}>
      <TouchableOpacity
        style={[styles.quickPill, { borderColor: question.categoryColor + '60' }]}
        onPress={onPress}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        activeOpacity={1}
      >
        <Ionicons name={question.icon} size={14} color={question.categoryColor || '#ea580c'} />
        <Text style={styles.quickPillText} numberOfLines={1}>{question.text}</Text>
      </TouchableOpacity>
    </Animated.View>
  );
};

// Animated Typing Indicator
const TypingIndicator = () => {
  const dot1 = useRef(new Animated.Value(0)).current;
  const dot2 = useRef(new Animated.Value(0)).current;
  const dot3 = useRef(new Animated.Value(0)).current;
  const scaleAnim = useRef(new Animated.Value(0.9)).current;

  useEffect(() => {
    Animated.spring(scaleAnim, { toValue: 1, friction: 6, useNativeDriver: true }).start();

    const animate = (dot, delay) => {
      return Animated.loop(
        Animated.sequence([
          Animated.delay(delay),
          Animated.timing(dot, { toValue: 1, duration: 300, useNativeDriver: true }),
          Animated.timing(dot, { toValue: 0, duration: 300, useNativeDriver: true }),
        ])
      );
    };

    const a1 = animate(dot1, 0);
    const a2 = animate(dot2, 200);
    const a3 = animate(dot3, 400);

    a1.start();
    a2.start();
    a3.start();

    return () => {
      a1.stop();
      a2.stop();
      a3.stop();
    };
  }, []);

  const dotStyle = (anim) => ({
    transform: [{ translateY: anim.interpolate({ inputRange: [0, 1], outputRange: [0, -6] }) }],
  });

  return (
    <Animated.View style={[styles.messageRow, styles.aiRow, { transform: [{ scale: scaleAnim }] }]}>
      <View style={[styles.messageBubble, styles.aiBubble]}>
        <View style={styles.typingRow}>
          <View style={styles.typingDotsContainer}>
            <Animated.View style={[styles.typingDot, dotStyle(dot1)]} />
            <Animated.View style={[styles.typingDot, dotStyle(dot2)]} />
            <Animated.View style={[styles.typingDot, dotStyle(dot3)]} />
          </View>
          <Text style={styles.typingText}>AI சிந்திக்கிறது...</Text>
        </View>
      </View>
    </Animated.View>
  );
};

// Pulsing Status Dot
const PulsingStatusDot = () => {
  const pulseAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, { toValue: 1.3, duration: 800, useNativeDriver: true }),
        Animated.timing(pulseAnim, { toValue: 1, duration: 800, useNativeDriver: true }),
      ])
    ).start();
  }, []);

  return (
    <Animated.View style={[styles.statusDot, { transform: [{ scale: pulseAnim }] }]} />
  );
};

// Message Data Component
const MessageData = ({ data }) => {
  if (!data) return null;

  if (data.type === 'time_slots') {
    return (
      <View style={styles.dataContainer}>
        {data.slots?.map((slot, i) => (
          <AnimatedTimeSlot key={i} slot={slot} index={i} />
        ))}
      </View>
    );
  }

  if (data.type === 'horoscope') {
    return (
      <View style={styles.dataContainer}>
        <AnimatedHoroscopeScore data={data} />
      </View>
    );
  }

  if (data.type === 'planets') {
    return (
      <View style={styles.dataContainer}>
        {data.planets?.map((planet, i) => (
          <View key={i} style={styles.planetItem}>
            <Text style={styles.planetName}>{planet.name}</Text>
            <View style={[styles.planetStatus, { backgroundColor: planet.strength > 50 ? '#dcfce7' : '#fef3c7' }]}>
              <Text style={[styles.planetStrength, { color: planet.strength > 50 ? '#16a34a' : '#d97706' }]}>
                {planet.strength}%
              </Text>
            </View>
          </View>
        ))}
      </View>
    );
  }

  return null;
};

// Animated Time Slot
const AnimatedTimeSlot = ({ slot, index }) => {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const translateX = useRef(new Animated.Value(-20)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, { toValue: 1, duration: 300, delay: index * 100, useNativeDriver: true }),
      Animated.timing(translateX, { toValue: 0, duration: 300, delay: index * 100, useNativeDriver: true }),
    ]).start();
  }, []);

  return (
    <Animated.View style={[styles.timeSlot, { opacity: fadeAnim, transform: [{ translateX }] }]}>
      <View style={styles.timeSlotLeft}>
        <Text style={styles.timeSlotTime}>{slot.start}</Text>
        <Text style={styles.timeSlotSep}>முதல்</Text>
        <Text style={styles.timeSlotTime}>{slot.end}</Text>
      </View>
      <View style={styles.timeSlotRight}>
        <Text style={styles.timeSlotLabel}>{slot.label}</Text>
        <Text style={styles.timeSlotScore}>{slot.quality}%</Text>
      </View>
    </Animated.View>
  );
};

// Animated Horoscope Score
const AnimatedHoroscopeScore = ({ data }) => {
  const scaleAnim = useRef(new Animated.Value(0)).current;
  const rotateAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.spring(scaleAnim, { toValue: 1, friction: 4, useNativeDriver: true }),
      Animated.timing(rotateAnim, { toValue: 1, duration: 800, useNativeDriver: true }),
    ]).start();
  }, []);

  const rotate = rotateAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  return (
    <Animated.View style={[styles.horoscopeScore, { transform: [{ scale: scaleAnim }] }]}>
      <Text style={styles.horoscopeLabel}>இன்றைய மதிப்பெண்</Text>
      <Animated.View style={{ transform: [{ rotate }] }}>
        <LinearGradient colors={['#7c3aed', '#a855f7']} style={styles.horoscopeCircle}>
          <Text style={styles.horoscopeValue}>{data.overall_score}%</Text>
        </LinearGradient>
      </Animated.View>
    </Animated.View>
  );
};

// Animated Send Button
const AnimatedSendButton = ({ onPress, disabled }) => {
  const scaleAnim = useRef(new Animated.Value(1)).current;
  const rotateAnim = useRef(new Animated.Value(0)).current;

  const handlePressIn = () => {
    Animated.parallel([
      Animated.spring(scaleAnim, { toValue: 0.85, useNativeDriver: true }),
      Animated.timing(rotateAnim, { toValue: 1, duration: 200, useNativeDriver: true }),
    ]).start();
  };

  const handlePressOut = () => {
    Animated.parallel([
      Animated.spring(scaleAnim, { toValue: 1, friction: 3, useNativeDriver: true }),
      Animated.timing(rotateAnim, { toValue: 0, duration: 200, useNativeDriver: true }),
    ]).start();
  };

  const rotate = rotateAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '45deg'],
  });

  return (
    <Animated.View style={{ transform: [{ scale: scaleAnim }, { rotate }] }}>
      <TouchableOpacity
        style={[styles.sendBtn, disabled && styles.sendBtnDisabled]}
        onPress={onPress}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        disabled={disabled}
        activeOpacity={1}
      >
        <LinearGradient
          colors={!disabled ? ['#f97316', '#ef4444'] : ['#d1d5db', '#9ca3af']}
          style={styles.sendBtnGradient}
        >
          <Ionicons name="send" size={20} color="#fff" />
        </LinearGradient>
      </TouchableOpacity>
    </Animated.View>
  );
};

// Clear Chat Modal
const ClearChatModal = ({ visible, onClose, onConfirm }) => {
  return (
    <Modal transparent visible={visible} animationType="fade">
      <View style={styles.modalOverlay}>
        <View style={styles.modalContent}>
          <View style={styles.modalIcon}>
            <Ionicons name="trash" size={32} color="#ef4444" />
          </View>
          <Text style={styles.modalTitle}>அரட்டையை அழிக்கவா?</Text>
          <Text style={styles.modalText}>அனைத்து செய்திகளும் நீக்கப்படும். இது மீண்டும் மாற்ற முடியாது.</Text>
          <View style={styles.modalButtons}>
            <TouchableOpacity style={styles.modalCancelBtn} onPress={onClose}>
              <Text style={styles.modalCancelText}>வேண்டாம்</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.modalConfirmBtn} onPress={onConfirm}>
              <Text style={styles.modalConfirmText}>அழி</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </Modal>
  );
};

// Message Action Modal
const MessageActionModal = ({ visible, onClose, onCopy, onShare }) => {
  return (
    <Modal transparent visible={visible} animationType="fade">
      <TouchableOpacity style={styles.actionModalOverlay} onPress={onClose} activeOpacity={1}>
        <View style={styles.actionModalContent}>
          <TouchableOpacity style={styles.actionItem} onPress={onCopy}>
            <Ionicons name="copy" size={22} color="#374151" />
            <Text style={styles.actionText}>நகல் எடு</Text>
          </TouchableOpacity>
          <View style={styles.actionDivider} />
          <TouchableOpacity style={styles.actionItem} onPress={onShare}>
            <Ionicons name="share-social" size={22} color="#374151" />
            <Text style={styles.actionText}>பகிர்</Text>
          </TouchableOpacity>
        </View>
      </TouchableOpacity>
    </Modal>
  );
};

export default function ChatScreen() {
  const { userProfile } = useAuth();
  const [messages, setMessages] = useState([welcomeMessage]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [newMessageIndex, setNewMessageIndex] = useState(-1);
  const [activeCategory, setActiveCategory] = useState(null);
  const [showClearModal, setShowClearModal] = useState(false);
  const [selectedMessage, setSelectedMessage] = useState(null);
  const [showActionModal, setShowActionModal] = useState(false);
  const [lastFailedMessage, setLastFailedMessage] = useState(null);
  const scrollViewRef = useRef(null);
  const insets = useSafeAreaInsets();
  const bottomPadding = Platform.OS === 'android' ? Math.max(insets.bottom, 80) : insets.bottom + 80;

  // Header animation
  const headerFadeAnim = useRef(new Animated.Value(0)).current;
  const headerSlideAnim = useRef(new Animated.Value(-20)).current;

  // Load chat history on mount
  useEffect(() => {
    loadChatHistory();
  }, []);

  // Save chat history when messages change
  useEffect(() => {
    if (messages.length > 1) {
      saveChatHistory();
    }
  }, [messages]);

  useEffect(() => {
    Animated.parallel([
      Animated.timing(headerFadeAnim, {
        toValue: 1,
        duration: 500,
        useNativeDriver: true,
      }),
      Animated.timing(headerSlideAnim, {
        toValue: 0,
        duration: 500,
        useNativeDriver: true,
        easing: Easing.out(Easing.ease),
      }),
    ]).start();
  }, []);

  useEffect(() => {
    scrollViewRef.current?.scrollToEnd({ animated: true });
  }, [messages]);

  const loadChatHistory = async () => {
    try {
      const history = await AsyncStorage.getItem('chat_history');
      if (history) {
        const parsed = JSON.parse(history);
        if (parsed.length > 0) {
          setMessages([welcomeMessage, ...parsed]);
        }
      }
    } catch (error) {
      console.error('Error loading chat history:', error);
    }
  };

  const saveChatHistory = async () => {
    try {
      // Save only the last 50 messages (excluding welcome)
      const toSave = messages.slice(1).slice(-50);
      await AsyncStorage.setItem('chat_history', JSON.stringify(toSave));
    } catch (error) {
      console.error('Error saving chat history:', error);
    }
  };

  const clearChatHistory = async () => {
    try {
      await AsyncStorage.removeItem('chat_history');
      setMessages([welcomeMessage]);
      setShowClearModal(false);
    } catch (error) {
      console.error('Error clearing chat history:', error);
    }
  };

  const handleSend = async (messageText = inputText) => {
    if (!messageText.trim()) return;

    const userMessage = {
      type: 'user',
      text: messageText,
      time: new Date().toLocaleTimeString('ta-IN', { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages(prev => [...prev, userMessage]);
    setNewMessageIndex(messages.length);
    setInputText('');
    setIsTyping(true);
    setLastFailedMessage(messageText);

    try {
      const response = await mobileAPI.sendChatMessage(messageText, userProfile);
      setIsTyping(false);
      setLastFailedMessage(null);

      // Determine follow-up suggestions based on response
      const followUp = response.category ? getFollowUpSuggestions(response.category) : null;

      setMessages(prev => {
        setNewMessageIndex(prev.length);
        return [...prev, {
          type: 'ai',
          text: response.message,
          time: new Date().toLocaleTimeString('ta-IN', { hour: '2-digit', minute: '2-digit' }),
          data: response.data,
          predictions: response.predictions,
          remedies: response.remedies,
          insight: response.insight,
          followUp: followUp,
          category: response.category,
        }];
      });
    } catch (error) {
      console.error('Chat error:', error);
      setIsTyping(false);
      setMessages(prev => {
        setNewMessageIndex(prev.length);
        return [...prev, {
          type: 'ai',
          text: 'மன்னிக்கவும், தற்போது சேவையில் சிக்கல். மீண்டும் முயற்சிக்கவும்.',
          time: new Date().toLocaleTimeString('ta-IN', { hour: '2-digit', minute: '2-digit' }),
          isError: true,
          insight: 'இணைப்பை சரிபார்த்து மீண்டும் முயற்சிக்கவும்.',
        }];
      });
    }
  };

  const handleRetry = () => {
    if (lastFailedMessage) {
      // Remove the error message
      setMessages(prev => prev.slice(0, -1));
      handleSend(lastFailedMessage);
    }
  };

  const handleQuickQuestion = (question) => {
    handleSend(question.text);
  };

  const handleLongPressMessage = (msg) => {
    setSelectedMessage(msg);
    setShowActionModal(true);
  };

  const handleCopyMessage = async () => {
    if (selectedMessage) {
      try {
        await Clipboard.setStringAsync(selectedMessage.text);
        Alert.alert('நகல் எடுக்கப்பட்டது', 'செய்தி நகல் எடுக்கப்பட்டது!');
      } catch (e) {
        // Fallback - just close modal
      }
    }
    setShowActionModal(false);
  };

  const handleShareMessage = async () => {
    if (selectedMessage) {
      try {
        await Share.share({
          message: `ஜோதிட AI பதில்:\n\n${selectedMessage.text}${selectedMessage.insight ? `\n\n💡 ${selectedMessage.insight}` : ''}`,
        });
      } catch (e) {
        // User cancelled
      }
    }
    setShowActionModal(false);
  };

  const currentQuestions = activeCategory
    ? questionCategories.find(c => c.id === activeCategory)?.questions || []
    : getAllQuestions().slice(0, 8);

  const currentCategoryColor = activeCategory
    ? questionCategories.find(c => c.id === activeCategory)?.color || '#f97316'
    : '#f97316';

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={90}
    >
      <LinearGradient colors={['#fff7ed', '#ffffff', '#fff7ed']} style={styles.gradient}>
        <LinearGradient
          colors={['#f97316', '#fbbf24', '#f97316']}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 0 }}
          style={styles.headerBar}
        />

        <Animated.View
          style={[
            styles.header,
            {
              opacity: headerFadeAnim,
              transform: [{ translateY: headerSlideAnim }],
            },
          ]}
        >
          <View style={styles.headerLeft}>
            <LinearGradient colors={['#f97316', '#ef4444']} style={styles.aiAvatar}>
              <Ionicons name="sparkles" size={24} color="#fff" />
            </LinearGradient>
            <View>
              <Text style={styles.headerTitle}>ஜோதிட AI</Text>
              <View style={styles.statusRow}>
                <PulsingStatusDot />
                <Text style={styles.statusText}>ஆன்லைன் • எல்லா கேள்விகளுக்கும் பதில்</Text>
              </View>
            </View>
          </View>
          <TouchableOpacity style={styles.clearBtn} onPress={() => setShowClearModal(true)}>
            <Ionicons name="trash-outline" size={20} color="#9ca3af" />
          </TouchableOpacity>
        </Animated.View>

        {/* Category Tabs */}
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          style={styles.categoryTabsRow}
          contentContainerStyle={styles.categoryTabsContent}
        >
          <AnimatedCategoryTab
            category={{ id: 'all', name: 'அனைத்தும்', icon: 'apps', color: '#f97316' }}
            isActive={activeCategory === null}
            onPress={() => setActiveCategory(null)}
            index={0}
          />
          {questionCategories.map((cat, i) => (
            <AnimatedCategoryTab
              key={cat.id}
              category={cat}
              isActive={activeCategory === cat.id}
              onPress={() => setActiveCategory(cat.id)}
              index={i + 1}
            />
          ))}
        </ScrollView>

        <ScrollView
          ref={scrollViewRef}
          style={styles.messagesContainer}
          contentContainerStyle={styles.messagesContent}
        >
          {/* Quick Question Cards - Only show if no user messages yet */}
          {messages.length <= 1 && (
            <View style={styles.quickCardsContainer}>
              <View style={styles.quickCardsRow}>
                {currentQuestions.slice(0, 2).map((q, i) => (
                  <AnimatedQuickCard
                    key={`${activeCategory}-${i}`}
                    question={q}
                    index={i}
                    onPress={() => handleQuickQuestion(q)}
                    categoryColor={currentCategoryColor}
                  />
                ))}
              </View>
              <View style={styles.quickCardsRow}>
                {currentQuestions.slice(2, 4).map((q, i) => (
                  <AnimatedQuickCard
                    key={`${activeCategory}-${i + 2}`}
                    question={q}
                    index={i + 2}
                    onPress={() => handleQuickQuestion(q)}
                    categoryColor={currentCategoryColor}
                  />
                ))}
              </View>
            </View>
          )}

          {/* Messages */}
          {messages.map((msg, i) => (
            <AnimatedMessageBubble
              key={i}
              msg={msg}
              isNew={i === newMessageIndex}
              onLongPress={handleLongPressMessage}
              onRetry={msg.isError ? handleRetry : null}
            />
          ))}

          {isTyping && <TypingIndicator />}
        </ScrollView>

        {/* Quick Pills - Always visible */}
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          style={styles.quickPillsRow}
          contentContainerStyle={styles.quickPillsContent}
        >
          {getAllQuestions().slice(0, 6).map((q, i) => (
            <AnimatedQuickPill
              key={i}
              question={q}
              onPress={() => handleQuickQuestion(q)}
            />
          ))}
        </ScrollView>

        <View style={[styles.inputContainer, { paddingBottom: bottomPadding }]}>
          <TextInput
            style={styles.input}
            value={inputText}
            onChangeText={setInputText}
            placeholder="தமிழில் எந்த கேள்வியும் கேளுங்கள்..."
            placeholderTextColor="#9ca3af"
            multiline
            onSubmitEditing={() => handleSend()}
          />
          <AnimatedSendButton onPress={() => handleSend()} disabled={!inputText.trim()} />
        </View>
      </LinearGradient>

      <ClearChatModal
        visible={showClearModal}
        onClose={() => setShowClearModal(false)}
        onConfirm={clearChatHistory}
      />

      <MessageActionModal
        visible={showActionModal}
        onClose={() => setShowActionModal(false)}
        onCopy={handleCopyMessage}
        onShare={handleShareMessage}
      />
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  gradient: { flex: 1 },
  headerBar: { height: 4 },
  header: {
    padding: 16,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#fed7aa',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  headerLeft: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  aiAvatar: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
  },
  headerTitle: { fontSize: 18, fontWeight: 'bold', color: '#1f2937' },
  statusRow: { flexDirection: 'row', alignItems: 'center', gap: 6, marginTop: 2 },
  statusDot: { width: 8, height: 8, borderRadius: 4, backgroundColor: '#22c55e' },
  statusText: { fontSize: 11, color: '#16a34a' },
  clearBtn: { padding: 8 },

  // Category Tabs
  categoryTabsRow: {
    maxHeight: 50,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#f3f4f6',
  },
  categoryTabsContent: {
    paddingHorizontal: 12,
    paddingVertical: 8,
    gap: 8,
    flexDirection: 'row',
  },
  categoryTab: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 14,
    paddingVertical: 8,
    backgroundColor: '#f9fafb',
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#e5e7eb',
  },
  categoryTabText: {
    fontSize: 12,
    color: '#6b7280',
  },

  // Quick Cards (shown initially)
  quickCardsContainer: {
    marginBottom: 16,
  },
  quickCardsRow: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 12,
  },
  quickCard: {
    flex: 1,
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: '#fed7aa',
    minHeight: 90,
    justifyContent: 'flex-start',
  },
  quickCardIcon: {
    width: 36,
    height: 36,
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
  },
  quickCardText: {
    fontSize: 13,
    color: '#374151',
    lineHeight: 18,
  },

  // Quick Pills (always visible above input)
  quickPillsRow: {
    maxHeight: 50,
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderTopColor: '#f3f4f6',
  },
  quickPillsContent: {
    paddingHorizontal: 12,
    paddingVertical: 8,
    gap: 8,
    flexDirection: 'row',
  },
  quickPill: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 12,
    paddingVertical: 6,
    backgroundColor: '#fff7ed',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#fed7aa',
  },
  quickPillText: {
    fontSize: 11,
    color: '#374151',
    maxWidth: 120,
  },

  // Messages
  messagesContainer: { flex: 1 },
  messagesContent: { padding: 16, paddingBottom: 20 },
  messageRow: { marginBottom: 16 },
  userRow: { alignItems: 'flex-end' },
  aiRow: { alignItems: 'flex-start' },
  messageBubble: { maxWidth: '85%', padding: 14, borderRadius: 16 },
  userBubble: { backgroundColor: '#f97316', borderBottomRightRadius: 4 },
  aiBubble: { backgroundColor: '#fff', borderWidth: 1, borderColor: '#fed7aa', borderBottomLeftRadius: 4 },
  messageText: { fontSize: 14, lineHeight: 20, color: '#374151' },
  userText: { color: '#fff' },
  messageTime: { fontSize: 10, color: '#9ca3af', marginTop: 4 },
  insightBox: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 6,
    marginTop: 12,
    padding: 10,
    backgroundColor: '#fff7ed',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#fed7aa',
  },
  insightText: { flex: 1, fontSize: 11, color: '#9a3412', lineHeight: 16 },
  typingRow: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  typingDotsContainer: { flexDirection: 'row', gap: 4 },
  typingDot: { width: 8, height: 8, borderRadius: 4, backgroundColor: '#ea580c' },
  typingText: { fontSize: 13, color: '#6b7280' },

  // Follow-up suggestions
  followUpContainer: {
    marginTop: 12,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#f3f4f6',
  },
  followUpTitle: {
    fontSize: 11,
    color: '#6b7280',
    marginBottom: 8,
  },
  followUpPill: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 10,
    paddingVertical: 6,
    backgroundColor: '#fff7ed',
    borderRadius: 12,
    marginBottom: 6,
    alignSelf: 'flex-start',
  },
  followUpText: {
    fontSize: 11,
    color: '#ea580c',
  },

  // Retry button
  retryBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginTop: 12,
    paddingVertical: 8,
    paddingHorizontal: 12,
    backgroundColor: '#fef2f2',
    borderRadius: 8,
    alignSelf: 'flex-start',
  },
  retryText: {
    fontSize: 12,
    color: '#ef4444',
    fontWeight: '500',
  },

  // Prediction data
  predictionContainer: {
    marginTop: 12,
  },
  predictionItem: {
    marginBottom: 12,
    padding: 10,
    backgroundColor: '#fafafa',
    borderRadius: 10,
  },
  predictionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginBottom: 6,
  },
  predictionTitle: {
    fontSize: 13,
    fontWeight: '600',
    color: '#374151',
  },
  predictionScoreBar: {
    height: 6,
    backgroundColor: '#e5e7eb',
    borderRadius: 3,
    marginBottom: 6,
    overflow: 'hidden',
  },
  predictionScoreFill: {
    height: '100%',
    borderRadius: 3,
  },
  predictionDesc: {
    fontSize: 12,
    color: '#6b7280',
    lineHeight: 16,
  },

  // Remedies data
  remediesContainer: {
    marginTop: 12,
    padding: 12,
    backgroundColor: '#f0fdf4',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#bbf7d0',
  },
  remediesHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginBottom: 10,
  },
  remediesTitle: {
    fontSize: 13,
    fontWeight: '600',
    color: '#16a34a',
  },
  remedyItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 8,
    marginBottom: 8,
  },
  remedyNumber: {
    width: 20,
    height: 20,
    backgroundColor: '#16a34a',
    borderRadius: 10,
    color: '#fff',
    fontSize: 11,
    fontWeight: '600',
    textAlign: 'center',
    lineHeight: 20,
  },
  remedyText: {
    flex: 1,
    fontSize: 12,
    color: '#374151',
    lineHeight: 18,
  },

  // Data displays
  dataContainer: { marginTop: 12 },
  timeSlot: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 10,
    backgroundColor: '#f0fdf4',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#bbf7d0',
    marginBottom: 6,
  },
  timeSlotLeft: { alignItems: 'center' },
  timeSlotTime: { fontSize: 14, fontWeight: '600', color: '#15803d' },
  timeSlotSep: { fontSize: 10, color: '#6b7280' },
  timeSlotRight: { alignItems: 'flex-end' },
  timeSlotLabel: { fontSize: 12, color: '#15803d', fontWeight: '500' },
  timeSlotScore: { fontSize: 20, fontWeight: 'bold', color: '#16a34a' },
  horoscopeScore: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 12,
    backgroundColor: '#faf5ff',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: '#e9d5ff',
  },
  horoscopeLabel: { fontSize: 12, color: '#7c3aed' },
  horoscopeCircle: {
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
  },
  horoscopeValue: { fontSize: 18, fontWeight: 'bold', color: '#fff' },

  // Planet data
  planetItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 10,
    backgroundColor: '#fafafa',
    borderRadius: 8,
    marginBottom: 6,
  },
  planetName: {
    fontSize: 13,
    fontWeight: '500',
    color: '#374151',
  },
  planetStatus: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  planetStrength: {
    fontSize: 12,
    fontWeight: '600',
  },

  // Input
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    padding: 12,
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderTopColor: '#fed7aa',
    gap: 10,
  },
  input: {
    flex: 1,
    backgroundColor: '#f9fafb',
    borderWidth: 1,
    borderColor: '#e5e7eb',
    borderRadius: 24,
    paddingHorizontal: 16,
    paddingVertical: 12,
    fontSize: 14,
    maxHeight: 100,
  },
  sendBtn: { width: 48, height: 48, borderRadius: 24, overflow: 'hidden' },
  sendBtnDisabled: { opacity: 0.5 },
  sendBtnGradient: { width: 48, height: 48, justifyContent: 'center', alignItems: 'center' },

  // Modals
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  modalContent: {
    backgroundColor: '#fff',
    borderRadius: 20,
    padding: 24,
    width: '100%',
    maxWidth: 320,
    alignItems: 'center',
  },
  modalIcon: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: '#fef2f2',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 8,
  },
  modalText: {
    fontSize: 14,
    color: '#6b7280',
    textAlign: 'center',
    lineHeight: 20,
    marginBottom: 20,
  },
  modalButtons: {
    flexDirection: 'row',
    gap: 12,
  },
  modalCancelBtn: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 12,
    backgroundColor: '#f3f4f6',
    alignItems: 'center',
  },
  modalCancelText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#6b7280',
  },
  modalConfirmBtn: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 12,
    backgroundColor: '#ef4444',
    alignItems: 'center',
  },
  modalConfirmText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#fff',
  },

  // Action Modal
  actionModalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.3)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  actionModalContent: {
    backgroundColor: '#fff',
    borderRadius: 16,
    width: 200,
    overflow: 'hidden',
  },
  actionItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    padding: 16,
  },
  actionText: {
    fontSize: 15,
    color: '#374151',
  },
  actionDivider: {
    height: 1,
    backgroundColor: '#f3f4f6',
  },
});
