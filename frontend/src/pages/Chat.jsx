import { useState, useEffect, useRef } from 'react';
import { Mic, MicOff, Send, Sparkles, Clock, Calendar, Heart, Briefcase, Star, ChevronRight, Volume2, Loader2 } from 'lucide-react';
import { chatAPI, panchangamAPI } from '../services/api';

const quickQuestions = [
  { icon: Clock, text: 'இன்று நல்ல நேரம் எப்போது?', category: 'time' },
  { icon: Calendar, text: 'இந்த வாரம் எப்படி இருக்கும்?', category: 'prediction' },
  { icon: Heart, text: 'என் காதல் வாழ்க்கை எப்படி?', category: 'love' },
  { icon: Briefcase, text: 'தொழில் முன்னேற்றம் உண்டா?', category: 'career' },
  { icon: Star, text: 'இன்றைய ராசிபலன்', category: 'horoscope' },
];

// Initial welcome message
const welcomeMessage = {
  type: 'ai',
  text: 'வணக்கம்! 🙏 நான் உங்கள் ஜோதிட AI உதவியாளர். தமிழில் உங்கள் கேள்விகளை கேளுங்கள்.',
  time: new Date().toLocaleTimeString('ta-IN', { hour: '2-digit', minute: '2-digit' }),
  insight: 'இன்றைய நாள் பற்றி அறிய "இன்று நல்ல நேரம்?" என்று கேளுங்கள்.'
};

export default function Chat() {
  const [messages, setMessages] = useState([welcomeMessage]);
  const [inputText, setInputText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [userProfile, setUserProfile] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Load user profile from localStorage
  useEffect(() => {
    const profile = localStorage.getItem('userProfile');
    if (profile) {
      setUserProfile(JSON.parse(profile));
    }
  }, []);

  const handleVoiceToggle = () => {
    setIsListening(!isListening);
    if (!isListening) {
      // Voice recognition placeholder
      setTimeout(() => {
        setInputText('நாளை திருமணத்துக்கு நல்ல நேரம்...');
        setIsListening(false);
      }, 2000);
    }
  };

  const handleSend = async () => {
    if (!inputText.trim()) return;

    const userMessage = {
      type: 'user',
      text: inputText,
      time: new Date().toLocaleTimeString('ta-IN', { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMessage]);
    const messageText = inputText;
    setInputText('');
    setIsTyping(true);

    try {
      // Call the backend AI chat API
      const response = await chatAPI.sendMessage(messageText, userProfile);

      setIsTyping(false);
      setMessages(prev => [...prev, {
        type: 'ai',
        text: response.message,
        time: new Date().toLocaleTimeString('ta-IN', { hour: '2-digit', minute: '2-digit' }),
        data: response.data,
        insight: response.insight,
        action: response.action
      }]);
    } catch (error) {
      console.error('Chat error:', error);
      setIsTyping(false);

      // Fallback: Try to get panchangam data for time-related questions
      if (messageText.includes('நேரம்') || messageText.includes('time') || messageText.includes('இன்று')) {
        try {
          const panchangam = await panchangamAPI.getToday();
          setMessages(prev => [...prev, {
            type: 'ai',
            text: `இன்றைய பஞ்சாங்கம்: ${panchangam.tamil_date}`,
            time: new Date().toLocaleTimeString('ta-IN', { hour: '2-digit', minute: '2-digit' }),
            data: {
              type: 'time_slots',
              slots: panchangam.nalla_neram?.map((slot, i) => ({
                start: slot.start,
                end: slot.end,
                quality: 85 - (i * 10),
                label: i === 0 ? 'சிறந்த நேரம்' : 'நல்ல நேரம்'
              })) || [],
              warning: panchangam.rahu_kalam ? {
                start: panchangam.rahu_kalam.start,
                end: panchangam.rahu_kalam.end,
                label: 'ராகு காலம் - தவிர்க்கவும்'
              } : null
            },
            insight: `நட்சத்திரம்: ${panchangam.nakshatra?.tamil || '-'}, திதி: ${panchangam.tithi?.tamil || '-'}`
          }]);
        } catch {
          setMessages(prev => [...prev, {
            type: 'ai',
            text: 'மன்னிக்கவும், தற்போது சேவையில் சிக்கல். மீண்டும் முயற்சிக்கவும்.',
            time: new Date().toLocaleTimeString('ta-IN', { hour: '2-digit', minute: '2-digit' }),
            insight: 'இணைப்பை சரிபார்க்கவும்.'
          }]);
        }
      } else {
        setMessages(prev => [...prev, {
          type: 'ai',
          text: 'மன்னிக்கவும், தற்போது சேவையில் சிக்கல். மீண்டும் முயற்சிக்கவும்.',
          time: new Date().toLocaleTimeString('ta-IN', { hour: '2-digit', minute: '2-digit' }),
          insight: 'இணைப்பை சரிபார்க்கவும்.'
        }]);
      }
    }
  };

  const handleQuickQuestion = (question) => {
    setInputText(question.text);
  };

  const renderMessageData = (data) => {
    if (!data) return null;

    if (data.type === 'time_slots') {
      return (
        <div className="mt-3 space-y-2">
          {data.slots.map((slot, i) => (
            <div key={i} className="flex items-center gap-3 p-3 bg-green-50 rounded-xl border border-green-200">
              <div className="text-center">
                <div className="text-lg font-bold text-green-700">{slot.start}</div>
                <div className="text-xs text-gray-500">முதல்</div>
                <div className="text-lg font-bold text-green-700">{slot.end}</div>
              </div>
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <span className="text-green-700 font-medium text-sm">{slot.label}</span>
                  <span className="text-2xl font-bold text-green-600">{slot.quality}%</span>
                </div>
                <div className="w-full bg-green-100 rounded-full h-2 mt-2">
                  <div className="bg-green-500 h-2 rounded-full" style={{ width: `${slot.quality}%` }}></div>
                </div>
              </div>
            </div>
          ))}
          {data.warning && (
            <div className="flex items-center gap-3 p-3 bg-red-50 rounded-xl border border-red-200">
              <div className="text-center">
                <div className="text-sm font-bold text-red-700">{data.warning.start} - {data.warning.end}</div>
              </div>
              <span className="text-red-700 text-sm">⚠️ {data.warning.label}</span>
            </div>
          )}
        </div>
      );
    }

    if (data.type === 'recommendation') {
      return (
        <div className="mt-3">
          <div className="flex items-center justify-between p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl border border-green-200 mb-3">
            <span className="text-green-700 font-medium">பரிந்துரை மதிப்பெண்</span>
            <span className="text-4xl font-bold text-green-600">{data.score}%</span>
          </div>
          {data.factors && data.factors.length > 0 && (
            <div className="grid grid-cols-3 gap-2">
              {data.factors.map((f, i) => (
                <div key={i} className="p-2 bg-gray-50 rounded-lg text-center border border-gray-200">
                  <div className={`text-lg font-bold ${f.positive ? 'text-green-600' : 'text-red-600'}`}>{f.value}%</div>
                  <div className="text-xs text-gray-600">{f.name}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      );
    }

    if (data.type === 'horoscope') {
      return (
        <div className="mt-3">
          <div className="flex items-center justify-between p-4 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-xl border border-purple-200 mb-3">
            <span className="text-purple-700 font-medium">இன்றைய மதிப்பெண்</span>
            <span className="text-4xl font-bold text-purple-600">{data.overall_score}%</span>
          </div>
          {data.areas && (
            <div className="grid grid-cols-2 gap-2">
              {Object.entries(data.areas).map(([area, score], i) => (
                <div key={i} className="p-3 bg-gray-50 rounded-lg border border-gray-200">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">{area}</span>
                    <span className={`text-lg font-bold ${score >= 70 ? 'text-green-600' : score >= 50 ? 'text-yellow-600' : 'text-red-600'}`}>
                      {score}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-1.5 mt-1">
                    <div
                      className={`h-1.5 rounded-full ${score >= 70 ? 'bg-green-500' : score >= 50 ? 'bg-yellow-500' : 'bg-red-500'}`}
                      style={{ width: `${score}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      );
    }

    if (data.type === 'weekly_forecast') {
      return (
        <div className="mt-3">
          <div className="flex items-center justify-between p-3 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-200 mb-3">
            <div>
              <span className="text-blue-700 text-sm">வார சராசரி</span>
              <p className="text-2xl font-bold text-blue-600">{data.average_score}%</p>
            </div>
            <div className="text-right text-xs">
              <p className="text-green-600">சிறந்த: {data.best_day?.day}</p>
              <p className="text-red-600">கவனம்: {data.worst_day?.day}</p>
            </div>
          </div>
          {data.days && (
            <div className="flex gap-1 overflow-x-auto pb-2">
              {data.days.map((day, i) => (
                <div
                  key={i}
                  className={`flex-shrink-0 w-14 p-2 rounded-lg text-center border ${
                    day.is_good ? 'bg-green-50 border-green-200' : 'bg-gray-50 border-gray-200'
                  }`}
                >
                  <p className="text-xs text-gray-500">{day.day}</p>
                  <p className={`text-sm font-bold ${day.is_good ? 'text-green-600' : 'text-gray-600'}`}>
                    {day.score}%
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      );
    }

    if (data.type === 'monthly_forecast') {
      return (
        <div className="mt-3">
          <div className="flex items-center justify-between p-3 bg-gradient-to-r from-orange-50 to-amber-50 rounded-xl border border-orange-200 mb-3">
            <div>
              <span className="text-orange-700 text-sm">{data.month_name} மாதம்</span>
              <p className="text-2xl font-bold text-orange-600">{data.average_score}%</p>
            </div>
            <div className="text-right text-xs">
              <p className="text-green-600">நல்ல நாட்கள்: {data.good_days_count}</p>
              <p className="text-red-600">கவனம்: {data.caution_days_count}</p>
            </div>
          </div>
          {data.best_periods?.length > 0 && (
            <div className="text-xs text-gray-600 bg-green-50 p-2 rounded-lg">
              <span className="font-medium text-green-700">சிறந்த காலம்: </span>
              {data.best_periods.slice(0, 2).map((p, i) => (
                <span key={i}>{p.start}-{p.end} ({p.score}%){i < 1 && data.best_periods.length > 1 ? ', ' : ''}</span>
              ))}
            </div>
          )}
        </div>
      );
    }

    if (data.type === 'yearly_forecast') {
      return (
        <div className="mt-3">
          <div className="flex items-center justify-between p-3 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-xl border border-purple-200 mb-3">
            <div>
              <span className="text-purple-700 text-sm">{data.year} வருடம்</span>
              <p className="text-2xl font-bold text-purple-600">{data.average_score}%</p>
            </div>
            <div className="text-right text-xs">
              <p className="text-green-600">சிறந்த: {data.best_months?.map(m => m.month).join(', ')}</p>
            </div>
          </div>
          {data.months && (
            <div className="grid grid-cols-4 gap-1">
              {data.months.map((month, i) => (
                <div
                  key={i}
                  className={`p-1.5 rounded text-center ${
                    month.type === 'excellent' ? 'bg-green-100 border border-green-200' :
                    month.type === 'good' ? 'bg-orange-100 border border-orange-200' :
                    'bg-gray-100 border border-gray-200'
                  }`}
                >
                  <p className="text-[10px] text-gray-500">{month.name}</p>
                  <p className={`text-xs font-bold ${
                    month.type === 'excellent' ? 'text-green-700' :
                    month.type === 'good' ? 'text-orange-700' : 'text-gray-600'
                  }`}>{month.score}%</p>
                </div>
              ))}
            </div>
          )}
        </div>
      );
    }

    if (data.type === 'three_year_forecast') {
      return (
        <div className="mt-3 space-y-3">
          {data.years?.map((yearData, yi) => (
            <div key={yi} className="border border-orange-100 rounded-xl p-2">
              <p className="text-sm font-medium text-orange-700 mb-2">{yearData.year}</p>
              <div className="flex gap-1 overflow-x-auto pb-1">
                {yearData.months?.map((month, mi) => (
                  <div
                    key={mi}
                    className={`flex-shrink-0 w-10 p-1 rounded text-center ${
                      month.type === 'excellent' ? 'bg-green-100' :
                      month.type === 'good' ? 'bg-orange-100' :
                      month.type === 'caution' ? 'bg-red-100' : 'bg-gray-100'
                    }`}
                  >
                    <p className="text-[8px] text-gray-500">{month.name?.substring(0, 2)}</p>
                    <p className={`text-[10px] font-bold ${
                      month.type === 'excellent' ? 'text-green-700' :
                      month.type === 'good' ? 'text-orange-700' :
                      month.type === 'caution' ? 'text-red-700' : 'text-gray-600'
                    }`}>{month.score}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      );
    }

    return null;
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-orange-50 flex flex-col">
      {/* Decorative Header */}
      <div className="bg-gradient-to-r from-orange-500 via-yellow-500 to-orange-500 h-1" />

      {/* Header */}
      <div className="p-4 border-b border-orange-100 bg-white">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-full bg-gradient-to-r from-orange-400 to-red-400 flex items-center justify-center shadow-lg">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-lg text-gray-800">ஜோதிட AI</h1>
            <p className="text-green-600 text-xs flex items-center gap-1">
              <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
              ஆன்லைன் • தமிழில் பேசுங்கள்
            </p>
          </div>
        </div>
      </div>

      {/* Quick Questions */}
      <div className="p-3 border-b border-orange-100 bg-white overflow-x-auto">
        <div className="flex gap-2">
          {quickQuestions.map((q, i) => (
            <button
              key={i}
              onClick={() => handleQuickQuestion(q)}
              className="flex items-center gap-2 px-3 py-2 bg-orange-50 rounded-full border border-orange-200 whitespace-nowrap text-sm hover:border-orange-400 transition-all text-gray-700"
            >
              <q.icon className="w-4 h-4 text-orange-500" />
              <span>{q.text}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 pb-32">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] ${msg.type === 'user' ? 'order-1' : 'order-2'}`}>
              <div className={`p-4 rounded-2xl ${
                msg.type === 'user'
                  ? 'bg-orange-500 text-white rounded-br-sm shadow-lg shadow-orange-500/20'
                  : 'bg-white border border-orange-200 rounded-bl-sm shadow-sm'
              }`}>
                <p className={`text-sm leading-relaxed ${msg.type === 'user' ? 'text-white' : 'text-gray-700'}`}>{msg.text}</p>

                {msg.data && renderMessageData(msg.data)}

                {msg.insight && (
                  <div className="mt-3 p-3 bg-orange-50 rounded-xl border border-orange-200">
                    <div className="flex items-start gap-2">
                      <Sparkles className="w-4 h-4 text-orange-500 mt-0.5 flex-shrink-0" />
                      <p className="text-orange-700 text-xs leading-relaxed">{msg.insight}</p>
                    </div>
                  </div>
                )}

                {msg.action && (
                  <button className="mt-3 w-full p-2 bg-orange-100 rounded-lg text-orange-700 text-sm flex items-center justify-center gap-2 hover:bg-orange-200 transition-all border border-orange-200">
                    {msg.action.text}
                    <ChevronRight className="w-4 h-4" />
                  </button>
                )}
              </div>

              <div className={`flex items-center gap-2 mt-1 ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                <span className="text-xs text-gray-400">{msg.time}</span>
                {msg.type === 'ai' && (
                  <button
                    onClick={() => setIsSpeaking(!isSpeaking)}
                    className="p-1 hover:bg-gray-100 rounded"
                  >
                    <Volume2 className={`w-3 h-3 ${isSpeaking ? 'text-orange-500' : 'text-gray-400'}`} />
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}

        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-white border border-orange-200 rounded-2xl rounded-bl-sm p-4 shadow-sm">
              <div className="flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin text-orange-500" />
                <span className="text-sm text-gray-500">AI சிந்திக்கிறது...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="fixed bottom-16 left-0 right-0 p-4 border-t border-orange-100 bg-white">
        <div className="flex items-center gap-3">
          <button
            onClick={handleVoiceToggle}
            className={`w-12 h-12 rounded-full flex items-center justify-center transition-all ${
              isListening
                ? 'bg-red-500 animate-pulse text-white'
                : 'bg-gray-100 hover:bg-gray-200 text-gray-600'
            }`}
          >
            {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
          </button>

          <div className="flex-1 relative">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="தமிழில் கேளுங்கள்..."
              className="w-full bg-gray-50 border border-gray-200 rounded-full px-4 py-3 pr-12 text-sm focus:outline-none focus:border-orange-400 focus:ring-2 focus:ring-orange-100"
            />
            {isListening && (
              <div className="absolute right-14 top-1/2 -translate-y-1/2 flex gap-0.5">
                {[...Array(4)].map((_, i) => (
                  <div
                    key={i}
                    className="w-1 bg-red-500 rounded-full animate-pulse"
                    style={{
                      height: `${10 + Math.random() * 15}px`,
                      animationDelay: `${i * 0.1}s`
                    }}
                  ></div>
                ))}
              </div>
            )}
          </div>

          <button
            onClick={handleSend}
            disabled={!inputText.trim()}
            className="w-12 h-12 rounded-full bg-gradient-to-r from-orange-500 to-red-500 flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg hover:shadow-orange-500/25 transition-all text-white"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
