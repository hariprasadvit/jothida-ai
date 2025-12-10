import { useState, useEffect } from 'react';
import { ChevronDown, ChevronUp, TrendingUp, TrendingDown, Minus, Loader2 } from 'lucide-react';
import { panchangamAPI } from '../services/api';

export default function ScoreBreakdown({ lat = 13.0827, lon = 80.2707, date = null }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [breakdown, setBreakdown] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBreakdown = async () => {
      try {
        setLoading(true);
        const data = await panchangamAPI.getScoreBreakdown(date, lat, lon);
        setBreakdown(data);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch score breakdown:', err);
        setError('தரவு ஏற்ற முடியவில்லை');
      } finally {
        setLoading(false);
      }
    };

    fetchBreakdown();
  }, [lat, lon, date]);

  const getPointsIcon = (points) => {
    if (points > 0) return <TrendingUp className="w-4 h-4 text-green-600" />;
    if (points < 0) return <TrendingDown className="w-4 h-4 text-red-600" />;
    return <Minus className="w-4 h-4 text-gray-400" />;
  };

  const getPointsColor = (points) => {
    if (points > 0) return 'text-green-600';
    if (points < 0) return 'text-red-600';
    return 'text-gray-500';
  };

  const getScoreBarColor = (points, maxPoints) => {
    const ratio = points / maxPoints;
    if (ratio >= 0.5) return 'bg-green-500';
    if (ratio >= 0) return 'bg-orange-500';
    return 'bg-red-500';
  };

  const getScoreLabel = (score) => {
    if (score >= 70) return { text: 'நல்லது', color: 'text-green-600', bg: 'bg-green-100' };
    if (score >= 40) return { text: 'சாதாரணம்', color: 'text-orange-600', bg: 'bg-orange-100' };
    return { text: 'கவனம்', color: 'text-red-600', bg: 'bg-red-100' };
  };

  if (loading) {
    return (
      <div className="bg-white rounded-2xl border border-orange-200 p-4 shadow-sm">
        <div className="flex items-center justify-center gap-2 py-4">
          <Loader2 className="w-5 h-5 text-orange-500 animate-spin" />
          <span className="text-gray-500 text-sm">மதிப்பெண் விவரம் ஏற்றுகிறது...</span>
        </div>
      </div>
    );
  }

  if (error || !breakdown) {
    return null;
  }

  const scoreLabel = getScoreLabel(breakdown.total_score);

  return (
    <div className="bg-white rounded-2xl border border-orange-200 shadow-sm overflow-hidden">
      {/* Header - Always visible */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full px-4 py-3 flex items-center justify-between hover:bg-orange-50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <div className="text-left">
            <p className="text-sm text-gray-500">இன்றைய மதிப்பெண் விவரம்</p>
            <div className="flex items-center gap-2 mt-0.5">
              <span className="text-2xl font-bold text-orange-600">{breakdown.total_score}</span>
              <span className="text-sm text-gray-400">/100</span>
              <span className={`text-xs px-2 py-0.5 rounded-full ${scoreLabel.bg} ${scoreLabel.color}`}>
                {scoreLabel.text}
              </span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-400">
            {isExpanded ? 'மூடு' : 'விரிவாக'}
          </span>
          {isExpanded ? (
            <ChevronUp className="w-5 h-5 text-gray-400" />
          ) : (
            <ChevronDown className="w-5 h-5 text-gray-400" />
          )}
        </div>
      </button>

      {/* Expanded Content */}
      {isExpanded && (
        <div className="px-4 pb-4 border-t border-orange-100">
          {/* Base Score */}
          <div className="mt-3 mb-4 text-center">
            <span className="text-xs text-gray-500">
              அடிப்படை மதிப்பெண்: <span className="font-medium">{breakdown.base_score}</span>
            </span>
          </div>

          {/* Factors */}
          <div className="space-y-3">
            {breakdown.factors.map((factor, index) => (
              <div key={index} className="bg-orange-50/50 rounded-xl p-3">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    {getPointsIcon(factor.points)}
                    <div>
                      <p className="text-sm font-medium text-gray-800">{factor.tamil_name}</p>
                      <p className="text-xs text-gray-500">{factor.name}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className={`text-sm font-bold ${getPointsColor(factor.points)}`}>
                      {factor.points > 0 ? '+' : ''}{factor.points}
                    </span>
                    <span className="text-xs text-gray-400 ml-1">
                      /{factor.max_points > 0 ? '+' : ''}{factor.max_points}
                    </span>
                  </div>
                </div>

                {/* Value */}
                <div className="mb-2">
                  <span className="text-xs px-2 py-0.5 bg-white rounded-full border border-orange-200 text-orange-700">
                    {factor.value}
                  </span>
                </div>

                {/* Progress Bar */}
                <div className="w-full bg-gray-200 rounded-full h-1.5">
                  <div
                    className={`h-1.5 rounded-full transition-all duration-500 ${getScoreBarColor(factor.points, factor.max_points)}`}
                    style={{
                      width: `${Math.abs(factor.points) / Math.abs(factor.max_points) * 100}%`
                    }}
                  />
                </div>

                {/* Description */}
                <p className="text-xs text-gray-600 mt-2 leading-relaxed">
                  {factor.description}
                </p>
              </div>
            ))}
          </div>

          {/* Total Summary */}
          <div className="mt-4 pt-3 border-t border-orange-200">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">மொத்த புள்ளிகள்:</span>
              <span className="text-sm font-bold text-orange-700">
                {breakdown.base_score}
                {breakdown.factors.reduce((sum, f) => sum + f.points, 0) >= 0 ? ' + ' : ' - '}
                {Math.abs(breakdown.factors.reduce((sum, f) => sum + f.points, 0))}
                = {breakdown.total_score}
              </span>
            </div>
          </div>

          {/* Calculated At */}
          <div className="mt-2 text-center">
            <span className="text-[10px] text-gray-400">
              கணக்கிடப்பட்டது: {new Date(breakdown.calculated_at).toLocaleTimeString('ta-IN')}
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
