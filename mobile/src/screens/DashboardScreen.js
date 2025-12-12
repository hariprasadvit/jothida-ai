import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  RefreshControl,
  Platform,
  Animated,
  Easing,
  Modal,
  Dimensions,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import Svg, { Path, Circle } from 'react-native-svg';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { mobileAPI } from '../services/api';
import notificationService from '../services/notificationService';

const { width } = Dimensions.get('window');

// Planet API name to translation key mapping
const planetTranslationKeys = {
  'Sun': 'sun_planet',
  'Moon': 'moon_planet',
  'Mars': 'mars',
  'Mercury': 'mercury',
  'Jupiter': 'jupiter',
  'Venus': 'venus',
  'Saturn': 'saturn',
  'Rahu': 'rahu',
  'Ketu': 'ketu',
};

// Tamil month names
const tamilMonths = [
  'சித்திரை', 'வைகாசி', 'ஆனி', 'ஆடி', 'ஆவணி', 'புரட்டாசி',
  'ஐப்பசி', 'கார்த்திகை', 'மார்கழி', 'தை', 'மாசி', 'பங்குனி'
];

const getTamilDay = (dayIndex) => {
  const days = ['ஞாயிறு', 'திங்கள்', 'செவ்வாய்', 'புதன்', 'வியாழன்', 'வெள்ளி', 'சனி'];
  return days[dayIndex];
};

// Format date in Tamil style
const formatTamilDate = (date) => {
  const d = new Date(date);
  const day = d.getDate();
  const month = d.getMonth();
  const year = d.getFullYear();
  const dayName = getTamilDay(d.getDay());

  const tamilMonthNames = [
    'ஜனவரி', 'பிப்ரவரி', 'மார்ச்', 'ஏப்ரல்', 'மே', 'ஜூன்',
    'ஜூலை', 'ஆகஸ்ட்', 'செப்டம்பர்', 'அக்டோபர்', 'நவம்பர்', 'டிசம்பர்'
  ];

  return `${dayName}, ${day} ${tamilMonthNames[month]} ${year}`;
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

// Animated Progress Bar
const AnimatedProgressBar = ({ score, color, delay = 0 }) => {
  const widthAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(widthAnim, {
      toValue: score,
      duration: 1000,
      delay,
      useNativeDriver: false,
      easing: Easing.out(Easing.ease),
    }).start();
  }, [score]);

  return (
    <View style={styles.progressBar}>
      <Animated.View
        style={[
          styles.progressFill,
          {
            backgroundColor: color,
            width: widthAnim.interpolate({
              inputRange: [0, 100],
              outputRange: ['0%', '100%'],
            }),
          },
        ]}
      />
    </View>
  );
};

// Animated Score Circle - Tappable
const AnimatedScoreCircle = ({ score, onPress, tapText }) => {
  const scaleAnim = useRef(new Animated.Value(0)).current;
  const rotateAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.spring(scaleAnim, {
        toValue: 1,
        friction: 4,
        tension: 50,
        useNativeDriver: true,
      }),
      Animated.timing(rotateAnim, {
        toValue: 1,
        duration: 800,
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
    <TouchableOpacity onPress={onPress} activeOpacity={0.8}>
      <Animated.View
        style={[
          styles.scoreCircle,
          { transform: [{ scale: scaleAnim }, { rotate }] },
        ]}
      >
        <Text style={styles.scoreCircleText}>{score}%</Text>
        <Text style={styles.tapHint}>{tapText}</Text>
      </Animated.View>
    </TouchableOpacity>
  );
};

// Animated Quick Action Button
const AnimatedQuickAction = ({ action, index, onPress }) => {
  const scaleAnim = useRef(new Animated.Value(1)).current;
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const translateY = useRef(new Animated.Value(20)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 400,
        delay: 300 + index * 100,
        useNativeDriver: true,
      }),
      Animated.spring(translateY, {
        toValue: 0,
        friction: 6,
        delay: 300 + index * 100,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  const handlePressIn = () => {
    Animated.spring(scaleAnim, { toValue: 0.92, useNativeDriver: true }).start();
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
        style={styles.quickActionBtn}
        onPress={onPress}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        activeOpacity={1}
      >
        <Ionicons name={action.icon} size={24} color={action.color} />
        <Text style={styles.quickActionLabel}>{action.label}</Text>
      </TouchableOpacity>
    </Animated.View>
  );
};

// Animated Life Area Card - Tappable for score details
const AnimatedLifeAreaCard = ({ area, index, onPress, t }) => {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const scaleAnim = useRef(new Animated.Value(0.8)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 400,
        delay: 200 + index * 100,
        useNativeDriver: true,
      }),
      Animated.spring(scaleAnim, {
        toValue: 1,
        friction: 6,
        delay: 200 + index * 100,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  return (
    <TouchableOpacity onPress={() => onPress(area)} activeOpacity={0.8}>
      <Animated.View
        style={[
          styles.lifeAreaCard,
          { opacity: fadeAnim, transform: [{ scale: scaleAnim }] },
        ]}
      >
        <View style={styles.lifeAreaHeader}>
          <Ionicons name={area.icon} size={20} color={area.color} />
          <View style={[styles.lifeAreaBadge, { backgroundColor: area.score > 75 ? '#dcfce7' : area.score > 50 ? '#fef3c7' : '#fef2f2' }]}>
            <Text style={[styles.lifeAreaBadgeText, { color: area.score > 75 ? '#16a34a' : area.score > 50 ? '#d97706' : '#dc2626' }]}>
              {area.score > 75 ? t('good') : area.score > 50 ? t('average') : t('caution')}
            </Text>
          </View>
        </View>
        <Text style={styles.lifeAreaName}>{area.name}</Text>
        <View style={styles.lifeAreaScoreRow}>
          <Text style={[styles.lifeAreaScore, { color: area.color }]}>{area.score}</Text>
          <Text style={styles.lifeAreaMax}>/100</Text>
          <Ionicons name="chevron-forward" size={16} color="#9ca3af" style={{ marginLeft: 'auto' }} />
        </View>
        <AnimatedProgressBar score={area.score} color={area.color} delay={400 + index * 100} />
      </Animated.View>
    </TouchableOpacity>
  );
};

// Month Projection Card
const MonthProjectionCard = ({ month, index, onPress }) => {
  const fadeAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 300,
      delay: index * 50,
      useNativeDriver: true,
    }).start();
  }, []);

  const getScoreColor = (score) => {
    if (score >= 75) return '#16a34a';
    if (score >= 50) return '#d97706';
    return '#dc2626';
  };

  return (
    <TouchableOpacity onPress={() => onPress(month)} activeOpacity={0.8}>
      <Animated.View style={[styles.monthCard, { opacity: fadeAnim }]}>
        <Text style={styles.monthName}>{month.name}</Text>
        <View style={[styles.monthScoreBadge, { backgroundColor: getScoreColor(month.score) + '20' }]}>
          <Text style={[styles.monthScore, { color: getScoreColor(month.score) }]}>{month.score}</Text>
        </View>
        <View style={styles.monthBarContainer}>
          <View style={[styles.monthBar, { width: `${month.score}%`, backgroundColor: getScoreColor(month.score) }]} />
        </View>
      </Animated.View>
    </TouchableOpacity>
  );
};

// Year Projection Card
const YearProjectionCard = ({ year, onPress }) => {
  const color = year.color || (year.score >= 75 ? '#16a34a' : year.score >= 50 ? '#d97706' : '#dc2626');

  return (
    <TouchableOpacity onPress={() => onPress(year)} activeOpacity={0.8} style={styles.yearCard}>
      <LinearGradient
        colors={[color + '10', color + '20']}
        style={styles.yearCardGradient}
      >
        <View style={[styles.yearIconBg, { backgroundColor: color + '20' }]}>
          <Ionicons name={year.icon || 'calendar'} size={20} color={color} />
        </View>
        <View style={styles.yearInfo}>
          <Text style={styles.yearName}>{year.year}</Text>
          <Text style={styles.yearLabel}>{year.label}</Text>
        </View>
        <View style={styles.yearScoreContainer}>
          <Text style={[styles.yearScore, { color }]}>{year.score}%</Text>
          <View style={[styles.yearScoreBar, { backgroundColor: color + '30' }]}>
            <View style={[styles.yearScoreFill, { width: `${year.score}%`, backgroundColor: color }]} />
          </View>
        </View>
        <Ionicons name="chevron-forward" size={18} color={color} />
      </LinearGradient>
    </TouchableOpacity>
  );
};

// Pulsing Sparkle Icon
const PulsingSparkle = () => {
  const pulseAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, { toValue: 1.3, duration: 800, useNativeDriver: true, easing: Easing.inOut(Easing.ease) }),
        Animated.timing(pulseAnim, { toValue: 1, duration: 800, useNativeDriver: true, easing: Easing.inOut(Easing.ease) }),
      ])
    ).start();
  }, []);

  return (
    <Animated.View style={{ transform: [{ scale: pulseAnim }] }}>
      <Ionicons name="sparkles" size={16} color="#ea580c" />
    </Animated.View>
  );
};

// Component name translation key mapping
const COMPONENT_KEYS = {
  dasha: { key: 'dashaBhukti', icon: 'time', color: '#8b5cf6' },
  house: { key: 'housePower', icon: 'home', color: '#3b82f6' },
  planet_strength: { key: 'planetPower', icon: 'planet', color: '#f59e0b' },
  transit: { key: 'transit', icon: 'swap-horizontal', color: '#10b981' },
  yoga: { key: 'yogaDosham', icon: 'sparkles', color: '#ec4899' },
  navamsa: { key: 'navamsam', icon: 'grid', color: '#6366f1' },
  // Life area components
  karaka: { key: 'karakaPlanet', icon: 'star', color: '#f97316' },
};

// Area name translation key mapping
const AREA_KEYS = {
  career: { key: 'careerLabel', icon: 'briefcase', color: '#3b82f6' },
  finance: { key: 'financeLabel', icon: 'wallet', color: '#10b981' },
  health: { key: 'healthLabel', icon: 'heart', color: '#ef4444' },
  relationships: { key: 'relationshipsLabel', icon: 'people', color: '#ec4899' },
};

// Score Justification Modal
const ScoreJustificationModal = ({ visible, onClose, data, t }) => {
  if (!data) return null;

  const breakdown = data.breakdown || {};
  const trace = data.calculation_trace || {};
  const stepByStep = trace.step_by_step || [];

  return (
    <Modal transparent visible={visible} animationType="slide">
      <View style={styles.modalOverlay}>
        <ScrollView style={styles.modalScrollView}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <View style={[styles.modalIconBg, { backgroundColor: (data.color || '#f97316') + '20' }]}>
                <Ionicons name={data.icon || 'star'} size={28} color={data.color || '#f97316'} />
              </View>
              <Text style={styles.modalTitle}>{data.title || data.name}</Text>
              <TouchableOpacity style={styles.modalCloseBtn} onPress={onClose}>
                <Ionicons name="close" size={24} color="#6b7280" />
              </TouchableOpacity>
            </View>

            <View style={styles.modalScoreSection}>
              <Text style={[styles.modalScoreValue, { color: data.color || '#f97316' }]}>{data.score}</Text>
              <Text style={styles.modalScoreMax}>/100</Text>
            </View>

            {data.quality && (
              <View style={[styles.qualityBadge, { backgroundColor: data.score >= 70 ? '#dcfce7' : data.score >= 50 ? '#fef3c7' : '#fee2e2' }]}>
                <Text style={[styles.qualityText, { color: data.score >= 70 ? '#166534' : data.score >= 50 ? '#a16207' : '#dc2626' }]}>
                  {data.quality}
                </Text>
              </View>
            )}

            {/* Dasha/Bhukti Info */}
            {(data.dasha_lord || data.bhukti_lord) && (
              <View style={styles.dashaInfoBox}>
                <Ionicons name="time" size={16} color="#8b5cf6" />
                <Text style={styles.dashaInfoText}>
                  {data.dasha_lord} {t('dashaLabel')} {data.bhukti_lord ? `- ${data.bhukti_lord} ${t('bhuktiLabel')}` : ''}
                </Text>
              </View>
            )}

            <View style={styles.modalDivider} />

            {/* Detailed Breakdown Section */}
            {stepByStep.length > 0 && (
              <>
                <Text style={styles.modalSectionTitle}>📊 {t('scoreCalculation')}</Text>
                <Text style={styles.formulaText}>{trace.formula}</Text>

                {stepByStep.map((step, i) => {
                  const compInfo = COMPONENT_KEYS[step.component] || { key: step.component, icon: 'help', color: '#6b7280' };
                  return (
                    <View key={i} style={styles.breakdownCard}>
                      <View style={styles.breakdownHeader}>
                        <View style={[styles.breakdownIconBg, { backgroundColor: compInfo.color + '20' }]}>
                          <Ionicons name={compInfo.icon} size={16} color={compInfo.color} />
                        </View>
                        <View style={styles.breakdownTitleRow}>
                          <Text style={styles.breakdownTitle}>{t(compInfo.key) || step.component}</Text>
                          <Text style={styles.breakdownWeight}>({step.weight})</Text>
                        </View>
                        <Text style={[styles.breakdownContribution, { color: compInfo.color }]}>
                          {step.contribution}
                        </Text>
                      </View>

                      {/* Progress bar for contribution */}
                      <View style={styles.breakdownProgressBg}>
                        <View style={[styles.breakdownProgressFill, {
                          width: `${Math.min(100, step.contribution * 3.33)}%`,
                          backgroundColor: compInfo.color
                        }]} />
                      </View>

                      {/* Factors for this component */}
                      {step.factors_detail && step.factors_detail.length > 0 && (
                        <View style={styles.breakdownFactors}>
                          {step.factors_detail.slice(0, 3).map((f, j) => (
                            <View key={j} style={styles.miniFactorRow}>
                              <Ionicons
                                name={f.positive !== false ? 'add-circle' : 'remove-circle'}
                                size={12}
                                color={f.positive !== false ? '#16a34a' : '#dc2626'}
                              />
                              <Text style={styles.miniFactorText} numberOfLines={1}>
                                {f.name}{f.detail ? ` (${f.detail})` : ''}
                              </Text>
                              <Text style={[styles.miniFactorValue, { color: f.positive !== false ? '#16a34a' : '#dc2626' }]}>
                                {f.positive !== false ? '+' : ''}{f.value}
                              </Text>
                            </View>
                          ))}
                        </View>
                      )}
                    </View>
                  );
                })}

                {/* Final Calculation */}
                {trace.final_calculation && (
                  <View style={styles.finalCalcBox}>
                    <Text style={styles.finalCalcLabel}>{t('total')}:</Text>
                    <Text style={styles.finalCalcFormula}>{trace.final_calculation.sum_of_contributions}</Text>
                    <Text style={styles.finalCalcResult}>= {trace.final_calculation.total}%</Text>
                  </View>
                )}
              </>
            )}

            {/* Simple Breakdown (if no detailed trace) */}
            {stepByStep.length === 0 && Object.keys(breakdown).length > 0 && (
              <>
                <Text style={styles.modalSectionTitle}>📊 {t('scoreBreakdown')}</Text>
                {Object.entries(breakdown).map(([key, value], i) => {
                  const compInfo = COMPONENT_KEYS[key] || { key: key, icon: 'help', color: '#6b7280' };
                  return (
                    <View key={i} style={styles.simpleBreakdownRow}>
                      <View style={styles.simpleBreakdownLeft}>
                        <Ionicons name={compInfo.icon} size={14} color={compInfo.color} />
                        <Text style={styles.simpleBreakdownLabel}>{t(compInfo.key) || key}</Text>
                      </View>
                      <View style={styles.simpleBreakdownRight}>
                        <View style={[styles.simpleProgressBg]}>
                          <View style={[styles.simpleProgressFill, {
                            width: `${Math.min(100, value * 3.33)}%`,
                            backgroundColor: compInfo.color
                          }]} />
                        </View>
                        <Text style={styles.simpleBreakdownValue}>{value}</Text>
                      </View>
                    </View>
                  );
                })}
              </>
            )}

            {/* Factors Section (for simple factor display) */}
            {data.factors && data.factors.length > 0 && stepByStep.length === 0 && (
              <>
                <View style={styles.modalDivider} />
                <Text style={styles.modalSectionTitle}>📈 {t('keyFactors')}</Text>
                {data.factors.map((factor, i) => (
                  <View key={i} style={styles.factorItem}>
                    <View style={styles.factorHeader}>
                      <Ionicons name={factor.positive ? 'add-circle' : 'remove-circle'} size={18} color={factor.positive ? '#16a34a' : '#dc2626'} />
                      <Text style={styles.factorName}>{factor.name}</Text>
                      <Text style={[styles.factorScore, { color: factor.positive ? '#16a34a' : '#dc2626' }]}>
                        {factor.positive ? '+' : ''}{factor.value}
                      </Text>
                    </View>
                    {factor.detail && <Text style={styles.factorDesc}>{factor.detail}</Text>}
                  </View>
                ))}
              </>
            )}

            {/* Area Scores (for yearly) */}
            {data.area_scores && Object.keys(data.area_scores).length > 0 && (
              <>
                <View style={styles.modalDivider} />
                <Text style={styles.modalSectionTitle}>🎯 {t('lifeAreasLabel')}</Text>
                <View style={styles.areaScoresGrid}>
                  {Object.entries(data.area_scores).map(([area, score], i) => {
                    const areaInfo = AREA_KEYS[area] || { key: area, icon: 'help', color: '#6b7280' };
                    return (
                      <View key={i} style={[styles.areaScoreCard, { borderColor: areaInfo.color + '40' }]}>
                        <Ionicons name={areaInfo.icon} size={16} color={areaInfo.color} />
                        <Text style={styles.areaScoreLabel}>{t(areaInfo.key) || area}</Text>
                        <Text style={[styles.areaScoreValue, { color: areaInfo.color }]}>{score}%</Text>
                      </View>
                    );
                  })}
                </View>
              </>
            )}

            {/* Positives Section */}
            {data.positives && data.positives.length > 0 && (
              <>
                <View style={styles.modalDivider} />
                <Text style={styles.modalSectionTitle}>✨ {t('goodOpportunities')}</Text>
                {data.positives.map((positive, i) => (
                  <View key={i} style={styles.positiveItem}>
                    <View style={styles.positiveIconBg}>
                      <Ionicons name={positive.icon || 'checkmark-circle'} size={20} color="#16a34a" />
                    </View>
                    <View style={styles.positiveContent}>
                      <Text style={styles.positiveTitle}>{positive.title}</Text>
                      <Text style={styles.positiveDesc}>{positive.description}</Text>
                    </View>
                  </View>
                ))}
              </>
            )}

            {/* Remedies Section */}
            {data.remedies && data.remedies.length > 0 && (
              <>
                <View style={styles.modalDivider} />
                <Text style={styles.modalSectionTitle}>🙏 {t('remediesLabel')}</Text>
                <View style={styles.remediesBox}>
                  {data.remedies.map((remedy, i) => (
                    <View key={i} style={styles.remedyItem}>
                      <Ionicons name="chevron-forward" size={14} color="#f97316" />
                      <Text style={styles.remedyText}>{remedy}</Text>
                    </View>
                  ))}
                </View>
              </>
            )}

            {/* Suggestion Section */}
            {data.suggestion && (
              <View style={styles.suggestionBox}>
                <Ionicons name="bulb" size={18} color="#f97316" />
                <Text style={styles.suggestionText}>{data.suggestion}</Text>
              </View>
            )}

            <TouchableOpacity style={styles.modalButton} onPress={onClose}>
              <Text style={styles.modalButtonText}>{t('ok')}</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </View>
    </Modal>
  );
};

// Timeline Year Detail Modal (Enhanced)
const TimelineYearModal = ({ visible, onClose, data, language }) => {
  if (!data) return null;

  const scores = data.scores || {};
  const trace = data.calculation_trace || {};
  const factors = data.factors || [];
  const events = data.events || [];
  const insight = data.insight || {};

  const isPeak = data.period_type === 'high';
  const isLow = data.period_type === 'low';
  const scoreColor = isPeak ? '#22c55e' : isLow ? '#ef4444' : '#3b82f6';

  const lifeAreas = [
    { key: 'career', label: t('career'), color: '#3b82f6', icon: 'briefcase' },
    { key: 'relationships', label: t('relationships'), color: '#ec4899', icon: 'heart' },
    { key: 'finances', label: t('finances'), color: '#22c55e', icon: 'cash' },
    { key: 'health', label: t('health'), color: '#f97316', icon: 'fitness' },
  ];

  return (
    <Modal transparent visible={visible} animationType="slide">
      <View style={styles.modalOverlay}>
        <ScrollView style={styles.modalScrollView}>
          <View style={styles.modalContent}>
            {/* Header */}
            <View style={styles.modalHeader}>
              <View style={[styles.modalIconBg, { backgroundColor: scoreColor + '20' }]}>
                <Text style={{ fontSize: 24, fontWeight: 'bold', color: scoreColor }}>{data.year}</Text>
              </View>
              <View style={{ flex: 1 }}>
                <Text style={styles.modalTitle}>{data.year} - {t('age')} {data.age}</Text>
                <Text style={{ fontSize: 12, color: '#8b5cf6', marginTop: 2 }}>
                  {data.dasha_tamil || data.dasha} {t('dasha')}
                </Text>
              </View>
              <TouchableOpacity style={styles.modalCloseBtn} onPress={onClose}>
                <Ionicons name="close" size={24} color="#6b7280" />
              </TouchableOpacity>
            </View>

            {/* Overall Score */}
            <View style={styles.modalScoreSection}>
              <Text style={[styles.modalScoreValue, { color: scoreColor }]}>{Math.round(data.overall_score)}</Text>
              <Text style={styles.modalScoreMax}>/100</Text>
            </View>

            <View style={[styles.qualityBadge, { backgroundColor: scoreColor + '20' }]}>
              <Text style={[styles.qualityText, { color: scoreColor }]}>
                {isPeak ? `⭐ ${t('peakYear')}` :
                 isLow ? `⚠️ ${t('challenging')}` :
                 `📊 ${t('normalYear')}`}
              </Text>
            </View>

            <View style={styles.modalDivider} />

            {/* Life Area Breakdown */}
            <Text style={styles.modalSectionTitle}>📊 {t('lifeAreasBreakdown')}</Text>
            <View style={styles.tlmAreaContainer}>
              {lifeAreas.map((area) => {
                const score = scores[area.key] || 0;
                return (
                  <View key={area.key} style={styles.tlmAreaRow}>
                    <View style={styles.tlmAreaInfo}>
                      <Ionicons name={area.icon} size={16} color={area.color} />
                      <Text style={styles.tlmAreaLabel}>{area.label}</Text>
                    </View>
                    <View style={styles.tlmAreaBarBg}>
                      <View style={[styles.tlmAreaBarFill, { width: `${score}%`, backgroundColor: area.color }]} />
                    </View>
                    <Text style={[styles.tlmAreaScore, { color: area.color }]}>{Math.round(score)}%</Text>
                  </View>
                );
              })}
            </View>

            {/* Calculation Trace */}
            {trace.formula && (
              <>
                <View style={styles.modalDivider} />
                <Text style={styles.modalSectionTitle}>🔮 {t('calculation')}</Text>
                <View style={styles.tlmTraceBox}>
                  <Text style={styles.tlmTraceVersion}>v{trace.engine_version || '2.3'}</Text>
                  <Text style={styles.tlmTraceFormula}>{trace.formula}</Text>
                  {trace.meta_multiplier && trace.meta_multiplier !== 1.0 && (
                    <View style={styles.tlmTraceMeta}>
                      <Ionicons name="flash" size={12} color="#f97316" />
                      <Text style={styles.tlmTraceMetaText}>
                        Meta: ×{trace.meta_multiplier?.toFixed(3) || '1.000'}
                      </Text>
                    </View>
                  )}
                </View>
              </>
            )}

            {/* Contributing Factors */}
            {factors.length > 0 && (
              <>
                <View style={styles.modalDivider} />
                <Text style={styles.modalSectionTitle}>⚡ {t('keyFactors')}</Text>
                {factors.slice(0, 5).map((factor, i) => (
                  <View key={i} style={styles.factorItem}>
                    <Ionicons
                      name={factor.positive !== false ? 'add-circle' : 'remove-circle'}
                      size={18}
                      color={factor.positive !== false ? '#16a34a' : '#dc2626'}
                    />
                    <View style={styles.factorContent}>
                      <Text style={styles.factorTitle}>{factor.name}</Text>
                      {factor.detail && <Text style={styles.factorDesc}>{factor.detail}</Text>}
                    </View>
                    <Text style={[styles.factorValue, { color: factor.positive !== false ? '#16a34a' : '#dc2626' }]}>
                      {factor.positive !== false ? '+' : ''}{factor.value}
                    </Text>
                  </View>
                ))}
              </>
            )}

            {/* Events */}
            {events.length > 0 && (
              <>
                <View style={styles.modalDivider} />
                <Text style={styles.modalSectionTitle}>🎯 {t('events')}</Text>
                <View style={styles.tlmEventsGrid}>
                  {events.map((event, i) => (
                    <View key={i} style={[styles.tlmEventChip, { backgroundColor: event.color + '20', borderColor: event.color }]}>
                      <Ionicons name={event.icon} size={14} color={event.color} />
                      <Text style={[styles.tlmEventText, { color: event.color }]} numberOfLines={1}>
                        {event.label_tamil || event.label}
                      </Text>
                    </View>
                  ))}
                </View>
              </>
            )}

            {/* Insight */}
            {insight.text && (
              <View style={[styles.suggestionBox, {
                backgroundColor: insight.mood === 'positive' ? '#dcfce720' :
                                 insight.mood === 'challenging' ? '#fee2e220' : '#fef3c720'
              }]}>
                <Ionicons name="bulb" size={18} color={
                  insight.mood === 'positive' ? '#16a34a' :
                  insight.mood === 'challenging' ? '#dc2626' : '#f97316'
                } />
                <Text style={styles.suggestionText}>{insight.text}</Text>
              </View>
            )}

            <TouchableOpacity style={styles.modalButton} onPress={onClose}>
              <Text style={styles.modalButtonText}>{t('ok')}</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </View>
    </Modal>
  );
};

export default function DashboardScreen({ navigation }) {
  const { userProfile } = useAuth();
  const { t, formatDate, language } = useLanguage();
  const [currentTime, setCurrentTime] = useState(new Date());
  const [panchangam, setPanchangam] = useState(null);
  const [jathagam, setJathagam] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [showScoreModal, setShowScoreModal] = useState(false);
  const [selectedScoreData, setSelectedScoreData] = useState(null);
  const [projectionView, setProjectionView] = useState('month'); // 'month' or 'year'
  const [lifeTimeline, setLifeTimeline] = useState(null);
  const [selectedTimelineYear, setSelectedTimelineYear] = useState(null);
  const [showTimelineModal, setShowTimelineModal] = useState(false);
  const [planetAura, setPlanetAura] = useState(null);
  const [selectedPlanet, setSelectedPlanet] = useState(null);
  const [transitsMap, setTransitsMap] = useState(null);
  const [dynamicLifeAreas, setDynamicLifeAreas] = useState(null);
  const [dynamicProjections, setDynamicProjections] = useState(null);
  const insets = useSafeAreaInsets();
  const bottomPadding = Platform.OS === 'android' ? Math.max(insets.bottom, 80) : insets.bottom + 80;

  // Header animation
  const headerFadeAnim = useRef(new Animated.Value(0)).current;
  const headerSlideAnim = useRef(new Animated.Value(-20)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(headerFadeAnim, { toValue: 1, duration: 600, useNativeDriver: true }),
      Animated.timing(headerSlideAnim, { toValue: 0, duration: 600, useNativeDriver: true, easing: Easing.out(Easing.ease) }),
    ]).start();
  }, []);

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    fetchData();
  }, [userProfile]);

  const fetchData = async () => {
    try {
      const panchangamData = await mobileAPI.getPanchangam();
      setPanchangam(panchangamData);

      // Check for birth details - also check alternate property names
      const birthDate = userProfile?.birthDate || userProfile?.birth_date;
      const birthTime = userProfile?.birthTime || userProfile?.birth_time || '12:00';
      const birthPlace = userProfile?.birthPlace || userProfile?.birth_place || 'Chennai';
      const userName = userProfile?.name || 'User';

      console.log('User profile for API calls:', { birthDate, birthTime, birthPlace, userName });

      if (birthDate) {
        const birthDetails = {
          name: userName,
          birthDate: birthDate,
          birthTime: birthTime,
          birthPlace: birthPlace,
        };

        console.log('Fetching personalized data with:', birthDetails);

        // Fetch jathagam first (needed for other calls)
        const jathagamData = await mobileAPI.getJathagam(birthDetails);
        console.log('Jathagam data received:', jathagamData ? 'Yes' : 'No');
        setJathagam(jathagamData);

        // Fetch all data in parallel for better performance
        const [timelineData, auraData, transitsData, lifeAreasData, projectionsData] = await Promise.all([
          // Life Timeline
          mobileAPI.getLifeTimeline(birthDetails, 10).catch(err => {
            console.error('Life Timeline API error:', err);
            return null;
          }),
          // Planet Aura
          mobileAPI.getPlanetAura(birthDetails).catch(err => {
            console.error('Planet Aura API error:', err);
            return null;
          }),
          // Transits Map
          mobileAPI.getTransitsMap(
            birthPlace,
            jathagamData?.rasi || jathagamData?.moon_sign?.rasi || ''
          ).catch(err => {
            console.error('Transits Map API error:', err);
            return null;
          }),
          // Life Areas
          mobileAPI.getLifeAreas(birthDetails).catch(err => {
            console.error('Life Areas API error:', err);
            return null;
          }),
          // Future Projections
          mobileAPI.getFutureProjections(birthDetails).catch(err => {
            console.error('Future Projections API error:', err);
            return null;
          }),
        ]);

        console.log('API responses:', {
          timeline: timelineData ? 'Yes' : 'No',
          aura: auraData ? 'Yes' : 'No',
          transits: transitsData ? 'Yes' : 'No',
          lifeAreas: lifeAreasData ? 'Yes' : 'No',
          projections: projectionsData ? 'Yes' : 'No',
          projectionsMonthly: projectionsData?.projections?.monthly?.length || 0,
          projectionsYearly: projectionsData?.projections?.yearly?.length || 0,
        });

        // Set all state
        setLifeTimeline(timelineData);
        setPlanetAura(auraData);
        setTransitsMap(transitsData);
        setDynamicLifeAreas(lifeAreasData);
        setDynamicProjections(projectionsData);

        // Schedule transit notifications
        if (transitsData) {
          await notificationService.initialize();
          await notificationService.updateTransitNotifications(transitsData);
        }
      } else {
        console.warn('No birth date available in userProfile:', userProfile);
      }
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    fetchData();
  };

  const getCurrentPeriod = () => {
    const hour = currentTime.getHours();
    if (hour >= 15 && hour < 17) return { label: t('rahuKalam'), color: '#dc2626', bg: '#fef2f2' };
    if (hour >= 9 && hour < 11) return { label: t('goodTime'), color: '#16a34a', bg: '#f0fdf4' };
    return { label: t('normalTime'), color: '#ea580c', bg: '#fff7ed' };
  };

  const period = getCurrentPeriod();

  // Area config for colors and icons
  const areaConfig = {
    love: { icon: 'heart', color: '#ec4899', name: t('love') },
    career: { icon: 'briefcase', color: '#3b82f6', name: t('career') },
    education: { icon: 'school', color: '#8b5cf6', name: t('education') },
    family: { icon: 'home', color: '#10b981', name: t('family') },
    health: { icon: 'fitness', color: '#f59e0b', name: t('health') },
  };

  // Get life areas - use dynamic data if available, otherwise fallback
  const getLifeAreas = () => {
    // If dynamic data is available from API, use it
    if (dynamicLifeAreas?.life_areas) {
      const apiAreas = dynamicLifeAreas.life_areas;
      return Object.keys(areaConfig).slice(0, 4).map(areaKey => {
        const area = apiAreas[areaKey];
        const config = areaConfig[areaKey];
        return {
          name: config.name,
          icon: config.icon,
          score: area?.score || 50,
          color: config.color,
          factors: area?.factors || [],
          suggestion: area?.suggestion || '',
          breakdown: area?.breakdown || {},
          calculation_trace: area?.calculation_trace || {},
          quality: area?.score >= 70 ? t('good') : area?.score >= 50 ? t('average') : t('caution')
        };
      });
    }

    // Fallback static data (should rarely be used now)
    return [
      {
        name: t('love'),
        icon: 'heart',
        score: 65,
        color: '#ec4899',
        factors: [],
        suggestion: ''
      },
      {
        name: t('career'),
        icon: 'briefcase',
        score: 60,
        color: '#3b82f6',
        factors: [],
        suggestion: ''
      },
      {
        name: t('education'),
        icon: 'school',
        score: 68,
        color: '#8b5cf6',
        factors: [],
        suggestion: ''
      },
      {
        name: t('family'),
        icon: 'home',
        score: 62,
        color: '#10b981',
        factors: [],
        suggestion: ''
      },
    ];
  };

  const lifeAreas = getLifeAreas();

  // Calculate overall score dynamically from life areas
  const overallScore = lifeAreas.length > 0
    ? Math.round(lifeAreas.reduce((sum, area) => sum + area.score, 0) / lifeAreas.length)
    : 72;

  // Month-wise projections (next 12 months) - uses dynamic API data
  const getMonthProjections = () => {
    // If dynamic projections are available from API, use them
    if (dynamicProjections?.projections?.monthly) {
      console.log('Using DYNAMIC monthly projections from API');
      return dynamicProjections.projections.monthly.map((m, i) => ({
        name: m.name,
        monthIndex: m.month - 1,
        year: m.year,
        score: m.score,
        quality: m.quality,
        factors: m.factors || [],
        breakdown: m.breakdown || {},
        calculation_trace: m.calculation_trace || {},
        dasha_lord: m.dasha_lord,
        bhukti_lord: m.bhukti_lord,
        suggestion: m.recommendation || '',
        isPersonalized: true
      }));
    }

    console.log('Using FALLBACK monthly projections (API data not available)');
    // Fallback to static data if API not available
    const months = [];
    const currentMonth = currentTime.getMonth();
    const monthKeys = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'];
    const baseScores = [72, 68, 75, 82, 70, 78, 65, 80, 73, 85, 77, 71];

    for (let i = 0; i < 12; i++) {
      const monthIndex = (currentMonth + i) % 12;
      const year = currentTime.getFullYear() + Math.floor((currentMonth + i) / 12);
      months.push({
        name: t(monthKeys[monthIndex]),
        monthIndex,
        year,
        score: baseScores[monthIndex],
        factors: [],
        suggestion: ''
      });
    }
    return months;
  };

  // 3-year projections - uses dynamic API data
  const getYearProjections = () => {
    const currentYear = currentTime.getFullYear();
    const icons = ['time-outline', 'trending-up', 'star'];
    const colors = ['#f59e0b', '#10b981', '#8b5cf6'];

    // If dynamic projections are available from API, use them
    if (dynamicProjections?.projections?.yearly) {
      console.log('Using DYNAMIC yearly projections from API');
      return dynamicProjections.projections.yearly.map((y, i) => ({
        year: y.year,
        score: y.score,
        label: y.label,
        quality: y.quality,
        icon: icons[i] || 'star',
        color: colors[i] || '#8b5cf6',
        factors: y.factors || [],
        breakdown: y.breakdown || {},
        calculation_trace: y.calculation_trace || {},
        area_scores: y.area_scores || {},
        dasha_lord: y.dasha_lord,
        bhukti_lord: y.bhukti_lord,
        positives: [],
        remedies: [],
        suggestion: y.recommendation || '',
        isPersonalized: true
      }));
    }

    console.log('Using FALLBACK yearly projections (API data not available)');
    // Fallback to static data
    return [
      {
        year: currentYear,
        score: 68,
        label: t('currentYear'),
        icon: 'time-outline',
        color: '#f59e0b',
        factors: [],
        positives: [],
        remedies: [],
        suggestion: ''
      },
      {
        year: currentYear + 1,
        score: 78,
        label: t('nextYear'),
        icon: 'trending-up',
        color: '#10b981',
        factors: [],
        positives: [],
        remedies: [],
        suggestion: ''
      },
      {
        year: currentYear + 2,
        score: 85,
        label: t('thirdYear'),
        icon: 'star',
        color: '#8b5cf6',
        factors: [],
        positives: [],
        remedies: [],
        suggestion: ''
      },
    ];
  };

  const monthProjections = getMonthProjections();
  const yearProjections = getYearProjections();

  const quickActions = [
    { icon: 'sparkles', label: t('remedy'), screen: 'Remedy', color: '#8b5cf6' },
    { icon: 'chatbubbles', label: t('aiQuestion'), screen: 'Chat', color: '#ea580c' },
    { icon: 'heart', label: t('matching'), screen: 'Matching', color: '#ef4444' },
    { icon: 'calendar', label: t('muhurtham'), screen: 'Muhurtham', color: '#16a34a' },
  ];

  const handleScorePress = (data) => {
    setSelectedScoreData({
      ...data,
      title: data.name || t('todayScore'),
    });
    setShowScoreModal(true);
  };

  const handleOverallScorePress = () => {
    setSelectedScoreData({
      title: t('todayScore'),
      score: overallScore,
      icon: 'star',
      color: '#f97316',
      factors: [],
      suggestion: ''
    });
    setShowScoreModal(true);
  };

  const handleMonthPress = (month) => {
    setSelectedScoreData({
      title: `${month.name} ${month.year}`,
      score: month.score,
      quality: month.quality,
      icon: 'calendar',
      color: '#3b82f6',
      factors: month.factors,
      breakdown: month.breakdown,
      calculation_trace: month.calculation_trace,
      dasha_lord: month.dasha_lord,
      bhukti_lord: month.bhukti_lord,
      suggestion: month.suggestion
    });
    setShowScoreModal(true);
  };

  const handleYearPress = (year) => {
    setSelectedScoreData({
      title: `${year.year}`,
      score: year.score,
      quality: year.quality,
      icon: year.icon || 'calendar-outline',
      color: year.color || '#8b5cf6',
      factors: year.factors,
      breakdown: year.breakdown,
      calculation_trace: year.calculation_trace,
      area_scores: year.area_scores,
      dasha_lord: year.dasha_lord,
      bhukti_lord: year.bhukti_lord,
      positives: year.positives,
      remedies: year.remedies,
      suggestion: year.suggestion
    });
    setShowScoreModal(true);
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#f97316" />
        <Text style={styles.loadingText}>{t('loading')}</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <LinearGradient colors={['#fff7ed', '#ffffff', '#fff7ed']} style={styles.gradient}>
        <ScrollView
          contentContainerStyle={[styles.scrollContent, { paddingBottom: bottomPadding }]}
          refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={['#f97316']} />}
        >
          <LinearGradient
            colors={['#f97316', '#ef4444', '#f97316']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.headerBar}
          />

          {/* Header */}
          <Animated.View
            style={[
              styles.header,
              { opacity: headerFadeAnim, transform: [{ translateY: headerSlideAnim }] },
            ]}
          >
            <View>
              <View style={styles.logoRow}>
                <View style={styles.logoIcon}>
                  <Svg width={28} height={28} viewBox="0 0 100 100">
                    <Path
                      d="M50 5 L55 40 L90 30 L60 50 L90 70 L55 60 L50 95 L45 60 L10 70 L40 50 L10 30 L45 40 Z"
                      fill="#f97316"
                    />
                    <Circle cx="50" cy="50" r="10" fill="#fff7ed" />
                  </Svg>
                </View>
                <Text style={styles.appTitle}>{t('appName')}</Text>
              </View>
              {userProfile && (
                <View style={styles.userInfo}>
                  <Text style={styles.greeting}>{t('greeting')}, {userProfile.name}</Text>
                  {userProfile.rasi && (
                    <Text style={styles.rasiInfo}>{userProfile.rasi} • {userProfile.nakshatra}</Text>
                  )}
                </View>
              )}
            </View>
            <View style={styles.timeContainer}>
              <Text style={styles.currentTime}>
                {currentTime.toLocaleTimeString('ta-IN', { hour: '2-digit', minute: '2-digit' })}
              </Text>
              <View style={[styles.periodBadge, { backgroundColor: period.bg }]}>
                <Text style={[styles.periodText, { color: period.color }]}>{period.label}</Text>
              </View>
            </View>
          </Animated.View>

          {/* Date Display */}
          <AnimatedCard delay={50} style={styles.dateCard}>
            <Text style={styles.dateText}>{formatDate(currentTime)}</Text>
          </AnimatedCard>

          {/* Story Preview Row */}
          <AnimatedCard delay={75}>
            <TouchableOpacity
              style={styles.storyPreviewRow}
              onPress={() => navigation.navigate('AstroFeed')}
              activeOpacity={0.8}
            >
              <View style={styles.storyCirclesContainer}>
                <View style={[styles.storyCircle, styles.storyCircleActive]}>
                  <LinearGradient
                    colors={['#f97316', '#ef4444', '#ec4899']}
                    style={styles.storyGradientBorder}
                  >
                    <View style={styles.storyInner}>
                      <Ionicons name="sunny" size={20} color="#f59e0b" />
                    </View>
                  </LinearGradient>
                  <Text style={styles.storyLabel}>{t('planet')}</Text>
                </View>
                <View style={[styles.storyCircle, styles.storyCircleActive]}>
                  <LinearGradient
                    colors={['#8b5cf6', '#6366f1', '#3b82f6']}
                    style={styles.storyGradientBorder}
                  >
                    <View style={styles.storyInner}>
                      <Ionicons name="moon" size={20} color="#a78bfa" />
                    </View>
                  </LinearGradient>
                  <Text style={styles.storyLabel}>{t('moon')}</Text>
                </View>
                <View style={[styles.storyCircle, styles.storyCircleActive]}>
                  <LinearGradient
                    colors={['#22c55e', '#16a34a', '#15803d']}
                    style={styles.storyGradientBorder}
                  >
                    <View style={styles.storyInner}>
                      <Ionicons name="sparkles" size={20} color="#22c55e" />
                    </View>
                  </LinearGradient>
                  <Text style={styles.storyLabel}>{t('insight')}</Text>
                </View>
                <View style={[styles.storyCircle, styles.storyCircleActive]}>
                  <LinearGradient
                    colors={['#f59e0b', '#d97706', '#b45309']}
                    style={styles.storyGradientBorder}
                  >
                    <View style={styles.storyInner}>
                      <Ionicons name="star" size={20} color="#f59e0b" />
                    </View>
                  </LinearGradient>
                  <Text style={styles.storyLabel}>{t('star')}</Text>
                </View>
                <View style={styles.storyCircle}>
                  <View style={styles.storyMoreCircle}>
                    <Ionicons name="add" size={24} color="#f97316" />
                  </View>
                  <Text style={styles.storyLabel}>{t('more')}</Text>
                </View>
              </View>
            </TouchableOpacity>
          </AnimatedCard>

          {/* Tamil Calendar */}
          <AnimatedCard delay={100} style={styles.card}>
            <View style={styles.cardHeader}>
              <Ionicons name="calendar" size={16} color="#ea580c" />
              <Text style={styles.cardTitle}>{t('todayPanchangam')}</Text>
            </View>
            <View style={styles.panchangamGrid}>
              <View style={styles.panchangamItem}>
                <Text style={styles.panchangamLabel}>{t('month')}</Text>
                <Text style={styles.panchangamValue}>{panchangam?.tamil_month || '-'}</Text>
              </View>
              <View style={styles.panchangamItem}>
                <Text style={styles.panchangamLabel}>{t('tithi')}</Text>
                <Text style={styles.panchangamValue}>{panchangam?.tithi?.name || '-'}</Text>
              </View>
              <View style={styles.panchangamItem}>
                <Text style={styles.panchangamLabel}>{t('nakshatra')}</Text>
                <Text style={styles.panchangamValue}>{panchangam?.nakshatra?.tamil || '-'}</Text>
              </View>
              <View style={styles.panchangamItem}>
                <Text style={styles.panchangamLabel}>{t('yoga')}</Text>
                <Text style={styles.panchangamValue}>{panchangam?.yoga?.name || '-'}</Text>
              </View>
            </View>
          </AnimatedCard>

          {/* Today's Score */}
          <AnimatedCard delay={200} style={styles.card}>
            <View style={styles.scoreRow}>
              <View>
                <Text style={styles.scoreLabel}>{t('todayScore')}</Text>
                <View style={styles.scoreValue}>
                  <Text style={styles.scoreNumber}>{overallScore}</Text>
                  <Text style={styles.scoreMax}>/100</Text>
                  <View style={[styles.scoreBadge, { backgroundColor: overallScore >= 70 ? '#dcfce7' : '#fef3c7' }]}>
                    <Ionicons name="trending-up" size={14} color={overallScore >= 70 ? '#16a34a' : '#d97706'} />
                    <Text style={[styles.scoreBadgeText, { color: overallScore >= 70 ? '#16a34a' : '#d97706' }]}>
                      {overallScore >= 70 ? t('good') : t('average')}
                    </Text>
                  </View>
                </View>
              </View>
              <AnimatedScoreCircle score={overallScore} onPress={handleOverallScorePress} tapText={t('tap')} />
            </View>

            <LinearGradient colors={['#fff7ed', '#fef3c7']} style={styles.insightBox}>
              <PulsingSparkle />
              <Text style={styles.insightText}>
                {jathagam?.dasha?.mahadasha
                  ? `${t(planetTranslationKeys[jathagam.dasha.mahadasha]) || jathagam.dasha.mahadasha} ${t('dashaRunning')}`
                  : t('defaultInsight')
                }
              </Text>
            </LinearGradient>
          </AnimatedCard>

          {/* Life Areas */}
          <AnimatedCard delay={300} style={styles.card}>
            <View style={styles.cardHeader}>
              <Ionicons name="star" size={16} color="#ea580c" />
              <Text style={styles.cardTitle}>{t('lifeAreas')}</Text>
              {dynamicLifeAreas?.life_areas ? (
                <View style={{ flexDirection: 'row', alignItems: 'center', marginLeft: 'auto', backgroundColor: '#dcfce7', paddingHorizontal: 8, paddingVertical: 2, borderRadius: 10, marginRight: 8 }}>
                  <Ionicons name="checkmark-circle" size={12} color="#16a34a" />
                  <Text style={{ fontSize: 10, color: '#16a34a', marginLeft: 4 }}>{t('personal')}</Text>
                </View>
              ) : (
                <View style={{ flexDirection: 'row', alignItems: 'center', marginLeft: 'auto', backgroundColor: '#fef3c7', paddingHorizontal: 8, paddingVertical: 2, borderRadius: 10, marginRight: 8 }}>
                  <Ionicons name="information-circle" size={12} color="#d97706" />
                  <Text style={{ fontSize: 10, color: '#d97706', marginLeft: 4 }}>{t('generic')}</Text>
                </View>
              )}
              <Text style={styles.tapHintSmall}>{t('tapForDetails')}</Text>
            </View>
            {/* Row 1 */}
            <View style={styles.lifeAreasRow}>
              {lifeAreas.slice(0, 2).map((area, i) => (
                <TouchableOpacity
                  key={i}
                  style={styles.lifeAreaCard}
                  onPress={() => handleScorePress(area)}
                  activeOpacity={0.8}
                >
                  <View style={styles.lifeAreaHeader}>
                    <View style={[styles.lifeAreaIconBg, { backgroundColor: area.color + '20' }]}>
                      <Ionicons name={area.icon} size={18} color={area.color} />
                    </View>
                    <View style={[styles.lifeAreaBadge, { backgroundColor: area.score >= 75 ? '#dcfce7' : area.score >= 50 ? '#fef3c7' : '#fef2f2' }]}>
                      <Text style={[styles.lifeAreaBadgeText, { color: area.score >= 75 ? '#16a34a' : area.score >= 50 ? '#d97706' : '#dc2626' }]}>
                        {area.score >= 75 ? t('good') : area.score >= 50 ? t('average') : t('caution')}
                      </Text>
                    </View>
                  </View>
                  <Text style={styles.lifeAreaName} numberOfLines={1}>{area.name}</Text>
                  <View style={styles.lifeAreaScoreRow}>
                    <Text style={[styles.lifeAreaScore, { color: area.color }]}>{area.score}</Text>
                    <Text style={styles.lifeAreaMax}>/100</Text>
                    <Ionicons name="chevron-forward" size={14} color="#9ca3af" style={{ marginLeft: 'auto' }} />
                  </View>
                  <View style={styles.lifeAreaProgressBar}>
                    <View style={[styles.lifeAreaProgressFill, { width: `${area.score}%`, backgroundColor: area.color }]} />
                  </View>
                </TouchableOpacity>
              ))}
            </View>
            {/* Row 2 */}
            <View style={styles.lifeAreasRow}>
              {lifeAreas.slice(2, 4).map((area, i) => (
                <TouchableOpacity
                  key={i + 2}
                  style={styles.lifeAreaCard}
                  onPress={() => handleScorePress(area)}
                  activeOpacity={0.8}
                >
                  <View style={styles.lifeAreaHeader}>
                    <View style={[styles.lifeAreaIconBg, { backgroundColor: area.color + '20' }]}>
                      <Ionicons name={area.icon} size={18} color={area.color} />
                    </View>
                    <View style={[styles.lifeAreaBadge, { backgroundColor: area.score >= 75 ? '#dcfce7' : area.score >= 50 ? '#fef3c7' : '#fef2f2' }]}>
                      <Text style={[styles.lifeAreaBadgeText, { color: area.score >= 75 ? '#16a34a' : area.score >= 50 ? '#d97706' : '#dc2626' }]}>
                        {area.score >= 75 ? t('good') : area.score >= 50 ? t('average') : t('caution')}
                      </Text>
                    </View>
                  </View>
                  <Text style={styles.lifeAreaName} numberOfLines={1}>{area.name}</Text>
                  <View style={styles.lifeAreaScoreRow}>
                    <Text style={[styles.lifeAreaScore, { color: area.color }]}>{area.score}</Text>
                    <Text style={styles.lifeAreaMax}>/100</Text>
                    <Ionicons name="chevron-forward" size={14} color="#9ca3af" style={{ marginLeft: 'auto' }} />
                  </View>
                  <View style={styles.lifeAreaProgressBar}>
                    <View style={[styles.lifeAreaProgressFill, { width: `${area.score}%`, backgroundColor: area.color }]} />
                  </View>
                </TouchableOpacity>
              ))}
            </View>
          </AnimatedCard>

          {/* Month & Year Projections */}
          <AnimatedCard delay={350} style={styles.card}>
            <View style={styles.cardHeader}>
              <Ionicons name="analytics" size={16} color="#ea580c" />
              <Text style={styles.cardTitle}>{t('futureProjection')}</Text>
              {dynamicProjections?.projections ? (
                <View style={{ flexDirection: 'row', alignItems: 'center', marginLeft: 'auto', backgroundColor: '#dcfce7', paddingHorizontal: 8, paddingVertical: 2, borderRadius: 10 }}>
                  <Ionicons name="checkmark-circle" size={12} color="#16a34a" />
                  <Text style={{ fontSize: 10, color: '#16a34a', marginLeft: 4 }}>{t('personal')}</Text>
                </View>
              ) : (
                <View style={{ flexDirection: 'row', alignItems: 'center', marginLeft: 'auto', backgroundColor: '#fef3c7', paddingHorizontal: 8, paddingVertical: 2, borderRadius: 10 }}>
                  <Ionicons name="information-circle" size={12} color="#d97706" />
                  <Text style={{ fontSize: 10, color: '#d97706', marginLeft: 4 }}>{t('generic')}</Text>
                </View>
              )}
            </View>

            {/* Toggle Buttons */}
            <View style={styles.projectionToggle}>
              <TouchableOpacity
                style={[styles.toggleBtn, projectionView === 'month' && styles.toggleBtnActive]}
                onPress={() => setProjectionView('month')}
              >
                <Text style={[styles.toggleText, projectionView === 'month' && styles.toggleTextActive]}>{t('monthly')}</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.toggleBtn, projectionView === 'year' && styles.toggleBtnActive]}
                onPress={() => setProjectionView('year')}
              >
                <Text style={[styles.toggleText, projectionView === 'year' && styles.toggleTextActive]}>{t('threeYears')}</Text>
              </TouchableOpacity>
            </View>

            {projectionView === 'month' ? (
              <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.monthsScroll}>
                {monthProjections.map((month, i) => (
                  <MonthProjectionCard key={i} month={month} index={i} onPress={handleMonthPress} />
                ))}
              </ScrollView>
            ) : (
              <View style={styles.yearsGrid}>
                {yearProjections.map((year, i) => (
                  <YearProjectionCard key={i} year={year} onPress={handleYearPress} />
                ))}
              </View>
            )}
          </AnimatedCard>

          {/* Past Years Analysis */}
          {lifeTimeline?.past_years?.length > 0 && (
            <AnimatedCard delay={375} style={styles.card}>
              <View style={styles.cardHeader}>
                <Ionicons name="time-outline" size={16} color="#6b7280" />
                <Text style={styles.cardTitle}>
                  {t('pastYears')}
                </Text>
              </View>
              <View style={styles.pastYearsGrid}>
                {lifeTimeline.past_years.map((yearData, index) => {
                  const scoreColor = yearData.overall_score >= 70 ? '#22c55e' : yearData.overall_score >= 50 ? '#f59e0b' : '#ef4444';
                  return (
                    <TouchableOpacity
                      key={yearData.year}
                      style={styles.pastYearCard}
                      onPress={() => {
                        setSelectedTimelineYear(yearData);
                        setShowTimelineModal(true);
                      }}
                    >
                      <View style={styles.pastYearHeader}>
                        <Text style={styles.pastYearLabel}>{yearData.year}</Text>
                        <View style={[styles.pastYearBadge, { backgroundColor: scoreColor + '20' }]}>
                          <Text style={[styles.pastYearScore, { color: scoreColor }]}>{Math.round(yearData.overall_score)}%</Text>
                        </View>
                      </View>
                      <Text style={styles.pastYearDasha}>
                        {yearData.dasha_tamil || yearData.dasha} {t('dasha')}
                      </Text>
                      <View style={styles.pastYearBar}>
                        <View style={[styles.pastYearBarFill, { width: `${yearData.overall_score}%`, backgroundColor: scoreColor }]} />
                      </View>
                    </TouchableOpacity>
                  );
                })}
              </View>
            </AnimatedCard>
          )}

          {/* Quick Actions */}
          <AnimatedCard delay={400} style={styles.card}>
            <Text style={styles.cardTitle}>{t('quickActions')}</Text>
            <View style={styles.quickActionsGrid}>
              {quickActions.map((action, i) => (
                <AnimatedQuickAction
                  key={i}
                  action={action}
                  index={i}
                  onPress={() => {
                    // Remedy screen is in root navigator, others are in tab navigator
                    if (action.screen === 'Remedy') {
                      navigation.getParent()?.navigate('Remedy');
                    } else {
                      navigation.navigate(action.screen);
                    }
                  }}
                />
              ))}
            </View>
          </AnimatedCard>

          {/* Current Dasha */}
          {jathagam?.dasha?.mahadasha && (
            <AnimatedCard delay={500}>
              <LinearGradient colors={['#faf5ff', '#eef2ff']} style={[styles.card, styles.dashaCard, { marginHorizontal: 0 }]}>
                <View style={styles.cardHeader}>
                  <Ionicons name="sparkles" size={16} color="#7c3aed" />
                  <Text style={[styles.cardTitle, { color: '#6b21a8' }]}>{t('currentDasha')}</Text>
                </View>
                <View style={styles.dashaGrid}>
                  <View style={styles.dashaItem}>
                    <Text style={styles.dashaLabel}>{t('mahaDasha')}</Text>
                    <Text style={styles.dashaValue}>
                      {t(planetTranslationKeys[jathagam.dasha.mahadasha]) || jathagam.dasha.mahadasha}
                    </Text>
                  </View>
                  {jathagam.dasha.antardasha && (
                    <View style={styles.dashaItem}>
                      <Text style={styles.dashaLabel}>{t('antarDasha')}</Text>
                      <Text style={styles.dashaValue}>
                        {t(planetTranslationKeys[jathagam.dasha.antardasha]) || jathagam.dasha.antardasha}
                      </Text>
                    </View>
                  )}
                </View>
              </LinearGradient>
            </AnimatedCard>
          )}

          {/* Life Timeline - Kundli Prediction (Enhanced v2) */}
          {lifeTimeline && (
            <AnimatedCard delay={550}>
              <LinearGradient colors={['#0f172a', '#1e293b']} style={[styles.card, styles.timelineCard, { marginHorizontal: 0 }]}>
                <View style={styles.cardHeader}>
                  <Ionicons name="time" size={16} color="#f97316" />
                  <Text style={[styles.cardTitle, { color: '#fff' }]}>
                    {t('lifeTimeline')}
                  </Text>
                  <TouchableOpacity onPress={() => setShowTimelineModal(true)}>
                    <Ionicons name="expand" size={18} color="#9ca3af" />
                  </TouchableOpacity>
                </View>

                {/* Life Trend Summary */}
                {lifeTimeline.life_trend && (
                  <View style={styles.trendSummary}>
                    <View style={[
                      styles.trendBadge,
                      {
                        backgroundColor: lifeTimeline.life_trend.direction === 'ascending' ? '#22c55e20' :
                                         lifeTimeline.life_trend.direction === 'descending' ? '#ef444420' : '#3b82f620'
                      }
                    ]}>
                      <Ionicons
                        name={lifeTimeline.life_trend.direction === 'ascending' ? 'trending-up' :
                              lifeTimeline.life_trend.direction === 'descending' ? 'trending-down' : 'remove'}
                        size={16}
                        color={lifeTimeline.life_trend.direction === 'ascending' ? '#22c55e' :
                               lifeTimeline.life_trend.direction === 'descending' ? '#ef4444' : '#3b82f6'}
                      />
                      <Text style={[
                        styles.trendText,
                        {
                          color: lifeTimeline.life_trend.direction === 'ascending' ? '#22c55e' :
                                 lifeTimeline.life_trend.direction === 'descending' ? '#ef4444' : '#3b82f6'
                        }
                      ]}>
                        {lifeTimeline.life_trend.direction_tamil}
                      </Text>
                    </View>
                    <Text style={styles.trendAvg}>
                      {t('avg')}: {lifeTimeline.life_trend.average_score}%
                    </Text>
                  </View>
                )}

                {/* Legend - Life Areas */}
                <View style={styles.timelineLegend}>
                  <View style={styles.timelineLegendRow}>
                    <View style={styles.timelineLegendItem}>
                      <View style={[styles.timelineLegendDot, { backgroundColor: '#3b82f6' }]} />
                      <Text style={styles.timelineLegendText}>{t('career')}</Text>
                    </View>
                    <View style={styles.timelineLegendItem}>
                      <View style={[styles.timelineLegendDot, { backgroundColor: '#ec4899' }]} />
                      <Text style={styles.timelineLegendText}>{t('relationships')}</Text>
                    </View>
                    <View style={styles.timelineLegendItem}>
                      <View style={[styles.timelineLegendDot, { backgroundColor: '#22c55e' }]} />
                      <Text style={styles.timelineLegendText}>{t('finances')}</Text>
                    </View>
                    <View style={styles.timelineLegendItem}>
                      <View style={[styles.timelineLegendDot, { backgroundColor: '#f97316' }]} />
                      <Text style={styles.timelineLegendText}>{t('health')}</Text>
                    </View>
                  </View>
                  <View style={styles.timelineLegendRow}>
                    <View style={styles.timelineLegendItem}>
                      <View style={[styles.timelineLegendDot, { backgroundColor: '#22c55e', borderWidth: 2, borderColor: '#fff' }]} />
                      <Text style={styles.timelineLegendText}>{t('high')} (≥72)</Text>
                    </View>
                    <View style={styles.timelineLegendItem}>
                      <View style={[styles.timelineLegendDot, { backgroundColor: '#ef4444', borderWidth: 2, borderColor: '#fff' }]} />
                      <Text style={styles.timelineLegendText}>{t('low')} (&lt;48)</Text>
                    </View>
                    <Text style={styles.timelineLegendVersion}>v2.3</Text>
                  </View>
                </View>

                {/* Interactive Timeline Slider with Stacked Bars */}
                <ScrollView
                  horizontal
                  showsHorizontalScrollIndicator={false}
                  contentContainerStyle={styles.timelineScrollContent}
                >
                  {lifeTimeline.yearly_timeline?.slice(0, 10).map((yearData, index) => {
                    const isCurrentYear = yearData.year === new Date().getFullYear();
                    const isPeak = yearData.period_type === 'high';
                    const isLow = yearData.period_type === 'low';
                    const scores = yearData.scores || {};

                    // Calculate segment heights (proportional to max 80px bar height)
                    const totalHeight = 80;
                    const careerH = (scores.career || 0) / 100 * totalHeight * 0.25;
                    const relationsH = (scores.relationships || 0) / 100 * totalHeight * 0.25;
                    const financeH = (scores.finances || 0) / 100 * totalHeight * 0.25;
                    const healthH = (scores.health || 0) / 100 * totalHeight * 0.25;

                    return (
                      <TouchableOpacity
                        key={yearData.year}
                        style={[
                          styles.timelineYear,
                          isCurrentYear && styles.timelineYearCurrent,
                          isPeak && styles.timelineYearPeak,
                          isLow && styles.timelineYearLow,
                        ]}
                        onPress={() => {
                          setSelectedTimelineYear(yearData);
                          setShowTimelineModal(true);
                        }}
                      >
                        {/* Stacked Score Bar */}
                        <View style={styles.timelineBarContainer}>
                          {/* Health (top) */}
                          <View style={[styles.timelineBarSegment, { height: healthH, backgroundColor: '#f97316' }]} />
                          {/* Finance */}
                          <View style={[styles.timelineBarSegment, { height: financeH, backgroundColor: '#22c55e' }]} />
                          {/* Relations */}
                          <View style={[styles.timelineBarSegment, { height: relationsH, backgroundColor: '#ec4899' }]} />
                          {/* Career (bottom) */}
                          <View style={[styles.timelineBarSegment, { height: careerH, backgroundColor: '#3b82f6', borderBottomLeftRadius: 14, borderBottomRightRadius: 14 }]} />
                        </View>

                        {/* Overall Score Badge */}
                        <View style={[styles.timelineScoreBadge, {
                          backgroundColor: isPeak ? '#22c55e' : isLow ? '#ef4444' : '#475569'
                        }]}>
                          <Text style={styles.timelineScoreText}>{Math.round(yearData.overall_score)}</Text>
                        </View>

                        {/* Year Label */}
                        <Text style={[styles.timelineYearLabel, isCurrentYear && styles.timelineYearLabelCurrent]}>
                          {yearData.year}
                        </Text>

                        {/* Age & Dasha */}
                        <Text style={styles.timelineAge}>
                          {yearData.age}{language === 'ta' ? 'வ' : language === 'kn' ? 'ವ' : 'y'}
                        </Text>
                        <Text style={styles.timelineDasha} numberOfLines={1}>
                          {yearData.dasha_tamil?.substring(0, 3) || yearData.dasha?.substring(0, 3)}
                        </Text>

                        {/* Event Indicators */}
                        {yearData.events?.length > 0 && (
                          <View style={styles.timelineEventDots}>
                            {yearData.events.slice(0, 3).map((event, i) => (
                              <View
                                key={i}
                                style={[styles.timelineEventDot, { backgroundColor: event.color }]}
                              />
                            ))}
                          </View>
                        )}
                      </TouchableOpacity>
                    );
                  })}
                </ScrollView>

                {/* Major Events Preview */}
                {lifeTimeline.major_events?.length > 0 && (
                  <View style={styles.majorEventsPreview}>
                    <Text style={styles.majorEventsTitle}>
                      {t('keyEvents')}
                    </Text>
                    <View style={styles.majorEventsList}>
                      {lifeTimeline.major_events.slice(0, 3).map((event, index) => (
                        <View key={index} style={styles.majorEventItem}>
                          <View style={[styles.majorEventIcon, { backgroundColor: event.color + '30' }]}>
                            <Ionicons name={event.icon} size={14} color={event.color} />
                          </View>
                          <Text style={styles.majorEventYear}>{event.year}</Text>
                          <Text style={styles.majorEventLabel} numberOfLines={1}>
                            {event.label_tamil}
                          </Text>
                        </View>
                      ))}
                    </View>
                  </View>
                )}

                {/* Peak/Low Years */}
                <View style={styles.peakLowContainer}>
                  {lifeTimeline.peak_periods?.[0] && (
                    <View style={[styles.peakLowItem, { backgroundColor: '#22c55e15' }]}>
                      <Ionicons name="arrow-up-circle" size={16} color="#22c55e" />
                      <Text style={[styles.peakLowText, { color: '#22c55e' }]}>
                        {t('best')}: {lifeTimeline.peak_periods[0].year}
                      </Text>
                    </View>
                  )}
                  {lifeTimeline.low_periods?.[0] && (
                    <View style={[styles.peakLowItem, { backgroundColor: '#ef444415' }]}>
                      <Ionicons name="alert-circle" size={16} color="#ef4444" />
                      <Text style={[styles.peakLowText, { color: '#ef4444' }]}>
                        {t('caution')}: {lifeTimeline.low_periods[0].year}
                      </Text>
                    </View>
                  )}
                </View>
              </LinearGradient>
            </AnimatedCard>
          )}

          {/* Aura Heatmap - Planet Strength Visualization */}
          {planetAura && (
            <AnimatedCard delay={600}>
              <LinearGradient colors={['#1e1b4b', '#312e81']} style={[styles.card, styles.auraCard, { marginHorizontal: 0 }]}>
                <View style={styles.cardHeader}>
                  <Ionicons name="planet" size={16} color="#a78bfa" />
                  <Text style={[styles.cardTitle, { color: '#fff' }]}>
                    {t('planetAuraMap')}
                  </Text>
                  <View style={[styles.auraBadge, { backgroundColor: planetAura.overall?.aura_color + '30' }]}>
                    <Text style={[styles.auraBadgeText, { color: planetAura.overall?.aura_color }]}>
                      {planetAura.overall?.aura_score}%
                    </Text>
                  </View>
                </View>

                {/* Overall Aura Status */}
                <View style={styles.auraOverview}>
                  <View style={[styles.auraLevelBadge, { backgroundColor: planetAura.overall?.aura_color + '20' }]}>
                    <Text style={[styles.auraLevelText, { color: planetAura.overall?.aura_color }]}>
                      {planetAura.overall?.aura_tamil || planetAura.overall?.aura_label}
                    </Text>
                  </View>
                  <View style={styles.auraStats}>
                    <View style={styles.auraStat}>
                      <Ionicons name="checkmark-circle" size={14} color="#22c55e" />
                      <Text style={styles.auraStatText}>{planetAura.overall?.favorable_count}</Text>
                    </View>
                    <View style={styles.auraStat}>
                      <Ionicons name="alert-circle" size={14} color="#ef4444" />
                      <Text style={styles.auraStatText}>{planetAura.overall?.unfavorable_count}</Text>
                    </View>
                  </View>
                </View>

                {/* Radial Heatmap - Circular Planet Layout */}
                <View style={styles.auraRadialContainer}>
                  {/* Center Circle */}
                  <View style={styles.auraCenterCircle}>
                    <Text style={styles.auraCenterScore}>{planetAura.overall?.aura_score}</Text>
                    <Text style={styles.auraCenterLabel}>{t('aura')}</Text>
                  </View>

                  {/* Planet Rings */}
                  {planetAura.planets?.map((planet, index) => {
                    const angle = (index * 40) * (Math.PI / 180);
                    const radius = 85;
                    const x = Math.cos(angle) * radius;
                    const y = Math.sin(angle) * radius;

                    return (
                      <TouchableOpacity
                        key={planet.name}
                        style={[
                          styles.auraPlanetOrb,
                          {
                            left: 110 + x - 22,
                            top: 110 + y - 22,
                            backgroundColor: planet.color + '30',
                            borderColor: planet.color,
                          },
                        ]}
                        onPress={() => setSelectedPlanet(planet)}
                      >
                        <Text style={styles.auraPlanetSymbol}>{planet.symbol}</Text>
                        <View style={[styles.auraPlanetStrength, { backgroundColor: planet.color }]}>
                          <Text style={styles.auraPlanetScore}>{planet.strength}</Text>
                        </View>
                      </TouchableOpacity>
                    );
                  })}

                  {/* Influence Lines - SVG alternative using Views */}
                  <View style={styles.auraRings}>
                    <View style={[styles.auraRing, { width: 180, height: 180 }]} />
                    <View style={[styles.auraRing, { width: 140, height: 140 }]} />
                    <View style={[styles.auraRing, { width: 100, height: 100 }]} />
                  </View>
                </View>

                {/* Planet Legend - Horizontal Scroll */}
                <ScrollView
                  horizontal
                  showsHorizontalScrollIndicator={false}
                  contentContainerStyle={styles.auraLegendScroll}
                >
                  {planetAura.planets?.map((planet) => (
                    <TouchableOpacity
                      key={planet.name}
                      style={[
                        styles.auraLegendItem,
                        selectedPlanet?.name === planet.name && styles.auraLegendItemActive,
                        { borderColor: planet.color }
                      ]}
                      onPress={() => setSelectedPlanet(selectedPlanet?.name === planet.name ? null : planet)}
                    >
                      <View style={[styles.auraLegendDot, { backgroundColor: planet.color }]} />
                      <Text style={styles.auraLegendName}>{planet.tamil}</Text>
                      <Text style={[styles.auraLegendScore, { color: planet.color }]}>{planet.strength}</Text>
                      {planet.transit_effect === 'favorable' && (
                        <Ionicons name="trending-up" size={12} color="#22c55e" />
                      )}
                      {planet.transit_effect === 'challenging' && (
                        <Ionicons name="trending-down" size={12} color="#ef4444" />
                      )}
                    </TouchableOpacity>
                  ))}
                </ScrollView>

                {/* Selected Planet Detail */}
                {selectedPlanet && (
                  <View style={[styles.auraPlanetDetail, { borderLeftColor: selectedPlanet.color }]}>
                    <View style={styles.auraPlanetDetailHeader}>
                      <Text style={styles.auraPlanetDetailSymbol}>{selectedPlanet.symbol}</Text>
                      <View>
                        <Text style={styles.auraPlanetDetailName}>{selectedPlanet.tamil}</Text>
                        <Text style={styles.auraPlanetDetailDomain}>{selectedPlanet.domain}</Text>
                      </View>
                      <View style={[styles.auraPlanetDetailScore, { backgroundColor: selectedPlanet.color }]}>
                        <Text style={styles.auraPlanetDetailScoreText}>{selectedPlanet.strength}%</Text>
                      </View>
                    </View>
                    <Text style={styles.auraPlanetDetailInsight}>{selectedPlanet.insight}</Text>
                    <View style={styles.auraPlanetDetailTags}>
                      {selectedPlanet.keywords?.slice(0, 3).map((kw, i) => (
                        <View key={i} style={[styles.auraKeywordTag, { backgroundColor: selectedPlanet.color + '20' }]}>
                          <Text style={[styles.auraKeywordText, { color: selectedPlanet.color }]}>{kw}</Text>
                        </View>
                      ))}
                    </View>
                  </View>
                )}

                {/* Transit Summary */}
                {planetAura.transit_summary && (
                  <View style={styles.auraTransitSummary}>
                    <Ionicons name="pulse" size={14} color="#a78bfa" />
                    <Text style={styles.auraTransitText}>{planetAura.transit_summary}</Text>
                  </View>
                )}

                {/* Dominant & Challenged Planets */}
                <View style={styles.auraDominantRow}>
                  {planetAura.dominant_planets?.length > 0 && (
                    <View style={styles.auraDominantSection}>
                      <Text style={styles.auraDominantLabel}>
                        💪 {t('strong')}
                      </Text>
                      <View style={styles.auraDominantList}>
                        {planetAura.dominant_planets.slice(0, 2).map((p, i) => (
                          <Text key={i} style={styles.auraDominantPlanet}>{p.tamil}</Text>
                        ))}
                      </View>
                    </View>
                  )}
                  {planetAura.challenged_planets?.length > 0 && (
                    <View style={styles.auraDominantSection}>
                      <Text style={styles.auraDominantLabel}>
                        🙏 {t('remedy')}
                      </Text>
                      <View style={styles.auraDominantList}>
                        {planetAura.challenged_planets.slice(0, 2).map((p, i) => (
                          <Text key={i} style={[styles.auraDominantPlanet, { color: '#f97316' }]}>{p.tamil}</Text>
                        ))}
                      </View>
                    </View>
                  )}
                </View>
              </LinearGradient>
            </AnimatedCard>
          )}

          {/* Transits Map - Live Planetary Movements - Premium Design */}
          {transitsMap && (
            <AnimatedCard delay={650}>
              <View style={styles.transitsContainer}>
                {/* Header with Glassmorphism */}
                <LinearGradient
                  colors={['#1e1b4b', '#312e81', '#3730a3']}
                  start={{ x: 0, y: 0 }}
                  end={{ x: 1, y: 1 }}
                  style={styles.transitsHeader}
                >
                  <View style={styles.transitsHeaderContent}>
                    <View style={styles.transitsHeaderLeft}>
                      <Text style={styles.transitsHeaderIcon}>🪐</Text>
                      <View>
                        <Text style={styles.transitsHeaderTitle}>
                          {t('liveTransits')}
                        </Text>
                        <Text style={styles.transitsHeaderSubtitle}>
                          {t('realTimePositions')}
                        </Text>
                      </View>
                    </View>
                    <View style={styles.livePulseContainer}>
                      <View style={styles.livePulseOuter}>
                        <View style={styles.livePulseInner} />
                      </View>
                      <Text style={styles.livePulseText}>{t('live')}</Text>
                    </View>
                  </View>
                </LinearGradient>

                {/* Moon Transit - Hero Section */}
                {transitsMap.moon_transit && (
                  <LinearGradient
                    colors={['#0f172a', '#1e293b']}
                    style={styles.moonHeroSection}
                  >
                    <View style={styles.moonHeroHeader}>
                      <View style={styles.moonHeroIconContainer}>
                        <Text style={styles.moonHeroIcon}>{transitsMap.moon_transit.phase_icon}</Text>
                        <View style={styles.moonHeroGlow} />
                      </View>
                      <View style={styles.moonHeroInfo}>
                        <Text style={styles.moonHeroLabel}>
                          {t('moonSign')}
                        </Text>
                        <Text style={styles.moonHeroSign}>
                          {transitsMap.moon_transit.current_sign_symbol} {transitsMap.moon_transit.current_sign_name}
                        </Text>
                        <Text style={styles.moonHeroPhase}>{transitsMap.moon_transit.phase}</Text>
                      </View>
                      {transitsMap.moon_transit.energy && (
                        <LinearGradient
                          colors={[transitsMap.moon_transit.energy.color + '40', transitsMap.moon_transit.energy.color + '20']}
                          style={styles.moonEnergyCard}
                        >
                          <Text style={styles.moonEnergyEmoji}>{transitsMap.moon_transit.energy.icon}</Text>
                          <Text style={[styles.moonEnergyMood, { color: transitsMap.moon_transit.energy.color }]}>
                            {transitsMap.moon_transit.energy.mood}
                          </Text>
                        </LinearGradient>
                      )}
                    </View>

                    {/* Countdown Timer */}
                    <View style={styles.countdownContainer}>
                      <Text style={styles.countdownLabel}>
                        ⏱ {t('nextSignChange')}
                      </Text>
                      <View style={styles.countdownTimerRow}>
                        <View style={styles.countdownBox}>
                          <LinearGradient colors={['#6366f1', '#4f46e5']} style={styles.countdownBoxGradient}>
                            <Text style={styles.countdownValue}>{transitsMap.moon_transit.time_to_transit?.hours || 0}</Text>
                          </LinearGradient>
                          <Text style={styles.countdownUnit}>{t('hours')}</Text>
                        </View>
                        <Text style={styles.countdownSeparator}>:</Text>
                        <View style={styles.countdownBox}>
                          <LinearGradient colors={['#6366f1', '#4f46e5']} style={styles.countdownBoxGradient}>
                            <Text style={styles.countdownValue}>{transitsMap.moon_transit.time_to_transit?.minutes || 0}</Text>
                          </LinearGradient>
                          <Text style={styles.countdownUnit}>{t('minutes')}</Text>
                        </View>
                      </View>
                      <View style={styles.nextSignRow}>
                        <Ionicons name="arrow-forward-circle" size={18} color="#a78bfa" />
                        <Text style={styles.nextSignText}>
                          {transitsMap.moon_transit.next_sign_symbol} {transitsMap.moon_transit.next_sign_name}
                        </Text>
                      </View>
                    </View>

                    {/* Alert Message */}
                    {transitsMap.moon_transit.transit_message && (
                      <View style={styles.alertMessageBox}>
                        <Ionicons name="notifications" size={16} color="#fbbf24" />
                        <Text style={styles.alertMessageText}>{transitsMap.moon_transit.transit_message}</Text>
                      </View>
                    )}
                  </LinearGradient>
                )}

                {/* Sky Map - Orbital View */}
                <View style={styles.orbitalSection}>
                  <Text style={styles.orbitalTitle}>
                    🌌 {t('celestialMap')}
                  </Text>
                  <View style={styles.orbitalContainer}>
                    {/* Outer Ring */}
                    <View style={styles.orbitalRingOuter} />
                    <View style={styles.orbitalRingMiddle} />
                    <View style={styles.orbitalRingInner} />

                    {/* Planet Positions */}
                    {transitsMap.sky_positions?.map((planet) => {
                      const angleRad = ((planet.angle - 90) * Math.PI) / 180;
                      const radius = planet.radius_factor * 75;
                      const x = Math.cos(angleRad) * radius;
                      const y = Math.sin(angleRad) * radius;

                      return (
                        <View
                          key={planet.planet}
                          style={[
                            styles.orbitalPlanet,
                            {
                              left: 85 + x - 15,
                              top: 85 + y - 15,
                              backgroundColor: planet.color + '30',
                              borderColor: planet.color,
                              shadowColor: planet.color,
                            },
                          ]}
                        >
                          <Text style={[styles.orbitalPlanetSymbol, { color: planet.color }]}>{planet.symbol}</Text>
                        </View>
                      );
                    })}

                    {/* Earth Center */}
                    <View style={styles.earthCenter}>
                      <Text style={styles.earthEmoji}>🌍</Text>
                    </View>
                  </View>
                </View>

                {/* Planet Cards - Horizontal Scroll */}
                <View style={styles.planetCardsSection}>
                  <Text style={styles.planetCardsTitle}>
                    📍 {t('planetPositions')}
                  </Text>
                  <ScrollView
                    horizontal
                    showsHorizontalScrollIndicator={false}
                    contentContainerStyle={styles.planetCardsScroll}
                  >
                    {Object.entries(transitsMap.planets || {}).map(([name, planet]) => (
                      <LinearGradient
                        key={name}
                        colors={[planet.color + '25', planet.color + '10']}
                        style={[styles.planetCard, { borderColor: planet.color + '60' }]}
                      >
                        <View style={[styles.planetCardIconBg, { backgroundColor: planet.color + '30' }]}>
                          <Text style={styles.planetCardSymbol}>{planet.symbol}</Text>
                        </View>
                        <Text style={styles.planetCardName}>{planet.tamil}</Text>
                        <View style={styles.planetCardSignRow}>
                          <Text style={[styles.planetCardSign, { color: planet.color }]}>
                            {planet.sign_symbol}
                          </Text>
                          <Text style={styles.planetCardSignName}>{planet.sign_name}</Text>
                        </View>
                        <Text style={styles.planetCardDegree}>{planet.degree_display}</Text>
                        {planet.is_retrograde && (
                          <View style={styles.retroIndicator}>
                            <Text style={styles.retroIndicatorText}>℞ {t('retrograde')}</Text>
                          </View>
                        )}
                      </LinearGradient>
                    ))}
                  </ScrollView>
                </View>

                {/* Retrograde Alert Section */}
                {transitsMap.retrogrades?.length > 0 && (
                  <View style={styles.retroAlertSection}>
                    <View style={styles.retroAlertHeader}>
                      <Text style={styles.retroAlertIcon}>⚡</Text>
                      <Text style={styles.retroAlertTitle}>
                        {t('retrogradeAlert')}
                      </Text>
                    </View>
                    {transitsMap.retrogrades.map((retro, index) => (
                      <LinearGradient
                        key={index}
                        colors={['#7f1d1d20', '#45122520']}
                        style={[styles.retroAlertCard, { borderLeftColor: retro.color }]}
                      >
                        <View style={styles.retroAlertCardHeader}>
                          <Text style={styles.retroAlertSymbol}>{retro.symbol}</Text>
                          <View style={styles.retroAlertInfo}>
                            <Text style={styles.retroAlertName}>{retro.tamil}</Text>
                            <View style={[
                              styles.retroStatusPill,
                              { backgroundColor: retro.status === 'retrograde' ? '#ef444440' : '#f59e0b40' }
                            ]}>
                              <Text style={[
                                styles.retroStatusText,
                                { color: retro.status === 'retrograde' ? '#fca5a5' : '#fcd34d' }
                              ]}>
                                {retro.status_tamil}
                              </Text>
                            </View>
                          </View>
                          {retro.days_remaining && (
                            <View style={styles.retroDaysLeft}>
                              <Text style={styles.retroDaysNumber}>{retro.days_remaining}</Text>
                              <Text style={styles.retroDaysLabel}>{t('days')}</Text>
                            </View>
                          )}
                        </View>
                        <Text style={styles.retroAlertMessage}>{retro.message}</Text>
                      </LinearGradient>
                    ))}
                  </View>
                )}

                {/* Upcoming Changes */}
                {transitsMap.upcoming_transits?.length > 0 && (
                  <View style={styles.upcomingSection}>
                    <Text style={styles.upcomingSectionTitle}>
                      📅 {t('comingUp')}
                    </Text>
                    {transitsMap.upcoming_transits.slice(0, 3).map((transit, index) => (
                      <View key={index} style={styles.upcomingCard}>
                        <View style={[styles.upcomingIconBox, { backgroundColor: transit.color + '30' }]}>
                          <Text style={styles.upcomingIcon}>{transit.symbol}</Text>
                        </View>
                        <View style={styles.upcomingDetails}>
                          <Text style={styles.upcomingPlanet}>{transit.tamil}</Text>
                          <View style={styles.upcomingArrowRow}>
                            <Text style={styles.upcomingFrom}>{transit.from_sign_name}</Text>
                            <Ionicons name="arrow-forward" size={12} color="#6366f1" />
                            <Text style={styles.upcomingTo}>{transit.to_sign_symbol} {transit.to_sign_name}</Text>
                          </View>
                        </View>
                        <View style={styles.upcomingTimeBox}>
                          <Text style={styles.upcomingTimeValue}>{Math.round(transit.hours_remaining)}</Text>
                          <Text style={styles.upcomingTimeUnit}>{t('hours')}</Text>
                        </View>
                      </View>
                    ))}
                  </View>
                )}

                {/* Auspicious Time Footer */}
                {transitsMap.auspicious_time && (
                  <LinearGradient
                    colors={[transitsMap.auspicious_time.color + '30', transitsMap.auspicious_time.color + '10']}
                    style={styles.auspiciousFooter}
                  >
                    <Ionicons name="sparkles" size={16} color={transitsMap.auspicious_time.color} />
                    <Text style={[styles.auspiciousText, { color: transitsMap.auspicious_time.color }]}>
                      {transitsMap.auspicious_time.name}
                    </Text>
                  </LinearGradient>
                )}
              </View>
            </AnimatedCard>
          )}
        </ScrollView>
      </LinearGradient>

      {/* Score Justification Modal */}
      <ScoreJustificationModal
        visible={showScoreModal}
        onClose={() => setShowScoreModal(false)}
        data={selectedScoreData}
        t={t}
      />

      {/* Timeline Year Detail Modal */}
      <TimelineYearModal
        visible={showTimelineModal}
        onClose={() => {
          setShowTimelineModal(false);
          setSelectedTimelineYear(null);
        }}
        data={selectedTimelineYear}
        language={language}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  gradient: { flex: 1 },
  scrollContent: {},
  loadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#fff7ed' },
  loadingText: { marginTop: 16, color: '#6b7280' },
  headerBar: { height: 4 },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start', padding: 16, backgroundColor: '#fff', borderBottomWidth: 1, borderBottomColor: '#fed7aa' },
  logoRow: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  logoIcon: { width: 28, height: 28 },
  appTitle: { fontSize: 20, fontWeight: 'bold', color: '#9a3412' },
  userInfo: { marginTop: 4 },
  greeting: { fontSize: 14, color: '#6b7280' },
  rasiInfo: { fontSize: 12, color: '#ea580c' },
  timeContainer: { alignItems: 'flex-end' },
  currentTime: { fontSize: 18, fontFamily: 'monospace', color: '#1f2937' },
  periodBadge: { paddingHorizontal: 8, paddingVertical: 4, borderRadius: 12, marginTop: 4 },
  periodText: { fontSize: 10, fontWeight: '600' },

  // Date card
  dateCard: { backgroundColor: '#fff7ed', marginHorizontal: 16, marginTop: 12, padding: 12, borderRadius: 12, alignItems: 'center', borderWidth: 1, borderColor: '#fed7aa' },
  dateText: { fontSize: 14, color: '#9a3412', fontWeight: '500' },

  // Story Preview Row (Instagram-style)
  storyPreviewRow: { paddingHorizontal: 16, paddingVertical: 12 },
  storyCirclesContainer: { flexDirection: 'row', justifyContent: 'space-around', alignItems: 'center' },
  storyCircle: { alignItems: 'center', width: 64 },
  storyCircleActive: {},
  storyGradientBorder: { width: 56, height: 56, borderRadius: 28, padding: 3, justifyContent: 'center', alignItems: 'center' },
  storyInner: { width: 48, height: 48, borderRadius: 24, backgroundColor: '#1a1a2e', justifyContent: 'center', alignItems: 'center' },
  storyMoreCircle: { width: 56, height: 56, borderRadius: 28, backgroundColor: '#fff7ed', borderWidth: 2, borderColor: '#fed7aa', borderStyle: 'dashed', justifyContent: 'center', alignItems: 'center' },
  storyLabel: { fontSize: 10, color: '#6b7280', marginTop: 4, textAlign: 'center' },

  card: { backgroundColor: '#fff', borderRadius: 16, padding: 16, marginHorizontal: 16, marginTop: 16, borderWidth: 1, borderColor: '#fed7aa' },
  cardHeader: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 12 },
  cardTitle: { fontSize: 14, fontWeight: '600', color: '#1f2937', flex: 1 },
  tapHintSmall: { fontSize: 10, color: '#9ca3af' },
  panchangamGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  panchangamItem: { flex: 1, minWidth: '45%', backgroundColor: '#fff7ed', borderRadius: 12, padding: 12 },
  panchangamLabel: { fontSize: 10, color: '#6b7280', marginBottom: 4 },
  panchangamValue: { fontSize: 12, fontWeight: '600', color: '#1f2937' },

  scoreRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  scoreLabel: { fontSize: 12, color: '#6b7280' },
  scoreValue: { flexDirection: 'row', alignItems: 'baseline', gap: 4, marginTop: 4 },
  scoreNumber: { fontSize: 36, fontWeight: 'bold', color: '#ea580c' },
  scoreMax: { fontSize: 14, color: '#9ca3af' },
  scoreBadge: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 8, paddingVertical: 4, borderRadius: 12, marginLeft: 8, gap: 4 },
  scoreBadgeText: { fontSize: 12, fontWeight: '500' },
  scoreCircle: { width: 70, height: 70, borderRadius: 35, backgroundColor: '#fff7ed', borderWidth: 4, borderColor: '#ea580c', justifyContent: 'center', alignItems: 'center' },
  scoreCircleText: { fontSize: 16, fontWeight: 'bold', color: '#ea580c' },
  tapHint: { fontSize: 8, color: '#9ca3af', marginTop: 2 },

  insightBox: { flexDirection: 'row', alignItems: 'flex-start', gap: 8, padding: 12, borderRadius: 12, marginTop: 16, borderWidth: 1, borderColor: '#fed7aa' },
  insightText: { flex: 1, fontSize: 13, color: '#374151', lineHeight: 20 },

  lifeAreasRow: { flexDirection: 'row', gap: 10, marginBottom: 10 },
  lifeAreaCard: { flex: 1, backgroundColor: '#fff', borderRadius: 14, padding: 14, borderWidth: 1, borderColor: '#fed7aa', minHeight: 120 },
  lifeAreaHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 },
  lifeAreaIconBg: { width: 32, height: 32, borderRadius: 16, justifyContent: 'center', alignItems: 'center' },
  lifeAreaBadge: { paddingHorizontal: 8, paddingVertical: 3, borderRadius: 10 },
  lifeAreaBadgeText: { fontSize: 10, fontWeight: '600' },
  lifeAreaName: { fontSize: 14, color: '#374151', fontWeight: '600', marginBottom: 6 },
  lifeAreaScoreRow: { flexDirection: 'row', alignItems: 'baseline' },
  lifeAreaScore: { fontSize: 26, fontWeight: 'bold' },
  lifeAreaMax: { fontSize: 11, color: '#9ca3af', marginLeft: 2 },
  lifeAreaProgressBar: { height: 5, backgroundColor: '#f3f4f6', borderRadius: 3, marginTop: 10, overflow: 'hidden' },
  lifeAreaProgressFill: { height: 5, borderRadius: 3 },
  progressBar: { height: 6, backgroundColor: '#f3f4f6', borderRadius: 3, marginTop: 8, overflow: 'hidden' },
  progressFill: { height: 6, borderRadius: 3 },

  // Projection styles
  projectionToggle: { flexDirection: 'row', backgroundColor: '#f3f4f6', borderRadius: 10, padding: 4, marginBottom: 12 },
  toggleBtn: { flex: 1, paddingVertical: 8, borderRadius: 8, alignItems: 'center' },
  toggleBtnActive: { backgroundColor: '#fff', shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.1, shadowRadius: 2, elevation: 2 },
  toggleText: { fontSize: 12, color: '#6b7280' },
  toggleTextActive: { color: '#f97316', fontWeight: '600' },

  monthsScroll: { marginHorizontal: -4 },
  monthCard: { width: 80, backgroundColor: '#fff', borderRadius: 12, padding: 10, marginHorizontal: 4, borderWidth: 1, borderColor: '#e5e7eb', alignItems: 'center' },
  monthName: { fontSize: 11, color: '#374151', fontWeight: '500', marginBottom: 6 },
  monthScoreBadge: { paddingHorizontal: 8, paddingVertical: 4, borderRadius: 10, marginBottom: 6 },
  monthScore: { fontSize: 14, fontWeight: 'bold' },
  monthBarContainer: { width: '100%', height: 4, backgroundColor: '#f3f4f6', borderRadius: 2 },
  monthBar: { height: 4, borderRadius: 2 },

  yearsGrid: { gap: 12 },

  // Past Years styles
  pastYearsGrid: { flexDirection: 'row', gap: 12 },
  pastYearCard: { flex: 1, backgroundColor: '#f9fafb', borderRadius: 12, padding: 12, borderWidth: 1, borderColor: '#e5e7eb' },
  pastYearHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 },
  pastYearLabel: { fontSize: 16, fontWeight: 'bold', color: '#374151' },
  pastYearBadge: { paddingHorizontal: 8, paddingVertical: 2, borderRadius: 10 },
  pastYearScore: { fontSize: 13, fontWeight: '600' },
  pastYearDasha: { fontSize: 11, color: '#6b7280', marginBottom: 8 },
  pastYearBar: { height: 4, backgroundColor: '#e5e7eb', borderRadius: 2, overflow: 'hidden' },
  pastYearBarFill: { height: 4, borderRadius: 2 },

  yearCard: { borderRadius: 14, overflow: 'hidden', borderWidth: 1, borderColor: '#e5e7eb' },
  yearCardGradient: { flexDirection: 'row', alignItems: 'center', padding: 16, gap: 12 },
  yearIconBg: { width: 44, height: 44, borderRadius: 22, justifyContent: 'center', alignItems: 'center' },
  yearInfo: { flex: 1 },
  yearName: { fontSize: 18, fontWeight: 'bold', color: '#1f2937' },
  yearLabel: { fontSize: 12, color: '#6b7280', marginTop: 2 },
  yearScoreContainer: { alignItems: 'flex-end', marginRight: 8 },
  yearScore: { fontSize: 22, fontWeight: 'bold' },
  yearScoreBar: { width: 60, height: 4, borderRadius: 2, marginTop: 4 },
  yearScoreFill: { height: 4, borderRadius: 2 },

  quickActionsGrid: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 12 },
  quickActionBtn: { flex: 1, alignItems: 'center', backgroundColor: '#fff', borderRadius: 12, padding: 16, marginHorizontal: 4, borderWidth: 1, borderColor: '#fed7aa' },
  quickActionLabel: { fontSize: 11, color: '#6b7280', marginTop: 8 },

  dashaCard: { borderColor: '#ddd6fe', marginHorizontal: 16 },
  dashaGrid: { flexDirection: 'row', gap: 12 },
  dashaItem: { flex: 1, backgroundColor: 'rgba(255,255,255,0.5)', borderRadius: 12, padding: 12 },
  dashaLabel: { fontSize: 11, color: '#6b7280' },
  dashaValue: { fontSize: 14, fontWeight: '600', color: '#7c3aed', marginTop: 4 },

  // Modal styles
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)' },
  modalScrollView: { marginTop: 'auto', maxHeight: '85%' },
  modalContent: { backgroundColor: '#fff', borderTopLeftRadius: 24, borderTopRightRadius: 24, padding: 20, paddingBottom: 40 },
  modalHeader: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 16 },
  modalIconBg: { width: 48, height: 48, borderRadius: 24, justifyContent: 'center', alignItems: 'center' },
  modalTitle: { flex: 1, fontSize: 18, fontWeight: 'bold', color: '#1f2937' },
  modalCloseBtn: { padding: 4 },
  modalScoreSection: { flexDirection: 'row', alignItems: 'baseline', justifyContent: 'center', marginBottom: 16 },
  modalScoreValue: { fontSize: 48, fontWeight: 'bold' },
  modalScoreMax: { fontSize: 18, color: '#9ca3af', marginLeft: 4 },
  modalDivider: { height: 1, backgroundColor: '#e5e7eb', marginVertical: 16 },
  modalSectionTitle: { fontSize: 14, fontWeight: '600', color: '#374151', marginBottom: 12 },
  factorItem: { backgroundColor: '#f9fafb', borderRadius: 12, padding: 12, marginBottom: 10 },
  factorHeader: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  factorName: { flex: 1, fontSize: 13, fontWeight: '500', color: '#374151' },
  factorScore: { fontSize: 14, fontWeight: 'bold' },
  factorDesc: { fontSize: 12, color: '#6b7280', marginTop: 6, marginLeft: 26 },

  // Positives styles
  positiveItem: { flexDirection: 'row', alignItems: 'flex-start', gap: 12, marginBottom: 12, backgroundColor: '#f0fdf4', borderRadius: 12, padding: 12, borderWidth: 1, borderColor: '#bbf7d0' },
  positiveIconBg: { width: 36, height: 36, borderRadius: 18, backgroundColor: '#dcfce7', justifyContent: 'center', alignItems: 'center' },
  positiveContent: { flex: 1 },
  positiveTitle: { fontSize: 14, fontWeight: '600', color: '#15803d', marginBottom: 4 },
  positiveDesc: { fontSize: 12, color: '#166534', lineHeight: 18 },

  // Remedies styles
  remediesBox: { backgroundColor: '#fef3c7', borderRadius: 12, padding: 12, borderWidth: 1, borderColor: '#fde68a' },
  remedyItem: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 8 },
  remedyText: { flex: 1, fontSize: 13, color: '#92400e', lineHeight: 18 },

  suggestionBox: { flexDirection: 'row', alignItems: 'flex-start', gap: 10, backgroundColor: '#fff7ed', borderRadius: 12, padding: 14, marginTop: 16, borderWidth: 1, borderColor: '#fed7aa' },
  suggestionText: { flex: 1, fontSize: 13, color: '#9a3412', lineHeight: 20 },
  modalButton: { backgroundColor: '#f97316', borderRadius: 12, paddingVertical: 14, alignItems: 'center', marginTop: 20 },
  modalButtonText: { color: '#fff', fontSize: 16, fontWeight: '600' },

  // Score breakdown detailed styles
  qualityBadge: { alignSelf: 'center', paddingHorizontal: 16, paddingVertical: 6, borderRadius: 20, marginBottom: 12 },
  qualityText: { fontSize: 14, fontWeight: '600' },
  dashaInfoBox: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, backgroundColor: '#f3e8ff', borderRadius: 10, paddingVertical: 8, paddingHorizontal: 12, marginBottom: 8 },
  dashaInfoText: { fontSize: 13, color: '#7c3aed', fontWeight: '500' },
  formulaText: { fontSize: 11, color: '#6b7280', fontFamily: 'monospace', backgroundColor: '#f3f4f6', padding: 10, borderRadius: 8, marginBottom: 12, textAlign: 'center' },

  // Breakdown card styles
  breakdownCard: { backgroundColor: '#f9fafb', borderRadius: 12, padding: 12, marginBottom: 10, borderWidth: 1, borderColor: '#e5e7eb' },
  breakdownHeader: { flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 8 },
  breakdownIconBg: { width: 32, height: 32, borderRadius: 16, justifyContent: 'center', alignItems: 'center' },
  breakdownTitleRow: { flex: 1, flexDirection: 'row', alignItems: 'center', gap: 6 },
  breakdownTitle: { fontSize: 13, fontWeight: '600', color: '#374151' },
  breakdownWeight: { fontSize: 11, color: '#9ca3af' },
  breakdownContribution: { fontSize: 16, fontWeight: 'bold' },
  breakdownProgressBg: { height: 6, backgroundColor: '#e5e7eb', borderRadius: 3, marginBottom: 8 },
  breakdownProgressFill: { height: 6, borderRadius: 3 },
  breakdownFactors: { marginTop: 4 },
  miniFactorRow: { flexDirection: 'row', alignItems: 'center', gap: 6, paddingVertical: 3 },
  miniFactorText: { flex: 1, fontSize: 11, color: '#6b7280' },
  miniFactorValue: { fontSize: 11, fontWeight: '600' },

  // Final calculation styles
  finalCalcBox: { backgroundColor: '#fef3c7', borderRadius: 10, padding: 12, marginTop: 8, alignItems: 'center' },
  finalCalcLabel: { fontSize: 12, color: '#92400e', fontWeight: '600', marginBottom: 4 },
  finalCalcFormula: { fontSize: 10, color: '#a16207', fontFamily: 'monospace', marginBottom: 4 },
  finalCalcResult: { fontSize: 18, fontWeight: 'bold', color: '#b45309' },

  // Simple breakdown styles
  simpleBreakdownRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingVertical: 8, borderBottomWidth: 1, borderBottomColor: '#f3f4f6' },
  simpleBreakdownLeft: { flexDirection: 'row', alignItems: 'center', gap: 8, flex: 1 },
  simpleBreakdownLabel: { fontSize: 13, color: '#374151' },
  simpleBreakdownRight: { flexDirection: 'row', alignItems: 'center', gap: 10, flex: 1.5 },
  simpleProgressBg: { flex: 1, height: 6, backgroundColor: '#e5e7eb', borderRadius: 3 },
  simpleProgressFill: { height: 6, borderRadius: 3 },
  simpleBreakdownValue: { fontSize: 14, fontWeight: '600', color: '#374151', minWidth: 35, textAlign: 'right' },

  // Area scores grid styles
  areaScoresGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10 },
  areaScoreCard: { flex: 1, minWidth: '45%', backgroundColor: '#fff', borderRadius: 10, padding: 12, alignItems: 'center', borderWidth: 1 },
  areaScoreLabel: { fontSize: 11, color: '#6b7280', marginTop: 4 },
  areaScoreValue: { fontSize: 18, fontWeight: 'bold', marginTop: 2 },

  // Life Timeline styles
  timelineCard: { borderColor: '#c4b5fd', marginHorizontal: 16, marginTop: 16 },
  trendSummary: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 },
  trendBadge: { flexDirection: 'row', alignItems: 'center', gap: 6, paddingHorizontal: 12, paddingVertical: 6, borderRadius: 20 },
  trendText: { fontSize: 13, fontWeight: '600' },
  trendAvg: { fontSize: 12, color: '#94a3b8' },
  // Legend styles
  timelineLegend: { backgroundColor: 'rgba(51, 65, 85, 0.5)', borderRadius: 10, padding: 10, marginBottom: 12 },
  timelineLegendRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 6 },
  timelineLegendItem: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  timelineLegendDot: { width: 10, height: 10, borderRadius: 5 },
  timelineLegendText: { fontSize: 10, color: '#94a3b8' },
  timelineLegendVersion: { fontSize: 9, color: '#64748b', fontStyle: 'italic' },
  timelineScrollContent: { paddingHorizontal: 4, paddingVertical: 8 },
  timelineYear: { alignItems: 'center', marginRight: 12, paddingVertical: 8, paddingHorizontal: 6, borderRadius: 12, minWidth: 56 },
  timelineYearCurrent: { backgroundColor: 'rgba(249, 115, 22, 0.15)', borderWidth: 2, borderColor: '#f97316' },
  timelineYearPeak: { backgroundColor: 'rgba(34, 197, 94, 0.1)' },
  timelineYearLow: { backgroundColor: 'rgba(239, 68, 68, 0.1)' },
  timelineBarContainer: { width: 28, height: 80, backgroundColor: '#334155', borderRadius: 14, justifyContent: 'flex-end', overflow: 'hidden', marginBottom: 4 },
  timelineBarSegment: { width: '100%' },
  timelineBar: { width: '100%', borderRadius: 14 },
  timelineScoreBadge: { paddingHorizontal: 6, paddingVertical: 2, borderRadius: 8, marginBottom: 4 },
  timelineScoreText: { fontSize: 10, fontWeight: '700', color: '#fff' },
  timelineYearLabel: { fontSize: 13, fontWeight: '600', color: '#e2e8f0' },
  timelineYearLabelCurrent: { color: '#f97316', fontWeight: '700' },
  timelineAge: { fontSize: 10, color: '#94a3b8', marginTop: 2 },
  timelineDasha: { fontSize: 8, color: '#a78bfa', marginTop: 1 },
  timelineEventDots: { flexDirection: 'row', gap: 3, marginTop: 4, minHeight: 10 },
  timelineEventDot: { width: 8, height: 8, borderRadius: 4 },
  // TimelineYearModal styles
  tlmAreaContainer: { marginBottom: 8 },
  tlmAreaRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 10 },
  tlmAreaInfo: { flexDirection: 'row', alignItems: 'center', width: 90, gap: 6 },
  tlmAreaLabel: { fontSize: 12, color: '#374151' },
  tlmAreaBarBg: { flex: 1, height: 12, backgroundColor: '#e5e7eb', borderRadius: 6, overflow: 'hidden', marginHorizontal: 8 },
  tlmAreaBarFill: { height: '100%', borderRadius: 6 },
  tlmAreaScore: { fontSize: 12, fontWeight: '600', width: 40, textAlign: 'right' },
  tlmTraceBox: { backgroundColor: '#f3f4f6', borderRadius: 10, padding: 12, marginBottom: 8 },
  tlmTraceVersion: { fontSize: 10, color: '#6b7280', marginBottom: 4 },
  tlmTraceFormula: { fontSize: 11, color: '#374151', fontFamily: 'monospace' },
  tlmTraceMeta: { flexDirection: 'row', alignItems: 'center', gap: 4, marginTop: 6 },
  tlmTraceMetaText: { fontSize: 11, color: '#f97316', fontWeight: '500' },
  tlmEventsGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  tlmEventChip: { flexDirection: 'row', alignItems: 'center', gap: 6, paddingHorizontal: 10, paddingVertical: 6, borderRadius: 16, borderWidth: 1 },
  tlmEventText: { fontSize: 11, fontWeight: '500' },
  majorEventsPreview: { marginTop: 16, paddingTop: 16, borderTopWidth: 1, borderTopColor: '#334155' },
  majorEventsTitle: { fontSize: 13, fontWeight: '600', color: '#e2e8f0', marginBottom: 10 },
  majorEventsList: { gap: 8 },
  majorEventItem: { flexDirection: 'row', alignItems: 'center', gap: 10, backgroundColor: 'rgba(51, 65, 85, 0.6)', borderRadius: 10, paddingVertical: 8, paddingHorizontal: 12 },
  majorEventIcon: { fontSize: 18 },
  majorEventYear: { fontSize: 13, fontWeight: '700', color: '#a78bfa', minWidth: 40 },
  majorEventLabel: { flex: 1, fontSize: 12, color: '#cbd5e1' },
  peakLowContainer: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 12, paddingTop: 12, borderTopWidth: 1, borderTopColor: '#334155' },
  peakLowItem: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  peakLowText: { fontSize: 12, color: '#cbd5e1' },

  // Aura Heatmap styles
  auraCard: { borderColor: '#8b5cf6', marginHorizontal: 16, marginTop: 16 },
  auraBadge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12 },
  auraBadgeText: { fontSize: 14, fontWeight: '700' },
  auraOverview: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 },
  auraLevelBadge: { paddingHorizontal: 14, paddingVertical: 6, borderRadius: 16 },
  auraLevelText: { fontSize: 13, fontWeight: '600' },
  auraStats: { flexDirection: 'row', gap: 12 },
  auraStat: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  auraStatText: { fontSize: 13, color: '#e5e7eb', fontWeight: '500' },

  // Radial container
  auraRadialContainer: { width: 220, height: 220, alignSelf: 'center', position: 'relative', marginVertical: 10 },
  auraCenterCircle: { position: 'absolute', left: 85, top: 85, width: 50, height: 50, borderRadius: 25, backgroundColor: '#4c1d95', justifyContent: 'center', alignItems: 'center', zIndex: 10 },
  auraCenterScore: { fontSize: 18, fontWeight: 'bold', color: '#fff' },
  auraCenterLabel: { fontSize: 9, color: '#c4b5fd' },

  // Planet orbs
  auraPlanetOrb: { position: 'absolute', width: 44, height: 44, borderRadius: 22, borderWidth: 2, justifyContent: 'center', alignItems: 'center', zIndex: 5 },
  auraPlanetSymbol: { fontSize: 16, color: '#fff' },
  auraPlanetStrength: { position: 'absolute', bottom: -4, right: -4, width: 20, height: 20, borderRadius: 10, justifyContent: 'center', alignItems: 'center' },
  auraPlanetScore: { fontSize: 9, fontWeight: 'bold', color: '#fff' },

  // Rings
  auraRings: { position: 'absolute', left: 20, top: 20, width: 180, height: 180, justifyContent: 'center', alignItems: 'center' },
  auraRing: { position: 'absolute', borderRadius: 100, borderWidth: 1, borderColor: 'rgba(167, 139, 250, 0.2)' },

  // Legend
  auraLegendScroll: { paddingVertical: 12, paddingHorizontal: 4 },
  auraLegendItem: { flexDirection: 'row', alignItems: 'center', gap: 6, backgroundColor: 'rgba(255,255,255,0.1)', paddingHorizontal: 10, paddingVertical: 6, borderRadius: 16, marginRight: 8, borderWidth: 1 },
  auraLegendItemActive: { backgroundColor: 'rgba(255,255,255,0.2)' },
  auraLegendDot: { width: 8, height: 8, borderRadius: 4 },
  auraLegendName: { fontSize: 11, color: '#e5e7eb' },
  auraLegendScore: { fontSize: 11, fontWeight: '600' },

  // Planet detail
  auraPlanetDetail: { backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: 12, padding: 12, marginTop: 8, borderLeftWidth: 3 },
  auraPlanetDetailHeader: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  auraPlanetDetailSymbol: { fontSize: 24, color: '#fff' },
  auraPlanetDetailName: { fontSize: 14, fontWeight: '600', color: '#fff' },
  auraPlanetDetailDomain: { fontSize: 11, color: '#a78bfa', textTransform: 'capitalize' },
  auraPlanetDetailScore: { marginLeft: 'auto', paddingHorizontal: 10, paddingVertical: 4, borderRadius: 10 },
  auraPlanetDetailScoreText: { fontSize: 13, fontWeight: 'bold', color: '#fff' },
  auraPlanetDetailInsight: { fontSize: 12, color: '#c4b5fd', marginTop: 8, lineHeight: 18 },
  auraPlanetDetailTags: { flexDirection: 'row', gap: 6, marginTop: 8, flexWrap: 'wrap' },
  auraKeywordTag: { paddingHorizontal: 8, paddingVertical: 3, borderRadius: 8 },
  auraKeywordText: { fontSize: 10, fontWeight: '500' },

  // Transit summary
  auraTransitSummary: { flexDirection: 'row', alignItems: 'center', gap: 8, backgroundColor: 'rgba(167, 139, 250, 0.15)', borderRadius: 10, padding: 10, marginTop: 12 },
  auraTransitText: { flex: 1, fontSize: 11, color: '#c4b5fd', lineHeight: 16 },

  // Dominant planets
  auraDominantRow: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 12, paddingTop: 12, borderTopWidth: 1, borderTopColor: 'rgba(167, 139, 250, 0.2)' },
  auraDominantSection: { flex: 1 },
  auraDominantLabel: { fontSize: 11, color: '#9ca3af', marginBottom: 4 },
  auraDominantList: { flexDirection: 'row', gap: 6 },
  auraDominantPlanet: { fontSize: 12, color: '#22c55e', fontWeight: '500' },

  // Transits Map - Premium Styles
  transitsContainer: { marginHorizontal: 16, marginTop: 16, borderRadius: 20, overflow: 'hidden', backgroundColor: '#0f0a1e' },
  transitsHeader: { padding: 16, borderBottomWidth: 1, borderBottomColor: 'rgba(139, 92, 246, 0.2)' },
  transitsHeaderContent: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  transitsHeaderLeft: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  transitsHeaderIcon: { fontSize: 28 },
  transitsHeaderTitle: { fontSize: 18, fontWeight: '700', color: '#fff' },
  transitsHeaderSubtitle: { fontSize: 11, color: '#a78bfa', marginTop: 2 },
  livePulseContainer: { flexDirection: 'row', alignItems: 'center', gap: 6, backgroundColor: 'rgba(239, 68, 68, 0.2)', paddingHorizontal: 10, paddingVertical: 5, borderRadius: 12 },
  livePulseOuter: { width: 12, height: 12, borderRadius: 6, backgroundColor: 'rgba(239, 68, 68, 0.3)', justifyContent: 'center', alignItems: 'center' },
  livePulseInner: { width: 6, height: 6, borderRadius: 3, backgroundColor: '#ef4444' },
  livePulseText: { fontSize: 10, fontWeight: '800', color: '#ef4444', letterSpacing: 1 },

  // Moon Hero Section
  moonHeroSection: { padding: 20 },
  moonHeroHeader: { flexDirection: 'row', alignItems: 'center', gap: 14 },
  moonHeroIconContainer: { position: 'relative' },
  moonHeroIcon: { fontSize: 44 },
  moonHeroGlow: { position: 'absolute', width: 50, height: 50, borderRadius: 25, backgroundColor: 'rgba(251, 191, 36, 0.15)', top: -3, left: -3 },
  moonHeroInfo: { flex: 1 },
  moonHeroLabel: { fontSize: 11, color: '#94a3b8', textTransform: 'uppercase', letterSpacing: 1 },
  moonHeroSign: { fontSize: 20, fontWeight: '700', color: '#fff', marginTop: 4 },
  moonHeroPhase: { fontSize: 12, color: '#a78bfa', marginTop: 2 },
  moonEnergyCard: { paddingHorizontal: 12, paddingVertical: 8, borderRadius: 12, alignItems: 'center' },
  moonEnergyEmoji: { fontSize: 18 },
  moonEnergyMood: { fontSize: 10, fontWeight: '600', marginTop: 2 },

  // Countdown Timer
  countdownContainer: { alignItems: 'center', marginTop: 24, paddingTop: 20, borderTopWidth: 1, borderTopColor: 'rgba(139, 92, 246, 0.15)' },
  countdownLabel: { fontSize: 12, color: '#94a3b8', marginBottom: 12 },
  countdownTimerRow: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  countdownBox: { alignItems: 'center' },
  countdownBoxGradient: { width: 70, height: 70, borderRadius: 16, justifyContent: 'center', alignItems: 'center' },
  countdownValue: { fontSize: 32, fontWeight: '800', color: '#fff' },
  countdownUnit: { fontSize: 10, color: '#94a3b8', marginTop: 6, textTransform: 'uppercase', letterSpacing: 1 },
  countdownSeparator: { fontSize: 32, fontWeight: '800', color: '#6366f1', marginBottom: 20 },
  nextSignRow: { flexDirection: 'row', alignItems: 'center', gap: 8, marginTop: 16, backgroundColor: 'rgba(139, 92, 246, 0.15)', paddingHorizontal: 14, paddingVertical: 8, borderRadius: 20 },
  nextSignText: { fontSize: 14, fontWeight: '600', color: '#a78bfa' },

  // Alert Message
  alertMessageBox: { flexDirection: 'row', alignItems: 'center', gap: 10, backgroundColor: 'rgba(251, 191, 36, 0.12)', borderRadius: 12, padding: 12, marginTop: 16, borderWidth: 1, borderColor: 'rgba(251, 191, 36, 0.2)' },
  alertMessageText: { flex: 1, fontSize: 12, color: '#fbbf24', lineHeight: 18 },

  // Orbital View
  orbitalSection: { padding: 20, paddingTop: 0 },
  orbitalTitle: { fontSize: 14, fontWeight: '600', color: '#e2e8f0', marginBottom: 16, textAlign: 'center' },
  orbitalContainer: { width: 170, height: 170, alignSelf: 'center', position: 'relative' },
  orbitalRingOuter: { position: 'absolute', width: 170, height: 170, borderRadius: 85, borderWidth: 1, borderColor: 'rgba(139, 92, 246, 0.2)' },
  orbitalRingMiddle: { position: 'absolute', width: 120, height: 120, borderRadius: 60, borderWidth: 1, borderColor: 'rgba(139, 92, 246, 0.15)', left: 25, top: 25 },
  orbitalRingInner: { position: 'absolute', width: 70, height: 70, borderRadius: 35, borderWidth: 1, borderColor: 'rgba(139, 92, 246, 0.1)', left: 50, top: 50 },
  orbitalPlanet: { position: 'absolute', width: 30, height: 30, borderRadius: 15, borderWidth: 2, justifyContent: 'center', alignItems: 'center', shadowOffset: { width: 0, height: 0 }, shadowOpacity: 0.5, shadowRadius: 8, elevation: 5 },
  orbitalPlanetSymbol: { fontSize: 14, fontWeight: '600' },
  earthCenter: { position: 'absolute', left: 70, top: 70, width: 30, height: 30, borderRadius: 15, backgroundColor: 'rgba(59, 130, 246, 0.3)', justifyContent: 'center', alignItems: 'center' },
  earthEmoji: { fontSize: 16 },

  // Planet Cards
  planetCardsSection: { paddingBottom: 16 },
  planetCardsTitle: { fontSize: 14, fontWeight: '600', color: '#e2e8f0', marginBottom: 12, paddingHorizontal: 20 },
  planetCardsScroll: { paddingHorizontal: 16 },
  planetCard: { alignItems: 'center', paddingHorizontal: 14, paddingVertical: 14, borderRadius: 16, marginRight: 12, borderWidth: 1, minWidth: 85 },
  planetCardIconBg: { width: 40, height: 40, borderRadius: 20, justifyContent: 'center', alignItems: 'center', marginBottom: 8 },
  planetCardSymbol: { fontSize: 20 },
  planetCardName: { fontSize: 11, color: '#e2e8f0', fontWeight: '500', marginBottom: 6 },
  planetCardSignRow: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  planetCardSign: { fontSize: 14, fontWeight: '700' },
  planetCardSignName: { fontSize: 10, color: '#94a3b8' },
  planetCardDegree: { fontSize: 9, color: '#64748b', marginTop: 4 },
  retroIndicator: { backgroundColor: 'rgba(239, 68, 68, 0.2)', paddingHorizontal: 8, paddingVertical: 3, borderRadius: 8, marginTop: 6 },
  retroIndicatorText: { fontSize: 9, color: '#fca5a5', fontWeight: '600' },

  // Retrograde Alert
  retroAlertSection: { padding: 16, paddingTop: 0 },
  retroAlertHeader: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 12 },
  retroAlertIcon: { fontSize: 18 },
  retroAlertTitle: { fontSize: 14, fontWeight: '700', color: '#fbbf24' },
  retroAlertCard: { borderRadius: 14, padding: 14, marginBottom: 10, borderLeftWidth: 4 },
  retroAlertCardHeader: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  retroAlertSymbol: { fontSize: 22, color: '#fff' },
  retroAlertInfo: { flex: 1 },
  retroAlertName: { fontSize: 14, fontWeight: '600', color: '#fff' },
  retroStatusPill: { paddingHorizontal: 8, paddingVertical: 3, borderRadius: 10, marginTop: 4, alignSelf: 'flex-start' },
  retroStatusText: { fontSize: 10, fontWeight: '600' },
  retroDaysLeft: { alignItems: 'center', backgroundColor: 'rgba(251, 191, 36, 0.15)', paddingHorizontal: 12, paddingVertical: 6, borderRadius: 10 },
  retroDaysNumber: { fontSize: 18, fontWeight: '800', color: '#fbbf24' },
  retroDaysLabel: { fontSize: 9, color: '#94a3b8' },
  retroAlertMessage: { fontSize: 11, color: '#94a3b8', marginTop: 10, lineHeight: 16 },

  // Upcoming Section
  upcomingSection: { padding: 16, paddingTop: 0 },
  upcomingSectionTitle: { fontSize: 14, fontWeight: '600', color: '#e2e8f0', marginBottom: 12 },
  upcomingCard: { flexDirection: 'row', alignItems: 'center', gap: 12, backgroundColor: 'rgba(255,255,255,0.04)', borderRadius: 14, padding: 12, marginBottom: 10 },
  upcomingIconBox: { width: 44, height: 44, borderRadius: 22, justifyContent: 'center', alignItems: 'center' },
  upcomingIcon: { fontSize: 20 },
  upcomingDetails: { flex: 1 },
  upcomingPlanet: { fontSize: 14, fontWeight: '600', color: '#fff' },
  upcomingArrowRow: { flexDirection: 'row', alignItems: 'center', gap: 6, marginTop: 4 },
  upcomingFrom: { fontSize: 11, color: '#94a3b8' },
  upcomingTo: { fontSize: 11, color: '#a78bfa', fontWeight: '500' },
  upcomingTimeBox: { alignItems: 'center', backgroundColor: 'rgba(99, 102, 241, 0.2)', paddingHorizontal: 14, paddingVertical: 8, borderRadius: 12 },
  upcomingTimeValue: { fontSize: 18, fontWeight: '800', color: '#818cf8' },
  upcomingTimeUnit: { fontSize: 9, color: '#94a3b8', marginTop: 2 },

  // Auspicious Footer
  auspiciousFooter: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, padding: 14, borderTopWidth: 1, borderTopColor: 'rgba(139, 92, 246, 0.1)' },
  auspiciousText: { fontSize: 13, fontWeight: '600' },
});
