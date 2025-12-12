import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  Platform,
  Animated,
  Easing,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { mobileAPI } from '../services/api';
import { useLanguage } from '../context/LanguageContext';

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

// Animated Event Button
const AnimatedEventButton = ({ type, isActive, onPress, delay = 0 }) => {
  const scaleAnim = useRef(new Animated.Value(0)).current;
  const pulseAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    Animated.spring(scaleAnim, {
      toValue: 1,
      friction: 6,
      tension: 80,
      delay,
      useNativeDriver: true,
    }).start();
  }, []);

  useEffect(() => {
    if (isActive) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(pulseAnim, { toValue: 1.05, duration: 500, useNativeDriver: true }),
          Animated.timing(pulseAnim, { toValue: 1, duration: 500, useNativeDriver: true }),
        ])
      ).start();
    } else {
      pulseAnim.setValue(1);
    }
  }, [isActive]);

  const handlePressIn = () => {
    Animated.spring(scaleAnim, { toValue: 0.95, useNativeDriver: true }).start();
  };

  const handlePressOut = () => {
    Animated.spring(scaleAnim, { toValue: 1, friction: 3, useNativeDriver: true }).start();
  };

  return (
    <Animated.View style={[styles.eventBtnWrapper, { transform: [{ scale: Animated.multiply(scaleAnim, pulseAnim) }] }]}>
      <TouchableOpacity
        style={[styles.eventBtn, isActive && styles.eventBtnActive]}
        onPress={onPress}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
        activeOpacity={0.9}
      >
        <View style={[styles.eventIconContainer, isActive && { backgroundColor: type.iconColor + '20' }]}>
          <Ionicons name={type.iconName} size={24} color={isActive ? type.iconColor : '#6b7280'} />
        </View>
        <Text style={[styles.eventLabel, isActive && { color: type.iconColor, fontWeight: '600' }]} numberOfLines={1}>{type.label}</Text>
      </TouchableOpacity>
    </Animated.View>
  );
};

// Animated Calendar Cell
const AnimatedCalendarCell = ({ day, isSelected, dateStyle, goodEvents, hasSelectedEvent, eventType, onPress, delay = 0, eventTypes }) => {
  const scaleAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.spring(scaleAnim, {
      toValue: 1,
      friction: 6,
      tension: 80,
      delay,
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
    <View style={styles.calendarCellWrapper}>
      <Animated.View style={[styles.calendarCellAnimated, { transform: [{ scale: scaleAnim }] }]}>
        <TouchableOpacity
          style={[
            styles.calendarCell,
            { backgroundColor: isSelected ? '#f97316' : dateStyle.bg, borderColor: isSelected ? '#f97316' : dateStyle.border }
          ]}
          onPress={onPress}
          onPressIn={handlePressIn}
          onPressOut={handlePressOut}
          activeOpacity={0.8}
        >
          <Text style={[styles.calendarDay, { color: isSelected ? '#fff' : dateStyle.text }]}>
            {day}
          </Text>
          {!isSelected && hasSelectedEvent && (
            <View style={styles.eventDot} />
          )}
        </TouchableOpacity>
      </Animated.View>
    </View>
  );
};

// Animated Time Slot
const AnimatedTimeSlot = ({ slot, index, eventTypes }) => {
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(20)).current;

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
        easing: Easing.out(Easing.ease),
      }),
    ]).start();
  }, []);

  const slotStyle = slot.type === 'excellent' ? { bg: '#f0fdf4', border: '#bbf7d0', text: '#15803d' }
    : slot.type === 'good' ? { bg: '#eff6ff', border: '#bfdbfe', text: '#2563eb' }
    : slot.type === 'avoid' ? { bg: '#fef2f2', border: '#fecaca', text: '#dc2626' }
    : slot.type === 'caution' ? { bg: '#fff7ed', border: '#fed7aa', text: '#ea580c' }
    : { bg: '#f9fafb', border: '#e5e7eb', text: '#6b7280' };

  return (
    <Animated.View style={{ opacity: fadeAnim, transform: [{ translateX: slideAnim }] }}>
      <View style={[styles.timeSlot, { backgroundColor: slotStyle.bg, borderColor: slotStyle.border }]}>
        <View>
          <Text style={styles.timeSlotTime}>{slot.time}</Text>
          <Text style={[styles.timeSlotLabel, { color: slotStyle.text }]}>{slot.label}</Text>
        </View>
        {slot.type !== 'avoid' && slot.type !== 'caution' && (
          <Text style={[styles.timeSlotScore, { color: slotStyle.text }]}>{slot.score}%</Text>
        )}
        {slot.type === 'excellent' && <Ionicons name="checkmark-circle" size={20} color="#16a34a" />}
        {(slot.type === 'avoid' || slot.type === 'caution') && <Ionicons name="alert-circle" size={20} color={slotStyle.text} />}
      </View>
    </Animated.View>
  );
};

// Pulsing Calendar Icon
const PulsingCalendarIcon = () => {
  const scaleAnim = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(scaleAnim, { toValue: 1.1, duration: 1000, useNativeDriver: true }),
        Animated.timing(scaleAnim, { toValue: 1, duration: 1000, useNativeDriver: true }),
      ])
    ).start();
  }, []);

  return (
    <Animated.View style={{ transform: [{ scale: scaleAnim }] }}>
      <Ionicons name="calendar-outline" size={48} color="#fed7aa" />
    </Animated.View>
  );
};

// Event type IDs for translation lookup - using Ionicons instead of emojis
const eventTypeIds = [
  { id: 'marriage', iconName: 'heart', iconColor: '#ec4899', labelKey: 'marriage' },
  { id: 'griha_pravesam', iconName: 'home', iconColor: '#f59e0b', labelKey: 'housewarming' },
  { id: 'vehicle', iconName: 'car', iconColor: '#3b82f6', labelKey: 'vehicle' },
  { id: 'business', iconName: 'briefcase', iconColor: '#6366f1', labelKey: 'business' },
  { id: 'travel', iconName: 'airplane', iconColor: '#06b6d4', labelKey: 'travel' },
  { id: 'general', iconName: 'star', iconColor: '#f97316', labelKey: 'general' },
];

export default function MuhurthamScreen() {
  const insets = useSafeAreaInsets();
  const bottomPadding = Platform.OS === 'android' ? Math.max(insets.bottom, 80) : insets.bottom + 80;
  const { t, getMonthName, getShortDayName, language } = useLanguage();

  // language is already 'ta', 'en', or 'kn' from LanguageContext
  const apiLang = language;

  // Build translated event types
  const eventTypes = eventTypeIds.map(et => ({
    ...et,
    label: t(et.labelKey)
  }));

  const [eventType, setEventType] = useState('general');
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState(null);
  const [calendarData, setCalendarData] = useState([]);
  const [dayDetails, setDayDetails] = useState(null);
  const [loadingCalendar, setLoadingCalendar] = useState(true);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const [error, setError] = useState(null);

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
    fetchCalendar();
    setSelectedDate(null);
    setDayDetails(null);
  }, [currentMonth, apiLang]);

  const fetchCalendar = async () => {
    setLoadingCalendar(true);
    setError(null);
    try {
      const month = currentMonth.getMonth() + 1;
      const year = currentMonth.getFullYear();
      const data = await mobileAPI.getMuhurthamCalendar(month, year, apiLang);
      setCalendarData(data || []);
    } catch (err) {
      console.error('Failed to fetch calendar:', err);
      setError(t('calendarLoadError'));
      setCalendarData([]);
    } finally {
      setLoadingCalendar(false);
    }
  };

  useEffect(() => {
    const fetchDayDetails = async () => {
      if (!selectedDate) return;

      setLoadingDetails(true);
      try {
        const dateStr = `${currentMonth.getFullYear()}-${String(currentMonth.getMonth() + 1).padStart(2, '0')}-${String(selectedDate).padStart(2, '0')}`;
        const data = await mobileAPI.getMuhurthamDayDetails(dateStr, apiLang);
        setDayDetails(data);
      } catch (err) {
        console.error('Failed to fetch day details:', err);
        setDayDetails(null);
      } finally {
        setLoadingDetails(false);
      }
    };

    fetchDayDetails();
  }, [selectedDate, currentMonth, apiLang]);

  const getDaysInMonth = (date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    return { firstDay, daysInMonth };
  };

  const { firstDay, daysInMonth } = getDaysInMonth(currentMonth);

  const prevMonth = () => {
    setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1));
  };

  const nextMonth = () => {
    setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1));
  };

  const getDayData = (day) => {
    const dayData = calendarData.find(d => {
      const date = new Date(d.date);
      return date.getDate() === day;
    });
    return dayData || null;
  };

  const getDateStyle = (day) => {
    const dayData = getDayData(day);
    if (!dayData) return { bg: '#fff', border: '#e5e7eb', text: '#374151' };

    const score = dayData.event_scores?.[eventType] ?? dayData.day_score;

    if (score >= 70) return { bg: '#f0fdf4', border: '#bbf7d0', text: '#15803d' };
    if (score >= 50) return { bg: '#fefce8', border: '#fef08a', text: '#a16207' };
    if (score < 40) return { bg: '#fef2f2', border: '#fecaca', text: '#dc2626' };
    return { bg: '#fff', border: '#e5e7eb', text: '#374151' };
  };

  const getGoodEventsForDay = (day) => {
    const dayData = getDayData(day);
    if (!dayData || !dayData.good_for_events) return [];
    return dayData.good_for_events;
  };

  return (
    <View style={styles.container}>
      <LinearGradient colors={['#fff7ed', '#ffffff', '#fff7ed']} style={styles.gradient}>
        <ScrollView contentContainerStyle={[styles.scrollContent, { paddingBottom: bottomPadding }]}>
          {/* Header Bar */}
          <LinearGradient
            colors={['#16a34a', '#22c55e', '#16a34a']}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 0 }}
            style={styles.headerBar}
          />

          {/* Header */}
          <Animated.View style={[styles.header, { opacity: headerFadeAnim, transform: [{ translateY: headerSlideAnim }] }]}>
            <View style={styles.headerRow}>
              <Ionicons name="calendar" size={20} color="#16a34a" />
              <Text style={styles.headerTitle}>{t('muhurthamFinder')}</Text>
            </View>
            <Text style={styles.headerSubtitle}>{t('auspiciousTime')}</Text>
          </Animated.View>

          {/* Event Type Selector */}
          <AnimatedCard delay={100} style={styles.card}>
            <View style={styles.cardHeader}>
              <Ionicons name="star" size={16} color="#ea580c" />
              <Text style={styles.cardTitle}>{t('eventType')}</Text>
            </View>
            <View style={styles.eventGrid}>
              {eventTypes.map((type, index) => (
                <AnimatedEventButton
                  key={type.id}
                  type={type}
                  isActive={eventType === type.id}
                  onPress={() => setEventType(type.id)}
                  delay={index * 50}
                />
              ))}
            </View>
          </AnimatedCard>

          {/* Error Display */}
          {error && (
            <View style={styles.errorBox}>
              <Ionicons name="alert-circle" size={16} color="#dc2626" />
              <Text style={styles.errorText}>{error}</Text>
            </View>
          )}

          {/* Calendar */}
          <AnimatedCard delay={200} style={styles.card}>
            <View style={styles.monthNav}>
              <TouchableOpacity onPress={prevMonth} style={styles.navBtn}>
                <Ionicons name="chevron-back" size={20} color="#6b7280" />
              </TouchableOpacity>
              <Text style={styles.monthTitle}>
                {getMonthName(currentMonth.getMonth())} {currentMonth.getFullYear()}
              </Text>
              <TouchableOpacity onPress={nextMonth} style={styles.navBtn}>
                <Ionicons name="chevron-forward" size={20} color="#6b7280" />
              </TouchableOpacity>
            </View>

            {/* Day Headers */}
            <View style={styles.dayHeaderRow}>
              {[0, 1, 2, 3, 4, 5, 6].map((i) => (
                <Text key={i} style={[styles.dayHeader, i === 0 && styles.sundayHeader]}>
                  {getShortDayName(i)}
                </Text>
              ))}
            </View>

            {loadingCalendar ? (
              <View style={styles.loadingContainer}>
                <ActivityIndicator size="large" color="#f97316" />
              </View>
            ) : (
              <View style={styles.calendarGrid}>
                {/* Empty cells for days before the first day */}
                {[...Array(firstDay)].map((_, i) => (
                  <View key={`empty-${i}`} style={styles.emptyCell} />
                ))}

                {/* Days of the month */}
                {[...Array(daysInMonth)].map((_, i) => {
                  const day = i + 1;
                  const isSelected = selectedDate === day;
                  const dateStyle = getDateStyle(day);
                  const goodEvents = getGoodEventsForDay(day);
                  const hasSelectedEvent = goodEvents.some(e => e.type === eventType);

                  return (
                    <AnimatedCalendarCell
                      key={day}
                      day={day}
                      isSelected={isSelected}
                      dateStyle={dateStyle}
                      goodEvents={goodEvents}
                      hasSelectedEvent={hasSelectedEvent}
                      eventType={eventType}
                      onPress={() => setSelectedDate(day)}
                      delay={(firstDay + i) * 15}
                      eventTypes={eventTypes}
                    />
                  );
                })}
              </View>
            )}

            {/* Legend */}
            <View style={styles.legendRow}>
              <View style={styles.legendItem}>
                <View style={[styles.legendDot, { backgroundColor: '#f0fdf4', borderColor: '#bbf7d0' }]} />
                <Text style={styles.legendText}>{t('goodDay')}</Text>
              </View>
              <View style={styles.legendItem}>
                <View style={[styles.legendDot, { backgroundColor: '#fefce8', borderColor: '#fef08a' }]} />
                <Text style={styles.legendText}>{t('normalDay')}</Text>
              </View>
              <View style={styles.legendItem}>
                <View style={[styles.legendDot, { backgroundColor: '#fef2f2', borderColor: '#fecaca' }]} />
                <Text style={styles.legendText}>{t('avoidDay')}</Text>
              </View>
            </View>
          </AnimatedCard>

          {/* Day Details */}
          {selectedDate && (
            <AnimatedCard delay={300} style={styles.card}>
              <View style={styles.cardHeader}>
                <Ionicons name="time" size={16} color="#ea580c" />
                <Text style={styles.cardTitle}>
                  {selectedDate} {getMonthName(currentMonth.getMonth())} - {t('bestTimes')}
                </Text>
              </View>

              {loadingDetails ? (
                <View style={styles.loadingContainer}>
                  <ActivityIndicator size="small" color="#f97316" />
                </View>
              ) : dayDetails ? (
                <View>
                  {/* Good Events */}
                  {dayDetails.good_for_events?.length > 0 && (
                    <View style={styles.goodEventsBox}>
                      <View style={styles.goodEventsTitleRow}>
                        <Ionicons name="checkmark-circle" size={14} color="#15803d" />
                        <Text style={styles.goodEventsTitle}>{t('todayGoodFor')}:</Text>
                      </View>
                      <View style={styles.goodEventsList}>
                        {dayDetails.good_for_events.map((evt, i) => {
                          const eventConfig = eventTypes.find(e => e.id === evt.type);
                          return (
                            <View key={i} style={styles.goodEventItem}>
                              <Ionicons name={eventConfig?.iconName || 'star'} size={14} color={eventConfig?.iconColor || '#16a34a'} />
                              <Text style={styles.goodEventLabel}>{evt.label || evt.tamil}</Text>
                              <Text style={styles.goodEventScore}>{evt.score}%</Text>
                            </View>
                          );
                        })}
                      </View>
                    </View>
                  )}

                  {/* Panchangam */}
                  <View style={styles.panchangamBox}>
                    <View style={styles.panchangamRow}>
                      <View style={styles.panchangamItem}>
                        <Text style={styles.panchangamLabel}>{t('tithi')}</Text>
                        <Text style={styles.panchangamValue}>{dayDetails.panchangam?.tithi?.name || '-'}</Text>
                      </View>
                      <View style={styles.panchangamItem}>
                        <Text style={styles.panchangamLabel}>{t('nakshatra')}</Text>
                        <Text style={styles.panchangamValue}>{dayDetails.panchangam?.nakshatra?.name || '-'}</Text>
                      </View>
                    </View>
                    <View style={styles.panchangamRow}>
                      <View style={styles.panchangamItem}>
                        <Text style={styles.panchangamLabel}>{t('yoga')}</Text>
                        <Text style={styles.panchangamValue}>{dayDetails.panchangam?.yoga?.name || '-'}</Text>
                      </View>
                      <View style={styles.panchangamItem}>
                        <Text style={styles.panchangamLabel}>{t('weekday')}</Text>
                        <Text style={styles.panchangamValue}>{dayDetails.panchangam?.vaaram || '-'}</Text>
                      </View>
                    </View>
                  </View>

                  {/* Time Slots */}
                  {dayDetails.time_slots?.length > 0 && (
                    <View style={styles.timeSlotsContainer}>
                      {dayDetails.time_slots.map((slot, i) => (
                        <AnimatedTimeSlot
                          key={i}
                          slot={slot}
                          index={i}
                          eventTypes={eventTypes}
                        />
                      ))}
                    </View>
                  )}

                  {/* Recommendation */}
                  {dayDetails.recommendation && (
                    <View style={styles.recommendationBox}>
                      <Ionicons name="sparkles" size={14} color="#ea580c" />
                      <View style={{ flex: 1 }}>
                        <Text style={styles.recommendationTitle}>{t('aiRecommendation')}</Text>
                        <Text style={styles.recommendationText}>{dayDetails.recommendation}</Text>
                      </View>
                    </View>
                  )}
                </View>
              ) : (
                <View style={styles.noDataContainer}>
                  <Text style={styles.noDataText}>{t('noDataAvailable')}</Text>
                </View>
              )}
            </AnimatedCard>
          )}

          {/* Select Date Prompt */}
          {!selectedDate && (
            <AnimatedCard delay={300} style={styles.promptCard}>
              <PulsingCalendarIcon />
              <Text style={styles.promptTitle}>{t('selectDate')}</Text>
              <Text style={styles.promptSubtitle}>{t('viewBestTimes')}</Text>
            </AnimatedCard>
          )}
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
  headerRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#15803d',
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
    flex: 1,
  },
  eventGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 10,
  },
  eventBtnWrapper: {
    width: '31%',
  },
  eventBtn: {
    padding: 12,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f9fafb',
    borderWidth: 1,
    borderColor: '#e5e7eb',
    minHeight: 80,
  },
  eventBtnActive: {
    backgroundColor: '#fff7ed',
    borderColor: '#f97316',
  },
  eventIconContainer: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: '#f3f4f6',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 6,
  },
  eventLabel: {
    fontSize: 10,
    color: '#374151',
    textAlign: 'center',
  },
  errorBox: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginHorizontal: 16,
    marginTop: 16,
    padding: 12,
    backgroundColor: '#fef2f2',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#fecaca',
  },
  errorText: {
    flex: 1,
    color: '#dc2626',
    fontSize: 13,
  },
  monthNav: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  navBtn: {
    padding: 8,
  },
  monthTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#374151',
  },
  dayHeaderRow: {
    flexDirection: 'row',
    marginBottom: 8,
  },
  dayHeader: {
    flex: 1,
    textAlign: 'center',
    fontSize: 11,
    fontWeight: '500',
    color: '#6b7280',
    paddingVertical: 8,
  },
  sundayHeader: {
    color: '#dc2626',
  },
  loadingContainer: {
    padding: 40,
    alignItems: 'center',
  },
  calendarGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  emptyCell: {
    width: '14.28%',
    height: 44,
  },
  calendarCellWrapper: {
    width: '14.28%',
    height: 44,
    padding: 2,
  },
  calendarCellAnimated: {
    flex: 1,
    width: '100%',
    height: '100%',
  },
  calendarCell: {
    flex: 1,
    width: '100%',
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 8,
    borderWidth: 1,
  },
  calendarDay: {
    fontSize: 15,
    fontWeight: '600',
    textAlign: 'center',
    includeFontPadding: false,
  },
  eventIconsRow: {
    flexDirection: 'row',
    position: 'absolute',
    bottom: 2,
    gap: 1,
  },
  eventMiniIcon: {
    fontSize: 6,
    opacity: 0.7,
  },
  eventMiniIconActive: {
    opacity: 1,
  },
  eventDot: {
    position: 'absolute',
    top: 3,
    right: 3,
    width: 5,
    height: 5,
    borderRadius: 2.5,
    backgroundColor: '#16a34a',
  },
  legendRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    gap: 16,
    marginTop: 16,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  legendDot: {
    width: 12,
    height: 12,
    borderRadius: 4,
    borderWidth: 1,
  },
  legendText: {
    fontSize: 10,
    color: '#6b7280',
  },
  goodEventsBox: {
    padding: 12,
    backgroundColor: '#f0fdf4',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#bbf7d0',
    marginBottom: 12,
  },
  goodEventsTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginBottom: 8,
  },
  goodEventsTitle: {
    fontSize: 12,
    fontWeight: '500',
    color: '#15803d',
  },
  goodEventsList: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  goodEventItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    paddingHorizontal: 8,
    paddingVertical: 4,
    backgroundColor: '#fff',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#bbf7d0',
  },
  goodEventLabel: {
    fontSize: 11,
    color: '#374151',
  },
  goodEventScore: {
    fontSize: 11,
    fontWeight: '600',
    color: '#16a34a',
  },
  panchangamBox: {
    padding: 12,
    backgroundColor: '#fff7ed',
    borderRadius: 12,
    marginBottom: 12,
  },
  panchangamRow: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 8,
  },
  panchangamItem: {
    flex: 1,
  },
  panchangamLabel: {
    fontSize: 10,
    color: '#6b7280',
  },
  panchangamValue: {
    fontSize: 12,
    fontWeight: '600',
    color: '#374151',
    marginTop: 2,
  },
  timeSlotsContainer: {
    gap: 8,
  },
  timeSlot: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 12,
    borderRadius: 12,
    borderWidth: 1,
  },
  timeSlotTime: {
    fontSize: 13,
    fontWeight: '600',
    color: '#374151',
  },
  timeSlotLabel: {
    fontSize: 11,
    marginTop: 2,
  },
  timeSlotScore: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  recommendationBox: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 8,
    marginTop: 12,
    padding: 12,
    backgroundColor: '#fff7ed',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#fed7aa',
  },
  recommendationTitle: {
    fontSize: 12,
    fontWeight: '600',
    color: '#9a3412',
  },
  recommendationText: {
    fontSize: 11,
    color: '#6b7280',
    marginTop: 4,
    lineHeight: 16,
  },
  noDataContainer: {
    padding: 24,
    alignItems: 'center',
  },
  noDataText: {
    fontSize: 13,
    color: '#9ca3af',
  },
  promptCard: {
    alignItems: 'center',
    padding: 32,
    marginHorizontal: 16,
    marginTop: 16,
    backgroundColor: '#fff7ed',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#fed7aa',
  },
  promptTitle: {
    fontSize: 14,
    color: '#6b7280',
    marginTop: 12,
  },
  promptSubtitle: {
    fontSize: 12,
    color: '#9ca3af',
    marginTop: 4,
  },
});
