import React, { useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Animated,
  Dimensions,
  Easing,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import Svg, { Path, Circle, Defs, RadialGradient, Stop, Ellipse, G } from 'react-native-svg';

const { width, height } = Dimensions.get('window');

// Mango Leaf Component - More detailed
const MangoLeaf = ({ x, y, rotation = 0, scale = 1 }) => (
  <G transform={`translate(${x}, ${y}) rotate(${rotation}) scale(${scale})`}>
    <Path
      d="M0 0 Q6 -12 0 -32 Q-6 -12 0 0"
      fill="#166534"
      stroke="#15803d"
      strokeWidth="0.3"
    />
    <Path d="M0 -3 L0 -28" stroke="#22c55e" strokeWidth="0.6" />
    <Path d="M0 -8 L-3 -12" stroke="#22c55e" strokeWidth="0.3" />
    <Path d="M0 -8 L3 -12" stroke="#22c55e" strokeWidth="0.3" />
    <Path d="M0 -14 L-3.5 -18" stroke="#22c55e" strokeWidth="0.3" />
    <Path d="M0 -14 L3.5 -18" stroke="#22c55e" strokeWidth="0.3" />
    <Path d="M0 -20 L-2.5 -24" stroke="#22c55e" strokeWidth="0.3" />
    <Path d="M0 -20 L2.5 -24" stroke="#22c55e" strokeWidth="0.3" />
  </G>
);

// Small Leaf for filling gaps
const SmallLeaf = ({ x, y, rotation = 0 }) => (
  <G transform={`translate(${x}, ${y}) rotate(${rotation})`}>
    <Path
      d="M0 0 Q3 -8 0 -18 Q-3 -8 0 0"
      fill="#15803d"
      stroke="#166534"
      strokeWidth="0.2"
    />
    <Path d="M0 -2 L0 -15" stroke="#22c55e" strokeWidth="0.4" />
  </G>
);

// Marigold Flower Component - More realistic with more petals
const MarigoldFlower = ({ cx, cy, size = 20, color = '#f97316' }) => (
  <G>
    {/* Outer layer - 16 petals */}
    {[...Array(16)].map((_, i) => (
      <Ellipse
        key={`outer-${i}`}
        cx={cx + (size * 0.45) * Math.cos((i * 22.5 * Math.PI) / 180)}
        cy={cy + (size * 0.45) * Math.sin((i * 22.5 * Math.PI) / 180)}
        rx={size * 0.22}
        ry={size * 0.12}
        fill={color}
        transform={`rotate(${i * 22.5 + 90}, ${cx + (size * 0.45) * Math.cos((i * 22.5 * Math.PI) / 180)}, ${cy + (size * 0.45) * Math.sin((i * 22.5 * Math.PI) / 180)})`}
      />
    ))}
    {/* Middle layer - 12 petals */}
    {[...Array(12)].map((_, i) => (
      <Ellipse
        key={`middle-${i}`}
        cx={cx + (size * 0.28) * Math.cos((i * 30 * Math.PI) / 180)}
        cy={cy + (size * 0.28) * Math.sin((i * 30 * Math.PI) / 180)}
        rx={size * 0.18}
        ry={size * 0.1}
        fill={color === '#f97316' ? '#fb923c' : '#fde047'}
        transform={`rotate(${i * 30 + 90}, ${cx + (size * 0.28) * Math.cos((i * 30 * Math.PI) / 180)}, ${cy + (size * 0.28) * Math.sin((i * 30 * Math.PI) / 180)})`}
      />
    ))}
    {/* Inner layer - 8 petals */}
    {[...Array(8)].map((_, i) => (
      <Ellipse
        key={`inner-${i}`}
        cx={cx + (size * 0.12) * Math.cos((i * 45 * Math.PI) / 180)}
        cy={cy + (size * 0.12) * Math.sin((i * 45 * Math.PI) / 180)}
        rx={size * 0.12}
        ry={size * 0.08}
        fill={color === '#f97316' ? '#fdba74' : '#fef08a'}
        transform={`rotate(${i * 45 + 90}, ${cx + (size * 0.12) * Math.cos((i * 45 * Math.PI) / 180)}, ${cy + (size * 0.12) * Math.sin((i * 45 * Math.PI) / 180)})`}
      />
    ))}
    <Circle cx={cx} cy={cy} r={size * 0.08} fill="#fbbf24" />
  </G>
);

// Rose Flower Component
const RoseFlower = ({ cx, cy, size = 18 }) => (
  <G>
    {[...Array(8)].map((_, i) => (
      <Ellipse
        key={i}
        cx={cx + (size * 0.3) * Math.cos((i * 45 * Math.PI) / 180)}
        cy={cy + (size * 0.3) * Math.sin((i * 45 * Math.PI) / 180)}
        rx={size * 0.25}
        ry={size * 0.2}
        fill="#dc2626"
        transform={`rotate(${i * 45}, ${cx + (size * 0.3) * Math.cos((i * 45 * Math.PI) / 180)}, ${cy + (size * 0.3) * Math.sin((i * 45 * Math.PI) / 180)})`}
      />
    ))}
    <Circle cx={cx} cy={cy} r={size * 0.15} fill="#b91c1c" />
  </G>
);

// Jasmine String Component
const JasmineString = ({ startX, startY, length, angle = 90 }) => {
  const flowers = Math.floor(length / 12);
  return (
    <G transform={`rotate(${angle}, ${startX}, ${startY})`}>
      {/* String */}
      <Path
        d={`M${startX} ${startY} L${startX} ${startY + length}`}
        stroke="#84cc16"
        strokeWidth="2"
      />
      {/* Jasmine buds */}
      {[...Array(flowers)].map((_, i) => (
        <G key={i}>
          <Ellipse
            cx={startX}
            cy={startY + 8 + i * 12}
            rx={5}
            ry={4}
            fill="#fefce8"
            stroke="#fef9c3"
            strokeWidth="0.5"
          />
          <Circle
            cx={startX}
            cy={startY + 6 + i * 12}
            r={2}
            fill="#fef9c3"
          />
        </G>
      ))}
    </G>
  );
};

// Toran (Mango Leaf Decoration) Component - Denser
const Toran = ({ width: toranWidth }) => {
  const leafCount = Math.floor(toranWidth / 10); // More leaves
  const smallLeafCount = Math.floor(toranWidth / 12);
  return (
    <Svg width={toranWidth} height={90} viewBox={`0 0 ${toranWidth} 90`}>
      {/* Rope/String */}
      <Path
        d={`M0 12 Q${toranWidth / 4} 20 ${toranWidth / 2} 15 Q${toranWidth * 3 / 4} 10 ${toranWidth} 15`}
        stroke="#92400e"
        strokeWidth="5"
        fill="none"
      />
      <Path
        d={`M0 12 Q${toranWidth / 4} 20 ${toranWidth / 2} 15 Q${toranWidth * 3 / 4} 10 ${toranWidth} 15`}
        stroke="#b45309"
        strokeWidth="3"
        fill="none"
      />

      {/* Back row of small leaves */}
      {[...Array(smallLeafCount)].map((_, i) => {
        const x = (i / smallLeafCount) * toranWidth + 6;
        const curveY = 15 + Math.sin((i / smallLeafCount) * Math.PI) * 5;
        const rotation = -15 + (i % 4) * 10;
        return (
          <SmallLeaf
            key={`small-${i}`}
            x={x}
            y={curveY + 25}
            rotation={rotation}
          />
        );
      })}

      {/* Main row of mango leaves */}
      {[...Array(leafCount)].map((_, i) => {
        const x = (i / leafCount) * toranWidth + 5;
        const curveY = 15 + Math.sin((i / leafCount) * Math.PI) * 6;
        const rotation = -12 + (i % 5) * 6;
        return (
          <MangoLeaf
            key={`main-${i}`}
            x={x}
            y={curveY + 40}
            rotation={rotation}
            scale={0.85}
          />
        );
      })}

      {/* Front row alternating */}
      {[...Array(Math.floor(leafCount / 2))].map((_, i) => {
        const x = (i / (leafCount / 2)) * toranWidth + 12;
        const curveY = 15 + Math.sin((i / (leafCount / 2)) * Math.PI) * 6;
        return (
          <MangoLeaf
            key={`front-${i}`}
            x={x}
            y={curveY + 48}
            rotation={(i % 2 === 0 ? -8 : 8)}
            scale={0.7}
          />
        );
      })}

      {/* Decorative flowers on toran */}
      {[...Array(7)].map((_, i) => {
        const x = 30 + (i * (toranWidth - 60) / 6);
        return (
          <MarigoldFlower
            key={`toran-flower-${i}`}
            cx={x}
            cy={18}
            size={14}
            color={i % 2 === 0 ? '#f97316' : '#fbbf24'}
          />
        );
      })}
    </Svg>
  );
};

// Hanging Garland Component
const HangingGarland = ({ x, length, type = 'marigold' }) => {
  const flowerCount = Math.floor(length / 25);
  return (
    <Svg width={40} height={length} style={{ position: 'absolute', left: x - 20 }}>
      {/* String */}
      <Path
        d={`M20 0 L20 ${length}`}
        stroke="#84cc16"
        strokeWidth="3"
      />

      {/* Flowers */}
      {[...Array(flowerCount)].map((_, i) => {
        const cy = 15 + i * 25;
        if (type === 'marigold') {
          return <MarigoldFlower key={i} cx={20} cy={cy} size={18} color={i % 2 === 0 ? '#f97316' : '#fbbf24'} />;
        } else if (type === 'rose') {
          return <RoseFlower key={i} cx={20} cy={cy} size={15} />;
        }
        return null;
      })}
    </Svg>
  );
};

// Sunburst Effect Component
const Sunburst = ({ style }) => {
  const rotateAnim = useRef(new Animated.Value(0)).current;
  const pulseAnim = useRef(new Animated.Value(0.8)).current;

  useEffect(() => {
    Animated.loop(
      Animated.timing(rotateAnim, {
        toValue: 1,
        duration: 60000,
        easing: Easing.linear,
        useNativeDriver: true,
      })
    ).start();

    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 2000,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 0.8,
          duration: 2000,
          useNativeDriver: true,
        }),
      ])
    ).start();
  }, []);

  const rotate = rotateAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  return (
    <Animated.View style={[style, { transform: [{ rotate }, { scale: pulseAnim }] }]}>
      <Svg width={400} height={400} viewBox="0 0 400 400">
        <Defs>
          <RadialGradient id="sunGrad" cx="50%" cy="50%" r="50%">
            <Stop offset="0%" stopColor="#fef08a" stopOpacity="1" />
            <Stop offset="30%" stopColor="#fde047" stopOpacity="0.8" />
            <Stop offset="60%" stopColor="#facc15" stopOpacity="0.4" />
            <Stop offset="100%" stopColor="#f97316" stopOpacity="0" />
          </RadialGradient>
        </Defs>

        {/* Central glow */}
        <Circle cx="200" cy="200" r="80" fill="url(#sunGrad)" />

        {/* Sun rays */}
        {[...Array(24)].map((_, i) => (
          <Path
            key={i}
            d={`M200 200 L${200 + 200 * Math.cos((i * 15 * Math.PI) / 180)} ${200 + 200 * Math.sin((i * 15 * Math.PI) / 180)}`}
            stroke="#fbbf24"
            strokeWidth={i % 2 === 0 ? 3 : 1.5}
            opacity={i % 2 === 0 ? 0.6 : 0.3}
          />
        ))}
      </Svg>
    </Animated.View>
  );
};

// Loading dots component
const LoadingDots = () => {
  const dot1 = useRef(new Animated.Value(0)).current;
  const dot2 = useRef(new Animated.Value(0)).current;
  const dot3 = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    const animateDot = (dot, delay) => {
      return Animated.loop(
        Animated.sequence([
          Animated.delay(delay),
          Animated.timing(dot, {
            toValue: 1,
            duration: 300,
            useNativeDriver: true,
          }),
          Animated.timing(dot, {
            toValue: 0,
            duration: 300,
            useNativeDriver: true,
          }),
        ])
      );
    };

    const anim1 = animateDot(dot1, 0);
    const anim2 = animateDot(dot2, 200);
    const anim3 = animateDot(dot3, 400);

    anim1.start();
    anim2.start();
    anim3.start();

    return () => {
      anim1.stop();
      anim2.stop();
      anim3.stop();
    };
  }, []);

  const dotStyle = (animValue) => ({
    transform: [
      {
        translateY: animValue.interpolate({
          inputRange: [0, 1],
          outputRange: [0, -8],
        }),
      },
    ],
  });

  return (
    <View style={styles.dotsRow}>
      <Animated.View style={[styles.dot, dotStyle(dot1)]} />
      <Animated.View style={[styles.dot, dotStyle(dot2)]} />
      <Animated.View style={[styles.dot, dotStyle(dot3)]} />
    </View>
  );
};

export default function SplashScreen({ onFinish }) {
  // Animated values
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const logoScale = useRef(new Animated.Value(0.5)).current;
  const logoOpacity = useRef(new Animated.Value(0)).current;
  const titleOpacity = useRef(new Animated.Value(0)).current;
  const garlandAnim = useRef(new Animated.Value(-100)).current;

  useEffect(() => {
    // Start animation sequence
    Animated.sequence([
      // Background and garlands
      Animated.parallel([
        Animated.timing(fadeAnim, {
          toValue: 1,
          duration: 600,
          useNativeDriver: true,
        }),
        Animated.spring(garlandAnim, {
          toValue: 0,
          friction: 8,
          tension: 40,
          useNativeDriver: true,
        }),
      ]),
      // Logo entrance
      Animated.parallel([
        Animated.timing(logoOpacity, {
          toValue: 1,
          duration: 500,
          useNativeDriver: true,
        }),
        Animated.spring(logoScale, {
          toValue: 1,
          friction: 5,
          tension: 40,
          useNativeDriver: true,
        }),
      ]),
      // Title
      Animated.timing(titleOpacity, {
        toValue: 1,
        duration: 400,
        useNativeDriver: true,
      }),
    ]).start();

    // Finish splash after animation
    const timer = setTimeout(() => {
      onFinish?.();
    }, 3500);

    return () => clearTimeout(timer);
  }, []);

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={['#fef3c7', '#fed7aa', '#fdba74', '#fb923c', '#f97316']}
        style={styles.gradient}
        start={{ x: 0.5, y: 0 }}
        end={{ x: 0.5, y: 1 }}
        locations={[0, 0.2, 0.4, 0.7, 1]}
      >
        {/* Sunburst effect in center */}
        <Sunburst style={styles.sunburst} />

        {/* Top decoration - Mango Toran */}
        <Animated.View
          style={[
            styles.toranContainer,
            {
              opacity: fadeAnim,
              transform: [{ translateY: garlandAnim }]
            }
          ]}
        >
          <Toran width={width} />
        </Animated.View>

        {/* Hanging garlands */}
        <Animated.View
          style={[
            styles.garlansWrapper,
            {
              opacity: fadeAnim,
              transform: [{ translateY: garlandAnim }]
            }
          ]}
        >
          {/* Left side garlands */}
          <HangingGarland x={30} length={height * 0.35} type="marigold" />
          <HangingGarland x={80} length={height * 0.25} type="rose" />

          {/* Center garlands */}
          <View style={styles.centerGarlands}>
            <Svg width={width * 0.6} height={height * 0.3} style={styles.jasmineContainer}>
              <JasmineString startX={width * 0.15} startY={0} length={height * 0.2} angle={100} />
              <JasmineString startX={width * 0.3} startY={0} length={height * 0.25} angle={90} />
              <JasmineString startX={width * 0.45} startY={0} length={height * 0.2} angle={80} />
            </Svg>
          </View>

          {/* Right side garlands */}
          <HangingGarland x={width - 80} length={height * 0.25} type="rose" />
          <HangingGarland x={width - 30} length={height * 0.35} type="marigold" />
        </Animated.View>

        {/* Decorative marigold clusters at top corners */}
        <Animated.View style={[styles.topLeftCluster, { opacity: fadeAnim }]}>
          <Svg width={100} height={100} viewBox="0 0 100 100">
            <MarigoldFlower cx={30} cy={40} size={25} />
            <MarigoldFlower cx={60} cy={25} size={20} />
            <MarigoldFlower cx={50} cy={60} size={22} />
            <RoseFlower cx={25} cy={70} size={15} />
            <RoseFlower cx={75} cy={50} size={15} />
          </Svg>
        </Animated.View>

        <Animated.View style={[styles.topRightCluster, { opacity: fadeAnim }]}>
          <Svg width={100} height={100} viewBox="0 0 100 100">
            <MarigoldFlower cx={70} cy={40} size={25} />
            <MarigoldFlower cx={40} cy={25} size={20} />
            <MarigoldFlower cx={50} cy={60} size={22} />
            <RoseFlower cx={75} cy={70} size={15} />
            <RoseFlower cx={25} cy={50} size={15} />
          </Svg>
        </Animated.View>

        {/* Main content */}
        <View style={styles.contentContainer}>
          {/* Logo */}
          <Animated.View
            style={[
              styles.logoContainer,
              {
                opacity: logoOpacity,
                transform: [{ scale: logoScale }],
              },
            ]}
          >
            <View style={styles.logoWrapper}>
              <LinearGradient
                colors={['#fff', '#fef3c7']}
                style={styles.logoBackground}
              >
                <LinearGradient
                  colors={['#f97316', '#ea580c']}
                  style={styles.logoInner}
                >
                  {/* Star/Zodiac symbol */}
                  <Svg width={50} height={50} viewBox="0 0 100 100">
                    <Path
                      d="M50 5 L55 40 L90 30 L60 50 L90 70 L55 60 L50 95 L45 60 L10 70 L40 50 L10 30 L45 40 Z"
                      fill="#fff"
                    />
                    <Circle cx="50" cy="50" r="10" fill="#f97316" />
                  </Svg>
                </LinearGradient>
              </LinearGradient>
            </View>
          </Animated.View>

          {/* Brand name */}
          <Animated.View style={{ opacity: titleOpacity }}>
            <Text style={styles.title}>jothida.ai</Text>
            <Text style={styles.subtitle}>Your Life Guide</Text>
          </Animated.View>

          {/* Loading dots */}
          <Animated.View style={[styles.loadingContainer, { opacity: titleOpacity }]}>
            <LoadingDots />
          </Animated.View>
        </View>
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
  sunburst: {
    position: 'absolute',
    top: height * 0.25,
    left: (width - 400) / 2,
    opacity: 0.6,
  },
  toranContainer: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    zIndex: 10,
  },
  garlansWrapper: {
    position: 'absolute',
    top: 60,
    left: 0,
    right: 0,
    height: height * 0.4,
    zIndex: 5,
  },
  centerGarlands: {
    position: 'absolute',
    left: width * 0.2,
    top: 20,
  },
  jasmineContainer: {
    position: 'absolute',
  },
  topLeftCluster: {
    position: 'absolute',
    top: 50,
    left: 10,
    zIndex: 15,
  },
  topRightCluster: {
    position: 'absolute',
    top: 50,
    right: 10,
    zIndex: 15,
  },
  contentContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: height * 0.1,
  },
  logoContainer: {
    marginBottom: 20,
  },
  logoWrapper: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.3,
    shadowRadius: 20,
    elevation: 15,
  },
  logoBackground: {
    width: 110,
    height: 110,
    borderRadius: 20,
    padding: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  logoInner: {
    width: 90,
    height: 90,
    borderRadius: 45,
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 42,
    fontWeight: 'bold',
    color: '#7c2d12',
    textAlign: 'center',
    textShadowColor: 'rgba(255, 255, 255, 0.5)',
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 2,
  },
  subtitle: {
    fontSize: 18,
    color: '#9a3412',
    textAlign: 'center',
    marginTop: 5,
    fontWeight: '500',
  },
  loadingContainer: {
    marginTop: 50,
  },
  dotsRow: {
    flexDirection: 'row',
    gap: 10,
  },
  dot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: '#7c2d12',
  },
});
