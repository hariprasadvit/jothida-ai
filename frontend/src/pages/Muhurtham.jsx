import { useState, useEffect } from 'react';
import { Calendar, Clock, CheckCircle, Star, ChevronLeft, ChevronRight, Sparkles, Loader2, AlertCircle } from 'lucide-react';
import { muhurthamAPI } from '../services/api';

const eventTypes = [
  { id: 'marriage', icon: '💒', label: 'திருமணம்' },
  { id: 'griha_pravesam', icon: '🏠', label: 'கிரஹ பிரவேசம்' },
  { id: 'vehicle', icon: '🚗', label: 'வாகனம்' },
  { id: 'business', icon: '💼', label: 'தொழில்' },
  { id: 'travel', icon: '✈️', label: 'பயணம்' },
  { id: 'general', icon: '⭐', label: 'பொது' },
];

export default function Muhurtham() {
  const [eventType, setEventType] = useState('general');
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState(null);
  const [calendarData, setCalendarData] = useState([]);
  const [dayDetails, setDayDetails] = useState(null);
  const [loadingCalendar, setLoadingCalendar] = useState(true);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const [error, setError] = useState(null);

  const monthNames = [
    'ஜனவரி', 'பிப்ரவரி', 'மார்ச்', 'ஏப்ரல்', 'மே', 'ஜூன்',
    'ஜூலை', 'ஆகஸ்ட்', 'செப்டம்பர்', 'அக்டோபர்', 'நவம்பர்', 'டிசம்பர்'
  ];

  const dayNames = ['ஞா', 'தி', 'செ', 'பு', 'வி', 'வெ', 'ச'];

  // Fetch calendar data when month changes
  useEffect(() => {
    const fetchCalendar = async () => {
      setLoadingCalendar(true);
      setError(null);
      try {
        const month = currentMonth.getMonth() + 1;
        const year = currentMonth.getFullYear();
        const data = await muhurthamAPI.getCalendar(month, year);
        setCalendarData(data);
      } catch (err) {
        console.error('Failed to fetch calendar:', err);
        setError('நாள்காட்டி தரவு ஏற்ற முடியவில்லை');
        // Fall back to empty calendar
        setCalendarData([]);
      } finally {
        setLoadingCalendar(false);
      }
    };

    fetchCalendar();
    setSelectedDate(null);
    setDayDetails(null);
  }, [currentMonth]);

  // Fetch day details when date is selected
  useEffect(() => {
    const fetchDayDetails = async () => {
      if (!selectedDate) return;

      setLoadingDetails(true);
      try {
        const dateStr = `${currentMonth.getFullYear()}-${String(currentMonth.getMonth() + 1).padStart(2, '0')}-${String(selectedDate).padStart(2, '0')}`;
        const data = await muhurthamAPI.getDayDetails(dateStr);
        setDayDetails(data);
      } catch (err) {
        console.error('Failed to fetch day details:', err);
        setDayDetails(null);
      } finally {
        setLoadingDetails(false);
      }
    };

    fetchDayDetails();
  }, [selectedDate, currentMonth]);

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

    if (!dayData) {
      return 'bg-white text-gray-700 border-gray-200';
    }

    // Use event-specific score if available
    const score = dayData.event_scores?.[eventType] ?? dayData.day_score;

    if (score >= 70) {
      return 'bg-green-100 text-green-700 border-green-300';
    } else if (score >= 50) {
      return 'bg-yellow-50 text-yellow-700 border-yellow-200';
    } else if (score < 40) {
      return 'bg-red-100 text-red-700 border-red-300';
    }

    return 'bg-white text-gray-700 border-gray-200';
  };

  const getGoodEventsForDay = (day) => {
    const dayData = getDayData(day);
    if (!dayData || !dayData.good_for_events) return [];
    return dayData.good_for_events;
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-orange-50 pb-24">
      {/* Decorative Header */}
      <div className="bg-gradient-to-r from-green-500 via-emerald-500 to-green-500 h-1" />

      {/* Header */}
      <div className="bg-white border-b border-orange-100 px-4 py-4">
        <h1 className="text-xl font-bold text-green-800 flex items-center gap-2">
          <Calendar className="w-5 h-5 text-green-600" />
          முகூர்த்தம் கண்டறிதல்
        </h1>
        <p className="text-gray-500 text-sm">சுப நேரம் தேர்வு</p>
      </div>

      {/* Event Type Selector */}
      <div className="mx-4 mt-4 bg-white rounded-2xl border border-orange-200 p-4 shadow-sm">
        <h2 className="text-sm font-medium text-gray-800 mb-3 flex items-center gap-2">
          <Star className="w-4 h-4 text-orange-500" />
          நிகழ்வு வகை
        </h2>
        <div className="grid grid-cols-3 gap-2">
          {eventTypes.map((type) => (
            <button
              key={type.id}
              onClick={() => setEventType(type.id)}
              className={`p-3 rounded-xl text-center transition-all border ${
                eventType === type.id
                  ? 'bg-orange-50 border-orange-400 shadow-sm'
                  : 'bg-gray-50 border-gray-200 hover:border-orange-300'
              }`}
            >
              <span className="text-2xl block mb-1">{type.icon}</span>
              <span className="text-xs text-gray-700">{type.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mx-4 mt-4 bg-red-50 border border-red-200 rounded-xl p-3 flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-red-500" />
          <span className="text-sm text-red-700">{error}</span>
        </div>
      )}

      {/* Calendar */}
      <div className="mx-4 mt-4 bg-white rounded-2xl border border-orange-200 p-4 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <button onClick={prevMonth} className="p-2 hover:bg-gray-100 rounded-lg">
            <ChevronLeft className="w-5 h-5 text-gray-600" />
          </button>
          <h2 className="text-lg font-semibold text-gray-800">
            {monthNames[currentMonth.getMonth()]} {currentMonth.getFullYear()}
          </h2>
          <button onClick={nextMonth} className="p-2 hover:bg-gray-100 rounded-lg">
            <ChevronRight className="w-5 h-5 text-gray-600" />
          </button>
        </div>

        {/* Day Headers */}
        <div className="grid grid-cols-7 gap-1 mb-2">
          {dayNames.map((day, i) => (
            <div key={i} className={`text-center text-xs font-medium py-2 ${i === 0 ? 'text-red-500' : 'text-gray-500'}`}>
              {day}
            </div>
          ))}
        </div>

        {/* Loading State */}
        {loadingCalendar ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="w-8 h-8 text-orange-500 animate-spin" />
          </div>
        ) : (
          <>
            {/* Calendar Days */}
            <div className="grid grid-cols-7 gap-1">
              {/* Empty cells for days before the first day */}
              {[...Array(firstDay)].map((_, i) => (
                <div key={`empty-${i}`} className="aspect-square" />
              ))}

              {/* Days of the month */}
              {[...Array(daysInMonth)].map((_, i) => {
                const day = i + 1;
                const isSelected = selectedDate === day;
                const goodEvents = getGoodEventsForDay(day);
                const hasSelectedEvent = goodEvents.some(e => e.type === eventType);

                return (
                  <button
                    key={day}
                    onClick={() => setSelectedDate(day)}
                    className={`aspect-square rounded-lg border flex flex-col items-center justify-center text-xs transition-all relative overflow-hidden ${
                      isSelected
                        ? 'bg-orange-500 text-white border-orange-500 shadow-lg'
                        : getDateStyle(day)
                    }`}
                  >
                    <span className="font-semibold text-sm">{day}</span>

                    {/* Show event icons row for good days - improved visibility */}
                    {!isSelected && goodEvents.length > 0 && (
                      <div className="flex justify-center items-center gap-0.5 mt-0.5">
                        {goodEvents.slice(0, 4).map((evt, idx) => {
                          const isCurrentEvent = evt.type === eventType;
                          return (
                            <span
                              key={idx}
                              className={`text-[10px] ${isCurrentEvent ? 'scale-125' : 'opacity-70'}`}
                              title={evt.tamil}
                            >
                              {eventTypes.find(e => e.id === evt.type)?.icon || '⭐'}
                            </span>
                          );
                        })}
                      </div>
                    )}

                    {/* Highlight badge for selected event type */}
                    {!isSelected && hasSelectedEvent && (
                      <div className="absolute top-0.5 right-0.5 w-2 h-2 bg-green-500 rounded-full shadow-sm"></div>
                    )}
                  </button>
                );
              })}
            </div>
          </>
        )}

        {/* Legend */}
        <div className="flex justify-center gap-4 mt-4 text-xs">
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded bg-green-100 border border-green-300"></span>
            நல்ல நாள்
          </span>
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded bg-yellow-50 border border-yellow-200"></span>
            சாதாரணம்
          </span>
          <span className="flex items-center gap-1">
            <span className="w-3 h-3 rounded bg-red-100 border border-red-300"></span>
            தவிர்க்கவும்
          </span>
        </div>
      </div>

      {/* Time Slots */}
      {selectedDate && (
        <div className="mx-4 mt-4 bg-white rounded-2xl border border-orange-200 p-4 shadow-sm">
          <h2 className="text-sm font-medium text-gray-800 mb-3 flex items-center gap-2">
            <Clock className="w-4 h-4 text-orange-500" />
            {selectedDate} {monthNames[currentMonth.getMonth()]} - சிறந்த நேரங்கள்
          </h2>

          {loadingDetails ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="w-6 h-6 text-orange-500 animate-spin" />
            </div>
          ) : dayDetails ? (
            <>
              {/* Event Scores */}
              {dayDetails.good_for_events && dayDetails.good_for_events.length > 0 && (
                <div className="mb-4 p-3 bg-green-50 rounded-xl border border-green-200">
                  <p className="text-xs font-medium text-green-700 mb-2">✓ இன்று நல்ல நாள்:</p>
                  <div className="flex flex-wrap gap-2">
                    {dayDetails.good_for_events.map((evt, i) => (
                      <span key={i} className="inline-flex items-center gap-1 px-2 py-1 bg-white rounded-lg text-xs border border-green-200">
                        <span>{eventTypes.find(e => e.id === evt.type)?.icon}</span>
                        <span className="text-gray-700">{evt.tamil}</span>
                        <span className="text-green-600 font-medium">{evt.score}%</span>
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Sun & Moon Times */}
              <div className="mb-4 p-3 bg-blue-50 rounded-xl border border-blue-200">
                <p className="text-xs font-medium text-blue-700 mb-2">☀️ சூரியன் & சந்திரன்</p>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div>
                    <span className="text-gray-500">சூரியோதயம்: </span>
                    <span className="font-medium text-gray-800">{dayDetails.panchangam?.sun_times?.sunrise || dayDetails.panchangam?.sunrise || '-'}</span>
                  </div>
                  <div>
                    <span className="text-gray-500">சூரியஸ்தமம்: </span>
                    <span className="font-medium text-gray-800">{dayDetails.panchangam?.sun_times?.sunset || dayDetails.panchangam?.sunset || '-'}</span>
                  </div>
                  <div>
                    <span className="text-gray-500">சந்திரோதயம்: </span>
                    <span className="font-medium text-gray-800">{dayDetails.panchangam?.moon_times?.moonrise || '-'}</span>
                  </div>
                  <div>
                    <span className="text-gray-500">சந்திராஸ்தமனம்: </span>
                    <span className="font-medium text-gray-800">{dayDetails.panchangam?.moon_times?.moonset || '-'}</span>
                  </div>
                </div>
              </div>

              {/* Panchangam Summary */}
              <div className="mb-4 p-3 bg-orange-50 rounded-xl">
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div>
                    <span className="text-gray-500">திதி: </span>
                    <span className="font-medium text-gray-800">{dayDetails.panchangam?.tithi?.tamil || '-'}</span>
                  </div>
                  <div>
                    <span className="text-gray-500">நட்சத்திரம்: </span>
                    <span className="font-medium text-gray-800">{dayDetails.panchangam?.nakshatra?.tamil || '-'}</span>
                  </div>
                  <div>
                    <span className="text-gray-500">யோகம்: </span>
                    <span className="font-medium text-gray-800">{dayDetails.panchangam?.yoga?.tamil || dayDetails.panchangam?.yoga?.name || '-'}</span>
                  </div>
                  <div>
                    <span className="text-gray-500">கிழமை: </span>
                    <span className="font-medium text-gray-800">{dayDetails.panchangam?.vaaram || '-'}</span>
                  </div>
                </div>
              </div>

              {/* Auspicious Times */}
              {dayDetails.panchangam?.auspicious && (
                <div className="mb-4 p-3 bg-green-50 rounded-xl border border-green-200">
                  <p className="text-xs font-medium text-green-700 mb-2">🌟 சுபமான நேரம்</p>
                  <div className="space-y-1 text-xs">
                    {dayDetails.panchangam.auspicious.abhijit && (
                      <div className="flex justify-between">
                        <span className="text-gray-600">அபிஜித் முகூர்த்தம்:</span>
                        <span className="font-medium text-green-700">
                          {dayDetails.panchangam.auspicious.abhijit.start} - {dayDetails.panchangam.auspicious.abhijit.end}
                        </span>
                      </div>
                    )}
                    {dayDetails.panchangam.auspicious.amrit_kalam && (
                      <div className="flex justify-between">
                        <span className="text-gray-600">அமிர்த காலம்:</span>
                        <span className="font-medium text-green-700">
                          {dayDetails.panchangam.auspicious.amrit_kalam.start} - {dayDetails.panchangam.auspicious.amrit_kalam.end}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Inauspicious Times */}
              {dayDetails.panchangam?.inauspicious && (
                <div className="mb-4 p-3 bg-red-50 rounded-xl border border-red-200">
                  <p className="text-xs font-medium text-red-700 mb-2">⚠️ தவிர்க்க வேண்டிய நேரம்</p>
                  <div className="space-y-1 text-xs">
                    {dayDetails.panchangam.inauspicious.rahu_kalam && (
                      <div className="flex justify-between">
                        <span className="text-gray-600">ராகு காலம்:</span>
                        <span className="font-medium text-red-700">
                          {dayDetails.panchangam.inauspicious.rahu_kalam.start} - {dayDetails.panchangam.inauspicious.rahu_kalam.end}
                        </span>
                      </div>
                    )}
                    {dayDetails.panchangam.inauspicious.yamagandam && (
                      <div className="flex justify-between">
                        <span className="text-gray-600">யமகண்டம்:</span>
                        <span className="font-medium text-red-700">
                          {dayDetails.panchangam.inauspicious.yamagandam.start} - {dayDetails.panchangam.inauspicious.yamagandam.end}
                        </span>
                      </div>
                    )}
                    {dayDetails.panchangam.inauspicious.kuligai && (
                      <div className="flex justify-between">
                        <span className="text-gray-600">குளிகை:</span>
                        <span className="font-medium text-orange-700">
                          {dayDetails.panchangam.inauspicious.kuligai.start} - {dayDetails.panchangam.inauspicious.kuligai.end}
                        </span>
                      </div>
                    )}
                    {dayDetails.panchangam.inauspicious.durmuhurtham?.map((dm, i) => (
                      <div key={i} className="flex justify-between">
                        <span className="text-gray-600">துர்முகூர்த்தம் {i + 1}:</span>
                        <span className="font-medium text-orange-700">{dm.start} - {dm.end}</span>
                      </div>
                    ))}
                    {dayDetails.panchangam.inauspicious.thyajyam?.map((th, i) => (
                      <div key={i} className="flex justify-between">
                        <span className="text-gray-600">தியாஜ்யம்:</span>
                        <span className="font-medium text-orange-700">{th.start} - {th.end}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Time Slots */}
              <div className="space-y-2">
                {dayDetails.time_slots?.map((slot, i) => (
                  <div
                    key={i}
                    className={`p-3 rounded-xl border flex items-center justify-between ${
                      slot.type === 'excellent' ? 'bg-green-50 border-green-200' :
                      slot.type === 'good' ? 'bg-blue-50 border-blue-200' :
                      slot.type === 'avoid' ? 'bg-red-50 border-red-200' :
                      slot.type === 'caution' ? 'bg-orange-50 border-orange-200' :
                      'bg-gray-50 border-gray-200'
                    }`}
                  >
                    <div>
                      <p className="font-medium text-gray-800 text-sm">{slot.time}</p>
                      <p className={`text-xs ${
                        slot.type === 'excellent' ? 'text-green-600' :
                        slot.type === 'good' ? 'text-blue-600' :
                        slot.type === 'avoid' ? 'text-red-600' :
                        slot.type === 'caution' ? 'text-orange-600' :
                        'text-gray-600'
                      }`}>{slot.label}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      {slot.type !== 'avoid' && slot.type !== 'caution' && (
                        <span className={`text-lg font-bold ${
                          slot.type === 'excellent' ? 'text-green-600' :
                          slot.type === 'good' ? 'text-blue-600' :
                          'text-gray-600'
                        }`}>{slot.score}%</span>
                      )}
                      {slot.type === 'excellent' && <CheckCircle className="w-5 h-5 text-green-500" />}
                      {slot.type === 'avoid' && <AlertCircle className="w-5 h-5 text-red-500" />}
                      {slot.type === 'caution' && <AlertCircle className="w-5 h-5 text-orange-500" />}
                    </div>
                  </div>
                ))}
              </div>

              {/* AI Recommendation */}
              {dayDetails.recommendation && (
                <div className="mt-4 p-3 bg-gradient-to-r from-orange-50 to-yellow-50 rounded-xl border border-orange-200">
                  <div className="flex items-start gap-2">
                    <Sparkles className="w-4 h-4 text-orange-500 mt-0.5" />
                    <div>
                      <p className="text-sm font-medium text-orange-700">AI பரிந்துரை</p>
                      <p className="text-xs text-gray-600 mt-1">
                        {dayDetails.recommendation}
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="text-center py-6 text-gray-500 text-sm">
              தரவு கிடைக்கவில்லை
            </div>
          )}
        </div>
      )}

      {/* Select Date Prompt */}
      {!selectedDate && (
        <div className="mx-4 mt-4 bg-orange-50 rounded-2xl border border-orange-200 p-6 text-center">
          <Calendar className="w-12 h-12 text-orange-400 mx-auto mb-3" />
          <p className="text-gray-600">நாளை தேர்வு செய்யவும்</p>
          <p className="text-sm text-gray-500 mt-1">சிறந்த நேரங்களை பார்க்க</p>
        </div>
      )}
    </div>
  );
}
