import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Animated, Easing, Platform, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import Svg, { Circle, Path } from 'react-native-svg';

export default function AppHeader({
  t,
  userProfile,
  title,
  subtitle,
  showTime = true,
  showBackButton = false,
  onBackPress,
}) {
  const insets = useSafeAreaInsets();
  const [now, setNow] = useState(() => new Date());

  const headerFadeAnim = useRef(new Animated.Value(0)).current;
  const headerSlideAnim = useRef(new Animated.Value(-20)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(headerFadeAnim, {
        toValue: 1,
        duration: 600,
        useNativeDriver: true,
      }),
      Animated.timing(headerSlideAnim, {
        toValue: 0,
        duration: 600,
        useNativeDriver: true,
        easing: Easing.out(Easing.ease),
      }),
    ]).start();
  }, [headerFadeAnim, headerSlideAnim]);

  useEffect(() => {
    if (!showTime) return undefined;
    const id = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(id);
  }, [showTime]);

  const appTitle = useMemo(() => {
    try {
      return t?.('appName') || 'Jothida AI';
    } catch {
      return 'Jothida AI';
    }
  }, [t]);

  const primaryText = useMemo(() => {
    if (title) return title;
    if (userProfile?.name) {
      const greet = t?.('greeting') || 'Hello';
      return `${greet}, ${userProfile.name}`;
    }
    return '';
  }, [t, title, userProfile?.name]);

  const secondaryText = useMemo(() => {
    if (subtitle) return subtitle;
    if (userProfile?.rasi && userProfile?.nakshatra) {
      return `${userProfile.rasi} • ${userProfile.nakshatra}`;
    }
    return '';
  }, [subtitle, userProfile?.rasi, userProfile?.nakshatra]);

  const period = useMemo(() => {
    const hour = now.getHours();

    const normal = {
      label: t?.('normalTime') || 'Normal',
      color: '#ea580c',
      bg: '#fff7ed',
    };

    if (!showTime) return normal;

    if (hour >= 15 && hour < 17) {
      return {
        label: t?.('rahuKalam') || 'Rahu Kalam',
        color: '#dc2626',
        bg: '#fef2f2',
      };
    }

    if (hour >= 9 && hour < 11) {
      return {
        label: t?.('goodTime') || 'Good Time',
        color: '#16a34a',
        bg: '#f0fdf4',
      };
    }

    return normal;
  }, [now, showTime, t]);

  const topMargin = Math.max(insets.top, 16);

  return (
    <Animated.View
      style={[
        styles.header,
        { marginTop: topMargin, opacity: headerFadeAnim, transform: [{ translateY: headerSlideAnim }] },
      ]}
    >
      <View>
        <View style={styles.logoRow}>
          {showBackButton && (
            <TouchableOpacity
              onPress={onBackPress}
              style={styles.backButton}
              accessibilityRole="button"
              accessibilityLabel={t?.('back') || 'Back'}
              hitSlop={{ top: 8, bottom: 8, left: 8, right: 8 }}
            >
              <Ionicons name="arrow-back" size={22} color="#6b5644" />
            </TouchableOpacity>
          )}
          <View style={styles.logoIcon}>
            <Svg width={28} height={28} viewBox="0 0 100 100">
              <Path
                d="M50 5 L55 40 L90 30 L60 50 L90 70 L55 60 L50 95 L45 60 L10 70 L40 50 L10 30 L45 40 Z"
                fill="#f97316"
              />
              <Circle cx="50" cy="50" r="10" fill="#fff7ed" />
            </Svg>
          </View>
          <Text style={styles.appTitle}>{appTitle}</Text>
        </View>

        {(primaryText || secondaryText) && (
          <View style={styles.userInfo}>
            {!!primaryText && <Text style={styles.primaryText}>{primaryText}</Text>}
            {!!secondaryText && <Text style={styles.secondaryText}>{secondaryText}</Text>}
          </View>
        )}
      </View>

      {showTime && (
        <View style={styles.timeContainer}>
          <Text style={styles.currentTime}>
            {now.toLocaleTimeString('ta-IN', { hour: '2-digit', minute: '2-digit' })}
          </Text>
          <View style={[styles.periodBadge, { backgroundColor: period.bg, borderColor: period.bg }]}>
            <Text style={[styles.periodText, { color: period.color }]}>{period.label}</Text>
          </View>
        </View>
      )}
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    padding: 24,
    paddingBottom: 20,
    backgroundColor: '#fff8f0',
    marginHorizontal: 16,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#e8d5c4',
    shadowColor: '#d4a574',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.08,
    shadowRadius: 12,
    elevation: 3,
    overflow: 'hidden',
  },
  logoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  backButton: {
    width: 38,
    height: 38,
    borderRadius: 19,
    backgroundColor: '#fef6ed',
    borderWidth: 1,
    borderColor: '#e8d5c4',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 2,
  },
  logoIcon: {
    width: 36,
    height: 36,
    justifyContent: 'center',
    alignItems: 'center',
  },
  appTitle: {
    fontSize: 24,
    fontWeight: '600',
    color: '#6b5644',
    letterSpacing: 0.5,
    fontFamily: Platform.OS === 'ios' ? 'Georgia' : 'serif',
  },
  userInfo: {
    marginTop: 8,
  },
  primaryText: {
    fontSize: 16,
    color: '#8b6f47',
    fontWeight: '500',
  },
  secondaryText: {
    fontSize: 14,
    color: '#c69c6d',
    marginTop: 3,
    fontWeight: '600',
  },
  timeContainer: {
    alignItems: 'flex-end',
  },
  currentTime: {
    fontSize: 22,
    fontFamily: 'monospace',
    color: '#6b5644',
    fontWeight: '600',
    letterSpacing: 1,
  },
  periodBadge: {
    paddingHorizontal: 14,
    paddingVertical: 6,
    borderRadius: 16,
    marginTop: 8,
    borderWidth: 1,
  },
  periodText: {
    fontSize: 11,
    fontWeight: '700',
    letterSpacing: 0.5,
  },
});
