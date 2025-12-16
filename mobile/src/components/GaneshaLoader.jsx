import React, { useEffect, useMemo, useRef } from 'react';
import { Animated, Easing, Image, Platform, StyleSheet, Text, View } from 'react-native';
import { FESTIVAL_ASSETS } from '../utils/festivalAssets';

export default function GaneshaLoader({ size = 160, label }) {
  const pulse = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    const anim = Animated.loop(
      Animated.sequence([
        Animated.timing(pulse, { toValue: 1, duration: 1100, easing: Easing.inOut(Easing.ease), useNativeDriver: true }),
        Animated.timing(pulse, { toValue: 0, duration: 1100, easing: Easing.inOut(Easing.ease), useNativeDriver: true }),
      ]),
    );
    anim.start();
    return () => anim.stop();
  }, [pulse]);

  const scale = useMemo(
    () =>
      pulse.interpolate({
        inputRange: [0, 1],
        outputRange: [1, 1.04],
      }),
    [pulse],
  );

  const resolvedLabel = label ?? 'Loading';

  return (
    <View style={styles.container}>
      <Animated.View style={[styles.imageWrap, { transform: [{ scale }] }]}
      >
        <Image
          source={{ uri: FESTIVAL_ASSETS.ganesha }}
          style={{ width: size, height: size }}
          resizeMode="contain"
        />
      </Animated.View>
      {!!resolvedLabel && <Text style={styles.label}>{resolvedLabel}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  imageWrap: {
    shadowColor: '#d4a574',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.12,
    shadowRadius: 14,
    elevation: 4,
  },
  label: {
    marginTop: 14,
    fontSize: 13,
    fontWeight: '800',
    color: '#8b6f47',
    letterSpacing: 0.4,
    fontFamily: Platform.OS === 'ios' ? 'Georgia' : undefined,
  },
});
