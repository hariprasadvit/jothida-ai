import React, { useCallback, useEffect, useRef, useState } from 'react';
import {
  ActivityIndicator,
  Animated,
  Platform,
  RefreshControl,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import AppHeader from '../components/AppHeader';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { remedyAPI } from '../services/api';

// Goal options for the remedy engine
const GOALS = [
  { id: 'love', icon: 'heart', color: '#ec4899', label: { ta: 'காதல்', en: 'Love', kn: 'ಪ್ರೀತಿ' } },
  { id: 'job', icon: 'briefcase', color: '#3b82f6', label: { ta: 'வேலை', en: 'Job', kn: 'ಉದ್ಯೋಗ' } },
  { id: 'wealth', icon: 'cash', color: '#f59e0b', label: { ta: 'செல்வம்', en: 'Wealth', kn: 'ಸಂಪತ್ತು' } },
  { id: 'peace', icon: 'leaf', color: '#22c55e', label: { ta: 'அமைதி', en: 'Peace', kn: 'ಶಾಂತಿ' } },
  { id: 'health', icon: 'fitness', color: '#ef4444', label: { ta: 'உடல்நலம்', en: 'Health', kn: 'ಆರೋಗ್ಯ' } },
  { id: 'education', icon: 'book', color: '#8b5cf6', label: { ta: 'கல்வி', en: 'Education', kn: 'ಶಿಕ್ಷಣ' } },
];

const AnimatedRemedyCard = ({ remedy, index, language, t }) => {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(30)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 400,
        delay: index * 100,
        useNativeDriver: true,
      }),
      Animated.timing(slideAnim, {
        toValue: 0,
        duration: 400,
        delay: index * 100,
        useNativeDriver: true,
      }),
    ]).start();
  }, [fadeAnim, index, slideAnim]);

  const getTypeIcon = (type) => {
    switch (type) {
      case 'dasha_remedy':
        return 'planet';
      case 'weak_planet_remedy':
        return 'trending-up';
      case 'dosha_remedy':
        return 'shield';
      case 'goal_remedy':
        return 'flag';
      default:
        return 'star';
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'dasha_remedy':
        return '#f97316';
      case 'weak_planet_remedy':
        return '#3b82f6';
      case 'dosha_remedy':
        return '#ef4444';
      case 'goal_remedy':
        return '#22c55e';
      default:
        return '#8b5cf6';
    }
  };

  return (
    <Animated.View
      style={[
        styles.remedyCard,
        {
          opacity: fadeAnim,
          transform: [{ translateY: slideAnim }],
        },
      ]}
    >
      <View style={[styles.remedyHeader, { borderLeftColor: getTypeColor(remedy.type) }]}>
        <View style={[styles.typeIconContainer, { backgroundColor: `${getTypeColor(remedy.type)}20` }]}>
          <Ionicons name={getTypeIcon(remedy.type)} size={24} color={getTypeColor(remedy.type)} />
        </View>
        <View style={styles.remedyHeaderText}>
          <Text style={styles.remedyTitle}>{language === 'ta' ? remedy.title_tamil : remedy.title}</Text>
          {(remedy.planet_tamil || remedy.planet) && (
            <Text style={styles.remedyPlanet}>
              {language === 'en' ? remedy.planet : remedy.planet_tamil} • {t('priority')}: {remedy.priority}
            </Text>
          )}
        </View>
        <View style={styles.effectivenessContainer}>
          <Text style={styles.effectivenessValue}>{remedy.effectiveness}%</Text>
          <Text style={styles.effectivenessLabel}>{t('effect')}</Text>
        </View>
      </View>

      {remedy.strength !== undefined && (
        <View style={styles.strengthBar}>
          <Text style={styles.strengthLabel}>
            {t('planetStrength')}: {remedy.strength}%
          </Text>
          <View style={styles.strengthBarBg}>
            <View
              style={[
                styles.strengthBarFill,
                {
                  width: `${remedy.strength}%`,
                  backgroundColor:
                    remedy.strength < 30 ? '#ef4444' : remedy.strength < 50 ? '#f59e0b' : '#22c55e',
                },
              ]}
            />
          </View>
        </View>
      )}

      <View style={styles.remediesList}>
        {remedy.remedies?.map((r, idx) => (
          <View key={idx} style={styles.remedyItem}>
            <View style={styles.remedyItemNumber}>
              <Text style={styles.remedyItemNumberText}>{idx + 1}</Text>
            </View>
            <View style={styles.remedyItemContent}>
              <Text style={styles.remedyItemText}>{language === 'ta' ? r.action_tamil || r.action : r.action}</Text>
              {r.timing && (
                <Text style={styles.remedyItemTiming}>
                  <Ionicons name="time-outline" size={12} color="#8b6f47" /> {r.timing}
                </Text>
              )}
            </View>
          </View>
        ))}
      </View>
    </Animated.View>
  );
};

const DailyRoutineCard = ({ routine, language, t }) => {
  return (
    <View style={styles.routineCard}>
      <Text style={styles.cardSectionTitle}>
        <Ionicons name="calendar-outline" size={18} color="#f97316" />{'  '}
        {t('dailySchedule')}
      </Text>

      <Text style={styles.routineSubTitle}>
        <Ionicons name="sunny-outline" size={16} color="#f59e0b" />{'  '}
        {t('morning')}
      </Text>
      {routine.morning?.map((item, idx) => (
        <View key={idx} style={styles.routineItem}>
          <Text style={styles.routineTime}>{item.time}</Text>
          <Text style={styles.routineActivity}>{language === 'ta' ? item.activity : item.activity_en}</Text>
        </View>
      ))}

      <Text style={styles.routineSubTitle}>
        <Ionicons name="moon-outline" size={16} color="#8b5cf6" />{'  '}
        {t('evening')}
      </Text>
      {routine.evening?.map((item, idx) => (
        <View key={idx} style={styles.routineItem}>
          <Text style={styles.routineTime}>{item.time}</Text>
          <Text style={styles.routineActivity}>{language === 'ta' ? item.activity : item.activity_en}</Text>
        </View>
      ))}

      {routine.weekly_special && (
        <>
          <Text style={styles.routineSubTitle}>
            <Ionicons name="star-outline" size={16} color="#f97316" />{'  '}
            {language === 'ta'
              ? `${routine.weekly_special.day} ${t('special')}`
              : `${routine.weekly_special.day_en} ${t('special')}`}
          </Text>
          {routine.weekly_special.activities?.map((activity, idx) => (
            <View key={idx} style={styles.routineItem}>
              <Text style={styles.routineActivity}>• {activity}</Text>
            </View>
          ))}
        </>
      )}
    </View>
  );
};

const LuckyItemsCard = ({ luckyItems, t }) => {
  const items = [
    { icon: 'color-palette', label: t('color'), value: luckyItems.color?.value || luckyItems.color?.value_en },
    { icon: 'diamond', label: t('gemstone'), value: luckyItems.gemstone?.value || luckyItems.gemstone?.value_en },
    { icon: 'calendar', label: t('day'), value: luckyItems.day?.value || luckyItems.day?.value_en },
    { icon: 'compass', label: t('direction'), value: luckyItems.direction?.value || luckyItems.direction?.value_en },
    { icon: 'apps', label: t('number'), value: luckyItems.number },
  ];

  return (
    <View style={styles.luckyCard}>
      <Text style={styles.cardSectionTitle}>
        <Ionicons name="sparkles" size={18} color="#f97316" />{'  '}
        {t('luckyItems')}
      </Text>
      <View style={styles.luckyItemsGrid}>
        {items.map((item, idx) => (
          <View key={idx} style={styles.luckyItem}>
            <View style={styles.luckyItemIcon}>
              <Ionicons name={item.icon} size={20} color="#f97316" />
            </View>
            <Text style={styles.luckyItemLabel}>{item.label}</Text>
            <Text style={styles.luckyItemValue}>{item.value}</Text>
          </View>
        ))}
      </View>
    </View>
  );
};

export default function RemedyScreen({ navigation }) {
  const insets = useSafeAreaInsets();
  const bottomPadding = Platform.OS === 'android' ? Math.max(insets.bottom, 80) : insets.bottom + 80;

  const { userProfile } = useAuth();
  const { t, language } = useLanguage();

  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedGoal, setSelectedGoal] = useState(null);
  const [remedyData, setRemedyData] = useState(null);
  const [error, setError] = useState(null);

  const fetchRemedies = useCallback(
    async (goal = null) => {
      try {
        setLoading(true);
        setError(null);

        if (!userProfile?.birthDate || !userProfile?.birthTime || !userProfile?.birthPlace) {
          setError(t('birthDetailsRequired'));
          setLoading(false);
          return;
        }

        const birthDetails = {
          name: userProfile.name,
          birthDate: userProfile.birthDate,
          birthTime: userProfile.birthTime,
          birthPlace: userProfile.birthPlace,
        };

        const data = await remedyAPI.getPersonalized(birthDetails, goal, language);
        setRemedyData(data);
      } catch (err) {
        console.error('Remedy API error:', err);
        setError(t('failedToLoadRemedies'));
      } finally {
        setLoading(false);
        setRefreshing(false);
      }
    },
    [language, t, userProfile],
  );

  useEffect(() => {
    fetchRemedies(selectedGoal);
  }, [fetchRemedies, selectedGoal]);

  const onRefresh = () => {
    setRefreshing(true);
    fetchRemedies(selectedGoal);
  };

  const handleGoalSelect = (goalId) => {
    setSelectedGoal(selectedGoal === goalId ? null : goalId);
  };

  return (
    <View style={styles.container}>
      <LinearGradient colors={['#faf7f2', '#f5ede5', '#fff8f0']} style={styles.gradient}>
        <ScrollView
          contentContainerStyle={[styles.scrollContent, { paddingBottom: bottomPadding }]}
          showsVerticalScrollIndicator={false}
          refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#f97316" />}
        >
          <AppHeader
            t={t}
            userProfile={userProfile}
            title={t('aiRemedyEngine')}
            subtitle={t('personalizedRemedies')}
            showBackButton
            onBackPress={() => navigation.goBack()}
          />

          <View style={styles.goalsSection}>
            <Text style={styles.goalsTitle}>{t('selectYourGoal')}</Text>
            <ScrollView
              horizontal
              showsHorizontalScrollIndicator={false}
              contentContainerStyle={styles.goalsContainer}
            >
              {GOALS.map((goal) => {
                const isActive = selectedGoal === goal.id;

                return (
                  <TouchableOpacity
                    key={goal.id}
                    style={[
                      styles.goalButton,
                      isActive && {
                        backgroundColor: `${goal.color}15`,
                        borderColor: goal.color,
                      },
                    ]}
                    onPress={() => handleGoalSelect(goal.id)}
                    activeOpacity={0.85}
                  >
                    <Ionicons name={goal.icon} size={22} color={isActive ? goal.color : '#8b6f47'} />
                    <Text style={[styles.goalLabel, isActive && { color: goal.color }]}>
                      {goal.label[language] || goal.label.en}
                    </Text>
                  </TouchableOpacity>
                );
              })}
            </ScrollView>
          </View>

          {loading ? (
            <View style={styles.loadingContainer}>
              <ActivityIndicator size="large" color="#f97316" />
              <Text style={styles.loadingText}>{t('generatingRemedies')}</Text>
            </View>
          ) : error ? (
            <View style={styles.errorContainer}>
              <Ionicons name="alert-circle" size={44} color="#ef4444" />
              <Text style={styles.errorText}>{error}</Text>
              <TouchableOpacity style={styles.retryButton} onPress={() => fetchRemedies(selectedGoal)} activeOpacity={0.9}>
                <Text style={styles.retryText}>{t('retry')}</Text>
              </TouchableOpacity>
            </View>
          ) : remedyData ? (
            <>
              <View style={styles.dashaCard}>
                <View style={styles.dashaHeader}>
                  <View style={styles.dashaIcon}>
                    <Ionicons name="planet" size={18} color="#f97316" />
                  </View>
                  <Text style={styles.dashaTitle}>{t('currentDashaLabel')}</Text>
                </View>

                <View style={styles.dashaContent}>
                  <View style={styles.dashaItem}>
                    <Text style={styles.dashaLabel}>{t('mahaDasha')}</Text>
                    <Text style={styles.dashaValue} numberOfLines={1}>
                      {language === 'en'
                        ? remedyData.current_dasha?.mahadasha_en || remedyData.current_dasha?.mahadasha
                        : remedyData.current_dasha?.mahadasha_tamil || remedyData.current_dasha?.mahadasha}
                    </Text>
                  </View>
                  <View style={styles.dashaItem}>
                    <Text style={styles.dashaLabel}>{t('remaining')}</Text>
                    <Text style={styles.dashaValue}>
                      {remedyData.current_dasha?.years_remaining} {t('years')}
                    </Text>
                  </View>
                </View>
              </View>

              {remedyData.weak_planets?.length > 0 && (
                <View style={styles.alertCard}>
                  <View style={styles.alertHeader}>
                    <Ionicons name="warning" size={18} color="#a16207" />
                    <Text style={styles.alertTitle}>{t('weakPlanets')}</Text>
                  </View>
                  <View style={styles.weakPlanetsContainer}>
                    {remedyData.weak_planets.map((planet, idx) => (
                      <View key={idx} style={styles.weakPlanetBadge}>
                        <Text style={styles.weakPlanetName}>
                          {language === 'en'
                            ? planet.planet_en || planet.planet
                            : planet.planet_tamil || planet.planet}
                        </Text>
                        <Text style={styles.weakPlanetStrength}>{planet.strength}%</Text>
                      </View>
                    ))}
                  </View>
                </View>
              )}

              {remedyData.goal_analysis && (
                <View style={styles.goalAnalysisCard}>
                  <Text style={styles.cardSectionTitle}>
                    <Ionicons name="analytics" size={18} color="#f97316" />{'  '}
                    {t('goalAnalysis')}
                  </Text>
                  <View style={styles.favorabilityContainer}>
                    <Text style={styles.favorabilityLabel}>{t('favorability')}</Text>
                    <View style={styles.favorabilityBar}>
                      <View
                        style={[
                          styles.favorabilityFill,
                          {
                            width: `${remedyData.goal_analysis.favorability}%`,
                            backgroundColor: remedyData.goal_analysis.favorability >= 60 ? '#22c55e' : '#f59e0b',
                          },
                        ]}
                      />
                    </View>
                    <Text style={styles.favorabilityValue}>{remedyData.goal_analysis.favorability}%</Text>
                  </View>
                </View>
              )}

              <Text style={styles.outerSectionTitle}>
                <Ionicons name="list" size={18} color="#f97316" />{'  '}
                {t('recommendedRemedies')}
              </Text>

              {remedyData.remedies?.map((remedy, index) => (
                <AnimatedRemedyCard
                  key={remedy.id || index}
                  remedy={remedy}
                  index={index}
                  language={language}
                  t={t}
                />
              ))}

              {remedyData.daily_routine && <DailyRoutineCard routine={remedyData.daily_routine} language={language} t={t} />}

              {remedyData.lucky_items && <LuckyItemsCard luckyItems={remedyData.lucky_items} t={t} />}
            </>
          ) : null}
        </ScrollView>
      </LinearGradient>
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
    paddingBottom: 80,
  },

  goalsSection: {
    backgroundColor: '#fff8f0',
    borderRadius: 20,
    padding: 18,
    marginHorizontal: 16,
    marginTop: 16,
    borderWidth: 1,
    borderColor: '#e8d5c4',
    shadowColor: '#d4a574',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 10,
    elevation: 2,
  },
  goalsTitle: {
    fontSize: 13,
    color: '#8b6f47',
    marginBottom: 12,
    fontWeight: '800',
    letterSpacing: 0.2,
  },
  goalsContainer: {
    gap: 10,
    paddingRight: 8,
  },
  goalButton: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 14,
    backgroundColor: '#fef6ed',
    borderWidth: 1,
    borderColor: '#e8d5c4',
    minWidth: 92,
  },
  goalLabel: {
    fontSize: 12,
    color: '#6b5644',
    marginTop: 6,
    fontWeight: '800',
  },

  loadingContainer: {
    alignItems: 'center',
    paddingVertical: 70,
    marginHorizontal: 16,
    marginTop: 18,
    backgroundColor: '#fff8f0',
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#e8d5c4',
  },
  loadingText: {
    color: '#8b6f47',
    marginTop: 16,
    fontSize: 13,
    fontWeight: '800',
  },
  errorContainer: {
    alignItems: 'center',
    paddingVertical: 60,
    marginHorizontal: 16,
    marginTop: 18,
    backgroundColor: '#fef2f2',
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#fecaca',
  },
  errorText: {
    color: '#dc2626',
    marginTop: 12,
    fontSize: 13,
    textAlign: 'center',
    fontWeight: '800',
    paddingHorizontal: 16,
  },
  retryButton: {
    marginTop: 18,
    paddingVertical: 12,
    paddingHorizontal: 24,
    backgroundColor: '#f97316',
    borderRadius: 12,
  },
  retryText: {
    color: '#fff',
    fontWeight: '900',
    letterSpacing: 0.4,
  },

  dashaCard: {
    backgroundColor: '#fff8f0',
    borderRadius: 20,
    padding: 18,
    marginHorizontal: 16,
    marginTop: 18,
    borderWidth: 1,
    borderColor: '#f4e4d7',
    shadowColor: '#d4a574',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 10,
    elevation: 2,
  },
  dashaHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    marginBottom: 14,
  },
  dashaIcon: {
    width: 34,
    height: 34,
    borderRadius: 17,
    backgroundColor: '#fff7ed',
    borderWidth: 1,
    borderColor: '#fed7aa',
    justifyContent: 'center',
    alignItems: 'center',
  },
  dashaTitle: {
    fontSize: 14,
    fontWeight: '900',
    color: '#6b5644',
    letterSpacing: 0.2,
  },
  dashaContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 14,
  },
  dashaItem: {
    flex: 1,
    backgroundColor: '#fef6ed',
    borderRadius: 14,
    borderWidth: 1,
    borderColor: '#e8d5c4',
    paddingVertical: 12,
    paddingHorizontal: 12,
    alignItems: 'center',
  },
  dashaLabel: {
    fontSize: 11,
    color: '#8b6f47',
    fontWeight: '900',
    textTransform: 'uppercase',
    letterSpacing: 0.8,
    marginBottom: 6,
  },
  dashaValue: {
    fontSize: 16,
    fontWeight: '900',
    color: '#ea580c',
  },

  alertCard: {
    backgroundColor: '#fefce8',
    borderRadius: 20,
    padding: 16,
    marginHorizontal: 16,
    marginTop: 18,
    borderWidth: 1,
    borderColor: '#fde68a',
  },
  alertHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    marginBottom: 12,
  },
  alertTitle: {
    fontSize: 13,
    fontWeight: '900',
    color: '#a16207',
    letterSpacing: 0.3,
  },
  weakPlanetsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  weakPlanetBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fffbeb',
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#fde68a',
    gap: 8,
  },
  weakPlanetName: {
    fontSize: 12,
    color: '#a16207',
    fontWeight: '900',
  },
  weakPlanetStrength: {
    fontSize: 11,
    color: '#8b6f47',
    fontWeight: '800',
  },

  goalAnalysisCard: {
    backgroundColor: '#fff8f0',
    borderRadius: 20,
    padding: 18,
    marginHorizontal: 16,
    marginTop: 18,
    borderWidth: 1,
    borderColor: '#e8d5c4',
    shadowColor: '#d4a574',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 10,
    elevation: 2,
  },
  favorabilityContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 10,
    gap: 12,
  },
  favorabilityLabel: {
    fontSize: 11,
    color: '#8b6f47',
    width: 92,
    fontWeight: '900',
    textTransform: 'uppercase',
    letterSpacing: 0.8,
  },
  favorabilityBar: {
    flex: 1,
    height: 10,
    backgroundColor: '#f4e4d7',
    borderRadius: 6,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: '#e8d5c4',
  },
  favorabilityFill: {
    height: '100%',
    borderRadius: 6,
  },
  favorabilityValue: {
    fontSize: 14,
    fontWeight: '900',
    color: '#6b5644',
    width: 50,
    textAlign: 'right',
  },

  outerSectionTitle: {
    fontSize: 14,
    fontWeight: '900',
    color: '#6b5644',
    marginTop: 22,
    marginBottom: 14,
    marginHorizontal: 16,
    letterSpacing: 0.3,
  },
  cardSectionTitle: {
    fontSize: 14,
    fontWeight: '900',
    color: '#6b5644',
    marginBottom: 14,
    letterSpacing: 0.2,
  },

  remedyCard: {
    backgroundColor: '#fff8f0',
    borderRadius: 20,
    padding: 18,
    marginHorizontal: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#e8d5c4',
    shadowColor: '#d4a574',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 10,
    elevation: 2,
  },
  remedyHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    borderLeftWidth: 4,
    paddingLeft: 12,
    marginLeft: -18,
    gap: 12,
  },
  typeIconContainer: {
    width: 44,
    height: 44,
    borderRadius: 22,
    justifyContent: 'center',
    alignItems: 'center',
  },
  remedyHeaderText: {
    flex: 1,
  },
  remedyTitle: {
    fontSize: 14,
    fontWeight: '900',
    color: '#6b5644',
    letterSpacing: 0.2,
  },
  remedyPlanet: {
    fontSize: 12,
    color: '#8b6f47',
    marginTop: 3,
    fontWeight: '800',
  },
  effectivenessContainer: {
    alignItems: 'center',
  },
  effectivenessValue: {
    fontSize: 16,
    fontWeight: '900',
    color: '#16a34a',
  },
  effectivenessLabel: {
    fontSize: 10,
    color: '#8b6f47',
    fontWeight: '900',
    textTransform: 'uppercase',
    letterSpacing: 0.8,
    marginTop: 2,
  },

  strengthBar: {
    marginTop: 16,
    marginBottom: 8,
  },
  strengthLabel: {
    fontSize: 12,
    color: '#8b6f47',
    marginBottom: 8,
    fontWeight: '800',
  },
  strengthBarBg: {
    height: 8,
    backgroundColor: '#f4e4d7',
    borderRadius: 6,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: '#e8d5c4',
  },
  strengthBarFill: {
    height: '100%',
    borderRadius: 6,
  },

  remediesList: {
    marginTop: 16,
  },
  remedyItem: {
    flexDirection: 'row',
    marginBottom: 12,
  },
  remedyItemNumber: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: '#fff7ed',
    borderWidth: 1,
    borderColor: '#fed7aa',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  remedyItemNumberText: {
    fontSize: 12,
    fontWeight: '900',
    color: '#ea580c',
  },
  remedyItemContent: {
    flex: 1,
  },
  remedyItemText: {
    fontSize: 13,
    color: '#6b5644',
    lineHeight: 20,
    fontWeight: '700',
  },
  remedyItemTiming: {
    fontSize: 11,
    color: '#8b6f47',
    marginTop: 4,
    fontWeight: '700',
  },

  routineCard: {
    backgroundColor: '#fff8f0',
    borderRadius: 20,
    padding: 18,
    marginHorizontal: 16,
    marginTop: 18,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#e8d5c4',
    shadowColor: '#d4a574',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 10,
    elevation: 2,
  },
  routineSubTitle: {
    fontSize: 13,
    fontWeight: '900',
    color: '#6b5644',
    marginTop: 16,
    marginBottom: 10,
    letterSpacing: 0.2,
  },
  routineItem: {
    flexDirection: 'row',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#e8d5c4',
  },
  routineTime: {
    fontSize: 12,
    color: '#ea580c',
    width: 90,
    fontWeight: '900',
  },
  routineActivity: {
    fontSize: 13,
    color: '#6b5644',
    flex: 1,
    fontWeight: '700',
  },

  luckyCard: {
    backgroundColor: '#fff8f0',
    borderRadius: 20,
    padding: 18,
    marginHorizontal: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#e8d5c4',
    shadowColor: '#d4a574',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 10,
    elevation: 2,
  },
  luckyItemsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
    marginTop: 8,
  },
  luckyItem: {
    alignItems: 'center',
    backgroundColor: '#fef6ed',
    borderRadius: 16,
    padding: 12,
    minWidth: 92,
    flex: 1,
    borderWidth: 1,
    borderColor: '#e8d5c4',
  },
  luckyItemIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#fff7ed',
    borderWidth: 1,
    borderColor: '#fed7aa',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
  },
  luckyItemLabel: {
    fontSize: 10,
    color: '#8b6f47',
    marginBottom: 4,
    fontWeight: '900',
    textTransform: 'uppercase',
    letterSpacing: 0.8,
    textAlign: 'center',
  },
  luckyItemValue: {
    fontSize: 13,
    fontWeight: '900',
    color: '#6b5644',
    textAlign: 'center',
  },
});
