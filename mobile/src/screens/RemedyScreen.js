import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Animated,
  Platform,
  RefreshControl,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
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

// Animated card component
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
  }, []);

  const getTypeIcon = (type) => {
    switch (type) {
      case 'dasha_remedy': return 'planet';
      case 'weak_planet_remedy': return 'trending-up';
      case 'dosha_remedy': return 'shield';
      case 'goal_remedy': return 'flag';
      default: return 'star';
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'dasha_remedy': return '#f97316';
      case 'weak_planet_remedy': return '#3b82f6';
      case 'dosha_remedy': return '#ef4444';
      case 'goal_remedy': return '#22c55e';
      default: return '#8b5cf6';
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
        <View style={[styles.typeIconContainer, { backgroundColor: getTypeColor(remedy.type) + '20' }]}>
          <Ionicons name={getTypeIcon(remedy.type)} size={24} color={getTypeColor(remedy.type)} />
        </View>
        <View style={styles.remedyHeaderText}>
          <Text style={styles.remedyTitle}>
            {language === 'ta' ? remedy.title_tamil : remedy.title}
          </Text>
          {(remedy.planet_tamil || remedy.planet) && (
            <Text style={styles.remedyPlanet}>
              {language === 'en' ? remedy.planet : remedy.planet_tamil} • {t('priority')}: {remedy.priority}
            </Text>
          )}
        </View>
        <View style={styles.effectivenessContainer}>
          <Text style={styles.effectivenessValue}>{remedy.effectiveness}%</Text>
          <Text style={styles.effectivenessLabel}>
            {t('effect')}
          </Text>
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
                  backgroundColor: remedy.strength < 30 ? '#ef4444' : remedy.strength < 50 ? '#f59e0b' : '#22c55e',
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
              <Text style={styles.remedyItemText}>
                {language === 'ta' ? (r.action_tamil || r.action) : r.action}
              </Text>
              {r.timing && (
                <Text style={styles.remedyItemTiming}>
                  <Ionicons name="time-outline" size={12} color="#9ca3af" /> {r.timing}
                </Text>
              )}
            </View>
          </View>
        ))}
      </View>
    </Animated.View>
  );
};

// Daily routine component
const DailyRoutineCard = ({ routine, language, t }) => {
  return (
    <View style={styles.routineCard}>
      <Text style={styles.sectionTitle}>
        <Ionicons name="calendar-outline" size={20} color="#f97316" />
        {'  '}
        {t('dailySchedule')}
      </Text>

      <Text style={styles.routineSubTitle}>
        <Ionicons name="sunny-outline" size={16} color="#f59e0b" />
        {'  '}
        {t('morning')}
      </Text>
      {routine.morning?.map((item, idx) => (
        <View key={idx} style={styles.routineItem}>
          <Text style={styles.routineTime}>{item.time}</Text>
          <Text style={styles.routineActivity}>
            {language === 'ta' ? item.activity : item.activity_en}
          </Text>
        </View>
      ))}

      <Text style={styles.routineSubTitle}>
        <Ionicons name="moon-outline" size={16} color="#8b5cf6" />
        {'  '}
        {t('evening')}
      </Text>
      {routine.evening?.map((item, idx) => (
        <View key={idx} style={styles.routineItem}>
          <Text style={styles.routineTime}>{item.time}</Text>
          <Text style={styles.routineActivity}>
            {language === 'ta' ? item.activity : item.activity_en}
          </Text>
        </View>
      ))}

      {routine.weekly_special && (
        <>
          <Text style={styles.routineSubTitle}>
            <Ionicons name="star-outline" size={16} color="#f97316" />
            {'  '}
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

// Lucky items component
const LuckyItemsCard = ({ luckyItems, language, t }) => {
  const items = [
    { icon: 'color-palette', label: t('color'), value: luckyItems.color?.value || luckyItems.color?.value_en },
    { icon: 'diamond', label: t('gemstone'), value: luckyItems.gemstone?.value || luckyItems.gemstone?.value_en },
    { icon: 'calendar', label: t('day'), value: luckyItems.day?.value || luckyItems.day?.value_en },
    { icon: 'compass', label: t('direction'), value: luckyItems.direction?.value || luckyItems.direction?.value_en },
    { icon: 'apps', label: t('number'), value: luckyItems.number },
  ];

  return (
    <View style={styles.luckyCard}>
      <Text style={styles.sectionTitle}>
        <Ionicons name="sparkles" size={20} color="#f97316" />
        {'  '}
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
  const { userProfile } = useAuth();
  const { t, language } = useLanguage();
  const insets = useSafeAreaInsets();

  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedGoal, setSelectedGoal] = useState(null);
  const [remedyData, setRemedyData] = useState(null);
  const [error, setError] = useState(null);

  const fetchRemedies = async (goal = null) => {
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
  };

  useEffect(() => {
    fetchRemedies(selectedGoal);
  }, [selectedGoal, language]);

  const onRefresh = () => {
    setRefreshing(true);
    fetchRemedies(selectedGoal);
  };

  const handleGoalSelect = (goalId) => {
    setSelectedGoal(selectedGoal === goalId ? null : goalId);
  };

  return (
    <View style={[styles.container, { paddingTop: insets.top }]}>
      <LinearGradient
        colors={['#1a1a2e', '#16213e', '#0f3460']}
        style={styles.headerGradient}
      >
        <View style={styles.header}>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => navigation.goBack()}
          >
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>
          <View style={styles.headerTitleContainer}>
            <Text style={styles.headerTitle}>
              {t('aiRemedyEngine')}
            </Text>
            <Text style={styles.headerSubtitle}>
              {t('personalizedRemedies')}
            </Text>
          </View>
          <View style={styles.headerRight}>
            <Ionicons name="sparkles" size={28} color="#f97316" />
          </View>
        </View>
      </LinearGradient>

      <ScrollView
        style={styles.content}
        contentContainerStyle={styles.contentContainer}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#f97316" />
        }
      >
        {/* Goal Selection */}
        <View style={styles.goalsSection}>
          <Text style={styles.goalsTitle}>
            {t('selectYourGoal')}
          </Text>
          <ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
            contentContainerStyle={styles.goalsContainer}
          >
            {GOALS.map((goal) => (
              <TouchableOpacity
                key={goal.id}
                style={[
                  styles.goalButton,
                  selectedGoal === goal.id && { backgroundColor: goal.color + '30', borderColor: goal.color },
                ]}
                onPress={() => handleGoalSelect(goal.id)}
              >
                <Ionicons
                  name={goal.icon}
                  size={24}
                  color={selectedGoal === goal.id ? goal.color : '#9ca3af'}
                />
                <Text
                  style={[
                    styles.goalLabel,
                    selectedGoal === goal.id && { color: goal.color },
                  ]}
                >
                  {goal.label[language] || goal.label.en}
                </Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>

        {loading ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#f97316" />
            <Text style={styles.loadingText}>
              {t('generatingRemedies')}
            </Text>
          </View>
        ) : error ? (
          <View style={styles.errorContainer}>
            <Ionicons name="alert-circle" size={48} color="#ef4444" />
            <Text style={styles.errorText}>{error}</Text>
            <TouchableOpacity style={styles.retryButton} onPress={() => fetchRemedies(selectedGoal)}>
              <Text style={styles.retryText}>
                {t('retry')}
              </Text>
            </TouchableOpacity>
          </View>
        ) : remedyData ? (
          <>
            {/* Current Dasha Info */}
            <View style={styles.dashaCard}>
              <View style={styles.dashaHeader}>
                <Ionicons name="planet" size={24} color="#f97316" />
                <Text style={styles.dashaTitle}>
                  {t('currentDashaLabel')}
                </Text>
              </View>
              <View style={styles.dashaContent}>
                <View style={styles.dashaItem}>
                  <Text style={styles.dashaLabel}>
                    {t('mahaDasha')}
                  </Text>
                  <Text style={styles.dashaValue}>
                    {language === 'en' ? (remedyData.current_dasha?.mahadasha_en || remedyData.current_dasha?.mahadasha) : (remedyData.current_dasha?.mahadasha_tamil || remedyData.current_dasha?.mahadasha)}
                  </Text>
                </View>
                <View style={styles.dashaItem}>
                  <Text style={styles.dashaLabel}>
                    {t('remaining')}
                  </Text>
                  <Text style={styles.dashaValue}>
                    {remedyData.current_dasha?.years_remaining} {t('years')}
                  </Text>
                </View>
              </View>
            </View>

            {/* Weak Planets Alert */}
            {remedyData.weak_planets?.length > 0 && (
              <View style={styles.alertCard}>
                <View style={styles.alertHeader}>
                  <Ionicons name="warning" size={20} color="#f59e0b" />
                  <Text style={styles.alertTitle}>
                    {t('weakPlanets')}
                  </Text>
                </View>
                <View style={styles.weakPlanetsContainer}>
                  {remedyData.weak_planets.map((planet, idx) => (
                    <View key={idx} style={styles.weakPlanetBadge}>
                      <Text style={styles.weakPlanetName}>{language === 'en' ? (planet.planet_en || planet.planet) : (planet.planet_tamil || planet.planet)}</Text>
                      <Text style={styles.weakPlanetStrength}>{planet.strength}%</Text>
                    </View>
                  ))}
                </View>
              </View>
            )}

            {/* Goal Analysis */}
            {remedyData.goal_analysis && (
              <View style={styles.goalAnalysisCard}>
                <Text style={styles.sectionTitle}>
                  <Ionicons name="analytics" size={20} color="#f97316" />
                  {'  '}
                  {t('goalAnalysis')}
                </Text>
                <View style={styles.favorabilityContainer}>
                  <Text style={styles.favorabilityLabel}>
                    {t('favorability')}
                  </Text>
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
                  <Text style={styles.favorabilityValue}>
                    {remedyData.goal_analysis.favorability}%
                  </Text>
                </View>
              </View>
            )}

            {/* Remedies List */}
            <Text style={styles.sectionTitle}>
              <Ionicons name="list" size={20} color="#f97316" />
              {'  '}
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

            {/* Daily Routine */}
            {remedyData.daily_routine && (
              <DailyRoutineCard routine={remedyData.daily_routine} language={language} t={t} />
            )}

            {/* Lucky Items */}
            {remedyData.lucky_items && (
              <LuckyItemsCard luckyItems={remedyData.lucky_items} language={language} t={t} />
            )}
          </>
        ) : null}

        {/* Bottom padding for tab bar */}
        <View style={{ height: Platform.OS === 'web' ? 80 : 100 }} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0a1a',
  },
  headerGradient: {
    paddingBottom: 16,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingTop: 8,
  },
  backButton: {
    width: 40,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },
  headerTitleContainer: {
    flex: 1,
    marginLeft: 8,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#fff',
  },
  headerSubtitle: {
    fontSize: 12,
    color: '#9ca3af',
    marginTop: 2,
  },
  headerRight: {
    width: 40,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    flex: 1,
  },
  contentContainer: {
    padding: 16,
  },
  goalsSection: {
    marginBottom: 20,
  },
  goalsTitle: {
    fontSize: 14,
    color: '#9ca3af',
    marginBottom: 12,
  },
  goalsContainer: {
    gap: 10,
  },
  goalButton: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 12,
    backgroundColor: '#1a1a2e',
    borderWidth: 1,
    borderColor: '#2a2a4e',
    minWidth: 80,
  },
  goalLabel: {
    fontSize: 12,
    color: '#9ca3af',
    marginTop: 6,
  },
  loadingContainer: {
    alignItems: 'center',
    paddingVertical: 60,
  },
  loadingText: {
    color: '#9ca3af',
    marginTop: 16,
    fontSize: 14,
  },
  errorContainer: {
    alignItems: 'center',
    paddingVertical: 60,
  },
  errorText: {
    color: '#ef4444',
    marginTop: 16,
    fontSize: 14,
    textAlign: 'center',
  },
  retryButton: {
    marginTop: 20,
    paddingVertical: 12,
    paddingHorizontal: 24,
    backgroundColor: '#f97316',
    borderRadius: 8,
  },
  retryText: {
    color: '#fff',
    fontWeight: '600',
  },
  dashaCard: {
    backgroundColor: '#1a1a2e',
    borderRadius: 16,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#f9731630',
  },
  dashaHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    marginBottom: 16,
  },
  dashaTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
  },
  dashaContent: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  dashaItem: {
    alignItems: 'center',
  },
  dashaLabel: {
    fontSize: 12,
    color: '#9ca3af',
    marginBottom: 4,
  },
  dashaValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#f97316',
  },
  alertCard: {
    backgroundColor: '#1a1a2e',
    borderRadius: 12,
    padding: 12,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#f59e0b30',
  },
  alertHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 10,
  },
  alertTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#f59e0b',
  },
  weakPlanetsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  weakPlanetBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f59e0b20',
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 20,
    gap: 6,
  },
  weakPlanetName: {
    fontSize: 12,
    color: '#f59e0b',
    fontWeight: '500',
  },
  weakPlanetStrength: {
    fontSize: 10,
    color: '#9ca3af',
  },
  goalAnalysisCard: {
    backgroundColor: '#1a1a2e',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  favorabilityContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 12,
    gap: 12,
  },
  favorabilityLabel: {
    fontSize: 12,
    color: '#9ca3af',
    width: 80,
  },
  favorabilityBar: {
    flex: 1,
    height: 8,
    backgroundColor: '#2a2a4e',
    borderRadius: 4,
    overflow: 'hidden',
  },
  favorabilityFill: {
    height: '100%',
    borderRadius: 4,
  },
  favorabilityValue: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#fff',
    width: 45,
    textAlign: 'right',
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
    marginBottom: 16,
    marginTop: 8,
  },
  remedyCard: {
    backgroundColor: '#1a1a2e',
    borderRadius: 16,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#2a2a4e',
  },
  remedyHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    borderLeftWidth: 4,
    paddingLeft: 12,
    marginLeft: -16,
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
    fontWeight: '600',
    color: '#fff',
  },
  remedyPlanet: {
    fontSize: 12,
    color: '#9ca3af',
    marginTop: 2,
  },
  effectivenessContainer: {
    alignItems: 'center',
  },
  effectivenessValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#22c55e',
  },
  effectivenessLabel: {
    fontSize: 10,
    color: '#9ca3af',
  },
  strengthBar: {
    marginTop: 16,
    marginBottom: 8,
  },
  strengthLabel: {
    fontSize: 12,
    color: '#9ca3af',
    marginBottom: 6,
  },
  strengthBarBg: {
    height: 6,
    backgroundColor: '#2a2a4e',
    borderRadius: 3,
    overflow: 'hidden',
  },
  strengthBarFill: {
    height: '100%',
    borderRadius: 3,
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
    backgroundColor: '#f9731630',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  remedyItemNumberText: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#f97316',
  },
  remedyItemContent: {
    flex: 1,
  },
  remedyItemText: {
    fontSize: 13,
    color: '#d1d5db',
    lineHeight: 20,
  },
  remedyItemTiming: {
    fontSize: 11,
    color: '#9ca3af',
    marginTop: 4,
  },
  routineCard: {
    backgroundColor: '#1a1a2e',
    borderRadius: 16,
    padding: 16,
    marginTop: 8,
    marginBottom: 16,
  },
  routineSubTitle: {
    fontSize: 14,
    fontWeight: '500',
    color: '#d1d5db',
    marginTop: 16,
    marginBottom: 8,
  },
  routineItem: {
    flexDirection: 'row',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#2a2a4e',
  },
  routineTime: {
    fontSize: 12,
    color: '#f97316',
    width: 90,
    fontWeight: '500',
  },
  routineActivity: {
    fontSize: 13,
    color: '#d1d5db',
    flex: 1,
  },
  luckyCard: {
    backgroundColor: '#1a1a2e',
    borderRadius: 16,
    padding: 16,
    marginBottom: 16,
  },
  luckyItemsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
    marginTop: 8,
  },
  luckyItem: {
    alignItems: 'center',
    backgroundColor: '#0a0a1a',
    borderRadius: 12,
    padding: 12,
    minWidth: 80,
    flex: 1,
  },
  luckyItemIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#f9731620',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
  },
  luckyItemLabel: {
    fontSize: 11,
    color: '#9ca3af',
    marginBottom: 4,
  },
  luckyItemValue: {
    fontSize: 13,
    fontWeight: '600',
    color: '#fff',
    textAlign: 'center',
  },
});
