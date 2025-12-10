import { useRef, useEffect } from 'react';
import { Animated, Easing } from 'react-native';

// Fade in animation hook
export const useFadeIn = (delay = 0, duration = 500) => {
  const opacity = useRef(new Animated.Value(0)).current;
  const translateY = useRef(new Animated.Value(20)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(opacity, {
        toValue: 1,
        duration,
        delay,
        useNativeDriver: true,
        easing: Easing.out(Easing.ease),
      }),
      Animated.timing(translateY, {
        toValue: 0,
        duration,
        delay,
        useNativeDriver: true,
        easing: Easing.out(Easing.ease),
      }),
    ]).start();
  }, []);

  return { opacity, transform: [{ translateY }] };
};

// Scale in animation hook
export const useScaleIn = (delay = 0, duration = 400) => {
  const scale = useRef(new Animated.Value(0.8)).current;
  const opacity = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.spring(scale, {
        toValue: 1,
        delay,
        friction: 6,
        tension: 80,
        useNativeDriver: true,
      }),
      Animated.timing(opacity, {
        toValue: 1,
        duration,
        delay,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  return { opacity, transform: [{ scale }] };
};

// Slide in from left animation hook
export const useSlideInLeft = (delay = 0, duration = 400) => {
  const translateX = useRef(new Animated.Value(-50)).current;
  const opacity = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(translateX, {
        toValue: 0,
        duration,
        delay,
        useNativeDriver: true,
        easing: Easing.out(Easing.ease),
      }),
      Animated.timing(opacity, {
        toValue: 1,
        duration,
        delay,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  return { opacity, transform: [{ translateX }] };
};

// Slide in from right animation hook
export const useSlideInRight = (delay = 0, duration = 400) => {
  const translateX = useRef(new Animated.Value(50)).current;
  const opacity = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.parallel([
      Animated.timing(translateX, {
        toValue: 0,
        duration,
        delay,
        useNativeDriver: true,
        easing: Easing.out(Easing.ease),
      }),
      Animated.timing(opacity, {
        toValue: 1,
        duration,
        delay,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  return { opacity, transform: [{ translateX }] };
};

// Pulse animation hook (continuous)
export const usePulse = (minScale = 0.95, maxScale = 1.05) => {
  const scale = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    const pulse = Animated.loop(
      Animated.sequence([
        Animated.timing(scale, {
          toValue: maxScale,
          duration: 1000,
          useNativeDriver: true,
          easing: Easing.inOut(Easing.ease),
        }),
        Animated.timing(scale, {
          toValue: minScale,
          duration: 1000,
          useNativeDriver: true,
          easing: Easing.inOut(Easing.ease),
        }),
      ])
    );
    pulse.start();
    return () => pulse.stop();
  }, []);

  return { transform: [{ scale }] };
};

// Bounce animation hook
export const useBounce = (delay = 0) => {
  const translateY = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    const bounce = Animated.loop(
      Animated.sequence([
        Animated.timing(translateY, {
          toValue: -10,
          duration: 500,
          delay,
          useNativeDriver: true,
          easing: Easing.out(Easing.ease),
        }),
        Animated.timing(translateY, {
          toValue: 0,
          duration: 500,
          useNativeDriver: true,
          easing: Easing.in(Easing.ease),
        }),
      ])
    );
    bounce.start();
    return () => bounce.stop();
  }, []);

  return { transform: [{ translateY }] };
};

// Stagger animation helper
export const createStaggeredAnimation = (count, baseDelay = 0, staggerDelay = 100) => {
  const animations = [];
  for (let i = 0; i < count; i++) {
    animations.push({
      delay: baseDelay + i * staggerDelay,
    });
  }
  return animations;
};

// Progress bar animation
export const useProgressAnimation = (toValue, duration = 1000, delay = 0) => {
  const width = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(width, {
      toValue,
      duration,
      delay,
      useNativeDriver: false, // width animation can't use native driver
      easing: Easing.out(Easing.ease),
    }).start();
  }, [toValue]);

  return width;
};

// Rotation animation
export const useRotation = (duration = 2000) => {
  const rotation = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    const rotate = Animated.loop(
      Animated.timing(rotation, {
        toValue: 1,
        duration,
        useNativeDriver: true,
        easing: Easing.linear,
      })
    );
    rotate.start();
    return () => rotate.stop();
  }, []);

  const rotateInterpolate = rotation.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  return { transform: [{ rotate: rotateInterpolate }] };
};

// Shimmer animation
export const useShimmer = (width, duration = 1500) => {
  const position = useRef(new Animated.Value(-width)).current;

  useEffect(() => {
    const shimmer = Animated.loop(
      Animated.timing(position, {
        toValue: width,
        duration,
        useNativeDriver: true,
        easing: Easing.linear,
      })
    );
    shimmer.start();
    return () => shimmer.stop();
  }, []);

  return { transform: [{ translateX: position }] };
};

// Card flip animation
export const useFlip = () => {
  const flipAnim = useRef(new Animated.Value(0)).current;

  const flip = () => {
    Animated.spring(flipAnim, {
      toValue: flipAnim._value === 0 ? 1 : 0,
      friction: 8,
      tension: 10,
      useNativeDriver: true,
    }).start();
  };

  const frontInterpolate = flipAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '180deg'],
  });

  const backInterpolate = flipAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['180deg', '360deg'],
  });

  return {
    flip,
    frontStyle: { transform: [{ rotateY: frontInterpolate }] },
    backStyle: { transform: [{ rotateY: backInterpolate }] },
  };
};

// Button press animation
export const useButtonPress = () => {
  const scale = useRef(new Animated.Value(1)).current;

  const onPressIn = () => {
    Animated.spring(scale, {
      toValue: 0.95,
      useNativeDriver: true,
    }).start();
  };

  const onPressOut = () => {
    Animated.spring(scale, {
      toValue: 1,
      friction: 3,
      useNativeDriver: true,
    }).start();
  };

  return {
    style: { transform: [{ scale }] },
    onPressIn,
    onPressOut,
  };
};

// Animated counter
export const useAnimatedCounter = (endValue, duration = 1000) => {
  const animatedValue = useRef(new Animated.Value(0)).current;
  const displayValue = useRef(0);

  useEffect(() => {
    animatedValue.addListener(({ value }) => {
      displayValue.current = Math.round(value);
    });

    Animated.timing(animatedValue, {
      toValue: endValue,
      duration,
      useNativeDriver: false,
      easing: Easing.out(Easing.ease),
    }).start();

    return () => animatedValue.removeAllListeners();
  }, [endValue]);

  return animatedValue;
};
