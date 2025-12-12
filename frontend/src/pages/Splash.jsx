import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

// Mango Leaf SVG Component
const MangoLeaf = ({ x, y, rotation = 0, scale = 1 }) => (
  <g transform={`translate(${x}, ${y}) rotate(${rotation}) scale(${scale})`}>
    <path
      d="M0 0 Q6 -12 0 -32 Q-6 -12 0 0"
      fill="#166534"
      stroke="#15803d"
      strokeWidth="0.3"
    />
    <path d="M0 -3 L0 -28" stroke="#22c55e" strokeWidth="0.6" />
    <path d="M0 -8 L-3 -12" stroke="#22c55e" strokeWidth="0.3" />
    <path d="M0 -8 L3 -12" stroke="#22c55e" strokeWidth="0.3" />
    <path d="M0 -14 L-3.5 -18" stroke="#22c55e" strokeWidth="0.3" />
    <path d="M0 -14 L3.5 -18" stroke="#22c55e" strokeWidth="0.3" />
  </g>
);

// Marigold Flower Component
const MarigoldFlower = ({ cx, cy, size = 20, color = '#f97316' }) => (
  <g>
    {/* Outer layer - 16 petals */}
    {[...Array(16)].map((_, i) => (
      <ellipse
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
      <ellipse
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
      <ellipse
        key={`inner-${i}`}
        cx={cx + (size * 0.12) * Math.cos((i * 45 * Math.PI) / 180)}
        cy={cy + (size * 0.12) * Math.sin((i * 45 * Math.PI) / 180)}
        rx={size * 0.12}
        ry={size * 0.08}
        fill={color === '#f97316' ? '#fdba74' : '#fef08a'}
        transform={`rotate(${i * 45 + 90}, ${cx + (size * 0.12) * Math.cos((i * 45 * Math.PI) / 180)}, ${cy + (size * 0.12) * Math.sin((i * 45 * Math.PI) / 180)})`}
      />
    ))}
    <circle cx={cx} cy={cy} r={size * 0.08} fill="#fbbf24" />
  </g>
);

// Rose Flower Component
const RoseFlower = ({ cx, cy, size = 18 }) => (
  <g>
    {[...Array(8)].map((_, i) => (
      <ellipse
        key={i}
        cx={cx + (size * 0.3) * Math.cos((i * 45 * Math.PI) / 180)}
        cy={cy + (size * 0.3) * Math.sin((i * 45 * Math.PI) / 180)}
        rx={size * 0.25}
        ry={size * 0.2}
        fill="#dc2626"
        transform={`rotate(${i * 45}, ${cx + (size * 0.3) * Math.cos((i * 45 * Math.PI) / 180)}, ${cy + (size * 0.3) * Math.sin((i * 45 * Math.PI) / 180)})`}
      />
    ))}
    <circle cx={cx} cy={cy} r={size * 0.15} fill="#b91c1c" />
  </g>
);

// Toran (Mango Leaf Decoration)
const Toran = ({ width: toranWidth }) => {
  const leafCount = Math.floor(toranWidth / 12);
  return (
    <svg width={toranWidth} height={90} viewBox={`0 0 ${toranWidth} 90`}>
      {/* Rope/String */}
      <path
        d={`M0 12 Q${toranWidth / 4} 20 ${toranWidth / 2} 15 Q${toranWidth * 3 / 4} 10 ${toranWidth} 15`}
        stroke="#92400e"
        strokeWidth="5"
        fill="none"
      />
      <path
        d={`M0 12 Q${toranWidth / 4} 20 ${toranWidth / 2} 15 Q${toranWidth * 3 / 4} 10 ${toranWidth} 15`}
        stroke="#b45309"
        strokeWidth="3"
        fill="none"
      />

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
    </svg>
  );
};

// Loading dots
const LoadingDots = () => {
  return (
    <div className="flex gap-2">
      {[0, 1, 2].map((i) => (
        <motion.div
          key={i}
          className="w-3 h-3 rounded-full bg-orange-800"
          animate={{ y: [0, -8, 0] }}
          transition={{
            duration: 0.6,
            repeat: Infinity,
            delay: i * 0.15,
          }}
        />
      ))}
    </div>
  );
};

// Sunburst animation
const Sunburst = () => (
  <motion.div
    className="absolute opacity-60"
    style={{ top: '20%', left: '50%', transform: 'translateX(-50%)' }}
    animate={{ rotate: 360 }}
    transition={{ duration: 60, repeat: Infinity, ease: 'linear' }}
  >
    <svg width={400} height={400} viewBox="0 0 400 400">
      <defs>
        <radialGradient id="sunGrad" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#fef08a" stopOpacity="1" />
          <stop offset="30%" stopColor="#fde047" stopOpacity="0.8" />
          <stop offset="60%" stopColor="#facc15" stopOpacity="0.4" />
          <stop offset="100%" stopColor="#f97316" stopOpacity="0" />
        </radialGradient>
      </defs>
      <circle cx="200" cy="200" r="80" fill="url(#sunGrad)" />
      {[...Array(24)].map((_, i) => (
        <path
          key={i}
          d={`M200 200 L${200 + 200 * Math.cos((i * 15 * Math.PI) / 180)} ${200 + 200 * Math.sin((i * 15 * Math.PI) / 180)}`}
          stroke="#fbbf24"
          strokeWidth={i % 2 === 0 ? 3 : 1.5}
          opacity={i % 2 === 0 ? 0.6 : 0.3}
        />
      ))}
    </svg>
  </motion.div>
);

export default function Splash() {
  const navigate = useNavigate();
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    const handleResize = () => setWidth(window.innerWidth);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useEffect(() => {
    // Navigate to onboarding after 3.5 seconds
    const timer = setTimeout(() => {
      const onboardingComplete = localStorage.getItem('onboardingComplete');
      if (onboardingComplete) {
        navigate('/dashboard');
      } else {
        navigate('/onboarding');
      }
    }, 3500);

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className="min-h-screen relative overflow-hidden bg-gradient-to-b from-amber-100 via-orange-200 to-orange-400">
      {/* Sunburst effect */}
      <Sunburst />

      {/* Top Toran decoration */}
      <motion.div
        className="absolute top-0 left-0 right-0 z-10"
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8, type: 'spring' }}
      >
        <Toran width={width} />
      </motion.div>

      {/* Top left flower cluster */}
      <motion.div
        className="absolute top-12 left-2 z-20"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        <svg width={100} height={100} viewBox="0 0 100 100">
          <MarigoldFlower cx={30} cy={40} size={25} />
          <MarigoldFlower cx={60} cy={25} size={20} />
          <MarigoldFlower cx={50} cy={60} size={22} />
          <RoseFlower cx={25} cy={70} size={15} />
        </svg>
      </motion.div>

      {/* Top right flower cluster */}
      <motion.div
        className="absolute top-12 right-2 z-20"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        <svg width={100} height={100} viewBox="0 0 100 100">
          <MarigoldFlower cx={70} cy={40} size={25} />
          <MarigoldFlower cx={40} cy={25} size={20} />
          <MarigoldFlower cx={50} cy={60} size={22} />
          <RoseFlower cx={75} cy={70} size={15} />
        </svg>
      </motion.div>

      {/* Main content */}
      <div className="flex flex-col items-center justify-center min-h-screen pt-20">
        {/* Logo */}
        <motion.div
          initial={{ scale: 0.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.5, type: 'spring', stiffness: 100 }}
          className="mb-6"
        >
          <div className="w-28 h-28 rounded-2xl bg-gradient-to-b from-white to-amber-100 p-2 shadow-xl">
            <div className="w-full h-full rounded-full bg-gradient-to-b from-orange-500 to-orange-600 flex items-center justify-center">
              <svg width={50} height={50} viewBox="0 0 100 100">
                <path
                  d="M50 5 L55 40 L90 30 L60 50 L90 70 L55 60 L50 95 L45 60 L10 70 L40 50 L10 30 L45 40 Z"
                  fill="#fff"
                />
                <circle cx="50" cy="50" r="10" fill="#f97316" />
              </svg>
            </div>
          </div>
        </motion.div>

        {/* Brand name */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="text-center"
        >
          <h1 className="text-5xl font-bold text-orange-900" style={{ textShadow: '0 1px 2px rgba(255,255,255,0.5)' }}>
            jothida.ai
          </h1>
          <p className="text-xl text-orange-800 mt-2 font-medium">
            Your Life Guide
          </p>
        </motion.div>

        {/* Loading dots */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="mt-12"
        >
          <LoadingDots />
        </motion.div>
      </div>
    </div>
  );
}
