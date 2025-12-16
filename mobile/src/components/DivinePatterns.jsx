import React, { useMemo, useRef, useState } from 'react';
import { Svg, Path, Circle, Defs, Pattern, Rect } from 'react-native-svg';
import { View, StyleSheet, useWindowDimensions } from 'react-native';

// 1. Kolam / Mandala Pattern (Traditional Indian Rangoli)
export const KolamPattern = ({ color = "#d4a574", opacity = 0.35, style }) => {
  const patternId = useRef(`kolam-${Math.random().toString(36).slice(2)}`).current;

  return (
    <View style={[styles.absoluteFill, style, { opacity }]} pointerEvents="none">
      <Svg height="100%" width="100%">
        <Defs>
          <Pattern id={patternId} x="0" y="0" width="60" height="60" patternUnits="userSpaceOnUse">
          <Path
            d="M30 0 C30 15 45 30 60 30 C45 30 30 45 30 60 C30 45 15 30 0 30 C15 30 30 15 30 0"
            fill="none"
            stroke={color}
            strokeWidth="3"
          />
          <Circle cx="30" cy="30" r="4" fill={color} />
        </Pattern>
      </Defs>
        <Rect x="0" y="0" width="100%" height="100%" fill={`url(#${patternId})`} />
      </Svg>
    </View>
  );
};

// 2. Scallop / Temple Arch Pattern (Subtle Illustration)
// View-based (not SVG) to ensure it renders reliably on native + web.
export const ScallopPattern = ({
  color = "#e8d5c4",
  opacity = 0.14,
  circleSize = 46,
  borderWidth = 2,
  style,
}) => {
  const { width: screenWidth } = useWindowDimensions();
  const [measuredHeight, setMeasuredHeight] = useState(0);

  const circles = useMemo(() => {
    if (!measuredHeight) return [];

    const size = circleSize;
    const step = Math.max(18, Math.round(size * 0.78));

    const cols = Math.ceil((screenWidth + size) / step) + 1;
    const rows = Math.ceil((measuredHeight + size) / step) + 1;

    const out = [];
    for (let row = 0; row < rows; row += 1) {
      const y = row * step - size / 2;
      const xOffset = row % 2 === 0 ? 0 : Math.round(step / 2);

      for (let col = 0; col < cols; col += 1) {
        const x = col * step + xOffset - size / 2;
        const localOpacity = row % 3 === 0 ? 0.22 : 0.14;

        out.push({
          key: `${row}-${col}`,
          left: x,
          top: y,
          opacity: localOpacity,
        });
      }
    }

    return out;
  }, [circleSize, measuredHeight, screenWidth]);

  return (
    <View
      pointerEvents="none"
      onLayout={(e) => setMeasuredHeight(e.nativeEvent.layout.height)}
      style={[styles.absoluteFill, style, { opacity }]}
    >
      {circles.map((c) => (
        <View
          key={c.key}
          style={{
            position: 'absolute',
            left: c.left,
            top: c.top,
            width: circleSize,
            height: circleSize,
            borderRadius: circleSize / 2,
            borderWidth,
            borderColor: color,
            opacity: c.opacity,
          }}
        />
      ))}
    </View>
  );
};

// 3. Lotus Corner Decoration (Sacred Lotus Petals)
export const LotusCorner = ({ color = "#d4a574", size = 60, style }) => (
  <View style={[style, { width: size, height: size, zIndex: 10 }]} pointerEvents="none">
    <Svg width="100%" height="100%" viewBox="0 0 100 100">
      <Path
        d="M0 0 Q50 0 50 50 Q0 50 0 0 M0 0 Q0 50 50 50 Q50 0 0 0"
        fill="none"
        stroke={color}
        strokeWidth="2.5"
        opacity="0.8"
      />
      <Path
        d="M0 0 C20 0 40 10 50 30 C60 10 80 0 100 0 L100 100 L0 100 Z"
        fill={color}
        opacity="0.35"
      />
      <Path
        d="M10 10 Q50 10 50 50 Q10 50 10 10"
        fill="none"
        stroke={color}
        strokeWidth="3.5"
        opacity="0.7"
      />
    </Svg>
  </View>
);

// 4. Om Symbol Watermark (Sacred Hindu Symbol)
export const OmWatermark = ({ color = "#f97316", size = 120, opacity = 0.12, style }) => (
  <View style={[style, { width: size, height: size, opacity, zIndex: 0 }]} pointerEvents="none">
    <Svg width="100%" height="100%" viewBox="0 0 500 500">
      <Path
        d="M250 100 C200 100 150 150 150 200 C150 250 200 250 200 250 C150 250 100 300 100 350 C100 450 250 450 250 350 M250 250 C300 250 350 300 350 350 M350 200 Q400 100 450 150 M350 100 Q400 50 450 100"
        fill="none"
        stroke={color}
        strokeWidth="30"
        strokeLinecap="round"
      />
    </Svg>
  </View>
);

// 4. Decorative Divider (Traditional Hindu Border Pattern)
export const DivineDivider = ({ color = "#d97706" }) => {
  const borderId = useRef(`border-${Math.random().toString(36).slice(2)}`).current;

  return (
    <View style={{ height: 24, width: '100%', overflow: 'hidden', marginVertical: 12, alignItems: 'center', justifyContent: 'center' }}>
      <Svg height="100%" width="100%">
        <Defs>
          <Pattern id={borderId} x="0" y="0" width="40" height="24" patternUnits="userSpaceOnUse">
          <Path
            d="M0 12 Q10 2 20 12 Q30 22 40 12"
            fill="none"
            stroke={color}
            strokeWidth="3"
            opacity="0.9"
          />
          <Circle cx="20" cy="12" r="3" fill={color} opacity="1" />
        </Pattern>
      </Defs>
        <Rect x="0" y="0" width="100%" height="100%" fill={`url(#${borderId})`} />
      </Svg>
    </View>
  );
};

const styles = StyleSheet.create({
  absoluteFill: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
  },
});
